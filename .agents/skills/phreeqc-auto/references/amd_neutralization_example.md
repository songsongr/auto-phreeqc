# 考题 2.2: 酸碱中和与沉淀滴定 (AMD + 石灰石)

**完成日期**: 2026-05-11
**模拟类型**: Batch-Reaction (REACTION + EQUILIBRIUM_PHASES)
**关键字**: AMD, 石灰石中和, 沉淀序列, pH 缓冲区间, Fe/Al 水解

## 输入参数

### AMD 组成
- pH = 2.0, pe = 4.0, T = 25°C
- Fe(2) = 500 mg/L, Fe(3) = 50 mg/L, Al = 200 mg/L, Mn = 50 mg/L, S(6) = 2600 mg/L
- 电荷近似平衡: 总阳离子 ~54.6 meq/L, SO₄²⁻ ~54.1 meq/L

### 中和方案
- 中和剂: Calcite (CaCO₃), REACTION 步进添加
- 总量: 0.05 mol, 100 步 (0.0005 mol/步)
- CO₂ 系统: 开放 (log PCO₂ = -3.4), EQUILIBRIUM_PHASES CO₂(g) -3.4 10.0
- 允许沉淀相: Gypsum, Fe(OH)₃(a), Gibbsite, Calcite (均为 SI=0, 0 mol — 仅沉淀)

### PHREEQC 输入结构
```
SOLUTION 1 AMD
    units mg/L; pH 2.0; pe 4.0; temp 25.0
    Fe(2) 500; Fe(3) 50; Al 200; Mn 50; S(6) 2600

EQUILIBRIUM_PHASES 1
    Gypsum 0.0 0.0        # 仅沉淀
    Fe(OH)3(a) 0.0 0.0    # 仅沉淀
    Gibbsite 0.0 0.0      # 仅沉淀
    CO2(g) -3.4 10.0      # 开放系统
    Calcite 0.0 0.0       # 仅沉淀 (中和后期)

REACTION 1
    Calcite 1.0
    0.05 moles in 100 steps

SELECTED_OUTPUT
    -file selected_output.txt
    -reset false
    -step true              # 每步输出
    -equilibrium_phases Gypsum Fe(OH)3(a) Gibbsite Calcite
    -pH true
    -pe true
    -totals Ca S Fe Al Mn C(4)
    -si Calcite Gypsum Fe(OH)3(a) Gibbsite
END
```

## 核心结果

### 石灰石消耗量
- **pH 7 达标**: 第 44 步, 0.0220 mol CaCO₃ (2.20 g / kg 水)
- 最终 pH: 7.70
- pH 7 后继续添加方解石导致过饱和再沉淀 (28.3 mmol)

### 沉淀序列 (按发生先后)

| 相 | 起始 pH | 对应 CaCO₃ | 最终沉淀量 | 最终质量 |
|----|---------|-----------|-----------|---------|
| Fe(OH)₃(a) | 3.42 | 9.5 mmol | 0.90 mmol | 0.10 g |
| Gibbsite | 3.92 | 11.0 mmol | 7.44 mmol | 0.58 g |
| Gypsum | 4.00 | 15.0 mmol | 6.73 mmol | 1.16 g |
| Calcite | 7.70 | 22.5 mmol | 28.32 mmol | 2.83 g |

### pH 缓冲区间

| 区间 | pH 范围 | CaCO₃ 消耗 | 主导过程 |
|------|---------|-----------|---------|
| 游离酸中和 | 2.0 → 3.0 | 8.0 mmol | CaCO₃ + 2H⁺ → Ca²⁺ + CO₂ + H₂O |
| Fe³⁺ 水解缓冲 | 3.4 → 3.9 | 1.5 mmol | Fe³⁺ + 3H₂O → Fe(OH)₃ + 3H⁺（释酸抑制pH升高）|
| Al³⁺ 水解缓冲 | 3.9 → 4.4 | 10.5 mmol | Al³⁺ + 3H₂O → Al(OH)₃ + 3H⁺ (**最大缓冲**) |
| pH 突跃 | 4.4 → 7.4 | 0.5 mmol | Al 缓冲耗竭, 游离 H⁺ 急剧减少 |
| 方解石过饱和 | 7.4 → 7.7 | 0.5 mmol | 开放 CO₂ 系统中 calcite SI 转为正值 |

