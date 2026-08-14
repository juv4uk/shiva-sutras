import os
import yaml

def get_canonical_subsets(yaml_path):
    canonical_sequence = [
        "a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au", 
        "h1", "y", "v", "r", "l", 
        "ñ", "m", "ṅ", "ṇ", "n", 
        "jh", "bh", "gh", "ḍh", "dh", 
        "j", "b", "g", "ḍ", "d", 
        "kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", 
        "k", "p", 
        "ś", "ṣ", "s", "h2"
    ]
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    targets = []
    for p in data['pratyaharas']:
        base_set = set(p['set'])
        has_h = 'h' in base_set
        
        possible_sets = []
        if has_h:
            s1 = base_set.copy(); s1.remove('h'); s1.add('h1')
            s2 = base_set.copy(); s2.remove('h'); s2.add('h2')
            s3 = base_set.copy(); s3.remove('h'); s3.add('h1'); s3.add('h2')
            possible_sets = [s1, s2, s3]
        else:
            possible_sets = [base_set]
            
        resolved_set = None
        start_idx = -1
        end_idx = -1
        for i in range(len(canonical_sequence)):
            for pts in possible_sets:
                L = len(pts)
                if i + L <= len(canonical_sequence):
                    if set(canonical_sequence[i:i+L]) == pts:
                        resolved_set = list(canonical_sequence[i:i+L])
                        start_idx = i
                        end_idx = i + L - 1
                        break
            if resolved_set:
                break
                
        if resolved_set:
            targets.append({
                'id': p['id'], 
                'set': resolved_set,
                'start': start_idx,
                'end': end_idx
            })
            
    return canonical_sequence, targets

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    
    elements, targets = get_canonical_subsets(yaml_path)
    
    # 1. Analyze boundaries (ending positions)
    end_positions = {}
    for t in targets:
        end_idx = t['end']
        end_sound = elements[end_idx]
        if end_idx not in end_positions:
            end_positions[end_idx] = []
        end_positions[end_idx].append(t['id'])
        
    out_file = os.path.join(base_dir, 'marker_analysis.md')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Canonical Order Marker Analysis\n\n")
        f.write(f"- Total target classes: {len(targets)}\n")
        f.write(f"- Number of distinct required marker positions (endings): {len(end_positions)}\n\n")
        
        f.write("## Required Marker Positions\n")
        sorted_positions = sorted(end_positions.keys())
        for pos in sorted_positions:
            sound = elements[pos]
            classes_ending_here = end_positions[pos]
            f.write(f"- **After sound `{sound}`** (index {pos}): required by {len(classes_ending_here)} classes ({', '.join(classes_ending_here)})\n")

if __name__ == '__main__':
    main()
