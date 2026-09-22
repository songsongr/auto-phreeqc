import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "doctor" / "import_phreeqc_guide.py"
SPEC = importlib.util.spec_from_file_location("import_phreeqc_guide", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

QUERY_PATH = Path(__file__).parents[1] / "doctor" / "query_phreeqc_guide.py"
QUERY_SPEC = importlib.util.spec_from_file_location("query_phreeqc_guide", QUERY_PATH)
QUERY = importlib.util.module_from_spec(QUERY_SPEC)
assert QUERY_SPEC and QUERY_SPEC.loader
QUERY_SPEC.loader.exec_module(QUERY)


def test_normalize_phreeqc_input_removes_documentation_line_numbers():
    raw = "Line 0: SOLUTION 1\nLine 1:    pH 7\nLine 2:    Ca 1e-3"
    assert MODULE.normalize_phreeqc_input(raw) == "SOLUTION 1\npH 7\nCa 1e-3"


def test_chunk_kind_distinguishes_input_and_related_sections():
    assert MODULE.chunk_kind("Example data block", "code", "keyword") == "phreeqc_input"
    assert MODULE.chunk_kind("Related keywords", "SOLUTION, MIX", "keyword") == "related_keywords"
    assert MODULE.chunk_kind("Notes", "details", "keyword") == "note"


def test_input_from_section_combines_multiple_code_blocks():
    fence = chr(96) * 3
    section = f"{fence}phreeqc\nLine 0: SOLUTION 1\n{fence}\n| |\n{fence}phreeqc\nLine 1: pH 7\n{fence}"
    assert MODULE.input_from_section(section) == "SOLUTION 1\npH 7"


def test_extract_tables_preserves_rows_and_cells():
    tables = MODULE.extract_tables("<table><tr><th>Name</th><th>Value</th></tr><tr><td>Ca</td><td>1</td></tr></table>")
    assert tables == [[['Name', 'Value'], ['Ca', '1']]]


def test_query_fts_expression_is_agent_safe():
    assert QUERY.fts_expression("surface complexation") == '("surface"* AND "complexation"* OR "surface_complexation"*)'
