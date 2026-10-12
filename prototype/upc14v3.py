#!/usr/bin/env python3
"""UPC-14 v3: English added to the EXISTING UPC-14 v2 sound graph.

Not another geometry. EXACTLY the same 14-bit field layout, bit meanings,
graph operations and 42 Śiva-sūtra vertices as prototype/upc14v2.py.
The English reference inventory contains 44 phonemes, but a mapping is
ADMITTED only when the old geometry expresses the phonetic distinction.
Unsupported phonemes are first-class evidence, not guessed bit patterns.

No change to UPC-7, SENS D7, v2 code or Sanskrit script views. Research
candidate; no owner ratification implied.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import unicodedata

import upc14v2 as graph

WIDTH = graph.WIDTH
# The sole permitted 14-bit layout (unchanged from the graph):
# meta(1) | place(5) | nasal(1) | aperture(3) | length(2) | voice(1) | asp(1)
FIELDS = (
    graph.META_SHIFT, graph.PLACE_SHIFT, graph.NASAL_SHIFT,
    graph.AP_SHIFT, graph.LEN_SHIFT, graph.VOICE_SHIFT, graph.ASP_SHIFT,
)


class UPC14V3Error(ValueError):
    """Phoneme absent from profile, or graph cannot represent it faithfully."""


class UnrepresentedSound(UPC14V3Error):
    """A known English phoneme for which the historical graph lacks a law."""


@dataclass(frozen=True)
class EnglishPhoneme:
    ipa: str
    family: str
    code: int | None
    graph_derivation: str | None
    evidence: str
    missing_law: str | None

    @property
    def mapped(self) -> bool:
        return self.code is not None


# PHONOLOGY first: these 44 IPA entries come from TWO independent
# source inventories, not English letters.
# /p k/ retain the base unaspirated segments, not an English phonemic
# aspirate contrast. The donor analyses disagree on strict identity:
# these entries explicitly retain the caveat instead of hiding it.
SHARED = (
    ("p", "p", "base-segment; English aspiration is positional"),
    ("b", "b", "base-segment; phonemic systems may differ"),
    ("k", "k", "base-segment; English aspiration is positional"),
    ("ɡ", "g", "base-segment; phonemic systems may differ"),
    ("m", "m", "base-segment; phonemic systems may differ"),
    ("ŋ", "ṅ", "base-segment; English distribution is restricted"),
    ("j", "y", "palatal approximant; v2 calls this y"),
)

# New valid sound vertices DERIVED BY EXISTING V2 EDGES:
# iː,uː = their source vowel followed by v2's long edge.
# w = labial voiced stop b, lift to semivowel, join with
#     the throat/velar articulator (bilabial + velar).
# Their codes use the SAME v2.make/unpack layout, not a new class/prefix.
DERIVED = (
    ("iː", "vowel", "long(i)", "close-front long monophthong"),
    ("uː", "vowel", "long(u)", "close-back rounded long monophthong"),
    ("w", "consonant", "join(lift(b),K)", "voiced labial-velar approximant"),
)

# INVENTORY ONLY. The old graph has no ALVEOLAR (distinct from its dental
# and retroflex place atoms), affricate, lateral, fricative manner distinct
# from its sibilant, seven vowel heights/front-back positions, or ordered
# glide trajectory. 'Free' bit words cannot be given these meanings by
# fiat. Every remaining IPA entry is retained explicitly with its
# missing typed law so admission cannot silently approximate it.
UNREPRESENTED_CONSONANTS = (
    ("t", "alveolar-place"),
    ("d", "alveolar-place"),
    ("t͡ʃ", "postalveolar-affricate"),
    ("d͡ʒ", "postalveolar-affricate"),
    ("f", "labiodental-fricative"),
    ("v", "labiodental-fricative"),
    ("θ", "dental-non-sibilant-fricative"),
    ("ð", "dental-non-sibilant-fricative"),
    ("s", "alveolar-sibilant-place"),
    ("z", "alveolar-sibilant-place"),
    ("ʃ", "postalveolar-sibilant-place"),
    ("ʒ", "postalveolar-sibilant-place"),
    ("h", "voiceless-glottal-vs-v2-h"),
    ("n", "alveolar-nasal-place"),
    ("ɹ", "alveolar-approximant-vs-v2-trill"),
    ("l", "alveolar-lateral-manner"),
)

UNREPRESENTED_VOWELS = (
    ("ɪ", "near-close-near-front-quality"),
    ("e", "short-DRESS-quality-vs-v2-long-e"),
    ("æ", "near-open-front-quality"),
    ("ɒ", "open-back-rounded-quality"),
    ("ʌ", "open-mid-central-quality"),
    ("ʊ", "near-close-near-back-rounded-quality"),
    ("ə", "central-reduced-quality"),
    ("ɑː", "open-back-unrounded-long-quality"),
    ("ɔː", "open-mid-back-rounded-long-quality"),
    ("ɜː", "open-mid-central-long-quality"),
    ("eɪ", "ordered-diphthong-start-and-target"),
    ("aɪ", "ordered-diphthong-start-and-target"),
    ("ɔɪ", "ordered-diphthong-start-and-target"),
    ("aʊ", "ordered-diphthong-start-and-target"),
    ("əʊ", "ordered-diphthong-start-and-target"),
    ("ɪə", "ordered-centring-diphthong"),
    ("eə", "ordered-centring-diphthong"),
    ("ʊə", "ordered-centring-diphthong"),
)


def _derived_code(expression: str) -> int:
    if expression == "long(i)":
        return graph.e_long(graph.SOUNDS["i"])
    if expression == "long(u)":
        return graph.e_long(graph.SOUNDS["u"])
    if expression == "join(lift(b),K)":
        return graph.e_join(graph.e_lift(graph.SOUNDS["b"], 1), graph.K)
    raise UPC14V3Error(f"unrecognized edge expression {expression!r}")


def _inventory() -> tuple[EnglishPhoneme, ...]:
    out: list[EnglishPhoneme] = []
    for ipa, source_label, evidence in SHARED:
        out.append(EnglishPhoneme(ipa, "consonant", graph.SOUNDS[source_label],
                                 f"v2.SOUNDS[{source_label}]", evidence, None))
    for ipa, family, expression, evidence in DERIVED:
        out.append(EnglishPhoneme(ipa, family, _derived_code(expression),
                                 expression, evidence, None))
    for ipa, needed in UNREPRESENTED_CONSONANTS:
        out.append(EnglishPhoneme(ipa, "consonant", None, None,
                                 "donor phoneme, unassigned", needed))
    for ipa, needed in UNREPRESENTED_VOWELS:
        out.append(EnglishPhoneme(ipa, "vowel", None, None,
                                 "donor phoneme, unassigned", needed))
    if len(out) != 44 or len({p.ipa for p in out}) != 44:
        raise UPC14V3Error("44 unique donor phonemes required")
    if sum(p.family == "consonant" for p in out) != 24:
        raise UPC14V3Error("24 consonants required")
    if sum(p.family == "vowel" for p in out) != 20:
        raise UPC14V3Error("20 vowels required")
    codes = [p.code for p in out if p.code is not None]
    if len(codes) != len(set(codes)):
        raise UPC14V3Error("two English phonemes share one sound code")
    for code in codes:
        if not isinstance(code, int) or graph.unpack(code).code != code:
            raise UPC14V3Error("not a historical UPC14-v2 geometric vertex")
        if code >> graph.META_SHIFT:
            raise UPC14V3Error("it-marker used as sound")
    if set(codes) - set(graph.SOUNDS.values()) != {
        _derived_code(expression) for _, _, expression, _ in DERIVED
    }:
        raise UPC14V3Error("undocumented new vertex")
    return tuple(out)


ENGLISH = _inventory()
_BY_IPA = {p.ipa: p for p in ENGLISH}
_BY_CODE = {p.code: p for p in ENGLISH if p.code is not None}


def describe_english_phoneme(ipa: str) -> EnglishPhoneme:
    """Information for *all 44* sounds, even those lacking legal v2 codes."""
    if not isinstance(ipa, str) or unicodedata.normalize("NFC", ipa) != ipa:
        raise UPC14V3Error("IPA token must be canonical NFC")
    try:
        return _BY_IPA[ipa]
    except KeyError as exc:
        raise UPC14V3Error(f"not in British English reference inventory: {ipa!r}") from exc


def encode_english_phoneme(ipa: str) -> int:
    """Return a real UPC14-v2 geometric vertex; never fabricate a new law."""
    row = describe_english_phoneme(ipa)
    if row.code is None:
        raise UnrepresentedSound(f"{ipa}: original UPC14 lacks {row.missing_law}")
    return row.code


def decode_english_phoneme(code: int) -> str:
    """Only codes with a proved current English mapping are admitted."""
    if type(code) is not int:
        raise UPC14V3Error("sound coordinate must be an integer")
    try:
        return _BY_CODE[code].ipa
    except KeyError as exc:
        raise UPC14V3Error(f"unadmitted English sound coordinate {code!r}") from exc


def encode_english_tokens(ipa_tokens: Iterable[str]) -> tuple[int, ...]:
    """Sequence of phonemic tokens; no letters, word segmentation or spelling."""
    return tuple(encode_english_phoneme(tok) for tok in ipa_tokens)


def decode_english_tokens(codes: Iterable[int]) -> tuple[str, ...]:
    return tuple(decode_english_phoneme(c) for c in codes)


def unresolved_laws() -> dict[str, tuple[str, ...]]:
    """Evidence-backed blocker groups. No bit-space assumption is smuggled in."""
    groups: dict[str, list[str]] = {}
    for item in ENGLISH:
        if item.missing_law is not None:
            groups.setdefault(item.missing_law, []).append(item.ipa)
    return {name: tuple(ipa) for name, ipa in groups.items()}


def bitstring(code: int) -> str:
    if type(code) is not int or not 0 <= code < (1 << WIDTH):
        raise UPC14V3Error("not a 14-bit code")
    return f"{code:014b}"


if __name__ == "__main__":
    print("UPC-14 v3: SAME geometric law as v2; English sound audit")
    print(f"English phonemes: {len(ENGLISH)}, geometric: "
          f"{sum(p.mapped for p in ENGLISH)}, "
          f"unrepresented: {sum(not p.mapped for p in ENGLISH)}")
    for row in ENGLISH:
        print(row.ipa, bitstring(row.code) if row.mapped else "UNREPRESENTED",
              row.graph_derivation or row.missing_law)
