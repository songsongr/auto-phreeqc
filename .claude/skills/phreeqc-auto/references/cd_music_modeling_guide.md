# CD-MUSIC 模型 PHREEQC 实现指南

> 基于: Hiemstra & Van Riemsdijk (1996) JCIS 179, 488-508 复现经验 (2026-06-04)

## 一、PHREEQC CD-MUSIC 语法速查

### SURFACE_MASTER_SPECIES (带分数电荷!)

```phreeqc
SURFACE_MASTER_SPECIES
    Goe_uni   Goe_uniOH-0.5    # 单配位位点, 分数电荷 -0.5
    Goe_tri   Goe_triO-0.5     # 三配位位点, 分数电荷 -0.5
```

**关键规则**: CD-MUSIC 位点必须带 Pauling 键价分数电荷。不同于 DLM 的中性位点 (Gth_sOH)。

### SURFACE_SPECIES

```phreeqc
SURFACE_SPECIES
    # 主物种 (identity reaction, logK=0)
    Goe_uniOH-0.5 = Goe_uniOH-0.5
        log_k 0.0; -cd_music 0 0 0

    # 质子化 (H+ 全部到 0-平面)
    Goe_uniOH-0.5 + H+ = Goe_uniOH2+0.5
        log_k 9.0; -cd_music 1 0 0

    # 电解质离子对 (Na+ 到扩散层)
    Goe_uniOH-0.5 + Na+ = Goe_uniOHNa+0.5
        log_k -0.5; -cd_music 0 0 1

    # 磷酸根单齿络合物 (3H+ 化学计量)
    Goe_uniOH-0.5 + PO4-3 + 3H+ = Goe_uniPO4H2-0.5 + H2O
        log_k 32.0; -cd_music 0.85 -0.85 0

    # 磷酸根双齿络合物 (2H+)
    2Goe_uniOH-0.5 + PO4-3 + 2H+ = Goe_uni2PO4-2 + 2H2O
        log_k 13.0; -cd_music 0.40 -1.40 0
```

**CD 参数规则**:
- `-cd_music Δz₀ Δz₁ Δz₂` — 三平面电荷分布变化
- **Δz₀ + Δz₁ + Δz₂ = 移动离子的净电荷变化** (如 2H⁺ + PO₄³⁻ → -1)
- 格式错误会导致元素不平衡错误

### SURFACE

```phreeqc
SURFACE 1
    -sites_units density              # 使用位点密度 (sites/nm²)
    Goe_uni  3.45  50.0  5.0          # 密度 SSA(m²/g) 质量(g)
    Goe_tri  2.7                       # 三配位共享 SSA
    -cd_music                          # 激活 CD-MUSIC
    -capacitances 1.1 5.0             # C1(0-1平面) C2(1-d平面) F/m²
    -Donnan 1e-8                      # Donnan 扩散层 (可选)
```

## 二、常见错误及解决

### 错误 1: 元素不平衡
```
ERROR: Equation does not balance for element, H: right - left = -1.0000
```
**原因**: 物种名称中的 H 原子数与反应式不匹配。检查: 反应物总 H = 生成物总 H。
**示例**: Goe_uniOH-0.5 (1H) + 2H⁺ (2H) = Goe_uniPO4H2-0.5 (2H) + H2O (2H) → 3≠4 不平衡!
**修正**: Goe_uniOH-0.5 + PO4-3 + H⁺ = Goe_uniPO4-2.5 + H2O (使用 1H⁺)

### 错误 2: log_k 与 CD 同行
```
ERROR: Elements in species have not been tabulated
```
**原因**: `log_k` 和 `-cd_music` 不能与反应式在同一物理行。
**解决**: 每个关键字独占一行或使用 `;` 分隔。

### 错误 3: Donnan 收敛失败
```
ERROR: Too many iterations in subroutine calc_psi_avg
```
**原因**: 初始 pH 太低 (表面电荷近零)，Donnan 电位计算发散。
**解决**: (a) 提高初始 pH 至 4-5; (b) 去掉 `-Donnan` 使用默认方法。

### 错误 4: 无主物种
```
ERROR: No master species for element Goe_b
```
**原因**: 物种名称不以已知表面位点元素名开头。PHREEQC 从物种名解析元素组成。
**规则**: 所有表面物种名必须以 SURFACE_MASTER_SPECIES 中定义的位点名开头。

## 三、位点容量约束

