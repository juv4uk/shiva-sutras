# Sutra graph (experiment, shiva-sutras#44 lab)

Which sutra refers to which, which depends on which, which are exceptions to which: a directed,
typed graph of the Astadhyayi built from **third-party data** (`ashtadhyayi-com/data`, directory
`sutraani/`: `data.txt` with `an` anuvrtti and `ad` adhikara, `kashika.txt` with `[[a.p.n]]`
cross-references). **That data declares no license**, so this directory holds only the scripts;
the derived edge list is not committed and the source text is never copied.

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/ashtadhyayi-com/data.git
git -C data sparse-checkout set sutraani
python3 prototype/sutra_graph/build_sutra_graph.py data/sutraani /tmp/sg
python3 prototype/sutra_graph/analyze.py /tmp/sg
python3 -m unittest prototype/sutra_graph/test_sutra_graph.py    # synthetic fixture, no third-party data
```

Edge kinds: `anuvrtti` and `adhikara` (from the dataset's own fields), `adhikara_kasika` (the Kasika says "adhikara" in a sentence that cites a sutra: the scope that the dataset's `ad` field does not show, e.g. 6.1.77 `aci` up to 6.1.108; **low precision**: the stem also matches other words), `kasika_ref` (Kasika text
cites another sutra; `label` = keyword stems in the same sentence), `apavada` (Kasika says "apavada" and
either names the sutra with a `[[ref]]` (explicit-ref) or a sutra text matches the quoted/compound name
(name:...)). Every kind is a heuristic or a third-party reading, not authority. Membership of the general sutra in the `ad` field of the apavada sutra supports the target only together with the affix name; it does not prove that the phrase refers to it (aṇ can be part of a compound). The curated layers (`apavada_manual.py`, `apavada_curated.tsv`) are hypotheses: the affix map and its measurements come from one agent, and a blind check of 25 edges by another agent (25/25) tests only the wording match, not that the target is the unique general sutra. **Coverage of
`apavada` is low: about 495 sutras mention the word, 51 edges are resolved, the rest need a human
reading** (`apavada_unresolved.tsv`).

Sanity checks the analysis prints: no anuvrtti or adhikara edge points forward (0 of 9266 and 0 of
14323); the 6.1 exceptions found (6.1.88 -> 6.1.87, 6.1.97 -> 6.1.101) agree with the Kasika
table made by the panini agent.

## Checked against the Kasika (panini agent, 16 sutras; not all of 6.1.77-113)
Matches: 6.1.87/88/97/101/109/110 anuvrtti and the adhikara 6.1.84 (up to and including 6.1.111; 6.1.112 is
the boundary). **Divergences (dataset vs Kasika):** 6.1.112 has `ati` from 6.1.109 in the dataset, while
the Kasika says `ut` from 6.1.111 (`ṅasiṅasoh iti vartate, ut iti ca`); 6.1.77's `aci` adhikara to 6.1.108 is
missing from the dataset's `ad` field (kept here as `adhikara_kasika`). Exact duplicate edges (the dataset
repeats some) are removed. The other 9000+ anuvrtti edges were not compared one by one.

## Measured precision of the `apavada` edges (independent review by the shiva agent, all 51 edges of the first version)
First version: **42 correct, 9 wrong** (82%). Three error classes: a sutra named in a denial ("na badhyate"); the generic
word `pratyaya` mapped to 3.1.1; the target named only as a consequence or as the source of a word. The extractor
now drops denials (`negated`), stops generic stems, and accepts an explicit reference only within 40 characters of the
word `apavada`. On the reviewer's verdicts: all 13 sampled correct edges kept, 7 of the 9 wrong ones gone (2 remain:
6.4.174->4.1.136, 7.3.23->6.3.27); 42 edges now. **This is tuned on the reviewer's own sample, so it is NOT an
independent precision estimate**; none of the 9 edges the reviewer listed as missing (for example 6.1.89->6.1.87,
4.3.28->4.1.73) is found yet, and ~440 sutras that mention `apavada` remain unresolved.
