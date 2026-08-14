import os
import yaml
import random

def main():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/candidate-phonological-rules.yaml'))
    out_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot'))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'pilot_20_rules_selection.yaml')
    
    with open(in_file, 'r', encoding='utf-8') as f:
        sutras = yaml.safe_load(f)
        
    # We only care about YES or MAYBE
    candidates = [s for s in sutras if s['phonology_candidate']['status'] in ['yes', 'maybe']]
    
    pilot_sutras = []
    selected_ids = set()
    
    def add_sutra(sutra, reason):
        if sutra['sutra_id'] not in selected_ids:
            sutra['pilot_selection_reason'] = reason
            pilot_sutras.append(sutra)
            selected_ids.add(sutra['sutra_id'])
            
    # Helper to find by trigger
    def find_and_add(trigger_match, reason, count=2):
        matches = [s for s in candidates if any(trigger_match in t for t in s['phonology_candidate']['triggers']) and s['sutra_id'] not in selected_ids]
        random.shuffle(matches)
        for m in matches[:count]:
            add_sutra(m, reason)
            
    def find_by_domain(domain_match, reason, count=2):
        matches = [s for s in candidates if s['candidate_domain'] == domain_match and s['sutra_id'] not in selected_ids]
        random.shuffle(matches)
        for m in matches[:count]:
            add_sutra(m, reason)
            
    def find_by_role(role_match, reason, count=2):
        matches = [s for s in candidates if 'roles' in s['phonology_candidate'] and role_match in s['phonology_candidate']['roles'].values() and s['sutra_id'] not in selected_ids]
        random.shuffle(matches)
        for m in matches[:count]:
            add_sutra(m, reason)

    # 1. Explicit substitution (lexical:आदेश or syntactic_replacement_pattern)
    find_and_add("syntactic_replacement_pattern", "explicit_substitution", 2)
    find_and_add("lexical:आदेश", "explicit_substitution", 1)
    
    # 2. Lopa
    find_and_add("lexical:लोप", "lopa_operation", 2)
    
    # 3. Agama
    find_and_add("lexical:आगम", "agama_operation", 2)
    
    # 4. Savarna
    find_and_add("lexical:सवर्ण", "savarna_operation", 2)
    
    # 5. Opaque target class
    find_by_role("target/left_context", "opaque_target_class", 2)
    
    # 6. Opaque context class
    find_by_role("right_context", "opaque_context_class", 2)
    
    # 7. Anuvrtti-heavy rule
    find_and_add("inherited-context-candidate", "anuvrtti_heavy_rule", 3)
    
    # 8. Shape-conditioned morphology
    find_and_add("derived_shape", "shape_conditioned_morphology", 2)
    
    # 9. Metalinguistic sound rule
    find_by_domain("metalinguistic_sound_structure", "metalinguistic_sound_rule", 2)
    
    # Fill up to 20 if needed
    remaining = 20 - len(pilot_sutras)
    if remaining > 0:
        other_candidates = [s for s in candidates if s['sutra_id'] not in selected_ids]
        random.shuffle(other_candidates)
        for m in other_candidates[:remaining]:
            add_sutra(m, "random_filler")
            
    # Sort by sutra ID to make it somewhat logical, though Aṣṭādhyāyī order is important
    # Actually sorting by sutra ID mathematically (1.1.1 -> 1, 1, 1)
    def parse_id(sid):
        return tuple(map(int, sid.split('.')))
        
    pilot_sutras.sort(key=lambda s: parse_id(s['sutra_id']))
    
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(pilot_sutras, f, allow_unicode=True, sort_keys=False)
        
    print(f"Pilot selection complete. {len(pilot_sutras)} sutras written to {out_file}.")

if __name__ == '__main__':
    # Set seed for reproducibility during tests
    random.seed(42)
    main()
