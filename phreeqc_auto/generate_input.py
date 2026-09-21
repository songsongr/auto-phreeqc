"""
PHREEQC input file generator.

Provides functions to generate PHREEQC keyword data blocks
and complete input files programmatically.
"""

from __future__ import annotations

import copy
import os
from typing import Any


def generate_solution_block(solution_id: int = 1, *, units: str = "mol/kgw", temp: float = 25.0,
                            pH: float = 7.0, pe: float = 4.0, density: float = 1.0, components: dict[str, Any] | None = None) -> str:
    """Generate a SOLUTION keyword block for PHREEQC.

    Args:
        solution_id: Solution number identifier (default 1).
        units: Concentration units string (default "mol/kgw").
        temp: Temperature in Celsius (default 25.0; line omitted when 25.0).
        pH: pH value (default 7.0).
        pe: pe value (default 4.0).
        density: Density in kg/L (default 1.0).
        components: Optional dict mapping component names to
            concentrations or values.

    Returns:
        Formatted SOLUTION keyword block as a string.
    """
    lines = [f"SOLUTION {solution_id}"]
    if units:
        lines.append(f"    units {units}")
    if temp != 25.0:
        lines.append(f"    temp {temp}")
    lines.append(f"    pH {pH}")
    lines.append(f"    pe {pe}")
    lines.append(f"    density {density}")
    if components:
        for name, value in components.items():
            lines.append(f"    {name} {value}")
    return "\n".join(lines)


def generate_equilibrium_phases_block(
    phases: dict[str, tuple[float, float]], block_id: int = 1
) -> str:
    """Generate an EQUILIBRIUM_PHASES keyword block.

    Args:
        phases: Dict mapping phase names to
            (saturation_index, amount) tuples.
        block_id: Phase assemblage number (default 1).

    Returns:
        Formatted EQUILIBRIUM_PHASES keyword block as a string.
    """
    lines = [f"EQUILIBRIUM_PHASES {block_id}"]
    for phase_name, (sat_index, amount) in phases.items():
        lines.append(f"    {phase_name} {sat_index} {amount}")
    return "\n".join(lines)


def generate_reaction_block(reactants: dict[str, float], *,
                            block_id: int = 1, moles: float = 1.0, steps: int = 10) -> str:
    """Generate a REACTION keyword block.

    Args:
        reactants: Dict mapping chemical formulas to stoichiometric
            coefficients.
        block_id: Reaction number identifier (default 1).
        moles: Total moles of reaction (default 1.0).
        steps: Number of reaction steps (default 10).

    Returns:
        Formatted REACTION keyword block as a string.
    """
    lines = [f"REACTION {block_id}"]
    for formula, coeff in reactants.items():
        lines.append(f"    {formula} {coeff}")
    lines.append(f"    {moles} moles in {steps} steps")
    return "\n".join(lines)


def generate_mix_block(mix_def: dict) -> str:
    """Generate a MIX keyword block for solution mixing.

    Args:
        mix_def: Dict with:

            - **id** (*int*) -- MIX block number (default 1).
            - **solutions** (*dict[int, float]*) -- Mapping of solution
              IDs to mixing fractions, e.g. ``{1: 0.5, 2: 0.5}``.

    Returns:
        Formatted MIX keyword block as a string.
    """
    mix_id = mix_def.get("id", 1)
    solutions: dict = mix_def.get("solutions", {})
    lines = [f"MIX {mix_id}"]
    for sol_id, fraction in solutions.items():
        lines.append(f"    {sol_id} {fraction}")
    return "\n".join(lines)


def generate_surface_master_species_block(surface_types: list[dict]) -> str:
    """Generate a SURFACE_MASTER_SPECIES keyword block.

    Args:
        surface_types: List of dicts with keys ``name`` (short identifier)
            and ``formula`` (master species formula).

    Returns:
        Formatted SURFACE_MASTER_SPECIES block as a string.
    """
    lines = ["SURFACE_MASTER_SPECIES"]
    for st in surface_types:
        lines.append(f"    {st['name']}   {st['formula']}")
    return "\n".join(lines)


