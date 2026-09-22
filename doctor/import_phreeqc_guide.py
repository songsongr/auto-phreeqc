#!/usr/bin/env python3
"""Import the USGS PHREEQC v3 HTML guide into the project's docs tree.

The importer deliberately uses only the Python standard library so that the
guide can be refreshed on a clean checkout. It keeps the downloaded HTML as
the source of truth and emits Markdown plus JSONL records for later indexing.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sqlite3
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen


BASE_URL = "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/"
ENTRY_URL = urljoin(BASE_URL, "phreeqc3.htm")
RETRIEVED = time.strftime("%Y-%m-%d", time.gmtime())
SCHEMA_VERSION = "0.3"

ZH_ALIASES = {
    "SOLUTION": ["溶液", "水溶液", "speciation", "形态分布"],
    "EQUILIBRIUM_PHASES": ["平衡相", "纯相平衡", "矿物平衡"],
    "EXCHANGE": ["离子交换", "阳离子交换"],
    "SURFACE": ["表面络合", "吸附", "表面吸附"],
    "GAS_PHASE": ["气相", "气体平衡", "气相平衡"],
    "KINETICS": ["动力学", "动力学反应"],
    "RATES": ["速率方程", "BASIC 速率"],
    "MIX": ["溶液混合", "混合"],
    "TRANSPORT": ["反应性运移", "溶质运移", "传输"],
    "ADVECTION": ["平流", "平流运移"],
    "INVERSE_MODELING": ["反演建模", "地球化学反演"],
    "SELECTED_OUTPUT": ["选定输出", "输出表"],
    "PHASES": ["矿物定义", "相定义"],
    "SOLUTION_SPECIES": ["水溶液物种", "溶液物种"],
    "SURFACE_SPECIES": ["表面物种", "表面络合物种"],
}

PHREEQC_BLOCKS = {
    "ADVECTION", "CALCULATE_VALUES", "COPY", "DATABASE", "DELETE", "DUMP",
    "END", "EQUILIBRIUM_PHASES", "EXCHANGE", "GAS_PHASE", "INCREMENTAL_REACTIONS",
    "INVERSE_MODELING", "KINETICS", "MIX", "NAMED_EXPRESSIONS", "PHASES", "PITZER",
    "RATES", "REACTION", "REACTION_PRESSURE", "REACTION_TEMPERATURE", "RUN_CELLS",
    "SAVE", "SELECTED_OUTPUT", "SOLID_SOLUTIONS", "SOLUTION", "SOLUTION_MODIFY",
    "SOLUTION_SPECIES", "SOLUTION_MASTER_SPECIES", "SOURCES", "SURFACE", "TRANSPORT",
    "TITLE", "USER_PRINT", "USER_PUNCH", "END",
}


def clean_text(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    return re.sub(r"[ \t\r\f\v]+", " ", value).strip()


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "page"


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def is_navigation(value: str) -> bool:
    compact = re.sub(r"\s+", " ", value).strip().lower()
    return (
        compact.startswith("| [next]")
        or compact.startswith("[next]")
        or ("[previous]" in compact and "[top]" in compact)
        or compact in {"next", "previous", "top"}
    )


def normalize_phreeqc_input(value: str) -> str:
    lines = []
    for line in value.replace("\xa0", " ").splitlines():
        line = re.sub(r"^\s*Line\s+[0-9A-Za-z]+:\s*", "", line, flags=re.I)
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def identifiers_from_text(value: str) -> List[str]:
    found = sorted(set(re.findall(r"(?<![\w-])-[a-z][a-z0-9_]*(?![\w-])", value, re.I)))
    return found


def input_from_section(value: str) -> Optional[str]:
    fence = chr(96) * 3
    blocks = re.findall(re.escape(fence) + r"phreeqc\s*\n(.*?)\n" + re.escape(fence), value, re.S)
    if not blocks:
        return None
    return normalize_phreeqc_input("\n".join(blocks))


class TableParser(HTMLParser):
    """Extract HTML tables without depending on the lossy paragraph parser."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.table_depth = 0
        self.current_table: Optional[List[List[str]]] = None
        self.current_row: Optional[List[str]] = None
        self.current_cell: Optional[List[str]] = None
        self.tables: List[List[List[str]]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        if tag == "table":
            self.table_depth += 1
            if self.table_depth == 1:
                self.current_table = []
        elif tag == "tr" and self.table_depth == 1:
            self.current_row = []
        elif tag in {"td", "th"} and self.table_depth == 1 and self.current_row is not None:
            self.current_cell = []
        elif tag == "br" and self.current_cell is not None:
            self.current_cell.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self.current_cell is not None and self.current_row is not None:
            self.current_row.append(clean_text("".join(self.current_cell)))
            self.current_cell = None
        elif tag == "tr" and self.current_row is not None and self.current_table is not None:
            if any(cell for cell in self.current_row):
                self.current_table.append(self.current_row)
            self.current_row = None
        elif tag == "table" and self.table_depth == 1:
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = None
            self.table_depth = 0

    def handle_data(self, data: str) -> None:
        if self.current_cell is not None:
            self.current_cell.append(re.sub(r"\s+", " ", data))


def extract_tables(source: str) -> List[List[List[str]]]:
    parser = TableParser()
    parser.feed(source)
    parser.close()
    return parser.tables


def extract_equations(content: str) -> List[str]:
    equations = []
    for line in content.splitlines():
        candidate = clean_text(re.sub(r"^\s*[|#`-]+\s*", "", line))
        if not candidate or candidate.startswith("Line "):
            continue
        if " = " in candidate or "→" in candidate or " -> " in candidate:
            if candidate not in equations and len(candidate) <= 300:
                equations.append(candidate)
    return equations


def example_simulation_types(title: str, content: str) -> List[str]:
    intro = content.split("Table ", 1)[0]
    text = f"{title} {intro[:3000]}".lower()
    rules = [
        ("speciation", ("speciation", "distribution of aqueous species")),
        ("equilibrium", ("equilibration", "pure phase", "equilibrium phases")),
        ("mixing", ("mixing", "mix solution")),
        ("reaction_path", ("reaction-path", "reaction path")),
        ("gas_phase", ("gas-phase", "gas phase", "gas solubility")),
        ("surface_complexation", ("surface complexation", "sorption")),
        ("kinetics", ("kinetic", "kinetics")),
        ("transport", ("transport", "advective", "diffusive flux", "diffusion")),
        ("cation_exchange", ("cation exchange", "exchange")),
        ("inverse_modeling", ("inverse modeling", "inverse model")),
        ("isotopes", ("isotope", "isotopes")),
    ]
    return [name for name, needles in rules if any(needle in text for needle in needles)]


class GuideParser(HTMLParser):
    """Extract readable blocks from the FrameMaker-exported HTML pages."""

    BLOCK_TAGS = {"p", "li", "pre", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}
    SKIP_CONTAINER_TAGS = {"script", "style", "noscript", "head", "title"}
    SKIP_VOID_TAGS = {"meta", "link"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_body = False
        self.skip_depth = 0
        self.current: Optional[Dict[str, object]] = None
        self.blocks: List[Tuple[str, str, Optional[str]]] = []
        self._link_stack: List[Optional[str]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        attr = {k.lower(): (v or "") for k, v in attrs}
        if tag == "body":
            self.in_body = True
            return
        if tag in self.SKIP_VOID_TAGS:
            return
        if tag in self.SKIP_CONTAINER_TAGS:
            self.skip_depth += 1
            return
        if not self.in_body or self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self.flush()
            kind = "row" if tag == "tr" else tag
            self.current = {"kind": kind, "parts": []}
        elif tag == "br" and self.current is not None:
            self.current["parts"].append("\n")  # type: ignore[index]
        elif tag in {"td", "th"} and self.current is not None:
            parts = self.current["parts"]  # type: ignore[index]
            if parts and not str(parts[-1]).endswith(" | "):
                parts.append(" | ")
        elif tag == "a":
            href = attr.get("href") or None
            anchor = attr.get("name") or attr.get("id")
            if anchor and self.current is not None and not self.current.get("anchor"):
                self.current["anchor"] = anchor
            self._link_stack.append(href)
            if href and self.current is not None:
                self.current["parts"].append("[")  # type: ignore[index]

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_CONTAINER_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if not self.in_body or self.skip_depth:
            return
        if tag == "a":
            href = self._link_stack.pop() if self._link_stack else None
            if href and self.current is not None:
                self.current["parts"].append(f"]({href})")  # type: ignore[index]
        elif tag in self.BLOCK_TAGS:
            self.flush()
        elif tag == "body":
            self.flush()
            self.in_body = False

    def handle_data(self, data: str) -> None:
        if not data or self.skip_depth or not self.in_body:
            return
        if self.current is None:
            self.current = {"kind": "p", "parts": []}
        if self.current["kind"] == "pre":
            text = data.replace("\r\n", "\n").replace("\r", "\n")
        else:
            text = re.sub(r"\s+", " ", data)
        self.current["parts"].append(text)  # type: ignore[index]

    def flush(self) -> None:
        if self.current is None:
            return
        kind = str(self.current["kind"])
        raw = "".join(str(p) for p in self.current["parts"])  # type: ignore[index]
        value = raw.strip("\n") if kind == "pre" else clean_text(raw.replace("\n", " "))
        if value:
            self.blocks.append((kind, value, self.current.get("anchor")))  # type: ignore[arg-type]
        self.current = None


def decode_html(raw: bytes, content_type: str = "") -> str:
    match = re.search(r"charset=([\w-]+)", content_type, re.I)
    encodings = [match.group(1)] if match else []
    encodings += ["utf-8", "iso-8859-1"]
    for encoding in encodings:
        try:
            return raw.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("iso-8859-1", errors="replace")


def fetch(url: str) -> Tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": "phreeqc-auto-guide-import/1.0"})
    with urlopen(request, timeout=45) as response:
        return response.read(), response.headers.get("Content-Type", "")


def local_html_links(source: str) -> Iterable[str]:
    for match in re.finditer(r"(?:href|src)\s*=\s*[\"']([^\"']+\.htm(?:#[^\"']*)?)[\"']", source, re.I):
        href = html.unescape(match.group(1))
        full, _ = urldefrag(urljoin(BASE_URL, href))
        parsed = urlparse(full)
        base = urlparse(BASE_URL)
        if parsed.netloc == base.netloc and parsed.path.startswith(base.path):
            yield full


def title_from_parser(source: str, page_parser: GuideParser, filename: str) -> str:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", source, re.I | re.S)
    if title_match:
        title = clean_text(re.sub(r"<[^>]+>", " ", title_match.group(1)))
        if title:
            return title
    for kind, value, _ in page_parser.blocks:
        if kind.startswith("h"):
            return value
    return Path(filename).stem


def markdown_from_blocks(title: str, page_parser: GuideParser) -> Tuple[str, List[str]]:
    fence = chr(96) * 3
    lines: List[str] = [f"# {title}", ""]
    headings: List[str] = []
    seen = set()
    index = 0
    while index < len(page_parser.blocks):
        kind, value, _ = page_parser.blocks[index]
        value = re.sub(r"\[\]\([^)]+\)", "", value)
        if is_navigation(value):
            index += 1
            continue
        if kind.startswith("h"):
            value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
            value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
            level = min(6, max(2, int(kind[1:])))
            if value.lower() == title.lower() and not headings:
                headings.append(value)
                continue
            lines += [f"{'#' * level} {value}", ""]
            headings.append(value)
        elif kind == "pre":
            code_lines = [value]
            next_index = index + 1
            while next_index < len(page_parser.blocks) and page_parser.blocks[next_index][0] == "pre":
                code_lines.append(page_parser.blocks[next_index][1])
                next_index += 1
            code = "\n".join(code_lines).rstrip()
            if code:
                lines += [fence + "phreeqc", code, fence, ""]
            index = next_index - 1
        elif kind == "row":
            lines.append(f"| {value.strip(' | ')} |")
        elif kind == "li":
            lines.append(f"- {value}")
        elif value not in seen:
            lines += [value, ""]
            seen.add(value)
        index += 1
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + "\n", headings


def category_for(title: str, source_file: str) -> str:
    upper = title.upper().strip()
    excluded = {"PHREEQC3 HTML", "PHREEQC VERSION 3"}
    if source_file.lower() in {"phreeqc3.htm", "phreeqc3-62.htm"}:
        return "navigation"
    if source_file.lower() == "gas_binary_parameters.htm":
        upper = "GAS_BINARY_PARAMETERS"
        title = upper
    if "EXAMPLE" in upper or source_file.lower().startswith("examples"):
        return "example"
    if upper not in excluded and upper == title.strip() and re.fullmatch(r"[A-Z0-9_+() .,/:\-$]+", upper or ""):
        if not upper.startswith("APPENDIX") and len(upper) <= 80:
            return "keyword"
    return "concept"


def split_sections(markdown: str) -> List[Tuple[str, str, int]]:
    matches = list(re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", markdown))
    if not matches:
        return [("page", markdown.strip(), 1)]
    sections: List[Tuple[str, str, int]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        content = markdown[match.start():end].strip()
        if content and not re.fullmatch(r"#\s+.+", content, flags=re.S):
            sections.append((match.group(2).strip(), content, len(match.group(1))))
    return sections


def chunk_kind(section_title: str, content: str, category: str) -> str:
    title = section_title.lower().strip()
    if category == "navigation":
        return "navigation"
    if "example data block" in title:
        return "phreeqc_input"
    if category == "example":
        return "tutorial"
    if title.startswith("example"):
        return "example_context"
    if "related keyword" in title:
        return "related_keywords"
    if title in {"explanation", "notes", "note"} or title.startswith(("explanation ", "notes ")):
        return "explanation" if title.startswith("explanation") else "note"
    if any(token in title for token in ("equation", "formula", "charge-potential", "activity coefficient")):
        return "equation"
    if "|" in content and content.count("|") >= 4:
        return "table"
    return "keyword" if category == "keyword" else "concept"


def build_agent_indexes(
    guide_root: Path,
    knowledge_dir: Path,
    records: List[Dict[str, object]],
    chunks: List[Dict[str, object]],
    keyword_terms: Dict[str, List[str]],
    failures: List[Dict[str, str]],
    table_records: List[Dict[str, object]],
) -> None:
    known_keywords = set(keyword_terms)
    for chunk in chunks:
        detected = set(chunk.get("keywords", []))
        if chunk.get("keyword"):
            detected.add(str(chunk["keyword"]))
        detected.update(
            token for token in re.findall(r"\b[A-Z][A-Z0-9_+$-]{2,}\b", str(chunk["content"]))
            if token in known_keywords
        )
        chunk["keywords"] = sorted(detected)
        chunk.setdefault("source_anchor", None)

    symbols: Dict[str, Dict[str, object]] = {}
    for keyword, paths in sorted(keyword_terms.items()):
        identifiers = sorted({
            identifier
            for chunk in chunks
            if chunk.get("keyword") == keyword
            for identifier in chunk.get("identifiers", [])
        })
        aliases = sorted(set([keyword, keyword.lower()] + ZH_ALIASES.get(keyword, [])))
        source_urls = sorted({
            str(chunk["source_url"])
            for chunk in chunks
            if chunk.get("keyword") == keyword
        })
        symbols[keyword] = {
            "symbol": keyword,
            "kind": "keyword",
            "aliases": aliases,
            "identifiers": identifiers,
            "source_pages": paths,
            "source_urls": source_urls,
        }
        for identifier in identifiers:
            symbols.setdefault(identifier, {
                "symbol": identifier,
                "kind": "identifier",
                "aliases": [identifier, identifier.lstrip("-")],
                "keyword": keyword,
                "source_pages": paths,
                "source_urls": source_urls,
            })
    (knowledge_dir / "symbols.json").write_text(
        json.dumps(symbols, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    relations = []
    for chunk in chunks:
        if chunk["type"] != "related_keywords" or not chunk.get("keyword"):
            continue
        source = str(chunk["keyword"])
        targets = sorted({
            token for token in re.findall(r"\b[A-Z][A-Z0-9_+$-]{2,}\b", str(chunk["content"]))
            if token in known_keywords and token != source
        })
        for target in targets:
            relations.append({
                "source": source,
                "relation": "related_to",
                "target": target,
                "source_file": chunk["source_file"],
                "source_url": chunk["source_url"],
            })
    with (knowledge_dir / "relations.jsonl").open("w", encoding="utf-8") as handle:
        for relation in relations:
            handle.write(json.dumps(relation, ensure_ascii=False) + "\n")

    equation_records = []
    for chunk in chunks:
        for number, expression in enumerate(extract_equations(str(chunk["content"])), start=1):
            equation_records.append({
                "id": f"{chunk['id']}::equation-{number}",
                "chunk_id": chunk["id"],
                "doc_id": chunk["doc_id"],
                "expression": expression,
                "source_file": chunk["source_file"],
                "source_url": chunk["source_url"],
                "source_anchor": chunk.get("source_anchor"),
            })
    with (knowledge_dir / "equations.jsonl").open("w", encoding="utf-8") as handle:
        for equation in equation_records:
            handle.write(json.dumps(equation, ensure_ascii=False) + "\n")

    with (knowledge_dir / "tables.jsonl").open("w", encoding="utf-8") as handle:
        for table in table_records:
            handle.write(json.dumps(table, ensure_ascii=False) + "\n")

    with (knowledge_dir / "chunks.jsonl").open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    database_path = knowledge_dir / "index.sqlite"
    if database_path.exists():
        database_path.unlink()
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(
            """
            CREATE TABLE documents (
                doc_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                source_file TEXT NOT NULL,
                source_url TEXT NOT NULL,
                page_path TEXT NOT NULL
            );
            CREATE TABLE chunks (
                chunk_id TEXT PRIMARY KEY,
                doc_id TEXT NOT NULL,
                position INTEGER NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                keyword TEXT,
                section_path TEXT NOT NULL,
                content TEXT NOT NULL,
                retrieval_text TEXT NOT NULL,
                input TEXT,
                identifiers TEXT NOT NULL,
                keywords TEXT NOT NULL,
                source_file TEXT NOT NULL,
                source_url TEXT NOT NULL,
                source_anchor TEXT,
                page_path TEXT NOT NULL
            );
            CREATE TABLE symbols (
                symbol TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                keyword TEXT,
                aliases TEXT NOT NULL,
                identifiers TEXT NOT NULL,
                source_pages TEXT NOT NULL,
                source_urls TEXT NOT NULL
            );
            CREATE TABLE relations (
                source TEXT NOT NULL,
                relation TEXT NOT NULL,
                target TEXT NOT NULL,
                source_url TEXT NOT NULL
            );
            CREATE TABLE tables (
                table_id TEXT PRIMARY KEY,
                doc_id TEXT NOT NULL,
                source_file TEXT NOT NULL,
                source_url TEXT NOT NULL,
                rows_json TEXT NOT NULL
            );
            CREATE TABLE equations (
                equation_id TEXT PRIMARY KEY,
                chunk_id TEXT NOT NULL,
                doc_id TEXT NOT NULL,
                expression TEXT NOT NULL,
                source_file TEXT NOT NULL,
                source_url TEXT NOT NULL,
                source_anchor TEXT
            );
            CREATE VIRTUAL TABLE chunks_fts USING fts5(
                chunk_id UNINDEXED,
                title,
                retrieval_text,
                content,
                keyword
            );
            """
        )
        connection.executemany(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?)",
            [
                (r["id"], r["title"], r["category"], r["source_file"], r["source_url"], r["markdown_path"])
                for r in records
            ],
        )
        connection.executemany(
            "INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    c["id"], c["doc_id"], c["position"], c["type"], c["title"], c.get("keyword"),
                    json.dumps(c["section_path"], ensure_ascii=False), c["content"],
                    c["retrieval_text"], c.get("input"), json.dumps(c.get("identifiers", []), ensure_ascii=False),
                    json.dumps(c.get("keywords", []), ensure_ascii=False), c["source_file"], c["source_url"],
                    c.get("source_anchor"), c["page_path"],
                )
                for c in chunks
            ],
        )
        connection.executemany(
            "INSERT INTO chunks_fts VALUES (?, ?, ?, ?, ?)",
            [(c["id"], c["title"], c["retrieval_text"], c["content"], c.get("keyword") or "") for c in chunks],
        )
        connection.executemany(
            "INSERT INTO symbols VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    key, value["kind"], value.get("keyword"),
                    json.dumps(value.get("aliases", []), ensure_ascii=False),
                    json.dumps(value.get("identifiers", []), ensure_ascii=False),
                    json.dumps(value.get("source_pages", []), ensure_ascii=False),
                    json.dumps(value.get("source_urls", []), ensure_ascii=False),
                )
                for key, value in symbols.items()
            ],
        )
        connection.executemany(
            "INSERT INTO relations VALUES (?, ?, ?, ?)",
            [(r["source"], r["relation"], r["target"], r["source_url"]) for r in relations],
        )
        connection.executemany(
            "INSERT INTO tables VALUES (?, ?, ?, ?, ?)",
            [
                (t["id"], t["doc_id"], t["source_file"], t["source_url"], json.dumps(t["rows"], ensure_ascii=False))
                for t in table_records
            ],
        )
        connection.executemany(
            "INSERT INTO equations VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    e["id"], e["chunk_id"], e["doc_id"], e["expression"],
                    e["source_file"], e["source_url"], e.get("source_anchor"),
                )
                for e in equation_records
            ],
        )
        connection.commit()
        fts5_available = True
    except sqlite3.OperationalError:
        connection.rollback()
        fts5_available = False
    finally:
        connection.close()

    counts: Dict[str, int] = {}
    for chunk in chunks:
        counts[chunk["type"]] = counts.get(chunk["type"], 0) + 1
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated": RETRIEVED,
        "source": ENTRY_URL,
        "parser": "doctor/import_phreeqc_guide.py",
        "documents": len(records),
        "chunks": len(chunks),
        "symbols": len(symbols),
        "relations": len(relations),
        "tables": len(table_records),
        "equations": len(equation_records),
        "chunk_types": counts,
        "failures": failures,
        "fts5_available": fts5_available,
        "agent_entrypoint": "index.sqlite",
        "auxiliary_indexes": ["symbols.json", "relations.jsonl", "tables.jsonl", "equations.jsonl"],
        "archive": {
            "raw_html": "source/html/",
            "parsed_pages": "parsed/pages/",
            "full_markdown": "parsed/full.md",
        },
    }
    (knowledge_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (knowledge_dir / "retrieval-policy.md").write_text(
        """# Agent 检索策略

1. 先读取 manifest.json，确认知识库版本和来源。
2. 先用 query-lexicon.json 拆解自然语言，得到 concepts、keywords 和 identifiers。
3. PHREEQC 关键词、-identifier 或中文术语优先查 symbols 表。
4. 简单查询优先精确标题/关键词；复杂查询使用核心概念的混合检索，不要求所有原词同时出现。
5. 自然语言解释使用 chunks_fts，按 type 过滤并优先返回 keyword、phreeqc_input、explanation、note。
6. 需要完整上下文时，根据 doc_id、parent_id 和 section_path 扩展到同一页面。
7. 需要可执行输入时只返回 type=phreeqc_input 且 input 非空的块。
8. 表格优先查 tables 表或 tables.jsonl；反应式、计算式优先查 equations 表或 equations.jsonl。
9. 示例选择优先查 examples.jsonl 的 simulation_types，再取对应 example 页的输入块。
10. 最终回答必须携带 source_url；不要把 full.md 作为默认上下文。

推荐查询顺序：query plan → symbol lookup → hybrid search → input/example filter → small-to-big context expansion → 原始 HTML 核验。
""",
        encoding="utf-8",
    )


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    argument_parser.add_argument("--refresh", action="store_true", help="replace the generated guide tree")
    argument_parser.add_argument("--reuse-source", action="store_true", help="reuse already downloaded HTML files")
    args = argument_parser.parse_args()

    root = args.root.resolve()
    guide_root = root / "docs" / "phreeqc-guide"
    source_dir = guide_root / "source" / "html"
    parsed_dir = guide_root / "parsed" / "pages"
    knowledge_dir = guide_root / "knowledge"
    if args.refresh and guide_root.exists():
        shutil.rmtree(guide_root)
    for directory in (
        source_dir,
        parsed_dir,
        knowledge_dir / "keywords",
        knowledge_dir / "concepts",
        knowledge_dir / "examples",
        knowledge_dir / "equations",
    ):
        directory.mkdir(parents=True, exist_ok=True)
    lexicon_source = root / "doctor" / "query-lexicon.json"
    lexicon_target = knowledge_dir / "query-lexicon.json"
    if lexicon_source.exists():
        shutil.copyfile(lexicon_source, lexicon_target)

    cached_homepage = source_dir / "phreeqc3.htm"
    if args.reuse_source and cached_homepage.exists():
        homepage_raw, homepage_type = cached_homepage.read_bytes(), ""
    else:
        homepage_raw, homepage_type = fetch(ENTRY_URL)
    homepage = decode_html(homepage_raw, homepage_type)
    urls = {ENTRY_URL}
    urls.update(local_html_links(homepage))
    urls.update(urljoin(BASE_URL, f"phreeqc3-{number}.htm") for number in range(1, 105))
    ordered_urls = sorted(urls, key=lambda item: (0 if item == ENTRY_URL else 1, item))

    records: List[Dict[str, object]] = []
    failures: List[Dict[str, str]] = []
    all_chunks: List[Dict[str, object]] = []
    keyword_terms: Dict[str, List[str]] = {}
    table_records: List[Dict[str, object]] = []
    for index, url in enumerate(ordered_urls, start=1):
        filename = Path(urlparse(url).path).name
        source_path = source_dir / filename
        try:
            if args.reuse_source and source_path.exists():
                raw, content_type = source_path.read_bytes(), ""
            else:
                raw, content_type = fetch(url)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failures.append({"url": url, "error": str(exc)})
            continue
        source_path.write_bytes(raw)
        source = decode_html(raw, content_type)
        html_tables = extract_tables(source)
        page_parser = GuideParser()
        page_parser.feed(source)
        page_parser.close()
        title = title_from_parser(source, page_parser, filename)
        if filename.lower() == "gas_binary_parameters.htm":
            title = "GAS_BINARY_PARAMETERS"
        markdown, headings = markdown_from_blocks(title, page_parser)
        heading_anchors = {}
        for kind, heading, anchor in page_parser.blocks:
            if kind.startswith("h") and anchor:
                normalized_heading = re.sub(r"\[\]\([^)]+\)", "", heading)
                normalized_heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", normalized_heading)
                heading_anchors.setdefault(normalized_heading.strip(), anchor)
        category = category_for(title, filename)
        stem = Path(filename).stem
        parsed_path = parsed_dir / f"{stem}.md"
        frontmatter = "\n".join([
            "---",
            f"title: {yaml_quote(title)}",
            f"source: {yaml_quote(url)}",
            f"source_file: {yaml_quote(filename)}",
            f"retrieved: {RETRIEVED}",
            f"category: {category}",
            "---",
            "",
        ])
        parsed_path.write_text(frontmatter + markdown, encoding="utf-8")
        record = {
            "id": stem,
            "title": title,
            "category": category,
            "source_file": filename,
            "source_url": url,
            "raw_path": str(source_path.relative_to(guide_root)).replace("\\", "/"),
            "markdown_path": str(parsed_path.relative_to(guide_root)).replace("\\", "/"),
            "headings": headings,
            "table_count": len(html_tables),
            "bytes": len(raw),
        }
        if category == "example":
            record["example_id"] = re.search(r"Example\s+(\d+)", title, re.I).group(1) if re.search(r"Example\s+(\d+)", title, re.I) else stem
            record["simulation_types"] = example_simulation_types(title, markdown)
        records.append(record)
        for table_number, rows in enumerate(html_tables, start=1):
            table_records.append({
                "id": f"{stem}::table-{table_number}",
                "doc_id": stem,
                "source_file": filename,
                "source_url": url,
                "rows": rows,
            })
        if category in {"keyword", "concept", "example"}:
            target_name = {"keyword": "keywords", "concept": "concepts", "example": "examples"}[category]
            target_dir = knowledge_dir / target_name
            knowledge_path = target_dir / f"{slugify(title)}.md"
            if category == "example":
                knowledge_path = target_dir / f"{stem}.md"
            knowledge_path.write_text(frontmatter + markdown, encoding="utf-8")
        if category == "keyword":
            keyword_terms.setdefault(title, []).append(str(parsed_path.relative_to(guide_root)).replace("\\", "/"))
        if category == "navigation":
            continue
        section_counts: Dict[str, int] = {}
        for position, (section_title, content, section_level) in enumerate(split_sections(markdown)):
            chunk_type = chunk_kind(section_title, content, category)
            normalized_code = input_from_section(content)
            if normalized_code:
                first_token = re.match(r"\s*([A-Z][A-Z0-9_]+)", normalized_code)
                if (
                    "input" in section_title.lower()
                    or "data block" in section_title.lower()
                    or (first_token and first_token.group(1) in set(keyword_terms) | PHREEQC_BLOCKS)
                ):
                    chunk_type = "phreeqc_input"
            chunk_base = f"{stem}::{slugify(section_title)}"
            section_counts[chunk_base] = section_counts.get(chunk_base, 0) + 1
            chunk_id = chunk_base if section_counts[chunk_base] == 1 else f"{chunk_base}-{section_counts[chunk_base]}"
            all_chunks.append({
                "id": chunk_id,
                "position": position,
                "type": chunk_type,
                "doc_id": stem,
                "parent_id": stem,
                "title": section_title,
                "keyword": title if category == "keyword" else None,
                "section_path": [title, section_title],
                "section_level": section_level,
                "content": content,
                "retrieval_text": " ".join(filter(None, [title, section_title, content])),
                "input": normalized_code,
                "identifiers": identifiers_from_text(content),
                "source_file": filename,
                "source_url": url,
                "source_anchor": heading_anchors.get(section_title),
                "page_path": str(parsed_path.relative_to(guide_root)).replace("\\", "/"),
                "retrieved": RETRIEVED,
            })
        if index % 20 == 0:
            print(f"Downloaded {index}/{len(ordered_urls)} pages", file=sys.stderr)

    records.sort(key=lambda item: str(item["source_file"]))
    (guide_root / "parsed" / "page-index.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (guide_root / "parsed" / "failures.json").write_text(json.dumps(failures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (knowledge_dir / "terms.json").write_text(json.dumps(keyword_terms, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    build_agent_indexes(guide_root, knowledge_dir, records, all_chunks, keyword_terms, failures, table_records)

    example_records = [
        record for record in records
        if record["category"] == "example" and str(record["source_file"]).startswith("phreeqc3-")
    ]
    equation_chunks = [chunk for chunk in all_chunks if chunk["type"] == "equation"]
    example_metadata = [
        {
            "example_id": record.get("example_id", record["id"]),
            "doc_id": record["id"],
            "title": record["title"],
            "source_file": record["source_file"],
            "source_url": record["source_url"],
            "simulation_types": record.get("simulation_types", []),
            "table_count": record.get("table_count", 0),
            "input_chunks": sum(1 for chunk in all_chunks if chunk["doc_id"] == record["id"] and chunk["type"] == "phreeqc_input"),
        }
        for record in example_records
    ]
    (knowledge_dir / "examples.jsonl").write_text(
        "".join(json.dumps(example, ensure_ascii=False) + "\n" for example in example_metadata),
        encoding="utf-8",
    )
    (knowledge_dir / "examples" / "index.md").write_text(
        "\n".join([
            "# 示例索引",
            "",
            "示例正文按官方来源页保存在 ../parsed/pages/，完整示例页副本保存在本目录。",
            "",
        ] + [
            f"- [{record['title']}]({(Path('..') / '..' / str(record['markdown_path'])).as_posix()}) — {record['source_file']}"
            for record in example_records
        ]) + "\n",
        encoding="utf-8",
    )
    (knowledge_dir / "equations" / "index.md").write_text(
        "\n".join([
            "# 公式与方程索引",
            "",
            "公式章节通过章节记录保留；原始 Markdown 位于 ../parsed/pages/。",
            "",
        ] + [
            f"- [{chunk['title']}]({(Path('..') / '..' / chunk['page_path']).as_posix()}) — {chunk['source_file']}"
            for chunk in equation_chunks
        ]) + "\n",
        encoding="utf-8",
    )
    (knowledge_dir / "README.md").write_text(
        "\n".join([
            "# PHREEQC 知识层",
            "",
            "本目录面向后续 Agent 检索，原始来源与逐页解析结果见上级目录。",
            "",
            "- chunks.jsonl：章节级 JSONL 记录，字段包括 type、keyword、content 和 source_url。",
            "- terms.json：关键词到来源页的符号映射。",
            "- symbols.json：关键词、-identifier 和中文别名的精确查找表。",
            "- query-lexicon.json：自然语言概念到 PHREEQC 关键词和 identifier 的查询映射。",
            "- index.sqlite：Agent 默认入口，包含 documents、chunks、symbols、relations 和 chunks_fts。",
            "- relations.jsonl：关键词之间的 related_to 关系。",
            "- tables.jsonl：从官方 HTML 表格抽取的行列数据；SQLite 中对应 tables 表。",
            "- equations.jsonl：从章节和输入块抽取的反应式/计算式；SQLite 中对应 equations 表。",
            "- examples.jsonl：示例编号、模拟类型、表格数和可执行输入块数。",
            "- benchmark-latest.json：最近一次检索准确性、覆盖率和延迟评测结果。",
            "- benchmark-advanced-latest.json：复杂查询和答案级覆盖评测结果。",
            "- 高级基准可用 `python doctor/benchmark_advanced_retrieval.py --check` 执行回归门禁。",
            "- manifest.json：知识库版本、统计和来源清单。",
            "- retrieval-policy.md：Agent 检索和上下文扩展规则。",
            "- keywords/：关键词数据块。",
            "- concepts/：概念、计算流程和附录。",
            "- examples/：示例页及示例章节索引。",
            "- equations/：公式章节索引。",
            "",
            "Agent 查询入口：python doctor/query_phreeqc_guide.py --symbol SOLUTION；也可使用 --search、--input、--related、--context 和 --examples。",
            "",
        ]) + "\n",
        encoding="utf-8",
    )

    full_lines = [
        "# PHREEQC Version 3 HTML User's Guide",
        "",
        f"> Canonical source: {ENTRY_URL}",
        f"> Retrieved: {RETRIEVED}",
        "",
    ]
    for record in records:
        page_path = guide_root / str(record["markdown_path"])
        full_lines.append(page_path.read_text(encoding="utf-8"))
        full_lines.append("\n---\n")
    (guide_root / "parsed" / "full.md").write_text("\n".join(full_lines), encoding="utf-8")

    index_lines = [
        "# PHREEQC Version 3 HTML User's Guide",
        "",
        f"本目录由 [USGS 官方 HTML 手册]({ENTRY_URL}) 自动整理生成，抓取日期为 {RETRIEVED}。",
        "",
        "## 知识层布局",
        "",
        "- source/html/：官方 HTML 原文，作为可追溯源文件。",
        "- parsed/pages/：逐页 Markdown，保留原章节、输入示例和说明。",
        "- parsed/full.md：按官方页序合并的完整 Markdown。",
        "- knowledge/keywords/：按 PHREEQC 关键词组织的可直接检索文档。",
        "- knowledge/concepts/：介绍、计算类型、模型和附录等概念文档。",
        "- knowledge/examples/：示例章节索引；示例正文按来源页保存在 parsed/pages/。",
        "- knowledge/equations/：公式相关章节索引；原始内容保留在对应页。",
        "- knowledge/chunks.jsonl：按章节切分的结构化记录，供 FTS/Embedding 索引使用。",
        "- knowledge/terms.json：关键词到来源页的符号映射。",
        "",
        f"共整理 {len(records)} 个页面，生成 {len(all_chunks)} 个章节记录。失败页面记录在 parsed/failures.json。",
        "",
        "## 页面索引",
        "",
        "| 类别 | 页面 | 原始 HTML | Markdown |",
        "|---|---|---|---|",
    ]
    for record in records:
        title = str(record["title"]).replace("|", "\\|")
        page = str(record["markdown_path"])
        raw = str(record["raw_path"])
        index_lines.append(f"| {record['category']} | {title} | [{record['source_file']}]({raw}) | [打开](parsed/pages/{Path(page).name}) |")
    (guide_root / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    source_readme = "\n".join([
        "# 官方来源",
        "",
        f"- 入口：[{ENTRY_URL}]({ENTRY_URL})",
        f"- 抓取日期：{RETRIEVED}",
        "- 抓取范围：入口页、官方目录列出的 HTML 页面，以及 phreeqc3-1.htm 到 phreeqc3-104.htm。",
        "- 原始文件：本目录中的 .htm 文件未做内容改写；解析结果见上级 parsed/。",
        "",
        "USGS 官方页面是本知识层的唯一原始来源。官方目录中的旧 examples.htm 链接当前返回 404，但示例正文已由 phreeqc3-63.htm 到 phreeqc3-84.htm 完整收录。若要刷新内容，请运行项目根目录下的 doctor/import_phreeqc_guide.py --refresh，并检查 parsed/failures.json。",
        "",
    ])
    (guide_root / "source" / "README.md").write_text(source_readme, encoding="utf-8")

    print(f"Imported {len(records)} pages and {len(all_chunks)} chunks into {guide_root}")
    if failures:
        print(f"Warnings: {len(failures)} source pages failed; see parsed/failures.json", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
