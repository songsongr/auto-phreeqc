# PHREEQC Agent Skill Iteration Task (improve-task.md)

## 🎯 训练目标
核心目标：测试并持续迭代 Agent 将自然语言指令转化为结构化 PHREEQC 输入的能力，涵盖从基础水质平衡到复杂动力学模拟的多个层次。
通过设计具有挑战性的考题，评估 Agent 在参数识别、默认值处理、数据库选择和潜在错误排查等方面的表现。

---
##  归档要求
1. 训练完成后把训练的例子总结经验补充进skill的references里
2. 完成情况概化后同步进CLAUDE.md
3. workpalce中的例子文件夹命名规范，ex：考题1.3命名为task1_3_simple_mixing

---

## 完成状态

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

## 已完成考题记录

### ✅ 考题 1.1 — Pb 形态分布 (2026-05-11)

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

### ✅ 考题 1.2 — 方解石饱和指数 (2026-05-11)

**输入**: Ca²⁺ = 80 mg/L, 碱度 = 200 mg/L as CaCO₃, pH = 7.2

**模拟方式**: 独立 coordinator Python 脚本，四步工作流 + pH 扫描 (6.0-8.5, 11步)

**关键发现**:

- Calcite SI at pH 7.2 = **+0.07** — 水样恰好处于方解石溶解平衡临界点
- pH 敏感性极强: SI 变化率 0.25/0.25 pH，SI=0 交叉点 pH ≈ 7.1
- Ca²⁺ (4.0 meq/L) 与碱度 (4.0 meq/L) 电荷完美平衡，pct_err = 0.05%
- pH 6.0 时 SI = -1.13 (方解石溶解)，pH 8.5 时 SI = +1.31 (过饱和沉淀)
- 碳酸盐体系中 HCO₃⁻ 占主导 (87.8%)，CO₃²⁻ 仅 0.1%

**暴露的 skill 薄弱点与本次修复**:

1. `generate_solution_block()` 不支持 `as <unit>` 语法 → **已修复**: 类型签名改为 `dict[str, Any]`，字符串值按原样写入
2. `parse_selected_output()` 遇到非数值列整行丢弃 → **已修复**: 改用逐值尝试 float 转换，非数值保留为字符串

### ✅ 考题 1.3 — 海水 + 纯水混合 (2026-05-11)

**输入**: 500mL 海水（标准组分）与 500mL 纯水混合

**模拟方式**: 独立 coordinator Python 脚本，调用 `generate_single_simulation()` 的 `solutions` + `mix` 新参数

**关键发现**:

- 离子强度精确减半: 0.6704 → 0.3378 mol/kgw (50.4%)
- pH 从 8.22 略微升高到 8.32 (+0.10) — 海水碱度缓冲体系导致
- 所有元素精确稀释 2 倍 (Ca, Mg, Na, Cl, K 稀释因子 0.5)
- 无新矿物沉淀风险，原有 Calcite / Dolomite / Aragonite 的 SI 下降但仍过饱和

**暴露的 skill 薄弱点与本次修复**:

1. `generate_input.py` 无 MIX 块支持 → **已修复**: 添加 `generate_mix_block()` + 扩展 `generate_single_simulation()` 支持 `solutions` list 和 `mix` dict
2. `parse_output.py` 提取函数只取首段 → **已修复**: `extract_saturation_indices()`、`extract_species_distribution()`、`extract_element_molalities()` 均添加 `last=True` 参数
3. `coordinator` 须取 SELECTED_OUTPUT 最后一行 → **已修复**: 多行数据中用 `data[-1]` 替代 `data[0]`

### ✅ 考题 2.1 — 重金属表面吸附 Cd 吸附曲线 (2026-05-11)

**输入**: 0.1g 铁锰结核粉末 (Goethite 20% + Birnessite 20%), 25mL 溶液, Cd 100 μg/L, NaNO₃ 0.01 M, pH 3-9

**模拟方式**: 独立 coordinator Python 脚本，REACTION NaOH 滴定法产生 pH 扫描 (30 步)，全程自动化。

**关键发现**:

- 吸附边极陡: pH 3.6→5.2 内吸附率从 8% → 99%，半吸附 pH₅₀ ≈ 4.54
- Birnessite 绝对主导 (99.9%+): PZC=2.5 酸性表面在宽 pH 范围内带负电
- Goethite 贡献可忽略: PZC=9.0 碱性表面在中性以下带正电排斥 Cd²⁺
- pH > 5.5 时 >99.9% Cd 被吸附，全由 Birnessite 位点 (Mn_sOCd⁺ + Mn_wOCd⁺) 完成

**暴露的 skill 薄弱点与本次修复**:

