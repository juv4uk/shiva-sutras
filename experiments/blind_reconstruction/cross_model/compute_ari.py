#!/usr/bin/env python3
"""
compute_ari.py — Cross-model stability measurement for L-001

Computes Adjusted Rand Index (ARI) between sarvam and kimi model family
annotations. ARI >= 0.80 is required by preregistration to declare any
structure "stable" and to enable outcome A or B.

Usage:
    python compute_ari.py

Input:
    cross_model/sarvam_annotations.json  (produced by sarvam pipeline)
    cross_model/kimi_annotations.json    (produced by owner via Kimi model)

Output:
    cross_model/ari_report.json
    cross_model/ari_report.md

Epistemic layer: ENGINEERING (stability measurement tool)
"""

import json
import os
import numpy as np
from collections import Counter
from itertools import combinations

def load_annotations(path):
    """Load JSON annotations: list of {sutra_id, sound_classes, status}."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_class_labels(annotations):
    """
    Convert annotations to per-sutra class-set labels.
    
    For ARI, we need two label arrays of the same length, where each element
    is a cluster ID. Sutras with the same set of sound_classes get the same
    cluster ID.
    """
    unique_sets = {}
    labels = []
    for a in annotations:
        key = frozenset(a['sound_classes'])
        if key not in unique_sets:
            unique_sets[key] = len(unique_sets)
        labels.append(unique_sets[key])
    return np.array(labels), unique_sets

def adjusted_rand_index(labels_a, labels_b):
    """
    Compute Adjusted Rand Index between two cluster labelings.
    
    ARI = 1.0 -> perfect agreement
    ARI = 0.0 -> random agreement
    ARI < 0.0 -> worse than random
    """
    n = len(labels_a)
    if n != len(labels_b):
        raise ValueError(f"Label arrays must have same length: {len(labels_a)} vs {len(labels_b)}")
    
    classes_a = np.unique(labels_a)
    classes_b = np.unique(labels_b)
    
    contingency = np.zeros((len(classes_a), len(classes_b)), dtype=np.int64)
    for i, ca in enumerate(classes_a):
        for j, cb in enumerate(classes_b):
            contingency[i, j] = np.sum((labels_a == ca) & (labels_b == cb))
    
    a_sums = contingency.sum(axis=1)
    b_sums = contingency.sum(axis=0)
    
    def comb2(x):
        return x * (x - 1) // 2
    
    index = sum(comb2(n_ij) for n_ij in contingency.flatten())
    expected_a = sum(comb2(a_i) for a_i in a_sums)
    expected_b = sum(comb2(b_j) for b_j in b_sums)
    max_index = (expected_a + expected_b) / 2
    
    if max_index == 0:
        return 1.0
    
    ari = (index - expected_a * expected_b / comb2(n)) / (max_index - expected_a * expected_b / comb2(n))
    return ari

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    sarvam_path = os.path.join(base_dir, 'sarvam_annotations.json')
    kimi_path = os.path.join(base_dir, 'kimi_annotations.json')
    
    if not os.path.exists(sarvam_path):
        print(f"ERROR: Sarvam annotations not found at {sarvam_path}")
        return
    if not os.path.exists(kimi_path):
        print(f"ERROR: Kimi annotations not found at {kimi_path}")
        print("The owner must run the Kimi model family independently and")
        print("produce kimi_annotations.json in the same format as sarvam_annotations.json")
        return
    
    sarvam_data = load_annotations(sarvam_path)
    kimi_data = load_annotations(kimi_path)
    
    sarvam_by_id = {a['sutra_id']: a for a in sarvam_data}
    kimi_by_id = {a['sutra_id']: a for a in kimi_data}
    
    common_ids = sorted(set(sarvam_by_id.keys()) & set(kimi_by_id.keys()))
    print(f"Sarvam: {len(sarvam_data)} sutras")
    print(f"Kimi: {len(kimi_data)} sutras")
    print(f"Common: {len(common_ids)} sutras")
    
    if len(common_ids) == 0:
        print("ERROR: No common sutra IDs between annotations")
        return
    
    sarvam_aligned = [sarvam_by_id[sid] for sid in common_ids]
    kimi_aligned = [kimi_by_id[sid] for sid in common_ids]
    
    sarvam_labels, sarvam_sets = build_class_labels(sarvam_aligned)
    kimi_labels, kimi_sets = build_class_labels(kimi_aligned)
    
    print(f"\nSarvam clusters: {len(sarvam_sets)}")
    print(f"Kimi clusters: {len(kimi_sets)}")
    
    ari = adjusted_rand_index(sarvam_labels, kimi_labels)
    
    print(f"\n{'='*50}")
    print(f"Adjusted Rand Index: {ari:.4f}")
    print(f"Threshold (preregistration): 0.80")
    if ari >= 0.80:
        print(f"PASS - structure is stable across model families")
    else:
        print(f"FAIL - structure is NOT stable across model families")
    print(f"{'='*50}")
    
    sarvam_classes = set()
    kimi_classes = set()
    for a in sarvam_aligned:
        sarvam_classes.update(a['sound_classes'])
    for a in kimi_aligned:
        kimi_classes.update(a['sound_classes'])
    
    shared = sarvam_classes & kimi_classes
    only_sarvam = sarvam_classes - kimi_classes
    only_kimi = kimi_classes - sarvam_classes
    
    print(f"\nClass overlap:")
    print(f"  Shared: {len(shared)}")
    print(f"  Only sarvam: {len(only_sarvam)} - {sorted(only_sarvam)}")
    print(f"  Only kimi: {len(only_kimi)} - {sorted(only_kimi)}")
    
    agreements = []
    for i, sid in enumerate(common_ids):
        s_set = set(sarvam_aligned[i]['sound_classes'])
        k_set = set(kimi_aligned[i]['sound_classes'])
        if len(s_set | k_set) == 0:
            agreements.append(1.0)
        else:
            agreements.append(len(s_set & k_set) / len(s_set | k_set))
    
    mean_jaccard = np.mean(agreements)
    print(f"\nPer-sutra Jaccard similarity: {mean_jaccard:.4f}")
    
    report = {
        'ari': round(ari, 4),
        'threshold': 0.80,
        'pass': ari >= 0.80,
        'common_sutras': len(common_ids),
        'sarvam_clusters': len(sarvam_sets),
        'kimi_clusters': len(kimi_sets),
        'shared_classes': len(shared),
        'only_sarvam': sorted(only_sarvam),
        'only_kimi': sorted(only_kimi),
        'mean_jaccard': round(mean_jaccard, 4),
    }
    
    out_json = os.path.join(base_dir, 'ari_report.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    out_md = os.path.join(base_dir, 'ari_report.md')
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(f"""# ARI Cross-Model Stability Report

**Date:** 2026-09-07
**Metric:** Adjusted Rand Index

## Result

| Metric | Value |
|:---|:---|
| ARI | {ari:.4f} |
| Threshold | 0.80 |
| Pass | {'YES' if ari >= 0.80 else 'NO'} |

## Details

- Common sutras: {len(common_ids)}
- Sarvam clusters: {len(sarvam_sets)}
- Kimi clusters: {len(kimi_sets)}
- Shared classes: {len(shared)}
- Mean per-sutra Jaccard: {mean_jaccard:.4f}

## Class overlap

- Only sarvam: {sorted(only_sarvam)}
- Only kimi: {sorted(only_kimi)}
""")
    
    print(f"\nReports: {out_json}, {out_md}")

if __name__ == '__main__':
    main()
