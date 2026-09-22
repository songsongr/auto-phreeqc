#!/usr/bin/env python3
"""Evaluate retrieval quality and latency for the generated PHREEQC guide index."""

from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from query_phreeqc_guide import context_chunks, examples, load_lexicon, search_chunks, symbol_lookup


SYMBOL_CASES = [
    ("SOLUTION", "SOLUTION"),
    ("溶液", "SOLUTION"),
    ("-pH", "-pH"),
    ("GAS_PHASE", "GAS_PHASE"),
    ("表面络合", "SURFACE"),
]

SEARCH_CASES = [
    ("surface complexation", {"phreeqc3-2", "phreeqc3-70", "phreeqc3-76"}),
    ("inverse modeling", {"phreeqc3-2", "phreeqc3-4", "phreeqc3-20", "phreeqc3-78", "phreeqc3-79", "phreeqc3-80"}),
    ("gas phase", {"phreeqc3-5", "phreeqc3-17", "phreeqc3-30", "phreeqc3-69", "phreeqc3-84", "phreeqc3-91"}),
    ("activity coefficient", {"phreeqc3-2", "phreeqc3-16", "phreeqc3-26", "phreeqc3-37", "mean_gammas"}),
]

INPUT_CASES = [
    ("GAS_PHASE", "GAS_PHASE"),
    ("TRANSPORT", "TRANSPORT"),
    ("-punch_cells", "-punch_cells"),
    ("SURFACE", "SURFACE"),
]

EXAMPLE_CASES = ["transport", "inverse_modeling", "kinetics", "surface_complexation", "gas_phase"]
CONTEXT_CASES = [
    ("phreeqc3-17::example-data-block-1", "phreeqc3-17"),
    ("phreeqc3-63::example-1-speciation-calculation", "phreeqc3-63"),
]


def latency_call(function, *args, **kwargs):
    started = time.perf_counter()
    result = function(*args, **kwargs)
    return result, (time.perf_counter() - started) * 1000


def summarize_latencies(values: List[float]) -> Dict[str, float]:
    if not values:
        return {"count": 0, "mean_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "max_ms": 0.0}
    ordered = sorted(values)
    return {
        "count": len(values),
        "mean_ms": round(statistics.mean(values), 3),
        "p50_ms": round(statistics.median(values), 3),
        "p95_ms": round(ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))], 3),
        "max_ms": round(max(values), 3),
    }


def run(root: Path, limit: int) -> Dict[str, Any]:
    db_path = root / "docs" / "phreeqc-guide" / "knowledge" / "index.sqlite"
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    lexicon = load_lexicon(root)
    latencies: List[float] = []
    report: Dict[str, Any] = {"database": str(db_path), "limit": limit}
    try:
        symbol_results = []
        for query, expected in SYMBOL_CASES:
            result, elapsed = latency_call(symbol_lookup, connection, query, limit)
            latencies.append(elapsed)
            symbol_results.append({
                "query": query,
                "expected": expected,
                "top": result[0]["symbol"] if result else None,
                "hit": bool(result and result[0]["symbol"] == expected),
                "returned": [item["symbol"] for item in result],
                "latency_ms": round(elapsed, 3),
            })
        report["symbol"] = {
            "top1_accuracy": round(sum(item["hit"] for item in symbol_results) / len(symbol_results), 3),
            "cases": symbol_results,
        }

        search_results = []
        for query, expected_docs in SEARCH_CASES:
            result, elapsed = latency_call(search_chunks, connection, query, limit, lexicon=lexicon)
            latencies.append(elapsed)
            returned_doc_list = list(dict.fromkeys(item["doc_id"] for item in result))
            returned_docs = set(returned_doc_list)
            relevant = returned_docs & expected_docs
            search_results.append({
                "query": query,
                "expected_docs": sorted(expected_docs),
                "returned_docs": returned_doc_list,
                "hit": bool(relevant),
                "precision_at_k": round(len(relevant) / max(1, len(returned_doc_list)), 3),
                "recall_at_k": round(len(relevant) / len(expected_docs), 3),
                "latency_ms": round(elapsed, 3),
            })
        report["search"] = {
            "hit_rate": round(sum(item["hit"] for item in search_results) / len(search_results), 3),
            "mean_precision_at_k": round(statistics.mean(item["precision_at_k"] for item in search_results), 3),
            "mean_recall_at_k": round(statistics.mean(item["recall_at_k"] for item in search_results), 3),
            "cases": search_results,
        }

        input_results = []
        for query, expected in INPUT_CASES:
            result, elapsed = latency_call(search_chunks, connection, query, limit, input_only=True, lexicon=lexicon)
            latencies.append(elapsed)
            matched = [
                item for item in result
                if expected.casefold() in str(item.get("input") or "").casefold()
                or expected.casefold() in str(item.get("identifiers") or "").casefold()
            ]
            input_results.append({
                "query": query,
                "expected": expected,
                "returned": [item["chunk_id"] for item in result],
                "hit": bool(matched),
                "latency_ms": round(elapsed, 3),
            })
        report["input"] = {
            "hit_rate": round(sum(item["hit"] for item in input_results) / len(input_results), 3),
            "cases": input_results,
        }

        example_results = []
        for simulation_type in EXAMPLE_CASES:
            result, elapsed = latency_call(examples, root, simulation_type, limit)
            latencies.append(elapsed)
            example_results.append({
                "simulation_type": simulation_type,
                "count": len(result),
                "all_tagged_correctly": all(simulation_type in item.get("simulation_types", []) for item in result),
                "examples": [item["example_id"] for item in result],
                "latency_ms": round(elapsed, 3),
            })
        report["examples"] = {"cases": example_results}

        context_results = []
        for chunk_id, expected_doc in CONTEXT_CASES:
            result, elapsed = latency_call(context_chunks, connection, chunk_id, 1)
            latencies.append(elapsed)
            context_results.append({
                "chunk_id": chunk_id,
                "expected_doc": expected_doc,
                "returned": [item["chunk_id"] for item in result],
                "target_present": any(item["chunk_id"] == chunk_id for item in result),
                "same_doc": bool(result) and all(item["doc_id"] == expected_doc for item in result),
                "latency_ms": round(elapsed, 3),
            })
        report["context"] = {"cases": context_results}
    finally:
        connection.close()
    report["latency_ms"] = summarize_latencies(latencies)
    return report


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args()
    report = run(args.root.resolve(), args.limit)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
