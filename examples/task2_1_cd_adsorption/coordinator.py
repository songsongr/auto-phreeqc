"""
考题 2.1 - Cd 在 Goethite + Birnessite 上的 pH 吸附边

REACTION 滴定法: 从 pH=3 开始逐步加 NaOH, 表面始终参与平衡
0.1g 铁锰结核粉末 (Goethite 20% + Birnessite 20%)
25mL 溶液, Cd 100 ug/L, NaNO3 0.01 M
"""

import sys, os, json

project_root = r"C:\Users\songsongr\Desktop\claudecodel_proj\auto_phreeqc_proj"
sys.path.insert(0, os.path.join(project_root, ".claude", "skills", "phreeqc-auto", "scripts"))

from generate_input import (
    generate_surface_master_species_block,
    generate_surface_species_block,
    generate_surface_block,
    generate_solution_block,
    generate_reaction_block,
    generate_selected_output_block,
    write_input_file,
)
from run_phreeqc import run_simulation
from parse_output import parse_selected_output

WORKSPACE = os.path.join(project_root, "workspace", "task2_1_cd_adsorption")
CHARTS = os.path.join(WORKSPACE, "charts")
os.makedirs(CHARTS, exist_ok=True)

# ── Build input: one simulation with REACTION sweep ─────────────────────
blocks = []

# TITLE
blocks.append("TITLE Cd adsorption edge on Goethite + Birnessite (pH 3-9)")

# Custom SURFACE_MASTER_SPECIES
blocks.append(generate_surface_master_species_block([
    {"name": "Gth_s", "formula": "Gth_sOH"},
    {"name": "Mn_s",  "formula": "Mn_sOH"},
    {"name": "Mn_w",  "formula": "Mn_wOH"},
]))

# Custom SURFACE_SPECIES
blocks.append(generate_surface_species_block([
    # Goethite
    {"reaction": "Gth_sOH = Gth_sOH",               "log_k": 0.0},
    {"reaction": "Gth_sOH + H+ = Gth_sOH2+",        "log_k": 9.0},
    {"reaction": "Gth_sOH = Gth_sO- + H+",          "log_k": -9.0},
    {"reaction": "Gth_sOH + Cd+2 = Gth_sOCd+ + H+", "log_k": 1.0},
    # Birnessite strong
    {"reaction": "Mn_sOH = Mn_sOH",                  "log_k": 0.0},
    {"reaction": "Mn_sOH + H+ = Mn_sOH2+",           "log_k": 2.5},
    {"reaction": "Mn_sOH = Mn_sO- + H+",             "log_k": -5.0},
    {"reaction": "Mn_sOH + Cd+2 = Mn_sOCd+ + H+",    "log_k": -1.0},
    # Birnessite weak
    {"reaction": "Mn_wOH = Mn_wOH",                  "log_k": 0.0},
    {"reaction": "Mn_wOH + H+ = Mn_wOH2+",           "log_k": 2.5},
    {"reaction": "Mn_wOH = Mn_wO- + H+",             "log_k": -5.0},
    {"reaction": "Mn_wOH + Cd+2 = Mn_wOCd+ + H+",    "log_k": -2.5},
]))

# SOLUTION: 25 mL, pH 3.0, NaNO3 0.01 M, Cd 100 ug/L
blocks.append(
    "SOLUTION 1\n"
    "    units mol/kgw\n"
    "    -water 0.025\n"
    "    pH    3.0\n"
    "    pe    4.0\n"
    "    temp  25.0\n"
    "    Na    0.01\n"
    "    N(5)  0.01\n"
    "    Cd    8.9e-7"
)

# SURFACE: Goethite 0.02g + Birnessite 0.02g
blocks.append(generate_surface_block([
    {"name": "Gth_sOH", "site_density": "5e-6",  "ssa": "50",   "mass": "0.02"},
    {"name": "Mn_sOH",  "site_density": "5e-6",  "ssa": "600",  "mass": "0.02"},
    {"name": "Mn_wOH",  "site_density": "2e-4"},
], block_id=1))

