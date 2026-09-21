"""Versioned custom-scenario validation, compilation, and input preview.

The Workbench runner predates the custom-model UI and consumes a flat
``params`` dictionary.  This module deliberately keeps the UI-facing scenario
format separate from that legacy contract:

``Scenario v1 -> validate/normalise -> legacy params -> existing generator``.

Keeping the adapter here makes the first custom-scenario release additive: the
nine built-in templates and their saved runs keep using the exact same runner
path as before.
"""

from __future__ import annotations

import copy
import json
import math
import os
from typing import Any


SCHEMA_VERSION = 1

# These limits are deliberately conservative.  They protect the local
# Workbench from accidentally creating a very large PHREEQC job while keeping
# normal educational and exploratory models comfortably in range.
MAX_SOLUTIONS = 50
MAX_COMPONENTS = 100
MAX_PHASES = 50
MAX_REACTANTS = 50
MAX_SELECTED_OUTPUT_ITEMS = 100
MAX_TRANSPORT_CELLS = 100
MAX_TRANSPORT_SHIFTS = 1_000
MAX_TRANSPORT_CELL_SHIFTS = 10_000

_ALLOWED_UNITS = {
    "mol/kgw",
    "mmol/kgw",
    "umol/kgw",
    "mol/l",
    "mmol/l",
    "umol/l",
    "mg/l",
    "ug/l",
    "ppm",
    "ppb",
}
_UNIT_CANONICAL = {unit.lower(): unit for unit in _ALLOWED_UNITS}
_FLOW_DIRECTIONS = {"forward", "backward", "diffusion_only"}
_TIME_UNITS = {"second", "seconds", "minute", "minutes", "hour", "hours", "day", "days", "year", "years"}


class ScenarioValidationError(ValueError):
    """Raised by :func:`compile_scenario` when a scenario is not valid."""

    def __init__(self, result: dict[str, Any]):
        self.result = result
        super().__init__("Scenario validation failed")


def _solution(solution_id: int = 1) -> dict[str, Any]:
    return {
        "id": solution_id,
        "units": "mol/kgw",
        "temp": 25.0,
        "pH": 7.0,
        "pe": 4.0,
        "density": 1.0,
        "components": {},
    }


def _base_scenario(name: str, scenario_type: str, modules: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "name": name,
        "scenario_type": scenario_type,
        "modules": modules,
    }


# The front end renders this public registry.  ``default_scenario`` values are
# intentionally minimal, but all are structurally valid and can be previewed
# without having to start from raw JSON.
_SCENARIO_TYPES: dict[str, dict[str, Any]] = {
    "speciation": {
        "label": "水化学形态分析",
        "label_en": "Aqueous speciation",
        "description": "计算单个水溶液的物种分布和饱和指数。",
        "description_en": "Speciate one aqueous solution and report saturation indices.",
        "allowed_modules": ("solutions", "selected_output"),
        "required_modules": ("solutions",),
        "default_scenario": _base_scenario(
            "未命名水化学形态分析",
            "speciation",
            {"solutions": [_solution()], "selected_output": {"pH": True, "pe": True}},
        ),
    },
    "equilibrium": {
        "label": "相平衡",
        "label_en": "Phase equilibrium",
        "description": "让水溶液与一个或多个矿物或气体相达到平衡。",
        "description_en": "Equilibrate a solution with one or more mineral or gas phases.",
        "allowed_modules": ("solutions", "equilibrium_phases", "selected_output"),
        "required_modules": ("solutions", "equilibrium_phases"),
        "default_scenario": _base_scenario(
            "未命名相平衡模拟",
            "equilibrium",
            {
                "solutions": [_solution()],
                "equilibrium_phases": {"Calcite": [0.0, 10.0]},
                "selected_output": {"pH": True, "si": ["Calcite"]},
            },
        ),
    },
    "mixing": {
        "label": "溶液混合",
        "label_en": "Solution mixing",
        "description": "按指定比例混合多个已定义溶液。",
        "description_en": "Mix several defined solutions in given proportions.",
        "allowed_modules": ("solutions", "mix", "selected_output"),
        "required_modules": ("solutions", "mix"),
        "default_scenario": _base_scenario(
            "未命名溶液混合模拟",
            "mixing",
            {
                "solutions": [_solution(1), _solution(2)],
                "mix": {"id": 1, "solutions": {"1": 0.5, "2": 0.5}},
                "selected_output": {"pH": True, "pe": True},
            },
        ),
    },
    "reaction_path": {
        "label": "反应路径 / 滴定",
        "label_en": "Reaction path / titration",
        "description": "逐步加入反应物，观察水化学状态随反应进程的变化。",
        "description_en": "Add a reactant stepwise and track the solution along the path.",
        "allowed_modules": ("solutions", "equilibrium_phases", "reaction", "selected_output"),
        "required_modules": ("solutions", "reaction"),
        "default_scenario": _base_scenario(
            "未命名反应路径模拟",
            "reaction_path",
            {
                "solutions": [_solution()],
                "reaction": {"reactants": {"NaCl": 1.0}, "moles": 0.001, "steps": 10},
                "selected_output": {"step": True, "pH": True, "pe": True},
            },
        ),
    },
    "gas_equilibrium": {
        "label": "气液平衡",
        "label_en": "Gas equilibrium",
        "description": "模拟水溶液与固定压力或固定体积气相之间的平衡。",
        "description_en": "Equilibrate a solution with a fixed-pressure or fixed-volume gas phase.",
        "allowed_modules": ("solutions", "gas_phase", "equilibrium_phases", "selected_output"),
        "required_modules": ("solutions", "gas_phase"),
        "default_scenario": _base_scenario(
            "未命名气液平衡模拟",
            "gas_equilibrium",
            {
                "solutions": [_solution()],
                "gas_phase": {
                    "fixed_pressure": True,
                    "pressure": 1.0,
                    "components": {"CO2(g)": 0.0},
                },
                "selected_output": {"pH": True, "pe": True},
            },
        ),
    },
    "transport": {
        "label": "反应性运移（高级）",
        "label_en": "Reactive transport (advanced)",
        "description": "一维平流-弥散反应性运移；运行前会限制单元数和时间步数。",
        "description_en": "One-dimensional advective-dispersive transport; cell and shift counts are capped.",
        "allowed_modules": (
            "solutions",
            "initial_cell_solution",
            "transport",
            "equilibrium_phases",
            "selected_output",
        ),
        "required_modules": ("solutions", "initial_cell_solution", "transport"),
        "default_scenario": _base_scenario(
            "未命名反应性运移模拟",
            "transport",
            {
                "solutions": [_solution(0)],
                "initial_cell_solution": {
                    "units": "mol/kgw",
                    "temp": 25.0,
                    "pH": 7.0,
                    "pe": 4.0,
                    "density": 1.0,
                    "components": {},
                },
                "transport": {
                    "cells": 10,
                    "length": 1.0,
                    "shifts": 10,
                    "time_step": 0.05,
                    "time_units": "day",
                    "flow_direction": "forward",
                    "dispersivity": 0.0,
                    "punch_cells": [10],
                    "punch_frequency": 1,
                },
                "selected_output": {"step": True, "pH": True, "pe": True},
            },
        ),
    },
}


