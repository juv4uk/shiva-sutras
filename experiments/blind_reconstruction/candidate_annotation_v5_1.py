import os
import re
import yaml

def get_domain_and_prior(sutra_id):
    parts = sutra_id.split('.')
    if len(parts) < 2: return "unknown", "low"
    adhyaya = parts[0]
    pada = parts[1]
    
    if (adhyaya, pada) in [("6", "2"), ("8", "1")]:
        domain = "prosody_accent"
        prior = "low"
    elif (adhyaya, pada) == ("1", "3"):
        domain = "grammatical_notation"
        prior = "low"
    else:
        domain = "segmental_phonology/morphophonology"
        
        high_priors = [
            ("6", "1"), ("6", "4"),
            ("7", "1"), ("7", "2"), ("7", "3"), ("7", "4"),
            ("8", "2"), ("8", "3"), ("8", "4")
        ]
        if (adhyaya, pada) in high_priors:
            prior = "high"
        elif (adhyaya, pada) == ("1", "1"):
            prior = "medium"
        else:
            prior = "low"
            
    return domain, prior

def build_declension_dict():
    opaque_bases = [
        "अच्", "अल्", "हल्", "इक्", "यण्", "एच्", "एङ्", "ऐच्", "अक्", "उक्", "अण्", "अश्",
        "हस्", "हश्", "यञ्", "झल्", "झर्", "खर्", "शर्", "जश्", "भश्", "वल्", "रल्", "मय्",
        "ञम्", "चय्", "यर्"
    ]
    declensions = {}
    for base in opaque_bases:
        if base.endswith('\u094d'):
            stem = base[:-1]
            declensions[base] = {'class': base, 'case': 'base'}
            declensions[stem + '\u0903'] = {'class': base, 'case': 'genitive/ablative'}
            declensions[stem + '\u093f'] = {'class': base, 'case': 'locative'}
        else:
            declensions[base] = {'class': base, 'case': 'base'}
    return declensions

OPAQUE_DECLENSIONS = build_declension_dict()

def detect_opaque_classes(padaccheda):
    found = []
    words = padaccheda.split()
    for word in words:
        if word in OPAQUE_DECLENSIONS:
            found.append(OPAQUE_DECLENSIONS[word])
    return found

def apply_vowel_sandhi(prefix, shape):
    if not prefix.endswith('\u094d'):
        return prefix + shape
        
    stem = prefix[:-1] # drop virama
    first_char = shape[0]
    rest_shape = shape[1:]
    
    vowel_map = {
        '\u0905': '',       # a -> no sign
        '\u0906': '\u093e', # ā
        '\u0907': '\u093f', # i
        '\u0908': '\u0940', # ī
        '\u0909': '\u0941', # u
        '\u090a': '\u0942', # ū
        '\u090b': '\u0943', # ṛ
        '\u090f': '\u0947', # e
        '\u0910': '\u0948', # ai
        '\u0913': '\u094b', # o
        '\u0914': '\u094c', # au
    }
    
    if first_char in vowel_map:
        return stem + vowel_map[first_char] + rest_shape
    else:
        return prefix + shape

def detect_latent_sandhi(text):
    prefixes = [
        "अग्", "इग्", "उग्", "अज्", "एज्", "ऐज्", "अल्", "हल्", "यण्", "अण्", "इण्",
        "अद्", "आद्", "इद्", "ईद्", "उद्", "ऊद्", "ऋद्", "एद्", "ओद्", "ऐद्", "औद्"
    ]
    shapes = ["उपध", "आदि", "आदे", "अन्त"]
    
    triggers = []
    for p in prefixes:
        for s in shapes:
            sandhi_form = apply_vowel_sandhi(p, s)
            if sandhi_form in text:
                triggers.append(f"latent_technical_compound:{sandhi_form}")
    return triggers

