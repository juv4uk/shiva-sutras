import os
import yaml
import random

def generate_batch_2():
    base_dir = os.path.dirname(__file__)
    candidate_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/candidate-phonological-rules.yaml'))
    batch1_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1/batch_1_50_semantic_contexts.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_200_sutras.yaml'))
    
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    with open(candidate_file, 'r', encoding='utf-8') as f:
        candidates = yaml.safe_load(f)
        
    b1_ids = set()
    if os.path.exists(batch1_file):
        with open(batch1_file, 'r', encoding='utf-8') as f:
            b1 = yaml.safe_load(f)
            b1_ids.update([s['rule_context']['sutra_id'] for s in b1])
            
    # Filter candidates (YES or MAYBE only, not in Batch 1)
    pool = [c for c in candidates if c.get('sutra_id') not in b1_ids]
    
    # Stratification logic
    buckets = {
        'substitution': [],
        'anuvrtti-heavy': [],
        'shape-conditioned': [],
        'metalinguistic': [],
        'prosody': [],
        'mixed/uncertain': []
    }
    
    for c in pool:
        d = c.get('domain', '')
        o = c.get('operation', '')
        # Simple heuristics for bucketing based on domain/operation strings
        if 'substitution' in o.lower():
            buckets['substitution'].append(c)
        elif 'lopa' in o.lower() or 'elision' in o.lower():
            buckets['anuvrtti-heavy'].append(c)
        elif 'prosody' in d.lower():
            buckets['prosody'].append(c)
        elif 'metalinguistic' in d.lower() or 'samjna' in d.lower():
            buckets['metalinguistic'].append(c)
        elif 'morphophonology' in d.lower() or 'shape' in d.lower():
            buckets['shape-conditioned'].append(c)
        else:
            buckets['mixed/uncertain'].append(c)
            
    # Quotas
    quotas = {
        'substitution': 50,
        'anuvrtti-heavy': 50,
        'shape-conditioned': 40,
        'metalinguistic': 20,
        'prosody': 20,
        'mixed/uncertain': 20
    }
    
    selected = []
    
    for b_name, q in quotas.items():
        b_list = buckets[b_name]
        random.shuffle(b_list)
        # Take up to q, if not enough, take all
        take = min(q, len(b_list))
        selected.extend(b_list[:take])
        print(f"Bucket {b_name}: Needed {q}, Found {len(b_list)}, Selected {take}")
        
    # If we fall short of 200, fill from remaining 'mixed/uncertain' or others
    needed = 200 - len(selected)
    if needed > 0:
        remaining = [c for c in pool if c not in selected]
        random.shuffle(remaining)
        selected.extend(remaining[:needed])
        print(f"Filled remaining {needed} from general pool.")
        
    # Format to semantic contexts Schema v1.0
    records = []
    for c in selected:
        record = {
            'rule_context': {
                'sutra_id': c['sutra_id'],
                'local_text': {
                    'source': c.get('source_text', 'UNKNOWN'),
                    'padaccheda': c.get('padaccheda', 'UNKNOWN')
                },
                'scope': {
                    'domain': c.get('domain', 'UNKNOWN')
                },
                'dependencies': {
                    'anuvrtti': []
                },
                'operation': {
                    'workflow_status': 'proposed',
                    'type': 'UNKNOWN',
                    'operands': []
                },
                'functional_reading': {
                    'summary': '',
                    'evidence_strength': 'UNRESOLVED'
                },
                'sound_set_relevance': {
                    'status': 'UNRESOLVED',
                    'basis': []
                },
                'unresolved_questions': ['pending_manual_validation'],
                'claims': []
            }
        }
        records.append(record)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(records, f, allow_unicode=True, sort_keys=False)
        
    print(f"Batch 2 generated with {len(records)} sutras at {out_file}")

if __name__ == '__main__':
    random.seed(123)
    generate_batch_2()
