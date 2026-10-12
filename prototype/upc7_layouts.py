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

    for index, ext in enumerate(geo.UK_EXT_VOWELS):
        names[geo.uk_ext_vowel_code(index)] = f"vowel.uk-ext.{ext}"
    for index, ext in enumerate(geo.UK_AFFRICATES):
        names[geo.uk_affricate_code(index)] = f"non-varga.uk-ext.{ext}"
    names[geo.softness_code()] = "non-varga.uk-ext.softness"

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

# Additional Sanskrit human projections.  These are spellings only: the UPC-7
# cell remains the identity.  Devanagari here is deliberately a direct
# cell-glyph projection, not a full orthographic compositor with matras/virama.
_IAST_VARGA = (
    ("k", "kh", "g", "gh", "ṅ"),
    ("c", "ch", "j", "jh", "ñ"),
    ("ṭ", "ṭh", "ḍ", "ḍh", "ṇ"),
    ("t", "th", "d", "dh", "n"),
    ("p", "ph", "b", "bh", "m"),
)
_DEVA_VARGA = (
    ("क", "ख", "ग", "घ", "ङ"),
    ("च", "छ", "ज", "झ", "ञ"),
    ("ट", "ठ", "ड", "ढ", "ण"),
    ("त", "थ", "द", "ध", "न"),
    ("प", "फ", "ब", "भ", "म"),
)
_IAST_VOWELS = (
    ("a", "ā"),
    ("i", "ī"),
    ("u", "ū"),
    ("ṛ", "ṝ"),
    ("ḷ", "ḹ"),
    ("e", "ai"),
    ("o", "au"),
)
_DEVA_VOWELS = (
    ("अ", "आ"),
    ("इ", "ई"),
    ("उ", "ऊ"),
    ("ऋ", "ॠ"),
    ("ऌ", "ॡ"),
    ("ए", "ऐ"),
    ("ओ", "औ"),
)
_SA_NONVARGA_PROJECTIONS = {
    "S": ("ś", "श"),
    "z": ("ṣ", "ष"),
    "y": ("y", "य"),
    "s": ("s", "स"),
    "r": ("r", "र"),
    "l": ("l", "ल"),
    "v": ("v", "व"),
    "h": ("h", "ह"),
}
_IAST_SA_SIGNS = {
    "anusvara": "ṃ",
    "visarga": "ḥ",
    "avagraha": "’",
    "danda": "।",
    "double-danda": "॥",
}
_DEVA_SA_SIGNS = {
    "anusvara": "ं",
    "visarga": "ः",
    "avagraha": "ऽ",
    "danda": "।",
    "double-danda": "॥",
}

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
_UK_UNASSIGNED_LETTERS: Tuple[str, ...] = ()

# shiva-sutras#31. Ukrainian sounds with a cell of their own in the extension
# row / extension cells (not identity aliases of a Sanskrit sound).
_UK_EXT_VOWELS = {"а": 0, "е": 1, "о": 2, "и": 3}
_UK_EXT_AFFRICATES = {"ц": 0, "ч": 1, "дз": 2, "дж": 3}
_UK_SOFTNESS = "ь"

# Spellings that are *sequences* of placed cells, not sounds of their own:
# palatalised consonants are consonant + `ь`; iotated vowels are й + vowel;
# щ is ш + ч. They encode; they are never rendered back as one letter.
_UK_SEQUENCES = {
    "щ": ("ш", "ч"),
    "є": ("й", "е"),
    "ї": ("й", "і"),
    "ю": ("й", "у"),
    "я": ("й", "а"),
}


def _is_cyrillic(text: str) -> bool:
    return any("Ѐ" <= ch <= "ӿ" for ch in text)


def _uk_known_unassigned(assigned: Iterable[str]) -> FrozenSet[str]:
    have = set(assigned)
    known = set(_UK_UNASSIGNED_LETTERS)
    for _, letter, _, _, _, _ in UKRAINIAN_SHARED:
        known.add(letter)
    for row in UKRAINIAN_NEW:
        known.add(row[2])
    placed = have | set(_UK_SEQUENCES)
    return frozenset(
        s for s in known if s not in have and _is_cyrillic(s) and not _decomposes(s, placed)
    )


