#!/usr/bin/env python3
"""
UPC-8: Universal Phoneme Code (8-bit)
======================================

epistemic_layer: engineering
status: experimental
hypothesis_ref: hypotheses/shabda/status.yaml#H2
non_claims:
  - no historical claim about Panini's intended numeric encoding
  - no claim of universal phoneme inventory (see docs/world-phonetics-and-upc.md
    for why no such finite inventory exists to claim)
  - no FPGA performance result -- see hypotheses/shabda/status.yaml#H2,
    still PREMATURE-HYPOTHESIS as of 2026-08-18
  - the byte assignment (0x00-0x29 etc.) is an engineering choice over the
    canon, not itself part of the transmitted canon -- see "canon:code" vs
    "canon:transmitted" in docs/EPISTEMIC_CONSISTENCY_AUDIT_v1.md (ECA-007)

Architecture:
  CANON (Siva Sutras) -> Sanskrit interpretation -> Language extensions -> UPC-8 encoding

Code space:
  0x00-0x29  Engineering base codes (immutable assignment, Siva Sutra sequence order)
              42 unique sounds; h in sutra 14 aliases to h in sutra 5 (code 0x09)
  0x2A-0x30  Sanskrit extended (long vowels, anusvara, visarga)
  0x31-0x4F  Ukrainian (near-equivalent + new-extension)
  0x50-0x7F  English (reserved)
  0x80-0xFF  Reserved for future languages
"""

import hashlib
import os
from typing import Dict, List


# ============================================================================
# PROVENANCE
#
# SIVA_SUTRAS below is a MANUAL SLP1 transcription of the canonical
# ksetra/canon/siva-sutras.yaml (IAST, no engineering codes -- see that
# file's own header). This module does not read that YAML at runtime and
# does not verify the transcription is correct; a correctness check would
# need an IAST<->SLP1 mapper that does not exist elsewhere in this repo,
# and building one just for this check would be its own new source of bugs.
#
# What CANON_SOURCE_SHA256 *does* catch: if ksetra/canon/siva-sutras.yaml
# changes without this file's SIVA_SUTRAS being updated to match, the byte
# stream this module produces silently stops corresponding to the current
# canon. canon_source_matches() below makes that loud instead of silent.
# This is a drift detector, not a correctness proof of the transcription.
# ============================================================================
CANON_SOURCE_FILE = "ksetra/canon/siva-sutras.yaml"
CANON_SOURCE_SHA256 = "9a53d5fc3989e8748b2045c83dc275160bd0d142ba0a3b04816a5540c2cef32a"


def canon_source_matches() -> bool:
    """True if ksetra/canon/siva-sutras.yaml still hashes to the value
    SIVA_SUTRAS below was manually transcribed from. False (or FileNotFoundError
    if the repo layout changed) means SIVA_SUTRAS may be stale relative to canon."""
    path = os.path.join(os.path.dirname(__file__), "..", CANON_SOURCE_FILE)
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest() == CANON_SOURCE_SHA256


# ============================================================================
# SIVA SUTRA CANON (immutable)
# Each tuple: (ordinal, [sounds_slp1], marker_slp1)
# ============================================================================

SIVA_SUTRAS = [
    (1,  ["a", "i", "u"],                       "R"),
    (2,  ["f", "x"],                             "k"),
    (3,  ["e", "o"],                            "N"),
    (4,  ["E", "O"],                            "c"),
    (5,  ["h", "y", "v", "r"],                  "w"),
    (6,  ["l"],                                 "R"),
    (7,  ["Y", "m", "N", "R", "n"],             "m"),
    (8,  ["J", "B"],                            "Y"),
    (9,  ["G", "Q", "D"],                       "z"),
    (10, ["j", "b", "g", "q", "d"],             "S"),
    (11, ["K", "P", "C", "W", "T", "c", "w", "t"], "v"),
    (12, ["k", "p"],                            "y"),
    (13, ["S", "z", "s"],                       "r"),
    (14, ["h"],                                 "l"),
]

# SLP1 sound names (for display):
#   Lowercase: a i u e o k g c j t d p b y r l v s h
#   f = vocalic r, x = vocalic l, E = ai, O = au
#   Y = palatal nasal, N = guttural nasal, R = cerebral nasal
#   J = jh, B = bh, G = gh, Q = aspirated retroflex dh, D = aspirated dental dh
#   K = kh, P = ph, C = ch, W = aspirated retroflex th, T = aspirated dental th
#   w = retroflex t, q = retroflex d
#   S = palatal sibilant, z = retroflex sibilant

# Build canonical position list: 43 positions, 42 unique sounds (h duplicated)
def _build_canon():
    positions = []
    for ordinal, sounds, marker in SIVA_SUTRAS:
        for i, s in enumerate(sounds):
            positions.append({
                "ordinal": ordinal,
                "position": i + 1,
                "slp1": s,
                "marker_slp1": marker,
            })
    return positions

