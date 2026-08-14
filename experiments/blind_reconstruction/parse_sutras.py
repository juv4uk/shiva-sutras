import os
import re
import yaml

def main():
    base_dir = os.path.dirname(__file__)
    html_file = os.path.join(base_dir, 'raw_ashtadhyayi.html')
    out_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/raw-sutras.yaml'))
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Extract tbody
    tbody_match = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL | re.IGNORECASE)
    if not tbody_match:
        print("Could not find tbody")
        return
        
    tbody = tbody_match.group(1)
    
    # Extract all trs
    trs = re.findall(r'<tr>(.*?)</tr>', tbody, re.DOTALL | re.IGNORECASE)
    
    sutras = []
    
    for tr in trs:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL | re.IGNORECASE)
        if len(tds) >= 10:
            sutra_krama = tds[0].strip()
            # sutra_krama format: 11001 -> 1.1.1
            # padding to 5 chars: 1, 1, 001
            if len(sutra_krama) == 5:
                adhyaya = sutra_krama[0]
                pada = sutra_krama[1]
                sutra_num = str(int(sutra_krama[2:]))
                sutra_id = f"{adhyaya}.{pada}.{sutra_num}"
            else:
                sutra_id = sutra_krama
                
            sutra_type = tds[3].strip()
            term = tds[4].strip()
            
            # Text is in tds[8]
            text = re.sub(r'<[^>]+>', '', tds[8]).strip()
            # Padaccheda is in tds[9]
            padaccheda = re.sub(r'<[^>]+>', '', tds[9]).strip()
            
            sutra = {
                'sutra_id': sutra_id,
                'source_text': text,
                'padaccheda': padaccheda,
                'sutra_type': sutra_type,
                'term': term
            }
            sutras.append(sutra)
            
    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(sutras, f, allow_unicode=True, sort_keys=False)
        
    print(f"Parsed {len(sutras)} sutras to {out_file}")

if __name__ == '__main__':
    main()
