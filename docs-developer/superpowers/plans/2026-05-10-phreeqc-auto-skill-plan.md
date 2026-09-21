# PHREEQC 全流程自动化 Skill — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个 Claude Code Skill，用户通过自然语言指令即可完成 PHREEQC 模拟的全流程（需求澄清 → 输入生成 → 批量运行 → 结果解析 → 可视化），使用 TeamCreate 分配子任务给多个 agent 并行执行。

**Architecture:** Skill 采用三级架构 — (1) 用户与 Skill 主进程半自动对话确定参数；(2) 主进程使用 TeamCreate 创建 agent 团队，并行执行输入生成、模拟运行、输出解析、可视化四个子任务；(3) 主进程汇总结果后呈现给用户。底层 Python 脚本作为工具函数被各 agent 调用。

**Tech Stack:** Python (标准库 + subprocess + matplotlib), Claude Code TeamCreate

---

## File Structure

```
auto_phreeqc_proj/
├── .claude/
│   └── skills/
│       └── phreeqc-auto/
│           ├── SKILL.md                    # 主 skill 定义文件
│           ├── scripts/
│           │   ├── __init__.py
│           │   ├── generate_input.py       # 生成 PHREEQC 输入文件
│           │   ├── run_phreeqc.py          # 运行 PHREEQC 模拟
│           │   ├── parse_output.py         # 解析 PHREEQC 输出
│           │   └── visualize.py            # 生成可视化图表
│           └── references/
│               └── phreeqc-examples.md     # PHREEQC 输入模板参考
├── docs/
│   └── superpowers/
│       ├── specs/
│       │   └── 2026-05-10-phreeqc-auto-skill-design.md
│       └── plans/
│           └── 2026-05-10-phreeqc-auto-skill-plan.md  ← 本文件
├── CLAUDE.md
└── workspace/                              # 模拟运行工作区（自动创建）
```

---

### Task 1: Python 工具库 — 输入生成 (generate_input.py)

**Files:**
- Create: `.claude/skills/phreeqc-auto/scripts/__init__.py`
- Create: `.claude/skills/phreeqc-auto/scripts/generate_input.py`

- [ ] **Step 1: Create `__init__.py`**

```python
# __init__.py
```

- [ ] **Step 2: Create `generate_input.py` — 核心输入生成函数**

```python
"""PHREEQC input file generator.

Generates .pqi input files from structured parameters (JSON/dict).
Supports SOLUTION (speciation) and EQUILIBRIUM_PHASES (batch reaction).
Supports parameter scanning: pH sweep, temperature sweep, reaction amount sweep.
"""

from __future__ import annotations

import os
from typing import Any


def generate_solution_block(
    solution_id: int = 1,
    *,
    units: str = "mol/kgw",
    temp: float = 25.0,
    pH: float = 7.0,
    pe: float = 4.0,
    density: float = 1.0,
    components: dict[str, float] | None = None,
) -> str:
    """Generate a SOLUTION keyword block.

    Args:
        solution_id: Solution number.
        units: Concentration units (mol/kgw, ppm, mg/L, etc.).
        temp: Temperature in Celsius.
        pH: pH value.
        pe: pe value.
        density: Solution density (g/cm3).
        components: Dict of component name -> concentration.

    Returns:
        Formatted PHREEQC input block as string.
    """
    lines = [f"SOLUTION {solution_id}", f"    units {units}"]
    if temp != 25.0:
        lines.append(f"    temp {temp}")
    lines.append(f"    pH {pH}")
    lines.append(f"    pe {pe}")
    lines.append(f"    density {density}")
    if components:
        for comp, conc in components.items():
            lines.append(f"    {comp} {conc}")
    lines.append("")
    return "\n".join(lines)


def generate_equilibrium_phases_block(
    phases: dict[str, tuple[float, float]],
    block_id: int = 1,
) -> str:
    """Generate an EQUILIBRIUM_PHASES keyword block.

    Args:
        phases: Dict of phase_name -> (saturation_index, amount).
        block_id: Phase assemblage number.

    Returns:
        Formatted PHREEQC input block.
    """
    lines = [f"EQUILIBRIUM_PHASES {block_id}"]
    for name, (si, amount) in phases.items():
        lines.append(f"    {name} {si} {amount}")
    lines.append("")
    return "\n".join(lines)


def generate_reaction_block(
    reactants: dict[str, float],
    *,
    block_id: int = 1,
    moles: float = 1.0,
    steps: int = 10,
) -> str:
    """Generate a REACTION keyword block with stepwise addition.

    Args:
        reactants: Dict of formula -> stoichiometric coefficient.
        block_id: Reaction number.
        moles: Total moles to add.
        steps: Number of equal steps.

    Returns:
        Formatted PHREEQC input block.
    """
    lines = [f"REACTION {block_id}"]
    for formula, coeff in reactants.items():
        lines.append(f"    {formula} {coeff}")
    lines.append(f"    {moles} moles in {steps} steps")
    lines.append("")
    return "\n".join(lines)


def generate_selected_output_block(
    *,
    file: str = "selected_output.txt",
    reset: bool = True,
    si: list[str] | None = None,
    totals: list[str] | None = None,
    molalities: list[str] | None = None,
    pH: bool = True,
    pe: bool = True,
    temperature: bool = False,
) -> str:
    """Generate a SELECTED_OUTPUT keyword block.

    Args:
        file: Output file path.
        reset: Whether to reset (true) or append.
        si: List of phases to output saturation indices for.
        totals: List of elements to output total concentrations.
        molalities: List of species to output molalities.
        pH: Include pH column.
        pe: Include pe column.
        temperature: Include temperature column.

    Returns:
        Formatted PHREEQC input block.
    """
    lines = [
        "SELECTED_OUTPUT 1",
        f"    -file {file}",
        f"    -reset {str(reset).lower()}",
    ]
    if pH:
        lines.append("    -pH")
    if pe:
        lines.append("    -pe")
    if temperature:
        lines.append("    -temperature")
    if si:
        lines.append(f"    -si {' '.join(si)}")
    if totals:
        lines.append(f"    -totals {' '.join(totals)}")
    if molalities:
        lines.append(f"    -molalities {' '.join(molalities)}")
    lines.append("")
    return "\n".join(lines)


def generate_parameter_sweep(
    simulation_type: str,
    base_params: dict[str, Any],
    sweep_param: str,
    sweep_values: list[float],
    output_dir: str = ".",
) -> str:
    """Generate a multi-step input file for parameter sweeping.

    Creates a single .pqi file with multiple simulation blocks,
    one per sweep step.

    Args:
        simulation_type: "speciation" or "batch_reaction".
        base_params: Base parameters for each simulation step.
        sweep_param: Parameter being swept ("pH", "temp", "si", etc.).
        sweep_values: Values to sweep through.
        output_dir: Directory for output files.

    Returns:
        Complete .pqi content as string.
    """
    blocks: list[str] = []
    for i, val in enumerate(sweep_values):
        step_params = dict(base_params)
        sel_file = os.path.join(output_dir, f"selected_{i+1:03d}.txt")

        if simulation_type == "speciation":
            sol = dict(step_params.get("solution", {}))
            sol[sweep_param] = val
            blocks.append(generate_solution_block(solution_id=i + 1, **sol))
        elif simulation_type == "batch_reaction":
            sol = dict(step_params.get("solution", {}))
            sol[sweep_param] = val
            blocks.append(generate_solution_block(solution_id=i + 1, **sol))

        phases = step_params.get("equilibrium_phases")
        if phases:
            blocks.append(generate_equilibrium_phases_block(phases, block_id=i + 1))

        reactants = step_params.get("reaction")
        if reactants:
            blocks.append(generate_reaction_block(reactants, block_id=i + 1))

        si_list = step_params.get("selected_output", {}).get("si")
        totals_list = step_params.get("selected_output", {}).get("totals")
        blocks.append(
            generate_selected_output_block(
                file=sel_file,
                si=si_list,
                totals=totals_list,
            )
        )
        blocks.append("END")

    return "\n".join(blocks)


def generate_single_simulation(
    simulation_type: str,
    params: dict[str, Any],
    output_file: str = "selected_output.txt",
) -> str:
    """Generate a single-step .pqi file.

    Args:
        simulation_type: "speciation" or "batch_reaction".
        params: Full simulation parameters.
        output_file: SELECTED_OUTPUT file path.

    Returns:
        Complete .pqi content as string.
    """
    blocks: list[str] = []

    sol = params.get("solution", {})
    blocks.append(generate_solution_block(**sol))

    phases = params.get("equilibrium_phases")
    if phases:
        blocks.append(generate_equilibrium_phases_block(phases))

    reactants = params.get("reaction")
    if reactants:
        rxn = params.get("reaction_params", {})
        blocks.append(generate_reaction_block(reactants, **rxn))

    sel = params.get("selected_output", {})
    sel["file"] = output_file
    blocks.append(generate_selected_output_block(**sel))
    blocks.append("END")

    return "\n".join(blocks)


def write_input_file(content: str, filepath: str) -> str:
    """Write .pqi content to file.

    Args:
        content: PHREEQC input content.
        filepath: Output path.

    Returns:
        Absolute path to the written file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(filepath)) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(filepath)
```

