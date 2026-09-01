"""
Task 1.2: Calcite Saturation Index (pH sensitivity analysis)
============================================================
Input:  Ca = 80 mg/L, Alkalinity = 200 mg/L as CaCO3, pH = 7.2
Output: Calcite SI at pH=7.2 + SI vs pH sweep (6.0-8.5)

考察重点:
  - 碱度单位转换: 200 mg/L as CaCO3 -> 4.0 meq/L (PHREEQC 自动转换)
  - 电荷平衡: Ca2+ (4.0 meq/L) vs Alkalinity (4.0 meq/L) -> 完美平衡
  - pH 敏感性: 方解石 SI 随 pH 变化趋势
"""
import sys, os, re, copy, json

# ---- Environment ----
PROJECT_ROOT = r"C:\Users\songsongr\Desktop\claudecodel_proj\auto_phreeqc_proj"
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "phreeqc-auto", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(WORKSPACE, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

from generate_input import generate_single_simulation, generate_parameter_sweep, write_input_file
from run_phreeqc import run_simulation, find_database
from parse_output import (
    parse_selected_output,
    extract_saturation_indices,
    extract_species_distribution,
    extract_element_molalities,
    to_json,
)
from visualize import plot_saturation_indices, plot_selected_output_sweep

def fix_alkalinity(text):
    """Post-process: Alkalinity 200 -> Alkalinity 200 as CaCO3.
    PHREEQC 原生支持 'as CaCO3' 后缀来自动转换碱度单位.
    generate_solution_block() 不支持该语法, 需要后处理.
    """
    return text.replace("Alkalinity 200", "Alkalinity 200 as CaCO3")

# =========================================================================
# Step 1: 构建参数 & 生成输入文件
# =========================================================================
print("=" * 60)
print("Step 1/4: 生成 PHREEQC 输入文件...")
print("=" * 60)

# -- 1a. 单点: pH=7.2 --
single_params = {
    "solution": {
        "id": 1, "units": "mg/L", "temp": 25.0,
        "pH": 7.2, "pe": 4.0, "density": 1.0,
        "components": {"Ca": 80, "Alkalinity": 200},
    },
    "selected_output": {
        "si": ["Calcite"],
        "totals": ["Ca", "C"],
        "pH": True,
    },
}

single_content = fix_alkalinity(generate_single_simulation(single_params, output_file="selected_output.txt"))
single_input_path = write_input_file(single_content, os.path.join(WORKSPACE, "input_single.pqi"))
print(f"  [OK] 单点输入: {single_input_path}")

# -- 1b. pH 扫描: 6.0 ~ 8.5 (步长 0.25, 共 11 步) --
base_params = {
    "solution": {
        "id": 1, "units": "mg/L", "temp": 25.0,
        "pH": 7.0, "pe": 4.0, "density": 1.0,
        "components": {"Ca": 80, "Alkalinity": 200},
    },
    "selected_output": {
        "si": ["Calcite", "Aragonite", "Dolomite"],
        "totals": ["Ca", "C"],
        "pH": True,
    },
}

ph_values = [6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5]
sweep_content = fix_alkalinity(generate_parameter_sweep(base_params, "solution.pH", ph_values, output_dir="."))
sweep_input_path = write_input_file(sweep_content, os.path.join(WORKSPACE, "input_sweep.pqi"))
print(f"  [OK] pH扫描输入: {sweep_input_path} ({len(ph_values)}步)")

# =========================================================================
# Step 2: 运行 PHREEQC
# =========================================================================
print("\n" + "=" * 60)
print("Step 2/4: 运行 PHREEQC...")
print("=" * 60)

db_path = find_database("phreeqc.dat")

# 单点
r1 = run_simulation(input_file=single_input_path,
    output_file=os.path.join(WORKSPACE, "output_single.qpo"),
    database=db_path, timeout=120, cwd=WORKSPACE)
if not r1["success"]:
    print(f"  [FAIL] 单点: {r1['error']}")
    sys.exit(1)
print(f"  [OK] 单点模拟成功")

# pH 扫描
r2 = run_simulation(input_file=sweep_input_path,
    output_file=os.path.join(WORKSPACE, "output_sweep.qpo"),
    database=db_path, timeout=120, cwd=WORKSPACE)
if not r2["success"]:
    print(f"  [FAIL] pH扫描: {r2['error']}")
    sys.exit(1)
print(f"  [OK] pH扫描模拟成功")

# =========================================================================
# Step 3: 解析输出
# =========================================================================
print("\n" + "=" * 60)
print("Step 3/4: 解析输出...")
print("=" * 60)

# 单点
with open(os.path.join(WORKSPACE, "output_single.qpo"), "r", encoding="utf-8", errors="replace") as f:
    otxt = f.read()

si_single = extract_saturation_indices(otxt)
species_single = extract_species_distribution(otxt)
elements_single = extract_element_molalities(otxt)
print(f"  [OK] 单点 - SI: {len(si_single)}矿物, 物种: {len(species_single)}, 元素: {len(elements_single)}")

# pH 扫描: 按 "Beginning of initial solution calculations" 切分
with open(os.path.join(WORKSPACE, "output_sweep.qpo"), "r", encoding="utf-8", errors="replace") as f:
    stxt = f.read()

blocks = re.split(r"Beginning of initial solution calculations", stxt)
all_si = [extract_saturation_indices(b) for b in blocks[1:]]
print(f"  [OK] pH扫描 - {len(all_si)} 步饱和指数")

# 读取 step 文件
step_data_list = []
for i in range(1, len(ph_values) + 1):
    sp = os.path.join(WORKSPACE, f"step_{i}.txt")
    if os.path.isfile(sp):
        step_data_list.append(parse_selected_output(sp))
print(f"  [OK] pH扫描 - {len(step_data_list)} 步 Selected Output")

# 保存 JSON (单点)
sel_file = os.path.join(WORKSPACE, "selected_output.txt")
sel_data = {}
if os.path.isfile(sel_file):
    sel_data = parse_selected_output(sel_file)

json_output = to_json(sel_data, si_single, species_single, elements_single,
    metadata={"task": "1.2", "pH": 7.2, "Ca_mg_L": 80, "Alkalinity_as_CaCO3": 200})
json_path = os.path.join(WORKSPACE, "results_single.json")
with open(json_path, "w", encoding="utf-8") as f:
    f.write(json_output)
print(f"  [OK] JSON: {json_path}")

# 保存 JSON (pH 扫描)
sweep_results = {"pH_values": ph_values, "steps": []}
for i, (ph, si_step) in enumerate(zip(ph_values, all_si)):
    step_info = {"pH": ph, "saturation_indices": si_step}
    sweep_results["steps"].append(step_info)
sweep_json_path = os.path.join(WORKSPACE, "results_sweep.json")
with open(sweep_json_path, "w", encoding="utf-8") as f:
    json.dump(sweep_results, f, indent=2, ensure_ascii=False)
print(f"  [OK] JSON (扫描): {sweep_json_path}")

# =========================================================================
# Step 4: 可视化
# =========================================================================
print("\n" + "=" * 60)
print("Step 4/4: 生成图表...")
print("=" * 60)

# 单点 SI 柱状图
c1 = plot_saturation_indices(
    {"saturation_indices": si_single},
    title="Saturation Indices (pH=7.2, Ca=80 mg/L, Alk=200 as CaCO3)",
    filepath=os.path.join(CHARTS_DIR, "saturation_indices_single.png"),
)
print(f"  [OK] 单点SI图: {c1}")

# pH 扫描: 从 step 文件提取 calcite SI 绘图
# 先查看 step 文件的列结构
if step_data_list and "columns" in step_data_list[0]:
    print(f"  [DEBUG] Step列: {step_data_list[0]['columns']}")

    # 手动构建 pH vs Calcite SI 数据
    ph_plot_data = {"columns": ["pH", "si_Calcite"], "data": []}
    for i, sd in enumerate(step_data_list):
        if sd.get("data") and len(sd["data"]) > 0:
            cols = sd["columns"]
            row = sd["data"][0]
            ph_idx = cols.index("pH") if "pH" in cols else -1
            si_idx = cols.index("si_Calcite") if "si_Calcite" in cols else -1
            if ph_idx >= 0 and si_idx >= 0:
                ph_plot_data["data"].append([row[ph_idx], row[si_idx]])

    # 也尝试使用 plot_selected_output_sweep
    c2 = plot_selected_output_sweep(
        ph_plot_data,
        x_column="pH", y_columns=["si_Calcite"],
        title="Calcite Saturation Index vs pH",
        xlabel="pH",
        filepath=os.path.join(CHARTS_DIR, "calcite_si_vs_ph.png"),
    )
    print(f"  [OK] pH扫描图: {c2}")
else:
    # 备用: 从 all_si 手动绘制
    print(f"  [WARN] 无法从 step 文件解析, 尝试从 all_si 手动绘图")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    calcite_si_vals = []
    for step_si in all_si:
        val = None
        for si_entry in step_si:
            if si_entry["phase"] == "Calcite":
                val = si_entry["si"]
                break
        calcite_si_vals.append(val)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ph_values, calcite_si_vals, marker="o", color="#2ca02c", linewidth=2)
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_xlabel("pH")
    ax.set_ylabel("Calcite SI")
    ax.set_title("Calcite Saturation Index vs pH")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    c2 = os.path.join(CHARTS_DIR, "calcite_si_vs_ph.png")
    fig.savefig(c2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] pH扫描图(备选): {c2}")

