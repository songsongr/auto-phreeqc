#!/usr/bin/env python3
"""Query the generated PHREEQC guide index for agents and shell workflows.

Examples:
  python doctor/query_phreeqc_guide.py --symbol SOLUTION
  python doctor/query_phreeqc_guide.py --search "surface complexation" --type explanation
  python doctor/query_phreeqc_guide.py --input "GAS_PHASE" --limit 5
  python doctor/query_phreeqc_guide.py --context gas_phase::example-data-block
  python doctor/query_phreeqc_guide.py --examples --simulation-type transport
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set


def database_path(root: Path) -> Path:
    return root / "docs" / "phreeqc-guide" / "knowledge" / "index.sqlite"


def lexicon_path(root: Path) -> Path:
    source = root / "doctor" / "query-lexicon.json"
    return source if source.exists() else root / "docs" / "phreeqc-guide" / "knowledge" / "query-lexicon.json"


def load_lexicon(root: Path) -> Dict[str, Dict[str, List[str]]]:
    path = lexicon_path(root)
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def build_query_plan(query: str, lexicon: Optional[Dict[str, Dict[str, List[str]]]] = None) -> Dict[str, List[str]]:
    text = query.strip()
    folded = text.casefold()
    plan: Dict[str, Set[str]] = {"concepts": set(), "keywords": set(), "identifiers": set(), "aliases": set()}
    for concept, entry in (lexicon or {}).items():
        aliases = [concept] + list(entry.get("aliases", []))
        if any(alias.casefold() in folded for alias in aliases):
            plan["concepts"].add(concept)
            plan["aliases"].update(aliases)
            plan["keywords"].update(entry.get("keywords", []))
            plan["identifiers"].update(entry.get("identifiers", []))
    plan["identifiers"].update(re.findall(r"(?<![\w-])-[a-z][a-z0-9_]*(?![\w-])", text, re.I))
    plan["keywords"].update(re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text))
    return {key: sorted(value) for key, value in plan.items()}


def source_link(row: Dict[str, Any]) -> str:
    url = str(row.get("source_url", ""))
    anchor = row.get("source_anchor")
    return f"{url}#{anchor}" if anchor else url


def decode_chunk(row: sqlite3.Row) -> Dict[str, Any]:
    item = dict(row)
    if isinstance(item.get("section_path"), str):
        try:
            item["section_path"] = json.loads(item["section_path"])
        except json.JSONDecodeError:
            pass
    for field in ("identifiers", "keywords"):
        if isinstance(item.get(field), str):
            try:
                item[field] = json.loads(item[field])
            except json.JSONDecodeError:
                pass
    item["source"] = source_link(item)
    return item


def fts_expression(query: str, mode: str = "and", extra_terms: Optional[List[str]] = None) -> str:
    raw_terms = re.findall(r"[\w+$-]+", query, re.UNICODE)
    for extra in extra_terms or []:
        raw_terms.extend(re.findall(r"[\w+$-]+", extra, re.UNICODE))
    terms = list(dict.fromkeys(raw_terms))
    if not terms:
        return ""
    joiner = " OR " if mode == "or" else " AND "
    expression = joiner.join('"' + term.replace('"', '""') + '"*' for term in terms)
    canonical = re.sub(r"\s+", "_", query.strip())
    if canonical and canonical.casefold() != query.strip().casefold() and re.fullmatch(r"[\w+$-]+", canonical, re.UNICODE):
        expression = f"({expression} OR \"{canonical.replace(chr(34), chr(34) * 2)}\"*)"
    return expression


def symbol_lookup(connection: sqlite3.Connection, query: str, limit: int) -> List[Dict[str, Any]]:
    normalized = query.strip().casefold()
    matches = []
    for row in connection.execute("SELECT * FROM symbols ORDER BY symbol"):
        aliases = json.loads(row["aliases"])
        symbol_normalized = str(row["symbol"]).casefold()
        alias_normalized = {str(alias).casefold() for alias in aliases}
        if normalized == symbol_normalized:
            rank = 0
        elif normalized in alias_normalized:
            rank = 1
        else:
            continue
        if normalized in {symbol_normalized, *alias_normalized}:
            item = dict(row)
            item["aliases"] = aliases
            item["identifiers"] = json.loads(row["identifiers"])
            item["source_pages"] = json.loads(row["source_pages"])
            item["source_urls"] = json.loads(row["source_urls"])
            matches.append((rank, item))
    matches.sort(key=lambda pair: (pair[0], str(pair[1]["symbol"])))
    return [item for _, item in matches[:limit]]


def search_chunks(
    connection: sqlite3.Connection,
    query: str,
    limit: int,
    chunk_type: Optional[str] = None,
    input_only: bool = False,
    lexicon: Optional[Dict[str, Dict[str, List[str]]]] = None,
    query_plan: Optional[Dict[str, List[str]]] = None,
) -> List[Dict[str, Any]]:
    original_plan = query_plan or build_query_plan(query, lexicon)
    plan = {key: list(values) for key, values in original_plan.items()}
    explicit_keywords = set(plan.get("keywords", []))
    related_keywords: Set[str] = set(explicit_keywords)
    if explicit_keywords:
        placeholders = ",".join("?" for _ in explicit_keywords)
        for row in connection.execute(
            f"SELECT target FROM relations WHERE source IN ({placeholders})",
            sorted(explicit_keywords),
        ):
            related_keywords.add(str(row[0]))
    plan["related_keywords"] = sorted(related_keywords - explicit_keywords)
    conditions = []
    filter_params: List[Any] = []
    if input_only:
        conditions.append("c.type = 'phreeqc_input'")
        conditions.append("c.input IS NOT NULL")
    if chunk_type:
        conditions.append("c.type = ?")
        filter_params.append(chunk_type)
    where = " AND ".join(conditions)
    candidate_limit = max(20, limit * 4)
    candidates: Dict[str, Dict[str, Any]] = {}

    def add_rows(rows: Iterable[sqlite3.Row]) -> None:
        for row in rows:
            item = decode_chunk(row)
            candidates[item["chunk_id"]] = item

    focused_terms = plan.get("concepts", []) + sorted(explicit_keywords)
    query_terms = list(dict.fromkeys(focused_terms or [query]))
    strict_expression = fts_expression(query, mode="and")
    if len(re.findall(r"[\w+$-]+", query, re.UNICODE)) <= 2:
        expressions = [strict_expression]
    else:
        # Complex queries use one strict pass plus one focused OR candidate
        # pass. Identifiers are resolved through the exact lookup below, and
        # ranking still rewards multiple concept/keyword hits.
        expressions = [strict_expression, fts_expression(" ".join(query_terms), mode="or")]
    for expression in expressions:
        if not expression:
            continue
        sql = """
            SELECT c.* FROM chunks c
            JOIN chunks_fts f ON f.chunk_id = c.chunk_id
            WHERE f.chunks_fts MATCH ?
        """
        params: List[Any] = [expression] + filter_params
        if where:
            sql += " AND " + where
        sql += " LIMIT ?"
        params.append(candidate_limit)
        try:
            add_rows(connection.execute(sql, params))
        except sqlite3.OperationalError:
            continue

    lookup_keywords = sorted(related_keywords)
    lookup_identifiers = sorted(set(plan.get("identifiers", [])))
    if lookup_keywords or lookup_identifiers:
        lookup_conditions = []
        lookup_params: List[Any] = []
        for term in lookup_keywords:
            lookup_conditions.append("upper(coalesce(c.keyword, '')) = upper(?)")
            lookup_params.append(term)
        for term in lookup_identifiers:
            lookup_conditions.append("lower(coalesce(c.input, '')) LIKE lower(?)")
            lookup_params.append(f"%{term}%")
        sql = "SELECT c.* FROM chunks c WHERE (" + " OR ".join(lookup_conditions) + ")"
        if where:
            sql += " AND " + where
        sql += " LIMIT ?"
        try:
            add_rows(connection.execute(sql, lookup_params + filter_params + [candidate_limit]))
        except sqlite3.OperationalError:
            pass

    if not candidates:
        raw_terms = list(dict.fromkeys(re.findall(r"[\w+$-]+", query, re.UNICODE)))
        like_conditions = []
        like_params: List[Any] = []
        for term in raw_terms:
            like_conditions.extend(["lower(c.title) LIKE lower(?)", "lower(c.content) LIKE lower(?)"])
            like_params.extend([f"%{term}%", f"%{term}%"])
        if not like_conditions:
            return []
        sql = "SELECT c.* FROM chunks c WHERE (" + " OR ".join(like_conditions) + ")"
        if where:
            sql += " AND " + where
        sql += " LIMIT ?"
        add_rows(connection.execute(sql, like_params + filter_params + [candidate_limit]))

    query_folded = query.casefold()
    query_terms_folded = [term.casefold() for term in re.findall(r"[\w+$-]+", query, re.UNICODE)]
    plan_terms_folded = [term.casefold() for term in query_terms]
    keyword_set = {value.casefold() for value in explicit_keywords}
    identifier_set = {value.casefold() for value in plan.get("identifiers", [])}
    alias_set = {value.casefold() for value in plan.get("aliases", [])}
    doc_categories = {
        str(row["doc_id"]): str(row["category"])
        for row in connection.execute("SELECT doc_id, category FROM documents")
    }
    type_weight = {
        "phreeqc_input": 55,
        "keyword": 30,
        "explanation": 20,
        "note": 14,
        "concept": 16,
        "tutorial": 12,
        "related_keywords": 8,
    }

    ranked = []
    for item in candidates.values():
        title = str(item.get("title") or "")
        keyword = str(item.get("keyword") or "")
        content = str(item.get("content") or "")
        input_text = str(item.get("input") or "")
        blob = " ".join([title, keyword, content, input_text]).casefold()
        normalized_title = title.replace("_", " ").casefold()
        normalized_keyword = keyword.replace("_", " ").casefold()
        score = float(type_weight.get(str(item.get("type")), 0))
        category = doc_categories.get(str(item.get("doc_id")), "")
        if category == "example" and any(
            concept in {"kinetics", "rate equation", "surface complexation", "transport", "inverse modeling", "gas phase"}
            for concept in plan.get("concepts", [])
        ):
            score += 28
        if query_folded in normalized_title or query_folded in normalized_keyword:
            score += 120
        if query_folded in blob:
            score += 30
        if normalized_title == query_folded or normalized_keyword == query_folded:
            score += 80
        for term in keyword_set:
            if term == keyword.casefold():
                score += 110
            elif term in keyword.casefold():
                score += 25
            elif term in blob:
                score += 25
        for identifier in identifier_set:
            if identifier in input_text.casefold():
                score += 160
            elif identifier in content.casefold():
                score += 105
        for alias in alias_set:
            if len(alias) >= 4 and alias in blob:
                score += 12
        score += sum(18 for term in query_terms_folded if term in blob)
        score += sum(16 for term in plan_terms_folded if term in blob)
        if input_only and input_text:
            score += 60
        ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], str(pair[1]["doc_id"]), int(pair[1].get("position", 0))))

    results = []
    per_doc: Dict[str, int] = {}
    max_per_doc = 3 if input_only else 2
    for _, item in ranked:
        doc_id = str(item["doc_id"])
        if per_doc.get(doc_id, 0) >= max_per_doc:
            continue
        results.append(item)
        per_doc[doc_id] = per_doc.get(doc_id, 0) + 1
        if len(results) >= limit:
            break
    return results


def context_chunks(connection: sqlite3.Connection, chunk_id: str, radius: int) -> List[Dict[str, Any]]:
    target = connection.execute("SELECT doc_id, position FROM chunks WHERE chunk_id = ?", (chunk_id,)).fetchone()
    if target is None:
        return []
    rows = connection.execute(
        """
        SELECT * FROM chunks
        WHERE doc_id = ? AND position BETWEEN ? AND ?
        ORDER BY position
        """,
        (target["doc_id"], max(0, target["position"] - radius), target["position"] + radius),
    )
    return [decode_chunk(row) for row in rows]


def related(connection: sqlite3.Connection, symbol: str, limit: int) -> List[Dict[str, Any]]:
    rows = connection.execute(
        "SELECT source, relation, target, source_url FROM relations WHERE source = ? OR target = ? LIMIT ?",
        (symbol.upper(), symbol.upper(), limit),
    )
    return [dict(row) for row in rows]


def examples(root: Path, simulation_type: Optional[str], limit: int) -> List[Dict[str, Any]]:
    path = root / "docs" / "phreeqc-guide" / "knowledge" / "examples.jsonl"
    if not path.exists():
        return []
    result = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if simulation_type and simulation_type.casefold() not in {str(value).casefold() for value in item.get("simulation_types", [])}:
            continue
        result.append(item)
        if len(result) >= limit:
            break
    return result


def render_text(payload: Dict[str, Any]) -> str:
    lines = []
    for result in payload.get("results", []):
        if "content" in result:
            lines.append(f"[{result.get('type')}] {result.get('chunk_id') or result.get('id')}")
            lines.append(str(result.get("source", result.get("source_url", ""))))
            lines.append(str(result.get("content", ""))[:600])
        elif "symbol" in result:
            lines.append(f"{result['symbol']}: {', '.join(result.get('aliases', []))}")
        else:
            lines.append(json.dumps(result, ensure_ascii=False))
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--symbol")
    modes.add_argument("--search")
    modes.add_argument("--input")
    modes.add_argument("--related")
    modes.add_argument("--context")
    modes.add_argument("--examples", action="store_true")
    parser.add_argument("--type", dest="chunk_type")
    parser.add_argument("--simulation-type")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()
    root = args.root.resolve()
    lexicon = load_lexicon(root)
    query_args = dict(vars(args))
    query_args["root"] = str(query_args["root"])
    payload: Dict[str, Any] = {"query": query_args, "results": []}
    if args.examples:
        payload["results"] = examples(root, args.simulation_type, args.limit)
    else:
        db_path = database_path(root)
        if not db_path.exists():
            parser.error(f"index not found: {db_path}")
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        try:
            if args.symbol:
                payload["results"] = symbol_lookup(connection, args.symbol, args.limit)
            elif args.search:
                payload["query_plan"] = build_query_plan(args.search, lexicon)
                payload["results"] = search_chunks(connection, args.search, args.limit, args.chunk_type, lexicon=lexicon)
            elif args.input:
                payload["query_plan"] = build_query_plan(args.input, lexicon)
                payload["results"] = search_chunks(connection, args.input, args.limit, args.chunk_type, input_only=True, lexicon=lexicon)
            elif args.related:
                payload["results"] = related(connection, args.related, args.limit)
            elif args.context:
                payload["results"] = context_chunks(connection, args.context, args.radius)
        finally:
            connection.close()
    if args.format == "text":
        print(render_text(payload))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
