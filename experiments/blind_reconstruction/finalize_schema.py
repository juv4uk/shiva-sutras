import os
import yaml

def finalize_schema():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts_v2_1.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts_final.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        contexts = yaml.safe_load(f)
        
    for ctx in contexts:
        rc = ctx['rule_context']
        status = rc['operation']['workflow_status']
        
        for op in rc['operation']['operands']:
            # 1. Cleanup outer semantic_type
            if 'semantic_type' in op and isinstance(op['semantic_type'], str):
                del op['semantic_type']
                
            # 2. Re-map unresolved roles
            if status != 'resolved':
                old_role = op.get('role', '')
                if old_role in ['target_class', 'replacement_class', 'left_context', 'right_context', 'source', 'replacement', 'base', 'suffix']:
                    op['role'] = 'unresolved_operand'
                    op['proposed_role'] = old_role
                    op['validated_role'] = None
            else:
                # For resolved, we just ensure no proposed_role exists, or set validated_role
                old_role = op.get('role', '')
                op['role'] = old_role
                op['proposed_role'] = None
                op['validated_role'] = old_role
                
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Finalized schema written to {out_file}")

if __name__ == '__main__':
    finalize_schema()
