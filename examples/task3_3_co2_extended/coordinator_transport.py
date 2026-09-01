"""
考题 3.3 扩展: 1D TRANSPORT + K-feldspar/Kaolinite 反应性运移
=============================================================
设定: CO2 酸性水注入含钙砂岩柱 (10 cells, 1m)
      K-feldspar 溶解 + Kaolinite 沉淀 + Calcite 平衡
      模拟空间矿物分带和孔隙度梯度

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
    to_json,
)
from visualize import plot_breakthrough_curve, plot_selected_output_sweep

print("=" * 60)
print("Step 1/4: 生成 TRANSPORT + KINETICS 输入文件...")
print("=" * 60)

# 10 years total
TEN_YEARS_S = int(10 * 365.25 * 86400)

# TRANSPORT 参数: 10 cells, 1m, slow Darcy velocity (0.1 m/yr)
# 10 years × 0.1 m/yr = 1m → water displaces 1 full column in simulation time
# Courant = v * dt / dx = (0.1 m/yr * yr/365.25 d) * dt / 0.1m
# Let's use Courant ≈ 0.5 for stability
# dt = Courant * dx / v = 0.5 * 0.1 / (0.1/365.25) = 182.6 days
# 10 years / 182.6 days = 20 shifts

N_CELLS = 10
COLUMN_LENGTH = 1.0
VELOCITY_M_PER_YR = 0.1  # slow deep groundwater
DT_DAYS = 182.625         # 0.5 year
N_SHIFTS = 20             # 20 × 0.5 yr = 10 years

MOLAR_VOL = {"Calcite": 36.93, "K-feldspar": 108.87, "Kaolinite": 99.52}

params = {
    # SOLUTION 0 = CO2 酸性入口水 (proxy for CO2-saturated water)
    "solutions": [
        {
            "id": 0, "units": "mol/kgw", "temp": 100.0,
            "pH": 4.0, "pe": -4.0, "density": 1.0,
            "components": {
                "C(4)": 0.50,     # high DIC from CO2 dissolution
                "Na": 0.043,      # background NaCl
                "Cl": 0.028,
            },
        },
    ],
    # 柱体初始溶液 (砂岩孔隙水, 同批反应)
    "initial_cell_solution": {
        "units": "mol/kgw", "temp": 100.0,
        "pH": 7.5, "pe": -4.0, "density": 1.0,
        "components": {
            "Ca": 0.010, "C(4)": 0.010,
            "Na": 0.043, "Cl": 0.028,
            "K": 0.0001, "Si": 0.0001,
        },
    },
    # 传输参数: 1m 柱, 慢速地下水流
    "transport": {
        "cells": N_CELLS,
        "length": COLUMN_LENGTH,
        "shifts": N_SHIFTS,
        "time_step": DT_DAYS,
        "time_units": "day",
        "flow_direction": "forward",
        "dispersivity": 0.02,
        "correct_disp": True,
        "punch_cells": [1, 5, 10],  # 入口/中段/出口
        "punch_frequency": 1,
        "print_cells": [1, 5, 10],
        "print_frequency": 5,
    },
    # Calcite 快速平衡 (每个 cell)
    "equilibrium_phases": {
        "Calcite": (0.0, 10.0),
    },
    "eq_block_id": 1,
    # 动力学矿物
    "kinetics": {
        "reactants": [
            {
                "name": "K-feldspar",
                "formula": "KAlSi3O8",
                "m": 3.0, "m0": 3.0,
                "parms": [0.2],
                "step_divide": 10,
                "cvode": True,
            },
            {
                "name": "Kaolinite",
                "formula": "Al2Si2O5(OH)4",
                "m": 0.5, "m0": 0.5,
                "parms": [10.0],
                "step_divide": 10,
                "cvode": True,
            },
        ],
    },
    "kinetics_block_id": 1,
    # 在 TRANSPORT 模式下, KINETICS 自动使用 transport time step 作为积分时间
    # 不需要显式 -steps; 用 -step_divide 控制子步数
    # RATES 块
    "rates": [
        {
            "name": "K-feldspar",
            "code": [
                "rem Palandri & Kharaka (2004)",
                "T = 298.15 + TC",
                "T0 = 298.15", "R = 8.314",
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
                "area = M * gfm * parm(1)",
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
                "T = 298.15 + TC",
                "T0 = 298.15", "R = 8.314",
                "k_25 = 10^(-13.18)",
                "Ea = 66200",
                "f_temp = exp(Ea / R * (1/T0 - 1/T))",
                "k_kao = k_25 * f_temp",
                "gfm = 258.16",
                "area = M * gfm * parm(1)",
                "sr_kao = SR(\"Kaolinite\")",
                "rate_kao = k_kao * area * (1 - sr_kao)",
                "moles_kao = rate_kao * TIME",
                "if moles_kao > M then moles_kao = M",
                "if moles_kao < -M * 0.5 then moles_kao = -M * 0.5",
                "SAVE moles_kao",
            ],
        },
    ],
    "selected_output": {
        "step": True,
        "totals": ["Ca", "K", "Al", "Si", "C"],
        "si": ["Calcite", "K-feldspar", "Kaolinite", "Quartz"],
        "equilibrium_phases": ["Calcite"],
        "pH": True, "temperature": True,
    },
}

content = "TITLE CO2 TRANSPORT + K-feldspar/Kaolinite (100C, 10 cells)\n\n"
content += generate_single_simulation(params, output_file="selected_transport.txt")
input_path = write_input_file(content, os.path.join(WORKSPACE, "input_transport.pqi"))
print(f"  [OK] 输入文件: {input_path}")
print()

# =========================================================================
# Step 2: 运行 PHREEQC
# =========================================================================
print("=" * 60)
print("Step 2/4: 运行 PHREEQC TRANSPORT (10 cells x 20 shifts)...")
print("=" * 60)

db_path = find_database("phreeqc.dat")
result = run_simulation(
    input_file=input_path,
    output_file=os.path.join(WORKSPACE, "output_transport.qpo"),
    database=db_path,
    timeout=600,
    cwd=WORKSPACE,
)

if not result["success"]:
    print(f"  [FAIL]  TRANSPORT 模拟失败: {result['error']}")
    sys.exit(1)
print(f"  [OK] TRANSPORT 模拟成功 (exit code: {result['exit_code']})")
print()

# =========================================================================
# Step 3: 解析输出
# =========================================================================
print("=" * 60)
print("Step 3/4: 解析输出...")
print("=" * 60)

with open(os.path.join(WORKSPACE, "output_transport.qpo"), "r", encoding="utf-8", errors="replace") as f:
    output_text = f.read()

si_data = extract_saturation_indices(output_text, last=True)
element_data = extract_element_molalities(output_text, last=True)
print(f"  [OK] 饱和指数 (最终, 末单元):")
for s in si_data:
    if s["phase"] in ("Calcite", "K-feldspar", "Kaolinite", "Quartz"):
        print(f"    {s['phase']}: SI = {s['si']:.3f}")
print(f"  [OK] 元素浓度 (最终): {len(element_data)} 个元素")

# SELECTED_OUTPUT 包含各 punch_cell 的突破数据
selected_file = os.path.join(WORKSPACE, "selected_transport.txt")
selected_data = {}
if os.path.isfile(selected_file):
    selected_data = parse_selected_output(selected_file)
    n_rows = selected_data.get("row_count", 0)
    print(f"  [OK] Selected output: {n_rows} 行")
    if n_rows > 0:
        cols = selected_data.get("columns", [])
        data = selected_data.get("data", [])
        print(f"  [OK] 列: {cols}")
        transp = [r for r in data if len(r) > 1 and r[1] == 'transp']
        print(f"  [OK] Transport 步数: {len(transp)}")
        if transp:
            print(f"    首: cell={transp[0][2]}, step={transp[0][5]}, pH={transp[0][6]}")
            print(f"    末: cell={transp[-1][2]}, step={transp[-1][5]}, pH={transp[-1][6]}")

# 提取 K-feldspar/Kaolinite 动力学数据 (仅 KINETICS 格式的行)
# KINETICS 行: "name  delta_moles  current_moles  formula  stoichiometry"
# 鉴别特征: current_moles 与初始量接近 (0.1-10), delta 量级小 (< 1)
# 排除: 平衡相输出行 (log_K >> 10 或 current 离初值太远)
kf_init_val = kf_final_val = None
kao_init_val = kao_final_val = None
kao_target_range = (0.3, 3.0)  # Kaolinite 初始 0.5 mol, 合理范围

transport_start = output_text.find("Beginning of transport calculations")

for line in output_text.splitlines():
    parts = line.split()
    if len(parts) < 3:
        continue
    try:
        d = float(parts[1])
        c = float(parts[2])
    except (ValueError, IndexError):
        continue

    # K-feldspar: 初始 3 mol, current 在 1-4 间
    if "K-feldspar" in parts[0] and -1 < d < 1 and 1 < c < 4:
        if transport_start > 0 and output_text.find(line) < transport_start:
            kf_init_val = c
        elif transport_start > 0:
            kf_final_val = c  # last occurrence = final state

    # Kaolinite: 仅 KINETICS 行 (最后字段为化学计量系数 1, 非配方名)
    # KINETICS: [name, delta, current, formula, coeff] → parts[-1] 是数字
    # Equilibrium: [name, si, logIAP, logK, formula] → parts[-1] 是配方
    is_kao_kinetics = False
    if "Kaolinite" in parts[0] and len(parts) >= 5:
        try:
            float(parts[-1])  # 最后字段是数字 → KINETICS 行
            is_kao_kinetics = True
        except ValueError:
            pass  # 最后字段非数字 → 平衡相行, 跳过

    if is_kao_kinetics and -1 < d < 1 and 0 < c < 3:
        if transport_start > 0 and output_text.find(line) < transport_start:
            kao_init_val = c
        elif transport_start > 0:
            kao_final_val = c

print(f"\n  [OK] K-feldspar: init ~{kf_init_val:.2f}, final ~{kf_final_val:.2f}")
if kf_init_val and kf_final_val:
    print(f"  [OK] K-feldspar dissolved: {kf_init_val - kf_final_val:.4e} mol/kgw")
print(f"  [OK] Kaolinite: init ~{kao_init_val:.2f}, final ~{kao_final_val:.2f}")

# 最终孔隙度估算
kf_total_delta = (kf_final_val - kf_init_val) if (kf_init_val and kf_final_val) else 0
kao_total_delta = (kao_final_val - kao_init_val) if (kao_init_val and kao_final_val) else 0
PHI_0 = 0.20
V_bulk = 1.0 / PHI_0 * 1000
dv = (kf_total_delta * MOLAR_VOL["K-feldspar"] +
      kao_total_delta * MOLAR_VOL["Kaolinite"])
phi_final = PHI_0 - dv / V_bulk
print(f"\n  [OK] 孔隙度变化(末cell): {phi_final - PHI_0:+.6f} "
      f"({(phi_final/PHI_0 - 1)*100:+.3f}%)")

json_output = to_json(selected_data, si_data, element_data, metadata={
    "temperature_C": 100.0,
    "n_cells": N_CELLS, "n_shifts": N_SHIFTS, "duration_years": 10,
    "kf_delta": float(kf_total_delta), "kao_delta": float(kao_total_delta),
    "phi_0": PHI_0, "phi_final": float(phi_final),
})
json_path = os.path.join(WORKSPACE, "results_transport.json")
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
    # 各出口单元突破曲线
    for col in ["Ca", "K", "Al", "Si", "pH"]:
        if col in selected_data.get("columns", []):
            plot_breakthrough_curve(
                selected_data, time_column="step",
                conc_column=col,
                title=f"{col} at Outlet Cells (CO2 TRANSPORT)",
                xlabel="Time Step (~0.5 yr)",
                filepath=os.path.join(CHARTS_DIR, f"bt_{col}.png"),
            )
    print(f"  [OK] 各元素突破曲线")

    # SI 演化 (只取末 cell)
    si_cols = [c for c in selected_data.get("columns", [])
               if c.startswith("si_")]
    if si_cols:
        plot_selected_output_sweep(
            selected_data, x_column="step", y_columns=si_cols,
            title="SI Evolution (outlet cell)",
            xlabel="Time Step (~0.5 yr)",
            filepath=os.path.join(CHARTS_DIR, "si_transport.png"),
        )
        print(f"  [OK] SI 演化 (TRANSPORT)")

print()
print("=" * 60)
print("  [OK] TRANSPORT 模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {CHARTS_DIR}")
print("=" * 60)
