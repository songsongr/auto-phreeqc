# PHREEQC 工作台

[English](../workbench/README.md)

[`phreeqc-auto`](../README.md) 运行库的自托管 Web 界面。你可以在浏览器中查看 PHREEQC 模拟过程、在子进程运行时实时观察事件日志，并检查解析结果、图表和原始产物——全程无需编写任何 Python 代码。

工作台通过轻量的 REST + SSE 接口调用公开的 `phreeqc_auto` 包，所有模拟都保留在本机工作区中。

```
┌────────────────────────────────┐    REST / SSE    ┌──────────────────────────┐
│  浏览器（React、ECharts）       │ ◀─────────────▶ │  Python 标准库 HTTP      │
│  /workbench/frontend           │                  │  /workbench/backend      │
└────────────────────────────────┘                  └──────────────┬───────────┘
                                                                    │ 导入
                                                                    ▼
                                                  ┌────────────────────────────┐
                                                  │ phreeqc_auto/              │
                                                  │   公开运行模块             │
                                                  └────────────────────────────┘
```

---

## ✨ 功能

- **9 个内置模板**：一键运行 L1/L2/L3 的用户示例，覆盖 Pb 形态分布、方解石 SI、海水混合、Cd 吸附、AMD 中和、阳离子交换、黄铁矿动力学、As 运移和超临界 CO₂。
- **参数编辑器**：每张模板卡片都有“Details”按钮，可打开结构化表单（溶液、组分、平衡相、反应、动力学、运移、混合、气相、交换、SELECTED_OUTPUT）以及原始 JSON 视图；两者会保持同步。启动前可通过实时“PHREEQC 输入预览”查看当前参数。
- **自定义模拟构建器**：“新建模拟”页还提供“自定义模拟”入口：先选择计算类型（水化学形态分析、相平衡、溶液混合、反应路径 / 滴定、气液平衡、反应性运移），再按需增删该类型允许的模块（SOLUTION、EQUILIBRIUM_PHASES、REACTION、MIX、GAS_PHASE、TRANSPORT、SELECTED_OUTPUT）。表单与 JSON 标签页编辑的是同一份 Scenario v1 文档；后端会逐字段校验，并在运行前展示生成的输入文件；任何场景都可以保存为可复用的自定义模板。
- **自动发现 PHREEQC**：工作台会扫描 `C:\Program Files\USGS\phreeqc-*`、`%PATH%` 和附近的 `.lnk` 快捷方式，以查找候选可执行文件和数据库；随后运行真实的最小 PHREEQC 任务，端到端验证可用性（已正确连接二进制与数据库，通常少于 30 ms）。
- **设置面板**：侧栏的“Settings”入口允许用户选择其他可执行文件 / 数据库路径（或清除覆盖设置以重新启用自动发现），执行连通性测试，并将选择持久化到工作区旁的 `workbench.json`。
- **运行时中止**：每个运行中的模拟都有“Abort”按钮，可终止 PHREEQC 子进程并将运行标记为 `aborted`。右上角的“Exit Workbench”也会在关闭服务器前中止所有正在运行的 PHREEQC 子进程，不会遗留孤立的 `phreeqc.exe` 进程。
- **外部运行结果导入器**：将工作台指向一个或多个目录后，用户手动生成的任意 `*.pqi` / `*.qpo` 文件对（例如从命令行、Notebook 等运行 PHREEQC）都会被自动发现，并以 `source: imported` 出现在运行列表中。通过内容哈希抑制重复导入。工作台未运行时，导入器不会激活，也绝不会触碰已配置监视目录以外的文件。
- **实时事件日志**：输入生成、PHREEQC stdout / stderr、解析和可视化等每一步都会即时流式传输到浏览器。
- **结果查看器**：每次运行提供 7 个标签页：输入文件、原始输出、SELECTED_OUTPUT、解析 JSON、图表库、文件列表和日志。
- **图表**：使用 ECharts 绘制饱和指数柱状图（按 SI 正负自动着色）和参数扫描的 SI 演化折线图。
- **文件下载**：可从浏览器下载每个产物（输入、输出、`results.json`、`charts/*.png`、事件日志）。
- **无需安装或网络依赖**：后端仅使用 Python 标准库（`http.server`、`threading`、`subprocess`）；前端内置固定版本的 React、Babel 和 ECharts，且不会修改 `pyproject.toml`。

