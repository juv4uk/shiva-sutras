#!/usr/bin/env python3
"""UPC-14 v3: conservative, typed 14-bit English sound inventory (research).

All 42 historical Śiva-sūtra sound coordinates from upc14v2 are unchanged.
The v2 meta-marker range 0b10xxxxxxxxxxxx is unchanged. Newly admitted
English contrasts use 0b11xxxxxxxxxxxx, never a v2 sound or it-marker.
This is an experimental reference-accent PHONEME layer, not orthography,
not universal IPA coverage, and not an owner ratification.

Sources: extensions/english-sarvam.yaml and english-claude-sarvam.yaml
(44 reference-accent phonemes each); official IPA chart for feature names.
The split (English /t/ alveolar vs Sanskrit /t/ dental, English /v/
labiodental fricative vs Sanskrit /v/ approximant, English /ɹ/ vs trill)
is DELIBERATE. Source disagreements remain visible in the documentation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple
import unicodedata

import upc14v2 as v2

WIDTH = 14
EXT_PREFIX = 0b11 << 12
KIND_VOWEL = 1 << 11

# Consonant payload: 0 (kind) | place 4 | manner 3 | voiced 1 | secondary 3
# 11 + 0 + PPPP + MMM + V + SSS = 14 bits.
PLACES = {
    "bilabial": 1, "labiodental": 2, "dental": 3, "alveolar": 4,
    "postalveolar": 5, "palatal": 6, "velar": 7,
    "labial-velar": 8, "glottal": 9, "retroflex": 10,
    "uvular": 11, "pharyngeal": 12, "linguolabial": 13,
    "epiglottal": 14,
}
MANNERS = {
    "stop": 0, "affricate": 1, "fricative": 2, "nasal": 3,
    "approximant": 4, "lateral-approximant": 5,
    "trill": 6, "tap": 7,
}
SECONDARY = {
    "plain": 0, "aspirated": 1, "labialized": 2, "palatalized": 3,
    "velarized": 4, "pharyngealized": 5, "ejective": 6,
    "implosive": 7,
}

# Vowel payload: 1 (kind) | height 3 | backness 3 | rounded 1 |
#                long 1 | trajectory 3. Glide gives a *target class*,
# NOT an exact time-resolved articulatory or acoustic trajectory.
HEIGHTS = {
    "close": 0, "near-close": 1, "close-mid": 2, "mid": 3,
    "open-mid": 4, "near-open": 5, "open": 6,
}
BACKNESSES = {
    "front": 0, "near-front": 1, "central": 2,
    "near-back": 3, "back": 4,
}
TRAJECTORIES = {
    "steady": 0, "toward-near-front-close": 1,
    "toward-near-back-close": 2, "toward-central-mid": 3,
}

class UPC14V3Error(ValueError):
    """An unadmitted, ambiguous or non-canonical v3 representation."""


class ConsonantFeatures(NamedTuple):
    place: str
    manner: str
    voiced: bool
    secondary: str = "plain"


class VowelFeatures(NamedTuple):
    height: str
    backness: str
    rounded: bool
    long: bool
    trajectory: str = "steady"


def _key(table: dict[str, int], name: str) -> int:
    try:
        return table[name]
    except KeyError as exc:
        raise UPC14V3Error(f"unratified/unknown feature {name!r}") from exc


def pack_consonant(f: ConsonantFeatures) -> int:
    """Injective coordinate for the declared consonant-feature product."""
    if not isinstance(f.voiced, bool):
        raise UPC14V3Error("voiced must be bool")
    return (EXT_PREFIX | (_key(PLACES, f.place) << 7) |
            (_key(MANNERS, f.manner) << 4) | (int(f.voiced) << 3) |
            _key(SECONDARY, f.secondary))


def pack_vowel(f: VowelFeatures) -> int:
    """Injective coordinate for declared reference-accent vowel features."""
    if not isinstance(f.rounded, bool) or not isinstance(f.long, bool):
        raise UPC14V3Error("rounded/long must be bool")
    return (EXT_PREFIX | KIND_VOWEL | (_key(HEIGHTS, f.height) << 8) |
            (_key(BACKNESSES, f.backness) << 5) |
            (int(f.rounded) << 4) | (int(f.long) << 3) |
            _key(TRAJECTORIES, f.trajectory))


def unpack_extension(code: int) -> ConsonantFeatures | VowelFeatures:
    """Invert *all* valid feature coordinates; not an admission decision."""
    if type(code) is not int or not 0 <= code < (1 << WIDTH) or code >> 12 != 0b11:
        raise UPC14V3Error("not a v3 14-bit sound extension")
    if code & KIND_VOWEL:
        h = (code >> 8) & 7
        b = (code >> 5) & 7
        glide = code & 7
        if h not in HEIGHTS.values() or b not in BACKNESSES.values() or glide not in TRAJECTORIES.values():
            raise UPC14V3Error("invalid vowel feature coordinate")
        rev_h = {value: name for name, value in HEIGHTS.items()}
        rev_b = {value: name for name, value in BACKNESSES.items()}
        rev_g = {value: name for name, value in TRAJECTORIES.items()}
        return VowelFeatures(rev_h[h], rev_b[b], bool(code & 16),
                             bool(code & 8), rev_g[glide])
    p = (code >> 7) & 15
    m = (code >> 4) & 7
    sec = code & 7
    if p not in PLACES.values():
        raise UPC14V3Error("invalid consonant place")
    rev_p = {value: name for name, value in PLACES.items()}
    rev_m = {value: name for name, value in MANNERS.items()}
    rev_s = {value: name for name, value in SECONDARY.items()}
    return ConsonantFeatures(rev_p[p], rev_m[m], bool(code & 8), rev_s[sec])


@dataclass(frozen=True)
class EnglishPhoneme:
    ipa: str
    code: int
    family: str
    evidence: str
    features: ConsonantFeatures | VowelFeatures | None
    v2_label: str | None = None


# Seven shared *segment* identities, NEVER a claim that English /p/ and
# Sanskrit /p/ have the same phonemic aspiration system or phonotactics.
# /p/, /k/: aspirated English onset is a conditioned ALLOPHONE, not v2 /ph/.
# /j/: IPA palatal glide is v2 sound labelled "y" in IAST.
SHARED_SEGMENTS = (
    ("p", "p", "contextual-aspiration"),
    ("b", "b", "independent-segment-agreement"),
    ("k", "k", "contextual-aspiration"),
    ("ɡ", "g", "independent-segment-agreement"),
    ("m", "m", "independent-segment-agreement"),
    ("ŋ", "ṅ", "independent-segment-agreement"),
    ("j", "y", "segment-with-profile-status"),
)

# Distinct English 14-bit EXTENSIONS, not approximated to Sanskrit s/t/v/h/r/l.
# IPA /t͡ʃ/ and /d͡ʒ/ are ONE affricate phoneme each in this profile.
NEW_CONSONANTS = (
    ("t", "alveolar", "stop", False),
    ("d", "alveolar", "stop", True),
    ("t͡ʃ", "postalveolar", "affricate", False),
    ("d͡ʒ", "postalveolar", "affricate", True),
    ("f", "labiodental", "fricative", False),
    ("v", "labiodental", "fricative", True),
    ("θ", "dental", "fricative", False),
    ("ð", "dental", "fricative", True),
    ("s", "alveolar", "fricative", False),
    ("z", "alveolar", "fricative", True),
    ("ʃ", "postalveolar", "fricative", False),
    ("ʒ", "postalveolar", "fricative", True),
    ("h", "glottal", "fricative", False),
    ("n", "alveolar", "nasal", True),
    ("w", "labial-velar", "approximant", True),
    ("ɹ", "postalveolar", "approximant", True),
    ("l", "alveolar", "lateral-approximant", True),
)

# British/reference-accent 12 monophthongs + 8 diphthongs.
# Tuple = (IPA, height, backness, rounded, phonological length, glide).
# The e-symbol follows the source inventories' DRESS /e/ convention,
# not a claim that the measured realization is always cardinal [e].
NEW_VOWELS = (
    ("ɪ", "near-close", "near-front", False, False, "steady"),
    ("e", "close-mid", "front", False, False, "steady"),
    ("æ", "near-open", "front", False, False, "steady"),
    ("ɒ", "open", "back", True, False, "steady"),
    ("ʌ", "open-mid", "central", False, False, "steady"),
    ("ʊ", "near-close", "near-back", True, False, "steady"),
    ("ə", "mid", "central", False, False, "steady"),
    ("iː", "close", "front", False, True, "steady"),
    ("ɑː", "open", "back", False, True, "steady"),
    ("ɔː", "open-mid", "back", True, True, "steady"),
    ("uː", "close", "back", True, True, "steady"),
    ("ɜː", "open-mid", "central", False, True, "steady"),
    ("eɪ", "close-mid", "front", False, False, "toward-near-front-close"),
    ("aɪ", "open", "front", False, False, "toward-near-front-close"),
    ("ɔɪ", "open-mid", "back", True, False, "toward-near-front-close"),
    ("aʊ", "open", "front", False, False, "toward-near-back-close"),
    ("əʊ", "mid", "central", False, False, "toward-near-back-close"),
    ("ɪə", "near-close", "near-front", False, False, "toward-central-mid"),
    ("eə", "close-mid", "front", False, False, "toward-central-mid"),
    ("ʊə", "near-close", "near-back", True, False, "toward-central-mid"),
)


def _build_inventory() -> tuple[EnglishPhoneme, ...]:
    rows: list[EnglishPhoneme] = []
    for ipa, v2_label, evidence in SHARED_SEGMENTS:
        rows.append(EnglishPhoneme(ipa, v2.SOUNDS[v2_label],
                                  "consonant", evidence, None, v2_label))
    for ipa, place, manner, voiced in NEW_CONSONANTS:
        f = ConsonantFeatures(place, manner, voiced)
        rows.append(EnglishPhoneme(ipa, pack_consonant(f),
                                  "consonant", "distinct-segment", f))
    for ipa, height, back, rounded, long, trajectory in NEW_VOWELS:
        f = VowelFeatures(height, back, rounded, long, trajectory)
        rows.append(EnglishPhoneme(ipa, pack_vowel(f),
                                  "vowel", "distinct-segment", f))
    if len(rows) != 44 or len({row.ipa for row in rows}) != 44:
        raise UPC14V3Error("reference-accent phoneme inventory not 44 distinct symbols")
    if len({row.code for row in rows}) != len(rows):
        raise UPC14V3Error("two English phonemes have the same 14-bit identity")
    for row in rows:
        if row.features is not None and unpack_extension(row.code) != row.features:
            raise UPC14V3Error("sound feature coordinates failed their inverse")
    return tuple(rows)


ENGLISH = _build_inventory()
_BY_IPA = {row.ipa: row for row in ENGLISH}
_BY_CODE = {row.code: row for row in ENGLISH}


def encode_english_phoneme(ipa: str) -> int:
    """IPA transcription of ONE English phoneme, never an English word."""
    if not isinstance(ipa, str) or unicodedata.normalize("NFC", ipa) != ipa:
        raise UPC14V3Error("IPA token must be a canonical NFC string")
    try:
        return _BY_IPA[ipa].code
    except KeyError as exc:
        raise UPC14V3Error(f"not an admitted English IPA phoneme: {ipa!r}") from exc


def decode_english_phoneme(code: int) -> str:
    """Only 44 admitted English segment identities; arbitrary bits fail shut."""
    if type(code) is not int:
        raise UPC14V3Error("not an integer 14-bit code")
    try:
        return _BY_CODE[code].ipa
    except KeyError as exc:
        raise UPC14V3Error(f"not an admitted English phoneme code: {code!r}") from exc


def project_to_legacy_upc7(ipa: str) -> int | None:
    """Strict seven-bit candidate for known exact v2 sound ancestry ONLY.

    The seven inherited v2 sounds preserve the UPC-14 -> derived UPC-7 route.
    No other English phone is squeezed into a false seven-bit sound identity.
    Does NOT ratify any SENS D7 mapping or alter any seven-bit table.
    """
    row = _BY_IPA.get(ipa)
    if row is None:
        raise UPC14V3Error(f"unknown English phoneme {ipa!r}")
    if row.v2_label is None:
        return None
    from upc7_derive import derive
    return derive(row.code)


def bitstring(code: int) -> str:
    if type(code) is not int or not 0 <= code < (1 << WIDTH):
        raise UPC14V3Error("not a 14-bit word")
    return f"{code:014b}"


if __name__ == "__main__":
    for entry in ENGLISH:
        seven = project_to_legacy_upc7(entry.ipa)
        print(entry.ipa, bitstring(entry.code),
              f"7:{seven:07b}" if seven is not None else "7:UNMAPPED",
              entry.evidence)
