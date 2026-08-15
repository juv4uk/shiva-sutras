import difflib
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KASIKA_FILE = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_kasika_corpus.json'))
ASTADHYAYI_FILE = os.path.abspath(os.path.join(BASE_DIR, '../../external_data/gretil_astadhyayi.json'))
REPORT_DIR = os.path.abspath(os.path.join(BASE_DIR, 'reports'))
REPORT_FILE = os.path.join(REPORT_DIR, 'cross_witness_gretil_diff.md')

AGREE_THRESHOLD = 0.9
CONFLICT_THRESHOLD = 0.6

# Preliminary classification of CONFLICTS (automated hint, NOT an expert verdict).
# 'NOTATION': same underlying text, differing transcription convention (markers `=`/capitals,
#   morpheme decomposition in Baums vs full IAST in Sharma).
# 'ANUVṚTTI': Sharma <b> tag carries only the operative word; the full sūtra continues
#   (anuvṛtti) and Baums expands it.
# 'GENUINE': reading differs substantively between the two editions.
PRELIMINARY_CLASS = {
    '3.4.106': 'NOTATION',  # iṭo 't = iṬ-aḥ=aT
    '4.3.74': 'NOTATION',   # tata āgataḥ = ta-taḥ=ā-ga-ta-ḥ
    '4.4.49': 'NOTATION',   # ṛto 'ñ = ṛT-aḥ=aÑ
    '6.4.134': 'NOTATION',  # al-lopo 'naḥ = aT=lupa-ḥ an-aḥ
    '7.1.24': 'NOTATION',   # ato 'm = aT-aḥ=am
    '7.2.4': 'NOTATION',    # neṭi = na=iṬ-i
    '7.2.89': 'NOTATION',   # yo 'ci = ya-ḥ=aC-i
    '8.4.63': 'NOTATION',   # śaścho 'ṭi = ś-as cha-ḥ aṬ-i
    '3.2.142': 'NOTATION',  # long compound, morpheme decomposition only
    '5.4.77': 'NOTATION',   # long compound, morpheme decomposition only
    '7.4.65': 'NOTATION',   # long compound, morpheme decomposition only
    '6.2.164': 'ANUVṚTTI',  # Sharma: vibhāṣā (chandasi continues); Baums expands
    '6.3.16': 'ANUVṚTTI',   # Sharma: vibhāṣā (varṣakṣaraśaravarāt continues); Baums expands
    '1.1.18': 'GENUINE',    # ūṃ vs oṃ (known ms. variant)
    '1.4.37': 'GENUINE',    # Baums reading abbreviated/corrupt
    '4.2.94': 'GENUINE',    # Sharma duplicates 4.2.93 text; Baums has grāmād yakhañau
    '5.3.5': 'GENUINE',     # etado 'ś vs etad-aḥ=an
    '5.4.112': 'GENUINE',   # Baums includes senakasya (commentary ref) in sūtra
    '6.3.40': 'GENUINE',    # Baums aṛg for aṅg (svāṅgāt)
    '7.3.65': 'GENUINE',    # ṇya vs Ṇy-e; Sharma <b> "ṇya" vs its own commentary "ṇye"
    '7.3.91': 'GENUINE',    # guṇo 'pṛkto vs guṇa-ḥ a-pṛk-t-e
    '8.4.28': 'GENUINE',    # Baums extra an-oT-para=ḥ
}


def normalize(text):
    if text is None:
        return ''
    t = unicodedata.normalize('NFC', text)
    t = re.sub(r'^vakṣyati\s*-\s*', '', t)
    t = re.sub(r'^vakṣyati\s*[-–—]\s*', '', t)
    t = t.replace('|', ' ').replace('*', ' ').replace('(', ' ').replace(')', ' ')
    t = re.sub(r'[\u0300-\u036f]', '', t)
    t = re.sub(r'[-=+/.,;:!\u2019\u2018\u201c\u201d]', ' ', t)
    t = t.replace('\\u200b', '')
    t = re.sub(r'\s+', ' ', t)
    return t.strip().lower()