- [ ] **Step 3: Verify file is valid Python**

Run: `python -c "import ast; ast.parse(open('project_root/.claude/skills/phreeqc-auto/scripts/generate_input.py').read()); print('OK')"`

Expected: `OK`

---

### Task 2: Python 工具库 — PHREEQC 运行器 (run_phreeqc.py)

**Files:**
- Create: `.claude/skills/phreeqc-auto/scripts/run_phreeqc.py`

- [ ] **Step 1: Create `run_phreeqc.py`**

```python
"""PHREEQC simulation runner.

Finds the PHREEQC executable, runs simulations, and handles errors.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys


def find_phreeqc_exe() -> str:
    """Locate the PHREEQC executable.

    Search order:
    1. PHREEQC_EXE environment variable
    2. phreeqc in PATH
    3. .lnk shortcut file in project root

    Returns:
        Path to the PHREEQC executable.

    Raises:
        FileNotFoundError: If PHREEQC cannot be found.
    """
    exe = os.environ.get("PHREEQC_EXE")
    if exe and os.path.isfile(exe):
        return exe

    exe = shutil.which("phreeqc")
    if exe:
        return exe

    exe = shutil.which("phreeqc.exe")
    if exe:
        return exe

    # Check project root for .lnk shortcut
    project_root = find_project_root()
    shortcut = os.path.join(
        project_root, "phreeqc-3.8.6-17100-x64 - 快捷方式.lnk"
    )
    if os.path.isfile(shortcut):
        resolved = resolve_lnk(shortcut)
        if resolved and os.path.isfile(resolved):
            return resolved

    raise FileNotFoundError(
        "PHREEQC executable not found. "
        "Set PHREEQC_EXE environment variable or add phreeqc to PATH."
    )


def find_project_root() -> str:
    """Find the project root by looking for CLAUDE.md."""
    candidate = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isfile(os.path.join(candidate, "CLAUDE.md")):
            return candidate
        candidate = os.path.dirname(candidate)
    return os.getcwd()


def resolve_lnk(lnk_path: str) -> str | None:
    """Resolve a Windows .lnk shortcut to its target path.

    Windows only: uses PowerShell to read the shortcut target.
    On other platforms, returns None.
    """
    if sys.platform != "win32":
        return None
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                f"(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk_path}').TargetPath",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        target = result.stdout.strip()
        return target if target else None
    except Exception:
        return None


def find_database(database_name: str = "phreeqc.dat") -> str:
    """Locate a PHREEQC database file.

    Search order:
    1. PHREEQC_DATABASE environment variable
    2. database/ subdirectory in project root
    3. PHREEQC installation directory

    Args:
        database_name: Database filename (e.g., "phreeqc.dat", "pitzer.dat").

    Returns:
        Path to the database file.

    Raises:
        FileNotFoundError: If database cannot be found.
    """
    env_db = os.environ.get("PHREEQC_DATABASE")
    if env_db and os.path.isfile(env_db):
        return env_db

    project_root = find_project_root()
    local_db = os.path.join(project_root, "database", database_name)
    if os.path.isfile(local_db):
        return local_db

    phreeqc_dir = os.path.dirname(find_phreeqc_exe())
    exe_db = os.path.join(phreeqc_dir, "database", database_name)
    if os.path.isfile(exe_db):
        return exe_db

    exe_db = os.path.join(phreeqc_dir, database_name)
    if os.path.isfile(exe_db):
        return exe_db

    raise FileNotFoundError(
        f"Database '{database_name}' not found. "
        "Set PHREEQC_DATABASE environment variable."
    )


def run_simulation(
    input_file: str,
    output_file: str | None = None,
    database: str | None = None,
    *,
    timeout: int = 300,
) -> dict:
    """Run a PHREEQC simulation.

    Args:
        input_file: Path to .pqi input file.
        output_file: Path for .qpo output file (auto if None).
        database: Path to database file (auto if None).
        timeout: Maximum run time in seconds.

    Returns:
        Dict with keys:
            - exit_code: int
            - stdout: str
            - stderr: str
            - output_file: str | None
            - success: bool
            - error: str | None
    """
    exe = find_phreeqc_exe()

    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".qpo"

    if database is None:
        database = find_database()

    os.makedirs(os.path.dirname(os.path.abspath(output_file)) or ".", exist_ok=True)

    try:
        proc = subprocess.run(
            [exe, input_file, output_file, database],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        result = {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "output_file": output_file if os.path.isfile(output_file) else None,
            "success": proc.returncode == 0,
            "error": None,
        }
        if not result["success"]:
            result["error"] = proc.stderr.strip() or proc.stdout.strip()
        return result
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "",
            "output_file": None,
            "success": False,
            "error": f"Simulation timed out after {timeout}s",
        }
    except FileNotFoundError as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "",
            "output_file": None,
            "success": False,
            "error": str(e),
        }
```

