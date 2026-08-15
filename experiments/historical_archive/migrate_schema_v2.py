import os
import yaml

def migrate_to_v2():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts_v2.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        contexts = yaml.safe_load(f)
        
    v2_contexts = []
    
    for ctx in contexts:
        old = ctx.get('rule_context', {})
        sid = old.get('sutra_id', '')
        
        v2 = {
            'rule_context': {
                'sutra_id': sid,
                'local_text': old.get('local_text', {}),
                'sources': old.get('sources', []),
                'dependencies': {
                    'anuvrtti': [],
                    'adhikara': []
                },
                'scope': {
                    'domain': 'UNRESOLVED',
                    'applies_to': [],
                    'productivity': {'status': 'UNKNOWN-BY-EVIDENCE'}
                },
                'operation': {
                    'workflow_status': old.get('semantic_operation', {}).get('status', 'PROPOSED'),
                    'type': old.get('semantic_operation', {}).get('type', 'UNKNOWN'),
                    'operands': []
                },
                'functional_reading': {
                    'summary': old.get('functional_reading', {}).get('summary', ''),
                    'evidence_strength': old.get('functional_reading', {}).get('confidence', 'UNRESOLVED')
                },
                'sound_set_relevance': {
                    'status': 'UNRESOLVED',
                    'candidate_roles': [],
                    'reason': 'Pending review'
                },
                'claims': [],
                'unresolved_questions': old.get('functional_reading', {}).get('unresolved', [])
            }
        }
        
        # Migrate inherited context to anuvrtti graph
        old_inherited = old.get('inherited_context', {}).get('from', [])
        for item in old_inherited:
            v2['rule_context']['dependencies']['anuvrtti'].append({
                'source_sutra': 'UNKNOWN',
                'inherited_item': item,
                'status': 'PROPOSED'
            })
            
        # Migrate arguments to typed operands
        args = old.get('semantic_operation', {}).get('arguments', {})
        for role, data in args.items():
            sym = data.get('symbol', 'UNKNOWN')
            content = data.get('content', 'UNKNOWN')
            
            # Map content to epistemic status
            interpretation_status = 'UNRESOLVED'
            membership_status = 'UNKNOWN-BY-EVIDENCE'
            if 'literal' in content:
                interpretation_status = 'SUPPORTED'
                membership_status = 'NOT-APPLICABLE'
            elif 'UNKNOWN-BY-BLINDING' in content:
                interpretation_status = 'SUPPORTED'
                membership_status = 'UNKNOWN-BY-BLINDING'
                
            v2['rule_context']['operation']['operands'].append({
                'role': role,
                'expression': sym,
                'semantic_type': 'UNRESOLVED',
                'interpretation': {
                    'value': content,
                    'status': interpretation_status
                },
                'membership': {
                    'value': None,
                    'status': membership_status
                }
            })
            
        # Migrate evidence map to claims
        ev_map = old.get('evidence_map', {})
        claim_id = 1
        for claim_type, ev in ev_map.items():
            v2['rule_context']['claims'].append({
                'id': f"C{claim_id:03d}",
                'claim': claim_type,
                'value': 'PROPOSED',
                'confidence': 'UNRESOLVED',
                'evidence': [
                    {
                        'source_id': ev.get('source', 'UNKNOWN'),
                        'supports': ev.get('evidence', '')
                    }
                ]
            })
            claim_id += 1
            
        v2_contexts.append(v2)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(v2_contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Migrated 20 sutras to Semantic Schema v2 at {out_file}")

if __name__ == '__main__':
    migrate_to_v2()
