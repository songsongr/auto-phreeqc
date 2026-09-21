# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-09-20

### Added
- Workbench 自定义模拟构建器 (custom simulation builder):
  - 六类模拟场景 (speciation / equilibrium / mixing / reaction_path /
    gas_equilibrium / transport)，统一的 Scenario v1 数据结构与模块注册表
  - `POST /api/v1/scenarios/validate` 结构化字段级校验 (中英文错误消息)
  - `POST /api/v1/scenarios/preview` 生成 PHREEQC 输入预览
  - 自定义模板持久化: `GET/POST /api/v1/scenarios/templates`、
    `GET/DELETE /api/v1/scenarios/templates/{id}`，保存于工作区
    `custom_templates.json` (上限 200 条)
  - `POST /api/v1/runs` 支持 `{"scenario": {...}}` 直接运行自定义模拟
  - 前端自定义模拟页面: 模块增删、溶液编辑器、字段/单位控件、
    相平衡编辑器、JSON 直接编辑、模板保存/加载/删除
- PHREEQC 可执行文件自动定位与版本识别 (`services/phreeqc_locator.py`)
- 文档拆分: 面向用户的 `docs/` (受版本控制) 与本机开发文档
  `docs-developer/` (已加入 `.gitignore`)
- `docs/index.md` 与 `docs/_config.yml` 作为 GitHub Pages 落地页
- `AGENTS.md` 取代 `CLAUDE.md`，覆盖多终端智能体的项目约定

### Changed
- `.github/workflows/docs.yml`: GitHub Pages 构建目录由 `./` 改为 `./docs`
- `services/runner.py` 改用 `phreeqc_locator` 解析可执行文件与数据库路径
- `start.windows.bat`: 同一端口已在运行时拒绝启动第二个实例
- 工作区版本号 0.1.0 -> 0.2.0 (`pyproject.toml` / `uv.lock`)

### Added
- Initial project structure with Claude Code skill (`phreeqc-auto`)
- Core Python scripts:
  - `generate_input.py` — PHREEQC input file generation
  - `run_phreeqc.py` — PHREEQC execution wrapper
  - `parse_output.py` — Output parsing utilities
  - `visualize.py` — Matplotlib-based visualization
- 9 benchmark examples across 3 difficulty levels:
  - L1: Pb speciation, Calcite SI, Seawater mixing
  - L2: Cd adsorption, AMD neutralization, Cation exchange
  - L3: Pyrite kinetics, As reactive transport, CO₂ injection
- Reference documents for each example workflow
- Coordinator script template for 4-step pipeline automation
- CD-MUSIC surface complexation modeling guide
- Support for SOLUTION, EQUILIBRIUM_PHASES, EXCHANGE, SURFACE, KINETICS,
  TRANSPORT, GAS_PHASE, REACTION, MIX, SELECTED_OUTPUT blocks
- pH scanning via REACTION titration method
- Visualizations: SI vs pH, speciation pie charts, breakthrough curves,
  adsorption edges, time-series plots