def annotate_sutra_base(sutra):
    triggers = []
    padaccheda = sutra.get('padaccheda', '')
    text = sutra.get('source_text', '') + " " + padaccheda
    
    # 1. Lexical Triggers
    lexical_keywords = [
        "आदेश", "लोप", "लुक्", "श्लु", "लुप्", 
        "आगम", "नुम्", "मुट्", "सुक्", "सुग्", "इट्", "टु",
        "दीर्घ", "ह्रस्व", "प्लुत", "गुण", "वृद्धि", "सवर्ण", "सन्धि", "संहिता"
    ]
    for kw in lexical_keywords:
        if kw in text:
            triggers.append(f"lexical:{kw}")
            
    # 2. Opaque Symbol Detection
    opaque_classes = detect_opaque_classes(padaccheda)
    roles = {}
    if opaque_classes:
        triggers.append("opaque_symbols_detected")
        for oc in opaque_classes:
            c = oc['class']
            case = oc['case']
            if case == 'base': roles[c] = 'replacement/target'
            elif case == 'locative': roles[c] = 'right_context'
            elif case == 'genitive/ablative': roles[c] = 'target/left_context'
            
    # 3. Derived Shape / Morpheme Triggers
    shape_keywords = [
        "उपध", "आदि", "आदे", "अन्त", "अल्", "एकाल्", "एकाच", "एकाच्", "अनेकाच", "अनेकाच्", "द्व्यच", "द्व्यच्",
        "गुरु", "लघु", "आत्", "अतः", "इतः", "उतः", "ऋतः", "वर्ण"
    ]
    has_shape = False
    for kw in shape_keywords:
        if kw in text:
            triggers.append(f"derived_shape:{kw}")
            has_shape = True
            
    # 4. Latent Sandhi Technical Compounds
    latent_triggers = detect_latent_sandhi(text)
    if latent_triggers:
        triggers.extend(latent_triggers)
        has_shape = True
        
    # 5. Prosody Morphemes (Compound-Aware)
    prosody_morphemes = ["उदात्त", "अनुदात्त", "स्वरित", "स्वर", "एकश्रुति"]
    has_prosody = False
    for kw in prosody_morphemes:
        if kw in text:
            triggers.append(f"prosody_morpheme:{kw}")
            has_prosody = True
            
    # 6. Syntactic Replacement Pattern (Bidirectional)
    has_syntactic_replacement = False
    if re.search(r'\S+\s+६/[१२३]\s+\S+\s+१/[१२३]', padaccheda) or re.search(r'\S+\s+१/[१२३]\s+\S+\s+६/[१२३]', padaccheda):
        triggers.append("syntactic_replacement_pattern")
        has_syntactic_replacement = True
            
    # 7. Domains & Priors
    domain, prior = get_domain_and_prior(sutra['sutra_id'])
    
    if has_prosody:
        domain = "prosody_accent"
    
    sutra_type = sutra.get('sutra_type')
    if sutra_type == 'संज्ञा':
        if has_shape:
            domain = "metalinguistic_sound_structure"
        elif domain != "prosody_accent":
            domain = "terminology"
            
    sutra['candidate_domain'] = domain
    triggers.append(f"prior:{prior}")
    
    # Status Logic
    status = "no"
    
    has_lexical = any(t.startswith("lexical:") for t in triggers)
    has_opaque = "opaque_symbols_detected" in triggers
    
    if has_lexical or has_opaque:
        status = "yes"
    elif prior == "high":
        status = "maybe"
        
    if (has_shape or has_syntactic_replacement or latent_triggers or has_prosody) and status == "no":
        status = "maybe"
        
    if sutra_type == 'विधि':
        triggers.append("type:vidhi")
        if status == "no":
            status = "maybe"
            
    if domain in ["prosody_accent", "grammatical_notation", "metalinguistic_sound_structure"]:
        if status == "yes":
            status = "maybe"
            triggers.append(f"demoted_due_to_domain:{domain}")
            
    sutra['phonology_candidate'] = {
        'status': status,
        'triggers': triggers,
        'opaque_classes': list(set([o['class'] for o in opaque_classes])),
        'roles': roles
    }
    return sutra

def main():
    base_dir = os.path.dirname(__file__)
    in_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/normalized-sutras.yaml'))
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/candidate-phonological-rules.yaml'))
    
    with open(in_file, 'r', encoding='utf-8') as f:
        sutras = yaml.safe_load(f)
        
    annotated = []
    
    # Pass 1: Base annotation
    for s in sutras:
        annotated.append(annotate_sutra_base(s))
        
    # Pass 2: Anuvrtti-risk propagation
    anuvrtti_active = False
    for i in range(len(annotated)):
        status = annotated[i]['phonology_candidate']['status']
        padaccheda = annotated[i].get('padaccheda', '')
        words_count = len(padaccheda.split())
        
        if status == "yes":
            anuvrtti_active = True
        else:
            if anuvrtti_active and words_count <= 3:
                if status == "no":
                    annotated[i]['phonology_candidate']['status'] = "maybe"
                    annotated[i]['phonology_candidate']['triggers'].append("inherited-context-candidate")
            else:
                anuvrtti_active = False
                
    stats = {'yes': 0, 'maybe': 0, 'no': 0}
    for a in annotated:
        stats[a['phonology_candidate']['status']] += 1
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(annotated, f, allow_unicode=True, sort_keys=False)
        
    print(f"Annotation v5.1 Complete. Total: {len(annotated)}")
    print(f"Yes: {stats['yes']}, Maybe: {stats['maybe']}, No: {stats['no']}")
    print(f"Candidate Harvest is officially FROZEN.")

if __name__ == '__main__':
    main()