def generate_surface_species_block(species: list[dict]) -> str:
    """Generate a SURFACE_SPECIES keyword block.

    Args:
        species: List of dicts, each with:
            - **reaction** (*str*) -- surface reaction equation.
            - **log_k** (*float*) -- log10 equilibrium constant.

    Returns:
        Formatted SURFACE_SPECIES block as a string.
    """
    lines = ["SURFACE_SPECIES"]
    for sp in species:
        lines.append(f"    {sp['reaction']}")
        lines.append(f"        log_k {sp['log_k']}")
    return "\n".join(lines)


def generate_surface_block(surfaces: list[dict], block_id: int = 1) -> str:
    """Generate a SURFACE keyword block.

    Supports both site-density and total-sites modes:

    - Full definition (new surface component): ``name``, ``site_density``
      (mol/m²), ``ssa`` (m²/g), ``mass`` (g).
    - Continuation (same component, different site type): ``name``,
      ``site_density`` only — reuses SSA and mass from previous line.

    Args:
        surfaces: List of surface definition dicts.
        block_id: Surface assemblage number (default 1).

    Returns:
        Formatted SURFACE keyword block as a string.
    """
    lines = [f"SURFACE {block_id}"]
    for s in surfaces:
        parts = [f"    {s['name']}", str(s["site_density"])]
        if "ssa" in s:
            parts.append(str(s["ssa"]))
            parts.append(str(s["mass"]))
        lines.append("  ".join(parts))
    return "\n".join(lines)


def generate_phases_block(phases: list[dict]) -> str:
    """Generate a PHASES keyword block for custom phase definitions.

    Args:
        phases: List of dicts with:
            - **name** (*str*) -- phase name.
            - **reaction** (*str*) -- dissolution reaction equation.
            - **log_k** (*float*) -- equilibrium constant.
            - **delta_h** (*float*, optional) -- enthalpy in kJ/mol.

    Returns:
        Formatted PHASES block as a string.
    """
    lines = ["PHASES"]
    for p in phases:
        lines.append(f"    {p['name']}")
        lines.append(f"        {p['reaction']}")
        lines.append(f"        log_k {p['log_k']}")
        if "delta_h" in p:
            lines.append(f"        delta_h {p['delta_h']}")
    return "\n".join(lines)


def generate_exchange_master_species_block(master_species: list[dict]) -> str:
    """Generate an EXCHANGE_MASTER_SPECIES keyword block.

    Args:
        master_species: List of dicts with keys ``name`` (short identifier,
            e.g. "X") and ``formula`` (master species formula, e.g. "X-").

    Returns:
        Formatted EXCHANGE_MASTER_SPECIES block as a string.
    """
    lines = ["EXCHANGE_MASTER_SPECIES"]
    for ms in master_species:
        lines.append(f"    {ms['name']}   {ms['formula']}")
    return "\n".join(lines)


def generate_exchange_species_block(species: list[dict]) -> str:
    """Generate an EXCHANGE_SPECIES keyword block.

    Args:
        species: List of dicts with:
            - **reaction** (*str*) -- exchange half-reaction equation.
            - **log_k** (*float*) -- log10 equilibrium constant.
            - **gamma** (*str*, optional) -- activity correction
              parameters (e.g. "4.0 0.075").
            - **delta_h** (*float*, optional) -- enthalpy in kJ/mol.

    Returns:
        Formatted EXCHANGE_SPECIES block as a string.
    """
    lines = ["EXCHANGE_SPECIES"]
    for sp in species:
        lines.append(f"    {sp['reaction']}")
        lines.append(f"        log_k {sp['log_k']}")
        if "gamma" in sp:
            lines.append(f"        -gamma {sp['gamma']}")
        if "delta_h" in sp:
            lines.append(f"        delta_h {sp['delta_h']}")
    return "\n".join(lines)


