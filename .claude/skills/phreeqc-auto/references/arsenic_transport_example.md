# 考题 3.2: 一维反应溶质运移 (As 穿透曲线)

**日期**: 2026-05-12 | **数据库**: phreeqc.dat + custom As definition

## 题目要求

设定一个 1 米长的沉积物柱，初始充满去离子水。以 1m/d 的速度流过含 1ppm 砷 (As) 的溶液，计算 5 天后砷在柱体出口的穿透曲线。

## 关键参数

| 参数 | 值 | 推理依据 |
|------|------|----------|
| 柱长 | 1.0 m | 题目指定 |
| 单元格数 | 20 | 内存效率与精度平衡，Pe_cell 约 5 |
| 单元长度 | 0.05 m | length / cells |
| 达西流速 | 1.0 m/d | 题目指定 |
| 时间步长 | 0.05 day (1.2 hr) | dt = dx/v = 0.05/1.0 |
| 总时间 | 5.0 day | 题目指定 |
| 运行步数 | 100 | total_time / dt |
| 弥散度 | 0.01 m | 实验室柱典型值，Pe_cell = 5 |
| 背景电解质 | NaCl (10+15 ppm) | 占位离子强度 ~4.9e-4 M |
| 初始溶液 | 去离子水 (pH=7) | 柱体初始条件 |
| 入口 As 浓度 | 1 ppm (1.335e-5 mol/kgw) | 题目指定 |
| 数据库 | phreeqc.dat | 默认但需自定义 As 主物种 |
| pH | 7.0 | 中性环境 [自动推理] |
| pe | 12.0 | 氧化环境 (有氧地下水) [自动推理] |

## 模拟方法

### 非保守示踪法

由于 **phreeqc.dat 不包含 As 主物种**，需要在输入文件中手动定义：

```
SOLUTION_MASTER_SPECIES
    As    AsO4-3    0.0    As    74.9216

SOLUTION_SPECIES
    AsO4-3 = AsO4-3
    log_k    0.0
```

As(V) 以 `AsO4-3` 作为主物种，不定义任何络合反应 → 纯保守示踪剂行为。

### 坐标脚本结构

```python
# Step 1: 自定义 As 定义 + 生成输入文件
as_block = """SOLUTION_MASTER_SPECIES
    As    AsO4-3    0.0    As    74.9216
SOLUTION_SPECIES
    AsO4-3 = AsO4-3
    log_k    0.0
"""

params = {
    "solutions": [{"id": 0, "units": "ppm", ...}],
    "initial_cell_solution": {"units": "mol/kgw", ...},
    "transport": {
        "cells": 20, "length": 1.0, "shifts": 100,
        "time_step": 0.05, "time_units": "day",
        "dispersivity": 0.01,
        "punch_cells": [20], "punch_frequency": 1,
    },
    "selected_output": {"step": True, "totals": ["As", "Na", "Cl"]},
}
content = as_block + "\n\n" + generate_single_simulation(params, ...)

# Step 2: 运行 PHREEQC
run_simulation(input_file, output_file, database, cwd=WORKSPACE)

# Step 3: 解析 SELECTED_OUTPUT 获取突破数据
selected = parse_selected_output("selected_output.txt")
transp_rows = [r for r in selected["data"] if r[1] == 'transp']

# Step 4: 绘制穿透曲线
plot_breakthrough_curve(selected, time_column="step", conc_column="As", ...)
```

### PHREEQC 输入结构

```
SOLUTION_MASTER_SPECIES      # [!] 仅 phreeqc.dat 需要
    As    AsO4-3  0  As  74.9
SOLUTION_SPECIES
    AsO4-3 = AsO4-3
    log_k 0.0

SOLUTION 0  (inlet: 1 ppm As + NaCl)
SOLUTION 1-20  (cells: DI water)
TRANSPORT
SELECTED_OUTPUT  (-step true, -totals As)
END
```

## 关键结果

| 指标 | 值 | 意义 |
|------|-----|------|
| 入口 As 浓度 | 1.335e-05 mol/kgw | 1 ppm As 完全正确 |
| Courant 数 | 1.0 | 临界稳定 |
| 首次穿透 | ~step 17 (0.85 day) | 约 0.85 PV |
| 1 PV ~ step 20 | 84% C/C0 | 因弥散导致不完全穿透 |
| 完全穿透 | ~step 28 (1.4 day, 1.4 PV) | 保守示踪剂无延迟 |
| Na/Cl 对比 | 完全一致 | 验证 As 为纯保守行为 |

### 突破曲线特征

