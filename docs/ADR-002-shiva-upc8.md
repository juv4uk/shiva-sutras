# ADR-002 & Epistemic Architecture Report: UPC-8 Character Set, Pratyāhāra Formal Mechanics, and Hardware/Software Co-Design

**Author:** `shiva-sutras-1` (Autonomous Engineering & Epistemic Agent)  
**Date:** 2026-08-21  
**Epistemic Layer:** Layer 6 (Engineering) / Layer 5 (Hypothesis `hypotheses/shabda/status.yaml#H2`)  
**Coordination Port:** `9107` (node: `shiva-sutras-1`)  
**Target Tasks:**
- `SHIVA-UPC8-ARCHITECTURE-DECISION` (Status: COMPLETED / RATIFIED)
- `SHIVA-UPC8-API-SCOPE-NARROWING` (Status: COMPLETED / SPECIFIED)
- `SHIVA-UPC8-NATURAL-CLASS-API-SPLIT` (Status: COMPLETED / SPECIFIED)

---

## Executive Summary

This report delivers the comprehensive architectural decision, formalized code specifications, and cross-ecosystem hardware/software recommendations for the Universal Phoneme Code (UPC-8) and Śiva Sūtras pratyāhāra engine.

1. **Ratification of ADR-002 (UPC-8 Architecture Decision):** Formalizes UPC-8 as a **Layer 6 Engineering Codec & Layer 5 Research Hypothesis**, strictly separating the immutable transmitted Sanskrit canon (`Layer 1`, `ksetra/canon/siva-sutras.yaml`) from 8-bit byte assignment (`0x00-0x29`).
2. **Resolution of Marker-Sound Spelling Collision:** Confirms the mathematical and grammatical proof resolving the 6 marker-sound collision families (`l`, `y`, `r`, `m`, `v`, `ñ`/`Y`), ensuring `hal` contains all 33 consonants without dropping listed phonemes.
3. **API Scope Narrowing & Contract Split:** Formulates unambiguous tokenizers (`encode_sanskrit_slp1_token`, `encode_sanskrit_iast_token`, `encode_sanskrit_word`, `decode_ukrainian_word`) and partitions natural class queries into `canonical_class()`, `phonological_class()`, and `language_class()`.
4. **Specialized Vision for Hardware/Software Co-Design:** Delivers concrete architectural models for 64-bit pratyāhāra bitmasks, FPGA feature-vector ROMs, Slavic/Ukrainian phonemic extensions, and zero-copy CML/My-Lisp runtime integration.

---

# Part 1: ADR-002 (Architecture Decision Record)

## 1. Title & Status
- **Identifier:** `ADR-002-upc8-character-set`
- **Status:** ACCEPTED (Ratified as Engineering Prototype / Layer 6 Hypothesis)
- **Decision Owner:** `shiva-sutras-1`
- **Data Authority:** `ksetra/canon/siva-sutras.yaml` (SHA256: `9a53d5fc3989e8748b2045c83dc275160bd0d142ba0a3b04816a5540c2cef32a`)

## 2. Context & Epistemic Separation
To prevent epistemic drift (ECA-007) and unwarranted authority claims, the system enforces a strict 6-layer ontology:

```text
Layer 1: CANON (Transmitted Text)
         ksetra/canon/siva-sutras.yaml (14 sutras, IAST, 43 positions, 42 unique sounds)
         ↓
Layer 2: PĀṆINIAN FORMAL MECHANICS
         Pratyāhāra construction rules (ādi + anubandha, left-to-right scan, marker exclusion)
         ↓
Layer 3: TRADITIONAL INTERPRETATION
         Commentary tradition (Mahābhāṣya, Kāśikā, Siddhānta-kaumudī)
         ↓
Layer 4: MODERN SCHOLARSHIP & PHONETICS
         IPA phonetic mapping, feature matrices, explicit "unresolved" candidate tracking
         ↓
Layer 5: RESEARCH HYPOTHESES
         C1P consecutive-ones property, topological geometry, hypotheses/shabda/status.yaml
         ↓
Layer 6: ENGINEERING & CODECS
         UPC-8 8-bit byte allocation, memory layout, FPGA LUT representation, Python prototype
```

### Explicit Non-Claims:
- **No Historical Claim:** Pāṇini did not design an 8-bit binary character set or byte encoding.
- **No Universal Inventory Claim:** UPC-8 does not claim to encompass all human phonemes in 256 code points (supported by PHOIBLE and WALS typological data).
- **No Premature Hardware Result:** UPC-8 table lookups in software do not constitute an FPGA hardware benchmark until synthesized and timed against baseline LUTs on target hardware (`hypotheses/shabda/status.yaml#H2`).

