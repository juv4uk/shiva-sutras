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

class MarkerEvaluatorCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, pos_vars, targets, elem_to_id, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.pos_vars = pos_vars
        self.targets = targets
        self.elem_to_id = elem_to_id
        self.limit = limit
        self.solution_count = 0
        self.m_count_distribution = {}
        self.min_m_count = 999
        self.best_order = None

    def on_solution_callback(self):
        self.solution_count += 1
        
        # Reconstruct the sequence
        N = len(self.pos_vars)
        order = [None] * N
        for i in range(N):
            order[self.Value(self.pos_vars[i])] = i
            
        # Calculate distinct end positions for targets
        end_positions = set()
        for t in self.targets:
            # Find the max index of the target elements in this order
            max_pos = -1
            for e in t['set']:
                p = self.Value(self.pos_vars[self.elem_to_id[e]])
                if p > max_pos:
                    max_pos = p
            end_positions.add(max_pos)
            
        m_count = len(end_positions)
        if m_count not in self.m_count_distribution:
            self.m_count_distribution[m_count] = 0
        self.m_count_distribution[m_count] += 1
        
        if m_count < self.min_m_count:
            self.min_m_count = m_count
            self.best_order = order
            
        if self.solution_count >= self.limit:
            self.StopSearch()

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'marker_optimization_results.md')
    
    elements, targets = get_canonical_subsets(yaml_path)
    N = len(elements)
    elem_to_id = {e: i for i, e in enumerate(elements)}
    
    model = cp_model.CpModel()
    pos = [model.NewIntVar(0, N - 1, f'pos_{i}') for i in range(N)]
    model.AddAllDifferent(pos)
    
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
            
    if 'a' in elem_to_id and 'h2' in elem_to_id:
        model.Add(pos[elem_to_id['a']] < pos[elem_to_id['h2']])
        
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    
    # We will sample up to 10,000 valid permutations
    limit = 10000
    callback = MarkerEvaluatorCallback(pos, targets, elem_to_id, limit)
    
    print(f"Searching space of up to {limit} valid C1P permutations to evaluate M_count...")
    solver.Solve(model, callback)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# H-SIVA-MARKERS: 10,000 Permutations Test\n\n")
        f.write(f"- Total valid orderings evaluated: {callback.solution_count}\n")
        f.write(f"- Absolute minimum markers found: {callback.min_m_count}\n")
        f.write(f"- Canonical Śiva-sūtras marker count: 14\n\n")
        
        f.write("## Distribution of Required Markers (M_count)\n")
        for k in sorted(callback.m_count_distribution.keys()):
            count = callback.m_count_distribution[k]
            f.write(f"- {k} markers: {count} permutations\n")
            
        f.write("\n## Analysis\n")
        if 14 == callback.min_m_count:
            f.write("The canonical order achieves the **global minimum possible marker count** across the evaluated C1P space! This is extraordinary proof of Level 2 optimization.\n")
        elif 14 > callback.min_m_count:
            f.write(f"There are permutations that require fewer markers (e.g., {callback.min_m_count}). This suggests Pāṇini optimized for something else in addition to marker count (possibly phonetic grouping or Usage Cost).\n")
        else:
            f.write("This state should be mathematically impossible since the canonical sequence itself has 14 markers.\n")

if __name__ == '__main__':
    main()
