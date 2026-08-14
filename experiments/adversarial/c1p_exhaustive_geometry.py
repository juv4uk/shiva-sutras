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
    out_file = os.path.join(base_dir, 'exhaustive_geometry_results.md')
    
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
    
    # We want M <= 14
    model.Add(m_count <= 14)
    
    # Define prefix_markers[i] = sum(is_end[0..i-1])
    prefix_markers = [model.NewIntVar(0, 14, f"prefix_markers_{i}") for i in range(N)]
    model.Add(prefix_markers[0] == 0)
    for i in range(1, N):
        model.Add(prefix_markers[i] == prefix_markers[i-1] + is_end[i-1])
        
    # Define Block ID for each phoneme: B[X] = prefix_markers[pos[X]]
    B = [model.NewIntVar(0, 14, f"B_{i}") for i in range(N)]
    for i in range(N):
        model.AddElement(pos[i], prefix_markers, B[i])
        
    # Define Class A and Class B block assignments
    # Class A:
    # 0: {a, i, u}, 1: {ṛ, ḷ}, 2: {ai, au}, 3: {e, o}, 4: {h1, r, v, y}, 5: {l}, 6: {m, n, ñ, ṅ, ṇ}
    # 7: {bh, jh}, 8: {dh, gh, ḍh}, 9: {b, d, g, j, ḍ}, 10: {c, ch, kh, ph, t, th, ṭ, ṭh}, 11: {k, p}, 12: {s, ś, ṣ}, 13: {h2}
    
    # Class B (Canonical):
    # 0: {a, i, u}, 1: {ṛ, ḷ}, 2: {e, o}, 3: {ai, au}, ... rest identical
    
    def get_class_assignment(swap_diphthongs=False):
        blocks = [
            ["a", "i", "u"], ["ṛ", "ḷ"], 
            ["e", "o"] if swap_diphthongs else ["ai", "au"],
            ["ai", "au"] if swap_diphthongs else ["e", "o"],
            ["h1", "r", "v", "y"], ["l"], ["m", "n", "ñ", "ṅ", "ṇ"],
            ["bh", "jh"], ["dh", "gh", "ḍh"], ["b", "d", "g", "j", "ḍ"],
            ["c", "ch", "kh", "ph", "t", "th", "ṭ", "ṭh"], ["k", "p"],
            ["s", "ś", "ṣ"], ["h2"]
        ]
        assignment = {}
        for block_idx, phonemes in enumerate(blocks):
            for ph in phonemes:
                assignment[elem_to_id[ph]] = block_idx
        return assignment
        
    assign_A = get_class_assignment(swap_diphthongs=False)
    assign_B = get_class_assignment(swap_diphthongs=True)
    
    # Constraint: Not Class A
    matches_A = []
    for i in range(N):
        match = model.NewBoolVar(f"match_A_{i}")
        model.Add(B[i] == assign_A[i]).OnlyEnforceIf(match)
        model.Add(B[i] != assign_A[i]).OnlyEnforceIf(match.Not())
        matches_A.append(match)
    model.Add(sum(matches_A) < N) # Cannot match all phonemes
    
    # Constraint: Not Class B
    matches_B = []
    for i in range(N):
        match = model.NewBoolVar(f"match_B_{i}")
        model.Add(B[i] == assign_B[i]).OnlyEnforceIf(match)
        model.Add(B[i] != assign_B[i]).OnlyEnforceIf(match.Not())
        matches_B.append(match)
    model.Add(sum(matches_B) < N)
    
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    
    print("Starting Exhaustive Two-Class Proof...")
    start_time = time.time()
    status = solver.Solve(model)
    elapsed = time.time() - start_time
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Experiment 5.4b: Exhaustive Two-Class Proof\n\n")
        f.write(f"**Question:** Does there exist ANY valid C1P ordering with M_count <= 14 that is NOT in Structural Class A and NOT in Structural Class B?\n")
        f.write(f"- Runtime: {elapsed:.2f} seconds\n\n")
        
        if status == cp_model.INFEASIBLE:
            f.write("## Result: UNSAT (NO)\n")
            f.write("The solver exhaustively proved that NO OTHER structural classes exist.\n")
            f.write("The M=14 optimum space contains **EXACTLY TWO** structural equivalence classes across all possible valid orderings.\n")
        elif status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            f.write("## Result: SAT (YES)\n")
            f.write("Found a solution that does NOT belong to Class A or B!\n")
            # Extract new class
            f.write("### New Witness Ordering:\n")
            order = [None] * N
            for i in range(N):
                order[solver.Value(pos[i])] = elements[i]
            f.write(" ".join(order) + "\n\n")
            f.write("### New Block Assignments:\n")
            for i in range(N):
                f.write(f"- `{elements[i]}` -> Block {solver.Value(B[i])}\n")

if __name__ == '__main__':
    main()
