import os
import yaml

def migrate_to_v2_1():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts_v2.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts_v2_1.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        contexts = yaml.safe_load(f)
        
    for ctx in contexts:
        rc = ctx['rule_context']
        sid = rc['sutra_id']
        op_type = rc['operation']['type']
        
        # 1. Normalize dependencies
        for anu in rc['dependencies']['anuvrtti']:
            if anu.get('source_sutra') == 'UNKNOWN':
                anu['source_sutra'] = None
                anu['source_status'] = 'UNKNOWN-BY-EVIDENCE'
            if 'PROPOSED' in anu.get('inherited_item', ''):
                anu['inherited_item'] = 'previous rule (placeholder)'
                
        # 2. Add basis to sound_set_relevance
        if 'basis' not in rc['sound_set_relevance']:
            rc['sound_set_relevance']['basis'] = []
            
        # 3. Restructure operands and roles
        new_operands = []
        for op in rc['operation']['operands']:
            old_role = op['role']
            new_role = old_role
            
            if op_type == 'suffixation':
                if old_role == 'target_class': new_role = 'base'
                elif old_role == 'replacement_class': new_role = 'suffix'
            elif op_type == 'metalinguistic_assignment':
                if old_role == 'target_class': new_role = 'metalinguistic_subject'
                elif old_role == 'assignment': new_role = 'metalinguistic_assignment'
                elif old_role == 'condition': new_role = 'semantic_condition'
            elif op_type in ['substitution', 'elision/lopa', 'augmentation/agama']:
                if old_role == 'target_class': new_role = 'source'
                elif old_role == 'replacement_class': new_role = 'replacement'
                
            op['role'] = new_role
            
            # Split interpretation and membership properly
            old_val = op['interpretation']['value']
            old_status = op['interpretation']['status']
            old_mem_status = op['membership']['status']
            
            semantic_type_val = 'UNKNOWN'
            mem_status = 'NOT-APPLICABLE'
            
            if 'UNKNOWN-BY-BLINDING' in old_val:
                semantic_type_val = 'technical_sound_class'
                mem_status = 'UNKNOWN-BY-BLINDING'
            elif 'UNKNOWN-BY-EVIDENCE' in old_val:
                semantic_type_val = 'UNKNOWN-BY-EVIDENCE'
                mem_status = 'UNKNOWN-BY-EVIDENCE'
            elif 'literal' in old_val:
                semantic_type_val = old_val.replace('literal (', '').replace(')', '').strip()
                if not semantic_type_val:
                    semantic_type_val = 'literal_value'
                    
            op['interpretation'] = {
                'semantic_type': {
                    'value': semantic_type_val,
                    'evidence_strength': 'SUPPORTED' if old_status == 'SUPPORTED' else 'UNRESOLVED'
                }
            }
            op['membership'] = {
                'value': None,
                'knowledge_status': mem_status
            }
            new_operands.append(op)
            
        rc['operation']['operands'] = new_operands
        
        # 4. Synchronize claims for resolved records
        if rc['operation']['workflow_status'] == 'resolved':
            rc['claims'] = [
                {
                    'id': 'C001',
                    'claim': 'operation.type',
                    'value': op_type,
                    'confidence': 'SUPPORTED',
                    'evidence': [{'source_id': 'kasika', 'supports': 'direct'}]
                }
            ]
            c_idx = 2
            for op in new_operands:
                rc['claims'].append({
                    'id': f'C{c_idx:03d}',
                    'claim': f"operands[{op['role']}]",
                    'value': op['expression'],
                    'confidence': 'SUPPORTED',
                    'evidence': [{'source_id': 'kasika', 'supports': 'direct'}]
                })
                c_idx += 1
                
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Migrated 20 sutras to Semantic Schema v2.1 at {out_file}")

if __name__ == '__main__':
    migrate_to_v2_1()