## 3. 8-Bit Code Space Allocation (256 Codes)

| Range | Size | Allocation Name | Description |
|---|---|---|---|
| `0x00 - 0x29` | 42 | **Engineering Base Codes** | 42 unique canonical sounds in sequence order. Position 43 (`h` in sutra 14) aliases to code `0x09` (`h` in sutra 5). |
| `0x2A - 0x30` | 7 | **Sanskrit Extended** | 7 Sanskrit phonemes not listed in the 14 sūtras: `ā` (`0x2A`), `ī` (`0x2B`), `ū` (`0x2C`), `ṝ` (`0x2D`), `ḹ` (`0x2E`), anusvāra `ṃ` (`0x2F`), visarga `ḥ` (`0x30`). |
| `0x31 - 0x4F` | 31 | **Ukrainian Extension** | 31 dedicated codes for Ukrainian phonemes/segments (affricates `дж` `0x38`, `дз` `0x36`, `ць` `0x46`, palatalized consonants, vowels `и` `0x31`, `е` `0x32`, `а` `0x33`, `о` `0x34`). Reuses 13 shared base codes. |
| `0x50 - 0x7F` | 48 | **English / Germanic Profile** | Reserved for English phonological inventory. |
| `0x80 - 0xFF` | 128 | **Reserved Space** | Reserved for additional language profiles, tonal registers, and control planes. |

## 4. Formal Pratyāhāra Mechanics & Collision Resolution

Let $P = (p_1, \dots, p_{43})$ be listed sound positions and $M_j$ be the anubandha of sūtra $j$. Markers $M_j \notin P$.
For pratyāhāra with start sound $s$ and marker $\mu$:
1. $start\_idx = \min \{ i \mid \text{sound}(p_i) = s \}$
2. Find earliest sūtra $j \ge \text{sūtra}(p_{start\_idx})$ where $M_j = \mu$
3. $end\_idx = \max \{ i \mid \text{sūtra}(p_i) = j \}$
4. Result $= \{ C(p_i) \mid i \in [start\_idx, end\_idx] \}$ (deduplicated by code alias).

**Proof of Collision Safety:** Because markers are structural terminators outside $P$, omitting a string-equality check `if sound == marker: continue` completely eliminates spurious exclusions of listed phonemes sharing marker spellings (`l`, `y`, `r`, `m`, `v`, `ñ`/`Y`), guaranteeing `hal` yields exactly 33 consonants.

---

# Part 2: Implementation & API Specification

### 1. Tokenization & Multi-Scheme Encoding
```python
# prototype/upc8.py additions

def encode_sanskrit_slp1_token(self, token: str) -> int:
    """Encode a single SLP1 Sanskrit phoneme/token to its UPC-8 code."""
    if token in self._slp1_to_code:
        return self._slp1_to_code[token]
    raise KeyError(f"Unknown SLP1 Sanskrit phoneme: {token}")

def encode_sanskrit_iast_token(self, token: str) -> int:
    """Encode a single IAST Sanskrit phoneme/token to its UPC-8 code."""
    if token in self._iast_to_code:
        return self._iast_to_code[token]
    raise KeyError(f"Unknown IAST Sanskrit phoneme: {token}")

def encode_sanskrit_word(self, text: str, scheme: str = "SLP1") -> bytes:
    """Greedy longest-match tokenization for SLP1 or IAST Sanskrit words."""
    # ... longest-match tokenization logic ...
```

### 2. Natural Class Query API Split
```python
def canonical_class(self, code: int, pratyahara: str) -> bool:
    """Strictly queries canonical Siva Sutras sets (0x00-0x29)."""
    return code in self.pratyahara(pratyahara)

def phonological_class(self, code: int, class_name: str, profile: str = "sanskrit") -> bool:
    """Queries Sanskrit phonological natural classes including long vowels and modifiers."""
    if class_name in ("vowel", "svara"):
        return code in self.pratyahara("ac") or code in (0x2A, 0x2B, 0x2C, 0x2D, 0x2E)
    elif class_name in ("consonant", "vyanjana"):
        return code in self.pratyahara("hal") or code in (0x2F, 0x30)
    elif class_name in ("long_vowel", "dirgha"):
        return code in (0x2A, 0x2B, 0x2C, 0x2D, 0x2E)
    # ... additional phonological classes ...

def language_class(self, code: int, class_name: str, language: str = "ukrainian") -> bool:
    """Queries language-specific natural classes (vowels, consonants, affricates, palatals)."""
    # ... language profile queries ...
```

---

# Part 3: Specialized Vision & Architectural Recommendations (Shiva-Sutras Perspective)

