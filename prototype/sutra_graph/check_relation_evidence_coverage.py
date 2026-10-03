#!/usr/bin/env python3
"""#103 — coverage guard for all current curated relation evidence overlays.

The graph remains authoritative as repo-curated-control.  Evidence overlays may
support existing edges at a commentarial/secondary tier, but they may not invent
relations, promote primary authority, or allocate D14 coordinates.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_graph(path: Path) -> set[tuple[str, str, str]]:
    out: set[tuple[str, str, str]] = set()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if set(reader.fieldnames or ()) != {"src", "dst", "kind", "label"}:
            raise ValueError("edge schema mismatch")
        for row in reader:
            out.add((row["src"], row["dst"], row["kind"]))
    if not out:
        raise ValueError("empty graph")
    return out


def read_overlay(path: Path) -> tuple[dict, set[tuple[str, str, str]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "panini-relation-evidence/v1"
    assert payload["authority"] == "commentarial-supported"
    assert payload["no_d14_allocation"] is True
    assert payload["primary_relation_promotions"] == 0

    sources = payload["sources"]
    edges: set[tuple[str, str, str]] = set()
    for row in payload["edges"]:
        edge = (row["src"], row["dst"], row["kind"])
        if edge in edges:
            raise AssertionError(f"duplicate overlay edge: {edge}")
        if row["status"] != "commentarial-supported":
            raise AssertionError(f"bad evidence tier: {edge}")
        if not row["source_keys"]:
            raise AssertionError(f"missing source keys: {edge}")
        for key in row["source_keys"]:
            if key not in sources:
                raise AssertionError(f"unknown source {key}: {edge}")
            if not str(sources[key]["url"]).startswith("https://"):
                raise AssertionError(f"non-https source {key}: {edge}")
        edges.add(edge)
    return payload, edges


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges", type=Path, required=True)
    ap.add_argument("--adhikara", type=Path, required=True)
    ap.add_argument("--remaining", type=Path, required=True)
    args = ap.parse_args()

    graph = read_graph(args.edges)
    adhikara_payload, adhikara = read_overlay(args.adhikara)
    remaining_payload, remaining = read_overlay(args.remaining)

    if adhikara & remaining:
        raise AssertionError(f"overlapping evidence overlays: {sorted(adhikara & remaining)}")

    union = adhikara | remaining
    if union != graph:
        raise AssertionError(
            f"relation evidence coverage mismatch missing={sorted(graph-union)} "
            f"extra={sorted(union-graph)}"
        )

    if not all(edge[2] == "adhikara" for edge in adhikara):
        raise AssertionError("adhikara overlay contains another relation kind")
    if any(edge[2] == "adhikara" for edge in remaining):
        raise AssertionError("remaining overlay duplicates adhikara evidence")

    expected_remaining_kinds = {"apavada", "blocks", "depends_on"}
    if {edge[2] for edge in remaining} != expected_remaining_kinds:
        raise AssertionError("remaining relation-kind set changed")

    primary_promotions = (
        adhikara_payload["primary_relation_promotions"]
        + remaining_payload["primary_relation_promotions"]
    )
    assert primary_promotions == 0

    print(f"CURATED-EDGES={len(graph)}")
    print(f"COMMENTARIAL-SUPPORTED-EDGES={len(union)}")
    print(f"ADHIKARA-SUPPORTED={len(adhikara)}")
    print(f"OTHER-RELATION-SUPPORTED={len(remaining)}")
    print("RELATION-EVIDENCE-COVERAGE=100%")
    print(f"PRIMARY-RELATION-PROMOTIONS={primary_promotions}")
    print("D14-FORCED-COORDINATES=0")
    print("D14-ALLOCATION=NONE")
    print("STATUS=PASS-CURATED-RELATION-EVIDENCE-COVERAGE")


if __name__ == "__main__":
    main()
