#!/usr/bin/env python3
"""
UPC-7 sound projection (shiva-sutras#87)
========================================

The exact 7-bit UPC-7 cell remains identity.  This module adds a
non-authoritative phonetic projection:

    UPC7 cell + language profile -> SoundProjection

IPA is evidence/UI notation, not identity.  A projection may be unresolved or
unsupported.  Signs and unassigned cells fail closed instead of pretending to
be speech.

The first evidence source is:
    docs/sanskrit-ukrainian-sounds-2026-10-02.tsv
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from upc7_layouts import ASSIGNED, UPC7Text

SOURCE = "docs/sanskrit-ukrainian-sounds-2026-10-02.tsv"
PROFILES = ("sa", "uk")


class UPC7SoundError(ValueError):
    pass


@dataclass(frozen=True)
class SoundProjection:
    code: int
    bits: str
    identity: str
    kind: str
    profile: str
    spelling: Optional[str]
    ipa: Optional[str]
    ipa_candidates: Tuple[str, ...]
    status: str
    confidence: str
    source: str

    @property
    def resolved(self) -> bool:
        return self.status == "resolved"


# Values are (preferred IPA, candidates, confidence).
# A missing preferred IPA means the source is explicitly unresolved.
_SA_IPA: Dict[str, Tuple[Optional[str], Tuple[str, ...], str]] = {
    "a": (None, ("ə", "ɐ"), "medium"),
    "ā": ("aː", (), "medium"),
    "i": ("i", (), "high"),
    "ī": ("iː", (), "medium"),
    "u": ("u", (), "high"),
    "ū": ("uː", (), "medium"),
    "ṛ": (None, ("ɽ̩", "ri", "ru"), "low"),
    "ṝ": (None, ("ɽ̩ː", "riː", "ruː"), "low"),
    "ḷ": (None, ("l̩",), "low"),
    "ḹ": (None, ("l̩ː",), "low"),
    "e": ("eː", (), "medium"),
    "ai": (None, ("ai", "ɐi"), "medium"),
    "o": ("oː", (), "medium"),
    "au": (None, ("au", "ɐu"), "medium"),
    "k": ("k", (), "high"),
    "kh": ("kʰ", (), "high"),
    "g": ("g", (), "high"),
    "gh": ("gʱ", (), "high"),
    "ṅ": ("ŋ", (), "medium"),
    "c": (None, ("c", "t͡ʃ"), "medium"),
    "ch": (None, ("cʰ", "t͡ʃʰ"), "medium"),
    "j": (None, ("ɟ", "d͡ʒ"), "medium"),
    "jh": (None, ("ɟʱ", "d͡ʒʱ"), "medium"),
    "ñ": ("ɲ", (), "medium"),
    "ṭ": ("ʈ", (), "high"),
    "ṭh": ("ʈʰ", (), "high"),
    "ḍ": ("ɖ", (), "high"),
    "ḍh": ("ɖʱ", (), "high"),
    "ṇ": ("ɳ", (), "high"),
    "t": ("t̪", (), "high"),
    "th": ("t̪ʰ", (), "high"),
    "d": ("d̪", (), "high"),
    "dh": ("d̪ʱ", (), "high"),
    "n": ("n̪", (), "high"),
    "p": ("p", (), "high"),
    "ph": ("pʰ", (), "high"),
    "b": ("b", (), "high"),
    "bh": ("bʱ", (), "high"),
    "m": ("m", (), "high"),
    "y": ("j", (), "high"),
    "r": (None, ("r", "ɾ"), "medium"),
    "l": ("l̪", (), "medium"),
    "v": ("ʋ", (), "medium"),
    "ś": ("ɕ", (), "medium"),
    "ṣ": ("ʂ", (), "medium"),
    "s": ("s̪", (), "high"),
    "h": ("ɦ", (), "medium"),
}

_UK_IPA: Dict[str, Tuple[Optional[str], Tuple[str, ...], str]] = {
    "к": ("k", (), "high"),
    "ґ": ("g", (), "high"),
    "т": ("t̪", (), "high"),
    "д": ("d̪", (), "high"),
    "н": ("n̪", (), "high"),
    "п": ("p", (), "high"),
    "б": ("b", (), "high"),
    "м": ("m", (), "high"),
    "х": ("x", (), "high"),
    "ш": ("ʃ", (), "high"),
    "ж": ("ʒ", (), "high"),
    "й": ("j", (), "high"),
    "с": ("s̪", (), "high"),
    "з": ("z", (), "high"),
    "р": ("r", (), "medium"),
    "л": (None, ("ɫ", "l̪"), "medium"),
    "ф": ("f", (), "high"),
    "в": (None, ("ʋ", "w"), "medium"),
    "г": ("ɦ", (), "medium"),
    "ц": ("t͡s", (), "high"),
    "ч": ("t͡ʃ", (), "high"),
    "дз": ("d͡z", (), "high"),
    "дж": ("d͡ʒ", (), "high"),
    "і": ("i", (), "high"),
    "у": ("u", (), "high"),
    "а": ("ɑ", (), "medium"),
    "е": (None, ("ɛ", "e"), "medium"),
    "о": (None, ("ɔ", "o"), "medium"),
    "и": ("ɪ", (), "medium"),
}


def _kind(identity: str) -> str:
    if identity.startswith("reserved."):
        return "unassigned"
    if identity == "non-varga.uk-ext.softness":
        return "modifier"
    if identity in ("sign.anusvara", "sign.visarga"):
        return "modifier"
    if identity.startswith(("varga.", "non-varga.", "vowel.")):
        return "phonological"
    return "non-sound"


def project_sound(code: int, profile: str) -> SoundProjection:
    if profile not in PROFILES:
        raise UPC7SoundError(f"unknown sound profile: {profile!r}")

    codec = UPC7Text()
    cell = codec.cells[code]
    kind = _kind(cell.name)

    if cell.status != ASSIGNED:
        return SoundProjection(
            code, cell.bits, cell.name, "unassigned", profile,
            None, None, (), "unassigned", "n/a", SOURCE
        )

    if kind == "non-sound":
        return SoundProjection(
            code, cell.bits, cell.name, kind, profile,
            None, None, (), "non-sound", "n/a", SOURCE
        )

    if kind == "modifier":
        spelling = codec.layout("uk" if profile == "uk" else "sa-iast").code_to_spelling.get(code)
        return SoundProjection(
            code, cell.bits, cell.name, kind, profile,
            spelling, None, (), "context-required", "source-backed", SOURCE
        )

    layout_name = "uk" if profile == "uk" else "sa-iast"
    spelling = codec.layout(layout_name).code_to_spelling.get(code)
    if spelling is None:
        return SoundProjection(
            code, cell.bits, cell.name, kind, profile,
            None, None, (), "unsupported", "n/a", SOURCE
        )

    table = _UK_IPA if profile == "uk" else _SA_IPA
    phonetic = table.get(spelling)
    if phonetic is None:
        return SoundProjection(
            code, cell.bits, cell.name, kind, profile,
            spelling, None, (), "unresolved", "unknown", SOURCE
        )

    ipa, candidates, confidence = phonetic
    status = "resolved" if ipa is not None else "unresolved"
    return SoundProjection(
        code, cell.bits, cell.name, kind, profile,
        spelling, ipa, candidates, status, confidence, SOURCE
    )


def sound_table(profile: str) -> Tuple[SoundProjection, ...]:
    return tuple(project_sound(code, profile) for code in range(128))


__all__ = [
    "PROFILES",
    "SOURCE",
    "SoundProjection",
    "UPC7SoundError",
    "project_sound",
    "sound_table",
]
