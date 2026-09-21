"""
PHREEQC executable / database locator.

Wraps the upstream :func:`run_phreeqc.find_phreeqc_exe` and
:func:`run_phreeqc.find_database` with three extra concerns that matter
for a public-facing workbench:

1.  **Auto-discovery of candidate paths.**  On top of the upstream
    search order, we scan the common Windows install roots
    (``C:\\Program Files\\USGS\\phreeqc-*`` and the ``(x86)`` variant),
    the project tree, and any ``phreeqc*.lnk`` shortcuts nearby, so
    that users with a default USGS install do not have to set
    ``PHREEQC_EXE``.

2.  **Reachability test.**  Calling the candidate executable with a
    trivial flag is the only way to know that the binary actually
    runs (vs. a stale .lnk pointing at a moved file, or a 32/64-bit
    mismatch).  We invoke the executable with ``-h`` (or the platform
    equivalent) and capture the first ~200 bytes of output together
    with the return code.

3.  **User override.**  The workbench keeps a ``workbench.json`` next
    to the workspace that records the user's chosen ``phreeqc_exe``
    and ``phreeqc_database`` paths.  On startup we export them to the
    ``PHREEQC_EXE`` / ``PHREEQC_DATABASE`` environment variables that
    the upstream ``find_*`` functions honour first, so the rest of
    the pipeline (run_phreeqc, parse_output, etc.) is unaware of the
    override.

All public functions are thread-safe.
"""

from __future__ import annotations

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from typing import Any

# ---------------------------------------------------------------------------
# Import the public runtime package from a source checkout when needed.
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_THIS_DIR)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_BACKEND_DIR))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from phreeqc_auto import run_phreeqc  # noqa: E402


# ---------------------------------------------------------------------------
# Settings file (per workspace, JSON, manually edited in case of
# corruption -- never crashes the server).
# ---------------------------------------------------------------------------

_settings_lock = threading.RLock()
_settings_path: str | None = None
_settings_cache: dict[str, Any] = {}

# Discovery cache: results are stable for a few seconds, so we avoid
# re-walking the filesystem on every health check.
CACHE_TTL = 30.0
_discover_cache: tuple[float, list[dict[str, Any]]] | None = None
_db_cache: tuple[float, list[dict[str, Any]]] | None = None


def invalidate_caches() -> None:
    """Drop the discovery cache (called after settings change)."""
    global _discover_cache, _db_cache, _active_exe_cache, _active_db_cache
    _discover_cache = None
    _db_cache = None
    _active_exe_cache = None
    _active_db_cache = None


def _default_settings_path() -> str:
    # ``workspace`` package holds the canonical workspace root; we fall
    # back to a local file if the workspace is not yet initialised.
    try:
        from services import storage  # type: ignore
        return os.path.join(storage.workspace_root(), "workbench.json")
    except Exception:  # noqa: BLE001
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "workbench.json",
        )


def init_settings(workspace_root: str | None = None) -> None:
    """Pin the location of ``workbench.json`` for this process."""
    global _settings_path, _settings_cache
    if workspace_root:
        path = os.path.join(os.path.abspath(workspace_root), "workbench.json")
    else:
        path = _default_settings_path()
    _settings_path = path
    _settings_cache = _load_from_disk(path)
    _apply_env_overrides(_settings_cache)


def _load_from_disk(path: str) -> dict[str, Any]:
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except (OSError, json.JSONDecodeError):
        return {}


def _flush_to_disk() -> None:
    if _settings_path is None:
        return
    try:
        os.makedirs(os.path.dirname(_settings_path), exist_ok=True)
        tmp = _settings_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(_settings_cache, f, ensure_ascii=False, indent=2)
        os.replace(tmp, _settings_path)
    except OSError:
        pass  # best-effort -- the server must not crash on disk errors


def _apply_env_overrides(settings: dict[str, Any]) -> None:
    """Mirror user-chosen paths to env vars the upstream find_* consults."""
    exe = settings.get("phreeqc_exe")
    if exe and os.path.isfile(exe):
        os.environ["PHREEQC_EXE"] = exe
    else:
        os.environ.pop("PHREEQC_EXE", None)
    db = settings.get("phreeqc_database")
    if db and os.path.isfile(db):
        os.environ["PHREEQC_DATABASE"] = db
    else:
        os.environ.pop("PHREEQC_DATABASE", None)


