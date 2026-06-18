"""
PHREEQC simulation runner.

Provides functions to locate the PHREEQC executable and database files,
and to run PHREEQC simulations with subprocess.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys


__all__ = [
    "find_phreeqc_exe",
    "find_database",
    "run_simulation",
]


def find_phreeqc_exe() -> str:
    """Locate the PHREEQC executable.

    Search order:
      1. ``PHREEQC_EXE`` environment variable -- returned if it points
         to a valid file.
      2. ``phreeqc`` on ``PATH`` (via ``shutil.which``).
      3. ``phreeqc.exe`` on ``PATH``.
      4. Windows ``.lnk`` shortcut at the project root.

    Returns:
        Absolute path to the PHREEQC executable.

    Raises:
        FileNotFoundError: If PHREEQC cannot be found through any of
            the search methods.
    """
    # 1. PHREEQC_EXE environment variable
    exe = os.environ.get("PHREEQC_EXE")
    if exe:
        exe = os.path.abspath(exe)
        if os.path.isfile(exe):
            return exe

    # 2 & 3. PATH lookup -- prefer .exe, reject batch wrappers
    found = shutil.which("phreeqc.exe")
    if found:
        return os.path.abspath(found)
    found = shutil.which("phreeqc")
    if found and not found.lower().endswith(('.bat', '.cmd')):
        return os.path.abspath(found)

    # 4. Windows .lnk shortcut at project root
    if sys.platform.startswith("win"):
        project_root = _find_project_root()
        lnk_name = "phreeqc-3.8.6-17100-x64 - 快捷方式.lnk"
        lnk_path = os.path.join(project_root, lnk_name)
        if os.path.isfile(lnk_path):
            target = _resolve_lnk(lnk_path)
            if target and os.path.isfile(target):
                return os.path.abspath(target)

    raise FileNotFoundError(
        "Could not locate PHREEQC executable. "
        "Set the PHREEQC_EXE environment variable to the full path of "
        "the PHREEQC executable, or ensure 'phreeqc' (or 'phreeqc.exe') "
        "is on your PATH."
    )


def _find_project_root() -> str:
    """Find the project root directory by searching upward for
    ``CLAUDE.md``.

    Starts from the directory containing this script and walks up at
    most 6 levels.  Falls back to ``os.getcwd()`` if no ``CLAUDE.md``
    is found.

    Returns:
        Absolute path to the project root directory.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(7):  # 6 levels up + current level
        candidate = os.path.join(script_dir, "CLAUDE.md")
        if os.path.isfile(candidate):
            return script_dir
        parent = os.path.dirname(script_dir)
        if parent == script_dir:
            break
        script_dir = parent
    return os.getcwd()


def _resolve_lnk(lnk_path: str) -> str | None:
    """Resolve a Windows ``.lnk`` shortcut to its target path.

    Uses PowerShell's ``WScript.Shell`` COM object to read the shortcut
    target.  If the target is a directory, searches for ``phreeqc.exe``
    in common subdirectories.  Returns ``None`` on non-Windows platforms
    or if resolution fails for any reason.

    Args:
        lnk_path: Absolute path to the ``.lnk`` file.

    Returns:
        The target path string, or ``None``.
    """
    if not sys.platform.startswith("win"):
        return None
    try:
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                f"(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk_path}').TargetPath",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        target = result.stdout.strip()
        if target:
            if os.path.isfile(target):
                return target
            if os.path.isdir(target):
                # lnk points to a directory -- search for phreeqc.exe
                # Prefer native Release over CLR or generic bin
                for sub in ("bin\\Release\\phreeqc.exe", "bin\\ClrRelease\\phreeqc.exe",
                            "bin\\phreeqc.exe", "phreeqc.exe"):
                    candidate = os.path.join(target, sub)
                    if os.path.isfile(candidate):
                        return candidate
    except Exception:
        pass
    return None


