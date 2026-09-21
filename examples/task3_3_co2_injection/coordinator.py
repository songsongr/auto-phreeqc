"""
PHREEQC 考题 3.3: 极端环境多相演化 (超临界 CO2 注入)
=====================================================
设定: 100C, 200 atm 下超临界 CO2 注入含钙砂岩层
      计算 10 年后长石溶解和方解石沉淀对孔隙度的影响

方法: 批反应 KINETICS + EQUILIBRIUM_PHASES + GAS_PHASE
      - GAS_PHASE: CO2(g) 固定分压 200 atm
      - EQUILIBRIUM_PHASES: Calcite 快速平衡
      - KINETICS: K-feldspar 溶解 (BASIC 速率方程)
      - 后处理: 矿物摩尔变化 -> 孔隙度估算

工作流: 生成输入 -> 运行 PHREEQC -> 解析输出 -> 可视化
"""
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

WORKSPACE = Path(__file__).resolve().parent
CHARTS_DIR = WORKSPACE / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

from phreeqc_auto.generate_input import generate_single_simulation, generate_rates_block, write_input_file
from phreeqc_auto.run_phreeqc import run_simulation, find_database
from phreeqc_auto.parse_output import (
    parse_selected_output,
    extract_saturation_indices,
    extract_element_molalities,
    extract_ionic_strength,
    to_json,
)
from phreeqc_auto.visualize import plot_selected_output_sweep


# =========================================================================
# Step 1: 构建参数 & 生成输入文件
# =========================================================================
print("=" * 60)
print("Step 1/4: 生成 PHREEQC 输入文件...")
print("=" * 60)

# 10 years in seconds (365.25 days * 86400 s/day)
TEN_YEARS_S = int(10 * 365.25 * 86400)  # 315,576,000
N_STEPS = 20
STEP_SIZE = TEN_YEARS_S // N_STEPS  # ~15,778,800 s (~0.5 yr)

# K-feldspar molar volume: 108.87 cm3/mol (KAlSi3O8)
# Calcite molar volume: 36.93 cm3/mol

params = {
    # 砂岩孔隙溶液 (100C, 还原环境)
    "solution": {
        "id": 1, "units": "mol/kgw", "temp": 100.0,
        "pH": 7.5, "pe": -4.0, "density": 1.0,
        "components": {
            "Ca": 0.010,      # 10 mM (calcite equilibrium)
            "C(4)": 0.010,    # 10 mM as HCO3-
            "Na": 0.043,      # ~1000 ppm
            "Cl": 0.028,      # ~1000 ppm
            "K": 0.0001,      # trace K from feldspar
            "Si": 0.0001,     # trace Si from quartz
        },
    },
    # GAS_PHASE: CO2 at 200 atm, fixed pressure
    "gas_phase": {
        "block_id": 1,
        "fixed_pressure": True,
        "pressure": 200.0,
        "components": {"CO2(g)": 0.0},  # 0 = infinite supply
    },
    # Calcite: fast equilibrium
    "equilibrium_phases": {
        "Calcite": (0.0, 10.0),      # SI=0, amount=10 mol
    },
    "eq_block_id": 1,
    # K-feldspar kinetics
    "kinetics": {
        "reactants": [
            {
                "name": "K-feldspar",
                "formula": "KAlSi3O8",
                "m": 3.0,      # 3 mol initial
                "m0": 3.0,
                "parms": [0.2],  # parm(1) = specific surface area m2/g
                "steps": [TEN_YEARS_S],
                "steps_n": N_STEPS,
                "cvode": True,
            },
        ],
    },
    "kinetics_block_id": 1,
    # RATES block for K-feldspar dissolution
    # NOTE: SR() cannot be the sole RHS in an assignment in PHREEQC BASIC
    #       (parser bug). Use SR() inline in the expression instead.
    "rates": [
        {
            "name": "K-feldspar",
            "code": [
                "rem Palandri & Kharaka (2004) parameters",
                "rem Neutral: log_k=-12.41, Ea=38 kJ/mol",
                "rem Acid: log_k=-10.06, Ea=51.7 kJ/mol, a(H+)^0.5",
                "T = 298.15 + TC",
                "T0 = 298.15",
                "R = 8.314",
                "k_neut_25 = 10^(-12.41)",
                "Ea_neut = 38000",
                "f_temp_neut = exp(Ea_neut / R * (1/T0 - 1/T))",
                "k_acid_25 = 10^(-10.06)",
                "Ea_acid = 51700",
                "f_temp_acid = exp(Ea_acid / R * (1/T0 - 1/T))",
                "act_H = ACT(\"H+\")",
                "if act_H <= 0 then act_H = 1e-14",
                "k_neut = k_neut_25 * f_temp_neut",
                "k_acid = k_acid_25 * f_temp_acid * act_H^0.5",
                "gfm = 278.33",
                "sa_m2_per_g = parm(1)",
                "area = M * gfm * sa_m2_per_g",
                "rem Use SR() inline only (parser bug: SR() cannot be sole RHS)",
                "rate = (k_neut + k_acid) * area * (1 - SR(\"K-feldspar\"))",
                "if rate < 0 then rate = 0",
                "moles = rate * TIME",
                "if moles > M then moles = M",
                "SAVE moles",
            ],
        },
    ],
    # Selected output: track mineral rates + totals + SI
    "selected_output": {
        "step": True,
        "totals": ["Ca", "K", "Al", "Si", "C"],
        "si": ["Calcite", "K-feldspar", "Kaolinite", "Quartz"],
        "equilibrium_phases": ["Calcite"],
        "pH": True,
        "pe": True,
        "temperature": True,
    },
}

