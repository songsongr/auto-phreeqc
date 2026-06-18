"""
Unit tests for the PHREEQC automation Python modules.

Tests for:
  - generate_input.py  (input file generation)
  - parse_output.py    (selected-output / standard-output parsing)
  - run_phreeqc.py     (executable / database discovery)
  - visualize.py       (import verification only -- no actual plots)

No PHREEQC executable is required to run these tests.
"""

import os
import sys
import json
import tempfile
import unittest

# Add the scripts directory to sys.path so we can import the modules
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import generate_input
import parse_output


# ============================================================================
# TestGenerateInput
# ============================================================================

class TestGenerateInput(unittest.TestCase):
    """Tests for generate_input.py"""

    maxDiff = None

    # ------------------------------------------------------------------
    # 1. generate_solution_block
    # ------------------------------------------------------------------

    def test_solution_block_includes_required_elements(self):
        """generate_solution_block includes SOLUTION 1, pH line, units, components."""
        block = generate_input.generate_solution_block(
            solution_id=1,
            units="mol/kgw",
            pH=7.0,
            pe=4.0,
            density=1.0,
            components={"Ca": 0.01, "Cl": 0.02},
        )
        self.assertIn("SOLUTION 1", block)
        self.assertIn("    units mol/kgw", block)
        self.assertIn("    pH 7.0", block)
        self.assertIn("    pe 4.0", block)
        self.assertIn("    density 1.0", block)
        self.assertIn("    Ca 0.01", block)
        self.assertIn("    Cl 0.02", block)

    def test_solution_block_omits_temp_when_default(self):
        """generate_solution_block omits temp line when temp=25.0."""
        block = generate_input.generate_solution_block(temp=25.0)
        self.assertNotIn("temp", block)

    def test_solution_block_includes_temp_when_non_default(self):
        """generate_solution_block includes temp line when temp != 25.0."""
        block = generate_input.generate_solution_block(temp=35.0)
        self.assertIn("    temp 35.0", block)

    # ------------------------------------------------------------------
    # 2. generate_equilibrium_phases_block
    # ------------------------------------------------------------------

    def test_equilibrium_phases_block(self):
        """generate_equilibrium_phases_block produces correct block."""
        block = generate_input.generate_equilibrium_phases_block(
            {"Calcite": (0.0, 10.0), "Gypsum": (-0.5, 5.0)},
            block_id=1,
        )
        self.assertIn("EQUILIBRIUM_PHASES 1", block)
        self.assertIn("    Calcite 0.0 10.0", block)
        self.assertIn("    Gypsum -0.5 5.0", block)

    # ------------------------------------------------------------------
    # 3. generate_reaction_block
    # ------------------------------------------------------------------

    def test_reaction_block(self):
        """generate_reaction_block produces correct REACTION block with moles in steps."""
        block = generate_input.generate_reaction_block(
            {"HCl": 1.0, "NaOH": 0.5},
            block_id=1, moles=2.0, steps=20,
        )
        self.assertIn("REACTION 1", block)
        self.assertIn("    HCl 1.0", block)
        self.assertIn("    NaOH 0.5", block)
        self.assertIn("    2.0 moles in 20 steps", block)

    # ------------------------------------------------------------------
    # 4. generate_selected_output_block
    # ------------------------------------------------------------------

    def test_selected_output_block(self):
        """generate_selected_output_block includes -file, -si, -totals."""
        block = generate_input.generate_selected_output_block(
            file="results.txt",
            si=["Calcite", "Gypsum"],
            totals=["Ca", "Mg"],
            molalities=["Ca+2", "Mg+2"],
        )
        self.assertIn("SELECTED_OUTPUT", block)
        self.assertIn("    -file results.txt", block)
        self.assertIn("    -si Calcite", block)
        self.assertIn("    -si Gypsum", block)
        self.assertIn("    -totals Ca", block)
        self.assertIn("    -totals Mg", block)
        self.assertIn("    -molalities Ca+2", block)
        self.assertIn("    -molalities Mg+2", block)

    def test_selected_output_block_minimal(self):
        """generate_selected_output_block works with no optional args."""
        block = generate_input.generate_selected_output_block(file="out.txt")
        self.assertIn("SELECTED_OUTPUT", block)
        self.assertIn("    -file out.txt", block)
        self.assertIn("    -pH", block)
        self.assertIn("    -pe", block)
        self.assertNotIn("-si", block)
        self.assertNotIn("-totals", block)
        self.assertNotIn("-molalities", block)

    # ------------------------------------------------------------------
    # 5. generate_single_simulation -- speciation (solution only)
    # ------------------------------------------------------------------

    def test_single_simulation_speciation(self):
        """generate_single_simulation produces .pqi for speciation (no reaction blocks)."""
        params = {
            "solution": {
                "id": 1,
                "units": "ppm",
                "pH": 8.2,
                "components": {"Ca": 400.0, "Mg": 1200.0},
            },
            "selected_output": {"si": ["Calcite"]},
        }
        content = generate_input.generate_single_simulation(
            params, output_file="speciation.txt",
        )
        self.assertIn("SOLUTION 1", content)
        self.assertIn("    units ppm", content)
        self.assertIn("    pH 8.2", content)
        self.assertIn("    Ca 400.0", content)
        self.assertIn("    Mg 1200.0", content)
        self.assertIn("SELECTED_OUTPUT", content)
        self.assertIn("    -file speciation.txt", content)
        self.assertIn("    -si Calcite", content)
        self.assertIn("END", content)
        self.assertNotIn("EQUILIBRIUM_PHASES", content)
        self.assertNotIn("REACTION", content)

    # ------------------------------------------------------------------
    # 6. generate_single_simulation -- batch (solution + phases + output)
    # ------------------------------------------------------------------

    def test_single_simulation_batch(self):
        """generate_single_simulation produces .pqi for batch run."""
        params = {
            "solution": {"pH": 7.0, "components": {"Na": 1.0, "Cl": 1.0}},
            "equilibrium_phases": {"Halite": (0.0, 10.0)},
            "selected_output": {"totals": ["Na", "Cl"]},
        }
        content = generate_input.generate_single_simulation(
            params, output_file="batch.txt",
        )
        self.assertIn("SOLUTION 1", content)
        self.assertIn("EQUILIBRIUM_PHASES 1", content)
        self.assertIn("    Halite 0.0 10.0", content)
        self.assertIn("SELECTED_OUTPUT", content)
        self.assertIn("    -file batch.txt", content)
        self.assertIn("    -totals Na", content)
        self.assertIn("    -totals Cl", content)
        self.assertIn("END", content)

    # ------------------------------------------------------------------
    # 7. write_input_file
    # ------------------------------------------------------------------

    def test_write_input_file(self):
        """write_input_file writes content and returns absolute path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_input.pqi")
            content = "SOLUTION 1\npH 7.0\nEND\n"
            result = generate_input.write_input_file(content, filepath)
            # Returns absolute path
            self.assertEqual(os.path.abspath(filepath), result)
            self.assertTrue(os.path.isabs(result))
            # File exists with correct content
            with open(result) as f:
                self.assertEqual(f.read(), content)

    def test_write_input_file_creates_dirs(self):
        """write_input_file creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested = os.path.join(tmpdir, "sub", "nested", "input.pqi")
            result = generate_input.write_input_file("test", nested)
            self.assertTrue(os.path.isfile(result))

    # ------------------------------------------------------------------
    # 8. generate_parameter_sweep
    # ------------------------------------------------------------------

    def test_parameter_sweep_structure(self):
        """generate_parameter_sweep produces multi-step with END separators."""
        base_params = {
            "solution": {"pH": 7.0, "components": {"Ca": 0.01}},
            "selected_output": {"si": ["Calcite"]},
        }
        content = generate_input.generate_parameter_sweep(
            base_params,
            sweep_param="solution.pH",
            sweep_values=[6.0, 7.0, 8.0],
            output_dir="/tmp/sweep",
        )
        # Each simulation ends with END, joined by blank lines
        self.assertEqual(content.count("END"), 3)
        self.assertIn("step_1.txt", content)
        self.assertIn("step_2.txt", content)
        self.assertIn("step_3.txt", content)
        # pH values are swept
        self.assertIn("    pH 6.0", content)
        self.assertIn("    pH 7.0", content)
        self.assertIn("    pH 8.0", content)