def generate_exchange_block(exchange_def: dict, block_id: int = 1) -> str:
    """Generate an EXCHANGE keyword block.

    Supports both explicit composition and equilibrate-with-solution modes:

    - Explicit: ``{"sites": "X", "moles": 0.1, "composition": "CaX2"}``
    - Equilibrate: ``{"sites": "X", "moles": 0.1, "equilibrate": 1}``

    Args:
        exchange_def: Dict with keys:
            - **sites** (*str*) -- exchange master species name (e.g. "X").
            - **moles** (*float*) -- total exchange sites in moles.
            - **composition** (*str*, optional) -- exchange composition
              formula (e.g. "CaX2", "NaX").
            - **equilibrate** (*int*, optional) -- solution number to
              equilibrate with.
        block_id: Exchange assemblage number (default 1).

    Returns:
        Formatted EXCHANGE keyword block as a string.
    """
    lines = [f"EXCHANGE {block_id}"]
    lines.append(f"    {exchange_def['sites']} {exchange_def['moles']}")
    if "composition" in exchange_def:
        lines.append(f"    -composition {exchange_def['composition']}")
    elif "equilibrate" in exchange_def:
        lines.append(f"    -equilibrate with solution {exchange_def['equilibrate']}")
    return "\n".join(lines)


def generate_kinetics_block(kinetics_def: dict, block_id: int = 1) -> str:
    """Generate a KINETICS keyword block.

    Args:
        kinetics_def: Dict with:
            - **reactants** (*list[dict]*) -- list of kinetic reactant defs.
              Each reactant dict has:
              - **name** (*str*) -- reactant name (matches RATES name).
              - **formula** (*str*, optional) -- chemical formula.
              - **stoichiometric_coefficient** (*float*, default 1).
              - **m** (*float*) -- current moles of reactant.
              - **m0** (*float*, optional) -- initial moles (defaults to m).
              - **parms** (*list[float]*, optional) -- parameters for RATES.
              - **tol** (*float*, optional) -- integration tolerance.
              - **steps** (*list[float]*) -- cumulative time steps in seconds.
              - **steps_n** (*int*, optional) -- sub-step count.
              - **step_divide** (*int*, optional) -- sub-division count.
              - **runge_kutta** (*int*, optional) -- RK order (1-6).
              - **cvode** (*bool*, optional) -- use CVODE solver.
        block_id: Kinetics number (default 1).

    Returns:
        Formatted KINETICS keyword block as a string.
    """
    lines = [f"KINETICS {block_id}"]
    # Collect global -steps from the first reactant that defines it.
    # In PHREEQC, -steps is a KINETICS-block-level keyword, not per-reactant.
    global_steps: list[float] | None = None
    global_steps_n: int | None = None

    for reactant in kinetics_def.get("reactants", []):
        lines.append(f"    {reactant['name']}")
        if "formula" in reactant:
            coeff = reactant.get("stoichiometric_coefficient", 1)
            lines.append(f"        -formula {reactant['formula']} {coeff}")
        lines.append(f"        -m {reactant.get('m', 0)}")
        m0 = reactant.get("m0", reactant.get("m", 0))
        lines.append(f"        -m0 {m0}")
        if "parms" in reactant:
            parms_str = ' '.join(str(p) for p in reactant['parms'])
            lines.append(f"        -parms {parms_str}")
        if "tol" in reactant:
            lines.append(f"        -tol {reactant['tol']}")
        # Collect global steps from first reactant
        if "steps" in reactant and global_steps is None:
            global_steps = reactant["steps"]
            global_steps_n = reactant.get("steps_n")
        if "step_divide" in reactant:
            lines.append(f"        -step_divide {reactant['step_divide']}")
        if "runge_kutta" in reactant:
            lines.append(f"        -runge_kutta {reactant['runge_kutta']}")
        if "cvode" in reactant:
            lines.append(f"        -cvode {'true' if reactant['cvode'] else 'false'}")

    # Write -steps once at the KINETICS block level
    if global_steps is not None:
        steps_str = ' '.join(str(s) for s in global_steps)
        if global_steps_n is not None:
            steps_str += f" in {global_steps_n} steps"
        lines.append(f"    -steps {steps_str}")
    return "\n".join(lines)


