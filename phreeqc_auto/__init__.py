"""Public Python API for repeatable PHREEQC simulations.

The package is intentionally independent of any AI-agent integration, so it
can be used from the Workbench, a normal Python program, or a thin user-facing
Claude/Codex skill.
"""

from .generate_input import generate_single_simulation, write_input_file
from .parse_output import parse_selected_output
from .run_phreeqc import find_database, find_phreeqc_exe, run_simulation

__all__ = [
    "find_database",
    "find_phreeqc_exe",
    "generate_single_simulation",
    "parse_selected_output",
    "run_simulation",
    "write_input_file",
]

__version__ = "0.2.0"
