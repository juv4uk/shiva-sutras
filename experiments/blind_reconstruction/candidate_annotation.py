import os
import re
import yaml
import random

def get_chapter_prior(sutra_id):
    parts = sutra_id.split('.')
    if len(parts) < 2: return "low"
    adhyaya = parts[0]
    pada = parts[1]
    
    high_priors = [
        ("6", "1"), ("6", "4"),
        ("7", "1"), ("7", "2"), ("7", "3"), ("7", "4"),
        ("8", "2"), ("8", "3"), ("8", "4")
    ]
    if (adhyaya, pada) in high_priors:
        return "high"
    if (adhyaya, pada) == ("1", "1"):
        return "medium"
    return "low"

def detect_opaque_classes(text):
    opaque_bases = [
        "अच्", "अल्", "हल्", "इक्", "यण्", "एच्", "एङ्", "ऐच्", "अक्", "उक्", "अण्", "अश्",
        "हस्", "हश्", "यञ्", "झल्", "झर्", "खर्", "शर्", "जश्", "भश्", "वल्", "रल्", "मय्",
        "ञम्", "चय्", "यर्"
    ]
    
    found = []
    # Devanagari text processing
    words = re.findall(r'\b[^\s\d/।]+\b', text)
    
    for base in opaque_bases:
        # Base form
        if base in text: # simple substring since sandhi might attach it
            found.append({'class': base, 'case': 'unknown'})
            
    return found

def annotate_sutra(sutra):
    triggers = []
    
    text = (sutra.get('source_text', '') + " " + sutra.get('padaccheda', ''))
    
    # 1. Lexical Triggers (Devanagari)
    lexical_keywords = [
        "आदेश", "लोप", "लुक्", "श्लु", "लुप्", 
        "आगम", "नुम्", "मुट्", "सुक्", "सुग्", "इट्", "टु",
        "दीर्घ", "ह्रस्व", "प्लुत", "गुण", "वृद्धि", "सवर्ण", "सन्धि", "संहिता", "स्वर"
    ]
    
    for kw in lexical_keywords:
        if kw in text:
            triggers.append(f"lexical:{kw}")
            
    # 2. Opaque Symbol Detection
    opaque_classes = detect_opaque_classes(text)
    roles = {}
    if opaque_classes:
        triggers.append("opaque_symbols_detected")
        for oc in opaque_classes:
            c = oc['class']
            case = oc['case']
            if case == 'base': roles[c] = 'replacement/target'
            elif case == 'locative': roles[c] = 'right_context'
            elif case == 'genitive/ablative': roles[c] = 'target/left_context'
            
    # 3. Chapter Priors
    prior = get_chapter_prior(sutra['sutra_id'])
    triggers.append(f"prior:{prior}")
    
    # Status Logic (OR-based)
    status = "no"
    
    has_lexical = any(t.startswith("lexical:") for t in triggers)
    has_opaque = "opaque_symbols_detected" in triggers
    
    if has_lexical or has_opaque:
        status = "yes"
    elif prior == "high":
        status = "maybe"
        
    # Additional trigger: if sutra type is vidhi
    if sutra.get('sutra_type') == 'विधि':
        triggers.append("type:vidhi")
        if status == "no":
            status = "maybe" # Just in case it's phonological
            
    # Create the output
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
    stats = {'yes': 0, 'maybe': 0, 'no': 0}
    
    for s in sutras:
        ann = annotate_sutra(s)
        stats[ann['phonology_candidate']['status']] += 1
        annotated.append(ann)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(annotated, f, allow_unicode=True, sort_keys=False)
        
    print(f"Annotation Complete. Total: {len(annotated)}")
    print(f"Yes: {stats['yes']}, Maybe: {stats['maybe']}, No: {stats['no']}")
    
    # Stratified Audit Sample Generation
    yes_sample = random.sample([s for s in annotated if s['phonology_candidate']['status'] == 'yes'], min(100, stats['yes']))
    maybe_sample = random.sample([s for s in annotated if s['phonology_candidate']['status'] == 'maybe'], min(100, stats['maybe']))
    no_sample = random.sample([s for s in annotated if s['phonology_candidate']['status'] == 'no'], min(100, stats['no']))
    
    audit_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/stratified_audit_sample.yaml'))
    with open(audit_file, 'w', encoding='utf-8') as f:
        yaml.dump({'YES_SAMPLE': yes_sample, 'MAYBE_SAMPLE': maybe_sample, 'NO_SAMPLE': no_sample}, f, allow_unicode=True, sort_keys=False)
        
    print(f"Stratified audit samples generated at {audit_file}")

if __name__ == '__main__':
    main()
