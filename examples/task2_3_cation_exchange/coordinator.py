"""
Task 2.3: Cation Exchange — Seawater Intrusion into Freshwater Aquifer.

Simulates progressive seawater intrusion (NaCl addition) into a
Ca-saturated clay exchanger, tracking Ca2+ displacement and release
into solution ("淡水端钙离子浓度的升高情况").

Workflow: generate -> run -> parse -> visualize
"""

import json
import os
import re
import sys

# --- Path setup ---
project_root = r"C:\Users\songsongr\Desktop\claudecodel_proj\auto_phreeqc_proj"
sys.path.insert(0, os.path.join(project_root, ".claude", "skills", "phreeqc-auto", "scripts"))

from generate_input import (
    generate_single_simulation,
    write_input_file,
)
from run_phreeqc import run_simulation
from parse_output import (
    parse_selected_output,
    extract_saturation_indices,
    extract_species_distribution,
    extract_element_molalities,
    extract_ionic_strength,
    extract_exchange_composition,
)
from visualize import plot_selected_output_sweep, plot_saturation_indices

WORKSPACE = os.path.join(project_root, "workspace", "task2_3_cation_exchange")
INPUT_FILE = os.path.join(WORKSPACE, "input.pqi")
OUTPUT_FILE = os.path.join(WORKSPACE, "output.qpo")
SELECTED_FILE = "selected_output.txt"
RESULTS_FILE = os.path.join(WORKSPACE, "results.json")

print("=" * 70)
print("Task 2.3: Cation Exchange — Seawater Intrusion into Freshwater Aquifer")
print("=" * 70)

# =========================================================================
# STEP 1: Generate Input
# =========================================================================
print("\n[STEP 1] Generating PHREEQC input file...")

params = {
    "solution": {
        "id": 1,
        "units": "ppm",
        "temp": 25.0,
        "pH": 7.2,
        "pe": 4.0,
        "density": 1.0,
        "components": {
            "Ca": 80.0,
            "Mg": 24.0,
            "Na": 23.0,
            "K": 3.0,
            "Alkalinity": "200 as CaCO3",
            "Cl": 35.0,
            "S(6)": 50.0,
            "Fe": 0.1,
            "Mn": 0.05,
        },
    },
    "exchange": {
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
        "totals": ["Ca", "Mg", "Na", "K", "Cl"],
        "si": ["Calcite", "Dolomite", "Gypsum", "Halite"],
        "pH": True,
        "pe": True,
    },
}

content = generate_single_simulation(params, output_file=SELECTED_FILE)
input_path = write_input_file(content, INPUT_FILE)
print(f"  [OK] Input: {input_path}")

# =========================================================================
# STEP 2: Run Simulation
# =========================================================================
print("\n[STEP 2] Running PHREEQC simulation...")
result = run_simulation(
    input_file=INPUT_FILE,
    output_file=OUTPUT_FILE,
    cwd=WORKSPACE,
    timeout=120,
)

if not result["success"]:
    print(f"  [FAIL] {result['error']}")
    sys.exit(1)
print(f"  [OK] Simulation completed")

# =========================================================================
# STEP 3: Parse Output
# =========================================================================
print("\n[STEP 3] Parsing output...")

# --- Selected Output ---
so_path = os.path.join(WORKSPACE, SELECTED_FILE)
so_data = parse_selected_output(so_path)
columns = so_data["columns"]
raw_data = so_data["data"]
print(f"  [OK] Selected output: {so_data['row_count']} rows, cols={len(columns)}")

