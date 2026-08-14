import os
import yaml
from ortools.sat.python import cp_model

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
            possible_sets = [
                base_set.difference({'h'}).union({'h1'}),
                base_set.difference({'h'}).union({'h2'}),
                base_set.difference({'h'}).union({'h1', 'h2'})
            ]
        else:
            possible_sets = [base_set]
            
        resolved_set = None
        for i in range(len(canonical_sequence)):
            for pts in possible_sets:
                L = len(pts)
                if i + L <= len(canonical_sequence):
                    if set(canonical_sequence[i:i+L]) == pts:
                        resolved_set = list(canonical_sequence[i:i+L])
                        break
            if resolved_set: break
        if resolved_set:
            targets.append({'id': p['id'], 'set': resolved_set})
    return canonical_sequence, targets

def is_m13_feasible(elements, targets_to_use):
    N = len(elements)
    elem_to_id = {e: i for i, e in enumerate(elements)}
    
    model = cp_model.CpModel()
    pos = [model.NewIntVar(0, N - 1, f'pos_{i}') for i in range(N)]
    model.AddAllDifferent(pos)
    
    end_pos_vars = []
    for t in targets_to_use:
        T_ids = [elem_to_id[e] for e in t['set']]
        L = len(T_ids)
        if L <= 1 or L == N: continue
        
        start_pos = model.NewIntVar(0, N - L, f"start_{t['id']}")
        end_pos = model.NewIntVar(L - 1, N - 1, f"end_{t['id']}")
        model.Add(end_pos == start_pos + L - 1)
        for i in T_ids:
            model.Add(pos[i] >= start_pos)
            model.Add(pos[i] <= end_pos)
        end_pos_vars.append(end_pos)
            
    if 'a' in elem_to_id and 'h2' in elem_to_id:
        model.Add(pos[elem_to_id['a']] < pos[elem_to_id['h2']])
        
    is_end = [model.NewBoolVar(f"is_end_{i}") for i in range(N)]
    for i in range(N):
        b_vars = []
        for e_var in end_pos_vars:
            b = model.NewBoolVar(f"b_end_{e_var.Name()}_at_{i}")
            model.Add(e_var == i).OnlyEnforceIf(b)
            model.Add(e_var != i).OnlyEnforceIf(b.Not())
            b_vars.append(b)
        model.AddMaxEquality(is_end[i], b_vars)
        
    m_count = model.NewIntVar(0, N, "m_count")
    model.Add(m_count == sum(is_end))
    
    TARGET_M = 13
    model.Add(m_count <= TARGET_M)
    
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return True
    return False

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'skeleton_results.md')
    
    elements, targets = get_canonical_subsets(yaml_path)
    
    print("Starting Ablation for M=14 Constraint Necessity...")
    load_bearing = []
    non_load_bearing = []
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Experiment 5.5: Constraint Necessity (The Skeleton)\n\n")
        
        for i, t in enumerate(targets):
            print(f"Testing {i+1}/{len(targets)}...")
            targets_to_use = [c for c in targets if c['id'] != t['id']]
            
            feasible = is_m13_feasible(elements, targets_to_use)
            if feasible:
                print(f"  -> SAT! LOAD-BEARING CONSTRAINT.")
                load_bearing.append(t['id'])
                f.write(f"- Removed `{t['id']}`: **SAT** (M drops to 13). `{t['id']}` is LOAD-BEARING.\n")
            else:
                print(f"  -> UNSAT! NOT load-bearing.")
                non_load_bearing.append(t['id'])
                f.write(f"- Removed `{t['id']}`: **UNSAT** (M remains 14).\n")
            f.flush()
                
        f.write("\n## The Skeleton (Load-Bearing Constraints)\n")
        f.write(f"Size of skeleton: {len(load_bearing)} out of {len(targets)} classes.\n")
        f.write(f"`{', '.join(load_bearing)}`\n\n")
        f.write("## Non-Load-Bearing Constraints (Redundant for M_count)\n")
        f.write(f"`{', '.join(non_load_bearing)}`\n")

if __name__ == '__main__':
    main()
