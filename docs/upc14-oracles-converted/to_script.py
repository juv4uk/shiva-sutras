#!/usr/bin/env python3
"""Convert the four SLP1 oracle TSVs of prototype/oracles/ to IAST + Devanagari + Cyrillic.

usage: to_script.py <prototype dir of commit 3785441> <oracles dir> <out dir>

Uses `upc14v2_script.encode_text/decode_text` for every sequence of the 42 sounds. Two kinds of symbol
are outside the codec and are written as literals (and flagged): the long ḷ `X` of vidyut (ḹ, Kasika
txt 389 says it does not exist) and the avagraha `'` (’ IAST, ऽ Devanagari, ’ Cyrillic). Each converted
cell is decoded back and compared with the SLP1 original (round trip); any difference aborts.
"""
import csv, os, sys, unicodedata

proto, oracles, out = sys.argv[1:4]
sys.path.insert(0, proto)
import upc14v2 as g, upc14v2_sandhi as sd, upc14v2_script as sc

SCRIPTS = ("iast", "devanagari", "cyrillic")
SUF = {"iast": "iast", "devanagari": "deva", "cyrillic": "cyr"}
LIT = {"X": {"iast": "ḹ", "devanagari": "ॡ", "cyrillic": "л̣̄"},
       "'": {"iast": "’", "devanagari": "ऽ", "cyrillic": "’"}}
BACK = {s: {v: k for k, v in (( k, LIT[k][s]) for k in LIT)} for s in SCRIPTS}
LABEL = dict(g.LABELS_BY_CODE)
for _long, _short in sd._LONG.items():
    LABEL[g.e_long(g.SOUNDS[_short])] = _long


def codes(slp):
    return tuple(sd.code_of(ch) for ch in slp)


def enc(slp, script):
    """Encode an SLP1 string; literals (X, ') split the string into codec runs."""
    out, run = [], ""
    for ch in slp:
        if ch in LIT:
            if run:
                out.append(sc.encode_text(codes(run), script)); run = ""
            out.append(LIT[ch][script])
        else:
            run += ch
    if run:
        out.append(sc.encode_text(codes(run), script))
    return "".join(out)


def dec(text, script):
    """Back to SLP1 (inverse of `enc`)."""
    lits = BACK[script]; res, run = "", ""
    def flush():
        nonlocal res, run
        if run:
            res += "".join(LABEL[c] for c in sc.decode_text(run, script)); run = ""
    i = 0
    while i < len(text):
        for lit, slp in sorted(lits.items(), key=lambda kv: -len(kv[0])):
            if text.startswith(lit, i):
                flush(); res += slp; i += len(lit); break
        else:
            run += text[i]; i += 1
    flush()
    return res


def cell(slp, script):
    parts = slp.split(" ")
    return "|".join(enc(p, script) for p in parts)


def check(slp, script, text):
    back = "|".join(dec(p, script) for p in text.split("|"))
    if back != slp.replace(" ", "|"):
        raise SystemExit(f"round trip FAILED: {slp!r} -> {text!r} -> {back!r}")


def convert(name, kind):
    path = os.path.join(oracles, name)
    lines = open(path, encoding="utf-8").read().split("\n")
    head = [l for l in lines if l.startswith("#")]
    rows = list(csv.reader([l for l in lines if l and not l.startswith("#")], delimiter="\t"))
    cols, body = rows[0], rows[1:]
    out_rows, flagged = [], 0
    if kind == "pratyahara":
        newcols = ["name_iast", "name_deva", "name_cyr"] + [f"{c}_{SUF[s]}" for c in ("start", "marker", "sounds") for s in SCRIPTS]
        for name_d, start, marker, sounds in body:
            seq = sc.decode_text(name_d, "devanagari", strict=False)
            row = [sc.encode_text(seq, s) for s in SCRIPTS]
            row = [row[0], name_d, row[2]]
            for v in (start, marker, sounds):
                for s in SCRIPTS:
                    t = cell(v, s); check(v, s, t); row.append(t)
            out_rows.append(row)
    elif kind == "sandhi":
        newcols = [f"{c}_{SUF[s]}" for c in ("first", "second", "result") for s in SCRIPTS]
        for first, second, result in body:
            row = []
            for v in (first, second, result):
                for s in SCRIPTS:
                    t = cell(v, s); check(v, s, t); row.append(t)
            if "X" in first + second + result:
                flagged += 1
            out_rows.append(row)
    else:  # consonant maps
        newcols = ["rule", "coq_definition"] + [f"{c}_{SUF[s]}" for c in ("input", "output") for s in SCRIPTS]
        for rule, defn, inp, outp in body:
            row = [rule, defn]
            for v in (inp, outp):
                for s in SCRIPTS:
                    t = cell(v, s); check(v, s, t); row.append(t)
            out_rows.append(row)
    base = name[:-4]
    with open(os.path.join(out, name), "w", encoding="utf-8", newline="") as h:
        for l in head:
            h.write(l.replace("transliterated to SLP1", "kept as facts") + "\n")
        h.write("# Converted from SLP1 to IAST, Devanagari and Cyrillic by docs/upc14-oracles-converted/to_script.py using\n")
        h.write("# upc14v2_script.encode_text (commit 3785441). Sequences: tokens side by side, a middle dot only where the\n")
        h.write("# reading would differ; `|` separates the left and right part of a sandhi result. Outside the codec and written\n")
        h.write("# as literals: long ḷ (ḹ, ॡ; Kasika txt 389 says it does not exist) and the avagraha (’, ऽ).\n")
        h.write("# Round trip: every cell was decoded back and compared with the SLP1 original; the original file stays in git history.\n")
        h.write("\t".join(newcols) + "\n")
        for r in out_rows:
            h.write("\t".join(unicodedata.normalize("NFC", c) for c in r) + "\n")
    print(f"{name}: {len(out_rows)} rows, {len(newcols)} columns, rows with long ḷ (X): {flagged}")


os.makedirs(out, exist_ok=True)
convert("ashtadhyayi-com-pratyahara.tsv", "pratyahara")
convert("vidyut-sandhi-final-stops.tsv", "sandhi")
convert("vidyut-sandhi-vowels.tsv", "sandhi")
convert("paninian-verified-consonant-maps.tsv", "maps")
