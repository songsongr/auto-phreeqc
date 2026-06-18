# 考题 2.1: Cd 吸附 pH 边 — Goethite + Birnessite (2026-05-11)

## 模拟参数

| 参数 | 值 |
|------|-----|
| 模拟类型 | 表面络合 + pH 参数扫描 (REACTION 滴定法) |
| pH 范围 | 3.0 → 9.0 (30 步 NaOH 滴定) |
| 吸附剂 | 0.1g 铁锰结核粉末 (Goethite 20% + Birnessite 20%) |
| Goethite | 0.02g, SSA 50 m²/g, 3.0 sites/nm², pKa 9.0 |
| Birnessite | 0.02g, SSA 600 m²/g, strong 5%/weak 95%, pKa 2.5/5.0 |
| 溶液体积 | 25mL (`-water 0.025`) |
| Cd 浓度 | 100 μg/L (8.9×10⁻⁷ mol/kgw) |
| 背景电解质 | NaNO₃ 0.01 M |
| 数据库 | phreeqc.dat（表面物种为自定义添加） |

## 关键结果

### 吸附边特征

| pH | Cd Sorbed % | 主导吸附位点 |
|----|-------------|-------------|
| 3.00 | 0.00% | (全部 Cd²⁺(aq)) |
| 3.96 | 27.87% | Mn_wOCd⁺ (49%) + Mn_sOCd⁺ (39%) |
| 4.54 | 84.35% | Mn_wOCd⁺ (47%) + Mn_sOCd⁺ (37%) |
| 5.23 | 99.12% | Mn_wOCd⁺ (56%) + Mn_sOCd⁺ (44%) |
| 9.03 | 100.00% | Mn_wOCd⁺ (56%) + Mn_sOCd⁺ (44%) |

- **半吸附 pH (pH₅₀)**: ~4.54
- **完全吸附**: pH > 5.5 时 >99.9%
- **吸附边陡峭**: 84% 吸附率变化发生在 pH 3.6–5.2 (ΔpH = 1.6)

### 矿物贡献分析

- **Birnessite 绝对主导**: Mn 位点吸附 Cd 占总吸附的 >99.9%（全 pH 范围）
- **Goethite 贡献可忽略**: Gth_sOCd⁺ 摩尔分数 < 10⁻³
- **原因**: Birnessite PZC ≈ 2.5（酸性），在 pH > 3 时始终带负电；Goethite PZC ≈ 9.0（碱性），在中性以下带正电排斥 Cd²⁺

## PHREEQC 输入文件结构

```
TITLE Cd adsorption edge on Goethite + Birnessite (pH 3-9)

SURFACE_MASTER_SPECIES
    Gth_s   Gth_sOH
    Mn_s    Mn_sOH
    Mn_w    Mn_wOH

SURFACE_SPECIES
    # Goethite: pKa 9.0, Cd logK 1.0
    Gth_sOH = Gth_sOH                log_k 0.0
    Gth_sOH + H+ = Gth_sOH2+         log_k 9.0
    Gth_sOH = Gth_sO- + H+           log_k -9.0
    Gth_sOH + Cd+2 = Gth_sOCd+ + H+  log_k 1.0
    # Birnessite strong: pKa 2.5/5.0, Cd logK -1.0
    Mn_sOH = Mn_sOH                  log_k 0.0
    Mn_sOH + H+ = Mn_sOH2+           log_k 2.5
    Mn_sOH = Mn_sO- + H+             log_k -5.0
    Mn_sOH + Cd+2 = Mn_sOCd+ + H+    log_k -1.0
    # Birnessite weak: pKa 2.5/5.0, Cd logK -2.5
    Mn_wOH = Mn_wOH                  log_k 0.0
    Mn_wOH + H+ = Mn_wOH2+           log_k 2.5
    Mn_wOH = Mn_wO- + H+             log_k -5.0
    Mn_wOH + Cd+2 = Mn_wOCd+ + H+    log_k -2.5

SOLUTION 1
    units mol/kgw
    -water 0.025
    pH    3.0
    pe    4.0
    Na    0.01
    N(5)  0.01
    Cd    8.9e-7

SURFACE 1
    Gth_sOH  5e-6  50  0.02
    Mn_sOH   5e-6  600 0.02
    Mn_wOH   2e-4

REACTION 1
    NaOH 1.0
    1.2e-4 moles in 30 steps

SELECTED_OUTPUT
    -file selected_output.txt
    -reset true
    -pH
    -totals Cd
    -molalities Gth_sOCd+
    -molalities Mn_sOCd+
    -molalities Mn_wOCd+
    -molalities Cd+2

END
```

## 关键技术要点

### 1. pH 扫描方法: REACTION 滴定优于 Fix_H+
- **Fix_H+ 失败原因**: phreeqc.dat 不含 HCl/NaOH 相定义；与水活度迭代冲突
- **REACTION 法优点**: 物理意义清晰（模拟 NaOH 滴定），数值稳定，自动产生平滑 pH 梯度
- **NaOH 用量的确定**: 须大于溶液 H⁺ 量（pH 3 时 2.5×10⁻⁵ mol/0.025kg）以克服表面位点脱质子缓冲。经验公式: N(NaOH) ≈ 0.7×N(表面位点) + N(溶液 H⁺)

### 2. 非默认水量的影响
- `-water 0.025` → 所有浓度仍以 mol/kgw 为单位，但总摩尔数缩小 40×
- REACTION 的绝对摩尔数须相应调小（与水量成正比）
- PHREEQC `units` 默认是 mmol/kgw，必须显式指定 `units mol/kgw`

### 3. 自定义 SURFACE_SPECIES 的注意事项
- `SURFACE_MASTER_SPECIES` 和 `SURFACE_SPECIES` 必须在 `END` 之前定义
- 位点密度单位: mol/m²（不是 sites/nm²）
- 多组分 SURFACE 块: 后续行复用前行的 SSA 和 mass

### 4. 吸附率计算
- 推荐使用质量平衡法: sorbed / (sorbed + aq) × 100
- 避免依赖 `-totals` 列: REACTION 稀释会导致 `-totals` 值漂移

## 暴露的 skill 薄弱点

1. **generate_input.py 无 SURFACE 支持** → 已修复: 添加 `generate_surface_master_species_block()`, `generate_surface_species_block()`, `generate_surface_block()`, `generate_phases_block()`
2. **generate_solution_block() 无 `-water` 参数** → 暂时使用手动构造 SOLUTION 块
3. **PHREEQC 默认单位 mmol/kgw 易被忽略** → coordinator 中显式使用 `units mol/kgw`
4. **Fix_H+ pH 固定方法不可靠** → 改用 REACTION 滴定法
5. **parse_selected_output 返回值是 dict 不是 tuple** → coordinator 中需要适配

## 输出文件

- 输入: `workspace/task2_1_cd_adsorption/input.pqi`
- 输出: `workspace/task2_1_cd_adsorption/output.qpo`
- 数据: `workspace/task2_1_cd_adsorption/selected_output.txt`
- 结果: `workspace/task2_1_cd_adsorption/results.json`
- 图表: `workspace/task2_1_cd_adsorption/charts/cd_adsorption_edge.png`
- 文献参数: `.claude/skills/phreeqc-auto/references/goethite_birnessite_surface_params.md`
