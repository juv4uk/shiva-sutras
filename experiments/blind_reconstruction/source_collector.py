import os
import yaml
import json
import datetime
import hashlib

from real_evidence import load_real_source

def compute_checksum(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def collect_sources():
    base_dir = os.path.dirname(__file__)
    blind_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml'))
    sources_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/sources'))
    external_corpus_file = os.path.abspath(os.path.join(base_dir, '../../external_data/kasika_corpus.json'))

    # FAIL CLOSED: the synthetic LLM-generated corpus must never overwrite REAL
    # GRETIL evidence. This legacy script is superseded by generate_real_sources.py.
    with open(blind_file, 'r', encoding='utf-8') as f:
        expert_sutras = yaml.safe_load(f)

    protected = 0
    missing = 0
    for item in expert_sutras:
        sid = item['sutra_id']
        record_id = f"KASIKA-{sid}"
        if load_real_source(sid) is not None:
            protected += 1
            continue
        if not os.path.exists(external_corpus_file):
            continue
        with open(external_corpus_file, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
        raw_text = corpus.get(record_id)
        if not raw_text:
            missing += 1
            continue
        print(f"REAL source missing for {record_id}; refusing to write synthetic substitute (fail closed).")
        missing += 1

    print(f"Source Collector (legacy): {protected} REAL sources protected from overwrite; "
          f"{missing} missing (no synthetic substitute written).")

if __name__ == '__main__':
    collect_sources()
