---
name: phreeqc-auto
description: >-
  PHREEQC 全流程自动化模拟。当用户提到 PHREEQC、地球化学模拟、溶液 speciation、批反应、矿物溶解沉淀、饱和指数计算、地球化学参数扫描、水质模拟时，必须使用此 skill。涉及地球化学计算、水化学分析或矿物-水相互作用的任何任务都需要此 skill。即使只是简单提及"模拟"+"溶液"或"矿物"的组合，也应触发此 skill 以确认用户需求。此 skill 是完成 PHREEQC 相关任务的唯一正确工具。
---

# PHREEQC 全流程自动化 Skill

本 Skill 实现基于自然语言的 PHREEQC 地球化学模拟全流程自动化：需求澄清 → 输入生成 → 模拟运行 → 输出解析 → 可视化。

## 工作流程概览

```
Phase 1: 需求澄清 ── 与用户半自动对话确定模拟参数
Phase 2: 任务编排 ── 按需拆分生成、运行、解析和可视化子任务
Phase 3: 结果呈现 ── 终端报告 + 数据文件 + 图表
```

## 工作目录

所有文件操作在项目根目录下执行。

### Workbench 强制交付（硬性规则）

所有由 agent 为用户实际运行的模拟必须先创建为 Workbench 运行，最终目录只能是
`workbench/workspace_workbench/<run_id>/`，不能写入根目录 `runs/` 或 `examples/`。
通过 `workbench/backend/services/storage.py` 的 `storage.create_run()` 建立运行记录，并在
`meta.json` 的 `params` 中完整写入用户确认的配置：模拟类型、组分及单位、温度、pH/pe
或气体边界、反应相、扫描/时间/单元参数、数据库与目标输出。

运行目录必须包含 `meta.json`、`events.log`、`input.pqi`、`output.qpo`、
`selected_output.txt`（适用时）、`results.json` 和 `charts/`；多阶段模拟还要保留所有
子步骤原始输入/输出和协调脚本。完成前必须以 `storage.list_runs()`、`storage.get_run()`
及规范产物存在性验证其在 WebUI 列表和详情页可见；若 Workbench 服务已运行，再验证
`/api/v1/runs/<run_id>` 和 `/files`。未通过验证时将运行标为失败，不得交付数值结果。
可执行模板见仓库 `docs/agent-usage.md` 的“Workbench 强制交付”。

## Phase 1: 需求澄清

**目标:** 与用户逐一确认模拟所需的关键参数。用户无法决定时，你根据地球化学常识推理合理默认值。

### 交互规则
1. **一次只问一个问题** — 不要一次性抛出所有问题
2. **显示已知参数** — 先总结你从用户指令中提取到的内容
3. **标记推理值** — 你推理的参数要标注 `[自动推理]`，让用户知道可以覆盖
4. **确认后才执行** — 汇总所有参数后让用户确认再进入 Phase 2

### Speciation 所需参数清单

| 参数 | 默认/推理规则 | 必需 |
|------|---------------|------|
| 温度 | 25°C（室温） | 是，可推理 |
| pH | 必须问用户 | 是 |
| pe/pe | 4.0（氧化环境）/ 可通过 O2/H2S 推理 | 是，可推理 |
| 离子组分 | 必须问用户（至少主要离子） | 是 |
| 浓度单位 | mol/kgw（默认，可改为 ppm/mg/L） | 是，可推理 |
| 数据库 | phreeqc.dat | 是，可推理 |
| 目标物 (SI) | 用户关注哪些矿物？ | 按需 |
| 密度 | 1.0（稀溶液） | 可推理 |

### Batch-Reaction 额外参数

| 参数 | 默认/推理规则 | 必需 |
|------|---------------|------|
| 反应相 | 必须问用户（哪些矿物/气体参与反应？） | 是 |
| 饱和指数目标 | 0.0（默认平衡） | 可推理 |
| 反应物量 | 必须问用户，或推理合理量（如 10 mol 矿物） | 是 |
| 反应步长 | 1 步（单步），或用户指定步数/扫描范围 | 按需 |
| 动力学/平衡 | 默认平衡 (EQUILIBRIUM_PHASES) | 可推理 |

### 参数扫描额外确认

| 参数 | 默认/推理规则 |
|------|---------------|
| 扫描变量 | pH, 温度, 反应量 中最常用的 |
| 扫描范围 | 用户指定，或推理合理范围 (如 pH 4-9) |
| 步数/步长 | 用户指定，或默认 10 步 |