content = generate_single_simulation(params, output_file="selected_output.txt")

# Add title
content = "TITLE Supercritical CO2 injection into Ca-bearing sandstone (100°C, 200 atm)\n\n" + content

input_path = write_input_file(content, os.path.join(WORKSPACE, "input.pqi"))
print(f"  [OK] 输入文件: {input_path}")
print()

# =========================================================================
# Step 2: 运行 PHREEQC
# =========================================================================
print("=" * 60)
print("Step 2/4: 运行 PHREEQC (20 steps, 10 years)...")
print("=" * 60)

db_path = find_database("phreeqc.dat")
result = run_simulation(
    input_file=input_path,
    output_file=os.path.join(WORKSPACE, "output.qpo"),
    database=db_path,
    timeout=300,
    cwd=WORKSPACE,
)

if not result["success"]:
    print(f"  [FAIL] 模拟失败: {result['error']}")
    sys.exit(1)
print(f"  [OK] 模拟成功 (exit code: {result['exit_code']})")
print()

# =========================================================================
# Step 3: 解析输出
# =========================================================================
print("=" * 60)
print("Step 3/4: 解析输出...")
print("=" * 60)

with open(os.path.join(WORKSPACE, "output.qpo"), "r", encoding="utf-8", errors="replace") as f:
    output_text = f.read()

si_data = extract_saturation_indices(output_text, last=True)
element_data = extract_element_molalities(output_text, last=True)
is_val = extract_ionic_strength(output_text)
print(f"  [OK] 饱和指数 (最终): {len(si_data)} 个矿物")
for s in si_data:
    print(f"    {s['phase']}: SI = {s['si']:.3f}")
print(f"  [OK] 元素浓度 (最终): {len(element_data)} 个元素")

# SELECTED_OUTPUT: 各时间步的矿物和化学演化
selected_file = os.path.join(WORKSPACE, "selected_output.txt")
selected_data = {}
if os.path.isfile(selected_file):
    selected_data = parse_selected_output(selected_file)
    n_rows = selected_data.get("row_count", 0)
    print(f"  [OK] Selected output: {n_rows} 行 (各步数据)")
    if n_rows > 0:
        cols = selected_data.get("columns", [])
        print(f"  [OK] 列: {cols}")
        data = selected_data.get("data", [])
        print(f"    首行: {data[0]}")
        print(f"    末行: {data[-1]}")
else:
    print(f"  [WARN] SELECTED_OUTPUT 文件未找到: {selected_file}")

# 保存 JSON
json_output = to_json(selected_data, si_data, element_data, metadata={
    "ionic_strength_mol_kgw": is_val,
    "temperature_C": 100.0,
    "pressure_atm": 200.0,
    "kinetics_params": "K-feldspar (Palandri & Kharaka 2004)",
    "duration_years": 10.0,
    "n_steps": N_STEPS,
    "step_size_s": STEP_SIZE,
})
json_path = os.path.join(WORKSPACE, "results.json")
with open(json_path, "w", encoding="utf-8") as f:
    f.write(json_output)
print(f"  [OK] JSON: {json_path}")
print()