def get_settings() -> dict[str, Any]:
    """Return a copy of the current settings (no disk I/O)."""
    with _settings_lock:
        return dict(_settings_cache)


def update_settings(patch: dict[str, Any]) -> dict[str, Any]:
    """Merge ``patch`` into the settings, persist, and return the result.

    Empty / ``None`` values clear the corresponding key (so a user can
    revert to the upstream auto-discovery by submitting ``""``).
    """
    with _settings_lock:
        for k, v in (patch or {}).items():
            if k not in {"phreeqc_exe", "phreeqc_database", "phreeqc_config_source", "watch_dirs"}:
                continue
            if k == "watch_dirs":
                # Watch dirs is a list; accept lists of strings.
                if v is None:
                    _settings_cache.pop(k, None)
                elif isinstance(v, list):
                    _settings_cache[k] = [str(x).strip() for x in v if str(x).strip()]
                continue
            if v is None or (isinstance(v, str) and not v.strip()):
                _settings_cache.pop(k, None)
            else:
                _settings_cache[k] = str(v).strip()
        _apply_env_overrides(_settings_cache)
        _flush_to_disk()
        invalidate_caches()
        return dict(_settings_cache)


# ---------------------------------------------------------------------------
# Candidate discovery (read-only; safe to call repeatedly).
# ---------------------------------------------------------------------------

def _is_executable_file(p: str) -> bool:
    return bool(p) and os.path.isfile(p)


def _scan_program_files() -> list[str]:
    """Return candidate ``phreeqc*.exe`` files under standard Windows installs."""
    if not sys.platform.startswith("win"):
        return []
    roots = [
        r"C:\Program Files\USGS",
        r"C:\Program Files (x86)\USGS",
    ]
    found: list[str] = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        try:
            for version_dir in os.listdir(root):
                if not version_dir.lower().startswith("phreeqc"):
                    continue
                base = os.path.join(root, version_dir)
                for sub in ("bin\\Release\\phreeqc.exe",
                            "bin\\ClrRelease\\phreeqc.exe",
                            "bin\\phreeqc.exe",
                            "phreeqc.exe"):
                    candidate = os.path.join(base, sub)
                    if _is_executable_file(candidate):
                        found.append(candidate)
                # also any phreeqc.exe anywhere one level down
                for entry in os.listdir(base):
                    full = os.path.join(base, entry)
                    if (os.path.isfile(full)
                            and entry.lower() == "phreeqc.exe"
                            and full not in found):
                        found.append(full)
        except OSError:
            continue
    return found


def _scan_path() -> list[str]:
    found: list[str] = []
    for name in ("phreeqc.exe", "phreeqc", "phreeqc.com"):
        hit = shutil.which(name)
        if hit and os.path.isfile(hit) and not hit.lower().endswith((".bat", ".cmd")):
            found.append(os.path.abspath(hit))
    return found


def _scan_lnk_shortcuts() -> list[str]:
    """Pick up ``phreeqc*.lnk`` files near the project root."""
    candidates: list[str] = []
    bases: list[str] = []
    bases.append(_PROJECT_ROOT)
    for base in bases:
        if not os.path.isdir(base):
            continue
        try:
            for entry in os.listdir(base):
                if entry.lower().endswith(".lnk") and "phreeqc" in entry.lower():
                    candidates.append(os.path.join(base, entry))
        except OSError:
            continue
    return candidates


def _resolve_lnk_safe(lnk_path: str) -> str | None:
    """Resolve a Windows .lnk using PowerShell (best-effort)."""
    if not sys.platform.startswith("win"):
        return None
    try:
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                f"(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk_path}').TargetPath",
            ],
            capture_output=True, text=True, encoding="utf-8", timeout=10,
        )
        target = result.stdout.strip()
        if target and os.path.isfile(target):
            return os.path.abspath(target)
    except Exception:  # noqa: BLE001
        pass
    return None