### 参数汇总格式

确认时使用如下格式：

```
📋 模拟参数汇总
━━━━━━━━━━━━━━━━━━━━
类型:  Speciation（海水）
温度:  25°C [自动推理]
pH:    8.22
组分:  Ca 412.3 ppm, Mg 1291.8 ppm, Na 10768 ppm, Cl 19353 ppm
数据库: phreeqc.dat [自动推理]
关注矿物: Calcite, Dolomite
━━━━━━━━━━━━━━━━━━━━
以上参数确认无误？要修改任何参数吗？
```

## Phase 2: 团队编排

用户确认参数后，将生成、运行、解析和可视化拆成可追踪的子任务。仅当宿主提供
可靠的子任务/并行能力时才并行执行；否则由当前 agent 按顺序完成，不能假设存在
`TeamCreate`、`TeamDelete` 或其他 Claude 专属工具。

### 子任务划分

如宿主支持并行 agent，在同一轮派发以下 4 个子任务；每个子任务都必须写入同一
Workbench run 目录并报告真实结果。宿主不支持并行时，按同样顺序在当前 agent 中执行：

**输入生成 Agent** — 任务说明模板:
```
You are generating PHREEQC input files for a {speciation/batch_reaction} simulation.

Parameters (confirmed by user):
{JSON parameters}

Using the public runtime module:
phreeqc_auto/generate_input.py

IMPORTANT: Work in the project root directory
- Create the Workbench run through storage.create_run() before writing input.
- Use workbench/workspace_workbench/<run-id>/ as the only result directory.
- Populate Workbench meta params with every confirmed simulation condition.
- Call generate_single_simulation(params, output_file="selected.txt") or generate_parameter_sweep(...)
- Write the result to workbench/workspace_workbench/<run-id>/input.pqi using write_input_file()

Generate SELECTED_OUTPUT that includes all relevant -si and -totals for the simulation.
```

**模拟运行 Agent** — 任务说明模板:
```
You are running a PHREEQC simulation. The input file is at:
project_root\workbench\workspace_workbench\<run-id>\input.pqi

Using the public runtime module:
phreeqc_auto/run_phreeqc.py

Call:
  from phreeqc_auto.run_phreeqc import run_simulation
  result = run_simulation(
      input_file="workbench/workspace_workbench/<run-id>/input.pqi",
      output_file="workbench/workspace_workbench/<run-id>/output.qpo",
      cwd="workbench/workspace_workbench/<run-id>",
  )

Check result["success"]. If failed, try one retry with adjusted parameters.
IMPORTANT: Always pass cwd=WORKBENCH_RUN_DIR so SELECTED_OUTPUT files are written correctly.
```

**输出解析 Agent** — 任务说明模板:
```
You are parsing PHREEQC output files from:
project_root\workbench\workspace_workbench\<run-id>\

Using the public runtime module:
  from phreeqc_auto.parse_output import parse_selected_output, extract_saturation_indices, to_json

- Parse selected_output.txt
- Read output.qpo for saturation indices, species distribution, element molalities
- Save results to workbench/workspace_workbench/<run-id>/results.json
```

**可视化 + 文档 Agent** — 任务说明模板:
```
You are creating visualizations AND a human-readable README from parsed PHREEQC results at:
project_root\workbench\workspace_workbench\<run-id>\results.json

Using the public runtime module:
  from phreeqc_auto.visualize import plot_saturation_indices, plot_selected_output_sweep

STEP 1 — Generate charts (save to workbench/workspace_workbench/<run-id>/charts/):
  - Load results.json
  - Call plot_saturation_indices(data, title=..., filepath="workbench/workspace_workbench/<run-id>/charts/<descriptive_name>.png")
  - If sweep data exists: plot_selected_output_sweep(selected_output, x_column, y_columns, ...)
  - Use descriptive filenames (e.g. "ph_titration.png" not "parameter_sweep.png")

STEP 2 — Write workbench/workspace_workbench/<run-id>/README.md with this EXACT structure:

```markdown
# 模拟: {简短描述}

**日期**: {YYYY-MM-DD} | **数据库**: {database}

## 模拟条件
{列出关键输入参数：溶液组分、反应物、温度、pH、pe 等}

## 关键结果
{3-5 条最重要的数值发现，每条一行}

## 图表说明

