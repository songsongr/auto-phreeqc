# auto-phreeqc

[English](../README.md) · [智能体使用](agent-usage.md) · [Workbench 指南](workbench-README.zh-CN.md)

**把地球化学问题转化为可复核的 PHREEQC 计算。**

`auto-phreeqc` 提供公开 Python 运行库、本地浏览器工作台、九个可运行案例，
以及可被 Codex 项目层自动发现的 PHREEQC Skill。它适用于水化学形态
分布、批量反应、混合、表面络合、离子交换、动力学和一维反应性运移。

> PHREEQC 程序和热力学数据库由 USGS 单独分发，仓库不会打包它们。请从
> [USGS PHREEQC 官方下载页](https://water.usgs.gov/water-resources/software/PHREEQC/)
> 获取并安装。

## 从哪里开始

| 你的目标 | 推荐入口 |
| --- | --- |
| 用自然语言描述模型 | 使用仓库随附的 `phreeqc-auto` Skill。 |
| 在浏览器中填写、运行和查看结果 | 启动本地 [Workbench](workbench-README.zh-CN.md)。 |
| 在 Python 程序中重复调用 | 使用根目录的 `phreeqc_auto` 包。 |
| 在已有模型上修改 | 从下方九个示例中选择最接近的一个。 |
| 查阅 PHREEQC v3 官方手册 | 使用[已整理的 HTML 手册知识库](phreeqc-guide/README.md)。 |

## 首次配置

### 交给智能体完成

克隆仓库后，直接对 Agent 说：

```text
帮我完成这个 auto-phreeqc 仓库的首次配置：运行仓库自带的安装和自检，启用
随附的 PHREEQC Skill；成功后告诉我可以开始自然语言计算。若本机没有
PHREEQC，请说明官方安装步骤，安装完成后继续自检。
```

Codex 会从 `.agents/skills/` 自动发现仓库级 Skill。该入口只负责加载仓库
Skill；本机配置和开发记录不会写入公开分发内容。

### 手动配置

要求：Python 3.9+、已安装的 PHREEQC 和目标数据库，以及 Git（若从 GitHub
克隆）。

```bash
git clone https://github.com/songsongr/auto-phreeqc-public.git
cd auto-phreeqc-public
python scripts/bootstrap.py
```

该命令会创建 `.venv/`、安装公开依赖、定位 PHREEQC 和数据库、把本机路径保存
在不提交到 Git 的 `.phreeqc-auto.local.json` 中，并运行一次临时计算自检。

若 PHREEQC 安装在非标准位置：

```bash
python scripts/bootstrap.py \
  --phreeqc-exe /path/to/phreeqc \
  --database /path/to/phreeqc.dat
```

也可设置 `PHREEQC_EXE` 和 `PHREEQC_DATABASE` 环境变量；它们优先于本地配置。

## 自然语言计算

配置通过后，在该仓库内向 Agent 描述目标即可。Skill 会先确认会影响结果的条件，
列出假设和单位，等待你的确认；随后把输入文件、PHREEQC 原始输出、结构化结果
和图表保存到单独结果目录。

示例：

```text
计算 25 °C、pH 7.2、Ca 80 mg/L、碱度 200 mg/L as CaCO3 的水样中方解石
饱和指数。先汇总单位、数据库和假设，等我确认后运行，并给出结果表和图。
```

参数扫描和运移问题还应明确变量范围、步数、时间单位、单元数和要追踪的输出。
完整流程见[智能体使用指南](agent-usage.md)。

## 本地 Workbench

Workbench 使用同一套公开运行库，配置完成后不依赖 AI 助手也可使用。

```bash
# Windows
.\start.windows.bat

# macOS、Linux 或 Git Bash
./start.unix.sh
```

在浏览器打开 <http://127.0.0.1:8765/>；服务仅监听本机。

## 九个可运行案例

每个目录均提供输入文件、协调脚本和预期结果。请复制到新的结果目录后再改动，
不要直接覆盖案例原件。

| 级别 | 目录 | 关注问题 |
| --- | --- | --- |
| L1 | `task1_1_pb_speciation` | NaCl 溶液中 Pb 形态分布 |
| L1 | `task1_2_calcite_si` | 方解石饱和指数和 pH 敏感性 |
| L1 | `task1_3_SimpleMix` | 海水与淡水混合 |
| L2 | `task2_1_cd_adsorption` | Cd 吸附边与表面络合 |
| L2 | `task2_2_amd_neutralization` | 酸性矿山排水中和 |
| L2 | `task2_3_cation_exchange` | 海水入侵下的阳离子交换 |
| L3 | `task3_1_pyrite_kinetics` | 黄铁矿溶解动力学 |
| L3 | `task3_2_as_transport` | As 一维反应性运移 |
| L3 | `task3_3_co2_injection` | CO₂ 注入下的多相演化 |

## 结果解释与可复现性

- 每次计算都应保留输入、原始输出、SELECTED_OUTPUT、图表和数据库名称；
- 未测得的氧化还原条件、默认参数应作为假设明确写出；
- 结果依赖热力学数据库和模型选择，解读前应查看收敛警告；
- 本项目不隶属于或受 USGS 背书。研究工作请按需要引用 PHREEQC 和本项目，
  详见 [CITATION.cff](../CITATION.cff)。

## 其他资料

- [智能体使用指南](agent-usage.md)
- [Workbench 使用指南](workbench-README.zh-CN.md)
- [贡献指南](../CONTRIBUTING.md)
- [安全策略](../SECURITY.md)
- [MIT 许可证](../LICENSE)
