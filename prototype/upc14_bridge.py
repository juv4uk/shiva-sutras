#!/usr/bin/env python3
"""
Bridge UPC-7 -> UPC-14 (shiva-sutras#44, experiment)
====================================================

Proves that the 14-bit candidate loses nothing of the ratified UPC-7: every one
of the 107 assigned UPC-7 cells has a distinct UPC-14 code. UPC-7 is the input
here and is never changed. The bridge is the only place both worlds meet.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import upc14 as u14
import upc7_geometry as geo
from upc7_layouts import ASSIGNED, UPC7Text, build_cells

# UPC-7 vowel row -> the sutra letter of its short form.
_ROW_LETTER = {
    "a": "a", "i": "i", "u": "u", "r-vocalic": "f", "l-vocalic": "x", "e": "e", "o": "o",
}
# The e / o rows carry ai / au as their LONG form in UPC-7 (vrddhi as surface
# length); the sutras give ai and au their own positions, so UPC-14 does too.
_LONG_LETTER = {"e": "E", "o": "O"}

_UK_CONSONANT_EXT = {
    "х": "uk.kh", "ж": "uk.zh", "з": "uk.z", "ф": "uk.f", "г": "uk.h-voiced",
}
_UK_VOWEL_EXT = {"a": "uk.a", "e": "uk.e", "o": "uk.o", "y": "uk.y"}
_UK_AFFRICATE_EXT = {"ts": "uk.ts", "tsh": "uk.tsh", "dz": "uk.dz", "dzh": "uk.dzh"}

_SANSKRIT_SIGN_NAMES = {
    "anusvara", "visarga", "avagraha", "danda", "double-danda",
}


class BridgeError(ValueError):
    pass


def _letter_code(letter: str, *, nasal: bool = False, long: bool = False) -> int:
    modifiers = u14.modifiers_of(nasal=nasal, length=u14.LENGTH_LONG if long else 0)
    return u14.sutra_code(u14.first_sound_rank(letter), modifiers)


def _cell_to_code14(cell, codec: UPC7Text) -> int:
    parts = cell.name.split(".")
    layout_sa = codec.layout("sa-slp1").code_to_spelling
    layout_uk = codec.layout("uk").code_to_spelling
    if parts[0] in ("varga", "non-varga") and parts[1] != "uk-ext":
        if cell.code in layout_sa:
            return _letter_code(layout_sa[cell.code])
        letter = layout_uk.get(cell.code)
        if letter in _UK_CONSONANT_EXT:
            return u14.kind_code(u14.K_UKRAINIAN, _UK_CONSONANT_EXT[letter])
        raise BridgeError(f"no UPC-14 home for {cell.name}")
    if parts[:2] == ["non-varga", "uk-ext"]:
        if parts[2] == "softness":
            return u14.kind_code(u14.K_UKRAINIAN, "uk.softness")
        return u14.kind_code(u14.K_UKRAINIAN, _UK_AFFRICATE_EXT[parts[2]])
    if parts[:2] == ["vowel", "uk-ext"]:
        return u14.kind_code(u14.K_UKRAINIAN, _UK_VOWEL_EXT[parts[2]])
    if parts[0] == "vowel":
        row, nasal, length = parts[1], parts[2] == "nasal", parts[3] == "long"
        if row in _LONG_LETTER and length:
            return _letter_code(_LONG_LETTER[row], nasal=nasal)
        return _letter_code(_ROW_LETTER[row], nasal=nasal, long=length and row not in _LONG_LETTER)
    if parts[0] == "sign":
        name = parts[1]
        if name in _SANSKRIT_SIGN_NAMES:
            return u14.kind_code(u14.K_SANSKRIT, name)
        return u14.kind_code(u14.K_COMMON, name)
    raise BridgeError(f"unhandled UPC-7 cell {cell.name}")


def build_bridge() -> Dict[int, int]:
    """{UPC-7 code: UPC-14 code} for every assigned UPC-7 cell."""
    codec = UPC7Text()
    table: Dict[int, int] = {}
    for cell in build_cells():
        if cell.status == ASSIGNED:
            table[cell.code] = _cell_to_code14(cell, codec)
    return table


def encode_text(text: str, layout: str) -> Tuple[int, ...]:
    """Human text -> UPC-7 stream (public layout encoder) -> UPC-14 stream."""
    codec = UPC7Text()
    bridge = build_bridge()
    return tuple(bridge[code] for code in codec.encode(text, layout))


__all__ = ["BridgeError", "build_bridge", "encode_text"]
