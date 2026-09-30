# UPC-14: a sutra-first 14-bit text code (experiment, shiva-sutras#44)

**Status: EXPERIMENTAL CANDIDATE beside UPC-7.** It changes no UPC-7 cell, table, pin
or witness. UPC-7 remains the ratified Text7 authority. This asks a design question:
what if the Śiva-sūtras are the *basis* of the code, then Sanskrit, then Ukrainian?

Owner direction (2026-09-30): pick the width from what an FPGA does cheaply, not from
8/16/32/64 symmetry. fpga-lisp `README.md:15`: a word is 32 bits = 4 tag + **28** value
bits, and 28 = 2 × 14 = 4 × 7. Fourteen divides the payload with no waste; fifteen or
sixteen leaves 13 or 12 bits unused.

## The layout

```text
code (14 bits) = K(2) | R(6) | M(6)

K = 00  śiva-sūtra   R = rank in the 14 sūtras (0..56)   M = modifiers
K = 01  Sanskrit     R = index of a Sanskrit sign
K = 10  Ukrainian    R = index of a sound the sūtras do not contain
K = 11  common       R = index of a common sign / text digit
```

Strata in the order the owner asked: the sūtras first, Sanskrit second, Ukrainian third.
For K=00 the **numeric order of R is the recited order** of the sūtras: 14 sūtras,
43 sounds and 14 it-markers, 57 positions (fits in 6 bits with 7 spare).

`M = accent(2) spare(1) nasal(1) length(2)` and exists only on the vowels
a i u ṛ ḷ e o ai au; e o ai au are long by nature, so they have no length modifier.
Everything else in `M` (and every rank ≥ 57) fails closed.

## What the sūtra order buys: a pratyāhāra is an interval

`ac`, `hal`, `iṇ` are intervals of `R`, with `M` ignored, so the long, nasal and accented
forms are members automatically (Pāṇini 1.1.69, savarṇa). There is no mask table.
Membership is two comparisons on the rank field. The marker keeps its own rank, so
"the ṇ of sūtra 1" and "the ṇ of sūtra 6" are different positions (ranks 3 and 19).

## Evidence (empirically confirmed, local run; `test_upc14.py`, 30 tests)

- The sūtra table typed here equals `ksetra/canon/siva-sutras-encoded.yaml` for all 14
  sūtras and markers (a separate source).
- **39 of the 42 classical pratyāhāras** in `ksetra/astadhyayi/pratyahara-usage.yaml`
  equal the interval derived from the ranks.
- **3 of the 42 entries in that YAML are wrong**, not the model (found by this check):
  `yaṇ` lists all 33 consonants from y (the set of `yar`; the oracle and 6.4.81 give
  {y v r l}); `has` and `jhas` are typed with a plain `s` (no such marker) and carry the
  whole `hal` / `jhal` sets. They are listed in the test with the reason, not skipped.
- A pratyāhāra *name* does not say which marker occurrence it means: classical `iṇ` uses
  the second ṇ (sūtra 6); with the first it would be `{i, u}`. In rank terms this is an
  explicit `nth` (`aṇ2` in the YAML is the same thing). The rule "first marker" of the
  oracle document is therefore not enough by itself.
- **Nothing of UPC-7 is lost:** all 107 assigned UPC-7 cells map to 107 *distinct* valid
  UPC-14 codes (`upc14_bridge.py`); 5 Sanskrit signs, 14 Ukrainian-only sounds, 27 common
  signs, the rest are sūtra cells. Ukrainian letters that are Sanskrit sounds (к і т н с
  …) land on the sūtra cell, so `kit` (SLP1) and `кіт` are one code stream.
- UPC-7's own 68 tests still pass unchanged.

## Where UPC-14 differs from UPC-7 (on purpose)

- **ai / au** have their own ranks (sūtra 4). UPC-7 encodes them as the long form of the
  e / o rows (a vṛddhi convention). The bridge maps `(e, long)` to `ai`.
- **it-markers** are cells in K=00 (the sūtra text can be written). In UPC-7 they do not
  exist. They are metalinguistic, not sounds.
- **`ha` occurs twice** in the sūtras (5 and 14): both ranks exist so the sūtra text can be
  written; ordinary text uses the first; both are the same sound. This is the one
  documented exception to one code per sound.
- **Accents** (udātta, anudātta, svarita) are a modifier, not separate cells.
- 216 defined cells out of 16384; every other bit pattern is invalid, on purpose.
- Text digits `0-9` are a **candidate** (K=11, #34), not ratified, and not in the bridge.

## Open, do not read as done

- No Ukrainian pratyāhāra: the Ukrainian-only sounds are outside the sūtras and have no
  rank order.
- Accent and length modifiers, and the pluta value (reserved), are a design proposal
  checked for internal consistency only, not against a Vedic corpus.
- Nothing here is measured on hardware; "two per FPGA cell" is arithmetic (2 × 14 = 28).
- Text density: 14 bits per sound is twice UPC-7's 7.
- No CI job (see the workflow) covers the FPGA claim; the tests cover the code only.
- Independence: the YAML sources are separate from this code, but the bridge and the
  tests were written by the same author.

## Non-claim

This is an engineering code. It is not evidence that Pāṇini used numeric codes, and it
does not modify the transmitted Śiva-sūtra text.
