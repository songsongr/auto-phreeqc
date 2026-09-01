// =====================================================================
// PHREEQC Workbench - Frontend entry point
// Loaded as type="text/babel" so JSX works without a build step.
// =====================================================================

const { useState, useEffect, useCallback, useRef, createContext, useContext } = React;

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

// ---------- i18n -------------------------------------------------------
const t = (key) => I18N[window.__locale || "zh"][key] || key;
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
    nav_settings: "设置",
    icon_settings: "⚙",
    settings_title: "PHREEQC 路径设置",
    settings_subtitle: "自动发现 + 可达性测试 + 手动指定。",
    settings_executables: "可执行文件候选",
    settings_databases: "数据库候选",
    settings_active: "当前生效",
    settings_use: "使用此路径",
    settings_test: "测试可及性",
    settings_save: "保存设置",
    settings_testing: "测试中…",
    settings_path_label: "PHREEQC 可执行文件",
    settings_db_label: "PHREEQC 数据库",
    settings_placeholder: "留空以使用自动发现",
    settings_test_passed: "✓ 可用",
    settings_test_failed: "✗ 失败",
    settings_clear: "清除",
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
    abort_btn: "中止计算",
    abort_title: "中止该模拟？",
    abort_body: "正在运行的 PHREEQC 进程会被立即终止，已生成的文件保留在 workspace 中。",
    abort_confirm: "中止",
    status_aborted: "已中止",
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
    nav_settings: "Settings",
    icon_settings: "⚙",
    settings_title: "PHREEQC path settings",
    settings_subtitle: "Auto-discovery + reachability test + manual override.",
    settings_executables: "Executable candidates",
    settings_databases: "Database candidates",
    settings_active: "Currently in use",
    settings_use: "Use this",
    settings_test: "Test reachability",
    settings_save: "Save settings",
    settings_testing: "Testing…",
    settings_path_label: "PHREEQC executable",
    settings_db_label: "PHREEQC database",
    settings_placeholder: "Leave empty for auto-discovery",
    settings_test_passed: "✓ OK",
    settings_test_failed: "✗ failed",
    settings_clear: "Clear",
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
    abort_btn: "Abort",
    abort_title: "Abort this simulation?",
    abort_body: "The running PHREEQC process will be terminated. Generated files are kept in the workspace.",
    abort_confirm: "Abort",
    status_aborted: "aborted",
  },
};
window.__locale = "zh";

// ---------- Shared components -----------------------------------------
function StatusBadge({ status }) {
  return <span className={`badge ${status}`}>{status || "unknown"}</span>;
}

