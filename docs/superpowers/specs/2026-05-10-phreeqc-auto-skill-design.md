# PHREEQC 全流程自动化 Skill — 设计文档

## 概述

设计一个 Claude Code Skill，用户通过自然语言指令即可完成 PHREEQC 地球化学模拟的全流程：需求澄清 → 输入生成 → 批量运行 → 结果解析 → 可视化 → 报告生成。Skill 内部使用 TeamCreate 协作功能，将子任务分配给多个 agent 并行执行。

## 架构

```
用户一句话指令
    │
    ▼
Phase 1: 需求澄清 (Skill 主进程)
    • 与用户逐一确认关键参数
    • 用户无法决定的参数 → Claude 推理默认值
    • 确认后进入执行阶段
    │
    ▼
Phase 2: Team 编排 (TeamCreate)
    Team Lead (当前会话):
    ├─ 创建 Agent Team
    ├─ 分配子任务给各 Agent
    └─ 收集结果 → 生成总结报告
    │
    ├── 输入生成 Agent: 读参数 → 生成 .pqi 文件 (含 SELECTED_OUTPUT)
    ├── 模拟运行 Agent:  调 PHREEQC 可执行文件 → 收集输出
    ├── 输出解析 Agent:  解析输出文件 → 生成结构化 JSON 数据
    └── 可视化 Agent:    读 JSON → matplotlib → 生成图表 (PNG/SVG)
    │
    ▼
Phase 3: 结果呈现
    • 终端摘要报告
    • 数据文件 (CSV/JSON)
    • 图表文件 (PNG/SVG)
```

## 关键技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 底层脚本语言 | Python | settings.local.json 已授权 python/pip |
| 图表库 | matplotlib | 成熟、输出质量高 |
| 数据交换格式 | JSON | Agent 间通过文件共享，JSON 易解析 |
| PHREEQC 调用 | Python subprocess | 直接调 PHREEQC 可执行文件 |
| 运行目录 | `workspace/` | 每次运行建独立子目录隔离不同任务 |

## 用户交互流程 (半自动模式)

1. 用户输入自然语言指令，如"模拟方解石在 pH 6-8 间的饱和指数变化，步长 0.5，25°C"
2. Skill 解析指令，提取已知参数
3. 逐一确认缺失的关键参数（温度、pH 范围、压力、离子强度等）
4. 用户无法决定的参数 → Claude 根据化学常识推理默认值
5. 汇总确认 → 进入执行
6. 执行完成后呈现结果

## 支持的计算类型 (v1)

### 1. 初始溶液计算 (Speciation)
- 输入：离子浓度、pH、pe、温度
- 输出：物种分布、饱和指数、电荷平衡
- 参数扫描维度：温度、pH、浓度

### 2. 批反应 (Batch-Reaction)
- 输入：溶液 + 矿物/气体组合 + 反应量
- 输出：反应路径、矿物溶解/沉淀量、溶液成分变化
- 参数扫描维度：反应量、温度、pH

### 3. (保留) 一维传输 — v2

### 4. (保留) 反演建模 — v3

## Agent 职责定义

### 输入生成 Agent
- 读取 Phase 1 确认的参数清单
- 根据参数生成 PHREEQC 格式的输入文件 (.pqi)
- 自动配置 SELECTED_OUTPUT 和 USER_GRAPH 便于解析
- **依赖**: 参数清单 (JSON)

### 模拟运行 Agent
- 调用 PHREEQC 可执行文件 (通过 `.lnk` 或直接 exe)
- 处理运行错误 (如收敛失败、非法参数)
- 收集标准输出和错误输出
- **依赖**: 输入文件 (.pqi)、数据库文件

### 输出解析 Agent
- 解析 PHREEQC 输出文件 (.qpo)
- 提取 SELECTED_OUTPUT 表格数据
- 结构化为 JSON 格式
- **依赖**: PHREEQC 输出文件

### 可视化 Agent
- 读 JSON 数据
- 用 matplotlib 绘制图表 (SI 曲线、浓度变化等)
- 保存为 PNG/SVG
- **依赖**: JSON 数据文件

## 与 CLAUDE.md 的关系

设计文档写入后，将方案 A (Skill+Team) 记录为主路线，方案 B (Python 库) 记录为未来参考。

## 输出产物

每次运行产出：
1. `workspace/<run-id>/simulation.pqi` — 输入文件
2. `workspace/<run-id>/simulation.qpo` — PHREEQC 输出
3. `workspace/<run-id>/results.json` — 解析后的结构化数据
4. `workspace/<run-id>/charts/*.png` — 可视化图表
5. 终端摘要报告
