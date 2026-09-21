# Coordinator 运行示例

本文档记录两次成功运行的 coordinator 脚本，作为后续模拟的参考模板。

## 示例 1: 海水 Speciation

**目录**: `workspace/seawater_speciation_001/`
**用途**: 标准海水 (ex1) 的物种分布计算，关注方解石和文石的饱和指数

### 参数
```python
# 海水组分 (ppm)
components = {
    "Ca": 412.3, "Mg": 1291.8, "Na": 10768.0, "K": 399.1,
    "Cl": 19353.0, "S(6)": 2712.0, "Alkalinity": 141.682,
    "Br": 67.3, "Sr": 13.3, "F": 1.3, "B": 4.9, "Si": 4.2,
}
solution = {"id": 1, "units": "ppm", "temp": 25.0, "pH": 8.2,
            "pe": 8.451, "density": 1.023, "components": components}
```

### 运行
```bash
cd <project_root>
PYTHONIOENCODING=utf-8 python workspace/seawater_speciation_001/run_coordinator.py
```

### 输出
- `input.pqi` — PHREEQC 输入文件
- `output.qpo` — 完整输出（含 74 个物种分布 + 27 个矿物 SI）
- `results.json` — 结构化解析结果
- `charts/saturation_indices.png` — 饱和指数柱状图

### 关键结果
```
Calcite:    SI = +0.85  (过饱和)
Aragonite:  SI = +0.70  (过饱和)
Dolomite:   SI = +2.58  (过饱和)
Quartz:     SI = -0.09  (接近平衡)
```

### 结构亮点
- 使用 `generate_single_simulation()` 生成单步输入
- 调用 `run_simulation(cwd=WORKSPACE)` 确保 SELECTED_OUTPUT 写入工作目录
- 从主输出文件解析 SI + 物种 + 元素浓度

---

## 示例 2: 海水 pH 扫描 (海洋酸化模拟)

**目录**: `workspace/ph_sweep_001/`
**用途**: 对标准海水 pH 7.5 → 8.5 扫描（步长 0.1，共 11 步），观察碳酸盐矿物 SI 变化

### 参数
```python
# 海水组分同 ex1 (同上)
ph_values = [7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5]
base_params = {
    "solution": { ... },  # 同示例 1
    "selected_output": {
        "si": ["Calcite", "Aragonite", "Dolomite", "Quartz", "Chalcedony"],
        "totals": ["Ca", "Mg", "Na", "Cl", "C", "S"],
        "pH": True,
    },
}
```

### 运行
```bash
cd <project_root>
PYTHONIOENCODING=utf-8 python workspace/ph_sweep_001/coordinator.py
```

### 输出
- `input.pqi` — 多步 PHREEQC 输入（11 个 END 分隔的 simulation block）
- `output.qpo` — 完整输出（11 个 SI 阶段）
- `step_1.txt` ~ `step_11.txt` — 每步 SELECTED_OUTPUT（含 pH, SI, totals）
- `results.json` — 结构化解析结果
- `charts/ph_sweep.png` — SI-pH 线图

### 关键结果
```
pH    Calcite SI    Aragonite SI
7.5     +0.20         +0.06
7.6     +0.30         +0.16
7.7     +0.39         +0.25
7.8     +0.49         +0.34
7.9     +0.58         +0.44
8.0     +0.67         +0.53
8.1     +0.76         +0.62
8.2     +0.85         +0.70
8.3     +0.93         +0.78
8.4     +1.01         +0.86
8.5     +1.08         +0.94
```

### 结构亮点
- 使用 `generate_parameter_sweep()` 生成多步扫描输入
- `output_dir="."` 配合 `cwd=WORKSPACE` 实现 SELECTED_OUTPUT 可控输出
- 主输出文件按 `"Beginning of initial solution calculations"` 分段提取各步 SI
- 使用 `plot_selected_output_sweep()` 或自定义 matplotlib 绘制 SI-pH 曲线

---

## Coordinator 通用最佳实践

```python
# 1. 环境设置
os.environ["PHREEQC_EXE"] = "..."   # 可选，自动查找
os.environ["PHREEQC_DATABASE"] = "..."  # 可选，自动查找

# 2. 工作目录
WORKSPACE = os.path.dirname(os.path.abspath(__file__))

# 3. 运行 PHREEQC (关键: cwd=WORKSPACE)
result = run_simulation(
    input_file=os.path.join(WORKSPACE, "input.pqi"),
    output_file=os.path.join(WORKSPACE, "output.qpo"),
    database=find_database("phreeqc.dat"),
    cwd=WORKSPACE,  # <-- 确保 SELECTED_OUTPUT 写入工作目录
)

# 4. 从主输出解析 (推荐)
output_text = open(os.path.join(WORKSPACE, "output.qpo")).read()
si_data = extract_saturation_indices(output_text)

# 5. Windows 中文终端
# 运行: PYTHONIOENCODING=utf-8 python coordinator.py
```
