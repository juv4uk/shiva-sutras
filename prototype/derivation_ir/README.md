# Panini Proof-Carrying Derivation IR & State Engine Prototype

## 1. Overview
This prototype implements the **Proof-Carrying Derivation Intermediate Representation (IR) v0.1** and State Transition Engine for the Pāṇinian grammar system (`my-lisp-panini`).

It bridges the 4-layer Vyākaraṇa architecture (*Sastra*, *Scholarly Interpretation*, *Computational Interpretation*, *My-Lisp Hypothesis*) into an executable, verifiable symbolic grammar machine.

---

## 2. Component Architecture

```
prototype/derivation_ir/
├── derivation_cell.py       # 32-bit uint32 Grammatical State Token
├── paribhasha_resolver.py   # 5-Tier Sūtra Conflict Resolution Engine
├── graph_engine.py          # Directed Semantic Graph (DAG) State Engine
├── proof_certificate.py     # JSON & S-Expression Proof Certificate Generator & Verifier
├── test_derivation_ir.py    # Comprehensive Unit and Integration Test Suite
└── README.md                # Architecture & Specification Documentation
```

---

## 3. 32-Bit `DerivationCell` Token Layout

Every phonological / morphological unit is packed into a 32-bit unsigned integer:

```
+--------------------+--------------------+--------------------+--------------------+
| Base Phoneme (8b)  | Svara/Length (8b)  | Anubandha/It (8b)  | Morpheme Tag (8b)  |
| Bits 31..24        | Bits 23..16        | Bits 15..8         | Bits 7..0          |
+--------------------+--------------------+--------------------+--------------------+
```

- **Base Phoneme (Bits 31..24):** SLP1 character code (`ord(ch)`).
- **Svara/Length (Bits 23..16):** Bitmask for Hrasva, Dīrgha, Pluta, Udātta, Anudātta, Svarita, Anunāsika.
- **Anubandha / It-Tags (Bits 15..8):** Bitmask for `Ś-it`, `P-it`, `K-it`, `Ṅ-it`, `Ṭ-it`, `Ṇ-it`, `M-it`, `Ṣ-it`.
- **Morpheme Tag (Bits 7..0):** Dhātu, Prātipadika, Vikaraṇa, Tiṅ, Sup, Kṛt, Taddhita, Āgama, Ādeśa, Abhyāsa, Lakāra.

---

## 4. Paribhāṣā Conflict Resolution Hierarchy

The engine implements the 5-tier traditional priority ordering:
1. **Apavāda > Utsarga:** Special exception rules override general rules (e.g. 2.4.75 *ślu* overrides 3.1.68 *śap*).
2. **Nitya > Anitya:** Rules whose conditions remain valid regardless of whether the competing rule applies override non-constant rules.
3. **Antaraṅga > Bahiraṅga:** Rules with internal / root-adjacent causes override rules with external causes.
4. **Para > Pūrva:** Within Sapta-adhyāyī (1.1 - 8.1), 1.4.2 *vipratiṣedhe paraṁ kāryam* selects the later rule.
5. **Asiddhatva (8.2.1 *pūrvatrāsiddham*):** Rules in Tripādī (8.2 - 8.4) are strictly invisible to Sapta-adhyāyī and prior Tripādī rules.

---

## 5. Directed Semantic Graph (DAG) State Engine

- **Immutable States:** Each state $S_i$ is uniquely identified by a canonical SHA-256 hash computed over its sorted terms and normalized relations.
- **Event Provenance:** Transitions depend explicitly on previous state observations, applicability checks, and rule decisions.
- **Self-Verifying Proof Certificates:** The verifier mathematically proves that state hashes, event dependencies, and morphological transformations form an unbroken chain without missing steps.

---

## 6. Running Tests

To run the complete test suite:
```bash
python3 test_derivation_ir.py
```
Or within the declared pure Guix shell:
```bash
guix shell --pure -m manifest.scm -- python3 test_derivation_ir.py
```
