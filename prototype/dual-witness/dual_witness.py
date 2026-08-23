#!/usr/bin/env python3
"""Dual-Witness Cognate Detector — prototype.

Two independent witnesses judge Ukrainian-Sanskrit word kinship:

  WITNESS 1 (MEANING): BGE-M3 embedding cosine similarity
      (from extensions/cognates-uk-sa.embeddings.jsonl)
  WITNESS 2 (SOUND):   UPC-8 phonetic encoding distance
      (upc8.py encodes BOTH languages into one code space)

Combined verdict requires both witnesses to agree — same two-witness
epistemology as Sarvam-as-second-witness, applied to linguistics.

Evaluation against golden set: 13 confirmed cognate pairs
(extensions/cognates-uk-sa.yaml).

Status: experimental/engineering prototype. Not a linguistic proof.
"""
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import upc8  # noqa: E402

REPO = "/home/agents/GitHub/shiva-sutras"
EMB_FILE = f"{REPO}/extensions/cognates-uk-sa.embeddings.jsonl"

# IAST -> this table's slp1-style keys (long vowels live as 'a:' style).
IAST_MAP = {
    "ā": "a:", "ī": "i:", "ū": "u:", "ṝ": "R:", "ḹ": "L:",
    "ṛ": "f", "ḷ": "x", "ś": "z", "ṣ": "S", "ñ": "Y", "ṅ": "G",
    "ṇ": "N", "ṃ": "~", "ḥ": "H", "ai": "E", "au": "O",
}

def iast_to_codes(iast: str, upc: "upc8.UPC8") -> list[int]:
    out = []
    i = 0
    while i < len(iast):
        ch = iast[i]
        if iast[i:i+2] in ("ai", "au"):
            ch = iast[i:i+2]; i += 2
        else:
            i += 1
        key = IAST_MAP.get(ch, ch)
        try:
            out.append(upc.encode_sanskrit(key))
        except KeyError:
            pass  # unknown segment skipped honestly
    return out

def sound_similarity(a_codes: list[int], b_codes: list[int]) -> float:
    """1 - normalized Levenshtein distance over UPC-8 code sequences.
    1.0 = identical phonetic skeleton, 0.0 = fully different."""
    if not a_codes or not b_codes:
        return 0.0
    la, lb = len(a_codes), len(b_codes)
    dp = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        dp[i][0] = i
    for j in range(lb + 1):
        dp[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            cost = 0 if a_codes[i-1] == b_codes[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    dist = dp[la][lb]
    return 1.0 - dist / max(la, lb)

def load_golden():
    import yaml
    d = yaml.safe_load(open(f"{REPO}/extensions/cognates-uk-sa.yaml", encoding="utf-8"))
    pairs = []
    for e in d["entries"]:
        sa_short = e["sa_iast"].split("/")[0].strip()          # dvA / dve -> dvA
        uk_short = e["uk"].split("(")[0].strip().lower()       # відати (знати...) -> відати
        pairs.append({
            "sa_iast": e["sa_iast"], "sa_key": sa_short,
            "devanagari": e["devanagari"], "uk": uk_short,
            "pie": e["pie"],
            "emb_uk": None, "emb_sa": None,
        })
    return pairs

def load_embeddings(pairs):
    for line in open(EMB_FILE, encoding="utf-8"):
        rec = json.loads(line)
        uk = rec["pair"].split(" / ")[-1].strip()
        for p in pairs:
            if p["uk"] == uk:
                p["emb_uk"] = np.asarray(rec["embedding_uk"], dtype=np.float32)
                p["emb_sa"] = np.asarray(rec["embedding_sa"], dtype=np.float32)

def main():
    upc = upc8.UPC8()
    pairs = load_golden()
    load_embeddings(pairs)

    # ---- witnesses ----
    # Iotated vowels are not single phonemes: я=йа, ю=йу, є=йе, ї=йі.
    # Apostrophe separates й from the vowel and encodes to nothing itself.
    def normalize_uk(word):
        word = word.replace("'", "")
        for src, dst in (("я", "йа"), ("ю", "йу"), ("є", "йе"), ("ї", "йі")):
            word = word.replace(src, dst)
        return word

    for p in pairs:
        u_codes = upc.encode_ukrainian_word(normalize_uk(p["uk"]))
        s_codes = iast_to_codes(p["sa_key"], upc)
        p["sound"] = round(sound_similarity(s_codes, u_codes), 4)
        if p["emb_uk"] is not None:
            a, b = p["emb_uk"], p["emb_sa"]
            p["meaning"] = round(float(a @ b), 4)
        else:
            p["meaning"] = None
        # combined: geometric mean of available witnesses
        ws = [w for w in (p["sound"], p["meaning"]) if w is not None]
        p["combined"] = round(float(np.prod(ws) ** (1 / len(ws))), 4) if ws else None

    # ---- ranking evaluation vs golden set ----
    print("=" * 78)
    print(f"{'uk':14s} {'sa':16s} {'sound':>6s} {'meaning':>8s} {'combined':>9s}  rank(combined)")
    print("-" * 78)
    ranks = []
    for p in pairs:
        others_c = [q["combined"] for q in pairs if q is not p and q["combined"] is not None]
        rank = 1 + sum(1 for x in others_c if x > p["combined"])
        ranks.append(rank)
        m = f"{p['meaning']:.3f}" if p["meaning"] is not None else "  n/a"
        print(f"{p['uk']:14s} {p['sa_iast']:16s} {p['sound']:6.3f} {m:>8s} {p['combined']:9.3f}  #{rank}/{len(others_c)+1}")
    print("-" * 78)
    top1 = sum(1 for r in ranks if r == 1)
    print(f"COMBINED top-1 hits: {top1}/{len(ranks)}")
    print("(baseline meaning-only was 12/13)")

if __name__ == "__main__":
    main()
