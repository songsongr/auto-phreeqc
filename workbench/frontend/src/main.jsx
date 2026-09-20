// =====================================================================
// PHREEQC Workbench - Frontend entry point
// Loaded as type="text/babel" so JSX works without a build step.
// =====================================================================

const { useState, useEffect, useCallback, useMemo, useRef, createContext, useContext } = React;

// ---------- API client (fetch wrapper) ---------------------------------
const API = {
  base: "",
  async request(method, path, body) {
    const opts = { method, headers: { "Content-Type": "application/json" } };
    if (body !== undefined) opts.body = JSON.stringify(body);
    const res = await fetch(this.base + path, opts);
    const ctype = res.headers.get("Content-Type") || "";
    let data;
    if (ctype.includes("application/json")) {
      data = await res.json();
    } else {
      data = await res.text();
    }
    if (!res.ok || (typeof data === "object" && data && data.ok === false)) {
      const err = (data && data.error) || { code: "HTTP_ERROR", message: res.statusText };
      throw new Error(`[${err.code}] ${err.message}`);
    }
    return data && typeof data === "object" && "data" in data ? data.data : data;
  },
  get(path)      { return this.request("GET", path); },
  post(path, b)  { return this.request("POST", path, b); },
  del(path)      { return this.request("DELETE", path); },
};

function parseSseEvents(payload) {
  if (Array.isArray(payload)) return payload;
  if (typeof payload !== "string") return [];
  return payload.split(/\n\n+/).flatMap((block) => {
    const data = block.split("\n").find((line) => line.startsWith("data:"));
    if (!data) return [];
    try {
      const event = JSON.parse(data.slice(5).trim());
      return event && !Array.isArray(event) && typeof event === "object" &&
        typeof event.ts === "number" && typeof event.kind === "string" ? [event] : [];
    }
    catch (e) { return []; }
  });
}

// ---------- i18n -------------------------------------------------------
// Two-language UI (zh / en).  PHREEQC input keywords (SOLUTION,
// SELECTED_OUTPUT, EQUILIBRIUM_PHASES, …) are emitted by the backend
// in English and intentionally not translated here.
const LANG_KEY = "phreeqc_workbench.lang";
const LangContext = createContext(null);

function LangProvider({ children }) {
  const [locale, setLocaleState] = useState(() => {
    try {
      const saved = localStorage.getItem(LANG_KEY);
      return (saved === "en" || saved === "zh") ? saved : "zh";
    } catch (e) { return "zh"; }
  });
  const setLocale = useCallback((next) => {
    if (next !== "zh" && next !== "en") return;
    try { localStorage.setItem(LANG_KEY, next); } catch (e) {}
    setLocaleState(next);
  }, []);
  const t = useCallback((key) => {
    const dict = I18N[locale] || I18N.zh;
    return dict[key] || key;
  }, [locale]);
  const value = useMemo(() => ({ locale, setLocale, t }), [locale, setLocale, t]);
  return <LangContext.Provider value={value}>{children}</LangContext.Provider>;
}

function useLang() {
  const ctx = useContext(LangContext);
  // Fallback for components rendered outside <LangProvider> (should not
  // happen, but keeps the page alive during HMR edge cases).
  if (!ctx) {
    return { locale: "zh", setLocale: () => {}, t: (k) => I18N.zh[k] || k };
  }
  return ctx;
}

const I18N = {
  zh: {
    workbench: "PHREEQC Workbench",
    nav_runs: "运行列表",
    nav_new: "新建模拟",
    health_ok: "PHREEQC 就绪",
    health_warn: "PHREEQC 未配置",
    runs_title: "运行列表",
    new_btn: "新建模拟",
    empty_runs: "暂无运行，点击右侧 “新建模拟” 开始。",
    templates_title: "选择内置模板",
    templates_subtitle: "9 个已验证的 PHREEQC 工作流，一键载入参数。",
    btn_start: "启动模拟",
    btn_delete: "删除",
    btn_view: "查看",
    btn_back: "返回",
    tab_input: "输入文件",
    tab_output: "PHREEQC 输出",
    tab_selected: "SELECTED_OUTPUT",
    tab_results: "解析结果",
    tab_charts: "图表",
    tab_files: "文件",
    tab_log: "运行日志",
    start_run: "启动",
    status: "状态",
    created: "创建",
    updated: "更新",
    name: "名称",
    action: "操作",
    exit_title: "退出 Workbench？",
    exit_body: "这将停止本地 PHREEQC 服务并关闭当前页面。正在运行的模拟会被中止。",
    exit_confirm: "确认退出",
    exit_cancel: "取消",
    exit_done: "服务已停止 — 您可以关闭此标签页。",
    icon_runs: "≡",
    icon_new: "+",
    icon_exit: "⏻",
    exit_btn: "退出",
    lang_zh: "中文",
    lang_en: "EN",
    nav_console: "控制台",
    icon_console: "🛠",
    console_title: "PHREEQC 控制台",
    console_subtitle: "自动寻找 + 手动配置 + 可达性测试。",
    settings_executables: "可执行文件候选",
    settings_databases: "数据库候选",
    settings_active: "当前生效",
    settings_use: "使用此路径",
    settings_test: "测试可及性",
    settings_auto: "自动配置环境",
    settings_configuring: "正在自动配置…",
    settings_save: "保存设置",
    settings_testing: "测试中…",
    settings_path_label: "PHREEQC 可执行文件",
    settings_db_label: "PHREEQC 数据库",
    settings_placeholder: "留空以使用自动发现",
    settings_test_passed: "✓ 可用",
    settings_test_failed: "✗ 失败",
    settings_clear: "清除",
    settings_version: "版本",
    settings_auto_done: "已自动配置并通过可及性测试。",
    settings_override_notice: "这会覆盖已自动配置的 PHREEQC 路径和数据库。",
    settings_override_cancel: "取消",
    settings_override_confirm: "仍然保存",
    tpl_btn_detail: "详情",
    tpl_btn_start: "启动模拟 →",
    tpl_edit_title: "参数编辑",
    tpl_edit_form: "表单",
    tpl_edit_json: "JSON",
    tpl_invalid_json: "JSON 格式错误",
    tpl_preview: "PHREEQC 输入预览",
    tpl_no_preview: "预览不可用",
    tpl_back: "← 返回模板",
    tpl_param_solution: "溶液 (Solution)",
    tpl_param_components: "组分 (Components)",
    tpl_param_equilibrium: "平衡相 (Equilibrium Phases)",
    tpl_param_reaction: "反应 (Reaction)",
    tpl_param_kinetics: "动力学 (Kinetics)",
    tpl_param_mix: "混合 (Mix)",
    tpl_param_transport: "运移 (Transport)",
    tpl_param_gas: "气相 (Gas Phase)",
    tpl_param_exchange: "交换 (Exchange)",
    tpl_param_selected: "SELECTED_OUTPUT",
    tpl_param_other: "其他",
    tpl_add: "+ 添加",
    tpl_remove: "×",
    custom_entry_title: "自定义模拟",
    custom_entry_summary: "从计算类型开始，按需组合溶液、反应、相平衡、气相与运移模块。",
    custom_entry_action: "开始配置 →",
    custom_title: "创建自定义模拟",
    custom_subtitle: "先选择计算类型，再按需添加模块；表单与 JSON 共用同一份场景定义。",
    custom_choose_type: "选择计算类型",
    custom_choose_type_help: "系统会载入一个最小可运行骨架；之后可以自由添加或移除允许的模块。",
    custom_change_type: "更换计算类型",
    custom_name: "模拟名称",
    custom_name_placeholder: "例如：石灰石中和试验",
    custom_modules: "参数模块",
    custom_add_module: "+ 添加模块",
    custom_add_solution: "+ 添加溶液",
    custom_remove_module: "移除模块",
    custom_required_module: "必需",
    custom_validate: "检查输入",
    custom_validating: "检查中…",
    custom_validation_ok: "场景结构检查通过。",
    custom_validation_errors: "请先修复以下问题：",
    custom_validation_warnings: "请留意：",
    custom_preview: "预览 PHREEQC 输入",
    custom_previewing: "生成预览中…",
    custom_save_template: "保存为模板",
    custom_saving_template: "保存中…",
    custom_template_saved: "已保存为自定义模板。",
    custom_start: "启动模拟",
    custom_starting: "创建运行中…",
    custom_preview_title: "PHREEQC 输入预览",
    custom_no_preview: "点击“预览 PHREEQC 输入”生成预览。",
    custom_load_error: "无法载入自定义模拟类型",
    custom_unknown_module: "高级参数",
    custom_json_help: "可编辑完整 Scenario JSON；切回表单前需要保持 JSON 有效。",
    custom_saved_title: "已保存的自定义模板",
    custom_saved_empty: "还没有保存的自定义模板。",
    custom_load: "载入",
    custom_delete: "删除",
    custom_overwrite_hint: "再次保存会覆盖当前载入的模板。",
    custom_modules_help: "按需增删模块；“必需”模块不可移除。",
    custom_add_module_hint: "添加模块",
    mod_solutions: "溶液 (SOLUTION)",
    mod_initial_cell_solution: "初始单元溶液",
    mod_equilibrium_phases: "平衡相 (EQUILIBRIUM_PHASES)",
    mod_reaction: "反应 (REACTION)",
    mod_mix: "混合 (MIX)",
    mod_gas_phase: "气相 (GAS_PHASE)",
    mod_transport: "运移 (TRANSPORT)",
    mod_selected_output: "选定输出 (SELECTED_OUTPUT)",
    abort_btn: "中止计算",
    abort_title: "中止该模拟？",
    abort_body: "正在运行的 PHREEQC 进程会被立即终止，已生成的文件保留在 workspace 中。",
    abort_confirm: "中止",
    status_aborted: "已中止",
    run_failed_artifacts: "该运行在生成全部结果文件前失败。请查看运行日志；仅已生成的文件会显示为可用标签。",
    failure_summary: "失败摘要",
    failure_stage: "失败位置",
    failure_exit_code: "退出码",
    failure_error_code: "错误码",
    failure_output: "关键输出",
    failure_environment: "运行环境",
    failure_copy: "复制错误信息",
    failure_copied: "已复制，可直接粘贴给 agent。",
    failure_no_output: "未提取到错误输出，请查看下方原始日志。",
  },
  en: {
    workbench: "PHREEQC Workbench",
    nav_runs: "Runs",
    nav_new: "New Simulation",
    health_ok: "PHREEQC ready",
    health_warn: "PHREEQC not configured",
    runs_title: "Run list",
    new_btn: "New Simulation",
    empty_runs: "No runs yet. Click \"New Simulation\" to start.",
    templates_title: "Built-in Templates",
    templates_subtitle: "9 verified PHREEQC workflows, one click to load parameters.",
    btn_start: "Start",
    btn_delete: "Delete",
    btn_view: "View",
    btn_back: "Back",
    tab_input: "Input File",
    tab_output: "PHREEQC Output",
    tab_selected: "SELECTED_OUTPUT",
    tab_results: "Parsed Results",
    tab_charts: "Charts",
    tab_files: "Files",
    tab_log: "Run Log",
    start_run: "Start",
    status: "Status",
    created: "Created",
    updated: "Updated",
    name: "Name",
    action: "Action",
    exit_title: "Exit Workbench?",
    exit_body: "This will stop the local PHREEQC service and close the page. Any running simulation will be aborted.",
    exit_confirm: "Exit",
    exit_cancel: "Cancel",
    exit_done: "Service stopped — you can close this tab.",
    icon_runs: "≡",
    icon_new: "+",
    icon_exit: "⏻",
    exit_btn: "Exit",
    lang_zh: "中文",
    lang_en: "EN",
    nav_console: "Console",
    icon_console: "🛠",
    console_title: "PHREEQC Console",
    console_subtitle: "Auto-discovery + manual configuration + reachability test.",
    settings_executables: "Executable candidates",
    settings_databases: "Database candidates",
    settings_active: "Currently in use",
    settings_use: "Use this",
    settings_test: "Test reachability",
    settings_auto: "Auto-configure environment",
    settings_configuring: "Auto-configuring…",
    settings_save: "Save settings",
    settings_testing: "Testing…",
    settings_path_label: "PHREEQC executable",
    settings_db_label: "PHREEQC database",
    settings_placeholder: "Leave empty for auto-discovery",
    settings_test_passed: "✓ OK",
    settings_test_failed: "✗ failed",
    settings_clear: "Clear",
    settings_version: "Version",
    settings_auto_done: "Auto-configured and reachability-tested.",
    settings_override_notice: "This will replace the auto-configured PHREEQC path and database.",
    settings_override_cancel: "Cancel",
    settings_override_confirm: "Save anyway",
    tpl_btn_detail: "Details",
    tpl_btn_start: "Start →",
    tpl_edit_title: "Parameter editor",
    tpl_edit_form: "Form",
    tpl_edit_json: "JSON",
    tpl_invalid_json: "Invalid JSON",
    tpl_preview: "PHREEQC input preview",
    tpl_no_preview: "Preview unavailable",
    tpl_back: "← Back to templates",
    tpl_param_solution: "Solution",
    tpl_param_components: "Components",
    tpl_param_equilibrium: "Equilibrium Phases",
    tpl_param_reaction: "Reaction",
    tpl_param_kinetics: "Kinetics",
    tpl_param_mix: "Mix",
    tpl_param_transport: "Transport",
    tpl_param_gas: "Gas Phase",
    tpl_param_exchange: "Exchange",
    tpl_param_selected: "SELECTED_OUTPUT",
    tpl_param_other: "Other",
    tpl_add: "+ Add",
    tpl_remove: "×",
    custom_entry_title: "Custom simulation",
    custom_entry_summary: "Start from a calculation type and compose solutions, reactions, phases, gas, and transport as needed.",
    custom_entry_action: "Configure →",
    custom_title: "Create custom simulation",
    custom_subtitle: "Choose a calculation type, add modules as needed, and edit one shared scenario in either form or JSON.",
    custom_choose_type: "Choose calculation type",
    custom_choose_type_help: "A minimal runnable skeleton is loaded first; you can then add or remove permitted modules.",
    custom_change_type: "Change calculation type",
    custom_name: "Simulation name",
    custom_name_placeholder: "For example: Calcite neutralization test",
    custom_modules: "Parameter modules",
    custom_add_module: "+ Add module",
    custom_add_solution: "+ Add solution",
    custom_remove_module: "Remove module",
    custom_required_module: "Required",
    custom_validate: "Check input",
    custom_validating: "Checking…",
    custom_validation_ok: "Scenario structure check passed.",
    custom_validation_errors: "Fix these issues before running:",
    custom_validation_warnings: "Please note:",
    custom_preview: "Preview PHREEQC input",
    custom_previewing: "Generating preview…",
    custom_save_template: "Save as template",
    custom_saving_template: "Saving…",
    custom_template_saved: "Saved as a custom template.",
    custom_start: "Start simulation",
    custom_starting: "Creating run…",
    custom_preview_title: "PHREEQC input preview",
    custom_no_preview: "Click “Preview PHREEQC input” to generate a preview.",
    custom_load_error: "Unable to load custom simulation types",
    custom_unknown_module: "Advanced parameters",
    custom_json_help: "Edit the complete Scenario JSON; it must be valid before returning to the form.",
    custom_saved_title: "Saved custom templates",
    custom_saved_empty: "No custom templates saved yet.",
    custom_load: "Load",
    custom_delete: "Delete",
    custom_overwrite_hint: "Saving again overwrites the template currently loaded.",
    custom_modules_help: "Add or remove modules as needed; required modules cannot be removed.",
    custom_add_module_hint: "Add module",
    mod_solutions: "Solutions (SOLUTION)",
    mod_initial_cell_solution: "Initial cell solution",
    mod_equilibrium_phases: "Equilibrium phases (EQUILIBRIUM_PHASES)",
    mod_reaction: "Reaction (REACTION)",
    mod_mix: "Mix (MIX)",
    mod_gas_phase: "Gas phase (GAS_PHASE)",
    mod_transport: "Transport (TRANSPORT)",
    mod_selected_output: "Selected output (SELECTED_OUTPUT)",
    abort_btn: "Abort",
    abort_title: "Abort this simulation?",
    abort_body: "The running PHREEQC process will be terminated. Generated files are kept in the workspace.",
    abort_confirm: "Abort",
    status_aborted: "aborted",
    run_failed_artifacts: "This run failed before all result files were generated. Check the run log; only available artifacts are shown as tabs.",
    failure_summary: "Failure summary",
    failure_stage: "Failed at",
    failure_exit_code: "Exit code",
    failure_error_code: "Error code",
    failure_output: "Key output",
    failure_environment: "Runtime environment",
    failure_copy: "Copy error details",
    failure_copied: "Copied — ready to paste to an agent.",
    failure_no_output: "No error output was extracted. See the raw log below.",
  },
};

