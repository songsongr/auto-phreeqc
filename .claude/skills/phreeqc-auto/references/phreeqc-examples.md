# PHREEQC 输入模板参考

本文件提供常见模拟场景的 PHREEQC 输入模板，供输入生成 Agent 参考。

## 1. 海水 Speciation（完整示例）

```
TITLE Speciation of seawater with uranium.
SOLUTION 1 SEAWATER
    units ppm
    pH 8.22
    pe 8.451
    temp 25.0
    density 1.023
    Ca 412.3
    Mg 1291.8
    Na 10768.0
    K 399.1
    Cl 19353.0
    Alkalinity 141.682 as HCO3
    S(6) 2712.0
    U 3.3
SELECTED_OUTPUT 1
    -file selected.txt
    -pH pe
    -si calcite dolomite
    -totals Ca Mg U
END
```

## 2. 批反应 — 矿物溶解/沉淀

```
TITLE Batch reaction: Calcite dissolution.
SOLUTION 1
    units mol/kgw
    pH 7.0
    pe 4.0
    temp 25.0
    Ca 0.001
    C(4) 0.001
EQUILIBRIUM_PHASES 1
    Calcite 0.0 10.0
    CO2(g) -1.5 10.0
SELECTED_OUTPUT 1
    -file selected.txt
    -pH pe
    -si calcite dolomite
    -totals Ca C
END
```

## 3. 参数扫描结构（pH 扫描）

```
# Each step is a separate simulation
SOLUTION 1
    units mol/kgw
    pH 6.0
    pe 4.0
    temp 25.0
    Ca 0.001
SELECTED_OUTPUT 1
    -file step_001.txt
    -pH
    -si calcite
    -totals Ca
END

SOLUTION 2
    units mol/kgw
    pH 7.0
    pe 4.0
    temp 25.0
    Ca 0.001
SELECTED_OUTPUT 1
    -file step_002.txt
    -pH
    -si calcite
    -totals Ca
END
END
```

## 4. 气体平衡

```
SOLUTION 1
    units mol/kgw
    pH 7.0
    temp 25.0
    Na 0.1
    Cl 0.1
GAS_PHASE 1
    -fixed_pressure
    -pressure 1.0
    CO2(g) 0.0003
SELECTED_OUTPUT 1
    -file selected.txt
    -pH
    -si calcite
    -totals C
END
```

## 5. 动力学反应

```
SOLUTION 1
    units mol/kgw
    pH 7.0
    temp 25.0
    Ca 0.0
KINETICS 1
    Calcite
    -m0 0.1
    -parms 100 1
RATES 1
    Calcite
    -start
    10 rem rate = k * (1 - SR)
    20 k = 10
    30 sr = SR("Calcite")
    40 rate = k * (1 - sr) * 1e-9
    50 moles = rate * TIME
    60 save moles
    -end
SELECTED_OUTPUT 1
    -file selected.txt
    -pH
    -si calcite
    -totals Ca
END
```

## 6. 一维反应溶质运移 (TRANSPORT)

```
TITLE 1D transport of As(V) through a sediment column.

# --- Inlet solution (SOLUTION 0 = boundary condition) ---
SOLUTION 0
    units ppm
    pH 7.0
    pe 12.0
    temp 25.0
    As 1.0    # 1 ppm As(V)

# --- Initial pore water in each cell ---
SOLUTION 1-20
    units mol/kgw
    pH 7.0
    pe 12.0
    temp 25.0

# --- Transport parameters ---
TRANSPORT
    -cells 20
    -length 1.0
    -shifts 100
    -time_step 0.05 day
    -flow_direction forward
    -dispersivity 0.01
    -correct_disp true
    -punch_cells 20
    -punch_frequency 1
    -print_cells 1-20
    -print_frequency 100

SELECTED_OUTPUT
    -file selected.txt
    -step true
    -pH
    -totals As

END
```

### TRANSPORT 参数速查

| 参数 | 说明 | 典型值 |
|------|------|--------|
| `-cells` | 单元数 | 20-100（越多曲线越光滑） |
| `-length` | 柱长 (m) | 0.1-10.0 |
| `-shifts` | 时间步数 | 100-1000 |
| `-time_step` | 步长 + 单位 | 0.05 day（= 1.2 hr） |
| `-flow_direction` | 流向 | forward / backward / diffusion_only |
| `-dispersivity` | 弥散度 (m) | 0.01 - 0.1 × cell_length |
| `-correct_disp` | 曲折度修正 | true / false |
| `-punch_cells` | 输出单元 | 最后一个单元（出口） |
| `-punch_frequency` | 输出频率 (shifts) | 1（每步都输出） |

### 稳定性条件
- **Courant number** << 1: `time_step × velocity / cell_length` < 1
- 对于 20 cells, 1m, 1m/d: cell_length = 0.05m, time_step = 0.05d → Courant = 1.0
- 建议 Courant ≤ 0.5-1.0 以避免数值振荡

## 7. 常用数据库及适用场景

| 数据库 | 适用场景 |
|--------|----------|
| phreeqc.dat | 一般用途（源自 PHREEQE） |
| wateq4f.dat | 天然水（低温环境） |
| llnl.dat | 高温地球化学（源自 EQ3/6） |
| minteq.dat | 环境/污染（源自 MINTEQA2） |
| pitzer.dat | 高离子强度（盐水、海水） |
| sit.dat | SIT 活度模型（中等离子强度） |
| iso.dat | 同位素分馏计算 |

## 8. 常用矿物化学式和 SI 查询名

| 矿物 | 化学式 | PHREEQC 查询名 |
|------|--------|----------------|
| 方解石 | CaCO3 | Calcite |
| 白云石 | CaMg(CO3)2 | Dolomite |
| 石膏 | CaSO4·2H2O | Gypsum |
| 硬石膏 | CaSO4 | Anhydrite |
| 石英 | SiO2 | Quartz |
| 非晶硅 | SiO2 | Chalcedony |
| 黄铁矿 | FeS2 | Pyrite |
| 赤铁矿 | Fe2O3 | Hematite |
| 针铁矿 | FeOOH | Goethite |
