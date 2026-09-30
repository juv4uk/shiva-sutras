#!/usr/bin/env python3
"""
UPC-14: a sutra-first 14-bit text code (shiva-sutras#44, experiment)
====================================================================

Status: EXPERIMENTAL CANDIDATE beside UPC-7. It does not replace, move or
re-pin any UPC-7 cell. UPC-7 stays the ratified Text7 authority; this module
asks whether a 14-bit code with the Siva-sutras as its *basis* is cleaner.

Why 14: an FPGA cell is 4 tag + 28 value bits (fpga-lisp README), and
28 = 2 x 14 = 4 x 7, so 14 divides the payload with no waste.

    code = K(2) | R(6) | M(6)

    K = 00  siva-sutra   R = rank in the 14 sutras (0..56), M = modifiers
    K = 01  sanskrit     R = index of a Sanskrit sign
    K = 10  ukrainian    R = index of a sound the sutras do not contain
    K = 11  common       R = index of a common sign / text digit

The order of codes IS the order of the sutras: for K=00 the numeric order of
`R` is the order in which the sounds and it-markers are recited. So a
pratyahara is an interval of `R`, with `M` ignored (long, nasal and accented
forms are included automatically, as savarna requires). No mask table.

Design rules, each checked in `test_upc14.py`:

* The sutra table is data written here from the 14 sutras, not imported from
  any UPC-7/UPC-8 module. UPC-7 is used only by the *bridge*.
* An it-marker has its own rank: `N` the marker of sutra 3 and `N` the nasal
  sound of sutra 7 are different codes (role is position).
* Nothing is guessed. A combination with no honest meaning is invalid and
  fails closed (a modifier on a consonant, a rank past 56, a spare bit set).
* `ha` occurs twice in the sutras (5 and 14). Both ranks exist so that the
  sutra text can be written; ordinary text uses the first, and both decode to
  the same sound. This is the one documented exception to one-code-per-sound.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List, Optional, Tuple

# ---------------------------------------------------------------------------
# The 14 sutras, in SLP1. The LAST token of each sutra is its it-marker.
# ---------------------------------------------------------------------------

SUTRAS: Tuple[Tuple[str, ...], ...] = (
    ("a", "i", "u", "R"),
    ("f", "x", "k"),
    ("e", "o", "N"),
    ("E", "O", "c"),
    ("h", "y", "v", "r", "w"),
    ("l", "R"),
    ("Y", "m", "N", "R", "n", "m"),
    ("J", "B", "Y"),
    ("G", "Q", "D", "z"),
    ("j", "b", "g", "q", "d", "S"),
    ("K", "P", "C", "W", "T", "c", "w", "t", "v"),
    ("k", "p", "y"),
    ("S", "z", "s", "r"),
    ("h", "l"),
)

# IAST for every SLP1 letter that occurs in the sutras.
IAST = {
    "a": "a", "i": "i", "u": "u", "f": "ṛ", "x": "ḷ", "e": "e", "o": "o",
    "E": "ai", "O": "au", "h": "h", "y": "y", "v": "v", "r": "r", "l": "l",
    "Y": "ñ", "m": "m", "N": "ṅ", "R": "ṇ", "n": "n", "J": "jh", "B": "bh",
    "G": "gh", "Q": "ḍh", "D": "dh", "j": "j", "b": "b", "g": "g", "q": "ḍ",
    "d": "d", "K": "kh", "P": "ph", "C": "ch", "W": "ṭh", "T": "th", "c": "c",
    "w": "ṭ", "t": "t", "k": "k", "p": "p", "S": "ś", "z": "ṣ", "s": "s",
}

SOUND, MARKER = "sound", "marker"


@dataclass(frozen=True)
class Position:
    """One place in the recited order of the sutras."""

    rank: int
    slp1: str
    role: str  # SOUND or MARKER
    sutra: int  # 1..14

    @property
    def iast(self) -> str:
        return IAST[self.slp1]


def _build_positions() -> Tuple[Position, ...]:
    out: List[Position] = []
    for number, sutra in enumerate(SUTRAS, start=1):
        for index, letter in enumerate(sutra):
            role = MARKER if index == len(sutra) - 1 else SOUND
            out.append(Position(len(out), letter, role, number))
    return tuple(out)


POSITIONS: Tuple[Position, ...] = _build_positions()
RANK_COUNT = len(POSITIONS)  # 57

VOWEL_LETTERS = ("a", "i", "u", "f", "x", "e", "o", "E", "O")
SHORT_LONG_VOWELS = ("a", "i", "u", "f", "x")  # have a length modifier
ALWAYS_LONG = ("e", "o", "E", "O")  # long by nature: no length modifier

# ---------------------------------------------------------------------------
# Code layout
# ---------------------------------------------------------------------------

K_SUTRA, K_SANSKRIT, K_UKRAINIAN, K_COMMON = 0, 1, 2, 3
KIND_NAMES = ("sutra", "sanskrit", "ukrainian", "common")

WIDTH = 14
CODE_MAX = (1 << WIDTH) - 1

# M = accent(2) spare(1) nasal(1) length(2)   (K = 00 only)
ACCENT_NONE, ACCENT_UDATTA, ACCENT_ANUDATTA, ACCENT_SVARITA = 0, 1, 2, 3
LENGTH_PLAIN, LENGTH_LONG = 0, 1  # 2, 3 are reserved


class UPC14Error(ValueError):
    """Base error."""


class InvalidCode(UPC14Error):
    """The bits do not name a cell. Fail closed; never repair."""


def make_code(kind: int, rank: int, modifiers: int = 0) -> int:
    if not 0 <= kind < 4:
        raise UPC14Error(f"invalid kind: {kind}")
    if not 0 <= rank < 64:
        raise UPC14Error(f"invalid rank field: {rank}")
    if not 0 <= modifiers < 64:
        raise UPC14Error(f"invalid modifier field: {modifiers}")
    return (kind << 12) | (rank << 6) | modifiers


def modifiers_of(accent: int = 0, nasal: bool = False, length: int = 0) -> int:
    if not 0 <= accent < 4 or not 0 <= length < 4:
        raise UPC14Error("modifier out of range")
    return (accent << 4) | (int(bool(nasal)) << 2) | length


def split(code: int) -> Tuple[int, int, int]:
    if not 0 <= code <= CODE_MAX:
        raise InvalidCode(f"not a 14-bit code: {code!r}")
    return code >> 12, (code >> 6) & 0b111111, code & 0b111111


def bits(code: int) -> str:
    return format(code, "014b")


def sutra_code(rank: int, modifiers: int = 0) -> int:
    return make_code(K_SUTRA, rank, modifiers)


# ---------------------------------------------------------------------------
# Meaning of a K=00 cell
# ---------------------------------------------------------------------------


def position_of_rank(rank: int) -> Position:
    if not 0 <= rank < RANK_COUNT:
        raise InvalidCode(f"rank {rank} is past the last position ({RANK_COUNT - 1})")
    return POSITIONS[rank]


def first_sound_rank(letter: str) -> int:
    """Rank of the first occurrence of `letter` as a SOUND (h -> sutra 5)."""
    for position in POSITIONS:
        if position.slp1 == letter and position.role == SOUND:
            return position.rank
    raise UPC14Error(f"{letter!r} is not a sound of the sutras")


def is_vowel_rank(rank: int) -> bool:
    position = position_of_rank(rank)
    return position.role == SOUND and position.slp1 in VOWEL_LETTERS


def validate(code: int) -> None:
    """Raise InvalidCode unless `code` names a defined cell of this candidate."""
    kind, rank, modifiers = split(code)
    if kind == K_SUTRA:
        position = position_of_rank(rank)
        accent, spare, nasal, length = (
            modifiers >> 4, (modifiers >> 3) & 1, (modifiers >> 2) & 1, modifiers & 3,
        )
        if spare:
            raise InvalidCode(f"spare modifier bit set: {bits(code)}")
        if length not in (LENGTH_PLAIN, LENGTH_LONG):
            raise InvalidCode(f"reserved length value: {bits(code)}")
        if modifiers and not (position.role == SOUND and position.slp1 in VOWEL_LETTERS):
            raise InvalidCode(f"modifiers on a non-vowel: {bits(code)}")
        if length == LENGTH_LONG and position.slp1 in ALWAYS_LONG:
            raise InvalidCode(f"{position.iast} is long by nature: {bits(code)}")
        return
    if modifiers:
        raise InvalidCode(f"modifiers only exist in the sutra kind: {bits(code)}")
    table = _KIND_TABLES[kind]
    if rank >= len(table):
        raise InvalidCode(f"no {KIND_NAMES[kind]} cell {rank}: {bits(code)}")


# ---------------------------------------------------------------------------
# Pratyahara = an interval of ranks
# ---------------------------------------------------------------------------


def marker_rank_after(start_rank: int, marker: str, nth: int = 1) -> int:
    """Rank of the `nth` marker `marker` after `start_rank`.

    `nth=1` is the ordinary rule (Panini 1.1.71: the first such marker). The
    classical `an` is used with both the marker of sutra 1 and the one of
    sutra 6; in rank terms that is simply `nth=1` and `nth=2`.
    """
    seen = 0
    for position in POSITIONS[start_rank + 1:]:
        if position.role == MARKER and position.slp1 == marker:
            seen += 1
            if seen == nth:
                return position.rank
    raise UPC14Error(f"no marker {marker!r} (occurrence {nth}) after rank {start_rank}")


def pratyahara_interval(start: str, marker: str, nth: int = 1) -> Tuple[int, int]:
    """`(first_rank, marker_rank)`: the sounds are the SOUND ranks in [first, marker)."""
    first = first_sound_rank(start)
    return first, marker_rank_after(first, marker, nth)


def pratyahara_ranks(start: str, marker: str, nth: int = 1) -> Tuple[int, ...]:
    first, end = pratyahara_interval(start, marker, nth)
    return tuple(p.rank for p in POSITIONS[first:end] if p.role == SOUND)


def in_pratyahara(code: int, first: int, end: int) -> bool:
    """Membership is two comparisons on the rank field; the modifiers are ignored."""
    kind, rank, _ = split(code)
    if kind != K_SUTRA or not first <= rank < end:
        return False
    return POSITIONS[rank].role == SOUND  # an it-marker inside the interval is not a member


def pratyahara_letters(start: str, marker: str, nth: int = 1) -> Tuple[str, ...]:
    return tuple(POSITIONS[r].slp1 for r in pratyahara_ranks(start, marker, nth))


# ---------------------------------------------------------------------------
# Kinds 01, 10, 11: closed name tables. Order = index. Names, not spellings.
# ---------------------------------------------------------------------------

SANSKRIT_SIGNS = ("anusvara", "visarga", "avagraha", "danda", "double-danda")

# Sounds the sutras do not contain, in the order UPC-7 lists them.
UKRAINIAN_EXT = (
    "uk.kh", "uk.zh", "uk.z", "uk.f", "uk.h-voiced",  # consonants outside the sutras
    "uk.a", "uk.e", "uk.o", "uk.y",                    # vowels outside the sutras
    "uk.ts", "uk.tsh", "uk.dz", "uk.dzh",              # affricates
    "uk.softness",
)

# The 27 human-surface signs UPC-7 keeps in class 11 (the other 5 are Sanskrit).
COMMON_SIGNS = (
    "space", "newline", "tab", "left-paren", "right-paren", "double-quote",
    "backslash", "underscore", "ampersand", "pipe", "backquote", "plus", "minus",
    "star", "slash", "equals", "less", "greater", "question", "bang",
    "apostrophe", "dot", "comma", "colon", "semicolon", "hash", "at",
)
# CANDIDATE, not ratified (#34): text digits, kept apart from Number.
TEXT_DIGITS = tuple(f"digit-{d}" for d in "0123456789")

_KIND_TABLES = {
    K_SANSKRIT: SANSKRIT_SIGNS,
    K_UKRAINIAN: UKRAINIAN_EXT,
    K_COMMON: COMMON_SIGNS + TEXT_DIGITS,
}


def kind_code(kind: int, name: str) -> int:
    return make_code(kind, _KIND_TABLES[kind].index(name))


# ---------------------------------------------------------------------------
# Describing a code (for humans; never identity)
# ---------------------------------------------------------------------------

ACCENT_NAMES = ("", "udatta", "anudatta", "svarita")


def describe(code: int) -> str:
    validate(code)
    kind, rank, modifiers = split(code)
    if kind == K_SUTRA:
        position = POSITIONS[rank]
        text = f"sutra {position.sutra} #{rank} {position.iast}"
        if position.role == MARKER:
            return text + " (it-marker)"
        extra = []
        if modifiers & 3:
            extra.append("long")
        if (modifiers >> 2) & 1:
            extra.append("nasal")
        if modifiers >> 4:
            extra.append(ACCENT_NAMES[modifiers >> 4])
        return text + (" [" + ",".join(extra) + "]" if extra else "")
    return f"{KIND_NAMES[kind]} {_KIND_TABLES[kind][rank]}"


def all_valid_codes() -> Tuple[int, ...]:
    out = []
    for code in range(CODE_MAX + 1):
        try:
            validate(code)
        except InvalidCode:
            continue
        out.append(code)
    return tuple(out)


__all__ = [
    "ACCENT_NAMES", "CODE_MAX", "COMMON_SIGNS", "InvalidCode", "MARKER", "POSITIONS",
    "RANK_COUNT", "SANSKRIT_SIGNS", "SHORT_LONG_VOWELS", "SOUND", "SUTRAS",
    "TEXT_DIGITS", "UKRAINIAN_EXT", "UPC14Error", "WIDTH", "all_valid_codes", "bits",
    "describe", "first_sound_rank", "in_pratyahara", "kind_code", "make_code",
    "marker_rank_after", "modifiers_of", "position_of_rank", "pratyahara_interval",
    "pratyahara_letters", "pratyahara_ranks", "split", "sutra_code", "validate",
]
