# PHREEQC Workbench

[简体中文](../docs/workbench-README.zh-CN.md)

A self-hosted web UI for the [`phreeqc-auto`](../README.md) skill.  Browse
PHREEQC simulations in the browser, watch a live event log as the
subprocess runs, and inspect parsed results, charts, and raw artifacts —
all without writing a single line of Python.

The workbench is **fully decoupled from the phreeqc-auto package**: it
talks to the four skill scripts over a thin REST + SSE interface and
contributes no runtime dependencies to the host project.

```
┌────────────────────────────────┐    REST / SSE    ┌──────────────────────────┐
│  Browser (React, ECharts)      │ ◀─────────────▶ │  Python stdlib HTTP       │
│  /workbench/frontend           │                  │  /workbench/backend      │
└────────────────────────────────┘                  └──────────────┬───────────┘
                                                                    │ imports
                                                                    ▼
                                                  ┌────────────────────────────┐
                                                  │ .claude/skills/            │
                                                  │   phreeqc-auto/scripts/*   │
                                                  └────────────────────────────┘
```

---

## ✨ Features

- **9 built-in templates** — one click to run the same L1/L2/L3
  workflows documented in the skill references (Pb speciation,
  calcite SI, seawater mixing, Cd adsorption, AMD neutralization,
  cation exchange, pyrite kinetics, As transport, supercritical CO₂).
- **Parameter editor** — every template card has a "Details" button
  that opens a structured form (Solution / Components / Equilibrium
  Phases / Reaction / Kinetics / Transport / Mix / Gas Phase / Exchange
  / SELECTED_OUTPUT) and a raw JSON view, both kept in sync.  A live
  "PHREEQC input preview" reflects the current parameters before
  starting.
- **Custom simulation builder** — the New Simulation page also offers a
  "Custom simulation" entry: pick one of six calculation types
  (aqueous speciation, phase equilibrium, mixing, reaction path, gas
  equilibrium, reactive transport) and then add or remove the modules
  that type allows (SOLUTION, EQUILIBRIUM_PHASES, REACTION, MIX,
  GAS_PHASE, TRANSPORT, SELECTED_OUTPUT).  The form and the JSON tab
  edit one and the same Scenario v1 document; the backend validates it
  field by field and shows the generated input before anything runs;
  any scenario can be saved as a reusable custom template.
- **Auto-discovery of PHREEQC** — the workbench scans `C:\Program
  Files\USGS\phreeqc-*`, `%PATH%`, and any nearby `.lnk` shortcut for
  candidate executables and databases, then runs a real minimal
  PHREEQC job to verify reachability (binary + database wired up
  end-to-end, typically < 30 ms).
- **Settings panel** — sidebar "Settings" entry lets the user pick a
  different executable / database path (or clear the override to
  re-enable auto-discovery), run a reachability test, and persist the
  choice in `workbench.json` next to the workspace.
- **Run-time abort** — every running simulation has an "Abort"
  button that terminates the PHREEQC subprocess and marks the run as
  `aborted`.  The "Exit Workbench" button in the top-right also
  aborts every running PHREEQC child before shutting the server down
  — no orphan `phreeqc.exe` processes are left behind.
- **External-run importer** — point the workbench at one or more
  directories and any `*.pqi` / `*.qpo` pair the user generates
  manually (running PHREEQC from the command line, from a notebook,
  etc.) is picked up automatically and appears in the run list with
  `source: imported`.  Duplicate imports are suppressed by content
  hash.  When the workbench is *not* running, the importer is simply
  inactive — it never touches files outside its configured watch
  directories.
- **Live event log** — every step (input generation, PHREEQC stdout /
  stderr, parse, visualization) is streamed to the browser as it
  happens.
- **Result inspector** — 7 tabs per run: input file, raw output,
  SELECTED_OUTPUT, parsed JSON, chart gallery, file list, log.
- **Charts** — saturation-index bar chart with ECharts (auto-coloured
  by SI sign) and SI evolution line chart for parameter sweeps.
- **File download** — every artifact (input, output, results.json,
  `charts/*.png`, event log) is downloadable from the browser.
- **No installation or network dependency** — the backend is built on Python
  stdlib (`http.server`, `threading`, `subprocess`), while fixed versions of
  React, Babel, and ECharts are bundled with the frontend. `pyproject.toml`
  is untouched.

---

## 🚀 Quick start

### Prerequisites

The workbench reuses everything `phreeqc-auto` already needs:

1. **PHREEQC** installed (v3.8.6+).  Set `PHREEQC_EXE` (or place
   `phreeqc.exe` on `PATH`).
2. **PHREEQC database** (e.g. `phreeqc.dat`).  Set
   `PHREEQC_DATABASE` (or place the file in the project root).
3. **Python 3.9+** (the workbench itself needs no extra packages).

### Start the server

Run the root-level launcher for your OS, or `cd workbench/` and run
the bundled launcher of the same name — both behave identically.

```bash
# from the repository root
./start.unix.sh                         # macOS / Linux / Git Bash
# or
start.windows.bat                       # Windows cmd

# or equivalently from workbench/
bash workbench/start.unix.sh
workbench\start.windows.bat
```

