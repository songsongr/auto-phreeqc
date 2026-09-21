"""
Workspace storage service for the Workbench.

Owns the on-disk layout of workbench runs. Each run is a directory under
``workspace_root/<run_id>/`` with the following files:

    meta.json           -- run metadata (status, params, timestamps, log tail)
    input.pqi           -- generated PHREEQC input (only after generation)
    output.qpo          -- PHREEQC stdout (only after run)
    selected_output.txt -- SELECTED_OUTPUT dump (only after run)
    results.json        -- parsed structured results (only after parsing)
    charts/             -- visualization PNGs (only after visualization)
    events.log          -- JSONL event log streamed to SSE clients
"""

from __future__ import annotations

import json
import os
import re
import shutil
import threading
import time
import uuid
from typing import Any


_run_lock = threading.RLock()
_workspace_root: str | None = None


def init(workspace_root: str | None = None) -> None:
    """Initialize the storage service. Idempotent."""
    global _workspace_root
    if workspace_root is None:
        # Default: <repo-root>/workbench/workspace_workbench/.
        # We anchor on the process cwd (set by the launcher to the repo root)
        # so the same default applies whether invoked from the repo root or
        # from workbench/ directly.
        workspace_root = os.path.join(
            os.getcwd(), "workbench", "workspace_workbench",
        )
    workspace_root = os.path.abspath(workspace_root)
    os.makedirs(workspace_root, exist_ok=True)
    _workspace_root = workspace_root


def workspace_root() -> str:
    if _workspace_root is None:
        init()
    assert _workspace_root is not None
    return _workspace_root


def _run_dir(run_id: str) -> str:
    return os.path.join(workspace_root(), run_id)


def _meta_path(run_id: str) -> str:
    return os.path.join(_run_dir(run_id), "meta.json")


def _events_path(run_id: str) -> str:
    return os.path.join(_run_dir(run_id), "events.log")


_VALID_RUN_ID = re.compile(r"^[a-zA-Z0-9_\-]{1,64}$")


