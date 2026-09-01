"""
External-run importer + directory watcher.

Users can run PHREEQC by hand (writing their own ``.pqi``, invoking
``phreeqc.exe`` from the command line, etc.).  When the workbench is
running it can optionally *watch* one or more directories and import
any new ``input.pqi`` / ``output.qpo`` pair it finds into the
workspace as an "imported" run, so the user does not have to
re-enter the simulation through the UI to inspect the result.

Design constraints
------------------

* The workbench must not interfere when it is *not* running.  The
  watcher only operates while the server process is alive, and it
  only watches directories the user has explicitly configured.
* Zero new dependencies.  We poll with ``os.scandir`` instead of
  pulling in ``watchdog``.
* Idempotent.  We record the *content hash* of every imported
  ``.pqi`` and skip duplicates, so re-scans are safe.
* The imported run participates in the rest of the workbench
  machinery (file download, results.json, charts tab) but cannot be
  re-started or aborted.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import threading
import time
from typing import Any

from services import storage  # noqa: E402

# ---------------------------------------------------------------------------
# Watcher state (single instance, process-global)
# ---------------------------------------------------------------------------

_lock = threading.RLock()
_watch_dirs: list[str] = []
_seen_hashes: set[str] = set()        # hashes of .pqi we have already imported
_thread: threading.Thread | None = None
_stop_flag = threading.Event()
_last_scan: float = 0.0
_scan_count: int = 0
imported_count: int = 0
SCAN_INTERVAL = 5.0  # seconds between polls

_PQI_RE = re.compile(r"^(?P<stem>.+)\.pqi$", re.IGNORECASE)
_QPO_RE = re.compile(r"^(?P<stem>.+)\.qpo$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def configure(dirs: list[str]) -> list[str]:
    """Replace the watch-dir list with the given (absolute) directories.

    Directories that do not exist are created.  Returns the canonical
    (absolute) list actually being watched.
    """
    global _watch_dirs
    canonical: list[str] = []
    with _lock:
        for d in dirs:
            d = d.strip()
            if not d:
                continue
            try:
                abs_d = os.path.abspath(d)
                os.makedirs(abs_d, exist_ok=True)
                canonical.append(abs_d)
            except OSError:
                continue
        _watch_dirs = canonical
    return canonical


def list_watch_dirs() -> list[str]:
    with _lock:
        return list(_watch_dirs)


def status() -> dict[str, Any]:
    with _lock:
        running = _thread is not None and _thread.is_alive() and not _stop_flag.is_set()
    return {
        "running": running,
        "watch_dirs": list_watch_dirs(),
        "last_scan_at": _last_scan or None,
        "scan_count": _scan_count,
        "imported_count": imported_count,
    }


def start() -> bool:
    """Start the background polling thread.  No-op if already running."""
    global _thread
    with _lock:
        if _thread is not None and _thread.is_alive() and not _stop_flag.is_set():
            return True
        _stop_flag.clear()
        _thread = threading.Thread(target=_loop, name="workbench-importer",
                                   daemon=True)
        _thread.start()
    return True


def stop() -> None:
    """Signal the polling thread to stop (does not block)."""
    _stop_flag.set()


def scan_once() -> list[str]:
    """Synchronously scan all watch dirs; returns the run_ids imported."""
    with _lock:
        dirs = list(_watch_dirs)
    new_run_ids: list[str] = []
    for d in dirs:
        try:
            entries = list(os.scandir(d))
        except OSError:
            continue
        # Build {stem: {"pqi": ..., "qpo": ..., "txt": ...}} so we can
        # match .pqi + .qpo pairs.  We only collect a .txt next to a
        # .pqi/.qpo as a candidate SELECTED_OUTPUT dump.
        by_stem: dict[str, dict[str, str]] = {}
        for e in entries:
            if not e.is_file():
                continue
            mp = _PQI_RE.match(e.name)
            mq = _QPO_RE.match(e.name)
            if not (mp or mq):
                continue
            stem = (mp or mq).group("stem")
            ext = "pqi" if mp else "qpo"
            slot = by_stem.setdefault(stem, {})
            slot[ext] = e.path
            # Look for a sibling <stem>.txt (e.g. selected_output.txt)
            txt_path = os.path.join(d, stem + ".txt")
            if os.path.isfile(txt_path):
                slot["txt"] = txt_path
        for stem, files in by_stem.items():
            pqi = files.get("pqi")
            qpo = files.get("qpo")
            if not pqi or not qpo:
                continue
            # Skip if the qpo is empty or older than the pqi (still
            # being written) -- wait for a "settled" file pair.
            try:
                pqi_mtime = os.path.getmtime(pqi)
                qpo_mtime = os.path.getmtime(qpo)
                if qpo_mtime < pqi_mtime:
                    continue
                if os.path.getsize(qpo) == 0:
                    continue
            except OSError:
                continue
            try:
                rid = _import_pair(pqi, qpo, files.get("txt"))
            except Exception:  # noqa: BLE001
                continue
            if rid:
                new_run_ids.append(rid)
    if new_run_ids:
        global imported_count
        with _lock:
            imported_count += len(new_run_ids)
    return new_run_ids


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------

def _loop() -> None:
    global _last_scan, _scan_count
    # Prime the seen-hash cache from runs we already imported in earlier
    # sessions.  We only need to scan existing run dirs once.
    _prime_seen_hashes()
    while not _stop_flag.is_set():
        try:
            scan_once()
        except Exception:  # noqa: BLE001
            pass
        with _lock:
            _last_scan = time.time()
            _scan_count += 1
        # Sleep in small slices so stop() reacts quickly.
        for _ in range(int(SCAN_INTERVAL * 10)):
            if _stop_flag.is_set():
                return
            time.sleep(0.1)


def _prime_seen_hashes() -> None:
    """Populate ``_seen_hashes`` from already-imported run directories."""
    root = storage.workspace_root()
    if not os.path.isdir(root):
        return
    for entry in os.listdir(root):
        run_dir = os.path.join(root, entry)
        if not os.path.isdir(run_dir):
            continue
        meta_p = os.path.join(run_dir, "meta.json")
        if not os.path.isfile(meta_p):
            continue
        try:
            import json
            with open(meta_p, encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, ValueError):
            continue
        if meta.get("source") != "imported":
            continue
        h = meta.get("source_hash")
        if isinstance(h, str):
            _seen_hashes.add(h)


def _file_hash(path: str) -> str:
    h = hashlib.sha1()
    try:
        size = os.path.getsize(path)
    except OSError:
        size = 0
    h.update(size.to_bytes(8, "big"))
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError:
        pass
    return h.hexdigest()


def _import_pair(pqi_path: str, qpo_path: str,
                 sel_path: str | None) -> str | None:
    """Create a workbench run from an external ``.pqi`` / ``.qpo`` pair.

    Returns the new run_id, or ``None`` if the pair was already
    imported (deduped by content hash).
    """
    h = _file_hash(pqi_path)
    with _lock:
        if h in _seen_hashes:
            return None
        _seen_hashes.add(h)

    # Use the .pqi stem (sanitised) as the run id; if it collides, fall
    # back to a generated id.
    stem = os.path.splitext(os.path.basename(pqi_path))[0]
    run_id = re.sub(r"[^A-Za-z0-9_-]", "_", stem)[:48] or storage.gen_run_id()
    if not re.match(r"^[a-zA-Z0-9_\-]{1,64}$", run_id):
        run_id = storage.gen_run_id()

    # If a run with this id already exists, append a suffix.
    if storage.get_run(run_id) is not None:
        run_id = storage.gen_run_id()

    # Copy the files into the run dir so the rest of the workbench
    # (results tab, charts, file download) sees a uniform layout.
    params = {"source": "imported", "original_pqi": pqi_path, "original_qpo": qpo_path}
    meta = storage.create_run(run_id, display_name=stem or run_id, params=params)
    # Patch the meta with the content hash + source marker.
    _patch_meta(run_id, {
        "source": "imported",
        "source_hash": h,
        "source_pqi": pqi_path,
        "source_qpo": qpo_path,
        "source_selected": sel_path,
    })
    storage.set_status(run_id, "succeeded")

    try:
        with open(pqi_path, encoding="utf-8", errors="replace") as f:
            pqi_text = f.read()
        storage.write_artifact(run_id, "input.pqi", pqi_text)
    except OSError:
        pass
    try:
        with open(qpo_path, encoding="utf-8", errors="replace") as f:
            qpo_text = f.read()
        storage.write_artifact(run_id, "output.qpo", qpo_text)
    except OSError:
        pass
    if sel_path and os.path.isfile(sel_path):
        try:
            with open(sel_path, encoding="utf-8", errors="replace") as f:
                sel_text = f.read()
            storage.write_artifact(run_id, "selected_output.txt", sel_text)
        except OSError:
            pass

    # Best-effort parse the same way the runner does.
    try:
        from services import runner  # type: ignore
        runner._parse_into(run_id, qpo_path, sel_path)
    except Exception:  # noqa: BLE001
        pass

    storage.append_event(run_id, {
        "kind": "imported",
        "message": f"Imported from {pqi_path}",
        "ts": time.time(),
    })
    storage.append_log(run_id, f"[imported] source: {pqi_path}")
    return run_id


def _patch_meta(run_id: str, patch: dict[str, Any]) -> None:
    """Merge ``patch`` into meta.json (best-effort)."""
    import json
    p = os.path.join(storage.workspace_root(), run_id, "meta.json")
    if not os.path.isfile(p):
        return
    try:
        with _lock:
            with open(p, encoding="utf-8") as f:
                meta = json.load(f)
            meta.update(patch)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
    except OSError:
        pass
