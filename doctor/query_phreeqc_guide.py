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
from typing import Any, Dict, Iterable, List, Optional


def database_path(root: Path) -> Path:
    return root / "docs" / "phreeqc-guide" / "knowledge" / "index.sqlite"


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


def fts_expression(query: str) -> str:
    terms = re.findall(r"[\w+$-]+", query, re.UNICODE)
    if not terms:
        return ""
    expression = " AND ".join('"' + term.replace('"', '""') + '"*' for term in terms)
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
) -> List[Dict[str, Any]]:
    expression = fts_expression(query)
    conditions = []
    params: List[Any] = []
    if input_only:
        conditions.append("c.type = 'phreeqc_input'")
        conditions.append("c.input IS NOT NULL")
    if chunk_type:
        conditions.append("c.type = ?")
        params.append(chunk_type)
    where = " AND ".join(conditions)
    if expression:
        sql = """
            SELECT c.* FROM chunks c
            JOIN chunks_fts f ON f.chunk_id = c.chunk_id
            WHERE f.chunks_fts MATCH ?
        """
        params = [expression] + params
        if where:
            sql += " AND " + where
        query_like = f"%{query}%"
        canonical_like = f"%{query.replace(' ', '_')}%"
        sql += """
            ORDER BY
                CASE
                    WHEN lower(c.title) = lower(?) OR lower(coalesce(c.keyword, '')) = lower(?)
                      OR lower(c.title) = lower(?) OR lower(coalesce(c.keyword, '')) = lower(?) THEN 0
                    WHEN lower(c.title) LIKE lower(?) OR lower(coalesce(c.keyword, '')) LIKE lower(?)
                      OR lower(c.title) LIKE lower(?) OR lower(coalesce(c.keyword, '')) LIKE lower(?) THEN 1
                    ELSE 2
                END,
                bm25(chunks_fts, 10.0, 5.0, 1.0, 1.0, 3.0),
                c.doc_id, c.position
            LIMIT ?
        """
        params.extend([
            query, query, query.replace(" ", "_"), query.replace(" ", "_"),
            query_like, query_like, canonical_like, canonical_like, limit,
        ])
        try:
            matches = [decode_chunk(row) for row in connection.execute(sql, params)]
            if matches:
                return matches
        except sqlite3.OperationalError:
            pass
    like = f"%{query}%"
    sql = "SELECT c.* FROM chunks c WHERE (c.title LIKE ? OR c.content LIKE ? OR c.retrieval_text LIKE ?)"
    params = [like, like, like]
    if where:
        sql += " AND " + where
    sql += " ORDER BY c.doc_id, c.position LIMIT ?"
    params.append(limit)
    return [decode_chunk(row) for row in connection.execute(sql, params)]


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
                payload["results"] = search_chunks(connection, args.search, args.limit, args.chunk_type)
            elif args.input:
                payload["results"] = search_chunks(connection, args.input, args.limit, args.chunk_type, input_only=True)
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
