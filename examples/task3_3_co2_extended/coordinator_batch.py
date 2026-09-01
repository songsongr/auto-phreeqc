"""
考题 3.3 扩展版: 批反应 + K-feldspar/Kaolinite 耦合动力学
========================================================
相比原版的变化:
  - 新增 Kaolinite 沉淀 RATES (消耗 Al+Si)
  - K-feldspar 因产物移除可持续溶解 (打破 SI≈0 瓶颈)
  - 孔隙度变化显著放大 (108.87 vs 99.52 cm3/mol)

工作流: 生成输入 -> 运行 PHREEQC -> 解析输出 -> 可视化
"""
import sys, os, json

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
    extract_element_molalities,
    extract_ionic_strength,
    to_json,
)
from visualize import plot_selected_output_sweep

print("=" * 60)
print("Step 1/4: 生成 PHREEQC 输入文件 (K-feldspar + Kaolinite)...")
print("=" * 60)

TEN_YEARS_S = int(10 * 365.25 * 86400)  # 315,576,000 seconds
N_STEPS = 20

# 摩尔体积 (cm3/mol)
MOLAR_VOL = {"Calcite": 36.93, "K-feldspar": 108.87, "Kaolinite": 99.52}

params = {
    "solution": {
        "id": 1, "units": "mol/kgw", "temp": 100.0,
        "pH": 7.5, "pe": -4.0, "density": 1.0,
        "components": {
            "Ca": 0.010, "C(4)": 0.010,
            "Na": 0.043, "Cl": 0.028,
            "K": 0.0001, "Si": 0.0001,
        },
    },
    "gas_phase": {
        "block_id": 1, "fixed_pressure": True,
        "pressure": 200.0, "components": {"CO2(g)": 0.0},
    },
    "equilibrium_phases": {"Calcite": (0.0, 10.0)},
    "eq_block_id": 1,
    # 两个动力学矿物: K-feldspar 溶解 + Kaolinite 沉淀
    "kinetics": {
        "reactants": [
            {
                "name": "K-feldspar",
                "formula": "KAlSi3O8",
                "m": 3.0, "m0": 3.0,
                "parms": [0.2],  # m2/g
                "steps": [TEN_YEARS_S],
                "steps_n": N_STEPS,
                "cvode": True,
            },
            {
                "name": "Kaolinite",
                "formula": "Al2Si2O5(OH)4",
                "m": 0.5, "m0": 0.5,
                "parms": [10.0],  # m2/g (high surface area clay)
                "steps": [TEN_YEARS_S],
                "steps_n": N_STEPS,
                "cvode": True,
            },
        ],
    },
    "kinetics_block_id": 1,
    # RATES: K-feldspar 溶解 + Kaolinite 沉淀
    "rates": [
        {
            "name": "K-feldspar",
            "code": [
                "rem Palandri & Kharaka (2004): k_neut + k_acid * aH+^0.5",
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
                "rem SR() must be inline (BASIC parser quirk)",
                "rate_kf = (k_neut + k_acid) * area * (1 - SR(\"K-feldspar\"))",
                "if rate_kf < 0 then rate_kf = 0",
                "moles_kf = rate_kf * TIME",
                "if moles_kf > M then moles_kf = M",
                "SAVE moles_kf",
            ],
        },
        {
            "name": "Kaolinite",
            "code": [
                "rem Kaolinite precipitation (Carroll & Walther 1990)",
                "rem log_k = -13.18 (25C), Ea = 66.2 kJ/mol",
                "T = 298.15 + TC",
                "T0 = 298.15",
                "R = 8.314",
                "k_25 = 10^(-13.18)",
                "Ea = 66200",
                "f_temp = exp(Ea / R * (1/T0 - 1/T))",
                "k_kao = k_25 * f_temp",
                "gfm = 258.16",
                "sa_m2_per_g = parm(1)",
                "area = M * gfm * sa_m2_per_g",
                "sr_kao = SR(\"Kaolinite\")",
                "rem Precipitation when SI > 0 (SR > 1)",
                "rate_kao = k_kao * area * (1 - sr_kao)",
                "rem Negative rate = precipitation (SAVE negative)",
                "moles_kao = rate_kao * TIME",
                "if moles_kao > M then moles_kao = M",
                "rem Limit precipitation: don't exceed half current moles",
                "if moles_kao < -M * 0.5 then moles_kao = -M * 0.5",
                "SAVE moles_kao",
            ],
        },
    ],
    "selected_output": {
        "step": True,
        "totals": ["Ca", "K", "Al", "Si", "C"],
        "si": ["Calcite", "K-feldspar", "Kaolinite", "Quartz", "Gibbsite"],
        "equilibrium_phases": ["Calcite"],
        "pH": True, "pe": True, "temperature": True,
    },
}