1. `generate_input.py` 无 SURFACE 块支持 → **已修复**: 添加 `generate_surface_master_species_block()`, `generate_surface_species_block()`, `generate_surface_block()`, `generate_phases_block()`
2. `generate_solution_block()` 无 `-water` 非默认水量参数 → **已知问题**: 暂用手动 SOLUTION 构造
3. 无 pH 扫描最佳实践 → **已建立**: REACTION 滴定法优于 Fix_H+ 相法
4. PHREEQC 默认单位 mmol/kgw 被忽略 → coordinator 显式使用 `units mol/kgw`
5. 吸附率计算依赖 `-totals` 列漂移 → 改用质量平衡法 (sorbed/(sorbed+aq))

**新增参考文件**:

- `references/cd_adsorption_edge_example.md` — 考题 2.1 完整模拟记录
- `references/goethite_birnessite_surface_params.md` — Goethite/Birnessite 文献参数汇总

### ✅ 考题 2.2 — 酸碱中和与沉淀滴定 (AMD + 石灰石) (2026-05-11)

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

### ✅ 考题 2.3 — 阳离子交换 (海水入侵) (2026-05-11)

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

---

## 🟢 Level 1: 基础水质平衡与组分分布 (初级)

**考题 1.1：金属形态分布**
> **Input:** “分析一个 pH 为 6.0、含有 10 mmol/L 氯化钠和 1 mg/L 铅的水样中，铅的主要存在形态及其浓度。”
*考察重点*：溶液基本定义、默认参数识别、数据库对金属络合常数的影响。

**考题 1.2：矿物饱和指数**
> **Input:** “已知某地下水的钙离子浓度为 80 mg/L，总碱度为 200 mg/L (as CaCO3)，pH 为 7.2。请计算该水样对方解石的饱和指数（SI）。”
*考察重点*：碱度单位转换逻辑（as CaCO3）、pH 敏感性识别。

**考题 1.3：简单溶液混合**
> **Input:** “将 500mL 的海水（标准组分）与 500mL 的纯水混合，计算混合后的离子强度和 pH 变化。”
*考察重点*：基准溶液的预设、混合比例控制（`MIX`）、潜在沉淀的排查逻辑。

---

## 🟡 Level 2: 反应路径与表面络合 (中级)

**考题 2.1：重金属表面吸附**
> **Input:** “模拟在 pH 3 到 9 的范围内，0.1g 铁锰结核粉末对 25mL 溶液中 100 μg/L 镉（Cd）的吸附率曲线。”
*考察重点*：体积非默认值（1kg水）的缩放处理（`-water 0.025`）、吸附模型选择（多组分/单组分）、比表面积与位点密度的参数缺失识别。

**考题 2.2：酸碱中和与沉淀滴定**
> **Input:** “模拟向 pH 为 2 的硫酸酸性矿山废水中逐步加入石灰石粉末，直到 pH 达到 7，记录石灰石的消耗量和石膏的沉淀量。”
*考察重点*：开放/封闭系统判定（CO2平衡）、反应步进设置（`REACTION` 或 `EQUILIBRIUM_PHASES`）。

**考题 2.3：阳离子交换**
> **Input:** “高盐度海水入侵淡水含水层，计算钠离子与粘土表面钙离子的交换过程，输出淡水端钙离子浓度的升高情况。”
*考察重点*：交换容量（CEC）的预设、离子强度耦合逻辑、`EXCHANGE` 模块调用。

---

## 🔴 Level 3: 动力学与多场耦合 (高级)

**考题 3.1：矿物溶解动力学**
> **Input:** “模拟黄铁矿（Pyrite）在富氧环境下的溶解过程，考虑动力学速率方程，计算 100 天内系统 pH 和总铁浓度的随时间变化趋势。”
*考察重点*：速率方程（`RATES` 和 `KINETICS`）的 BASIC 脚本生成、时间步长提取、比表面积/速率常数的参数补全。

**考题 3.2：一维反应溶质运移**
> **Input:** “设定一个 1 米长的沉积物柱，初始充满去离子水。以 1m/d 的速度流过含 1ppm 砷（As）的溶液，计算 5 天后砷在柱体出口的穿透曲线。”
*考察重点*：时空网格离散规则（Cells / Time steps）、弥散系数（Dispersivity）的不确定性风险识别、`TRANSPORT` 模块调用。

**考题 3.3：极端环境多相演化**
> **Input:** “模拟 100°C、200 atm 压力下，超临界 CO2 注入含钙砂岩层的过程。计算 10 年后长石溶解和方解石沉淀对储层孔隙度的估算影响。”
*考察重点*：高压/高温数据库匹配（如 Pitzer / phreeqc.dat 高压修正）、不收敛风险评估、孔隙度随时间变化的二次计算逻辑。