---

## 🚀 快速开始

### 前置条件

工作台复用 phreeqc-auto 已经需要的全部环境：

1. 已安装 **PHREEQC**（v3.8.6+）。设置 `PHREEQC_EXE`，或将 `phreeqc.exe` 放入 `PATH`。
2. 准备 **PHREEQC 数据库**（例如 `phreeqc.dat`）。设置 `PHREEQC_DATABASE`，或将该文件放在项目根目录。
3. **Python 3.9+**（工作台本身不需要额外安装包）。

### 启动服务器

在项目根目录运行对应操作系统的启动器；也可以先 `cd workbench/`，再运行同名的内置启动器，两种方式行为完全相同。

```bash
# 在仓库根目录执行
./start.unix.sh                         # macOS / Linux / Git Bash
# 或
start.windows.bat                       # Windows cmd

# 或在 workbench/ 中等效执行
bash workbench/start.unix.sh
workbench\start.windows.bat
```

脚本默认绑定到 `127.0.0.1:8765`，并尝试在默认浏览器中打开页面。将自定义端口作为第一个参数传入：

```bash
./start.unix.sh 8780
PORT=8780 ./start.unix.sh
```

若希望启动服务器时**不**自动打开浏览器（例如无头环境），请直接调用后端模块：

```bash
PYTHONIOENCODING=utf-8 python workbench/backend/app.py --port 8765
```

命令行参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--host` | `127.0.0.1` | 绑定主机（默认仅限本机，较安全） |
| `--port` | `8765` | 绑定端口 |
| `--workspace` | `workbench/workspace_workbench` | 存放运行记录和产物的位置（相对仓库根目录） |

---

## 🧭 使用工作台

1. 在任意现代浏览器中打开 `http://127.0.0.1:8765/`。
2. 顶部状态圆点显示是否已找到 PHREEQC 和数据库。
3. 点击 **新建模拟 (New Simulation)**，查看 9 个内置模板。选择其中一个后，系统会加载并启动它，然后直接跳转到该运行的详情页。
4. 如果想自己搭模型，就在同一页选择 **自定义模拟 (Custom simulation)**：选择计算类型、命名、增删模块，点击“检查输入”校验，再点击“启动模拟”。自定义场景可以保存为模板，并在页面底部的列表中一键载入。
5. 在运行详情页查看 **运行日志 (Run Log)** 标签；模拟进行期间，PHREEQC 的 stdout/stderr 会持续流入此处。
6. 当运行状态为 `succeeded` 后，切换到 **图表 (Charts)** 或 **解析结果 (Parsed Results)** 标签，查看 SI 柱状图、SELECTED_OUTPUT 表格以及物种 / 元素分布。
7. **文件 (Files)** 标签列出全部产物；点击“下载”即可保存。

---

## 🛠 架构与约定

### 后端（`workbench/backend/`）

| 文件 | 用途 |
|------|------|
| `app.py` | HTTP 服务器、路由分发、SSE 端点 |
| `services/storage.py` | 每次运行的目录布局与 JSONL 事件日志 |
| `services/templates.py` | 9 组内置 PHREEQC 参数 |
| `services/runner.py` | generate → run → parse → visualize 流水线 |
| `services/__init__.py` | 包标记 |

设计说明：

