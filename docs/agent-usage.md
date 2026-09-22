# 使用 Codex 完成 PHREEQC 计算

本指南说明如何让 AI 编程助手在本仓库内完成可复核的 PHREEQC 模拟。运行计算
仍在你的本机进行：智能体负责整理条件、生成输入、调用公开运行库、解析输出和
解释结果。

## 首次配置

在仓库根目录让 Agent 运行：

```bash
python doctor/bootstrap.py
```

该命令创建项目专属 `.venv/`，安装 `phreeqc_auto`，定位 PHREEQC 程序和数据库，
写入不提交到 Git 的 `.phreeqc-auto.local.json`，并进行一次临时计算。若程序安装
在非标准位置，传入两个路径：

```bash
python doctor/bootstrap.py \
  --phreeqc-exe /path/to/phreeqc \
  --database /path/to/phreeqc.dat
```

若输出显示找不到 PHREEQC，请先通过 [USGS 官方下载页](https://water.usgs.gov/water-resources/software/PHREEQC/)
安装它，再重新运行上述命令。不要让 Agent 静默安装系统级外部软件。

## Skill 如何被发现

- **Codex**：仓库根目录的 `.agents/skills/phreeqc-auto/` 是项目层自动发现入口。

运行代码的唯一来源始终是根目录 `phreeqc_auto/` 包；Skill 目录只保存行为规则
和参考资料，不保存另一份运行实现。

## 可以直接对 Agent 说什么

首次配置：

```text
配置这个 auto-phreeqc 仓库并运行自检。成功后启用随附 Skill，等待我的自然语言
计算请求；若 PHREEQC 缺失，说明官方安装步骤后继续配置。
```

开始计算：

```text
模拟 25 °C、pH 7.2、Ca 80 mg/L、碱度 200 mg/L as CaCO3 的水样；计算方解石
饱和指数。先说明单位、数据库和假设，等我确认后运行，并输出表格和图。
```

## 一次计算的标准流程

1. **澄清目标**：形态分析、批反应、混合、表面络合、离子交换、动力学或运移。
2. **确认条件**：组分、浓度单位、温度、pH、pe/氧化还原状态、反应相、数据库和
   需要的指标。扫描和运移还要确认范围、步数、时间单位、单元数与输出位置。
3. **汇总假设**：智能体必须把缺失条件和拟采用的默认值列出，等待确认后才修改模型
   或启动计算。
4. **运行并保留证据**：按下述 Workbench 强制交付规则创建运行记录并保存 `.pqi`、
   原始输出、SELECTED_OUTPUT、结构化结果和图表；不修改 `examples/` 中的案例文件。
5. **汇报解读**：报告关键数值、图表坐标与趋势、数据库名称、假设以及收敛或模型
   限制。

## Workbench 强制交付

所有由 agent 为用户实际运行的模拟都必须显示为一个 Workbench 运行，而不是写入根目录
`runs/` 或临时目录。创建输入前，使用 Workbench 存储服务创建
`workbench/workspace_workbench/<run_id>/`。`params` 必须包含用户确认的配置：模拟类型、
组分和单位、温度、pH/pe 或气体边界、反应相、扫描/时间/单元设置、数据库和目标输出。

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT / "workbench" / "backend"))
from services import storage

run_id = "descriptive_unique_run_id"
storage.init(str(PROJECT_ROOT / "workbench" / "workspace_workbench"))
storage.create_run(
    run_id,
    display_name="用户可读的模拟名称",
    params={
        "simulation_type": "batch_reaction",
        "confirmed_conditions": {"units": "mol/kgw", "temp_c": 25.0},
        "database": "minteq.v4.dat",
        "requested_outputs": ["pH", "selected_output"],
    },
)
run_dir = Path(storage.workspace_root()) / run_id
```

将 `input.pqi`、`output.qpo`、`selected_output.txt`（适用时）、`results.json`、图表及
`events.log` 写入该目录；复杂算例还应保存全部子步骤输入/输出和协调脚本。结束时设置
`succeeded` 或 `failed` 并校验 WebUI 契约：

```python
storage.set_status(run_id, "succeeded")
visible = any(item["run_id"] == run_id for item in storage.list_runs())
required = ["meta.json", "events.log", "input.pqi", "output.qpo", "results.json"]
assert visible and storage.get_run(run_id) is not None
assert all((run_dir / name).is_file() for name in required)
```

上述验证确保下次启动 Workbench 时，运行会出现在列表并能打开详情页；如果服务已经
运行，还应请求 `/api/v1/runs/<run_id>` 和 `/api/v1/runs/<run_id>/files` 进行在线验证。
验证失败时不得交付模拟数值，必须将状态标为 `failed` 并报告缺失项。

## 运行库接口

智能体和 Workbench 都应调用根目录的公开包：

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
```

`run_simulation()` 会优先使用 `PHREEQC_EXE` / `PHREEQC_DATABASE`，其次使用
`.phreeqc-auto.local.json`、`PATH` 和常见安装位置。多阶段计算提取标准输出时，
通常应使用 `last=True` 获取最终阶段。

## 选择案例

新问题应先从最相近的案例复制输入到结果目录，再调整条件：

| 类型 | 起点 |
| --- | --- |
| Pb 形态分布 | `examples/task1_1_pb_speciation/` |
| 方解石饱和指数 | `examples/task1_2_calcite_si/` |
| 海水与纯水混合 | `examples/task1_3_SimpleMix/` |
| Cd 表面吸附 | `examples/task2_1_cd_adsorption/` |
| AMD 石灰石中和 | `examples/task2_2_amd_neutralization/` |
| 阳离子交换 | `examples/task2_3_cation_exchange/` |
| 黄铁矿动力学 | `examples/task3_1_pyrite_kinetics/` |
| As 一维运移 | `examples/task3_2_as_transport/` |
| CO₂ 注入 | `examples/task3_3_co2_injection/` |

案例能帮助确定输入结构和输出指标，但不能替代对当前样品条件的确认。
