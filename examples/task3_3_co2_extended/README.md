# 考题 3.3 扩展: 耦合动力学 + 反应性运移

**日期**: 2026-05-12 | **数据库**: phreeqc.dat

## 三种模拟对比

| 指标 | 原版批反应 | 扩展批反应 (耦合) | TRANSPORT 运移 |
|------|-----------|-------------------|----------------|
| K-feldspar 溶解 | -0.007 mol | **-0.078 mol** (10×) | **-0.189 mol** (27×) |
| Kaolinite 沉淀 | N/A | +0.039 mol | +0.095 mol |
| 最终 Kspar SI | 0.000 | 0.000 | 0.000 |
| 最终 Kaol SI | 5.62 (冻结) | **0.000** (平衡) | **-0.000** (平衡) |
| **孔隙度变化** | **+0.007%** | **+0.46%** (66×) | **+1.12%** (160×) |
| pH 终值 | 5.99 | 6.22 | 5.02 (出口) |
| 计算时间 | ~5s | ~10s | ~60s |

## 核心改进: Kaolinite 沉淀 RATES

### 原版的问题
单矿物 (K-feldspar) 动力学中，Al 和 Si 在溶液中积累 → 溶液快速达到 K-feldspar 平衡 (SI≈0) → 速率因子 (1-SR) ≈ 0 → 溶解趋停。

### 扩展后
添加 Kaolinite 沉淀 RATES → Al 和 Si 被持续消耗 → K-feldspar SI 保持 < 0 → 溶解持续进行:

```
KAlSi₃O₈ + H⁺ + ½H₂O → ½Al₂Si₂O₅(OH)₄ + K⁺ + 2SiO₂(aq)
(108.87 cm³/mol)       →  (49.76 cm³/mol)
```

**净反应**每 mol K-feldspar 溶解:
- 移除体积: 108.87 cm³
- 新增体积: 49.76 cm³ (0.5 mol Kaolinite)
- **净增孔**: 59.11 cm³/mol Kspar

### 质量平衡验证
- 0.078 mol Kspar × 1 Al = 0.078 mol Al 释放
- 0.039 mol Kaolinite × 2 Al = 0.078 mol Al 消耗
- **完美平衡** ✓

## TRANSPORT 空间效应

1D 柱 (10 cells, 1m, 0.1 m/yr 流速):

### pH 空间梯度
```
入口 (cell 1):  pH = 6.00  (强 CO₂ 影响)
中段 (cell 5):  pH = 5.50
出口 (cell 10): pH = 5.02  (积累酸化)
```

### 矿物蚀变分带
```
Cell 1-3:  Kspar 溶解最强烈, Kaolinite 沉淀最多
Cell 4-6:  中等蚀变, 溶液组成过渡
Cell 7-10: CO₂ 前锋累积, pH 最低
```

### 孔隙度空间变化 (末单元)
- K-feldspar 溶解: -0.189 mol × 108.87 = -20.58 cm³ (孔隙 +)
- Kaolinite 沉淀: +0.095 mol × 99.52 = +9.40 cm³ (孔隙 -)
- **净增孔: +11.17 cm³ → φ 0.200 → 0.202 (+1.12%)**

## Skill 迭代总结

### 新增 generate_input.py 功能
1. `generate_gas_phase_block()` — GAS_PHASE 关键字块 (固定压力/体积)
2. `generate_reaction_pressure_block()` — 高压反应条件
3. KINETICS -steps 移至块级别 (支持多反应物)
4. RATES 空白行过滤

### 关键发现
1. **多矿物耦合**: 单矿物动力学 → SI 趋零冻结; 加产物矿物 → 持续反应
2. **SR() 限制**: PHREEQC BASIC 中 SR() 不能做赋值唯一 RHS, 需内联
3. **KINETICS -steps 位置**: 在 PHREEQC 中 -steps 是块级别参数, 非反应物级别
4. **孔隙度增强**: K-feldspar/Kaolinite 摩尔体积差 (108.9 vs 99.5) 使净增孔显著
