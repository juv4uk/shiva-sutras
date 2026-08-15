import os
import yaml

def validator_v2():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_automatic.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        sutras = yaml.safe_load(f)
        
    for c in sutras:
        rc = c['rule_context']
        status = rc['operation'].get('workflow_status', 'PROPOSED')
        if status != 'resolved':
            continue
            
        demote = False
        reason = []
        
        op_type = rc['operation'].get('type', 'UNKNOWN')
        if op_type == 'UNKNOWN':
            demote = True
            reason.append("operation.type is UNKNOWN")
            
        has_unresolved_role = False
        roles = []
        for op in rc['operation'].get('operands', []):
            role = op.get('validated_role') or op.get('role')
            roles.append(role)
            if role == 'unresolved_operand':
                has_unresolved_role = True
        
        if has_unresolved_role:
            demote = True
            reason.append("contains unresolved_operand")
            
        if 'pending_manual_validation' in rc.get('unresolved_questions', []):
            demote = True
            reason.append("pending_manual_validation in unresolved_questions")
            
        if op_type == 'substitution':
            if 'source' not in roles or 'replacement' not in roles:
                demote = True
                reason.append("substitution missing source or replacement")
        elif op_type == 'elision/lopa':
            if 'deleted_element' not in roles and 'source' not in roles:
                demote = True
                reason.append("elision missing deleted_element")
        elif op_type == 'suffixation':
            if 'base' not in roles or 'suffix' not in roles:
                demote = True
                reason.append("suffixation missing base or suffix")
                
        for claim in rc.get('claims', []):
            for ev in claim.get('evidence', []):
                s_id = ev.get('source_id')
                if s_id and 'KASIKA' in s_id:
                    if not ev.get('locator', ''):
                        demote = True
                        reason.append("claim missing locator")
                    # Check the actual source file
                    s_file = os.path.abspath(os.path.join(base_dir, f"../../ksetra/astadhyayi/sources/{s_id}.yaml"))
                    if not os.path.exists(s_file):
                        demote = True
                        reason.append(f"source file {s_id} not found")
                    else:
                        with open(s_file, 'r', encoding='utf-8') as sf:
                            s_data = yaml.safe_load(sf)
                            if s_data.get('source_status') != 'REAL':
                                demote = True
                                reason.append(f"source {s_id} is not REAL")
                            if "simulated" in str(s_data.get('raw_text', '')).lower():
                                demote = True
                                reason.append(f"source {s_id} contains simulated text")
                    
        if rc.get('sound_set_relevance', {}).get('status') == 'CANDIDATE':
            if not any(r in ['source', 'replacement', 'deleted_element', 'left_context', 'right_context'] for r in roles):
                demote = True
                reason.append("CANDIDATE relevance without valid context operands")
                
        if demote:
            rc['operation']['workflow_status'] = 'REVIEWED'
            if 'unresolved_questions' not in rc:
                rc['unresolved_questions'] = []
            rc['unresolved_questions'].append(f"Demoted by Validator v2: {', '.join(reason)}")
            
    with open(in_file, 'w', encoding='utf-8') as f:
        yaml.dump(sutras, f, allow_unicode=True, sort_keys=False)
        
    print(f"Validator v2 completed. Applied to {in_file}")

if __name__ == '__main__':
    validator_v2()
