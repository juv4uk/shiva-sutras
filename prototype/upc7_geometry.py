#!/usr/bin/env python3
"""
UPC-7 geometric candidate (shiva-sutras#29)
============================================

Logical code shape:

    CCxxxxx
    ^^
    2-bit class
      xxxxx = 5-bit class payload

Classes:
    00 varga consonants
    01 non-varga consonants
    10 vowels
    11 signs / human-surface operator glyphs

This module is intentionally independent from prototype/upc8.py's older flat
table. It encodes the newer UPC-8 class-geometry ideas into a 7-bit candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


CLASS_VARGA = 0b00
CLASS_NONVARGA = 0b01
CLASS_VOWEL = 0b10
CLASS_SIGN = 0b11

CLASS_NAMES = {
    CLASS_VARGA: "varga",
    CLASS_NONVARGA: "non-varga",
    CLASS_VOWEL: "vowel",
    CLASS_SIGN: "sign/operator",
}

UPC7_MIN = 0
UPC7_MAX = 0x7F
PAYLOAD_MASK = 0x1F


class UPC7GeometryError(ValueError):
    pass


def checked_code(code: int) -> int:
    if not isinstance(code, int) or isinstance(code, bool):
        raise UPC7GeometryError(f"UPC-7 code must be int, got {type(code).__name__}")
    if not UPC7_MIN <= code <= UPC7_MAX:
        raise UPC7GeometryError(f"outside 7-bit UPC-7 domain: {code!r}")
    return code


def make_code(cls: int, payload: int) -> int:
    if cls not in CLASS_NAMES:
        raise UPC7GeometryError(f"invalid 2-bit class: {cls!r}")
    if not 0 <= payload <= PAYLOAD_MASK:
        raise UPC7GeometryError(f"invalid 5-bit payload: {payload!r}")
    return (cls << 5) | payload


def class_of(code: int) -> int:
    return checked_code(code) >> 5


def payload_of(code: int) -> int:
    return checked_code(code) & PAYLOAD_MASK


# ---------------------------------------------------------------------------
# class 00: varga consonants
# ---------------------------------------------------------------------------

VARGA_PLACES = ("K", "C", "T-retroflex", "T-dental", "P")
VARGA_MEMBERS = (
    "voiceless",
    "voiceless-aspirated",
    "voiced",
    "voiced-aspirated",
    "nasal",
)


def varga_code(place: int, member: int) -> int:
    if not 0 <= place < len(VARGA_PLACES):
        raise UPC7GeometryError(f"invalid varga place: {place}")
    if not 0 <= member < len(VARGA_MEMBERS):
        raise UPC7GeometryError(f"invalid varga member: {member}")
    return make_code(CLASS_VARGA, place * 5 + member)


def decode_varga(code: int) -> Tuple[int, int]:
    if class_of(code) != CLASS_VARGA:
        raise UPC7GeometryError("not a varga code")
    payload = payload_of(code)
    if payload >= 25:
        raise UPC7GeometryError("reserved varga payload")
    return divmod(payload, 5)


# ---------------------------------------------------------------------------
# class 01: non-varga consonants
# ---------------------------------------------------------------------------

NONVARGA_PLACES = (
    "K", "C", "T-retroflex", "T-dental",
    "P", "G-glottal", "U-uvular-pharyngeal", "reserved",
)

NONVARGA_SLOTS = (
    "primary-voiceless-fricative",
    "voiced-fricative",
    "primary-sonorant",
    "lateral-or-secondary-sonorant",
)


def nonvarga_code(place: int, slot: int) -> int:
    if not 0 <= place < 8:
        raise UPC7GeometryError(f"invalid non-varga place: {place}")
    if not 0 <= slot < 4:
        raise UPC7GeometryError(f"invalid non-varga slot: {slot}")
    return make_code(CLASS_NONVARGA, (place << 2) | slot)


def decode_nonvarga(code: int) -> Tuple[int, int]:
    if class_of(code) != CLASS_NONVARGA:
        raise UPC7GeometryError("not a non-varga code")
    payload = payload_of(code)
    return payload >> 2, payload & 0b11


# Current corrected UPC-8 class-01 union(Sanskrit, Ukrainian).
# Values come from the owner-designed class-01 corrected geometry.
CURRENT_UPC8_NONVARGA = {
    0x40: ("х",),
    0x48: ("ś", "ш"),
    0x49: ("ж",),
    0x4B: ("y", "й"),
    0x50: ("ṣ",),
    0x58: ("s", "с"),
    0x59: ("з",),
    0x5D: ("r", "р"),
    0x5F: ("l", "л"),
    0x60: ("ф",),
    0x63: ("v", "в"),
    0x68: ("h",),
    0x69: ("г",),
}


def compress_upc8_nonvarga(code: int) -> int:
    """Compress a currently representable UPC-8 class-01 point.

    Old geometry:
        01 ppp mm v
        ppp = place
        mm  = fricative/approximant/trill/lateral
        v   = voice

    UPC-7 keeps place and four local slots. Only distinctions used by the
    current Sanskrit∪Ukrainian union are admitted. Other old points fail
    closed rather than colliding.
    """
    if code not in CURRENT_UPC8_NONVARGA:
        raise UPC7GeometryError(
            f"UPC-8 class-01 point 0x{code:02X} is not in the current admitted union"
        )

    place = (code >> 3) & 0b111
    manner = (code >> 1) & 0b11
    voice = code & 1

    if manner == 0:       # fricative
        slot = 1 if voice else 0
    elif manner == 1 and voice:  # voiced approximant
        slot = 2
    elif manner == 2 and voice:  # voiced trill/tap
        slot = 2
    elif manner == 3 and voice:  # voiced lateral
        slot = 3
    else:
        raise UPC7GeometryError(
            f"UPC-8 class-01 point 0x{code:02X} has no collision-free UPC-7 slot"
        )

    return nonvarga_code(place, slot)


# ---------------------------------------------------------------------------
# class 10: vowels
# ---------------------------------------------------------------------------

VOWEL_ROWS = ("a", "i", "u", "r-vocalic", "l-vocalic", "e", "o")


def vowel_code(row: int, nasal: bool = False, length: bool = False) -> int:
    if not 0 <= row < 7:
        raise UPC7GeometryError(f"invalid/reserved vowel row: {row}")
    payload = (row << 2) | (int(bool(nasal)) << 1) | int(bool(length))
    return make_code(CLASS_VOWEL, payload)


def decode_vowel(code: int) -> Tuple[int, bool, bool]:
    if class_of(code) != CLASS_VOWEL:
        raise UPC7GeometryError("not a vowel code")
    payload = payload_of(code)
    row = payload >> 2
    if row == 7:
        raise UPC7GeometryError("reserved vowel row")
    return row, bool((payload >> 1) & 1), bool(payload & 1)


def compress_upc8_vowel(code: int) -> int:
    """Compress admitted UPC-8 class-10 vowel geometry to UPC-7.

    UPC-8 layout:
        10 ppp f n l
               ^
               explicit FREE bit

    UPC-7:
        10 ppp n l

    The only discarded bit must be zero. Reserved row 7 is rejected.
    """
    if not 0x80 <= code <= 0xBF:
        raise UPC7GeometryError(f"not UPC-8 class-10: 0x{code:02X}")

    row = (code >> 3) & 0b111
    free = (code >> 2) & 1
    nasal = bool((code >> 1) & 1)
    length = bool(code & 1)

    if free:
        raise UPC7GeometryError(
            f"UPC-8 vowel 0x{code:02X} uses the FREE bit; no UPC-7 identity assigned"
        )
    if row == 7:
        raise UPC7GeometryError(
            f"UPC-8 vowel 0x{code:02X} is in reserved row 7"
        )

    return vowel_code(row, nasal=nasal, length=length)


# ---------------------------------------------------------------------------
# class 11: signs and human-surface operator glyphs
# ---------------------------------------------------------------------------

SIGN_NAMES = (
    "space",
    "newline",
    "tab",
    "left-paren",
    "right-paren",
    "double-quote",
    "backslash",
    "underscore",
    "anusvara",
    "visarga",
    "avagraha",
    "danda",
    "double-danda",
    "ampersand",
    "pipe",
    "backquote",
    "plus",
    "minus",
    "star",
    "slash",
    "equals",
    "less",
    "greater",
    "question",
    "bang",
    "apostrophe",
    "dot",
    "comma",
    "colon",
    "semicolon",
    "hash",
    "at",
)

assert len(SIGN_NAMES) == 32
SIGN_CODE: Dict[str, int] = {
    name: make_code(CLASS_SIGN, index) for index, name in enumerate(SIGN_NAMES)
}
CODE_SIGN: Dict[int, str] = {code: name for name, code in SIGN_CODE.items()}

ASCII_SURFACE_GLYPHS = {
    "space": " ",
    "newline": "\n",
    "tab": "\t",
    "left-paren": "(",
    "right-paren": ")",
    "double-quote": '"',
    "backslash": "\\",
    "underscore": "_",
    "ampersand": "&",
    "pipe": "|",
    "backquote": "`",
    "plus": "+",
    "minus": "-",
    "star": "*",
    "slash": "/",
    "equals": "=",
    "less": "<",
    "greater": ">",
    "question": "?",
    "bang": "!",
    "apostrophe": "'",
    "dot": ".",
    "comma": ",",
    "colon": ":",
    "semicolon": ";",
    "hash": "#",
    "at": "@",
}


def sign_code(name: str) -> int:
    try:
        return SIGN_CODE[name]
    except KeyError as exc:
        raise UPC7GeometryError(f"unknown UPC-7 sign/operator: {name!r}") from exc


def sign_name(code: int) -> str:
    if class_of(code) != CLASS_SIGN:
        raise UPC7GeometryError("not a sign/operator code")
    return CODE_SIGN[code]


def code_bits(code: int) -> str:
    return f"{checked_code(code):07b}"


def all_codes() -> Tuple[int, ...]:
    return tuple(range(128))


__all__ = [
    "ASCII_SURFACE_GLYPHS",
    "CLASS_NAMES",
    "CLASS_NONVARGA",
    "CLASS_SIGN",
    "CLASS_VARGA",
    "CLASS_VOWEL",
    "CODE_SIGN",
    "CURRENT_UPC8_NONVARGA",
    "SIGN_CODE",
    "SIGN_NAMES",
    "UPC7GeometryError",
    "all_codes",
    "checked_code",
    "class_of",
    "code_bits",
    "compress_upc8_nonvarga",
    "compress_upc8_vowel",
    "decode_nonvarga",
    "decode_varga",
    "decode_vowel",
    "make_code",
    "nonvarga_code",
    "payload_of",
    "sign_code",
    "sign_name",
    "varga_code",
    "vowel_code",
]
