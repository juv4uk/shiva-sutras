# Blind Reconstruction Experiments

This directory contains scripts and data for systematically reconstructing the Śiva-sūtras from authentic traditional usage to prove their optimal ordering without relying on blind faith.

## Data Provenance: `verified_ashtadhyayi.txt`

The file `verified_ashtadhyayi.txt` is the verified academic data source used by our extraction scripts, replacing the old unverified HTML scrape.

**Provenance Details:**
- **Source:** GRETIL (Göttingen Register of Electronic Texts in Indian Languages) mirror.
- **Base Edition:** *Kāśikāvṛtti*, edited by Aryendra Sharma (input by Ms. Mari Minamino).
- **Format:** UTF-8 encoded text.
- **Acquisition Method:** Downloaded via `fetch_verified_corpus.py` from the stable INDOLOGY/GRETIL-mirror on GitHub.
- **Epistemic Status:** AUTHENTICITY-VERIFIED (Attributed).
- **Notes:** This file contains the sūtras as established by standard critical editions. It provides the necessary epistemic foundation to test the linguistic independence of the 42-class model without the risk of *False Certainty* associated with synthetic or unverified web scrapes.
