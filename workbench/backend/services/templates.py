"""
Built-in simulation templates.

Each template corresponds to one of the 9 verified reference examples
documented in ``.claude/skills/phreeqc-auto/references/``. The
``instantiate(tpl)`` step deep-copies the params so that subsequent edits
by the user do not mutate the master template.
"""

from __future__ import annotations

import copy
from typing import Any


# ---------------------------------------------------------------------------
# Master template definitions
# ---------------------------------------------------------------------------

_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "pb_speciation",
        "level": "L1",
        "title": "Pb speciation in NaCl solution",
        "summary": "10 mmol/L NaCl, 1 mg/L Pb, pH 6.0; identifies dominant Pb species and saturation indices.",
        "params": {
            "solution": {
                "id": 1,
                "units": "mmol/kgw",
                "temp": 25.0,
                "pH": 6.0,
                "pe": 12.0,
                "components": {
                    "Na": 10.0,
                    "Cl": 10.0,
                    "Pb": 0.004828,  # 1 mg/L ≈ 4.828e-3 mmol/kgw
                },
            },
            "selected_output": {
                "pH": True,
                "pe": True,
                "si": [
                    "Pb(OH)2", "Cerussite", "Anglesite", "PbO",
                    "Galena", "Hydrocerrusite", "Laurionite",
                ],
                "totals": ["Pb", "Na", "Cl"],
                "molalities": ["Pb+2", "PbOH+", "PbCl+", "PbCl2", "PbCl3-", "Pb(OH)2", "Pb(OH)3-"],
            },
        },
    },
    {
        "id": "calcite_si",
        "level": "L1",
        "title": "Calcite saturation index at given pH",
        "summary": "Ca 80 mg/L, alkalinity 200 mg/L as HCO3, pH 7.2; tracks Calcite SI across pH 6-8.5.",
        "params": {
            "solution": {
                "id": 1,
                "units": "ppm",
                "temp": 25.0,
                "pH": 7.2,
                "pe": 4.0,
                "components": {
                    "Ca": 80.0,
                    "C(4)": 200.0,
                    # 200 mg/L as HCO3 -> 200 mg/L as HCO3- alkalinity
                },
            },
            "equilibrium_phases": {"Calcite": (0.0, 10.0)},
            "selected_output": {
                "pH": True,
                "si": ["Calcite", "Aragonite", "Dolomite", "Siderite"],
                "totals": ["Ca", "C(4)", "Alkalinity"],
            },
        },
    },
    {
        "id": "seawater_mixing",
        "level": "L1",
        "title": "Seawater + pure water mixing",
        "summary": "500 mL seawater mixed with 500 mL pure water; verifies halving of ionic strength.",
        "params": {
            "solutions": [
                {
                    "id": 1,
                    "units": "ppm",
                    "temp": 25.0,
                    "pH": 8.22,
                    "pe": 8.451,
                    "components": {
                        "Ca": 412.3, "Mg": 1291.8, "Na": 10768.0, "K": 399.1,
                        "Cl": 19353.0, "S(6)": 2712.0, "Alkalinity": "141.682 as HCO3",
                    },
                },
                {
                    "id": 2,
                    "units": "mol/kgw",
                    "temp": 25.0,
                    "pH": 7.0,
                    "pe": 4.0,
                    "components": {},
                },
            ],
            "mix": {"id": 1, "solutions": {1: 0.5, 2: 0.5}},
            "selected_output": {
                "pH": True,
                "si": ["Calcite", "Aragonite", "Dolomite"],
                "totals": ["Ca", "Mg", "Na", "Cl", "K", "S(6)"],
            },
        },
    },
    {
        "id": "cd_adsorption",
        "level": "L2",
        "title": "Cd adsorption on Fe-Mn oxides",
        "summary": "0.1 g goethite + birnessite in 25 mL solution, Cd 100 ug/L, pH 3-9 scan via NaOH titration.",
        "params": {
            "solution": {
                "id": 1,
                "units": "mmol/kgw",
                "temp": 25.0,
                "pH": 5.0,
                "pe": 12.0,
                "components": {
                    "Na": 10.0,
                    "N(5)": 10.0,
                    "Cd": 0.000889,  # 100 ug/L ≈ 8.89e-4 mmol/kgw
                },
            },
            "selected_output": {
                "pH": True,
                "totals": ["Cd", "Na", "N(5)"],
                "molalities": ["Cd+2", "CdOH+", "Cd(OH)2", "CdNO3+"],
            },
        },
    },
    {
        "id": "amd_neutralization",
        "level": "L2",
        "title": "AMD neutralization with limestone",
        "summary": "Acid mine drainage (pH 2, Fe 500, Al 200 mg/L) titrated with Calcite to pH 7.",
        "params": {
            "solution": {
                "id": 1,
                "units": "ppm",
                "temp": 25.0,
                "pH": 2.0,
                "pe": 4.0,
                "components": {
                    "Fe(2)": 500.0, "Fe(3)": 50.0, "Al": 200.0, "Mn": 50.0,
                    "S(6)": 2600.0,
                },
            },
            "equilibrium_phases": {
                "Fe(OH)3(a)": (0.0, 10.0),
                "Gibbsite": (0.0, 10.0),
                "Gypsum": (0.0, 10.0),
                "Calcite": (0.0, 10.0),
            },
            "reaction": {
                "reactants": {"Calcite": 1.0},
                "moles": 0.03,
                "steps": 100,
            },
            "selected_output": {
                "step": True,
                "pH": True,
                "pe": True,
                "si": ["Fe(OH)3(a)", "Gibbsite", "Gypsum", "Calcite"],
                "totals": ["Fe(2)", "Fe(3)", "Al", "Mn", "S(6)", "Ca"],
                "equilibrium_phases": ["Fe(OH)3(a)", "Gibbsite", "Gypsum", "Calcite"],
            },
        },
    },
    {
        "id": "cation_exchange",
        "level": "L2",
        "title": "Cation exchange (seawater intrusion)",
        "summary": "Freshwater with Ca-saturated exchanger titrated by NaCl 0-0.3 mol.",
        "params": {
            "solution": {
                "id": 1,
                "units": "ppm",
                "temp": 25.0,
                "pH": 7.2,
                "pe": 4.0,
                "components": {"Ca": 80.0, "C(4)": 200.0, "Cl": 50.0},
            },
            "exchange": {
                "block_id": 1,
                "sites": "X",
                "moles": 0.05,
                "equilibrate": 1,
            },
            "reaction": {
                "reactants": {"NaCl": 1.0},
                "moles": 0.3,
                "steps": 30,
            },
            "selected_output": {
                "step": True,
                "pH": True,
                "totals": ["Ca", "Na", "Cl", "K", "Mg"],
            },
        },
    },
    {
        "id": "pyrite_kinetics",
        "level": "L3",
        "title": "Pyrite oxidation kinetics",
        "summary": "Pyrite + O2 kinetic dissolution with Fe(OH)3 precipitation over 100 days.",
        "params": {
            "solution": {
                "id": 1,
                "units": "mol/kgw",
                "temp": 25.0,
                "pH": 7.0,
                "pe": 8.0,
                "components": {},
            },
            "equilibrium_phases": {"Fe(OH)3(a)": (0.0, 0.0)},
            "kinetics": {
                "reactants": [{
                    "name": "Pyrite",
                    "formula": "FeS2",
                    "m": 1.0,
                    "m0": 1.0,
                    "parms": [0.01],
                    "steps": [8640000],  # 100 days in seconds
                    "steps_n": 50,
                }],
            },
            "rates": [{
                "name": "Pyrite",
                "code": [
                    "rem Williamson & Rimstidt (1994)",
                    "rate = 10.0e-10 * (1.0 - SR(\"Pyrite\"))",
                    "moles = rate * TIME",
                    "SAVE moles",
                ],
            }],
            "selected_output": {
                "step": True,
                "pH": True,
                "pe": True,
                "si": ["Pyrite", "Fe(OH)3(a)", "Goethite", "Siderite"],
                "totals": ["Fe(2)", "Fe(3)", "S(6)", "S(-2)"],
                "equilibrium_phases": ["Fe(OH)3(a)"],
            },
        },
    },
    {
        "id": "as_transport",
        "level": "L3",
        "title": "1D reactive transport (As breakthrough)",
        "summary": "20-cell column, As injected at inlet; tracks breakthrough at outlet.",
        "params": {
            "solutions": [
                {
                    "id": 0,
                    "units": "mol/kgw",
                    "temp": 25.0,
                    "pH": 7.0,
                    "pe": 12.0,
                    "components": {"As": 0.001},
                },
            ],
            "initial_cell_solution": {
                "units": "mol/kgw",
                "temp": 25.0,
                "pH": 7.0,
                "pe": 4.0,
            },
            "transport": {
                "cells": 20,
                "length": 1.0,
                "shifts": 100,
                "time_step": 0.05,
                "time_units": "day",
                "flow_direction": "forward",
                "dispersivity": 0.01,
                "punch_cells": [20],
                "punch_frequency": 1,
            },
            "selected_output": {
                "step": True,
                "totals": ["As"],
                "pH": True,
            },
        },
    },
    {
        "id": "co2_injection",
        "level": "L3",
        "title": "Supercritical CO2 injection",
        "summary": "CO2(g) injected at 200 atm with kinetic K-feldspar dissolution and Kaolinite precipitation.",
        "params": {
            "solution": {
                "id": 1,
                "units": "mol/kgw",
                "temp": 100.0,
                "pH": 7.5,
                "pe": -4.0,
                "components": {
                    "Ca": 0.01, "C(4)": 0.01, "Na": 0.1, "Cl": 0.1,
                },
            },
            "gas_phase": {
                "block_id": 1,
                "fixed_pressure": True,
                "pressure": 200.0,
                "components": {"CO2(g)": 0.0},
            },
            "equilibrium_phases": {"Calcite": (0.0, 10.0)},
            "kinetics": {
                "reactants": [
                    {
                        "name": "K-feldspar",
                        "formula": "KAlSi3O8",
                        "m": 3.0,
                        "m0": 3.0,
                        "parms": [0.2],
                        "steps": [315576000],  # 10 years in seconds
                        "steps_n": 20,
                        "cvode": True,
                    },
                ],
            },
            "rates": [{
                "name": "K-feldspar",
                "code": [
                    "rem Palandri & Kharaka (2004)",
                    "k_neut_25 = 10^(-12.41)",
                    "rate = k_neut_25 * (1.0 - SR(\"K-feldspar\"))",
                    "moles = rate * TIME",
                    "SAVE moles",
                ],
            }],
            "selected_output": {
                "step": True,
                "totals": ["Ca", "K", "Al", "Si", "C(4)"],
                "si": ["Calcite", "K-feldspar", "Kaolinite"],
                "equilibrium_phases": ["Calcite"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def list_templates() -> list[dict]:
    return [
        {
            "id": t["id"],
            "level": t["level"],
            "title": t["title"],
            "summary": t["summary"],
        }
        for t in _TEMPLATES
    ]


def get_template(tpl_id: str) -> dict | None:
    for t in _TEMPLATES:
        if t["id"] == tpl_id:
            return copy.deepcopy(t)
    return None


def instantiate(tpl: dict) -> dict:
    """Return a deep-copied params dict for the given template."""
    return copy.deepcopy(tpl["params"])