```
         C/C0
         1.0 |'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
             |                                                                                        
         0.8 |                                                      .,--''''''''''''''''''            
             |                                                ,.-''''''''''                           
         0.6 |                                           ,.-''''                                      
             |                                      ,.-''''                                          
         0.5 |------------------------------------+---''''----0.5PV midpoint                          
             |                                 ,.-''''                                               
         0.4 |                              ,.''''                                                   
             |                         ,.-''''                                                       
         0.2 |                    ,.-''''                                                            
             |              ,.-''''                                                                  
         0.0 |,,,,,,,,,,,,.''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
             0        5        10       15       20       25       30       35       40       45  step
```

## Skill 扩展：新增功能

本次实现新增以下功能到 skill 脚本：

### 1. `generate_input.py`: `generate_transport_block()`

支持 TRANSPORT 关键词块生成，参数包括：
- `cells`, `length`, `shifts`, `time_step`, `time_units`
- `flow_direction`, `dispersivity`, `correct_disp`
- `punch_cells`, `punch_frequency`, `print_cells`, `print_frequency`

### 2. `generate_input.py`: TRANSPORT 自动处理

`generate_single_simulation()` 中新增 transport 模式：
- `"solutions"` 中包含 `id=0` 作为入口边界条件
- `"initial_cell_solution"` 模板自动生成 `SOLUTION 1..N`
- `transport.cells` 决定自动生成的单元数量
- `selected_output.step` 在 transport 模式下默认 `True`

### 3. `visualize.py`: `plot_breakthrough_curve()`

穿透曲线专用绘图函数：
- 支持单列 (`conc_column`) 或多列 (`conc_columns`) 对比
- 自动检测 x 列 (`time_column`)
- 标注 C/C0 = 0.5 参考线

### 4. 参考文档更新
- `references/phreeqc-examples.md` 新增 Section 6: TRANSPORT 模板 + 参数速查
- `SKILL.md` 新增生成器 API: 一维传输模拟 (TRANSPORT) 小节

## 已知问题与对策

### phreeqc.dat 不含 As 主物种

**症状**: `WARNING: Could not find element in database, As. Concentration is set to zero.`
**解决**: 在 input 文件中手动添加 `SOLUTION_MASTER_SPECIES` / `SOLUTION_SPECIES` 块

底层成因: phreeqc.dat (源自 PHREEQE) 仅包含基本元素 (Ca, Mg, Na, K, Fe, Mn, Al, Si, Cl, C, S, N, P, F, Br, Li, Zn, Cd, Pb, Cu)。As 等重金属/类金属需在输入中自定义。

**候选数据库**:
- `llnl.dat` — 含完整 As 热力学数据 (As(-3), As(+3), As(+5)), 推荐用于反应性运移
- `minteq.dat` — 含 As 物种和环境污染物数据, 但不如 llnl.dat 全面
- 自定义 → 在 input 文件中手动添加 (推荐用于保守示踪)

### As 反应性运移扩展

当前实现为保守示踪剂，如需模拟 As 的吸附/反应行为：

1. **HFO (Hydrous Ferric Oxide) 表面络合**: 
   - Dzombak & Morel 模型参数
   - 两种位点: Hfo_s (强位, 0.005 mol/mol Fe) + Hfo_w (弱位, 0.2 mol/mol Fe)
   - As(V) 在 HFO 上有强吸附，pH 4-8 吸附率 > 90%
   
2. **含铁矿物共存**:
   - 针铁矿 (Goethite)、赤铁矿 (Hematite) 是常见 As 吸附剂
   - 需定义 SURFACE_MASTER_SPECIES / SURFACE_SPECIES / SURFACE

3. **数据库选择**:
   - 使用 `llnl.dat` + `minteq.dat` 表面络合参数
   - 或从文献中提取 HFO-As 络合常数

### TRANSPORT 稳定性条件

- **Courant 数** = v × dt / dx < 1
- 20 cells, 1m, 1m/d: dx = 0.05m, dt_max = 0.05 day → Courant = 1.0
- Courant > 1 导致数值振荡, 解决方案: 增加细胞数或减少 dt
- **Peclet 数(细胞)**: Pe_cell = dx / α (α = dispersivity)
- Pe_cell >> 1 导致数值振荡, 建议 Pe_cell ≤ 10
- Pe_cell = 0.05/0.01 = 5 → 安全范围, 曲线适度展宽

## 与其他考题的关联

| 考题 | 关联点 | 共享技术 |
|------|--------|----------|
| 考题 2.1 (Cd 吸附) | 重金属吸附模型 | SURFACE 块 + HFO 参数 |
| 考题 3.1 (黄铁矿动力学) | 反应速率与传输耦合 | KINETICS + TRANSPORT |
| 考题 3.3 (CO2 注入) | 多相流传输 | TRANSPORT + GAS_PHASE |
