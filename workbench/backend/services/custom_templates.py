"""User-saved custom scenarios for the Workbench custom-simulation page.

A saved custom template is a normalised Scenario v1 document plus the
bookkeeping the list view needs.  Records are kept in a single JSON file in
the workspace root (next to ``workbench.json``) so they survive a server
restart and stay out of version control, exactly like the runs themselves.

Reading a corrupt or hand-edited file must never take the server down: this
module degrades to "no saved templates" and reports write errors to the
caller.
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid
from typing import Any

from services import scenarios


# Guard rails for a local, single-user store.
MAX_TEMPLATES = 200
MAX_NAME_LENGTH = 128

_lock = threading.RLock()
_store_path: str | None = None


def init(workspace_root: str | None = None) -> None:
    """Pin the store location for this process.  Idempotent."""

    global _store_path
    if workspace_root is None:
        from services import storage  # local import avoids an import cycle

        root = storage.workspace_root()
    else:
        root = os.path.abspath(workspace_root)
    _store_path = os.path.join(root, "custom_templates.json")


def _path() -> str:
    if _store_path is None:
        init()
    assert _store_path is not None
    return _store_path


def _load() -> list[dict[str, Any]]:
    path = _path()
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    return [
        record for record in data
        if isinstance(record, dict) and isinstance(record.get("id"), str)
        and isinstance(record.get("scenario"), dict)
    ]


def _flush(records: list[dict[str, Any]]) -> None:
    """Write the store atomically so a crash cannot truncate it."""

    path = _path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _summary(record: dict[str, Any]) -> dict[str, Any]:
    scenario = record["scenario"]
    return {
        "id": record["id"],
        "name": record.get("name") or scenario.get("name") or record["id"],
        "scenario_type": scenario.get("scenario_type", ""),
        "modules": sorted(scenario.get("modules", {}).keys()),
        "description": scenario.get("description", ""),
        "created_at": record.get("created_at"),
        "updated_at": record.get("updated_at"),
    }


def list_templates() -> list[dict[str, Any]]:
    with _lock:
        records = _load()
    records.sort(key=lambda item: item.get("updated_at") or 0, reverse=True)
    return [_summary(record) for record in records]


def get_template(template_id: str) -> dict[str, Any] | None:
    with _lock:
        for record in _load():
            if record["id"] == template_id:
                return record
    return None


def save_template(scenario: Any, *, template_id: str | None = None) -> dict[str, Any]:
    """Validate, normalise, and persist a scenario.

    Raises :class:`scenarios.ScenarioValidationError` when the scenario is not
    valid; the caller can surface ``exc.result`` to the UI unchanged.
    """

    validation = scenarios.validate_scenario(scenario)
    if not validation["valid"]:
        raise scenarios.ScenarioValidationError(validation)

    normalised = validation["scenario"]
    name = (normalised.get("name") or "").strip()
    if not name:
        raise ValueError("场景名称不能为空。")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"场景名称最多 {MAX_NAME_LENGTH} 个字符。")

    now = time.time()
    with _lock:
        records = _load()
        existing = next(
            (record for record in records if template_id and record["id"] == template_id),
            None,
        )
        if existing is None and len(records) >= MAX_TEMPLATES:
            raise ValueError(f"自定义模板数量已达上限（{MAX_TEMPLATES}）。")
        record = {
            "id": existing["id"] if existing else "custom_" + uuid.uuid4().hex[:10],
            "name": name,
            "created_at": existing.get("created_at") if existing else now,
            "updated_at": now,
            "scenario": normalised,
        }
        if existing:
            records[records.index(existing)] = record
        else:
            records.append(record)
        _flush(records)
    return record


def delete_template(template_id: str) -> bool:
    with _lock:
        records = _load()
        remaining = [record for record in records if record["id"] != template_id]
        if len(remaining) == len(records):
            return False
        _flush(remaining)
    return True