# REACTION: NaOH titration
# 0.025 kg water at pH 3: [H+] = 1e-3 M, H+ moles = 2.5e-5 mol
# Surface sites act as massive H+ buffer: ~2.5e-3 mol sites total
# To reach pH 9, must neutralize solution H+ + deprotonate surface sites
# Estimate: 2.5e-5 mol (solution H+) + surface deprotonation buffer
# From v4 test: 3.5e-5 mol NaOH covered pH 3.0→7.3
# Extrapolate: 7e-5 mol reached pH 7.9; need ~1.2e-4 for pH 9
blocks.append(generate_reaction_block(
    reactants={"NaOH": 1.0},
    block_id=1,
    moles=1.2e-4,
    steps=30,
))

# SELECTED_OUTPUT
blocks.append(generate_selected_output_block(
    file="selected_output.txt",
    reset=True,
    pH=True,
    pe=False,
    temperature=False,
    totals=["Cd", "Na"],
    molalities=["Gth_sOCd+", "Mn_sOCd+", "Mn_wOCd+", "Cd+2"],
))

blocks.append("END")

full_input = "\n\n".join(blocks)

input_path = os.path.join(WORKSPACE, "input.pqi")
write_input_file(full_input, input_path)
print(f"[OK] Input written: {input_path}")
print(f"--- input.pqi ---")
print(full_input[:2000])
print(f"... ({len(full_input)} chars total)")

# ── Run PHREEQC ─────────────────────────────────────────────────────────
result = run_simulation(
    input_file=input_path,
    output_file=os.path.join(WORKSPACE, "output.qpo"),
    cwd=WORKSPACE,
)

if not result["success"]:
    print(f"\n[FAIL] PHREEQC returned error:\n{result.get('stderr', '')[:2000]}")
    sys.exit(1)
print(f"\n[OK] PHREEQC finished: exit_code={result['exit_code']}")

# ── Parse ───────────────────────────────────────────────────────────────
selected_path = os.path.join(WORKSPACE, "selected_output.txt")
if not os.path.exists(selected_path):
    print(f"[FAIL] selected_output.txt not found in {WORKSPACE}")
    for root, dirs, files in os.walk(WORKSPACE):
        for f in files:
            print(f"  Found: {os.path.join(root, f)}")
    sys.exit(1)

result_parsed = parse_selected_output(selected_path)
if "error" in result_parsed:
    print(f"[FAIL] Parse error: {result_parsed['error']}")
    sys.exit(1)

headers = result_parsed["columns"]
data_rows = result_parsed["data"]
print(f"\n[OK] Parsed {result_parsed['row_count']} rows, {len(headers)} columns")
print(f"  Headers: {headers}")

# ── Calculate Cd sorbed % ───────────────────────────────────────────────
results = []
for row in data_rows:
    row_dict = dict(zip(headers, row))
    try:
        ph = float(row_dict.get("pH", 0))
        cd_tot = float(row_dict.get("Cd", 0))
        cd_aq = float(row_dict.get("m_Cd+2", 0))
        cd_gth = float(row_dict.get("m_Gth_sOCd+", 0))
        cd_mns = float(row_dict.get("m_Mn_sOCd+", 0))
        cd_mnw = float(row_dict.get("m_Mn_wOCd+", 0))
    except (ValueError, TypeError) as e:
        print(f"  Skip row: {e} -> {row}")
        continue

    cd_sorbed = cd_gth + cd_mns + cd_mnw
    cd_mass_balance = cd_aq + cd_sorbed
    # Use mass-balance denominator (aq + sorbed) instead of -totals Cd,
    # which can drift due to REACTION dilution
    cd_sorbed_pct = (cd_sorbed / cd_mass_balance * 100) if cd_mass_balance > 0 else 0.0

    results.append({
        "step": len(results) + 1,
        "pH": ph,
        "Cd_sorbed_pct": cd_sorbed_pct,
        "Cd_total_mol": cd_tot,
        "Cd_aq_mol": cd_aq,
        "Cd_sorbed_Gth": cd_gth,
        "Cd_sorbed_Mn_s": cd_mns,
        "Cd_sorbed_Mn_w": cd_mnw,
    })

