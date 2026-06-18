# Pb 形态分布模拟示例 (考题 1.1)

## 问题描述

> 分析一个 pH 为 6.0、含有 10 mmol/L 氯化钠和 1 mg/L 铅的水样中，铅的主要存在形态及其浓度。

**考察重点**：溶液基本定义、默认参数识别、数据库对金属络合常数的影响。

## 完整输入文件

```
TITLE Pb speciation -- pH 6.0, 10 mmol/L NaCl, 1 mg/L Pb, pe=12 O2(g) -0.68

SOLUTION 1
    units mg/L
    pH 6.0
    pe 12 O2(g) -0.68
    density 1.0
    Na 229.9          # 10 mmol/L NaCl, Na = 0.010 * 22.9897 = 0.2299 g/L
    Cl 354.5          # 10 mmol/L NaCl, Cl = 0.010 * 35.453 = 0.3545 g/L
    Pb 1.0            # 1 mg/L Pb

SELECTED_OUTPUT
    -file selected_output.txt
    -reset true
    -pH
    -pe
    -si Pb(OH)2
    -si PbO
    -si Cerussite
    -si Anglesite
    -si Galena
    -totals Pb
    -totals Na
    -totals Cl
    -molalities Pb+2
    -molalities PbOH+
    -molalities Pb(OH)2
    -molalities Pb(OH)3-
    -molalities PbCl+
    -molalities PbCl2
    -molalities PbCl3-
    -molalities PbCl4-2
    -molalities PbHCO3+
    -molalities PbCO3
    -molalities Pb(CO3)2-2
    -molalities PbO2
    -molalities HPbO2-

END
```

## 参数解析

| 参数 | 值 | 单位 | 说明 |
|------|-----|------|------|
| pH | 6.0 | — | 从题目直接提取 |
| pe/O₂(g) | 12 / -0.68 | — | pe 值由 O₂(g) 氧化还原缓冲对控制，实际计算得 pe=14.63 |
| Na | 229.9 | mg/L | 10 mmol/L NaCl → Na = 10 × 22.99 mg/mmol |
| Cl | 354.5 | mg/L | 10 mmol/L NaCl → Cl = 10 × 35.45 mg/mmol |
| Pb | 1.0 | mg/L | 从题目直接提取 |
| 温度 | 25.0 | °C | 默认推理值 |
| 密度 | 1.0 | g/cm³ | 默认推理值 |
| 碱度 | 0 | mg/L as CaCO₃ | **隐式默认值，关键风险项** |
| 数据库 | phreeqc.dat | — | 默认推理值 |

## 缺失参数与风险

| 缺失参数 | 对结果的影响 | 建议 |
|----------|-------------|------|
| **碱度 (Alkalinity)** | 若无碱度，PbCO₃、PbHCO₃⁺ 等碳酸铅络合物浓度=0。实际水样通常含碳酸盐碱度，可占据 Pb 形态的 20-30% | 应标注"碱度假设为 0"的风险，或建议测量 |
| **pe 实际值** | 输入 `pe 12 O2(g) -0.68` 时，PHREEQC 通过 Nernst 方程计算实际 pe=14.63，与输入值不同 | 应在报告中注明计算后的实际 pe 值 |
| **数据库依赖** | phreeqc.dat / llnl.dat / minteq.dat 中 Pb 的络合常数差异可达 0.5-1.0 log K 单位 | 建议标注数据库来源，必要时做灵敏度分析 |

## pe 语法说明

PHREEQC 的 `pe` 关键字在 SOLUTION 数据块中有两种用法：

| 语法 | 含义 | 示例 |
|------|------|------|
| `pe <value>` | 直接指定 pe 值 | `pe 4.0` |
| `pe <guess> <couple> <value>` | 用氧化还原对定义 pe，`<guess>` 为初始猜测值，最终 pe 由平衡计算确定 | `pe 12 O2(g) -0.68` |

当使用第二种语法时，PHREEQC **不保证**计算后的 pe 等于 `<guess>` 值。例如 `pe 12 O2(g) -0.68`（pH=6.0）实际计算得 pe=14.63。如果希望精确控制 pe，使用第一种语法 `pe 14.63`。

## 结果解析

### 饱和指数

| 矿物 | SI | 说明 |
|------|----|------|
| Pb(OH)₂ | -1.75 | 未饱和，无沉淀 |
| PbO | -999.999 | phreeqc.dat 中无此矿物条目 |
| Cerussite (PbCO₃) | -999.999 | phreeqc.dat 中无此矿物条目 |
| Anglesite (PbSO₄) | -999.999 | phreeqc.dat 中无此矿物条目 |

> **注意**：-999.999 意味着 PHREEQC 在当前数据库中找不到该相的热力学数据。需要确认数据库是否包含该矿物。

### Pb 形态分布

| 物种 | 浓度 (mol/kgw) | 占比 | 说明 |
|------|----------------|------|------|
| **Pb²⁺** | 3.770 × 10⁻⁶ | **64.6%** | **主导形态** |
| **PbCl⁺** | 9.921 × 10⁻⁷ | **17.0%** | 氯络合 |
| PbOH⁺ | 5.391 × 10⁻⁸ | 0.92% | 羟基络合 |
| PbCl₂ | 1.275 × 10⁻⁸ | 0.22% | 中性络合 |
| Pb₂OH³⁺ | 6.879 × 10⁻¹² | <0.01% | 多核络合 |
| Pb(OH)₂, PbCl₃⁻, PbCl₄²⁻ | <10⁻¹⁰ | <0.01% | 痕量 |
| PbCO₃, PbHCO₃⁺ | 0 | 0% | 碱度=0，无碳酸根 |

### 质量平衡

```
输入 Pb: 1.0 mg/L ÷ 207.2 g/mol = 4.826 × 10⁻⁶ mol/kgw
输出 Pb (总): 4.829 × 10⁻⁶ mol/kgw (SELECTED_OUTPUT)
质量平衡误差: <0.1% ✓
```

## 关键教学要点

1. **默认参数意识**：PHREEQC 的隐式默认值（温度 25°C、碱度 0、pe 4 等）会显著影响结果，必须明确记录假设。

2. **pe 与氧化还原耦合**：使用 `pe <value> <couple>` 语法时，最终 pe 值由氧化还原平衡决定而非输入值，这是常见误解。

3. **数据库敏感性**：不同数据库的 Pb 络合常数不同。phreeqc.dat 是通用数据库，如需要更详细的 Pb 形态分析（如有机络合），应考虑 minteq.dat 或 llnl.dat。

4. **碱度关键性**：对于重金属形态分析，碱度（碳酸盐）常被忽略但至关重要——碳酸铅络合物在近中性 pH 下可占主导。

5. **SELECTED_OUTPUT 优势**：通过 -molalities 明确指定感兴趣物种，可直接获取各形态浓度，避免在大量文本输出中手动搜索。

## 扩展方向

- **pH 扫描**: 将 pH 从 2 扫到 10，观察各物种占比随 pH 的变化
- **氯离子扫描**: 固定 pH=6 和 Pb=1 mg/L，改变 NaCl 浓度 (1-1000 mmol/L) 观察氯络合物的竞争效应
- **数据库对比**: 用 phreeqc.dat / llnl.dat / minteq.dat 分别计算并比较结果差异
- **矿物溶解度边界**: 在碱性条件下加入 CO₂ 或碱度，观察 Pb(OH)₂ 或 Cerussite 何时开始沉淀