- **零新增依赖**：仅使用 Python 标准库（`http.server`、`threading`、`json`、`urllib`、`mimetypes`、`re`、`subprocess`、`pathlib`、`os`）。
- **路由**通过 `@route(method, pattern)` 声明；路径参数使用 `{name}`，`{name+}` 可匹配包含 `/` 的路径片段（用于 `charts/saturation_indices.png` 一类的子目录产物）。
- **使用 SSE 流式传输**：长时间运行的 PHREEQC 子进程输出会逐行写入 `events.log`（JSONL）。客户端轮询 `/api/v1/runs/{id}/events`，接收截至当前收集到的全部事件。这是简单的长轮询模型，不需要持久 WebSocket。
- **路径安全**：在读取或写入前，所有产物路径都会校验以防止目录遍历（`..`、绝对路径）。

### 前端（`workbench/frontend/`）

| 文件 | 用途 |
|------|------|
| `index.html` | 单页应用入口，加载内置 React/Babel/ECharts 资源 |
| `styles.css` | 主题变量和组件样式 |
| `src/main.jsx` | 应用、页面和组件（集中在一个文件中，在没有打包器时保持构建简单） |

设计说明：

- **无需构建步骤或网络连接**：内置的 Babel Standalone 会在浏览器中编译 `src/main.jsx` 的 JSX，因此工作台在离线或受限网络环境中仍然可用。
- **国际化**：`main.jsx` 顶部包含 `I18N.zh` 和 `I18N.en` 字典。设置 `window.__locale = "en"` 可切换语言。
- **ECharts**：本地内置，无需额外安装。SI 柱状图会根据符号着色（绿色 = 过饱和，蓝色 = 欠饱和）。
- **长轮询**：运行活跃期间每 1.5 秒获取一次日志；当 `status === "succeeded"` 时，页面会自动从 SSE 事件列表切换到表格视图。

### API 约定

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/v1/system/health` | GET | PHREEQC、数据库和工作区状态 |
| `/api/v1/templates` | GET | 列出 9 个内置模板 |
| `/api/v1/templates/{id}` | GET | 获取一个模板（含完整参数） |
| `/api/v1/scenarios/types` | GET | 场景类型与模块注册表 |
| `/api/v1/scenarios/validate` | POST | 对 Scenario v1 做结构校验 |
| `/api/v1/scenarios/preview` | POST | 校验并渲染对应的 `.pqi` 文本 |
| `/api/v1/scenarios/templates` | GET | 列出自定义模板 |
| `/api/v1/scenarios/templates` | POST | 保存或覆盖自定义模板 |
| `/api/v1/scenarios/templates/{id}` | GET | 获取单个自定义模板 |
| `/api/v1/scenarios/templates/{id}` | DELETE | 删除自定义模板 |
| `/api/v1/runs` | GET | 列出全部运行 |
| `/api/v1/runs` | POST | 通过 `template_id`、`scenario` 或 `params` 创建运行 |
| `/api/v1/runs/{id}` | GET | 运行元数据和结果摘要 |
| `/api/v1/runs/{id}` | DELETE | 删除运行及其产物 |
| `/api/v1/runs/{id}/start` | POST | 在后台启动流水线 |
| `/api/v1/runs/{id}/input` | GET | 生成的 `.pqi` 文本 |
| `/api/v1/runs/{id}/output` | GET | PHREEQC stdout / `output.qpo` |
| `/api/v1/runs/{id}/selected-output` | GET | SELECTED_OUTPUT 导出内容 |
| `/api/v1/runs/{id}/results` | GET | 解析后的 `results.json` |
| `/api/v1/runs/{id}/files` | GET | 列出所有产物（路径和大小） |
| `/api/v1/runs/{id}/files/{name+}` | GET | 下载单个产物 |
| `/api/v1/runs/{id}/events` | GET | SSE：截至当前的全部事件 |
| `/api/v1/preview-input` | POST | 根据原始参数渲染 `.pqi` |
| `/api/v1/system/importer/status` | GET | 外部运行结果导入器状态 |
| `/api/v1/system/importer/configure` | POST | 设置 `watch_dirs`（持久化并自动启动） |
| `/api/v1/system/importer/start` | POST | 启动轮询线程 |
| `/api/v1/system/importer/stop` | POST | 停止轮询线程 |
| `/api/v1/system/importer/scan` | POST | 立即触发一次扫描 |

成功响应格式：

```json
{"ok": true, "data": ...}
```

失败响应格式：

```json
{"ok": false, "error": {"code": "PHREEQC_NOT_FOUND", "message": "..."}}
```

错误代码为稳定、机器可读的字符串：

| 代码 | 含义 |
|------|------|
| `PHREEQC_NOT_FOUND` | 未能通过 `PHREEQC_EXE` 环境变量 / PATH 查找到 PHREEQC |
| `DATABASE_NOT_FOUND` | 未能通过 `PHREEQC_DATABASE` 环境变量 / 查找规则找到数据库 |
| `INVALID_PARAMS` | 请求体缺少必填字段 |
| `INVALID_PATH` | 产物名称或 URL 路径未通过校验 |
| `RUN_NOT_FOUND` | 未知的 `run_id` |
| `RUN_ALREADY_ACTIVE` | 对正在运行的任务调用了 `start` |
| `SIM_TIMEOUT` | PHREEQC 子进程超过 300 秒 |
| `INTERNAL_ERROR` | 未处理的异常 |

---

## 🗂 工作区布局

每次运行位于 `workbench/workspace_workbench/<run_id>/` 下（已被 gitignore 忽略；每次服务器启动时重新创建）：

```
workbench/workspace_workbench/
└── <run_id>/
    ├── meta.json           # 状态、参数、日志尾部、摘要
    ├── events.log          # JSONL 格式的步骤 / stdout / 错误事件流
    ├── input.pqi           # 生成的 PHREEQC 输入
    ├── output.qpo          # PHREEQC stdout
    ├── selected_output.txt # SELECTED_OUTPUT 数据
    ├── results.json        # 解析后的结构化结果
    ├── phreeqc.log         # PHREEQC 内部日志（通常为空）
    └── charts/
        ├── saturation_indices.png
        └── si_evolution.png
