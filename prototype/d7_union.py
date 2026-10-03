#!/usr/bin/env python3
"""D7 model A as an executable witness: a TYPED DISJOINT UNION  Sound7 (+) Number  (research; nothing enters SENS core).

    Sound7(cell)     a 7-bit sound cell (identity = the cell number, as in Text identity #1700); NO arithmetic, NO ordering
    Number(q)        an exact rational (arbitrary precision; no fixed width: SENS #2443)

Laws stated here, each with a falsifier in test_d7_union.py:
  L1  eq is defined on every pair; across the two types it is 0 (false), never an error and never a numeric comparison
      (SENS: Text7 == Number is false).
  L2  arithmetic and ordering are defined on Number x Number only; any operation that mixes types or touches Sound7 raises.
  L3  independence: relabelling the Sound7 cells (any permutation of 0..127) changes no Number result, and a Number that fits
      in 7 bits is NOT the Sound7 with the same bits.
  L4  no implicit conversion in either direction; the only projections are explicit, named, and lossy (`sound_to_wire`).

Honesty note: L3's relabelling test is true BY CONSTRUCTION here (Number code never reads a Sound cell); it documents the
independence claim as an executable contract, it does not discover it. The code-level evidence for the real SENS is
my-lisp-panini#47 (d7_probe) and SENS #2443/PR #2449.

This is the model-A WITNESS only: it does not show that models B/C/D are false, and it states no Sound<->Number equation.
"""
from fractions import Fraction
from typing import Union


class D7TypeError(TypeError):
    pass


class Sound7:
    __slots__ = ("cell",)

    def __init__(self, cell: int):
        if not isinstance(cell, int) or isinstance(cell, bool) or not 0 <= cell <= 127:
            raise D7TypeError(f"Sound7 cell must be an int 0..127, got {cell!r}")
        self.cell = cell

    def __repr__(self):
        return f"Sound7({self.cell})"


class Number:
    __slots__ = ("q",)

    def __init__(self, q):
        self.q = Fraction(q)

    def __repr__(self):
        return f"Number({self.q})"


D7 = Union[Sound7, Number]


def eq(a: D7, b: D7) -> int:
    """PredicateBit (1/0). Same type: identity; different types: 0."""
    if isinstance(a, Sound7) and isinstance(b, Sound7):
        return int(a.cell == b.cell)
    if isinstance(a, Number) and isinstance(b, Number):
        return int(a.q == b.q)
    return 0


def _nn(a: D7, b: D7, op: str) -> None:
    if not (isinstance(a, Number) and isinstance(b, Number)):
        raise D7TypeError(f"{op} is defined on Number x Number only, got {type(a).__name__} and {type(b).__name__}")


def add(a: D7, b: D7) -> Number:
    _nn(a, b, "add")
    return Number(a.q + b.q)


def mul(a: D7, b: D7) -> Number:
    _nn(a, b, "mul")
    return Number(a.q * b.q)


def lt(a: D7, b: D7) -> int:
    _nn(a, b, "lt")
    return int(a.q < b.q)


def sound_to_wire(s: Sound7) -> str:
    """The only projection: an explicit machine token, a String, never a Number."""
    if not isinstance(s, Sound7):
        raise D7TypeError("sound_to_wire takes a Sound7")
    return "#t7:%02x" % s.cell
