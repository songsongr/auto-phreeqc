# 考题 3.1 — 黄铁矿氧化动力学 (Pyrite Kinetics)

**日期**: 2026-05-12 | **状态**: ✅ 已完成

## 输入

"模拟黄铁矿（Pyrite）在富氧环境下的溶解过程，考虑动力学速率方程，计算 100 天内系统 pH 和总铁浓度的随时间变化趋势。考虑二次矿物沉淀。"

## 模拟方式

独立 coordinator Python 脚本，调用 skill 四步工作流 (generate → run → parse → visualize)，全程自动化。

### 新增 Skill 功能
本次模拟首次使用 KINETICS 和 RATES 关键字，需要新增以下生成器：

- `generate_kinetics_block()` — KINETICS 关键字块
- `generate_rates_block()` — RATES 关键字块 (含 PHREEQC BASIC 自动编号)
- `generate_single_simulation()` 中集成 kinetics/rates 支持

## 参数配置

| 参数 | 值 | 推理方式 |
|------|-----|----------|
| 初始溶液 pH | 7.0 (纯水 + 微量 K/Na/Cl) | 中性起始条件 |
| O₂ 环境 | O₂(g) SI=-0.68 (大气平衡) | EQUILIBRIUM_PHASES 开放系统 |
| 黄铁矿初始量 | 0.5 mol (~60g) | 合理实验室规模 |
| 速率常数 k | 1.0×10⁻⁷ mol/m²/s | Williamson & Rimstidt (1994) |
| 比表面积 A₀ | 100 m² | 细粉 0.5 m²/g × 200g |
| O₂ 反应级数 | 0.5 | Williamson & Rimstidt |
| H⁺ 反应级数 | −0.11 | Williamson & Rimstidt |
| 时间步长 | 18 步对数递增 (1h→100d) | 初始反应快，后期减缓 |
| 积分器 | CVODE | KINETICS -cvode true |
| 二次矿物 | Fe(OH)₃(a) SI=0, Jarosite-K SI=0 | 允许沉淀 (初始量=0) |
| Goethite | 仅监测 SI，未设为活动相 | 晶质相形成缓慢 |

## 关键发现

### 反应路径
```
阶段 1 (0-1h):  pH 7.0 → 3.07 — 中性 pH 下溶解极快
                黄铁矿溶解 → Fe²⁺ → Fe³⁺ (O₂ 氧化) → 水解产酸

阶段 2 (1h-2d): pH 3.07 → 1.93 — Jarosite-K 沉淀消耗 K⁺
                K⁺ 耗尽后 Jarosite 停止形成

阶段 3 (2d-100d): pH 1.93 → 1.03 — 黄铁矿持续溶解
                  极端酸性下 Fe(OH)₃(a) 和 Goethite 均不饱和
                  所有 Fe 和 S 累积在溶液中
```

### 数值结果 (100 天终态)
| 指标 | 值 | 解读 |
|------|-----|------|
| pH | 1.03 | 极端酸性 AMD |
| 溶解 Fe | 0.502 mol/kgw (28 g/L) | ~100% 黄铁矿溶解 |
| 溶解 S | 1.004 mol/kgw (96 g/L SO₄) | Fe:S = 1:2 精确 |
| Jarosite-K | 0.1 mmol 沉淀 | K⁺ 限制 |
| O₂ 消耗 | 1.87 mol | 大气持续补充 |
| SI Pyrite | −220 | 极强溶解驱动力 |
| SI Fe(OH)₃(a) | −4.98 | 酸度过高, 不沉淀 |
| SI Goethite | +0.92 | 热力学过饱和 (未活动) |

### 暴露的 Skill 薄弱点 & 本次修复

#### 1. KINETICS/RATES 关键字缺失 — **已修复**
**问题**: `generate_input.py` 无 `generate_kinetics_block()` 和 `generate_rates_block()` 函数
**修复**: 新增两个生成器函数，支持完整 KINETICS 参数 (`-formula`, `-m`, `-m0`, `-parms`, `-tol`, `-steps`, `-cvode` 等) 和 RATES 块 (PHREEQC BASIC 自动行号编号)

