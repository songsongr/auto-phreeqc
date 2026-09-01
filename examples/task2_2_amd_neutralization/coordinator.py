"""
Task 2.2: AMD Neutralization with Calcite (Limestone) Titration
Coordinator script — 4-step workflow: generate → run → parse → visualize

Simulates adding calcite powder stepwise to acid mine drainage (pH=2, H2SO4-based)
until pH reaches ~7. Tracks calcite consumption and gypsum precipitation.

AMD composition (typical high-sulfide coal mine drainage):
    Fe(2) = 500 mg/L, Fe(3) = 50 mg/L, Al = 200 mg/L, Mn = 50 mg/L
    S(6) = 2600 mg/L (charge-balanced with metal cations at pH 2)
"""

import json
import os
import sys

# --- Path setup ---
project_root = r"C:\Users\songsongr\Desktop\claudecodel_proj\auto_phreeqc_proj"
sys.path.insert(0, os.path.join(project_root, ".claude", "skills", "phreeqc-auto", "scripts"))
workspace = os.path.join(project_root, "workspace", "task2_2_amd_neutralization")

from generate_input import (
    generate_solution_block,
    generate_equilibrium_phases_block,
    generate_reaction_block,
    generate_selected_output_block,
    write_input_file,
)
from run_phreeqc import run_simulation
from parse_output import (
    parse_selected_output,
    extract_saturation_indices,
    extract_species_distribution,
    extract_element_molalities,
    extract_ionic_strength,
    to_json,
)
from visualize import plot_selected_output_sweep, plot_saturation_indices


def build_input() -> str:
    """Build the PHREEQC input file for AMD calcite titration."""
    blocks = []

    # --- Title ---
    blocks.append("TITLE Task 2.2: AMD Neutralization with Calcite (Limestone Powder)")

    # --- SOLUTION: Acid Mine Drainage ---
    sol_block = generate_solution_block(
        solution_id=1,
        units="mg/L",
        temp=25.0,
        pH=2.0,
        pe=4.0,
        density=1.0,
        components={
            "Fe(2)": 500,
            "Fe(3)": 50,
            "Al": 200,
            "Mn": 50,
            "S(6)": 2600,
        },
    )
    blocks.append(sol_block)

    # --- EQUILIBRIUM_PHASES: allow precipitates + open CO2 system ---
    # Gypsum, Fe(OH)3(a), Gibbsite: SI=0, 0 mol = precipitate-only
    # CO2(g): log PCO2 = -3.4 (atmospheric), 10 mol reservoir
    # Calcite: SI=0, 0 mol = precipitate-only (if oversaturated during neutralization)
    eq_block = generate_equilibrium_phases_block(
        phases={
            "Gypsum": (0.0, 0.0),
            "Fe(OH)3(a)": (0.0, 0.0),
            "Gibbsite": (0.0, 0.0),
            "CO2(g)": (-3.4, 10.0),
            "Calcite": (0.0, 0.0),
        },
        block_id=1,
    )
    blocks.append(eq_block)

    # --- REACTION: stepwise calcite addition ---
    # 0.05 mol total in 100 steps = 0.0005 mol/step
    # Expected consumption to pH 7: ~0.02-0.03 mol (based on acid capacity estimate)
    rxn_block = generate_reaction_block(
        reactants={"Calcite": 1.0},
        block_id=1,
        moles=0.05,
        steps=100,
    )
    blocks.append(rxn_block)

    # --- SELECTED_OUTPUT: track every reaction step ---
    so_block = generate_selected_output_block(
        file="selected_output.txt",
        reset=False,
        step=True,
        equilibrium_phases=["Gypsum", "Fe(OH)3(a)", "Gibbsite", "Calcite"],
        pH=True,
        pe=True,
        totals=["Ca", "S", "Fe", "Al", "Mn", "C(4)"],
        si=["Calcite", "Gypsum", "Fe(OH)3(a)", "Gibbsite"],
    )
    blocks.append(so_block)

    return "\n\n".join(blocks) + "\n\nEND"


