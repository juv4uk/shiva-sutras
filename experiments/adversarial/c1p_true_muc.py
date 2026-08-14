import os
import yaml
from ortools.sat.python import cp_model
import time

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
    
    model.Add(m_count <= 13)
    
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return True
    return False

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'true_muc_results.md')
    
    elements, targets = get_canonical_subsets(yaml_path)
    
    # Known individually critical constraints (these will definitely be in the MUC)
    critical_ids = {"aṇ", "aṭ", "eṅ", "aic", "yañ", "jhaṣ", "chav"}
    
    current_core = [t for t in targets]
    
    print("Starting Greedy MUC Extraction for M=14...")
    start_time = time.time()
    
    # We iterate over all targets. If removing a target keeps the system UNSAT, 
    # we permanently remove it. If removing it makes the system SAT, we must keep it.
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Experiment 5.5c: True Minimal Forcing Core (MUC)\n\n")
        f.write("Finding the exact minimal subset of constraints that force M=14.\n\n")
        
        for i in range(len(targets) - 1, -1, -1):
            t = targets[i]
            
            # Skip if it's already known to be critical to save time
            if t['id'] in critical_ids:
                print(f"Skipping (known critical)")
                continue
                
            print(f"[{len(current_core)} constraints left] Trying to remove...")
            
            # Create a test core without this target
            test_core = [c for c in current_core if c['id'] != t['id']]
            
            is_sat = is_m13_feasible(elements, test_core)
            
            if is_sat:
                print(f"  -> SAT! Must KEEP.")
            else:
                print(f"  -> UNSAT! Successfully REMOVED.")
                current_core = test_core # Permanently remove
                
        elapsed = time.time() - start_time
        
        core_ids = [c['id'] for c in current_core]
        
        f.write(f"- Extraction Time: {elapsed:.2f} seconds\n")
        f.write(f"- True Minimal Forcing Core Size: **{len(current_core)}** classes (out of 42)\n\n")
        
        f.write("## The True MUC\n")
        f.write(f"`{', '.join(core_ids)}`\n\n")
        
        f.write("## Redundant Classes (Not in this MUC)\n")
        redundant = [c['id'] for c in targets if c['id'] not in core_ids]
        f.write(f"`{', '.join(redundant)}`\n\n")

if __name__ == '__main__':
    main()