def gen_run_id() -> str:
    return "run_" + uuid.uuid4().hex[:10]


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def create_run(
    run_id: str, *, display_name: str, params: dict, description: str = ""
) -> dict:
    if not _VALID_RUN_ID.match(run_id):
        raise ValueError(
            f"Invalid run id: {run_id!r}. Use 1-64 chars [a-zA-Z0-9_-]."
        )
    with _run_lock:
        run_dir = _run_dir(run_id)
        if os.path.isdir(run_dir):
            raise ValueError(f"Run already exists: {run_id}")
        os.makedirs(run_dir, exist_ok=True)
        os.makedirs(os.path.join(run_dir, "charts"), exist_ok=True)
        meta = {
            "run_id": run_id,
            "name": display_name,
            "description": description.strip(),
            "params": params,
            "status": "created",
            "created_at": time.time(),
            "updated_at": time.time(),
            "log_tail": [],
        }
        with open(_meta_path(run_id), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        # Initialize empty event log
        open(_events_path(run_id), "w", encoding="utf-8").close()
        return meta


def get_run(run_id: str) -> dict | None:
    p = _meta_path(run_id)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        meta = json.load(f)
    # Always recompute status if a run is "running" but the process is gone
    return meta


def set_status(run_id: str, status: str) -> None:
    p = _meta_path(run_id)
    if not os.path.isfile(p):
        return
    with _run_lock:
        with open(p, encoding="utf-8") as f:
            meta = json.load(f)
        meta["status"] = status
        meta["updated_at"] = time.time()
        with open(p, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)


def append_log(run_id: str, line: str) -> None:
    """Append a log line to meta.json (keeps last 200)."""
    p = _meta_path(run_id)
    if not os.path.isfile(p):
        return
    with _run_lock:
        with open(p, encoding="utf-8") as f:
            meta = json.load(f)
        tail = meta.get("log_tail", [])
        tail.append(line)
        meta["log_tail"] = tail[-200:]
        meta["updated_at"] = time.time()
        with open(p, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)


def set_result_summary(run_id: str, summary: dict) -> None:
    p = _meta_path(run_id)
    if not os.path.isfile(p):
        return
    with _run_lock:
        with open(p, encoding="utf-8") as f:
            meta = json.load(f)
        meta["result_summary"] = summary
        meta["updated_at"] = time.time()
        with open(p, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)


def list_runs() -> list[dict]:
    root = workspace_root()
    if not os.path.isdir(root):
        return []
    items: list[dict] = []
    for entry in sorted(os.listdir(root), reverse=True):
        run_dir = os.path.join(root, entry)
        if not os.path.isdir(run_dir):
            continue
        meta_p = os.path.join(run_dir, "meta.json")
        if not os.path.isfile(meta_p):
            continue
        try:
            with open(meta_p, encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        items.append({
            "run_id": meta.get("run_id", entry),
            "name": meta.get("name", entry),
            "description": meta.get("description", ""),
            "status": meta.get("status", "unknown"),
            "created_at": meta.get("created_at"),
            "updated_at": meta.get("updated_at"),
        })
    return items


def delete_run(run_id: str) -> bool:
    run_dir = _run_dir(run_id)
    if not os.path.isdir(run_dir):
        return False
    with _run_lock:
        shutil.rmtree(run_dir, ignore_errors=True)
    return True


# ---------------------------------------------------------------------------
# Artifact I/O
# ---------------------------------------------------------------------------

def _safe_relpath(name: str) -> str | None:
    """Validate a relative artifact path. Returns the cleaned form or None.

    Allows forward slashes for subdirectories (e.g. ``charts/foo.png``)
    but rejects any traversal attempt (``..``, absolute paths).
    """
    name = name.replace("\\", "/")
    if not name or name.startswith("/") or name.startswith("../") or "/../" in name or name.endswith("/..") or name == "..":
        return None
    # Reject Windows drive letters
    if len(name) >= 2 and name[1] == ":":
        return None
    return name


def write_artifact(run_id: str, name: str, content: str) -> str:
    """Write a text artifact into the run directory. Returns the absolute path."""
    rel = _safe_relpath(name)
    if rel is None:
        raise ValueError(f"Invalid artifact name: {name!r}")
    run_dir = _run_dir(run_id)
    os.makedirs(run_dir, exist_ok=True)
    full = os.path.join(run_dir, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return full


def write_binary_artifact(run_id: str, name: str, data: bytes) -> str:
    rel = _safe_relpath(name)
    if rel is None:
        raise ValueError(f"Invalid artifact name: {name!r}")
    run_dir = _run_dir(run_id)
    os.makedirs(run_dir, exist_ok=True)
    full = os.path.join(run_dir, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f:
        f.write(data)
    return full


def read_artifact(run_id: str, name: str) -> str | None:
    rel = _safe_relpath(name)
    if rel is None:
        return None
    full = os.path.join(_run_dir(run_id), rel.replace("/", os.sep))
    if not os.path.isfile(full):
        return None
    try:
        with open(full, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def read_artifact_preview(
    run_id: str, name: str, *, max_chars: int = 200_000
) -> tuple[str | None, int]:
    """Read at most ``max_chars`` from a text artifact and report its byte size.

    Large PHREEQC output files can contain many megabytes of transport-step
    diagnostics.  The UI uses this bounded reader instead of rendering the
    entire file in one browser DOM node.
    """
    rel = _safe_relpath(name)
    if rel is None:
        return None, 0
    full = os.path.join(_run_dir(run_id), rel.replace("/", os.sep))
    if not os.path.isfile(full):
        return None, 0
    try:
        size = os.path.getsize(full)
        with open(full, encoding="utf-8", errors="replace") as f:
            return f.read(max_chars), size
    except OSError:
        return None, 0


def read_binary_artifact(run_id: str, name: str) -> tuple[bytes | None, str]:
    rel = _safe_relpath(name)
    if rel is None:
        return None, "application/octet-stream"
    full = os.path.join(_run_dir(run_id), rel.replace("/", os.sep))
    if not os.path.isfile(full):
        return None, "application/octet-stream"
    import mimetypes
    ctype, _ = mimetypes.guess_type(full)
    if ctype is None:
        ctype = "application/octet-stream"
    with open(full, "rb") as f:
        return f.read(), ctype


def list_artifacts(run_id: str) -> list[dict] | None:
    run_dir = _run_dir(run_id)
    if not os.path.isdir(run_dir):
        return None
    items: list[dict] = []
    for root, _, files in os.walk(run_dir):
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, run_dir).replace(os.sep, "/")
            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0
            items.append({"path": rel, "size": size})
    items.sort(key=lambda x: x["path"])
    return items


# ---------------------------------------------------------------------------
# Event log (JSONL, consumed by SSE clients)
# ---------------------------------------------------------------------------

def append_event(run_id: str, event: dict) -> None:
    p = _events_path(run_id)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def consume_events(run_id: str) -> list[dict] | None:
    """Return all events currently in the log (one-shot SSE delivery).

    The client is expected to call this endpoint periodically; missing
    events between calls are lost (this is a simple polling model, not
    long-lived push).  The endpoint stays open until the client
    disconnects or the run terminates.
    """
    p = _events_path(run_id)
    if not os.path.isfile(p):
        return None
    events: list[dict] = []
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return None
    return events