def generate_rates_block(rates_defs: list[dict], block_id: int = 1) -> str:
    """Generate a RATES keyword block with embedded BASIC code.

    Supports the full PHREEQC BASIC language for rate equations, including:
    - ``SR("phase")`` -- saturation ratio
    - ``TOT("element")`` -- total element concentration
    - ``ACT("species")`` -- activity
    - ``M`` -- current moles of kinetic reactant
    - ``M0`` -- initial moles
    - ``TIME`` -- time step in seconds
    - ``parm(N)`` -- user parameter from KINETICS -parms
    - ``SAVE moles`` -- moles added/removed this time step

    Args:
        rates_defs: List of dicts, each with:
            - **name** (*str*) -- rate name (matches KINETICS reactant).
            - **code** (*list[str]*) -- list of BASIC code lines
              (without line numbers, they will be auto-numbered).
        block_id: Rates number (default 1).

    Returns:
        Formatted RATES keyword block as a string.
    """
    lines = [f"RATES {block_id}"]
    for rate_def in rates_defs:
        lines.append(f"    {rate_def['name']}")
        lines.append("    -start")
        line_num = 0
        for code_line in rate_def.get('code', []):
            stripped = code_line.strip()
            if not stripped:
                continue  # skip blank lines (PHREEQC BASIC requires numbered lines)
            first_word = stripped.split()[0]
            already_numbered = (
                first_word.rstrip('.').isdigit() and
                len(first_word) <= 6
            )
            if already_numbered:
                lines.append(f"    {stripped}")
                continue
            line_num += 1
            lines.append(f"    {line_num * 10} {stripped}")
        lines.append("    -end")
    return "\n".join(lines)


def generate_transport_block(
    *,
    cells: int = 20,
    length: float = 1.0,
    shifts: int = 100,
    time_step: float = 0.05,
    time_units: str = "day",
    flow_direction: str = "forward",
    dispersivity: float = 0.0,
    diffusion_coefficient: float | None = None,
    correct_disp: bool = False,
    punch_cells: list[int] | None = None,
    punch_frequency: int = 1,
    print_cells: list[int] | None = None,
    print_frequency: int = 1,
    pore_volume: bool = False,
    warning: bool = True,
) -> str:
    """Generate a TRANSPORT keyword block for 1D advection-dispersion.

    Args:
        cells: Number of cells in the column (default 20).
        length: Column length in meters (default 1.0).
        shifts: Number of time shifts (default 100).
        time_step: Time step size (default 0.05).
        time_units: Units for time_step (default "day").
        flow_direction: "forward" (default), "backward", or
            "diffusion_only".
        dispersivity: Dispersivity in meters (default 0.0).
        diffusion_coefficient: Pore-water diffusion coefficient
            (m2/s, optional).
        correct_disp: Whether to correct dispersion for tortuosity
            (default False).
        punch_cells: List of cell numbers to include in selected
            output (default None = all cells).
        punch_frequency: Output frequency for selected output in
            shifts (default 1 = every shift).
        print_cells: List of cell numbers to print to main output
            (default None = all cells).
        print_frequency: Print frequency for main output in shifts
            (default 1 = every shift).
        pore_volume: Whether to include the number of pore volumes
            in the output (default False).
        warning: Whether to print stability warnings
            (default True).

    Returns:
        Formatted TRANSPORT keyword block as a string.
    """
    lines = ["TRANSPORT"]
    lines.append(f"    -cells {cells}")
    lines.append(f"    -length {length}")
    lines.append(f"    -shifts {shifts}")
    lines.append(f"    -time_step {time_step} {time_units}")
    lines.append(f"    -flow_direction {flow_direction}")
    if dispersivity > 0:
        lines.append(f"    -dispersivity {dispersivity}")
    if diffusion_coefficient is not None:
        lines.append(f"    -diffusion_coefficient {diffusion_coefficient}")
    if correct_disp:
        lines.append("    -correct_disp true")
    if punch_cells:
        cells_str = " ".join(str(c) for c in punch_cells)
        lines.append(f"    -punch_cells {cells_str}")
    lines.append(f"    -punch_frequency {punch_frequency}")
    if print_cells:
        cells_str = " ".join(str(c) for c in print_cells)
        lines.append(f"    -print_cells {cells_str}")
    lines.append(f"    -print_frequency {print_frequency}")
    if pore_volume:
        lines.append("    -pore_volume")
    if not warning:
        lines.append("    -warning false")
    return "\n".join(lines)


