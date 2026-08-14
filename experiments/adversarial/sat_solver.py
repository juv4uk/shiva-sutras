import os
from ortools.sat.python import cp_model
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
    # Resolve exact subsets by finding them in the canonical sequence
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
        for i in range(len(canonical_sequence)):
            for pts in possible_sets:
                L = len(pts)
                if i + L <= len(canonical_sequence):
                    if set(canonical_sequence[i:i+L]) == pts:
                        resolved_set = list(canonical_sequence[i:i+L])
                        break
            if resolved_set:
                break
                
        if not resolved_set:
            print(f"WARNING: Could not resolve exact set for {p['id']}")
            
        targets.append({'id': p['id'], 'set': resolved_set})
        
    return canonical_sequence, targets

class SolutionCounter(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        if self.solution_count % 1000 == 0:
            print(f"Solutions found so far: {self.solution_count}")

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    
    elements, targets = get_canonical_subsets(yaml_path)
    N = len(elements)
    
    # Map elements to integers 0..N-1
    elem_to_id = {e: i for i, e in enumerate(elements)}
    
    model = cp_model.CpModel()
    
    # pos[i] is the position of element i in the new permutation
    pos = [model.NewIntVar(0, N - 1, f'pos_{i}') for i in range(N)]
    model.AddAllDifferent(pos)
    
    # For each target set, enforce that its elements form a contiguous block
    for t in targets:
        T_ids = [elem_to_id[e] for e in t['set']]
        L = len(T_ids)
        if L <= 1 or L == N:
            continue # Trivial
            
        start_pos = model.NewIntVar(0, N - L, f"start_{t['id']}")
        end_pos = model.NewIntVar(L - 1, N - 1, f"end_{t['id']}")
        model.Add(end_pos == start_pos + L - 1)
        
        for i in T_ids:
            model.Add(pos[i] >= start_pos)
            model.Add(pos[i] <= end_pos)
            
    # Symmetry breaking: reverse of any valid sequence is also valid.
    # We force 'a' to appear before 'h2' to cut the search space in half.
    if 'a' in elem_to_id and 'h2' in elem_to_id:
        model.Add(pos[elem_to_id['a']] < pos[elem_to_id['h2']])
        
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.max_time_in_seconds = 60.0 # 1 minute limit
    solution_counter = SolutionCounter()
    
    print("Starting CP-SAT solver to find ALL valid permutations...")
    status = solver.Solve(model, solution_counter)
    
    print(f"\nStatus: {solver.StatusName(status)}")
    print(f"Total valid permutations found: {solution_counter.solution_count}")
    
    out_file = os.path.join(base_dir, 'sat_results.md')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# SAT Solver Results\n")
        f.write(f"- Total elements: {N}\n")
        f.write(f"- Total constraints (target sets): {len(targets)}\n")
        f.write(f"- Total valid permutations: {solution_counter.solution_count}\n")
        f.write("\n## Symmetry Analysis\n")
        if solution_counter.solution_count > 0:
            f.write(f"The number of solutions ({solution_counter.solution_count}) indicates the size of the equivalence class of valid orderings.\n")

if __name__ == '__main__':
    main()
