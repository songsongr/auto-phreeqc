"""Check whether this checkout is ready to run PHREEQC calculations.

This command is intentionally dependency-light so an agent can use it during
first-run setup. It validates the executable and database discovered by the
public runtime and, with ``--run``, performs a disposable calculation.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from phreeqc_auto.run_phreeqc import (  # noqa: E402
    find_database,
    find_phreeqc_exe,
    run_simulation,
    save_local_config,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify an auto-phreeqc setup.")
    parser.add_argument("--phreeqc-exe", help="Path to phreeqc or phreeqc.exe")
    parser.add_argument("--database", help="Path to a PHREEQC .dat database")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run a disposable aqueous-solution calculation after discovery.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    report: dict[str, object] = {"project_root": str(PROJECT_ROOT)}

    try:
        executable = args.phreeqc_exe or find_phreeqc_exe(project_root=str(PROJECT_ROOT))
        database = args.database or find_database(project_root=str(PROJECT_ROOT))
        config_path = save_local_config(
            executable, database, project_root=str(PROJECT_ROOT)
        )
    except FileNotFoundError as exc:
        report.update({"ready": False, "error": str(exc)})
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    report.update(
        {
            "ready": True,
            "phreeqc_exe": executable,
            "database": database,
            "local_config": config_path,
        }
    )

    if args.run:
        with tempfile.TemporaryDirectory(prefix="auto-phreeqc-doctor-") as directory:
            run_dir = Path(directory)
            input_file = run_dir / "doctor.pqi"
            output_file = run_dir / "doctor.qpo"
            input_file.write_text("SOLUTION 1\n    pH 7.0\nEND\n", encoding="utf-8")
            result = run_simulation(
                str(input_file),
                output_file=str(output_file),
                database=database,
                cwd=str(run_dir),
                project_root=str(PROJECT_ROOT),
            )
            report["test_run"] = {
                "success": result["success"],
                "exit_code": result["exit_code"],
                "error": result["error"],
            }
            if not result["success"]:
                report["ready"] = False

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