def generate_gas_phase_block(
    *,
    block_id: int = 1,
    fixed_pressure: bool = True,
    pressure: float = 1.0,
    volume: float | None = None,
    temperature: float | None = None,
    components: dict[str, float] | None = None,
) -> str:
    """Generate a GAS_PHASE keyword block for gas phase equilibria.

    Supports both fixed-pressure and fixed-volume gas phases.
    For high-pressure CO2 injection, use ``fixed_pressure=True``
    with the target pressure in atm.

    Args:
        block_id: Gas phase number identifier (default 1).
        fixed_pressure: Whether to maintain constant pressure
            by exchanging gas with solution (default True).
        pressure: Gas pressure in atm (default 1.0).
        volume: Gas volume in liters (optional; needed for
            non-fixed pressure mode only).
        temperature: Temperature in Celsius (optional; defaults
            to SOLUTION temperature).
        components: Dict mapping gas component names to mole
            amounts (e.g. ``{"CO2(g)": 0.0}`` for infinite
            supply under fixed pressure).

    Returns:
        Formatted GAS_PHASE keyword block as a string.
    """
    lines = [f"GAS_PHASE {block_id}"]
    if fixed_pressure:
        lines.append("    -fixed_pressure")
    lines.append(f"    -pressure {pressure}")
    if volume is not None:
        lines.append(f"    -volume {volume}")
    if temperature is not None:
        lines.append(f"    -temperature {temperature}")
    if components:
        for name, amount in components.items():
            lines.append(f"    {name} {amount}")
    return "\n".join(lines)


def generate_reaction_pressure_block(
    *,
    block_id: int = 1,
    pressure: float = 1.0,
    steps: int = 1,
) -> str:
    """Generate a REACTION_PRESSURE keyword block.

    Used to set or vary pressure for batch-reaction calculations,
    e.g., high-pressure CO2 injection at 200 atm.

    Args:
        block_id: Reaction pressure number (default 1).
        pressure: Pressure in atm (default 1.0).
        steps: Number of pressure steps (default 1).

    Returns:
        Formatted REACTION_PRESSURE keyword block as a string.
    """
    lines = [f"REACTION_PRESSURE {block_id}"]
    lines.append(f"    {pressure}")
    if steps > 1:
        lines.append(f"    {steps} steps")
    return "\n".join(lines)