The script binds to `127.0.0.1:8765` by default and tries to open
the page in your default browser.  Pass a custom port as the first
argument:

```bash
./start.unix.sh 8780
PORT=8780 ./start.unix.sh
```

To start the server **without** auto-launching a browser (e.g. when
running headless), invoke the backend module directly:

```bash
PYTHONIOENCODING=utf-8 python workbench/backend/app.py --port 8765
```

CLI flags:

| Flag            | Default      | Description                                   |
|-----------------|--------------|-----------------------------------------------|
| `--host`        | `127.0.0.1`  | Bind host (localhost only by default — safe)  |
| `--port`        | `8765`       | Bind port                                     |
| `--workspace`   | `workbench/workspace_workbench` | Where runs and artifacts are stored (relative to the repo root) |

---

## 🧭 Using the workbench

1. **Open** `http://127.0.0.1:8765/` in any modern browser.
2. The top status dot shows whether PHREEQC and the database were
   located.
3. Click **新建模拟 (New Simulation)** to see the 9 built-in
   templates.  Pick one — it is loaded, started, and you are taken
   straight to the run detail page.
4. To build your own model instead, pick **自定义模拟 (Custom
   simulation)** on the same page: choose a calculation type, name it,
   add the modules you need, click 检查输入 to validate, then 启动模拟.
   Custom scenarios can be saved as templates and loaded back from the
   list at the bottom of the page.
5. On the run detail page, watch the **运行日志 (Run Log)** tab —
   it streams PHREEQC's stdout/stderr as the simulation progresses.
6. Once the run is `succeeded`, switch to the **图表 (Charts)** or
   **解析结果 (Parsed Results)** tab to see the SI bar chart, the
   SELECTED_OUTPUT table, and the species/element breakdown.
7. The **文件 (Files)** tab lists every artifact; click 下载 to
   download it.

---

## 🛠 Architecture & conventions

### Backend (`workbench/backend/`)

| File                            | Purpose                                        |
|---------------------------------|------------------------------------------------|
| `app.py`                        | HTTP server, route dispatch, SSE endpoint      |
| `services/storage.py`           | Per-run directory layout + JSONL event log     |
| `services/templates.py`         | 9 built-in PHREEQC parameter sets              |
| `services/runner.py`            | generate → run → parse → visualize pipeline    |
| `services/__init__.py`          | Package marker                                 |

Design notes:

- **Zero new dependencies** — only the Python standard library
  (`http.server`, `threading`, `json`, `urllib`, `mimetypes`,
  `re`, `subprocess`, `pathlib`, `os`).
- **Routes** are declared with `@route(method, pattern)`; path
  parameters use `{name}`, and `{name+}` matches a path segment
  that may contain `/` (used for subdirectory artifacts like
  `charts/saturation_indices.png`).
- **SSE for streaming** — long-running PHREEQC subprocess output is
  written line-by-line to `events.log` (JSONL).  Clients poll
  `/api/v1/runs/{id}/events` and receive all events collected so far.
  A simple long-poll model — no persistent WebSocket needed.
- **Path safety** — all artifact paths are validated against
  traversal (`..`, absolute paths) before being read or written.

### Frontend (`workbench/frontend/`)

| File             | Purpose                                         |
|------------------|-------------------------------------------------|
| `index.html`     | Single-page entry, loads bundled React/Babel/ECharts assets |
| `styles.css`     | Theme tokens + component styles                 |
| `src/main.jsx`   | App, pages, components (one file — keeps the    |
|                  | build trivial when no bundler is present)       |

Design notes:

- **No build step or network connection required** — bundled Babel
  Standalone compiles JSX in `src/main.jsx` in the browser, so the
  workbench remains usable in offline or restricted environments.
- **i18n** — `I18N.zh` and `I18N.en` dictionaries at the top of
  `main.jsx`.  Toggle by setting `window.__locale = "en"`.
- **ECharts** — bundled locally, with no extra installation. The SI bar chart colours each
  bar by sign (green = supersaturated, blue = undersaturated).
- **Long polling** — the run log is fetched every 1.5 s while a
  run is active; the page transitions from the SSE event list into
  the table view automatically once `status === "succeeded"`.

### API conventions

