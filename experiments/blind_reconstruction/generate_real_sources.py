import hashlib
import json
import os
import sys
import yaml
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KASIKA_FILE = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_kasika_corpus.json'))
MANIFEST_FILE = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_raw/manifest.json'))
REFERENCED_FILE = os.path.abspath(os.path.join(BASE_DIR, 'referenced_sutra_ids.json'))
SOURCES_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../ksetra/astadhyayi/sources'))
REPORT_FILE = os.path.join(os.path.join(BASE_DIR, 'reports'), 'real_source_generation.md')


def main():
    with open(KASIKA_FILE, encoding='utf-8') as f:
        corpus = json.load(f)
    with open(MANIFEST_FILE, encoding='utf-8') as f:
        manifest = json.load(f)
    with open(REFERENCED_FILE, encoding='utf-8') as f:
        referenced = json.load(f)

    kasika_manifest = next(m for m in manifest if m['id'] == 'GRETIL-KASIKA')
    raw_file = os.path.join(os.path.dirname(MANIFEST_FILE), kasika_manifest['filename'])

    os.makedirs(SOURCES_DIR, exist_ok=True)

    generated = []
    missing = []

    for sid in referenced:
        rec = corpus.get(sid)
        if not rec:
            missing.append(sid)
            continue

        record_id = f"KASIKA-{sid}"
        source_data = {
            'source_id': record_id,
            'locator': {'sutra': sid},
            'witness_text': {
                'sutra': rec['sutra'],
                'commentary': rec['commentary'],
            },
            'integrity': {
                'reproducible': True,
                'source_file': os.path.basename(raw_file),
                'source_file_sha256': kasika_manifest['sha256'],
                'source_file_size_bytes': kasika_manifest['size_bytes'],
            },
            'provenance': {
                'authenticity': 'AUTHENTICITY-VERIFIED (Attributed)',
                'status': 'REAL',
                'witness': 'GRETIL-KASIKA',
                'external_source': kasika_manifest['url'],
                'edition': kasika_manifest['edition'],
                'editor': kasika_manifest['editor'],
                'publisher': kasika_manifest['publisher'],
                'year': kasika_manifest['year'],
                'digitizer': kasika_manifest['digitizer'],
                'retrieved_at_utc': kasika_manifest['retrieved_at_utc'],
                'license': kasika_manifest['license'],
                'notes': 'Text extracted from GRETIL Kāśikāvṛtti; authenticity is attributed via the cited academic edition, not proven by reproduction.',
            },
        }

        with open(os.path.join(SOURCES_DIR, f'{record_id}.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(source_data, f, allow_unicode=True, sort_keys=False)
        generated.append(sid)

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('# Real Source Generation Report\n\n')
        f.write(f'- Referenced sūtras: {len(referenced)}\n')
        f.write(f'- Generated: {len(generated)} real source files from GRETIL Kāśikāvṛtti.\n')
        f.write(f'- Missing from corpus: {len(missing)}\n')
        f.write(f'- Source file (raw): {os.path.basename(raw_file)}\n')
        f.write(f'- Raw SHA-256: {kasika_manifest["sha256"]}\n')
        f.write(f'- Edition: {kasika_manifest["edition"]} ({kasika_manifest["editor"]}, {kasika_manifest["year"]})\n')
        f.write(f'- Epistemic status: AUTHENTICITY-VERIFIED (Attributed)\n\n')
        if missing:
            f.write('## Missing (absent from Sharma Kāśikā edition)\n\n')
            f.write('These sūtras are referenced in the blind pipeline but absent from the GRETIL Sharma Kāśikā edition. They are NOT assigned REAL status until a second witness provides them.\n\n')
            for sid in missing:
                f.write(f'- {sid}\n')

    print(f"Generated {len(generated)} real source files; {len(missing)} missing.")


if __name__ == '__main__':
    main()
