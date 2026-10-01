#!/usr/bin/env python3
"""Spelling views of the 42 sounds: IAST, Devanagari and Ukrainian Cyrillic (stage 1 of removing SLP1).

The graph (`upc14v2`) never needed a spelling: a sound is its code. Its debug labels were
SLP1, which is case-sensitive (k and K are two sounds) and a third script nobody asked for.
Here are the two scripts the project keeps: IAST (lowercase Latin with diacritics) and
Devanagari. They are VIEWS: `to_iast(code)` / `to_devanagari(code)` read a code, and
`code_from_iast(text)` / `code_from_devanagari(text)` read a spelling. Identity stays the
code, never the string.

Length and nose are coordinates of the code, so they are spelled by a rule, not listed:
long vowel = the long form (ā ī ū ṝ; Devanagari आ ई ऊ ॠ), nasal = a combining tilde
(IAST) or candrabindu (Devanagari). Stage 1 keeps the SLP1 debug keys of `upc14v2.SOUNDS`
as the way the SPELLING TABLE is addressed internally; stage 2 re-keys the graph and the
tests by IAST and deletes this bridge.

A consonant in Devanagari is written bare with virama (क्), a vowel as its independent letter.

Cyrillic (`to_cyrillic`, `code_from_cyrillic`) follows the way Ukrainian and Russian Vaishnava
(Krishna-tradition) publications write Sanskrit: aspirates as a digraph with х (кх, гх, чх,
джх), diacritics as combining marks (ṭ т̣, ṇ н̣, ṅ н̇, ñ н̃, ś ш́, ṣ ш̣, ṛ р̣, ḷ л̣, long vowel with
a macron), ai = ай, au = ау. HYPOTHESIS: written from the author's memory of that practice, not
checked against a printed standard (BBT, ISKCON); there is no one official table. It is a VIEW:
a sound's identity is its code, not a Cyrillic spelling, and the choice binds nothing else.
Strings are NFC-normalised on both sides (some marks compose, ӯ).
"""

from __future__ import annotations

import unicodedata

from typing import Dict

import upc14v2 as g
import upc14v2_sandhi as sd

# one row per sound: legacy debug key -> (IAST, Devanagari, Cyrillic)
_ROWS = {
    "a": ("a", "अ", "а"), "i": ("i", "इ", "і"), "u": ("u", "उ", "у"), "f": ("ṛ", "ऋ", "р̣"), "x": ("ḷ", "ऌ", "л̣"),
    "e": ("e", "ए", "е"), "o": ("o", "ओ", "о"), "E": ("ai", "ऐ", "ай"), "O": ("au", "औ", "ау"),
    "k": ("k", "क्", "к"), "K": ("kh", "ख्", "кх"), "g": ("g", "ग्", "г"), "G": ("gh", "घ्", "гх"), "N": ("ṅ", "ङ्", "н̇"),
    "c": ("c", "च्", "ч"), "C": ("ch", "छ्", "чх"), "j": ("j", "ज्", "дж"), "J": ("jh", "झ्", "джх"), "Y": ("ñ", "ञ्", "н̃"),
    "w": ("ṭ", "ट्", "т̣"), "W": ("ṭh", "ठ्", "т̣х"), "q": ("ḍ", "ड्", "д̣"), "Q": ("ḍh", "ढ्", "д̣х"), "R": ("ṇ", "ण्", "н̣"),
    "t": ("t", "त्", "т"), "T": ("th", "थ्", "тх"), "d": ("d", "द्", "д"), "D": ("dh", "ध्", "дх"), "n": ("n", "न्", "н"),
    "p": ("p", "प्", "п"), "P": ("ph", "फ्", "пх"), "b": ("b", "ब्", "б"), "B": ("bh", "भ्", "бх"), "m": ("m", "म्", "м"),
    "y": ("y", "य्", "й"), "r": ("r", "र्", "р"), "l": ("l", "ल्", "л"), "v": ("v", "व्", "в"),
    "S": ("ś", "श्", "ш́"), "z": ("ṣ", "ष्", "ш̣"), "s": ("s", "स्", "с"), "h": ("h", "ह्", "х"),
}
_N = unicodedata.normalize
# long vowel: the long form of the base spelling (a rule on four vowels; ḷ has none)
_LONG = (
    {"a": "ā", "i": "ī", "u": "ū", "ṛ": "ṝ"},
    {"अ": "आ", "इ": "ई", "उ": "ऊ", "ऋ": "ॠ"},
    {"а": "а\u0304", "і": "і\u0304", "у": "у\u0304", "р\u0323": "р\u0323\u0304"},
)
_NASAL = ("\u0303", "\u0901", "\u0303")   # combining tilde, candrabindu, combining tilde
_SCRIPTS = ("iast", "devanagari", "cyrillic")


def _spell(code: int, column: int) -> str:
    """Spell a code: base sound, then long, then nasal (the rule, not a list)."""
    base = sd.base(code)
    v = g.unpack(code)
    key = g.LABELS_BY_CODE[base]
    text = _ROWS[key][column]
    if v.aperture >= g.VOWEL and v.length == g.LONG and key in "aiuf":
        text = _LONG[column][text]
    if v.nasal and v.aperture >= g.VOWEL:
        text += _NASAL[column]
    return _N("NFC", text)


def to_iast(code: int) -> str:
    return _spell(code, 0)


def to_devanagari(code: int) -> str:
    return _spell(code, 1)


def to_cyrillic(code: int) -> str:
    return _spell(code, 2)


def _reader(column: int) -> Dict[str, int]:
    table = {row[column]: g.SOUNDS[key] for key, row in _ROWS.items()}
    out = dict(table)
    for short, long_ in _LONG[column].items():
        out[long_] = g.e_long(table[short])
    for text, code in list(out.items()):
        if g.unpack(code).aperture >= g.VOWEL:
            out[text + _NASAL[column]] = g.e_nasal(code)
    return {_N("NFC", k): c for k, c in out.items()}


_FROM = tuple(_reader(i) for i in range(3))


def _read(text: str, column: int) -> int:
    try:
        return _FROM[column][_N("NFC", text)]
    except KeyError:
        raise g.GraphError(f"{text!r} is not a {_SCRIPTS[column]} sound of this graph") from None


def code_from_iast(text: str) -> int:
    return _read(text, 0)


def code_from_devanagari(text: str) -> int:
    return _read(text, 1)


def code_from_cyrillic(text: str) -> int:
    return _read(text, 2)


__all__ = ["code_from_cyrillic", "code_from_devanagari", "code_from_iast", "to_cyrillic", "to_devanagari", "to_iast"]