| Path                                | Method | Description                          |
|-------------------------------------|--------|--------------------------------------|
| `/api/v1/system/health`             | GET    | PHREEQC + DB + workspace status      |
| `/api/v1/templates`                 | GET    | List 9 built-in templates            |
| `/api/v1/templates/{id}`            | GET    | One template (with full params)      |
| `/api/v1/scenarios/types`           | GET    | Scenario types + module registry     |
| `/api/v1/scenarios/validate`        | POST   | Structural check of a Scenario v1    |
| `/api/v1/scenarios/preview`         | POST   | Validate + render its `.pqi` text    |
| `/api/v1/scenarios/templates`       | GET    | List saved custom templates          |
| `/api/v1/scenarios/templates`       | POST   | Save or overwrite a custom template  |
| `/api/v1/scenarios/templates/{id}`  | GET    | One saved custom template            |
| `/api/v1/scenarios/templates/{id}`  | DELETE | Delete a saved custom template       |
| `/api/v1/runs`                      | GET    | List all runs                        |
| `/api/v1/runs`                      | POST   | Create run from `template_id`, `scenario` or `params` |
| `/api/v1/runs/{id}`                 | GET    | Run metadata + result summary        |
| `/api/v1/runs/{id}`                 | DELETE | Delete run and its artifacts         |
| `/api/v1/runs/{id}/start`           | POST   | Launch the pipeline in background    |
| `/api/v1/runs/{id}/input`           | GET    | Generated `.pqi` text                |
| `/api/v1/runs/{id}/output`          | GET    | PHREEQC stdout / `output.qpo`        |
| `/api/v1/runs/{id}/selected-output` | GET    | SELECTED_OUTPUT dump                 |
| `/api/v1/runs/{id}/results`         | GET    | Parsed `results.json`                |
| `/api/v1/runs/{id}/files`           | GET    | List all artifacts (path + size)     |
| `/api/v1/runs/{id}/files/{name+}`   | GET    | Download a single artifact           |
| `/api/v1/runs/{id}/events`          | GET    | SSE: all events so far               |
| `/api/v1/preview-input`             | POST   | Render a `.pqi` from raw params      |
| `/api/v1/system/importer/status`    | GET    | External-run importer status         |
| `/api/v1/system/importer/configure` | POST   | Set watch_dirs (persisted, auto-start) |
| `/api/v1/system/importer/start`     | POST   | Start the polling thread             |
| `/api/v1/system/importer/stop`      | POST   | Stop the polling thread              |
| `/api/v1/system/importer/scan`      | POST   | Trigger an immediate scan            |

Response envelope (success):

```json
{"ok": true, "data": ...}
```

Response envelope (failure):

```json
{"ok": false, "error": {"code": "PHREEQC_NOT_FOUND", "message": "..."}}
```

Error codes are stable, machine-readable strings:

| Code                    | Meaning                                       |
|-------------------------|-----------------------------------------------|
| `PHREEQC_NOT_FOUND`     | `PHREEQC_EXE` env var / PATH lookup failed   |
| `DATABASE_NOT_FOUND`    | `PHREEQC_DATABASE` env var / lookup failed   |
| `INVALID_PARAMS`        | Request body missing required fields          |
| `INVALID_PATH`          | Artifact name or URL path failed validation   |
| `RUN_NOT_FOUND`         | Unknown `run_id`                              |
| `RUN_ALREADY_ACTIVE`    | `start` called on a running run               |
| `SIM_TIMEOUT`           | PHREEQC subprocess exceeded 300 s             |
| `INTERNAL_ERROR`        | Unhandled exception                           |

---

## 🗂 Workspace layout

Each run lives under `workbench/workspace_workbench/<run_id>/` (gitignored; recreated
on every server start):

```
workbench/workspace_workbench/
└── <run_id>/
    ├── meta.json           # status, params, log tail, summary
    ├── events.log          # JSONL stream of step/stdout/error events
    ├── input.pqi           # generated PHREEQC input
    ├── output.qpo          # PHREEQC stdout
    ├── selected_output.txt # SELECTED_OUTPUT data
    ├── results.json        # parsed structured result
    ├── phreeqc.log         # PHREEQC internal log (often empty)
    └── charts/
        ├── saturation_indices.png
        └── si_evolution.png
```

The `meta.json` is updated atomically (read-modify-write under an
`RLock`) on every status transition.

Custom scenarios saved from the builder live next to the runs, in
`workbench/workspace_workbench/custom_templates.json` (same gitignored
workspace, also written atomically).

---

## 🧪 Tested

The workbench was end-to-end smoke tested with 8 of the 9 built-in
templates (L1, L2, and L3) producing `succeeded` runs end-to-end on
Windows 10, Python 3.13, PHREEQC 3.8.6-17100.  The 9th template
(`pyrite_kinetics`) reports a `failed` status because PHREEQC's
default KINETICS numerical parameters cannot converge the test
configuration in the stock `phreeqc.dat` — this is a PHREEQC-level
parameter issue (add `KNOBS`; see `references/pyrite_kinetics_example.md`),
not a workbench issue.

The custom-simulation path is additionally covered end to end: all six
scenario types compile to valid input and produce `succeeded` runs, and
the browser flow (choose type → edit modules → 检查输入 → preview →
save/load template → 启动模拟) was exercised in a headless browser
against a live server.

---

## 🔒 Safety

- The server binds to `127.0.0.1` by default — it is **not** exposed
  to the LAN.  If you need LAN access, pass `--host 0.0.0.0` and
  add a reverse proxy with TLS; the workbench is single-user.
- All artifact paths are validated against path traversal.
- The SSE endpoint is unauthenticated because of the local-only
  binding; if you change the host, add auth.
- The frontend only talks to the same origin; no third-party
  trackers.

---

## 📚 Related

- `../README.md` — top-level project
- `../.claude/skills/phreeqc-auto/SKILL.md` — the skill the workbench
  wraps
- `../.claude/skills/phreeqc-auto/references/*.md` — 9 verified
  workflows that the templates mirror
