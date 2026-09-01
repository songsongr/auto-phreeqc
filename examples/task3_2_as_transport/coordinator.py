"""
PHREEQC 考题 3.2: 一维反应溶质运移 (As 穿透曲线)
================================================
设定: 1m 长的沉积物柱，初始充满去离子水
      以 1m/d 的速度流过含 1ppm As(V) 的溶液
      计算 5 天后砷在柱体出口的穿透曲线

方法: 非保守示踪 (As(V) 定义为主物种，作为保守示踪剂)
      因为 phreeqc.dat 无 As 主物种，手动定义 As 的
      SOLUTION_MASTER_SPECIES / SOLUTION_SPECIES。

工作流: 生成输入 -> 运行 PHREEQC -> 解析输出 -> 可视化
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
    extract_element_molalities,
    extract_ionic_strength,
    to_json,
)
from visualize import plot_breakthrough_curve

# =========================================================================
# Step 1: 构建参数 & 生成输入文件
# =========================================================================
print("=" * 60)
print("Step 1/4: 生成 PHREEQC 输入文件...")
print("=" * 60)

# phreeqc.dat 不含 As, 需手动定义
# 保守示踪: AsO4-3 作为主物种 (不进行络合反应)
as_species_block = """# --- Custom As master species (conservative tracer) ---
SOLUTION_MASTER_SPECIES
    As    AsO4-3    0.0    As    74.9216

SOLUTION_SPECIES
    AsO4-3 = AsO4-3
    log_k    0.0
"""

params = {
    # SOLUTION 0 = 入口边界条件 (含 As 的注入溶液)
    "solutions": [
        {
            "id": 0, "units": "ppm", "temp": 25.0,
            "pH": 7.0, "pe": 12.0, "density": 1.0,
            "components": {
                "As": 1.0,     # 1 ppm As(V) 保守示踪剂
                "Na": 10.0,    # 背景电解质 NaCl (~0.4 mM)
                "Cl": 15.0,
            },
        },
    ],
    # 柱体初始孔隙溶液 (SOLUTION 1..20 自动生成)
    "initial_cell_solution": {
        "units": "mol/kgw", "temp": 25.0,
        "pH": 7.0, "pe": 12.0, "density": 1.0,
    },
    # 传输参数
    "transport": {
        "cells": 20,
        "length": 1.0,
        "shifts": 100,
        "time_step": 0.05,
        "time_units": "day",
        "flow_direction": "forward",
        "dispersivity": 0.01,
        "correct_disp": True,
        "punch_cells": [20],    # 出口单元突破曲线
        "punch_frequency": 1,    # 每步输出
        "print_cells": [1, 10, 20],
        "print_frequency": 25,   # 每 25 步打印柱体剖面
    },
    "selected_output": {
        "step": True,
        "totals": ["As", "Na", "Cl"],
        "pH": True,
        "pe": True,
    },
}

content = generate_single_simulation(params, output_file="selected_output.txt")
# 在生成的内容前插入 As 定义块
content = as_species_block + "\n\n" + content

input_path = write_input_file(content, os.path.join(WORKSPACE, "input.pqi"))
print(f"  [OK] 输入文件: {input_path}")
print()

# =========================================================================
# Step 2: 运行 PHREEQC
# =========================================================================
print("=" * 60)
print("Step 2/4: 运行 PHREEQC (100 shifts, 5 days)...")
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

si_data = extract_saturation_indices(output_text)
element_data = extract_element_molalities(output_text)
is_val = extract_ionic_strength(output_text)
print(f"  [OK] 饱和指数: {len(si_data)} 个矿物")
print(f"  [OK] 元素浓度: {len(element_data)} 个元素")
if is_val is not None:
    print(f"  [OK] 离子强度: {is_val}")
else:
    print("  [WARN] 未找到离子强度")

selected_file = os.path.join(WORKSPACE, "selected_output.txt")
selected_data = {}
if os.path.isfile(selected_file):
    selected_data = parse_selected_output(selected_file)
    n_rows = selected_data.get("row_count", 0)
    print(f"  [OK] Selected output: {n_rows} 行 (突破曲线数据点)")
    if n_rows > 0:
        cols = selected_data.get("columns", [])
        print(f"  [OK] 列: {cols}")
        data = selected_data.get("data", [])
        # 只取 transport step 数据 (state='transp') 用于绘图
        transp_rows = [r for r in data if len(r) > 1 and r[1] == 'transp']
        print(f"  [OK] Transport step 行数: {len(transp_rows)}")
        if transp_rows:
            print(f"    首 (time={transp_rows[0][4]}) As={transp_rows[0][15]}")
            print(f"    末 (time={transp_rows[-1][4]}) As={transp_rows[-1][15]}")
            print(f"    Na 首={transp_rows[0][16]} 末={transp_rows[-1][16]}")
            print(f"    Cl 首={transp_rows[0][17]} 末={transp_rows[-1][17]}")
        # 检查 inlet 溶液 As 浓度
        i_soln_rows = [r for r in data if len(r) > 1 and r[1] == 'i_soln' and r[2] == 0.0]
        if i_soln_rows:
            print(f"  [INFO] Inlet As (soln=0) = {i_soln_rows[0][15]}")
else:
    print(f"  [WARN] SELECTED_OUTPUT 文件未找到: {selected_file}")

# 保存 JSON
json_output = to_json(selected_data, si_data, element_data, metadata={
    "ionic_strength_mol_kgw": is_val,
    "transport_params": {
        "cells": 20, "length_m": 1.0, "shifts": 100,
        "time_step_day": 0.05, "velocity_m_per_d": 1.0,
        "dispersivity_m": 0.01,
    },
})
json_path = os.path.join(WORKSPACE, "results.json")
with open(json_path, "w", encoding="utf-8") as f:
    f.write(json_output)
print(f"  [OK] JSON: {json_path}")
print()

# =========================================================================
# Step 4: 可视化 — 突破曲线
# =========================================================================
print("=" * 60)
print("Step 4/4: 生成图表...")
print("=" * 60)

if selected_data.get("row_count", 0) > 0:
    bt_file = plot_breakthrough_curve(
        selected_data,
        time_column="step",
        conc_column="As",
        title="As Breakthrough Curve (1m column, 1m/d)",
        xlabel="Time Step (0.05 day each)",
        ylabel="Total As (mol/kgw)",
        filepath=os.path.join(CHARTS_DIR, "as_breakthrough.png"),
    )
    print(f"  [OK] As 穿透曲线: {bt_file}")

    bt_cl = plot_breakthrough_curve(
        selected_data,
        time_column="step",
        conc_column="Cl",
        title="Cl- Breakthrough Curve (conservative tracer)",
        xlabel="Time Step (0.05 day each)",
        ylabel="Total Cl (mol/kgw)",
        filepath=os.path.join(CHARTS_DIR, "cl_breakthrough.png"),
    )
    print(f"  [OK] Cl 穿透曲线: {bt_cl}")

    bt_both = plot_breakthrough_curve(
        selected_data,
        time_column="step",
        conc_columns=["As", "Cl"],
        title="As and Cl Breakthrough Curves",
        xlabel="Time Step (0.05 day each)",
        ylabel="Concentration (mol/kgw)",
        filepath=os.path.join(CHARTS_DIR, "both_breakthrough.png"),
    )
    print(f"  [OK] As+Cl 对比: {bt_both}")
else:
    print("  [SKIP] 无 SELECTED_OUTPUT 数据，跳过绘图")

print()
print("=" * 60)
print("  [OK] 模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {CHARTS_DIR}")
print("=" * 60)