- [ ] **Step 2: Verify Python syntax**

Run: `python -c "import ast; ast.parse(open('project_root/.claude/skills/phreeqc-auto/scripts/run_phreeqc.py').read()); print('OK')"`

Expected: `OK`

---

### Task 3: Python 工具库 — 输出解析器 (parse_output.py)

**Files:**
- Create: `.claude/skills/phreeqc-auto/scripts/parse_output.py`

- [ ] **Step 1: Create `parse_output.py`**

```python
"""PHREEQC output parser.

Parses SELECTED_OUTPUT files and standard PHREEQC output into structured JSON.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any


def parse_selected_output(filepath: str) -> dict[str, Any]:
    """Parse a PHREEQC SELECTED_OUTPUT text file.

    SELECTED_OUTPUT format is tabular with a header row followed
    by data rows. Values are space/tab separated.

    Args:
        filepath: Path to the SELECTED_OUTPUT file.

    Returns:
        Dict with keys:
            - columns: list of column names
            - data: list of lists (each inner list is one row)
            - row_count: int
    """
    if not os.path.isfile(filepath):
        return {"columns": [], "data": [], "row_count": 0, "error": "File not found"}

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return {"columns": [], "data": [], "row_count": 0, "error": "Empty file"}

    # First non-comment line is the header
    header_line = None
    data_lines: list[str] = []
    for line in lines:
        if line.startswith("#") or line.startswith("Selected"):
            continue
        if header_line is None:
            header_line = line
        else:
            data_lines.append(line)

    if header_line is None:
        return {"columns": [], "data": [], "row_count": 0, "error": "No header found"}

    columns = header_line.split()
    data: list[list[float]] = []
    for line in data_lines:
        try:
            row = [float(val) for val in line.split()]
            if len(row) == len(columns):
                data.append(row)
        except ValueError:
            continue

    return {
        "columns": columns,
        "data": data,
        "row_count": len(data),
    }


def extract_saturation_indices(output_text: str) -> list[dict[str, Any]]:
    """Extract saturation indices from standard PHREEQC output text.

    Scans for the saturation index table in the output.

    Args:
        output_text: Full PHREEQC stdout/output text.

    Returns:
        List of dicts: [{phase, log_sr, si}, ...]
    """
    results: list[dict[str, Any]] = []
    in_si_table = False

    for line in output_text.split("\n"):
        stripped = line.strip()
        if "Saturation indices" in stripped or re.search(
            r"^\s*Phase\s+SI\s", stripped
        ):
            in_si_table = True
            continue
        if in_si_table:
            if not stripped or stripped.startswith("---"):
                continue
            match = re.match(
                r"^\s*(\S[\w()\[\]\+-]*\S?)\s+(-?\d+\.\S+)", stripped
            )
            if match:
                phase, si_str = match.groups()
                try:
                    si = float(si_str)
                    results.append({"phase": phase.strip(), "si": si})
                except ValueError:
                    continue
            elif results:
                # Table ended
                break

    return results


def extract_species_distribution(output_text: str) -> list[dict[str, Any]]:
    """Extract species distribution from standard PHREEQC output.

    Args:
        output_text: Full PHREEQC output text.

    Returns:
        List of dicts: [{species, molality, activity, log_molality}, ...]
    """
    results: list[dict[str, Any]] = []
    in_species = False

    for line in output_text.split("\n"):
        stripped = line.strip()
        if re.search(r"^\s*Species\s+Molality", stripped):
            in_species = True
            continue
        if in_species:
            if not stripped or stripped.startswith("---"):
                continue
            match = re.match(
                r"^\s*(\S[\w()\[\]\+-]*)\s+(\S+)\s+(\S+)",
                stripped,
            )
            if match:
                species, mol, act = match.groups()
                try:
                    results.append(
                        {
                            "species": species.strip(),
                            "molality": float(mol),
                            "activity": float(act),
                        }
                    )
                except ValueError:
                    continue
            elif results:
                break

    return results


def extract_element_molalities(output_text: str) -> dict[str, float]:
    """Extract total element molalities from PHREEQC output.

    Args:
        output_text: Full PHREEQC output text.

    Returns:
        Dict of element -> molality.
    """
    results: dict[str, float] = {}
    in_mol = False

    for line in output_text.split("\n"):
        stripped = line.strip()
        if re.search(r"^\s*Element\s+Molality", stripped):
            in_mol = True
            continue
        if in_mol:
            if not stripped or stripped.startswith("---"):
                continue
            match = re.match(r"^\s*(\w+)\s+(\S+)", stripped)
            if match:
                elem, val = match.groups()
                try:
                    results[elem] = float(val)
                except ValueError:
                    continue
            elif results:
                break

    return results


def to_json(
    selected_output_data: dict,
    saturation_indices: list | None = None,
    species: list | None = None,
    elements: dict | None = None,
    metadata: dict | None = None,
) -> str:
    """Serialize parsed results to JSON string.

    Args:
        selected_output_data: Result from parse_selected_output().
        saturation_indices: Result from extract_saturation_indices().
        species: Result from extract_species_distribution().
        elements: Result from extract_element_molalities().
        metadata: Additional metadata (simulation type, parameters, etc.).

    Returns:
        JSON string.
    """
    result: dict[str, Any] = {
        "selected_output": selected_output_data,
    }
    if saturation_indices:
        result["saturation_indices"] = saturation_indices
    if species:
        result["species"] = species
    if elements:
        result["elements"] = elements
    if metadata:
        result["metadata"] = metadata

    return json.dumps(result, indent=2, ensure_ascii=False)
```