def main():
    print("=" * 60)
    print("Task 2.2: AMD Neutralization with Calcite")
    print("=" * 60)

    # Step 1: Generate input
    print("\n[1/4] Generating PHREEQC input file...")
    input_content = build_input()
    input_path = write_input_file(input_content, os.path.join(workspace, "input.pqi"))
    print(f"  Input written to: {input_path}")

    # Step 2: Run simulation
    print("\n[2/4] Running PHREEQC simulation...")
    result = run_simulation(
        input_file=input_path,
        output_file=os.path.join(workspace, "output.qpo"),
        cwd=workspace,
        timeout=300,
    )
    if not result["success"]:
        print(f"  [FAIL] PHREEQC failed: {result['error']}")
        print(f"  stdout:\n{result['stdout'][:2000]}")
        return 1
    print(f"  [OK] Simulation completed successfully")

    # Step 3: Parse output
    print("\n[3/4] Parsing results...")

    # Parse selected output (reaction step data)
    so_path = os.path.join(workspace, "selected_output.txt")
    if not os.path.isfile(so_path):
        print(f"  [FAIL] selected_output.txt not found at {so_path}")
        return 1

    so_data = parse_selected_output(so_path)
    if "error" in so_data:
        print(f"  [FAIL] Parse error: {so_data['error']}")
        return 1

    print(f"  Selected output: {so_data['row_count']} rows, {len(so_data['columns'])} columns")
    print(f"  Columns: {so_data['columns']}")

    # Read full output text for SI, species, elements
    with open(os.path.join(workspace, "output.qpo"), encoding="utf-8") as f:
        output_text = f.read()

    # Extract final state data
    si_list = extract_saturation_indices(output_text, last=True)
    species = extract_species_distribution(output_text, last=True)
    elements = extract_element_molalities(output_text, last=True)
    ionic_str = extract_ionic_strength(output_text, last=True)

    print(f"  Final saturation indices: {len(si_list)} phases")
    print(f"  Final species: {len(species)} species")
    print(f"  Final elements: {len(elements)} elements")
    print(f"  Final ionic strength: {ionic_str:.4f} mol/kgw" if ionic_str else "  Ionic strength: N/A")

    # Step 4: Analyze and visualize
    print("\n[4/4] Analyzing and visualizing...")

    # --- ANALYSIS: Find pH=7 crossing point ---
    columns = so_data["columns"]
    data = so_data["data"]

    ph_idx = columns.index("pH") if "pH" in columns else -1
    if ph_idx < 0:
        print("  [FAIL] pH column not found in selected output")
        return 1

    # Extract pH series
    ph_series = [row[ph_idx] for row in data]
    step_size = 0.05 / 100  # 0.0005 mol calcite per step

    # Find where pH crosses 7.0
    calcite_to_ph7 = None
    step_at_ph7 = None
    for i, ph in enumerate(ph_series):
        if ph >= 7.0:
            step_at_ph7 = i + 1  # 1-indexed step
            calcite_to_ph7 = step_at_ph7 * step_size
            break

    if calcite_to_ph7 is None:
        print("  [WARN] pH never reached 7.0 within 100 steps (0.05 mol calcite)")
        step_at_ph7 = len(ph_series)
        calcite_to_ph7 = step_at_ph7 * step_size

    print(f"\n  {'='*50}")
    print(f"  KEY RESULT: pH 7.0 reached at step {step_at_ph7}")
    print(f"  Calcite consumed: {calcite_to_ph7:.4f} mol ({calcite_to_ph7*100.09:.2f} g as CaCO3)")
    print(f"  Final pH: {ph_series[-1]:.2f}")

    # Find gypsum precipitation at pH=7
    # In EQUILIBRIUM_PHASES with 0 initial moles:
    # d_Phase > 0 = phase precipitated (added to assemblage)
    # The d_ column shows cumulative change from initial state
    gypsum_at_ph7 = None
    if "d_Gypsum" in columns:
        gy_idx = columns.index("d_Gypsum")
        gypsum_series = [row[gy_idx] for row in data]
        if step_at_ph7 is not None and step_at_ph7 <= len(gypsum_series):
            gypsum_at_ph7 = gypsum_series[step_at_ph7 - 1]
            gypsum_mass = gypsum_at_ph7 * 172.17  # CaSO4·2H2O molar mass
            print(f"  Gypsum precipitated at pH 7: {gypsum_at_ph7:.4f} mol ({gypsum_mass:.2f} g)")
        final_gypsum = gypsum_series[-1]
        print(f"  Final Gypsum precipitated: {final_gypsum:.4f} mol ({final_gypsum*172.17:.2f} g)")

    # Fe(OH)3 and Gibbsite precipitation (positive = precipitated)
    for min_name, molar_mass in [("d_Fe(OH)3(a)", 106.87), ("d_Gibbsite", 78.00)]:
        if min_name in columns:
            min_idx = columns.index(min_name)
            min_series = [row[min_idx] for row in data]
            final_precip = min_series[-1]
            min_label = min_name.replace("d_", "")
            print(f"  Final {min_label} precipitated: {final_precip:.4f} mol ({final_precip*molar_mass:.2f} g)")

    # Calcite precipitation (after pH 7, solution becomes saturated)
    if "d_Calcite" in columns:
        cal_idx = columns.index("d_Calcite")
        cal_series = [row[cal_idx] for row in data]
        final_calcite_precip = cal_series[-1]
        print(f"  Final Calcite re-precipitated: {final_calcite_precip:.4f} mol ({final_calcite_precip*100.09:.2f} g)")

    # Actual net calcite consumption = added - re-precipitated
    net_calcite = calcite_to_ph7 - (cal_series[step_at_ph7 - 1] if step_at_ph7 and step_at_ph7 <= len(cal_series) else 0)
    print(f"  Net calcite consumed to pH 7: {net_calcite:.4f} mol ({net_calcite*100.09:.2f} g)")

    # Precipitation onset detection
    print(f"\n  --- Precipitation Sequence ---")
    precip_phases_info = {
        "d_Fe(OH)3(a)": ("Fe(OH)3(a)", 106.87),
        "d_Gibbsite": ("Gibbsite", 78.00),
        "d_Gypsum": ("Gypsum", 172.17),
        "d_Calcite": ("Calcite", 100.09),
    }
    precip_events = []
    for col_name, (label, mass) in precip_phases_info.items():
        if col_name in columns:
            col_idx = columns.index(col_name)
            # Find first step where precipitation > 0
            for i, row in enumerate(data):
                if row[col_idx] > 0:
                    ph_at_onset = ph_series[i]
                    calcite_at_onset = (i + 1) * step_size
                    precip_events.append((calcite_at_onset, label, ph_at_onset, i+1, mass, row[col_idx]))
                    break

    precip_events.sort()  # Sort by calcite consumption
    # Also get final amounts
    final_amounts = {}
    for col_name, (label, mass) in precip_phases_info.items():
        if col_name in columns:
            col_idx = columns.index(col_name)
            final_amounts[label] = (data[-1][col_idx], mass)

    for cal, label, ph, step, mass, onset_amt in precip_events:
        final_amt, fmass = final_amounts.get(label, (onset_amt, mass))
        print(f"  {label}: onset at pH {ph:.2f} ({cal*1000:.1f} mmol calcite, step {step}), "
              f"final {final_amt*1000:.2f} mmol ({final_amt*fmass:.2f} g)")

    # pH buffer plateau analysis
    print(f"\n  --- pH Buffer Regions ---")
    print(f"  Initial pH: {ph_series[0]:.2f}")

    # Calculate pH change rate (delta pH per mmol calcite)
    ph_deltas = []
    for i in range(1, len(ph_series)):
        dpH = ph_series[i] - ph_series[i-1]
        dCal = step_size * 1000  # mmol
        if dCal > 0:
            ph_deltas.append(dpH / dCal)

    # Identify the Al buffer exhaustion (the massive pH jump)
    max_dph_idx = max(range(len(ph_deltas)), key=lambda i: ph_deltas[i])
    print(f"  Max pH jump: step {max_dph_idx+2}: pH {ph_series[max_dph_idx]:.2f} -> {ph_series[max_dph_idx+1]:.2f} "
          f"(delta = {ph_deltas[max_dph_idx]*step_size*1000:.1f} pH/mmol calcite)")

    # Free acid buffer (pH 2-3): relatively steep slope
    free_acid_end = None
    for i, ph in enumerate(ph_series):
        if ph >= 3.0:
            free_acid_end = i
            break
    if free_acid_end:
        print(f"  Free acid neutralization: pH 2.0 -> 3.0, {free_acid_end*step_size*1000:.1f} mmol calcite")

    # Fe hydrolysis buffer (from Fe(OH)3 onset to Gibbsite onset)
    fe_event = next((e for e in precip_events if e[1] == "Fe(OH)3(a)"), None)
    al_event = next((e for e in precip_events if e[1] == "Gibbsite"), None)
    if fe_event and al_event:
        buffer_cal = (al_event[0] - fe_event[0]) * 1000  # mmol
        print(f"  Fe hydrolysis buffer: pH {fe_event[2]:.2f} -> {al_event[2]:.2f}, "
              f"{buffer_cal:.1f} mmol calcite consumed")

    # Al hydrolysis buffer (from Gibbsite onset to just before the pH jump)
    if al_event:
        # The buffer ends at the step BEFORE the big pH jump
        al_buffer_end_idx = max_dph_idx  # ph_deltas[max_dph_idx] = ph[al_buffer_end_idx+1] - ph[al_buffer_end_idx]
        al_buffer_end_step = al_buffer_end_idx + 1  # 1-indexed
        al_end_ph = ph_series[al_buffer_end_idx]
        al_start_step = al_event[3]  # Gibbsite onset step (1-indexed)
        al_start_idx = al_start_step - 1  # 0-indexed
        buffer_cal = (al_buffer_end_step - al_start_step) * step_size * 1000
        print(f"  Al hydrolysis buffer: pH {al_event[2]:.2f} -> {al_end_ph:.2f}, "
              f"{buffer_cal:.1f} mmol calcite consumed ({al_buffer_end_step - al_start_step} steps)")

    print(f"  {'='*50}")

    # --- VISUALIZATION ---

    # Chart 1: pH titration curve (pH vs calcite added)
    calcite_added = [(i + 1) * step_size * 1000 for i in range(len(data))]  # mmol

    # Build pseudo-selected-output with calcite column for plotting
    so_with_calcite = {
        "columns": columns + ["calcite_mmol"],
        "data": [row + [calcite_added[i]] for i, row in enumerate(data)],
        "row_count": len(data),
    }

    # pH vs calcite
    chart1_path = plot_selected_output_sweep(
        so_with_calcite,
        x_column="calcite_mmol",
        y_columns=["pH"],
        title="AMD Neutralization: pH vs Calcite Added",
        xlabel="Calcite Added (mmol)",
        filepath=os.path.join(workspace, "charts", "ph_titration.png"),
    )
    print(f"  [CHART] {chart1_path}")

    # Chart 2: Multi-panel — pH, gypsum, Fe(OH)3, Gibbsite vs calcite
    phases_to_plot = []
    for col in ["d_Gypsum", "d_Fe(OH)3(a)", "d_Gibbsite"]:
        if col in columns:
            phases_to_plot.append(col)

    if phases_to_plot:
        # Convert d_phase (negative = precipitated) to absolute precipitate amount
        precip_data = []
        for col in phases_to_plot:
            col_idx = columns.index(col)
            precip_col_name = col.replace("d_", "precip_")
            precip_data.append(precip_col_name)

        so_precip = {
            "columns": columns + ["calcite_mmol"],
            "data": [],
            "row_count": len(data),
        }
        for i, row in enumerate(data):
            new_row = list(row) + [calcite_added[i]]
            so_precip["data"].append(new_row)
        # Update columns to include renamed ones
        # Actually, let me just plot with the original d_* columns

        chart2_path = plot_selected_output_sweep(
            so_with_calcite,
            x_column="calcite_mmol",
            y_columns=["pH"] + phases_to_plot,
            title="AMD Neutralization: pH and Mineral Precipitation",
            xlabel="Calcite Added (mmol)",
            filepath=os.path.join(workspace, "charts", "precipitation_curves.png"),
        )
        print(f"  [CHART] {chart2_path}")

    # Chart 3: Ca, S, Fe, Al, Mn totals vs calcite
    totals_to_plot = []
    for col in ["Ca", "S", "Fe", "Al", "Mn"]:
        if col in columns:
            totals_to_plot.append(col)

    if totals_to_plot:
        chart3_path = plot_selected_output_sweep(
            so_with_calcite,
            x_column="calcite_mmol",
            y_columns=totals_to_plot,
            title="AMD Neutralization: Element Totals vs Calcite Added",
            xlabel="Calcite Added (mmol)",
            filepath=os.path.join(workspace, "charts", "element_totals.png"),
        )
        print(f"  [CHART] {chart3_path}")

    # Chart 4: Saturation indices vs calcite
    si_to_plot = []
    for col in ["si_Calcite", "si_Gypsum", "si_Fe(OH)3(a)", "si_Gibbsite"]:
        if col in columns:
            si_to_plot.append(col)

    if si_to_plot:
        chart4_path = plot_selected_output_sweep(
            so_with_calcite,
            x_column="calcite_mmol",
            y_columns=si_to_plot,
            title="AMD Neutralization: Saturation Indices vs Calcite Added",
            xlabel="Calcite Added (mmol)",
            filepath=os.path.join(workspace, "charts", "si_evolution.png"),
        )
        print(f"  [CHART] {chart4_path}")

    # --- SAVE RESULTS ---
    results = {
        "metadata": {
            "task": "2.2",
            "title": "AMD Neutralization with Calcite (Limestone)",
            "initial_pH": 2.0,
            "target_pH": 7.0,
            "amd_composition": {
                "Fe(2)": "500 mg/L",
                "Fe(3)": "50 mg/L",
                "Al": "200 mg/L",
                "Mn": "50 mg/L",
                "S(6)": "2600 mg/L",
            },
            "calcite_total": 0.05,  # mol
            "steps": 100,
            "step_size_mol": 0.0005,
            "co2_system": "open (log PCO2 = -3.4)",
        },
        "key_results": {
            "step_at_ph7": step_at_ph7,
            "calcite_to_ph7_mol": calcite_to_ph7,
            "calcite_to_ph7_g": calcite_to_ph7 * 100.09,
            "final_pH": ph_series[-1],
            "final_calcite_added_mol": len(ph_series) * step_size,
        },
        "selected_output": {
            "columns": columns,
            "row_count": len(data),
        },
        "final_state": {
            "saturation_indices": si_list,
            "species_distribution": species[:30],  # top 30 species
            "element_molalities": elements,
            "ionic_strength": ionic_str,
        },
    }
    results_path = os.path.join(workspace, "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n  [JSON] Results saved to: {results_path}")

    print(f"\n{'='*60}")
    print("Simulation complete!")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
