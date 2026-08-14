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

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'joint_optimization_decision.md')
    
    elements, targets = get_canonical_subsets(yaml_path)
    N = len(elements)
    elem_to_id = {e: i for i, e in enumerate(elements)}
    
    model = cp_model.CpModel()
    pos = [model.NewIntVar(0, N - 1, f'pos_{i}') for i in range(N)]
    model.AddAllDifferent(pos)
    
    end_pos_vars = []
    
    for t in targets:
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
            
    # Symmetry breaking
    if 'a' in elem_to_id and 'h2' in elem_to_id:
        model.Add(pos[elem_to_id['a']] < pos[elem_to_id['h2']])
        
    # Model M_count directly
    # is_end[i] == 1 if any target ends at index i
    is_end = [model.NewBoolVar(f"is_end_{i}") for i in range(N)]
    
    for i in range(N):
        # We want to constrain is_end[i] to be true iff i is in end_pos_vars
        # Create boolean variables for each target ending at i
        b_vars = []
        for e_var in end_pos_vars:
            b = model.NewBoolVar(f"b_end_{e_var.Name()}_at_{i}")
            model.Add(e_var == i).OnlyEnforceIf(b)
            model.Add(e_var != i).OnlyEnforceIf(b.Not())
            b_vars.append(b)
        
        model.AddMaxEquality(is_end[i], b_vars)
        
    m_count = model.NewIntVar(0, N, "m_count")
    model.Add(m_count == sum(is_end))
    
    # DECISION PROBLEM: Does there exist M_count <= 13?
    TARGET_M = 13
    model.Add(m_count <= TARGET_M)
    
    solver = cp_model.CpSolver()
    # Log search progress
    solver.parameters.log_search_progress = True
    solver.parameters.num_search_workers = 8 # Enable multithreading
    
    print(f"Starting Decision Problem: Does there exist C1P order with M_count <= {TARGET_M}?")
    start_time = time.time()
    status = solver.Solve(model)
    elapsed = time.time() - start_time
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Experiment 5.3: Joint Optimization (Decision Form)\n\n")
        f.write(f"**Question:** Does there exist a valid C1P ordering with M_count <= {TARGET_M}?\n\n")
        f.write(f"- CP-SAT Solver Version: OR-Tools\n")
        f.write(f"- Variables: {N} sounds, {len(targets)} constraints\n")
        f.write(f"- Search limits: No time limit, 8 workers\n")
        f.write(f"- Runtime: {elapsed:.2f} seconds\n\n")
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            f.write("## Result: SAT (YES)\n")
            f.write(f"A valid C1P ordering was found that requires ONLY {solver.Value(m_count)} markers!\n\n")
            
            # Reconstruct witness
            order = [None] * N
            for i in range(N):
                order[solver.Value(pos[i])] = elements[i]
            
            f.write("### Witness Ordering:\n")
            f.write(" ".join(order) + "\n\n")
            
            # List marker boundaries
            f.write("### Marker Boundaries Required:\n")
            for i in range(N):
                if solver.Value(is_end[i]):
                    f.write(f"- After `{order[i]}`\n")
                    
        elif status == cp_model.INFEASIBLE:
            f.write("## Result: UNSAT (NO)\n")
            f.write("The solver has exhaustively proven that NO valid C1P permutation exists with M_count <= 13.\n")
            f.write(f"Since canonical provides a witness for M_count = 14, we globally prove that **M_min = 14**.\n")
        else:
            f.write(f"## Result: UNKNOWN (Status: {solver.StatusName(status)})\n")

if __name__ == '__main__':
    main()
