"""
PHREEQC Auto Workbench - Backend HTTP Server.

A zero-dependency HTTP server built on Python standard library (http.server
+ asyncio + SSE) that wraps the existing phreeqc-auto skill scripts to
provide a JSON REST + Server-Sent Events API for the WebUI workbench.

Design notes
------------
- No third-party web framework is used (no FastAPI / Flask) so the
  workbench does not pollute the phreeqc-auto dependency graph.
- Long-running PHREEQC subprocesses are streamed to clients via SSE
  (text/event-stream) at ``/api/v1/runs/{id}/events``.
- File downloads are served directly from the workspace directory with
  strict path-traversal protection.
- All responses use a uniform envelope::

      {"ok": true,  "data": ...}
      {"ok": false, "error": {"code": "...", "message": "..."}}
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socketserver import ThreadingMixIn
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

# Make the skill scripts importable as a library
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_SCRIPTS = os.path.join(
    PROJECT_ROOT, ".claude", "skills", "phreeqc-auto", "scripts"
)
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)

# Make local workbench modules importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services import storage  # noqa: E402  (after sys.path manipulation)
from services import templates as tpl_service  # noqa: E402
from services import runner  # noqa: E402
from services import scenarios  # noqa: E402
from services import custom_templates  # noqa: E402
from services import phreeqc_locator as phreeqc_locator  # noqa: E402
from services.process_registry import registry  # noqa: E402
from services import importer as run_importer  # noqa: E402


API_PREFIX = "/api/v1"
# Static dir: prefer the workbench/frontend directory (single-page app
# with all assets), fall back to workbench/backend/static.
_FRONTEND_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend"))
_BACKEND_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
STATIC_DIR = _FRONTEND_DIR if os.path.isdir(_FRONTEND_DIR) else _BACKEND_STATIC
WORKBENCH_VERSION = "0.2.0"


class SingleInstanceHTTPServer(ThreadingHTTPServer):
    """Refuse a second Workbench on the same port.

    ``HTTPServer`` enables address reuse by default.  On Windows that can
    allow several workbench processes to listen on one port, so requests are
    routed unpredictably to stale instances.  A local workbench should have
    exactly one owner for its configured port.
    """

    allow_reuse_address = False
    allow_reuse_port = False


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------

def envelope_ok(data: Any = None, status: int = 200) -> tuple[int, bytes, str]:
    body = json.dumps({"ok": True, "data": data}, ensure_ascii=False).encode("utf-8")
    return status, body, "application/json; charset=utf-8"


def envelope_error(code: str, message: str, status: int = 400) -> tuple[int, bytes, str]:
    payload = {"ok": False, "error": {"code": code, "message": message}}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return status, body, "application/json; charset=utf-8"


# ---------------------------------------------------------------------------
# Error codes (machine-readable enum)
# ---------------------------------------------------------------------------

EC_PHREEQC_NOT_FOUND = "PHREEQC_NOT_FOUND"
EC_DATABASE_NOT_FOUND = "DATABASE_NOT_FOUND"
EC_INVALID_PARAMS = "INVALID_PARAMS"
EC_INVALID_PATH = "INVALID_PATH"
EC_RUN_NOT_FOUND = "RUN_NOT_FOUND"
EC_RUN_ALREADY_ACTIVE = "RUN_ALREADY_ACTIVE"
EC_RUN_NOT_ACTIVE = "RUN_NOT_ACTIVE"
EC_SIM_TIMEOUT = "SIM_TIMEOUT"
EC_INTERNAL = "INTERNAL_ERROR"


# ---------------------------------------------------------------------------
# Route dispatcher
# ---------------------------------------------------------------------------

# A route is (method, regex_pattern, handler)
# Patterns use {name} for path parameters and the handler receives
# (handler, path_params, query_params, body_dict) -> (status, body_bytes, content_type)

ROUTES: list[tuple[str, str, Callable]] = []


def route(method: str, pattern: str):
    def decorator(fn: Callable) -> Callable:
        ROUTES.append((method, pattern, fn))
        return fn
    return decorator


import re


def _match_route(method: str, path: str):
    """Find the first matching route. Returns (handler, params) or (None, None).

    Path parameters are converted to a regex automatically.  Use
    ``{name+}`` (note the trailing ``+``) to match a path segment that
    may contain ``/`` (e.g. ``{name+}`` matches ``charts/foo.png``).
    """
    for m, pattern, fn in ROUTES:
        if m != method:
            continue
        regex = "^"
        cursor = 0
        for match in re.finditer(r"\{(\w+)(\+?)\}", pattern):
            regex += re.escape(pattern[cursor:match.start()])
            if match.group(2) == "+":
                regex += r"(?P<" + match.group(1) + r">.+)"
            else:
                regex += r"(?P<" + match.group(1) + r">[^/]+)"
            cursor = match.end()
        regex += re.escape(pattern[cursor:]) + "$"
        match = re.match(regex, path)
        if match:
            return fn, match.groupdict()
    return None, None


# ---------------------------------------------------------------------------
# Route: System
# ---------------------------------------------------------------------------

@route("GET", "/api/v1/system/health")
def system_health(handler, params, query, body):
    phreeqc_ok = False
    phreeqc_exe = None
    phreeqc_error = None
    try:
        phreeqc_exe = phreeqc_locator.find_phreeqc_exe()
        phreeqc_ok = os.path.isfile(phreeqc_exe)
    except FileNotFoundError as exc:
        phreeqc_error = str(exc)
    except Exception as exc:  # noqa: BLE001
        phreeqc_error = str(exc)

    database_ok = False
    database_path = None
    database_error = None
    try:
        database_path = phreeqc_locator.find_database()
        database_ok = os.path.isfile(database_path)
    except FileNotFoundError as exc:
        database_error = str(exc)
    except Exception as exc:  # noqa: BLE001
        database_error = str(exc)

    return envelope_ok({
        "workbench_version": WORKBENCH_VERSION,
        "phreeqc": {
            "ok": phreeqc_ok,
            "executable": phreeqc_exe,
            "error": phreeqc_error,
        },
        "database": {
            "ok": database_ok,
            "path": database_path,
            "error": database_error,
        },
        "workspace_root": storage.workspace_root(),
    })


@route("POST", "/api/v1/system/shutdown")
def system_shutdown(handler, params, query, body):
    """Stop the workbench server.  Called by the front-end "Exit" button
    after the user confirms in a modal dialog.

    Before shutting down the listening socket we terminate any PHREEQC
    children that the runner spawned, so no orphan ``phreeqc.exe``
    processes are left behind.  We also stop the file watcher thread
    so it does not race with the shutdown.

    The handler does **not** call ``server.shutdown()`` itself.  Instead,
    it sets ``handler._shutdown_after_response = True`` and returns 200.
    The HTTP layer (in :meth:`WorkbenchHandler.do_POST`) detects this
    flag after the response is written and triggers the shutdown on a
    background thread, so the client can read the JSON body before the
    listening socket closes.
    """
    aborted = registry.abort_all(grace_seconds=2.0)
    if aborted:
        print(f"[workbench] aborting {len(aborted)} running run(s): {aborted}", flush=True)
    try:
        run_importer.stop()
    except Exception:  # noqa: BLE001
        pass
    print("[workbench] shutdown requested by client; stopping server…", flush=True)
    handler._shutdown_after_response = True
    return envelope_ok({"stopping": True, "aborted_runs": aborted})


# ---------------------------------------------------------------------------
# Route: External-run importer
# ---------------------------------------------------------------------------

@route("GET", "/api/v1/system/importer/status")
def importer_status(handler, params, query, body):
    return envelope_ok(run_importer.status())


@route("POST", "/api/v1/system/importer/configure")
def importer_configure(handler, params, query, body):
    """Replace the watch-dir list and start (or leave stopped) the
    background poller.

    Body: ``{"watch_dirs": ["C:/path/a", "C:/path/b"], "auto_start": true}``
    """
    if not isinstance(body, dict):
        return envelope_error(EC_INVALID_PARAMS, "Body must be a JSON object")
    raw = body.get("watch_dirs") or []
    if not isinstance(raw, list):
        return envelope_error(EC_INVALID_PARAMS, "'watch_dirs' must be a list of strings")
    dirs = run_importer.configure([str(x) for x in raw])
    auto_start = bool(body.get("auto_start", True))
    if auto_start and dirs:
        run_importer.start()
    elif not auto_start:
        run_importer.stop()
    return envelope_ok(run_importer.status())


@route("POST", "/api/v1/system/importer/start")
def importer_start(handler, params, query, body):
    if not run_importer.list_watch_dirs():
        return envelope_error(
            EC_INVALID_PARAMS,
            "No watch directories configured; call /configure first.",
        )
    run_importer.start()
    return envelope_ok(run_importer.status())


@route("POST", "/api/v1/system/importer/stop")
def importer_stop(handler, params, query, body):
    run_importer.stop()
    return envelope_ok(run_importer.status())


@route("POST", "/api/v1/system/importer/scan")
def importer_scan(handler, params, query, body):
    """Trigger an immediate scan (returns the newly-imported run ids)."""
    new_runs = run_importer.scan_once()
    return envelope_ok({"imported": new_runs, "status": run_importer.status()})


@route("GET", "/api/v1/system/phreeqc/candidates")
def list_phreeqc_candidates(handler, params, query, body):
    """Return discovered PHREEQC executables and databases."""
    exes = phreeqc_locator.discover_executables()
    primary = None
    try:
        primary = phreeqc_locator.find_phreeqc_exe()
    except FileNotFoundError:
        primary = None
    dbs = phreeqc_locator.discover_databases(primary)
    primary_db = None
    try:
        primary_db = phreeqc_locator.find_database()
    except FileNotFoundError:
        primary_db = None
    return envelope_ok({
        "settings": phreeqc_locator.get_settings(),
        "executables": exes,
        "databases": dbs,
        "active": {
            "executable": primary,
            "database": primary_db,
            "version": phreeqc_locator.detected_version(primary),
        },
    })


@route("POST", "/api/v1/system/phreeqc/test")
def test_phreeqc_path(handler, params, query, body):
    """Run a reachability test for a candidate path.

    Body: ``{"executable": "C:/.../phreeqc.exe"}`` -- the database
    argument is optional; if absent we use the upstream auto-discovery.
    """
    if not isinstance(body, dict):
        return envelope_error(EC_INVALID_PARAMS, "Body must be a JSON object")
    exe = (body.get("executable") or "").strip()
    if not exe:
        return envelope_error(EC_INVALID_PARAMS, "Field 'executable' is required")
    result = phreeqc_locator.test_executable(exe, body.get("database"))
    if body.get("database"):
        result["database"] = phreeqc_locator.test_database(body["database"])
    elif result.get("ok"):
        # If the probe used an implicit database, surface its test too.
        try:
            result["database"] = phreeqc_locator.test_database(
                phreeqc_locator.find_database()
            )
        except FileNotFoundError:
            result["database"] = {"ok": False, "error": "no database found"}
    return envelope_ok(result)


@route("POST", "/api/v1/system/phreeqc/auto-configure")
def auto_configure_phreeqc(handler, params, query, body):
    """Discover, test, and persist the first working PHREEQC setup."""
    databases = phreeqc_locator.discover_databases()
    valid_databases = [
        item["path"] for item in databases
        if item["exists"] and phreeqc_locator.test_database(item["path"]).get("ok")
    ]
    # Prefer PHREEQC's general-purpose default database.  Other databases
    # remain available for an explicit user selection in the settings panel.
    database = next(
        (path for path in valid_databases if os.path.basename(path).lower() == "phreeqc.dat"),
        valid_databases[0] if valid_databases else None,
    )
    if not database:
        return envelope_error(EC_INVALID_PATH, "No usable PHREEQC database was found")

    attempts: list[dict] = []
    for item in phreeqc_locator.discover_executables():
        if not item["exists"]:
            continue
        probe = phreeqc_locator.test_executable(item["path"], database)
        attempts.append({"path": item["path"], "ok": probe.get("ok"), "error": probe.get("error")})
        if probe.get("ok"):
            settings = phreeqc_locator.update_settings({
                "phreeqc_exe": item["path"],
                "phreeqc_database": database,
                "phreeqc_config_source": "auto",
            })
            probe["database"] = phreeqc_locator.test_database(database)
            return envelope_ok({"settings": settings, "test": probe, "attempts": attempts})
    return envelope_error(EC_INVALID_PATH, "No discovered PHREEQC executable passed the reachability test")


@route("POST", "/api/v1/system/phreeqc/settings")
def update_phreeqc_settings(handler, params, query, body):
    """Persist the user's path overrides.  Pass empty strings to clear."""
    if not isinstance(body, dict):
        return envelope_error(EC_INVALID_PARAMS, "Body must be a JSON object")
    allowed = {"phreeqc_exe", "phreeqc_database", "watch_dirs"}
    patch = {k: body.get(k) for k in allowed if k in body}
    existing = phreeqc_locator.get_settings()
    changed = any(
        str(patch[key] or "").strip() != str(existing.get(key) or "").strip()
        for key in ("phreeqc_exe", "phreeqc_database") if key in patch
    )
    if changed:
        patch["phreeqc_config_source"] = "manual"
    settings = phreeqc_locator.update_settings(patch)
    # Echo a quick reachability summary so the UI can flag typos
    # without a second round-trip.
    summary: dict = {}
    if settings.get("phreeqc_exe"):
        summary["executable"] = phreeqc_locator.test_executable(
            settings["phreeqc_exe"], settings.get("phreeqc_database")
        )
    if settings.get("phreeqc_database"):
        summary["database"] = phreeqc_locator.test_database(settings["phreeqc_database"])
    # If watch_dirs changed, reconfigure the importer.
    if "watch_dirs" in body:
        try:
            wd = settings.get("watch_dirs") or []
            run_importer.configure(wd)
            if wd:
                run_importer.start()
        except Exception as exc:  # noqa: BLE001
            summary["importer_error"] = str(exc)
    summary["importer"] = run_importer.status()
    return envelope_ok({"settings": settings, "test": summary})