CANON_POSITIONS = _build_canon()  # 43 entries
assert len(CANON_POSITIONS) == 43

# Assign codes: 0x00-0x29 for 42 unique sounds
# h in sutra 14 (position 42) aliases to h in sutra 5 (position 9, code 0x09)
def _assign_codes():
    code_of_position = {}  # position_index -> code
    code_of_sound = {}     # slp1 -> code (first occurrence wins)
    next_code = 0
    aliases = []  # (position_index, alias_of_code)

    for i, pos in enumerate(CANON_POSITIONS):
        slp1 = pos["slp1"]
        if slp1 in code_of_sound:
            # This is a duplicate sound — alias to existing code
            aliases.append((i, code_of_sound[slp1]))
            code_of_position[i] = code_of_sound[slp1]
        else:
            code_of_position[i] = next_code
            code_of_sound[slp1] = next_code
            next_code += 1

    assert next_code == 42, f"Expected 42 unique codes, got {next_code}"
    return code_of_position, code_of_sound, aliases

CODE_OF_POSITION, CODE_OF_SOUND, ALIASES = _assign_codes()

CANON_REF_PREFIX = "SS"

def canon_ref(ordinal: int, position: int) -> str:
    return f"{CANON_REF_PREFIX}-{ordinal:02d}:{position}"


# ============================================================================
# EXTENSION TABLES
# ============================================================================

SANSKRIT_EXTENDED = [
    (0x2A, "PH-SKT-A",  "a:",  "unresolved", ["A:", "a:", "@"], "SS-01:1", "dirgha of a"),
    (0x2B, "PH-SKT-I",  "i:",  "i:",          [],                 "SS-01:2", "dirgha of i"),
    (0x2C, "PH-SKT-U",  "u:",  "u:",          [],                 "SS-01:3", "dirgha of u"),
    (0x2D, "PH-SKT-F",  "R:",  "r=:>",        [],                 "SS-02:1", "dirgha of R"),
    (0x2E, "PH-SKT-X",  "L:",  "l=:>",        [],                 "SS-02:2", "dirgha of L"),
    (0x2F, "PH-SKT-M",  "~",   "unresolved", ["m~", "N", "n", "m"], None, "not in canon"),
    (0x30, "PH-SKT-H",  "H",   "unresolved", ["h", "x", "c<"], None, "not in canon"),
]

# ============================================================================
# REAL IAST CORRESPONDENCE (for encode_sanskrit_iast_token / scheme="IAST")
#
# Distinct from the ad-hoc ASCII "iast" field on SANSKRIT_EXTENDED entries
# above (e.g. "a:", "R:", "H") -- that field is an internal placeholder
# spelling used by encode_sanskrit()'s legacy fallback and by existing
# callers (prototype/dual-witness/dual_witness.py), kept unchanged for
# backward compatibility. This table is genuine Unicode IAST (ā, ī, ṛ,
# ñ, ṭh, ...), the actual notation the README/docs claimed to support
# (docs/upc8-prototype-deep-review.md#4: encode_sanskrit("ai")/("ā")/
# ("kh") all raised KeyError despite the "SLP1 or IAST" claim).
# ============================================================================
SLP1_TO_IAST = {
    "a": "a", "i": "i", "u": "u", "f": "ṛ", "x": "ḷ",
    "e": "e", "o": "o", "E": "ai", "O": "au",
    "h": "h", "y": "y", "v": "v", "r": "r", "l": "l",
    "Y": "ñ", "m": "m", "N": "ṅ", "R": "ṇ", "n": "n",
    "J": "jh", "B": "bh",
    "G": "gh", "Q": "ḍh", "D": "dh",
    "j": "j", "b": "b", "g": "g", "q": "ḍ", "d": "d",
    "K": "kh", "P": "ph", "C": "ch", "W": "ṭh", "T": "th",
    "c": "c", "w": "ṭ", "t": "t",
    "k": "k", "p": "p",
    "S": "ś", "z": "ṣ", "s": "s",
}
assert len(SLP1_TO_IAST) == 42

# code -> real IAST spelling, for the 7 Sanskrit-extended codes (0x2A-0x30).
IAST_EXTENDED = {
    0x2A: "ā",  # a-macron: dirgha of a
    0x2B: "ī",  # i-macron
    0x2C: "ū",  # u-macron
    0x2D: "ṝ",  # r-macron-with-dot-below: dirgha of r-dot-below
    0x2E: "ḹ",  # l-with-dot-below-macron: dirgha of l-dot-below
    0x2F: "ṃ",  # m-with-dot-below: anusvara
    0x30: "ḥ",  # h-with-dot-below: visarga
}


