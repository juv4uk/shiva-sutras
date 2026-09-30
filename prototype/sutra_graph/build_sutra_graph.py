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

FLAGS = {"apavada": "अपवाद", "pratishedha": "प्रतिषेध", "nishedha": "निषेध", "vipratishedha": "विप्रतिषेध",
         "paratvat": "परत्वात्", "atidesha": "अतिदेश", "vibhasha": "विभाषा", "niyama": "नियम",
         "nivrtti": "निवृत्ति", "badha": "बाध"}
# a sutra named only in a denial ("...(6.1.95) iti etat tu pararupam na badhyate") is not an exception edge
GENERIC_STEMS = {"प्रत्यय", "संज्ञा", "अङ्ग", "धातु", "विभक्ति"}   # a general word is not the name of one sutra
NEGATED_BADHA = re.compile(r"न\s+(?:तु\s+)?बाध|बाध[^\s।॥]*\s+न\b|न\s+तु\s+[^\s।॥]+\s+बाध")

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
    # sutra texts as suffix keys: nominative ending removed (`-m`, visarga), longest first
    suffix_keys = sorted(((re.sub(r"(म्|ः)$", "", k), v) for k, v in key_of.items()), key=lambda kv: -len(kv[0]))
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
            negated = bool(NEGATED_BADHA.search(sent))
            if negated:
                flags = (flags + ",negated").strip(",")
            refs = [latin_digits(m.group(1)) for m in ref_rx.finditer(sent)]
            for r in refs:
                edges.append((me, r, "kasika_ref", flags))
            if "धिकार" in sent:                        # scope declared in the Kasika (e.g. 6.1.77: "aci" up to 6.1.108)
                for r in refs:
                    if r != me:
                        edges.append((me, r, "adhikara_kasika", (sent.split() or [""])[0]))
            if "पवाद" not in sent:
                continue
            resolved = False
            if not negated:                            # (a) a sutra cited right next to `apavada` (<= 40 characters)
                apav_at = [m.start() for m in re.finditer("पवाद", sent)]
                for m in ref_rx.finditer(sent):
                    r = latin_digits(m.group(1))
                    near = any(0 <= a - m.end() <= 40 or 0 <= m.start() - a <= 12 for a in apav_at)
                    if r != me and near:
                        edges.append((me, r, "apavada", "explicit-ref"))
                        resolved = True
            words = sent.replace("<<", " ").replace(">>", " ").split()
            for m in apav_rx.finditer(sent):           # (b) names: a compound before `apavada`; sandhi joins it to the
                for width in (1, 2, 3):                # preceding word, so a SUFFIX of the stem may equal a sutra text
                    stem = norm(" ".join(sent[:m.end(1)].split()[-width:]))
                    for key, ids in suffix_keys:
                        if len(key) >= 5 and key not in GENERIC_STEMS and stem.endswith(key) and len(ids) == 1:   # a generic word (samjnayam) names many
                            tgt = ids[0]
                            if tgt != me:
                                edges.append((me, tgt, "apavada", "name:" + key))
                                resolved = True
                            break                                                     # longest unambiguous key wins
            if not resolved:                           # (c) kept only as a count
                unresolved[me] += 1
    with open(os.path.join(a.out_dir, "apavada_unresolved.tsv"), "w", encoding="utf-8") if os.makedirs(a.out_dir, exist_ok=True) is None else None as f:
        f.write("sutra\tmentions\n")
        for s, n in sorted(unresolved.items()):
            f.write(f"{s}\t{n}\n")
    edges = list(dict.fromkeys(edges))                    # exact duplicates removed, order kept
    os.makedirs(a.out_dir, exist_ok=True)
    with open(os.path.join(a.out_dir, "edges.tsv"), "w", encoding="utf-8") as f:
        f.write("src\tdst\tkind\tlabel\n")
        for e in edges:
            f.write("\t".join(e) + "\n")
    c = collections.Counter(e[2] for e in edges)
    print(len(by_id), "sutras;", dict(c))

if __name__ == "__main__":
    main()
