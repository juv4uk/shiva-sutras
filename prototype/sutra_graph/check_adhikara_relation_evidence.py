#!/usr/bin/env python3
"""#103 — verify relation-evidence overlay against the curated graph.

This checker does not prove Pāṇinian grammar from source text. It enforces that:
- relation evidence only attaches to edges already present in the curated fixture;
- the evidence set is exactly the current 6.1.84 adhikāra edge subset;
- no other relation kind is silently promoted;
- evidence status remains commentarial-supported, never primary relation authority;
- D14 coordinates remain unallocated.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_edges(path: Path) -> set[tuple[str, str, str]]:
    out: set[tuple[str, str, str]] = set()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if set(reader.fieldnames or ()) != {"src", "dst", "kind", "label"}:
            raise ValueError("edge schema mismatch")
        for row in reader:
            out.add((row["src"], row["dst"], row["kind"]))
    return out


def sutra_tuple(node: str) -> tuple[int, int, int]:
    parts = node.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"bad sūtra id: {node}")
    return tuple(map(int, parts))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, required=True)
    args = ap.parse_args()

    graph = read_edges(args.edges)
    payload = json.loads(args.evidence.read_text(encoding="utf-8"))

    assert payload["schema"] == "panini-relation-evidence/v1"
    assert payload["authority"] == "commentarial-supported"
    assert payload["no_d14_allocation"] is True
    assert payload["primary_relation_promotions"] == 0
    assert payload["relation_kind"] == "adhikara"
    assert payload["anchor_node"] == "6.1.84"

    sources = payload["sources"]
    evidence_edges: set[tuple[str, str, str]] = set()
    for row in payload["edges"]:
        edge = (row["src"], row["dst"], row["kind"])
        if edge in evidence_edges:
            raise AssertionError(f"duplicate relation evidence: {edge}")
        if edge not in graph:
            raise AssertionError(f"evidence invents graph edge: {edge}")
        if row["kind"] != "adhikara" or row["dst"] != "6.1.84":
            raise AssertionError(f"out-of-scope relation promotion: {edge}")
        if row["status"] != "commentarial-supported":
            raise AssertionError(f"unexpected evidence tier: {edge}")
        if not row["source_keys"]:
            raise AssertionError(f"missing source key: {edge}")
        for key in row["source_keys"]:
            if key not in sources:
                raise AssertionError(f"unknown source key {key}: {edge}")
            if not sources[key]["url"].startswith("https://"):
                raise AssertionError(f"non-https source {key}: {edge}")
        evidence_edges.add(edge)

    expected = {
        edge
        for edge in graph
        if edge[2] == "adhikara" and edge[1] == "6.1.84"
    }
    if evidence_edges != expected:
        raise AssertionError(
            f"adhikara evidence coverage mismatch missing={sorted(expected-evidence_edges)} "
            f"extra={sorted(evidence_edges-expected)}"
        )

    start = sutra_tuple(payload["scope_claim"]["start"])
    end = sutra_tuple(payload["scope_claim"]["through"])
    for src, dst, _kind in evidence_edges:
        pos = sutra_tuple(src)
        if not (start < pos <= end):
            raise AssertionError(f"edge outside declared adhikara scope: {src}")
        if sutra_tuple(dst) != start:
            raise AssertionError(f"unexpected adhikara anchor: {dst}")

    unsupported_kinds = sorted({
        kind for (_src, _dst, kind) in graph
        if kind != "adhikara"
    })
    assert unsupported_kinds == ["apavada", "blocks", "depends_on"]

    print(f"CURATED-EDGES={len(graph)}")
    print(f"COMMENTARIAL-SUPPORTED-ADHIKARA-EDGES={len(evidence_edges)}")
    print(f"PRIMARY-RELATION-PROMOTIONS={payload['primary_relation_promotions']}")
    print("UNTOUCHED-RELATION-KINDS=" + ",".join(unsupported_kinds))
    print("D14-FORCED-COORDINATES=0")
    print("D14-ALLOCATION=NONE")
    print("STATUS=PASS-RELATION-EVIDENCE-OVERLAY")


if __name__ == "__main__":
    main()
