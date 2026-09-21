"""
考题 1.3 -- 海水 + 纯水混合模拟
================================
Input: 将 500mL 的海水（标准组分）与 500mL 的纯水混合，
       计算混合后的离子强度和 pH 变化。

考察重点: 基准溶液的预设、混合比例控制（MIX）、潜在沉淀排查

步骤:
  1. 单独运行海水 speciation（获取参考 pH、离子强度）
  2. 运行海水 + 纯水 MIX 模拟（获取混合后 pH、离子强度）
  3. 对比并检查潜在沉淀
"""

import json
import os
import sys
from pathlib import Path

# ---- 环境设置 ----
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

WORKSPACE = Path(__file__).resolve().parent
CHARTS_DIR = WORKSPACE / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

from phreeqc_auto.generate_input import generate_single_simulation, write_input_file
from phreeqc_auto.run_phreeqc import run_simulation, find_database
from phreeqc_auto.parse_output import (
    parse_selected_output,
    extract_saturation_indices,
    extract_species_distribution,
    extract_element_molalities,
    extract_ionic_strength,
    to_json,
)
from phreeqc_auto.visualize import plot_multi_panel, plot_saturation_indices


# ---- 海水组分 (基于 ex1, 不含 U) ----
SEAWATER_COMPONENTS = {
    "Ca": 412.3,
    "Mg": 1291.8,
    "Na": 10768.0,
    "K": 399.1,
    "Cl": 19353.0,
    "Alkalinity": 141.682,
    "S(6)": 2712.0,
}

# 关注矿物（海水混合可能产生的沉淀）
SI_PHASES = ["Calcite", "Dolomite", "Aragonite", "Gypsum", "Halite", "Brucite"]
TOTAL_ELEMENTS = ["Ca", "Mg", "Na", "K", "Cl", "S", "C"]


# =========================================================================
# Simulation A: 海水单独 Speciation (参考)
# =========================================================================
print("=" * 60)
print("Sim A: 海水 Speciation (参考)")
print("=" * 60)

params_a = {
    "solution": {
        "id": 1,
        "units": "ppm",
        "temp": 25.0,
        "pH": 8.22,
        "pe": 8.451,
        "density": 1.023,
        "components": dict(SEAWATER_COMPONENTS),
    },
    "selected_output": {
        "si": SI_PHASES,
        "totals": TOTAL_ELEMENTS,
        "pH": True,
        "pe": True,
    },
}

content_a = generate_single_simulation(params_a, output_file="selected_output_a.txt")
input_path_a = write_input_file(content_a, os.path.join(WORKSPACE, "input_a.pqi"))
print(f"  [OK] 输入文件: {input_path_a}")

db_path = find_database("phreeqc.dat")
result_a = run_simulation(
    input_file=input_path_a,
    output_file=os.path.join(WORKSPACE, "output_a.qpo"),
    database=db_path,
    timeout=120,
    cwd=WORKSPACE,
)

if not result_a["success"]:
    print(f"  [FAIL] 模拟 A 失败: {result_a['error']}")
    sys.exit(1)
print(f"  [OK] 模拟 A 成功")

# 解析模拟 A 输出
with open(os.path.join(WORKSPACE, "output_a.qpo"), "r", encoding="utf-8", errors="replace") as f:
    otxt_a = f.read()

si_a = extract_saturation_indices(otxt_a)
species_a = extract_species_distribution(otxt_a)
elements_a = extract_element_molalities(otxt_a)
is_a = extract_ionic_strength(otxt_a)
print(f"  [OK] 离子强度: {is_a} mol/kgw" if is_a is not None else "  [WARN] 未找到离子强度")
print(f"  [OK] 饱和指数: {len(si_a)} 个矿物, 物种: {len(species_a)} 个")

selected_a = parse_selected_output(os.path.join(WORKSPACE, "selected_output_a.txt"))
# 单溶液模拟: 只有1行数据
pH_a = selected_a["data"][0][selected_a["columns"].index("pH")] if selected_a.get("data") else None
print(f"  [OK] pH: {pH_a}" if pH_a else "  [WARN] 未获取 pH")

print()


# =========================================================================
# Simulation B: 海水 + 纯水 MIX
# =========================================================================
print("=" * 60)
print("Sim B: 海水 (500mL) + 纯水 (500mL) 混合")
print("=" * 60)

