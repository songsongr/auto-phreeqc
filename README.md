# phreeqc-auto 🔬

[![CI](https://github.com/songsongr/auto-phreeqc/actions/workflows/ci.yml/badge.svg)](https://github.com/songsongr/auto-phreeqc/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)

**Automated geochemical simulation workflows for PHREEQC**, powered by Claude Code.

> PHREEQC is a computer program for speciation, batch-reaction, one-dimensional transport,
> and inverse geochemical calculations developed by the U.S. Geological Survey (USGS).

This project provides a **Claude Code Skill** (`phreeqc-auto`) that enables natural-language-driven
geochemical modeling — describe your simulation in plain language, and the skill handles
input generation, execution, output parsing, and visualization.

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

**As a Claude Code Skill:**

```bash
# In Claude Code, simply describe your simulation:
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
.claude/skills/phreeqc-auto/
├── SKILL.md                          # Claude Code skill definition
├── scripts/
│   ├── generate_input.py             # PHREEQC input file generation
│   ├── run_phreeqc.py                # PHREEQC runner
│   ├── parse_output.py               # Output parser
│   └── visualize.py                  # Visualization tools
└── references/
    ├── coordinator_template.py       # Coordinator script template
    ├── pb_speciation_example.md      # Example: Pb speciation
    ├── calcite_si_example.md         # Example: Calcite saturation index
    ├── seawater_mixing_example.md    # Example: Seawater + pure water mixing
    ├── cd_adsorption_edge_example.md # Example: Cd adsorption on Fe-Mn oxides
    ├── amd_neutralization_example.md # Example: Acid mine drainage neutralization
    ├── cation_exchange_example.md    # Example: Cation exchange in seawater intrusion
    ├── pyrite_kinetics_example.md    # Example: Pyrite oxidation kinetics
    ├── arsenic_transport_example.md  # Example: 1D As reactive transport
    ├── extreme_co2_injection_example.md  # Example: Supercritical CO₂ injection
    ├── cd_music_modeling_guide.md    # CD-MUSIC surface complexation modeling
    └── goethite_birnessite_surface_params.md  # Surface parameters reference
```

---

## 📚 Examples

Nine benchmark examples across three difficulty levels are documented in `references/`:

| Level | Example | Description |
|-------|---------|-------------|
| 🟢 L1 | Pb speciation | Pb species distribution in NaCl solution |
| 🟢 L1 | Calcite SI | Saturation index vs pH sensitivity analysis |
| 🟢 L1 | Seawater mixing | Simple dilution of seawater with pure water |
| 🟡 L2 | Cd adsorption | Surface complexation on Fe-Mn oxides |
| 🟡 L2 | AMD neutralization | Acid mine drainage + limestone treatment |
| 🟡 L2 | Cation exchange | Seawater intrusion ion exchange |
| 🔴 L3 | Pyrite kinetics | Mineral dissolution kinetics |
| 🔴 L3 | As transport | 1D reactive transport with adsorption |
| 🔴 L3 | CO₂ injection | Supercritical CO₂ multiphase evolution |

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