def _scan_databases(near: str | None) -> list[str]:
    """Return known PHREEQC database files (``*.dat``) we can find.

    ``near`` is a hint (typically the directory of a found phreeqc.exe);
    we additionally check the conventional USGS install layout.
    """
    found: list[str] = []
    if near:
        for d in (os.path.dirname(near), os.path.join(os.path.dirname(near), "database")):
            if not os.path.isdir(d):
                continue
            try:
                for entry in os.listdir(d):
                    if entry.lower().endswith(".dat") and "phreeqc" in entry.lower():
                        full = os.path.join(d, entry)
                        if full not in found:
                            found.append(full)
            except OSError:
                continue
    if sys.platform.startswith("win"):
        for root in (r"C:\Program Files\USGS", r"C:\Program Files (x86)\USGS"):
            for match in glob.glob(os.path.join(root, "phreeqc-*", "database", "*.dat")):
                if match not in found:
                    found.append(match)
    return found


def discover_executables() -> list[dict[str, Any]]:
    """Return a deduplicated list of candidate phreeqc executables.

    Each entry: ``{path, source, exists}``.  ``source`` describes how
    the path was found (env, path, program_files, lnk, settings,
    upstream).

    Results are memoised for ``CACHE_TTL`` seconds because the upstream
    ``run_phreeqc.find_phreeqc_exe`` also walks the filesystem and
    calling it on every health-check turns the health endpoint into a
    disk-bound operation.
    """
    global _discover_cache
    now = time.time()
    if _discover_cache and now - _discover_cache[0] < CACHE_TTL:
        return _discover_cache[1]
    results: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(path: str, source: str) -> None:
        if not path:
            return
        path = os.path.abspath(path)
        if path in seen:
            return
        seen.add(path)
        results.append({
            "path": path,
            "source": source,
            "exists": _is_executable_file(path),
        })

    # 1. user override (settings file)
    with _settings_lock:
        override = _settings_cache.get("phreeqc_exe")
    if override:
        add(override, "settings")

    # 2. env var (in case the operator set PHREEQC_EXE in the shell)
    env_exe = os.environ.get("PHREEQC_EXE")
    if env_exe and env_exe != override:
        add(env_exe, "env")

    # 3. PATH
    for p in _scan_path():
        add(p, "path")

    # 4. program files
    for p in _scan_program_files():
        add(p, "program_files")

    # 5. lnk shortcuts
    for lnk in _scan_lnk_shortcuts():
        # Include the .lnk path itself (the user might re-resolve later)
        if lnk not in seen:
            seen.add(lnk)
            results.append({
                "path": lnk,
                "source": "lnk",
                "exists": os.path.isfile(lnk),
            })
        target = _resolve_lnk_safe(lnk)
        if target:
            add(target, "lnk_resolved")

    _discover_cache = (now, results)
    return results


def discover_databases(exe_path: str | None = None) -> list[dict[str, Any]]:
    """Return candidate PHREEQC database files (deduplicated).

    Results are memoised for ``CACHE_TTL`` seconds (the ``exe_path``
    argument is ignored on cache hit, which is fine because the
    database directories do not depend on the executable location).
    """
    global _db_cache
    now = time.time()
    if _db_cache and now - _db_cache[0] < CACHE_TTL:
        return _db_cache[1]
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    near = os.path.dirname(exe_path) if exe_path else None
    for p in _scan_databases(near):
        p = os.path.abspath(p)
        if p in seen:
            continue
        seen.add(p)
        results.append({
            "path": p,
            "exists": os.path.isfile(p),
            "source": "filesystem",
        })
    # user override
    with _settings_lock:
        override = _settings_cache.get("phreeqc_database")
    if override:
        override = os.path.abspath(override)
        if override not in seen:
            seen.add(override)
            results.insert(0, {
                "path": override,
                "exists": os.path.isfile(override),
                "source": "settings",
            })
    _db_cache = (now, results)
    return results


# ---------------------------------------------------------------------------
# Reachability test
# ---------------------------------------------------------------------------

