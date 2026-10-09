#!/usr/bin/env python3
"""#103 — primary text node-anchor guard for the curated Pāṇini graph.

This checker deliberately proves less than the graph relation harness:
- every node in curated_controls_edges.tsv has exactly one independently
  readable textual-edition anchor;
- no edge relation is promoted by those node anchors;
- D14 allocation remains empty.

It never infers adhikāra/apavāda/blocks/depends_on from sūtra text alone.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def edge_nodes(path: Path) -> set[str]:
    out: set[str] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if set(reader.fieldnames or ()) != {"src", "dst", "kind", "label"}:
            raise ValueError("curated edge schema mismatch")
        for row in reader:
            out.add(row["src"])
            out.add(row["dst"])
    if not out:
        raise ValueError("curated graph is empty")
    return out


def expected_ref(node_id: str) -> str:
    parts = node_id.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"non-canonical sūtra node id: {node_id}")
    return f"PS_{parts[0]},{parts[1]}.{parts[2]}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges", type=Path, required=True)
    ap.add_argument("--anchors", type=Path, required=True)
    args = ap.parse_args()

    nodes = edge_nodes(args.edges)
    payload = json.loads(args.anchors.read_text(encoding="utf-8"))

    assert payload["schema"] == "panini-primary-text-anchors/v1"
    assert payload["authority"] == "textual-edition-anchor-only"
    assert payload["no_d14_allocation"] is True
    assert payload["relation_promotions"] == 0

    sources = payload["sources"]
    anchors = payload["anchors"]
    by_node: dict[str, dict[str, object]] = {}
    for row in anchors:
        node_id = row["node_id"]
        if node_id in by_node:
            raise AssertionError(f"duplicate text anchor: {node_id}")
        if row["canonical_ref"] != expected_ref(node_id):
            raise AssertionError(f"canonical ref mismatch: {node_id}")
        if not str(row["text"]).strip():
            raise AssertionError(f"empty sūtra text: {node_id}")
        if row["source_key"] not in sources:
            raise AssertionError(f"unknown source key: {node_id}")
        if row["relation_authority"] != "none":
            raise AssertionError(f"node text illegally promotes relation: {node_id}")
        source = sources[row["source_key"]]
        if not str(source["url"]).startswith("https://"):
            raise AssertionError(f"non-https textual source: {node_id}")
        by_node[node_id] = row

    anchored = set(by_node)
    missing = sorted(nodes - anchored)
    extra = sorted(anchored - nodes)
    if missing or extra:
        raise AssertionError(f"anchor coverage mismatch missing={missing} extra={extra}")

    print(f"CURATED-GRAPH-NODES={len(nodes)}")
    print(f"TEXTUAL-ANCHORS={len(anchors)}")
    print("ANCHOR-COVERAGE=100%")
    print("RELATION-PROMOTIONS=0")
    print("EDGE-AUTHORITY=repo-curated-control")
    print("D14-FORCED-COORDINATES=0")
    print("D14-ALLOCATION=NONE")
    print("STATUS=PASS-TEXT-NODE-ANCHORS")


if __name__ == "__main__":
    main()
