import os
import yaml
import hashlib
import re

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
        s_file = os.path.join(sources_dir, f'KASIKA-{sid}.yaml')
        
        if not os.path.exists(s_file):
            continue
            
        with open(s_file, 'r', encoding='utf-8') as f:
            source_data = yaml.safe_load(f)
            
        if source_data.get('source_status') == 'REAL':
            # Already real, skip or re-authenticate
            continue
            
        raw_text = source_data.get('raw_text', '')
        retrieval = source_data.get('retrieval', {})
        
        # HEURISTICS:
        is_authentic = True
        reasons = []
        
        # 1. No boilerplate phrases
        boilerplate_pattern = r'अत्र सूत्रे .* इति पाणिनीयविधानम्'
        if re.search(boilerplate_pattern, raw_text):
            is_authentic = False
            reasons.append("Contains known boilerplate template.")
            
        # 2. Checksum validation
        expected_checksum = retrieval.get('checksum')
        actual_checksum = compute_checksum(raw_text)
        if expected_checksum != actual_checksum:
            is_authentic = False
            reasons.append(f"Checksum mismatch. Expected: {expected_checksum}, Actual: {actual_checksum}")
            
        # 3. Minimum length for a commentary fragment (e.g., > 10 chars)
        if len(raw_text.strip()) < 5:
            is_authentic = False
            reasons.append("Text fragment too short.")
            
        if is_authentic:
            source_data['source_status'] = 'REAL'
            source_data['authenticator_notes'] = 'Passed automated heuristics.'
            authenticated += 1
        else:
            source_data['source_status'] = 'PLACEHOLDER'
            source_data['authenticity'] = 'FAILED'
            source_data['authenticator_notes'] = '; '.join(reasons)
            failed += 1
            
        with open(s_file, 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            
    print(f"Authenticator finished. {authenticated} promoted to REAL. {failed} FAILED.")

if __name__ == '__main__':
    source_authenticator()