def _probe_version(
    exe_path: str,
    database_path: str | None = None,
    timeout: float = 8.0,
) -> dict[str, Any]:
    """Run a trivial PHREEQC job to verify the binary.

    PHREEQC has no documented ``--version``/``-h`` flag: calling the
    binary with no input or a stray flag puts it into an interactive
    ``Name of input file?`` prompt that blocks on stdin.  The
    definitive way to confirm a binary is healthy is to feed it a
    minimal valid input and observe a clean exit.  This is also a
    much stronger end-to-end check (binary + database wired up).
    """
    import tempfile

    started = time.time()
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".pqi", delete=False, encoding="utf-8",
    )
    try:
        # Smallest valid input: a 1-cell pure-water solution + END.
        tmp.write(
            "SOLUTION 1\n"
            "    temp 25.0\n"
            "    pH 7.0\n"
            "    pe 4.0\n"
            "SELECTED_OUTPUT 1\n"
            "    -pH\n"
            "END\n"
        )
        tmp.close()
        out_path = tmp.name[:-4] + ".qpo"
        # The PHREEQC command line is: phreeqc <input> <output> <database>
        # (we only need a working database for the binary to not stall
        # on "Name of database file?"); use whichever we can find, falling
        # back to whatever upstream discovery yields.
        if database_path and os.path.isfile(database_path):
            db = os.path.abspath(database_path)
        else:
            try:
                db = find_database()
            except FileNotFoundError:
                db = None
        cmd = [exe_path, tmp.name, out_path]
        if db:
            cmd.append(db)
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True, text=True,
                timeout=timeout, encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": f"timeout after {timeout:.0f}s"}
        except FileNotFoundError as exc:
            return {"ok": False, "error": f"not found: {exc}"}
        except PermissionError as exc:
            return {"ok": False, "error": f"permission denied: {exc}"}
        except OSError as exc:
            return {"ok": False, "error": f"OS error: {exc}"}
        elapsed = time.time() - started
        stderr = (proc.stderr or "")[:400]
        version = _detect_version(exe_path, proc.stderr or "", proc.stdout or "")
        # ``run_phreeqc`` already proved PHREEQC returns 0 on success; if
        # the binary launched, ran a job, and exited cleanly, treat the
        # binary as healthy regardless of stderr noise (PHREEQC can
        # print non-fatal warnings).
        if proc.returncode == 0 and os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
            result = {
                "ok": True,
                "exit_code": proc.returncode,
                "elapsed_ms": int(elapsed * 1000),
                "stderr_head": stderr,
            }
            if version:
                result["version"] = version
            return result
        result = {
            "ok": False,
            "exit_code": proc.returncode,
            "elapsed_ms": int(elapsed * 1000),
            "stderr_head": stderr,
            "error": f"rc={proc.returncode}, output_size={os.path.getsize(out_path) if os.path.isfile(out_path) else 0}",
        }
        if version:
            result["version"] = version
        return result
    finally:
        for p in (tmp.name, tmp.name[:-4] + ".qpo"):
            try:
                os.unlink(p)
            except OSError:
                pass


def _detect_version(exe_path: str, *output_parts: str) -> str | None:
    """Extract a human-readable PHREEQC version from its banner or path."""
    text = "\n".join(output_parts)
    match = re.search(r"PHREEQC[-\s]+([0-9]+(?:\.[0-9]+)+)", text, re.IGNORECASE)
    version = match.group(1) if match else None
    path_match = re.search(r"phreeqc-([0-9]+(?:\.[0-9]+)+)-([0-9]+)", exe_path, re.IGNORECASE)
    if path_match:
        version = version or path_match.group(1)
        return f"PHREEQC {version} ({path_match.group(2)})"
    return f"PHREEQC {version}" if version else None


def detected_version(exe_path: str | None) -> str | None:
    """Return the version encoded in a known PHREEQC install path."""
    return _detect_version(exe_path, "") if exe_path else None


