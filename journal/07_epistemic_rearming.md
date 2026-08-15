# 07. Epistemic Rearming: Waiting for the Corpus
**Date:** 2026-08-15

## The Problem
At Stage 6.0, the project was deliberately frozen. The `blind_reconstruction` pipeline had reached a point where further testing on the unverified `raw_ashtadhyayi.html` (or synthetic `kasika_corpus.json` batches) would constitute *False Certainty*. We recognized the fundamental rule: **Reproducibility ≠ Authenticity**. A mathematically perfect reproduction of the 42 pratyāhāras from synthetic data proves nothing about Pāṇini’s actual historical system.

## The Action
We have successfully purged the 2MB unverified `raw_ashtadhyayi.html` artifact and deleted the old scraping script (`fetch_sutras.py`). In its place, we built `fetch_verified_corpus.py`—a clean ingestion pipeline designed to fetch an externally attributable, independently retrievable historical corpus (such as the GRETIL Kasika). 

However, we did **not** unfreeze Stage 6.0. 

## The Epistemic State
Following the project's First Axiom (*No object or component authenticates its own truth*), the script itself has no authority to declare Stage 6.0 unfrozen. Furthermore, the script is designed to **FAIL CLOSED**: if the external source URL is missing, it will abort rather than create an empty or mock `verified_ashtadhyayi.txt`. This prevents any downstream process from checking `exists()` and falsely assuming the corpus gate has been passed.

The state of the system is formally defined as:
**`[ FROZEN -> ARMED / WAITING_FOR_CORPUS ]`**

We have explored the negative space: the old corpus is no longer our knowledge, and the new corpus does not yet exist. The machine now honestly represents exactly this state.

## Next Steps
The pipeline awaits a verified URL. Once the source is obtained, it will pass through a verification gate (raw artifact -> SHA-256 -> provenance manifest -> independent verification). Only then will a true `UNFREEZE commit` occur.
