#!/usr/bin/env python3
"""
Slavic & Ukrainian Phonological Feature Matrix Engine
=====================================================

Epistemic Layer: Layer 6 (Engineering / Language Profile)
Status: Experimental Prototype

Capabilities:
1. Universal Articulatory Feature Matrix for Ukrainian & Slavic phonemes (0x31..0x4F).
2. Iotated Vowel Decomposition (я, ю, є, ї) with contextual palatalization.
3. Affricate and Soft-Cluster Multi-character Lexing (дж, дз, ць, ч, щ).
4. Historical Slavic Palatalization Transformations (First, Second, Third)
   modeled as geometric feature shifts in articulatory space.
"""

from typing import Dict, List, Optional, Tuple

# Articulatory Feature Vectors
# Dimensions:
# (Place: 0=Labial, 1=Dental, 2=Postalveolar, 3=Palatal, 4=Velar, 5=Glottal)
# (Manner: 0=Stop, 1=Affricate, 2=Fricative, 3=Nasal, 4=Liquid, 5=Vowel)
# (Voiced: 0=No, 1=Yes)
# (Soft/Palatalized: 0=Hard, 1=Soft)

class PhonemeFeature:
    def __init__(self, code: int, symbol: str, place: int, manner: int, voiced: int, soft: int, is_vowel: bool = False):
        self.code = code
        self.symbol = symbol
        self.place = place     # 0: Labial, 1: Dental, 2: Postalveolar, 3: Palatal, 4: Velar, 5: Glottal
        self.manner = manner   # 0: Stop, 1: Affricate, 2: Fricative, 3: Nasal, 4: Liquid, 5: Vowel
        self.voiced = voiced   # 0: Voiceless, 1: Voiced
        self.soft = soft       # 0: Hard, 1: Soft
        self.is_vowel_flag = is_vowel

    def __repr__(self):
        return f"PhonemeFeature({self.symbol}, code=0x{self.code:02X}, place={self.place}, manner={self.manner}, soft={self.soft})"

# Phoneme Registry (0x31..0x4F + shared 0x00..0x29)
SLAVIC_REGISTRY: Dict[str, PhonemeFeature] = {
    # Vowels
    "а": PhonemeFeature(0x33, "а", 3, 5, 1, 0, is_vowel=True),
    "е": PhonemeFeature(0x32, "е", 3, 5, 1, 0, is_vowel=True),
    "и": PhonemeFeature(0x31, "и", 3, 5, 1, 0, is_vowel=True),
    "і": PhonemeFeature(0x01, "і", 3, 5, 1, 1, is_vowel=True),
    "о": PhonemeFeature(0x34, "о", 3, 5, 1, 0, is_vowel=True),
    "у": PhonemeFeature(0x02, "у", 3, 5, 1, 0, is_vowel=True),

    # Semivowel
    "й": PhonemeFeature(0x0A, "й", 3, 4, 1, 1),

    # Hard Consonants
    "б": PhonemeFeature(0x19, "б", 0, 0, 1, 0),
    "п": PhonemeFeature(0x26, "п", 0, 0, 0, 0),
    "в": PhonemeFeature(0x40, "в", 0, 2, 1, 0),
    "м": PhonemeFeature(0x0F, "м", 0, 3, 1, 0),
    "ф": PhonemeFeature(0x39, "ф", 0, 2, 0, 0),

    "д": PhonemeFeature(0x1C, "д", 1, 0, 1, 0),
    "т": PhonemeFeature(0x24, "т", 1, 0, 0, 0),
    "з": PhonemeFeature(0x3A, "з", 1, 2, 1, 0),
    "с": PhonemeFeature(0x29, "с", 1, 2, 0, 0),
    "дз": PhonemeFeature(0x36, "дз", 1, 1, 1, 0),
    "ц": PhonemeFeature(0x35, "ц", 1, 1, 0, 0),
    "н": PhonemeFeature(0x12, "н", 1, 3, 1, 0),
    "л": PhonemeFeature(0x3F, "л", 1, 4, 1, 0),
    "р": PhonemeFeature(0x0C, "р", 1, 4, 1, 0),

    "ж": PhonemeFeature(0x3C, "ж", 2, 2, 1, 0),
    "ш": PhonemeFeature(0x3B, "ш", 2, 2, 0, 0),
    "дж": PhonemeFeature(0x38, "дж", 2, 1, 1, 0),
    "ч": PhonemeFeature(0x37, "ч", 2, 1, 0, 0),

    "г": PhonemeFeature(0x3E, "г", 5, 2, 1, 0),
    "ґ": PhonemeFeature(0x1A, "ґ", 4, 0, 1, 0),
    "к": PhonemeFeature(0x25, "к", 4, 0, 0, 0),
    "х": PhonemeFeature(0x3D, "х", 4, 2, 0, 0),

    # Soft / Palatalized Consonants
    "дь": PhonemeFeature(0x42, "дь", 1, 0, 1, 1),
    "ть": PhonemeFeature(0x41, "ть", 1, 0, 0, 1),
    "зь": PhonemeFeature(0x45, "зь", 1, 2, 1, 1),
    "сь": PhonemeFeature(0x44, "сь", 1, 2, 0, 1),
    "дзь": PhonemeFeature(0x47, "дзь", 1, 1, 1, 1),
    "ць": PhonemeFeature(0x46, "ць", 1, 1, 0, 1),
    "нь": PhonemeFeature(0x43, "нь", 1, 3, 1, 1),
    "ль": PhonemeFeature(0x49, "ль", 1, 4, 1, 1),
    "рь": PhonemeFeature(0x48, "рь", 1, 4, 1, 1),
    "мь": PhonemeFeature(0x4B, "мь", 0, 3, 1, 1),
    "пь": PhonemeFeature(0x4C, "пь", 0, 0, 0, 1),
    "бь": PhonemeFeature(0x4D, "бь", 0, 0, 1, 1),
    "фь": PhonemeFeature(0x4E, "фь", 0, 2, 0, 1),
    "вь": PhonemeFeature(0x4F, "вь", 0, 2, 1, 1),
}