def find_database(database_name: str = "phreeqc.dat") -> str:
    """Locate a PHREEQC database file.

    Search order:
      1. ``PHREEQC_DATABASE`` environment variable.
      2. ``database/{database_name}`` relative to the project root.
      3. Standard install locations (``C:\\Program Files\\USGS\\phreeqc-*\\database\\``
         on Windows, ``/usr/local/share/phreeqc/database/`` on Unix).
      4. ``database/{database_name}`` relative to the PHREEQC executable
         directory.
      5. ``{database_name}`` in the PHREEQC executable directory.

    Args:
        database_name: Name of the database file to locate
            (default ``"phreeqc.dat"``).

    Returns:
        Absolute path to the database file.

    Raises:
        FileNotFoundError: If the database file cannot be found through
            any of the search methods.
    """
    # 1. PHREEQC_DATABASE environment variable
    db = os.environ.get("PHREEQC_DATABASE")
    if db:
        db = os.path.abspath(db)
        if os.path.isfile(db):
            return db

    project_root = _find_project_root()

    # 2. database/{name} relative to project root
    candidate = os.path.join(project_root, "database", database_name)
    if os.path.isfile(candidate):
        return os.path.abspath(candidate)

    # 3. Standard install locations (fallback when exe not resolvable)
    if sys.platform.startswith("win"):
        _search = os.path.join(
            "C:\\Program Files\\USGS", "phreeqc-*", "database", database_name
        )
        import glob as _glob
        for candidate in _glob.glob(_search):
            if os.path.isfile(candidate):
                return os.path.abspath(candidate)
        _search = os.path.join(
            "C:\\Program Files (x86)\\USGS", "phreeqc-*", "database", database_name
        )
        for candidate in _glob.glob(_search):
            if os.path.isfile(candidate):
                return os.path.abspath(candidate)
    else:
        for _base in ("/usr/local/share/phreeqc/database",
                      "/usr/share/phreeqc/database"):
            candidate = os.path.join(_base, database_name)
            if os.path.isfile(candidate):
                return os.path.abspath(candidate)

    # 4 & 5. Relative to PHREEQC exe directory
    try:
        exe_dir = os.path.dirname(find_phreeqc_exe())
    except FileNotFoundError:
        exe_dir = None

    if exe_dir:
        # 4. exe_dir/database/{name}
        candidate = os.path.join(exe_dir, "database", database_name)
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

        # 5. exe_dir/{name}
        candidate = os.path.join(exe_dir, database_name)
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

    raise FileNotFoundError(
        f"Could not locate database '{database_name}'. "
        "Set the PHREEQC_DATABASE environment variable to the full path "
        "of the database file, or place the file in the project's "
        "'database/' directory."
    )


def run_simulation(
    input_file: str,
    output_file: str | None = None,
    database: str | None = None,
    *,
    timeout: int = 300,
    cwd: str | None = None,
) -> dict:
    """Run a PHREEQC simulation.

    Locates the PHREEQC executable and database automatically, then
    invokes the subprocess::

        phreeqc <input_file> [output_file] [database]

    Args:
        input_file: Path to the PHREEQC input file.
        output_file: Path for the output file.  If ``None``, PHREEQC
            will derive the output filename from the input file (by
            appending ``.out``).
        database: Path to the database file.  If ``None``, the database
            is located automatically via :func:`find_database`.
        timeout: Maximum runtime in seconds (default 300).  Raises
            ``TimeoutExpired`` in the result dict when exceeded.
        cwd: Working directory for the PHREEQC subprocess.  When set,
            SELECTED_OUTPUT files with relative paths will be written
            relative to this directory (default ``None``, which inherits
            the current process's working directory).

    Returns:
        A dict with the following keys:

        - **exit_code** (*int | None*): Process exit code, or ``None``
          if the process timed out.
        - **stdout** (*str*): Captured stdout text.
        - **stderr** (*str*): Captured stderr text.
        - **output_file** (*str | None*): Absolute path to the output
          file (``None`` if no output file was specified).
        - **success** (*bool*): ``True`` if exit code is 0.
        - **error** (*str | None*): Human-readable error message, or
          ``None`` on success.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    exe = find_phreeqc_exe()
    if database is None:
        database = find_database()

    output_file_abs = (
        os.path.abspath(output_file) if output_file else None
    )

    cmd = [exe, os.path.abspath(input_file)]
    if output_file_abs:
        cmd.append(output_file_abs)
    cmd.append(database)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            cwd=cwd,
        )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "output_file": output_file_abs,
            "success": proc.returncode == 0,
            "error": None if proc.returncode == 0 else (
                proc.stderr.strip() or proc.stdout.strip() or
                f"Process exited with code {proc.returncode}"
            ),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "exit_code": None,
            "stdout": exc.stdout if exc.stdout else "",
            "stderr": exc.stderr if exc.stderr else "",
            "output_file": output_file_abs,
            "success": False,
            "error": f"Simulation timed out after {timeout} seconds",
        }
    except FileNotFoundError:
        raise
    except OSError as exc:
        return {
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "output_file": output_file_abs,
            "success": False,
            "error": f"OS error running PHREEQC: {exc}",
        }
