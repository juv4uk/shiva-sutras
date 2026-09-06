#!/usr/bin/env python3
"""
compute_ari.py - Cross-model stability measurement for L-001

Computes Adjusted Rand Index (ARI) between sarvam and kimi model family
annotations. ARI >= 0.80 is required by preregistration to declare any
structure "stable" and to enable outcome A or B.

Usage:
    python compute_ari.py

Input:
    cross_model/sarvam_annotations.json  (sarvam pipeline results)
    cross_model/kimi_annotations.json    (owner provides via Kimi model)

Both files have format:
    {
      "model_family": "sarvam|kimi",
      "pipeline": "...",
      "total_sutras": 3983,
      "sutras_with_classes": 213,
      "unique_classes": [...],
      "status_counts": {"yes": N, "maybe": N, "no": N},
      "annotations": [
        {"sutra_id": "1.1.1", "sound_classes": ["..."], "status": "yes"},
        ...
      ]
    }

Output:
    cross_model/ari_report.json
    cross_model/ari_report.md
"""

import json
import os
import numpy as np

def load_annotations(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'annotations' in data:
        return data['annotations'], data
    elif isinstance(data, list):
        return data, {'model_family': 'unknown'}
    else:
        raise ValueError(f"Unexpected format in {path}")

def build_class_labels(annotations):
    unique_sets = {}
    labels = []
    for a in annotations:
        key = frozenset(a['sound_classes'])
        if key not in unique_sets:
            unique_sets[key] = len(unique_sets)
        labels.append(unique_sets[key])
    return np.array(labels), unique_sets

def adjusted_rand_index(labels_a, labels_b):
    n = len(labels_a)
    if n != len(labels_b):
        raise ValueError(f"Length mismatch: {len(labels_a)} vs {len(labels_b)}")
    
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
        print(f"ERROR: {sarvam_path} not found")
        return
    if not os.path.exists(kimi_path):
        print(f"ERROR: {kimi_path} not found")
        print("Owner must provide kimi_annotations.json (same format as sarvam)")
        return
    
    sarvam_data, sarvam_meta = load_annotations(sarvam_path)
    kimi_data, kimi_meta = load_annotations(kimi_path)
    
    sarvam_by_id = {a['sutra_id']: a for a in sarvam_data}
    kimi_by_id = {a['sutra_id']: a for a in kimi_data}
    
    # Load full sutra list from v5.1 to get all 3983 IDs
    all_ids = sorted(set(sarvam_by_id.keys()) | set(kimi_by_id.keys()))
    v51_path = os.path.join(base_dir, '../../ksetra/astadhyayi/blind/candidate-phonological-rules.yaml')
    if os.path.exists(v51_path):
        import yaml
        with open(v51_path, 'r') as f:
            sutras = yaml.safe_load(f)
        all_ids = sorted(set(s['sutra_id'] for s in sutras))
    
    print(f"Sarvam: {len(sarvam_data)} annotated, {sarvam_meta.get('total_sutras', '?')} total")
    print(f"Kimi: {len(kimi_data)} annotated, {kimi_meta.get('total_sutras', '?')} total")
    print(f"Total sutras for ARI: {len(all_ids)}")
    
    # Sutras without annotations get empty set
    sarvam_aligned = [sarvam_by_id.get(sid, {'sutra_id': sid, 'sound_classes': [], 'status': 'no'}) for sid in all_ids]
    kimi_aligned = [kimi_by_id.get(sid, {'sutra_id': sid, 'sound_classes': [], 'status': 'no'}) for sid in all_ids]
    
    sarvam_labels, sarvam_sets = build_class_labels(sarvam_aligned)
    kimi_labels, kimi_sets = build_class_labels(kimi_aligned)
    
    print(f"\nSarvam clusters: {len(sarvam_sets)}")
    print(f"Kimi clusters: {len(kimi_sets)}")
    
    ari = adjusted_rand_index(sarvam_labels, kimi_labels)
    
    print(f"\n{'='*50}")
    print(f"Adjusted Rand Index: {ari:.4f}")
    print(f"Threshold: 0.80")
    print(f"{'PASS' if ari >= 0.80 else 'FAIL'}")
    print(f"{'='*50}")
    
    sarvam_classes = set(c for a in sarvam_aligned for c in a['sound_classes'])
    kimi_classes = set(c for a in kimi_aligned for c in a['sound_classes'])
    shared = sarvam_classes & kimi_classes
    only_sarvam = sarvam_classes - kimi_classes
    only_kimi = kimi_classes - sarvam_classes
    
    print(f"\nShared classes: {len(shared)}")
    print(f"Only sarvam: {len(only_sarvam)} - {sorted(only_sarvam)}")
    print(f"Only kimi: {len(only_kimi)} - {sorted(only_kimi)}")
    
    agreements = []
    for i in range(len(all_ids)):
        s_set = set(sarvam_aligned[i]['sound_classes'])
        k_set = set(kimi_aligned[i]['sound_classes'])
        if len(s_set | k_set) == 0:
            agreements.append(1.0)
        else:
            agreements.append(len(s_set & k_set) / len(s_set | k_set))
    mean_jaccard = float(np.mean(agreements))
    print(f"\nMean per-sutra Jaccard: {mean_jaccard:.4f}")
    
    report = {
        'ari': round(float(ari), 4),
        'threshold': 0.80,
        'pass': bool(ari >= 0.80),
        'total_sutras': len(all_ids),
        'sarvam_clusters': len(sarvam_sets),
        'kimi_clusters': len(kimi_sets),
        'shared_classes': len(shared),
        'only_sarvam': sorted(only_sarvam),
        'only_kimi': sorted(only_kimi),
        'mean_jaccard': round(mean_jaccard, 4),
    }
    
    with open(os.path.join(base_dir, 'ari_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(base_dir, 'ari_report.md'), 'w', encoding='utf-8') as f:
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

- Total sutras: {len(all_ids)}
- Sarvam clusters: {len(sarvam_sets)}
- Kimi clusters: {len(kimi_sets)}
- Shared classes: {len(shared)}
- Mean per-sutra Jaccard: {mean_jaccard:.4f}

## Class overlap

- Only sarvam: {sorted(only_sarvam)}
- Only kimi: {sorted(only_kimi)}
""")
    
    print(f"\nReports written.")

if __name__ == '__main__':
    main()
