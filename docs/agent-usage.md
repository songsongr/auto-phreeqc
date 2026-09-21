# 在 Claude Code 和 Codex 中使用 auto-phreeqc

本指南面向希望以自然语言协作完成 PHREEQC 模拟的用户。无论使用 Claude Code 还是 Codex，都应以仓库根目录为工作目录，并通过 `phreeqc_auto` Python 包完成输入生成、计算、结果解析和图表输出。

## 准备环境

1. 安装 PHREEQC，并确保可执行文件和所用数据库可访问。
2. 在仓库根目录安装 Python 包：

   ```bash
   python -m pip install -e .
   ```

3. 建议显式设置以下环境变量，避免不同电脑上的安装位置差异：

   ```powershell
   $env:PHREEQC_EXE = "C:\\path\\to\\phreeqc.exe"
   $env:PHREEQC_DATABASE = "C:\\path\\to\\phreeqc.dat"
   ```

   macOS、Linux 或 Git Bash 中可使用：

   ```bash
   export PHREEQC_EXE="/path/to/phreeqc"
   export PHREEQC_DATABASE="/path/to/phreeqc.dat"
   ```

运行前可用 `find_phreeqc_exe()` 与 `find_database()` 验证路径。若未设置环境变量，运行库也会尝试从常见安装位置和项目位置寻找它们。

## 安装随附 Skill（可选）

仓库中的 `skills/phreeqc-auto/` 是精简的用户 Skill，不包含开发提示词或
内部记录。若希望工具自动发现它，可将整个文件夹复制到对应工具的 Skill
目录；也可以直接在请求中引用仓库内的 `skills/phreeqc-auto/SKILL.md`。

- **Claude Code**：复制到项目的 `.claude/skills/phreeqc-auto/`。
- **Codex**：复制到 Codex 用户目录中的 `skills/phreeqc-auto/`，或把本仓库
  作为工作区并在请求中引用该文件。

## 每次运行前先确认什么

无论由人还是智能体生成输入，都应先把以下信息汇总给用户确认，再开始计算：

1. **目标和模型类型**：物种分布、批反应、混合、表面络合、离子交换、动力学或一维运移。
2. **溶液组成**：各组分、浓度、单位、温度、pH、pe 或氧化还原条件。
3. **反应条件**：参与的矿物、气体、表面或交换位点；平衡或动力学假设；反应量与时间。
4. **扫描设置**：待变化的变量、范围、步数，以及需要追踪的指标。
5. **数据库和输出**：数据库文件、要提取的总量或饱和指数、需要的表格和图表。
6. **默认值和不确定项**：明确标出推定值，等待用户确认或修改。

确认摘要时，应同时说明输入和结果将保存到哪个独立目录。不要覆盖 `examples/` 中的原始案例文件。

## 在 Claude Code 中使用

在仓库根目录启动 Claude Code，并让它先阅读 [`skills/phreeqc-auto/SKILL.md`](../skills/phreeqc-auto/SKILL.md) 和本指南。随后可直接描述目标，例如：

> 用 25°C、pH 7.2 的 Ca–碳酸盐水样计算方解石饱和指数；先列出单位、碱度表达方式和数据库假设，等我确认后再运行，并生成结果表和图。

一个完整的协作过程应当是：

1. Claude Code 提取已知条件并提出必要的补充问题。
2. 它给出包含默认值的参数摘要，等待确认。
3. 确认后，它调用 `phreeqc_auto` 生成 `.pqi` 输入、运行 PHREEQC、解析输出，并把表格和图表写入结果目录。
4. 它报告关键数值、文件路径、图表含义和需要注意的收敛或数据库问题。

## 在 Codex 中使用

将该仓库作为 Codex 工作区打开，并在请求中说明使用 [`skills/phreeqc-auto/SKILL.md`](../skills/phreeqc-auto/SKILL.md)。提示词可与 Claude Code 相同，例如：

> 请使用 phreeqc-auto 完成海水与纯水等体积混合模拟。先总结配方、浓度单位、温度、pH、数据库和希望输出的离子强度；我确认后再生成输入并运行。请保留原始输出、结构化结果和图表。

Codex 应遵循相同的确认、运行和汇报顺序。对参数扫描或运移模拟，要额外确认扫描范围、步数、时间单位、单元数和输出单元。

## 直接调用公开运行库

下面是一个可作为智能体执行目标的最小示例。它创建独立结果目录，生成输入，运行计算，解析 SELECTED_OUTPUT，并保存饱和指数图。