params_b = {
    "solutions": [
        {
            "id": 1,
            "units": "ppm",
            "temp": 25.0,
            "pH": 8.22,
            "pe": 8.451,
            "density": 1.023,
            "components": dict(SEAWATER_COMPONENTS),
        },
        {
            "id": 2,
            "units": "mol/kgw",
            "temp": 25.0,
            "pH": 7.0,
            "pe": 4.0,
            "density": 1.0,
            "components": {},
        },
    ],
    "mix": {
        "id": 1,
        "solutions": {1: 0.5, 2: 0.5},
    },
    "selected_output": {
        "si": SI_PHASES,
        "totals": TOTAL_ELEMENTS,
        "pH": True,
        "pe": True,
    },
}

content_b = generate_single_simulation(params_b, output_file="selected_output_b.txt")
input_path_b = write_input_file(content_b, os.path.join(WORKSPACE, "input_b.pqi"))
print(f"  [OK] 输入文件: {input_path_b}")

# 检查生成内容
print()
print("  --- 生成输入文件预览 (前 15 行) ---")
with open(input_path_b, "r") as f:
    lines_b = f.readlines()
for line in lines_b[:15]:
    print(f"    {line}", end="")
if len(lines_b) > 15:
    print(f"    ... ({len(lines_b)} lines total)")
print()

result_b = run_simulation(
    input_file=input_path_b,
    output_file=os.path.join(WORKSPACE, "output_b.qpo"),
    database=db_path,
    timeout=120,
    cwd=WORKSPACE,
)

if not result_b["success"]:
    print(f"  [FAIL] 模拟 B 失败: {result_b['error']}")
    sys.exit(1)
print(f"  [OK] 模拟 B 成功")

# 解析模拟 B 输出
with open(os.path.join(WORKSPACE, "output_b.qpo"), "r", encoding="utf-8", errors="replace") as f:
    otxt_b = f.read()

si_b = extract_saturation_indices(otxt_b, last=True)
species_b = extract_species_distribution(otxt_b, last=True)
elements_b = extract_element_molalities(otxt_b, last=True)
is_b = extract_ionic_strength(otxt_b)
print(f"  [OK] 混合离子强度: {is_b} mol/kgw" if is_b is not None else "  [WARN] 未找到离子强度")

selected_b = parse_selected_output(os.path.join(WORKSPACE, "selected_output_b.txt"))
# MIX 模拟有3行数据: [海水, 纯水, 混合后]; 取最后一行(=最终反应态)
pH_b = selected_b["data"][-1][selected_b["columns"].index("pH")] if selected_b.get("data") else None
print(f"  [OK] 混合 pH: {pH_b}" if pH_b else "  [WARN] 未获取 pH")

print()


# =========================================================================
# 结果对比分析
# =========================================================================
print("=" * 60)
print("结果对比分析")
print("=" * 60)

print()
print(f"  {'参数':<25} {'海水(未混合)':<20} {'混合后':<20}")
print(f"  {'-'*25} {'-'*20} {'-'*20}")

pH_ref = pH_a if pH_a is not None else 0.0
if selected_b["data"] and len(selected_b["data"]) > 0:
    pH_mix = pH_b if pH_b is not None else 0.0
else:
    pH_mix = 0.0

print(f"  {'pH':<25} {pH_ref:<20.4f} {pH_mix:<20.4f}")
is_a_val = is_a if is_a is not None else 0.0
is_b_val = is_b if is_b is not None else 0.0
print(f"  {'离子强度 (mol/kgw)':<25} {is_a_val:<20.4f} {is_b_val:<20.4f}")

# 元素浓度对比
if elements_a or elements_b:
    print()
    print(f"  {'元素':<10} {'海水 (mol/kgw)':<20} {'混合 (mol/kgw)':<20}")
    print(f"  {'-'*10} {'-'*20} {'-'*20}")
    all_elems = sorted(set(list(elements_a.keys()) + list(elements_b.keys())))
    for elem in all_elems:
        ea = elements_a.get(elem, 0)
        eb = elements_b.get(elem, 0)
        print(f"  {elem:<10} {ea:<20.6e} {eb:<20.6e}")

# 稀释因子
if elements_a and elements_b:
    for elem in ["Ca", "Mg", "Na", "Cl"]:
        if elem in elements_a and elem in elements_b and elements_a[elem] > 0:
            ratio = elements_b[elem] / elements_a[elem]
            print(f"  {elem} 稀释因子: {ratio:.4f} (理论 0.5 表示等体积混合稀释一倍)")
            break

