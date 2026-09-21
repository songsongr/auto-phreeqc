# PHREEQC 案例索引

这些案例位于仓库的 `examples/` 下。使用时先复制最接近的输入文件到新的结果目录，再根据当前样品和目标调整；不要直接改动案例源文件。

| 目标 | 案例目录 | 主要 PHREEQC 关键词 | 建议关注的结果 |
|---|---|---|---|
| Pb 水溶液形态分布 | `task1_1_pb_speciation` | `SOLUTION`、`SELECTED_OUTPUT` | 物种分布、饱和指数 |
| 方解石饱和指数及 pH 扫描 | `task1_2_calcite_si` | `SOLUTION`、`EQUILIBRIUM_PHASES` | Calcite SI、pH 趋势 |
| 海水与纯水混合 | `task1_3_SimpleMix` | `SOLUTION`、`MIX` | 混合后 pH、离子浓度与 SI |
| Cd 在矿物表面的吸附 | `task2_1_cd_adsorption` | `SURFACE`、`REACTION` | 溶解态 Cd 与表面物种 |
| 酸性矿山排水的石灰石中和 | `task2_2_amd_neutralization` | `SOLUTION`、`EQUILIBRIUM_PHASES` | pH、金属浓度、沉淀趋势 |
| 海水入侵下的阳离子交换 | `task2_3_cation_exchange` | `EXCHANGE`、`REACTION` | Na/Ca/Mg 交换变化 |
| 黄铁矿氧化动力学 | `task3_1_pyrite_kinetics` | `KINETICS`、`RATES` | pH、硫酸盐和金属随时间变化 |
| As 一维反应运移 | `task3_2_as_transport` | `TRANSPORT`、`SURFACE` | 穿透曲线与沿程浓度 |
| CO2 注入与多相反应 | `task3_3_co2_injection` | `GAS_PHASE`、`EQUILIBRIUM_PHASES` | pH、矿物变化、孔隙度代理指标 |

每个案例通常包含 `.pqi` 输入、`.qpo` 原始输出、`selected_output` 表格、`results.json` 和 `coordinator.py`。其中 `coordinator.py` 是可运行示例；公用生成、运行、解析和绘图函数在 `phreeqc_auto/` 包中。

## 选择案例的原则

先按反应类型选择案例，而不是只按元素名称选择：平衡计算优先查看 `SOLUTION` 与 `EQUILIBRIUM_PHASES`，吸附或交换查看 `SURFACE` 或 `EXCHANGE`，时间演化查看 `KINETICS`，空间运移查看 `TRANSPORT`。然后明确单位、数据库、温度、pH、氧化还原条件和输出指标。
