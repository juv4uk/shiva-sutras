# Stress Test: 10 dhātus × 3 forms

**Date:** 2026-09-07
**Machine version:** post-jhi-fix (commits `4210358`–`30f8041`)
**Previous score:** 27/27 (100%) on 3 dhātus (pac, bhU, tud)

## Method

Extended from 3 dhātus (classes 1, 6) to 10 dhātus across 4 classes (1, 4, 6, 10). Tested 3 forms each (3rd sg, 3rd pl, 1st sg) = 30 forms total.

## Results

**Score: 14/27 tested (51.9%)** — down from 100% at narrow scope.

### Per-dhātu breakdown

| dhātu | Class | 3rd sg | 3rd pl | 1st sg | Score |
|:---|:---|:---|:---|:---|:---|
| bhU | 1 | bhavati ✓ | bhavanti ✓ | bhavāmi ✓ | 3/3 |
| pac | 6 | pacati ✓ | pacanti ✓ | pacāmi ✓ | 3/3 |
| tud | 6 | tudati ✓ | tudanti ✓ | tudāmi ✓ | 3/3 |
| kfuS | 6 | kfuSati ✓ | kfuSanti ✓ | kfuSAmi ✓ | 3/3 |
| paS | 4 | paSyati ✓ | paSyanti ✓ | paSyami ✗ | 2/3 |
| gam | 1 | gamati ✗ | gamanti ✗ | gamAmi ✗ | 0/3 |
| stu | 6 | stuati ✗ | stuanti ✗ | stuAmi ✗ | 0/3 |
| driz | 4 | dfzyati ✗ | dfzyanti ✗ | dfzyami ✗ | 0/3 |
| cur | 10 | curiti ✗ | curinti ✗ | curimi ✗ | 0/3 |

## Failure categories

### 1. VRDDHI_SCOPE (1 form: paS 1st sg)

**Issue:** Vṛddhi (a→ā) only triggers when `vikaraṇa == [a]` (exact list match). Class 4 (Śya) has vikaraṇa `[s, y, a]` — the final 'a' should get vṛddhi too.

**Fix:** Check if vikaraṇa *ends in* 'a', not if it *is* 'a'.

**Difficulty:** Easy — 1 line change.

### 2. GUṆA_SCOPE (3 forms: stu)

**Issue:** Guṇa currently only applies to long vowels (U, I, F, X). Short vowels (u, i, f, x) should also get guṇa when the dhātu ends in a vowel and vikaraṇa is sārvadhātuka.

stu (class 6) should be: stu + a + ti → guṇa u→o → stoati → eco → stavati. But actual expected form is "stauti" — this may require further investigation of whether stu is truly class 6.

**Difficulty:** Medium — requires confirming whether guṇa applies to class 6 for vowel-final roots.

### 3. VIKARAṆA_WRONG (3 forms: cur, class 10)

**Issue:** Class 10 (Ṇic) vikaraṇa is encoded as `N+i+c → i`. But class 10 surface forms use "aya" (e.g., corayati = cur + aya + ti). The Ṇic suffix undergoes guṇa/vṛddhi expansion: i → aya.

**Fix:** Class 10 vikaraṇa should be "aya" after expansion, not "i".

**Difficulty:** Medium — requires special vikaraṇa expansion rule for Ṇic.

### 4. ENCODING (3 forms: driz)

**Issue:** SLP1 encoding error in test data. "driz" is not valid SLP1 — the correct form is "dRz" (d + ṛ + ś). R = ṛ (short vocalic R), z = ś.

**Fix:** Use correct SLP1: dRz.

**Difficulty:** Trivial — data fix.

### 5. IRREGULAR_STEM (3 forms: gam)

**Issue:** gam → gacch before vowel. This is not a regular sandhi rule but a dhātu-specific stem alternation (7.3.77 + special rules). The machine produces "gamati" instead of "gacchati".

**Fix:** Requires a dhātu-specific lookup table for irregular stems. Not a general rule.

**Difficulty:** Hard — requires exception dictionary, not a systematic rule.

## Honest assessment

The machine is **not general-purpose**. It achieves 100% on the narrow test set (3 regular dhātus in classes 1 and 6) but drops to ~52% when extended to 4 classes and irregular roots.

### What works (14/27)
- Classes 1 and 6 with regular consonant-final roots (pac, tud, kfuS, bhU)
- jhi → nti ādeśa (8.4.62)
- vṛddhi for 1st person (7.3.101) — but only when vikaraṇa is exactly [a]
- guṇa for long vowels (U→o, I→e)
- eco sandhi (o→av before vowel)
- it-lopa (hal antyam + ñiṭ)

### What doesn't work (13/27)
- Vṛddhi for non-[a] vikaraṇas (class 4 Śya)
- Guṇa for short vowels (u, i, f, x) in vowel-final roots
- Class 10 (Ṇic) vikaraṇa expansion (i → aya)
- SLP1 encoding errors in test data
- Irregular stem formation (gam → gacch)

## Roadmap

1. **Easy wins (4 forms):** Fix vṛddhi scope + SLP1 encoding → 18/27 (66.7%)
2. **Medium wins (6 forms):** Fix Ṇic vikaraṇa + guṇa short vowels → 24/27 (88.9%)
3. **Hard (3 forms):** Irregular stem dictionary → 27/27 (100%)

## Epistemic note

This stress test does NOT weaken L-001-005 (computational coherence). The claim was SUPPORTED, not PROVED, and explicitly noted "4 gaps" and "covers only laṭ parasmaipada/ātmanepada." The stress test reveals additional gaps at scale — this is expected and honest. The claim's limitations section already stated: "covers only laṭ, not full Aṣṭādhyāyī."

What the stress test DOES show: the machine's core pipeline (pratyāhāra resolution → it-lopa → ādeśa → guṇa → vṛddhi → eco → concat) is sound for regular roots. The gaps are in scope (which vowels trigger guṇa), data (SLP1 encoding), and exceptions (irregular stems) — not in the fundamental architecture.
