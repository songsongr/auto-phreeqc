"""
PHREEQC output parser.

Provides functions to parse PHREEQC SELECTED_OUTPUT files and standard
output text, extracting tabular data, saturation indices, species
distributions, and element molalities.
"""

from __future__ import annotations

import json
from typing import Any


__all__ = [
    "parse_selected_output",
    "extract_saturation_indices",
    "extract_species_distribution",
    "extract_element_molalities",
    "extract_ionic_strength",
    "extract_exchange_composition",
    "to_json",
]


def parse_selected_output(filepath: str) -> dict:
    """Parse a PHREEQC SELECTED_OUTPUT text file.

    The file is expected to be tabular with a header row (column names)
    followed by data rows, separated by whitespace.  Comment lines
    starting with ``#`` or ``Selected`` are ignored.

    Args:
        filepath: Path to the SELECTED_OUTPUT file.

    Returns:
        A dict with keys ``columns`` (list of column names), ``data``
        (list of lists of floats), and ``row_count`` (int).  On error,
        the dict contains an ``error`` key with a description string.
    """
    try:
        with open(filepath) as f:
            lines = f.readlines()
    except FileNotFoundError as e:
        return {"error": f"File not found: {e}"}
    except OSError as e:
        return {"error": f"Error reading file: {e}"}

    # Collect non-comment, non-empty lines
    data_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip comment lines
        if stripped.startswith("#") or stripped.startswith("Selected"):
            continue
        data_lines.append(stripped)

    if not data_lines:
        return {"columns": [], "data": [], "row_count": 0}

    # First non-comment line is the column header
    columns = data_lines[0].split()
    num_cols = len(columns)

    # Parse data rows with mixed-type support.
    # PHREEQC may output non-numeric values (e.g. "i_soln" in the
    # "state" column).  Each value is tried as float individually;
    # non-numeric values are kept as strings.
    data: list[list] = []
    for line in data_lines[1:]:
        parts = line.split()
        if len(parts) != num_cols:
            continue  # skip malformed rows
        row: list = []
        for p in parts:
            try:
                row.append(float(p))
            except ValueError:
                row.append(p)  # keep non-numeric as string
        data.append(row)

    return {
        "columns": columns,
        "data": data,
        "row_count": len(data),
    }


def extract_saturation_indices(output_text: str, last: bool = False) -> list[dict]:
    """Extract saturation indices from standard PHREEQC output.

    Scans for the ``Saturation indices`` section header and extracts
    phase name and SI value pairs.

    Args:
        output_text: Full text of a PHREEQC output file.
        last: If ``True``, extract from the **last** occurrence
            (final state after all reactions). Default ``False``.

    Returns:
        List of dicts with keys ``phase`` (str) and ``si`` (float).
        Returns an empty list if the section is not found.
    """
    lines = output_text.splitlines()

    if last:
        # Find the LAST "Saturation indices" section
        pos = -1
        for i, line in enumerate(lines):
            if "Saturation indices" in line.strip():
                pos = i
        if pos < 0:
            return []
        lines = lines[pos:]  # Start from the last section

    results: list[dict[str, Any]] = []
    in_section = False

    for line in lines:
        stripped = line.strip()

        if not in_section:
            if "Saturation indices" in stripped:
                in_section = True
            continue

        # End of section
        if not stripped:
            if results:
                break
            continue
        if stripped.startswith("-"):
            continue

        # Skip column header line (starts with "Phase")
        if stripped.split() and stripped.split()[0] == "Phase":
            continue

        # Parse data line
        parts = stripped.split()
        if len(parts) < 2:
            continue

        try:
            si_val = float(parts[1])
        except ValueError:
            continue

        results.append({"phase": parts[0], "si": si_val})

    return results


def extract_species_distribution(output_text: str, last: bool = False) -> list[dict]:
    """Extract species distribution from PHREEQC output.

    Scans for a column header containing ``Species`` and ``Molality``
    and extracts species name, molality, and activity from subsequent
    data lines.

    Args:
        output_text: Full text of a PHREEQC output file.
        last: If ``True``, extract from the **last** occurrence
            (final state after all reactions). Default ``False``.

    Returns:
        List of dicts with keys ``species`` (str), ``molality`` (float),
        and ``activity`` (float).  Returns an empty list if the section
        is not found.
    """
    lines = output_text.splitlines()

    if last:
        # Find the LAST "Molality ... Species" header
        pos = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (
                "Molality" in stripped
                and "Species" in stripped
                and not stripped.startswith("-")
            ):
                pos = i
        if pos < 0:
            return []
        lines = lines[pos:]

    results: list[dict[str, Any]] = []
    in_section = False

    for line in lines:
        stripped = line.strip()

        if not in_section:
            # Column header contains "Molality" and "Species"
            # but is not a dashed separator
            if (
                "Molality" in stripped
                and "Species" in stripped
                and not stripped.startswith("-")
            ):
                in_section = True
            continue

        # Skip blank lines before first data row; break afterward
        if not stripped:
            if results:
                break
            continue
        if stripped.startswith("-"):
            break

        # Parse data line
        parts = stripped.split()
        if len(parts) < 3:
            continue

        try:
            molality = float(parts[1])
            activity = float(parts[2])
        except (ValueError, IndexError):
            continue

        results.append({
            "species": parts[0],
            "molality": molality,
            "activity": activity,
        })

    return results