def _decomposes(spelling: str, placed: set) -> bool:
    """True when `spelling` is fully covered by placed spellings (longest match)."""
    if not spelling:
        return True
    for length in range(len(spelling), 0, -1):
        if spelling[:length] in placed and _decomposes(spelling[length:], placed):
            return True
    return False


def _uk_case_aliases(
    direct_spellings: Iterable[str],
    sequences: Mapping[str, Tuple[str, ...]],
) -> Dict[str, Tuple[str, ...]]:
    """Explicit Ukrainian case aliases for input only.

    The aliases are generated once from the declared Ukrainian layout inventory.
    The encoder does not case-fold arbitrary input.  This is intentionally not
    shared with SLP1, where ASCII case can distinguish phonological identity.
    """
    direct = set(direct_spellings)
    aliases: Dict[str, Tuple[str, ...]] = {}
    for spelling in sorted(direct | set(sequences)):
        if not _is_cyrillic(spelling):
            continue
        parts = sequences.get(spelling, (spelling,))
        candidates = {
            spelling.upper(),
            spelling[:1].upper() + spelling[1:],
        }
        for alias in candidates:
            if alias == spelling:
                continue
            previous = aliases.get(alias)
            if previous is not None and previous != parts:
                raise UPC7LayoutError(
                    f"uk: case alias {alias!r} is ambiguous: {previous} vs {parts}"
                )
            aliases[alias] = tuple(parts)
    return aliases


@dataclass(frozen=True)
class Layout:
    """A human projection over UPC-7 codes.

    `code_to_spelling` may be partial. `known_unassigned` lists spellings the
    project knows but has no cell for; encoding one of them fails closed.
    """

    name: str
    code_to_spelling: Mapping[int, str]
    known_unassigned: FrozenSet[str] = frozenset()
    sequences: Mapping[str, Tuple[str, ...]] = None  # type: ignore[assignment]
    input_aliases: Mapping[str, Tuple[str, ...]] = None  # type: ignore[assignment]

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
        if self.sequences is None:
            object.__setattr__(self, "sequences", {})
        for key, parts in self.sequences.items():
            if key in seen:
                raise UPC7LayoutError(f"{self.name}: {key!r} is both a cell and a sequence")
            missing = [p for p in parts if p not in seen]
            if missing:
                raise UPC7LayoutError(f"{self.name}: sequence {key!r} uses unplaced {missing}")

        if self.input_aliases is None:
            object.__setattr__(self, "input_aliases", {})
        occupied = set(seen) | set(self.sequences) | set(self.known_unassigned)
        for alias, parts in self.input_aliases.items():
            if alias in occupied:
                raise UPC7LayoutError(
                    f"{self.name}: input alias {alias!r} shadows a canonical spelling"
                )
            missing = [p for p in parts if p not in seen]
            if missing:
                raise UPC7LayoutError(
                    f"{self.name}: input alias {alias!r} uses unplaced {missing}"
                )

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


def _sa_projection(
    name: str,
    varga_rows: Tuple[Tuple[str, ...], ...],
    vowel_rows: Tuple[Tuple[str, str], ...],
    nonvarga_index: int,
    signs: Mapping[str, str],
) -> Layout:
    """Build a Sanskrit human projection over the already assigned cells."""
    spellings: Dict[int, str] = {}
    for place, row in enumerate(varga_rows):
        for member, spelling in enumerate(row):
            spellings[geo.varga_code(place, member)] = spelling
    for row, (short, long_) in enumerate(vowel_rows):
        spellings[geo.vowel_code(row)] = short
        spellings[geo.vowel_code(row, length=True)] = long_
    for legacy_code, forms in CURRENT_UPC8_NONVARGA.items():
        for form in forms:
            slp1 = _IAST_TO_SLP1.get(form)
            if slp1 in _SA_NONVARGA_PROJECTIONS:
                spellings[geo.compress_upc8_nonvarga(legacy_code)] = (
                    _SA_NONVARGA_PROJECTIONS[slp1][nonvarga_index]
                )
    for sign, glyph in signs.items():
        spellings[geo.sign_code(sign)] = glyph
    # These layouts use distinct Sanskrit glyphs for avagraha/danda, so all
    # generic ASCII text-sign cells can remain directly available as text.
    for sign, glyph in ASCII_SURFACE_GLYPHS.items():
        spellings[geo.sign_code(sign)] = glyph
    return Layout(name, spellings)


