#!/usr/bin/env python3
"""Graph-ID invariance / held-out-edge attack for shiva-sutras#103.

The checker is deliberately independent of SENS D14 numbering.

Input is a derived edge TSV with columns:
    src, dst, kind, label

It treats node IDs as opaque transport keys. Queries depend only on typed graph
structure and transported provenance labels.

This file can run on:
- a real /tmp/sg/edges.tsv produced by build_sutra_graph.py from source data;
- the synthetic fixture used by test_sutra_graph.py.

No D14 coordinate allocation occurs here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, order=True)
class Edge:
    src: str
    dst: str
    kind: str
    label: str


def read_edges(path: Path) -> tuple[Edge, ...]:
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"src", "dst", "kind", "label"}
        if set(reader.fieldnames or ()) != required:
            raise ValueError(f"edge schema mismatch: {reader.fieldnames!r}")
        for row in reader:
            rows.append(Edge(row["src"], row["dst"], row["kind"], row["label"]))
    if not rows:
        raise ValueError("empty graph")
    return tuple(rows)


def nodes(edges: Iterable[Edge]) -> tuple[str, ...]:
    return tuple(sorted({e.src for e in edges} | {e.dst for e in edges}))


def rename_graph(edges: Iterable[Edge], mapping: dict[str, str]) -> tuple[Edge, ...]:
    ns = set(nodes(edges))
    if set(mapping) != ns or set(mapping.values()) != ns:
        raise ValueError("renaming must be a bijection over exactly the graph nodes")
    return tuple(
        Edge(mapping[e.src], mapping[e.dst], e.kind, e.label)
        for e in edges
    )


def inverse_mapping(mapping: dict[str, str]) -> dict[str, str]:
    return {v: k for k, v in mapping.items()}


def query_targets(
    edges: Iterable[Edge],
    source: str,
    kind: str,
    label: str | None = None,
) -> tuple[str, ...]:
    return tuple(sorted(
        e.dst
        for e in edges
        if e.src == source
        and e.kind == kind
        and (label is None or e.label == label)
    ))


def canonical_query_signature(
    edges: Iterable[Edge],
    source: str,
    kind: str,
    label: str | None = None,
) -> str:
    payload = "\n".join(query_targets(edges, source, kind, label))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def lawful_rename_invariant(
    edges: tuple[Edge, ...],
    source: str,
    kind: str,
    mapping: dict[str, str],
    label: str | None = None,
) -> bool:
    before = query_targets(edges, source, kind, label)
    renamed = rename_graph(edges, mapping)
    after_renamed = query_targets(
        renamed,
        mapping[source],
        kind,
        label,
    )
    inv = inverse_mapping(mapping)
    after = tuple(sorted(inv[x] for x in after_renamed))
    return before == after


def delete_one_required_edge_fails(
    edges: tuple[Edge, ...],
    source: str,
    kind: str,
    label: str | None = None,
) -> bool:
    matching = [
        e for e in edges
        if e.src == source
        and e.kind == kind
        and (label is None or e.label == label)
    ]
    if not matching:
        raise ValueError("query has no positive edge to hold out")
    victim = matching[0]
    reduced = tuple(e for e in edges if e != victim)
    return (
        query_targets(edges, source, kind, label)
        != query_targets(reduced, source, kind, label)
    )


def mutate_edge_kind_fails(
    edges: tuple[Edge, ...],
    source: str,
    kind: str,
    label: str | None = None,
) -> bool:
    matching = [
        e for e in edges
        if e.src == source
        and e.kind == kind
        and (label is None or e.label == label)
    ]
    if not matching:
        raise ValueError("query has no positive edge to mutate")
    victim = matching[0]
    replacement = Edge(victim.src, victim.dst, "__wrong_kind__", victim.label)
    mutated = tuple(replacement if e == victim else e for e in edges)
    return (
        query_targets(edges, source, kind, label)
        != query_targets(mutated, source, kind, label)
    )


def broken_renaming_fails(
    edges: tuple[Edge, ...],
    source: str,
    kind: str,
    mapping: dict[str, str],
    label: str | None = None,
) -> bool:
    """Rename the query node but intentionally do not transport graph edges."""
    before = query_targets(edges, source, kind, label)
    broken = query_targets(edges, mapping[source], kind, label)
    return before != broken


def deterministic_permutation(ns: tuple[str, ...], seed: int) -> dict[str, str]:
    shuffled = list(ns)
    random.Random(seed).shuffle(shuffled)
    return dict(zip(ns, shuffled, strict=True))


def choose_positive_query(edges: tuple[Edge, ...]) -> tuple[str, str, str | None]:
    # Prefer source-grounded structural edge classes over free-form references.
    priorities = ("anuvrtti", "adhikara", "apavada", "kasika_ref")
    for kind in priorities:
        candidates = sorted(e for e in edges if e.kind == kind)
        if candidates:
            edge = candidates[0]
            return edge.src, edge.kind, edge.label or None
    edge = sorted(edges)[0]
    return edge.src, edge.kind, edge.label or None


def run(edges: tuple[Edge, ...], trials: int) -> dict[str, object]:
    source, kind, label = choose_positive_query(edges)
    ns = nodes(edges)

    lawful = 0
    broken = 0
    nontrivial = 0

    for seed in range(trials):
        mapping = deterministic_permutation(ns, seed)
        if any(mapping[n] != n for n in ns):
            nontrivial += 1

        if lawful_rename_invariant(edges, source, kind, mapping, label):
            lawful += 1
        if broken_renaming_fails(edges, source, kind, mapping, label):
            broken += 1

    assert lawful == trials
    assert nontrivial > 0
    assert broken > 0
    assert delete_one_required_edge_fails(edges, source, kind, label)
    assert mutate_edge_kind_fails(edges, source, kind, label)

    return {
        "nodes": len(ns),
        "edges": len(edges),
        "query_source": source,
        "query_kind": kind,
        "query_label": label or "",
        "query_targets": list(query_targets(edges, source, kind, label)),
        "lawful_relabel_passes": lawful,
        "broken_relabel_changes": broken,
        "nontrivial_permutations": nontrivial,
        "delete_edge_fails": True,
        "wrong_edge_kind_fails": True,
        "d14_forced_coordinates": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("edges_tsv", type=Path)
    parser.add_argument("--trials", type=int, default=64)
    args = parser.parse_args()

    result = run(read_edges(args.edges_tsv), args.trials)
    for key, value in result.items():
        print(f"{key.upper()}={value}")
    print("NODE-IDS=OPAQUE")
    print("D14-ALLOCATION=NONE")
    print("STATUS=PASS-GRAPH-RELABELLING-HARNESS")


if __name__ == "__main__":
    main()
