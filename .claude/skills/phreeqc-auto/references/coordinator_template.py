"""
PHREEQC 模拟协调脚本模板
========================
使用示例:  python coordinator.py

该模板演示了完整的四步工作流:
  1. 构建参数 → 生成输入文件
  2. 运行 PHREEQC
  3. 解析输出 (主输出 + SELECTED_OUTPUT)
  4. 可视化

支持单溶液 speciation 和多溶液 MIX 两种模式。

注意事项:
  - Windows 中文终端: 设置 PYTHONIOENCODING=utf-8
  - 使用 cwd=WORKSPACE 确保 SELECTED_OUTPUT 写入可控位置
  - 路径中避免 Unicode 字符 (✓✗📄📊) 防止 GBK 编码崩溃
  - 多溶液模拟 (MIX): 使用 `solutions` list + `mix` dict 参数
  - 多段输出: 提取函数加 `last=True` 获取最终态数据
  - SELECTED_OUTPUT 多行数据: 用 `data[-1]` 取最后一行
"""
import sys, os

# ---- 环境设置 ----
# 项目根目录: 从当前文件向上回溯到包含 pyproject.toml 的目录
_PROJECT_MARKER = "pyproject.toml"
_current = os.path.dirname(os.path.abspath(__file__))
while _current and not os.path.isfile(os.path.join(_current, _PROJECT_MARKER)):
    _current = os.path.dirname(_current)
PROJECT_ROOT = _current
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
    extract_ionic_strength,  # 新增: 离子强度提取
    to_json,
)
from visualize import plot_saturation_indices, plot_selected_output_sweep

# =========================================================================
# Step 1: 构建参数 & 生成输入文件
# =========================================================================
print("=" * 60)
print("Step 1/4: 生成 PHREEQC 输入文件...")
print("=" * 60)

# 单溶液模式 (speciation / batch-reaction)
# params = {
#     "solution": {
#         "id": 1, "units": "ppm", "temp": 25.0,
#         "pH": 8.2, "pe": 8.451, "density": 1.023,
#         "components": {
#             "Ca": 412.3, "Mg": 1291.8, "Na": 10768.0,
#             "Cl": 19353.0, "S(6)": 2712.0, "Alkalinity": 141.682,
#         },
#     },
#     "selected_output": {
#         "si": ["Calcite", "Aragonite", "Dolomite"],
#         "totals": ["Ca", "Mg", "C"],
#         "pH": True,
#     },
# }

# 多溶液 + MIX 模式 (溶液混合)
params = {
    "solutions": [
        {
            "id": 1, "units": "ppm", "temp": 25.0,
            "pH": 8.22, "pe": 8.451, "density": 1.023,
            "components": {
                "Ca": 412.3, "Mg": 1291.8, "Na": 10768.0,
                "K": 399.1, "Cl": 19353.0, "S(6)": 2712.0,
                "Alkalinity": 141.682,
            },
        },
        {
            "id": 2, "units": "mol/kgw", "temp": 25.0,
            "pH": 7.0, "pe": 4.0, "density": 1.0,
            "components": {},
        },
    ],
    "mix": {"id": 1, "solutions": {1: 0.5, 2: 0.5}},
    "selected_output": {
        "si": ["Calcite", "Dolomite", "Aragonite", "Gypsum", "Halite"],
        "totals": ["Ca", "Mg", "Na", "K", "Cl", "S", "C"],
        "pH": True,
        "pe": True,
    },
}

content = generate_single_simulation(params, output_file="selected_output.txt")
input_path = write_input_file(content, os.path.join(WORKSPACE, "input.pqi"))
print(f"  [OK] 输入文件: {input_path}")
print()

# =========================================================================
# Step 2: 运行 PHREEQC (cwd=WORKSPACE 确保 SELECTED_OUTPUT 写入工作目录)
# =========================================================================
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

# 方法 A: 从主输出文件解析饱和指数 (推荐)
with open(os.path.join(WORKSPACE, "output.qpo"), "r", encoding="utf-8", errors="replace") as f:
    output_text = f.read()

si_data = extract_saturation_indices(output_text)
species_data = extract_species_distribution(output_text)
element_data = extract_element_molalities(output_text)
is_val = extract_ionic_strength(output_text)
print(f"  [OK] 饱和指数: {len(si_data)} 个矿物")
print(f"  [OK] 物种分布: {len(species_data)} 个物种")
print(f"  [OK] 元素浓度: {len(element_data)} 个元素")
print(f"  [OK] 离子强度: {is_val}" if is_val is not None else "  [WARN] 未找到离子强度")

# 注意: 多溶液模拟(MIX/参数扫描)中输出含多段数据,
# 用 last=True 获取最终态:
#   si_data = extract_saturation_indices(output_text, last=True)
#   element_data = extract_element_molalities(output_text, last=True)

# 方法 B: 从 SELECTED_OUTPUT 文件解析 (需要 cwd 正确)
selected_file = os.path.join(WORKSPACE, "selected_output.txt")
selected_data = {}
if os.path.isfile(selected_file):
    selected_data = parse_selected_output(selected_file)
    print(f"  [OK] Selected output: {selected_data.get('row_count', 0)} 行")
    # 多行数据(如 MIX 模拟): 用 data[-1] 取最终态
    if selected_data.get("row_count", 0) > 1:
        last_row = selected_data["data"][-1]
        print(f"  [NOTE] 多行 SELECTED_OUTPUT, 取末行作为结果")

# 保存 JSON
metadata = {"ionic_strength_mol_kgw": is_val} if is_val is not None else None
json_output = to_json(selected_data, si_data, species_data, element_data, metadata=metadata)
json_path = os.path.join(WORKSPACE, "results.json")
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

si_chart = plot_saturation_indices(
    {"saturation_indices": si_data},
    title="Saturation Indices",
    filepath=os.path.join(CHARTS_DIR, "saturation_indices.png"),
)
print(f"  [OK] 图表: {si_chart}")
print()

# =========================================================================
# 结果摘要
# =========================================================================
print("=" * 60)
print("  [OK] 模拟完成!")
print(f"  [JSON] {json_path}")
print(f"  [CHART] {si_chart}")
print("=" * 60)
