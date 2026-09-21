"""Create a project-local Python environment and verify PHREEQC readiness."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = PROJECT_ROOT / ".auto-phreeqc-venv"
VENV_PYTHON = VENV_DIR / (
    "Scripts/python.exe" if sys.platform.startswith("win") else "bin/python"
)
USGS_DOWNLOAD_PAGE = "https://water.usgs.gov/water-resources/software/PHREEQC/"


def _run(command: list[str]) -> int:
    print("+", " ".join(command))
    return subprocess.run(command, cwd=PROJECT_ROOT, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set up auto-phreeqc in a project-local virtual environment."
    )
    parser.add_argument("--with-dev", action="store_true", help="Also install test tools.")
    parser.add_argument("--phreeqc-exe", help="Optional PHREEQC executable path.")
    parser.add_argument("--database", help="Optional PHREEQC database path.")
    args = parser.parse_args()

    uv = shutil.which("uv")
    if not VENV_PYTHON.exists():
        if uv:
            if _run([uv, "venv", str(VENV_DIR)]) != 0:
                return 1
        elif _run([sys.executable, "-m", "venv", str(VENV_DIR)]) != 0:
            return 1

    extras = ".[dev]" if args.with_dev else "."
    if uv:
        if _run([uv, "pip", "install", "--python", str(VENV_PYTHON), "-e", extras]) != 0:
            return 1
    else:
        # Some managed Python distributions create a virtual environment
        # without pip. Ensure it is present before asking it to install the
        # package.
        has_pip = subprocess.run(
            [str(VENV_PYTHON), "-m", "pip", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
        if not has_pip:
            has_pip = _run([str(VENV_PYTHON), "-m", "ensurepip", "--upgrade"]) == 0
        if not has_pip:
            print("Unable to bootstrap pip in the project environment. Install or repair Python, then rerun setup.")
            return 1
        if _run([str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip"]) != 0:
            return 1
        if _run([str(VENV_PYTHON), "-m", "pip", "install", "-e", extras]) != 0:
            return 1

    doctor_command = [str(VENV_PYTHON), "scripts/doctor.py", "--run"]
    if args.phreeqc_exe:
        doctor_command.extend(["--phreeqc-exe", args.phreeqc_exe])
    if args.database:
        doctor_command.extend(["--database", args.database])
    code = _run(doctor_command)
    if code == 2:
        print("\nPHREEQC was not found. Install it from the official USGS page, then rerun:")
        print(f"  {USGS_DOWNLOAD_PAGE}")
        print("\nAfter installation, bootstrap will discover standard locations automatically.")
    elif code == 0:
        print("\nSetup complete. The repository-local phreeqc-auto Skill is ready to use.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
