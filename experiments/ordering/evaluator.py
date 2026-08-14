import yaml
import os
import random

def load_targets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    targets = []
    for p in data['pratyaharas']:
        targets.append({
            'id': p['id'],
            'set': p['set']
        })
    return targets

def is_contiguous(sequence, target_set):
    """
    Checks if target_set can be found as a contiguous slice in the sequence.
    Handles 'h' specially since 'h' appears twice in the canonical sequence (h1, h2).
    """
    L = len(target_set)
    if L == 0: return False
    if L > len(sequence): return False
    
    # We will generate all possible exact target sets by resolving 'h'
    # In target_set, 'h' might appear 1 or 2 times. 
    # Usually it's 1 time in our YAML (even if technically hal has two, we might have de-duplicated it in Python script. 
    # Let's count how many h's).
    base_set = set(target_set)
    has_h = 'h' in base_set
    
    possible_target_sets = []
    if has_h:
        # It could map to h1, h2, or both
        s1 = base_set.copy()
        s1.remove('h')
        s1.add('h1')
        possible_target_sets.append(s1)
        
        s2 = base_set.copy()
        s2.remove('h')
        s2.add('h2')
        possible_target_sets.append(s2)
        
        s3 = base_set.copy()
        s3.remove('h')
        s3.add('h1')
        s3.add('h2')
        possible_target_sets.append(s3)
    else:
        possible_target_sets.append(base_set)
        
    for i in range(len(sequence) - L + 1):
        # We need to check slices of length L, or L+1 (if target set had one 'h' but maps to h1 and h2)
        # Actually, let's just check all slices of length len(pts) for each pts in possible_target_sets
        for pts in possible_target_sets:
            slice_len = len(pts)
            if i + slice_len <= len(sequence):
                slice_set = set(sequence[i:i+slice_len])
                if slice_set == pts:
                    return True
    return False

def evaluate(sequence, targets):
    score = 0
    failed = []
    for t in targets:
        if is_contiguous(sequence, t['set']):
            score += 1
        else:
            failed.append(t['id'])
    return score, failed

def main():
    base_dir = os.path.dirname(__file__)
    yaml_path = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/pratyahara-usage.yaml'))
    targets = load_targets(yaml_path)
    
    # Define the 42 distinct slots
    canonical_sequence = [
        "a", "i", "u", 
        "ṛ", "ḷ", 
        "e", "o", 
        "ai", "au", 
        "h1", "y", "v", "r", 
        "l", 
        "ñ", "m", "ṅ", "ṇ", "n", 
        "jh", "bh", 
        "gh", "ḍh", "dh", 
        "j", "b", "g", "ḍ", "d", 
        "kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", 
        "k", "p", 
        "ś", "ṣ", "s", 
        "h2"
    ]
    
    out_file = os.path.join(base_dir, 'results_001.md')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(f"Loaded {len(targets)} target pratyaharas.\n\n")
        
        # 1. Baseline (Original)
        score_orig, failed_orig = evaluate(canonical_sequence, targets)
        f.write(f"--- BASELINE (Original Śiva-sūtras) ---\n")
        f.write(f"Score: {score_orig}/{len(targets)}\n")
        if failed_orig:
            f.write(f"Failed: {failed_orig}\n")
            
        # 2. Alphabetic (Traditional Indian Alphabet order)
        # Vowels first, then consonants in varga order
        alphabetic_sequence = [
            "a", "i", "u", "ṛ", "ḷ", "e", "ai", "o", "au",
            "k", "kh", "g", "gh", "ṅ",
            "c", "ch", "j", "jh", "ñ",
            "ṭ", "ṭh", "ḍ", "ḍh", "ṇ",
            "t", "th", "d", "dh", "n",
            "p", "ph", "b", "bh", "m",
            "y", "r", "l", "v",
            "ś", "ṣ", "s", "h1", "h2"
        ]
        score_alpha, failed_alpha = evaluate(alphabetic_sequence, targets)
        f.write(f"\n--- ALPHABETIC ORDER ---\n")
        f.write(f"Score: {score_alpha}/{len(targets)}\n")
        
        # 3. Random permutations
        f.write(f"\n--- RANDOM SEARCH (10,000 permutations) ---\n")
        iterations = 10000
        max_score = 0
        scores = []
        
        for _ in range(iterations):
            seq = canonical_sequence.copy()
            random.shuffle(seq)
            score, _ = evaluate(seq, targets)
            scores.append(score)
            if score > max_score:
                max_score = score
                
        avg_score = sum(scores) / len(scores)
        f.write(f"Max score achieved: {max_score}/{len(targets)}\n")
        f.write(f"Average score: {avg_score:.2f}/{len(targets)}\n")
    print("Results written to results_001.md")

if __name__ == "__main__":
    main()
