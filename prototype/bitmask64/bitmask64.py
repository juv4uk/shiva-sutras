#!/usr/bin/env python3
"""
64-Bit Pratyāhāra Bitmask Engine (UPC-8 / Śiva Sūtras)
======================================================

Epistemic Layer: Layer 6 (Engineering)
Status: Experimental Prototype
Hypothesis Reference: hypotheses/shabda/status.yaml#H2

Mathematical & Architectural Design:
- Canonical sounds span exactly 42 unique codes (0x00 to 0x29).
- Any pratyāhāra S ⊆ {0, ..., 41} is encoded as a single 64-bit unsigned integer mask:
      Mask(S) = ∑_{c ∈ S} 2^c
- Membership test is O(1) in a single CPU/FPGA clock cycle:
      is_member(sound_code, mask) = ((1 << sound_code) & mask) != 0
- Set intersection, union, difference, and subset inclusion are single bitwise ALU instructions:
      S₁ ∩ S₂  ->  mask1 & mask2
      S₁ ∪ S₂  ->  mask1 | mask2
      S₁ \ S₂  ->  mask1 & ~mask2
      S₁ ⊆ S₂  ->  (mask1 & ~mask2) == 0
- The entire 42-pratyāhāra classical Pāṇinian canon is stored in a 336-byte ROM table (42 × 8 bytes).
"""

from typing import Dict, List, Set, Tuple, Union
import time

# ============================================================================
# 42 CANONICAL SOUNDS & BIT POSITIONS
# ============================================================================

# Order of sounds across 14 Śiva Sūtras:
# Sutra 1: a, i, u (R)
# Sutra 2: f(ṛ), x(ḷ) (k)
# Sutra 3: e, o (N)
# Sutra 4: E(ai), O(au) (c)
# Sutra 5: h, y, v, r (w)
# Sutra 6: l (R)
# Sutra 7: Y(ñ), m, N(ṅ), R(ṇ), n (m)
# Sutra 8: J(jh), B(bh) (Y)
# Sutra 9: G(gh), Q(ḍh), D(dh) (z)
# Sutra 10: j, b, g, q(ḍ), d (S)
# Sutra 11: K(kh), P(ph), C(ch), W(ṭh), T(th), c, w(ṭ), t (v)
# Sutra 12: k, p (y)
# Sutra 13: S(ś), z(ṣ), s (r)
# Sutra 14: h (l) -> positional alias to code 0x09 (bit 9)

CANONICAL_SOUNDS: List[str] = [
    # Sutra 1-4: Vowels (ac) -> bits 0..8
    "a", "i", "u", "f", "x", "e", "o", "E", "O",
    # Sutra 5-6: Semivowels + h -> bits 9..13
    "h", "y", "v", "r", "l",
    # Sutra 7: Nasals (ña-ma-ṅa-ṇa-na) -> bits 14..18
    "Y", "m", "N", "R", "n",
    # Sutra 8-9: Voiced Aspirated Stops -> bits 19..23
    "J", "B", "G", "Q", "D",
    # Sutra 10: Voiced Unaspirated Stops -> bits 24..28
    "j", "b", "g", "q", "d",
    # Sutra 11: Voiceless Aspirated Stops + Voiceless Palatal/Retroflex/Dental -> bits 29..36
    "K", "P", "C", "W", "T", "c", "w", "t",
    # Sutra 12: Voiceless Velar/Labial Stops -> bits 37..38
    "k", "p",
    # Sutra 13: Sibilants (Sar) -> bits 39..41
    "S", "z", "s",
]

assert len(CANONICAL_SOUNDS) == 42, f"Expected 42 unique sounds, got {len(CANONICAL_SOUNDS)}"

# Map sound SLP1 -> bit index (0..41)
SOUND_TO_BIT: Dict[str, int] = {sound: i for i, sound in enumerate(CANONICAL_SOUNDS)}
BIT_TO_SOUND: Dict[int, str] = {i: sound for i, sound in enumerate(CANONICAL_SOUNDS)}

# Single-bit masks (sound -> 1 << bit)
SOUND_MASKS: Dict[str, int] = {sound: (1 << bit) for sound, bit in SOUND_TO_BIT.items()}

# ============================================================================
# 42 CLASSICAL PRATYĀHĀRA BITMASKS (PĀṆINIAN CANON)
# Precomputed 64-bit masks (Total table size = 42 * 8 bytes = 336 bytes)
# ============================================================================

