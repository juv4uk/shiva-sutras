#!/usr/bin/env python3
"""Step 1 of uk<->sa roadmap: formalize cognates as data + first metric.

Outputs:
1. extensions/cognates-uk-sa.yaml          — the data authority
2. extensions/cognates-uk-sa.embeddings.jsonl — BGE-M3 vectors per term
3. stdout report: within-pair vs cross-pair cosine similarity
   (first quantitative evidence of uk-sa semantic kinship)
"""
import json, os, sys
import numpy as np

VAULT = "/mnt/c/Users/user/Downloads/chatGPT-2023-2026/Obsidian"
REPO = "/home/agents/GitHub/shiva-sutras"

ENTRIES = [
    # sa_iast, devanagari, uk, pie, status
    ("bhrātṛ",        "भ्रातृ",     "брат",                    "*bʰréh₂tēr",            "confirmed"),
    ("dāma / dama",   "दाम",         "дім",                     "*dṓm",                  "confirmed"),
    ("daśa",          "दश",          "десять",                  "*déḱm̥t",                "confirmed"),
    ("dvā / dve",     "द्वा / द्वे",  "два",                     "*dwóh₁",                "confirmed"),
    ("hṛdayam",       "हृदयम्",      "серце",                   "*ḱērd",                 "confirmed"),
    ("mātā / mātṛ",   "माता / मातृ", "мати",                    "*méh₂tēr",              "confirmed"),
    ("nāma",          "नाम",         "ім'я",                    "*h₁nómn̥",              "confirmed"),
    ("nāsā / nāsikā", "नासा",        "ніс",                     "*néh₂s-",               "confirmed"),
    ("naktam",        "नक्तम्",      "ніч",                     "*nókʷts",               "confirmed"),
    ("nava",          "नव",          "новий",                   "*néwos",                "confirmed"),
    ("sapta",         "सप्त",        "сім",                     "*septḿ̥",               "confirmed"),
    ("tri",           "त्रि",         "три",                     "*tréyes",               "confirmed"),
    ("√vid (veda)",   "वेद",         "відати (знати, арх.)",    "*weyd-",                "confirmed"),
]

# The 15th source row is a phoneme observation (ś ↔ ш), not a lexeme pair:
# recorded in YAML as an observation, excluded from the embedding metric.
PHONEME_NOTE = {
    "sa": "ś (sūtra 5)", "uk": "ш", "pie": "*ḱ- (палаталізація)",
    "note": "фонема, не слово — підтверджено як звуковий закон"
}

# ---- 1. YAML data authority ----
yaml_lines = [
    "# Cognates: Ukrainian <-> Sanskrit (Step 1 of the uk-sa understanding roadmap)",
    "# Джерело: Sanskrit Terms Index (валт), зведено власником; статуси за таблицею.",
    "# Цей файл = data authority. Валт-нота лишається навігацією з лінком сюди.",
    "meta:",
    '  version: "0.1"',
    '  created: "2026-08-22"',
    '  source_note: "Sanskrit Terms Index.md"',
    '  status_vocabulary: [confirmed, pending, rejected]',
    "entries:",
]
for iast, deva, uk, pie, status in ENTRIES:
    yaml_lines += [
        f"  - sa_iast: \"{iast}\"",
        f"    devanagari: \"{deva}\"",
        f"    uk: \"{uk}\"",
        f"    pie: \"{pie}\"",
        f"    status: {status}",
    ]
yaml_lines += [
    "observations:",  # non-lexeme evidence kept, excluded from metrics
    f"  - sa: \"{PHONEME_NOTE['sa']}\"",
    f"    uk: \"{PHONEME_NOTE['uk']}\"",
    f"    pie: \"{PHONEME_NOTE['pie']}\"",
    f"    note: \"{PHONEME_NOTE['note']}\"",
]
os.makedirs(f"{REPO}/extensions", exist_ok=True)
open(f"{REPO}/extensions/cognates-uk-sa.yaml", "w", encoding="utf-8").write("\n".join(yaml_lines) + "\n")
print(f"yaml written: {len(ENTRIES)} entries + 1 phoneme observation")

# ---- 2. embeddings (GPU, tiny batch) ----
sys.path.insert(0, "/home/agents/GitHub/vault-semantic-mcp")
from embeddings import BGEEmbedder
emb = BGEEmbedder("/home/agents/GitHub/vault-semantic-mcp/config.json")

uk_texts = [f"українське слово: {uk}" for _,_,uk,_,_ in ENTRIES]
sa_texts = [f"sanskrit term: {iast} ({deva})" for iast,deva,_,_,_ in ENTRIES]

def enc(texts):
    r = emb.model.encode(texts, batch_size=8, max_length=256,
                         return_dense=True, return_sparse=False, return_colbert_vecs=False)
    v = np.asarray(r['dense_vecs'], dtype=np.float32)
    return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)

U, S = enc(uk_texts), enc(sa_texts)

with open(f"{REPO}/extensions/cognates-uk-sa.embeddings.jsonl", "w", encoding="utf-8") as out:
    for i, (iast, deva, uk, pie, status) in enumerate(ENTRIES):
        rec = {
            "pair": f"{iast} / {uk}", "status": status, "model": "BAAI/bge-m3",
            "embedding_uk": U[i].tolist(), "embedding_sa": S[i].tolist(),
        }
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("embeddings written")

# ---- 3. THE METRIC ----
def cos(a, b): return float(a @ b)
within = [cos(U[i], S[i]) for i in range(len(ENTRIES))]
cross = [cos(U[i], S[j]) for i in range(len(ENTRIES)) for j in range(len(ENTRIES)) if i != j]

print("\n=== FIRST QUANTITATIVE EVIDENCE: uk-sa kinship ===")
print(f"within-pair mean cosine : {np.mean(within):.4f}")
print(f"cross-pair  mean cosine : {np.mean(cross):.4f}")
print(f"delta                   : {np.mean(within)-np.mean(cross):+.4f}")
print("\nper-pair (rank among 13 cross-sims for same uk word):")
for i, (iast, deva, uk, pie, status) in enumerate(ENTRIES):
    sims = sorted((cos(U[i], S[j]) for j in range(len(ENTRIES)) if j != i), reverse=True)
    rank = sum(1 for x in sims if x > within[i]) + 1
    print(f"  {uk:12s} ↔ {iast:14s} {within[i]:.3f}  (rank {rank}/{len(ENTRIES)})")