# ---------------------------------------------------------------------------
# Route: Templates (the 9 built-in workflows)
# ---------------------------------------------------------------------------

@route("GET", "/api/v1/templates")
def list_templates(handler, params, query, body):
    items = tpl_service.list_templates()
    return envelope_ok({"templates": items})


@route("GET", "/api/v1/templates/{id}")
def get_template(handler, params, query, body):
    tid = params["id"]
    item = tpl_service.get_template(tid)
    if item is None:
        return envelope_error(EC_INVALID_PARAMS, f"Template not found: {tid}", 404)
    return envelope_ok(item)


# ---------------------------------------------------------------------------
# Route: custom scenarios (Scenario v1 -> legacy params -> runner)
# ---------------------------------------------------------------------------

def _scenario_error(result: dict) -> tuple[int, bytes, str]:
    """Turn a validation result into the standard error envelope."""

    errors = result.get("errors") or []
    message = errors[0].get("message") if errors else "Scenario validation failed"
    return envelope_error(EC_INVALID_PARAMS, f"{message} ({len(errors)} issue(s))")


def _body_scenario(body: Any) -> Any:
    """Extract the scenario payload, accepting either envelope-free form.

    The custom-scenario UI posts ``{"scenario": {...}}``; raw Scenario v1
    objects are accepted too so the endpoint can be driven by hand.
    """

    if isinstance(body, dict) and "scenario" in body:
        return body["scenario"]
    return body


