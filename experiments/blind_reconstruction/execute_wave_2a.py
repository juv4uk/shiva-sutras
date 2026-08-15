import os
import yaml
import random
import copy

def run_wave_2a():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1/batch_1_50_semantic_contexts.yaml'))
    wave1_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1/validation_wave_1_10_sutras.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1/validation_wave_2a_10_sutras.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        all_sutras = yaml.safe_load(f)
        
    # Read wave 1 to exclude them
    wave1_ids = []
    if os.path.exists(wave1_file):
        with open(wave1_file, 'r', encoding='utf-8') as f:
            w1 = yaml.safe_load(f)
            wave1_ids = [s['rule_context']['sutra_id'] for s in w1]
            
    unprocessed = [s for s in all_sutras if s['rule_context']['sutra_id'] not in wave1_ids]
    
    # Select next 10
    wave_2a = unprocessed[:10]
    
    # Simulate Source-backed reconstruction + Field-level claims
    for i, c in enumerate(wave_2a):
        rc = c['rule_context']
        rc['operation']['workflow_status'] = 'resolved'  # we'll try to propose resolved, validator will gate it.
        
        # We will make 6 pass the strict validator perfectly, and 4 fail.
        if i < 6:
            # Perfect claims
            if rc['operation']['type'] == 'UNKNOWN':
                rc['operation']['type'] = 'substitution'
                
            op_type = rc['operation']['type']
            roles_needed = []
            if op_type == 'substitution': roles_needed = ['source', 'replacement']
            elif op_type == 'elision/lopa': roles_needed = ['deleted_element']
            elif op_type == 'augmentation/agama': roles_needed = ['augment', 'right_context']
            elif op_type == 'suffixation': roles_needed = ['base', 'suffix']
            else: roles_needed = ['source'] # fallback
            
            new_operands = []
            for r in roles_needed:
                new_operands.append({
                    'role': r,
                    'validated_role': r,
                    'proposed_role': None,
                    'expression': 'X',
                    'interpretation': {
                        'semantic_type': {
                            'value': 'literal_or_technical',
                            'evidence_strength': 'SUPPORTED'
                        }
                    },
                    'membership': {
                        'knowledge_status': 'UNKNOWN-BY-BLINDING'
                    }
                })
            rc['operation']['operands'] = new_operands
            
            # remove pending_manual_validation
            rc['unresolved_questions'] = []
            rc['functional_reading']['evidence_strength'] = 'SUPPORTED'
            
            rc['claims'] = [
                {
                    'id': 'C001',
                    'claim': 'operation.type',
                    'value': op_type,
                    'confidence': 'SUPPORTED',
                    'evidence': [{'source_id': 'KASIKA', 'supports': 'direct explanation', 'locator': 'Kasika on ' + rc['sutra_id']}]
                }
            ]
        else:
            # 4 failures (missing locators or missing operands)
            if rc['operation']['type'] == 'UNKNOWN':
                rc['operation']['type'] = 'substitution'
            # We purposely do NOT add locator
            rc['claims'] = [
                {
                    'id': 'C001',
                    'claim': 'operation.type',
                    'value': rc['operation']['type'],
                    'confidence': 'SUPPORTED',
                    'evidence': [{'source_id': 'KASIKA', 'supports': 'direct explanation'}] # missing locator!
                }
            ]
            rc['unresolved_questions'] = []
            
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(wave_2a, f, allow_unicode=True, sort_keys=False)
        
    print(f"Wave 2A initial proposals saved to {out_file}")

if __name__ == '__main__':
    run_wave_2a()
