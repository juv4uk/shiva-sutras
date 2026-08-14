import urllib.request
import os

def main():
    url = "https://sanskritdocuments.org/learning_tools/ashtadhyayi/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        base_dir = os.path.dirname(__file__)
        out_file = os.path.join(base_dir, 'raw_ashtadhyayi.html')
        
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"Downloaded {len(html)} characters to {out_file}")
    except Exception as e:
        print(f"Error fetching: {e}")

if __name__ == '__main__':
    main()