function HealthDot({ health }) {
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
function DictEditor({ value, onChange, label }) {
  const entries = Object.entries(value || {});
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
          <input value={k} disabled style={{ background: "var(--surface-2)" }} />
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

// ---------- Run list page ----------------------------------------------
function RunListPage({ onNew, onOpen }) {
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
function TemplateGallery({ onCreate, onDetail, onBack }) {
  const [templates, setTemplates] = useState([]);
  useEffect(() => { API.get("/api/v1/templates").then(d => setTemplates(d.templates || [])); }, []);

  const handleStart = async (tid, e) => {
    if (e) e.stopPropagation();
    try {
      const run = await API.post("/api/v1/runs", { template_id: tid });
      await API.post("/api/v1/runs/" + run.run_id + "/start");
      onCreate(run.run_id);
    } catch (err) { alert("Failed: " + err.message); }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{t("templates_title")}</h1>
          <div className="subtitle">{t("templates_subtitle")}</div>
        </div>
        <button className="btn ghost" onClick={onBack}>← {t("btn_back")}</button>
      </div>
      <div className="grid-3">
        {templates.map(tpl => (
          <div key={tpl.id} className="card template-card" onClick={() => onDetail(tpl.id)}>
            <span className={`level ${tpl.level}`}>{tpl.level}</span>
            <h3>{tpl.title}</h3>
            <p>{tpl.summary}</p>
            <div className="actions" onClick={(e) => e.stopPropagation()}>
              <button className="btn sm ghost" onClick={() => onDetail(tpl.id)}>{t("tpl_btn_detail")}</button>
              <button className="btn sm primary" onClick={(e) => handleStart(tpl.id, e)}>{t("tpl_btn_start")}</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---------- Run detail page --------------------------------------------
function RunDetailPage({ runId, onBack }) {
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
    if (tab === "input"    && !input)    API.get("/api/v1/runs/" + runId + "/input").then(d => setInput(typeof d === "string" ? d : "")).catch(e => setError(e.message));
    if (tab === "output"   && !output)   API.get("/api/v1/runs/" + runId + "/output").then(d => setOutput(typeof d === "string" ? d : "")).catch(e => setError(e.message));
    if (tab === "selected" && !selected) API.get("/api/v1/runs/" + runId + "/selected-output").then(d => setSelected(typeof d === "string" ? d : "")).catch(e => setError(e.message));
    if (tab === "results"  && !results)  API.get("/api/v1/runs/" + runId + "/results").then(d => setResults(typeof d === "string" ? JSON.parse(d) : d)).catch(e => setError(e.message));
  }, [tab, runId, input, output, selected, results]);

  // Stream events via long-poll: keep hitting /events until backoff
  useEffect(() => {
    let cancelled = false;
    let lastTs = 0;
    const poll = async () => {
      if (cancelled) return;
      try {
        const evs = await API.get("/api/v1/runs/" + runId + "/events");
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

  if (error) return <div className="card" style={{ borderColor: "var(--error)", color: "var(--error)" }}>{error}</div>;
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

      <div className="tabs">
        <button className={tab === "log" ? "active" : ""} onClick={() => setTab("log")}>{t("tab_log")}</button>
        <button className={tab === "input" ? "active" : ""} onClick={() => setTab("input")}>{t("tab_input")}</button>
        <button className={tab === "selected" ? "active" : ""} onClick={() => setTab("selected")}>{t("tab_selected")}</button>
        <button className={tab === "output" ? "active" : ""} onClick={() => setTab("output")}>{t("tab_output")}</button>
        <button className={tab === "results" ? "active" : ""} onClick={() => setTab("results")}>{t("tab_results")}</button>
        <button className={tab === "charts" ? "active" : ""} onClick={() => setTab("charts")}>{t("tab_charts")}</button>
        <button className={tab === "files" ? "active" : ""} onClick={() => setTab("files")}>{t("tab_files")}</button>
      </div>

      {tab === "log"    && <EventLog events={events} />}
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
  const [data, setData] = useState(null);
  const [exePath, setExePath] = useState("");
  const [dbPath, setDbPath] = useState("");
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState(null);

  const refresh = useCallback(async () => {
    try {
      const d = await API.get("/api/v1/system/phreeqc/candidates");
      setData(d);
      setExePath((d.settings && d.settings.phreeqc_exe) || d.active.executable || "");
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

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{t("settings_title")}</h1>
          <div className="subtitle">{t("settings_subtitle")}</div>
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
            <button className="btn sm" onClick={() => runTest(exePath)} disabled={testing || !exePath}>
              {testing ? t("settings_testing") : t("settings_test")}
            </button>
            <button className="btn sm ghost" onClick={() => clearOverride("phreeqc_exe")} disabled={saving}>
              {t("settings_clear")} (exe)
            </button>
            <button className="btn sm ghost" onClick={() => clearOverride("phreeqc_database")} disabled={saving}>
              {t("settings_clear")} (db)
            </button>
            <button className="btn sm primary" onClick={saveSettings} disabled={saving}>
              {saving ? "..." : t("settings_save")}
            </button>
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
          <button className={view.page === "settings" ? "active" : ""}
                  onClick={() => setView({ page: "settings" })}>
            <span className="icon">{t("icon_settings")}</span>
            <span>{t("nav_settings")}</span>
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
          <button className="btn danger" onClick={() => setExitOpen(true)} title={t("exit_title")}>
            <span className="icon" aria-hidden="true" style={{ width: 14, height: 14, display: "inline-grid", placeItems: "center" }}>{t("icon_exit")}</span>
            <span>{t("nav_runs") === "运行列表" ? "退出" : "Exit"}</span>
          </button>
        </div>
        <main>
          {view.page === "list" && <RunListPage onNew={() => setView({ page: "new" })} onOpen={(id) => setView({ page: "detail", runId: id })} />}
          {view.page === "new" && <TemplateGallery
              onCreate={(id) => setView({ page: "detail", runId: id })}
              onDetail={(tid) => setView({ page: "tplDetail", templateId: tid })}
              onBack={() => setView({ page: "list" })} />}
          {view.page === "tplDetail" && <TemplateDetailPage
              templateId={view.templateId}
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
root.render(<App />);
