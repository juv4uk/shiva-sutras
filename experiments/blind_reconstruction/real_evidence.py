"""Shared loader for REAL Kāśikā evidence.

The 4 legacy execution scripts (`execute_wave_2a_real.py`, `execute_track_ab.py`,
`execute_batch2_phase1.py`, `execute_waves_2bcd.py`) used to fabricate
`"Simulated Kasika raw text..."` source files. They must now read the REAL
GRETIL-derived artifacts in `ksetra/astadhyayi/sources/` and fail closed for
the 32 sūtras that are absent from the Sharma edition corpus.

Usage:
    from real_evidence import load_real_source, real_evidence_for
    rec = load_real_source('1.1.1')          # dict or None
    frag = real_evidence_for('1.1.1')        # evidence_fragment dict or None
"""

import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../ksetra/astadhyayi/sources'))


def source_path(sutra_id):
    return os.path.join(SOURCES_DIR, f'KASIKA-{sutra_id}.yaml')


def load_real_source(sutra_id):
    """Return the parsed REAL source record (dict) or None if absent."""
    path = source_path(sutra_id)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return None
    prov = data.get('provenance', {})
    if prov.get('status') != 'REAL':
        return None
    return data


def real_evidence_for(sutra_id):
    """Build an evidence_fragment from the REAL source, or None on any gap.

    The fragment carries the actual GRETIL commentary text (verbatim, not a
    paraphrase) so downstream claims are grounded in reproducible evidence
    rather than a `normalized_summary` placeholder.
    """
    rec = load_real_source(sutra_id)
    if rec is None:
        return None
    wt = rec.get('witness_text', {})
    sutra = wt.get('sutra', '')
    commentary = wt.get('commentary', '')
    if not (sutra or commentary):
        return None
    return {
        'source_id': f'KASIKA-{sutra_id}',
        'locator': 'vrtti-start',
        'source_file': source_path(sutra_id),
        'witness_sutra': sutra,
        'witness_commentary': commentary,
        'evidence_strength': 'VERIFIED-ATTRIBUTED',
        'supports': 'direct statement in Kāśikāvṛtti',
    }


def has_real_source(sutra_id):
    return load_real_source(sutra_id) is not None