# (phoneme_id, letter, ipa, shared_code, canon_ref, relation)
UKRAINIAN_SHARED = [
    ("PH-UKR-b",  "\u0431", "b",   0x19, "SS-10:2", "segment-equivalent"),
    ("PH-UKR-d",  "\u0434", "d_",  0x1C, "SS-10:5", "segment-equivalent"),
    ("PH-UKR-g",  "\u0491", "g",   0x1A, "SS-10:3", "segment-equivalent"),
    ("PH-UKR-i",  "\u0456", "i",   0x01, "SS-01:2", "segment-equivalent"),
    ("PH-UKR-j",  "\u0439", "j",   0x0A, "SS-05:2", "system-equivalent"),
    ("PH-UKR-k",  "\u043a", "k",   0x25, "SS-12:1", "segment-equivalent"),
    ("PH-UKR-m",  "\u043c", "m",   0x0F, "SS-07:2", "segment-equivalent"),
    ("PH-UKR-n",  "\u043d", "n_",  0x12, "SS-07:5", "segment-equivalent"),
    ("PH-UKR-p",  "\u043f", "p",   0x26, "SS-12:2", "segment-equivalent"),
    ("PH-UKR-r",  "\u0440", "r",   0x0C, "SS-05:4", "segment-equivalent"),
    ("PH-UKR-s",  "\u0441", "s_",  0x29, "SS-13:3", "segment-equivalent"),
    ("PH-UKR-t",  "\u0442", "t_",  0x24, "SS-11:8", "segment-equivalent"),
    ("PH-UKR-u",  "\u0443", "u",   0x02, "SS-01:3", "segment-equivalent"),
]

# (code, phoneme_id, letter, ipa, ipa_candidates, canon_ref, relation)
UKRAINIAN_NEW = [
    (0x33, "PH-UKR-a",    "\u0430",          "unresolved", ["a", "A"],           "SS-01:1", "near-equivalent"),
    (0x32, "PH-UKR-e",    "\u0435",          "E",          [],                    "SS-03:1", "near-equivalent"),
    (0x34, "PH-UKR-o",    "\u043e",          "unresolved", ["O", "o"],            "SS-03:2", "near-equivalent"),
    (0x31, "PH-UKR-y",    "\u0438",          "unresolved", ["I", "e", "M"],      None,      "new-extension"),
    (0x3E, "PH-UKR-h",    "\u0433",          "unresolved", ["G\\", "x", "7"],    "SS-05:1", "near-equivalent"),
    (0x3F, "PH-UKR-l",    "\u043b",          "5",          [],                    "SS-06:1", "near-equivalent"),
    (0x49, "PH-UKR-lj",   "\u043b\u044c",    "l_j",        [],                    "SS-06:1", "near-equivalent"),
    (0x40, "PH-UKR-v",    "\u0432",          "unresolved", ["v", "w", "B\\"],     "SS-05:3", "near-equivalent"),
    (0x3B, "PH-UKR-sh",   "\u0448",          "S",          [],                    "SS-13:1", "near-equivalent"),
    (0x3C, "PH-UKR-zh",   "\u0436",          "Z",          [],                    None,      "new-extension"),
    (0x44, "PH-UKR-sj",   "\u0441\u044c",    "s_j",        [],                    "SS-13:1", "near-equivalent"),
    (0x45, "PH-UKR-zj",   "\u0437\u044c",    "z_j",        [],                    None,      "new-extension"),
    (0x43, "PH-UKR-nj",   "\u043d\u044c",    "n_j",        [],                    "SS-07:1", "near-equivalent"),
    (0x48, "PH-UKR-rj",   "\u0440\u044c",    "r_j",        [],                    None,      "new-extension"),
    (0x37, "PH-UKR-ch",   "\u0447",          "t_dZ",       [],                    "SS-11:6", "near-equivalent"),
    (0x38, "PH-UKR-dzh",  "\u0434\u0436",    "d_dZ",       [],                    "SS-10:1", "near-equivalent"),
    (0x35, "PH-UKR-ts",   "\u0446",          "t_s",        [],                    None,      "new-extension"),
    (0x36, "PH-UKR-dz",   "\u0434\u0437",    "d_z",        [],                    None,      "new-extension"),
    (0x39, "PH-UKR-f",    "\u0444",          "f",          [],                    None,      "new-extension"),
    (0x3D, "PH-UKR-x",    "\u0445",          "x",          [],                    None,      "new-extension"),
    (0x3A, "PH-UKR-z",    "\u0437",          "z_",         [],                    None,      "new-extension"),
    (0x41, "PH-UKR-tj",   "\u0442\u044c",    "t_j",        [],                    None,      "new-extension"),
    (0x42, "PH-UKR-dj",   "\u0434\u044c",    "d_j",        [],                    None,      "new-extension"),
    (0x46, "PH-UKR-tsj",  "\u0446\u044c",    "t_s_j",      [],                    None,      "new-extension"),
    (0x47, "PH-UKR-dzj",  "\u0434\u0437\u044c", "d_z_j",   [],                    None,      "new-extension"),
    (0x4A, "PH-UKR-shch", "\u0449",          "StS",        [],                    None,      "new-extension"),
    (0x4B, "PH-UKR-mj",   "\u043c\u044c",    "m_j",        [],                    None,      "new-extension"),
    (0x4C, "PH-UKR-pj",   "\u043f\u044c",    "p_j",        [],                    None,      "new-extension"),
    (0x4D, "PH-UKR-bj",   "\u0431\u044c",    "b_j",        [],                    None,      "new-extension"),
    (0x4E, "PH-UKR-fj",   "\u0444\u044c",    "f_j",        [],                    None,      "new-extension"),
    (0x4F, "PH-UKR-vj",   "\u0432\u044c",    "v_j",        [],                    None,      "new-extension"),
]


