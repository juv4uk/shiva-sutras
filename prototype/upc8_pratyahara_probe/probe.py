#!/usr/bin/env python3
"""UPC8 → Pratyāhāra Probe (vyasa, 2026-08-23).

Prototype question: when Ukrainian phonemes are encoded in UPC-8
(slavic_phonetics feature space), which Pāṇinian pratyāhāras do they
fall into, and what is their nearest Sanskrit counterpart?

Method:
  1. Load the immutable Śiva-sūtra canon (ksetra/canon/siva-sutras.yaml).
  2. Build pratyāhāra expansion per Pāṇini 1.1.71.
  3. Define a minimal articulatory feature space shared by BOTH sides
     (place/manner/voiced/soft; retroflex added on the Sanskrit side --
     its absence in Slavic is itself informative: distance must be large).
  4. For each probed Ukrainian phoneme: exact weighted distance to every
     Sanskrit sound, nearest neighbour, and pratyāhāra memberships.

STATUS: engineering prototype -- feature assignments are hand-curated
M0 data, not a verified phonology. Distances are ORIENTATIONAL.
"""

import math
import yaml
from pathlib import Path

CANON = Path(__file__).resolve().parents[2] / "ksetra" / "canon" / "siva-sutras.yaml"

# ────────────────────────────── Śiva-sūtras ──────────────────────────

def load_sutras():
    doc = yaml.safe_load(CANON.read_text(encoding="utf-8"))
    return doc["sutras"]

def flat_sequence(sutras):
    """[(sound, it_marker_or_None)] in canonical order."""
    seq = []
    for s in sutras:
        for snd in s["sounds"]:
            seq.append((snd, s["it_marker_iast"]))
    return seq

def build_pratyaharas(seq, sutras):
    """Pratyāhāra XY per Pāṇini 1.1.71: sounds from the first occurrence
    of X up to the END of the sūtra whose it-marker is Y (the marker
    belongs to the sūtra's last sound -- this was the v1 bug)."""
    marker_end = {}
    idx = -1
    for s_ in sutras:
        idx += len(s_["sounds"])
        marker_end[s_["it_marker_iast"]] = idx

    n = len(seq)
    result = {}
    for xi in range(n):
        x = seq[xi][0]
        for marker, yend in marker_end.items():
            if yend < xi:
                continue
            key = f"{x}{marker}"
            if key not in result:
                result[key] = [snd for snd, _ in seq[xi : yend + 1]]
    return result

# ──────────────────────── shared feature space ────────────────────────
# dims: (place, manner, voiced, soft)
# place: 0 labial · 1 dental · 2 postalveolar · 3 palatal · 4 velar ·
#        5 glottal · 6 RETROFLEX (Sanskrit-only; absence in Ukrainian
#        is information, not an error)
# manner: 0 stop · 1 affricate · 2 fricative · 3 nasal · 4 liquid/
#         semivowel · 5 vowel

SA_FEATURES = {
    # vowels
    "a": (4, 5, 1, 0), "ā": (4, 5, 1, 0),
    "i": (3, 5, 1, 0), "ī": (3, 5, 1, 0),
    "u": (4, 5, 1, 0), "ū": (4, 5, 1, 0),
    "ṛ": (6, 5, 1, 0), "ḷ": (1, 5, 1, 0),
    "e": (3, 5, 1, 0), "ai": (3, 5, 1, 0),
    "o": (4, 5, 1, 0), "au": (4, 5, 1, 0),
    # gutturals
    "k": (4, 0, 0, 0), "kh": (4, 0, 0, 0),
    "g": (4, 0, 1, 0), "gh": (4, 0, 1, 0), "ṅ": (4, 3, 1, 0),
    # palatals
    "c": (3, 1, 0, 0), "ch": (3, 1, 0, 0),
    "j": (3, 1, 1, 0), "jh": (3, 1, 1, 0), "ñ": (3, 3, 1, 0),
    # retroflexes (Ukrainian has none -- distance must show it)
    "ṭ": (6, 0, 0, 0), "ṭh": (6, 0, 0, 0),
    "ḍ": (6, 0, 1, 0), "ḍh": (6, 0, 1, 0), "ṇ": (6, 3, 1, 0),
    # dentals
    "t": (1, 0, 0, 0), "th": (1, 0, 0, 0),
    "d": (1, 0, 1, 0), "dh": (1, 0, 1, 0), "n": (1, 3, 1, 0),
    # labials
    "p": (0, 0, 0, 0), "ph": (0, 0, 0, 0),
    "b": (0, 0, 1, 0), "bh": (0, 0, 1, 0), "m": (0, 3, 1, 0),
    # semivowels & fricatives & h
    "y": (3, 4, 1, 0), "r": (2, 4, 1, 0), "l": (1, 4, 1, 0), "v": (0, 4, 1, 0),
    "ś": (3, 2, 0, 0), "ṣ": (6, 2, 0, 0), "s": (1, 2, 0, 0), "h": (5, 2, 1, 0),
}

