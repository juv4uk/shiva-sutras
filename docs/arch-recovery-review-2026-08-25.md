# Architecture Recovery Review — shiva-sutras

**Дата:** 2026-08-25 · **Автор:** Vyasa (COMPILER STEWARD)
**Тип:** read-only recovery review · **Задача:** ARCH-RECOVERY-REVIEW-SIVA
**Ресурси:** читання; жодних масових прогонів (resource policy)

---

## 1. As-built шари (директива власника про шари дотримана)

```
L1 SOURCE      ksetra/sanskritworld_texts/        (Devanagari оригінали, immutable)
L2 REPRESENT   ksetra/sanskritworld_texts_md/     (147MB похідні MD/IAST)
               ksetra/canon/siva-sutras.yaml      (Immutable Canon v1.0, IAST-only,
                                                   14 сутр / 43 записи / 42 унікальні звуки;
                                                   provenance+witnesses+variants+unresolved
                                                   сусіди в тому ж каталозі)
L3 KNOWLEDGE   Obsidian semantic graph (Валт) + extensions/*.yaml
```

Прототипний пояс (prototype/): пʼять оглянутих 2026-08-24 елементів
(phonetics/oracle/bitmask64/cml_lowering/derivation_ir) + slavic_phonetics,
fpga_alu, upc8 — класифікація A-D у моєму steward review від 2026-08-24.

## 2. Сильне

1. **Канон як окремий immutable артефакт** із provenance-сусідами — рідкісна
   для прототипів дисципліна; саме він врятував аудит масок (еталон знайдено).
2. **License гігієна**: NOTICE-third-party.md + LICENSE-MATRIX екосистеми
   застосовуються до корпусних даних; код прототипів власницький.
3. **Cognates uk-sa golden set**: 18 пар + 2 decoys, owner-approved, VERIFIED,
   embeddings-метрика 12/13 rank-1 — зрілий extension.
4. **Drift-checker історія**: SHIVA-DRIFT-* цикли відпрацювали і закриті в реєстрі.
5. **Сьогоднішній контент**: saṃjñā-kośa словник тегів + 100% семантичне
   покриття corpus-файлів (fc079c3, 338e89a).

## 3. Відкриті фронти / борги

| # | Пріоритет | Що |
|---|---|---|
| 1 | HIGH | phonetics-KB маски ХИБНІ — BLOCKED гейт стоїть (fpga-lisp@ba0fa0b); регенерація програмно: canon → oracle codes → hex; врахувати SLP1-внутрішні ключі оракула та dedup-h (43 записи vs 42 унікальних) |
| 2 | MED | канон README варто дописати: «записи vs унікальні» + чому h повторюється — наступний аудитор спіткнеться саме там |
| 3 | MED | UPC8 design-четвірка (API-SCOPE-NARROWING, NATURAL-CLASS-API-SPLIT, ARCHITECTURE-DECISION, FPGA-BITMAP-EXPERIMENT) — локальні рішення чекають домену; ADR-002 вже є фундаментом |
| 4 | LOW | untracked WIP: docs/VIVEKA-FINDINGS-2026-08-24.md, extensions/{hindi,polish,language-profile-priority}.yaml — авторам варто закомітити або явно кинути |
| 5 | LOW | tasks.my: 11 локальних відкритих, реєстру не суперечать |

## 4. Звірка шарів канон ↔ оракул [VERIFIED сьогодні]

Послідовність звуків збігається позиційно; різниця — РІЗНІ СКРИПТИ
(канон IAST, оракул внутрішньо SLP1: f/x/E/O/Y/J/Q/W...) та
dedup-h (43→42). Жодного конфлікту ПОРЯДКУ не виявлено. Маски KB
проти оракула — окреме підтверджене пошкодження (+8 зсув приголосних
класів, ~8 зайвих записів у таблиці-джерелі KB).

---
*Read-only. Усі числа — з живих файлів сьогодні.*
