---
name: phreeqc-auto
description: 使用 phreeqc_auto 包生成、运行、解析和可视化 PHREEQC 地球化学模拟；适用于物种分布、反应、混合、吸附、交换、动力学和一维运移问题。
---

# PHREEQC 自动模拟

使用本技能把用户已确认的地球化学条件转换为可复核的 PHREEQC 输入、计算结果和图表。使用仓库中的 `phreeqc_auto` 包完成运行和解析。

## 开始前

1. 若当前工作区是本仓库，先阅读 `docs/agent-usage.md`；否则确认本机 PHREEQC、数据库和 `phreeqc_auto` 包可用。
2. 从用户请求中提取模型目标、溶液组成、浓度单位、温度、pH、pe 或氧化还原条件、反应相、数据库和希望得到的指标。
3. 对缺失但会影响结果的条件提出问题；可建议默认值，但必须明确标为默认值。
4. 在生成输入或运行计算前，给出一份完整参数摘要并等待用户确认。扫描、动力学和运移问题还要确认变量范围、步数、时间单位、单元数和输出位置。

## 执行方式

将每次模拟写入一个独立结果目录，保留输入、原始输出、SELECTED_OUTPUT、结构化结果和图表。不要修改 `examples/` 中的源文件。

使用公开运行库完成以下步骤：

```python
from phreeqc_auto import (
    generate_single_simulation,
    parse_selected_output,
    run_simulation,
    write_input_file,
)
from phreeqc_auto.parse_output import (
    extract_element_molalities,
    extract_saturation_indices,
    extract_species_distribution,
)
from phreeqc_auto.visualize import (
    plot_breakthrough_curve,
    plot_saturation_indices,
    plot_selected_output_sweep,
)
```

1. 用 `generate_single_simulation(params)` 生成 PHREEQC 文本，并用 `write_input_file()` 保存为 `.pqi`。
2. 用 `run_simulation(input_file, output_file=..., cwd=...)` 执行计算。检查返回值的 `success`；失败时说明错误，修改任何模型条件前重新确认。
3. 用 `parse_selected_output()` 读取 SELECTED_OUTPUT 表格；用标准输出提取函数获取饱和指数、物种分布或元素摩尔浓度。多阶段计算通常应使用 `last=True` 获取最终阶段。
4. 按问题选择图表：单点饱和指数用 `plot_saturation_indices()`，参数扫描用 `plot_selected_output_sweep()`，一维运移用 `plot_breakthrough_curve()`。

## 九个案例的使用

选择最接近用户目标的案例，复制其输入到新的结果目录后再调整参数：

| 模型类型 | 案例目录 |
|---|---|
| Pb 形态分布 | `examples/task1_1_pb_speciation/` |
| 方解石饱和指数 | `examples/task1_2_calcite_si/` |
| 海水与纯水混合 | `examples/task1_3_SimpleMix/` |
| Cd 表面吸附 | `examples/task2_1_cd_adsorption/` |
| AMD 石灰石中和 | `examples/task2_2_amd_neutralization/` |
| 阳离子交换 | `examples/task2_3_cation_exchange/` |
| 黄铁矿动力学 | `examples/task3_1_pyrite_kinetics/` |
| As 一维运移 | `examples/task3_2_as_transport/` |
| CO₂ 注入 | `examples/task3_3_co2_injection/` |

案例用于帮助选择输入结构和输出指标，不应代替对当前样品条件的确认。

## 结果汇报

完成后应向用户简洁说明：

- 已确认的模拟条件和数据库；
- 是否成功完成，若失败则给出可操作的错误说明；
- 最重要的数值与地球化学含义；
- 输入、原始输出、表格和图表的路径；
- 影响解读的假设、单位或数据库限制。

不要把图表只当作装饰：说明坐标、单位、阈值以及趋势与模型条件的关系。