def extract_element_molalities(output_text: str, last: bool = False) -> dict[str, float]:
    """Extract total element molalities from PHREEQC output.

    Scans for a column header containing ``Element`` and ``Molality``
    and extracts element name and molality from subsequent lines.

    Args:
        output_text: Full text of a PHREEQC output file.
        last: If ``True``, extract from the **last** occurrence
            (final state after all reactions). Default ``False``.

    Returns:
        Dict mapping element names to molality values.  Returns an empty
        dict if the section is not found.
    """
    lines = output_text.splitlines()

    if last:
        # Find the LAST "Element ... Molality" header
        pos = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (
                "Element" in stripped
                and "Molality" in stripped
                and not stripped.startswith("-")
            ):
                pos = i
        if pos < 0:
            return []
        lines = lines[pos:]

    results: dict[str, float] = {}
    in_section = False

    for line in lines:
        stripped = line.strip()

        if not in_section:
            # Column header contains "Element" and "Molality"
            # but is not a dashed separator
            if (
                "Element" in stripped
                and "Molality" in stripped
                and not stripped.startswith("-")
            ):
                in_section = True
            continue

        # Skip blank lines before first data row; break afterward
        if not stripped:
            if results:
                break
            continue
        if stripped.startswith("-"):
            break

        parts = stripped.split()
        if len(parts) < 2:
            continue

        try:
            molality = float(parts[1])
        except ValueError:
            continue

        results[parts[0]] = molality

    return results


def extract_ionic_strength(output_text: str, last: bool = True) -> float | None:
    """Extract ionic strength from PHREEQC standard output.

    Scans for lines containing ``Ionic strength`` and extracts the
    numeric value.

    Args:
        output_text: Full text of a PHREEQC output file.
        last: If ``True`` (default), returns the **last** occurrence
            (final simulation state after all reactions).  If
            ``False``, returns the **first** occurrence.

    Returns:
        Ionic strength in mol/kgw, or ``None`` if not found.
    """
    found: float | None = None
    for line in output_text.splitlines():
        if "Ionic strength" in line:
            parts = line.split()
            if parts:
                try:
                    val = float(parts[-1])
                    if not last:
                        return val
                    found = val
                except ValueError:
                    pass
    return found


def extract_exchange_composition(output_text: str, last: bool = False) -> list[dict]:
    """Extract exchange assemblage composition from PHREEQC output.

    Scans for ``Exchange composition`` section headers (dashed
    separators) or ``Exchange 1.`` blocks and extracts exchange species
    name, moles, equivalents, and equivalent fraction from the
    subsequent data table.

    Args:
        output_text: Full text of a PHREEQC output file.
        last: If ``True``, extract from the **last** occurrence
            (final state after all reactions). Default ``False``.

    Returns:
        List of dicts with keys ``species`` (str), ``moles`` (float),
        ``equivalents`` (float), and ``eq_frac`` (float, equivalent
        fraction).  Returns an empty list if the section is not found.
    """
    lines = output_text.splitlines()

    if last:
        pos = -1
        for i, line in enumerate(lines):
            s = line.strip()
            if ("Exchange composition" in s
                    and s.startswith("-")):
                pos = i
        if pos < 0:
            return []
        lines = lines[pos:]

    results: list[dict[str, Any]] = []
    in_section = False

    for line in lines:
        stripped = line.strip()

        if not in_section:
            # Section is marked by a dashed "Exchange composition" line
            # or "Exchange 1." heading
            if (("Exchange composition" in stripped
                    and stripped.startswith("-"))
                    or stripped.startswith("Exchange ")):
                in_section = True
            continue

        # End of section — dashed separator or blank after data
        if stripped.startswith("-"):
            if results:
                break
            continue
        if stripped.startswith("="):
            continue
        if not stripped:
            if results:
                break
            continue

        # Skip section lines showing total moles (e.g. "X  5.000e-02 mol")
        parts = stripped.split()
        if len(parts) >= 2 and parts[0].isalpha() and not parts[0][0].isupper():
            # lines like "X  5.000e-02 mol" have single-char or short site id
            if len(parts[0]) <= 2 and "mol" in parts[-1]:
                continue

        # Skip column header lines
        if parts and parts[0] in ("Species", "Exchange"):
            continue

        # Parse data line: Species Moles Equivalents Eq_Fraction [Log_Gamma]
        # Expected: CaX2  1.817e-02  3.634e-02  7.268e-01  -0.233
        if len(parts) < 3:
            continue

        try:
            moles = float(parts[1])
            equivalents = float(parts[2])
            eq_frac = float(parts[3]) if len(parts) >= 4 else 0.0
        except (ValueError, IndexError):
            continue

        results.append({
            "species": parts[0],
            "moles": moles,
            "equivalents": equivalents,
            "eq_frac": eq_frac,
        })

    return results


def to_json(
    selected_output_data: dict,
    saturation_indices: list[dict] | None = None,
    species: list[dict] | None = None,
    elements: dict[str, float] | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    """Serialize parsed results to a JSON string.

    Args:
        selected_output_data: Dict from
            :func:`parse_selected_output`.
        saturation_indices: Optional list from
            :func:`extract_saturation_indices`.
        species: Optional list from
            :func:`extract_species_distribution`.
        elements: Optional dict from
            :func:`extract_element_molalities`.
        metadata: Optional dict with arbitrary metadata (e.g.
            simulation parameters, timestamps).

    Returns:
        JSON string with ``indent=2`` and ``ensure_ascii=False``.
    """
    result: dict[str, Any] = {
        "selected_output": selected_output_data,
    }
    if saturation_indices is not None:
        result["saturation_indices"] = saturation_indices
    if species is not None:
        result["species_distribution"] = species
    if elements is not None:
        result["element_molalities"] = elements
    if metadata is not None:
        result["metadata"] = metadata
    return json.dumps(result, indent=2, ensure_ascii=False)
