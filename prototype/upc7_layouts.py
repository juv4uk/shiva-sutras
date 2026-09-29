#!/usr/bin/env python3
"""
UPC-7 human layouts on geometry v2 (shiva-sutras#29)
====================================================

`upc7_geometry.py` says *where* every cell of the 7-bit space lives. This
module says *how a human spells it*. A layout is a projection: it never changes
which code a sound has, it only names it.

    text ──encode(layout)──▶ UPC-7 codes ──render(other layout)──▶ text

Design rules (each one is checked in `test_upc7_layouts.py`):

* Cells come from the geometry, not from the legacy flat UPC-8 numbers.
* A layout is injective: one spelling names at most one code.
* Nothing is invented. A sound the owner has not placed in the geometry stays
  *unassigned* and fails closed, even when a neighbouring sound looks similar.
  In particular a known-but-unplaced spelling such as ``дж`` is rejected as a
  whole; it is never silently read as ``д`` followed by ``ж``.
* Layouts are total over what they claim and silent about nothing else.
* Host ``str`` is transport for humans only. The value is the tuple of ints
  0..127.

The legacy donor `upc8.py` is used for one thing only: the *inventory* of
Ukrainian spellings the project already knows about, so that they can be
rejected explicitly instead of being mis-encoded.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List, Mapping, Tuple

import upc7_geometry as geo
from upc7_geometry import (
    ASCII_SURFACE_GLYPHS,
    CLASS_NAMES,
    CURRENT_UPC8_NONVARGA,
    NONVARGA_PLACES,
    NONVARGA_SLOTS,
    SIGN_NAMES,
    VARGA_MEMBERS,
    VARGA_PLACES,
    VOWEL_ROWS,
)
from upc8 import UKRAINIAN_NEW, UKRAINIAN_SHARED


class UPC7LayoutError(ValueError):
    """Base error of the layout layer."""


class UnknownLayout(UPC7LayoutError):
    pass


class UnknownSpelling(UPC7LayoutError):
    """The text has a spelling this layout does not know at all."""


class UnassignedSpelling(UnknownSpelling):
    """The spelling is known to the project, but has no UPC-7 cell yet."""


class UnrenderableCode(UPC7LayoutError):
    """A code exists but this layout has no honest spelling for it."""


# ---------------------------------------------------------------------------
# The 128 cells
# ---------------------------------------------------------------------------

ASSIGNED = "assigned"
RESERVED = "reserved"


@dataclass(frozen=True)
class Cell:
    """One of the 128 cells. `name` is the stable structural identity."""

    code: int
    klass: str
    status: str
    name: str

    @property
    def bits(self) -> str:
        return geo.code_bits(self.code)


def _oral_or_nasal(nasal: bool) -> str:
    return "nasal" if nasal else "oral"


def _short_or_long(length: bool) -> str:
    return "long" if length else "short"


def build_cells() -> Tuple[Cell, ...]:
    """All 128 cells, derived from the geometry. Deterministic, ordered by code."""
    names: Dict[int, str] = {}

    for place, place_name in enumerate(VARGA_PLACES):
        for member, member_name in enumerate(VARGA_MEMBERS):
            names[geo.varga_code(place, member)] = f"varga.{place_name}.{member_name}"

    # Only the points the owner-corrected class-01 union actually uses.
    for legacy_code in CURRENT_UPC8_NONVARGA:
        code = geo.compress_upc8_nonvarga(legacy_code)
        place, slot = geo.decode_nonvarga(code)
        names[code] = f"non-varga.{NONVARGA_PLACES[place]}.{NONVARGA_SLOTS[slot]}"

    for row, row_name in enumerate(VOWEL_ROWS):
        for nasal in (False, True):
            for length in (False, True):
                code = geo.vowel_code(row, nasal=nasal, length=length)
                names[code] = (
                    f"vowel.{row_name}.{_oral_or_nasal(nasal)}.{_short_or_long(length)}"
                )

    for sign in SIGN_NAMES:
        names[geo.sign_code(sign)] = f"sign.{sign}"

    cells: List[Cell] = []
    for code in geo.all_codes():
        klass = CLASS_NAMES[geo.class_of(code)]
        if code in names:
            cells.append(Cell(code, klass, ASSIGNED, names[code]))
        else:
            payload = geo.payload_of(code)
            cells.append(Cell(code, klass, RESERVED, f"reserved.{klass}.{payload:05b}"))
    return tuple(cells)


# ---------------------------------------------------------------------------
# Spelling data (all of it is a projection; none of it is identity)
# ---------------------------------------------------------------------------

# Sanskrit, SLP1. Rows are varga places, columns are the five members
# (voiceless, voiceless+aspirated, voiced, voiced+aspirated, nasal).
_SLP1_VARGA = ("kKgGN", "cCjJY", "wWqQR", "tTdDn", "pPbBm")

# Vowel rows: (short, long). `e`/`o` rows carry ai/au as their long form: the
# class-10 spec (§3.3) encodes the vrddhi pair as surface length.
_SLP1_VOWELS = (("a", "A"), ("i", "I"), ("u", "U"), ("f", "F"), ("x", "X"), ("e", "E"), ("o", "O"))

# IAST spellings that the corrected class-01 union pairs with a Sanskrit sound.
_IAST_TO_SLP1 = {"ś": "S", "ṣ": "z", "y": "y", "s": "s", "r": "r", "l": "l", "v": "v", "h": "h"}

# Sanskrit-only signs (class 11). SLP1 writes these with ASCII characters that
# the ASCII sign layer also uses, so they take priority inside `sa-slp1`.
_SA_SIGNS = {
    "anusvara": "M",
    "visarga": "H",
    "avagraha": "'",
    "danda": ".",
    "double-danda": "..",
}

# Ukrainian letters the donor marks as identity aliases of a Sanskrit sound
# (UKRAINIAN_SHARED, relation segment-/system-equivalent), placed on varga
# cells. (place, member) as in `upc7_geometry`.
_UK_VARGA = {
    "к": (0, 0), "ґ": (0, 2),
    "т": (3, 0), "д": (3, 2), "н": (3, 4),
    "п": (4, 0), "б": (4, 2), "м": (4, 4),
}
# Ukrainian vowels that are identity aliases: і = i, у = u (oral, short).
_UK_VOWELS = {"і": 1, "у": 2}

# Ukrainian letters the project knows but the geometry has not placed. They are
# rejected explicitly. Base letters first, then the multi-letter phonemes the
# donor lists (palatalised consonants, affricates).
_UK_UNASSIGNED_LETTERS = ("а", "е", "о", "и", "є", "ї", "ю", "я", "ц", "ч", "щ", "ь")


def _is_cyrillic(text: str) -> bool:
    return any("Ѐ" <= ch <= "ӿ" for ch in text)


def _uk_known_unassigned(assigned: Iterable[str]) -> FrozenSet[str]:
    have = set(assigned)
    known = set(_UK_UNASSIGNED_LETTERS)
    for _, letter, _, _, _, _ in UKRAINIAN_SHARED:
        known.add(letter)
    for row in UKRAINIAN_NEW:
        known.add(row[2])
    return frozenset(s for s in known if s not in have and _is_cyrillic(s))


@dataclass(frozen=True)
class Layout:
    """A human projection over UPC-7 codes.

    `code_to_spelling` may be partial. `known_unassigned` lists spellings the
    project knows but has no cell for; encoding one of them fails closed.
    """

    name: str
    code_to_spelling: Mapping[int, str]
    known_unassigned: FrozenSet[str] = frozenset()

    def __post_init__(self) -> None:
        seen: Dict[str, int] = {}
        for code, spelling in self.code_to_spelling.items():
            geo.checked_code(code)
            if not spelling:
                raise UPC7LayoutError(f"{self.name}: empty spelling for code {code}")
            if spelling in seen and seen[spelling] != code:
                raise UPC7LayoutError(
                    f"{self.name}: spelling {spelling!r} names both "
                    f"{geo.code_bits(seen[spelling])} and {geo.code_bits(code)}"
                )
            seen[spelling] = code
        clash = self.known_unassigned & set(seen)
        if clash:
            raise UPC7LayoutError(f"{self.name}: assigned and unassigned: {sorted(clash)}")

    @property
    def spelling_to_code(self) -> Dict[str, int]:
        return {spelling: code for code, spelling in self.code_to_spelling.items()}


def _sa_slp1() -> Layout:
    spellings: Dict[int, str] = {}
    for place, letters in enumerate(_SLP1_VARGA):
        for member, letter in enumerate(letters):
            spellings[geo.varga_code(place, member)] = letter
    for row, (short, long_) in enumerate(_SLP1_VOWELS):
        spellings[geo.vowel_code(row)] = short
        spellings[geo.vowel_code(row, length=True)] = long_
    for legacy_code, forms in CURRENT_UPC8_NONVARGA.items():
        for form in forms:
            if form in _IAST_TO_SLP1:
                spellings[geo.compress_upc8_nonvarga(legacy_code)] = _IAST_TO_SLP1[form]
    for sign, glyph in _SA_SIGNS.items():
        spellings[geo.sign_code(sign)] = glyph
    for sign, glyph in ASCII_SURFACE_GLYPHS.items():
        if glyph not in _SA_SIGNS.values():  # ' and . belong to the Sanskrit signs here
            spellings[geo.sign_code(sign)] = glyph
    return Layout("sa-slp1", spellings)


def _uk() -> Layout:
    spellings: Dict[int, str] = {}
    for letter, (place, member) in _UK_VARGA.items():
        spellings[geo.varga_code(place, member)] = letter
    for letter, row in _UK_VOWELS.items():
        spellings[geo.vowel_code(row)] = letter
    for legacy_code, forms in CURRENT_UPC8_NONVARGA.items():
        for form in forms:
            if _is_cyrillic(form):
                spellings[geo.compress_upc8_nonvarga(legacy_code)] = form
    for sign, glyph in ASCII_SURFACE_GLYPHS.items():
        spellings[geo.sign_code(sign)] = glyph
    return Layout("uk", spellings, _uk_known_unassigned(spellings.values()))


LAYOUT_NAMES = ("sa-slp1", "uk", "bits")


def build_layouts() -> Dict[str, Layout]:
    """The spelling layouts. `bits` is a diagnostic view, not a language."""
    return {"sa-slp1": _sa_slp1(), "uk": _uk()}


# ---------------------------------------------------------------------------
# Codec
# ---------------------------------------------------------------------------


class UPC7Text:
    """Encode, render and switch layouts over the 7-bit code stream."""

    def __init__(self) -> None:
        self.layouts = build_layouts()
        self.cells = build_cells()

    def layout(self, name: str) -> Layout:
        try:
            return self.layouts[name]
        except KeyError:
            raise UnknownLayout(name) from None

    def encode(self, text: str, layout: str) -> Tuple[int, ...]:
        if layout == "bits":
            return self._encode_bits(text)
        chosen = self.layout(layout)
        table = chosen.spelling_to_code
        candidates = sorted(set(table) | chosen.known_unassigned, key=len, reverse=True)
        codes: List[int] = []
        index = 0
        while index < len(text):
            for spelling in candidates:
                if text.startswith(spelling, index):
                    if spelling in chosen.known_unassigned:
                        raise UnassignedSpelling(
                            f"{layout}: {spelling!r} at offset {index} has no UPC-7 cell yet"
                        )
                    codes.append(table[spelling])
                    index += len(spelling)
                    break
            else:
                raise UnknownSpelling(
                    f"{layout}: no spelling at offset {index}: {text[index:index + 8]!r}"
                )
        return tuple(codes)

    def render(self, codes: Iterable[int], layout: str) -> str:
        checked = tuple(geo.checked_code(code) for code in codes)
        if layout == "bits":
            return " ".join(geo.code_bits(code) for code in checked)
        mapping = self.layout(layout).code_to_spelling
        out: List[str] = []
        for code in checked:
            if code not in mapping:
                raise UnrenderableCode(
                    f"{layout}: {geo.code_bits(code)} has no spelling in this layout"
                )
            out.append(mapping[code])
        return "".join(out)

    def switch_layout(self, text: str, from_layout: str, to_layout: str) -> str:
        """Change only the human projection; the code stream is untouched."""
        return self.render(self.encode(text, from_layout), to_layout)

    @staticmethod
    def _encode_bits(text: str) -> Tuple[int, ...]:
        codes: List[int] = []
        for token in text.split():
            if len(token) != 7 or set(token) - {"0", "1"}:
                raise UnknownSpelling(f"bits: expected 7-bit cells, got {token!r}")
            codes.append(int(token, 2))
        return tuple(codes)


__all__ = [
    "ASSIGNED",
    "Cell",
    "LAYOUT_NAMES",
    "Layout",
    "RESERVED",
    "UPC7LayoutError",
    "UPC7Text",
    "UnassignedSpelling",
    "UnknownLayout",
    "UnknownSpelling",
    "UnrenderableCode",
    "build_cells",
    "build_layouts",
]
