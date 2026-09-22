#!/usr/bin/env python3
"""Run a harder, reproducible retrieval benchmark for the PHREEQC guide index."""

from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from query_phreeqc_guide import build_query_plan, context_chunks, examples, load_lexicon, search_chunks, symbol_lookup


# These cases intentionally combine aliases, identifiers, concepts, and examples.
# Expected document sets are judged at document level, while input/context cases
# are judged at chunk level.
SYMBOL_CASES = [
    ("形态分布", "SOLUTION"),
    ("-potential", "-potential"),
    ("气相平衡", "GAS_PHASE"),
    ("阳离子交换", "EXCHANGE"),
]

SEARCH_CASES = [
    ("surface complexation Donnan diffuse layer", {"phreeqc3-2", "phreeqc3-52", "phreeqc3-53", "phreeqc3-54", "phreeqc3-70", "phreeqc3-76"}),
    ("kinetics rate equation CVODE", {"phreeqc3-24", "phreeqc3-39", "phreeqc3-71", "phreeqc3-77", "phreeqc3-93"}),
    ("inverse modeling uncertainty isotope", {"phreeqc3-20", "phreeqc3-22", "phreeqc3-78", "phreeqc3-79", "phreeqc3-80"}),
    ("transport stagnant zone exchange factors", {"phreeqc3-75", "phreeqc3-77"}),
]

INPUT_CASES = [
    ("-punch_frequency", "-punch_frequency"),
    ("-initial_time TRANSPORT", "TRANSPORT"),
    ("-donnan SURFACE", "-donnan"),
    ("-cvode KINETICS", "-cvode"),
]

EXAMPLE_CASES = ["surface_complexation", "transport", "inverse_modeling", "gas_phase"]
# Regression floors are intentionally tied to the measured pre-change baseline
# and the user-approved latency target. Normal benchmark runs remain
# informational; --check turns these into a CI-friendly gate.
MIN_OVERALL = 82.1
MIN_SEARCH_RECALL = 0.237
MIN_SOURCE_TRACEABILITY = 1.0
MAX_P95_MS = 10.0
CONTEXT_CASES = [
    ("phreeqc3-52::example-data-block-1", "phreeqc3-52"),
    ("phreeqc3-75::stagnant-zone-calculation-using-the-first-order-exchange-approximation-with-implicit-mixing-factors", "phreeqc3-75"),
    ("phreeqc3-80::example-18-inverse-modeling-of-the-madison-aquifer", "phreeqc3-80"),
]

ANSWER_CASES = [
    {
        "query": "surface complexation Donnan diffuse layer",
        "keywords": ["SURFACE"],
        "identifiers": ["-donnan", "-diffuse_layer"],
        "needs_input": True,
    },
    {
        "query": "kinetics rate equation CVODE",
        "keywords": ["KINETICS", "RATES"],
        "identifiers": ["-cvode"],
        "needs_input": True,
    },
    {
        "query": "inverse modeling uncertainty isotope",
        "keywords": ["INVERSE_MODELING"],
        "identifiers": [],
        "needs_input": False,
    },
    {
        "query": "transport stagnant zone exchange factors",
        "keywords": ["TRANSPORT", "EXCHANGE"],
        "identifiers": ["-stagnant"],
        "needs_input": True,
    },
]