### charts/{filename1}.png
**类型**: {si_bars / si_sweep / selected_output_sweep / multi_panel}
**内容**: {一句话描述这张图表达什么}
**X 轴**: {变量名 + 单位/范围}
**Y 轴**: {变量名 + 单位}
{如有多个线条/颜色}: **线条**: {图例说明}
**解读**: {2-4 句话分析图中趋势、拐点、异常值。解释拐点的地球化学意义。SI 图中标出 SI=0 交叉点的物理含义。}

### charts/{filename2}.png
...
```

RULES for README.md:
- Write in Chinese (zh-CN)
- "关键结果" section: extract the most important numbers from results.json (final pH, SI values, breakthrough concentrations, etc.)
- "解读" section: explain trends and inflection points in geochemical terms — WHY does the curve look this way?
- For SI sweep charts: note where SI crosses 0, what that means for precipitation/dissolution
- For titration curves: identify buffer plateaus and what chemical reactions cause them
- Do NOT just describe what the axes say — explain the geochemical story the chart tells
- Keep each chart section self-contained so the user can read just one and understand it
```

### 收集结果

1. 等待所有子任务完成并收集结果。
2. 检查每个阶段的真实文件、返回值和错误信息。
3. 不创建或清理宿主未提供的团队资源；只清理本次任务产生的临时文件。

### 工作区目录结构

每次运行创建独立目录：
```
workbench/workspace_workbench/
├── <run-id>/
│   ├── meta.json                 # Workbench configuration and status
│   ├── events.log                # Workbench event stream
│   ├── input.pqi                # 输入文件
│   ├── output.qpo               # PHREEQC 原始输出
│   ├── selected_output.txt      # SELECTED_OUTPUT 数据
│   ├── results.json             # 解析后的结构化数据（机器中间格式）
│   ├── README.md                # 人类可读：模拟条件 + 关键结果 + 每张图解读
│   └── charts/
│       ├── ph_titration.png     # 使用描述性文件名
│       └── si_evolution.png
```

## Phase 3: 结果呈现

所有 agent 完成后，汇总结果呈现给用户。

### 终端摘要格式

```
═══ PHREEQC 模拟结果 ═══
模拟类型: Speciation
参数: pH=7.0, T=25°C

── 饱和指数 ──
Calcite:     0.52  (饱和)
Dolomite:    1.23  (过饱和)
Quartz:     -0.31  (未饱和)

── 主要组分 ──
Ca²⁺:    1.23e-3 mol/kgw
Mg²⁺:    5.67e-4 mol/kgw

── 输出文件 ──
📋 workbench/workspace_workbench/<run-id>/README.md    ← 推荐首先查看：含图表解读
📄 workbench/workspace_workbench/<run-id>/results.json
📊 workbench/workspace_workbench/<run-id>/charts/
```

### 输出文件
告诉用户数据文件和图表文件的路径。**重点推荐 README.md** — 这是回看时理解模拟内容和图表含义的最佳入口。

## 脚本路径参考

公开运行库位于项目根目录的相对路径：
```
phreeqc_auto/generate_input.py
phreeqc_auto/run_phreeqc.py
phreeqc_auto/parse_output.py
phreeqc_auto/visualize.py
```

从项目根目录运行时直接 import：
```python
from phreeqc_auto.generate_input import generate_single_simulation
from phreeqc_auto.run_phreeqc import run_simulation
```

## 参考文件

- **`references/phreeqc-examples.md`** — PHREEQC 输入文件模板（ex1-ex22 示例摘要）
- **`references/coordinator-template.py`** — coordinator 脚本模板（四步框架 + cwd 最佳实践）
- **`references/coordinator-examples.md`** — 完整运行示例（海水 speciation + pH 扫描），含参数、输出结构、关键结果
- **`references/pb_speciation_example.md`** — 考题 1.1: Pb 形态分布完整示例 + 风险分析
- **`references/calcite_si_example.md`** — 考题 1.2: 方解石饱和指数 + pH 敏感性分析
- **`references/seawater_mixing_example.md`** — 考题 1.3: 海水 + 纯水混合 + MIX 用法
- **`references/cd_adsorption_edge_example.md`** — 考题 2.1: Cd 吸附曲线 + 表面络合 + pH 扫描
- **`references/amd_neutralization_example.md`** — 考题 2.2: AMD 石灰石中和 + 沉淀序列 + pH 缓冲区间
- **`references/cation_exchange_example.md`** — 考题 2.3: 海水入侵阳离子交换 + Na⁺/Ca²⁺ 竞争 + 交换组成演化
- **`references/pyrite_kinetics_example.md`** — 考题 3.1: 黄铁矿氧化动力学 + KINETICS/RATES + BASIC 速率方程 + 二次矿物沉淀
- **`references/arsenic_transport_example.md`** — 考题 3.2: 一维反应溶质运移 + TRANSPORT + As 自定义主物种 + 突破曲线
- **`references/extreme_co2_injection_example.md`** — 考题 3.3: 超临界 CO₂ 注入 + GAS_PHASE + RATES 高速率方程 + 孔隙度估算
- **`references/goethite_birnessite_surface_params.md`** — Goethite/Birnessite 文献参数汇总
- **`references/cd_music_modeling_guide.md`** — CD-MUSIC 模型 PHREEQC 实现指南 (2026-06-04 新增)：语法速查、常见错误、位点容量约束、Donnan vs TP 模型差异、文献复现标准流程

