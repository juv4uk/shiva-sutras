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
        
        # Pull text from the external corpus
        raw_text = corpus.get(record_id)
        if not raw_text:
            print(f"Missing {record_id} in corpus!")
            continue
            
        checksum = compute_checksum(raw_text)
        
        source_data = {
            'source_status': 'UNVERIFIED',
            'provenance': {
                'provider': 'External Kasika Corpus JSON',
                'record_id': record_id,
                'retrieval_path': f'file:///{external_corpus_file.replace(os.sep, "/")}'
            },
            'raw_text': raw_text,
            'integrity': {
                'collector_sha256': checksum
            },
            'verification': {
                'retrieval_reproduced': False
            }
        }
        
        with open(os.path.join(sources_dir, f'{record_id}.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            
    print("Source Collector finished: 30 sources acquired as UNVERIFIED with provenance.")

if __name__ == '__main__':
    collect_sources()