# =========================================================================
# 结果摘要
# =========================================================================
print("\n" + "=" * 60)
print("  [OK] 模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {c1}")
print(f"  [CHART] {c2}")
print("=" * 60)

# 打印主要结果
calcite_si_main = None
for s in si_single:
    if s["phase"] == "Calcite":
        calcite_si_main = s["si"]
        break

print()
print("=== 主要结果: Calcite SI at pH = 7.2 ===")
print(f"  Calcite SI = {calcite_si_main:.3f}")

# pH 扫描表
print()
print("=== pH 敏感性扫描 ===")
print(f"  {'pH':<8} {'Calcite SI':<12} {'SI>0?':<10}")
print(f"  {'-'*30}")
for i, ph in enumerate(ph_values):
    if i < len(all_si):
        calcite_val = None
        for si_entry in all_si[i]:
            if si_entry["phase"] == "Calcite":
                calcite_val = si_entry["si"]
                break
        if calcite_val is not None:
            status = "过饱和" if calcite_val > 0 else ("平衡" if abs(calcite_val) < 0.01 else "未饱和")
            print(f"  {ph:<8.2f} {calcite_val:<+12.3f} {status:<10}")

# 电荷平衡信息
print()
print("=== 水化学分析 ===")
ca_mmol = 80.0 / 40.078  # 2.0 mmol/L
ca_meq = ca_mmol * 2      # 4.0 meq/L
alk_meq = 200.0 / 50.045  # 4.0 meq/L
print(f"  Ca2+  : {ca_mmol:.2f} mmol/L = {ca_meq:.2f} meq/L")
print(f"  碱度  : {alk_meq:.2f} meq/L (as CaCO3: {200:.0f} mg/L)")
print(f"  电荷平衡: Ca2+ {ca_meq:.2f} = 碱度 {alk_meq:.2f} -> {abs(ca_meq - alk_meq):.4f} meq/L 差 (完美平衡)")
print()