# 潜在沉淀排查
print()
print("-- 饱和指数对比 (潜在沉淀排查) --")
print(f"  {'矿物':<15} {'海水 SI':<15} {'混合 SI':<15} {'说明':<25}")
print(f"  {'-'*15} {'-'*15} {'-'*15} {'-'*25}")

si_map_a = {s["phase"]: s["si"] for s in si_a}
si_map_b = {s["phase"]: s["si"] for s in si_b}
all_phases = sorted(set(list(si_map_a.keys()) + list(si_map_b.keys())))

for phase in all_phases:
    sa = si_map_a.get(phase, -999)
    sb = si_map_b.get(phase, -999)
    note = ""
    if sb >= 0 and sa >= 0:
        note = "均饱和/过饱和"
    elif sb > -0.5:
        note = "接近平衡"
    elif sb >= 0 and sa < 0:
        note = "混合后出现过饱和! 可能沉淀"
    elif sb < 0:
        note = "未饱和, 无沉淀风险"
    print(f"  {phase:<15} {sa:<15.4f} {sb:<15.4f} {note:<25}")

print()
print("=" * 60)
print("  结论")
print("=" * 60)

if is_a_val > 0 and is_b_val > 0:
    dil_ratio = is_b_val / is_a_val
    print(f"  * 离子强度降为原始的 {dil_ratio:.1%} ({is_a_val:.4f} -> {is_b_val:.4f} mol/kgw)")
    if 0.4 < dil_ratio < 0.6:
        print(f"    等体积混合稀释倍数约 2 倍, 符合预期")
else:
    print(f"  * 离子强度数据不完整")

if pH_a and pH_b:
    print(f"  * pH 从 {pH_a:.2f} 变为 {pH_b:.2f} (变化 {pH_b - pH_a:+.2f})")

# 检查哪些矿物混合后接近或超过饱和
precip_risk = [p for p in all_phases if si_map_b.get(p, -999) >= -0.3]
if precip_risk:
    print(f"  * 混合后潜在沉淀风险矿物: {', '.join(precip_risk)}")
else:
    print(f"  * 混合后无显著沉淀风险 (所有 SI < -0.3)")

print()


# =========================================================================
# 可视化
# =========================================================================
print("=" * 60)
print("可视化")
print("=" * 60)

# 双面板 SI 对比
chart1 = plot_multi_panel(
    [{"saturation_indices": si_a}, {"saturation_indices": si_b}],
    ["Seawater (A)", "Seawater + Pure Water (B)"],
    filepath=os.path.join(CHARTS_DIR, "si_comparison.png"),
)
print(f"  [OK] SI 对比图: {chart1}")

# 也可保持各自的单独图
chart2 = plot_saturation_indices(
    {"saturation_indices": si_a},
    title="Seawater Saturation Indices (before mixing)",
    filepath=os.path.join(CHARTS_DIR, "si_seawater.png"),
)
chart3 = plot_saturation_indices(
    {"saturation_indices": si_b},
    title="Mixed Solution Saturation Indices",
    filepath=os.path.join(CHARTS_DIR, "si_mixed.png"),
)
print(f"  [OK] 海水 SI: {chart2}")
print(f"  [OK] 混合 SI: {chart3}")


# =========================================================================
# 保存 JSON 结果
# =========================================================================
results = {
    "simulation": "exam_1.3_seawater_mixing",
    "description": "500mL seawater + 500mL pure water mixing simulation",
    "reference_seawater": {
        "pH": pH_a,
        "ionic_strength_mol_kgw": is_a_val,
        "saturation_indices": si_a,
        "element_molalities": elements_a,
    },
    "mixed_solution": {
        "pH": pH_b,
        "ionic_strength_mol_kgw": is_b_val,
        "saturation_indices": si_b,
        "element_molalities": elements_b,
    },
    "comparison": {
        "ph_change": (pH_b - pH_a) if (pH_a and pH_b) else None,
        "ionic_strength_dilution_ratio": (is_b_val / is_a_val) if is_a_val > 0 else None,
        "potential_precipitates": precip_risk,
    },
}

json_path = os.path.join(WORKSPACE, "results.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"  [OK] JSON 结果: {json_path}")

print()
print("=" * 60)
print("  考题 1.3 模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {chart1}")
print("=" * 60)
