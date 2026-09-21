"""
Run orchestration service.

This module is the glue between the workbench HTTP layer and the four
phreeqc-auto skill scripts:

    generate_input.generate_single_simulation
    run_phreeqc.run_simulation
    parse_output.parse_selected_output + helpers
    visualize.plot_* (optional best-effort)

It runs the full pipeline in a background thread and streams events
into the storage event log so SSE clients can observe progress.
"""

from __future__ import annotations

import os
import re
import sys
import threading
import time
import traceback
from typing import Any

# Re-import path setup from app.py contract
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_THIS_DIR)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_BACKEND_DIR))
_SKILL_SCRIPTS = os.path.join(
    _PROJECT_ROOT, ".claude", "skills", "phreeqc-auto", "scripts"
)
if _SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, _SKILL_SCRIPTS)

# Storage is importable via package init
from services import storage  # noqa: E402
from services.process_registry import registry  # noqa: E402
from services import phreeqc_locator  # noqa: E402

# Skill scripts (imported lazily inside functions to keep cold-start fast)
def _import_generate():
    import generate_input  # type: ignore
    return generate_input


def _import_run_phreeqc():
    import run_phreeqc  # type: ignore
    return run_phreeqc


def _import_parse():
    import parse_output  # type: ignore
    return parse_output


def _import_visualize():
    try:
        import visualize  # type: ignore
        return visualize
    except Exception:  # noqa: BLE001
        return None


# Re-exports for direct callers
def find_phreeqc_exe() -> str:
    return phreeqc_locator.find_phreeqc_exe()


def find_database(name: str = "phreeqc.dat") -> str:
    return phreeqc_locator.find_database(name)


# ---------------------------------------------------------------------------
# Event helpers
# ---------------------------------------------------------------------------

def _emit(run_id: str, kind: str, message: str, **extra: Any) -> None:
    event = {
        "kind": kind,
        "message": message,
        "ts": time.time(),
        **extra,
    }
    storage.append_event(run_id, event)
    storage.append_log(run_id, f"[{kind}] {message}")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def _parse_into(run_id: str, output_path: str, selected_path: str | None) -> dict:
    """Parse an existing PHREEQC output into results.json.

    Returns the parsed dict (or ``{}`` on failure).  Shared by the
    normal pipeline and the external-run importer.
    """
    parsed: dict = {}
    try:
        parse_output = _import_parse()
    except Exception:
        return parsed
    if selected_path and os.path.isfile(selected_path):
        try:
            parsed = parse_output.parse_selected_output(selected_path)
        except Exception:
            parsed = {}
    if os.path.isfile(output_path):
        try:
            with open(output_path, encoding="utf-8", errors="replace") as f:
                qpo_text = f.read()
            try:
                si = parse_output.extract_saturation_indices(qpo_text, last=True)
                species = parse_output.extract_species_distribution(qpo_text, last=True)
                elements = parse_output.extract_element_molalities(qpo_text, last=True)
                ionic = parse_output.extract_ionic_strength(qpo_text)
                parsed["saturation_indices"] = si
                parsed["species_distribution"] = species
                parsed["element_molalities"] = elements
                parsed["ionic_strength"] = ionic
            except Exception:
                pass
        except OSError:
            pass
    import json as _json
    try:
        storage.write_artifact(
            run_id, "results.json",
            _json.dumps(parsed, ensure_ascii=False, indent=2, default=str),
        )
        storage.set_result_summary(run_id, {
            "row_count": parsed.get("row_count", 0),
            "columns": parsed.get("columns", []),
            "has_si": bool(parsed.get("saturation_indices")),
            "has_species": bool(parsed.get("species_distribution")),
        })
    except OSError:
        pass
    return parsed