@route("GET", "/api/v1/scenarios/types")
def list_scenario_types(handler, params, query, body):
    """Scenario types, their module skeletons, and the module registry."""

    return envelope_ok({
        "schema_version": scenarios.SCHEMA_VERSION,
        "types": scenarios.list_scenario_types(),
        "modules": scenarios.list_modules(),
    })


@route("POST", "/api/v1/scenarios/validate")
def validate_scenario(handler, params, query, body):
    """Structural check only.  Invalid input is data, not an HTTP error."""

    return envelope_ok(scenarios.validate_scenario(_body_scenario(body)))


@route("POST", "/api/v1/scenarios/preview")
def preview_scenario(handler, params, query, body):
    """Validate and, when valid, return the generated PHREEQC input text."""

    return envelope_ok(scenarios.preview_scenario(_body_scenario(body)))


@route("GET", "/api/v1/scenarios/templates")
def list_custom_templates(handler, params, query, body):
    return envelope_ok({"templates": custom_templates.list_templates()})


@route("GET", "/api/v1/scenarios/templates/{id}")
def get_custom_template(handler, params, query, body):
    """Full record (including the scenario) so the editor can load it back."""

    record = custom_templates.get_template(params["id"])
    if record is None:
        return envelope_error(EC_INVALID_PARAMS, f"Template not found: {params['id']}", 404)
    return envelope_ok(record)