def _compute_pratyahara_mask(sounds: List[str]) -> int:
    mask = 0
    for s in sounds:
        if s in SOUND_TO_BIT:
            mask |= (1 << SOUND_TO_BIT[s])
    return mask

# Classical 42 Pratyāhāras with their precise constituent sounds
PRATYAHARA_DEFINITIONS: Dict[str, List[str]] = {
    "ac":   ["a", "i", "u", "f", "x", "e", "o", "E", "O"],
    "ak":   ["a", "i", "u", "f", "x"],
    "ik":   ["i", "u", "f", "x"],
    "uk":   ["u", "f", "x"],
    "eN":   ["e", "o"],
    "ec":   ["e", "o", "E", "O"],
    "Ec":   ["E", "O"],
    "al":   CANONICAL_SOUNDS,  # All 42 sounds
    "hal":  CANONICAL_SOUNDS[9:],  # 33 consonants (h + semivowels + stops + sibilants)
    "val":  CANONICAL_SOUNDS[10:], # All consonants except initial h (32 consonants)
    "ral":  CANONICAL_SOUNDS[12:], # All consonants from r onwards (30 consonants)
    "Jal":  ["J", "B", "G", "Q", "D", "j", "b", "g", "q", "d",
             "K", "P", "C", "W", "T", "c", "w", "t", "k", "p", "S", "z", "s", "h"],
    "Sal":  ["S", "z", "s", "h"],
    "Sar":  ["S", "z", "s"],
    "yar":  CANONICAL_SOUNDS[10:42], # All consonants except h (32 consonants)
    "yay":  ["y", "v", "r", "l", "Y", "m", "N", "R", "n", "J", "B", "G", "Q", "D",
             "j", "b", "g", "q", "d", "K", "P", "C", "W", "T", "c", "w", "t", "k", "p"],
    "yaR":  ["y", "v", "r", "l"],
    "yam":  ["y", "v", "r", "l", "Y", "m", "N", "R", "n"],
    "yaY":  ["y", "v", "r", "l", "Y", "m", "N", "R", "n", "J", "B"],
    "vaw":  ["v", "r"],
    "may":  ["m", "N", "R", "n", "J", "B", "G", "Q", "D", "j", "b", "g", "q", "d",
             "K", "P", "C", "W", "T", "c", "w", "t", "k", "p"],
    "am":   ["a", "i", "u", "f", "x", "e", "o", "E", "O", "h", "y", "v", "r", "l",
             "Y", "m", "N", "R", "n"],
    "aw":   ["a", "i", "u", "f", "x", "e", "o", "E", "O", "h", "y", "v", "r"],
    "iR":   ["i", "u", "f", "x", "e", "o", "E", "O", "h", "y", "v", "r", "l"],
    "aR":   ["a", "i", "u"], # aR 1 (sutra 1)
    "eR":   ["e", "o"],
    "nam":  ["N", "R", "n"],
    "JaS":  ["J", "B", "G", "Q", "D", "j", "b", "g", "q", "d"],
    "jaS":  ["j", "b", "g", "q", "d"],
    "baS":  ["b", "g", "q", "d"],
    "Jaz":  ["J", "B", "G", "Q", "D"],
    "Baz":  ["B", "G", "Q", "D"],
    "Jay":  ["J", "B", "G", "Q", "D", "j", "b", "g", "q", "d", "K", "P", "C", "W",
             "T", "c", "w", "t", "k", "p"],
    "Kay":  ["K", "P", "C", "W", "T", "c", "w", "t", "k", "p"],
    "xay":  ["K", "P", "C", "W", "T", "c", "w", "t"],
    "car":  ["c", "w", "t", "k", "p", "S", "z", "s"],
    "cav":  ["c", "w", "t"],
    "caw":  ["c", "w"],
    "Kar":  ["K", "P", "C", "W", "T", "c", "w", "t", "k", "p", "S", "z", "s"],
    "Jar":  ["J", "B", "G", "Q", "D", "j", "b", "g", "q", "d", "K", "P", "C", "W",
             "T", "c", "w", "t", "k", "p", "S", "z", "s"],
    "haS":  ["h", "y", "v", "r", "l", "Y", "m", "N", "R", "n", "J", "B", "G", "Q",
             "D", "j", "b", "g", "q", "d"],
    "hal":  CANONICAL_SOUNDS[9:],
}

# Compile 64-bit integer masks table:
PRATYAHARA_TABLE_64: Dict[str, int] = {
    name: _compute_pratyahara_mask(sounds) for name, sounds in PRATYAHARA_DEFINITIONS.items()
}

