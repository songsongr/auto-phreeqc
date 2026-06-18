# 考题 3.3: 极端环境多相演化 (超临界 CO₂ 注入)

**日期**: 2026-05-12 | **数据库**: phreeqc.dat

## 题目要求

模拟 100°C、200 atm 压力下，超临界 CO₂ 注入含钙砂岩层的过程。计算 10 年后长石溶解和方解石沉淀对储层孔隙度的估算影响。

## 关键参数

| 参数 | 值 | 推理依据 |
|------|------|----------|
| 温度 | 100°C | 题目指定 (深部地质埋存条件) |
| 压力 | 200 atm | 题目指定 (超临界 CO₂, ~2 km 深度) |
| 数据库 | phreeqc.dat | 包含 Calcite + K-feldspar PHASES 定义 |
| CO₂ 方式 | GAS_PHASE fixed_pressure | 200 atm 恒压 (无穷供应) |
| Calcite | EQUILIBRIUM_PHASES (SI=0, 10 mol) | 快速平衡反应 |
| K-feldspar | KINETICS (3 mol) + RATES | 慢速动力学反应 |
| 速率参数 | Palandri & Kharaka (2004) | 文献标准速率常数 |
| 孔隙溶液 | Ca²⁺ 10 mM, HCO₃⁻ 10 mM, NaCl | 典型砂岩孔隙水 |
| pH | 7.5 | 碳酸盐缓冲含水层 [自动推理] |
| pe | -4.0 | 还原环境 (深部) [自动推理] |
| 时间 | 10 年 (20 步, CVODE) | 题目指定 |
| 初始孔隙度 | 0.20 | 典型砂岩 [自动推理] |

## 模拟方法

### 三阶段批反应框架

```
GAS_PHASE (CO₂ 200 atm)
    │
    ├── EQUILIBRIUM_PHASES (Calcite 快速平衡)
    │       └─ 瞬态 pH 缓冲 + Ca 循环
    │
    └── KINETICS + RATES (K-feldspar 慢速溶解)
            └─ 温度修正 + H⁺ 促进 + 近平衡抑制
```

### PHREEQC 输入结构

```
TITLE Supercritical CO2 injection into Ca-bearing sandstone

RATES 1
    K-feldspar
    -start
    ... (BASIC code with Palandri & Kharaka 2004 kinetics)
    -end

SOLUTION 1  (sandstone pore water, 100C, pH 7.5)
GAS_PHASE 1 (CO2(g) at 200 atm, fixed_pressure)
EQUILIBRIUM_PHASES 1 (Calcite)
KINETICS 1 (K-feldspar, 3 mol, 20 steps, 10 years)
SELECTED_OUTPUT (-step, -totals Ca K Al Si C, -si ..., -equilibrium_phases)

END
```

### K-feldspar 速率方程

```
RATES K-feldspar
    k_neutral = 10^(-12.41) × exp(Ea/RT)
    k_acid = 10^(-10.06) × exp(Ea/RT) × a(H+)^0.5
    rate = (k_neutral + k_acid) × area × (1 - SR("K-feldspar"))
```

### 孔隙度计算

```python
PHI_0 = 0.20
MOLAR_VOL = {"Calcite": 36.93, "K-feldspar": 108.87}  # cm³/mol
V_bulk = 1.0 / PHI_0 * 1000  # cm³ per kg water
phi = PHI_0 - (d_Calcite * V_cal + d_Kspar * V_kspar) / V_bulk
```

## 关键结果

| 指标 | 变化 | 意义 |
|------|------|------|
| pH | 7.5 → 5.99 | CO₂ 溶解导致酸化 pH 下降 1.5 |
| Calcite | +0.004 mol (沉淀) | CO₂ → HCO₃⁻ → CaCO₃(s) |
| K-feldspar | -0.007 mol (溶解) | 0.24% 溶解, 速率受近平衡抑制 |
| Kaolinite SI | 5.62 | 热力学有利但动力学禁止 |
| **孔隙度** | **0.2000 → 0.20014 (+0.07%)** | 微小增加 (Kspar 溶 > Calcite 沉) |

### 地球化学演化轨迹

```
pH
7.5 |...............
    |               \
7.0 |                \_______
    |                        \
6.0 |                         ···········
    |
    +--CO2溶解--+--Calcite缓冲--+--准稳态-->
       步 0-2       步 3-10       步 11-20
```

## Skill 扩展: 新增功能

### 1. `generate_gas_phase_block()`

支持 GAS_PHASE 关键字块生成... (内容不变)

---

