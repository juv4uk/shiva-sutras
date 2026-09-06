# L-001 Pipeline Output

## What's here

| File | Description |
|:---|:---|
| `sarvam_annotations.json` | Pipeline results (v5.1 structural + v6.1 declined-form / visarga-sandhi / compound / conjunct) |
| `compute_ari.py` | ARI computation script (supplementary — used for within-model convergence checks if needed) |

## Format

`sarvam_annotations.json` is a JSON object:

```json
{
  "model_family": "sarvam",
  "pipeline": "v5.1 + v6.1",
  "total_sutras": 3983,
  "sutras_with_classes": 213,
  "unique_classes": ["अच्", "हल्", ...],
  "status_counts": {"yes": 510, "maybe": 1215, "no": 2258},
  "annotations": [
    {"sutra_id": "1.1.3", "sound_classes": ["इक्"], "status": "yes"},
    ...
  ]
}
```

- `sutra_id`: Pāṇinian sūtra reference (adhyāya.pāda.sūtra)
- `sound_classes`: sorted list of Devanagari pratyāhāra labels detected
- `status`: "yes" / "maybe" / "no"

## Status

Cross-model requirement removed in preregistration rev 2 (2026-09-07).
See `journal/0012-preregistration-rev2-remove-cross-model.yaml`.