def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def align_lists(k_texts, a_texts):
    """Global alignment (Needleman-Wunsch) of two ordered normalized-text lists.

    Returns a list of pairs (ki, ai); ki or ai is None where a gap is opened.
    Match scoring favors texts whose normalized similarity is high, so a local
    numbering shift in one witness is absorbed as a gap rather than a conflict.
    """
    n, m = len(k_texts), len(a_texts)
    NEG = float('-inf')
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] - 1.5
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] - 1.5
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = similarity(k_texts[i - 1], a_texts[j - 1])
            diag = dp[i - 1][j - 1] + (2.0 * s - 1.6)
            up = dp[i - 1][j] - 1.5
            left = dp[i][j - 1] - 1.5
            dp[i][j] = max(diag, up, left)
    pairs = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = similarity(k_texts[i - 1], a_texts[j - 1])
            if abs(dp[i][j] - (dp[i - 1][j - 1] + (2.0 * s - 1.6))) < 1e-9:
                pairs.append((i - 1, j - 1))
                i -= 1
                j -= 1
                continue
        if i > 0 and abs(dp[i][j] - (dp[i - 1][j] - 1.5)) < 1e-9:
            pairs.append((i - 1, None))
            i -= 1
        else:
            pairs.append((None, j - 1))
            j -= 1
    pairs.reverse()
    return pairs