def generate_selected_output_block(*, file: str = "selected_output.txt",
                                   reset: bool = True, step: bool = False,
                                   equilibrium_phases: list[str] | None = None,
                                   si: list[str] | None = None, totals: list[str] | None = None,
                                   molalities: list[str] | None = None, pH: bool = True, pe: bool = True,
                                   temperature: bool = False) -> str:
    """Generate a SELECTED_OUTPUT keyword block.

    Args:
        file: Output file path (default "selected_output.txt").
        reset: Whether to reset selected output (default True).
        step: Whether to print output for each reaction/transport step
            (default False).
        equilibrium_phases: Optional list of phase names for
            equilibrium-phase assemblage data output.
        si: Optional list of phase names for saturation index output.
        totals: Optional list of element names for total
            concentration output.
        molalities: Optional list of species names for molality output.
        pH: Include pH in output (default True).
        pe: Include pe in output (default True).
        temperature: Include temperature in output (default False).

    Returns:
        Formatted SELECTED_OUTPUT keyword block as a string.
    """
    lines = ["SELECTED_OUTPUT"]
    lines.append(f"    -file {file}")
    lines.append(f"    -reset {'true' if reset else 'false'}")
    if step:
        lines.append("    -step true")
    if pH:
        lines.append("    -pH")
    if pe:
        lines.append("    -pe")
    if temperature:
        lines.append("    -temperature")
    if equilibrium_phases:
        lines.append(f"    -equilibrium_phases {' '.join(equilibrium_phases)}")
    if si:
        for phase in si:
            lines.append(f"    -si {phase}")
    if totals:
        for element in totals:
            lines.append(f"    -totals {element}")
    if molalities:
        for species in molalities:
            lines.append(f"    -molalities {species}")
    return "\n".join(lines)