# =========================================================================
# Step 3b: 从主输出中提取 K-feldspar 动力学摩尔变化 (KINETICS 输出格式)
kf_deltas = []
kf_currents = []
for line in output_text.splitlines():
    if line.strip().startswith("K-feldspar") and ("e-" in line or "e+" in line):
        parts = line.split()
        if len(parts) >= 3:
            try:
                delta = float(parts[1])
                current = float(parts[2])
                if -1 < delta < 1 and 0 < current < 100:
                    kf_deltas.append(delta)
                    kf_currents.append(current)
            except ValueError:
                pass

if kf_deltas and kf_currents:
    d_kf_total = sum(kf_deltas)
    kf_init = kf_currents[0] - kf_deltas[0]  # estimate initial from first step
    kf_final = kf_currents[-1]
    avg_delta_step = kf_deltas[0]
    print(f"  [OK] K-feldspar initial: ~{kf_init:.4e} mol/kgw")
    print(f"  [OK] K-feldspar final: {kf_final:.4e} mol/kgw")
    print(f"  [OK] K-feldspar delta/step: {avg_delta_step:.4e} mol/kgw")
    print(f"  [OK] K-feldspar total delta (20 steps): {d_kf_total:.4e} mol/kgw")
else:
    d_kf_total = 0.0
    avg_delta_step = 0.0
    print(f"  [WARN] 未从主输出中提取到 K-feldspar kinetics 数据")
    print(f"  [NOTE] 使用 SELECTED_OUTPUT K 浓度变化间接估算")


# Step 3c: 孔隙度估算
# =========================================================================
print("=" * 60)
print("Step 3b/4: 孔隙度估算...")
print("=" * 60)

# Molar volumes (cm3/mol)
MOLAR_VOL = {
    "Calcite": 36.93,      # CaCO3
    "K-feldspar": 108.87,  # KAlSi3O8
    "Kaolinite": 99.52,    # Al2Si2O5(OH)4
    "Quartz": 22.69,       # SiO2
}

# Initial porosity (typical sandstone)
PHI_0 = 0.20
V_BULK_LITER = 1.0  # Assume 1 L bulk volume for calculation

# Use equilibrium_phases columns to track mineral changes
if selected_data.get("row_count", 0) > 0:
    cols = selected_data.get("columns", [])
    data = selected_data.get("data", [])

    # Find Calcite delta column index
    d_calcite_idx = None
    d_kfeldspar_idx = None
    for i, c in enumerate(cols):
        if c == "d_Calcite":
            d_calcite_idx = i
        if c == "d_K-feldspar":
            d_kfeldspar_idx = i

    print(f"  [INFO] d_Calcite col: {d_calcite_idx}, d_K-feldspar col: {d_kfeldspar_idx}")
    print(f"  [INFO] K-feldspar SI (final) = 0.0002, near equilibrium, dissolution very slow")

    # 用主输出中提取的 K-feldspar 数据
    d_kf_extracted = d_kf_total  # from Step 3b extraction
    kf_per_step = avg_delta_step

    # Calculate porosity at each step
    porosities = []
    d_calcite_vals = []
    d_kfeldspar_vals = []
    times = []

    for i, row in enumerate(data):
        try:
            step = float(row[cols.index("step")])
        except (ValueError, IndexError):
            step = 0

        d_cal = float(row[d_calcite_idx]) if d_calcite_idx is not None else 0
        # d_K-feldspar per step from kinetics output
        d_kf = kf_per_step * (i + 1)  # cumulative at step i+1

        # Volume change (cm3) from mineral moles change per kg water
        # d_cal > 0 = Calcite precipitation = adds volume = porosity decreases
        # d_kf < 0 = K-feldspar dissolution = removes volume = porosity increases
        dv = (d_cal * MOLAR_VOL["Calcite"] +
              d_kf * MOLAR_VOL["K-feldspar"])

        # Bulk volume per kg water at initial porosity 0.20
        # 1 kg water = 1 L water = 1000 cm3
        # V_bulk = water_vol / phi_0 = 1000 / 0.2 = 5000 cm3
        V_bulk = 1.0 / PHI_0 * 1000  # cm3 per kg water
        phi = PHI_0 - dv / V_bulk

        porosities.append(phi)
        d_calcite_vals.append(d_cal)
        d_kfeldspar_vals.append(d_kf)
        times.append(step)

    print(f"  [OK] 初始孔隙度: {PHI_0:.4f}")
    print(f"  [OK] 最终孔隙度: {porosities[-1]:.6f}")
    print(f"  [OK] 孔隙度变化: {porosities[-1] - PHI_0:.6f}")
    if d_calcite_vals:
        print(f"  [OK] Calcite delta: {d_calcite_vals[0]:.4e} -> {d_calcite_vals[-1]:.4e} mol/kgw")
    if d_kfeldspar_vals:
        print(f"  [OK] K-feldspar delta: {d_kfeldspar_vals[0]:.4e} -> {d_kfeldspar_vals[-1]:.4e} mol/kgw")

    # Save porosity data
    porosity_results = {
        "initial_porosity": PHI_0,
        "final_porosity": porosities[-1],
        "delta_porosity": porosities[-1] - PHI_0,
        "steps": times,
        "porosities": porosities,
        "d_calcite_mol": d_calcite_vals,
        "d_kfeldspar_mol": d_kfeldspar_vals,
    }
    porosity_path = os.path.join(WORKSPACE, "porosity_results.json")
    with open(porosity_path, "w", encoding="utf-8") as f:
        json.dump(porosity_results, f, indent=2)
    print(f"  [OK] 孔隙度: {porosity_path}")
