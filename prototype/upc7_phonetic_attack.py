#!/usr/bin/env python3
"""Phonetic attack on the 16 shared Sanskrit/Ukrainian letters (research, hypothesis; dossier of shiva-sutras PR #99).

Measured from the repository's artifacts: Ukrainian lemmas of dict_uk (base.lst), Sanskrit words of the Kasika (Devanagari, decoded by
upc14v2_script), the SENS literal table docs/research/data/1700-uk-literals-vs-upc7.tsv (read only, path below). No phonetics is computed here:
this file counts what the shared cells do to cross-layout rendering and to text identity.
"""
import os
import re
import sys
from collections import Counter
from typing import Dict, List, Optional, Tuple

import uk_orth
import upc14v2_script as sc
import upc7_derive as D
import upc7_lang as L

DICT_UK = "/home/agents/GitHub/dict_uk/data/dict/base.lst"
_KASIKA_REL = os.path.join("ksetra", "sanskritworld_texts", "shastra", "grammar", "kAshikAvRRitti.txt")      # a git submodule: absent in a bare worktree
KASIKA = next((p for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", _KASIKA_REL), os.path.join("/home/agents/GitHub/shiva-sutras", _KASIKA_REL)) if os.path.exists(p)), None)
SENS_LITERALS = "/home/agents/work/sens-sonnet/docs/research/data/1700-uk-literals-vs-upc7.tsv"

UNAMBIGUOUS = ("к", "ґ", "т", "д", "н", "п", "б", "м", "і", "у", "й", "с")      # the 12 pairs
CLOSE = ("р", "л", "в", "ш")
SHARED_CELLS_12 = {L.UK_CELL[t] for t in UNAMBIGUOUS}
SHARED_CELLS_16 = {L.UK_CELL[t] for t in UNAMBIGUOUS + CLOSE}


def ukrainian_lemmas() -> List[str]:
    out = set()
    with open(DICT_UK, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(" ") or not line.strip():
                continue
            word = line.split()[0]
            if re.fullmatch(r"[а-щьюяєіїґ']+", word):
                out.add(word)
    return sorted(out)


def uk_cells(word: str) -> Optional[Tuple[int, ...]]:
    try:
        return tuple(L.UK_CELL[t] for t in uk_orth.to_tokens(word))
    except Exception:                                    # noqa: BLE001
        return None


def sanskrit_words(limit: int = 400000) -> List[str]:
    text = open(KASIKA, encoding="utf-8").read()
    words = set(re.findall(r"[ऀ-ॣ०-९]+", text))
    return sorted(words)[:limit]


def sa_cells(word: str) -> Optional[Tuple[int, ...]]:
    try:
        return tuple(D.derive(v) for v in sc.decode_text(word, "devanagari", strict=False))
    except Exception:                                    # noqa: BLE001
        return None


def stats() -> Dict[str, object]:
    uk = {w: c for w in ukrainian_lemmas() if (c := uk_cells(w)) is not None}
    sa = {w: c for w in sanskrit_words() if (c := sa_cells(w)) is not None}
    out: Dict[str, object] = {"uk_lemmas_encoded": len(uk), "sa_words_encoded": len(sa)}
    for name, cells in (("12", SHARED_CELLS_12), ("16", SHARED_CELLS_16)):
        out[f"uk_renderable_in_sa_{name}"] = sum(1 for c in uk.values() if set(c) <= cells)
        out[f"sa_renderable_in_uk_{name}"] = sum(1 for c in sa.values() if set(c) <= cells)
    g_cell, h_cell = L.UK_ONLY_CELL["г"], L.SANSKRIT_CELL["h"]
    out["uk_lemmas_with_g(г)"] = sum(1 for c in uk.values() if g_cell in c)
    out["sa_words_with_h"] = sum(1 for c in sa.values() if h_cell in c)
    # words made only of shared cells, same cell stream in both languages (homographs across layouts)
    uk_by = {}
    for w, c in uk.items():
        if set(c) <= SHARED_CELLS_16:
            uk_by.setdefault(c, []).append(w)
    homo = [(c, uk_by[c], [w for w, cc in sa.items() if cc == c]) for c in uk_by if any(cc == c for cc in sa.values())]
    out["homographs_16"] = len(homo)
    out["homographs_12"] = sum(1 for c, _, _ in homo if set(c) <= SHARED_CELLS_12)
    out["homograph_examples"] = [(L.LangText().render(c, "sa-iast"), u[:2], s[:2]) for c, u, s in homo[:12]]
    return out


def sens_literal_counts() -> Optional[Dict[str, int]]:
    if not os.path.exists(SENS_LITERALS):
        return None
    import csv
    rows = [r for r in csv.DictReader(open(SENS_LITERALS, encoding="utf-8"), delimiter="\t") if r["result"] == "encodes"]
    out = {"encodable_literals": len(rows)}
    for ch in "гхрлвш":
        out[ch] = sum(1 for r in rows if ch in r["literal_prefix"].lower())      # the file keeps a PREFIX of each literal: a lower bound
    return out


def script_probe() -> Dict[str, str]:
    """How the shared and the near-confusable letters read in each Sanskrit-Cyrillic spelling."""
    t = L.LangText()
    out = {}
    for layout, s in (("sa-cyr", "р"), ("sa-cyr", "р̣"), ("sa-cyr", "ш"), ("sa-cyr", "ш́"), ("sa-cyr", "ш̣"), ("sa-cyr", "в"), ("uk", "ш"), ("uk", "р"), ("sa-iast", "ṛ"), ("sa-iast", "ś"), ("sa-iast", "ṣ")):
        try:
            cells = t.encode(s, layout)
            out[f"{layout}:{s!r}"] = "->".join(format(c, "07b") for c in cells) + " = " + t.render(cells, "sa-iast") if layout != "uk" else "->".join(format(c, "07b") for c in cells)
        except Exception as exc:                        # noqa: BLE001
            out[f"{layout}:{s!r}"] = f"{type(exc).__name__}"
    return out


if __name__ == "__main__":
    for k, v in stats().items():
        print(k, v)
    print("SENS", sens_literal_counts())
    for k, v in script_probe().items():
        print(k, v)
