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
(name:...)). Every kind is a heuristic or a third-party reading, not authority. **Coverage of
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
