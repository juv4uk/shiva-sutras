import os
import yaml

def gather_local_context():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts.yaml'))
    raw_sutras_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/raw-sutras.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        contexts = yaml.safe_load(f)
        
    with open(raw_sutras_file, 'r', encoding='utf-8') as f:
        raw_sutras = yaml.safe_load(f)
        
    def get_neighbors(sid, count=3):
        # Very simple approximation: find index in raw_sutras and slice
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

    resolved_ids = ['1.1.69', '6.4.21', '6.4.77', '8.3.33', '4.4.57']
        
    for ctx in contexts:
        rc = ctx['rule_context']
        sid = rc['sutra_id']
        
        if sid not in resolved_ids:
            # 1. Gather local context
            rc['local_text']['neighbors'] = get_neighbors(sid, 3)
            
            # 2. Propose inherited context (dummy for now)
            rc['inherited_context']['from'] = ['PROPOSED: previous rule']
            
            # 3. Mark evidence map
            rc['evidence_map']['inherited_context'] = {
                'source': 'auto_context_gatherer',
                'evidence': 'Pending validation against Kasika'
            }
            
    with open(in_file, 'w', encoding='utf-8') as f:
        yaml.dump(contexts, f, allow_unicode=True, sort_keys=False)
        
    print("Local context gathered for the 15 sutras.")

if __name__ == '__main__':
    gather_local_context()
