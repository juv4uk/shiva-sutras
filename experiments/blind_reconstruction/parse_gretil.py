import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_raw'))
OUT_KASIKA = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_kasika_corpus.json'))
OUT_ASTADHYAYI = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_astadhyayi.json'))


def norm_sid(adhy, pada, sutra):
    return f"{int(adhy)}.{int(pada)}.{int(sutra)}"


def parse_kasika(raw):
    """Parse jvkasipu.htm -> {sid: {'sutra': str, 'commentary': str}}"""
    starts = list(re.finditer(r'_____START JKv_(\d+),(\d+)\.(\d+):', raw))
    records = {}
    for i, m in enumerate(starts):
        sid = norm_sid(m.group(1), m.group(2), m.group(3))
        end = starts[i + 1].start() if i + 1 < len(starts) else len(raw)
        block = raw[m.end():end]
        cut = block.find('<b>')
        if cut != -1:
            block = block[:cut]
        block = block.replace('<BR>', '\n').replace('<br>', '\n')
        block = re.sub(r'<[^>]+>', '', block)
        lines = []
        for ln in block.split('\n'):
            ln = ln.strip()
            if not ln or set(ln) <= {'_'}:
                continue
            lines.append(ln)
        commentary = ' '.join(lines)

        pre = raw[max(0, m.start() - 400):m.start()]
        h = re.findall(r'<b>(.*?)</b>\s*\|\|\s*PS_(\d+),(\d+)\.(\d+)\s*\|', pre)
        sutra_text = h[-1][0] if h else ''
        records[sid] = {'sutra': sutra_text, 'commentary': commentary}
    return records


def parse_astadhyayi(raw):
    """Parse panini_u.htm -> {sid: {'sutra': str}}"""
    records = {}
    pat = re.compile(r'^(\d+)\.(\d+)\.(\d+)\s+(.*?)(<BR>)?$')
    for line in raw.splitlines():
        t = line.strip()
        m = pat.match(t)
        if not m:
            continue
        sid = norm_sid(m.group(1), m.group(2), m.group(3))
        text = m.group(4).strip()
        if sid in records:
            continue  # keep first occurrence on duplicates
        records[sid] = {'sutra': text}
    return records


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    kasika_path = os.path.join(RAW_DIR, 'jvkasipu.htm')
    asta_path = os.path.join(RAW_DIR, 'panini_u.htm')

    with open(kasika_path, encoding='utf-8') as f:
        kasika_records = parse_kasika(f.read())
    with open(asta_path, encoding='utf-8') as f:
        asta_records = parse_astadhyayi(f.read())

    with open(OUT_KASIKA, 'w', encoding='utf-8') as f:
        json.dump(kasika_records, f, ensure_ascii=False, indent=1, sort_keys=True)
    with open(OUT_ASTADHYAYI, 'w', encoding='utf-8') as f:
        json.dump(asta_records, f, ensure_ascii=False, indent=1, sort_keys=True)

    print(f"Kāśikā: {len(kasika_records)} records -> {OUT_KASIKA}")
    print(f"Aṣṭādhyāyī (Baums): {len(asta_records)} records -> {OUT_ASTADHYAYI}")
    missing_comm = sum(1 for v in kasika_records.values() if not v['commentary'])
    missing_sutra = sum(1 for v in kasika_records.values() if not v['sutra'])
    print(f"Kāśikā records missing commentary: {missing_comm}, missing sutra text: {missing_sutra}")


if __name__ == '__main__':
    main()
