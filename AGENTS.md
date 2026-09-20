# AGENTS.md

本文件为在本项目中工作的智能体终端（Claude Code、Codex 等）提供指导。

## 项目概述

PHREEQC 是美国地质调查局（USGS）的地球化学模拟程序，用于计算物种组成、批量反应、一维迁移和反演地球化学计算。版本 3.8.6-17100。

本项目是用于自动化 PHREEQC 模拟的封装项目。主 PHREEQC 可执行文件通过快捷方式 `phreeqc-3.8.6-17100-x64 - 快捷方式.lnk` 访问。

## 构建命令

### Windows (Visual Studio)
- 解决方案：`phreeqc.sln`（Visual Studio C++ 项目 — `phreeqc.vcproj`）
- 构建：在 VS 中选择 Release/Debug/ClrRelease 并构建
- CLR 构建需要注册 ZedGraph.dll 以支持图表功能

### Linux (configure/make)
./configure
make
make check
make install

### 运行 PHREEQC
phreeqc input [output [database [screen_output]]]
使用 `PHREEQC_DATABASE` 环境变量或 `phreeqc.dat` 作为默认数据库。

### 本机安装路径（需根据本地环境修改）
- **PHREEQC.exe**: `C:\Program Files\USGS\phreeqc-3.8.6-17100-x64\bin\Release\phreeqc.exe`
- **数据库目录**: `C:\Program Files\USGS\phreeqc-3.8.6-17100-x64\database\`
- **环境变量**（建议设置）:
  ```
  PHREEQC_EXE="/path/to/phreeqc.exe"
  PHREEQC_DATABASE="/path/to/phreeqc.dat"
  ```
- **Windows 编码**: 中文终端运行 Python 脚本时设置 `PYTHONIOENCODING=utf-8` 避免 GBK 错误

## 测试命令

Windows 批处理测试运行器：
test\test.bat [start_test [stop_test [nochart_flag]]]
- 默认运行示例测试 1–22
- 单个测试：`test\test.bat 5 5`
- 测试使用 `examples/` 中的输入文件（ex1 到 ex22）

Linux：`make check`

## 核心架构

### 入口点
- `class_main.cpp` — `main()` 函数，实例化 `Phreeqc` 类

### 核心引擎
- `Phreeqc.h/cpp` — 主模拟类，所有地球化学计算的中央协调器

### 主要模块

| 模块 | 文件 | 用途 |
|------|------|------|
| 物种组成/模型 | `model.cpp` | 核心化学平衡计算 |
| 迁移 | `transport.cpp` | 一维溶质迁移（平流、扩散） |
| 反演建模 | `inverse.cpp` | 反演地球化学计算 |
| 动力学 | `kinetics.cpp`、`integrate.cpp`、`cvode.cpp` | 动力学反应和 CVODE 常微分方程积分 |
| 输入解析 | `parse.cpp`、`read.cpp`、`readtr.cpp`、`input.cpp` | 基于关键字的输入文件解析器 |
| 输出 | `print.cpp`、`SelectedOutput.cpp`、`UserPunch.cpp` | 表格和格式化输出 |
| 物种预计算 | `prep.cpp` | 化学物种准备和平衡 |
| BASIC 解释器 | `basicsubs.cpp`、`PBasic.cpp/h` | 内嵌 BASIC 用于用户自定义函数 |
| 活度模型 | `pitzer.cpp`、`sit.cpp`、`dw.cpp` | Pitzer、SIT 和 Debye-Hückel 活度模型 |

### 数据模型类（均在 `src/` 中）
每个地球化学组件都有 C++ 类对（`.cxx`/`.h`）：
- `Solution.h/cxx`、`ISolution.h/cxx`、`ISolutionComp.h/cxx` — 水溶液
- `Exchange.h/cxx`、`ExchComp.h/cxx` — 离子交换
- `Surface.h/cxx`、`SurfaceComp.h/cxx`、`SurfaceCharge.h/cxx` — 表面络合
- `GasPhase.h/cxx`、`GasComp.h/cxx` — 气相平衡
- `SSassemblage.h/cxx`、`SS.h/cxx`、`SScomp.h/cxx` — 固溶体
- `PPassemblage.h/cxx`、`PPassemblageComp.h/cxx` — 纯相组合
- `cxxKinetics.h/cxx` — 动力学反应物
- `cxxMix.h/cxx` — 溶液混合
- `Use.h/cpp` — 反应物使用跟踪
- `Pressure.h/cxx`、`Temperature.h/cxx` — 压力/温度条件

### 通用工具类
- `common/PHRQ_base.h/cxx` — 带有工具方法的基类
- `common/PHRQ_io.h/cpp` — I/O 抽象（文件、字符串、标准输出）
- `common/Parser.h/cxx` — 输入文本解析器
- `common/Utils.h/cxx` — 字符串/数值工具

### 数据库文件
- `database/` 包含：`phreeqc.dat`、`pitzer.dat`、`sit.dat`、`iso.dat`、`llnl.dat`、`minteq.dat`、`wateq4f.dat` 等

## PHREEQC 输入文件格式约定
来源: USGS TM 6-A43 (parkhurst.appelo.2013 — 即 `phreeqc-v3程序说明.pdf`)

### 通用规则
- **关键字数据块 (keyword data blocks)**: 每个数据块以关键字开头，后续行放数据
- **自由格式**: 空格/制表符分隔（`SOLUTION_SPREAD` 例外，仅制表符）
- **大小写不敏感**（化学式除外）
- **顺序无关**: 关键字数据块在同一模拟中可以任意顺序排列
- **注释**: `#` 开头，整行注释不回显到输出文件
- **行分隔**: `;` — 同一物理行放多个逻辑行；`\` — 行尾反斜杠连接两物理行
- **重复计数**: `*` — 如 `4*1.0` 等于四个 1.0
- **整数范围**: `-` — 如 `SOLUTION 2-5`，`-print_cells 1-20`

### 标识符 (identifier) 规则
- 可完整拼写，或加 `-` 前缀后缩写到唯一识别
- 带 `-` 前缀形式始终可接受且推荐
- 示例: `-temperature` 可缩写为 `-t`（在 SOLUTION 数据块中）

### 化学式约定
- 缔合反应: 物种在等号后第一位
- 溶解反应: 矿物在等号左边第一位
- 水合水用 `:` 替代 `·`（如 CaSO4:2H2O）
- 元素名用 `[13C]` 方括号形式表示同位素
- 价态用括号: `S(6)`=硫酸盐, `S(-2)`=硫化物
- 电荷: `Al+3` 或 `Al+++`（注意 `Al3+` 是 3 个 Al 原子+1 电荷）

### log K 温度依赖性
- Van't Hoff: `log_k` + `delta_h`（单位 kJ/mol，可设为 kcal/mol）
- 分析表达式: `-analytical_expression A1 A2 A3 A4 A5 A6`
  - log K = A1 + A2·T + A3/T + A4·log10(T) + A5/T² + A6·T²

### 所有输入关键字
| 关键字 | 用途 |
|--------|------|
| **SOLUTION** | 定义水溶液组分 |
| **SOLUTION_SPREAD** | 制表符分隔批量定义多个溶液 |
| **SOLUTION_MASTER_SPECIES** | 定义元素及主物种 |
| **SOLUTION_SPECIES** | 定义水溶液物种反应和热力学数据 |
| **EQUILIBRIUM_PHASES** | 定义矿物/气体组合（同义词 PURE_PHASES） |
| **EXCHANGE** | 定义离子交换组合 |
| **EXCHANGE_MASTER_SPECIES** | 定义交换位点和主物种 |
| **EXCHANGE_SPECIES** | 定义交换反应和热力学数据 |
| **SURFACE** | 定义表面络合组合 |
| **SURFACE_MASTER_SPECIES** | 定义表面位点和主物种 |
| **SURFACE_SPECIES** | 定义表面反应和热力学数据 |
| **GAS_PHASE** | 定义气相组分 |
| **SOLID_SOLUTIONS** | 定义固溶体组合 |
| **REACTION** | 定义不可逆反应 |
| **REACTION_PRESSURE** | 定义批反应压力 |
| **REACTION_TEMPERATURE** | 定义批反应温度 |
| **KINETICS** | 定义动力学反应和参数 |
| **RATES** | 用 BASIC 定义速率方程 |
| **MIX** | 定义溶液混合比例 |
| **INVERSE_MODELING** | 反演地球化学建模 |
| **PHASES** | 定义矿物/气体的溶解反应和热力学 |
| **ADVECTION** | 平流反应性传输（无弥散） |
| **TRANSPORT** | 平流-弥散反应性传输（支持双重孔隙度） |
| **PRINT** | 选择输出文件要打印的数据块 |
| **SELECTED_OUTPUT** | 打印选定数据到用户定义文件 |
| **USER_GRAPH** | 用户定义 X-Y 图 |
| **USER_PRINT** | 用户定义输出打印 |
| **USER_PUNCH** | 用户定义选定输出打印 |
| **TITLE** | 输出标题 |
| **END** | 模拟结束标记 |
| **COPY** / **DELETE** / **DUMP** / **SAVE** / **USE** | 反应物管理操作 |
| **RUN_CELLS** | 对指定编号单元运行反应模拟 |
| **DATABASE** | 指定数据库文件 |
| **KNOBS** | 数值方法和调试参数 |
| **INCLUDE$** | 插入文件到输入/数据库 |
| **INCREMENTAL_REACTIONS** | 定义反应增量方式 |
| **CALCULATE_VALUES** | 定义 BASIC 函数 |
| **NAMED_EXPRESSIONS** | 命名分析表达式或分馏因子 |
| **PITZER** / **SIT** / **LLNL_AQUEOUS_MODEL_PARAMETERS** | 活度模型参数 |
| **ISOTOPES** / **ISOTOPE_ALPHAS** / **ISOTOPE_RATIOS** | 同位素定义 |

### 数据库文件 (`database/`)
1. **phreeqc.dat** — 默认数据库（源自 PHREEQE）
2. **Amm.dat** — 氨解耦版
3. **wateq4f.dat** — 源自 WATEQ4F
4. **llnl.dat** — 源自 LLNL（EQ3/6）
5. **minteq.dat** / **minteq.v4.dat** — 源自 MINTEQA2
6. **pitzer.dat** — Pitzer 活度模型
7. **sit.dat** — SIT 活度模型
8. **iso.dat** — 同位素计算

### 计算类型
1. **初始溶液计算** (Speciation) — 仅 SOLUTION，计算物种分布和饱和指数
2. **批反应** (Batch-Reaction) — 溶液 + 反应物，计算系统平衡
3. **平流传输** (ADVECTION) — 一维柱平流 + 化学反应
4. **平流-弥散传输** (TRANSPORT) — 一维平流 + 弥散 + 反应
5. **反演建模** (INVERSE_MODELING) — 摩尔平衡计算

### 输入文件结构示例
```
TITLE Example 1.--Add uranium and speciate seawater.
SOLUTION 1 SEAWATER
    units ppm
    pH 8.22
    pe 8.451
    temp 25.0
    density 1.023
    Ca 412.3
    Mg 1291.8
    Na 10768.0
    Cl 19353.0
    Alkalinity 141.682 as HCO3
    S(6) 2712.0
    ...
