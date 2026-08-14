import os
import re
import yaml
import random

def get_domain_and_prior(sutra_id):
    parts = sutra_id.split('.')
    if len(parts) < 2: return "unknown", "low"
    adhyaya = parts[0]
    pada = parts[1]
    
    # Domains
    if (adhyaya, pada) in [("6", "2"), ("8", "1")]:
        domain = "prosody_accent"
        prior = "low"
    elif (adhyaya, pada) == ("1", "3"):
        domain = "grammatical_notation"
        prior = "low"
    else:
        domain = "segmental_phonology/morphophonology" # Broad domain, will be split in semantic pass
        
        # Priors
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
            stem = base[:-1] # Remove virama
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

def annotate_sutra_base(sutra):
    triggers = []
    
    padaccheda = sutra.get('padaccheda', '')
    text = sutra.get('source_text', '') + " " + padaccheda
    
    # 1. Lexical Triggers (Exact word matches mostly, but substring is okay for text)
    lexical_keywords = [
        "आदेश", "लोप", "लुक्", "श्लु", "लुप्", 
        "आगम", "नुम्", "मुट्", "सुक्", "सुग्", "इट्", "टु",
        "दीर्घ", "ह्रस्व", "प्लुत", "गुण", "वृद्धि", "सवर्ण", "सन्धि", "संहिता", "स्वर"
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
            
    # 3. Shape-Condition Detector
    shape_keywords = [
        "अन्त", "उपधा", "आदि", "आत्", "अतः", "इतः", "उतः", "ऋतः", 
        "द्व्यच", "द्व्यच्", "एकाच", "एकाच्", "अनेकाच", "अनेकाच्",
        "वर्ण", "अनुदात्त", "उदात्त"
    ]
    has_shape = False
    for kw in shape_keywords:
        if kw in text:
            triggers.append(f"form-shape-condition:{kw}")
            has_shape = True
            
    # 4. Chapter Priors and Domains
    domain, prior = get_domain_and_prior(sutra['sutra_id'])
    if sutra.get('sutra_type') == 'संज्ञा':
        domain = "terminology"
        
    sutra['candidate_domain'] = domain
    triggers.append(f"prior:{prior}")
    
    # Status Logic (OR-based)
    status = "no"
    
    has_lexical = any(t.startswith("lexical:") for t in triggers)
    has_opaque = "opaque_symbols_detected" in triggers
    
    if has_lexical or has_opaque:
        status = "yes"
    elif prior == "high":
        status = "maybe"
        
    if has_shape and status == "no":
        status = "maybe"
        
    if sutra.get('sutra_type') == 'विधि':
        triggers.append("type:vidhi")
        if status == "no":
            status = "maybe"
            
    if domain in ["prosody_accent", "grammatical_notation"]:
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
        
    print(f"Annotation v3 Complete. Total: {len(annotated)}")
    print(f"Yes: {stats['yes']}, Maybe: {stats['maybe']}, No: {stats['no']}")
    
    # Stratified Audit Sample Generation
    yes_sample = random.sample([s for s in annotated if s['phonology_candidate']['status'] == 'yes'], min(100, stats['yes']))
    maybe_sample = random.sample([s for s in annotated if s['phonology_candidate']['status'] == 'maybe'], min(100, stats['maybe']))
    no_sample = random.sample([s for s in annotated if s['phonology_candidate']['status'] == 'no'], min(100, stats['no']))
    
    audit_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/stratified_audit_sample_v3.yaml'))
    with open(audit_file, 'w', encoding='utf-8') as f:
        yaml.dump({'YES_SAMPLE': yes_sample, 'MAYBE_SAMPLE': maybe_sample, 'NO_SAMPLE': no_sample}, f, allow_unicode=True, sort_keys=False)
        
    print(f"New stratified audit samples generated at {audit_file}")

if __name__ == '__main__':
    main()