def list_scenario_types() -> list[dict[str, Any]]:
    """Return the UI-safe scenario-type registry with fresh defaults."""

    return [
        {
            "id": type_id,
            "label": config["label"],
            "label_en": config["label_en"],
            "description": config["description"],
            "description_en": config["description_en"],
            "allowed_modules": list(config["allowed_modules"]),
            "required_modules": list(config["required_modules"]),
            "default_scenario": copy.deepcopy(config["default_scenario"]),
        }
        for type_id, config in _SCENARIO_TYPES.items()
    ]


def list_modules() -> list[dict[str, Any]]:
    """Return the module registry with a fresh copy of each default value.

    The defaults are harvested from the scenario-type skeletons above so the
    registry cannot drift from the definitions the UI is allowed to start
    from.
    """

    modules: dict[str, Any] = {}
    for config in _SCENARIO_TYPES.values():
        for name, default in config["default_scenario"]["modules"].items():
            modules.setdefault(name, copy.deepcopy(default))
    return [{"id": name, "default": default} for name, default in modules.items()]


def get_default_scenario(scenario_type: str) -> dict[str, Any] | None:
    """Return a deep copy of one type's default scenario, if it exists."""

    config = _SCENARIO_TYPES.get(scenario_type)
    return copy.deepcopy(config["default_scenario"]) if config else None


def _error(errors: list[dict[str, str]], path: str, code: str, message: str) -> None:
    errors.append({"path": path, "code": code, "message": message})


def _warning(warnings: list[dict[str, str]], path: str, message: str) -> None:
    warnings.append({"path": path, "message": message})


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _normalise_number(
    value: Any,
    *,
    path: str,
    errors: list[dict[str, str]],
    minimum: float | None = None,
    maximum: float | None = None,
    default: float | None = None,
) -> float | None:
    if value is None and default is not None:
        return float(default)
    if not _is_number(value):
        _error(errors, path, "INVALID_NUMBER", "必须是有限数值。")
        return None
    number = float(value)
    if minimum is not None and number < minimum:
        _error(errors, path, "NUMBER_TOO_SMALL", f"必须大于或等于 {minimum}。")
    if maximum is not None and number > maximum:
        _error(errors, path, "NUMBER_TOO_LARGE", f"必须小于或等于 {maximum}。")
    return number