# --- Standard Output ---
with open(OUTPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
    otxt = f.read()

si_final = extract_saturation_indices(otxt, last=True)
species_final = extract_species_distribution(otxt, last=True)
elements_final = extract_element_molalities(otxt, last=True)
is_final = extract_ionic_strength(otxt, last=True)
exchange_final = extract_exchange_composition(otxt, last=True)

# --- Filter reaction steps (state="react") ---
state_idx = columns.index("state") if "state" in columns else None
rx_data = []
for row in raw_data:
    if state_idx is not None:
        if row[state_idx] == "react":
            rx_data.append(row)
    else:
        rx_data.append(row)

n_init = so_data["row_count"] - len(rx_data)
print(f"  [OK] Reaction steps: {len(rx_data)} ({n_init} initial soln rows filtered)")

# --- Extract step-by-step exchange composition ---
# Split output by "Exchange composition" sections
ex_sections = []
for i, line in enumerate(otxt.splitlines()):
    s = line.strip()
    if "Exchange composition" in s and s.startswith("-"):
        ex_sections.append(i)

# Parse exchange composition for each step
exchange_steps = []
for sect_start in ex_sections:
    # Take 30 lines starting from section header
    section_text = "\n".join(otxt.splitlines()[sect_start:sect_start + 30])
    ex_data = extract_exchange_composition(section_text)
    if ex_data:
        exchange_steps.append(ex_data)

# Skip the initial exchange (before batch-reaction), keep reaction steps
if len(exchange_steps) > len(rx_data):
    exchange_steps = exchange_steps[-len(rx_data):]

print(f"  [OK] Exchange steps parsed: {len(exchange_steps)}")

# =========================================================================
# STEP 4: Key Results
# =========================================================================
print("\n" + "=" * 70)
print("RESULTS: Seawater Intrusion Cation Exchange")
print("=" * 70)

ca_idx = columns.index("Ca") if "Ca" in columns else None
na_idx = columns.index("Na") if "Na" in columns else None
mg_idx = columns.index("Mg") if "Mg" in columns else None
cl_idx = columns.index("Cl") if "Cl" in columns else None
k_idx = columns.index("K") if "K" in columns else None
ph_idx = columns.index("pH") if "pH" in columns else None
rxn_idx = columns.index("reaction") if "reaction" in columns else None

# --- Step-by-step table ---
print(f"\n  {'Step':>4s} {'NaCl_add':>9s}  {'Ca_soln':>9s}  {'Na_soln':>9s}  {'Cl_soln':>9s}  {'pH':>6s}  {'Ex_NaX%':>8s}  {'Ex_CaX2%':>8s}")
print(f"  {'-'*4} {'-'*9}  {'-'*9}  {'-'*9}  {'-'*9}  {'-'*6}  {'-'*8}  {'-'*8}")

for i, row in enumerate(rx_data):
    rxn = row[rxn_idx] if rxn_idx is not None else (i + 1) * 0.01
    ca = row[ca_idx] if ca_idx is not None else float('nan')
    na = row[na_idx] if na_idx is not None else float('nan')
    cl = row[cl_idx] if cl_idx is not None else float('nan')
    ph = row[ph_idx] if ph_idx is not None else float('nan')

    # Get exchange fractions for this step
    ex_nax_pct = 0.0
    ex_cax2_pct = 0.0
    if i < len(exchange_steps):
        for ex in exchange_steps[i]:
            if ex["species"] == "NaX":
                ex_nax_pct = ex["eq_frac"] * 100
            elif ex["species"] == "CaX2":
                ex_cax2_pct = ex["eq_frac"] * 100

    if i < 8 or i >= len(rx_data) - 5 or i % 5 == 0:
        print(f"  {i+1:4d} {rxn:9.4f}  {ca:9.6f}  {na:9.6f}  {cl:9.6f}  {ph:6.2f}  {ex_nax_pct:7.1f}%  {ex_cax2_pct:7.1f}%")

# --- Exchange composition evolution ---
print(f"\n  Exchange Composition Evolution (key steps):")
print(f"  {'Step':>5s} {'NaCl_add':>9s}  {'NaX_mol':>10s}  {'CaX2_mol':>10s}  {'MgX2_mol':>10s}  {'NaX%':>7s}  {'CaX2%':>7s}")
print(f"  {'-'*5} {'-'*9}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*7}  {'-'*7}")
key_indices = [0, 4, 9, 14, 19, 24, 29]
for idx in key_indices:
    if idx >= len(exchange_steps):
        break
    rxn = rx_data[idx][rxn_idx] if rxn_idx is not None else (idx + 1) * 0.01
    ex = exchange_steps[idx]
    nax = next((e["moles"] for e in ex if e["species"] == "NaX"), 0)
    cax2 = next((e["moles"] for e in ex if e["species"] == "CaX2"), 0)
    mgx2 = next((e["moles"] for e in ex if e["species"] == "MgX2"), 0)
    nax_pct = next((e["eq_frac"] for e in ex if e["species"] == "NaX"), 0) * 100
    cax2_pct = next((e["eq_frac"] for e in ex if e["species"] == "CaX2"), 0) * 100
    print(f"  {idx+1:5d} {rxn:9.4f}  {nax:10.6f}  {cax2:10.6f}  {mgx2:10.6f}  {nax_pct:6.1f}%  {cax2_pct:6.1f}%")

# --- Ca mass balance ---
print(f"\n  Calcium Mass Balance:")
if ca_idx is not None and len(rx_data) > 0:
    ca_aq_initial = rx_data[0][ca_idx]  # mol/kgw in solution
    ca_aq_final = rx_data[-1][ca_idx]
    ca_aq_increase = ca_aq_final - ca_aq_initial

    # Exchange Ca change
    if len(exchange_steps) >= 2:
        ca_ex_initial = next((e["moles"] for e in exchange_steps[0] if e["species"] == "CaX2"), 0)
        ca_ex_final = next((e["moles"] for e in exchange_steps[-1] if e["species"] == "CaX2"), 0)
        ca_ex_decrease = ca_ex_initial - ca_ex_final
    else:
        ca_ex_initial = float('nan')
        ca_ex_final = float('nan')
        ca_ex_decrease = float('nan')

    print(f"    Ca in solution: {ca_aq_initial:.6f} -> {ca_aq_final:.6f} mol/kgw")
    print(f"      = {ca_aq_initial * 40078:.1f} -> {ca_aq_final * 40078:.1f} mg/L  "
          f"(increase: +{ca_aq_increase * 40078:.1f} mg/L, {ca_aq_increase / ca_aq_initial * 100:.0f}%)")
    print(f"    Ca on exchanger: {ca_ex_initial:.6f} -> {ca_ex_final:.6f} mol")
    print(f"      = {ca_ex_initial * 40078:.1f} -> {ca_ex_final * 40078:.1f} mg  "
          f"(decrease: -{ca_ex_decrease * 40078:.1f} mg)")

    # Verify conservation: Ca_ex_decrease (mol/0.05mol_X) should equal Ca_aq_increase (mol/kgw)
    # Since exchanger is 0.05 mol X sites per ~1 kg water (approx)
    print(f"    Ca released from exchanger: {ca_ex_decrease * 40078:.1f} mg  (per 0.05 mol X sites)")
    print(f"    Ca gained in solution:      {ca_aq_increase * 40078:.1f} mg  (per kg water)")

# --- Final exchange composition ---
print(f"\n  Final Exchange Assemblage ({len(exchange_final)} species):")
for ex in exchange_final:
    print(f"    {ex['species']:10s}  {ex['moles']:.6f} mol  "
          f"eq={ex['equivalents']:.6f}  frac={ex['eq_frac']:.4f}")

# --- Final state summary ---
print(f"\n  Final Solution State:")
print(f"    Ionic strength: {is_final:.4f} mol/kgw")
print(f"    pH: {rx_data[-1][ph_idx]:.2f}" if ph_idx is not None else "    pH: N/A")

print(f"\n  Key Saturation Indices (relevant to Ca/Na):")
for si in si_final:
    if si["phase"] in ("Calcite", "Dolomite", "Gypsum", "Halite", "Anhydrite"):
        flag = "[SAT]" if si["si"] >= 0 else "[UNDER]"
        print(f"    {si['phase']:15s}  SI = {si['si']:7.3f}  {flag}")

# =========================================================================
# STEP 5: Save Results
# =========================================================================
print("\n[STEP 5] Saving structured results...")

# Build exchange summary array
ex_summary = []
for i, ex in enumerate(exchange_steps):
    rxn = rx_data[i][rxn_idx] if rxn_idx is not None and i < len(rx_data) else (i + 1) * 0.01
    entry = {"step": i + 1, "NaCl_added_mol": rxn}
    for e in ex:
        entry[f"ex_{e['species']}_moles"] = e["moles"]
        entry[f"ex_{e['species']}_eq_frac"] = e["eq_frac"]
    ex_summary.append(entry)

results = {
    "selected_output_columns": so_data["columns"],
    "selected_output_data": so_data["data"],
    "n_reaction_steps": len(rx_data),
    "saturation_indices_final": si_final,
    "species_distribution_final": species_final[:20],
    "element_molalities_final": elements_final,
    "ionic_strength_final": is_final,
    "exchange_composition_final": exchange_final,
    "exchange_composition_steps": ex_summary,
    "metadata": {
        "task": "2.3_cation_exchange",
        "description": "Seawater intrusion — Na+ displaces Ca2+ on clay exchanger",
        "freshwater": "Ca-HCO3 type, Ca 80 ppm, Na 23 ppm, pH 7.2",
        "exchanger": "0.05 mol X sites, Ca-saturated (equilibrated with freshwater)",
        "reaction": "NaCl 0.3 mol in 30 steps",
        "key_finding": (
            f"Ca increased from {rx_data[0][ca_idx] * 40078:.1f} to "
            f"{rx_data[-1][ca_idx] * 40078:.1f} mg/L (+{((rx_data[-1][ca_idx] - rx_data[0][ca_idx]) / rx_data[0][ca_idx] * 100):.0f}%), "
            f"NaX fraction from "
            f"{next((e['eq_frac'] for e in exchange_steps[0] if e['species'] == 'NaX'), 0) * 100:.1f}% to "
            f"{next((e['eq_frac'] for e in exchange_steps[-1] if e['species'] == 'NaX'), 0) * 100:.1f}%"
        ),
    },
}

with open(RESULTS_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"  [OK] Results: {RESULTS_FILE}")

# =========================================================================
# STEP 6: Visualize
# =========================================================================
print("\n[STEP 6] Creating charts...")

# Chart 1: Ca & Na in solution vs reaction progress
chart1 = os.path.join(WORKSPACE, "charts", "ca_na_vs_intrusion.png")
if ca_idx is not None and na_idx is not None:
    plot_selected_output_sweep(
        so_data, x_column="reaction", y_columns=["Ca", "Na"],
        title="Ca & Na in Solution vs Seawater Intrusion (NaCl addition)",
        xlabel="NaCl added (mol)", filepath=chart1,
    )
    print(f"  [OK] {chart1}")

# Chart 2: All cations
chart2 = os.path.join(WORKSPACE, "charts", "cations_vs_intrusion.png")
cation_cols = [c for c in ["Ca", "Mg", "Na", "K"] if c in columns]
if cation_cols:
    plot_selected_output_sweep(
        so_data, x_column="reaction", y_columns=cation_cols,
        title="Major Cations vs Seawater Intrusion Progress",
        xlabel="NaCl added (mol)", filepath=chart2,
    )
    print(f"  [OK] {chart2}")

# Chart 3: SI bar chart
chart3 = os.path.join(WORKSPACE, "charts", "si_final.png")
if si_final:
    plot_saturation_indices(
        si_final, title="Final Saturation Indices after Seawater Intrusion",
        filepath=chart3,
    )
    print(f"  [OK] {chart3}")

print(f"\n{'=' * 70}")
print("Task 2.3 COMPLETE!")
print(f"  Workspace: {WORKSPACE}")
print(f"  Results:   {RESULTS_FILE}")
print(f"  Charts:    {WORKSPACE}/charts/")
print(f"{'=' * 70}")