#### 2. PHREEQC BASIC 变量名与系统变量冲突 — **已记录**
**问题**: 用户变量 `m` 和 `m0` 与系统变量 `M` (current moles) 和 `M0` (initial moles) 冲突，导致 "Illegal command in line" 错误
**原因**: PHREEQC BASIC 大小写不敏感，`m`=`M`，`m0`=`M0`
**解决**: 使用不冲突的变量名 (如 `cur_mol`, `moles_init`)，或通过 `parm(N)` 传递初始值

#### 3. parm 传递初始摩尔数模式 — **已建立**
**问题**: RATES 中每次调用局部变量重置，无法保存初始值
**解决**: 通过 `-parms k A0 n_O2 n_H m_init` 传递初始摩尔数，用 `parm(5)` 读取

#### 4. SELECTED_OUTPUT 中 -totals 列名不包含 `tot_` 前缀 — **已记录**
**问题**: `-totals Fe` 生成的列名是 `Fe`，不是 `tot_Fe`。而 `-si Calcite` 生成的列名是 `si_Calcite`
**原因**: PHREEQC 对 -totals 列直接用元素名，对 -si 列加 `si_` 前缀
**解决**: 在 parse 代码中按元素名查找 (如 `cols.index("Fe")`)

#### 5. EQUILIBRIUM_PHASES 中 Goethite 未设为活动相 — **设计决策**
**结果**: Goethite 持续过饱和 (SI +0.92) 但不沉淀
**原因**: Goethite 虽在 `-equilibrium_phases` SELECTED_OUTPUT 监测列表中，但未在 EQUILIBRIUM_PHASES 关键字块中设为活动相。这是有意的 — 在 100 天尺度上晶质 Goethite 不会形成
**改善建议**: 若需要 Goethite 沉淀，将其加入 EQUILIBRIUM_PHASES `Goethite 0 0`

#### 6. 反应初始阶段 pe 冲突 — **已观察**
**现象**: 初始 SOLUTION 设 pe=4.0，但 EQUILIBRIUM_PHASES O₂(g) -0.68 推动 pe 至 17-20
**影响**: 初始 pe 值被覆盖，不影响结果 (O₂ 平衡决定实际 pe)

## Skill 代码改动

### generate_input.py 新增函数

```python
def generate_kinetics_block(kinetics_def: dict, block_id: int = 1) -> str
def generate_rates_block(rates_defs: list[dict], block_id: int = 1) -> str
```

`generate_single_simulation()` 新增参数支持:
- `params["kinetics"]` → `generate_kinetics_block()`
- `params["rates"]` → `generate_rates_block()`

### RATES BASIC 自动编号规则
- 若代码行首字已是数字 (≤6字符)，不做修改
- 若代码行无行号，从 10 开始每行 +10 自动编号
- 推荐写法: 不写行号，由生成器自动编号

### 最佳实践: KINETICS + EQUILIBRIUM_PHASES 共存

当动力学溶解与平衡沉淀共存时：
```
RATES → 定义速率方程 (黄铁矿溶解)
KINETICS → 调用 RATES，控制时间步长
EQUILIBRIUM_PHASES → 二次矿物沉淀 (瞬时平衡)
```

PHREEQC 在每个 KINETICS 时间步内：
1. 执行动力学反应 (SAVE moles)
2. 重新计算溶液 speciation
3. 与 EQUILIBRIUM_PHASES 平衡 (沉淀/溶解)

这保证了反应顺序的正确性：先溶解释放 Fe²⁺，再氧化为 Fe³⁺，最后检查矿物饱和并沉淀。

## 输出文件

```
workspace/task3_1_pyrite_kinetics/
├── input.pqi              # PHREEQC 输入 (RATES + KINETICS + EQUILIBRIUM_PHASES)
├── output.qpo             # 完整输出文本
├── selected.txt           # SELECTED_OUTPUT 时间序列数据 (18 steps)
├── results.json           # 结构化解析结果
├── README.md              # 人类可读报告 (含图表解读)
├── coordinator.py         # 协调脚本
└── charts/
    ├── ph_vs_time.png     # pH 时间演化
    ├── tot_fe_s_vs_time.png   # 总 Fe 和总 S 浓度
    ├── si_vs_time.png     # 矿物饱和指数
    └── phase_delta_vs_time.png  # 相摩尔量变化
```