def _normalise_int(
    value: Any,
    *,
    path: str,
    errors: list[dict[str, str]],
    minimum: int | None = None,
    maximum: int | None = None,
    default: int | None = None,
) -> int | None:
    if value is None and default is not None:
        return default
    if not isinstance(value, int) or isinstance(value, bool):
        _error(errors, path, "INVALID_INTEGER", "必须是整数。")
        return None
    if minimum is not None and value < minimum:
        _error(errors, path, "INTEGER_TOO_SMALL", f"必须大于或等于 {minimum}。")
    if maximum is not None and value > maximum:
        _error(errors, path, "INTEGER_TOO_LARGE", f"必须小于或等于 {maximum}。")
    return value


def _normalise_bool(
    value: Any,
    *,
    path: str,
    errors: list[dict[str, str]],
    default: bool | None = None,
) -> bool | None:
    if value is None and default is not None:
        return default
    if not isinstance(value, bool):
        _error(errors, path, "INVALID_BOOLEAN", "必须是 true 或 false。")
        return None
    return value


def _normalise_text(
    value: Any,
    *,
    path: str,
    errors: list[dict[str, str]],
    required: bool = True,
    max_length: int = 128,
) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str):
        _error(errors, path, "INVALID_TEXT", "必须是文本。")
        return None
    text = value.strip()
    if required and not text:
        _error(errors, path, "EMPTY_TEXT", "不能为空。")
    if len(text) > max_length:
        _error(errors, path, "TEXT_TOO_LONG", f"最多允许 {max_length} 个字符。")
    # The generator writes names and selected-output items into line-oriented
    # PHREEQC input.  Reject line controls and PHREEQC line/comment separators
    # rather than accepting a value that can inject an unintended block.
    if any(ord(char) < 32 for char in text) or any(char in text for char in (";", "#", "\\")):
        _error(errors, path, "UNSAFE_TEXT", "不能包含换行、控制字符或 PHREEQC 行分隔符。")
    return text


def _check_fields(
    raw: dict[str, Any],
    allowed: set[str],
    *,
    path: str,
    errors: list[dict[str, str]],
) -> None:
    for key in raw:
        if key not in allowed:
            _error(errors, f"{path}.{key}", "UNKNOWN_FIELD", "此字段不受当前场景架构支持。")


