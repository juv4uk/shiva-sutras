#!/usr/bin/env python3
"""
DerivationCell: 32-bit Grammatical State Token for Panini Grammar Machine.

Binary Layout (32 bits, big-endian):
+--------------------+--------------------+--------------------+--------------------+
| Base Phoneme (8b)  | Svara/Length (8b)  | Anubandha/It (8b)  | Morpheme Tag (8b)  |
| Bits 31..24        | Bits 23..16        | Bits 15..8         | Bits 7..0          |
+--------------------+--------------------+--------------------+--------------------+
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, IntFlag
from typing import List, Tuple, Optional


class MorphemeTag(IntEnum):
    """Morpheme Origin / Functional Tag (Bits 7..0)."""
    NONE = 0x00
    DHATU = 0x01          # Verbal Root (dhātu)
    PRATIPADIKA = 0x02    # Nominal Stem (prātipadika)
    VIKARANA = 0x03       # Thematic Affix (vikaraṇa, e.g. Śap)
    TIN = 0x04            # Verbal Suffix (tiṅ, e.g. tip)
    SUP = 0x05            # Nominal Case Suffix (sup)
    KRIT = 0x06           # Primary Suffix (kṛt)
    TADDHITA = 0x07       # Secondary Suffix (taddhita)
    AGAMA = 0x08          # Augment (āgama, e.g. iṭ)
    ADESA = 0x09          # Substitute (ādeśa, e.g. av-ādeśa)
    ABHYASA = 0x0A        # Reduplicated Portion (abhyāsa)
    ABHYASTA = 0x0B       # Full Reduplicated Form (abhyasta)
    LAKARA = 0x0C         # Abstract Lakāra marker (laṭ, liṭ, etc.)
    MARKER_SLU = 0x0D     # Ślu Null Vikaraṇa Marker


class SvaraLength(IntFlag):
    """Phonological Length and Accent Modulation (Bits 23..16)."""
    NONE = 0x00
    HRASVA = 0x01         # Short Vowel (1 mātrā)
    DIRGHA = 0x02         # Long Vowel (2 mātrās)
    PLUTA = 0x04          # Protract Vowel (3 mātrās)
    UDATTA = 0x08         # High Pitch Accent (udātta)
    ANUDATTA = 0x10       # Low Pitch Accent (anudātta)
    SVARITA = 0x20        # Circumflex Accent (svarita)
    ANUNASIKA = 0x40      # Nasalized (mukhanāsikāvacanaḥ)
    SAMVARTA = 0x80       # Closed / Open Vowel Quality


class AnubandhaTag(IntFlag):
    """It-Marker / Anubandha Bitmask (Bits 15..8)."""
    NONE = 0x00
    S_IT = 0x01           # Ś-it (causes sārvadhātuka saṁjñā 3.4.113)
    P_IT = 0x02           # P-it (udātta accent / prevents ṅidvat 1.2.4)
    K_IT = 0x04           # K-it (prevents guṇa/vṛddhi 1.1.5)
    NG_IT = 0x08          # Ṅ-it (prevents guṇa/vṛddhi 1.1.5)
    T_IT = 0x10           # Ṭ-it (triggers ṭere 3.4.79, svarita)
    N_IT = 0x20           # Ṇ-it (triggers vṛddhi 7.2.115)
    M_IT = 0x40           # M-it (antya-ac-para āgama 1.1.47)
    SH_IT = 0x80          # Ṣ-it (triggers ṅīṣ 4.1.41)


# Standard SLP1 ASCII mapping (canonical internal representation)
SLP1_GLYPHS = "aAiIuUfFxXeEoOkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshMH'"


@dataclass(frozen=True)
class DerivationCell:
    """
    32-bit token packing base phoneme, svara/length, anubandha markers, and morpheme origin.
    """
    phoneme: str                     # 1-char SLP1 glyph (or empty string for elided trace)
    svara: SvaraLength = SvaraLength.NONE
    anubandha: AnubandhaTag = AnubandhaTag.NONE
    morpheme: MorphemeTag = MorphemeTag.NONE

    def __post_init__(self):
        if len(self.phoneme) > 1:
            raise ValueError(f"DerivationCell phoneme must be 0 or 1 character, got: {self.phoneme!r}")
        if self.phoneme and self.phoneme not in SLP1_GLYPHS:
            raise ValueError(f"DerivationCell phoneme not in SLP1 set: {self.phoneme!r}")

    @property
    def raw_phoneme_byte(self) -> int:
        return ord(self.phoneme) if self.phoneme else 0

    def to_uint32(self) -> int:
        """Serialize cell into a 32-bit unsigned integer."""
        b3 = (self.raw_phoneme_byte & 0xFF) << 24
        b2 = (int(self.svara) & 0xFF) << 16
        b1 = (int(self.anubandha) & 0xFF) << 8
        b0 = (int(self.morpheme) & 0xFF)
        return b3 | b2 | b1 | b0

    @classmethod
    def from_uint32(cls, value: int) -> DerivationCell:
        """Deserialize cell from a 32-bit unsigned integer."""
        b3 = (value >> 24) & 0xFF
        b2 = (value >> 16) & 0xFF
        b1 = (value >> 8) & 0xFF
        b0 = value & 0xFF
        phoneme = chr(b3) if b3 != 0 else ""
        return cls(
            phoneme=phoneme,
            svara=SvaraLength(b2),
            anubandha=AnubandhaTag(b1),
            morpheme=MorphemeTag(b0)
        )

    def with_anubandha(self, flag: AnubandhaTag) -> DerivationCell:
        """Return a new cell with additional anubandha markers."""
        return DerivationCell(
            phoneme=self.phoneme,
            svara=self.svara,
            anubandha=self.anubandha | flag,
            morpheme=self.morpheme
        )

    def with_morpheme(self, tag: MorphemeTag) -> DerivationCell:
        """Return a new cell with an updated morpheme origin tag."""
        return DerivationCell(
            phoneme=self.phoneme,
            svara=self.svara,
            anubandha=self.anubandha,
            morpheme=tag
        )

    def with_phoneme(self, new_phoneme: str) -> DerivationCell:
        """Return a new cell with modified surface phoneme, retaining metadata."""
        return DerivationCell(
            phoneme=new_phoneme,
            svara=self.svara,
            anubandha=self.anubandha,
            morpheme=self.morpheme
        )

    def to_dict(self) -> dict:
        return {
            "phoneme": self.phoneme,
            "raw_hex": f"0x{self.to_uint32():08X}",
            "svara": self.svara.name,
            "anubandha": [tag.name for tag in AnubandhaTag if tag in self.anubandha and tag != AnubandhaTag.NONE],
            "morpheme": self.morpheme.name
        }


class DerivationStream:
    """A sequence of DerivationCell tokens representing a morphological term or word."""

    def __init__(self, cells: Optional[List[DerivationCell]] = None):
        self.cells: List[DerivationCell] = list(cells) if cells else []

    @classmethod
    def from_slp1(cls, text: str, morpheme: MorphemeTag = MorphemeTag.NONE, anubandha: AnubandhaTag = AnubandhaTag.NONE) -> DerivationStream:
        cells = [
            DerivationCell(phoneme=ch, morpheme=morpheme, anubandha=anubandha)
            for ch in text
        ]
        return cls(cells)

    @property
    def surface_text(self) -> str:
        """Render active surface phonemes as an SLP1 string."""
        return "".join(c.phoneme for c in self.cells if c.phoneme)

    def pack_uint32_list(self) -> List[int]:
        return [c.to_uint32() for c in self.cells]

    @classmethod
    def unpack_uint32_list(cls, values: List[int]) -> DerivationStream:
        return cls([DerivationCell.from_uint32(v) for v in values])

    def __len__(self) -> int:
        return len(self.cells)

    def __repr__(self) -> str:
        return f"DerivationStream({self.surface_text!r}, len={len(self.cells)})"