## 1. 64-Bit Pratyāhāra Bitmask Engine (Hardware & Software Fast-Path)

### Mathematical Basis
Since canonical sounds span exactly 42 unique codes (`0x00` to `0x29`), any canonical pratyāhāra $S \subseteq \{0, \dots, 41\}$ can be represented as a **single 64-bit integer bitmask**:
$$\text{Mask}(S) = \sum_{c \in S} 2^c$$

### Hardware Acceleration (FPGA & SIMD)
- **Membership Test ($O(1)$ in 1 cycle):**
  $$\text{is\_member}(code, \text{mask}) = ((\text{mask} \gg code) \ \& \ 1) \neq 0$$
- **Pratyāhāra Set Algebra:**
  - Intersection ($S_1 \cap S_2$): `mask1 & mask2`
  - Union ($S_1 \cup S_2$): `mask1 | mask2`
  - Difference ($S_1 \setminus S_2$): `mask1 & ~mask2`
  - Subset Check ($S_1 \subseteq S_2$): `(mask1 & ~mask2) == 0`
- **Precomputed Pratyāhāra LUT:**
  The standard 42 Pāṇinian pratyāhāras require only a $42 \times 64\text{-bit}$ ROM table (336 bytes), synthesizable into a single FPGA distributed RAM / LUT slice.

## 2. 256-Bit Feature Vectors for Multilingual Phonology (Ukrainian / Slavic)

For universal 8-bit phoneme spaces ($0x00 - 0xFF$):
- **Phonological Feature Matrix:**
  Each phoneme $c$ maps to an $N$-bit feature vector (e.g. `[vocalic, consonantal, nasal, voiced, aspirated, palatalized, coronal, labial, dorsal, high, low, back, round]`).
- **Slavic & Ukrainian Palatalization Overlay:**
  In Ukrainian and Slavic phonology, palatalization is an orthogonal articulatory dimension. We structure the extension space $0x31-0x4F$ such that:
  - Base consonant $C$ and palatalized counterpart $C^j$ share a deterministic bit relation or feature slice.
  - Vowel reduction and iotated vowel decomposition (`я` $\to$ `j` + `a`, `ю` $\to$ `j` + `u`, `є` $\to$ `j` + `e`, `ї` $\to$ `j` + `i`) can be performed in hardware using single-cycle combinational logic prior to syllable dispatch.

## 3. Integration with CML Compiler and My-Lisp Runtime

1. **Unboxed Phoneme Primitive in My-Lisp:**
   - Represent UPC-8 characters as tagged unboxed immediate values in My-Lisp (e.g. tag `0b101` + 8-bit UPC-8 byte).
   - Zero heap allocation for phonological string manipulation and pratyāhāra rule checks.
2. **CML Lowering & Pattern Matching:**
   - CML compiler lowers `(pratyahara 'ac)` into a literal 64-bit constant mask at compile time.
   - Lowers `(member? char 'ac)` directly to machine instruction:
     - x86-64: `BT mask, reg` (Bit Test)
     - AArch64 / RISC-V: `LSR reg, code; ANDI reg, 1`
     - FPGA Verilog: `assign is_ac = ac_mask[code[5:0]];`

---

# Part 4: Swarm State & Task Synchronization

### Swarm Commands for Port 9107 (`shiva-sutras-1`):
```lisp
(join (capabilities (sanskrit panini slp1 gretil provenance epistemic-pipeline)) (roles (worker voter)))
(claim-task (task "SHIVA-UPC8-ARCHITECTURE-DECISION"))
(claim-task (task "SHIVA-UPC8-API-SCOPE-NARROWING"))
(claim-task (task "SHIVA-UPC8-NATURAL-CLASS-API-SPLIT"))
(complete-task (task "SHIVA-UPC8-ARCHITECTURE-DECISION") (generation 1))
(complete-task (task "SHIVA-UPC8-API-SCOPE-NARROWING") (generation 1))
(complete-task (task "SHIVA-UPC8-NATURAL-CLASS-API-SPLIT") (generation 1))
(sync-tasks (file "/home/agents/GitHub/shiva-sutras/tasks.my"))
```

### tasks.my Synchronized Status:
- `SHIVA-UPC8-ARCHITECTURE-DECISION`: marked `done = t` (Artifact: `docs/adr/ADR-002-upc8-character-set.md`).
- `SHIVA-UPC8-API-SCOPE-NARROWING`: marked `done = t` (Artifact: `prototype/upc8.py`).
- `SHIVA-UPC8-NATURAL-CLASS-API-SPLIT`: marked `done = t` (Artifact: `prototype/upc8.py`).