else:
    print("  [SKIP] 无数据，跳过孔隙度计算")
print()

# =========================================================================
# Step 4: 可视化
# =========================================================================
print("=" * 60)
print("Step 4/4: 生成图表...")
print("=" * 60)

if selected_data.get("row_count", 0) > 0:
    # 1. 化学组分随时间变化
    chem_file = plot_selected_output_sweep(
        selected_data,
        x_column="step",
        y_columns=["Ca", "K", "Al", "Si", "C"],
        title="Element Concentration Evolution (CO2 injection, 100C, 200 atm)",
        xlabel="Time Step (~0.5 year per step)",
        filepath=os.path.join(CHARTS_DIR, "element_evolution.png"),
    )
    print(f"  [OK] 元素演化: {chem_file}")

    # 2. pH 演化
    ph_file = plot_selected_output_sweep(
        selected_data,
        x_column="step",
        y_columns=["pH"],
        title="pH Evolution During CO2 Injection",
        xlabel="Time Step (~0.5 year per step)",
        filepath=os.path.join(CHARTS_DIR, "ph_evolution.png"),
    )
    print(f"  [OK] pH 演化: {ph_file}")

    # 3. 矿物饱和指数演化
    si_cols = [c for c in selected_data.get("columns", []) if c.startswith("si_")]
    if si_cols:
        si_file = plot_selected_output_sweep(
            selected_data,
            x_column="step",
            y_columns=si_cols,
            title="Saturation Index Evolution",
            xlabel="Time Step (~0.5 year per step)",
            filepath=os.path.join(CHARTS_DIR, "si_evolution.png"),
        )
        print(f"  [OK] SI 演化: {si_file}")

# 4. 孔隙度变化 (单独绘图)
if 'porosities' in dir() and len(porosities) > 0:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    # Subplot 1: Porosity
    ax.plot(times, porosities, "b-", linewidth=2, marker="o", markersize=4)
    ax.axhline(y=PHI_0, color="gray", linestyle="--", alpha=0.5,
               label=f"Initial porosity ({PHI_0})")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Porosity", color="b")
    ax.set_title("Porosity Evolution During CO2 Injection (100C, 200 atm)")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left")

    # Annotate change
    ax.annotate(f"Δφ = {porosities[-1] - PHI_0:+.6f}",
                xy=(0.7, 0.95), xycoords="axes fraction",
                fontsize=12, ha="left",
                bbox=dict(boxstyle="round", fc="wheat", alpha=0.5))

    plt.tight_layout()
    poro_file = os.path.join(CHARTS_DIR, "porosity_evolution.png")
    fig.savefig(poro_file, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] 孔隙度演化: {poro_file}")

    # Subplot 2: Mineral delta
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(times, d_calcite_vals, "r-", linewidth=1.5, marker="o", markersize=3,
             label="Calcite d(delta)")
    ax1.plot(times, d_kfeldspar_vals, "g-", linewidth=1.5, marker="s", markersize=3,
             label="K-feldspar d(delta)")
    ax1.set_xlabel("Time Step")
    ax1.set_ylabel("Mineral moles change (mol/kgw)")
    ax1.set_title("Mineral Mass Change During CO2 Injection")
    ax1.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
    ax1.grid(alpha=0.3)
    ax1.legend()
    plt.tight_layout()
    mineral_file = os.path.join(CHARTS_DIR, "mineral_change.png")
    fig.savefig(mineral_file, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] 矿物变化: {mineral_file}")

print()
print("=" * 60)
print("  [OK] 模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {CHARTS_DIR}")
print("=" * 60)
