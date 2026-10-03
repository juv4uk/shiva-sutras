#!/usr/bin/env python3
"""Write `upc7-table-v3.tsv`: the language-faithful 7-bit table, one row per cell, with its spelling in every layout.

A CANDIDATE: it does not replace `upc7-table.tsv` (SENS pins that by sha). `pinned_bits` and `change` show how each cell differs.
Run: python3 prototype/build_v3_table.py > prototype/upc7-table-v3.tsv
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import upc7_geometry as geo  # noqa: E402
import upc7_lang as L  # noqa: E402

COLUMNS = ["bits", "hex", "class", "sound", "sa-iast", "sa-deva", "sa-cyr", "uk", "language", "pinned_bits", "change"]


def pinned_cells():
    out, by_bits = {}, {}
    with open(os.path.join(HERE, "upc7-table.tsv"), encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            by_bits[row["bits"]] = row["status"]
            if row["status"] == "assigned":
                for col in ("sa-iast", "uk"):
                    if row[col]:
                        out.setdefault((col, row[col]), row["bits"])
    return out, by_bits


def rows():
    text = L.LangText()
    pinned, by_bits = pinned_cells()
    shared_uk = {sk: tok for tok, sk in L.SHARED.items()}
    out = []
    for name, cell in L.SANSKRIT_CELL.items():
        spell = {lay: text.render([cell], lay) for lay in ("sa-iast", "sa-deva", "sa-cyr")}
        uk = shared_uk.get(name, "")
        old = pinned.get(("sa-iast", name)) or (pinned.get(("uk", uk)) if uk else None)
        out.append([cell, name, spell["sa-iast"], spell["sa-deva"], spell["sa-cyr"], uk, "Sanskrit + Ukrainian" if uk else "Sanskrit", old])
    for tok, cell in L.UK_ONLY_CELL.items():
        out.append([cell, tok, "", "", "", tok, "Ukrainian", pinned.get(("uk", tok))])
    for glyph, cell in L.SIGN_CELL.items():
        out.append([cell, geo.SIGN_NAMES[cell & 31], glyph, glyph, glyph, glyph, "signs", format(cell, "07b")])     # the sign cells are the pinned geometry's, unchanged
    for name, cell in L.SANSKRIT_SIGN_CELL.items():
        spell = {lay: L.SANSKRIT_SIGN_SPELLING[lay][name] for lay in ("sa-iast", "sa-deva", "sa-cyr")}
        out.append([cell, name, spell["sa-iast"], spell["sa-deva"], spell["sa-cyr"], "", "Sanskrit", None])
    for d, cell in L.DIGIT_CELL.items():
        out.append([cell, f"digit-{d}", d, L.DIGIT_SPELLING["sa-deva"][int(d)], d, d, "text digit", None])
    for glyph, cell in L.PUNCT_CELL.items():
        out.append([cell, f"punct-{glyph}", glyph, glyph, glyph, glyph, "punctuation", None])
    out.append([L.CAPITAL_CELL, "capital", "", "", "", "(next letter uppercase)", "Ukrainian", None])
    table = []
    for cell, sound, iast, deva, cyr, uk, lang, old in sorted(out, key=lambda r: r[0]):
        bits = format(cell, "07b")
        if old is not None:
            change = "same" if old == bits else f"moved from {old}"
        elif by_bits.get(bits) == "assigned":
            change = "same cell, no spelling in the pinned table"
        else:
            change = "new cell"
        table.append([bits, f"0x{cell:02X}", ["varga", "non-varga", "vowel", "sign"][cell >> 5], sound, iast, deva, cyr, uk, lang, old or "", change])
    return table


def main():
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(COLUMNS)
    for row in rows():
        writer.writerow([c.replace("\n", "\\n").replace("\t", "\\t") if isinstance(c, str) else c for c in row])


if __name__ == "__main__":
    main()