EQUILIBRIUM_PHASES 1
    Calcite 0.0 10.0
    ...
END
```

### 官方示例 (ex1-ex22)
| 示例 | 内容 |
|------|------|
| ex1 | 海水物种分布（含铀） |
| ex2 | 与纯相平衡（石膏/硬石膏温度依赖性） |
| ex3 | 溶液混合 |
| ex4 | 蒸发和均匀氧化还原反应 |
| ex5 | 不可逆反应 |
| ex6 | 反应路径计算（K-长石溶解） |
| ex7 | 气相计算 |
| ex8 | 表面络合 |
| ex9 | Fe²⁺的动力学氧化 |
| ex10 | 文石-菱锶矿固溶体 |
| ex11 | 传输和阳离子交换 |
| ex12 | 热和溶质的平流-扩散通量 |
| ex13 | 双重孔隙度传输 |
| ex14 | 传输 + 平衡相/交换/表面 |
| ex15 | 动力学生物降解 + 细胞生长 + 吸附 |
| ex16-18 | 反演建模（Sierra泉水、蒸发、Madison含水层） |
| ex19 | Cd²⁺吸附等温线 |
| ex20 | 方解石同位素分布 |
| ex21 | 径向扩散池中的同位素扩散 |
| ex22 | 高压CO₂溶解度 |

## 自动化 Skill

项目包含一个 Claude Code Skill (`phreeqc-auto`) 用于全流程自动化模拟。

### 使用方法
触发方式：在 Claude Code 中直接输入 PHREEQC 模拟相关的自然语言指令，如：
- "模拟海水在 pH 7-9 间的方解石饱和指数变化"
- "做方解石溶解的批反应模拟，温度 25-60°C"

Skill 会引导你确认参数 → 自动创建 agent 团队 → 生成输入文件 → 运行模拟 → 解析结果 → 生成图表。

### Skill 文件位置
```
.claude/skills/phreeqc-auto/
├── SKILL.md                          # 主 skill 定义（加载入口）
├── scripts/
│   ├── generate_input.py             # PHREEQC 输入文件生成
│   ├── run_phreeqc.py                # PHREEQC 运行器
│   ├── parse_output.py               # 输出解析器
│   └── visualize.py                  # 可视化工具
└── references/
    ├── phreeqc-examples.md           # 输入模板参考（ex1-ex22 示例摘要）
    ├── pb_speciation_example.md      # 考题 1.1: Pb 形态分布完整示例 + 风险分析
    ├── calcite_si_example.md         # 考题 1.2: 方解石饱和指数 + pH 敏感性分析
    ├── coordinator_template.py       # 协调脚本模板（四步框架: 生成→运行→解析→可视化）
    └── coordinator-examples.md       # 完整运行示例（海水 speciation + pH 扫描）