def _sa_iast() -> Layout:
    return _sa_projection("sa-iast", _IAST_VARGA, _IAST_VOWELS, 0, _IAST_SA_SIGNS)


def _sa_deva() -> Layout:
    return _sa_projection("sa-deva", _DEVA_VARGA, _DEVA_VOWELS, 1, _DEVA_SA_SIGNS)


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
    for letter, index in _UK_EXT_VOWELS.items():
        spellings[geo.uk_ext_vowel_code(index)] = letter
    for letter, index in _UK_EXT_AFFRICATES.items():
        spellings[geo.uk_affricate_code(index)] = letter
    spellings[geo.softness_code()] = _UK_SOFTNESS
    for sign, glyph in ASCII_SURFACE_GLYPHS.items():
        spellings[geo.sign_code(sign)] = glyph
    sequences = dict(_UK_SEQUENCES)
    return Layout(
        "uk",
        spellings,
        _uk_known_unassigned(spellings.values()),
        sequences,
        _uk_case_aliases(spellings.values(), sequences),
    )


# English is a PHONEME profile, not English orthography and not Sanskrit IAST.
# Source: extensions/english-sarvam.yaml (44-phoneme SSBE candidate) independently
# compared with english-claude-sarvam.yaml. That independent annotation
# disputes the *equivalence label* for p/k (aspiration status), although
# the base phoneme slots are the same. This is a provisional, narrowly
# scoped English phonemic pilot, NOT owner-ratified universal equivalence.
# The English /j/ ↔ Sanskrit y [j] mapping is a *system-equivalent* in
# Sarvam and segment-equivalent in Claude-Sarvam; include it as separately
# qualified evidence, not as an English orthography or general proof.
# New English-only and near-equivalent phonemes gain NO seven-bit identity.
#
# These cells are already assigned in the immutable seven-bit geometry.
# No reserved bits, D2 structure, case folding or aspirated /th/ alias.
_EN_PILOT = (
    ("k", geo.varga_code(0, 0), "k"),
    ("ɡ", geo.varga_code(0, 2), "g"),
    ("ŋ", geo.varga_code(0, 4), None),
    ("p", geo.varga_code(4, 0), "p"),
    ("b", geo.varga_code(4, 2), "b"),
    ("m", geo.varga_code(4, 4), "m"),
    ("j", _sa_iast().spelling_to_code["y"], "y"),
)

# Known English phonemes/letters not sound-equivalent in the researched
# canonical Sanskrit geometry. Refuse; do not approximate e.g. "th" -> थ.
_EN_UNPLACED = frozenset((
    "th", "sh", "ch", "ph", "dh", "f", "v", "w", "r", "s", "t", "d",
    "n", "h", "l", "z", "a", "e", "i", "o", "u", "q", "x",
    "θ", "ð", "ə", "ɪ", "æ", "ʌ", "ʊ", "ʒ", "ʃ", "tʃ", "dʒ",
))


def _en() -> Layout:
    """Conservative English Roman phoneme surface, not a grapheme-to-phoneme reader.

    Only 6 one-letter sound spellings are currently admitted. For /ŋ/
    use en-ipa, not the context-sensitive English letters "ng".
    """
    spellings = {code: roman for _ipa, code, roman in _EN_PILOT if roman}
    return Layout("en", spellings, _EN_UNPLACED)


def _en_ipa() -> Layout:
    """Seven placed English candidates; only four exact across both audits."""
    spellings = {code: ipa for ipa, code, _roman in _EN_PILOT}
    return Layout("en-ipa", spellings, _EN_UNPLACED)


LAYOUT_NAMES = ("sa-slp1", "sa-iast", "sa-deva", "uk", "en", "en-ipa", "bits")


