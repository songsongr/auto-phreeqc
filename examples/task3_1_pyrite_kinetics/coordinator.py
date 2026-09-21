"""
考题 3.1 — 黄铁矿氧化动力学模拟 (Pyrite Oxidation Kinetics)

黄铁矿在富氧环境下的溶解过程，考虑动力学速率方程 (RATES/KINETICS)，
二次矿物沉淀 (Fe(OH)3(a), Jarosite-K)，
计算 100 天内系统 pH 和总铁浓度的随时间变化趋势。

速率方程: Williamson & Rimstidt (1994)
  R = k * A * [O2]^0.5 * [H+]^(-0.11) * (m/m0)^(2/3)

协调脚本: 生成 → 运行 → 解析 → 可视化 四步全自动化
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

WORKSPACE = Path(__file__).resolve().parent
WORKSPACE.mkdir(exist_ok=True)

from phreeqc_auto.generate_input import generate_single_simulation, write_input_file
from phreeqc_auto.run_phreeqc import run_simulation
from phreeqc_auto.parse_output import parse_selected_output, extract_saturation_indices, to_json
from phreeqc_auto.visualize import plot_selected_output_sweep, plot_saturation_indices


def build_params() -> dict:
    """构建黄铁矿氧化动力学模拟参数。"""

    time_steps = [
        3600, 7200, 21600, 86400, 172800, 259200,
        432000, 604800, 864000, 1209600, 1728000,
        2419200, 3283200, 4320000, 5529600, 6912000,
        8467200, 8640000,
    ]

    rates_code = [
        "10 k = parm(1)",
        "20 a0 = parm(2)",
        "30 n2 = parm(3)",
        "40 nH = parm(4)",
        "50 mi = parm(5)",
        "90 if M <= 0 then goto 200",
        "100 a_now = a0 * (M/mi)^(2/3)",
        "110 o2v = TOT(\"O(0)\")",
        "120 if o2v <= 0 then o2v = 1e-12",
        "130 rate = k * a_now * o2v^n2 * ACT(\"H+\")^(-nH)",
        "140 delta = rate * TIME",
        "150 if delta > M then delta = M",
        "200 SAVE delta",
    ]

    params = {
        "solution": {
            "id": 1,
            "units": "mol/kgw",
            "temp": 25.0,
            "pH": 7.0,
            "pe": 4.0,
            "density": 1.0,
            "components": {
                "K": "1e-4",
                "Na": "1e-4",
                "Cl": "1e-4",
            },
        },
        "equilibrium_phases": {
            "O2(g)": (-0.68, 10.0),
            "Fe(OH)3(a)": (0.0, 0.0),
            "Jarosite-K": (0.0, 0.0),
        },
        "kinetics": {
            "reactants": [{
                "name": "Pyrite",
                "formula": "FeS2",
                "stoichiometric_coefficient": 1.0,
                "m": 0.5,
                "m0": 0.5,
                "parms": [1.0e-7, 100.0, 0.5, -0.11, 0.5],
                "tol": 1e-8,
                "steps": time_steps,
                "cvode": True,
            }],
        },
        "rates": [{
            "name": "Pyrite",
            "code": rates_code,
        }],
        "selected_output": {
            "reset": True,
            "step": True,
            "pH": True,
            "pe": True,
            "temperature": False,
            "totals": ["Fe", "S", "K"],
            "si": ["Pyrite", "Fe(OH)3(a)", "Goethite", "Jarosite-K"],
            "equilibrium_phases": [
                "Pyrite", "Fe(OH)3(a)", "Goethite", "Jarosite-K", "O2(g)",
            ],
        },
    }
    return params


def main():
    print("=" * 60)
    print("考题 3.1: 黄铁矿氧化动力学模拟")
    print("=" * 60)

    # ── Step 1: Generate input ──
    print("\n[1/4] 生成 PHREEQC 输入文件...")
    params = build_params()
    pqi_content = generate_single_simulation(params, output_file="selected.txt")
    input_path = write_input_file(pqi_content, os.path.join(WORKSPACE, "input.pqi"))
    print(f"  [OK] 输入文件: {input_path}")

    # ── Step 2: Run simulation ──
    print("\n[2/4] 运行 PHREEQC 模拟 (动力学, 100天)...")
    result = run_simulation(
        input_file=input_path,
        output_file=os.path.join(WORKSPACE, "output.qpo"),
        cwd=WORKSPACE,
        timeout=300,
    )

    if not result["success"]:
        print(f"  [FAIL] PHREEQC 运行失败!")
        print(f"  stdout:\n{result['stdout'][:2000]}")
        print(f"  stderr:\n{result['stderr'][:2000]}")
        return

    print(f"  [OK] 模拟完成, exit_code={result['exit_code']}")
    output_text = result["stdout"]

    # ── Step 3: Parse output ──
    print("\n[3/4] 解析模拟结果...")
    selected_path = os.path.join(WORKSPACE, "selected.txt")
    selected = parse_selected_output(selected_path)

    if "error" in selected:
        print(f"  [FAIL] 解析 SELECTED_OUTPUT 失败: {selected['error']}")
        return

    print(f"  [OK] SELECTED_OUTPUT: {selected['row_count']} 时间步, "
          f"{len(selected['columns'])} 列")
    print(f"  列名: {', '.join(selected['columns'])}")

    # Print key time series summary
    cols = selected["columns"]
    data = selected["data"]
    # Filter to only 'react' state rows (skip initial i_soln)
    react_data = [r for r in data if len(r) > 1 and r[1] == "react"]
    if not react_data:
        react_data = data  # fallback
    if react_data:
        ti_col = cols.index("time")
        ph_col = cols.index("pH")
        pe_col = cols.index("pe")
        fe_col = cols.index("Fe") if "Fe" in cols else -1
        s_col = cols.index("S") if "S" in cols else -1
        si_col = cols.index("si_Goethite") if "si_Goethite" in cols else cols.index("si_Fe(OH)3(a)")
        print("\n  时间序列摘要:")
        print(f"  {'步':>3s} {'时间/天':>9s} {'pH':>7s} {'pe':>7s} "
              f"{'Fe/mol':>12s} {'S/mol':>12s} {'SI_Goe':>8s}")
        print(f"  {'-'*60}")
        for idx in [0, len(react_data)//4, len(react_data)//2, 3*len(react_data)//4, -1]:
            row = react_data[idx]
            print(f"  {idx+1:3d} {row[ti_col]/86400:9.3f} {row[ph_col]:7.3f} "
                  f"{row[pe_col]:7.2f} {row[fe_col]:12.4e} {row[s_col]:12.4e} "
                  f"{row[si_col]:8.3f}")

    # Extract final saturation indices
    si_final = extract_saturation_indices(output_text, last=True)
    print(f"\n  最终饱和指数 (last state):")
    for si in si_final:
        print(f"    {si['phase']:<20s} SI = {si['si']:8.3f}")

    # ── Save results.json ──
    results_json = to_json(
        selected,
        saturation_indices=si_final,
        metadata={
            "title": "黄铁矿氧化动力学模拟",
            "date": "2026-05-12",
            "database": "phreeqc.dat",
            "pyrite_initial_mol": 0.5,
            "rate_constant": "1e-7 mol/m2/s",
            "surface_area": "100 m2",
            "time_days": 100,
        },
    )
    results_path = os.path.join(WORKSPACE, "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        f.write(results_json)
    print(f"  [OK] 结果保存到: {results_path}")

    # ── Step 4: Visualize ──
    print("\n[4/4] 生成可视化图表...")
    charts_dir = os.path.join(WORKSPACE, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    # --- Convert time from seconds to days for readable plots ---
    import copy
    selected_days = copy.deepcopy(selected)
    try:
        time_idx = selected_days["columns"].index("time")
        for row in selected_days["data"]:
            row[time_idx] = row[time_idx] / 86400.0
        selected_days["columns"][time_idx] = "time_days"
    except (ValueError, IndexError):
        selected_days = selected

    # Chart 1: pH over time
    plot_selected_output_sweep(
        selected_days,
        x_column="time_days",
        y_columns=["pH"],
        title="黄铁矿氧化动力学 — pH 时间演化 (100 天)",
        xlabel="时间 (天)",
        filepath=os.path.join(charts_dir, "ph_vs_time.png"),
    )

    # Chart 2: Total Fe and S over time
    plot_selected_output_sweep(
        selected_days,
        x_column="time_days",
        y_columns=["Fe", "S"],
        title="总 Fe 和总 S 浓度时间演化",
        xlabel="时间 (天)",
        filepath=os.path.join(charts_dir, "tot_fe_s_vs_time.png"),
    )

    # Chart 3: Saturation indices over time
    si_cols = [c for c in selected_days["columns"] if c.startswith("si_")]
    if si_cols:
        plot_selected_output_sweep(
            selected_days,
            x_column="time_days",
            y_columns=si_cols,
            title="矿物饱和指数时间演化",
            xlabel="时间 (天)",
            filepath=os.path.join(charts_dir, "si_vs_time.png"),
        )

    # Chart 4: d_Phase amounts over time (moles of precipitation/dissolution)
    dphase_cols = [c for c in selected_days["columns"] if c.startswith("d_")]
    if dphase_cols:
        plot_selected_output_sweep(
            selected_days,
            x_column="time_days",
            y_columns=dphase_cols,
            title="相摩尔量变化 (Δ moles) 时间演化",
            xlabel="时间 (天)",
            filepath=os.path.join(charts_dir, "phase_delta_vs_time.png"),
        )

    print(f"  [OK] 图表保存到: {charts_dir}")
    print(f"\n{'='*60}")
    print("模拟完成!")
    print(f"工作目录: {WORKSPACE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