```

### 方案 B（未来参考）：独立 Python 库
当需要脱离 Claude Code 独立使用自动化功能时，可重构为独立的 Python 包：

```
phreeqc_auto/
├── __init__.py
├── generate_input.py
├── runner.py
├── parser.py
└── visualize.py
```

然后在 Claude Code 中通过 Bash 工具调用 Python 脚本，而非使用 TeamCreate 编排 agent。

### 设计文档
详细设计见 `docs-developer/superpowers/specs/2026-05-10-phreeqc-auto-skill-design.md`
实现计划见 `docs-developer/superpowers/plans/2026-05-10-phreeqc-auto-skill-plan.md`

> `docs-developer/` 是本机开发文档目录，已被 `.gitignore` 忽略，不会随仓库分发；
> 面向用户的中文文档放在受版本控制的 `docs/` 下。

## Skill 考题 (improve-task)

`docs-developer/improve-task.md` 包含 9 道用于评估和迭代 phreeqc-auto skill 能力的考题，分三个级别。

### 完成状态

| 级别 | 考题 | 内容 | 状态 | 参考文件 |
|------|------|------|------|---------|
| 🟢 L1 | 1.1 | 铅形态分布 (Pb speciation) | ✅ 已完成 | `references/pb_speciation_example.md` |
| 🟢 L1 | 1.2 | 矿物饱和指数 (Calcite SI) | ✅ 已完成 | `references/calcite_si_example.md` |
| 🟢 L1 | 1.3 | 简单溶液混合 (Seawater + pure water) | ✅ 已完成 | `references/seawater_mixing_example.md` |
| 🟡 L2 | 2.1 | 重金属表面吸附 (Cd 吸附曲线) | ✅ 已完成 | `references/cd_adsorption_edge_example.md` |
| 🟡 L2 | 2.2 | 酸碱中和与沉淀滴定 (AMD + 石灰石) | ✅ 已完成 | `references/amd_neutralization_example.md` |
| 🟡 L2 | 2.3 | 阳离子交换 (海水入侵) | ✅ 已完成 | `references/cation_exchange_example.md` |
| 🔴 L3 | 3.1 | 矿物溶解动力学 (黄铁矿氧化) | ✅ 已完成 | `references/pyrite_kinetics_example.md` |
| 🔴 L3 | 3.2 | 一维反应溶质运移 (As 穿透曲线) | ✅ 已完成 | `references/arsenic_transport_example.md` |
| 🔴 L3 | 3.3 | 极端环境多相演化 (超临界 CO₂ 注入) | ✅ 已完成 | `references/extreme_co2_injection_example.md` |

### 已完成考题记录

#### ✅ 考题 1.1 — Pb 形态分布 (2026-05-11)

**输入**: pH=6.0, 10 mmol/L NaCl, 1 mg/L Pb, pe=12 O2(g) -0.68

**模拟方式**: 独立 coordinator Python 脚本，调用 skill 的 `generate_input.py` / `run_phreeqc.py` / `parse_output.py` / `visualize.py` 四步工作流，全程自动化无需人工干预。

**关键发现**:
- Pb²⁺ 主导 (64.6%)，PbCl⁺ 次之 (17.0%)，其余羟基/氯络合物占比 <1%
- 所有 Pb 矿物均未饱和 (SI < 0)，无沉淀风险
- pe 输入 12，经 O₂(g) -0.68 平衡计算后实际 pe=14.63（Nernst 方程决定）
- 碱度=0 导致碳酸铅络合物全部为 0 — 这是最大不确定性来源
- phreeqc.dat 中 PbO, Cerussite, Anglesite, Galena 均无热力学数据（SI=-999.999）

**暴露的 skill 薄弱点**:
1. `generate_solution_block()` 不支持 `pe <value> <couple>` 完整语法 → 需后处理替换
2. `parse_selected_output()` 遇到非数值列（如 "i_soln"）整行丢弃 → 需支持混合类型
3. 无内置 pe 语法说明文档 → 已通过参考文档补全
4. 无数据库矿物存在性预检机制 → 需用户手动确认

#### ✅ 考题 1.2 — 方解石饱和指数 (2026-05-11)

**输入**: Ca²⁺ = 80 mg/L, 碱度 = 200 mg/L as CaCO₃, pH = 7.2

**模拟方式**: 独立 coordinator Python 脚本，四步工作流 + pH 扫描 (6.0-8.5, 11步)

**关键发现**:
- Calcite SI at pH 7.2 = **+0.07** — 水样恰好处于方解石溶解平衡临界点
- pH 敏感性极强: SI 变化率 0.25/0.25 pH，SI=0 交叉点 pH ≈ 7.1
- Ca²⁺ (4.0 meq/L) 与碱度 (4.0 meq/L) 电荷完美平衡，pct_err = 0.05%
- pH 6.0 时 SI = -1.13 (方解石溶解)，pH 8.5 时 SI = +1.31 (过饱和沉淀)
- 碳酸盐体系中 HCO₃⁻ 占主导 (87.8%)，CO₃²⁻ 仅 0.1%

**暴露的 skill 薄弱点 & 本次修复**:
1. `generate_solution_block()` 不支持 `as <unit>` 语法 → **已修复**: 类型签名改为 `dict[str, Any]`，字符串值按原样写入
2. `parse_selected_output()` 遇到非数值列整行丢弃 → **已修复**: 改用逐值尝试 float 转换，非数值保留为字符串

#### ✅ 考题 1.3 — 海水 + 纯水混合 (2026-05-11)

**输入**: 500mL 海水（标准组分）与 500mL 纯水混合

**模拟方式**: 独立 coordinator Python 脚本，调用 `generate_single_simulation()` 的 `solutions` + `mix` 新参数

**关键发现**:
- 离子强度精确减半: 0.6704 → 0.3378 mol/kgw (50.4%)
- pH 从 8.22 略微升高到 8.32 (+0.10) — 海水碱度缓冲体系导致
- 所有元素精确稀释 2 倍 (Ca, Mg, Na, Cl, K 稀释因子 0.5)
- 无新矿物沉淀风险，原有 Calcite / Dolomite / Aragonite 的 SI 下降但仍过饱和

**暴露的 skill 薄弱点 & 本次修复**:
1. `generate_input.py` 无 MIX 块支持 → **已修复**: 添加 `generate_mix_block()` + 扩展 `generate_single_simulation()` 支持 `solutions` list 和 `mix` dict
2. `parse_output.py` 提取函数只取首段 → **已修复**: `extract_saturation_indices()`、`extract_species_distribution()`、`extract_element_molalities()` 均添加 `last=True` 参数
3. `coordinator` 须取 SELECTED_OUTPUT 最后一行 → **已修复**: 多行数据中用 `data[-1]` 替代 `data[0]`

#### ✅ 考题 2.1 — 重金属表面吸附 Cd 吸附曲线 (2026-05-11)

**输入**: 0.1g 铁锰结核粉末 (Goethite 20% + Birnessite 20%), 25mL 溶液, Cd 100 μg/L, NaNO₃ 0.01 M, pH 3-9

**模拟方式**: 独立 coordinator Python 脚本，REACTION NaOH 滴定法产生 pH 扫描 (30 步)，全程自动化。

**关键发现**:
- 吸附边极陡: pH 3.6→5.2 内吸附率从 8% → 99%，半吸附 pH₅₀ ≈ 4.54
- Birnessite 绝对主导 (99.9%+): PZC=2.5 酸性表面在宽 pH 范围内带负电
- Goethite 贡献可忽略: PZC=9.0 碱性表面在中性以下带正电排斥 Cd²⁺
- pH > 5.5 时 >99.9% Cd 被吸附，全由 Birnessite 位点 (Mn_sOCd⁺ + Mn_wOCd⁺) 完成

**暴露的 skill 薄弱点 & 本次修复**:
1. `generate_input.py` 无 SURFACE 块支持 → **已修复**: 添加 `generate_surface_master_species_block()`, `generate_surface_species_block()`, `generate_surface_block()`, `generate_phases_block()`
2. `generate_solution_block()` 无 `-water` 非默认水量参数 → **已知问题**: 暂用手动 SOLUTION 构造
3. 无 pH 扫描最佳实践 → **已建立**: REACTION 滴定法优于 Fix_H+ 相法
4. PHREEQC 默认单位 mmol/kgw 被忽略 → coordinator 显式使用 `units mol/kgw`
5. 吸附率计算依赖 `-totals` 列漂移 → 改用质量平衡法 (sorbed/(sorbed+aq))

**新增参考文件**:
- `references/cd_adsorption_edge_example.md` — 考题 2.1 完整模拟记录
- `references/goethite_birnessite_surface_params.md` — Goethite/Birnessite 文献参数汇总

#### ✅ 考题 2.2 — 酸碱中和与沉淀滴定 (AMD + 石灰石) (2026-05-11)

**输入**: pH=2 硫酸 AMD, Fe(2)=500, Fe(3)=50, Al=200, Mn=50 (mg/L), S(6)=2600 mg/L, 逐步加 Calcite 到 pH=7

**模拟方式**: 独立 coordinator Python 脚本，REACTION Calcite 100 步 + EQUILIBRIUM_PHASES 多相沉淀 + 开放 CO₂ 系统。

**关键发现**:
- pH 7 达标需 0.0220 mol CaCO₃ (2.20 g / kg 水)，第 44/100 步
- 沉淀序列: Fe(OH)₃(a) @pH 3.42 → Gibbsite @pH 3.92 → Gypsum @pH 4.00 → Calcite @pH 7.70
- Fe²⁺ 全程不沉淀 (500 mg/L 溶解态): 开放 CO₂ 系统下 pe 随 pH 升高而骤降 (10 → -1.77)，Fe²⁺ 始终为热力学稳定形态 — 需主动曝气
- Al³⁺ 是最大酸缓冲源: 10.5 mmol CaCO₃ 消耗 (超过游离酸 8.0 mmol 和 Fe³⁺ 1.5 mmol)，每 mol Al³⁺ 沉淀释放 3 mol H⁺
- 石膏竞争效应: pH 4.0 起 Ca²⁺ 被 SO₄²⁻ 截获沉淀，间接增加中和剂需求

**本次 skill 修复**:
1. `generate_selected_output_block()` 添加 `step: bool` 和 `equilibrium_phases: list[str]` 参数 — **已修复**
2. d_Phase 列符号约定澄清: 0 mol 初始量时 d_Phase > 0 = 沉淀 (正 = 相量增加) — 已记录到参考文档
3. pH 缓冲区间自动识别需求已记录，待添加 `detect_buffer_regions()` 工具函数

**新增参考文件**:
- `references/amd_neutralization_example.md` — 考题 2.2 完整模拟记录

#### ✅ 考题 2.3 — 阳离子交换 (海水入侵) (2026-05-11)

**输入**: 淡水 (Ca-HCO₃ 型, Ca 80 mg/L, pH 7.2) + Ca-饱和粘土交换剂 (0.05 mol X 位点) + 逐步添加 NaCl (0-0.3 mol, 30 步) 模拟海水入侵

**模拟方式**: 独立 coordinator Python 脚本，REACTION NaCl 逐步添加法模拟渐进式海水入侵，四步工作流全程自动化。

**关键发现**:
- 淡水端 Ca²⁺ 浓度从 112.9 → 496.4 mg/L (+383.4 mg/L, +340%)，全由交换剂 Ca²⁺ 被 Na⁺ 置换释放
- Ca 质量平衡完美: 交换剂释放 383.5 mg = 溶液增加 383.4 mg (误差 0.1 mg, <0.03%)
- 交换组成: 初始 CaX₂ 76.0% → 最终 NaX 57.3% / CaX₂ 34.4%
- Na⁺ 虽选择性最低 (log_K=0.0)，但浓度优势 (最终 ~270× 初始) 克服选择性劣势
- 初始溶液中 Ca 实际为 112.9 mg/L (含交换剂 Ca-平衡时从交换剂获取的额外 Ca，高于输入的 80 mg/L)
- Mg²⁺ 同时被置换: MgX₂ 从 22.9% → 8.1%
- pH 稳定 (7.20→7.03)，无矿物沉淀风险 (Calcite SI 0.12, Gypsum -2.14, Halite -2.96)

**本次 skill 修复**:
1. `generate_input.py` 添加 `generate_exchange_master_species_block()`, `generate_exchange_species_block()`, `generate_exchange_block()` — **已修复**
2. `generate_exchange_block()` 支持两种模式: `-composition` 显式指定 / `-equilibrate with solution N` 溶液平衡 — **已修复**
3. `generate_single_simulation()` 支持 `exchange_master_species`, `exchange_species`, `exchange` 参数 — **已修复**
4. `parse_output.py` 添加 `extract_exchange_composition()` 解析交换组成 (species, moles, equivalents, eq_frac) — **已修复**
5. SELECTED_OUTPUT `step`/`equilibrium_phases` 参数传透修复 — **已修复**

**暴露的 skill 薄弱点**:
1. PHREEQC 不在 SELECTED_OUTPUT 中直接输出各步交换组成 → 需从标准输出文本多次解析 `Exchange composition` 段落 (性能较低)
2. 交换选择性 (Gaines-Thomas) 与浓度效应的竞争关系需地球化学背景知识来正确设计模拟
3. `-equilibrate with solution N` 时初始溶液实际组分可能与输入不同 (Ca 从交换剂获得了额外 Ca)

**新增参考文件**:
- `references/cation_exchange_example.md` — 考题 2.3 完整模拟记录
