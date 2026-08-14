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

class GeometryEvaluatorCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, pos_vars, targets, elem_to_id, elements, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.pos_vars = pos_vars
        self.targets = targets
        self.elem_to_id = elem_to_id
        self.elements = elements
        self.limit = limit
        self.solution_count = 0
        
        self.m14_count = 0
        # structural_classes maps fingerprint -> list of witnesses
        self.structural_classes = {}

    def on_solution_callback(self):
        self.solution_count += 1
        
        # Reconstruct the sequence
        N = len(self.pos_vars)
        order = [None] * N
        for i in range(N):
            order[self.Value(self.pos_vars[i])] = self.elements[i]
            
        # Calculate distinct end positions for targets
        end_positions = set()
        for t in self.targets:
            max_pos = -1
            for e in t['set']:
                p = self.Value(self.pos_vars[self.elem_to_id[e]])
                if p > max_pos:
                    max_pos = p
            end_positions.add(max_pos)
            
        if len(end_positions) == 14:
            self.m14_count += 1
            
            # Create Structural Fingerprint
            sorted_ends = sorted(list(end_positions))
            fingerprint_blocks = []
            start_idx = 0
            for end_idx in sorted_ends:
                block_sounds = order[start_idx:end_idx+1]
                # Sort internally to abstract away P-node permutations
                sorted_block = tuple(sorted(block_sounds))
                fingerprint_blocks.append(sorted_block)
                start_idx = end_idx + 1
                
            fingerprint = tuple(fingerprint_blocks)
            rev_fingerprint = tuple(reversed(fingerprint_blocks))
            
            # Normalize for global reversal symmetry
            canonical_fingerprint = min(fingerprint, rev_fingerprint)
            
            if canonical_fingerprint not in self.structural_classes:
                self.structural_classes[canonical_fingerprint] = []
            self.structural_classes[canonical_fingerprint].append(order)
            
        if self.solution_count >= self.limit:
            self.StopSearch()

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    out_file = os.path.join(base_dir, 'geometry_results.md')
    
    canonical_seq, targets = get_canonical_subsets(yaml_path)
    N = len(canonical_seq)
    elem_to_id = {e: i for i, e in enumerate(canonical_seq)}
    
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
    
    # We will sample 50,000 valid permutations
    limit = 50000
    callback = GeometryEvaluatorCallback(pos, targets, elem_to_id, canonical_seq, limit)
    
    print(f"Searching space of {limit} valid C1P permutations for Geometry extraction...")
    solver.Solve(model, callback)
    
    # Get the canonical order's fingerprint
    canon_end_positions = set()
    for t in targets:
        max_pos = -1
        for e in t['set']:
            p = elem_to_id[e]
            if p > max_pos: max_pos = p
        canon_end_positions.add(max_pos)
        
    sorted_ends = sorted(list(canon_end_positions))
    canon_blocks = []
    start_idx = 0
    for end_idx in sorted_ends:
        block_sounds = canonical_seq[start_idx:end_idx+1]
        canon_blocks.append(tuple(sorted(block_sounds)))
        start_idx = end_idx + 1
        
    canon_fp = tuple(canon_blocks)
    rev_canon_fp = tuple(reversed(canon_blocks))
    normalized_canon_fp = min(canon_fp, rev_canon_fp)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Experiment 5.4: Geometry of the Optimum (M=14)\n\n")
        f.write(f"- Total raw C1P orderings evaluated: {callback.solution_count}\n")
        f.write(f"- Raw orderings achieving M=14: {callback.m14_count}\n")
        f.write(f"- Number of UNIQUE Structural Equivalence Classes: {len(callback.structural_classes)}\n\n")
        
        f.write("## Structural Equivalence Classes\n")
        is_canon_found = False
        
        for fp, witnesses in callback.structural_classes.items():
            is_canonical = (fp == normalized_canon_fp)
            if is_canonical: is_canon_found = True
            
            f.write(f"### Class (Witnesses: {len(witnesses)}) {'⭐ [CANONICAL]' if is_canonical else ''}\n")
            # Print the blocks
            for i, block in enumerate(fp):
                f.write(f"- Block {i+1}: `{{ {', '.join(block)} }}`\n")
            f.write("\n")
            
        f.write("## Analysis\n")
        if len(callback.structural_classes) == 1:
            f.write("Astounding! All raw optimum permutations collapse into a SINGLE Structural Equivalence Class. The marker geometry is an absolute invariant of the optimum space!\n")
        else:
            f.write(f"There are {len(callback.structural_classes)} different structural ways to achieve M=14 in this sample.\n")

if __name__ == '__main__':
    main()
