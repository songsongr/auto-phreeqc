# phreeqc-auto 🔬

[![CI](https://github.com/songsongr/auto-phreeqc/actions/workflows/ci.yml/badge.svg)](https://github.com/songsongr/auto-phreeqc/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)

**Automated geochemical simulation workflows for PHREEQC**, designed for use from any agent terminal.

> PHREEQC is a computer program for speciation, batch-reaction, one-dimensional transport,
> and inverse geochemical calculations developed by the U.S. Geological Survey (USGS).

This project provides agent-ready workflows for natural-language-driven geochemical modeling.
Describe your simulation in plain language, and the workflow handles input generation,
execution, output parsing, and visualization. It can be used from any agent terminal;
Codex and Claude Code are listed below as examples.

---

## ✨ Features

- **🧪 Natural-language to simulation**: Describe your experiment in plain text, get a complete PHREEQC simulation
- **📂 4‑step pipeline**: Generate input → Run PHREEQC → Parse output → Visualize results
- **📊 Rich visualizations**: pH scans, titration curves, breakthrough curves, speciation pie charts, time-series plots
- **📚 9 verified example workflows** covering 3 difficulty levels, from basic speciation to reactive transport
- **🐍 Standalone Python library**: Use `generate_input.py`, `run_phreeqc.py`, `parse_output.py`, and `visualize.py` independently

### Supported simulation types

| Type | Examples |
|------|----------|
| Speciation | Pb speciation in seawater, carbonate system analysis |
| Batch reaction | Mineral dissolution/precipitation, titration, mixing |
| Surface complexation | Cd adsorption edges (Goethite/Birnessite) |
| Ion exchange | Seawater intrusion, freshwater-saltwater interaction |
| Kinetics | Pyrite oxidation, Fe²⁺ oxidation |
| Reactive transport | 1D advection-dispersion, As breakthrough curves |
| Extreme conditions | Supercritical CO₂ injection, high P/T systems |

---

## 🚀 Quick Start

### Prerequisites

1. **PHREEQC** installed (v3.8.6+)
   - Download from [USGS PHREEQC website](https://www.usgs.gov/software/phreeqc-geochemical-modeling)
   - Set `PHREEQC_EXE` environment variable to your executable path

2. **Python** 3.9+ with required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **PHREEQC database**:
   - Download `phreeqc.dat` (or another database) from your PHREEQC installation
   - Set `PHREEQC_DATABASE` environment variable to the database path

### Environment variables

```bash
# Required
export PHREEQC_EXE="/path/to/phreeqc.exe"
export PHREEQC_DATABASE="/path/to/phreeqc.dat"
```

### Usage

**From an agent terminal (for example, Codex or Claude Code):**

```bash
# Simply describe your simulation:
# "Simulate calcite saturation index in seawater at pH 7-9"
```

**As a standalone Python library:**

```python
from scripts.generate_input import generate_single_simulation
from scripts.run_phreeqc import run_phreeqc
from scripts.parse_output import extract_saturation_indices
from scripts.visualize import plot_si_vs_ph

# Generate input
input_text = generate_single_simulation(
    solutions=[{
        "number": 1,
        "components": {
            "pH": 7.2, "temp": 25.0,
            "Ca": 80, "Alkalinity": "200 as HCO3",
        }
    }]
)

# Run simulation
output = run_phreeqc(input_text, output_dir="./results")

# Parse results
si_data = extract_saturation_indices(output)

# Visualize
plot_si_vs_ph(si_data, "Calcite")
```

---

## 📁 Project Structure

```
.                                       # repo root
├── README.md / CLAUDE.md / LICENSE     # project metadata
├── pyproject.toml / uv.lock            # Python package definition + lockfile
├── start.unix.sh                       # launcher for macOS / Linux / Git Bash
├── start.windows.bat                   # launcher for Windows cmd
├── .gitignore
│
├── .claude/skills/phreeqc-auto/        # Claude Code skill (see SKILL.md)
├── .github/                            # CI workflows, Pages, Discussions
├── docs/                               # long-form docs (GitHub Pages site)
│
├── workbench/                          # PHREEQC Web Workbench (zero-dep, stdlib only)
│   ├── start.unix.sh / start.windows.bat
│   ├── backend/app.py                  # stdlib HTTP server (REST + SSE)
│   ├── backend/services/               # locator, registry, runner, storage, templates, importer
│   ├── frontend/                       # bundled React, Babel, and ECharts assets
│   └── workspace_workbench/            # runtime-generated runs (gitignored)
│
├── examples/                           # curated reference simulations (one per task)
│   ├── task1_1_pb_speciation/
│   ├── task1_2_calcite_si/
│   ├── task1_3_SimpleMix/
│   ├── task2_1_cd_adsorption/
│   ├── task2_2_amd_neutralization/
│   ├── task2_3_cation_exchange/
│   ├── task3_1_pyrite_kinetics/
│   ├── task3_2_as_transport/
│   ├── task3_3_co2_extended/
│   └── task3_3_co2_injection/
│
└── external_runs/                      # default watch dir for WebBench external-run importer
```

---

## 📚 Examples

Nine benchmark examples across three difficulty levels are documented in `references/`.
Each example also ships a ready-to-run folder under `examples/` (one subdirectory per
task), so you can `cd examples/task1_1_pb_speciation/` and re-run the simulation with
your local PHREEQC install.

| Level | Example | `examples/` folder | Description |
|-------|---------|--------------------|-------------|
| 🟢 L1 | Pb speciation | `task1_1_pb_speciation/` | Pb species distribution in NaCl solution |
| 🟢 L1 | Calcite SI | `task1_2_calcite_si/` | Saturation index vs pH sensitivity analysis |
| 🟢 L1 | Seawater mixing | `task1_3_SimpleMix/` | Simple dilution of seawater with pure water |
| 🟡 L2 | Cd adsorption | `task2_1_cd_adsorption/` | Surface complexation on Fe-Mn oxides |
| 🟡 L2 | AMD neutralization | `task2_2_amd_neutralization/` | Acid mine drainage + limestone treatment |
| 🟡 L2 | Cation exchange | `task2_3_cation_exchange/` | Seawater intrusion ion exchange |
| 🔴 L3 | Pyrite kinetics | `task3_1_pyrite_kinetics/` | Mineral dissolution kinetics |
| 🔴 L3 | As transport | `task3_2_as_transport/` | 1D reactive transport with adsorption |
| 🔴 L3 | CO₂ injection | `task3_3_co2_injection/` | Supercritical CO₂ multiphase evolution |

---

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/songsongr/auto-phreeqc.git
cd auto-phreeqc

# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Run tests
pytest .claude/skills/phreeqc-auto/scripts/test_scripts.py
```

---

## 🖥 WebUI Workbench

A self-hosted browser UI is included under [`workbench/`](workbench/)
that wraps the skill with a REST + SSE API and an ECharts-powered
result inspector.  No new Python packages are added — the backend is
built on the standard library, and the frontend bundles its React, Babel,
and ECharts assets for local use. See [`workbench/README.md`](workbench/README.md) for
architecture, API conventions, and the full list of 9 built-in
templates.

Quick start:

```bash
# Windows  (cmd.exe / Windows Terminal / PowerShell)
.\start.windows.bat

# macOS / Linux / Git Bash on Windows
./start.unix.sh        # or: bash workbench/start.unix.sh
```

Then open <http://127.0.0.1:8765/>.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

This project is **not affiliated with or endorsed by the U.S. Geological Survey (USGS)**.
PHREEQC is a USGS product and should be cited accordingly when used in research:

> Parkhurst, D.L. and Appelo, C.A.J., 2013. Description of input and examples for PHREEQC
> version 3 — A computer program for speciation, batch-reaction, one-dimensional transport,
> and inverse geochemical calculations. USGS Techniques and Methods, book 6, chap. A43, 497 p.