## 扩展版本: 耦合动力学 + TRANSPORT

**工作目录**: `workspace/task3_3_co2_extended/`

### 扩展内容

在原版 1.0 基础上新增:
1. **Kaolinite 沉淀 RATES** — 打破 K-feldspar SI≈0 瓶颈
2. **TRANSPORT + KINETICS** — 1D 反应性运移 (10 cells, 1m)
3. **孔隙度空间梯度** — 沿柱矿物分带

### 扩展批反应结果

| 对比项 | 原版 (单一 Kspar) | 扩展版 (Kspar + Kaolinite) | 增益 |
|--------|-------------------|---------------------------|------|
| K-feldspar 溶解 | -0.007 mol | **-0.078 mol** | **10×** |
| Kaolinite 沉淀 | N/A | +0.039 mol | 新增矿物 |
| 终态 Kspar SI | 0.000 | 0.000 | — |
| 终态 Kaol SI | 5.62 (冻结) | **0.000** (平衡) | 解冻 |
| 孔隙度变化 | +0.007% | **+0.46%** | **66×** |

**机理**: Kspar 溶解释放 Al³⁺ → Kaolinite 沉淀消耗 Al³⁺ → Kspar SI 持续 < 0 → 溶解不停止

### TRANSPORT 结果

**参数**: 10 cells, 1m 柱, 0.1 m/yr 流速, CO₂ 酸性入口 (pH 4)

| 位置 | pH | Kspar 剩余 | Kaolinite | 孔隙度 |
|------|-----|-----------|-----------|--------|
| Cell 1 (入口) | 6.00 | ~2.90 mol | ~0.52 mol | ~0.2005 |
| Cell 10 (出口) | 5.02 | **2.81 mol** | **0.59 mol** | **0.2022** |

**净反应** (出口单元):
- Kspar 溶解: -0.189 mol → 体积 -20.58 cm³ (增孔)
- Kaolinite 沉淀: +0.095 mol → 体积 +9.40 cm³ (减孔)
- **净 Δφ = +1.12%** (porosity 0.2000 → 0.2022)

### 扩展中的关键发现

1. **多矿物动力学必须耦合产物矿物**: 单矿物 → 产物积累 → SI 趋零冻结; 加产物矿物 → 持续反应
2. **摩尔体积差决定增孔效率**: Kspar(108.87) : Kaolinite(99.52) ≈ 2.2:1 → 每反应 1 mol Kspar 净增孔 ~59 cm³
3. **KINETICS -steps 是块级参数**: PHREEQC 中 -steps 定义在 KINETICS 块级别, 非 per-reactant。多反应物时只需定义一个 -steps
4. **TRANSPORT + KINETICS 可行**: CVODE 积分器 + step_divide 处理刚性微分方程，10×20 步约 60s

## 已知问题与对策

### CO₂ 注入模拟收敛性

高 pCO₂ (200 atm) 可能导致收敛困难。对策:
- 使用 CVODE 积分器 (`cvode: True`) 处理刚性微分方程
- 适当增加容差 (`tol: 1e-8`)
- 减小初始步长 (`-step_divide 10`)

### phreeqc.dat 温度极限

phreeqc.dat 的热力学数据在 0-100°C 有效。100°C 为上限。超过 100°C 建议使用 `llnl.dat` 或 `wateq4f.dat`。

### K-feldspar 近平衡抑制

当 SI ≈ 0 时, (1-SR) ≈ 0 → 溶解速率趋近于 0。这是地质条件下长石溶解的真实行为:
- 长时间尺度需要次生矿物沉淀 (如 Kaolinite) 来持续移出产物
- 如需模拟大量溶解, 需在 RATES 中添加 Kaolinite 沉淀

### 孔隙度估算精度

当前孔隙度采用简单线性估算 (忽略矿物-水质量比的非线性效应)。改进方向:
- 使用 `USER_PUNCH` 在 PHREEQC 内部直接计算孔隙度
- 考虑孔隙度-渗透率耦合 (Kozeny-Carman 方程)

## 与其他考题的关联

| 考题 | 关联点 | 共享技术 |
|------|--------|----------|
| 考题 2.2 (AMD 中和) | CO₂ 酸化与石灰中和对比 | EQUILIBRIUM_PHASES 缓冲 |
| 考题 3.1 (黄铁矿动力学) | RATES 定义 + Arrhenius 温度修正 | KINETICS + RATES + CVODE |
| 考题 3.2 (As 传输) | TRANSPORT 传输耦合 (可扩展) | 反应性运移 + KINETICS |