def build_layouts() -> Dict[str, Layout]:
    """The spelling layouts. `bits` is a diagnostic view, not a language."""
    return {
        "sa-slp1": _sa_slp1(),
        "sa-iast": _sa_iast(),
        "sa-deva": _sa_deva(),
        "uk": _uk(),
        "en": _en(),
        "en-ipa": _en_ipa(),
    }


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
        sequences = chosen.sequences
        aliases = chosen.input_aliases
        candidates = sorted(
            set(table) | set(sequences) | set(aliases) | chosen.known_unassigned,
            key=len,
            reverse=True,
        )
        codes: List[int] = []
        index = 0
        while index < len(text):
            for spelling in candidates:
                if text.startswith(spelling, index):
                    if spelling in chosen.known_unassigned:
                        raise UnassignedSpelling(
                            f"{layout}: {spelling!r} at offset {index} has no UPC-7 cell yet"
                        )
                    if spelling in aliases:
                        codes.extend(table[part] for part in aliases[spelling])
                    elif spelling in sequences:
                        codes.extend(table[part] for part in sequences[spelling])
                    else:
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

    def render_tokens(self, codes: Iterable[int], layout: str) -> Tuple[str, ...]:
        """Lossless single-cell spellings; TOKEN BOUNDARIES are not concatenated.

        This representation is invertible even where the visual string is
        ambiguous (IAST k+h, Ukrainian д+ж, SLP1 dot+dot).
        """
        checked = tuple(geo.checked_code(code) for code in codes)
        if layout == "bits":
            return tuple(geo.code_bits(code) for code in checked)
        mapping = self.layout(layout).code_to_spelling
        tokens: List[str] = []
        for index, code in enumerate(checked):
            if code not in mapping:
                raise UnrenderableCode(
                    f"{layout}: {geo.code_bits(code)} at {index} has no glyph"
                )
            tokens.append(mapping[code])
        return tuple(tokens)

    def encode_tokens(self, tokens: Iterable[str], layout: str) -> Tuple[int, ...]:
        """Invert render_tokens exactly; never parse across token boundaries."""
        items = tuple(tokens)
        if layout == "bits":
            codes: List[int] = []
            for spelling in items:
                if len(spelling) != 7 or set(spelling) - {"0", "1"}:
                    raise UnknownSpelling(f"bits: expected 7-bit cell, got {spelling!r}")
                codes.append(int(spelling, 2))
            return tuple(codes)
        inverse = self.layout(layout).spelling_to_code
        codes = []
        for spelling in items:
            try:
                codes.append(inverse[spelling])
            except (KeyError, TypeError):
                raise UnknownSpelling(
                    f"{layout}: {spelling!r} is not a single direct cell spelling"
                ) from None
        return tuple(codes)

    def render_checked(self, codes: Iterable[int], layout: str) -> str:
        """Only return text if the exact sequence survives decode -> encode.

        Sound codes are not text delimiters: k+h and kh, d+zh and dzh,
        a+i and ai, etc. may spell alike. Raw render() is a presentation
        view; render_checked() is a strict, reversible encoding boundary.
        """
        checked = tuple(geo.checked_code(code) for code in codes)
        rendered = self.render(checked, layout)
        try:
            reconstructed = self.encode(rendered, layout)
        except (UnknownSpelling, UnassignedSpelling) as exc:
            raise UnrenderableCode(
                f"{layout}: spelling {rendered!r} cannot recover the exact codes"
            ) from exc
        if reconstructed != checked:
            raise UnrenderableCode(
                f"{layout}: ambiguous concatenation {rendered!r}: "
                f"{tuple(geo.code_bits(c) for c in checked)} != "
                f"{tuple(geo.code_bits(c) for c in reconstructed)}"
            )
        return rendered

    def switch_layout(self, text: str, from_layout: str, to_layout: str) -> str:
        """Switch with exact 7-bit identity preserved, or refuse.

        This does not promise identical *source spelling*. Ukrainian case
        aliases and sequence spellings are intentionally many-to-one.
        """
        return self.render_checked(self.encode(text, from_layout), to_layout)

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