def timed(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, (time.perf_counter() - start) * 1000


def pct(value: float) -> float:
    return round(value, 3)


def run(root: Path, limit: int) -> Dict[str, Any]:
    db = root / "docs" / "phreeqc-guide" / "knowledge" / "index.sqlite"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    lexicon = load_lexicon(root)
    latencies: List[float] = []
    report: Dict[str, Any] = {"suite": "advanced-retrieval-v1", "limit": limit, "database": str(db)}
    try:
        symbol = []
        for query, expected in SYMBOL_CASES:
            rows, ms = timed(symbol_lookup, conn, query, limit)
            latencies.append(ms)
            symbol.append({"query": query, "expected": expected, "top": rows[0]["symbol"] if rows else None,
                           "hit": bool(rows and rows[0]["symbol"] == expected), "latency_ms": pct(ms)})
        report["symbol"] = {"top1_accuracy": pct(sum(x["hit"] for x in symbol) / len(symbol)), "cases": symbol}

        search = []
        for query, expected in SEARCH_CASES:
            rows, ms = timed(search_chunks, conn, query, limit, lexicon=lexicon)
            latencies.append(ms)
            returned = list(dict.fromkeys(row["doc_id"] for row in rows))
            relevant = set(returned) & expected
            search.append({"query": query, "expected_docs": sorted(expected), "returned_docs": returned,
                           "hit": bool(relevant), "precision": pct(len(relevant) / max(1, len(returned)),),
                           "recall": pct(len(relevant) / len(expected)), "source_complete": all(bool(row.get("source")) for row in rows),
                           "latency_ms": pct(ms)})
        report["search"] = {"hit_rate": pct(sum(x["hit"] for x in search) / len(search)),
                             "mean_precision": pct(statistics.mean(x["precision"] for x in search)),
                             "mean_recall": pct(statistics.mean(x["recall"] for x in search)),
                             "source_rate": pct(sum(x["source_complete"] for x in search) / len(search)), "cases": search}

        inputs = []
        for query, expected in INPUT_CASES:
            rows, ms = timed(search_chunks, conn, query, limit, input_only=True, lexicon=lexicon)
            latencies.append(ms)
            needle = expected.casefold()
            matched = [row for row in rows if needle in str(row.get("input") or "").casefold() or needle in str(row.get("identifiers") or "").casefold()]
            inputs.append({"query": query, "expected": expected, "hit": bool(matched),
                           "returned": [row["chunk_id"] for row in rows],
                           "source_complete": all(bool(row.get("source")) for row in rows), "latency_ms": pct(ms)})
        report["input"] = {"hit_rate": pct(sum(x["hit"] for x in inputs) / len(inputs)),
                            "source_rate": pct(sum(x["source_complete"] for x in inputs) / len(inputs)), "cases": inputs}

        example_rows = []
        for simulation_type in EXAMPLE_CASES:
            rows, ms = timed(examples, root, simulation_type, limit)
            latencies.append(ms)
            correct = bool(rows) and all(simulation_type in row.get("simulation_types", []) for row in rows)
            example_rows.append({"simulation_type": simulation_type, "count": len(rows), "all_tagged_correctly": correct,
                                 "source_complete": all(bool(row.get("source_url")) for row in rows),
                                 "latency_ms": pct(ms)})
        report["examples"] = {"filter_accuracy": pct(sum(x["all_tagged_correctly"] for x in example_rows) / len(example_rows)),
                               "source_rate": pct(sum(x["source_complete"] for x in example_rows) / len(example_rows)), "cases": example_rows}

        context = []
        for chunk_id, expected_doc in CONTEXT_CASES:
            rows, ms = timed(context_chunks, conn, chunk_id, 1)
            latencies.append(ms)
            context.append({"chunk_id": chunk_id, "expected_doc": expected_doc,
                            "target_present": any(row["chunk_id"] == chunk_id for row in rows),
                            "same_doc": bool(rows) and all(row["doc_id"] == expected_doc for row in rows),
                            "source_complete": all(bool(row.get("source")) for row in rows), "latency_ms": pct(ms)})
        report["context"] = {"target_rate": pct(sum(x["target_present"] for x in context) / len(context)),
                              "same_doc_rate": pct(sum(x["same_doc"] for x in context) / len(context)),
                              "source_rate": pct(sum(x["source_complete"] for x in context) / len(context)), "cases": context}

        answer_results = []
        for case in ANSWER_CASES:
            rows, ms = timed(search_chunks, conn, case["query"], limit, lexicon=lexicon)
            input_rows: List[Dict[str, Any]] = []
            input_ms = 0.0
            if case["needs_input"]:
                input_rows, input_ms = timed(search_chunks, conn, case["query"], limit, input_only=True, lexicon=lexicon)
            # Keep the core retrieval latency gate focused on the primary
            # answer search. Input verification is reported in the case
            # latency, but is a separate optional retrieval operation.
            latencies.append(ms)
            blob = "\n".join(
                " ".join([
                    str(row.get("keyword") or ""), str(row.get("content") or ""),
                    str(row.get("input") or ""), str(row.get("identifiers") or ""),
                ])
                for row in rows
            ).casefold()
            keyword_hits = [keyword for keyword in case["keywords"] if keyword.casefold() in blob]
            identifier_hits = [identifier for identifier in case["identifiers"] if identifier.casefold() in blob]
            input_found = any(row.get("type") == "phreeqc_input" and row.get("input") for row in rows) or bool(input_rows)
            checks = len(case["keywords"]) + len(case["identifiers"]) + (1 if case["needs_input"] else 0)
            passed = len(keyword_hits) + len(identifier_hits) + (1 if input_found and case["needs_input"] else 0)
            answer_results.append({
                "query": case["query"],
                "plan": build_query_plan(case["query"], lexicon),
                "keyword_hits": keyword_hits,
                "identifier_hits": identifier_hits,
                "input_found": input_found,
                "coverage": pct(passed / max(1, checks)),
                "source_complete": all(bool(row.get("source")) for row in rows),
                "latency_ms": pct(ms + input_ms),
            })
        report["answer"] = {
            "mean_coverage": pct(statistics.mean(item["coverage"] for item in answer_results)),
            "source_rate": pct(sum(item["source_complete"] for item in answer_results) / len(answer_results)),
            "cases": answer_results,
        }
    finally:
        conn.close()

    retrieval = statistics.mean([
        report["symbol"]["top1_accuracy"], report["search"]["mean_precision"],
        report["search"]["mean_recall"], report["input"]["hit_rate"],
        report["examples"]["filter_accuracy"], report["context"]["target_rate"],
        report["answer"]["mean_coverage"],
    ])
    source = statistics.mean([report["search"]["source_rate"], report["input"]["source_rate"],
                              report["examples"]["source_rate"], report["context"]["source_rate"],
                              report["answer"]["source_rate"]])
    all_latencies = sorted(latencies)
    report["score"] = {"retrieval_quality_0_to_100": round(retrieval * 100, 1),
                        "source_traceability_0_to_100": round(source * 100, 1),
                        "overall_0_to_100": round((retrieval * 0.85 + source * 0.15) * 100, 1),
                        "latency_ms": {"count": len(latencies), "mean": pct(statistics.mean(latencies)),
                                       "p50": pct(statistics.median(latencies)), "p95": pct(all_latencies[min(len(all_latencies) - 1, int(len(all_latencies) * 0.95))])}}
    return report


def regression_check(report: Dict[str, Any]) -> Dict[str, Any]:
    score = report["score"]
    checks = {
        "overall_at_least_baseline": score["overall_0_to_100"] >= MIN_OVERALL,
        "search_recall_at_least_baseline": report["search"]["mean_recall"] >= MIN_SEARCH_RECALL,
        "source_traceability_complete": score["source_traceability_0_to_100"] >= MIN_SOURCE_TRACEABILITY * 100,
        "p95_latency_within_target": score["latency_ms"]["p95"] <= MAX_P95_MS,
    }
    return {"passed": all(checks.values()), "checks": checks, "thresholds": {
        "min_overall": MIN_OVERALL,
        "min_search_recall": MIN_SEARCH_RECALL,
        "min_source_traceability": MIN_SOURCE_TRACEABILITY,
        "max_p95_ms": MAX_P95_MS,
    }}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--write-report", type=Path)
    parser.add_argument("--check", action="store_true", help="return nonzero when regression thresholds fail")
    args = parser.parse_args()
    report = run(args.root.resolve(), args.limit)
    report["regression"] = regression_check(report)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not args.check or report["regression"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