# ── Output ──────────────────────────────────────────────────────────────
print(f"\n{'='*80}")
print(f"  Cd Adsorption pH Edge Results (Goethite 0.02g + Birnessite 0.02g)")
print(f"{'='*80}")
print(f"{'Step':>5} {'pH':>6} {'Sorbed%':>8} {'Cd_aq(mol)':>14} {'Gth_sOCd+':>14} {'Mn_sOCd+':>14} {'Mn_wOCd+':>14}")
print(f"{'-'*80}")
for r in results:
    print(f"{r['step']:5d} {r['pH']:6.2f} {r['Cd_sorbed_pct']:7.2f}% {r['Cd_aq_mol']:14.3e} {r['Cd_sorbed_Gth']:14.3e} {r['Cd_sorbed_Mn_s']:14.3e} {r['Cd_sorbed_Mn_w']:14.3e}")

# Save
with open(os.path.join(WORKSPACE, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

# Text chart
print(f"\n{'='*80}")
print(f"  Cd Sorbed % vs pH")
print(f"{'='*80}")
valid = [r for r in results if r['Cd_sorbed_pct'] > 0]
max_pct = max(r["Cd_sorbed_pct"] for r in valid) if valid else 1.0
for r in results:
    bar_len = max(1, int(r["Cd_sorbed_pct"] / max_pct * 50))
    bar = "#" * bar_len
    print(f"  pH {r['pH']:5.2f} |{bar:<50} {r['Cd_sorbed_pct']:6.1f}%")

print(f"\n[DONE] Results saved to {os.path.join(WORKSPACE, 'results.json')}")

# ── Visualization ───────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    ph_vals = [r["pH"] for r in results]
    sorb_pct = [r["Cd_sorbed_pct"] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Cd Sorbed % vs pH
    ax1.plot(ph_vals, sorb_pct, "o-", color="#d62728", linewidth=2, markersize=5, label="Total Cd sorbed")
    ax1.axvline(x=4.54, color="gray", linestyle="--", alpha=0.5, label="50% at pH 4.54")
    ax1.axhline(y=50, color="gray", linestyle="--", alpha=0.5)
    ax1.set_xlabel("pH")
    ax1.set_ylabel("Cd Sorbed (%)")
    ax1.set_title("Cd Adsorption Edge: Goethite + Birnessite")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(2.5, 9.5)
    ax1.set_ylim(-5, 105)

    # Right: Species distribution (stacked area)
    total_arr = np.array([r["Cd_aq_mol"] + r["Cd_sorbed_Gth"] + r["Cd_sorbed_Mn_s"] + r["Cd_sorbed_Mn_w"] for r in results])
    frac_aq = np.array([r["Cd_aq_mol"] / t * 100 for r, t in zip(results, total_arr)])
    frac_mnw = np.array([r["Cd_sorbed_Mn_w"] / t * 100 for r, t in zip(results, total_arr)])
    frac_mns = np.array([r["Cd_sorbed_Mn_s"] / t * 100 for r, t in zip(results, total_arr)])
    frac_gth = np.array([r["Cd_sorbed_Gth"] / t * 100 for r, t in zip(results, total_arr)])

    ax2.fill_between(ph_vals, 0, frac_aq, alpha=0.7, color="#1f77b4", label="Cd$^{2+}$(aq)")
    ax2.fill_between(ph_vals, frac_aq, frac_aq + frac_mnw, alpha=0.7, color="#ff7f0e", label="Mn$_w$OCd$^+$")
    ax2.fill_between(ph_vals, frac_aq + frac_mnw, frac_aq + frac_mnw + frac_mns, alpha=0.7, color="#2ca02c", label="Mn$_s$OCd$^+$")
    ax2.fill_between(ph_vals, frac_aq + frac_mnw + frac_mns, np.ones_like(ph_vals) * 100, alpha=0.7, color="#9467bd", label="Gth$_s$OCd$^+$")
    ax2.set_xlabel("pH")
    ax2.set_ylabel("Cd Species (%)")
    ax2.set_title("Cd Speciation vs pH")
    ax2.legend(fontsize=8, loc="center left")
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(2.5, 9.5)
    ax2.set_ylim(0, 105)

    plt.tight_layout()
    chart_path = os.path.join(CHARTS, "cd_adsorption_edge.png")
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[CHART] Saved to {chart_path}")
except ImportError as e:
    print(f"[WARN] matplotlib not available: {e}")