@route("POST", "/api/v1/scenarios/templates")
def save_custom_template(handler, params, query, body):
    """Save (or overwrite) a custom scenario as a reusable template."""

    if not isinstance(body, dict):
        return envelope_error(EC_INVALID_PARAMS, "Body must be a JSON object")
    try:
        record = custom_templates.save_template(
            _body_scenario(body), template_id=body.get("template_id"),
        )
    except scenarios.ScenarioValidationError as exc:
        return _scenario_error(exc.result)
    except ValueError as exc:
        return envelope_error(EC_INVALID_PARAMS, str(exc))
    return envelope_ok(record, status=201)


@route("DELETE", "/api/v1/scenarios/templates/{id}")
def delete_custom_template(handler, params, query, body):
    if not custom_templates.delete_template(params["id"]):
        return envelope_error(EC_INVALID_PARAMS, f"Template not found: {params['id']}", 404)
    return envelope_ok({"deleted": params["id"]})


# ---------------------------------------------------------------------------
# Route: Runs
# ---------------------------------------------------------------------------

@route("GET", "/api/v1/runs")
def list_runs(handler, params, query, body):
    return envelope_ok({"runs": storage.list_runs()})


@route("POST", "/api/v1/runs")
def create_run(handler, params, query, body):
    """Create a new run from a template id, a Scenario v1, or raw params.

    Body: ``{"template_id": "pb_speciation"}``, ``{"scenario": {...}}`` or
    ``{"params": {...}}``.  All three end up as the same legacy ``params``
    document, so a custom scenario follows the identical runner path.
    """
    if not isinstance(body, dict):
        return envelope_error(EC_INVALID_PARAMS, "Body must be a JSON object")
    if "template_id" in body:
        tid = body["template_id"]
        tpl = tpl_service.get_template(tid)
        if tpl is None:
            return envelope_error(EC_INVALID_PARAMS, f"Template not found: {tid}")
        params_dict = tpl_service.instantiate(tpl)
        run_id = tpl["id"]
        display_name = tpl["title"]
    elif "scenario" in body:
        result = scenarios.validate_scenario(body["scenario"])
        if not result["valid"]:
            return _scenario_error(result)
        params_dict = result["params"]
        run_id = body.get("run_id") or storage.gen_run_id()
        display_name = body.get("name") or result["scenario"].get("name") or run_id
    elif "params" in body:
        params_dict = body["params"]
        run_id = body.get("run_id") or storage.gen_run_id()
        display_name = body.get("name", run_id)
    else:
        return envelope_error(
            EC_INVALID_PARAMS, "Body must contain 'template_id', 'scenario' or 'params'"
        )

    try:
        run = storage.create_run(run_id, display_name=display_name, params=params_dict)
    except ValueError as exc:
        return envelope_error(EC_INVALID_PARAMS, str(exc))
    return envelope_ok(run, status=201)