## 生成器 API

`generate_single_simulation(params)` 支持以下参数结构：

### 单溶液模拟（默认）
```python
params = {
    "solution": {"id": 1, "units": "ppm", "pH": 8.22, "pe": 8.451, ...},
    "selected_output": {...},
}
```

### 多溶液 + MIX 模拟
```python
params = {
    "solutions": [
        {"id": 1, "units": "ppm", "pH": 8.22, "pe": 8.451, ...},
        {"id": 2, "units": "mol/kgw", "pH": 7.0, "pe": 4.0, ...},
    ],
    "mix": {"id": 1, "solutions": {1: 0.5, 2: 0.5}},
    "selected_output": {...},
}
```

### 一维传输模拟 (TRANSPORT)

```python
params = {
    # SOLUTION 0 = inlet boundary condition
    "solutions": [
        {"id": 0, "units": "ppm", "pH": 7.0, "pe": 12.0,
         "components": {"As": 1.0}},
    ],
    # Auto-generates SOLUTION 1..20 from this template
    "initial_cell_solution": {
        "units": "mol/kgw", "pH": 7.0, "pe": 12.0,
    },
    "transport": {
        "cells": 20,
        "length": 1.0,
        "shifts": 100,
        "time_step": 0.05,
        "time_units": "day",
        "flow_direction": "forward",
        "dispersivity": 0.01,
        "punch_cells": [20],      # outlet cell breakthrough
        "punch_frequency": 1,      # every shift
    },
    "selected_output": {
        "step": True,              # auto-enabled for transport
        "totals": ["As"],
        "pH": True,
    },
}
```

**关键规则:**
- `solutions` 中 `id=0` 为入口边界条件，必须定义
- `initial_cell_solution` 为柱体孔隙溶液模板，自动生成 `SOLUTION 1..N`
- `transport.cells` 自动决定 `SOLUTION 1..N` 数量
- `selected_output.step` 默认 `True`（传输模拟中每步追踪浓度变化）
- `punch_cells` 指定输出哪些单元的突破曲线数据

**典型突破曲线绘图:**
```python
from phreeqc_auto.visualize import plot_breakthrough_curve
bt = plot_breakthrough_curve(
    selected_output,        # dict from parse_selected_output
    time_column="step",     # X 轴
    conc_column="As",       # Y 轴 (单列) 或 conc_columns=["As", "Fe"]
    title="As Breakthrough Curve",
    xlabel="Time (days)",
    ylabel="Total As (mol/kgw)",
    filepath="charts/breakthrough_curve.png",
)
```

### 气体平衡模拟 (GAS_PHASE)

用于气相平衡或高压气体注入 (如 CO₂ 地质封存):

```python
params = {
    "solution": {"id": 1, "units": "mol/kgw", "temp": 100.0,
                 "pH": 7.5, "pe": -4.0,
                 "components": {"Ca": 0.01, "C(4)": 0.01, ...}},
    "gas_phase": {
        "block_id": 1,
        "fixed_pressure": True,          # 恒压模式
        "pressure": 200.0,               # 200 atm
        "components": {"CO2(g)": 0.0},   # 0 = 无穷供应
    },
    "equilibrium_phases": {"Calcite": (0.0, 10.0)},
    "kinetics": {
        "reactants": [{
            "name": "K-feldspar",
            "formula": "KAlSi3O8",
            "m": 3.0, "m0": 3.0,
            "parms": [0.2],              # m2/g 比表面积
            "steps": [315576000],        # 10 years in seconds
            "steps_n": 20,
            "cvode": True,               # 刚性积分器
        }],
    },
    "rates": [{
        "name": "K-feldspar",
        "code": [
            "rem Palandri & Kharaka (2004)",
            "k_neut_25 = 10^(-12.41)",
            "f_temp = exp(Ea/R * (1/T0 - 1/T))",
            "rem SR() must be used inline only (BASIC parser quirk)",
            "rate = k * area * (1 - SR(\"K-feldspar\"))",
            "moles = rate * TIME",
            "SAVE moles",
        ],
    }],
    "selected_output": {
        "step": True,
        "totals": ["Ca", "K", "Al", "Si", "C"],
        "si": ["Calcite", "K-feldspar", "Kaolinite"],
        "equilibrium_phases": ["Calcite"],
    },
}
```

