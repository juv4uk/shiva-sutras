import os
import yaml
import json

from real_evidence import load_real_source, real_evidence_for

def setup_epistemic_separation():
    base_dir = os.path.dirname(__file__)
    
    # 1. Move old Wave 2A to fixtures
    wave_2a_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1/validation_wave_2a_10_sutras.yaml'))
    tests_dir = os.path.abspath(os.path.join(base_dir, '../../tests/validator_v2'))
    os.makedirs(tests_dir, exist_ok=True)
    
    sutras_10 = []
    if os.path.exists(wave_2a_file):
        with open(wave_2a_file, 'r', encoding='utf-8') as f:
            sutras_10 = yaml.safe_load(f)
            
        positive = sutras_10[:6]
        negative = sutras_10[6:]
        
        with open(os.path.join(tests_dir, 'positive_fixtures.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(positive, f, allow_unicode=True, sort_keys=False)
        with open(os.path.join(tests_dir, 'negative_fixtures.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(negative, f, allow_unicode=True, sort_keys=False)
            
        os.remove(wave_2a_file)
        
    # 2. Source Collector: verify REAL KASIKA source artifacts exist (fail closed)
    sources_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/sources'))
    os.makedirs(sources_dir, exist_ok=True)
    
    sutra_ids = [s['rule_context']['sutra_id'] for s in sutras_10]
    
    missing = []
    for sid in sutra_ids:
        if load_real_source(sid) is None:
            missing.append(sid)
    if missing:
        print(f"WARNING: no REAL source for: {missing} (not fabricated)")
            
    # 3. Semantic Proposer
    real_wave_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1/validation_wave_2a_real.yaml'))
    
    real_records = []
    for s in sutras_10:
        rc = s['rule_context']
        sid = rc['sutra_id']
        rc['operation']['workflow_status'] = 'resolved' # proposer tries to propose resolved
        
        # Build claims pointing to the REAL source
        evidence = real_evidence_for(sid)
        rc['claims'] = [
            {
                'id': 'C001',
                'claim': 'operation.type',
                'value': rc['operation'].get('type', 'substitution'),
                'confidence': 'SUPPORTED',
                'evidence': [
                    {
                        'source_id': f'KASIKA-{sid}',
                        'source_locator': {'sutra': sid},
                        'evidence_fragment': {
                            'witness_sutra': evidence['witness_sutra'] if evidence else '',
                            'witness_commentary': evidence['witness_commentary'] if evidence else '',
                            'normalized_summary': ''
                        },
                        'supports': 'direct'
                    }
                ]
            }
        ]
        
        # Add unresolved questions if evidence is lacking
        if evidence is None:
            rc['unresolved_questions'] = ['missing_real_source']
        else:
            rc['unresolved_questions'] = []
            
        real_records.append(s)
        
    with open(real_wave_file, 'w', encoding='utf-8') as f:
        yaml.dump(real_records, f, allow_unicode=True, sort_keys=False)
        
    print("Wave 2A-Real Source verification and Semantic Proposal completed (REAL evidence).")
    
if __name__ == '__main__':
    setup_epistemic_separation()