```

每次状态切换时，都会在 `RLock` 保护下以原子方式（读-改-写）更新 `meta.json`。

从构建器保存的自定义场景与运行记录放在一起：`workbench/workspace_workbench/custom_templates.json`（同样位于被 gitignore 忽略的工作区中，写入同样是原子的）。

---

## 🧪 已测试

已在 Windows 10、Python 3.13、PHREEQC 3.8.6-17100 环境下对 9 个内置模板中的 8 个（L1、L2、L3）完成端到端冒烟测试，均成功生成 `succeeded` 运行。第 9 个模板（`pyrite_kinetics`）会报告 `failed`，原因是 PHREEQC 默认的 KINETICS 数值参数无法使测试配置在原版 `phreeqc.dat` 中收敛。这是 PHREEQC 层面的参数问题（请加入 `KNOBS` 并检查该示例的 `input.pqi`），并非工作台问题。

自定义模拟路径同样经过端到端验证：六种场景类型都能编译出有效输入并得到 `succeeded` 运行；浏览器端流程（选择类型 → 编辑模块 → 检查输入 → 预览 → 保存 / 载入模板 → 启动模拟）已在无头浏览器中对运行中的服务器完整走通。

---

## 🔒 安全性

- 服务器默认绑定至 `127.0.0.1`，**不会**暴露到局域网。若需要局域网访问，请传入 `--host 0.0.0.0` 并添加使用 TLS 的反向代理；该工作台面向单用户。
- 所有产物路径均经过校验，以防目录遍历攻击。
- SSE 端点未鉴权，因为默认仅允许本机连接；若修改主机绑定，请增加认证机制。
- 前端仅与同源通信，不包含第三方跟踪器。

---

## 📚 相关内容

- `../README.md`：顶层项目说明
- `../phreeqc_auto/`：工作台调用的公开运行库
- `../examples/`：模板所镜像的九个用户示例
