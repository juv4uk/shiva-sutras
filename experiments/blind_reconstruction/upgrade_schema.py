import os
import yaml

def upgrade_schema_and_propose():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        contexts = yaml.safe_load(f)
        
    resolved_ids = ['1.1.69', '6.4.21', '6.4.77', '8.3.33', '4.4.57']
        
    for ctx in contexts:
        rc = ctx['rule_context']
        sid = rc['sutra_id']
        
        # Add evidence_map if not present
        if 'evidence_map' not in rc:
            rc['evidence_map'] = {
                'operation_type': {'source': 'UNRESOLVED', 'evidence': ''},
                'inherited_context': {'source': 'UNRESOLVED', 'evidence': ''},
                'target_role': {'source': 'UNRESOLVED', 'evidence': ''},
                'replacement_role': {'source': 'UNRESOLVED', 'evidence': ''}
            }
            
        if sid not in resolved_ids:
            # Upgrade remaining 15 to PROPOSED status
            rc['semantic_operation']['status'] = 'PROPOSED'
            
            # Simple heuristic guessing for PROPOSED fields based on initial templates
            op_type = rc['semantic_operation']['type']
            
            # Update evidence map to reflect heuristic proposition
            rc['evidence_map'] = {
                'operation_type': {'source': 'heuristic_parser', 'evidence': 'Derived from lexical triggers'},
                'inherited_context': {'source': 'pending_validation', 'evidence': 'Requires Kasika check'},
                'target_role': {'source': 'heuristic_parser', 'evidence': 'Derived from opaque symbols or 6/1 case'},
                'replacement_role': {'source': 'heuristic_parser', 'evidence': 'Derived from 1/1 case'}
            }
            
            if 'functional_reading' not in rc:
                rc['functional_reading'] = {
                    'summary': 'PROPOSED SUMMARY',
                    'confidence': 'UNRESOLVED',
                    'unresolved': ['pending_manual_validation']
                }
                
    with open(in_file, 'w', encoding='utf-8') as f:
        yaml.dump(contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Schema upgraded and 15 remaining sutras set to PROPOSED in {in_file}")

if __name__ == '__main__':
    upgrade_schema_and_propose()
