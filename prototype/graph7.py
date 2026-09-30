#!/usr/bin/env python3
"""Tantu-7: graph-first 7-bit identity codec.

A 7-bit cell addresses one of 42 sound vertices (0..41). The graph is not
flattened into the identity: edges are derived from the sutra path, varga
rows, and vowel relations. This keeps the small code honest: seven bits name
a vertex; graph structure supplies meaning.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

WIDTH = 7
MAX_CODE = (1 << WIDTH) - 1
NODE_BITS = 6
NODE_MASK = (1 << NODE_BITS) - 1
META_BIT = 1 << NODE_BITS

class Tantu7Error(ValueError):
    pass
class InvalidNode(Tantu7Error):
    pass
class UnknownSound(Tantu7Error):
    pass

SOUNDS = (
    "a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au",
    "h", "y", "v", "r", "l", "ñ", "m", "ṅ", "ṇ", "n",
    "j", "jh", "b", "bh", "g", "gh", "k", "kh", "c", "ch",
    "ṭ", "ṭh", "ḍ", "ḍh", "t", "th", "d", "dh", "p", "ph",
    "ś", "ṣ", "s",
)
NAME_TO_NODE = {name: i for i, name in enumerate(SOUNDS)}
NODE_TO_NAME = dict(enumerate(SOUNDS))

SUTRAS = (
    ("a", "i", "u", "ṇ"), ("ṛ", "ḷ", "k"), ("e", "o", "ṅ"),
    ("ai", "au", "c"), ("h", "y", "v", "r", "ṭ"), ("l", "ṇ"),
    ("ñ", "m", "ṅ", "ṇ", "n", "m"), ("jh", "bh", "ñ"),
    ("gh", "ḍh", "dh", "ṣ"), ("j", "b", "g", "ḍ", "d", "ś"),
    ("kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", "v"),
    ("k", "p", "y"), ("ś", "ṣ", "s", "r"), ("h", "l"),
)

@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    kind: str


def node(sound: str) -> int:
    try:
        return NAME_TO_NODE[sound]
    except KeyError as exc:
        raise UnknownSound(sound) from exc


def code(sound_or_node: str | int) -> int:
    index = node(sound_or_node) if isinstance(sound_or_node, str) else sound_or_node
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(SOUNDS):
        raise InvalidNode(index)
    return index


def validate(code_value: int) -> int:
    if isinstance(code_value, bool) or not isinstance(code_value, int) or not 0 <= code_value <= MAX_CODE:
        raise InvalidNode(f"not a 7-bit cell: {code_value!r}")
    if code_value & META_BIT or code_value > NODE_MASK:
        raise InvalidNode(f"meta/reserved cell, not a sound vertex: {code_value:07b}")
    if code_value >= len(SOUNDS):
        raise InvalidNode(f"unassigned vertex cell: {code_value:07b}")
    return code_value


def bits(code_value: int) -> str:
    return f"{validate(code_value):07b}"


def decode(code_value: int) -> str:
    return NODE_TO_NAME[validate(code_value)]


def _add(edges: set[Edge], a: str, b: str, kind: str) -> None:
    edges.add(Edge(node(a), node(b), kind))


def graph_edges() -> Tuple[Edge, ...]:
    edges: set[Edge] = set()
    # Sutra-path edges: markers are omitted, repeated sounds remain one vertex.
    for row in SUTRAS:
        sounds = [x for x in row[:-1] if x in NAME_TO_NODE]
        for a, b in zip(sounds, sounds[1:]):
            _add(edges, a, b, "sutra")
    # Five isomorphic varga rows: same articulatory slot across places.
    rows = (("k", "kh", "g", "gh", "ṅ"), ("c", "ch", "j", "jh", "ñ"),
            ("ṭ", "ṭh", "ḍ", "ḍh", "ṇ"), ("t", "th", "d", "dh", "n"),
            ("p", "ph", "b", "bh", "m"))
    for row_a, row_b in zip(rows, rows[1:]):
        for a, b in zip(row_a, row_b):
            _add(edges, a, b, "varga-shift")
    # Feature/derivation links: short -> long/wide or stop -> related sonorant.
    for a, b in (("a", "ai"), ("a", "au"), ("i", "y"), ("u", "v"), ("ṛ", "r"), ("ḷ", "l"),
                 ("e", "ai"), ("o", "au"), ("j", "y"), ("d", "r"), ("b", "v")):
        _add(edges, a, b, "lift")
    return tuple(sorted(edges, key=lambda e: (e.source, e.target, e.kind)))

EDGES = graph_edges()
ADJACENCY: Dict[int, Tuple[Edge, ...]] = {i: tuple(e for e in EDGES if e.source == i) for i in range(len(SOUNDS))}

def neighbors(vertex: int | str, kind: str | None = None) -> Tuple[int, ...]:
    source = node(vertex) if isinstance(vertex, str) else validate(vertex)
    return tuple(e.target for e in ADJACENCY[source] if kind is None or e.kind == kind)


def render(path: Iterable[int]) -> str:
    return " ".join(bits(value) for value in path)

__all__ = ["ADJACENCY", "EDGES", "Edge", "InvalidNode", "SOUNDS", "Tantu7Error", "bits", "code", "decode", "graph_edges", "neighbors", "node", "render", "validate"]
