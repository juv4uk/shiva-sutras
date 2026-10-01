#!/usr/bin/env python3
"""Reading the external-oracle TSVs (columns `*_iast`, `*_deva`, `*_cyr`) for the tests.

A cell is a sequence of sound names in the project's text format: tokens side by side, a middle
dot only where the plain reading would differ, `|` between the left and right part of a sandhi
result. `names(cell)` returns the tuple of IAST names; the avagraha ’ and the long ḷ ḹ (which the
codec does not write, Kasika txt 389) are read as tokens of their own.
"""

import csv
import os
import unicodedata

import upc14v2 as g
import upc14v2_sandhi as sd

HERE = os.path.dirname(__file__)
AVAGRAHA = "’"


def rows(name):
    """The data rows of `oracles/<name>` (comment lines start with `#`)."""
    with open(os.path.join(HERE, "oracles", name), encoding="utf-8") as handle:
        lines = [line for line in handle if not line.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))


def _vocabulary():
    out = {sd.label_of(c) for c in g.SOUNDS.values()}
    out |= set(sd._LONG)                                             # ā ī ū ṝ ḹ
    for text in list(out):
        nasal = unicodedata.normalize("NFC", text + "̃")
        try:
            sd.code_of(nasal)
            out.add(nasal)
        except g.GraphError:
            pass
    out.add(AVAGRAHA)
    return sorted(out, key=len, reverse=True)


_VOCAB = _vocabulary()


def names(cell):
    """Tuple of IAST sound names in `cell` (no `|`): longest token first, `·` is only a boundary."""
    text, out, i = unicodedata.normalize("NFC", cell), [], 0
    while i < len(text):
        if text[i] == "·":
            i += 1
            continue
        for token in _VOCAB:
            if text.startswith(token, i):
                out.append(token)
                i += len(token)
                break
        else:
            raise ValueError(f"{text[i:i + 3]!r} at {i} in {cell!r} is not a sound name")
    return tuple(out)


def parts(cell):
    """`d|a` -> (("d",), ("a",)): a tuple of name-tuples, one per `|` part."""
    return tuple(names(part) for part in cell.split("|"))