# Mapping hard consonant -> soft counterpart
HARD_TO_SOFT: Dict[str, str] = {
    "д": "дь", "т": "ть", "з": "зь", "с": "сь",
    "дз": "дзь", "ц": "ць", "н": "нь", "л": "ль", "р": "рь",
    "б": "бь", "п": "пь", "в": "вь", "м": "мь", "ф": "фь",
}

# ============================================================================
# IOTATED VOWEL DECOMPOSITION ENGINE
# ============================================================================

def decompose_iotated(text: str) -> List[str]:
    """
    Context-aware phonemic decomposition of Ukrainian words with iotated vowels (я, ю, є, ї).
    - Initial or post-vocalic / post-apostrophe: я -> [й, а], ю -> [й, у], є -> [й, е], ї -> [й, і].
    - Post-consonantal: palatalizes preceding consonant (д + я -> дь + а).
    """
    vowels = {"а", "е", "и", "і", "о", "у"}
    iotated_map = {"я": "а", "ю": "у", "є": "е", "ї": "і"}
    apostrophes = {"'", "’", "`"}

    tokens: List[str] = []
    i = 0
    while i < len(text):
        ch = text[i]

        # Multi-char affricates / soft signs
        if i + 2 < len(text) and text[i:i+3] == "дзь":
            tokens.append("дзь")
            i += 3
            continue
        if i + 1 < len(text) and text[i:i+2] in ("дж", "дз", "ць", "ль", "нь", "сь", "ть", "дь", "зь", "рь", "мь", "пь", "бь", "фь", "вь"):
            tokens.append(text[i:i+2])
            i += 2
            continue
        if ch == "щ":
            tokens.extend(["ш", "ч"])
            i += 1
            continue

        if ch in iotated_map:
            vowel_core = iotated_map[ch]
            # Rule for 'ї': ALWAYS decomposes to [й, і]
            if ch == "ї":
                tokens.extend(["й", "і"])
            elif i == 0 or text[i-1] in vowels or text[i-1] in apostrophes or (tokens and tokens[-1] == "й"):
                tokens.extend(["й", vowel_core])
            else:
                # Post-consonantal: soften the previous consonant if possible
                if tokens and tokens[-1] in HARD_TO_SOFT:
                    tokens[-1] = HARD_TO_SOFT[tokens[-1]]
                tokens.append(vowel_core)
            i += 1
        elif ch in apostrophes:
            # Apostrophe prevents softening of preceding consonant
            i += 1
        else:
            tokens.append(ch)
            i += 1
    return tokens

# ============================================================================
# HISTORICAL SLAVIC PALATALIZATIONS ENGINE
# ============================================================================

def apply_first_palatalization(consonant: str) -> str:
    """
    First Slavic Palatalization (Перша палаталізація):
    Velars (к, г, х) shift to Postalveolar Sibilants/Affricates (ч, ж, ш)
    before front vowels (*e, *i, *ь).
    - к (velar stop) -> ч (postalveolar affricate)
    - г (velar/glottal fricative) -> ж (postalveolar fricative)
    - х (velar fricative) -> ш (postalveolar fricative)
    """
    shifts = {
        "к": "ч",
        "г": "ж",
        "ґ": "дж",
        "х": "ш",
    }
    return shifts.get(consonant, consonant)

def apply_second_palatalization(consonant: str) -> str:
    """
    Second Slavic Palatalization (Друга палаталізація):
    Velars shift to Dental Sibilants/Affricates before diphthongal *ě / *oi.
    - к -> ць
    - г -> зь (or дзь)
    - х -> сь
    """
    shifts = {
        "к": "ць",
        "г": "зь",
        "х": "сь",
    }
    return shifts.get(consonant, consonant)

def geometric_palatalization_shift(phoneme: PhonemeFeature, rule: int = 1) -> PhonemeFeature:
    """
    Models palatalization as a geometric displacement in articulatory space:
    - Rule 1: Place 4 (Velar) -> Place 2 (Postalveolar), Manner -> Fricative/Affricate.
    - Rule 2: Place 4 (Velar) -> Place 1 (Dental), Soft -> 1.
    """
    if phoneme.place != 4 and phoneme.place != 5: # Not velar/glottal
        return phoneme
    if rule == 1:
        new_symbol = apply_first_palatalization(phoneme.symbol)
    elif rule == 2:
        new_symbol = apply_second_palatalization(phoneme.symbol)
    else:
        new_symbol = phoneme.symbol
    return SLAVIC_REGISTRY.get(new_symbol, phoneme)
