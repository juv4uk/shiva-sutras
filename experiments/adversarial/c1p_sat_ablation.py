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
                
        if resolved_set:
            targets.append({'id': p['id'], 'set': resolved_set})
            
    return canonical_sequence, targets

class SolutionLimitCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.solution_count = 0
        self.limit = limit

    def on_solution_callback(self):
        self.solution_count += 1
        if self.solution_count >= self.limit:
            self.StopSearch()

def count_solutions(elements, active_targets, max_sols=100, enforce_symmetry_break=True):
    N = len(elements)
    elem_to_id = {e: i for i, e in enumerate(elements)}
    
    model = cp_model.CpModel()
    pos = [model.NewIntVar(0, N - 1, f'pos_{i}') for i in range(N)]
    model.AddAllDifferent(pos)
    
    for t in active_targets:
        T_ids = [elem_to_id[e] for e in t['set']]
        L = len(T_ids)
        if L <= 1 or L == N:
            continue
            
        start_pos = model.NewIntVar(0, N - L, f"start_{t['id']}")
        end_pos = model.NewIntVar(L - 1, N - 1, f"end_{t['id']}")
        model.Add(end_pos == start_pos + L - 1)
        
        for i in T_ids:
            model.Add(pos[i] >= start_pos)
            model.Add(pos[i] <= end_pos)
            
    if enforce_symmetry_break and 'a' in elem_to_id and 'h2' in elem_to_id:
        model.Add(pos[elem_to_id['a']] < pos[elem_to_id['h2']])
        
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.max_time_in_seconds = 10.0
    callback = SolutionLimitCallback(max_sols)
    
    status = solver.Solve(model, callback)
    
    # If the solver reached the limit or finished optimally
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return callback.solution_count
    elif status == cp_model.INFEASIBLE:
        return 0
    else:
        # Timeout or UNKNOWN
        return callback.solution_count

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'c1p_ablation_results.md')
    
    elements, targets = get_canonical_subsets(yaml_path)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(f"# C1P Exact Admissible Orderings and Ablation\n\n")
        f.write(f"- Total elements: {len(elements)}\n")
        f.write(f"- Total constraints: {len(targets)}\n\n")
        
        f.write("## Step 1: Evaluating full constraint set\n")
        sols = count_solutions(elements, targets, max_sols=10000, enforce_symmetry_break=True)
        f.write(f"Valid permutations with all constraints (modulo reversal): {sols}\n")
        
        if sols == 1:
            f.write("-> The canonical ordering is practically UNIQUE!\n")
        elif sols == 0:
            f.write("-> ERROR: Found 0 solutions. Check constraint formulation.\n")
            return
        else:
            f.write(f"-> There are at least {sols} valid orderings. The order is NOT strictly unique.\n")
            f.write("We cannot find a unique minimal determining set if the base space is not unique.\n")
            
        f.write("\n## Step 2: Greedy Ablation (Finding Minimal Determining Set)\n")
        baseline_sols = sols
        active_constraints = targets.copy()
        redundant = []
        critical = []
        
        for t in targets:
            test_constraints = [c for c in active_constraints if c['id'] != t['id']]
            test_sols = count_solutions(elements, test_constraints, max_sols=baseline_sols + 1, enforce_symmetry_break=True)
            
            if test_sols == baseline_sols:
                active_constraints = test_constraints
                redundant.append(t['id'])
                f.write(f"[-] Removed `{t['id']}` (Redundant, space still {baseline_sols})\n")
                f.flush()
            else:
                critical.append(t['id'])
                f.write(f"[+] Kept `{t['id']}` (CRITICAL, removing it explodes space > {baseline_sols})\n")
                f.flush()
                
        f.write("\n### ABLATION RESULTS\n")
        f.write(f"Original Constraints: {len(targets)}\n")
        f.write(f"Minimal Determining Set Size: {len(critical)}\n")
        f.write(f"Critical Constraints: {', '.join(critical)}\n")
        f.write(f"Redundant Constraints: {', '.join(redundant)}\n")

if __name__ == '__main__':
    main()
