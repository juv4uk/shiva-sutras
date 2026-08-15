import os
import yaml
import random

def generate_expert_blind():
    base_dir = os.path.dirname(__file__)
    auto_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_automatic.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml'))
    
    with open(auto_file, 'r', encoding='utf-8') as f:
        sutras = yaml.safe_load(f)
        
    buckets = {
        'substitution': [],
        'anuvrtti-heavy': [],
        'shape-conditioned': [],
        'metalinguistic': [],
        'prosody': [],
        'mixed/uncertain': []
    }
    
    # We use simple string matching to stratify, similar to earlier
    for c in sutras:
        d = c['rule_context']['scope']['domain']
        o = c['rule_context']['operation']['type']
        d_lower = d.lower()
        o_lower = o.lower()
        
        if 'substitution' in o_lower:
            buckets['substitution'].append(c)
        elif 'lopa' in o_lower or 'elision' in o_lower:
            buckets['anuvrtti-heavy'].append(c)
        elif 'prosody' in d_lower:
            buckets['prosody'].append(c)
        elif 'metalinguistic' in d_lower or 'samjna' in d_lower:
            buckets['metalinguistic'].append(c)
        elif 'morphophonology' in d_lower or 'shape' in d_lower:
            buckets['shape-conditioned'].append(c)
        else:
            buckets['mixed/uncertain'].append(c)
            
    selected = []
    
    for b_name, b_list in buckets.items():
        random.shuffle(b_list)
        take = min(5, len(b_list))
        selected.extend(b_list[:take])
        
    # If we fall short of 30, backfill
    needed = 30 - len(selected)
    if needed > 0:
        remaining = [c for c in sutras if c not in selected]
        random.shuffle(remaining)
        selected.extend(remaining[:needed])
        
    # Build expert template
    expert_records = []
    for c in selected:
        rc = c['rule_context']
        sid = rc['sutra_id']
        
        template = {
            'sutra_id': sid,
            'source_locator': f'sources/KASIKA-{sid}.yaml',
            'expert_reconstruction': {
                'operation_type': 'FILL_ME',
                'operands': [],
                'dependencies': [],
                'sound_set_relevance': 'FILL_ME'
            },
            'claims': [],
            'uncertainty': {
                'type': 'NONE' # EVIDENCE | INTERPRETATION | NONE
            },
            'workflow_status': 'FILL_ME' # RESOLVED | REVIEWED
        }
        expert_records.append(template)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(expert_records, f, allow_unicode=True, sort_keys=False)
        
    print(f"Expert blind template generated with {len(expert_records)} sutras at {out_file}")

if __name__ == '__main__':
    random.seed(999)
    generate_expert_blind()
