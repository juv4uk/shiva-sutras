#!/usr/bin/env python3
"""
Sutra dependency graph of the Astadhyayi, from third-party data (experiment, shiva-sutras#44 lab).

Input: a checkout of https://github.com/ashtadhyayi-com/data (directory `sutraani/`): `data.txt`
(3983 sutras with `an` anuvrtti, `ad` adhikara, `type`) and `kashika.txt` (Kasika per sutra,
with `[[a.p.n]]` cross-references). That data declares NO license: this script READS it and writes
only derived edges (sutra ids, edge kind, the inherited word) to a directory the caller chooses.
Nothing of the source text is copied into the repository.

Edge kinds (every one is a HEURISTIC or third-party reading, not authority):
  anuvrtti   sutra -> sutra   from `an`: the word is carried into the sutra from an earlier one
  adhikara   sutra -> sutra   from `ad`: the sutra lies under that governing (adhikara) sutra
  kasika_ref sutra -> sutra   from `[[a.p.n]]` in the Kasika on the sutra; `flags` records which
                              keyword stems occur in the same sentence (apavada, pratishedha, ...)
  apavada    sutra -> sutra   only from the pattern "<quoted sutra>-sya apavadah" in the Kasika,
                              resolved against sutra texts; the exception points at the general rule
"""
import argparse, collections, json, os, re, sys

def sid(five):              # '61088' -> '6.1.88'
    return f"{five[0]}.{five[1]}.{int(five[2:])}"

_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

def latin_digits(s):
    return s.translate(_DIGITS)

def norm(text):             # compare sutra quotations: no spaces, no hyphens, no final visarga
    t = re.sub(r"[\s\-‌‍।॥]+", "", text)
    return t[:-1] if t.endswith("ः") else t

FLAGS = {"apavada": "अपवाद", "pratishedha": "प्रतिषेध", "nishedha": "निषेध",
         "atidesha": "अतिदेश", "vibhasha": "विभाषा", "niyama": "नियम", "badhaka": "बाध"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir", help="ashtadhyayi-com/data/sutraani")
    ap.add_argument("out_dir")
    a = ap.parse_args()
    data = json.load(open(os.path.join(a.data_dir, "data.txt"), encoding="utf-8"))["data"]
    kas = json.load(open(os.path.join(a.data_dir, "kashika.txt"), encoding="utf-8"))
    by_id = {f"{x['a']}{x['p']}{int(x['n']):03d}": x for x in data}
    text_of = {sid(k): v["s"] for k, v in by_id.items()}
    key_of = {}
    for k, v in by_id.items():
        key_of.setdefault(norm(v["s"]), []).append(sid(k))
    edges = []
    # anuvrtti and adhikara
    for k, v in by_id.items():
        for part in filter(None, v["an"].split("##")):
            word, _, src = part.rpartition("$")
            if src.isdigit() and len(src) == 5:
                edges.append((sid(k), sid(src), "anuvrtti", word))
        for part in filter(None, v["ad"].split("##")):
            word, _, rest = part.partition("$")
            bits = rest.split("$")
            if len(bits) == 3 and all(b.isdigit() for b in bits):
                edges.append((sid(k), f"{bits[0]}.{bits[1]}.{bits[2]}", "adhikara", word))
    # Kasika references and apavada mentions
    sentence = re.compile(r"[^।॥\n]+")
    ref_rx = re.compile(r"\[\[([0-9०-९]+\.[0-9०-९]+\.[0-9०-९]+)\]\]")
    # the word carrying "apavada": `X-apavadah` (compound), `X-syapavadah`, `X apavadah`
    apav_rx = re.compile(r"([^\s।॥<>\[\]]*?)(?:स्य)?\s*(?:ा|अ)?पवाद")
    unresolved = collections.Counter()
    for k, body in kas.items():
        me = sid(k)
        for sent in sentence.findall(body):
            flags = ",".join(n for n, stem in FLAGS.items() if stem in sent)
            refs = [latin_digits(m.group(1)) for m in ref_rx.finditer(sent)]
            for r in refs:
                edges.append((me, r, "kasika_ref", flags))
            if "पवाद" not in sent:
                continue
            if refs:                                   # (a) the sentence names the sutra it is an exception to
                for r in refs:
                    if r != me:
                        edges.append((me, r, "apavada", "explicit-ref"))
                continue
            resolved = False
            for m in apav_rx.finditer(sent):           # (b) resolve the quoted/compound name against sutra texts
                stem = norm(m.group(1))
                for tgt in key_of.get(stem, ()):
                    if tgt != me:
                        edges.append((me, tgt, "apavada", "name:" + m.group(1)))
                        resolved = True
            if not resolved:                           # (c) kept only as a count
                unresolved[me] += 1
    with open(os.path.join(a.out_dir, "apavada_unresolved.tsv"), "w", encoding="utf-8") if os.makedirs(a.out_dir, exist_ok=True) is None else None as f:
        f.write("sutra\tmentions\n")
        for s, n in sorted(unresolved.items()):
            f.write(f"{s}\t{n}\n")
    os.makedirs(a.out_dir, exist_ok=True)
    with open(os.path.join(a.out_dir, "edges.tsv"), "w", encoding="utf-8") as f:
        f.write("src\tdst\tkind\tlabel\n")
        for e in edges:
            f.write("\t".join(e) + "\n")
    c = collections.Counter(e[2] for e in edges)
    print(len(by_id), "sutras;", dict(c))

if __name__ == "__main__":
    main()