```python
from pathlib import Path

from phreeqc_auto import (
    generate_single_simulation,
    parse_selected_output,
    run_simulation,
    write_input_file,
)
from phreeqc_auto.parse_output import extract_saturation_indices
from phreeqc_auto.visualize import plot_saturation_indices

run_dir = Path("runs/calcite_si")
charts_dir = run_dir / "charts"
charts_dir.mkdir(parents=True, exist_ok=True)

params = {
    "solution": {
        "id": 1,
        "units": "mg/L",
        "temp": 25.0,
        "pH": 7.2,
        "pe": 4.0,
        "components": {
            "Ca": 80.0,
            "Alkalinity": "200 as CaCO3",
        },
    },
    "selected_output": {
        "pH": True,
        "pe": True,
        "totals": ["Ca", "C"],
        "si": ["Calcite"],
    },
}

input_text = generate_single_simulation(params)
input_path = write_input_file(input_text, str(run_dir / "input.pqi"))

result = run_simulation(
    input_path,
    output_file=str(run_dir / "output.qpo"),
    cwd=str(run_dir),
)
if not result["success"]:
    raise RuntimeError(result["error"])

selected = parse_selected_output(str(run_dir / "selected_output.txt"))
output_text = Path(result["output_file"]).read_text(
    encoding="utf-8", errors="replace"
)
saturation_indices = extract_saturation_indices(output_text, last=True)
chart_path = plot_saturation_indices(
    saturation_indices,
    title="方解石饱和指数",
    filepath=str(charts_dir / "saturation_indices.png"),
)

print(selected["columns"])
print(chart_path)
```

常用模块与输出如下：

| 目的 | 函数或模块 | 典型产物 |
|---|---|---|
| 生成输入 | `generate_single_simulation()`、`write_input_file()` | `input.pqi` |
| 执行计算 | `run_simulation()` | `output.qpo`、SELECTED_OUTPUT 文件 |
| 解析表格 | `parse_selected_output()` | 列名、数据行、行数 |
| 提取标准输出 | `extract_saturation_indices()`、`extract_species_distribution()`、`extract_element_molalities()` | 饱和指数、物种分布、元素摩尔浓度 |
| 单点结果图 | `plot_saturation_indices()` | 饱和指数条形图 |
| 参数扫描图 | `plot_selected_output_sweep()` | 多曲线扫描图 |
| 运移结果图 | `plot_breakthrough_curve()` | 突破曲线 |

含有多个反应阶段或多个溶液的计算，提取标准输出时通常应传入 `last=True`，以取得最终阶段的数据。

## 九个随附案例

每个案例目录都包含可检查的 PHREEQC 输入和结果文件。处理新问题时，先选择最接近的案例作为起点，把输入复制到新的结果目录后再修改。

| 级别 | 案例 | 目录 | 适用问题 |
|---|---|---|---|
| L1 | Pb 形态分布 | `examples/task1_1_pb_speciation/` | 铅在 NaCl 溶液中的物种分布 |
| L1 | 方解石饱和指数 | `examples/task1_2_calcite_si/` | pH 对饱和指数的影响 |
| L1 | 海水与纯水混合 | `examples/task1_3_SimpleMix/` | 稀释和 `MIX` 计算 |
| L2 | Cd 表面吸附 | `examples/task2_1_cd_adsorption/` | 氧化物表面络合与 pH 扫描 |
| L2 | AMD 石灰石中和 | `examples/task2_2_amd_neutralization/` | 酸性矿山排水中和与沉淀 |
| L2 | 阳离子交换 | `examples/task2_3_cation_exchange/` | 海水入侵下的离子交换 |
| L3 | 黄铁矿动力学 | `examples/task3_1_pyrite_kinetics/` | 矿物溶解动力学 |
| L3 | As 一维运移 | `examples/task3_2_as_transport/` | 反应性运移与突破曲线 |
| L3 | CO₂ 注入 | `examples/task3_3_co2_injection/` | 高压 CO₂ 条件下的多相演化 |

## 结果交付清单

一次完成的模拟至少应交付：

- 完整的输入文件和所用数据库名称；
- PHREEQC 原始输出与 SELECTED_OUTPUT 数据；
- 可复核的结构化结果或表格；
- 与问题匹配的图表，并标出坐标含义、单位和关键阈值；
- 简明结论，包括主要数值、模型假设、异常信息和下一步可调整的参数。

模型结论受输入条件和热力学数据库影响。若计算未收敛、目标元素不在数据库中，或所需物相缺少数据，应如实报告原因，并在修改条件后重新获得用户确认。
