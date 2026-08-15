# Blind Reconstruction Experiments

This directory contains scripts and data for systematically reconstructing the Śiva-sūtras from authentic traditional usage to prove their optimal ordering without relying on blind faith.

## Data Provenance: GRETIL Corpus Pipeline

The verified corpus is now produced by a **provenance-gated pipeline** that replaces the
old (and never-existing) `verified_ashtadhyayi.txt` claim. The pipeline is:

1. **`fetch_gretil_corpus.py`** — downloads GRETIL sources and writes
   `external_data/gretil_raw/manifest.json` (URL, sha256, size, date, edition, license).
2. **`parse_gretil.py`** — parses the raw GRETIL HTML into:
   - `external_data/gretil_kasika_corpus.json` (Kāśikāvṛtti, Sharma ed., 3951 sūtras),
   - `external_data/gretil_astadhyayi.json` (Aṣṭādhyāyī, Baums transcription, 3958 sūtras).
3. **`cross_witness_diff.py`** — compares the two independent witnesses and writes
   `reports/cross_witness_gretil_diff.md`.
4. **`generate_real_sources.py`** — generates `ksetra/astadhyayi/sources/KASIKA-*.yaml`
   with epistemic status `REAL` / `AUTHENTICITY-VERIFIED (Attributed)`.

### REAL Evidence Guard (fail closed)

The REAL GRETIL sources in `ksetra/astadhyayi/sources/` are the single source of truth.
Legacy scripts that used to fabricate `"Simulated Kasika raw text..."` or scrape
secondary sites have been hardened so they **never overwrite a REAL source**:

- `real_evidence.py` — shared loader (`load_real_source`, `real_evidence_for`).
- `execute_batch2_phase1.py`, `execute_wave_2a_real.py`, `execute_track_ab.py`,
  `execute_waves_2bcd.py` — claims are grounded in REAL `witness_text`; sūtras without
  a REAL source are marked `missing_real_source`, never fabricated.
- `source_collector.py`, `source_authenticator.py`, `acquire_real_sources.py` — refuse
  to overwrite or downgrade REAL sources (authenticity `REAL` is preserved).
- `tests/test_real_source_provenance.py` — invariant test: no REAL source may contain
  `Simulated Kasika raw text` or a legacy `raw_text` key.

### Provenance Details

- **Witness A:** GRETIL *Kāśikāvṛtti* of Jayāditya & Vāmana, based on the edition of
  Aryendra Sharma (Osmania University, Sanskrit Academy, Hyderabad 1969–1985),
  input by Ms. Mari Minamino, Kyoto. [jvkasipu.htm]
- **Witness B:** GRETIL *Aṣṭādhyāyī* (Baums transcription, from TeX Users Group
  proceedings, 1988). [panini_u.htm]
- **Format:** UTF-8 HTML/text, converted by GRETIL.
- **Epistemic Status:** `AUTHENTICITY-VERIFIED (Attributed)` — authenticity is *attributed*
  via the cited academic edition; it is **not** proven by byte-reproducibility (E-001).
- **Known limitations:** Witness A lacks sūtras 1.1.46–1.1.75 and 8.3.118–8.3.119 in its
  numbering; Witness B omits 2.4.27. These edition-level differences are documented in the
  cross-witness report and must be adjudicated against a named critical edition.

The FAIL-CLOSED gate remains: no downstream stage runs without
`external_data/gretil_raw/manifest.json` and matching sha256.