def _normalise_components(value: Any, *, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        _error(errors, path, "INVALID_COMPONENTS", "组分必须是名称到浓度的对象。")
        return {}
    if len(value) > MAX_COMPONENTS:
        _error(errors, path, "TOO_MANY_COMPONENTS", f"最多允许 {MAX_COMPONENTS} 个组分。")
    components: dict[str, Any] = {}
    for raw_name, raw_amount in value.items():
        name = _normalise_text(raw_name, path=f"{path}.{raw_name}", errors=errors, max_length=96)
        if name is None:
            continue
        if _is_number(raw_amount):
            amount = float(raw_amount)
            if amount < 0:
                _error(errors, f"{path}.{raw_name}", "NEGATIVE_CONCENTRATION", "浓度不能为负数。")
            components[name] = amount
        elif isinstance(raw_amount, str):
            amount_text = _normalise_text(
                raw_amount,
                path=f"{path}.{raw_name}",
                errors=errors,
                max_length=128,
            )
            if amount_text is not None:
                components[name] = amount_text
        else:
            _error(errors, f"{path}.{raw_name}", "INVALID_CONCENTRATION", "浓度必须是有限数值或安全的 PHREEQC 文本值。")
    return components


def _normalise_solution(
    raw: Any,
    *,
    path: str,
    errors: list[dict[str, str]],
    default_id: int | None = None,
    include_id: bool = True,
) -> dict[str, Any]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_SOLUTION", "溶液必须是对象。")
        return {}
    allowed = {"units", "temp", "pH", "pe", "density", "components"}
    if include_id:
        allowed.add("id")
    _check_fields(raw, allowed, path=path, errors=errors)

    solution: dict[str, Any] = {}
    if include_id:
        solution_id = _normalise_int(
            raw.get("id"),
            path=f"{path}.id",
            errors=errors,
            minimum=0,
            maximum=9_999,
            default=default_id,
        )
        if solution_id is not None:
            solution["id"] = solution_id

    units_raw = raw.get("units", "mol/kgw")
    units_text = _normalise_text(units_raw, path=f"{path}.units", errors=errors, max_length=16)
    if units_text is not None:
        units = _UNIT_CANONICAL.get(units_text.lower())
        if units is None:
            allowed_units = ", ".join(sorted(_ALLOWED_UNITS))
            _error(errors, f"{path}.units", "UNSUPPORTED_UNIT", f"支持的单位：{allowed_units}。")
        else:
            solution["units"] = units

    for key, minimum, maximum, default in (
        ("temp", -273.15, 1_000.0, 25.0),
        ("pH", -20.0, 40.0, 7.0),
        ("pe", -100.0, 100.0, 4.0),
        ("density", 0.01, 5.0, 1.0),
    ):
        number = _normalise_number(
            raw.get(key),
            path=f"{path}.{key}",
            errors=errors,
            minimum=minimum,
            maximum=maximum,
            default=default,
        )
        if number is not None:
            solution[key] = number
    solution["components"] = _normalise_components(raw.get("components"), path=f"{path}.components", errors=errors)
    return solution


def _normalise_solutions(raw: Any, *, path: str, errors: list[dict[str, str]]) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        _error(errors, path, "INVALID_SOLUTIONS", "solutions 必须是数组。")
        return []
    if not raw:
        _error(errors, path, "EMPTY_SOLUTIONS", "至少需要定义一个溶液。")
    if len(raw) > MAX_SOLUTIONS:
        _error(errors, path, "TOO_MANY_SOLUTIONS", f"最多允许 {MAX_SOLUTIONS} 个显式溶液。")
    solutions = [
        _normalise_solution(item, path=f"{path}[{index}]", errors=errors, default_id=index + 1)
        for index, item in enumerate(raw)
    ]
    ids = [item.get("id") for item in solutions if "id" in item]
    seen: set[int] = set()
    for solution_id in ids:
        if solution_id in seen:
            _error(errors, path, "DUPLICATE_SOLUTION_ID", f"溶液编号 {solution_id} 重复。")
        seen.add(solution_id)
    return solutions


def _normalise_mix(raw: Any, *, path: str, errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_MIX", "mix 必须是对象。")
        return {}
    _check_fields(raw, {"id", "solutions"}, path=path, errors=errors)
    mix_id = _normalise_int(raw.get("id"), path=f"{path}.id", errors=errors, minimum=1, maximum=9_999, default=1)
    source_map = raw.get("solutions")
    if not isinstance(source_map, dict):
        _error(errors, f"{path}.solutions", "INVALID_MIX_SOURCES", "mix.solutions 必须是溶液编号到比例的对象。")
        source_map = {}
    if len(source_map) < 2:
        _error(errors, f"{path}.solutions", "TOO_FEW_MIX_SOURCES", "至少需要两个待混合溶液。")
    if len(source_map) > MAX_SOLUTIONS:
        _error(errors, f"{path}.solutions", "TOO_MANY_MIX_SOURCES", f"最多允许 {MAX_SOLUTIONS} 个混合来源。")

    sources: dict[str, float] = {}
    total = 0.0
    for raw_id, raw_fraction in source_map.items():
        try:
            source_id = int(raw_id)
        except (TypeError, ValueError):
            _error(errors, f"{path}.solutions.{raw_id}", "INVALID_SOLUTION_ID", "混合来源编号必须是整数。")
            continue
        if str(source_id) != str(raw_id) and not isinstance(raw_id, int):
            _error(errors, f"{path}.solutions.{raw_id}", "INVALID_SOLUTION_ID", "混合来源编号必须是整数文本。")
            continue
        if source_id < 0 or source_id > 9_999:
            _error(errors, f"{path}.solutions.{raw_id}", "INVALID_SOLUTION_ID", "混合来源编号超出范围。")
            continue
        fraction = _normalise_number(
            raw_fraction,
            path=f"{path}.solutions.{raw_id}",
            errors=errors,
            minimum=0.0,
        )
        if fraction is None:
            continue
        if fraction == 0:
            _error(errors, f"{path}.solutions.{raw_id}", "ZERO_MIX_FRACTION", "混合比例必须大于 0。")
        sources[str(source_id)] = fraction
        total += fraction
    if sources and not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        _warning(warnings, f"{path}.solutions", f"混合比例之和为 {total:g}，不会自动归一化。")
    result: dict[str, Any] = {"solutions": sources}
    if mix_id is not None:
        result["id"] = mix_id
    return result


def _normalise_equilibrium_phases(raw: Any, *, path: str, errors: list[dict[str, str]]) -> dict[str, list[float]]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_EQUILIBRIUM_PHASES", "equilibrium_phases 必须是相名到配置的对象。")
        return {}
    if not raw:
        _error(errors, path, "EMPTY_EQUILIBRIUM_PHASES", "至少需要定义一个平衡相。")
    if len(raw) > MAX_PHASES:
        _error(errors, path, "TOO_MANY_PHASES", f"最多允许 {MAX_PHASES} 个平衡相。")
    phases: dict[str, list[float]] = {}
    for raw_name, config in raw.items():
        name = _normalise_text(raw_name, path=f"{path}.{raw_name}", errors=errors, max_length=96)
        if name is None:
            continue
        saturation_index: Any = None
        amount: Any = None
        if isinstance(config, (list, tuple)) and len(config) == 2:
            saturation_index, amount = config
        elif isinstance(config, dict):
            _check_fields(config, {"saturation_index", "si", "amount"}, path=f"{path}.{raw_name}", errors=errors)
            saturation_index = config.get("saturation_index", config.get("si"))
            amount = config.get("amount")
        else:
            _error(errors, f"{path}.{raw_name}", "INVALID_PHASE_CONFIG", "相配置必须是 [饱和指数, 摩尔数] 或对象。")
            continue
        si_value = _normalise_number(
            saturation_index,
            path=f"{path}.{raw_name}.saturation_index",
            errors=errors,
            minimum=-1_000.0,
            maximum=1_000.0,
        )
        amount_value = _normalise_number(
            amount,
            path=f"{path}.{raw_name}.amount",
            errors=errors,
            minimum=-1_000_000_000.0,
            maximum=1_000_000_000.0,
        )
        if si_value is not None and amount_value is not None:
            phases[name] = [si_value, amount_value]
    return phases


def _normalise_reaction(raw: Any, *, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_REACTION", "reaction 必须是对象。")
        return {}
    _check_fields(raw, {"block_id", "reactants", "moles", "steps"}, path=path, errors=errors)
    raw_reactants = raw.get("reactants")
    if not isinstance(raw_reactants, dict):
        _error(errors, f"{path}.reactants", "INVALID_REACTANTS", "reactants 必须是反应物到系数的对象。")
        raw_reactants = {}
    if not raw_reactants:
        _error(errors, f"{path}.reactants", "EMPTY_REACTANTS", "至少需要一个反应物。")
    if len(raw_reactants) > MAX_REACTANTS:
        _error(errors, f"{path}.reactants", "TOO_MANY_REACTANTS", f"最多允许 {MAX_REACTANTS} 个反应物。")
    reactants: dict[str, float] = {}
    for raw_name, raw_coefficient in raw_reactants.items():
        name = _normalise_text(raw_name, path=f"{path}.reactants.{raw_name}", errors=errors, max_length=96)
        coefficient = _normalise_number(raw_coefficient, path=f"{path}.reactants.{raw_name}", errors=errors)
        if coefficient == 0:
            _error(errors, f"{path}.reactants.{raw_name}", "ZERO_REACTANT_COEFFICIENT", "反应物系数不能为 0。")
        if name is not None and coefficient is not None:
            reactants[name] = coefficient
    result: dict[str, Any] = {"reactants": reactants}
    block_id = _normalise_int(raw.get("block_id"), path=f"{path}.block_id", errors=errors, minimum=1, maximum=9_999, default=1)
    moles = _normalise_number(raw.get("moles"), path=f"{path}.moles", errors=errors, minimum=0.0, default=1.0)
    steps = _normalise_int(raw.get("steps"), path=f"{path}.steps", errors=errors, minimum=1, maximum=10_000, default=10)
    if moles == 0:
        _error(errors, f"{path}.moles", "ZERO_REACTION_MOLES", "反应总摩尔数必须大于 0。")
    if block_id is not None:
        result["block_id"] = block_id
    if moles is not None:
        result["moles"] = moles
    if steps is not None:
        result["steps"] = steps
    return result


def _normalise_gas_phase(raw: Any, *, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_GAS_PHASE", "gas_phase 必须是对象。")
        return {}
    _check_fields(raw, {"block_id", "fixed_pressure", "pressure", "volume", "temperature", "components"}, path=path, errors=errors)
    result: dict[str, Any] = {}
    block_id = _normalise_int(raw.get("block_id"), path=f"{path}.block_id", errors=errors, minimum=1, maximum=9_999, default=1)
    fixed_pressure = _normalise_bool(raw.get("fixed_pressure"), path=f"{path}.fixed_pressure", errors=errors, default=True)
    pressure = _normalise_number(raw.get("pressure"), path=f"{path}.pressure", errors=errors, minimum=0.000001, maximum=100_000.0, default=1.0)
    volume_value = raw.get("volume")
    volume: float | None = None
    if volume_value is not None:
        volume = _normalise_number(volume_value, path=f"{path}.volume", errors=errors, minimum=0.000001, maximum=1_000_000.0)
    if fixed_pressure is False and volume is None:
        _error(errors, f"{path}.volume", "MISSING_GAS_VOLUME", "固定体积气相必须提供正的 volume。")
    temperature_value = raw.get("temperature")
    temperature: float | None = None
    if temperature_value is not None:
        temperature = _normalise_number(temperature_value, path=f"{path}.temperature", errors=errors, minimum=-273.15, maximum=1_000.0)
    components = _normalise_components(raw.get("components"), path=f"{path}.components", errors=errors)
    if not components:
        _error(errors, f"{path}.components", "EMPTY_GAS_COMPONENTS", "至少需要一个气相组分。")
    for name, amount in components.items():
        if not _is_number(amount):
            _error(errors, f"{path}.components.{name}", "INVALID_GAS_AMOUNT", "气相组分量必须是有限数值。")
        elif float(amount) < 0:
            _error(errors, f"{path}.components.{name}", "NEGATIVE_GAS_AMOUNT", "气相组分量不能为负数。")
    if block_id is not None:
        result["block_id"] = block_id
    if fixed_pressure is not None:
        result["fixed_pressure"] = fixed_pressure
    if pressure is not None:
        result["pressure"] = pressure
    if volume is not None:
        result["volume"] = volume
    if temperature is not None:
        result["temperature"] = temperature
    result["components"] = {name: float(amount) for name, amount in components.items() if _is_number(amount)}
    return result


def _normalise_cell_list(
    raw: Any,
    *,
    path: str,
    errors: list[dict[str, str]],
    cell_start: int,
    cell_end: int,
) -> list[int] | None:
    if raw is None:
        return None
    if not isinstance(raw, list):
        _error(errors, path, "INVALID_CELL_LIST", "必须是单元编号数组。")
        return None
    values: list[int] = []
    for index, item in enumerate(raw):
        cell = _normalise_int(item, path=f"{path}[{index}]", errors=errors, minimum=cell_start, maximum=cell_end)
        if cell is not None:
            values.append(cell)
    if len(values) != len(set(values)):
        _error(errors, path, "DUPLICATE_CELL", "单元编号不能重复。")
    return values


def _normalise_transport(raw: Any, *, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_TRANSPORT", "transport 必须是对象。")
        return {}
    allowed = {
        "cells", "cell_id_start", "length", "shifts", "time_step", "time_units",
        "flow_direction", "dispersivity", "diffusion_coefficient", "correct_disp",
        "punch_cells", "punch_frequency", "print_cells", "print_frequency",
        "pore_volume", "warning",
    }
    _check_fields(raw, allowed, path=path, errors=errors)
    result: dict[str, Any] = {}
    cells = _normalise_int(raw.get("cells"), path=f"{path}.cells", errors=errors, minimum=1, maximum=MAX_TRANSPORT_CELLS, default=20)
    cell_id_start = _normalise_int(raw.get("cell_id_start"), path=f"{path}.cell_id_start", errors=errors, minimum=1, maximum=9_999, default=1)
    shifts = _normalise_int(raw.get("shifts"), path=f"{path}.shifts", errors=errors, minimum=1, maximum=MAX_TRANSPORT_SHIFTS, default=100)
    if cells is not None and shifts is not None and cells * shifts > MAX_TRANSPORT_CELL_SHIFTS:
        _error(
            errors,
            path,
            "TRANSPORT_QUOTA_EXCEEDED",
            f"cells × shifts 不能超过 {MAX_TRANSPORT_CELL_SHIFTS}。",
        )
    length = _normalise_number(raw.get("length"), path=f"{path}.length", errors=errors, minimum=0.000001, maximum=1_000_000.0, default=1.0)
    time_step = _normalise_number(raw.get("time_step"), path=f"{path}.time_step", errors=errors, minimum=0.000000001, maximum=1_000_000_000.0, default=0.05)
    time_units = _normalise_text(raw.get("time_units", "day"), path=f"{path}.time_units", errors=errors, max_length=16)
    if time_units is not None and time_units.lower() not in _TIME_UNITS:
        _error(errors, f"{path}.time_units", "UNSUPPORTED_TIME_UNIT", "时间单位必须为 second/minute/hour/day/year 之一。")
    flow_direction = _normalise_text(raw.get("flow_direction", "forward"), path=f"{path}.flow_direction", errors=errors, max_length=32)
    if flow_direction is not None and flow_direction not in _FLOW_DIRECTIONS:
        _error(errors, f"{path}.flow_direction", "UNSUPPORTED_FLOW_DIRECTION", "流向必须为 forward、backward 或 diffusion_only。")
    dispersivity = _normalise_number(raw.get("dispersivity"), path=f"{path}.dispersivity", errors=errors, minimum=0.0, maximum=1_000_000.0, default=0.0)
    diffusion_value = raw.get("diffusion_coefficient")
    diffusion: float | None = None
    if diffusion_value is not None:
        diffusion = _normalise_number(diffusion_value, path=f"{path}.diffusion_coefficient", errors=errors, minimum=0.0, maximum=1_000_000.0)
    correct_disp = _normalise_bool(raw.get("correct_disp"), path=f"{path}.correct_disp", errors=errors, default=False)
    pore_volume = _normalise_bool(raw.get("pore_volume"), path=f"{path}.pore_volume", errors=errors, default=False)
    warning = _normalise_bool(raw.get("warning"), path=f"{path}.warning", errors=errors, default=True)
    punch_frequency = _normalise_int(raw.get("punch_frequency"), path=f"{path}.punch_frequency", errors=errors, minimum=1, maximum=MAX_TRANSPORT_SHIFTS, default=1)
    print_frequency = _normalise_int(raw.get("print_frequency"), path=f"{path}.print_frequency", errors=errors, minimum=1, maximum=MAX_TRANSPORT_SHIFTS, default=1)

    if cells is not None and cell_id_start is not None:
        cell_end = cell_id_start + cells - 1
        punch_cells = _normalise_cell_list(raw.get("punch_cells"), path=f"{path}.punch_cells", errors=errors, cell_start=cell_id_start, cell_end=cell_end)
        print_cells = _normalise_cell_list(raw.get("print_cells"), path=f"{path}.print_cells", errors=errors, cell_start=cell_id_start, cell_end=cell_end)
    else:
        punch_cells = None
        print_cells = None

    for key, value in (
        ("cells", cells), ("cell_id_start", cell_id_start), ("shifts", shifts),
        ("length", length), ("time_step", time_step), ("time_units", time_units),
        ("flow_direction", flow_direction), ("dispersivity", dispersivity),
        ("correct_disp", correct_disp), ("pore_volume", pore_volume), ("warning", warning),
        ("punch_frequency", punch_frequency), ("print_frequency", print_frequency),
    ):
        if value is not None:
            result[key] = value
    if diffusion is not None:
        result["diffusion_coefficient"] = diffusion
    if punch_cells is not None:
        result["punch_cells"] = punch_cells
    if print_cells is not None:
        result["print_cells"] = print_cells
    return result


def _normalise_selected_output(raw: Any, *, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        _error(errors, path, "INVALID_SELECTED_OUTPUT", "selected_output 必须是对象。")
        return {}
    list_fields = {"si", "totals", "molalities", "equilibrium_phases"}
    bool_fields = {"reset", "step", "pH", "pe", "temperature"}
    _check_fields(raw, list_fields | bool_fields, path=path, errors=errors)
    result: dict[str, Any] = {}
    for field in bool_fields:
        if field in raw:
            value = _normalise_bool(raw[field], path=f"{path}.{field}", errors=errors)
            if value is not None:
                result[field] = value
    for field in list_fields:
        if field not in raw:
            continue
        raw_items = raw[field]
        if not isinstance(raw_items, list):
            _error(errors, f"{path}.{field}", "INVALID_OUTPUT_LIST", "必须是文本数组。")
            continue
        if len(raw_items) > MAX_SELECTED_OUTPUT_ITEMS:
            _error(errors, f"{path}.{field}", "TOO_MANY_OUTPUT_ITEMS", f"最多允许 {MAX_SELECTED_OUTPUT_ITEMS} 项。")
        items: list[str] = []
        for index, item in enumerate(raw_items):
            text = _normalise_text(item, path=f"{path}.{field}[{index}]", errors=errors, max_length=96)
            if text is not None:
                items.append(text)
        result[field] = items
    return result


def _normalise_metadata(raw: Any, *, path: str, errors: list[dict[str, str]]) -> Any:
    try:
        serialised = json.dumps(raw, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _error(errors, path, "INVALID_METADATA", "metadata 必须是 JSON 可表示的值。")
        return None
    if len(serialised) > 20_000:
        _error(errors, path, "METADATA_TOO_LARGE", "metadata 不能超过 20 KB。")
    return copy.deepcopy(raw)


def validate_scenario(scenario: Any) -> dict[str, Any]:
    """Validate and normalise a Scenario v1 payload.

    The return value is intentionally data-first so a browser can render all
    field errors without parsing prose exceptions.  On success it includes
    both a canonical scenario snapshot and the legacy ``params`` dictionary
    consumed by the established runner.
    """

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if not isinstance(scenario, dict):
        _error(errors, "$", "INVALID_SCENARIO", "scenario 必须是 JSON 对象。")
        return {"valid": False, "errors": errors, "warnings": warnings}

    _check_fields(
        scenario,
        {"schema_version", "name", "scenario_type", "modules", "description", "metadata"},
        path="$",
        errors=errors,
    )
    schema_version = _normalise_int(
        scenario.get("schema_version"),
        path="$.schema_version",
        errors=errors,
        default=SCHEMA_VERSION,
    )
    if schema_version is not None and schema_version != SCHEMA_VERSION:
        _error(
            errors,
            "$.schema_version",
            "UNSUPPORTED_SCHEMA_VERSION",
            f"仅支持场景架构版本 {SCHEMA_VERSION}。",
        )
    name = _normalise_text(scenario.get("name"), path="$.name", errors=errors, max_length=120)
    scenario_type = _normalise_text(scenario.get("scenario_type"), path="$.scenario_type", errors=errors, max_length=64)
    type_config = _SCENARIO_TYPES.get(scenario_type or "")
    if scenario_type is not None and type_config is None:
        _error(errors, "$.scenario_type", "UNSUPPORTED_SCENARIO_TYPE", "不支持的模拟计算类型。")
    raw_modules = scenario.get("modules")
    if not isinstance(raw_modules, dict):
        _error(errors, "$.modules", "INVALID_MODULES", "modules 必须是对象。")
        raw_modules = {}

    modules: dict[str, Any] = {}
    if type_config is not None:
        allowed_modules = set(type_config["allowed_modules"])
        for module_name, raw_value in raw_modules.items():
            module_path = f"$.modules.{module_name}"
            if module_name not in allowed_modules:
                if raw_value is not None:
                    _error(errors, module_path, "MODULE_NOT_ALLOWED", "此计算类型不支持该模块。")
                continue
            # ``null`` means that an optional module is disabled.  This makes
            # a form that renders all known modules convenient without adding
            # meaningless empty blocks to the PHREEQC input.
            if raw_value is None:
                continue
            if module_name == "solutions":
                modules[module_name] = _normalise_solutions(raw_value, path=module_path, errors=errors)
            elif module_name == "initial_cell_solution":
                modules[module_name] = _normalise_solution(
                    raw_value, path=module_path, errors=errors, include_id=False
                )
            elif module_name == "mix":
                modules[module_name] = _normalise_mix(raw_value, path=module_path, errors=errors, warnings=warnings)
            elif module_name == "equilibrium_phases":
                modules[module_name] = _normalise_equilibrium_phases(raw_value, path=module_path, errors=errors)
            elif module_name == "reaction":
                modules[module_name] = _normalise_reaction(raw_value, path=module_path, errors=errors)
            elif module_name == "gas_phase":
                modules[module_name] = _normalise_gas_phase(raw_value, path=module_path, errors=errors)
            elif module_name == "transport":
                modules[module_name] = _normalise_transport(raw_value, path=module_path, errors=errors)
            elif module_name == "selected_output":
                modules[module_name] = _normalise_selected_output(raw_value, path=module_path, errors=errors)

        for module_name in type_config["required_modules"]:
            if module_name not in modules:
                _error(errors, f"$.modules.{module_name}", "MISSING_REQUIRED_MODULE", "此计算类型需要该模块。")

    solution_ids = {
        solution["id"]
        for solution in modules.get("solutions", [])
        if isinstance(solution, dict) and "id" in solution
    }
    mix = modules.get("mix")
    if isinstance(mix, dict):
        for source_id in mix.get("solutions", {}):
            if int(source_id) not in solution_ids:
                _error(
                    errors,
                    f"$.modules.mix.solutions.{source_id}",
                    "MIX_SOLUTION_NOT_FOUND",
                    f"引用的溶液 {source_id} 不存在。",
                )
    if scenario_type == "transport":
        if 0 not in solution_ids:
            _error(
                errors,
                "$.modules.solutions",
                "TRANSPORT_INLET_MISSING",
                "TRANSPORT 必须提供 id 为 0 的入口溶液。",
            )

    normalised: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "name": name or "",
        "scenario_type": scenario_type or "",
        "modules": modules,
    }
    if "description" in scenario:
        description = _normalise_text(
            scenario.get("description"),
            path="$.description",
            errors=errors,
            required=False,
            max_length=1_000,
        )
        if description is not None:
            normalised["description"] = description
    if "metadata" in scenario:
        normalised["metadata"] = _normalise_metadata(scenario.get("metadata"), path="$.metadata", errors=errors)

    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}
    params = _compile_normalised_scenario(normalised)
    return {
        "valid": True,
        "scenario": normalised,
        "params": params,
        "errors": [],
        "warnings": warnings,
    }


def _compile_normalised_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    """Compile a known-valid, normalised scenario into legacy runner params."""

    modules = scenario["modules"]
    params: dict[str, Any] = {}
    if "solutions" in modules:
        params["solutions"] = copy.deepcopy(modules["solutions"])
    if "initial_cell_solution" in modules:
        params["initial_cell_solution"] = copy.deepcopy(modules["initial_cell_solution"])
    if "mix" in modules:
        mix = copy.deepcopy(modules["mix"])
        mix["solutions"] = {int(solution_id): fraction for solution_id, fraction in mix["solutions"].items()}
        params["mix"] = mix
    if "equilibrium_phases" in modules:
        params["equilibrium_phases"] = copy.deepcopy(modules["equilibrium_phases"])
    if "reaction" in modules:
        params["reaction"] = copy.deepcopy(modules["reaction"])
    if "gas_phase" in modules:
        params["gas_phase"] = copy.deepcopy(modules["gas_phase"])
    if "transport" in modules:
        params["transport"] = copy.deepcopy(modules["transport"])
    if "selected_output" in modules:
        params["selected_output"] = copy.deepcopy(modules["selected_output"])
    return params


def compile_scenario(scenario: Any) -> dict[str, Any]:
    """Return legacy params or raise :class:`ScenarioValidationError`."""

    validation = validate_scenario(scenario)
    if not validation["valid"]:
        raise ScenarioValidationError(validation)
    return validation["params"]


def preview_scenario(scenario: Any, *, output_file: str = "selected_output.txt") -> dict[str, Any]:
    """Validate a scenario and, if valid, generate its PHREEQC input text."""

    validation = validate_scenario(scenario)
    if not validation["valid"]:
        return validation
    try:
        from phreeqc_auto.generate_input import generate_single_simulation

        validation["input"] = generate_single_simulation(
            validation["params"], output_file=output_file
        )
    except Exception as exc:  # noqa: BLE001 - return a structured field error to the UI
        validation["valid"] = False
        validation["errors"] = [{
            "path": "$.modules",
            "code": "INPUT_GENERATION_FAILED",
            "message": f"无法生成 PHREEQC 输入：{exc}",
        }]
    return validation
