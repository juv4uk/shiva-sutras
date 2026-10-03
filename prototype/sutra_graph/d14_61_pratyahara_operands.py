#!/usr/bin/env python3
"""Bounded D14 donor witness for rule -> pratyahara operand edges (#117).

This module does not allocate D14 coordinates and does not build another rule
graph. It resolves source forms already present in the 6.1 donor slice to the
existing Shiva-sutra/pratyahara graph in prototype/upc14v2.py.

Authority ceiling: repo-grounded control. The source-form -> canonical-class
mapping is explicit and tiny by design; generic Sanskrit inflection parsing is
not claimed here.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import sys
from typing import Dict, Tuple

PROTOTYPE = Path(__file__).resolve().parents[1]
if str(PROTOTYPE) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE))

import upc14v2 as g  # noqa: E402


@dataclass(frozen=True)
class PratyaharaNode:
    """Typed grammatical class node backed by the existing sutra-path donor."""
    node_id: str
    canonical_name: str
    start: str
    marker: str
    nth: int
    start_occurrence: int
    members: Tuple[str, ...]


@dataclass(frozen=True)
class RuleClassEdge:
    """A source-grounded rule operand/context edge."""
    rule_id: str
    relation: str
    source_form: str
    canonical_class: str
    grammatical_form: str
    class_node: PratyaharaNode
    provenance: Tuple[str, ...]
    evidence_tier: str = "repo-grounded-control"


SOURCE_FORMS: Dict[Tuple[str, str], Tuple[str, str, str]] = {
    ("6.1.77", "aci"): ("ac", "locative-singular", "uses-class"),
    ("6.1.101", "akaḥ"): ("ak", "genitive-singular", "uses-class"),
    ("6.1.101", "aci"): ("ac", "inherited-locative-context", "inherits-class-context"),
}

PROVENANCE: Dict[Tuple[str, str], Tuple[str, ...]] = {
    ("6.1.77", "aci"): (
        "prototype/sutra_graph/README.md: 6.1.77 aci scope to 6.1.108",
        "prototype/upc14v2_vowel_sandhi.py: AC computed from sutra-path pratyahara",
    ),
    ("6.1.101", "akaḥ"): (
        "docs/text7-candidate-d-ratification-2026-10-03.md: tests assert 1.1.9 + 6.1.101",
        "prototype/upc14v2_vowel_sandhi.py: 6.1.101 uses AK + savarna AC",
    ),
    ("6.1.101", "aci"): (
        "prototype/sutra_graph/README.md: 6.1.77 aci scope reaches 6.1.101",
        "prototype/upc14v2_vowel_sandhi.py: 6.1.101 consumes right operand in AC",
    ),
}


def _members(name: str) -> Tuple[str, ...]:
    return tuple(g.LABELS_BY_CODE[code] for code in g.pratyahara_named(name))


def resolve_pratyahara(name: str, *, node_id: str | None = None) -> PratyaharaNode:
    """Resolve one admitted named class from the existing pratyahara graph."""
    try:
        start, marker, nth, occurrence = g.NAMED_PRATYAHARA[name]
    except KeyError as exc:
        raise g.GraphError(f"unknown pratyahara operand: {name!r}") from exc

    return PratyaharaNode(
        node_id=node_id or f"opaque:{name}",
        canonical_name=name,
        start=start,
        marker=marker,
        nth=nth,
        start_occurrence=occurrence,
        members=_members(name),
    )


def edge_for(rule_id: str, source_form: str, *, node_id: str | None = None) -> RuleClassEdge:
    """Build a typed edge for one bounded 6.1 source-form control."""
    key = (rule_id, source_form)
    try:
        canonical, grammatical_form, relation = SOURCE_FORMS[key]
        provenance = PROVENANCE[key]
    except KeyError as exc:
        raise KeyError(f"unresolved source operand/context: {rule_id} {source_form}") from exc

    return RuleClassEdge(
        rule_id=rule_id,
        relation=relation,
        source_form=source_form,
        canonical_class=canonical,
        grammatical_form=grammatical_form,
        class_node=resolve_pratyahara(canonical, node_id=node_id),
        provenance=provenance,
    )


def relabel(edge: RuleClassEdge, new_node_id: str) -> RuleClassEdge:
    """Opaque-ID relabel; semantics and members must stay unchanged."""
    return replace(edge, class_node=replace(edge.class_node, node_id=new_node_id))


def bounded_edges() -> Tuple[RuleClassEdge, ...]:
    return (
        edge_for("6.1.77", "aci", node_id="class:opaque:01"),
        edge_for("6.1.101", "akaḥ", node_id="class:opaque:02"),
        edge_for("6.1.101", "aci", node_id="class:opaque:01"),
    )


if __name__ == "__main__":
    for edge in bounded_edges():
        print(
            edge.rule_id,
            edge.relation,
            edge.source_form,
            "->",
            edge.class_node.node_id,
            edge.canonical_class,
            ",".join(edge.class_node.members),
            sep="\t",
        )