def generate_single_simulation(params: dict,
                               output_file: str = "selected_output.txt") -> str:
    """Generate a single simulation's .pqi file content.

    Inspects *params* to decide which keyword blocks to include and
    calls the individual block generators accordingly.

    For transport simulations, the function auto-generates cell solutions
    (SOLUTION 1 through N) from *initial_cell_solution* when a
    ``"transport"`` key is present.  The inlet solution (SOLUTION 0) must
    be provided in the ``"solutions"`` list with ``"id": 0``.

    Args:
        params: Dict of simulation parameters.  Expected sub-keys:

            - **solution** (*dict*) -- passed to
              :func:`generate_solution_block`.
            - **solutions** (*list[dict]*) -- for multi-solution setups
              (MIX or TRANSPORT).  For transport, include ``{"id": 0,
              ...}`` for the inlet boundary condition.
            - **initial_cell_solution** (*dict*, optional) -- template for
              auto-generating transport cell solutions 1..N.  Only used
              when ``"transport"`` is present.
            - **transport** (*dict*, optional) -- passed to
              :func:`generate_transport_block`.
            - **equilibrium_phases** (*dict*, optional) -- passed to
              :func:`generate_equilibrium_phases_block`.
            - **reaction** (*dict*, optional) -- passed to
              :func:`generate_reaction_block`.
            - **kinetics** (*dict*, optional) -- passed to
              :func:`generate_kinetics_block`.
            - **rates** (*list[dict]*, optional) -- passed to
              :func:`generate_rates_block`.
            - **selected_output** (*dict*, optional) -- passed to
              :func:`generate_selected_output_block`.
            - **eq_block_id** (*int*, optional) -- block id for
              EQUILIBRIUM_PHASES (default 1).

        output_file: Path for the selected output file
            (default "selected_output.txt").

    Returns:
        Complete .pqi content as a string, ending with ``END``.
    """
    blocks = []

    # --- Global definition blocks (placed before simulations) ---
    if "exchange_master_species" in params:
        blocks.append(generate_exchange_master_species_block(
            params["exchange_master_species"],
        ))
    if "exchange_species" in params:
        blocks.append(generate_exchange_species_block(
            params["exchange_species"],
        ))
    if "surface_master_species" in params:
        blocks.append(generate_surface_master_species_block(
            params["surface_master_species"],
        ))
    if "surface_species" in params:
        blocks.append(generate_surface_species_block(
            params["surface_species"],
        ))
    if "phases" in params:
        blocks.append(generate_phases_block(params["phases"]))

    # --- RATES block (global definition) ---
    if "rates" in params:
        blocks.append(generate_rates_block(
            params["rates"],
            block_id=params.get("rates_block_id", 1),
        ))

    # --- Exchange block ---
    if "exchange" in params:
        blocks.append(generate_exchange_block(
            params["exchange"],
            block_id=params.get("exchange_block_id", 1),
        ))

    # --- Surface block ---
    if "surface" in params:
        blocks.append(generate_surface_block(
            params["surface"],
            block_id=params.get("surface_block_id", 1),
        ))

    is_transport = "transport" in params

    # --- Solutions ---
    # For transport: SOLUTION 0 (inlet) + auto-generated cell solutions
    if is_transport:
        transport_cfg = params["transport"]
        n_cells = transport_cfg.get("cells", 20)
        cell_id_start = transport_cfg.get("cell_id_start", 1)

        # Write explicitly-provided solutions first (including inlet)
        written_ids: set[int] = set()
        if "solutions" in params:
            for sol in params["solutions"]:
                sid = sol.get("id", 1)
                blocks.append(generate_solution_block(
                    solution_id=sid,
                    units=sol.get("units", "mol/kgw"),
                    temp=sol.get("temp", 25.0),
                    pH=sol.get("pH", 7.0),
                    pe=sol.get("pe", 4.0),
                    density=sol.get("density", 1.0),
                    components=sol.get("components"),
                ))
                written_ids.add(sid)

        # Auto-generate cell solutions for any missing IDs
        initial = params.get("initial_cell_solution", {})
        for cell_id in range(cell_id_start, cell_id_start + n_cells):
            if cell_id not in written_ids:
                blocks.append(generate_solution_block(
                    solution_id=cell_id,
                    units=initial.get("units", "mol/kgw"),
                    temp=initial.get("temp", 25.0),
                    pH=initial.get("pH", 7.0),
                    pe=initial.get("pe", 4.0),
                    density=initial.get("density", 1.0),
                    components=initial.get("components"),
                ))

    elif "solutions" in params:
        for sol in params["solutions"]:
            blocks.append(generate_solution_block(
                solution_id=sol.get("id", 1),
                units=sol.get("units", "mol/kgw"),
                temp=sol.get("temp", 25.0),
                pH=sol.get("pH", 7.0),
                pe=sol.get("pe", 4.0),
                density=sol.get("density", 1.0),
                components=sol.get("components"),
            ))
    elif "solution" in params:
        sol = params["solution"]
        blocks.append(generate_solution_block(
            solution_id=sol.get("id", 1),
            units=sol.get("units", "mol/kgw"),
            temp=sol.get("temp", 25.0),
            pH=sol.get("pH", 7.0),
            pe=sol.get("pe", 4.0),
            density=sol.get("density", 1.0),
            components=sol.get("components"),
        ))

    # --- Mix block ---
    if "mix" in params:
        blocks.append(generate_mix_block(params["mix"]))

    # --- Transport block ---
    if is_transport:
        blocks.append(generate_transport_block(
            cells=transport_cfg.get("cells", 20),
            length=transport_cfg.get("length", 1.0),
            shifts=transport_cfg.get("shifts", 100),
            time_step=transport_cfg.get("time_step", 0.05),
            time_units=transport_cfg.get("time_units", "day"),
            flow_direction=transport_cfg.get("flow_direction", "forward"),
            dispersivity=transport_cfg.get("dispersivity", 0.0),
            diffusion_coefficient=transport_cfg.get("diffusion_coefficient"),
            correct_disp=transport_cfg.get("correct_disp", False),
            punch_cells=transport_cfg.get("punch_cells"),
            punch_frequency=transport_cfg.get("punch_frequency", 1),
            print_cells=transport_cfg.get("print_cells"),
            print_frequency=transport_cfg.get("print_frequency", 1),
            pore_volume=transport_cfg.get("pore_volume", False),
            warning=transport_cfg.get("warning", True),
        ))

    # --- Gas phase block ---
    if "gas_phase" in params:
        gp = params["gas_phase"]
        blocks.append(generate_gas_phase_block(
            block_id=gp.get("block_id", 1),
            fixed_pressure=gp.get("fixed_pressure", True),
            pressure=gp.get("pressure", 1.0),
            volume=gp.get("volume"),
            temperature=gp.get("temperature"),
            components=gp.get("components"),
        ))

    # --- Reaction pressure block ---
    if "reaction_pressure" in params:
        rp = params["reaction_pressure"]
        blocks.append(generate_reaction_pressure_block(
            block_id=rp.get("block_id", 1),
            pressure=rp.get("pressure", 1.0),
            steps=rp.get("steps", 1),
        ))

    # --- Equilibrium phases (batch reactions) ---
    if "equilibrium_phases" in params:
        blocks.append(generate_equilibrium_phases_block(
            params["equilibrium_phases"],
            block_id=params.get("eq_block_id", 1),
        ))

    # --- Reaction block ---
    if "reaction" in params:
        rxn = params["reaction"]
        blocks.append(generate_reaction_block(
            rxn.get("reactants", {}),
            block_id=rxn.get("block_id", 1),
            moles=rxn.get("moles", 1.0),
            steps=rxn.get("steps", 10),
        ))

    # --- Kinetics block ---
    if "kinetics" in params:
        blocks.append(generate_kinetics_block(
            params["kinetics"],
            block_id=params.get("kinetics_block_id", 1),
        ))

    # --- Selected output ---
    so = params.get("selected_output", {})
    # For transport, default step to True
    so_step = so.get("step", is_transport)
    blocks.append(generate_selected_output_block(
        file=output_file,
        reset=so.get("reset", True),
        step=so_step,
        equilibrium_phases=so.get("equilibrium_phases"),
        si=so.get("si"),
        totals=so.get("totals"),
        molalities=so.get("molalities"),
        pH=so.get("pH", True),
        pe=so.get("pe", True),
        temperature=so.get("temperature", False),
    ))

    return "\n\n".join(blocks) + "\n\nEND"


