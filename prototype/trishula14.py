#!/usr/bin/env python3
"""Trishula-14: an independent typed feature cell for the 42 sounds.

Bit layout (MSB -> LSB):
    kind[3] | index[5] | variant[3] | voice[1] | aspiration[1] | length[1]

The layout is deliberately boring: every field has a declared meaning and
invalid combinations fail closed.  It is a representation experiment, not a
claim about historical phonetics or hardware.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

WIDTH = 14
MAX_CODE = (1 << WIDTH) - 1
KIND_VOWEL, KIND_STOP, KIND_SONORANT, KIND_SIBILANT, KIND_GLOTTAL = range(5)

class Trishula14Error(ValueError):
    pass
class InvalidCode(Trishula14Error):
    pass
class UnknownSound(Trishula14Error):
    pass

@dataclass(frozen=True)
class Feature:
    kind: int
    index: int
    variant: int = 0
    voice: int = 0
    aspiration: int = 0
    length: int = 0

    @property
    def code(self) -> int:
        return ((self.kind & 0b111) << 11) | ((self.index & 0b1_1111) << 6) | ((self.variant & 0b111) << 3) | ((self.voice & 1) << 2) | ((self.aspiration & 1) << 1) | (self.length & 1)


def _stop(place: int, member: int) -> Feature:
    # member: voiceless, voiceless-aspirated, voiced, voiced-aspirated, nasal
    return Feature(KIND_STOP, place, member, int(member >= 2), int(member in (1, 3)))

# A complete, collision-free canonical inventory.
FEATURES: Dict[str, Feature] = {
    **{name: Feature(KIND_VOWEL, i, length=int(name in {"ai", "au"})) for i, name in enumerate(("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au"))},
    **{name: _stop(place, member) for place, row in enumerate((("k", "kh", "g", "gh", "ṅ"), ("c", "ch", "j", "jh", "ñ"), ("ṭ", "ṭh", "ḍ", "ḍh", "ṇ"), ("t", "th", "d", "dh", "n"), ("p", "ph", "b", "bh", "m"))) for member, name in enumerate(row)},
    "y": Feature(KIND_SONORANT, 0, 0, 1), "v": Feature(KIND_SONORANT, 1, 0, 1),
    "r": Feature(KIND_SONORANT, 2, 1, 1), "l": Feature(KIND_SONORANT, 3, 2, 1),
    "ś": Feature(KIND_SIBILANT, 0, 0, 0, 1), "ṣ": Feature(KIND_SIBILANT, 1, 1, 0, 1), "s": Feature(KIND_SIBILANT, 2, 2, 0, 1),
    "h": Feature(KIND_GLOTTAL, 0, 0, 1, 1),
}
CODE_TO_SOUND = {feature.code: name for name, feature in FEATURES.items()}

# The 14 recited rows are kept as a path only for pratyāhāra queries.
SUTRAS = (("a", "i", "u", "ṇ"), ("ṛ", "ḷ", "k"), ("e", "o", "ṅ"), ("ai", "au", "c"), ("h", "y", "v", "r", "ṭ"), ("l", "ṇ"), ("ñ", "m", "ṅ", "ṇ", "n", "m"), ("jh", "bh", "ñ"), ("gh", "ḍh", "dh", "ṣ"), ("j", "b", "g", "ḍ", "d", "ś"), ("kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", "v"), ("k", "p", "y"), ("ś", "ṣ", "s", "r"), ("h", "l"))


def validate(feature: Feature) -> Feature:
    if not (0 <= feature.kind < 5 and 0 <= feature.index < 32 and 0 <= feature.variant < 8):
        raise InvalidCode(f"field outside Trishula-14 domain: {feature}")
    if feature.kind == KIND_VOWEL and feature.index > 8:
        raise InvalidCode("unknown vowel row")
    if feature.kind == KIND_STOP and feature.index > 4:
        raise InvalidCode("unknown stop place")
    if feature.kind == KIND_STOP and feature.variant > 4:
        raise InvalidCode("unknown stop member")
    if feature.kind == KIND_GLOTTAL and feature.index != 0:
        raise InvalidCode("unknown glottal slot")
    return feature


def check(code: int) -> int:
    if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code <= MAX_CODE:
        raise InvalidCode(f"not a 14-bit code: {code!r}")
    feature = Feature((code >> 11) & 7, (code >> 6) & 31, (code >> 3) & 7, (code >> 2) & 1, (code >> 1) & 1, code & 1)
    validate(feature)
    if code not in CODE_TO_SOUND:
        raise InvalidCode(f"valid fields but unassigned canonical cell: {code:014b}")
    return code


def encode(sound: str) -> int:
    try:
        return FEATURES[sound].code
    except KeyError as exc:
        raise UnknownSound(sound) from exc


def decode(code: int) -> str:
    check(code)
    return CODE_TO_SOUND[code]


def bits(code: int) -> str:
    return f"{check(code):014b}"


def parse_bits(text: str) -> Tuple[int, ...]:
    cells = tuple(text.split())
    out = []
    for cell in cells:
        if len(cell) != WIDTH or set(cell) - {"0", "1"}:
            raise InvalidCode(f"expected 14-bit cells: {cell!r}")
        out.append(check(int(cell, 2)))
    return tuple(out)


def render(codes: Iterable[int]) -> str:
    return " ".join(bits(c) for c in codes)


def pratyahara(start: str, marker: str) -> Tuple[int, ...]:
    path = tuple(token for row in SUTRAS for token in row)
    begin = path.index(start)
    for i in range(begin + 1, len(path)):
        if path[i] == marker and i == sum(len(row) for row in SUTRAS[:next(j for j, row in enumerate(SUTRAS) if marker in row and sum(len(x) for x in SUTRAS[:j + 1]) - 1 == i) + 1]) - 1:
            return tuple(encode(token) for token in path[begin:i])
    raise UnknownSound(f"marker {marker!r} not found after {start!r}")

__all__ = ["FEATURES", "Feature", "InvalidCode", "Trishula14Error", "UnknownSound", "bits", "check", "decode", "encode", "parse_bits", "pratyahara", "render"]
