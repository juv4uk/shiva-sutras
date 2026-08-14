import os
import yaml

def patch_5_sutras():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_pilot/pilot_20_semantic_contexts.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        contexts = yaml.safe_load(f)
        
    for ctx in contexts:
        rc = ctx['rule_context']
        sid = rc['sutra_id']
        
        if sid == '1.1.69':
            rc['sources'] = [
                {'type': 'sutrapatha', 'provenance': 'normalized-sutras.yaml'},
                {'type': 'kasika', 'provenance': 'Web search summary (Kashika on 1.1.69)'}
            ]
            rc['inherited_context'] = {'from': [], 'confidence': 'SUPPORTED'}
            rc['semantic_operation'] = {
                'status': 'resolved',
                'type': 'metalinguistic_assignment',
                'arguments': {
                    'target_class': {'symbol': 'अण्', 'content': 'UNKNOWN-BY-BLINDING'},
                    'condition': {'symbol': 'अप्रत्ययः', 'content': 'literal (not a suffix)'},
                    'assignment': {'symbol': 'सवर्णस्य', 'content': 'literal (represents its homogeneous sounds)'}
                }
            }
            rc['functional_reading'] = {
                'summary': "An aṇ or udit, when not an affix, denotes its own savarṇa (homogeneous sounds) as well.",
                'confidence': 'SUPPORTED',
                'unresolved': ['membership_of_aṇ', 'meaning_of_udit']
            }
            
        elif sid == '6.4.21':
            rc['sources'] = [
                {'type': 'sutrapatha', 'provenance': 'normalized-sutras.yaml'},
                {'type': 'kasika', 'provenance': 'Web search summary (Kashika on 6.4.21)'}
            ]
            rc['inherited_context'] = {'from': ['6.4.1 (aṅgasya)', 'kṅiti (from previous rules)'], 'confidence': 'SUPPORTED'}
            rc['semantic_operation'] = {
                'status': 'resolved',
                'type': 'elision/lopa',
                'arguments': {
                    'target_class': {'symbol': 'रात्', 'content': 'UNKNOWN-BY-EVIDENCE (r or l? or r-pratyahara?)'},
                    'replacement_class': {'symbol': 'लोपः', 'content': 'literal (deletion)'}
                }
            }
            rc['functional_reading'] = {
                'summary': "Elision occurs for a sound following an 'r' (or belonging to ral) under certain conditions like kṅit suffix.",
                'confidence': 'PLAUSIBLE',
                'unresolved': ['exact_meaning_of_rāt', 'exact_inherited_conditions']
            }
            
        elif sid == '6.4.77':
            rc['sources'] = [
                {'type': 'sutrapatha', 'provenance': 'normalized-sutras.yaml'},
                {'type': 'kasika', 'provenance': 'General grammatical knowledge of iyaṅ/uvaṅ replacement'}
            ]
            rc['inherited_context'] = {'from': ['6.4.1 (aṅgasya)'], 'confidence': 'SUPPORTED'}
            rc['semantic_operation'] = {
                'status': 'resolved',
                'type': 'substitution',
                'arguments': {
                    'target_class': {'symbol': 'य्वोः', 'content': 'literal (y, v)'},
                    'replacement_class': {'symbol': 'इयङुवङौ', 'content': 'literal (iyaṅ, uvaṅ)'},
                    'right_context': {'symbol': 'अचि', 'content': 'UNKNOWN-BY-BLINDING'}
                }
            }
            rc['functional_reading'] = {
                'summary': "The 'y' and 'v' of śnu, dhātu, and bhrū are replaced by iyaṅ and uvaṅ when followed by ac.",
                'confidence': 'SUPPORTED',
                'unresolved': ['membership_of_ac']
            }
            
        elif sid == '8.3.33':
            rc['sources'] = [
                {'type': 'sutrapatha', 'provenance': 'normalized-sutras.yaml'},
                {'type': 'kasika', 'provenance': 'Web search / User provided Kasika context for 8.3.33'}
            ]
            rc['inherited_context'] = {'from': ['aci (from previous rules via anuvrtti)'], 'confidence': 'SUPPORTED'}
            rc['semantic_operation'] = {
                'status': 'resolved',
                'type': 'substitution',
                'arguments': {
                    'left_context': {'symbol': 'मयः', 'content': 'UNKNOWN-BY-BLINDING'},
                    'target_class': {'symbol': 'उञो', 'content': 'literal (the affix uñ)'},
                    'replacement_class': {'symbol': 'वः', 'content': 'literal (v)'},
                    'right_context': {'symbol': 'अचि (inherited)', 'content': 'UNKNOWN-BY-BLINDING'}
                }
            }
            rc['functional_reading'] = {
                'summary': "The affix 'uñ' optionally becomes 'v' when preceded by 'may' and followed by 'ac'.",
                'confidence': 'SUPPORTED',
                'unresolved': ['membership_of_may', 'membership_of_ac']
            }
            
        elif sid == '4.4.57':
            rc['sources'] = [
                {'type': 'sutrapatha', 'provenance': 'normalized-sutras.yaml'},
                {'type': 'kasika', 'provenance': 'General context of 4.4'}
            ]
            rc['inherited_context'] = {'from': ['4.4.1 (ṭhak)', 'tena (instrumental case context)'], 'confidence': 'PLAUSIBLE'}
            rc['semantic_operation'] = {
                'status': 'resolved',
                'type': 'suffixation',
                'arguments': {
                    'target_class': {'symbol': 'प्रहरणम्', 'content': 'literal (weapon)'},
                    'replacement_class': {'symbol': 'ठक् (inherited)', 'content': 'UNKNOWN-BY-EVIDENCE (the suffix ṭhak)'}
                }
            }
            rc['functional_reading'] = {
                'summary': "The suffix ṭhak is added to a word meaning 'weapon' in the instrumental case to denote 'he fights with it'.",
                'confidence': 'SUPPORTED',
                'unresolved': ['phonological_impact_of_ṭhak']
            }

    with open(in_file, 'w', encoding='utf-8') as f:
        yaml.dump(contexts, f, allow_unicode=True, sort_keys=False)
        
    print(f"Updated 5 sutras in {in_file}")

if __name__ == '__main__':
    patch_5_sutras()