# Ukrainian probes: taken verbatim from prototype/slavic_phonetics
# PhonemeFeature fields (code kept for traceability).
UK_PROBES = {
    "б": (0, 0, 1, 0),   # 0x19 voiced labial stop
    "п": (0, 0, 0, 0),   # 0x26 voiceless labial stop
    "д": (1, 0, 1, 0),   # 0x1C voiced dental stop
    "т": (1, 0, 0, 0),   # 0x24 voiceless dental stop
    "ґ": (4, 0, 1, 0),   # voiced velar stop
    "г": (5, 2, 1, 0),   # 0x41 voiced glottal fricative
    "й": (3, 4, 1, 1),   # 0x0A palatal semivowel, soft
    "в": (0, 4, 1, 0),   # 0x40 labial semivowel/fricative
    "м": (0, 3, 1, 0),   # 0x0F labial nasal
    "н": (1, 3, 1, 0),   # dental nasal
    "і": (3, 5, 1, 1),   # 0x01 palatal vowel, soft
    "и": (3, 5, 1, 0),   # 0x31
    "ч": (3, 1, 0, 1),   # palatal affricate
    "ж": (2, 2, 1, 0),   # postalveolar fricative
}

W_PLACE, W_MANNER, W_VOICED, W_SOFT = 2.0, 2.0, 1.0, 0.5

def distance(f1, f2):
    return (W_PLACE * abs(f1[0] - f2[0])
            + W_MANNER * abs(f1[1] - f2[1])
            + W_VOICED * abs(f1[2] - f2[2])
            + W_SOFT * abs(f1[3] - f2[3]))

def main():
    seq = flat_sequence(load_sutras())
    pratyaharas = build_pratyaharas(seq, load_sutras())
    sounds_in_order = [snd for snd, _ in seq]

    print("=== canonical pratyāhāra coverage ===")
    ac = pratyaharas.get("ac", [])
    print(f"  ac   ({len(ac):2d}) = {' '.join(ac)}")
    nonac = [snd for snd, _ in seq if snd not in ac]
    print(f"  non-ac({len(nonac):2d}) = {' '.join(nonac)}")
    for key in ["yu", "yaL", "caR", "jaY"]:
        members = pratyaharas.get(key)
        if members:
            tail = " ..." if len(members) > 12 else ""
            print(f"  {key:4s} ({len(members):2d}) = {' '.join(members[:12])}{tail}")
    print()
    print("=== Ukrainian phoneme → nearest Sanskrit sound ===")
    header = f"{'укр':4s} {'nearest':10s} {'dist':>6s}  pratyāhāras containing nearest"
    print(header)
    rows = []
    for uk, feats in UK_PROBES.items():
        ranked = sorted(
            ((distance(feats, f), s) for s, f in SA_FEATURES.items()),
            key=lambda pair: pair[0],
        )
        best_d, best_sa = ranked[0]
        inside = [key for key, members in pratyaharas.items() if best_sa in members]
        shown = ", ".join(sorted(inside)[:6])
        rows.append((uk, best_sa, best_d, shown))
        print(f"{uk:4s} {best_sa:10s} {best_d:6.1f}  {shown}")

    print()
    print("=== sanity anchors (known answers must hold) ===")
    ok = True
    checks = [
        ("п", "p", "voiceless labial stop → p"),
        ("б", "b", "voiced labial stop → b"),
        ("т", "t", "dental stop → t"),
        ("н", "n", "dental nasal → n"),
    ]
    for uk, expected_sa, why in checks:
        got = rows[[r[0] for r in rows].index(uk)][1]
        status = "OK" if got == expected_sa else "FAIL"
        if got != expected_sa:
            ok = False
        print(f"  {uk} -> {got} (expected {expected_sa}) [{why}] {status}")
    print()
    print("VERDICT:", "anchors hold — probe is calibrated" if ok else "ANCHORS FAILED — recalibrate before interpreting anything")

if __name__ == "__main__":
    main()