- [ ] **Step 2: Verify Python syntax**

Run: `python -c "import ast; ast.parse(open('project_root/.claude/skills/phreeqc-auto/scripts/parse_output.py').read()); print('OK')"`

Expected: `OK`

---

### Task 4: Python 工具库 — 可视化工具 (visualize.py)

**Files:**
- Create: `.claude/skills/phreeqc-auto/scripts/visualize.py`

- [ ] **Step 1: Create `visualize.py`**

```python
"""PHREEQC results visualizer.

Creates matplotlib plots from parsed PHREEQC output data.
Supports SI plots, concentration plots, and multi-panel figures.
"""

from __future__ import annotations

import json
import os
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_saturation_indices(
    data: dict[str, Any],
    *,
    sweep_param: str | None = None,
    title: str = "Saturation Indices",
    filepath: str | None = None,
) -> str:
    """Plot saturation indices as a grouped bar chart or sweep line plot.

    Args:
        data: Parsed results dict (from parse_output.to_json output).
        sweep_param: If set, use this as X axis (line plot).
        title: Chart title.
        filepath: Output path (auto-gen if None).

    Returns:
        Path to the saved figure.
    """
    si_data = data.get("saturation_indices", [])
    if not si_data:
        return ""

    phases = [s["phase"] for s in si_data]
    values = [s["si"] for s in si_data]

    fig, ax = plt.subplots(figsize=(10, max(4, len(phases) * 0.4)))
    colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in values]
    bars = ax.barh(phases, values, color=colors)
    ax.axvline(0, color="gray", linestyle="-", linewidth=0.5)
    ax.set_xlabel("Saturation Index (SI)")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)

    for bar, val in zip(bars, values):
        label = f"  {val:.2f}  "
        x = bar.get_width()
        ax.text(
            x + 0.01 if x >= 0 else x - 0.01,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left" if x >= 0 else "right",
            fontsize=8,
        )

    plt.tight_layout()
    return _save_figure(fig, filepath or "saturation_indices.png")


def plot_selected_output_sweep(
    selected_output: dict[str, Any],
    x_column: str,
    y_columns: list[str],
    title: str = "Parameter Sweep",
    xlabel: str | None = None,
    filepath: str | None = None,
) -> str:
    """Plot SELECTED_OUTPUT data as line plot (one line per Y column).

    Args:
        selected_output: Dict with columns and data from parse_selected_output().
        x_column: Column name to use as X axis.
        y_columns: Column names to plot as Y axis.
        title: Chart title.
        xlabel: X axis label (defaults to x_column).
        filepath: Output path.

    Returns:
        Path to the saved figure.
    """
    columns = selected_output.get("columns", [])
    data = selected_output.get("data", [])

    if x_column not in columns:
        return ""
    x_idx = columns.index(x_column)
    x_vals = [row[x_idx] for row in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10.colors

    for i, y_col in enumerate(y_columns):
        if y_col not in columns:
            continue
        y_idx = columns.index(y_col)
        y_vals = [row[y_idx] for row in data]
        ax.plot(
            x_vals, y_vals, marker="o", label=y_col, color=colors[i % len(colors)]
        )

    ax.set_xlabel(xlabel or x_column)
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return _save_figure(fig, filepath or "parameter_sweep.png")


def plot_multi_panel(
    data_sets: list[dict[str, Any]],
    titles: list[str],
    *,
    filepath: str = "multi_panel.png",
) -> str:
    """Create a multi-panel figure from multiple results.

    Args:
        data_sets: List of parsed result dicts.
        titles: List of panel titles (one per data_set).
        filepath: Output path.

    Returns:
        Path to the saved figure.
    """
    n = len(data_sets)
    cols = min(2, n)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(8 * cols, 5 * rows))
    if rows == 1 and cols == 1:
        axes = [axes]
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for ax, data, title in zip(axes, data_sets, titles):
        si_data = data.get("saturation_indices", [])
        if si_data:
            phases = [s["phase"] for s in si_data]
            values = [s["si"] for s in si_data]
            colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in values]
            ax.barh(phases, values, color=colors)
            ax.axvline(0, color="gray", linewidth=0.5)
        ax.set_title(title)
        ax.grid(axis="x", alpha=0.3)

    for i in range(n, len(axes)):
        axes[i].set_visible(False)

    plt.tight_layout()
    return _save_figure(fig, filepath)


def _save_figure(fig: plt.Figure, filepath: str) -> str:
    """Save a figure to file and close it.

    Args:
        fig: Matplotlib figure.
        filepath: Output path.

    Returns:
        Absolute path to saved file.
    """
    abspath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(abspath) or ".", exist_ok=True)
    fig.savefig(abspath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return abspath
```

