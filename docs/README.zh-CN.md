# phreeqc-auto 🔬

[English](../README.md)

[![CI](https://github.com/songsongr/auto-phreeqc/actions/workflows/ci.yml/badge.svg)](https://github.com/songsongr/auto-phreeqc/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](../pyproject.toml)

**面向 PHREEQC 的自动化地球化学模拟工作流**，可在任意智能体终端中使用。

> PHREEQC 是由美国地质调查局（USGS）开发的计算机程序，可进行物种组成、批量反应、一维迁移和反演地球化学计算。

本项目提供适合智能体使用、由自然语言驱动的地球化学建模工作流。只需用日常语言描述模拟需求，工作流即可完成输入生成、执行、输出解析与可视化。它可在任意智能体终端中使用；下文以 Codex 和 Claude Code 为例。

---

## ✨ 功能特性

- **🧪 从自然语言到模拟**：用纯文本描述实验，即可得到完整的 PHREEQC 模拟
- **📂 四步流水线**：生成输入 → 运行 PHREEQC → 解析输出 → 结果可视化
- **📊 丰富的可视化**：pH 扫描、滴定曲线、穿透曲线、物种组成饼图和时间序列图
- **📚 9 个经验证的示例工作流**：涵盖三个难度级别，从基础物种组成到反应性迁移
- **🐍 独立 Python 库**：可单独使用 `generate_input.py`、`run_phreeqc.py`、`parse_output.py` 和 `visualize.py`

### 支持的模拟类型

| 类型 | 示例 |
|------|------|
| 物种组成 | 海水中的 Pb 物种组成、碳酸盐体系分析 |
| 批量反应 | 矿物溶解/沉淀、滴定、混合 |
| 表面络合 | Cd 吸附边（针铁矿/水钠锰矿） |
| 离子交换 | 海水入侵、淡水-咸水相互作用 |
| 动力学 | 黄铁矿氧化、Fe²⁺ 氧化 |
| 反应性迁移 | 一维平流-弥散、As 穿透曲线 |
| 极端条件 | 超临界 CO₂ 注入、高温高压体系 |

---

## 🚀 快速开始

### 前置条件

1. 安装 **PHREEQC**（v3.8.6+）
   - 从 [USGS PHREEQC 网站](https://www.usgs.gov/software/phreeqc-version-3)下载
   - 64 位批处理版本的 PHREEQC 推荐使用。32 位 GUI 版本尚未通过适配过程。
   - 将 `PHREEQC_EXE` 环境变量设为可执行文件路径

2. 安装 **Python** 3.9+ 及所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 准备 **PHREEQC 数据库**：
   - 从 PHREEQC 安装目录中获取 `phreeqc.dat`（或其他数据库）
   - 将 `PHREEQC_DATABASE` 环境变量设为数据库路径

### 环境变量

```bash
# 必需
export PHREEQC_EXE="/path/to/phreeqc.exe"
export PHREEQC_DATABASE="/path/to/phreeqc.dat"
```

### 使用方法

**在智能体终端中使用（例如 Codex 或 Claude Code）：**

```bash
# 从本仓库的根目录打开 claude code cli，或在 codex 等桌面端中直接将本仓库作为工作区即可开始使用自然语言进行模拟：
# 直接描述你的模拟需求：
# “模拟海水在 pH 7-9 范围内的方解石饱和指数”
```

**作为独立 Python 库使用：**

```python
from scripts.generate_input import generate_single_simulation
from scripts.run_phreeqc import run_phreeqc
from scripts.parse_output import extract_saturation_indices
from scripts.visualize import plot_si_vs_ph

# 生成输入
input_text = generate_single_simulation(
    solutions=[{
        "number": 1,
        "components": {
            "pH": 7.2, "temp": 25.0,
            "Ca": 80, "Alkalinity": "200 as HCO3",
        }
    }]
)

# 运行模拟
output = run_phreeqc(input_text, output_dir="./results")

# 解析模拟结果
si_data = extract_saturation_indices(output)

# 可视化结果
plot_si_vs_ph(si_data, "Calcite")
```

---

## 📁 项目结构

```
.                                       # 仓库根目录
├── README.md / AGENTS.md / LICENSE     # 项目元数据
├── pyproject.toml / uv.lock            # Python 包定义与锁定文件
├── start.unix.sh                       # macOS / Linux / Git Bash 启动脚本
├── start.windows.bat                   # Windows cmd 启动脚本
├── .gitignore
│
├── .claude/skills/phreeqc-auto/        # Claude Code skill（见 SKILL.md）
├── .github/                            # CI 工作流、Pages、Discussions
├── docs/                               # 面向用户的中文文档 + GitHub Pages 首页
├── docs-developer/                     # 本机开发笔记（已被 git 忽略）
│
├── workbench/                          # PHREEQC Web Workbench（零依赖，仅标准库）
│   ├── start.unix.sh / start.windows.bat
│   ├── backend/app.py                  # 标准库 HTTP 服务（REST + SSE）
│   ├── backend/services/               # 定位、注册、运行、存储、模板与导入服务
│   ├── frontend/                       # 随附的 React、Babel 与 ECharts 资源
│   └── workspace_workbench/            # 运行时生成的记录（已被 git 忽略）
│
├── examples/                           # 精选参考模拟（每个任务一个）
│   ├── task1_1_pb_speciation/
│   ├── task1_2_calcite_si/
│   ├── task1_3_SimpleMix/
│   ├── task2_1_cd_adsorption/
│   ├── task2_2_amd_neutralization/
│   ├── task2_3_cation_exchange/
│   ├── task3_1_pyrite_kinetics/
│   ├── task3_2_as_transport/
│   ├── task3_3_co2_extended/
│   └── task3_3_co2_injection/
│
└── external_runs/                      # WebBench 外部运行导入器的默认监听目录
```

---

## 📚 示例

`references/` 中记录了九个跨三个难度级别的基准示例。每个示例还在 `examples/` 中附带一个可直接运行的文件夹（每个任务一个子目录），因此你可以进入 `examples/task1_1_pb_speciation/` 并使用本地 PHREEQC 安装重新运行模拟。

| 级别 | 示例 | `examples/` 文件夹 | 说明 |
|------|------|--------------------|------|
| 🟢 L1 | Pb 物种组成 | `task1_1_pb_speciation/` | NaCl 溶液中 Pb 的物种分布 |
| 🟢 L1 | 方解石 SI | `task1_2_calcite_si/` | 饱和指数随 pH 的敏感性分析 |
| 🟢 L1 | 海水混合 | `task1_3_SimpleMix/` | 海水与纯水的简单稀释 |
| 🟡 L2 | Cd 吸附 | `task2_1_cd_adsorption/` | 铁锰氧化物上的表面络合 |
| 🟡 L2 | AMD 中和 | `task2_2_amd_neutralization/` | 酸性矿山排水与石灰石处理 |
| 🟡 L2 | 阳离子交换 | `task2_3_cation_exchange/` | 海水入侵引起的离子交换 |
| 🔴 L3 | 黄铁矿动力学 | `task3_1_pyrite_kinetics/` | 矿物溶解动力学 |
| 🔴 L3 | As 迁移 | `task3_2_as_transport/` | 含吸附过程的一维反应性迁移 |
| 🔴 L3 | CO₂ 注入 | `task3_3_co2_injection/` | 超临界 CO₂ 多相演化 |

---

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/songsongr/auto-phreeqc.git
cd auto-phreeqc

# 安装开发依赖
pip install -r requirements.txt
pip install -e .[dev]

# 运行测试
pytest .claude/skills/phreeqc-auto/scripts/test_scripts.py
```

---

## 🖥 WebUI Workbench

项目在 [`workbench/`](../workbench/) 下提供了可自托管的浏览器界面。它通过 REST + SSE API 封装 skill，并使用 ECharts 驱动结果查看器。后端仅基于 Python 标准库，前端为本地使用打包了 React、Babel 和 ECharts 资源，无需增加新的 Python 依赖。有关架构、API 约定和全部 9 个内置模板，请参阅 [`workbench/README.md`](../workbench/README.md)。

快速启动：

```bash
# Windows（cmd.exe / Windows Terminal / PowerShell）
.\start.windows.bat

# macOS / Linux / Windows 上的 Git Bash
./start.unix.sh        # 或：bash workbench/start.unix.sh
```

然后打开 <http://127.0.0.1:8765/>。

---

## 🤝 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](../CONTRIBUTING.md) 了解贡献指南。

---

## 📄 许可证

本项目采用 MIT 许可证——详情请见 [LICENSE](../LICENSE)。

---

## ⚠️ 免责声明

本项目**与美国地质调查局（USGS）不存在关联，也未获得其认可**。PHREEQC 是 USGS 产品；在研究中使用时，应按如下方式引用：

> Parkhurst, D.L. and Appelo, C.A.J., 2013. Description of input and examples for PHREEQC
> version 3 — A computer program for speciation, batch-reaction, one-dimensional transport,
> and inverse geochemical calculations. USGS Techniques and Methods, book 6, chap. A43, 497 p.
