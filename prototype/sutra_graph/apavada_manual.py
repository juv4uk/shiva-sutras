#!/usr/bin/env python3
"""Curated affix -> sutra layer for `apavada` mentions (HYPOTHESIS, not canon).

Input: the data dir of build_sutra_graph.py, and a map TSV (affix, target_sutra, condition_field,
condition_value, ...) made by the shiva agent. A Kasika sentence "<affix>-o 'pavadah" under a sutra
S gives the edge S -> target, only if the map's condition holds for S (`ad` contains the target, or
`an` contains the word). One map row per affix with a condition; rows without one (name) fire
unconditionally. Affixes are matched only as the exact word `<affix>o'` before "pavada".
"""
import argparse, collections, json, os, re

DEVA = {"aṇ": "अण्", "ṭhak": "ठक्", "yat": "यत्", "cha": "छ", "ṭhañ": "ठञ्", "ka": "क",
        "ṛtvaṇ": "ऋत्वण्", "iñ": "इञ्", "ktin": "क्तिन्", "tral": "त्रल्", "ap": "अप्", "ghañ": "घञ्"}


def sid(five):
    return f"{five[0]}.{five[1]}.{int(five[2:])}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir"); ap.add_argument("map_tsv"); ap.add_argument("out_tsv")
    a = ap.parse_args()
    data = json.load(open(os.path.join(a.data_dir, "data.txt"), encoding="utf-8"))["data"]
    kas = json.load(open(os.path.join(a.data_dir, "kashika.txt"), encoding="utf-8"))
    field = {f"{x['a']}{x['p']}{int(x['n']):03d}": x for x in data}
    rows = [l.rstrip("\n").split("\t") for l in open(a.map_tsv, encoding="utf-8")][1:]
    # shiva §8: for thak the condition `ad has 4.4.1` is wrong in 5.1.66-71; a second one (`ad has 5.1.19`) is needed
    rows.append(["ṭhak", "5.1.19", "ad", "5.1.19", "n/a", "shiva §8 (2026-09-30), not in his TSV", "hypothesis"])
    by_affix = collections.defaultdict(list)
    for r in rows:
        by_affix[r[0]].append(r)
    out, seen = [], collections.Counter()
    for k, body in kas.items():
        for sent in re.findall(r"[^।॥\n]+", body):
            if "पवाद" not in sent:
                continue
            # the whole word is `<affix>o'pavadah` (virama dropped by sandhi), or for a stem in -a: `<affix>syapavadah`
            for m in re.finditer(r"(\S+?)(?:ोऽ|स्या)पवाद", sent):
                word = m.group(1).split()[-1].lstrip("<>")
                for aff, rs in by_affix.items():
                    if word != DEVA[aff].rstrip("्"):
                        continue
                    seen[aff] += 1
                    ad = [p.partition("$")[2].replace("$", ".") for p in field[k]["ad"].split("##") if p]
                    for r in rs:
                        f, val = r[2], r[3]
                        if val.startswith("none"):                # two candidate targets, no condition: not decidable
                            continue
                        ok = (f == "name") or (f == "ad" and val in ad) or (f == "an" and val in field[k]["an"])
                        if ok and r[1] != sid(k):
                            out.append((sid(k), r[1], "apavada", "manual:" + aff))
    out = list(dict.fromkeys(out))
    with open(a.out_tsv, "w", encoding="utf-8") as f:
        f.write("src\tdst\tkind\tlabel\n")
        f.writelines("\t".join(e) + "\n" for e in out)
    print(len(out), "manual edges; affix sentences seen:", dict(seen))


if __name__ == "__main__":
    main()
