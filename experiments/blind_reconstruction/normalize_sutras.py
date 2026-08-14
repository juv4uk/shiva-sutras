import os
import yaml

def main():
    base_dir = os.path.dirname(__file__)
    raw_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/raw-sutras.yaml'))
    norm_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/normalized-sutras.yaml'))
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_sutras = yaml.safe_load(f)
        
    normalized = []
    
    for r in raw_sutras:
        stype = r.get('sutra_type', '')
        
        domain = "unknown"
        if stype == "संज्ञा":
            domain = "terminology"
        elif stype == "परिभाषा":
            domain = "metarule"
        elif stype == "अधिकार":
            domain = "heading"
        elif stype == "विधि":
            domain = "operation"
            
        n = {
            'sutra_id': r['sutra_id'],
            'source_text': r['source_text'],
            'padaccheda': r['padaccheda'],
            'source_url_or_id': 'sanskritdocuments-sutrapāṭha',
            'source_layer': 'sutrapāṭha_raw',
            'candidate_domain': domain,
            'phonology': 'unknown',
            'reason': '',
            'status': 'RAW'
        }
        normalized.append(n)
        
    with open(norm_file, 'w', encoding='utf-8') as f:
        yaml.dump(normalized, f, allow_unicode=True, sort_keys=False)
        
    print(f"Normalized {len(normalized)} sutras to {norm_file}")

if __name__ == '__main__':
    main()
