import os
import yaml
import random

def generate_batch_1():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/candidate-phonological-rules.yaml'))
    raw_sutras_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/raw-sutras.yaml'))
    out_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1'))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'batch_1_50_semantic_contexts.yaml')
    
    with open(in_file, 'r', encoding='utf-8') as f:
        sutras = yaml.safe_load(f)
        
    with open(raw_sutras_file, 'r', encoding='utf-8') as f:
        raw_sutras = yaml.safe_load(f)
        
    # Exclude pilot sutras
    pilot_ids = ['1.1.69', '1.3.12', '4.4.18', '4.4.57', '5.3.31', '5.3.92', '6.3.68', '6.3.105', '6.4.21', '6.4.77', '6.4.111', '7.1.39', '7.1.41', '7.2.37', '7.2.91', '7.3.89', '8.3.33', '8.3.59', '8.4.45', '8.4.46']
    
    candidates = [s for s in sutras if s['phonology_candidate']['status'] in ['yes', 'maybe'] and s['sutra_id'] not in pilot_ids]
    
    batch_1 = []
    selected_ids = set()
    
    def add_sutra(sutra):
        if sutra['sutra_id'] not in selected_ids:
            batch_1.append(sutra)
            selected_ids.add(sutra['sutra_id'])
            
    # Stratified selection (aiming for 50 total)
    categories = [
        ("syntactic_replacement_pattern", 5),
        ("lexical:लोप", 5),
        ("lexical:आगम", 5),
        ("lexical:सवर्ण", 5),
        ("derived_shape", 5),
        ("inherited-context-candidate", 5),
        ("prosody_morpheme", 5),
        ("domain_metalinguistic", 5) # Domain match
    ]
    
    for trigger, count in categories:
        if trigger == "domain_metalinguistic":
            matches = [s for s in candidates if s['candidate_domain'] == 'metalinguistic_sound_structure' and s['sutra_id'] not in selected_ids]
        else:
            matches = [s for s in candidates if any(trigger in t for t in s['phonology_candidate']['triggers']) and s['sutra_id'] not in selected_ids]
        random.shuffle(matches)
        for m in matches[:count]:
            add_sutra(m)
            
    # Fill remaining to 50
    remaining = 50 - len(batch_1)
    if remaining > 0:
        other_candidates = [s for s in candidates if s['sutra_id'] not in selected_ids]
        random.shuffle(other_candidates)
        for m in other_candidates[:remaining]:
            add_sutra(m)
            
    # Sort by ID
    def parse_id(sid):
        return tuple(map(int, sid.split('.')))
    batch_1.sort(key=lambda s: parse_id(s['sutra_id']))
    
    # Generate Semantic Schema v1.0 (FROZEN)
    v1_contexts = []
    
    def get_neighbors(sid, count=3):
        idx = -1
        for i, s in enumerate(raw_sutras):
            if s['sutra_id'] == sid:
                idx = i
                break
        if idx == -1: return []
        start = max(0, idx - count)
        end = min(len(raw_sutras), idx + count + 1)
        neighbors = []
        for i in range(start, end):
            if i != idx:
                neighbors.append(f"{raw_sutras[i]['sutra_id']}: {raw_sutras[i]['source_text']}")
        return neighbors

    for sutra in batch_1:
        sid = sutra['sutra_id']
        triggers = sutra['phonology_candidate']['triggers']
        
        # Heuristic operation type
        op_type = 'UNKNOWN'
        if any("आदेश" in t or "syntactic_replacement_pattern" in t for t in triggers):
            op_type = 'substitution'
        elif any("लोप" in t for t in triggers):
            op_type = 'elision/lopa'
        elif any("आगम" in t for t in triggers):
            op_type = 'augmentation/agama'
        elif sutra['candidate_domain'] == 'metalinguistic_sound_structure':
            op_type = 'metalinguistic_assignment'
            
        # Determine sound set relevance candidate
        relevance_status = 'UNRESOLVED'
        candidate_roles = []
        if op_type in ['substitution', 'augmentation/agama']:
            relevance_status = 'CANDIDATE'
            candidate_roles = ['source', 'left_context', 'right_context']
            
        v1 = {
            'rule_context': {
                'sutra_id': sid,
                'local_text': {
                    'source': sutra['source_text'],
                    'padaccheda': sutra['padaccheda'],
                    'neighbors': get_neighbors(sid, 3)
                },
                'sources': [{'type': 'sutrapatha', 'provenance': 'normalized-sutras.yaml'}],
                'dependencies': {
                    'anuvrtti': [{'source_sutra': None, 'source_status': 'UNKNOWN-BY-EVIDENCE', 'inherited_item': 'pending Kasika lookup'}],
                    'adhikara': []
                },
                'scope': {
                    'domain': sutra['candidate_domain'],
                    'applies_to': [],
                    'productivity': {'status': 'UNKNOWN-BY-EVIDENCE'}
                },
                'operation': {
                    'workflow_status': 'PROPOSED',
                    'type': op_type,
                    'operands': []
                },
                'functional_reading': {
                    'summary': 'PROPOSED: Pending manual validation',
                    'evidence_strength': 'UNRESOLVED'
                },
                'sound_set_relevance': {
                    'status': relevance_status,
                    'basis': ['heuristic_parser_proposal'],
                    'candidate_roles': candidate_roles,
                    'reason': 'Requires source-backed semantic review'
                },
                'claims': [],
                'unresolved_questions': ['pending_manual_validation']
            }
        }
        
        # Heuristic operands based on roles
        roles = sutra.get('phonology_candidate', {}).get('roles', {})
        for r_class, r_role in roles.items():
            op_role = 'unresolved_operand'
            if op_type == 'substitution':
                if 'target' in r_role: op_role = 'source'
                elif 'replacement' in r_role: op_role = 'replacement'
                elif 'right_context' in r_role: op_role = 'right_context'
            
            v1['rule_context']['operation']['operands'].append({
                'role': 'unresolved_operand',
                'proposed_role': op_role,
                'validated_role': None,
                'expression': r_class,
                'interpretation': {
                    'semantic_type': {
                        'value': 'technical_sound_class',
                        'evidence_strength': 'UNRESOLVED'
                    }
                },
                'membership': {
                    'knowledge_status': 'UNKNOWN-BY-BLINDING'
                }
            })
            
        v1_contexts.append(v1)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(v1_contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Batch 1 (50 sutras) generated at {out_file}")

if __name__ == '__main__':
    random.seed(101) # Seed for reproducibility
    generate_batch_1()
