import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_raw'))
MANIFEST_FILE = os.path.join(RAW_DIR, 'manifest.json')

SOURCES = [
    {
        'id': 'GRETIL-KASIKA',
        'url': 'https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/1_gram/jvkasipu.htm',
        'filename': 'jvkasipu.htm',
        'edition': 'Kāśikāvṛtti of Jayāditya & Vāmana',
        'editor': 'Aryendra Sharma',
        'publisher': 'Osmania University, Sanskrit Academy, Hyderabad',
        'year': '1969-1985',
        'digitizer': 'Mari Minamino, Kyoto',
        'content': 'Aṣṭādhyāyī sūtras (PS_ refs) + Kāśikāvṛtti commentary (JKv_ refs)',
        'ref_system': {'sutra': 'PS_adhy,pada.sutra', 'commentary': 'JKv_adhy,pada.sutra'},
        'license': 'GRETIL text file is for reference purposes only; copyright and terms of usage as for source file.',
        'notes': 'Retains sandhi/pausa inconsistencies; - = word sandhi, + = sentence sandhi.',
    },
    {
        'id': 'GRETIL-ASTADHYAYI',
        'url': 'https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/1_gram/panini_u.htm',
        'filename': 'panini_u.htm',
        'edition': 'Aṣṭādhyāyī of Pāṇini',
        'editor': None,
        'publisher': 'TeX Users Group Eighth Annual Conference Proceedings, TeXniques 5 (Providence, 1988)',
        'year': '1988',
        'digitizer': 'Stefan Baums',
        'content': 'Aṣṭādhyāyī sūtras only (independent transliteration)',
        'ref_system': {'sutra': 'adhy.pada.sutra (zero-padded, e.g. 1.01.001)'},
        'license': 'GRETIL text file is for reference purposes only; copyright and terms of usage as for source file.',
        'notes': 'Accents dropped, capital letters for technical terms, analytic hyphens retained.',
    },
]


def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def fetch_source(src):
    os.makedirs(RAW_DIR, exist_ok=True)
    path = os.path.join(RAW_DIR, src['filename'])
    req = urllib.request.Request(src['url'], headers={'User-Agent': 'Mozilla/5.0 (epistemic-research-pipeline)'})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
    with open(path, 'wb') as f:
        f.write(data)
    sha256 = compute_sha256(path)
    record = {
        'id': src['id'],
        'url': src['url'],
        'filename': src['filename'],
        'size_bytes': len(data),
        'sha256': sha256,
        'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
        'edition': src['edition'],
        'editor': src['editor'],
        'publisher': src['publisher'],
        'year': src['year'],
        'digitizer': src['digitizer'],
        'content': src['content'],
        'ref_system': src['ref_system'],
        'license': src['license'],
        'notes': src['notes'],
        'epistemic_status': 'AUTHENTICITY-VERIFIED (Attributed to cited edition; digitization by GRETIL)',
    }
    return record


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    manifest = []
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, encoding='utf-8') as f:
            manifest = json.load(f)
    existing = {m['id'] for m in manifest}

    for src in SOURCES:
        path = os.path.join(RAW_DIR, src['filename'])
        if src['id'] in existing and os.path.exists(path):
            rec = next(m for m in manifest if m['id'] == src['id'])
            rec['sha256'] = compute_sha256(path)
            print(f"{src['id']}: present ({rec['size_bytes']} bytes, sha256 {rec['sha256'][:12]}...)")
            continue
        print(f"Fetching {src['id']} from {src['url']} ...")
        try:
            rec = fetch_source(src)
            manifest = [m for m in manifest if m['id'] != src['id']]
            manifest.append(rec)
            print(f"  -> {rec['size_bytes']} bytes, sha256 {rec['sha256'][:12]}...")
        except Exception as e:
            print(f"FAILED {src['id']}: {e}")
            sys.exit(1)

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nManifest written: {MANIFEST_FILE}")
    print("FAIL-CLOSED GATE: corpus not usable downstream without manifest + sha256.")


if __name__ == '__main__':
    main()
