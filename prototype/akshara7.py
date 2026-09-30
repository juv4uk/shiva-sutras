#!/usr/bin/env python3
"""Akshara-7: a compact, self-contained Śiva-sūtra code.

The top bit identifies a sound or meta cell; the remaining six bits are a
family-local payload. This is an independent engineering experiment, not a
projection of UPC-8 and not a historical or hardware claim.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

WIDTH = 7
MAX_CODE = (1 << WIDTH) - 1
SOUND, META = 0, 1
PAYLOAD_MASK = 0b11_1111

class Akshara7Error(ValueError):
    pass
class InvalidCode(Akshara7Error):
    pass
class UnknownSound(Akshara7Error):
    pass

SOUND_ORDER = (
    "a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au",
    "h", "y", "v", "r", "l", "ñ", "m", "ṅ", "ṇ", "n",
    "j", "jh", "b", "bh", "g", "gh", "k", "kh", "c", "ch",
    "ṭ", "ṭh", "ḍ", "ḍh", "t", "th", "d", "dh", "p", "ph",
    "ś", "ṣ", "s",
)
SOUND_CODE = {name: i for i, name in enumerate(SOUND_ORDER)}
CODE_SOUND = {code: name for name, code in SOUND_CODE.items()}
SUTRAS = (
    ("a", "i", "u", "ṇ"), ("ṛ", "ḷ", "k"), ("e", "o", "ṅ"),
    ("ai", "au", "c"), ("h", "y", "v", "r", "ṭ"), ("l", "ṇ"),
    ("ñ", "m", "ṅ", "ṇ", "n", "m"), ("jh", "bh", "ñ"),
    ("gh", "ḍh", "dh", "ṣ"), ("j", "b", "g", "ḍ", "d", "ś"),
    ("kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", "v"),
    ("k", "p", "y"), ("ś", "ṣ", "s", "r"), ("h", "l"),
)
MARKER_CODE = {i: (META << 6) | i for i in range(len(SUTRAS))}

@dataclass(frozen=True)
class Cell:
    family: int
    payload: int

def check(code: int) -> int:
    if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code <= MAX_CODE:
        raise InvalidCode(f"not a 7-bit code: {code!r}")
    family, payload = code >> 6, code & PAYLOAD_MASK
    if family == SOUND and payload >= len(SOUND_ORDER):
        raise InvalidCode(f"reserved Akshara-7 cell: {code:07b}")
    if family == META and payload >= len(SUTRAS):
        raise InvalidCode(f"unknown marker cell: {code:07b}")
    return code

def bits(code: int) -> str:
    return f"{check(code):07b}"

def encode(sound: str) -> int:
    try:
        return SOUND_CODE[sound]
    except KeyError as exc:
        raise UnknownSound(sound) from exc

def decode(code: int) -> str:
    check(code)
    try:
        return CODE_SOUND[code]
    except KeyError as exc:
        raise InvalidCode(f"not a sound cell: {code:07b}") from exc

def parse_bits(text: str) -> Tuple[int, ...]:
    cells = tuple(text.split())
    if not cells:
        return ()
    out = []
    for cell in cells:
        if len(cell) != WIDTH or set(cell) - {"0", "1"}:
            raise InvalidCode(f"expected whitespace-separated 7-bit cells: {cell!r}")
        out.append(check(int(cell, 2)))
    return tuple(out)

def render(codes: Iterable[int]) -> str:
    return " ".join(bits(code) for code in codes)

def _path():
    for sutra_index, sutra in enumerate(SUTRAS):
        for index, token in enumerate(sutra):
            yield token, index == len(sutra) - 1, sutra_index

def pratyahara(start: str, marker: str, occurrence: int = 1) -> Tuple[int, ...]:
    path = tuple(_path())
    starts = [i for i, (token, _, _) in enumerate(path) if token == start]
    if not 1 <= occurrence <= len(starts):
        raise UnknownSound(f"no occurrence {occurrence} of {start!r}")
    begin = starts[occurrence - 1]
    for end in range(begin + 1, len(path)):
        token, is_marker, _ = path[end]
        if is_marker and token == marker:
            return tuple(encode(t) for t, _, _ in path[begin:end])
    raise UnknownSound(f"marker {marker!r} not found after {start!r}")

__all__ = ["SOUND_CODE", "SUTRAS", "Akshara7Error", "InvalidCode", "UnknownSound", "bits", "check", "decode", "encode", "parse_bits", "pratyahara", "render"]