- [ ] **Step 2: Verify Python syntax**

Run: `python -c "import ast; ast.parse(open('project_root/.claude/skills/phreeqc-auto/scripts/visualize.py').read()); print('OK')"`

Expected: `OK`

---

### Task 5: PHREEQC 输入模板参考 (references/phreeqc-examples.md)

**Files:**
- Create: `.claude/skills/phreeqc-auto/references/phreeqc-examples.md`

- [ ] **Step 1: Create reference file**

```markdown
# PHREEQC 输入模板参考

本文件提供常见模拟场景的 PHREEQC 输入模板，供输入生成 Agent 参考。

## 1. 海水 Speciation（完整示例）

```
TITLE Speciation of seawater with uranium.
SOLUTION 1 SEAWATER
    units ppm
    pH 8.22
    pe 8.451
    temp 25.0
    density 1.023
    Ca 412.3
    Mg 1291.8
    Na 10768.0
    K 399.1
    Cl 19353.0
    Alkalinity 141.682 as HCO3
    S(6) 2712.0
    U 3.3
SELECTED_OUTPUT 1
    -file selected.txt
    -pH pe
    -si calcite dolomite
    -totals Ca Mg U
END
```

## 2. 批反应 — 矿物溶解/沉淀

```
TITLE Batch reaction: Calcite dissolution.
SOLUTION 1
    units mol/kgw
    pH 7.0
    pe 4.0
    temp 25.0
    Ca 0.001
    C(4) 0.001
EQUILIBRIUM_PHASES 1
    Calcite 0.0 10.0
    CO2(g) -1.5 10.0
SELECTED_OUTPUT 1
    -file selected.txt
    -pH pe
    -si calcite dolomite
    -totals Ca C
END
```

## 3. 参数扫描结构（pH 扫描）

```
# Each step is a separate simulation
SOLUTION 1
    units mol/kgw
    pH 6.0
    pe 4.0
    temp 25.0
    Ca 0.001
SELECTED_OUTPUT 1
    -file step_001.txt
    -pH
    -si calcite
    -totals Ca
END

SOLUTION 2
    units mol/kgw
    pH 7.0
    pe 4.0
    temp 25.0
    Ca 0.001
SELECTED_OUTPUT 1
    -file step_002.txt
    -pH
    -si calcite
    -totals Ca
END
END
```

## 4. 气体平衡

```
SOLUTION 1
    units mol/kgw
    pH 7.0
    temp 25.0
    Na 0.1
    Cl 0.1
GAS_PHASE 1
    -fixed_pressure
    -pressure 1.0
    CO2(g) 0.0003
SELECTED_OUTPUT 1
    -file selected.txt
    -pH
    -si calcite
    -totals C
END
```

## 5. 动力学反应

```
SOLUTION 1
    units mol/kgw
    pH 7.0
    temp 25.0
    Ca 0.0
KINETICS 1
    Calcite
    -m0 0.1
    -parms 100 1
RATES 1
    Calcite
    -start
    10 rem rate = k * (1 - SR)
    20 k = 10
    30 sr = SR("Calcite")
    40 rate = k * (1 - sr) * 1e-9
    50 moles = rate * TIME
    60 save moles
    -end
SELECTED_OUTPUT 1
    -file selected.txt
    -pH
    -si calcite
    -totals Ca
END
```

## 6. 常用数据库及适用场景

| 数据库 | 适用场景 |
|--------|----------|
| phreeqc.dat | 一般用途（源自 PHREEQE） |
| wateq4f.dat | 天然水（低温环境） |
| llnl.dat | 高温地球化学（源自 EQ3/6） |
| minteq.dat | 环境/污染（源自 MINTEQA2） |
| pitzer.dat | 高离子强度（盐水、海水） |
| sit.dat | SIT 活度模型（中等离子强度） |
| iso.dat | 同位素分馏计算 |

## 7. 常用矿物化学式和 SI 查询名

| 矿物 | 化学式 | PHREEQC 查询名 |
|------|--------|----------------|
| 方解石 | CaCO3 | Calcite |
| 白云石 | CaMg(CO3)2 | Dolomite |
| 石膏 | CaSO4·2H2O | Gypsum |
| 硬石膏 | CaSO4 | Anhydrite |
| 石英 | SiO2 | Quartz |
| 非晶硅 | SiO2 | Chalcedony |
| 黄铁矿 | FeS2 | Pyrite |
| 赤铁矿 | Fe2O3 | Hematite |
| 针铁矿 | FeOOH | Goethite |
```

---

### Task 6: 主 Skill 定义文件 (SKILL.md)

**Files:**
- Create: `.claude/skills/phreeqc-auto/SKILL.md`

**注意:** 这是整个项目的核心 — Skill 被触发时，Claude 会加载并遵循此文件中的指令。

- [ ] **Step 1: Create SKILL.md**

