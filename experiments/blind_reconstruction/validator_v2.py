import os
import yaml

class SemanticValidator:
    def validate_record(self, rc):
        demote = False
        reason = []
        
        op_type = rc.get('operation', {}).get('type', 'UNKNOWN')
        if op_type in ['UNKNOWN', 'insufficient_evidence']:
            demote = True
            reason.append("RESOLVED requires reconstructed operation")
            
        has_unresolved_role = False
        roles = []
        for op in rc.get('operation', {}).get('operands', []):
            role = op.get('validated_role') or op.get('role')
            roles.append(role)
            if role == 'unresolved_operand':
                has_unresolved_role = True
            # Test for opaque class expansion
            if 'a, i, u' in str(op.get('value', '')):
                demote = True
                reason.append("Explicit phoneme lists are strictly forbidden")
        
        if has_unresolved_role:
            demote = True
            reason.append("contains unresolved_operand")
            
        if 'pending_manual_validation' in rc.get('unresolved_questions', []):
            demote = True
            reason.append("pending_manual_validation in unresolved_questions")
            
        # Check claims and evidence
        for claim in rc.get('claims', []):
            if claim.get('type') == 'authenticity' and claim.get('status') != 'VERIFIED':
                demote = True
                reason.append("Cannot resolve without VERIFIED authenticity")

            for ev in claim.get('evidence', []):
                if 'KASIKA' in ev.get('source_id', ''):
                    if not ev.get('locator', ''):
                        demote = True
                        reason.append("claim missing locator")
                if "..." in str(ev.get('raw_text', '')):
                    demote = True
                    reason.append("Ellipsis (...) found in evidence raw_text")
                    
        # Also check evidence_layer directly if formatted that way
        ev_layer = rc.get('evidence_layer', {})
        if ev_layer:
            if "..." in str(ev_layer.get('raw_text', '')):
                demote = True
                reason.append("Ellipsis (...) found in evidence raw_text")
        
        return not demote, reason

    def validate_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        # If it's a list of sutras
        is_list = isinstance(data, list)
        records = data if is_list else [data]
        
        all_valid = True
        all_reasons = []
        
        for record in records:
            # Map batch structure to record structure
            if 'rule_context' in record:
                rc = record['rule_context']
            else:
                rc = record # Expert reconstruction structure
                if 'expert_reconstruction' in record:
                    rc['operation'] = record['expert_reconstruction']
            
            is_valid, reason = self.validate_record(rc)
            if not is_valid:
                all_valid = False
                all_reasons.extend(reason)
                
        return all_valid, all_reasons

def validator_v2():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_automatic.yaml'))
    if not os.path.exists(in_file):
        print(f"Skipping: {in_file} not found")
        return
        
    validator = SemanticValidator()
    
    with open(in_file, 'r', encoding='utf-8') as f:
        sutras = yaml.safe_load(f)
        
    for c in sutras:
        rc = c.get('rule_context', {})
        status = rc.get('operation', {}).get('workflow_status', 'PROPOSED')
        if status != 'resolved':
            continue
            
        is_valid, reason = validator.validate_record(rc)
        
        if not is_valid:
            rc['operation']['workflow_status'] = 'REVIEWED'
            if 'unresolved_questions' not in rc:
                rc['unresolved_questions'] = []
            rc['unresolved_questions'].append(f"Demoted by Validator v2: {', '.join(reason)}")
            
    with open(in_file, 'w', encoding='utf-8') as f:
        yaml.dump(sutras, f, allow_unicode=True, sort_keys=False)
        
    print(f"Validator v2 completed. Applied to {in_file}")

if __name__ == '__main__':
    validator_v2()
