import os
import yaml
import json
import hashlib
from urllib.parse import urlparse, unquote

def compute_checksum(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def source_authenticator():
    base_dir = os.path.dirname(__file__)
    blind_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml'))
    sources_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/sources'))
    
    with open(blind_file, 'r', encoding='utf-8') as f:
        expert_sutras = yaml.safe_load(f)
        
    authenticated = 0
    failed = 0
    
    for item in expert_sutras:
        sid = item['sutra_id']
        record_id = f'KASIKA-{sid}'
        s_file = os.path.join(sources_dir, f'{record_id}.yaml')
        
        if not os.path.exists(s_file):
            continue
            
        with open(s_file, 'r', encoding='utf-8') as f:
            source_data = yaml.safe_load(f)
            
        if source_data.get('source_status') == 'VERIFIED-REPRODUCIBLE':
            continue
            
        provenance = source_data.get('provenance', {})
        retrieval_path = provenance.get('retrieval_path', '')
        integrity = source_data.get('integrity', {})
        collector_sha256 = integrity.get('collector_sha256', '')
        raw_text = source_data.get('raw_text', '')
        
        # 1. Reject ellipses
        if '...' in raw_text:
            source_data['source_status'] = 'PLACEHOLDER'
            source_data['verification'] = {'retrieval_reproduced': False, 'error': 'Contains ellipsis'}
            failed += 1
            with open(s_file, 'w', encoding='utf-8') as f:
                yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            continue
            
        # 2. Independent Retrieval
        is_authentic = False
        reasons = []
        
        if retrieval_path.startswith('file:///'):
            # Parse local file URI
            local_path = unquote(urlparse(retrieval_path).path)
            # Handle Windows paths like /C:/...
            if os.name == 'nt' and local_path.startswith('/'):
                local_path = local_path[1:]
                
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as cf:
                    corpus = json.load(cf)
                    
                independent_text = corpus.get(provenance.get('record_id'))
                if independent_text is not None:
                    verifier_sha256 = compute_checksum(independent_text)
                    if verifier_sha256 == collector_sha256 and verifier_sha256 == compute_checksum(raw_text):
                        is_authentic = True
                    else:
                        reasons.append("Checksum mismatch between collector, verifier, and raw_text.")
                else:
                    reasons.append(f"Record {provenance.get('record_id')} not found in corpus.")
            else:
                reasons.append(f"Retrieval path {local_path} not found.")
        else:
            reasons.append("Unsupported retrieval scheme for simulated environment.")
            
        if is_authentic:
            source_data['source_status'] = 'VERIFIED-REPRODUCIBLE'
            source_data['verification'] = {
                'retrieval_reproduced': True,
                'reproduced_sha256': verifier_sha256,
                'notes': 'Independent retrieval matched bytes perfectly.'
            }
            authenticated += 1
        else:
            source_data['source_status'] = 'UNVERIFIED'
            source_data['verification'] = {
                'retrieval_reproduced': False,
                'error': '; '.join(reasons)
            }
            failed += 1
            
        with open(s_file, 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            
    print(f"Authenticator finished. {authenticated} promoted to VERIFIED-REPRODUCIBLE. {failed} FAILED.")

if __name__ == '__main__':
    source_authenticator()