@route("GET", "/api/v1/runs/{id}")
def get_run(handler, params, query, body):
    run = storage.get_run(params["id"])
    if run is None:
        return envelope_error(EC_RUN_NOT_FOUND, f"Run not found: {params['id']}", 404)
    return envelope_ok(run)


@route("DELETE", "/api/v1/runs/{id}")
def delete_run(handler, params, query, body):
    ok = storage.delete_run(params["id"])
    if not ok:
        return envelope_error(EC_RUN_NOT_FOUND, f"Run not found: {params['id']}", 404)
    return envelope_ok({"deleted": params["id"]})


@route("POST", "/api/v1/runs/{id}/start")
def start_run(handler, params, query, body):
    run = storage.get_run(params["id"])
    if run is None:
        return envelope_error(EC_RUN_NOT_FOUND, f"Run not found: {params['id']}", 404)
    if run["status"] in ("pending", "running"):
        return envelope_error(
            EC_RUN_ALREADY_ACTIVE,
            f"Run is already {run['status']}",
        )
    storage.set_status(params["id"], "pending")
    # Launch in a background thread; progress is published via SSE.
    threading.Thread(
        target=runner.execute_run,
        args=(params["id"],),
        daemon=True,
    ).start()
    return envelope_ok({"run_id": params["id"], "status": "pending"})