# ============================================================================
# CORE BITMASK ENGINE FUNCTIONS
# ============================================================================

def sound_to_bit(sound_or_code: Union[str, int]) -> int:
    """Convert SLP1 string or numeric UPC code (0x00-0x29) to 64-bit single-bit mask (1 << bit)."""
    if isinstance(sound_or_code, int):
        if 0 <= sound_or_code < 42:
            return 1 << sound_or_code
        raise ValueError(f"Code 0x{sound_or_code:02X} is outside canonical space (0x00-0x29)")
    if sound_or_code in SOUND_TO_BIT:
        return 1 << SOUND_TO_BIT[sound_or_code]
    raise KeyError(f"Unknown canonical sound: {sound_or_code}")

def is_member(sound_or_code: Union[str, int], pratyahara_mask: int) -> bool:
    """Fast-path membership check: ((1 << bit) & mask) != 0."""
    try:
        bit_mask = sound_to_bit(sound_or_code)
        return (bit_mask & pratyahara_mask) != 0
    except (KeyError, ValueError):
        return False

def get_pratyahara_mask(name: str) -> int:
    """Retrieve the precomputed 64-bit mask for a given pratyāhāra name."""
    if name in PRATYAHARA_TABLE_64:
        return PRATYAHARA_TABLE_64[name]
    raise KeyError(f"Unknown pratyāhāra name: {name}")

def mask_intersect(m1: int, m2: int) -> int:
    """Set intersection: S₁ ∩ S₂."""
    return m1 & m2

def mask_union(m1: int, m2: int) -> int:
    """Set union: S₁ ∪ S₂."""
    return m1 | m2

def mask_diff(m1: int, m2: int) -> int:
    """Set difference: S₁ \\ S₂."""
    return m1 & ~m2

def mask_subset(m1: int, m2: int) -> bool:
    """Subset test: True if S₁ ⊆ S₂."""
    return (m1 & ~m2) == 0

def mask_disjoint(m1: int, m2: int) -> bool:
    """Disjoint test: True if S₁ ∩ S₂ = ∅."""
    return (m1 & m2) == 0

def mask_count(m: int) -> int:
    """Count number of sounds in mask (popcount)."""
    return bin(m).count('1')

def mask_to_sounds(m: int) -> List[str]:
    """Decompile a 64-bit mask back to a list of SLP1 sound strings."""
    result = []
    for bit in range(42):
        if (m & (1 << bit)) != 0:
            result.append(BIT_TO_SOUND[bit])
    return result

def sounds_to_mask(sounds: List[str]) -> int:
    """Compile arbitrary list of SLP1 sounds to 64-bit mask."""
    return _compute_pratyahara_mask(sounds)

# ============================================================================
# EXPORT GENERATORS (C / VERILOG)
# ============================================================================

def export_c_header() -> str:
    """Generate C header file with 64-bit pratyāhāra mask constants."""
    lines = [
        "/* Auto-generated 64-bit Pratyahara Masks (UPC-8 / Siva Sutras) */",
        "#ifndef SHIVA_PRATYAHARA_MASKS_H",
        "#define SHIVA_PRATYAHARA_MASKS_H",
        "",
        "#include <stdint.h>",
        "#include <stdbool.h>",
        "",
        "/* Fast membership test macro: 1 cycle */",
        "#define UPC8_IS_MEMBER(code, mask) ((((uint64_t)1 << (code)) & (mask)) != 0)",
        "",
        "/* Pratyahara 64-bit Constants */",
    ]
    for name, mask in sorted(PRATYAHARA_TABLE_64.items()):
        c_name = f"UPC8_MASK_{name.upper()}"
        lines.append(f"#define {c_name:<20} 0x{mask:016X}ULL  /* {mask_count(mask)} sounds */")
    lines.extend([
        "",
        "#endif /* SHIVA_PRATYAHARA_MASKS_H */",
    ])
    return "\n".join(lines)

def export_verilog_lut() -> str:
    """Generate synthesizable Verilog module for pratyāhāra decoding."""
    lines = [
        "// Auto-generated synthesizable Verilog ROM/LUT for Pratyahara Membership",
        "module pratyahara_lut (",
        "    input  wire [5:0]  sound_code,    // 0x00 to 0x29 (6-bit code)",
        "    input  wire [63:0] pratyahara_mask,",
        "    output wire        is_member",
        ");",
        "    assign is_member = pratyahara_mask[sound_code];",
        "endmodule",
    ]
    return "\n".join(lines)