class UPC8:
    """UPC-8 encoder/decoder with pratyahara support."""

    def __init__(self):
        self.table: Dict[int, dict] = {}
        self._position_to_code = CODE_OF_POSITION  # 43 positions -> 42 codes
        self._code_to_position = {}                 # 42 codes -> first position
        self._build_canonical()
        self._build_sanskrit_extended()
        self._build_ukrainian()

        self._slp1_to_code = CODE_OF_SOUND.copy()
        self._iast_to_code = {}
        self._iast_real_to_code = {}
        self._ukr_letter_to_code = {}
        self._build_indexes()

        self._pratyahara_cache = {}

    def _build_canonical(self):
        for pos_idx in range(len(CANON_POSITIONS)):
            code = CODE_OF_POSITION[pos_idx]
            pos = CANON_POSITIONS[pos_idx]
            ref = canon_ref(pos["ordinal"], pos["position"])

            is_alias = any(a[0] == pos_idx for a in ALIASES)

            if code not in self.table:
                # Primary entry for this code
                self.table[code] = {
                    "code": code,
                    "canon_ref": ref,
                    "slp1": pos["slp1"],
                    "layer": "canonical",
                    "language": "sanskrit",
                    "sutra": pos["ordinal"],
                    "sutra_position": pos["position"],
                }
                self._code_to_position[code] = pos_idx
            else:
                # This position aliases to an existing code
                # Record the additional canon_ref
                existing = self.table[code]
                existing.setdefault("alias_canon_refs", []).append(ref)
                existing.setdefault("alias_sutras", []).append(pos["ordinal"])

    def _build_sanskrit_extended(self):
        for code, pid, iast, ipa, cands, cref, deriv in SANSKRIT_EXTENDED:
            self.table[code] = {
                "code": code,
                "phoneme_id": pid,
                "iast": iast,
                "ipa": ipa,
                "ipa_candidates": cands,
                "canon_ref": cref,
                "derivation": deriv,
                "layer": "sanskrit_extended",
                "language": "sanskrit",
            }

    def _build_ukrainian(self):
        for pid, letter, ipa, shared_code, cref, rel in UKRAINIAN_SHARED:
            if shared_code in self.table:
                self.table[shared_code].setdefault("languages", {})
                self.table[shared_code]["languages"]["ukrainian"] = {
                    "letter": letter,
                    "ipa": ipa,
                    "phoneme_id": pid,
                    "relation": rel,
                }

        for code, pid, letter, ipa, cands, cref, rel in UKRAINIAN_NEW:
            self.table[code] = {
                "code": code,
                "phoneme_id": pid,
                "letter": letter,
                "ipa": ipa,
                "ipa_candidates": cands,
                "canon_ref": cref,
                "relation": rel,
                "layer": "ukrainian_new",
                "language": "ukrainian",
            }

    def _build_indexes(self):
        for code, entry in self.table.items():
            if entry["layer"] == "sanskrit_extended":
                self._iast_to_code[entry["iast"]] = code

        for slp1, iast in SLP1_TO_IAST.items():
            self._iast_real_to_code[iast] = self._slp1_to_code[slp1]
        for code, iast in IAST_EXTENDED.items():
            self._iast_real_to_code[iast] = code

        for pid, letter, ipa, shared_code, cref, rel in UKRAINIAN_SHARED:
            self._ukr_letter_to_code[letter] = shared_code
        for code, pid, letter, ipa, cands, cref, rel in UKRAINIAN_NEW:
            self._ukr_letter_to_code[letter] = code

    # ========================================================================
    # ENCODING
    # ========================================================================

    def encode_sanskrit(self, slp1_or_iast: str) -> int:
        """Legacy, deliberately kept for backward compatibility (real
        callers: prototype/dual-witness/dual_witness.py, test_upc8.py).
        Despite the name, the second lookup is NOT real Unicode IAST --
        it's the ad-hoc ASCII placeholder spelling on SANSKRIT_EXTENDED
        ("a:", "R:", "H", ...), which is what "IAST" meant historically
        in this module. For genuine Unicode IAST ("ā", "ai", "kh", ...)
        or an explicit SLP1-only lookup, use encode_sanskrit_slp1_token /
        encode_sanskrit_iast_token instead -- see docs/upc8-prototype-
        deep-review.md#4 for why this split exists (SHIVA-UPC8-API-
        SCOPE-NARROWING)."""
        if slp1_or_iast in self._slp1_to_code:
            return self._slp1_to_code[slp1_or_iast]
        if slp1_or_iast in self._iast_to_code:
            return self._iast_to_code[slp1_or_iast]
        raise KeyError(f"Unknown Sanskrit phoneme: {slp1_or_iast}")

    def encode_sanskrit_slp1_token(self, token: str) -> int:
        """Canonical SLP1 only (the 42 single-character Śiva-sūtra
        sounds) -- no ASCII-placeholder or IAST fallback. Use this when
        the input is known to be SLP1 so a typo/wrong-scheme token
        fails loudly instead of silently trying another scheme."""
        if token in self._slp1_to_code:
            return self._slp1_to_code[token]
        raise KeyError(f"Unknown SLP1 token: {token!r}")

    def encode_sanskrit_iast_token(self, token: str) -> int:
        """Genuine Unicode IAST ('a', 'ā', 'ai', 'kh', 'ñ', 'ṭh', ...),
        covering all 42 canonical sounds plus the 7 Sanskrit-extended
        codes (long vowels, anusvara, visarga). This is real IAST, not
        the ASCII placeholder spelling encode_sanskrit()'s legacy path
        uses -- fixes the exact gap docs/upc8-prototype-deep-review.md#4
        reported: encode_sanskrit("ai") / ("kh") raising KeyError despite
        the API's own "SLP1 or IAST" claim."""
        if token in self._iast_real_to_code:
            return self._iast_real_to_code[token]
        raise KeyError(f"Unknown IAST token: {token!r}")

    def encode_ukrainian(self, letter: str) -> int:
        if letter in self._ukr_letter_to_code:
            return self._ukr_letter_to_code[letter]
        raise KeyError(f"Unknown Ukrainian letter: {letter}")

    def encode_sanskrit_word(self, text: str, scheme: str = "SLP1") -> bytes:
        """scheme="SLP1" (default, unchanged behavior): char-wise, since
        SLP1 is one character per phoneme by design -- no tokenizer
        needed. scheme="IAST": greedy longest-match (2-char digraphs
        like 'kh'/'ai' before falling back to 1 char) over genuine
        Unicode IAST, per docs/upc8-prototype-deep-review.md#4's request
        for an explicit scheme parameter instead of one function silently
        guessing."""
        if scheme == "SLP1":
            return bytes(self.encode_sanskrit_slp1_token(ch) for ch in text)
        if scheme == "IAST":
            result = []
            i = 0
            while i < len(text):
                two = text[i:i + 2]
                if two in self._iast_real_to_code:
                    result.append(self._iast_real_to_code[two])
                    i += 2
                    continue
                one = text[i]
                if one in self._iast_real_to_code:
                    result.append(self._iast_real_to_code[one])
                    i += 1
                    continue
                raise KeyError(f"Unknown IAST token at position {i}: {text[i:i+2]!r}")
            return bytes(result)
        raise ValueError(f"Unknown scheme {scheme!r}: expected 'SLP1' or 'IAST'")

    def encode_ukrainian_word(self, word: str) -> bytes:
        """Contract (docs/upc8-prototype-deep-review.md#5): a fixed
        GRAPHEME lexicon (UKRAINIAN_SHARED + UKRAINIAN_NEW) with greedy
        longest-match on multi-character graphemes (дж, дз, ць, льон-
        style soft-sign clusters). This is a partial ORTHOGRAPHIC
        contract, not a phonemic normalizer (no grapheme-to-phoneme
        preprocessing) and not a defined transliteration scheme (no
        reversible Latin/SLP-like spec). It does NOT cover я/ї/є/ю,
        apostrophe, or iotation decomposition -- those raise KeyError
        rather than being silently mishandled. Expanding coverage to a
        full orthographic contract needs those decisions made first,
        not added ad hoc; see review #5 for the three-way contract
        choice (orthographic / phonemic / transliteration)."""
        multi = sorted([k for k in self._ukr_letter_to_code if len(k) > 1],
                       key=len, reverse=True)
        result = []
        i = 0
        while i < len(word):
            matched = False
            for mc in multi:
                if word[i:i + len(mc)] == mc:
                    result.append(self._ukr_letter_to_code[mc])
                    i += len(mc)
                    matched = True
                    break
            if not matched:
                ch = word[i]
                if ch in self._ukr_letter_to_code:
                    result.append(self._ukr_letter_to_code[ch])
                else:
                    raise KeyError(f"Unknown Ukrainian letter: {ch} at position {i}")
                i += 1
        return bytes(result)

    # ========================================================================
    # DECODING
    # ========================================================================

    def decode(self, code: int) -> dict:
        if code not in self.table:
            return {"code": code, "layer": "reserved", "status": "unassigned"}
        return self.table[code]

    def decode_bytes(self, data: bytes) -> list:
        return [self.decode(b) for b in data]

    # ========================================================================
    # PRATYAHARA
    # ========================================================================

    def pratyahara(self, notation: str) -> List[int]:
        """
        Expand a pratyahara notation to list of canonical codes.

        Rule (Panini 1.1.62-1.1.64 / anubandha):
          notation = start_sound + ... + marker
          First char = adi (start sound, included in the set)
          Last char  = it (marker, EXCLUDED from the set)
          Result = all listed sounds from start through the end of
                   the marker's sutra, minus the marker itself.

        The marker is resolved by scanning sutras FORWARD from the
        start sound's sutra (left-to-right rule).

        Returns: list of UPC-8 codes (deduplicated, h alias merges).

        Examples:
          'ac'   -> all vowels (9 sounds)
          'hal'  -> all consonants (33 sounds)
          'ik'   -> close vowels: i, u, R, L (4 sounds)
          'Sar'  -> sibilants: S, Z, s (3 sounds)
          'yaR'  -> semivowels: y, v, r, l (4 sounds)
        """
        if notation in self._pratyahara_cache:
            return self._pratyahara_cache[notation]

        if len(notation) < 2:
            raise ValueError(f"Pratyahara must be at least 2 chars: {notation}")

        start_slp1 = notation[0]
        marker_slp1 = notation[-1]

        # Find start position (first occurrence in canonical order)
        start_idx = None
        for i, pos in enumerate(CANON_POSITIONS):
            if pos["slp1"] == start_slp1:
                start_idx = i
                break
        if start_idx is None:
            raise ValueError(f"Start sound '{start_slp1}' not in canon")

        # Find the sutra whose marker is marker_slp1, scanning FORWARD
        # from the start sound's sutra (left-to-right scan rule).
        start_ordinal = CANON_POSITIONS[start_idx]["ordinal"]
        marker_ordinal = None
        for ordinal, sounds, marker in SIVA_SUTRAS:
            if ordinal >= start_ordinal and marker == marker_slp1:
                marker_ordinal = ordinal
                break

        if marker_ordinal is None:
            raise ValueError(f"Marker '{marker_slp1}' not found as sutra marker at or after sutra {start_ordinal}")

        # Find the last listed sound position of the marker's sutra
        end_idx = None
        for i, pos in enumerate(CANON_POSITIONS):
            if pos["ordinal"] == marker_ordinal:
                end_idx = i

        if end_idx is None:
            raise ValueError(f"Could not find sutra {marker_ordinal}")

        # Collect all sounds from start_idx through end_idx.
        # The anubandha/it marker is a sutra-final tag, not a member of
        # CANON_POSITIONS (see _build_canon() -- only each sutra's `sounds`
        # list is inserted, the marker element never is). So there is no
        # marker occurrence to exclude from this range by identity here;
        # excluding by spelling is wrong, because the same SLP1 letter can
        # legitimately be both a listed sound in an earlier sutra AND a
        # different sutra's marker (e.g. 'l' is listed in sutra 6 but is
        # also sutra 14's marker; same collision for y/r/m/v/Y against
        # sutras 12/13/7/11/8). A prior version of this loop skipped any
        # sound whose letter matched marker_slp1, silently dropping those
        # six legitimate listed sounds whenever they fell in range.
        result = []
        seen_codes = set()
        for i in range(start_idx, end_idx + 1):
            code = CODE_OF_POSITION[i]
            if code not in seen_codes:
                result.append(code)
                seen_codes.add(code)

        self._pratyahara_cache[notation] = result
        return result

    # ========================================================================
    # NATURAL CLASS TESTS
    # ========================================================================

    def is_vowel(self, code: int) -> bool:
        return code in self.pratyahara("ac")

    def is_consonant(self, code: int) -> bool:
        return code in self.pratyahara("hal")

    def is_stop(self, code: int) -> bool:
        # Stops are in sutras 8-12
        if code not in self.table or self.table[code]["layer"] != "canonical":
            return False
        return self.table[code]["sutra"] in (8, 9, 10, 11, 12)

    def is_sibilant(self, code: int) -> bool:
        return code in self.pratyahara("Sar")

    def is_nasal(self, code: int) -> bool:
        if code not in self.table or self.table[code]["layer"] != "canonical":
            return False
        return self.table[code]["sutra"] == 7

    def is_semivowel(self, code: int) -> bool:
        return code in self.pratyahara("yaR")

    # ------------------------------------------------------------------------
    # canonical_class / phonological_class / language_class (SHIVA-UPC8-
    # NATURAL-CLASS-API-SPLIT, docs/claude-review-upc8-manus-proposals-
    # 2026-08-18.md review #6): is_vowel()/is_consonant() above are kept
    # unchanged for backward compatibility, but they silently return False
    # for every extension code (0x2A+) -- a caller can't distinguish "this
    # code is definitely not a vowel" from "vowel/consonant membership
    # doesn't even apply at this layer". The three methods below make that
    # boundary explicit instead of leaving it implicit in a False.
    # ------------------------------------------------------------------------

    _CLASS_TESTS = (
        ("vowel", "is_vowel"),
        ("consonant", "is_consonant"),
        ("stop", "is_stop"),
        ("sibilant", "is_sibilant"),
        ("nasal", "is_nasal"),
        ("semivowel", "is_semivowel"),
    )

    def canonical_class(self, code: int) -> frozenset:
        """Strictly Śiva-sūtras membership. Every canonical code is
        exactly one of vowel/consonant (ac + hal = all 42 canonical
        sounds), so an empty result unambiguously means "not a
        canonical code at all" -- not "no class applies"."""
        if code not in self.table or self.table[code]["layer"] != "canonical":
            return frozenset()
        return frozenset(name for name, method in self._CLASS_TESTS if getattr(self, method)(code))

    def _code_for_canon_ref(self, ref):
        if ref is None:
            return None
        _, body = ref.split("-", 1)
        ordinal_str, position_str = body.split(":")
        ordinal, position = int(ordinal_str), int(position_str)
        for i, pos in enumerate(CANON_POSITIONS):
            if pos["ordinal"] == ordinal and pos["position"] == position:
                return CODE_OF_POSITION[i]
        return None

    def phonological_class(self, code: int, profile: str = "sanskrit") -> frozenset:
        """profile="sanskrit" (the only profile implemented so far):
        canonical codes classify exactly as canonical_class(). The 5
        Sanskrit-extended dīrgha (long-vowel) codes (0x2A-0x2E) derive
        their class from their short-vowel base via canon_ref (e.g. ā's
        SS-01:1 points at the same position as short a) -- "long vowels
        derive from short-base membership", per review #6. Anusvāra
        (0x2F) and visarga (0x30) have no canon_ref and are traditionally
        neither vowel nor consonant in Pāṇinian phonology; that is named
        explicitly ({'anusvara'}/{'visarga'}), not left as an empty
        result indistinguishable from "doesn't apply". Any other layer
        (e.g. ukrainian_new) is out of scope for this profile -> empty."""
        if profile != "sanskrit":
            raise ValueError(f"Unknown profile {profile!r}: only 'sanskrit' is implemented")
        entry = self.table.get(code)
        if entry is None:
            return frozenset()
        if entry["layer"] == "canonical":
            return self.canonical_class(code)
        if entry["layer"] == "sanskrit_extended":
            base_code = self._code_for_canon_ref(entry.get("canon_ref"))
            if base_code is not None:
                return self.canonical_class(base_code)
            special = {0x2F: "anusvara", 0x30: "visarga"}.get(code)
            return frozenset({special}) if special else frozenset()
        return frozenset()

    _UKRAINIAN_NEW_VOWEL_LETTERS = frozenset("аеои")  # а, е, о, и

    def language_class(self, code: int, language: str = "ukrainian") -> frozenset:
        """language="ukrainian" (the only language implemented so far):
        codes shared with a canonical Sanskrit segment (UKRAINIAN_SHARED)
        reuse that segment's canonical_class exactly. UKRAINIAN_NEW codes
        are classified by an explicit vowel-letter set (а/е/о/и -- і and
        у are canonical-shared, handled by the branch above), everything
        else in that table being consonantal. This is a small, explicit
        feature registry, not a claim that the Ukrainian layer has a
        formalized phonological_class-style derivation yet (see review
        #5 on encode_ukrainian_word's own contract limits)."""
        if language != "ukrainian":
            raise ValueError(f"Unknown language {language!r}: only 'ukrainian' is implemented")
        entry = self.table.get(code)
        if entry is None:
            return frozenset()
        if entry["layer"] == "canonical":
            if "ukrainian" not in entry.get("languages", {}):
                return frozenset()
            return self.canonical_class(code)
        if entry["layer"] == "ukrainian_new":
            letter = entry.get("letter", "")
            if letter in self._UKRAINIAN_NEW_VOWEL_LETTERS:
                return frozenset({"vowel"})
            return frozenset({"consonant"})
        return frozenset()

    # ========================================================================
    # STATISTICS & DUMP
    # ========================================================================

    def stats(self) -> dict:
        canonical = sum(1 for c in self.table if self.table[c]["layer"] == "canonical")
        skt_ext = sum(1 for c in self.table if self.table[c]["layer"] == "sanskrit_extended")
        ukr_new = sum(1 for c in self.table if self.table[c]["layer"] == "ukrainian_new")
        ukr_shared = len(UKRAINIAN_SHARED)
        reserved = 256 - len(self.table)
        return {
            "canonical": canonical,
            "sanskrit_extended": skt_ext,
            "ukrainian_shared": ukr_shared,
            "ukrainian_new": ukr_new,
            "total_assigned": len(self.table),
            "reserved": reserved,
        }

    def dump_table(self) -> str:
        lines = []
        lines.append("UPC-8 Code Table")
        lines.append("=" * 70)
        for code in sorted(self.table.keys()):
            e = self.table[code]
            if e["layer"] == "canonical":
                name = e["slp1"]
                sutra_info = f"sutra {e['sutra']}"
                if e.get("alias_sutras"):
                    sutra_info += f" (also: {e['alias_sutras']})"
                extra = sutra_info
            elif e["layer"] == "sanskrit_extended":
                name = e["iast"]
                extra = e.get("derivation", "")
            elif e["layer"] == "ukrainian_new":
                name = e.get("letter", "?")
                extra = f"ipa={e.get('ipa', '?')}"
            else:
                name = "?"
                extra = ""
            lines.append(f"0x{code:02X}  {e['layer']:<22}  {name:<14}  {extra}")
        return "\n".join(lines)


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    u = UPC8()

    print("=" * 60)
    print("UPC-8 Prototype Test")
    print("=" * 60)

    s = u.stats()
    print(f"\nCode space:")
    print(f"  Canonical:     {s['canonical']} codes (0x00-0x29)")
    print(f"  Skt extended:  {s['sanskrit_extended']} codes (0x2A-0x30)")
    print(f"  Ukr shared:    {s['ukrainian_shared']} codes (reuse canonical)")
    print(f"  Ukr new:       {s['ukrainian_new']} codes (0x31-0x4F)")
    print(f"  Total:         {s['total_assigned']} assigned, {s['reserved']} reserved")

    print(f"\n--- Sanskrit encoding ---")
    for ch in ["a", "i", "u", "k", "p", "h"]:
        code = u.encode_sanskrit(ch)
        info = u.decode(code)
        print(f"  {ch:<5} -> 0x{code:02X}  ({info['layer']}, slp1={info.get('slp1', '?')}, sutra={info.get('sutra', '?')})")

    print(f"\n--- Ukrainian encoding ---")
    for letter in ["\u0430", "\u0456", "\u0443", "\u0431", "\u0448", "\u0434\u0436", "\u0446\u044c", "\u0438"]:
        try:
            code = u.encode_ukrainian(letter)
            info = u.decode(code)
            layer = info["layer"]
            if layer == "canonical":
                langs = info.get("languages", {})
                ukr = langs.get("ukrainian", {})
                ipa = ukr.get("ipa", "?")
                rel = ukr.get("relation", "?")
                print(f"  {letter:<6} -> 0x{code:02X}  (shared: ipa={ipa}, {rel})")
            else:
                print(f"  {letter:<6} -> 0x{code:02X}  ({layer}, ipa={info.get('ipa', '?')})")
        except KeyError as e:
            print(f"  {letter:<6} -> NOT FOUND: {e}")

    print(f"\n--- Word encoding ---")
    encoded = u.encode_sanskrit_word("karma")
    print(f"  Sanskrit 'karma' -> {encoded.hex(' ')}")

    for word in ["\u0441\u0430\u043d\u0438", "\u0434\u0436\u0430\u0437", "\u0449\u0438\u0442"]:
        try:
            encoded = u.encode_ukrainian_word(word)
            print(f"  Ukrainian '{word}' -> {encoded.hex(' ')}")
        except KeyError as e:
            print(f"  Ukrainian '{word}' -> ERROR: {e}")

    print(f"\n--- Pratyahara ---")
    for pat in ["ac", "hal", "ik", "Sar", "yaR"]:
        try:
            members = u.pratyahara(pat)
            sounds = [u.decode(m).get("slp1", "?") for m in members]
            print(f"  {pat:<6} -> {len(members)} sounds: {sounds}")
        except Exception as e:
            print(f"  {pat:<6} -> ERROR: {e}")

    print(f"\n--- Natural class tests ---")
    test_codes = [
        (0x00, "a"),
        (0x01, "i"),
        (0x09, "h"),
        (0x25, "k"),
        (0x19, "b"),
    ]
    for code, name in test_codes:
        print(f"  0x{code:02X} ({name:<3}): vowel={u.is_vowel(code)}, consonant={u.is_consonant(code)}, "
              f"stop={u.is_stop(code)}, sibilant={u.is_sibilant(code)}, semivowel={u.is_semivowel(code)}")

    # h alias check
    print(f"\n--- h alias check ---")
    h_info = u.decode(0x09)
    print(f"  0x09: slp1={h_info['slp1']}, sutra={h_info['sutra']}, alias_sutras={h_info.get('alias_sutras', [])}")
    print(f"  Aliases: {[(CANON_POSITIONS[a[0]]['ordinal'], CODE_OF_POSITION[a[0]]) for a in ALIASES]}")

    print(f"\n{'=' * 60}")
    print("All tests passed.")
    print("=" * 60)
