# auto-phreeqc 🔬

[简体中文](docs/README.zh-CN.md)

[![CI](https://github.com/songsongr/auto-phreeqc-public/actions/workflows/ci.yml/badge.svg)](https://github.com/songsongr/auto-phreeqc-public/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)

`auto-phreeqc` is a user-facing toolkit for PHREEQC geochemical modelling.
It provides a reusable Python package, a local browser Workbench, nine
reproducible examples, and concise guidance for using an AI coding assistant
to turn a simulation description into a reproducible PHREEQC run.

PHREEQC itself is developed by the U.S. Geological Survey (USGS) for
speciation, batch-reaction, reactive transport, and inverse geochemical
calculations.

## What is included

- `phreeqc_auto/`: generate inputs, locate PHREEQC, run calculations, parse
  outputs, and make plots.
- `workbench/`: a local Web Workbench for editing, running, and reviewing
  simulations without writing Python.
- `examples/`: nine curated simulations, from aqueous speciation to reactive
  transport.
- `skills/phreeqc-auto/`: a compact, user-facing skill for Claude Code or
  Codex-compatible workflows. See [agent usage](docs/agent-usage.md).

## Quick start

Install the project and point it at a local PHREEQC installation:

```bash
git clone https://github.com/songsongr/auto-phreeqc-public.git
cd auto-phreeqc-public
python -m pip install -e ".[dev]"

# macOS / Linux
export PHREEQC_EXE="/path/to/phreeqc"
export PHREEQC_DATABASE="/path/to/phreeqc.dat"

# Windows PowerShell
$env:PHREEQC_EXE = "C:\\path\\to\\phreeqc.exe"
$env:PHREEQC_DATABASE = "C:\\path\\to\\phreeqc.dat"
```

The package looks first at these environment variables, then at `PATH` and
standard installation locations. PHREEQC is not bundled with this repository.

### Python API

```python
from pathlib import Path

from phreeqc_auto.generate_input import generate_single_simulation, write_input_file
from phreeqc_auto.parse_output import parse_selected_output
from phreeqc_auto.run_phreeqc import run_simulation

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
if result["success"]:
    selected = parse_selected_output(str(run_dir / "selected_output.txt"))
    print(selected)
else:
    print(result["error"])
```

Run the automated checks with:

```bash
python -m pytest tests -v
```

## Local Workbench

Start the local browser UI with the launcher for your system:

```bash
# Windows
.\start.windows.bat

# macOS / Linux / Git Bash
./start.unix.sh
```

Then open <http://127.0.0.1:8765/>. The Workbench calls the same public
`phreeqc_auto` package as the command-line examples; it does not require an
AI assistant to be installed.

## Examples

The following nine examples are retained as runnable, user-facing references:

| Level | Example | Folder |
| --- | --- | --- |
| L1 | Pb speciation | `examples/task1_1_pb_speciation/` |
| L1 | Calcite saturation index | `examples/task1_2_calcite_si/` |
| L1 | Seawater mixing | `examples/task1_3_SimpleMix/` |
| L2 | Cd adsorption edge | `examples/task2_1_cd_adsorption/` |
| L2 | AMD neutralization | `examples/task2_2_amd_neutralization/` |
| L2 | Cation exchange | `examples/task2_3_cation_exchange/` |
| L3 | Pyrite kinetics | `examples/task3_1_pyrite_kinetics/` |
| L3 | Arsenic transport | `examples/task3_2_as_transport/` |
| L3 | CO₂ injection | `examples/task3_3_co2_injection/` |

Each example contains a coordinator script and its expected artefacts. Use
them as starting points, then adapt the parameters to your own system.

## Documentation and contributing

- [Chinese documentation](docs/README.zh-CN.md)
- [Workbench guide](docs/workbench-README.zh-CN.md)
- [Using Claude Code or Codex](docs/agent-usage.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## License and disclaimer

This project is licensed under the [MIT License](LICENSE). It is not
affiliated with or endorsed by the USGS. Cite PHREEQC appropriately in
research; see [CITATION.cff](CITATION.cff).
