# Goethite & Birnessite Cd²⁺ 表面络合参数

## 来源

| 矿物 | 模型 | 主要文献 | DOI |
|------|------|---------|-----|
| Goethite | CD-MUSIC / DLM | Hiemstra & Van Riemsdijk (1996) | 10.1006/jcis.1996.0242 |
| Goethite | Cd²⁺ DLM | Venema et al. (1996) | 10.1006/jcis.1996.0097 |
| Goethite | Cd²⁺ 吸附边 | Mustafa et al. (2004) | 10.1016/j.jcis.2004.01.017 |
| Birnessite | Cd²⁺ DLM | Tonkin et al. (2004) | 10.1016/S0883-2927(03)00118-5 |
| Birnessite | 替代参数化 | Appelo & Postma (1999) | 10.1016/S0016-7037(99)00205-7 |

## 状态

PHREEQC 所有标准数据库（phreeqc.dat, wateq4f.dat, minteq.v4.dat 等）均**不含** Goethite 或 Birnessite 的 SURFACE_SPECIES 定义。两者仅以矿物相 (PHASES) 存在。需在输入文件中自定义 SURFACE_MASTER_SPECIES + SURFACE_SPECIES 数据块。

## Goethite (α-FeOOH)

### 物理化学性质
| 参数 | 值 | 说明 |
|------|-----|------|
| 比表面积 (SSA) | 50–100 m²/g | 依赖合成方法；Venema et al. 用 94.5 m²/g |
| 零点电荷 (PZC) | 9.0–9.4 | 偏碱性 |
| 表面位点密度 | ~3.0 sites/nm² | CD-MUSIC 晶面模型 |
| 位点密度 (mol/m²) | ~5.0×10⁻⁶ | 简化为单一 ≡FeOH 位点 |
| pKa1 / pKa2 (DLM) | 9.0 / -9.0 | 两性质子化/去质子化 |

### Cd²⁺ 吸附
- **反应**: ≡FeOH + Cd²⁺ = ≡FeOCd⁺ + H⁺
- **log K (DLM)**: ≈ **1.0**
- **条件**: 0.01–0.1 M NaNO₃, 25°C

### PHREEQC 输入定义
```
SURFACE_MASTER_SPECIES
    Gth_s   Gth_sOH

SURFACE_SPECIES
    Gth_sOH = Gth_sOH
        log_k 0.0
    Gth_sOH + H+ = Gth_sOH2+
        log_k 9.0
    Gth_sOH = Gth_sO- + H+
        log_k -9.0
    Gth_sOH + Cd+2 = Gth_sOCd+ + H+
        log_k 1.0

SURFACE 1
    Gth_sOH  5e-6  50.0  0.02
```

## Birnessite (δ-MnO₂)

### 物理化学性质
| 参数 | 值 | 说明 |
|------|-----|------|
| 比表面积 (SSA) | 600–750 m²/g | Tonkin et al. (2004) |
| 零点电荷 (PZC) | 1.5–3.0 | **强酸性**氧化物 |
| 总位点密度 | ~0.3 mol/mol Mn | 双位点模型 |
| 强位点比例 | 5% | ≡Mn_sOH |
| 弱位点比例 | 95% | ≡Mn_wOH |
| pKa1 / pKa2 (DLM) | 2.5 / -5.0 | 远低于 Fe 氧化物 |

### Cd²⁺ 吸附
- **强位点**: ≡Mn_sOH + Cd²⁺ = ≡Mn_sOCd⁺ + H⁺, **log K ≈ -1.0**
- **弱位点**: ≡Mn_wOH + Cd²⁺ = ≡Mn_wOCd⁺ + H⁺, **log K ≈ -2.5**
- **条件**: 0.01 M NaNO₃, 25°C

### PHREEQC 输入定义
```
SURFACE_MASTER_SPECIES
    Mn_s   Mn_sOH
    Mn_w   Mn_wOH

SURFACE_SPECIES
    Mn_sOH = Mn_sOH
        log_k 0.0
    Mn_sOH + H+ = Mn_sOH2+
        log_k 2.5
    Mn_sOH = Mn_sO- + H+
        log_k -5.0
    Mn_sOH + Cd+2 = Mn_sOCd+ + H+
        log_k -1.0
    Mn_wOH = Mn_wOH
        log_k 0.0
    Mn_wOH + H+ = Mn_wOH2+
        log_k 2.5
    Mn_wOH = Mn_wO- + H+
        log_k -5.0
    Mn_wOH + Cd+2 = Mn_wOCd+ + H+
        log_k -2.5

SURFACE 1
    Mn_sOH   5e-6   600.0  0.02
    Mn_wOH   2e-4
```

## 关键矿物学差异

| 特性 | Goethite | Birnessite |
|------|----------|------------|
| PZC | ~9.0 (碱性) | ~2.5 (酸性) |
| 低 pH (3-5) 吸附 | 弱 — 表面带正电 | **强** — 表面带负电 |
| 高 pH (7-9) 吸附 | **强** — 表面带负电 | 极强 — 显著负电 |
| Cd 结合强度 | 中等 (log K ~1.0) | 更强 (强位点 log K ~-1.0) |
| SSA | 50 m²/g | 600 m²/g |

## 使用注意事项

1. **电容模型**: 本参数采用扩散层模型 (DLM)，未包含 Stern 层电容。若需 CD-MUSIC (Triple Layer)，需额外定义 C₁, C₂。
2. **离子强度**: DLM 参数在 0.01 M 离子强度下拟合。更高离子强度时需使用活度系数修正或 TLM。
3. **氧化还原**: Birnessite 的 Mn 平均氧化度影响表面电荷。假定 Mn(IV) 为主。
4. **不确定性**: log K 值主要来源于单一研究组的拟合，系统间不确定性约 ±0.5 log 单位。
5. **竞争离子**: 本参数仅适用于 Cd²⁺。若有 Ca²⁺、Mg²⁺、Zn²⁺ 等竞争离子，需添加额外 SURFACE_SPECIES。