// ---------- Shared components -----------------------------------------
function StatusBadge({ status }) {
  return <span className={`badge ${status}`}>{status || "unknown"}</span>;
}

function HealthDot({ health }) {
  const { t } = useLang();
  if (!health) return null;
  const phreeqcOk = health.phreeqc && health.phreeqc.ok;
  return (
    <div className="status">
      <span className={`status-dot ${phreeqcOk ? "ok" : "warn"}`}></span>
      <span>{phreeqcOk ? t("health_ok") : t("health_warn")}</span>
    </div>
  );
}

// Confirm modal — backdrop click and Escape both cancel; Enter triggers
// the confirm callback.  The danger variant styles the icon red.
function ConfirmModal({ open, title, body, danger, confirmLabel, cancelLabel,
                        onConfirm, onCancel, busy }) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === "Escape") onCancel(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onCancel]);
  if (!open) return null;
  return (
    <div className="modal-backdrop" onClick={onCancel}>
      <div className="modal" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <h3>
          {danger && <span className="icon" aria-hidden="true">!</span>}
          {title}
        </h3>
        <div className="body">{body}</div>
        <div className="actions">
          <button className="btn" onClick={onCancel} disabled={busy}>{cancelLabel}</button>
          <button className={`btn ${danger ? "danger" : "primary"}`}
                  onClick={onConfirm} disabled={busy} autoFocus>
            {busy ? "..." : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

function Spinner() {
  return <span style={{
    display: "inline-block", width: 12, height: 12, marginRight: 6,
    border: "2px solid var(--border)", borderTopColor: "var(--primary)",
    borderRadius: "50%", animation: "spin 0.8s linear infinite"
  }} />;
}

// ---------- Param editor: shared form helpers ---------------------------
// These accept a `params` object (the same shape used by the backend)
// and produce either editable JSX form sections or a raw JSON <textarea>.

function ParamNumber({ value, onChange, step }) {
  return <input type="number" step={step || "any"} value={value ?? ""}
                onChange={(e) => onChange(e.target.value === "" ? null : Number(e.target.value))} />;
}

function ParamText({ value, onChange }) {
  return <input type="text" value={value ?? ""} onChange={(e) => onChange(e.target.value)} />;
}

// A key/value pair editor for dicts like `components: {Na: 10, Cl: 10}`.
// Both columns stay editable: PHREEQC identifiers (element, species, phase
// names) are typed in by the user, so a fixed key column would leave newly
// added rows unnamed.
function DictEditor({ value, onChange, label }) {
  const { t } = useLang();
  const entries = Object.entries(value || {});
  const rename = (k, newKey) => {
    if (newKey === k) return;
    const next = {};
    for (const [existing, v] of Object.entries(value || {})) {
      next[existing === k ? newKey : existing] = v;
    }
    onChange(next);
  };
  const set = (k, v) => {
    const next = { ...value };
    if (v === "" || v === null) delete next[k];
    else next[k] = isNaN(Number(v)) || v === "" ? v : Number(v);
    onChange(next);
  };
  const add = () => onChange({ ...value, [""]: "" });
  const remove = (k) => {
    const next = { ...value }; delete next[k]; onChange(next);
  };
  return (
    <div className="kv-list-edit">
      {entries.map(([k, v]) => (
        <div key={k} className="row">
          <input value={k} onChange={(e) => rename(k, e.target.value)} />
          <input value={v} onChange={(e) => set(k, e.target.value)} />
          <button className="btn sm" onClick={() => remove(k)}>{t("tpl_remove")}</button>
        </div>
      ))}
      <button className="btn sm ghost" style={{ alignSelf: "flex-start" }} onClick={add}>{t("tpl_add")}</button>
    </div>
  );
}

// A list editor for arrays like `totals: ["Ca", "K"]` or `si: ["Calcite"]`.
function ListEditor({ value, onChange, itemType }) {
  const { t } = useLang();
  const arr = Array.isArray(value) ? value : [];
  const set = (i, v) => {
    const next = arr.slice(); next[i] = itemType === "number" ? Number(v) : v; onChange(next);
  };
  const add = () => onChange([...arr, itemType === "number" ? 0 : ""]);
  const remove = (i) => { const next = arr.slice(); next.splice(i, 1); onChange(next); };
  return (
    <div className="kv-list-edit">
      {arr.map((v, i) => (
        <div key={i} className="row">
          <input value={v} onChange={(e) => set(i, e.target.value)} />
          <span></span>
          <button className="btn sm" onClick={() => remove(i)}>{t("tpl_remove")}</button>
        </div>
      ))}
      <button className="btn sm ghost" style={{ alignSelf: "flex-start" }} onClick={add}>{t("tpl_add")}</button>
    </div>
  );
}

// Equilibrium phases like {"Calcite": (0, 10)}: keep as an editable JSON
// blob (the value is a Python tuple; the editor stores as [a, b]).
function EqPhasesEditor({ value, onChange }) {
  const { t } = useLang();
  const obj = value || {};
  const entries = Object.entries(obj);
  const set = (k, idx, raw) => {
    const next = { ...obj };
    const cur = Array.isArray(next[k]) ? next[k].slice() : [0, 0];
    cur[idx] = raw === "" ? 0 : Number(raw);
    next[k] = cur;
    onChange(next);
  };
  const rename = (k, newK) => {
    if (!newK || newK === k) return;
    const next = {};
    for (const [kk, vv] of entries) next[kk === k ? newK : kk] = vv;
    onChange(next);
  };
  const add = () => onChange({ ...obj, ["Calcite"]: [0, 10] });
  const remove = (k) => { const n = { ...obj }; delete n[k]; onChange(n); };
  return (
    <div className="kv-list-edit">
      {entries.map(([k, v]) => (
        <div key={k} className="row" style={{ gridTemplateColumns: "1fr 100px 100px auto" }}>
          <input value={k} onChange={(e) => rename(k, e.target.value)} />
          <input type="number" step="any" value={(v && v[0]) || 0} onChange={(e) => set(k, 0, e.target.value)} />
          <input type="number" step="any" value={(v && v[1]) || 0} onChange={(e) => set(k, 1, e.target.value)} />
          <button className="btn sm" onClick={() => remove(k)}>{t("tpl_remove")}</button>
        </div>
      ))}
      <button className="btn sm ghost" style={{ alignSelf: "flex-start" }} onClick={add}>{t("tpl_add")}</button>
    </div>
  );
}

// Form for a single SOLUTION block.
function SolutionForm({ value, onChange }) {
  const v = value || {};
  const set = (k, val) => onChange({ ...v, [k]: val });
  return (
    <div className="param-grid">
      <div className="kv-input"><label>id</label><ParamNumber value={v.id} onChange={(x) => set("id", x)} step="1" /></div>
      <div className="kv-input"><label>units</label>
        <select value={v.units || "ppm"} onChange={(e) => set("units", e.target.value)}>
          <option value="ppm">ppm</option>
          <option value="mg/L">mg/L</option>
          <option value="mmol/kgw">mmol/kgw</option>
          <option value="mol/kgw">mol/kgw</option>
        </select>
      </div>
      <div className="kv-input"><label>temp (°C)</label><ParamNumber value={v.temp} onChange={(x) => set("temp", x)} /></div>
      <div className="kv-input"><label>pH</label><ParamNumber value={v.pH} onChange={(x) => set("pH", x)} step="0.1" /></div>
      <div className="kv-input"><label>pe</label><ParamNumber value={v.pe} onChange={(x) => set("pe", x)} step="0.1" /></div>
    </div>
  );
}

// Top-level ParamForm -- renders one section per known param block.
function ParamForm({ params, onChange }) {
  const { t } = useLang();
  const set = (key, val) => onChange({ ...params, [key]: val });
  return (
    <div className="param-editor">
      {params.solution && (
        <div className="param-section">
          <h4>{t("tpl_param_solution")}</h4>
          <SolutionForm value={params.solution} onChange={(v) => set("solution", v)} />
          {params.solution.components !== undefined && (
            <>
              <div style={{ fontSize: 11, color: "var(--text-2)", margin: "10px 0 4px" }}>
                {t("tpl_param_components")}
              </div>
              <DictEditor value={params.solution.components}
                          onChange={(v) => set("solution", { ...params.solution, components: v })} />
            </>
          )}
        </div>
      )}
      {Array.isArray(params.solutions) && (
        <div className="param-section">
          <h4>Solutions (multi)</h4>
          {params.solutions.map((sol, i) => (
            <div key={i} style={{ marginBottom: 10, paddingBottom: 10, borderBottom: "1px dashed var(--border)" }}>
              <div style={{ fontSize: 11, color: "var(--text-2)", marginBottom: 4 }}>#{i + 1}</div>
              <SolutionForm value={sol} onChange={(v) => {
                const next = params.solutions.slice(); next[i] = v; set("solutions", next);
              }} />
              {sol.components !== undefined && (
                <div style={{ marginTop: 6 }}>
                  <DictEditor value={sol.components} onChange={(v) => {
                    const next = params.solutions.slice();
                    next[i] = { ...sol, components: v };
                    set("solutions", next);
                  }} />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      {params.equilibrium_phases && (
        <div className="param-section">
          <h4>{t("tpl_param_equilibrium")}</h4>
          <EqPhasesEditor value={params.equilibrium_phases}
                           onChange={(v) => set("equilibrium_phases", v)} />
        </div>
      )}
      {params.exchange && (
        <div className="param-section">
          <h4>{t("tpl_param_exchange")}</h4>
          <div className="param-grid">
            {Object.entries(params.exchange).map(([k, v]) => (
              <div key={k} className="kv-input"><label>{k}</label>
                <ParamText value={typeof v === "object" ? JSON.stringify(v) : v}
                           onChange={(nv) => {
                             let parsed = nv;
                             try { parsed = JSON.parse(nv); } catch { /* keep string */ }
                             set("exchange", { ...params.exchange, [k]: parsed });
                           }} />
              </div>
            ))}
          </div>
        </div>
      )}
      {params.gas_phase && (
        <div className="param-section">
          <h4>{t("tpl_param_gas")}</h4>
          <div className="param-grid">
            {Object.entries(params.gas_phase).map(([k, v]) => (
              <div key={k} className="kv-input"><label>{k}</label>
                <ParamText value={typeof v === "object" ? JSON.stringify(v) : v}
                           onChange={(nv) => {
                             let parsed = nv;
                             try { parsed = JSON.parse(nv); } catch { /* keep string */ }
                             set("gas_phase", { ...params.gas_phase, [k]: parsed });
                           }} />
              </div>
            ))}
          </div>
        </div>
      )}
      {params.transport && (
        <div className="param-section">
          <h4>{t("tpl_param_transport")}</h4>
          <div className="param-grid">
            {Object.entries(params.transport).map(([k, v]) => (
              <div key={k} className="kv-input"><label>{k}</label>
                {Array.isArray(v)
                  ? <ListEditor value={v} onChange={(nv) => set("transport", { ...params.transport, [k]: nv })} />
                  : <ParamText value={v} onChange={(nv) => {
                      let parsed = nv;
                      try { parsed = JSON.parse(nv); } catch { /* keep string */ }
                      set("transport", { ...params.transport, [k]: parsed });
                    }} />}
              </div>
            ))}
          </div>
        </div>
      )}
      {params.mix && (
        <div className="param-section">
          <h4>{t("tpl_param_mix")}</h4>
          <DictEditor value={params.mix.solutions || {}} onChange={(v) => set("mix", { ...params.mix, solutions: v })} />
        </div>
      )}
      {params.selected_output && (
        <div className="param-section">
          <h4>{t("tpl_param_selected")}</h4>
          {Object.entries(params.selected_output).map(([k, v]) => (
            <div key={k} style={{ marginBottom: 6 }}>
              <div style={{ fontSize: 11, color: "var(--text-2)", marginBottom: 2 }}>{k}</div>
              {typeof v === "boolean"
                ? <label style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                    <input type="checkbox" checked={v} onChange={(e) => {
                      const next = { ...params.selected_output, [k]: e.target.checked };
                      set("selected_output", next);
                    }} /> {String(v)}
                  </label>
                : Array.isArray(v)
                  ? <ListEditor value={v} onChange={(nv) => set("selected_output", { ...params.selected_output, [k]: nv })} />
                  : <ParamText value={v} onChange={(nv) => set("selected_output", { ...params.selected_output, [k]: nv })} />}
            </div>
          ))}
        </div>
      )}
      {params.reaction && (
        <div className="param-section">
          <h4>{t("tpl_param_reaction")}</h4>
          <div className="param-grid">
            {Object.entries(params.reaction).map(([k, v]) => (
              <div key={k} className="kv-input"><label>{k}</label>
                {typeof v === "object" && v !== null && !Array.isArray(v)
                  ? <DictEditor value={v} onChange={(nv) => set("reaction", { ...params.reaction, [k]: nv })} />
                  : <ParamText value={typeof v === "object" ? JSON.stringify(v) : v}
                               onChange={(nv) => {
                                 let parsed = nv;
                                 try { parsed = JSON.parse(nv); } catch { /* keep string */ }
                                 set("reaction", { ...params.reaction, [k]: parsed });
                               }} />}
              </div>
            ))}
          </div>
        </div>
      )}
      {params.kinetics && (
        <div className="param-section">
          <h4>{t("tpl_param_kinetics")}</h4>
          <pre className="code" style={{ fontSize: 11 }}>{JSON.stringify(params.kinetics, null, 2)}</pre>
          <div style={{ fontSize: 11, color: "var(--text-2)", marginTop: 4 }}>
            Kinetics blocks are advanced; use the JSON tab to edit.
          </div>
        </div>
      )}
      {Object.keys(params).filter(k => ![
        "solution", "solutions", "equilibrium_phases", "exchange",
        "gas_phase", "transport", "mix", "selected_output", "reaction",
        "kinetics", "rates", "initial_cell_solution"
      ].includes(k)).length > 0 && (
        <div className="param-section">
          <h4>{t("tpl_param_other")}</h4>
          {Object.entries(params).filter(([k]) => ![
            "solution", "solutions", "equilibrium_phases", "exchange",
            "gas_phase", "transport", "mix", "selected_output", "reaction",
            "kinetics", "rates", "initial_cell_solution"
          ].includes(k)).map(([k, v]) => (
            <div key={k} className="kv-input">
              <label>{k}</label>
              <ParamText value={typeof v === "object" ? JSON.stringify(v) : v}
                         onChange={(nv) => {
                           let parsed = nv;
                           try { parsed = JSON.parse(nv); } catch { /* keep string */ }
                           onChange({ ...params, [k]: parsed });
                         }} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ---------- Template detail / param editor page ------------------------
function TemplateDetailPage({ templateId, onCreate, onBack }) {
  const { t } = useLang();
  const [tpl, setTpl] = useState(null);
  const [params, setParams] = useState(null);
  const [mode, setMode] = useState("form"); // "form" | "json"
  const [jsonText, setJsonText] = useState("");
  const [jsonError, setJsonError] = useState(null);
  const [preview, setPreview] = useState(null);
  const [previewing, setPreviewing] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    API.get("/api/v1/templates/" + templateId).then(d => {
      setTpl(d);
      setParams(d.params);
      setJsonText(JSON.stringify(d.params, null, 2));
    });
  }, [templateId]);

  // When the form edits `params`, keep the JSON view in sync.
  useEffect(() => {
    if (mode === "json") return; // don't clobber user input in JSON mode
    setJsonText(JSON.stringify(params, null, 2));
  }, [params, mode]);

  // When the JSON is edited, re-validate but do NOT overwrite the form
  // (the form retains the last valid form-mode state).
  const handleJsonChange = (txt) => {
    setJsonText(txt);
    try {
      const parsed = JSON.parse(txt);
      setJsonError(null);
      setParams(parsed);
    } catch (e) {
      setJsonError(e.message);
    }
  };

  const switchMode = (next) => {
    if (next === "json") {
      setJsonText(JSON.stringify(params, null, 2));
      setJsonError(null);
    } else if (next === "form") {
      // Try to parse current JSON before leaving; bail if invalid.
      try { setParams(JSON.parse(jsonText)); setJsonError(null); }
      catch (e) { setJsonError(e.message); return; }
    }
    setMode(next);
  };

  const refreshPreview = async () => {
    setPreviewing(true);
    try {
      // /preview-input returns text/plain, not envelope; we wrap the call.
      const res = await fetch(API.base + "/api/v1/preview-input", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ params }),
      });
      const txt = await res.text();
      if (!res.ok) {
        setPreview({ error: txt });
      } else {
        setPreview({ text: txt });
      }
    } catch (e) {
      setPreview({ error: e.message });
    }
    setPreviewing(false);
  };

  const handleStart = async () => {
    if (jsonError) {
      alert(t("tpl_invalid_json") + ": " + jsonError);
      return;
    }
    setSubmitting(true);
    try {
      const run = await API.post("/api/v1/runs", { params });
      await API.post("/api/v1/runs/" + run.run_id + "/start");
      onCreate(run.run_id);
    } catch (e) {
      alert("Failed: " + e.message);
    }
    setSubmitting(false);
  };

  if (!tpl) return <div className="empty">Loading…</div>;
  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{tpl.title}</h1>
          <div className="subtitle">{tpl.summary}</div>
        </div>
        <div className="action-row">
          <button className="btn ghost" onClick={onBack}>{t("tpl_back")}</button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="edit-mode-toggle">
          <button className={mode === "form" ? "active" : ""} onClick={() => switchMode("form")}>
            {t("tpl_edit_form")}
          </button>
          <button className={mode === "json" ? "active" : ""} onClick={() => switchMode("json")}>
            {t("tpl_edit_json")}
          </button>
        </div>
        {mode === "form"
          ? <ParamForm params={params} onChange={setParams} />
          : <textarea className={"json-edit" + (jsonError ? " invalid" : "")}
                      value={jsonText} onChange={(e) => handleJsonChange(e.target.value)} />
        }
        {jsonError && <div style={{ color: "var(--error)", fontSize: 12, marginTop: 6 }}>
          {t("tpl_invalid_json")}: {jsonError}
        </div>}
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="page-header" style={{ marginBottom: 8 }}>
          <h3 style={{ fontSize: 14 }}>{t("tpl_preview")}</h3>
          <button className="btn sm" onClick={refreshPreview} disabled={previewing || !!jsonError}>
            {previewing ? "..." : "刷新 / Refresh"}
          </button>
        </div>
        {preview
          ? (preview.error
              ? <pre className="preview-pane" style={{ color: "var(--error)" }}>{preview.error}</pre>
              : <pre className="preview-pane">{preview.text}</pre>)
          : <div className="empty" style={{ padding: 16 }}>{t("tpl_no_preview")}</div>}
      </div>

      <div className="action-row" style={{ justifyContent: "flex-end" }}>
        <button className="btn primary" onClick={handleStart} disabled={submitting || !!jsonError}>
          {submitting ? "..." : t("tpl_btn_start")}
        </button>
      </div>
    </div>
  );
}

// ---------- Custom scenario page ---------------------------------------
// The custom editor owns exactly one Scenario v1 document.  Validation,
// input preview, saving and the run itself all round-trip through the
// backend, so the form, the JSON tab and the runner cannot disagree about
// what a module means.

const SOLUTION_UNITS = [
  "mol/kgw", "mmol/kgw", "umol/kgw",
  "mol/l", "mmol/l", "umol/l",
  "mg/l", "ug/l", "ppm", "ppb",
];

const MODULE_LABEL = {
  solutions: "mod_solutions",
  initial_cell_solution: "mod_initial_cell_solution",
  equilibrium_phases: "mod_equilibrium_phases",
  reaction: "mod_reaction",
  mix: "mod_mix",
  gas_phase: "mod_gas_phase",
  transport: "mod_transport",
  selected_output: "mod_selected_output",
};

function LabeledField({ label, children }) {
  return <div className="kv-input"><label>{label}</label>{children}</div>;
}

function UnitSelect({ value, onChange }) {
  // Keep an unrecognised unit visible instead of silently rewriting it, so a
  // hand-edited JSON value is never lost just by switching to the form tab.
  const units = !value || SOLUTION_UNITS.includes(value)
    ? SOLUTION_UNITS
    : [value, ...SOLUTION_UNITS];
  return (
    <select value={value || "mol/kgw"} onChange={(e) => onChange(e.target.value)}>
      {units.map((unit) => <option key={unit} value={unit}>{unit}</option>)}
    </select>
  );
}

// One widget per value type, shared by every module editor.
function FieldInput({ value, onChange }) {
  if (typeof value === "boolean") {
    return (
      <label style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
        <input type="checkbox" checked={value} onChange={(e) => onChange(e.target.checked)} />
        <span style={{ fontSize: 12, color: "var(--text-2)" }}>{String(value)}</span>
      </label>
    );
  }
  if (typeof value === "number") return <ParamNumber value={value} onChange={onChange} />;
  if (Array.isArray(value)) {
    if (value.length && value[0] !== null && typeof value[0] === "object") {
      // Not reachable for the modules shipped today; the JSON tab is the
      // authority for shapes this form has no widget for.
      return <pre className="code" style={{ fontSize: 11 }}>{JSON.stringify(value, null, 2)}</pre>;
    }
    return <ListEditor value={value} onChange={onChange} itemType={typeof value[0]} />;
  }
  if (value !== null && typeof value === "object") {
    return <DictEditor value={value} onChange={onChange} />;
  }
  return <ParamText value={value} onChange={onChange} />;
}

function SolutionEditor({ value, onChange, withId }) {
  const { t } = useLang();
  const solution = value || {};
  const set = (key, next) => onChange({ ...solution, [key]: next });
  return (
    <div>
      <div className="param-grid">
        {withId && (
          <LabeledField label="id">
            <ParamNumber value={solution.id} onChange={(x) => set("id", x)} step="1" />
          </LabeledField>
        )}
        <LabeledField label="units">
          <UnitSelect value={solution.units} onChange={(x) => set("units", x)} />
        </LabeledField>
        <LabeledField label="temp (°C)">
          <ParamNumber value={solution.temp} onChange={(x) => set("temp", x)} />
        </LabeledField>
        <LabeledField label="pH">
          <ParamNumber value={solution.pH} onChange={(x) => set("pH", x)} step="0.1" />
        </LabeledField>
        <LabeledField label="pe">
          <ParamNumber value={solution.pe} onChange={(x) => set("pe", x)} step="0.1" />
        </LabeledField>
        <LabeledField label="density">
          <ParamNumber value={solution.density} onChange={(x) => set("density", x)} step="0.001" />
        </LabeledField>
      </div>
      <div style={{ fontSize: 11, color: "var(--text-2)", margin: "10px 0 4px" }}>
        {t("tpl_param_components")}
      </div>
      <DictEditor value={solution.components} onChange={(x) => set("components", x)} />
    </div>
  );
}

function SolutionsEditor({ value, onChange }) {
  const { t } = useLang();
  const list = Array.isArray(value) ? value : [];
  const update = (index, next) => onChange(list.map((item, i) => (i === index ? next : item)));
  const remove = (index) => onChange(list.filter((_, i) => i !== index));
  const add = () => {
    const ids = list.map((item) => item && item.id).filter((id) => typeof id === "number");
    const nextId = ids.length ? Math.max(...ids) + 1 : 1;
    onChange([...list, {
      id: nextId, units: "mol/kgw", temp: 25.0, pH: 7.0, pe: 4.0, density: 1.0, components: {},
    }]);
  };
  return (
    <div>
      {list.map((solution, index) => (
        <div key={index} style={{ marginBottom: 12, paddingBottom: 10, borderBottom: "1px dashed var(--border)" }}>
          <div className="row" style={{ justifyContent: "space-between", marginBottom: 6 }}>
            <span style={{ fontSize: 11, color: "var(--text-2)" }}>
              SOLUTION {solution.id ?? index + 1}
            </span>
            <button className="btn sm" onClick={() => remove(index)}>{t("tpl_remove")}</button>
          </div>
          <SolutionEditor value={solution} withId onChange={(next) => update(index, next)} />
        </div>
      ))}
      <button className="btn sm ghost" onClick={add}>{t("custom_add_solution")}</button>
    </div>
  );
}

function ModuleEditor({ name, value, onChange }) {
  if (name === "solutions") {
    return <SolutionsEditor value={value} onChange={onChange} />;
  }
  if (name === "initial_cell_solution") {
    return <SolutionEditor value={value} withId={false} onChange={onChange} />;
  }
  if (name === "equilibrium_phases") {
    // Phase entries are [saturation_index, moles] pairs; the generic dict
    // field would flatten them into a single text value.
    return <EqPhasesEditor value={value} onChange={onChange} />;
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {Object.entries(value || {}).map(([field, fieldValue]) => (
        <div key={field}>
          <div style={{ fontSize: 11, color: "var(--text-2)", marginBottom: 3 }}>{field}</div>
          <FieldInput value={fieldValue}
                      onChange={(next) => onChange({ ...value, [field]: next })} />
        </div>
      ))}
    </div>
  );
}

function CustomScenarioPage({ onCreate, onBack }) {
  const { t, locale } = useLang();
  const [registry, setRegistry] = useState(null);
  const [loadError, setLoadError] = useState(null);
  const [typeId, setTypeId] = useState("");
  const [scenario, setScenario] = useState(null);
  const [mode, setMode] = useState("form"); // "form" | "json"
  const [jsonText, setJsonText] = useState("");
  const [jsonError, setJsonError] = useState(null);
  const [validation, setValidation] = useState(null);
  const [preview, setPreview] = useState(null);
  const [busy, setBusy] = useState("");
  const [notice, setNotice] = useState("");
  const [savedTemplates, setSavedTemplates] = useState([]);
  const [savedId, setSavedId] = useState(null);

  const refreshSaved = useCallback(() => {
    API.get("/api/v1/scenarios/templates")
      .then((d) => setSavedTemplates(d.templates || []))
      .catch(() => setSavedTemplates([]));
  }, []);

  useEffect(() => {
    API.get("/api/v1/scenarios/types")
      .then((d) => {
        setRegistry(d);
        const first = (d.types || [])[0];
        if (first) {
          setTypeId(first.id);
          setScenario(first.default_scenario);
          setJsonText(JSON.stringify(first.default_scenario, null, 2));
        }
      })
      .catch((e) => setLoadError(e.message));
    refreshSaved();
  }, [refreshSaved]);

  // The form is the source of truth; the JSON tab is regenerated from it.
  useEffect(() => {
    if (mode === "json") return;
    setJsonText(JSON.stringify(scenario, null, 2));
  }, [scenario, mode]);

  const apply = useCallback((next) => {
    setScenario(next);
    setValidation(null);
    setPreview(null);
    setNotice("");
  }, []);

  const types = (registry && registry.types) || [];
  const typeEntry = types.find((item) => item.id === typeId) || null;
  const modules = (scenario && scenario.modules) || {};
  const present = Object.keys(modules);
  const required = (typeEntry && typeEntry.required_modules) || [];
  const allowed = (typeEntry && typeEntry.allowed_modules) || [];
  const addable = allowed.filter((name) => present.indexOf(name) === -1);

  const typeLabel = (entry) => (locale === "en" && entry.label_en ? entry.label_en : entry.label);
  const typeDescription = (entry) =>
    (locale === "en" && entry.description_en ? entry.description_en : entry.description);
  const moduleLabel = (name) => t(MODULE_LABEL[name] || "custom_unknown_module");

  const chooseType = (id) => {
    const entry = types.find((item) => item.id === id);
    if (!entry) return;
    setTypeId(id);
    setSavedId(null);
    setJsonError(null);
    apply(entry.default_scenario);
  };

  const handleJsonChange = (text) => {
    setJsonText(text);
    try {
      apply(JSON.parse(text));
      setJsonError(null);
    } catch (e) {
      setJsonError(e.message);
    }
  };

  const switchMode = (next) => {
    if (next === "json") {
      setJsonText(JSON.stringify(scenario, null, 2));
      setJsonError(null);
    } else if (next === "form") {
      try {
        apply(JSON.parse(jsonText));
        setJsonError(null);
      } catch (e) {
        setJsonError(e.message);
        return;
      }
    }
    setMode(next);
  };

  const moduleDefault = (name) => {
    const entry = ((registry && registry.modules) || []).find((item) => item.id === name);
    return entry ? JSON.parse(JSON.stringify(entry.default)) : {};
  };
  const addModule = (name) =>
    apply({ ...scenario, modules: { ...modules, [name]: moduleDefault(name) } });
  const removeModule = (name) => {
    const next = { ...modules };
    delete next[name];
    apply({ ...scenario, modules: next });
  };
  const setModule = (name, value) =>
    apply({ ...scenario, modules: { ...modules, [name]: value } });
  const setScenarioName = (nextName) => apply({ ...scenario, name: nextName });

  const checkInput = async () => {
    setBusy("validate");
    try {
      const result = await API.post("/api/v1/scenarios/validate", { scenario });
      setValidation(result);
      setPreview(null);
    } catch (e) {
      setValidation({ valid: false, errors: [{ path: "$", message: e.message }], warnings: [] });
    }
    setBusy("");
  };

  const runPreview = async () => {
    setBusy("preview");
    try {
      const result = await API.post("/api/v1/scenarios/preview", { scenario });
      setValidation(result);
      setPreview(result.valid ? { text: result.input } : null);
    } catch (e) {
      setPreview({ error: e.message });
    }
    setBusy("");
  };

  const saveTemplate = async () => {
    setBusy("save");
    try {
      const body = { scenario };
      if (savedId) body.template_id = savedId;
      const record = await API.post("/api/v1/scenarios/templates", body);
      setSavedId(record.id);
      setNotice(t("custom_template_saved"));
      refreshSaved();
    } catch (e) {
      setValidation({ valid: false, errors: [{ path: "$", message: e.message }], warnings: [] });
    }
    setBusy("");
  };

  const startRun = async () => {
    setBusy("start");
    try {
      const run = await API.post("/api/v1/runs", { scenario });
      await API.post("/api/v1/runs/" + run.run_id + "/start");
      onCreate(run.run_id);
    } catch (e) {
      setNotice(e.message);
      await checkInput();
    }
    setBusy("");
  };

  const loadSaved = async (id) => {
    try {
      const record = await API.get("/api/v1/scenarios/templates/" + id);
      setSavedId(record.id);
      setTypeId(record.scenario.scenario_type);
      setMode("form");
      setJsonError(null);
      apply(record.scenario);
    } catch (e) {
      setNotice(e.message);
    }
  };

  const deleteSaved = async (id) => {
    try {
      await API.del("/api/v1/scenarios/templates/" + id);
      if (savedId === id) setSavedId(null);
      refreshSaved();
    } catch (e) {
      setNotice(e.message);
    }
  };

  if (loadError) {
    return (
      <div>
        <div className="page-header"><h1>{t("custom_title")}</h1></div>
        <div className="card">{t("custom_load_error")}: {loadError}</div>
        <div className="action-row" style={{ marginTop: 12 }}>
          <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
        </div>
      </div>
    );
  }
  if (!scenario || !typeEntry) return <div className="empty">Loading…</div>;

  const chipStyle = {
    display: "inline-flex", alignItems: "center", gap: 6,
    padding: "3px 8px", border: "1px solid var(--border)", borderRadius: 999, fontSize: 12,
  };
  const blocked = busy !== "" || !!jsonError;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{t("custom_title")}</h1>
          <div className="subtitle">{t("custom_subtitle")}</div>
        </div>
        <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="param-grid">
          <LabeledField label={t("custom_choose_type")}>
            <select value={typeId} onChange={(e) => chooseType(e.target.value)}>
              {types.map((entry) => (
                <option key={entry.id} value={entry.id}>{typeLabel(entry)}</option>
              ))}
            </select>
          </LabeledField>
          <LabeledField label={t("custom_name")}>
            <input type="text" value={scenario.name || ""}
                   placeholder={t("custom_name_placeholder")}
                   onChange={(e) => setScenarioName(e.target.value)} />
          </LabeledField>
        </div>
        <div style={{ fontSize: 12, color: "var(--text-2)", marginTop: 8 }}>
          {typeDescription(typeEntry)}
        </div>
        <div style={{ fontSize: 11, color: "var(--text-2)", marginTop: 4 }}>
          {t("custom_choose_type_help")}
        </div>
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="page-header" style={{ marginBottom: 8 }}>
          <h3 style={{ fontSize: 14 }}>{t("custom_modules")}</h3>
          <span style={{ fontSize: 11, color: "var(--text-2)" }}>{t("custom_modules_help")}</span>
        </div>
        <div className="action-row" style={{ flexWrap: "wrap", gap: 6 }}>
          {present.map((name) => (
            <span key={name} style={chipStyle}>
              <span>{moduleLabel(name)}</span>
              {required.indexOf(name) !== -1
                ? <span style={{ opacity: 0.6 }}>{t("custom_required_module")}</span>
                : <button className="btn sm ghost" style={{ padding: "0 4px" }}
                          onClick={() => removeModule(name)}>{t("tpl_remove")}</button>}
            </span>
          ))}
        </div>
        {addable.length > 0 && (
          <div className="action-row" style={{ flexWrap: "wrap", gap: 6, marginTop: 10 }}>
            <span style={{ fontSize: 11, color: "var(--text-2)" }}>{t("custom_add_module_hint")}</span>
            {addable.map((name) => (
              <button key={name} className="btn sm" onClick={() => addModule(name)}>
                + {moduleLabel(name)}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="edit-mode-toggle">
          <button className={mode === "form" ? "active" : ""} onClick={() => switchMode("form")}>
            {t("tpl_edit_form")}
          </button>
          <button className={mode === "json" ? "active" : ""} onClick={() => switchMode("json")}>
            {t("tpl_edit_json")}
          </button>
        </div>
        {mode === "form" ? (
          <div className="param-editor">
            {present.map((name) => (
              <div className="param-section" key={name}>
                <h4>{moduleLabel(name)}</h4>
                <ModuleEditor name={name} value={modules[name]}
                              onChange={(next) => setModule(name, next)} />
              </div>
            ))}
          </div>
        ) : (
          <>
            <div style={{ fontSize: 11, color: "var(--text-2)", marginBottom: 4 }}>
              {t("custom_json_help")}
            </div>
            <textarea className={"json-edit" + (jsonError ? " invalid" : "")}
                      value={jsonText} onChange={(e) => handleJsonChange(e.target.value)} />
          </>
        )}
        {jsonError && (
          <div style={{ color: "var(--error)", fontSize: 12, marginTop: 6 }}>
            {t("tpl_invalid_json")}: {jsonError}
          </div>
        )}
      </div>

      {validation && (
        <div className="card" style={{ marginBottom: 12 }}>
          {validation.valid && (validation.errors || []).length === 0 && (
            <div style={{ color: "var(--success)", fontSize: 12 }}>
              {t("custom_validation_ok")}
            </div>
          )}
          {(validation.errors || []).length > 0 && (
            <div>
              <div style={{ fontSize: 12, color: "var(--error)", marginBottom: 6 }}>
                {t("custom_validation_errors")}
              </div>
              <ul style={{ margin: 0, paddingLeft: 18, fontSize: 12 }}>
                {validation.errors.map((err, i) => (
                  <li key={i}><code>{err.path}</code> — {err.message}</li>
                ))}
              </ul>
            </div>
          )}
          {(validation.warnings || []).length > 0 && (
            <div style={{ marginTop: 8 }}>
              <div style={{ fontSize: 12, color: "var(--warn)", marginBottom: 6 }}>
                {t("custom_validation_warnings")}
              </div>
              <ul style={{ margin: 0, paddingLeft: 18, fontSize: 12 }}>
                {validation.warnings.map((warn, i) => (
                  <li key={i}><code>{warn.path}</code> — {warn.message}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="page-header" style={{ marginBottom: 8 }}>
          <h3 style={{ fontSize: 14 }}>{t("custom_preview_title")}</h3>
          <button className="btn sm" onClick={runPreview} disabled={blocked}>
            {busy === "preview" ? t("custom_previewing") : t("custom_preview")}
          </button>
        </div>
        {preview
          ? (preview.error
              ? <pre className="preview-pane" style={{ color: "var(--error)" }}>{preview.error}</pre>
              : <pre className="preview-pane">{preview.text}</pre>)
          : <div className="empty" style={{ padding: 16 }}>{t("custom_no_preview")}</div>}
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="page-header" style={{ marginBottom: 8 }}>
          <h3 style={{ fontSize: 14 }}>{t("custom_saved_title")}</h3>
          <span style={{ fontSize: 11, color: "var(--text-2)" }}>{t("custom_overwrite_hint")}</span>
        </div>
        {savedTemplates.length === 0
          ? <div className="empty" style={{ padding: 12 }}>{t("custom_saved_empty")}</div>
          : (
            <div className="action-row" style={{ flexWrap: "wrap", gap: 6 }}>
              {savedTemplates.map((item) => (
                <span key={item.id} style={chipStyle}>
                  <span>{item.name}</span>
                  <button className="btn sm ghost" style={{ padding: "0 4px" }}
                          onClick={() => loadSaved(item.id)}>{t("custom_load")}</button>
                  <button className="btn sm ghost" style={{ padding: "0 4px" }}
                          onClick={() => deleteSaved(item.id)}>{t("custom_delete")}</button>
                </span>
              ))}
            </div>
          )}
      </div>

      <div className="action-row" style={{ justifyContent: "flex-end", gap: 8 }}>
        {notice && <span style={{ fontSize: 12, color: "var(--text-2)" }}>{notice}</span>}
        <button className="btn" onClick={checkInput} disabled={blocked}>
          {busy === "validate" ? t("custom_validating") : t("custom_validate")}
        </button>
        <button className="btn" onClick={saveTemplate} disabled={blocked}>
          {busy === "save" ? t("custom_saving_template") : t("custom_save_template")}
        </button>
        <button className="btn primary" onClick={startRun} disabled={blocked}>
          {busy === "start" ? t("custom_starting") : t("custom_start")}
        </button>
      </div>
    </div>
  );
}

// ---------- Run list page ----------------------------------------------
function RunListPage({ onNew, onOpen }) {
  const { t } = useLang();
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await API.get("/api/v1/runs");
      setRuns(data.runs || []);
      setError(null);
    } catch (e) { setError(e.message); }
    setLoading(false);
  }, []);

  useEffect(() => { refresh(); }, [refresh]);

  // Poll while any run is running
  useEffect(() => {
    const hasRunning = runs.some(r => r.status === "running" || r.status === "pending");
    if (!hasRunning) return;
    const id = setInterval(refresh, 2000);
    return () => clearInterval(id);
  }, [runs, refresh]);

  const handleDelete = async (id) => {
    if (!confirm("Delete run " + id + "?")) return;
    try { await API.del("/api/v1/runs/" + id); refresh(); }
    catch (e) { alert("Delete failed: " + e.message); }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{t("runs_title")}</h1>
          <div className="subtitle">共 {runs.length} 条运行记录</div>
        </div>
        <button className="btn primary" onClick={onNew}>+ {t("new_btn")}</button>
      </div>
      {error && <div className="card" style={{ borderColor: "var(--error)", color: "var(--error)" }}>{error}</div>}
      {loading && runs.length === 0 ? <div className="empty">Loading…</div>
       : runs.length === 0 ? <div className="empty">{t("empty_runs")}</div>
       : (
        <div className="card" style={{ padding: 0 }}>
          <table className="table">
            <thead>
              <tr>
                <th>{t("name")}</th>
                <th>ID</th>
                <th>{t("status")}</th>
                <th>{t("created")}</th>
                <th>{t("updated")}</th>
                <th>{t("action")}</th>
              </tr>
            </thead>
            <tbody>
              {runs.map(r => (
                <tr key={r.run_id}>
                  <td>{r.name}</td>
                  <td className="mono">{r.run_id}</td>
                  <td><StatusBadge status={r.status} /></td>
                  <td className="mono">{r.created_at ? new Date(r.created_at * 1000).toLocaleString() : "-"}</td>
                  <td className="mono">{r.updated_at ? new Date(r.updated_at * 1000).toLocaleString() : "-"}</td>
                  <td>
                    <button className="btn sm" onClick={() => onOpen(r.run_id)}>{t("btn_view")}</button>
                    <button className="btn sm danger" onClick={() => handleDelete(r.run_id)} style={{ marginLeft: 4 }}>{t("btn_delete")}</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
       )
      }
    </div>
  );
}

// ---------- Template gallery page --------------------------------------
function TemplateGallery({ onDetail, onCustom, onBack }) {
  const { t } = useLang();
  const [templates, setTemplates] = useState([]);
  useEffect(() => { API.get("/api/v1/templates").then(d => setTemplates(d.templates || [])); }, []);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{t("templates_title")}</h1>
          <div className="subtitle">{t("templates_subtitle")}</div>
        </div>
        <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
      </div>
      <div className="card" style={{ marginBottom: 16, cursor: "pointer" }} onClick={onCustom}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
          <div>
            <h3 style={{ fontSize: 14 }}>{t("custom_entry_title")}</h3>
            <p style={{ fontSize: 12, color: "var(--text-2)", marginTop: 4 }}>
              {t("custom_entry_summary")}
            </p>
          </div>
          <span className="btn sm primary">{t("custom_entry_action")}</span>
        </div>
      </div>
      <div className="grid-3">
        {templates.map(tpl => (
          <div key={tpl.id} className="card template-card" onClick={() => onDetail(tpl.id)}>
            <span className={`level ${tpl.level}`}>{tpl.level}</span>
            <h3>{tpl.title}</h3>
            <p>{tpl.summary}</p>
            <div className="actions" onClick={(e) => e.stopPropagation()}>
              <button className="btn sm ghost" onClick={() => onDetail(tpl.id)}>{t("tpl_btn_detail")}</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---------- Run detail page --------------------------------------------
function RunDetailPage({ runId, onBack }) {
  const { t } = useLang();
  const [run, setRun] = useState(null);
  const [tab, setTab] = useState("log");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [selected, setSelected] = useState("");
  const [results, setResults] = useState(null);
  const [files, setFiles] = useState([]);
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);
  const [abortOpen, setAbortOpen] = useState(false);
  const [aborting, setAborting] = useState(false);
  const artifactPaths = new Set(files.map((file) => file.path));
  const hasArtifact = (path) => artifactPaths.has(path);
  const fallbackEvents = (run && run.log_tail ? run.log_tail : []).map((line) => {
    const match = String(line).match(/^\[([^\]]+)\]\s*(.*)$/);
    return { kind: match ? match[1] : "log", message: match ? match[2] : String(line), ts: 0 };
  });
  const logEvents = events.length ? events : fallbackEvents;

  const refreshAll = useCallback(async () => {
    try {
      const r = await API.get("/api/v1/runs/" + runId);
      setRun(r);
      const f = await API.get("/api/v1/runs/" + runId + "/files");
      setFiles(f.files || []);
    } catch (e) { setError(e.message); }
  }, [runId]);

  // Initial load + poll while running
  useEffect(() => { refreshAll(); }, [refreshAll]);
  useEffect(() => {
    if (!run) return;
    if (run.status !== "running" && run.status !== "pending") return;
    const id = setInterval(refreshAll, 2000);
    return () => clearInterval(id);
  }, [run, refreshAll]);

  // Lazy-load tab content
  useEffect(() => {
    if ((tab === "input" || (run && run.status === "failed")) && hasArtifact("input.pqi") && !input) {
      API.get("/api/v1/runs/" + runId + "/input").then(d => setInput(typeof d === "string" ? d : "")).catch(e => setError(e.message));
    }
    if (tab === "output" && hasArtifact("output.qpo") && !output) {
      API.get("/api/v1/runs/" + runId + "/output").then(d => setOutput(typeof d === "string" ? d : "")).catch(e => setError(e.message));
    }
    if (tab === "selected" && hasArtifact("selected_output.txt") && !selected) {
      API.get("/api/v1/runs/" + runId + "/selected-output").then(d => setSelected(typeof d === "string" ? d : "")).catch(e => setError(e.message));
    }
    if (tab === "results" && hasArtifact("results.json") && !results) {
      API.get("/api/v1/runs/" + runId + "/results").then(d => setResults(typeof d === "string" ? JSON.parse(d) : d)).catch(e => setError(e.message));
    }
  }, [tab, runId, input, output, selected, results, files, run]);

  // Stream events via long-poll: keep hitting /events until backoff
  useEffect(() => {
    let cancelled = false;
    let lastTs = 0;
    const poll = async () => {
      if (cancelled) return;
      try {
        const evs = parseSseEvents(await API.get("/api/v1/runs/" + runId + "/events"));
        if (Array.isArray(evs) && evs.length > lastTs) {
          setEvents(evs);
          lastTs = evs.length;
        }
      } catch (e) { /* ignore transient */ }
      if (!cancelled) setTimeout(poll, 1500);
    };
    poll();
    return () => { cancelled = true; };
  }, [runId]);

  const handleAbort = async () => {
    setAborting(true);
    try {
      await API.post("/api/v1/runs/" + runId + "/abort", {});
    } catch (e) {
      alert("Abort failed: " + e.message);
    }
    setAborting(false);
    setAbortOpen(false);
    refreshAll();
  };

  // Poll events faster while running
  const isActive = run && (run.status === "running" || run.status === "pending");

  if (error) return (
    <div className="card" style={{ borderColor: "var(--error)", color: "var(--error)" }}>
      <div style={{ marginBottom: 12 }}>{error}</div>
      <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
    </div>
  );
  if (!run) return <div className="empty">Loading…</div>;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{run.name}</h1>
          <div className="subtitle mono">{run.run_id}</div>
        </div>
        <div className="action-row">
          <StatusBadge status={run.status} />
          {isActive && <Spinner />}
          {isActive && (
            <button className="btn danger sm" onClick={() => setAbortOpen(true)}>
              {t("abort_btn")}
            </button>
          )}
          <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="kv-list">
          <div className="k">Status</div><div className="v">{run.status}</div>
          <div className="k">Created</div><div className="v">{new Date(run.created_at * 1000).toLocaleString()}</div>
          <div className="k">Updated</div><div className="v">{new Date(run.updated_at * 1000).toLocaleString()}</div>
          {run.result_summary && <>
            <div className="k">Rows</div><div className="v">{run.result_summary.row_count || 0}</div>
            <div className="k">SI extracted</div><div className="v">{run.result_summary.has_si ? "yes" : "no"}</div>
          </>}
        </div>
      </div>

      {run.status === "failed" && (
        <>
          <FailureSummary run={run} events={logEvents} input={input} />
          <div className="card" style={{ marginBottom: 16, borderColor: "var(--warning, #d97706)" }}>
            {t("run_failed_artifacts")}
          </div>
        </>
      )}

      <div className="tabs">
        <button className={tab === "log" ? "active" : ""} onClick={() => setTab("log")}>{t("tab_log")}</button>
        {hasArtifact("input.pqi") && <button className={tab === "input" ? "active" : ""} onClick={() => setTab("input")}>{t("tab_input")}</button>}
        {hasArtifact("selected_output.txt") && <button className={tab === "selected" ? "active" : ""} onClick={() => setTab("selected")}>{t("tab_selected")}</button>}
        {hasArtifact("output.qpo") && <button className={tab === "output" ? "active" : ""} onClick={() => setTab("output")}>{t("tab_output")}</button>}
        {hasArtifact("results.json") && <button className={tab === "results" ? "active" : ""} onClick={() => setTab("results")}>{t("tab_results")}</button>}
        {files.some((file) => file.path.startsWith("charts/")) && <button className={tab === "charts" ? "active" : ""} onClick={() => setTab("charts")}>{t("tab_charts")}</button>}
        <button className={tab === "files" ? "active" : ""} onClick={() => setTab("files")}>{t("tab_files")}</button>
      </div>

      {tab === "log"    && <EventLog events={logEvents} />}
      {tab === "input"  && <CodeView code={input || "(not generated yet)"} />}
      {tab === "output" && <CodeView code={output || "(not generated yet)"} />}
      {tab === "selected" && <CodeView code={selected || "(not generated yet)"} />}
      {tab === "results" && <ResultsView results={results} />}
      {tab === "charts"  && <ChartsView runId={runId} files={files} />}
      {tab === "files"   && <FileListView runId={runId} files={files} />}

      <ConfirmModal
        open={abortOpen}
        danger
        title={t("abort_title")}
        body={t("abort_body")}
        confirmLabel={t("abort_confirm")}
        cancelLabel={t("exit_cancel")}
        onConfirm={handleAbort}
        onCancel={() => { if (!aborting) setAbortOpen(false); }}
        busy={aborting}
      />
    </div>
  );
}

function FailureSummary({ run, events, input }) {
  const { t } = useLang();
  const [copied, setCopied] = useState(false);
  const step = [...events].reverse().find((event) => event.kind === "step");
  const finalError = [...events].reverse().find((event) => event.kind === "error");
  const exitMatch = finalError && String(finalError.message).match(/exit code\s+(\d+)/i);
  const exitCode = exitMatch ? exitMatch[1] : null;
  const errorCode = exitCode ? `PHREEQC_EXIT_${exitCode}` : "RUN_FAILED";
  const output = events.filter((event) =>
    (event.kind === "error" || event.kind === "stderr") && String(event.message || "").trim()
  ).slice(-8);
  const executable = events.find((event) => event.kind === "info" && String(event.message).startsWith("PHREEQC exe:"));
  const database = events.find((event) => event.kind === "info" && String(event.message).startsWith("PHREEQC database:"));

  const copyDetails = async () => {
    const keyOutput = output.map((event) => `[${event.kind}] ${event.message}`).join("\n") || "(none extracted)";
    const apiBase = window.location.origin + "/api/v1/runs/" + encodeURIComponent(run.run_id);
    const details = [
      "请帮助分析一个 PHREEQC 运行失败问题。",
      "",
      `运行 ID：${run.run_id}`,
      `运行详情地址：${apiBase}`,
      `事件日志地址：${apiBase}/events`,
      `输入文件地址：${apiBase}/input`,
      `运行阶段：${step ? step.message : "未从日志提取到"}`,
      `错误码：${errorCode}`,
      `退出码：${exitCode || "未从日志提取到"}`,
      executable ? `PHREEQC：${executable.message.replace(/^PHREEQC exe:\s*/, "")}` : "PHREEQC：未从日志提取到",
      database ? `数据库：${database.message.replace(/^PHREEQC database:\s*/, "")}` : "数据库：未从日志提取到",
      "",
      "关键日志：",
      keyOutput,
      "",
      "PHREEQC 输入文件：",
      input || "(输入文件正在加载；请稍后再次复制，或从“输入文件”标签复制。)",
      "",
      "请根据输入文件和日志解释失败原因，并给出可验证的修改建议；不要假设具体研究目标。",
    ].join("\n");
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(details);
      } else {
        const area = document.createElement("textarea");
        area.value = details;
        area.style.position = "fixed";
        area.style.opacity = "0";
        document.body.appendChild(area);
        area.select();
        document.execCommand("copy");
        area.remove();
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch (e) {
      setCopied(false);
    }
  };

  return (
    <div className="card" style={{ marginBottom: 12, borderColor: "var(--warning, #d97706)" }}>
      <div className="card-title" style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
        <span>{t("failure_summary")}</span>
        <button className="btn sm" onClick={copyDetails}>{t("failure_copy")}</button>
      </div>
      <div className="kv-list" style={{ marginTop: 10 }}>
        <div className="k">{t("failure_stage")}</div><div className="v">{step ? step.message : "-"}</div>
        <div className="k">{t("failure_error_code")}</div><div className="v mono">{errorCode}</div>
        <div className="k">{t("failure_exit_code")}</div><div className="v mono">{exitCode || "-"}</div>
        {(executable || database) && <><div className="k">{t("failure_environment")}</div><div className="v mono">{[executable, database].filter(Boolean).map((event) => event.message.replace(/^PHREEQC (exe|database):\s*/, "")).join("\n")}</div></>}
      </div>
      <div style={{ marginTop: 12, fontSize: 12, color: "var(--muted)" }}>{t("failure_output")}</div>
      {output.length ? <div className="code" style={{ marginTop: 6, maxHeight: 170 }}>{output.map((event, index) => <div key={index}>[{event.kind}] {event.message}</div>)}</div> : <div className="empty" style={{ padding: "8px 0" }}>{t("failure_no_output")}</div>}
      {copied && <div className="test-result ok" style={{ marginTop: 10 }}>{t("failure_copied")}</div>}
    </div>
  );
}

function EventLog({ events }) {
  if (!events || events.length === 0) return <div className="empty">No events yet</div>;
  return (
    <div className="event-log">
      {events.map((ev, i) => (
        <div key={i} className={`ev ${ev.kind}`}>
          <span className="ts">{new Date(ev.ts * 1000).toLocaleTimeString()}</span>
          <span className="kind">[{ev.kind}]</span>
          <span>{ev.message}</span>
        </div>
      ))}
    </div>
  );
}

function CodeView({ code }) {
  return <div className="code">{code}</div>;
}

function ResultsView({ results }) {
  if (!results) return <div className="empty">No results yet</div>;
  if (results.error) return <div className="card" style={{ borderColor: "var(--error)" }}>{results.error}</div>;
  return (
    <div className="col">
      {results.columns && results.columns.length > 0 && (
        <div className="card">
          <div className="card-title">SELECTED_OUTPUT 数据 ({results.row_count || 0} 行 × {results.columns.length} 列)</div>
          <div style={{ maxHeight: 320, overflow: "auto" }}>
            <table className="table">
              <thead>
                <tr>{results.columns.map(c => <th key={c}>{c}</th>)}</tr>
              </thead>
              <tbody>
                {(results.data || []).slice(0, 100).map((row, i) => (
                  <tr key={i}>
                    {row.map((v, j) => <td key={j} className="mono">{typeof v === "number" ? v.toExponential(3) : v}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {results.saturation_indices && (
        <div className="card">
          <div className="card-title">饱和指数 (Saturation Indices)</div>
          <SatIndexChart data={results.saturation_indices} />
          <table className="table" style={{ marginTop: 12 }}>
            <thead><tr><th>Phase</th><th>SI</th><th>State</th></tr></thead>
            <tbody>
              {normalizeSIList(results.saturation_indices).map(([k, v]) => (
                <tr key={k}>
                  <td className="mono">{k}</td>
                  <td className="mono">{typeof v === "number" ? v.toFixed(3) : v}</td>
                  <td>{typeof v === "number" ? (v > 0 ? <span style={{ color: "var(--success)" }}>supersaturated</span> : v < 0 ? <span style={{ color: "var(--primary)" }}>undersaturated</span> : "equilibrium") : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {results.species_distribution && (
        <div className="card">
          <div className="card-title">物种分布 (Species Distribution)</div>
          <pre className="code">{JSON.stringify(results.species_distribution, null, 2)}</pre>
        </div>
      )}
      {results.element_molalities && (
        <div className="card">
          <div className="card-title">元素摩尔浓度 (Element Molalities)</div>
          <pre className="code">{JSON.stringify(results.element_molalities, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

function normalizeSIList(data) {
  // Accept:
  //   list of dicts:   [{phase: "Calcite", si: 0.52}, ...]
  //   list of pairs:   [["Calcite", 0.52], ...]
  //   dict:            {Calcite: 0.52, ...}
  if (Array.isArray(data)) {
    return data.map((item) => {
      if (Array.isArray(item)) return [item[0], item[1]];
      if (item && typeof item === "object") {
        const name = item.phase || item.name || item.species || JSON.stringify(item);
        const value = item.si ?? item.value ?? item.SI;
        return [name, value];
      }
      return [String(item), null];
    });
  }
  if (data && typeof data === "object") return Object.entries(data);
  return [];
}

function SatIndexChart({ data }) {
  const ref = useRef(null);
  useEffect(() => {
    if (!ref.current || !window.echarts) return;
    const chart = window.echarts.init(ref.current);
    const entries = normalizeSIList(data);
    const names = entries.map(([k]) => k).reverse();
    const values = entries.map(([, v]) => (typeof v === "number" ? v : 0)).reverse();
    chart.setOption({
      tooltip: { trigger: "axis" },
      grid: { left: 80, right: 20, top: 20, bottom: 20 },
      xAxis: { type: "value", name: "SI" },
      yAxis: { type: "category", data: names, axisLabel: { fontSize: 10 } },
      series: [{
        type: "bar",
        data: values,
        itemStyle: { color: (p) => p.value > 0 ? "#16a34a" : p.value < 0 ? "#2563eb" : "#888" },
        label: { show: true, position: "right", formatter: (p) => Number(p.value).toFixed(2), fontSize: 10 }
      }]
    });
    const resize = () => chart.resize();
    window.addEventListener("resize", resize);
    return () => { window.removeEventListener("resize", resize); chart.dispose(); };
  }, [data]);
  const entries = normalizeSIList(data);
  return <div ref={ref} style={{ width: "100%", height: Math.max(180, entries.length * 22) }} />;
}

function ChartsView({ runId, files }) {
  const charts = files.filter(f => f.path.startsWith("charts/") && f.path.endsWith(".png"));
  if (charts.length === 0) return <div className="empty">No charts yet</div>;
  return (
    <div className="grid-2">
      {charts.map(c => (
        <div key={c.path} className="card">
          <div className="card-title">{c.path}</div>
          <img className="chart-img" src={`/api/v1/runs/${runId}/files/${c.path}`} alt={c.path} />
        </div>
      ))}
    </div>
  );
}

function FileListView({ runId, files }) {
  if (files.length === 0) return <div className="empty">No files yet</div>;
  return (
    <div className="card" style={{ padding: 0 }}>
      <table className="table">
        <thead><tr><th>Path</th><th>Size</th><th></th></tr></thead>
        <tbody>
          {files.map(f => (
            <tr key={f.path}>
              <td className="mono">{f.path}</td>
              <td className="mono">{f.size} B</td>
              <td>
                <a className="btn sm" href={`/api/v1/runs/${runId}/files/${f.path}`} download>下载</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ---------- Settings panel --------------------------------------------
function SettingsPanel({ health, onHealthChange, onBack }) {
  const { t } = useLang();
  const [data, setData] = useState(null);
  const [exePath, setExePath] = useState("");
  const [dbPath, setDbPath] = useState("");
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState(null);
  const [autoConfiguring, setAutoConfiguring] = useState(false);
  const [showOverwriteNotice, setShowOverwriteNotice] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const d = await API.get("/api/v1/system/phreeqc/candidates");
      setData(d);
      const firstAvailableExe = (d.executables || []).find((candidate) => candidate.exists);
      setExePath(
        (d.settings && d.settings.phreeqc_exe) ||
        (d.active && d.active.executable) ||
        (firstAvailableExe && firstAvailableExe.path) ||
        ""
      );
      setDbPath((d.settings && d.settings.phreeqc_database) || d.active.database || "");
    } catch (e) {
      setData({ error: e.message });
    }
  }, []);

  useEffect(() => { refresh(); }, [refresh]);

  const runTest = async (path) => {
    if (!path) return;
    setTesting(true);
    setTestResult(null);
    try {
      const r = await API.post("/api/v1/system/phreeqc/test",
                                 { executable: path, database: dbPath || undefined });
      setTestResult(r);
    } catch (e) {
      setTestResult({ ok: false, error: e.message });
    }
    setTesting(false);
  };

  const saveSettings = async () => {
    setShowOverwriteNotice(false);
    setSaving(true);
    setSaveMsg(null);
    try {
      const r = await API.post("/api/v1/system/phreeqc/settings", {
        phreeqc_exe: exePath.trim(),
        phreeqc_database: dbPath.trim(),
      });
      setSaveMsg({ ok: true, text: "已保存 / Saved" });
      // Refresh health after save so the sidebar status updates
      API.get("/api/v1/system/health").then(onHealthChange).catch(() => {});
      refresh();
    } catch (e) {
      setSaveMsg({ ok: false, text: e.message });
    }
    setSaving(false);
  };

  const requestSave = () => {
    const configured = data && data.settings;
    const isAutoConfigured = configured && configured.phreeqc_config_source === "auto";
    const pathsChanged = isAutoConfigured && (
      exePath.trim().toLowerCase() !== String(configured.phreeqc_exe || "").trim().toLowerCase() ||
      dbPath.trim().toLowerCase() !== String(configured.phreeqc_database || "").trim().toLowerCase()
    );
    if (pathsChanged) {
      setShowOverwriteNotice(true);
      return;
    }
    saveSettings();
  };

  const autoConfigure = async () => {
    setAutoConfiguring(true);
    setSaveMsg(null);
    setTestResult(null);
    try {
      const r = await API.post("/api/v1/system/phreeqc/auto-configure", {});
      setExePath(r.settings.phreeqc_exe || "");
      setDbPath(r.settings.phreeqc_database || "");
      setTestResult(r.test);
      setSaveMsg({ ok: true, text: t("settings_auto_done") });
      API.get("/api/v1/system/health").then(onHealthChange).catch(() => {});
      refresh();
    } catch (e) {
      setSaveMsg({ ok: false, text: e.message });
    }
    setAutoConfiguring(false);
  };

  const clearOverride = async (key) => {
    setSaving(true);
    try {
      const patch = key === "phreeqc_exe"
        ? { phreeqc_exe: "" }
        : { phreeqc_database: "" };
      await API.post("/api/v1/system/phreeqc/settings", patch);
      API.get("/api/v1/system/health").then(onHealthChange).catch(() => {});
      refresh();
    } catch (e) { setSaveMsg({ ok: false, text: e.message }); }
    setSaving(false);
  };

  if (!data) return <div className="empty">Loading…</div>;
  if (data.error) return <div className="card" style={{ borderColor: "var(--error)", color: "var(--error)" }}>{data.error}</div>;

  const activeExe = data.active && data.active.executable;
  const activeDb = data.active && data.active.database;
  const activeVersion = data.active && data.active.version;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{t("console_title")}</h1>
          <div className="subtitle">{t("console_subtitle")}</div>
        </div>
        <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="settings-section">
          <h4>{t("settings_active")}</h4>
          <div className="kv-list">
            <div className="k">PHREEQC</div>
            <div className="v">{activeExe || "(not found)"}</div>
            <div className="k">Database</div>
            <div className="v">{activeDb || "(not found)"}</div>
            {activeVersion && <><div className="k">{t("settings_version")}</div><div className="v">{activeVersion}</div></>}
            <div className="k">Status</div>
            <div className="v">
              {health && health.phreeqc && health.phreeqc.ok
                ? <span style={{ color: "var(--success)" }}>{t("settings_test_passed")}</span>
                : <span style={{ color: "var(--error)" }}>{t("settings_test_failed")}</span>}
            </div>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="settings-section">
          <h4>{t("settings_executables")}</h4>
          <div className="candidate-list">
            {data.executables.map((c, i) => (
              <div key={i} className="candidate"
                   onClick={() => setExePath(c.path)}
                   title="点击填入路径 / Click to fill">
                <span className={"src" + (activeExe && activeExe.toLowerCase() === c.path.toLowerCase() ? " active" : "")}>
                  {c.source}
                </span>
                <span className="path">{c.path}</span>
                <span className={"exists" + (c.exists ? "" : " no")}>
                  {c.exists ? "✓" : "✗"}
                </span>
              </div>
            ))}
            {data.executables.length === 0 && <div className="empty">No candidates</div>}
          </div>
        </div>

        <div className="settings-section">
          <h4>{t("settings_databases")}</h4>
          <div className="candidate-list">
            {data.databases.map((c, i) => (
              <div key={i} className="candidate"
                   onClick={() => setDbPath(c.path)}
                   title="点击填入路径 / Click to fill">
                <span className={"src" + (activeDb && activeDb.toLowerCase() === c.path.toLowerCase() ? " active" : "")}>
                  {c.source}
                </span>
                <span className="path">{c.path}</span>
                <span className={"exists" + (c.exists ? "" : " no")}>
                  {c.exists ? "✓" : "✗"}
                </span>
              </div>
            ))}
            {data.databases.length === 0 && <div className="empty">No candidates</div>}
          </div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 12 }}>
        <div className="settings-section">
          <div className="kv-input" style={{ marginBottom: 8 }}>
            <label>{t("settings_path_label")}</label>
            <input type="text" value={exePath} onChange={(e) => setExePath(e.target.value)}
                   placeholder={t("settings_placeholder")} />
          </div>
          <div className="kv-input" style={{ marginBottom: 8 }}>
            <label>{t("settings_db_label")}</label>
            <input type="text" value={dbPath} onChange={(e) => setDbPath(e.target.value)}
                   placeholder={t("settings_placeholder")} />
          </div>
          <div className="action-row" style={{ flexWrap: "wrap" }}>
            <button className="btn sm primary" onClick={autoConfigure} disabled={autoConfiguring || saving}>
              {autoConfiguring ? t("settings_configuring") : t("settings_auto")}
            </button>
            <button className="btn sm" onClick={() => runTest(exePath)} disabled={testing || !exePath}>
              {testing ? t("settings_testing") : t("settings_test")}
            </button>
            <button className="btn sm ghost" onClick={() => clearOverride("phreeqc_exe")} disabled={saving}>
              {t("settings_clear")} (exe)
            </button>
            <button className="btn sm ghost" onClick={() => clearOverride("phreeqc_database")} disabled={saving}>
              {t("settings_clear")} (db)
            </button>
            <span style={{ position: "relative", display: "inline-flex" }}>
              <button className="btn sm primary" onClick={requestSave} disabled={saving || autoConfiguring}>
                {saving ? "..." : t("settings_save")}
              </button>
              {showOverwriteNotice && (
                <span style={{ position: "absolute", zIndex: 5, right: 0, bottom: "calc(100% + 8px)", width: 270,
                  padding: 10, border: "1px solid var(--warning, #d97706)", borderRadius: 6, background: "var(--card, #fff)",
                  boxShadow: "0 4px 14px rgba(0,0,0,.16)", fontSize: 12, lineHeight: 1.45 }}>
                  {t("settings_override_notice")}
                  <span style={{ display: "flex", justifyContent: "flex-end", gap: 6, marginTop: 8 }}>
                    <button className="btn sm ghost" onClick={() => setShowOverwriteNotice(false)}>{t("settings_override_cancel")}</button>
                    <button className="btn sm primary" onClick={saveSettings}>{t("settings_override_confirm")}</button>
                  </span>
                </span>
              )}
            </span>
          </div>
          {saveMsg && (
            <div className={"test-result " + (saveMsg.ok ? "ok" : "bad")} style={{ marginTop: 8 }}>
              {saveMsg.text}
            </div>
          )}
          {testResult && (
            <div className={"test-result " + (testResult.ok ? "ok" : "bad")}>
              {testResult.ok ? t("settings_test_passed") : t("settings_test_failed")}
              {" — "}
              {testResult.error || ("exit_code=" + testResult.exit_code + " in " + testResult.elapsed_ms + "ms")}
              {testResult.version && <div style={{ marginTop: 4 }}>{t("settings_version")}: {testResult.version}</div>}
              {testResult.database && (
                <div style={{ marginTop: 4 }}>
                  DB: {testResult.database.ok ? "✓" : "✗"} {testResult.database.path}
                  {testResult.database.size ? " (" + (testResult.database.size / 1024).toFixed(1) + " KB)" : ""}
                  {testResult.database.error ? " — " + testResult.database.error : ""}
                </div>
              )}
              {testResult.stderr_head && (
                <div style={{ marginTop: 4, opacity: 0.8, fontSize: 11 }}>
                  {testResult.stderr_head.slice(0, 200)}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ---------- App root ---------------------------------------------------
function App() {
  const { t, locale, setLocale } = useLang();
  const [view, setView] = useState({ page: "list" });
  const [health, setHealth] = useState(null);
  const [exitOpen, setExitOpen] = useState(false);
  const [exitBusy, setExitBusy] = useState(false);
  const [exitDone, setExitDone] = useState(false);

  useEffect(() => {
    API.get("/api/v1/system/health").then(setHealth).catch(() => setHealth({ phreeqc: { ok: false } }));
  }, []);

  // Confirming exit: ask the backend to shut down, then show a final
  // message.  The user can still close the tab manually.
  const handleConfirmExit = async () => {
    setExitBusy(true);
    try {
      await API.post("/api/v1/system/shutdown", {});
    } catch (e) {
      // Server may have already closed the connection -- that is fine.
      console.warn("shutdown call:", e.message);
    }
    setExitBusy(false);
    setExitDone(true);
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="logo">P</div>
          <span>{t("workbench")}</span>
        </div>
        <div className="nav">
          <button className={view.page === "settings" ? "active" : ""}
                  onClick={() => setView({ page: "settings" })}>
            <span className="icon">{t("icon_console")}</span>
            <span>{t("nav_console")}</span>
          </button>
          <button className={view.page === "list" ? "active" : ""}
                  onClick={() => setView({ page: "list" })}>
            <span className="icon">{t("icon_runs")}</span>
            <span>{t("nav_runs")}</span>
          </button>
          <button className={view.page === "new" ? "active" : ""}
                  onClick={() => setView({ page: "new" })}>
            <span className="icon">{t("icon_new")}</span>
            <span>{t("nav_new")}</span>
          </button>
        </div>
        <div className="spacer" />
        <div className="footer">
          <HealthDot health={health} />
          {health && health.phreeqc && health.phreeqc.executable && (
            <div className="path-hint" title={health.phreeqc.executable}>
              {health.phreeqc.executable}
            </div>
          )}
        </div>
      </aside>

      <div style={{ display: "flex", flexDirection: "column", minWidth: 0 }}>
        <div className="topbar">
          {exitDone
            ? <span style={{ fontSize: 12, color: "var(--text-2)" }}>{t("exit_done")}</span>
            : <HealthDot health={health} />}
          <div className="lang-switch" role="group" aria-label="Language">
            <button className={"lang-btn" + (locale === "zh" ? " active" : "")}
                    onClick={() => setLocale("zh")} title="中文">
              {t("lang_zh")}
            </button>
            <span className="lang-sep" aria-hidden="true">|</span>
            <button className={"lang-btn" + (locale === "en" ? " active" : "")}
                    onClick={() => setLocale("en")} title="English">
              {t("lang_en")}
            </button>
          </div>
          <button className="btn danger" onClick={() => setExitOpen(true)} title={t("exit_title")}>
            <span className="icon" aria-hidden="true" style={{ width: 14, height: 14, display: "inline-grid", placeItems: "center" }}>{t("icon_exit")}</span>
            <span>{t("exit_btn")}</span>
          </button>
        </div>
        <main>
          {view.page === "list" && <RunListPage onNew={() => setView({ page: "new" })} onOpen={(id) => setView({ page: "detail", runId: id })} />}
          {view.page === "new" && <TemplateGallery
              onDetail={(tid) => setView({ page: "tplDetail", templateId: tid })}
              onCustom={() => setView({ page: "custom" })}
              onBack={() => setView({ page: "list" })} />}
          {view.page === "tplDetail" && <TemplateDetailPage
              templateId={view.templateId}
              onCreate={(id) => setView({ page: "detail", runId: id })}
              onBack={() => setView({ page: "new" })} />}
          {view.page === "custom" && <CustomScenarioPage
              onCreate={(id) => setView({ page: "detail", runId: id })}
              onBack={() => setView({ page: "new" })} />}
          {view.page === "detail" && <RunDetailPage runId={view.runId} onBack={() => setView({ page: "list" })} />}
          {view.page === "settings" && <SettingsPanel
              health={health}
              onHealthChange={setHealth}
              onBack={() => setView({ page: "list" })} />}
        </main>
      </div>

      <ConfirmModal
        open={exitOpen}
        danger
        title={t("exit_title")}
        body={t("exit_body")}
        confirmLabel={t("exit_confirm")}
        cancelLabel={t("exit_cancel")}
        onConfirm={handleConfirmExit}
        onCancel={() => { if (!exitBusy) setExitOpen(false); }}
        busy={exitBusy}
      />
    </div>
  );
}

// Mount
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<LangProvider><App /></LangProvider>);