content = "TITLE CO2 injection + K-feldspar/Kaolinite coupled kinetics (100C, 200 atm)\n\n"
content += generate_single_simulation(params, output_file="selected_output.txt")
input_path = write_input_file(content, os.path.join(WORKSPACE, "input_batch.pqi"))
print(f"  [OK] 输入文件: {input_path}")
print()

# =========================================================================
# Step 2: 运行 PHREEQC
# =========================================================================
print("=" * 60)
print("Step 2/4: 运行 PHREEQC (20 steps, 10 years, dual RATES)...")
print("=" * 60)

db_path = find_database("phreeqc.dat")
result = run_simulation(
    input_file=input_path,
    output_file=os.path.join(WORKSPACE, "output_batch.qpo"),
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

with open(os.path.join(WORKSPACE, "output_batch.qpo"), "r", encoding="utf-8", errors="replace") as f:
    output_text = f.read()

si_data = extract_saturation_indices(output_text, last=True)
element_data = extract_element_molalities(output_text, last=True)
is_val = extract_ionic_strength(output_text)
print(f"  [OK] 饱和指数 (最终):")
for s in si_data:
    if s["phase"] in ("Calcite", "K-feldspar", "Kaolinite", "Quartz", "Gibbsite"):
        print(f"    {s['phase']}: SI = {s['si']:.3f}")
print(f"  [OK] 元素浓度 (最终): {len(element_data)} 个元素")

selected_file = os.path.join(WORKSPACE, "selected_output.txt")
selected_data = {}
if os.path.isfile(selected_file):
    selected_data = parse_selected_output(selected_file)
    n_rows = selected_data.get("row_count", 0)
    print(f"  [OK] Selected output: {n_rows} 行")
    if n_rows > 0:
        cols = selected_data.get("columns", [])
        data = selected_data.get("data", [])
        print(f"    首行: {data[0]}")
        print(f"    末行: {data[-1]}")

# 提取 K-feldspar + Kaolinite 动力学数据
kf_deltas, kao_deltas = [], []
for line in output_text.splitlines():
    parts = line.split()
    if len(parts) >= 4:
        try:
            delta = float(parts[1])
            cur = float(parts[2])
            name = parts[0].strip()
            if "K-feldspar" in name and -1 < delta < 1 and 0 < cur < 100:
                kf_deltas.append(delta)
            elif "Kaolinite" in name and -1 < delta < 1 and 0 < cur < 100:
                kao_deltas.append(delta)
        except (ValueError, IndexError):
            pass

kf_d_total = sum(kf_deltas) if kf_deltas else 0
kao_d_total = sum(kao_deltas) if kao_deltas else 0
print(f"\n  [OK] K-feldspar total delta: {kf_d_total:.4e} mol/kgw (over {len(kf_deltas)} steps)")
print(f"  [OK] Kaolinite total delta: {kao_d_total:.4e} mol/kgw")

# 孔隙度估算
PHI_0 = 0.20
V_bulk = 1.0 / PHI_0 * 1000
dv_total = (kf_d_total * MOLAR_VOL["K-feldspar"] +
            kao_d_total * MOLAR_VOL["Kaolinite"])
phi_final = PHI_0 - dv_total / V_bulk
print(f"\n  [OK] 初始孔隙度: {PHI_0:.4f}")
print(f"  [OK] 孔隙度变化: {phi_final - PHI_0:+.6f}")
print(f"  [OK] 最终孔隙度: {phi_final:.6f}")
print(f"  [OK] 变化率: {(phi_final/PHI_0-1)*100:+.3f}%")

# 保存
json_output = to_json(selected_data, si_data, element_data, metadata={
    "ionic_strength_mol_kgw": is_val,
    "temperature_C": 100.0, "pressure_atm": 200.0,
    "duration_years": 10.0, "n_steps": N_STEPS,
    "phi_0": PHI_0, "phi_final": phi_final,
    "kf_delta_total": kf_d_total, "kao_delta_total": kao_d_total,
})
json_path = os.path.join(WORKSPACE, "results_batch.json")
with open(json_path, "w", encoding="utf-8") as f:
    f.write(json_output)
print(f"  [OK] JSON: {json_path}")
print()

# =========================================================================
# Step 4: 可视化
# =========================================================================
print("=" * 60)
print("Step 4/4: 生成图表...")
print("=" * 60)

if selected_data.get("row_count", 0) > 0:
    # 元素演化
    plot_selected_output_sweep(
        selected_data, x_column="step",
        y_columns=["Ca", "K", "Al", "Si", "C"],
        title="Element Evolution (K-feldspar + Kaolinite)",
        xlabel="Time Step (~0.5 yr)",
        filepath=os.path.join(CHARTS_DIR, "element_evolution.png"),
    )
    print("  [OK] 元素演化")

    # pH + pe
    for col in ["pH", "pe"]:
        if col in selected_data.get("columns", []):
            plot_selected_output_sweep(
                selected_data, x_column="step",
                y_columns=[col],
                title=f"{col.upper()} Evolution",
                xlabel="Time Step (~0.5 yr)",
                filepath=os.path.join(CHARTS_DIR, f"{col}_evolution.png"),
            )
    print("  [OK] pH/pe 演化")

    # SI
    si_cols = [c for c in selected_data.get("columns", [])
               if c.startswith("si_") and c[3:] in ("Calcite", "K-feldspar", "Kaolinite", "Quartz", "Gibbsite")]
    if si_cols:
        plot_selected_output_sweep(
            selected_data, x_column="step", y_columns=si_cols,
            title="SI Evolution (key minerals)",
            xlabel="Time Step (~0.5 yr)",
            filepath=os.path.join(CHARTS_DIR, "si_evolution.png"),
        )
        print("  [OK] SI 演化")

    # Porosity evolution by steps
    d_cal_idx = None
    for i, c in enumerate(selected_data.get("columns", [])):
        if c == "d_Calcite":
            d_cal_idx = i
            break

    if d_cal_idx is not None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        data = selected_data["data"]
        steps = [r[selected_data["columns"].index("step")] for r in data if r[1] != "i_soln"]
        step_data = [r for r in data if r[1] != "i_soln"]

        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()

        n_steps = len(step_data)
        cum_kf = [kf_d_total * (i + 1) / n_steps for i in range(n_steps)]
        cum_kao = [kao_d_total * (i + 1) / n_steps for i in range(n_steps)]

        porosities = []
        cal_dv_values = []
        kf_dv_values = []
        kao_dv_values = []

        for i in range(n_steps):
            d_cal = float(step_data[i][d_cal_idx]) if d_cal_idx is not None else 0
            cal_dv = d_cal * MOLAR_VOL["Calcite"]
            kf_dv = cum_kf[i] * MOLAR_VOL["K-feldspar"]
            kao_dv = cum_kao[i] * MOLAR_VOL["Kaolinite"]
            dv = cal_dv + kf_dv + kao_dv
            phi = PHI_0 - dv / V_bulk
            porosities.append(phi)
            cal_dv_values.append(cal_dv)
            kf_dv_values.append(kf_dv)
            kao_dv_values.append(kao_dv)

        ax1.plot(range(1, n_steps + 1), porosities, "b-", linewidth=2, marker="o", markersize=4)
        ax1.axhline(PHI_0, color="gray", linestyle="--", alpha=0.5, label=f"Initial φ₀={PHI_0}")
        ax1.set_xlabel("Time Step (~0.5 yr)")
        ax1.set_ylabel("Porosity", color="b")
        ax1.tick_params(axis="y", labelcolor="b")

        colors = ["#d62728", "#2ca02c", "#ff7f0e"]
        labels = ["Calcite", "K-feldspar", "Kaolinite"]
        dvs = [cal_dv_values, kf_dv_values, kao_dv_values]
        ax2.stackplot(range(1, n_steps + 1), *dvs, colors=colors, labels=labels, alpha=0.6)
        ax2.set_ylabel("Cumulative volume change (cm³)", color="gray")
        ax2.tick_params(axis="y", labelcolor="gray")

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left")

        ax1.set_title("Porosity Evolution with Coupled K-feldspar-Kaolinite Kinetics")
        ax1.grid(alpha=0.3)
        plt.tight_layout()
        poro_file = os.path.join(CHARTS_DIR, "porosity_evolution.png")
        fig.savefig(poro_file, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  [OK] 孔隙度演化 (含 stackplot): {poro_file}")

print()
print("=" * 60)
print("  [OK] 拓展批反应模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {CHARTS_DIR}")
print("=" * 60)
