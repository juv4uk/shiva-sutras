#!/usr/bin/env python3
"""VARṆA-7 — a 7-bit sound-identity codec  (my design).

Design idea
-----------
The existing UPC-7 partitions its 7 bits by *category* (varga / non-varga /
vowel / sign). VARṆA-7 partitions them by **prayatna (articulatory effort)**,
the four internal efforts the Kāśikā names on sūtra 1.1.9:

    spṛṣṭa        full contact      -> the 25 stop consonants (varga)
    īṣat-spṛṣṭa   slight contact    -> the 4 semivowels
    ūṣman         breath / friction -> the 3 sibilants + h
    vivṛta        open              -> the vowels
    + a saṃjñā region for meta cells (it-markers, signs, extensions)

Layout (CCxxxxx):  2-bit region + 5-bit payload

    00  SPARSA   payload = place*5 + member        25 used, 7 reserved
    01  ANTAS    payload = place(3) | kind(2)      8 used, 24 reserved
    10  SVARA    payload = row(3) | nasal | length  28 used, 4 reserved
    11  SAMJNA   payload = index(5)                32 named

VARṆA-7 is an *identity* codec: every distinct sound/sign is one cell, and the
SLP1 spelling round-trips. It is the phonetic twin of UPC-7, not a replacement
for it, and it is deliberately *not* a claim about Pāṇini.

Known limit (documented, not hidden): with only a length bit for the e/o rows,
`e` and `ai` share a row and differ by the length bit — exactly as in UPC-7.
So a length-based savarṇa test would wrongly call e and ai savarṇa. VARṆA-7
therefore exposes savarṇa as a *function* with that caveat, and the companion
14-bit code PRĀṆA-14 carries a separate `wide` bit that fixes it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

WIDTH = 7
MAX_CODE = (1 << WIDTH) - 1  # 0x7F

REGION_SHIFT = 5
PAYLOAD_MASK = 0x1F

SPARSA = 0b00
ANTAS = 0b01
SVARA = 0b10
SAMJNA = 0b11

REGION_NAMES = {
    SPARSA: "sparśa",
    ANTAS: "antastha/ūṣman",
    SVARA: "svara",
    SAMJNA: "saṃjñā",
}


class VarnaError(ValueError):
    """Anything that is not a well-formed VARṆA-7 cell. Fail closed."""


def checked(code: int) -> int:
    if not isinstance(code, int) or isinstance(code, bool):
        raise VarnaError(f"code must be int, got {type(code).__name__}")
    if not 0 <= code <= MAX_CODE:
        raise VarnaError(f"outside the 7-bit domain: {code!r}")
    return code


def make(region: int, payload: int) -> int:
    if region not in REGION_NAMES:
        raise VarnaError(f"invalid region: {region!r}")
    if not 0 <= payload <= PAYLOAD_MASK:
        raise VarnaError(f"invalid 5-bit payload: {payload!r}")
    return (region << REGION_SHIFT) | payload


def region_of(code: int) -> int:
    return checked(code) >> REGION_SHIFT


def payload_of(code: int) -> int:
    return checked(code) & PAYLOAD_MASK


def bits(code: int) -> str:
    return f"{checked(code):07b}"


# --------------------------------------------------------------------------
# 00 SPARSA — the 25 stops
# --------------------------------------------------------------------------

SPARSA_PLACES = ("throat", "palate", "roof", "teeth", "lips")
SPARSA_MEMBERS = ("unvoiced", "unvoiced-aspirated", "voiced", "voiced-aspirated", "nasal")


def sparsa_code(place: int, member: int) -> int:
    if not 0 <= place < 5:
        raise VarnaError(f"invalid sparśa place: {place}")
    if not 0 <= member < 5:
        raise VarnaError(f"invalid sparśa member: {member}")
    return make(SPARSA, place * 5 + member)


def decode_sparsa(code: int) -> Tuple[int, int]:
    if region_of(code) != SPARSA:
        raise VarnaError("not a sparśa cell")
    payload = payload_of(code)
    if payload >= 25:
        raise VarnaError("reserved sparśa payload")
    return divmod(payload, 5)


# --------------------------------------------------------------------------
# 01 ANTAS — semivowels, sibilants, h
# --------------------------------------------------------------------------

ANTAS_PLACES = ("throat", "palate", "roof", "teeth", "lips", "glottal", "reserved6", "reserved7")
ANTAS_KINDS = ("voiceless-fricative", "voiced-fricative", "sonorant", "lateral")


def antas_code(place: int, kind: int) -> int:
    if not 0 <= place < 8:
        raise VarnaError(f"invalid antas place: {place}")
    if not 0 <= kind < 4:
        raise VarnaError(f"invalid antas kind: {kind}")
    return make(ANTAS, (place << 2) | kind)


def decode_antas(code: int) -> Tuple[int, int]:
    if region_of(code) != ANTAS:
        raise VarnaError("not an antas cell")
    payload = payload_of(code)
    return payload >> 2, payload & 0b11


def antas_effort(kind: int) -> str:
    """fricatives are ūṣman; sonorants/laterals are īṣat-spṛṣṭa."""
    return "ūṣman" if kind in (0, 1) else "īṣat-spṛṣṭa"


# --------------------------------------------------------------------------
# 10 SVARA — the vowels
# --------------------------------------------------------------------------

SVARA_ROWS = ("a", "i", "u", "ṛ", "ḷ", "e", "o")


def svara_code(row: int, nasal: bool = False, length: bool = False) -> int:
    if not 0 <= row < 7:
        raise VarnaError(f"invalid svara row: {row}")
    payload = (row << 2) | (int(bool(nasal)) << 1) | int(bool(length))
    return make(SVARA, payload)


def decode_svara(code: int) -> Tuple[int, bool, bool]:
    if region_of(code) != SVARA:
        raise VarnaError("not a svara cell")
    payload = payload_of(code)
    row = payload >> 2
    if row == 7:
        raise VarnaError("svara row 7 is reserved")
    return row, bool((payload >> 1) & 1), bool(payload & 1)


# --------------------------------------------------------------------------
# 11 SAMJNA — meta cells (signs / it-markers / extensions)
# --------------------------------------------------------------------------

SAMJNA_NAMES = (
    "space", "newline", "tab", "left-paren", "right-paren", "double-quote",
    "backslash", "underscore", "anusvara", "visarga", "avagraha", "danda",
    "double-danda", "ampersand", "pipe", "backquote", "plus", "minus", "star",
    "slash", "equals", "less", "greater", "question", "bang", "apostrophe",
    "dot", "comma", "colon", "semicolon", "hash", "at",
)
assert len(SAMJNA_NAMES) == 32

SAMJNA_CODE: Dict[str, int] = {n: make(SAMJNA, i) for i, n in enumerate(SAMJNA_NAMES)}
CODE_SAMJNA: Dict[int, str] = {c: n for n, c in SAMJNA_CODE.items()}


def samjna_code(name: str) -> int:
    try:
        return SAMJNA_CODE[name]
    except KeyError as exc:
        raise VarnaError(f"unknown saṃjñā cell: {name!r}") from exc


def samjna_name(code: int) -> str:
    if region_of(code) != SAMJNA:
        raise VarnaError("not a saṃjñā cell")
    return CODE_SAMJNA[code]


# --------------------------------------------------------------------------
# The sound table: SLP1 spelling -> VARṆA-7 cell
# --------------------------------------------------------------------------

SOUND_SLP1: Dict[str, int] = {}

# 25 stops (SLP1: k K g G N / c C j J Y / w W q Q R / t T d D n / p P b B m)
_STOP_SLP1 = (
    ("k", "K", "g", "G", "N"),
    ("c", "C", "j", "J", "Y"),
    ("w", "W", "q", "Q", "R"),
    ("t", "T", "d", "D", "n"),
    ("p", "P", "b", "B", "m"),
)
for _p, _row in enumerate(_STOP_SLP1):
    for _m, _s in enumerate(_row):
        SOUND_SLP1[_s] = sparsa_code(_p, _m)

# 8 antastha / ūṣman
for _s, _p, _k in (("y", 1, 2), ("r", 2, 2), ("l", 3, 3), ("v", 4, 2),
                   ("S", 1, 0), ("z", 2, 0), ("s", 3, 0), ("h", 0, 1)):
    SOUND_SLP1[_s] = antas_code(_p, _k)

# vowels: short and long. E = ai (long form of e), O = au (long form of o).
_VOWEL_SLP1 = (
    ("a", "A"), ("i", "I"), ("u", "U"), ("f", "F"), ("x", "X"),
    ("e", "E"), ("o", "O"),
)
for _r, (_short, _long) in enumerate(_VOWEL_SLP1):
    SOUND_SLP1[_short] = svara_code(_r, length=False)
    SOUND_SLP1[_long] = svara_code(_r, length=True)

# Sanskrit signs
SOUND_SLP1["M"] = samjna_code("anusvara")
SOUND_SLP1["H"] = samjna_code("visarga")

CODE_TO_SLP1: Dict[int, str] = {}
for _s, _c in SOUND_SLP1.items():
    if _c in CODE_TO_SLP1:
        raise VarnaError(f"cell collision at {bits(_c)}: {_s} and {CODE_TO_SLP1[_c]}")
    CODE_TO_SLP1[_c] = _s

# longest-match keys for encoding
_ENC_KEYS = sorted(SOUND_SLP1, key=len, reverse=True)


def encode_slp1(text: str) -> Tuple[int, ...]:
    """Encode an SLP1 string to a tuple of VARṆA-7 cells (longest match)."""
    out: List[int] = []
    i = 0
    while i < len(text):
        for key in _ENC_KEYS:
            if text.startswith(key, i):
                out.append(SOUND_SLP1[key])
                i += len(key)
                break
        else:
            raise VarnaError(f"cannot encode SLP1 at position {i}: {text[i:]!r}")
    return tuple(out)


def render_slp1(codes: Tuple[int, ...]) -> str:
    out = []
    for c in codes:
        if c not in CODE_TO_SLP1:
            raise VarnaError(f"cell {bits(c)} has no SLP1 spelling")
        out.append(CODE_TO_SLP1[c])
    return "".join(out)


# --------------------------------------------------------------------------
# savarṇa — same place and same effort (1.1.9)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SavarnaKey:
    region: int
    place: int
    effort: str


def savarna_key(code: int) -> SavarnaKey:
    region = region_of(code)
    if region == SPARSA:
        place, _member = decode_sparsa(code)
        return SavarnaKey(region, place, "spṛṣṭa")
    if region == ANTAS:
        place, kind = decode_antas(code)
        return SavarnaKey(region, place, antas_effort(kind))
    if region == SVARA:
        row, _nasal, _length = decode_svara(code)
        return SavarnaKey(region, row, "vivṛta")
    raise VarnaError("a saṃjñā cell is not a sound; savarṇa is undefined")


def savarna(a: int, b: int) -> bool:
    """1.1.9: same place, same effort.

    Exact for stops, semivowels, sibilants, h, and the a/i/u/ṛ/ḷ vowel rows.
    On the e/o rows, ai/au are stored as the 'long' variant (UPC-7 convention),
    so e and ai share a key — a known 7-bit imprecision, fixed in PRĀṆA-14.
    """
    return savarna_key(a) == savarna_key(b)


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------


def _selftest() -> None:
    # 1. every sound round-trips through SLP1
    for s, c in SOUND_SLP1.items():
        assert render_slp1((c,)) == s, (s, bits(c))
        assert encode_slp1(s) == (c,), (s,)
    # 2. no cell collision among sounds
    assert len(set(SOUND_SLP1.values())) == len(SOUND_SLP1)
    # 3. sparśa grid: 25 cells, 5x5
    assert len({sparsa_code(p, m) for p in range(5) for m in range(5)}) == 25
    # 4. savarṇa spot-checks (Kāśikā 1.1.9)
    assert savarna(SOUND_SLP1["k"], SOUND_SLP1["g"])        # same varga
    assert savarna(SOUND_SLP1["k"], SOUND_SLP1["N"])        # nasal stop too
    assert not savarna(SOUND_SLP1["k"], SOUND_SLP1["c"])    # different place
    assert savarna(SOUND_SLP1["a"], SOUND_SLP1["A"])        # a / ā
    assert savarna(SOUND_SLP1["i"], SOUND_SLP1["I"])        # i / ī
    assert not savarna(SOUND_SLP1["i"], SOUND_SLP1["y"])    # vowel vs semivowel
    assert not savarna(SOUND_SLP1["S"], SOUND_SLP1["s"])    # different place
    # 5. multi-sound encode / decode
    assert render_slp1(encode_slp1("kfta")) == "kfta"
    assert render_slp1(encode_slp1("saMskfta")) == "saMskfta"
    # 6. reject non-sound savarṇa
    try:
        savarna(samjna_code("space"), SOUND_SLP1["a"])
        raise AssertionError("saṃjñā cell must not be a sound")
    except VarnaError:
        pass
    # 7. reserved rows/cells fail closed
    bad = make(SVARA, (7 << 2))  # raw row-7 cell: constructible, must not decode
    try:
        decode_svara(bad)
        raise AssertionError("row 7 must be rejected on decode")
    except VarnaError:
        pass
    try:
        svara_code(7)
        raise AssertionError("row 7 must be rejected by the constructor")
    except VarnaError:
        pass
    try:
        decode_sparsa(sparsa_code(0, 0) | 0)  # sanity: a real cell decodes
    except VarnaError:
        raise AssertionError("a real sparśa cell must decode")
    try:
        decode_sparsa(make(SPARSA, 25))  # first reserved sparśa payload
        raise AssertionError("reserved sparśa payload must be rejected")
    except VarnaError:
        pass
    print("VARṆA-7 self-test: OK")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--selftest"] or not sys.argv[1:]:
        _selftest()
        if not sys.argv[1:]:
            print()
            for s, c in sorted(SOUND_SLP1.items(), key=lambda kv: kv[1]):
                print(f"  {bits(c)}  {c:3d}  0x{c:02X}  {REGION_NAMES[region_of(c)]:<14} {s}")
