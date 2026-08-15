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
            
        integrity = source_data.get('integrity', {})
        if integrity.get('reproducible') == True:
            continue
            
        retrieval_path = integrity.get('retrieval_path', '')
        collector_sha256 = integrity.get('collector_sha256', '')
        raw_text = source_data.get('raw_text', '')
        
        is_reproducible = False
        reasons = []
        
        if retrieval_path.startswith('file:///'):
            local_path = unquote(urlparse(retrieval_path).path)
            if os.name == 'nt' and local_path.startswith('/'):
                local_path = local_path[1:]
                
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as cf:
                    corpus = json.load(cf)
                    
                independent_text = corpus.get(record_id)
                if independent_text is not None:
                    verifier_sha256 = compute_checksum(independent_text)
                    if verifier_sha256 == collector_sha256 and verifier_sha256 == compute_checksum(raw_text):
                        is_reproducible = True
                    else:
                        reasons.append("Checksum mismatch between collector, verifier, and raw_text.")
                else:
                    reasons.append(f"Record {record_id} not found in corpus.")
            else:
                reasons.append(f"Retrieval path {local_path} not found.")
        else:
            reasons.append("Unsupported retrieval scheme.")
            
        if is_reproducible:
            integrity['reproducible'] = True
            integrity['sha256_match'] = True
            authenticated += 1
        else:
            integrity['reproducible'] = False
            integrity['sha256_match'] = False
            integrity['error'] = '; '.join(reasons)
            failed += 1
            
        source_data['integrity'] = integrity
        
        # Explicitly declare authenticity as UNVERIFIED to recognize our research bounds
        provenance = source_data.get('provenance', {})
        provenance['authenticity'] = 'UNVERIFIED'
        provenance['external_source'] = None
        source_data['provenance'] = provenance
            
        with open(s_file, 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            
    print(f"Authenticator finished. {authenticated} proven REPRODUCIBLE (Authenticity Unverified). {failed} FAILED.")

if __name__ == '__main__':
    source_authenticator()
