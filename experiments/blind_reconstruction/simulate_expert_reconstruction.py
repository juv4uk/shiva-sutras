import os
import yaml

def simulate_expert():
    base_dir = os.path.dirname(__file__)
    blind_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml'))
    
    with open(blind_file, 'r', encoding='utf-8') as f:
        expert_sutras = yaml.safe_load(f)
        
    resolved_sutras = ['3.4.105', '6.4.81', '1.1.10', '6.1.122', '8.4.31']
    
    for item in expert_sutras:
        sid = item['sutra_id']
        
        # User defined behavior:
        if sid in resolved_sutras:
            item['workflow_status'] = 'RESOLVED'
            item['expert_reconstruction']['operation_type'] = 'reconstructed'
            item['expert_reconstruction']['sound_set_relevance'] = 'KNOWN'
            item['uncertainty']['type'] = 'NONE'
        else:
            item['workflow_status'] = 'REVIEWED'
            item['expert_reconstruction']['operation_type'] = 'insufficient_evidence'
            item['expert_reconstruction']['sound_set_relevance'] = 'UNKNOWN'
            item['uncertainty']['type'] = 'EVIDENCE'
            item['uncertainty']['reason'] = 'Local evidence text does not unambiguously specify operation or opaque classes.'
            
        # Keep source authenticity as UNVERIFIED per user mandate
        item['claims'] = [{
            'type': 'authenticity',
            'status': 'AUTHENTICITY_UNVERIFIED'
        }]
        
    with open(blind_file, 'w', encoding='utf-8') as f:
        yaml.dump(expert_sutras, f, allow_unicode=True, sort_keys=False)
        
    print(f"Simulated expert reconstruction completed for 30 sutras.")

if __name__ == '__main__':
    simulate_expert()