def execute_run(run_id: str) -> None:
    """Execute the full generate -> run -> parse -> visualize pipeline.

    Intended to be invoked in a background thread. All exceptions are
    captured and surfaced via events; this function never raises.
    """
    try:
        run = storage.get_run(run_id)
        if run is None:
            _emit(run_id, "error", f"Run not found: {run_id}")
            return

        params = run.get("params", {})
        storage.set_status(run_id, "running")
        _emit(run_id, "start", f"Run {run_id} started")

        run_dir = os.path.join(storage.workspace_root(), run_id)
        os.makedirs(run_dir, exist_ok=True)
        os.makedirs(os.path.join(run_dir, "charts"), exist_ok=True)

        # ----- Step 1: generate input -----
        try:
            _emit(run_id, "step", "Step 1/4: generating PHREEQC input file")
            generate_input = _import_generate()
            input_text = generate_input.generate_single_simulation(
                params, output_file="selected_output.txt"
            )
            storage.write_artifact(run_id, "input.pqi", input_text)
            _emit(
                run_id, "input_generated",
                f"input.pqi generated ({len(input_text)} chars)",
                size=len(input_text),
            )
        except Exception as exc:  # noqa: BLE001
            _emit(
                run_id, "error",
                f"Failed to generate input: {exc}",
                traceback=traceback.format_exc(),
            )
            storage.set_status(run_id, "failed")
            return

        # ----- Step 2: run PHREEQC -----
        try:
            _emit(run_id, "step", "Step 2/4: running PHREEQC subprocess")
            exe = phreeqc_locator.find_phreeqc_exe()
            database = phreeqc_locator.find_database()
            input_path = os.path.join(run_dir, "input.pqi")
            output_path = os.path.join(run_dir, "output.qpo")
            _emit(
                run_id, "info",
                f"PHREEQC exe: {exe}",
                executable=exe,
            )
            _emit(
                run_id, "info",
                f"PHREEQC database: {database}",
                database=database,
            )

            # Use Popen (not subprocess.run) so we can register and
            # terminate the child via the process registry.  The
            # CREATE_NEW_PROCESS_GROUP flag on Windows allows us to send
            # CTRL_BREAK_EVENT to interrupt long-running simulations.
            import subprocess as _sp
            if os.name == "nt":
                creationflags = _sp.CREATE_NEW_PROCESS_GROUP
            else:
                creationflags = 0
            proc = _sp.Popen(
                [exe, input_path, output_path, database],
                stdout=_sp.PIPE, stderr=_sp.PIPE,
                text=True, encoding="utf-8", errors="replace",
                cwd=run_dir,
                creationflags=creationflags,
            )
            registry.register(run_id, proc)
            try:
                try:
                    stdout, stderr = proc.communicate(timeout=300)
                except _sp.TimeoutExpired:
                    registry.abort(run_id, grace_seconds=2.0)
                    try:
                        stdout, stderr = proc.communicate(timeout=5)
                    except Exception:  # noqa: BLE001
                        stdout, stderr = "", ""
                    _emit(
                        run_id, "error",
                        "PHREEQC simulation timed out (300s) and was terminated",
                    )
                    storage.set_status(run_id, "failed")
                    return
            finally:
                registry.unregister(run_id)

            # Stream stdout/stderr to the event log (last 100 lines each)
            for line in (stdout or "").splitlines()[-100:]:
                _emit(run_id, "stdout", line)
            for line in (stderr or "").splitlines()[-100:]:
                _emit(run_id, "stderr", line)
            if proc.returncode != 0:
                _emit(
                    run_id, "error",
                    f"PHREEQC failed: exit code {proc.returncode}",
                )
                # Distinguish user abort from generic failure: the
                # registry only sets status when the run thread is the
                # one calling abort().  If the run was aborted via the
                # API, the storage status was already set; otherwise it
                # is a normal failure.
                if storage.get_run(run_id).get("status") != "aborted":
                    storage.set_status(run_id, "failed")
                return
            # PHREEQC normally writes its complete report to output.qpo.  A
            # few Windows builds instead emit it on stderr while leaving the
            # requested output file empty. Preserve that report so the output
            # tab remains useful and downstream parsing has a real artifact.
            try:
                output_is_empty = (not os.path.isfile(output_path) or
                                   os.path.getsize(output_path) == 0)
                fallback_report = max((stderr or "", stdout or ""), key=len)
                if output_is_empty and fallback_report:
                    storage.write_artifact(run_id, "output.qpo", fallback_report)
                    _emit(
                        run_id,
                        "warn",
                        "output.qpo was empty; saved PHREEQC process output as fallback",
                    )
            except OSError as exc:
                _emit(run_id, "warn", f"Could not create output fallback: {exc}")
            _emit(
                run_id, "simulation_done",
                "PHREEQC simulation completed",
                exit_code=proc.returncode,
            )
        except Exception as exc:  # noqa: BLE001
            _emit(
                run_id, "error",
                f"Failed to run PHREEQC: {exc}",
                traceback=traceback.format_exc(),
            )
            storage.set_status(run_id, "failed")
            return

        # ----- Step 3: parse output -----
        try:
            _emit(run_id, "step", "Step 3/4: parsing PHREEQC output")
            run_dir = os.path.join(storage.workspace_root(), run_id)
            selected_path = os.path.join(run_dir, "selected_output.txt")
            output_path = os.path.join(run_dir, "output.qpo")
            parsed = _parse_into(run_id, output_path, selected_path)
            _emit(
                run_id, "parse_done",
                f"Parsed {parsed.get('row_count', 0)} data rows",
            )
        except Exception as exc:  # noqa: BLE001
            _emit(
                run_id, "warn",
                f"Parse step failed: {exc}",
                traceback=traceback.format_exc(),
            )
            # Non-fatal: results.json is missing but the simulation succeeded.

        # ----- Step 4: visualize (best-effort) -----
        try:
            _emit(run_id, "step", "Step 4/4: generating visualizations")
            visualize = _import_visualize()
            chart_paths: list[str] = []
            if visualize is not None:
                si = parsed.get("saturation_indices") or []
                # SI bar chart
                if si:
                    try:
                        rel = "charts/saturation_indices.png"
                        png_path = os.path.join(run_dir, rel)
                        os.makedirs(os.path.dirname(png_path), exist_ok=True)
                        visualize.plot_saturation_indices(
                            si, title="Saturation Indices",
                            filepath=png_path,
                        )
                        chart_paths.append(rel)
                    except Exception as exc:  # noqa: BLE001
                        _emit(run_id, "warn", f"SI chart failed: {exc}")
                # Sweep / multi-row chart
                columns = parsed.get("columns") or []
                data = parsed.get("data") or []
                if data and columns:
                    si_cols = [c for c in columns if c.startswith("si_")][:6]
                    if si_cols:
                        try:
                            rel = "charts/si_evolution.png"
                            x_col = columns[0]
                            png_path = os.path.join(run_dir, rel)
                            os.makedirs(os.path.dirname(png_path), exist_ok=True)
                            visualize.plot_selected_output_sweep(
                                {"columns": columns, "data": data},
                                x_column=x_col, y_columns=si_cols,
                                title="SI Evolution",
                                filepath=png_path,
                            )
                            chart_paths.append(rel)
                        except Exception as exc:  # noqa: BLE001
                            _emit(run_id, "warn", f"Sweep chart failed: {exc}")
            _emit(
                run_id, "visualize_done",
                f"Generated {len(chart_paths)} chart(s)",
                charts=chart_paths,
            )
        except Exception as exc:  # noqa: BLE001
            _emit(run_id, "warn", f"Visualization failed: {exc}")

        storage.set_status(run_id, "succeeded")
        _emit(run_id, "success", f"Run {run_id} completed successfully")
    except Exception as exc:  # noqa: BLE001  (top-level safety net)
        try:
            _emit(
                run_id, "error",
                f"Pipeline crashed: {exc}",
                traceback=traceback.format_exc(),
            )
            storage.set_status(run_id, "failed")
        except Exception:  # noqa: BLE001
            pass