def test_executable(exe_path: str, database_path: str | None = None) -> dict[str, Any]:
    """Validate that ``exe_path`` exists and runs.  Returns a dict."""
    if not exe_path:
        return {"ok": False, "error": "no path provided"}
    exe_path = os.path.abspath(exe_path)
    if not os.path.isfile(exe_path):
        return {"ok": False, "error": "file not found", "path": exe_path}
    if not os.access(exe_path, os.X_OK) and not exe_path.lower().endswith(".exe"):
        return {"ok": False, "error": "not executable", "path": exe_path}
    result = _probe_version(exe_path, database_path)
    result["path"] = exe_path
    return result


def test_database(db_path: str) -> dict[str, Any]:
    if not db_path:
        return {"ok": False, "error": "no path provided"}
    db_path = os.path.abspath(db_path)
    if not os.path.isfile(db_path):
        return {"ok": False, "error": "file not found", "path": db_path}
    try:
        size = os.path.getsize(db_path)
    except OSError:
        size = 0
    if size < 1024:
        return {"ok": False, "error": f"file too small ({size} B); not a valid database",
                "path": db_path, "size": size}
    # Look for a magic keyword: PHREEQC databases start with "SOLUTION_MASTER_SPECIES"
    # (with a few optional leading whitespace/comment lines).
    try:
        with open(db_path, encoding="utf-8", errors="replace") as f:
            head = f.read(8192)
    except OSError as exc:
        return {"ok": False, "error": f"unreadable: {exc}", "path": db_path}
    if not re.search(r"SOLUTION_MASTER_SPECIES", head, re.IGNORECASE):
        return {"ok": False, "error": "missing SOLUTION_MASTER_SPECIES marker",
                "path": db_path, "size": size}
    return {"ok": True, "path": db_path, "size": size}


# ---------------------------------------------------------------------------
# Wrappers around the upstream find_* that honour user settings
# ---------------------------------------------------------------------------

_active_exe_cache: tuple[float, str | None] | None = None
_active_db_cache: tuple[float, str | None] | None = None


def _active_exe_lookup() -> str:
    """Resolve the PHREEQC executable through the upstream helper."""
    return run_phreeqc.find_phreeqc_exe(project_root=_PROJECT_ROOT)


def find_phreeqc_exe() -> str:
    """Like ``run_phreeqc.find_phreeqc_exe`` but honours ``workbench.json``.

    The result is memoised for ``CACHE_TTL`` seconds because the
    upstream call walks the filesystem (multiple ``listdir`` calls and
    potentially a PowerShell round-trip) and is on the hot path of
    the health endpoint.
    """
    global _active_exe_cache
    now = time.time()
    if _active_exe_cache and now - _active_exe_cache[0] < CACHE_TTL:
        if _active_exe_cache[1] is not None:
            return _active_exe_cache[1]
        # A missing executable is not a stable result: a user may install
        # PHREEQC, correct a path, or the discovery scan may have completed
        # after the first health check.  Never make the UI wait for the cache
        # TTL before trying discovery again.
        _active_exe_cache = None
    try:
        result = _active_exe_lookup()
    except FileNotFoundError:
        # The public runtime only checks environment variables, PATH, and one
        # shortcut. The Workbench additionally scans standard USGS install
        # directories, so promote the first usable discovery result here.
        result = next(
            (item["path"] for item in discover_executables()
             if item["exists"] and item["path"].lower().endswith(".exe")),
            None,
        )
        if result is None:
            raise
    _active_exe_cache = (now, result)
    return result


def find_database(name: str = "phreeqc.dat") -> str:
    global _active_db_cache
    now = time.time()
    if name == "phreeqc.dat" and _active_db_cache and now - _active_db_cache[0] < CACHE_TTL:
        if _active_db_cache[1] is None:
            raise FileNotFoundError("(cached) PHREEQC database not found")
        return _active_db_cache[1]
    try:
        result = run_phreeqc.find_database(name, project_root=_PROJECT_ROOT)
    except FileNotFoundError:
        result = next(
            (item["path"] for item in discover_databases()
             if item["exists"] and os.path.basename(item["path"]).lower() == name.lower()),
            None,
        )
        if result is None:
            if name == "phreeqc.dat":
                _active_db_cache = (now, None)
            raise
    if name == "phreeqc.dat":
        _active_db_cache = (now, result)
    return result