**关键规则:**
- `GAS_PHASE` 定义气相组成和分压; `fixed_pressure=True` 时气相与外源无限交换
- CO₂(g) 量设为 0 时在固定压力模式下表示无穷供应源
- `KINETICS` 中 `steps` 使用总秒数 + `steps_n` 定义等分步
- 孔隙度需要在后处理中根据矿物摩尔变化 × 摩尔体积计算: `phi = phi_0 - Σ(Δn × V_m) / V_bulk`
- **SR() 不能作为赋值语句唯一 RHS** — 使用内联: `moles = rate * (1 - SR("phase"))`

**典型矿物摩尔体积:**
| 矿物 | 摩尔体积 (cm³/mol) |
|------|--------------------|
| Calcite | 36.93 |
| K-feldspar | 108.87 |
| Kaolinite | 99.52 |
| Quartz | 22.69 |

### 输出解析: `last=True` 参数
多段输出（多溶液 + MIX）中，提取函数默认返回第一次出现的数据。
需要最终态数据时传入 `last=True`：
```python
si = extract_saturation_indices(otxt, last=True)
el = extract_element_molalities(otxt, last=True)
sp = extract_species_distribution(otxt, last=True)
is_ = extract_ionic_strength(otxt)  # 默认 last=True
```

## 已知问题

### Windows 中文终端 Unicode 编码
**症状**: coordinator 脚本运行时 `UnicodeEncodeError: 'gbk' codec can't encode character`
**原因**: Windows 中文版控制台默认 CP936(GBK)，无法输出 BMP 外 Unicode（✓📄📊等）
**解决**: 运行脚本时设置 `PYTHONIOENCODING=utf-8`，或使用 ASCII 安全字符 `[OK]` `[FAIL]` `[JSON]` `[CHART]`

### Windows .lnk 指向目录
**症状**: `find_phreeqc_exe()` 找不到 PHREEQC 可执行文件
**原因**: `.lnk` 快捷方式目标可能是目录（如 `phreeqc-3.8.6-17100-x64`）而非直接指向 .exe
**解决**: `_resolve_lnk()` 已支持目录递归搜索（`bin/Release/phreeqc.exe` → `bin/phreeqc.exe` → `phreeqc.exe`）

### SELECTED_OUTPUT 文件未写入预期位置
**症状**: `selected_output.txt` 或 `step_*.txt` 未生成
**原因**: PHREEQC 子进程 CWD 未设置，SELECTED_OUTPUT 的相对路径解析到意外位置
**解决**: 调用 `run_simulation()` 时传入 `cwd=WORKSPACE`

### 多溶液模拟中 SELECTED_OUTPUT 含多行数据
**症状**: MIX 模拟中 `selected_output.txt` 含多行（初始溶液 + 反应态），取 `data[0]` 得到错误数据
**原因**: PHREEQC 在单 END 块中对每个初始溶液 + 反应步都输出一行
**解决**: 使用 `data[-1]` 取最后一行（最终反应态），或按 `state` 列过滤 (`react` = 反应步)

### 输出解析函数只取首段数据
**症状**: MIX 等多段输出中 `extract_saturation_indices()` 返回首段（初始溶液）而非末段（混合液）
**原因**: 所有提取函数默认从头扫描，找到第一个匹配段即返回
**解决**: 传入 `last=True` 获取最终态数据。单溶液模拟中 first = last，无需此参数

## 局限与注意事项

1. **PHREEQC 可执行文件**: 必须可通过 PATH 或 `PHREEQC_EXE` 环境变量访问
2. **数据库**: 可通过 `PHREEQC_DATABASE` 环境变量或项目 `database/` 目录访问
3. **Windows .lnk**: `run_phreeqc.py` 支持解析 .lnk 快捷方式
4. **计算时间**: 复杂模拟（传输、动力学）可能超时，默认 timeout 300 秒
5. **收敛失败**: 某些输入组合导致 PHREEQC 收敛失败，需提示用户调整参数
6. **matplotlib 后端**: 使用 Agg 后端（无显示器需求），仅输出文件

