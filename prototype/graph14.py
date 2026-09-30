#!/usr/bin/env python3
"""Bandha-14: graph-first 14-bit relation cells.

Layout: source[6] | target[6] | relation[2].  A cell is an oriented edge
reference, not a phoneme feature record. The same 42-node inventory is used
as the graph, while relation kind says why the edge exists.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

WIDTH = 14
MAX_CODE = (1 << WIDTH) - 1
NODE_MASK = 0b11_1111
RELATION_MASK = 0b11
SUTRA, VARGA, LIFT, REVERSE = range(4)

class Bandha14Error(ValueError):
    pass
class InvalidRelation(Bandha14Error):
    pass
class UnknownSound(Bandha14Error):
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
RELATION_NAMES = {SUTRA: "sutra", VARGA: "varga", LIFT: "lift", REVERSE: "reverse"}

@dataclass(frozen=True)
class Relation:
    source: int
    target: int
    kind: int
    @property
    def code(self) -> int:
        return (self.source << 8) | (self.target << 2) | self.kind


def node(sound: str) -> int:
    try:
        return NAME_TO_NODE[sound]
    except KeyError as exc:
        raise UnknownSound(sound) from exc


def relation(source: int | str, target: int | str, kind: int | str) -> Relation:
    s = node(source) if isinstance(source, str) else source
    t = node(target) if isinstance(target, str) else target
    if isinstance(kind, str):
        try:
            kind = {v: k for k, v in RELATION_NAMES.items()}[kind]
        except KeyError as exc:
            raise InvalidRelation(kind) from exc
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (s, t, kind)):
        raise InvalidRelation((s, t, kind))
    if not (0 <= s < len(SOUNDS) and 0 <= t < len(SOUNDS) and 0 <= kind <= RELATION_MASK):
        raise InvalidRelation((s, t, kind))
    return Relation(s, t, kind)


def unpack(code_value: int) -> Relation:
    if isinstance(code_value, bool) or not isinstance(code_value, int) or not 0 <= code_value <= MAX_CODE:
        raise InvalidRelation(f"not a 14-bit relation cell: {code_value!r}")
    return relation((code_value >> 8) & NODE_MASK, (code_value >> 2) & NODE_MASK, code_value & RELATION_MASK)


def bits(code_value: int) -> str:
    unpack(code_value)
    return f"{code_value:014b}"


def decode(code_value: int) -> Tuple[str, str, str]:
    edge = unpack(code_value)
    return NODE_TO_NAME[edge.source], NODE_TO_NAME[edge.target], RELATION_NAMES[edge.kind]


def encode(source: int | str, target: int | str, kind: int | str) -> int:
    return relation(source, target, kind).code


def reverse(code_value: int) -> int:
    edge = unpack(code_value)
    return relation(edge.target, edge.source, REVERSE).code


def adjacency(codes: Iterable[int]) -> Dict[int, Tuple[int, ...]]:
    out: Dict[int, list[int]] = {}
    for value in codes:
        edge = unpack(value)
        out.setdefault(edge.source, []).append(edge.target)
    return {key: tuple(value) for key, value in out.items()}

__all__ = ["Bandha14Error", "InvalidRelation", "Relation", "SOUNDS", "adjacency", "bits", "decode", "encode", "node", "relation", "reverse", "unpack"]