```markdown
---
name: phreeqc-auto
description: >-
  PHREEQC 全流程自动化模拟。当用户提到 PHREEQC、地球化学模拟、溶液 speciation、批反应、矿物溶解沉淀、饱和指数计算、地球化学参数扫描、水质模拟时，必须使用此 skill。涉及地球化学计算、水化学分析或矿物-水相互作用的任何任务都需要此 skill。即使只是简单提及"模拟"+"溶液"或"矿物"的组合，也应触发此 skill 以确认用户需求。此 skill 是完成 PHREEQC 相关任务的唯一正确工具。
---

# PHREEQC 全流程自动化 Skill

本 Skill 实现基于自然语言的 PHREEQC 地球化学模拟全流程自动化：需求澄清 → 输入生成 → 模拟运行 → 输出解析 → 可视化。

## 工作流程概览

```
Phase 1: 需求澄清 ── 与用户半自动对话确定模拟参数
Phase 2: 团队编排 ── 用 TeamCreate 分配子任务给 agent 团队
Phase 3: 结果呈现 ── 终端报告 + 数据文件 + 图表
```

## 工作目录

所有文件操作在项目根目录下执行。

## Phase 1: 需求澄清

**目标:** 与用户逐一确认模拟所需的关键参数。用户无法决定时，你根据地球化学常识推理合理默认值。

### 交互规则
1. **一次只问一个问题** — 不要一次性抛出所有问题
2. **显示已知参数** — 先总结你从用户指令中提取到的内容
3. **标记推理值** — 你推理的参数要标注 `[自动推理]`，让用户知道可以覆盖
4. **确认后才执行** — 汇总所有参数后让用户确认再进入 Phase 2

### Speciation 所需参数清单

| 参数 | 默认/推理规则 | 必需 |
|------|---------------|------|
| 温度 | 25°C（室温） | 是，可推理 |
| pH | 必须问用户 | 是 |
| pe/pe | 4.0（氧化环境）/ 可通过 O2/H2S 推理 | 是，可推理 |
| 离子组分 | 必须问用户（至少主要离子） | 是 |
| 浓度单位 | mol/kgw（默认，可改为 ppm/mg/L） | 是，可推理 |
| 数据库 | phreeqc.dat | 是，可推理 |
| 目标物 (SI) | 用户关注哪些矿物？ | 按需 |
| 密度 | 1.0（稀溶液） | 可推理 |

### Batch-Reaction 额外参数

| 参数 | 默认/推理规则 | 必需 |
|------|---------------|------|
| 反应相 | 必须问用户（哪些矿物/气体参与反应？） | 是 |
| 饱和指数目标 | 0.0（默认平衡） | 可推理 |
| 反应物量 | 必须问用户，或推理合理量（如 10 mol 矿物） | 是 |
| 反应步长 | 1 步（单步），或用户指定步数/扫描范围 | 按需 |
| 动力学/平衡 | 默认平衡 (EQUILIBRIUM_PHASES) | 可推理 |

### 参数扫描额外确认

| 参数 | 默认/推理规则 |
|------|---------------|
| 扫描变量 | pH, 温度, 反应量 中最常用的 |
| 扫描范围 | 用户指定，或推理合理范围 (如 pH 4-9) |
| 步数/步长 | 用户指定，或默认 10 步 |

### 参数汇总格式

确认时使用如下格式：

```
📋 模拟参数汇总
━━━━━━━━━━━━━━━━━━━━
类型:  Speciation（海水）
温度:  25°C [自动推理]
pH:    8.22
组分:  Ca 412.3 ppm, Mg 1291.8 ppm, Na 10768 ppm, Cl 19353 ppm
数据库: phreeqc.dat [自动推理]
关注矿物: Calcite, Dolomite
━━━━━━━━━━━━━━━━━━━━
以上参数确认无误？要修改任何参数吗？
```

## Phase 2: 团队编排

用户确认参数后，使用 TeamCreate 创建 agent 团队并行执行子任务。

### 团队结构

```
Team Lead (当前会话):
├── Agent 1: 输入生成 (generate_input.py)
├── Agent 2: 模拟运行 (run_phreeqc.py)
├── Agent 3: 输出解析 (parse_output.py)
└── Agent 4: 可视化 (visualize.py)
```

### 步骤

1. **创建工作目录**: 在 `workspace/` 下创建本次运行的唯一 ID 子目录

2. **创建团队**: 使用 `TeamCreate` 创建团队，设置 `team_name="phreeqc-sim"`

3. **并发分配任务**: 在同一消息中同时 spawn 所有 agent（使用 Agent 工具，设置 team_name="phreeqc-sim"）

4. **给每个 agent 的 prompt 结构**:
   - 用中文明确描述任务
   - 提供输入文件路径
   - 说明预期的输出文件路径
   - 引用 Python 脚本的调用方法（脚本在 `.claude/skills/phreeqc-auto/scripts/`）
   - 说明如何验证结果

5. **收集结果**: 各 agent 完成后接收结果，检查是否有错误

6. **清理团队**: 使用 `TeamDelete` 删除团队

### Agent 1: 输入生成

**任务:** 根据确认的参数生成 PHREEQC 输入文件 (.pqi)

**使用的脚本:** `generate_input.py`

**调用方法:**
```python
import sys
sys.path.insert(0, r'<project_root>/.claude/skills/phreeqc-auto/scripts')
from generate_input import generate_single_simulation, generate_parameter_sweep, write_input_file

# 单次模拟
content = generate_single_simulation(simulation_type, params, output_file="selected.txt")
pqi_path = write_input_file(content, "workspace/<run-id>/input.pqi")
```

**参数传递格式 (JSON):**
将确认的参数整理为 JSON 字典传参。对 simulation_type 判断：
- 仅有 SOLUTION → "speciation"
- 含 EQUILIBRIUM_PHASES 或 REACTION → "batch_reaction"

**验证:** 生成的 .pqi 文件非空且包含有效的关键字块。

### Agent 2: 模拟运行

**任务:** 调用 PHREEQC 可执行文件进行模拟

**使用的脚本:** `run_phreeqc.py`

**调用方法:**
```python
import sys
sys.path.insert(0, r'<project_root>/.claude/skills/phreeqc-auto/scripts')
from run_phreeqc import run_simulation

result = run_simulation(
    input_file="workspace/<run-id>/input.pqi",
    output_file="workspace/<run-id>/output.qpo",
    database="workspace/<run-id>/phreeqc.dat",  # or auto-detect
)
```

**错误处理:** 如果失败，检查 PHREEQC exe 路径、输入文件格式、数据库路径。尝试修复并重试 1 次。

**成功条件:** result["success"] == True 且 result["output_file"] 存在。

### Agent 3: 输出解析

**任务:** 解析 PHREEQC 输出文件，提取结构化数据

**使用的脚本:** `parse_output.py`

**调用方法:**
```python
import sys, json
sys.path.insert(0, r'<project_root>/.claude/skills/phreeqc-auto/scripts')
from parse_output import parse_selected_output, extract_saturation_indices, to_json

