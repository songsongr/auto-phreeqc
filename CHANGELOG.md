# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with Claude Code skill (`phreeqc-auto`)
- Core Python scripts:
  - `generate_input.py` — PHREEQC input file generation
  - `run_phreeqc.py` — PHREEQC execution wrapper
  - `parse_output.py` — Output parsing utilities
  - `visualize.py` — Matplotlib-based visualization
- 9 benchmark examples across 3 difficulty levels:
  - L1: Pb speciation, Calcite SI, Seawater mixing
  - L2: Cd adsorption, AMD neutralization, Cation exchange
  - L3: Pyrite kinetics, As reactive transport, CO₂ injection
- Reference documents for each example workflow
- Coordinator script template for 4-step pipeline automation
- CD-MUSIC surface complexation modeling guide
- Support for SOLUTION, EQUILIBRIUM_PHASES, EXCHANGE, SURFACE, KINETICS,
  TRANSPORT, GAS_PHASE, REACTION, MIX, SELECTED_OUTPUT blocks
- pH scanning via REACTION titration method
- Visualizations: SI vs pH, speciation pie charts, breakthrough curves,
  adsorption edges, time-series plots