def _set_nested_param(params: dict, path: str, value: Any) -> dict:
    """Set a value in a nested dict using a dot-separated path.

    Intermediate dicts are created as needed.

    Args:
        params: The (possibly nested) dict to modify.
        path: Dot-separated key path (e.g. ``"solution.pH"``).
        value: The value to set at the target key.

    Returns:
        The modified *params* dict.
    """
    keys = path.split(".")
    d = params
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value
    return params


def generate_parameter_sweep(base_params: dict, sweep_param: str,
                             sweep_values: list | tuple, output_dir: str = ".") -> str:
    """Generate a multi-step .pqi file for parameter scanning.

    Each sweep value produces a separate simulation block (separated by
    ``END``).  The sweep parameter is overridden per step by applying it
    to a deep copy of *base_params* via :func:`_set_nested_param`, then
    :func:`generate_single_simulation` is called for each step.

    Args:
        base_params: Base parameter dict (same structure as
            :func:`generate_single_simulation`).
        sweep_param: Dot-separated path to the parameter being swept
            (e.g. ``"solution.pH"``).
        sweep_values: Iterable of parameter values to sweep over.
        output_dir: Directory for per-step selected-output files
            (default ``"."``).

    Returns:
        Complete multi-simulation .pqi content as a string, with each
        simulation terminated by ``END``.
    """
    all_simulations = []
    for i, value in enumerate(sweep_values, start=1):
        params = copy.deepcopy(base_params)
        _set_nested_param(params, sweep_param, value)
        output_filename = os.path.join(output_dir, f"step_{i}.txt")
        sim_content = generate_single_simulation(
            params, output_file=output_filename,
        )
        all_simulations.append(sim_content)
    return "\n\n".join(all_simulations)


def write_input_file(content: str, filepath: str) -> str:
    """Write *content* to *filepath*, creating parent directories.

    Args:
        content: String content to write.
        filepath: Destination file path (may be relative).

    Returns:
        Absolute path to the written file.
    """
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath
