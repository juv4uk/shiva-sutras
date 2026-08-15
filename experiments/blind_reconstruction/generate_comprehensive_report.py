import os
import yaml
from collections import defaultdict

def generate_report():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(base_dir, '../../ksetra/astadhyayi/blind/semantic_batch_1'))
    reports_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\09507e3f-a04d-486e-ae1f-f594c1b203bd"
    
    files = [
        'validation_wave_1_10_sutras.yaml',
        'validation_wave_2a_real.yaml',
        'validation_wave_2B.yaml',
        'validation_wave_2C.yaml',
        'validation_wave_2D.yaml'
    ]
    
    stats = {
        'status': defaultdict(int),
        'reasons': defaultdict(int),
        'pipeline_vs_evidence': {'UNRESOLVED-BY-PIPELINE': 0, 'UNRESOLVED-BY-EVIDENCE': 0},
        'sound_set': defaultdict(int),
        'cross_tab': defaultdict(lambda: {'RESOLVED': 0, 'REVIEWED': 0, 'PROPOSED': 0})
    }
    
    total_processed = 0
    
    for fname in files:
        fpath = os.path.join(data_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, 'r', encoding='utf-8') as f:
            records = yaml.safe_load(f)
            
        for rc_full in records:
            rc = rc_full['rule_context']
            total_processed += 1
            
            # 1. Status
            status = rc['operation'].get('workflow_status', 'PROPOSED').upper()
            stats['status'][status] += 1
            
            # 2 & 3. Reasons and Pipeline vs Evidence
            if status == 'REVIEWED':
                uqs = rc.get('unresolved_questions', [])
                if not uqs:
                    uqs = ['missing_operand_evidence'] # fallback
                    
                is_pipeline = False
                for q in uqs:
                    if 'pending_manual_validation' in q or 'Demoted' in q or 'missing' in q:
                        is_pipeline = True
                        stats['reasons']['missing_operand_evidence'] += 1
                    elif 'ambiguous_anuvrtti' in q:
                        stats['reasons']['ambiguous_anuvrtti'] += 1
                    elif 'ambiguous_semantic_role' in q:
                        stats['reasons']['ambiguous_semantic_role'] += 1
                    else:
                        stats['reasons']['missing_operand_evidence'] += 1
                        is_pipeline = True
                        
                if is_pipeline or any('UNKNOWN' in rc['operation'].get('type', '')) or not rc.get('claims'):
                    stats['pipeline_vs_evidence']['UNRESOLVED-BY-PIPELINE'] += 1
                else:
                    stats['pipeline_vs_evidence']['UNRESOLVED-BY-EVIDENCE'] += 1
                    
            # 4. Sound Set
            ssr = rc.get('sound_set_relevance', {}).get('status', 'UNRESOLVED')
            stats['sound_set'][ssr] += 1
            
            # 5. Cross-tabulation
            op_type = rc['operation'].get('type', 'UNKNOWN')
            
            # simplify operation types
            display_type = 'unknown'
            if 'substitution' in op_type: display_type = 'substitution'
            elif 'lopa' in op_type or 'elision' in op_type: display_type = 'lopa'
            elif 'agama' in op_type or 'augment' in op_type: display_type = 'agama'
            elif 'metalinguistic' in op_type: display_type = 'metalinguistic'
            elif 'prosody' in op_type: display_type = 'prosody'
            else:
                # check if anuvrtti-heavy or shape-conditioned based on operands
                if 'unresolved_operand' in str(rc): display_type = 'anuvrtti-heavy'
                else: display_type = 'shape-conditioned/other'
                
            stats['cross_tab'][display_type][status] += 1

    # Generate Markdown Report
    report = f"""# Batch-1 Comprehensive Epistemic Report (50 Sutras)

## 1. Загальний Статус (Status Distribution)
- **RESOLVED**: {stats['status']['RESOLVED']}
- **REVIEWED**: {stats['status']['REVIEWED']}
- **PROPOSED**: {stats['status']['PROPOSED']}

## 2. Природа Невідомості (Pipeline vs Evidence)
Серед {stats['status']['REVIEWED']} REVIEWED записів:
- **UNRESOLVED-BY-PIPELINE**: {stats['pipeline_vs_evidence']['UNRESOLVED-BY-PIPELINE']}
  *(Автоматика не змогла надійно розпізнати ролі / бракувало локаторів)*
- **UNRESOLVED-BY-EVIDENCE**: {stats['pipeline_vs_evidence']['UNRESOLVED-BY-EVIDENCE']}
  *(Саме джерело містить об'єктивну багатозначність, яка блокує валідатор)*

## 3. Детальний розподіл причин (Reason Breakdown)
- `missing_operand_evidence` / Validator Demotions: {stats['reasons']['missing_operand_evidence']}
- `ambiguous_anuvrtti`: {stats['reasons']['ambiguous_anuvrtti']}
- `ambiguous_semantic_role`: {stats['reasons']['ambiguous_semantic_role']}

## 4. Оцінка релевантності звукових множин (Sound Set Relevance)
- **CANDIDATE**: {stats['sound_set'].get('CANDIDATE', 0)}
- **NO_EVIDENCE**: {stats['sound_set'].get('NO_EVIDENCE', 0)}
- **UNRESOLVED**: {stats['sound_set'].get('UNRESOLVED', 0)}

## 5. Перехресна таблиця: Operation Type vs Status

| Тип Операції (Operation Type) | RESOLVED | REVIEWED | PROPOSED |
|-------------------------------|----------|----------|----------|
"""
    for op, counts in sorted(stats['cross_tab'].items()):
        report += f"| {op.ljust(29)} | {str(counts['RESOLVED']).ljust(8)} | {str(counts['REVIEWED']).ljust(8)} | {str(counts['PROPOSED']).ljust(8)} |\n"
        
    report += """
> [!NOTE]
> Записи залишені у своєму $B_1^{automatic}$ стані. Будь-яка ручна експертиза в майбутньому (Manual Adjudication) дозволить виміряти **Expert Gain** — здатність людини переводити UNRESOLVED-BY-PIPELINE та UNRESOLVED-BY-EVIDENCE у RESOLVED.
"""

    with open(os.path.join(reports_dir, 'batch_1_epistemic_report.md'), 'w', encoding='utf-8') as f:
        f.write(report)
        
    print("Report generated successfully.")

if __name__ == '__main__':
    generate_report()
