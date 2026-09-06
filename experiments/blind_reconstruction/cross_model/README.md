# Cross-Model Stability Measurement

## What's here

| File | Description |
|:---|:---|
| `sarvam_annotations.json` | Sarvam model family results (v5.1 + v6.1 pipeline) |
| `kimi_annotations.json` | Kimi model family results — **to be provided by owner** |
| `compute_ari.py` | ARI computation script |

## Format

Both annotation files are JSON arrays of objects:

```json
[
  {
    "sutra_id": "1.1.1",
    "sound_classes": ["अच्", "हल्"],
    "status": "yes"
  },
  ...
]
```

- `sutra_id`: Pāṇinian sūtra reference (adhyāya.pāda.sūtra)
- `sound_classes`: sorted list of Devanagari pratyāhāra labels detected
- `status`: "yes" / "maybe" / "no"

## How to run

1. Place `kimi_annotations.json` in this directory (same format as sarvam)
2. Run: `python compute_ari.py`
3. Check `ari_report.json` and `ari_report.md` for results

## Threshold

Preregistration requires ARI ≥ 0.80 across model families to declare structure "stable".
