"""
PHREEQC visualization tools.

Provides functions to create publication-quality plots from PHREEQC
simulation results, including saturation index bar charts, parameter
sweep line plots, and multi-panel comparison figures.
"""

from __future__ import annotations

import os
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


__all__ = [
    "plot_saturation_indices",
    "plot_selected_output_sweep",
    "plot_multi_panel",
    "plot_breakthrough_curve",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def plot_saturation_indices(
    data: dict[str, Any] | list[dict[str, Any]],
    *,
    sweep_param: str | None = None,
    title: str = "Saturation Indices",
    filepath: str | None = None,
) -> str:
    """Plot saturation indices from parsed PHREEQC results.

    Two modes:

    - **Bar chart** (default, *sweep_param* is ``None``): Horizontal bar
      chart with phase names on the Y-axis and SI values on the X-axis.
      Bars are coloured green for saturated (SI >= 0) and red for
      undersaturated (SI < 0).  Numerical SI values are labelled next to
      each bar.

    - **Sweep line plot** (*sweep_param* is set): Multi-line plot with the
      sweep parameter on the X-axis and SI values on the Y-axis.  Each line
      represents one phase.

    Args:
        data: Parsed results dict or a list of saturation index dicts.
            If a dict, ``data["saturation_indices"]`` is used as the SI
            list.  Each SI dict must have ``"phase"`` (str) and ``"si"``
            (float) keys.
            In sweep mode, ``data[sweep_param]`` provides the X-axis
            values and ``data["saturation_indices"]`` must be a list of
            lists (one inner list per sweep step).
        sweep_param: Key in *data* for the sweep parameter values.
            When ``None`` (default), a bar chart is produced.
        title: Plot title (default ``"Saturation Indices"``).
        filepath: Path to save the figure.  Auto-generated if ``None``.

    Returns:
        Absolute path to the saved figure file, or ``""`` when there
        is no saturation index data to plot.
    """
    # --- resolve raw SI payload ---
    if isinstance(data, list):
        raw_si: Any = data
    elif isinstance(data, dict):
        raw_si = data.get("saturation_indices", [])
    else:
        return ""

    if not raw_si:
        return ""

    if sweep_param is not None:
        return _plot_si_sweep(data, raw_si, sweep_param, title, filepath)
    return _plot_si_bars(raw_si, title, filepath)


def plot_selected_output_sweep(
    selected_output: dict[str, Any],
    x_column: str,
    y_columns: list[str],
    title: str = "Parameter Sweep",
    xlabel: str | None = None,
    filepath: str | None = None,
) -> str:
    """Plot selected-output columns as a multi-line parameter sweep.

    Creates a line plot using *x_column* for the X axis and one line per
    column in *y_columns*.

    Args:
        selected_output: Dict from
            :func:`~scripts.parse_output.parse_selected_output`. Must
            contain ``"columns"`` (list of str) and ``"data"`` (list of
            list of float) keys.
        x_column: Name of the column to use for the X axis.
        y_columns: Names of the columns to plot as lines.
        title: Plot title (default ``"Parameter Sweep"``).
        xlabel: Label for the X axis.  Defaults to *x_column* when
            ``None``.
        filepath: Path to save the figure.  Auto-generated if ``None``.

    Returns:
        Absolute path to the saved figure file, or ``""`` if *x_column*
        is not found in the column list.
    """
    columns = selected_output.get("columns", [])
    raw_data = selected_output.get("data", [])

    if x_column not in columns:
        return ""

    x_idx = columns.index(x_column)

    # Resolve column indices for y_columns
    y_indices: list[int] = []
    valid_labels: list[str] = []
    for col in y_columns:
        if col in columns:
            y_indices.append(columns.index(col))
            valid_labels.append(col)

    if not y_indices:
        return ""

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10(range(len(y_indices)))
    x_vals = [row[x_idx] for row in raw_data]

    for i, (y_idx, label) in enumerate(zip(y_indices, valid_labels)):
        y_vals = [row[y_idx] for row in raw_data]
        ax.plot(
            x_vals,
            y_vals,
            marker="o",
            color=colors[i],
            label=label,
            linewidth=1.5,
        )

    ax.set_xlabel(xlabel if xlabel else x_column)
    ax.set_ylabel("Value")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    if filepath is None:
        filepath = "selected_output_sweep.png"
    return _save_figure(fig, filepath)


def plot_multi_panel(
    data_sets: list[dict[str, Any]],
    titles: list[str],
    *,
    filepath: str = "multi_panel.png",
) -> str:
    """Create a multi-panel figure comparing saturation indices.

    Each panel shows a horizontal bar chart of saturation indices for
    one data set.  Panels are arranged in up to 2 columns with dynamic
    rows.

    Args:
        data_sets: List of parsed result dicts or SI lists, one per
            panel.
        titles: List of titles, one per panel.
        filepath: Path to save the figure
            (default ``"multi_panel.png"``).

    Returns:
        Absolute path to the saved figure file.
    """
    n = len(data_sets)
    ncols = min(2, n)
    nrows = max(1, (n + 1) // 2)

    fig, axes = plt.subplots(
        nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False
    )

    for idx in range(n):
        row, col = divmod(idx, ncols)
        ax = axes[row][col]

        si_list = _resolve_si_bar_data(data_sets[idx])
        if not si_list:
            ax.text(
                0.5, 0.5, "No data",
                ha="center", va="center", transform=ax.transAxes,
            )
            ax.set_title(titles[idx] if idx < len(titles) else "")
            continue

        phases = [entry["phase"] for entry in si_list]
        si_values = [entry["si"] for entry in si_list]
        y_pos = range(len(phases))
        colors = ["#2ca02c" if v >= 0 else "#d62728" for v in si_values]

        ax.barh(y_pos, si_values, color=colors, edgecolor="white", linewidth=0.5)

        # Value labels
        si_range = _safe_si_range(si_values)
        for i, val in enumerate(si_values):
            if val >= 0:
                label_x = val + 0.02 * si_range
                ha = "left"
            else:
                label_x = val - 0.02 * si_range
                ha = "right"
            ax.text(
                label_x, i, f"{val:.2f}",
                va="center", ha=ha, fontsize=8,
            )

        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(phases, fontsize=9)
        ax.set_title(titles[idx] if idx < len(titles) else "", fontsize=10)
        ax.axvline(0, color="gray", linestyle="--", linewidth=0.8)
        ax.grid(axis="x", alpha=0.3)

    # Hide unused subplots
    for idx in range(n, nrows * ncols):
        row, col = divmod(idx, ncols)
        axes[row][col].set_visible(False)

    plt.tight_layout()
    return _save_figure(fig, filepath)


def plot_breakthrough_curve(
    selected_output: dict[str, Any],
    *,
    time_column: str = "step",
    conc_column: str | None = None,
    conc_columns: list[str] | None = None,
    title: str = "Breakthrough Curve",
    xlabel: str = "Time (days)",
    ylabel: str = "Concentration",
    filepath: str | None = None,
) -> str:
    """Plot a breakthrough curve from transport SELECTED_OUTPUT data.

    Creates a line plot with time (or step) on the X-axis and one or
    more concentration columns on the Y-axis, with a horizontal dashed
    line at C/C0 = 0.5 for reference.

    Args:
        selected_output: Dict from
            :func:`~scripts.parse_output.parse_selected_output`. Must
            contain ``"columns"`` and ``"data"`` keys.
        time_column: Name of the column to use for the X axis
            (default ``"step"``).  Common alternatives: ``"time"``.
        conc_column: Single column name for the Y axis.  Mutually
            exclusive with *conc_columns*.
        conc_columns: Multiple column names for the Y axis.  Mutually
            exclusive with *conc_column*.
        title: Plot title (default ``"Breakthrough Curve"``).
        xlabel: Label for the X axis (default ``"Time (days)"``).
        ylabel: Label for the Y axis (default ``"Concentration"``).
        filepath: Path to save the figure.  Auto-generated if ``None``.

    Returns:
        Absolute path to the saved figure file, or ``""`` on failure.
    """
    columns = selected_output.get("columns", [])
    raw_data = selected_output.get("data", [])

    if time_column not in columns:
        return ""

    x_idx = columns.index(time_column)

    # Determine Y columns
    y_columns: list[str] = []
    if conc_column:
        y_columns = [c for c in [conc_column] if c in columns]
    elif conc_columns:
        y_columns = [c for c in conc_columns if c in columns]

    if not y_columns:
        # Try common concentration-related columns
        candidates = [c for c in columns if c.lower().startswith("tot") or c.lower() == "as"]
        if candidates:
            y_columns = candidates[:3]
        else:
            return ""

    y_indices = [columns.index(c) for c in y_columns]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10(range(len(y_indices)))

    x_vals = [row[x_idx] for row in raw_data]

    for i, (y_idx, label) in enumerate(zip(y_indices, y_columns)):
        y_vals = [row[y_idx] for row in raw_data]
        ax.plot(
            x_vals,
            y_vals,
            marker=".",
            color=colors[i],
            label=label,
            linewidth=1.5,
            markersize=3,
        )

    # Reference lines
    max_conc = 0.0
    for row in raw_data:
        for y_idx in y_indices:
            try:
                max_conc = max(max_conc, float(row[y_idx]) if row[y_idx] is not None else 0.0)
            except (TypeError, ValueError):
                pass

    if max_conc > 0:
        ax.axhline(
            y=max_conc * 0.5,
            color="gray",
            linestyle="--",
            linewidth=0.8,
            alpha=0.6,
            label=f"C/C0 = 0.5 ({max_conc * 0.5:.3e})",
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    if filepath is None:
        filepath = "breakthrough_curve.png"
    return _save_figure(fig, filepath)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _plot_si_bars(
    raw_si: Any,
    title: str,
    filepath: str | None,
) -> str:
    """Create a horizontal bar chart of saturation indices."""
    # Normalise: if raw_si is a list-of-lists (sweep shape), take first step
    if raw_si and isinstance(raw_si[0], list):
        raw_si = raw_si[0]

    if not raw_si:
        return ""

    phases = [entry["phase"] for entry in raw_si]
    si_values = [entry["si"] for entry in raw_si]
    n = len(phases)

    fig, ax = plt.subplots(figsize=(max(8, n * 0.4), max(4, n * 0.4)))

    y_pos = range(n)
    colors = ["#2ca02c" if v >= 0 else "#d62728" for v in si_values]

    ax.barh(y_pos, si_values, color=colors, edgecolor="white", linewidth=0.5)

    # Value labels next to each bar
    si_range = _safe_si_range(si_values)
    for i, val in enumerate(si_values):
        if val >= 0:
            label_x = val + 0.02 * si_range
            ha = "left"
        else:
            label_x = val - 0.02 * si_range
            ha = "right"
        ax.text(
            label_x, i, f"{val:.2f}",
            va="center", ha=ha, fontsize=9,
        )

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(phases)
    ax.set_xlabel("Saturation Index (SI)")
    ax.set_title(title)
    ax.axvline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    if filepath is None:
        filepath = "saturation_indices.png"
    return _save_figure(fig, filepath)


def _plot_si_sweep(
    data: dict[str, Any],
    raw_si: Any,
    sweep_param: str,
    title: str,
    filepath: str | None,
) -> str:
    """Create a multi-line plot of SI values across a parameter sweep."""
    sweep_values: list[float] = data.get(sweep_param, [])
    if not sweep_values:
        return ""

    # raw_si should be a list of lists (one inner list per sweep step)
    all_si: list[list[dict[str, Any]]] = raw_si
    if not all_si or not isinstance(all_si[0], list):
        # Not a nested list -- nothing to sweep over
        return ""

    if not all_si[0]:
        return ""

    # Phase names from the first step
    phase_names = [entry["phase"] for entry in all_si[0]]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10(range(len(phase_names)))
    x_vals = sweep_values

    for idx, phase_name in enumerate(phase_names):
        y_vals: list[float] = []
        for step_si in all_si:
            matches = [e["si"] for e in step_si if e["phase"] == phase_name]
            y_vals.append(matches[0] if matches else float("nan"))
        ax.plot(
            x_vals,
            y_vals,
            marker="o",
            color=colors[idx],
            label=phase_name,
            linewidth=1.5,
        )

    ax.set_xlabel(sweep_param.replace("_", " ").title())
    ax.set_ylabel("Saturation Index (SI)")
    ax.set_title(title)
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(alpha=0.3)
    plt.tight_layout()

    if filepath is None:
        filepath = "saturation_indices_sweep.png"
    return _save_figure(fig, filepath)


def _resolve_si_bar_data(
    data: dict[str, Any] | list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Extract a flat list of ``{phase, si}`` dicts for bar charts."""
    if isinstance(data, list):
        raw = data
    elif isinstance(data, dict):
        raw = data.get("saturation_indices", [])
    else:
        return []

    if not raw:
        return []

    # If it is a list-of-lists, take the first step
    if isinstance(raw[0], list):
        return raw[0] if raw[0] else []
    return raw


def _safe_si_range(si_values: list[float]) -> float:
    """Compute a safe range for label offset, avoiding zero division."""
    lo, hi = min(si_values), max(si_values)
    rng = hi - lo
    if rng == 0:
        return abs(hi) + 1.0 if hi != 0 else 1.0
    return rng


def _save_figure(fig: Any, filepath: str) -> str:
    """Save a matplotlib figure, creating directories if needed.

    Args:
        fig: The matplotlib figure object.
        filepath: Destination path (may be relative).

    Returns:
        Absolute path to the saved file.
    """
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return filepath