sel_data = parse_selected_output("workspace/<run-id>/selected_output.txt")
si_data = extract_saturation_indices(output_text)

# 读取完整的 .qpo 文件用于解析 SI
with open("workspace/<run-id>/output.qpo") as f:
    full_output = f.read()

results = {
    "selected_output": sel_data,
    "saturation_indices": extract_saturation_indices(full_output),
    "species": extract_species_distribution(full_output),
    "elements": extract_element_molalities(full_output),
    "metadata": {...}
}

with open("workspace/<run-id>/results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
```

### Agent 4: 可视化

**任务:** 读取解析后的 JSON 数据，生成图表

**使用的脚本:** `visualize.py`

**调用方法:**
```python
import sys, json
sys.path.insert(0, r'<project_root>/.claude/skills/phreeqc-auto/scripts')
from visualize import plot_saturation_indices, plot_selected_output_sweep

with open("workspace/<run-id>/results.json") as f:
    data = json.load(f)

chart_paths = []
# SI 图
path = plot_saturation_indices(data, title="Saturation Indices",
    filepath="workspace/<run-id>/charts/saturation_indices.png")
chart_paths.append(path)

# 如果有 sweep 数据
sel = data.get("selected_output", {})
if sel.get("row_count", 0) > 1:
    # 自动检测扫描列和数值列
    ...
```

### 工作区目录结构

每次运行创建独立目录：
```
workspace/
├── 20260510_1430_calcite_sweep/
│   ├── input.pqi                # 输入文件
│   ├── output.qpo               # PHREEQC 原始输出
│   ├── selected_output.txt      # SELECTED_OUTPUT 数据
│   ├── results.json             # 解析后的结构化数据
│   └── charts/
│       ├── saturation_indices.png
│       └── parameter_sweep.png
```

## Phase 3: 结果呈现

所有 agent 完成后，汇总结果呈现给用户。

### 终端摘要格式

```
═══ PHREEQC 模拟结果 ═══
模拟类型: Speciation
参数: pH=7.0, T=25°C

── 饱和指数 ──
Calcite:     0.52  (饱和)
Dolomite:    1.23  (过饱和)
Quartz:     -0.31  (未饱和)

── 主要组分 ──
Ca²⁺:    1.23e-3 mol/kgw
Mg²⁺:    5.67e-4 mol/kgw

── 输出文件 ──
📄 workspace/run_001/results.json
📊 workspace/run_001/charts/saturation_indices.png
```

### 输出文件
告诉用户数据文件和图表文件的路径，用户可以直接查看。

## 脚本路径参考

所有 Python 脚本位于项目根目录的相对路径：
```
.claude/skills/phreeqc-auto/scripts/generate_input.py
.claude/skills/phreeqc-auto/scripts/run_phreeqc.py
.claude/skills/phreeqc-auto/scripts/parse_output.py
.claude/skills/phreeqc-auto/scripts/visualize.py
```

import 时使用：
```python
import sys
sys.path.insert(0, os.path.join(project_root, ".claude", "skills", "phreeqc-auto", "scripts"))
```

`project_root` 为项目根目录

## 局限与注意事项

1. **PHREEQC 可执行文件**: 必须可通过 PATH 或 `PHREEQC_EXE` 环境变量访问
2. **数据库**: 可通过 `PHREEQC_DATABASE` 环境变量或项目 `database/` 目录访问
3. **Windows .lnk**: `run_phreeqc.py` 支持解析 .lnk 快捷方式
4. **计算时间**: 复杂模拟（传输、动力学）可能超时，默认 timeout 300 秒
5. **收敛失败**: 某些输入组合导致 PHREEQC 收敛失败，需提示用户调整参数
6. **matplotlib 后端**: 使用 Agg 后端（无显示器需求），仅输出文件
```

---

### Task 7: 更新 CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: 在 CLAUDE.md 末尾添加技能和方案B参考**

在 CLAUDE.md 末尾添加以下内容：

```markdown
## 自动化 Skill

项目包含一个 Claude Code Skill (`phreeqc-auto`) 用于全流程自动化模拟。

### 使用方法
触发方式：在 Claude Code 中直接输入 PHREEQC 模拟相关的自然语言指令，如：
- "模拟海水在 pH 7-9 间的方解石饱和指数变化"
- "做方解石溶解的批反应模拟，温度 25-60°C"

Skill 会引导你确认参数 → 自动创建 agent 团队 → 生成输入文件 → 运行模拟 → 解析结果 → 生成图表。

### Skill 文件位置
```
.claude/skills/phreeqc-auto/
├── SKILL.md                          # 主 skill 定义（加载入口）
├── scripts/
│   ├── generate_input.py             # PHREEQC 输入文件生成
│   ├── run_phreeqc.py                # PHREEQC 运行器
│   ├── parse_output.py               # 输出解析器
│   └── visualize.py                  # 可视化工具
└── references/
    └── phreeqc-examples.md           # 输入模板参考
```

### 方案 B（未来参考）：独立 Python 库
当需要脱离 Claude Code 独立使用自动化功能时，可重构为独立的 Python 包：

```
phreeqc_auto/
├── __init__.py
├── generate_input.py
├── runner.py
├── parser.py
└── visualize.py
```

然后在 Claude Code 中通过 Bash 工具调用 Python 脚本，而非使用 TeamCreate 编排 agent。

### 设计文档
详细设计见 `docs/superpowers/specs/2026-05-10-phreeqc-auto-skill-design.md`
```

---

### Task 8: 创建测试运行脚本（可选，用于验证）

**Files:**
- Create: `.claude/skills/phreeqc-auto/scripts/test_scripts.py`

**注意:** 此任务提供基本的单元测试验证 Python 函数逻辑，无需 PHREEQC 可执行文件。

- [ ] **Step 1: Create test script**

```python
"""Tests for PHREEQC automation scripts (no PHREEQC executable needed)."""

import json
import os
import sys
import tempfile
import unittest

# Add scripts to path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)


class TestGenerateInput(unittest.TestCase):
    """Tests for generate_input.py"""

    def setUp(self):
        from generate_input import (
            generate_equilibrium_phases_block,
            generate_reaction_block,
            generate_selected_output_block,
            generate_single_simulation,
            generate_solution_block,
            write_input_file,
        )
        self.generate_solution_block = generate_solution_block
        self.generate_equilibrium_phases_block = generate_equilibrium_phases_block
        self.generate_reaction_block = generate_reaction_block
        self.generate_selected_output_block = generate_selected_output_block
        self.generate_single_simulation = generate_single_simulation
        self.write_input_file = write_input_file

    def test_solution_block_has_required_fields(self):
        block = self.generate_solution_block(pH=7.0)
        self.assertIn("SOLUTION 1", block)
        self.assertIn("pH 7.0", block)
        self.assertIn("units", block)

    def test_solution_block_with_components(self):
        block = self.generate_solution_block(pH=8.0, components={"Ca": 0.001, "Mg": 0.002})
        self.assertIn("Ca 0.001", block)
        self.assertIn("Mg 0.002", block)

    def test_equilibrium_phases_block(self):
        block = self.generate_equilibrium_phases_block({"Calcite": (0.0, 10.0)})
        self.assertIn("EQUILIBRIUM_PHASES 1", block)
        self.assertIn("Calcite 0.0 10.0", block)

    def test_reaction_block(self):
        block = self.generate_reaction_block({"CO2": 1.0}, moles=0.1, steps=5)
        self.assertIn("REACTION 1", block)
        self.assertIn("0.1 moles in 5 steps", block)

    def test_selected_output_block(self):
        block = self.generate_selected_output_block(si=["Calcite"], totals=["Ca"])
        self.assertIn("SELECTED_OUTPUT 1", block)
        self.assertIn("-si Calcite", block)
        self.assertIn("-totals Ca", block)

    def test_write_input_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_input_file("TEST CONTENT", os.path.join(tmp, "test.pqi"))
            with open(path) as f:
                self.assertEqual(f.read(), "TEST CONTENT")

    def test_single_simulation_speciation(self):
        params = {
            "solution": {"pH": 7.0, "components": {"Ca": 0.001}},
            "selected_output": {"si": ["Calcite"]},
        }
        content = self.generate_single_simulation("speciation", params)
        self.assertIn("SOLUTION 1", content)
        self.assertIn("SELECTED_OUTPUT 1", content)
        self.assertIn("END", content)

    def test_single_simulation_batch(self):
        params = {
            "solution": {"pH": 7.0, "components": {"Ca": 0.001}},
            "equilibrium_phases": {"Calcite": (0.0, 10.0)},
            "selected_output": {"si": ["Calcite"], "totals": ["Ca"]},
        }
        content = self.generate_single_simulation("batch_reaction", params)
        self.assertIn("SOLUTION 1", content)
        self.assertIn("EQUILIBRIUM_PHASES 1", content)
        self.assertIn("SELECTED_OUTPUT 1", content)


class TestParseOutput(unittest.TestCase):
    """Tests for parse_output.py"""

    def setUp(self):
        from parse_output import (
            extract_element_molalities,
            extract_saturation_indices,
            parse_selected_output,
        )
        self.parse_selected_output = parse_selected_output
        self.extract_saturation_indices = extract_saturation_indices
        self.extract_element_molalities = extract_element_molalities

    def test_parse_selected_output_simple(self):
        content = "pH\tpe\tsi_Calcite\n7.0\t4.0\t0.5\n8.0\t4.0\t1.2\n"
        with tempfile.TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "sel.txt")
            with open(fp, "w") as f:
                f.write(content)
            result = self.parse_selected_output(fp)
        self.assertEqual(result["columns"], ["pH", "pe", "si_Calcite"])
        self.assertEqual(len(result["data"]), 2)
        self.assertAlmostEqual(result["data"][0][0], 7.0)
        self.assertAlmostEqual(result["data"][1][2], 1.2)

    def test_parse_selected_output_empty(self):
        result = self.parse_selected_output("nonexistent.txt")
        self.assertIn("error", result)

    def test_extract_saturation_indices(self):
        text = """
        Some output...
        Saturation indices:
        Phase SI
        Calcite 0.52
        Dolomite 1.23
        Quartz -0.31
        End of table.
        """
        result = self.extract_saturation_indices(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["phase"], "Calcite")
        self.assertAlmostEqual(result[0]["si"], 0.52)
        self.assertAlmostEqual(result[2]["si"], -0.31)

    def test_extract_element_molalities(self):
        text = """
        Element Molality
        Ca 1.23e-03
        Mg 5.67e-04
        Na 1.08e-02
        """
        result = self.extract_element_molalities(text)
        self.assertAlmostEqual(result["Ca"], 1.23e-03)
        self.assertAlmostEqual(result["Mg"], 5.67e-04)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests**

Run: `python -m unittest .claude/skills/phreeqc-auto/scripts/test_scripts.py -v`

Expected: All tests pass (except possibly the `write_input_file` test which creates a temp file)

---

## Verification

### 端到端验证

1. **语法验证**: 所有 Python 文件通过 `ast.parse`
2. **单元测试**: `test_scripts.py` 全部通过
3. **Skill 语法验证**: SKILL.md 格式正确（YAML frontmatter + markdown）
4. **手动测试**: 在 Claude Code 中触发 skill，输入"模拟海水 speciation，pH 8.2，关注方解石饱和指数"
   - 期望: skill 触发 → 澄清参数 → 创建团队 → 运行模拟 → 呈现结果

### 验证命令

```bash
# 语法检查所有脚本
for f in .claude/skills/phreeqc-auto/scripts/*.py; do
    python -c "import ast; ast.parse(open('$f').read()); echo '$f: OK'"
done

# 运行单元测试
python -m unittest .claude/skills/phreeqc-auto/scripts/test_scripts.py -v
```
