# 考题 3.3: 极端环境多相演化 (超临界 CO₂ 注入)

**日期**: 2026-05-12 | **数据库**: phreeqc.dat | **方法**: KINETICS + EQUILIBRIUM_PHASES + GAS_PHASE

## 模拟条件

- **温度/压力**: 100°C, 200 atm (超临界 CO₂ 条件)
- **孔隙溶液**: Ca²⁺ 10 mM + HCO₃⁻ 10 mM + NaCl (pH=7.5, pe=-4, 还原环境)
- **CO₂ 注入**: GAS_PHASE CO₂(g) 固定分压 200 atm
- **Calcite**: EQUILIBRIUM_PHASES (快速平衡, 10 mol 初始)
- **K-feldspar**: KINETICS + RATES (3 mol 初始, Palandri & Kharaka 2004 速率参数)
  - Neutral: log k = -12.41, Ea = 38 kJ/mol
  - Acid: log k = -10.06, Ea = 51.7 kJ/mol, a(H⁺)^0.5
  - 比表面积: 0.2 m²/g (2000 cm²/g)
  - CVODE 积分器
- **时间**: 20 步, 10 年 (315,576,000 秒)

## 关键结果

| 指标 | 初始值 | 最终值 | 变化 |
|------|--------|--------|------|
| pH | 7.50 | 5.99 | -1.50 |
| pe | -4.00 | -2.54 | +1.46 |
| Ca²⁺ | 10.00 mM | 6.19 mM | -3.81 mM |
| K⁺ | 0.10 mM | 0.46 mM | +0.36 mM |
| Al³⁺ | 0.00 mM | 0.36 mM | +0.36 mM |
| Si | 0.10 mM | 1.19 mM | +1.09 mM |
| 离子强度 | 0.055 | 0.049 | -0.006 |
| Calcite | 10.000 mol | 10.004 mol | +0.004 mol (沉淀) |
| K-feldspar | 3.000 mol | 2.993 mol | -0.007 mol (溶解) |
| **孔隙度** | **0.2000** | **0.20014** | **+0.00014 (+0.07%)** |

## 地球化学过程解析

### 阶段 1: CO₂ 溶解与酸化 (步 0-2)
CO₂(g) + H₂O → H₂CO₃ → H⁺ + HCO₃⁻
- 200 atm CO₂ 快速溶解, pH 从 7.5 降到 ~6.0
- Calcite 瞬时响应缓冲 pH: CaCO₃ + H⁺ ↔ Ca²⁺ + HCO₃⁻

### 阶段 2: 长石-碳酸盐竞争 (步 3-15)
KAlSi₃O₈ + 4H⁺ → K⁺ + Al³⁺ + 3SiO₂ + 2H₂O
- K-feldspar 缓慢溶解, 释放 K, Al, Si
- Ca²⁺ + HCO₃⁻ → CaCO₃(s) + H⁺ (Calcite 沉淀)
- Kaolinite 高度过饱和 (SI = 5.62) 但动力学不允许沉淀
- 溶液组成靠近 K-feldspar 平衡 (SI = 0.0002) → 溶解速率趋近于 0

### 阶段 3: 准稳态 (步 16-20)
- pH 稳定在 ~6.0
- Calcite 保持平衡 (SI = 0.00)
- K-feldspar 溶解近乎停止 (速率 ∝ 1-SR ≈ 0)

### 孔隙度分析
- Calcite 沉淀: +3.81e-3 mol × 36.93 cm³/mol = +0.141 cm³ (减孔)
- K-feldspar 溶解: -7.27e-3 mol × 108.87 cm³/mol = -0.792 cm³ (增孔)
- **净孔体积变化: -0.651 cm³ → 孔隙度 +0.00014**

孔隙度变化极小 (< 0.1% 相对), 说明 10 年的 CO₂ 注入对储层孔隙度的直接影响有限。主要原因是: (1) Calcite 沉淀量小; (2) K-feldspar 速率受近平衡抑制。

## 图表说明

### charts/ph_evolution.png
**类型**: selected_output_sweep (pH 演化)
**内容**: 注 CO₂ 后 pH 随时间变化
**X 轴**: Time Step (~0.5 年/步, 共 10 年)
**Y 轴**: pH
**解读**: pH 从初始 7.5 在第一步骤骤降至 6.0, 随后缓慢降至 5.99。初始骤降由 200 atm CO₂ 快速溶解引起; 之后 Calcite 缓冲使 pH 缓慢稳定。

### charts/element_evolution.png
**类型**: selected_output_sweep (元素浓度)
**内容**: Ca, K, Al, Si, C 浓度随时间变化
**X 轴**: Time Step
**Y 轴**: Total Concentration (mol/kgw)
**解读**: Ca 从 0.01 M 降至 0.0062 M (Calcite 沉淀消耗), K 从 0.0001 升至 0.00046 M (K-feldspar 释放), 与 K-feldspar 溶解的化学计量一致 (每 mol K-feldspar 释放 1 K + 3 Si + 1 Al)。

### charts/si_evolution.png
**类型**: selected_output_sweep (饱和指数演化)
**内容**: Calcite, K-feldspar, Kaolinite, Quartz 的 SI
**X 轴**: Time Step
**Y 轴**: SI
**解读**: Calcite SI = 0 始终维持 (快速平衡)。Kaolinite SI = 5.6 高度过饱和 (表明次生高岭石热力学有利但动力学受限)。K-feldspar SI 从初始末知 (-999) 很快收敛到 ~0, 解释了速率降低的原因。

### charts/porosity_evolution.png
**类型**: 孔隙度演化
**内容**: 10 年间孔隙度变化轨迹
**X 轴**: Time Step
**Y 轴**: Porosity
**解读**: 孔隙度从 0.2000 缓慢增至 0.20014 (+0.07%)。由于 K-feldspar 溶解体积 (108.87 cm³/mol) 远大于 Calcite 沉淀体积 (36.93 cm³/mol), 净效果为增孔。但总量极小。

### charts/mineral_change.png
**类型**: 矿物质量变化
**内容**: Calcite 和 K-feldspar 的摩尔变化
**X 轴**: Time Step
**Y 轴**: Mineral moles change (mol/kgw)
**线条**: Calcite d(delta) (红色), K-feldspar d(delta) (绿色)
**解读**: Calcite 持续沉淀 (+3.8e-3 mol), K-feldspar 持续溶解 (-7.3e-3 mol)。两条曲线近似线性, 说明在模拟时间尺度内反应速率变化不大, 但 K-feldspar 速率已接近零 (SI ≈ 0)。

## 局限性

1. **批反应近似**: 未考虑 CO₂ 注入的空间梯度 (实际为径向流动)
2. **单一动力学矿物**: 只考虑了 K-feldspar, 未包括其他长石/黏土矿物
3. **Kaolinite 不沉淀**: 热力学有利 (SI=5.6) 但 RATES 中未包含, 默认动力学禁止
4. **孔隙度反馈**: 未考虑孔隙度变化对渗透率和反应表面积的反向影响
5. **温度恒定**: 假设 100°C 恒温, 未考虑注入引起的温度梯度
