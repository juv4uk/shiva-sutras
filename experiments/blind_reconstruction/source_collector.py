import os
import yaml
import json
import datetime
import hashlib

def compute_checksum(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def collect_sources():
    base_dir = os.path.dirname(__file__)
    blind_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml'))
    sources_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/sources'))
    external_corpus_file = os.path.abspath(os.path.join(base_dir, '../../external_data/kasika_corpus.json'))
    
    with open(blind_file, 'r', encoding='utf-8') as f:
        expert_sutras = yaml.safe_load(f)
        
    with open(external_corpus_file, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
        
    for item in expert_sutras:
        sid = item['sutra_id']
        record_id = f"KASIKA-{sid}"
        
        raw_text = corpus.get(record_id)
        if not raw_text:
            print(f"Missing {record_id} in corpus!")
            continue
            
        checksum = compute_checksum(raw_text)
        
        source_data = {
            'locator': {'sutra': sid},
            'raw_text': raw_text,
            'integrity': {
                'reproducible': False,
                'sha256_match': False,
                'collector_sha256': checksum,
                'retrieval_path': f'file:///{external_corpus_file.replace(os.sep, "/")}'
            },
            'provenance': {
                'authenticity': 'UNVERIFIED',
                'external_source': None,
                'notes': 'LLM generated local corpus. Reproducibility verified locally, but authenticity to original external Kasika source is unverified.'
            }
        }
        
        with open(os.path.join(sources_dir, f'{record_id}.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            
    print("Source Collector finished: 30 sources acquired with honest Epistemic Status.")

if __name__ == '__main__':
    collect_sources()