@route("POST", "/api/v1/runs/{id}/abort")
def abort_run(handler, params, query, body):
    """Abort a running simulation.

    Terminates the PHREEQC subprocess (if any) and marks the run as
    ``aborted``.  Returns 200 even if no live process was found, so
    the UI can recover a stuck ``running`` record.
    """
    run = storage.get_run(params["id"])
    if run is None:
        return envelope_error(EC_RUN_NOT_FOUND, f"Run not found: {params['id']}", 404)
    if run["status"] not in ("pending", "running"):
        return envelope_error(
            EC_RUN_NOT_ACTIVE,
            f"Run is not active (status={run['status']})",
        )
    terminated = registry.abort(params["id"], grace_seconds=2.0)
    storage.set_status(params["id"], "aborted")
    return envelope_ok({
        "run_id": params["id"],
        "status": "aborted",
        "terminated": terminated,
    })


@route("GET", "/api/v1/runs/{id}/input")
def get_input(handler, params, query, body):
    """Return the generated .pqi input file content."""
    text = storage.read_artifact(params["id"], "input.pqi")
    if text is None:
        return envelope_error(EC_RUN_NOT_FOUND, "input.pqi not found", 404)
    body_bytes = text.encode("utf-8")
    return 200, body_bytes, "text/plain; charset=utf-8"


@route("GET", "/api/v1/runs/{id}/output")
def get_output(handler, params, query, body):
    text = storage.read_artifact(params["id"], "output.qpo")
    if text is None:
        return envelope_error(EC_RUN_NOT_FOUND, "output.qpo not found", 404)
    body_bytes = text.encode("utf-8")
    return 200, body_bytes, "text/plain; charset=utf-8"


@route("GET", "/api/v1/runs/{id}/selected-output")
def get_selected_output(handler, params, query, body):
    text = storage.read_artifact(params["id"], "selected_output.txt")
    if text is None:
        return envelope_error(EC_RUN_NOT_FOUND, "selected_output.txt not found", 404)
    body_bytes = text.encode("utf-8")
    return 200, body_bytes, "text/plain; charset=utf-8"


@route("GET", "/api/v1/runs/{id}/results")
def get_results(handler, params, query, body):
    text = storage.read_artifact(params["id"], "results.json")
    if text is None:
        return envelope_error(EC_RUN_NOT_FOUND, "results.json not found", 404)
    # results.json is already a JSON object; pass it through the
    # standard envelope so the client can consume it uniformly.
    import json as _json
    return 200, _json.dumps({"ok": True, "data": _json.loads(text)},
                            ensure_ascii=False).encode("utf-8"), \
           "application/json; charset=utf-8"


@route("GET", "/api/v1/runs/{id}/files")
def list_run_files(handler, params, query, body):
    files = storage.list_artifacts(params["id"])
    if files is None:
        return envelope_error(EC_RUN_NOT_FOUND, f"Run not found: {params['id']}", 404)
    return envelope_ok({"files": files})


