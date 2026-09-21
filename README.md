# auto-phreeqc

[![CI](https://github.com/songsongr/auto-phreeqc-public/actions/workflows/ci.yml/badge.svg)](https://github.com/songsongr/auto-phreeqc-public/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)

**Turn a geochemical question into a reproducible PHREEQC calculation.**

`auto-phreeqc` combines a public Python runtime, a local browser Workbench,
nine runnable modelling examples, and an AI-agent Skill. It helps users build
and review simulations for aqueous speciation, batch reactions, mixing,
surface complexation, ion exchange, kinetics, and one-dimensional transport.

[中文文档](docs/README.zh-CN.md) · [Workbench guide](docs/workbench-README.zh-CN.md) · [Agent guide](docs/agent-usage.md)

> PHREEQC itself is developed and distributed separately by the U.S.
> Geological Survey (USGS). This repository does not bundle its executable or
> thermodynamic databases. Download it from the [official USGS page](https://water.usgs.gov/water-resources/software/PHREEQC/).

## Choose how you want to work

| If you want to… | Start here |
| --- | --- |
| Describe a model in natural language | Use an AI coding agent and the included `phreeqc-auto` Skill. |
| Build and inspect a calculation in a browser | Launch the local [Workbench](#local-workbench). |
| Integrate PHREEQC into Python code | Use the [`phreeqc_auto`](#python-library) package. |
| Adapt a known model | Start from one of the [nine examples](#included-examples). |

## First-time setup

### Let an agent set up the repository

After cloning, tell your coding agent:

```text
Configure this auto-phreeqc repository for first use. Run its setup and health
check, enable the included PHREEQC Skill, and tell me when it is ready for a
natural-language calculation. If PHREEQC is not installed, explain the
official installation step and resume setup afterwards.
```

The repository contains public instructions for Codex and Claude Code. Codex
automatically discovers the repository Skill from `.agents/skills/`; Claude
Code has a small repository entry point that directs it to the same public
Skill. Neither contains development prompts or private project notes.

### Set it up yourself

Requirements:

- Python 3.9 or later;
- a local PHREEQC installation and the database you intend to use;
- Git, if cloning from GitHub.

```bash
git clone https://github.com/songsongr/auto-phreeqc-public.git
cd auto-phreeqc-public
python scripts/bootstrap.py
```

The setup command creates `.auto-phreeqc-venv/`, installs the public package, searches for
PHREEQC, writes discovered paths to the untracked
`.phreeqc-auto.local.json`, and runs a disposable calculation. A successful
health-check report means this checkout is ready to use.

If PHREEQC is installed in a nonstandard location, pass its paths explicitly:

```bash
python scripts/bootstrap.py \
  --phreeqc-exe /path/to/phreeqc \
  --database /path/to/phreeqc.dat
```

On Windows PowerShell, use the same command on one line, replacing the two
paths with your `phreeqc.exe` and `phreeqc.dat` locations. You may instead set
`PHREEQC_EXE` and `PHREEQC_DATABASE`; these environment variables take
precedence over the local configuration file.

## Use natural language for a calculation

Once setup passes, open the repository as your agent workspace and describe
your task. The Skill asks for conditions that materially affect a result,
summarizes assumptions before a run, and preserves the input, raw output,
structured data, and figures in a separate result directory.

For example:

```text
Calculate the calcite saturation index for water at 25 °C and pH 7.2 with
80 mg/L Ca and 200 mg/L alkalinity as CaCO3. First summarize the units,
database, and assumptions. Wait for my confirmation before running, then give
me the result table and a chart.
```

For a parameter scan or transport model, also specify (or let the agent ask
for) the variable range, number of steps, time unit, cell count, and outputs
to track. See the [agent guide](docs/agent-usage.md) for the full workflow and
the public [Skill](skills/phreeqc-auto/SKILL.md) for its modelling rules.

## Local Workbench

The Workbench is a local browser interface for editing, running, and reviewing
models. It uses the same public runtime as the agent workflow, so it works
without an AI assistant after first-time setup.

```bash
# Windows
.\start.windows.bat

# macOS, Linux, or Git Bash
./start.unix.sh
```

Open <http://127.0.0.1:8765/>. The server listens only on your local computer.

## Python library

The package is useful when your own program needs repeatable, file-based
PHREEQC runs:

```python
from pathlib import Path

from phreeqc_auto import (
    generate_single_simulation,
    parse_selected_output,
    run_simulation,
    write_input_file,
)

run_dir = Path("runs/calcite")
params = {
    "solution": {
        "id": 1,
        "units": "mg/L",
        "temp": 25.0,
        "pH": 7.2,
        "components": {"Ca": 80, "Alkalinity": "200 as CaCO3"},
    },
    "selected_output": {"pH": True, "si": ["Calcite"], "totals": ["Ca"]},
}

input_path = write_input_file(
    generate_single_simulation(params, output_file="selected_output.txt"),
    str(run_dir / "input.pqi"),
)
result = run_simulation(
    input_path,
    output_file=str(run_dir / "output.qpo"),
    cwd=str(run_dir),
)
if not result["success"]:
    raise RuntimeError(result["error"])

selected_output = parse_selected_output(str(run_dir / "selected_output.txt"))
print(selected_output["columns"])
```

## Included examples

Each example includes an input file, a coordinator script, and expected output
artefacts. Copy an example into a new results directory before changing it.

| Level | Example | Model focus |
| --- | --- | --- |
| L1 | `task1_1_pb_speciation` | Pb speciation in NaCl solution |
| L1 | `task1_2_calcite_si` | Calcite saturation index and pH sensitivity |
| L1 | `task1_3_SimpleMix` | Seawater and freshwater mixing |
| L2 | `task2_1_cd_adsorption` | Cd adsorption edge and surface complexation |
| L2 | `task2_2_amd_neutralization` | Acid mine drainage neutralization |
| L2 | `task2_3_cation_exchange` | Cation exchange during saline intrusion |
| L3 | `task3_1_pyrite_kinetics` | Pyrite dissolution kinetics |
| L3 | `task3_2_as_transport` | One-dimensional reactive arsenic transport |
| L3 | `task3_3_co2_injection` | Multiphase evolution during CO₂ injection |

## Reproducibility and limits

- Save the input file, PHREEQC output, selected output, figures, and the
  database name with every result.
- Treat default values and unmeasured redox conditions as assumptions, not
  observations.
- Results depend on the selected thermodynamic database and model choices.
  Inspect convergence warnings before interpreting a result.
- This toolkit is not affiliated with or endorsed by USGS. For research,
  cite PHREEQC and this project as appropriate; see [CITATION.cff](CITATION.cff).

## Development and support

- [Chinese documentation](docs/README.zh-CN.md)
- [Agent workflow](docs/agent-usage.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [MIT License](LICENSE)

To verify the public Python package after a development checkout:

```bash
python -m pytest tests -v
```