# ============================================================================
# TestParseOutput
# ============================================================================

class TestParseOutput(unittest.TestCase):
    """Tests for parse_output.py"""

    # ------------------------------------------------------------------
    # 1. parse_selected_output -- basic
    # ------------------------------------------------------------------

    def test_parse_selected_output(self):
        """parse_selected_output parses tabular data into columns + data."""
        content = (
            "step\tpH\t\tCa\t\tMg\n"
            "1\t7.0\t\t0.01\t\t0.02\n"
            "2\t8.0\t\t0.02\t\t0.03\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(content)
            tmpname = f.name
        try:
            result = parse_output.parse_selected_output(tmpname)
            self.assertEqual(result["columns"], ["step", "pH", "Ca", "Mg"])
            self.assertEqual(len(result["data"]), 2)
            self.assertEqual(result["row_count"], 2)
            self.assertEqual(result["data"][0], [1.0, 7.0, 0.01, 0.02])
            self.assertEqual(result["data"][1], [2.0, 8.0, 0.02, 0.03])
        finally:
            os.unlink(tmpname)

    def test_parse_selected_output_skips_comments(self):
        """parse_selected_output ignores comment lines starting with # or Selected."""
        content = (
            "# This is a header comment\n"
            "Selected output file\n"
            "pH\tCa\n"
            "7.0\t0.01\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(content)
            tmpname = f.name
        try:
            result = parse_output.parse_selected_output(tmpname)
            self.assertEqual(result["columns"], ["pH", "Ca"])
            self.assertEqual(result["data"], [[7.0, 0.01]])
        finally:
            os.unlink(tmpname)

    # ------------------------------------------------------------------
    # 2. parse_selected_output -- nonexistent file
    # ------------------------------------------------------------------

    def test_parse_selected_output_nonexistent(self):
        """parse_selected_output returns error key for nonexistent file."""
        result = parse_output.parse_selected_output(
            os.path.join(tempfile.gettempdir(), "_does_not_exist_12345_.txt")
        )
        self.assertIn("error", result)
        self.assertIn("File not found", result["error"])

    # ------------------------------------------------------------------
    # 3. parse_selected_output -- empty file
    # ------------------------------------------------------------------

    def test_parse_selected_output_empty(self):
        """parse_selected_output handles empty file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            tmpname = f.name
        try:
            result = parse_output.parse_selected_output(tmpname)
            self.assertEqual(result["columns"], [])
            self.assertEqual(result["data"], [])
            self.assertEqual(result["row_count"], 0)
        finally:
            os.unlink(tmpname)

    # ------------------------------------------------------------------
    # 4. extract_saturation_indices
    # ------------------------------------------------------------------

    _SI_OUTPUT = """\
                               Saturation indices
                               ==================

  Phase                 SI**  log IAP   log KT

  Calcite              0.85   1.85      1.00
  Dolomite             1.20   3.50      2.30
  Quartz              -0.50  -4.00     -3.50

"""

    def test_extract_saturation_indices(self):
        """extract_saturation_indices extracts correct SI values."""
        result = parse_output.extract_saturation_indices(self._SI_OUTPUT)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {"phase": "Calcite", "si": 0.85})
        self.assertEqual(result[1], {"phase": "Dolomite", "si": 1.20})
        self.assertEqual(result[2], {"phase": "Quartz", "si": -0.50})

    # ------------------------------------------------------------------
    # 5. extract_saturation_indices -- no section
    # ------------------------------------------------------------------

    def test_extract_saturation_indices_no_section(self):
        """extract_saturation_indices returns [] when no SI section."""
        text = "Some random output\nno saturation indices here\n"
        result = parse_output.extract_saturation_indices(text)
        self.assertEqual(result, [])

    # ------------------------------------------------------------------
    # 6. extract_species_distribution
    # ------------------------------------------------------------------

    _SPECIES_OUTPUT = """\
                             Species distribution
                             ====================

  Species                Molality       Activity     Log Mol    Log Act
  H+                      1.234e-08      1.234e-08    -7.909     -7.909
  OH-                     5.678e-07      5.678e-07    -6.246     -6.246
  Ca+2                    1.000e-02      5.000e-03    -2.000     -2.301
"""

    def test_extract_species_distribution(self):
        """extract_species_distribution extracts correct species, molality, activity."""
        result = parse_output.extract_species_distribution(self._SPECIES_OUTPUT)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {"species": "H+", "molality": 1.234e-08, "activity": 1.234e-08})
        self.assertEqual(result[1], {"species": "OH-", "molality": 5.678e-07, "activity": 5.678e-07})
        self.assertEqual(result[2], {"species": "Ca+2", "molality": 1.000e-02, "activity": 5.000e-03})

    def test_extract_species_distribution_no_section(self):
        """extract_species_distribution returns [] when no species section."""
        result = parse_output.extract_species_distribution("no species here")
        self.assertEqual(result, [])

    # ------------------------------------------------------------------
    # 7. extract_element_molalities
    # ------------------------------------------------------------------

    _ELEMENT_OUTPUT = """\
  Ca                    1.234e-02
  Cl                    2.468e-02
  Mg                    3.456e-03

"""

    def test_extract_element_molalities(self):
        """extract_element_molalities extracts correct element molalities."""
        text = (
            "  Element          Molality\n"
            "  =======          =======\n"
            "  Ca                    1.234e-02\n"
            "  Cl                    2.468e-02\n"
            "  Mg                    3.456e-03\n"
        )
        result = parse_output.extract_element_molalities(text)
        self.assertAlmostEqual(result["Ca"], 1.234e-02)
        self.assertAlmostEqual(result["Cl"], 2.468e-02)
        self.assertAlmostEqual(result["Mg"], 3.456e-03)

    def test_extract_element_molalities_no_section(self):
        """extract_element_molalities returns {} when no element section."""
        result = parse_output.extract_element_molalities("no elements here")
        self.assertEqual(result, {})

    def test_extract_element_molalities_needs_header_line(self):
        """extract_element_molalities only parses section after header line."""
        # The element output without the header line should not match
        result = parse_output.extract_element_molalities(self._ELEMENT_OUTPUT)
        self.assertEqual(result, {})

    # ------------------------------------------------------------------
    # to_json
    # ------------------------------------------------------------------

    def test_to_json(self):
        """to_json serialises parsed data to JSON correctly."""
        so_data = {"columns": ["pH"], "data": [[7.0]], "row_count": 1}
        si_data = [{"phase": "Calcite", "si": 0.85}]
        species = [{"species": "H+", "molality": 1e-8, "activity": 1e-8}]
        elements = {"Ca": 0.01}
        metadata = {"simulation": "test"}

        json_str = parse_output.to_json(so_data, si_data, species, elements, metadata)
        parsed = json.loads(json_str)

        self.assertEqual(parsed["selected_output"], so_data)
        self.assertEqual(parsed["saturation_indices"], si_data)
        self.assertEqual(parsed["species_distribution"], species)
        self.assertEqual(parsed["element_molalities"], elements)
        self.assertEqual(parsed["metadata"], metadata)


# ============================================================================
# TestRunPhreeqc (imports only -- no actual PHREEQC execution)
# ============================================================================

class TestRunPhreeqc(unittest.TestCase):
    """Tests for run_phreeqc.py (import verification and logic tests)."""

    def test_module_imports(self):
        """run_phreeqc module can be imported and exposes expected names."""
        import run_phreeqc
        expected = {"find_phreeqc_exe", "find_database", "run_simulation"}
        self.assertTrue(expected.issubset(set(run_phreeqc.__all__)))

    def test_find_phreeqc_exe_behavior(self):
        """find_phreeqc_exe either returns a path or raises FileNotFoundError.

        This test does not require PHREEQC to be installed.  If the
        executable happens to be available on this machine the function
        should return a non-empty string; otherwise it raises.
        """
        import run_phreeqc
        try:
            path = run_phreeqc.find_phreeqc_exe()
            self.assertIsInstance(path, str)
            self.assertTrue(len(path) > 0)
        except FileNotFoundError:
            pass  # Expected when PHREEQC is not available

    def test_find_database_raises_when_not_found(self):
        """find_database raises FileNotFoundError when db cannot be located."""
        import run_phreeqc
        with self.assertRaises(FileNotFoundError):
            try:
                run_phreeqc.find_database("_nonexistent_db_file_.dat")
            except FileNotFoundError:
                raise


# ============================================================================
# TestVisualize (imports only)
# ============================================================================

class TestVisualize(unittest.TestCase):
    """Tests for visualize.py (import verification only)."""

    def test_module_imports(self):
        """visualize module can be imported and exposes expected names."""
        import visualize
        expected = {"plot_saturation_indices", "plot_selected_output_sweep", "plot_multi_panel"}
        self.assertTrue(expected.issubset(set(visualize.__all__)))


# ============================================================================
# Entry point
# ============================================================================

if __name__ == "__main__":
    unittest.main()