### 关键发现

1. **Fe²⁺ 不沉淀**: 500 mg/L Fe²⁺ 在全过程中保持溶解态。当 pH 从 4.4 跃升到 7.4 时，pe 从 ~7.2 骤降至 -1.77，Fe²⁺ 仍是热力学稳定形态。需要主动曝气才能氧化沉淀 Fe²⁺。

2. **Al 是最大酸源**: Al³⁺ (200 mg/L) 水解消耗 10.5 mmol CaCO₃，超过游离酸 (8.0 mmol) 和 Fe³⁺ (1.5 mmol) 的总和。因为每 mol Al³⁺ 沉淀释放 3 mol H⁺。

3. **石膏竞争效应**: 石膏从 pH 4.0 就开始沉淀（与 Gibbsite 几乎同时），Ca²⁺ 被 SO₄²⁻ 固定为固相，每 mol 石膏沉淀消耗 1 mol Ca²⁺ 但不贡献酸中和 — 间接增加石灰石需求。

4. **CO₂ 开放系统的双重效应**: 大气 CO₂ 溶解为中和反应提供额外的 HCO₃⁻ 缓冲，但也抑制了 calcite 饱和（降低 CO₃²⁻ 活度），使得 calcite 在 pH < 7.7 始终欠饱和。

## 暴露的 Skill 薄弱点

### 1. `generate_selected_output_block()` 缺少关键选项

**问题**: 当前函数不支持 `-step` 和 `-equilibrium_phases` 参数，REACTION 步进输出只能通过后处理字符串替换 hack 实现。

**修复方案**: 在 `generate_selected_output_block()` 中添加:
```python
step: bool = False,
equilibrium_phases: list[str] | None = None,
```

### 2. `d_Phase` 列符号约定不明确

**问题**: EQUILIBRIUM_PHASES 设 0 mol 初始量时，d_Phase > 0 表示**沉淀**（相量增加），与"溶解为正"的直觉相反。初次使用时以为沉淀量应为负值。

**说明**: PHREEQC 中 `d_Phase` 列始终表示"组合中相量的变化"，正 = 增加（沉淀或剩余未溶解），负 = 减少（溶解）。当初始量为 0 时，沉淀必然导致正变化。

### 3. pH 缓冲区间分析无自动化工具

**问题**: 当前无 `calc_pH_buffer_regions()` 等辅助函数，多级缓冲识别需要在 coordinator 中手写分析逻辑。

**建议**: 在 `parse_output.py` 中添加:
```python
def detect_buffer_regions(ph_data, calcite_data, threshold=0.1):
    """Detect pH buffer plateaus from titration data.
    Returns list of (start_idx, end_idx, buffer_type) tuples."""
```

### 4. 开放/封闭 CO₂ 系统选择无指导

**问题**: Skill 没有关于何时使用开放 vs 封闭 CO₂ 系统的指导文档。AMD 中和通常为开放系统（与大气交换），但地下水中和可能是封闭系统。

**建议**: 在 references 中添加 CO₂ 系统选择指南。

## 输出文件

- `input.pqi` — PHREEQC 输入文件
- `output.qpo` — PHREEQC 标准输出
- `selected_output.txt` — 101 行 × 20 列步进数据
- `results.json` — 结构化结果
- `charts/ph_titration.png` — pH 滴定曲线
- `charts/precipitation_curves.png` — pH + 沉淀曲线
- `charts/element_totals.png` — 元素总浓度变化
- `charts/si_evolution.png` — 饱和指数演变
