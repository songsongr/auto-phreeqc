"""
PHREEQC Pb Speciation Coordinator
===================================
考题 1.1: 铅形态分布
pH=6.0, 10 mmol/L NaCl, 1 mg/L Pb, pe=12 O2(g) -0.68
"""
import sys, os

PROJECT_ROOT = r"C:\Users\songsongr\Desktop\claudecodel_proj\auto_phreeqc_proj"
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "phreeqc-auto", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(WORKSPACE, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

from generate_input import generate_single_simulation, write_input_file
from run_phreeqc import run_simulation, find_database
from parse_output import (
    parse_selected_output,
    extract_saturation_indices,
    extract_species_distribution,
    extract_element_molalities,
    to_json,
)
from visualize import plot_saturation_indices

# ============================================================
# Step 1: 构建参数 & 生成输入文件
# ============================================================
print("=" * 60)
print("Step 1/4: 生成 PHREEQC 输入文件...")
print("=" * 60)

# 计算: 10 mmol/L NaCl = 0.010 mol/L
# Na: 0.010 * 22.9897 g/mol = 0.229897 g/L = 229.9 mg/L
# Cl: 0.010 * 35.453 g/mol = 0.35453 g/L = 354.5 mg/L

params = {
    "solution": {
        "id": 1,
        "units": "mg/L",
        "temp": 25.0,
        "pH": 6.0,
        "pe": 12.0,  # will be overridden in post-processing
        "density": 1.0,
        "components": {
            "Na": 229.9,      # 10 mmol/L
            "Cl": 354.5,      # 10 mmol/L
            "Pb": 1.0,        # 1 mg/L
        },
    },
    "selected_output": {
        "si": ["Pb(OH)2", "PbO", "Cerussite", "Anglesite", "Galena"],
        "totals": ["Pb", "Na", "Cl"],
        "molalities": [
            "Pb+2", "PbOH+", "Pb(OH)2", "Pb(OH)3-",
            "PbCl+", "PbCl2", "PbCl3-", "PbCl4-2",
            "PbHCO3+", "PbCO3", "Pb(CO3)2-2",
            "PbO2", "HPbO2-",
        ],
        "pH": True,
        "pe": True,
    },
}

content = generate_single_simulation(params, output_file="selected_output.txt")

# Fix: replace "pe 12.0" with "pe 12 O2(g) -0.68" (user-specified syntax)
content = content.replace("pe 12.0", "pe 12 O2(g) -0.68")

# Add TITLE block at the top
content = "TITLE Pb speciation -- pH 6.0, 10 mmol/L NaCl, 1 mg/L Pb, pe=12 O2(g) -0.68\n\n" + content

input_path = write_input_file(content, os.path.join(WORKSPACE, "input.pqi"))
print(f"  [OK] Input file: {input_path}")

# Show the generated input
print()
print("Generated input.pqi:")
print("-" * 40)
with open(input_path) as f:
    print(f.read())
print("-" * 40)

# ============================================================
# Step 2: 运行 PHREEQC
# ============================================================
print()
print("=" * 60)
print("Step 2/4: 运行 PHREEQC...")
print("=" * 60)

db_path = find_database("phreeqc.dat")
result = run_simulation(
    input_file=input_path,
    output_file=os.path.join(WORKSPACE, "output.qpo"),
    database=db_path,
    timeout=120,
    cwd=WORKSPACE,
)

if not result["success"]:
    print(f"  [FAIL] Simulation failed: {result['error']}")
    if result['stderr']:
        print(f"  [STDERR] {result['stderr']}")
    if not result['stderr'] and result['stdout']:
        print(f"  [STDOUT] {result['stdout'][:2000]}")
    sys.exit(1)
print(f"  [OK] Simulation succeeded (exit code: {result['exit_code']})")

# ============================================================
# Step 3: 解析输出
# ============================================================
print()
print("=" * 60)
print("Step 3/4: 解析输出...")
print("=" * 60)

with open(os.path.join(WORKSPACE, "output.qpo"), "r", encoding="utf-8", errors="replace") as f:
    output_text = f.read()

si_data = extract_saturation_indices(output_text)
species_data = extract_species_distribution(output_text)
element_data = extract_element_molalities(output_text)
print(f"  [OK] Saturation indices: {len(si_data)} minerals")
print(f"  [OK] Species distribution: {len(species_data)} species")
print(f"  [OK] Element molalities: {len(element_data)} elements")

selected_file = os.path.join(WORKSPACE, "selected_output.txt")
selected_data = {}
if os.path.isfile(selected_file):
    selected_data = parse_selected_output(selected_file)
    print(f"  [OK] Selected output: {selected_data.get('row_count', 0)} rows")

json_output = to_json(
    selected_data, si_data, species_data, element_data,
    metadata={
        "simulation": "Pb speciation",
        "pH": 6.0,
        "pe": 12.0,
        "redox_couple": "O2(g) -0.68",
        "NaCl": "10 mmol/L",
        "Pb": "1 mg/L",
        "database": "phreeqc.dat",
    },
)
json_path = os.path.join(WORKSPACE, "results.json")
with open(json_path, "w", encoding="utf-8") as f:
    f.write(json_output)
print(f"  [OK] JSON: {json_path}")

# ============================================================
# Step 4: 可视化
# ============================================================
print()
print("=" * 60)
print("Step 4/4: 生成图表...")
print("=" * 60)

si_chart = plot_saturation_indices(
    {"saturation_indices": si_data},
    title="Saturation Indices - Pb Speciation (pH 6.0, 10 mM NaCl, 1 mg/L Pb)",
    filepath=os.path.join(CHARTS_DIR, "saturation_indices.png"),
)
print(f"  [OK] Chart: {si_chart}")

# ============================================================
# Results summary
# ============================================================
print()
print("=" * 60)
print("Pb Speciation Results")
print("=" * 60)

if si_data:
    print()
    print("Saturation Indices:")
    for s in si_data:
        marker = "SATURATED" if s["si"] >= 0 else "undersaturated"
        print(f"  {s['phase']:<20} {s['si']:>8.2f}  ({marker})")

if species_data:
    print()
    print("Pb Species Distribution:")
    pb_species = [s for s in species_data if "Pb" in s["species"] or "pb" in s["species"].lower()]
    if pb_species:
        total_pb = sum(s["molality"] for s in pb_species)
        print(f"  Total Pb molality: {total_pb:.6e} mol/kgw")
        print(f"  Total Pb concentration: {total_pb * 207.2 * 1000:.4f} ug/L (1 mg/L input)")
        print()
        print(f"  {'Species':<25} {'Molality':<18} {'Activity':<18} {'% of Pb':<12}")
        print(f"  {'-'*25} {'-'*18} {'-'*18} {'-'*12}")
        for s in sorted(pb_species, key=lambda x: x["molality"], reverse=True):
            pct = (s["molality"] / total_pb * 100) if total_pb > 0 else 0
            print(f"  {s['species']:<25} {s['molality']:<18.6e} {s['activity']:<18.6e} {pct:<12.2f}")
    else:
        print("  No Pb-specific species found in output")
        print()
        print("  All species:")
        for s in species_data[:20]:
            print(f"  {s['species']:<25} {s['molality']:<18.6e} {s['activity']:<18.6e}")

if element_data:
    print()
    print("Element Molalities:")
    for elem, mol in element_data.items():
        print(f"  {elem:<8} {mol:.6e} mol/kgw")

print()
print("=" * 60)
print(f"  [OK] Simulation complete!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {si_chart}")
print("=" * 60)