**SSA=50 m²/g, 5 g/L, 3.45 sites/nm²**:
- 单齿 (1:1 sites:P): 容量 = 1.43 mmol/L / 1.0 mmol/L P = **143%** → 可达到 100% 吸附
- 双齿 (2:1 sites:P): 容量 = 0.72 mmol/L / 1.0 mmol/L P = **72%** → **不足以达到 99.8%**

**论文针铁矿参数 (SSA=105 m²/g)**:
- 单齿容量 = **300%** → 充足
- 双齿容量 = **150%** → 也充足

**教训**: 开始模拟前必须计算位点容量。如果位点不足，需要：
1. 使用更多针铁矿 (更高的 mass 参数)
2. 使用论文报道的 SSA 值 (通常 80-105 m²/g)
3. 确保低 pH 时单齿络合物占优 (1:1 化学计量)

## 四、PHREEQC Donnan vs 论文 TP 模型的静电差异

### 论文方法 (Gouy-Chapman + 固定 C1, C2)
- 三平面电位通过电容方程 + Gouy-Chapman 积分求解
- 高离子强度下扩散层被压缩，|ψ₁| 较小
- 论文 CD 值为键价推导的物理值

### PHREEQC Donnan 方法
- Donnan 平均浓度替代 GC 分布
- 相同条件下 |ψ₁| 可能更大 → 更大的静电惩罚
- 键价推导的 CD 值可能产生过大的静电效应

### 对复现的影响
**论文的 CD 值 (从 f 值推导) 在 PHREEQC 中无法直接使用**, 因为:
1. Donnan 与 GC 静电计算给出不同的平面电位
2. 相同 CD 值产生不同的有效结合常数
3. 需要优化"有效 CD 值"来匹配实验数据

**推荐的复现策略**:
1. 保持论文的 C1, C2, SSA, 位点密度固定
2. 使用论文的络合物种类和化学计量 (H⁺ 数)
3. CD 值可以从论文 f 值出发，但需要允许调整
4. logK 值必须针对 PHREEQC 重新优化

## 五、工作流程建议

### 文献复现任务的标准流程

```
Phase 0 — 论文预处理 (强制，不可跳过)
  □ 获取完整论文 PDF
  □ 提取: SSA, 浓度, 离子强度, PZC, 温度
  □ 提取: 位点密度, C1, C2, f 值/CD 参数
  □ 提取: 络合物种类, 反应式, logK 值范围
  □ 确认: Fig./Table 数据可用于验证
  □ 评估: 位点容量是否充足

Phase 1 — 初始模拟
  □ 从论文参数出发构建 PHREEQC 输入
  □ 运行单点测试 (如 pH=7) 验证可行性
  □ 全 pH 范围扫描观察吸附边形状

Phase 2 — 参数优化 (仅在必要时)
  □ 固定物理锚点 (CD, C1, C2, SSA)
  □ 调整条件参数 (logK) 匹配实验数据
  □ 记录每次调整的理由和效果

Phase 3 — 验证与报告
  □ 计算 MAPE, RMSE, R²
  □ 分析偏差来源 (静电模型差异, 位点容量, etc.)
  □ 生成包含模拟条件和局限性的完整报告
```

## 六、参考参数 (来自文献)

### Hiemstra & Van Riemsdijk (1996) 确认值
| 参数 | 值 | 来源 |
|------|-----|------|
| SSA | 105 m²/g | p.10, 正文 |
| PZC | 9.5 (本实验) / 9.2 (计算平均值) | p.10-12 |
| C1 | 0.9 F/m² | p.12, Fig.6 |
| C2 | 4-5 F/m² | p.15, 正文 |
| logK_H | 9.2-9.5 | 从 PZC 推导 |
| Ns (110面) | 6 nm⁻² | p.11 |
| f(monodentate) | 0.25 | p.14 |
| f(bidentate NP) | 0.50 | p.14 |
| f(bidentate P) | 0.60 | p.14 |

### 最优有效参数 (PHREEQC 优化, MAPE=37%)
| 参数 | 值 |
|------|-----|
| 单齿2H CD | (0.85, -0.85, 0) |
| 单齿1H CD | (0.45, -1.45, 0) |
| 双齿NP CD | (0.40, -1.40, 0) |
| 双齿P CD | (0.50, -0.50, 0) |
| logK 单齿2H | 32 |
| logK 单齿1H | 21 |
| logK 双齿NP | 13 |
| logK 双齿P | 23 |

---

*指南版本: v1.0 — 2026-06-04*
