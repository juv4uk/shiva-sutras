import os
import yaml
import urllib.request
import re
import time
from datetime import datetime

from real_evidence import load_real_source

def acquire_real_sources():
    base_dir = os.path.dirname(__file__)
    blind_file = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml'))
    sources_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/sources'))
    
    with open(blind_file, 'r', encoding='utf-8') as f:
        expert_sutras = yaml.safe_load(f)
        
    protected = 0
    for item in expert_sutras:
        sid = item['sutra_id']
        parts = sid.split('.')
        if len(parts) != 3:
            continue

        # FAIL CLOSED: never overwrite REAL GRETIL evidence with a scrape.
        if load_real_source(sid) is not None:
            protected += 1
            continue

        url = f"https://ashtadhyayi.com/sutraani/{parts[0]}/{parts[1]}/{parts[2]}"
        print(f"Fetching {sid} from {url}...")
        
        raw_text = ""
        status = "MISSING"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                
                # Try to extract Kasika Vrtti from Ashtadhyayi.com HTML
                # Usually wrapped in divs with 'kasika' in ID or class, or specific tabs
                kasika_match = re.search(r'id="kasika"[^>]*>.*?<div[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
                if not kasika_match:
                    kasika_match = re.search(r'काश्यपिकासहितं काशिकाविवरणम्.*?<div[^>]*>(.*?)</div>', html, re.DOTALL)
                if not kasika_match:
                    kasika_match = re.search(r'class="vritti"[^>]*kasika[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
                    
                if kasika_match:
                    raw_html = kasika_match.group(1)
                    # Strip tags
                    clean_text = re.sub(r'<[^>]+>', ' ', raw_html).strip()
                    clean_text = re.sub(r'\s+', ' ', clean_text)
                    if len(clean_text) > 10:
                        raw_text = clean_text
                        status = "REAL"
                        
                # Fallback: if we couldn't parse the exact Kasika div but got the page, store a marker or raw text snippet
                if status == "MISSING":
                    # We will just mark it as missing if we can't reliably get the text, 
                    # to enforce the epistemic gate.
                    pass
                    
        except Exception as e:
            print(f"Failed to fetch {sid}: {e}")

        if not raw_text:
            print(f"NO authentic text recovered for {sid}; refusing to write placeholder (fail closed).")
            continue
            
        source_data = {
            'source_id': f'KASIKA-{sid}',
            'locator': {'sutra': sid},
            'source_url': url,
            'source_status': status,
            'retrieval': {
                'method': 'web_scraping',
                'retrieved_at': datetime.utcnow().isoformat() + 'Z'
            },
            'raw_text': raw_text,
        }
        
        with open(os.path.join(sources_dir, f'KASIKA-{sid}.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
            
        time.sleep(0.5) # Be gentle to the server
        
    print(f"Real source acquisition (legacy) completed. {protected} REAL sources protected from overwrite.")

if __name__ == '__main__':
    acquire_real_sources()
