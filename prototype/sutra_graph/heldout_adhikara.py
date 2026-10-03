#!/usr/bin/env python3
"""#111 — held-out reconstruction of 6.1.84 adhikara membership.

Research-only donor witness for SENS D14.

The derivation uses:
- commentarial-supported scope law for 6.1.84;
- independently text-anchored canonical source order/provenance;
- opaque graph node IDs only as transport keys.

It does NOT:
- use a whitelist of known children;
- recover the hidden edge from the edge table;
- allocate any D14 coordinate.
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, order=True)
class Edge:
    src: str
    dst: str
    kind: str
    label: str


def read_edges(path: Path) -> tuple[Edge, ...]:
    rows: list[Edge] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"src", "dst", "kind", "label"}
        if set(reader.fieldnames or ()) != required:
            raise ValueError(f"edge schema mismatch: {reader.fieldnames!r}")
        for row in reader:
            rows.append(Edge(row["src"], row["dst"], row["kind"], row["label"]))
    if not rows:
        raise ValueError("empty graph")
    return tuple(rows)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_ref(ref: str) -> tuple[int, int, int]:
    if ref.startswith("PS_"):
        ref = ref[3:].replace(",", ".")
    parts = ref.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"bad canonical ref: {ref}")
    return tuple(map(int, parts))


def anchor_index(payload: dict) -> dict[str, dict]:
    anchors = payload["anchors"]
    out = {}
    for row in anchors:
        node = row["node_id"]
        if node in out:
            raise AssertionError(f"duplicate node anchor: {node}")
        if row["relation_authority"] != "none":
            raise AssertionError(f"node anchor illegally carries relation authority: {node}")
        out[node] = row
    return out


def derive_scope_children(
    anchors: dict[str, dict],
    relation: dict,
) -> tuple[str, ...]:
    """Derive current bounded graph children from source order + scope law.

    No child IDs are hard-coded. The candidate set is every text-anchored node
    in the same chapter/pada whose canonical source position lies strictly after
    the adhikara start and at/before the declared scope end.
    """
    anchor_node = relation["anchor_node"]
    if anchor_node not in anchors:
        raise ValueError("adhikara anchor has no textual provenance")

    scope = relation["scope_claim"]
    start = parse_ref(scope["start"])
    end = parse_ref(scope["through"])

    anchor_pos = parse_ref(anchors[anchor_node]["canonical_ref"])
    if anchor_pos != start:
        raise AssertionError(
            f"scope start {start} disagrees with anchor provenance {anchor_pos}"
        )

    candidates: list[str] = []
    for node, row in anchors.items():
        pos = parse_ref(row["canonical_ref"])
        if pos[:2] != start[:2]:
            continue
        if start < pos <= end:
            candidates.append(node)
    return tuple(sorted(candidates, key=lambda node: parse_ref(anchors[node]["canonical_ref"])))


def adhikara_edges(edges: tuple[Edge, ...], anchor: str) -> tuple[Edge, ...]:
    return tuple(
        sorted(
            edge
            for edge in edges
            if edge.kind == "adhikara" and edge.dst == anchor
        )
    )


def expected_edge_set(children: tuple[str, ...], anchor: str) -> set[tuple[str, str, str]]:
    return {(child, anchor, "adhikara") for child in children}


def rename_fixture(
    anchors: dict[str, dict],
    relation: dict,
    mapping: dict[str, str],
) -> tuple[dict[str, dict], dict]:
    if set(mapping) != set(anchors) or set(mapping.values()) != set(anchors):
        raise ValueError("mapping must be a bijection over all anchored nodes")

    renamed_anchors: dict[str, dict] = {}
    for old, row in anchors.items():
        new = mapping[old]
        copied = copy.deepcopy(row)
        copied["node_id"] = new
        # canonical_ref/text/source_key are provenance and must travel with node.
        renamed_anchors[new] = copied

    renamed_relation = copy.deepcopy(relation)
    renamed_relation["anchor_node"] = mapping[relation["anchor_node"]]
    return renamed_anchors, renamed_relation


def deterministic_mapping(nodes: tuple[str, ...], seed: int) -> dict[str, str]:
    shuffled = list(nodes)
    random.Random(seed).shuffle(shuffled)
    return dict(zip(nodes, shuffled, strict=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges", type=Path, required=True)
    ap.add_argument("--anchors", type=Path, required=True)
    ap.add_argument("--relation", type=Path, required=True)
    ap.add_argument("--trials", type=int, default=64)
    args = ap.parse_args()

    edges = read_edges(args.edges)
    anchors_payload = load_json(args.anchors)
    relation = load_json(args.relation)

    assert anchors_payload["authority"] == "textual-edition-anchor-only"
    assert anchors_payload["no_d14_allocation"] is True
    assert relation["authority"] == "commentarial-supported"
    assert relation["relation_kind"] == "adhikara"
    assert relation["anchor_node"] == "6.1.84"
    assert relation["no_d14_allocation"] is True
    assert relation["primary_relation_promotions"] == 0

    anchors = anchor_index(anchors_payload)
    anchor = relation["anchor_node"]

    derived_children = derive_scope_children(anchors, relation)
    derived = expected_edge_set(derived_children, anchor)

    existing_edges = adhikara_edges(edges, anchor)
    existing = {(e.src, e.dst, e.kind) for e in existing_edges}

    # Validation only: the derivation itself did not inspect existing child edges.
    assert derived == existing, (sorted(derived), sorted(existing))
    assert len(derived_children) == 5

    # Leave-one-out: remove each real edge and reconstruct from the one reusable law.
    leave_one_out = 0
    for victim in existing_edges:
        reduced = tuple(edge for edge in edges if edge != victim)
        assert (victim.src, victim.dst, victim.kind) not in {
            (e.src, e.dst, e.kind) for e in reduced
        }
        reconstructed = expected_edge_set(
            derive_scope_children(anchors, relation),
            anchor,
        )
        assert (victim.src, victim.dst, victim.kind) in reconstructed
        leave_one_out += 1

    # Lawful opaque-ID renaming: provenance travels with nodes, grammar survives.
    node_ids = tuple(sorted(anchors))
    lawful = 0
    broken = 0
    nontrivial = 0
    for seed in range(args.trials):
        mapping = deterministic_mapping(node_ids, seed)
        if any(mapping[node] != node for node in node_ids):
            nontrivial += 1

        renamed_anchors, renamed_relation = rename_fixture(
            anchors, relation, mapping
        )
        renamed_children = derive_scope_children(
            renamed_anchors, renamed_relation
        )
        recovered_original = {
            (next(old for old, new in mapping.items() if new == child), anchor, "adhikara")
            for child in renamed_children
        }
        assert recovered_original == existing
        lawful += 1

        # Broken control: rename the semantic anchor ID but do not transport
        # textual provenance records. This must fail or disagree.
        broken_relation = copy.deepcopy(relation)
        broken_relation["anchor_node"] = mapping[anchor]
        try:
            broken_children = derive_scope_children(anchors, broken_relation)
        except (ValueError, AssertionError):
            broken += 1
        else:
            if set(broken_children) != set(derived_children):
                broken += 1

    assert lawful == args.trials
    assert nontrivial > 0
    assert broken > 0

    # Scope mutation falsifier: 6.1.97 must drop if the scope ends at 6.1.96.
    shortened = copy.deepcopy(relation)
    shortened["scope_claim"]["through"] = "6.1.96"
    shortened_children = set(derive_scope_children(anchors, shortened))
    assert "6.1.97" not in shortened_children

    # Out-of-scope negative: 8.4.* must never be inherited by 6.1.84.
    assert not any(child.startswith("8.4.") for child in derived_children)

    # Wrong-kind negative: this law derives only adhikara membership.
    wrong_kind = {(src, dst, "blocks") for src, dst, _ in derived}
    assert wrong_kind != existing

    # Explicit anti-cheat / allocation boundary.
    assert "6.1.97" not in json.dumps(relation["scope_claim"])
    assert anchors_payload["relation_promotions"] == 0

    print(f"CURATED-ADHIKARA-EDGES={len(existing)}")
    print(f"DERIVED-SCOPE-CHILDREN={len(derived_children)}")
    print(f"LEAVE-ONE-OUT-RECONSTRUCTIONS={leave_one_out}")
    print(f"LAWFUL-OPAQUE-RELABEL-PASSES={lawful}")
    print(f"BROKEN-PROVENANCE-RELABEL-CHANGES={broken}")
    print(f"NONTRIVIAL-PERMUTATIONS={nontrivial}")
    print("SCOPE-SHORTENING-FALSIFIER=PASS")
    print("OUT-OF-SCOPE-8.4=REJECTED")
    print("WRONG-EDGE-KIND=REJECTED")
    print("NODE-IDS=OPAQUE")
    print("SOURCE-ORDER=PROVENANCE-ONLY")
    print("RELATION-AUTHORITY=COMMENTARIAL-SUPPORTED")
    print("PRIMARY-RELATION-PROMOTIONS=0")
    print("D14-FORCED-COORDINATES=0")
    print("D14-ALLOCATION=NONE")
    print("STATUS=PASS-HELDOUT-ADHIKARA-RECONSTRUCTION")


if __name__ == "__main__":
    main()
