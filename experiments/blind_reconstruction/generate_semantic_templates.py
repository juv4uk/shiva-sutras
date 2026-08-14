import os
import yaml

def generate_semantic_templates():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_rules_selection.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        pilot_sutras = yaml.safe_load(f)
        
    semantic_contexts = []
    
    for sutra in pilot_sutras:
        context = {
            'rule_context': {
                'sutra_id': sutra['sutra_id'],
                'pilot_selection_reason': sutra['pilot_selection_reason'],
                'local_text': {
                    'source': sutra['source_text'],
                    'padaccheda': sutra['padaccheda']
                },
                'inherited_context': {
                    'from': [],
                    'confidence': 'UNRESOLVED'
                },
                'adhikara': {
                    'inherited_from': []
                },
                'semantic_operation': {
                    'status': 'unresolved',
                    'type': 'UNKNOWN',
                    'arguments': {
                        'target_class': {'symbol': 'UNKNOWN', 'content': 'UNKNOWN'},
                        'replacement_class': {'symbol': 'UNKNOWN', 'content': 'UNKNOWN'},
                        'left_context': {'symbol': 'UNKNOWN', 'content': 'UNKNOWN'},
                        'right_context': {'symbol': 'UNKNOWN', 'content': 'UNKNOWN'}
                    }
                }
            }
        }
        
        # Best effort pre-fill based on triggers
        roles = sutra.get('phonology_candidate', {}).get('roles', {})
        for r_class, r_role in roles.items():
            if 'target' in r_role:
                context['rule_context']['semantic_operation']['arguments']['target_class']['symbol'] = r_class
            if 'replacement' in r_role:
                context['rule_context']['semantic_operation']['arguments']['replacement_class']['symbol'] = r_class
            if 'right_context' in r_role:
                context['rule_context']['semantic_operation']['arguments']['right_context']['symbol'] = r_class
                
        # Fill operation type
        triggers = sutra.get('phonology_candidate', {}).get('triggers', [])
        if any("आदेश" in t or "syntactic_replacement_pattern" in t for t in triggers):
            context['rule_context']['semantic_operation']['type'] = 'substitution'
        elif any("लोप" in t for t in triggers):
            context['rule_context']['semantic_operation']['type'] = 'elision/lopa'
        elif any("आगम" in t for t in triggers):
            context['rule_context']['semantic_operation']['type'] = 'augmentation/agama'
            
        semantic_contexts.append(context)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(semantic_contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Semantic templates generated at {out_file}")

if __name__ == '__main__':
    generate_semantic_templates()