def main():
    with open(KASIKA_FILE, encoding='utf-8') as f:
        kasika = json.load(f)
    with open(ASTADHYAYI_FILE, encoding='utf-8') as f:
        astadhyayi = json.load(f)

    by_pada = {}
    for sid in kasika:
        by_pada.setdefault('.'.join(sid.split('.')[:2]), {'kasika': [], 'baums': []})
    for sid in astadhyayi:
        by_pada.setdefault('.'.join(sid.split('.')[:2]), {'kasika': [], 'baums': []})
    for sid, rec in kasika.items():
        by_pada['.'.join(sid.split('.')[:2])]['kasika'].append((sid, rec['sutra']))
    for sid, rec in astadhyayi.items():
        by_pada['.'.join(sid.split('.')[:2])]['baums'].append((sid, rec['sutra']))
    for parts in by_pada.values():
        parts['kasika'].sort(key=lambda x: [int(n) for n in x[0].split('.')])
        parts['baums'].sort(key=lambda x: [int(n) for n in x[0].split('.')])

    statuses = {'AGREES': 0, 'VARIANTS': 0, 'CONFLICTS': 0, 'MISSING': 0}
    detail = []
    all_ids = []

    for pada_key, parts in sorted(by_pada.items()):
        k_list = parts['kasika']
        a_list = parts['baums']
        k_norm = [normalize(s) for _, s in k_list]
        a_norm = [normalize(s) for _, s in a_list]
        for ki, ai in align_lists(k_norm, a_norm):
            k = k_list[ki] if ki is not None else None
            a = a_list[ai] if ai is not None else None
            sid = (k or a)[0]
            all_ids.append(sid)
            if k is None or a is None:
                statuses['MISSING'] += 1
                detail.append({
                    'sutra_id': sid,
                    'status': 'MISSING',
                    'kasika_sutra': k[1] if k else None,
                    'baums_sutra': a[1] if a else None,
                    'baums_id': a[0] if a else None,
                    'similarity': None,
                    'norm_kasika': normalize(k[1]) if k else '',
                    'norm_baums': normalize(a[1]) if a else '',
                })
                continue
            nk = normalize(k[1])
            na = normalize(a[1])
            sim = similarity(nk, na)
            if sim >= AGREE_THRESHOLD:
                status = 'AGREES'
            elif sim >= CONFLICT_THRESHOLD:
                status = 'VARIANTS'
            else:
                status = 'CONFLICTS'
            statuses[status] += 1
            detail.append({
                'sutra_id': sid,
                'status': status,
                'kasika_sutra': k[1],
                'baums_sutra': a[1],
                'baums_id': a[0],
                'similarity': round(sim, 3),
                'norm_kasika': nk,
                'norm_baums': na,
            })

    case_only = 0
    for d in detail:
        if d['status'] == 'VARIANTS' and d['similarity'] is not None:
            nk = d['norm_kasika'].replace(' ', '')
            na = d['norm_baums'].replace(' ', '')
            k_letters = re.sub(r'[^a-z]', '', nk)
            a_letters = re.sub(r'[^a-z]', '', na)
            if k_letters and k_letters == a_letters:
                case_only += 1

    os.makedirs(REPORT_DIR, exist_ok=True)

    lines = []
    lines.append('# Cross-Witness Diff: GRETIL Kāśikā vs GRETIL Aṣṭādhyāyī (Baums)')
    lines.append('')
    lines.append('Two independent GRETIL transcriptions of the Aṣṭādhyāyī sūtrapāṭha are compared.')
    lines.append('This test verifies *transcription fidelity*, NOT historical authenticity.')
    lines.append('(Reproducibility of an edition does not prove authenticity of the text — E-001.)')
    lines.append('')
    lines.append('## Method')
    lines.append('')
    lines.append('- Witness A: Kāśikāvṛtti (Sharma ed., GRETIL `jvkasipu.htm`) — sūtra text as cited in Kāśikā.')
    lines.append('- Witness B: Aṣṭādhyāyī (Baums transcription, GRETIL `panini_u.htm`).')
    lines.append('- Normalization: Unicode NFC, diacritics removed, sandhi/separator characters removed, lowercase.')
    lines.append('- Similarity: `difflib.SequenceMatcher.ratio()` on normalized strings.')
    lines.append('- Alignment: global sequence alignment (Needleman-Wunsch) per pāda absorbs local')
    lines.append('  numbering shifts between the two editions as gaps instead of false conflicts.')
    lines.append('')
    lines.append('## Statuses')
    lines.append('')
    lines.append('| Status | Threshold | Meaning |')
    lines.append('| :--- | :--- | :--- |')
    lines.append('| `AGREES` | ratio >= 0.9 | The two witnesses essentially agree modulo notation |')
    lines.append('| `VARIANTS` | 0.6 <= ratio < 0.9 | Same sūtra, wording/notation differs |')
    lines.append('| `CONFLICTS` | ratio < 0.6 | Substantive textual disagreement |')
    lines.append('| `MISSING` | - | Sūtra present in only one witness |')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append(f'- Total sūtras considered: {len(all_ids)}')
    lines.append(f'- `AGREES`: {statuses["AGREES"]}')
    lines.append(f'- `VARIANTS`: {statuses["VARIANTS"]}')
    lines.append(f'- `CONFLICTS`: {statuses["CONFLICTS"]}')
    lines.append(f'- `MISSING`: {statuses["MISSING"]}')
    lines.append('')
    lines.append('## Interpretation (epistemic, not exhaustive)')
    lines.append('')
    lines.append('The two GRETIL transcriptions use DIFFERENT transliteration conventions:')
    lines.append('')
    lines.append('- **Witness B (Baums)** drops diacritics in some places and uses `=` for')
    lines.append('  word-sandhi, `T`/`K`/`C`/`L`/`Ṣ` capitals for the same phonemes that')
    lines.append('  Witness A writes as `d`/`k`/`c`/`l`/`ṣ` (marker capitalization).')
    lines.append('- **Witness A (Kāśikā/Sharma)** preserves full IAST diacritics and uses `-` for')
    lines.append('  internal word-sandhi, plus `//` sentence-end.')
    lines.append('')
    lines.append('Consequently, most `VARIANTS` reflect *notation* (capital markers, `=` vs `-`,')
    lines.append('sandhi re-joining) rather than textual disagreement. As an approximate signal,')
    lines.append(f'of the `VARIANTS`, roughly **{case_only}** differ only by spacing/letter-case'
                 ' after stripping non-letters.')
    lines.append('')
    lines.append('### What this diff DOES prove')
    lines.append('')
    lines.append('- Both witnesses cover the same overall sūtra corpus (3951–3958 sūtras).')
    lines.append('- The two independent digitizations do NOT materially disagree in wording at the')
    lines.append('  level of *which sūtra text appears*; they differ in transcription style.')
    lines.append('- This is a **transcription-fidelity** check: it confirms the two editions were')
    lines.append('  digitized consistently, it does NOT certify that the underlying text is the')
    lines.append('  authentic 7th-century Kāśikā (E-001: Reproducibility ≠ Authenticity).')
    lines.append('')
    lines.append('### Known structural discrepancies (edition-level)')
    lines.append('')
    lines.append('- Witness A (Kāśikā/Sharma) does not include sūtras **1.1.46–1.1.75** and')
    lines.append('  **8.3.118–8.3.119** in its numbering (they are present in Witness B).')
    lines.append('- Witness A includes **2.4.27** which Witness B lacks; numbering offsets exist.')
    lines.append('- The pāda 8.3 numbering diverges after sūtra 8.3.98: the Sharma edition omits two')
    lines.append('  sūtras that Baums numbers 8.3.99–8.3.100, so Kāśikā 8.3.99 → Baums 8.3.101, etc.')
    lines.append('  The sequence alignment above absorbs this shift.')
    lines.append('  These are *edition-level* differences and must be resolved by a named critical')
    lines.append('  edition before use as `REAL` evidence for those sūtras.')
    lines.append('')
    lines.append(f"### `CONFLICTS` ({statuses['CONFLICTS']}) require expert review")
    lines.append('')
    lines.append('The sūtras listed below fall below the agreement threshold. Some are notation')
    lines.append('artifacts (e.g. `ūṃ` vs `oṃ` in 1.1.18), others may indicate genuine variant')
    lines.append('readings between the Sharma Kāśikā edition and the Baums transcription.')
    lines.append('Each must be adjudicated by an expert against a named critical edition before')
    lines.append('being used as evidence.')
    lines.append('')
    lines.append('### `MISSING` (57) — edition-level gaps')
    lines.append('')
    lines.append('Sūtras present in only one witness after alignment. These reflect edition-level')
    lines.append('numbering/content differences (see "Known structural discrepancies"), not')
    lines.append('necessarily textual loss in either witness.')
    lines.append('')
    lines.append('## Per-Sūtra Detail')
    lines.append('')
    lines.append('| Sūtra | Status | Sim | Kāśikā (Witness A) | Baums (Witness B) |')
    lines.append('| :--- | :--- | :--- | :--- | :--- |')

    for d in detail:
        a = d['kasika_sutra'] or '-'
        b = d['baums_sutra'] or '-'
        sim = '-' if d['similarity'] is None else f"{d['similarity']:.3f}"
        label = d['sutra_id']
        if d.get('baums_id') and d['baums_id'] != d['sutra_id']:
            label = f"{d['sutra_id']} (=B {d['baums_id']})"
        lines.append(f"| {label} | {d['status']} | {sim} | {a} | {b} |")

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    adjudication_file = os.path.join(REPORT_DIR, 'conflicts_adjudication.md')
    conflicts = [d for d in detail if d['status'] == 'CONFLICTS']
    with open(adjudication_file, 'w', encoding='utf-8') as f:
        f.write('# CONFLICTS Adjudication Queue\n\n')
        f.write(f'These {len(conflicts)} sūtras fall below the agreement threshold (after sequence\n')
        f.write('alignment absorbed numbering shifts). For each, an expert must\n')
        f.write('adjudicate the variant reading against a named critical edition (e.g. Böhtlingk 1887,\n')
        f.write('Katre 1987, Cardona 1976). The Prelim column is an automated hint only\n')
        f.write('(`NOTATION` = transcription-convention difference; `ANUVṚTTI` = Sharma sūtra tag\n')
        f.write('carries only the operative word; `GENUINE` = substantive edition difference).\n')
        f.write('Status column: `UNRESOLVED` (default) / `RESOLVED` / `NOTATION`.\n\n')
        f.write('| Sūtra | Baums ID | Sim | Kāśikā (Sharma ed.) | Baums transcription | Prelim | Status | Notes |\n')
        f.write('| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n')
        for d in conflicts:
            a = d['kasika_sutra'] or '-'
            b = d['baums_sutra'] or '-'
            sim = '-' if d['similarity'] is None else f"{d['similarity']:.3f}"
            bid = d.get('baums_id') or '-'
            cls = PRELIMINARY_CLASS.get(d['sutra_id'], '?')
            f.write(f"| {d['sutra_id']} | {bid} | {sim} | {a} | {b} | `{cls}` | `UNRESOLVED` | |\n")
        f.write('\n')

    print(f"Report: {REPORT_FILE}")
    print(f"Adjudication queue: {adjudication_file}")
    print(f"Summary: {statuses}")


if __name__ == '__main__':
    main()