@route("GET", "/api/v1/runs/{id}/files/{name+}")
def get_run_file(handler, params, query, body):
    name = params["name"]
    # Strict filename validation: no path traversal only.  Subdirectory
    # separators are explicitly allowed because artifacts may live under
    # e.g. ``charts/saturation_indices.png``.
    if ".." in name:
        return envelope_error(EC_INVALID_PATH, "Invalid filename", 400)
    if os.path.isabs(name) or name.startswith(("/", "\\")):
        return envelope_error(EC_INVALID_PATH, "Invalid filename", 400)
    data, mime = storage.read_binary_artifact(params["id"], name)
    if data is None:
        return envelope_error(EC_RUN_NOT_FOUND, f"File not found: {name}", 404)
    return 200, data, mime


# ---------------------------------------------------------------------------
# Route: input preview (preview a .pqi file from raw params without saving)
# ---------------------------------------------------------------------------

@route("POST", "/api/v1/preview-input")
def preview_input(handler, params, query, body):
    if not isinstance(body, dict) or "params" not in body:
        return envelope_error(EC_INVALID_PARAMS, "Body must contain 'params'")
    try:
        from generate_input import generate_single_simulation  # type: ignore
        text = generate_single_simulation(body["params"], output_file="selected_output.txt")
    except Exception as exc:  # noqa: BLE001
        return envelope_error(EC_INVALID_PARAMS, f"Failed to generate input: {exc}")
    return 200, text.encode("utf-8"), "text/plain; charset=utf-8"


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class WorkbenchHandler(BaseHTTPRequestHandler):
    server_version = "phreeqc-workbench/{}".format(WORKBENCH_VERSION)

    # Suppress default per-request stderr logging
    def log_message(self, format, *args):  # noqa: A002
        sys.stderr.write(
            "[%s] %s - %s\n"
            % (self.log_date_time_string(), self.address_string(), format % args)
        )

    # ---- helpers ----
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_sse(self, events: list[dict]) -> None:
        """Send a Server-Sent Events stream and close."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        try:
            for ev in events:
                payload = json.dumps(ev, ensure_ascii=False)
                self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return
        finally:
            try:
                self.wfile.write(b"event: end\ndata: {}\n\n")
                self.wfile.flush()
            except Exception:  # noqa: BLE001
                pass

    def _parse_body(self) -> dict | None:
        # Cap request bodies at 4 MiB.  The largest legitimate payload
        # is a template with ~10k components; anything beyond is either
        # accidental or hostile, and BaseHTTPRequestHandler will happily
        # block on a 5 GB body.
        MAX_BODY = 4 * 1024 * 1024
        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
        except (TypeError, ValueError):
            self._send(*envelope_error(EC_INVALID_PARAMS, "Invalid Content-Length"))
            return None
        if length < 0 or length > MAX_BODY:
            self._send(*envelope_error(
                EC_INVALID_PARAMS,
                f"Request body too large (limit {MAX_BODY} bytes)",
            ))
            return None
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            self._send(*envelope_error(EC_INVALID_PARAMS, f"Invalid JSON: {exc}"))
            return None

    # ---- verb dispatchers ----
    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        # SSE: /api/v1/runs/{id}/events
        if path.startswith(API_PREFIX + "/runs/") and path.endswith("/events"):
            rid = path[len(API_PREFIX) + len("/runs/"):-len("/events")].strip("/")
            events = storage.consume_events(rid)
            if events is None:
                self._send(*envelope_error(EC_RUN_NOT_FOUND, "Run not found", 404))
                return
            self._send_sse(events)
            return

        handler_fn, path_params = _match_route("GET", path)
        if handler_fn is None:
            # Fall back to static file serving
            self._serve_static(path)
            return
        try:
            status, body, ctype = handler_fn(self, path_params, query, {})
        except Exception as exc:  # noqa: BLE001
            status, body, ctype = envelope_error(EC_INTERNAL, str(exc), 500)
        self._send(status, body, ctype)

    def do_POST(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._parse_body()
        if body is None:
            return
        handler_fn, path_params = _match_route("POST", path)
        if handler_fn is None:
            self._send(*envelope_error(EC_INVALID_PATH, "Not found", 404))
            return
        try:
            status, body_b, ctype = handler_fn(self, path_params, {}, body)
        except Exception as exc:  # noqa: BLE001
            status, body_b, ctype = envelope_error(EC_INTERNAL, str(exc), 500)
        self._send(status, body_b, ctype)
        # If the handler flagged the server for shutdown, do it AFTER the
        # response has been written so the client can read the body.
        if getattr(self, "_shutdown_after_response", False):
            threading.Thread(
                target=self.server.shutdown, daemon=True
            ).start()

    def do_DELETE(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        handler_fn, path_params = _match_route("DELETE", path)
        if handler_fn is None:
            self._send(*envelope_error(EC_INVALID_PATH, "Not found", 404))
            return
        try:
            status, body, ctype = handler_fn(self, path_params, {}, {})
        except Exception as exc:  # noqa: BLE001
            status, body, ctype = envelope_error(EC_INTERNAL, str(exc), 500)
        self._send(status, body, ctype)

    # ---- static ----
    def _serve_static(self, path: str) -> None:
        if path == "/" or path == "":
            path = "/index.html"
        # Prevent path traversal
        clean = path.lstrip("/")
        if ".." in clean or clean.startswith("/"):
            self._send(*envelope_error(EC_INVALID_PATH, "Invalid path", 400))
            return
        full = os.path.normpath(os.path.join(STATIC_DIR, clean))
        if not full.startswith(os.path.abspath(STATIC_DIR)):
            self._send(*envelope_error(EC_INVALID_PATH, "Invalid path", 400))
            return
        if not os.path.isfile(full):
            # SPA fallback: serve index.html for unknown GETs (no extension)
            if "." not in os.path.basename(clean):
                full = os.path.join(STATIC_DIR, "index.html")
                if not os.path.isfile(full):
                    self.send_response(404)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.send_header("Content-Length", "13")
                    self.end_headers()
                    self.wfile.write(b"404 Not Found")
                    return
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", "13")
                self.end_headers()
                self.wfile.write(b"404 Not Found")
                return
        ctype, _ = mimetypes.guess_type(full)
        if ctype is None:
            ctype = "application/octet-stream"
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        # index.html must not be cached aggressively
        if os.path.basename(full) == "index.html":
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="PHREEQC Auto Workbench backend")
    p.add_argument("--host", default="127.0.0.1", help="Bind host (default 127.0.0.1)")
    p.add_argument("--port", type=int, default=8765, help="Bind port (default 8765)")
    p.add_argument("--workspace", default=None,
                   help="Workspace root directory (default ./workspace_workbench)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    storage.init(workspace_root=args.workspace)
    phreeqc_locator.init_settings(workspace_root=args.workspace)
    custom_templates.init(workspace_root=storage.workspace_root())
    # Restore the file watcher if the user previously configured one.
    try:
        watch_dirs = phreeqc_locator.get_settings().get("watch_dirs") or []
        if watch_dirs:
            run_importer.configure(watch_dirs)
            run_importer.start()
            print(f"[workbench] importer watching: {watch_dirs}")
    except Exception as exc:  # noqa: BLE001
        print(f"[workbench] importer restore failed: {exc}")
    server = SingleInstanceHTTPServer((args.host, args.port), WorkbenchHandler)
    print(f"[workbench] listening on http://{args.host}:{args.port}")
    print(f"[workbench] static dir: {STATIC_DIR}")
    print(f"[workbench] workspace:  {storage.workspace_root()}")
    print(f"[workbench] settings:   {phreeqc_locator.get_settings()}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[workbench] shutting down...")
        aborted = registry.abort_all(grace_seconds=2.0)
        if aborted:
            print(f"[workbench] aborted {len(aborted)} run(s): {aborted}")
        try:
            run_importer.stop()
        except Exception:  # noqa: BLE001
            pass
        server.shutdown()


if __name__ == "__main__":
    main()
