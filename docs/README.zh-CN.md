# auto-phreeqc 🔬

[English](../README.md)

[![CI](https://github.com/songsongr/auto-phreeqc-public/actions/workflows/ci.yml/badge.svg)](https://github.com/songsongr/auto-phreeqc-public/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)

`auto-phreeqc` 是面向 PHREEQC 的用户端工具集：提供可复用的 Python
运行库、本地浏览器工作台、九个可复现实例，以及适用于 Claude Code 和
Codex 的简明使用指南。

PHREEQC 本体由美国地质调查局（USGS）开发，可用于水化学形态分析、批量
反应、反应性运移和反演地球化学计算。

## 包含内容

- `phreeqc_auto/`：生成 PHREEQC 输入、定位安装、运行模拟、解析结果与
  绘图的公开 Python 包。
- `workbench/`：在浏览器中编辑、启动并查看模拟的本地工作台。
- `examples/`：九个由浅入深的可运行示例。
- `skills/phreeqc-auto/`：不包含开发提示词的精简用户 Skill；安装方式见
  [智能体使用指南](agent-usage.md)。

## 快速开始

```bash
git clone https://github.com/songsongr/auto-phreeqc-public.git
cd auto-phreeqc-public
python -m pip install -e ".[dev]"
```

在运行前配置本机 PHREEQC：

```bash
# macOS / Linux
export PHREEQC_EXE="/path/to/phreeqc"
export PHREEQC_DATABASE="/path/to/phreeqc.dat"

# Windows PowerShell
$env:PHREEQC_EXE = "C:\\path\\to\\phreeqc.exe"
$env:PHREEQC_DATABASE = "C:\\path\\to\\phreeqc.dat"
```

运行库会优先使用这些环境变量，其次查找 `PATH` 和常见安装位置。仓库不
包含 PHREEQC 可执行程序或数据库文件。

### Python 调用

```python
from pathlib import Path

from phreeqc_auto.generate_input import generate_single_simulation, write_input_file
from phreeqc_auto.run_phreeqc import run_simulation

run_dir = Path("runs/calcite")
params = {
    "solution": {
        "id": 1,
        "units": "mg/L",
        "temp": 25.0,
        "pH": 7.2,
        "components": {"Ca": 80, "Alkalinity": "200 as CaCO3"},
    },
    "selected_output": {"pH": True, "si": ["Calcite"], "totals": ["Ca"]},
}

input_file = write_input_file(
    generate_single_simulation(params, output_file="selected_output.txt"),
    str(run_dir / "input.pqi"),
)
result = run_simulation(
    input_file,
    output_file=str(run_dir / "output.qpo"),
    cwd=str(run_dir),
)
print(result["success"], result["error"])
```

运行自动化测试：

```bash
python -m pytest tests -v
```

## 本地 Web Workbench

```bash
# Windows
.\start.windows.bat

# macOS / Linux / Git Bash
./start.unix.sh
```

随后访问 <http://127.0.0.1:8765/>。工作台使用相同的公开
`phreeqc_auto` 运行库，不需要安装 AI 助手也可正常使用。更多说明见
[工作台指南](workbench-README.zh-CN.md)。

## 九个示例

| 级别 | 示例 | 目录 |
| --- | --- | --- |
| L1 | Pb 形态分布 | `examples/task1_1_pb_speciation/` |
| L1 | 方解石饱和指数 | `examples/task1_2_calcite_si/` |
| L1 | 海水混合 | `examples/task1_3_SimpleMix/` |
| L2 | Cd 吸附边 | `examples/task2_1_cd_adsorption/` |
| L2 | AMD 石灰石中和 | `examples/task2_2_amd_neutralization/` |
| L2 | 阳离子交换 | `examples/task2_3_cation_exchange/` |
| L3 | 黄铁矿动力学 | `examples/task3_1_pyrite_kinetics/` |
| L3 | 砷反应性运移 | `examples/task3_2_as_transport/` |
| L3 | CO₂ 注入 | `examples/task3_3_co2_injection/` |

每个目录都保留了可直接执行的协调脚本与预期产物，适合作为构建自身模型的
起点。

## 更多资料

- [智能体使用指南](agent-usage.md)
- [英文说明](../README.md)
- [贡献指南](../CONTRIBUTING.md)
- [安全策略](../SECURITY.md)