### RATES BASIC 变量名冲突
**症状**: `ERROR: Illegal command in line: ... in BASIC line` 当使用 `m = M` 或 `m0 = M0` 等赋值
**原因**: PHREEQC BASIC 大小写不敏感，单字母变量 `m` 与系统变量 `M` (current moles) 冲突
**解决**: 使用区分度高的变量名 (如 `cur_mol`)，或通过 `parm(N)` 传递值
**通用规则**: 变量名避免使用单字母 `m`，使用 `cur_mol`、`moles_init`、`delta` 等

### RATES 中局部变量不持久化
**症状**: `m_init = M` 在第一次调用正确，后续调用取当前值而非初始值
**原因**: RATES 中所有局部变量在每次调用时重置
**解决**: 需要持久化的值通过 KINETICS `-parms` 传递 (如 `parm(5)=0.5` 代表初始摩尔数)

### SELECTED_OUTPUT 列名约定
**结果**: `-totals Fe` 生成列名 `Fe` (`-si Pyrite` 生成 `si_Pyrite`)
**注意**: 使用 `-totals` 时列名不含 `tot_` 前缀，与 `-si` 的 `si_` 前缀不同

### 数据库不含特定元素 (如 As in phreeqc.dat)
**症状**: `WARNING: Could not find element in database, As. Concentration is set to zero.`
**原因**: phreeqc.dat (源自 PHREEQE) 仅包含常见元素 (Ca, Mg, Na, K, Fe, Mn, Al, Si, Cl, C, S, N, P, F, Br, Li, Zn, Cd, Pb, Cu)，不含 As, Hg, Se 等类金属/重金属
**解决**: 
1. 在 input 文件中手动添加 `SOLUTION_MASTER_SPECIES` / `SOLUTION_SPECIES` (保守示踪用)
2. 使用 `llnl.dat` (含完整 As 热力学) 或 `minteq.dat` 替代 phreeqc.dat
3. 确认目标元素在不同数据库中的存在性后选择合适数据库

### RATES BASIC 中 `SR()` 不能单独赋给变量
**症状**: `ERROR: Illegal command in line: ... in BASIC line ... sr = SR("K-feldspar")`
**原因**: PHREEQC BASIC 解析器的一个边界 bug — `SR(phase)` 函数不能作为赋值语句的唯一右侧表达式 (如 `sr = SR("K-feldspar")`)。但 `SR()` 在更大的表达式中内联使用时完全正常。
**解决**: 使用内联形式 `moles = rate * (1 - SR("phase")) * TIME` 而非 `sr = SR("phase")` 再使用 `sr`。`ACT()` 和其他 BASIC 函数不受此限制。

### KINETICS `-steps` 是块级别参数 (非 per-reactant)
**症状**: `ERROR: To define equal time increments, only one total time should be defined.` 当 KINETICS 中有多个反应物时
**原因**: PHREEQC 的 KINETICS 数据块中 `-steps` 是块级别关键词, 只能定义一次。`generate_kinetics_block()` 会将首个反应物的 `steps` 参数提至块级别, 其余反应物的 `steps` 被忽略。
**解决**: 对于多反应物 KINETICS, 只需在第一个反应物中定义 `steps` + `steps_n`, 或在所有反应物中定义相同的值。使用 `-step_divide` 控制子步积分精度。

### 单矿物 RATES 趋于冻结 (需要产物矿物耦合)
**症状**: K-feldspar 仅在初始几大步溶解, 然后 SI → 0, (1-SR) → 0, 速率趋停。即使大量 CO₂ 存在, 溶解量也很小 (< 0.01 mol)。
**原因**: 溶液中的 Al 和 Si 积累使 K-feldspar 接近饱和平衡。单矿物动力学缺少产物矿物析出通道。
**解决**: 添加 Kaolinite (或其他次生矿物) 的 RATES 沉淀方程 → Al 和 Si 被消耗 → K-feldspar SI 保持 < 0 → 溶解持续进行。净反应: `Kspar + H⁺ → ½Kaolinite + K⁺ + 2SiO₂`, 摩尔体积差 108.87 vs 49.76 cm³/mol 使净增孔显著。
