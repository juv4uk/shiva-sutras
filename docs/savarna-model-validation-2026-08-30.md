# SAVARNA-MODEL-VALIDATION — Верифікація формалізації sūtra 1.1.9

**Статус:** PARTIAL — реалізація компаратора звірена й коректна, але модель, яку він реалізує, є НЕПОВНОЮ формалізацією читання Kāśikā.
**Дата:** 2026-08-30
**Автор:** Sakshi (wsl-sakshi-1, верифікатор/свідок, capability `shiva-sutras sanskrit verification`)
**Task:** SAVARNA-MODEL-VALIDATION (generation 1)
**Епістемічні джерела:**
- SOURCE = `ksetra/sanskritworld_texts/shastra/grammar/kAshikAvRRitti.txt`, sūtra 1.1.9, рядки 375–404 (першоджерело, прочитано напряму)
- SHIVA/Sakshi = власне читання тексту верифікатором
- SARVAM_WITNESS = `sarvam-ai_transliterate_text` підтвердив читання санскриту (нижче)
- Критика: `docs/CONSOLIDATED_CRITIQUE_AND_REACTIONS.md`, пункт 4

---

## 0. Короткий висновок (Bottom line)

> **«Correct implementation of a model is not validation of the model»** — критика (пункт 4) підтверджується.
> Python-модель `pvc16.py::is_savarna_with` і Verilog-компаратор `fpga_alu.v` (рядки 57–60) є **реалізаційно тотожними** — логічної розбіжності між ними немає. Обидва коректно реалізують одне й те саме *припущення*.
> Але саме припущення (модель), звірене з текстом Kāśikā 1.1.9, є **PARTIAL**:
> - коректно кодує умови `sthāna + prayatna` та виняток sūtra 1.1.10 (ac/hal);
> - **не виражає** чотиричленності внутрішнього prayatna (spṛṣṭa/īṣat-spṛṣṭa/saṃvṛta/vivṛta);
> - **не виражає** правила «r та ūṣman не мають savarṇa» (`रेफोष्मणां सवर्णा न सन्ति`);
> - ризик **хибних позитивних** savarṇa для одно-стганних нерозривних (не-stop) звуків через зведення prayatna до одного біта.

---

## 1. Першоджерело (SOURCE) — Kāśikā на sūtra 1.1.9

Текст із файлу (Devanagari, збережено дослівно):

> **१,१.९ ॥ तुल्यास्यप्रयत्नं सवर्णम् ॥**
> तुल्यशब्दः सदृशपर्यायः । आस्ये भवमास्यं ताल्वादिस्थानम् । प्रयतनं प्रयत्नः स्पृष्टतादिर्वर्णगुणः । तुल्य आस्ये प्रयत्नो यस्य वर्णस्य येन वर्णेन सह स समानजातीयं प्रति सवर्णसञ्ज्ञो भवति ।
> चत्वार आभ्यन्तराः प्रयत्नाः सवर्णसंज्ञायामाश्रीयन्ते स्पृष्टता, ईषत्स्पृष्टता, संवृतता, विवृतता च इति । … रेफोष्मणां सवर्णा न सन्ति । वर्ग्यो वर्ग्येण सवर्णः ॥

**SARVAM_WITNESS** (транслітерація ключової фрази, endpoint `transliterate_text`):
- input `तुल्यास्यप्रयत्नं सवर्णम्` → output `Tulyaasya prayatna svarnam`
- підтверджує читання `tulyāsyaprayatnaṃ savarṇam` (IAST). Жодної розбіжності з SOURCE.

**Змістовний розбір (SHIVA/Sakshi читання):**
- sūtra: «[звук] із однаковим āsya-prayatna є savarṇa». Kāśikā: `tulya` = подібний; `āsya` = місце (sthāna, tālu-тощо); `prayatna` = якість `spṛṣṭatā` і т.ін.
- умова savarṇa = **однакове sthāna** І **однаковий prayatna**.
- **чотири ābhyantara prayatna** (рядок 386): `spṛṣṭatā, īṣat-spṛṣṭatā, saṃvṛtatā, vivṛtatā` — вони різні, тому не можна їх зводити до одного бінарного прапора.
- `रेफोष्मणां सवर्णा न सन्ति` (рядок 392): **r та ūṣman (ś, ṣ, s) не мають savarṇa**.
- `वर्ग्यो वर्ग्येण सवर्णः` (рядок 393): vargīya (член зупинкової серії) є savarṇa лише з vargīya тієї ж серії.
- sūtra 1.1.10 (рядки 410–417): ac (голосні) і hal (приголосні) не є savarṇa взаємно, навіть при tulyāsyaprayatna (приклад: a–h обидва kaṇṭha, але не savarṇa).

---

## 2. Реалізація під звірку

### Python — `prototype/pvc16/pvc16.py::is_savarna_with`
```python
same_sthana   = (self.sthana_mask == other.sthana_mask) and (self.sthana_mask != 0)
same_prayatna = (bool(self.code & PRAYATNA_SPRSTA) == bool(other.code & PRAYATNA_SPRSTA)) \
                and (self.is_vowel == other.is_vowel)
return same_sthana and same_prayatna
```
де `STHANA = code[5:1]`, `PRAYATNA_SPRSTA = 1<<6` (біт 6), `FLAG_VOWEL = 1<<0` (біт 0).

### Verilog — `prototype/fpga_alu/fpga_alu.v`, рядки 57–60
```verilog
wire same_sthana_comb   = (sth_a == sth_b) && (sth_a != 5'b00000);
wire same_prayatna_comb = (spr_a == spr_b) && (vow_a == vow_b);
wire is_savarna_comb    = same_sthana_comb && same_prayatna_comb;
```
де `sth_a = sound_a[5:1]`, `spr_a = sound_a[6]`, `vow_a = sound_a[0]`.

### Звірка Python ↔ Verilog
| Вимірювання | Python | Verilog | Збіг |
|---|---|---|---|
| стхана (місце) | `sthana_mask == other` та `!=0` | `sth_a == sth_b` та `!= 5'b0` | ✅ ідентично |
| prayatna | лише біт SPRSTA (біт 6) | лише `spr_a == spr_b` (біт 6) | ✅ ідентично |
| голосність (виняток 1.1.10) | `is_vowel == is_vowel` | `vow_a == vow_b` | ✅ ідентично |

**Висновок про реалізацію:** НЕ виявлено логічної розбіжності між Python-моделлю і Verilog-компаратором. Обидва реалізують один і той самий бінарний критерій `(same sthāna) && (same spṛṣṭa-bit) && (same vowelness)`.

---

## 3. Звірка моделі з першоджерелом (головний результат)

### 3.1 Що модель кодує КОРЕКТНО ✅
1. **sthāna обов'язковий** — Kāśikā (рядок 396): «kacaṭatapānāṃ bhinnasthānānāṃ tulyaprayatnānāṃ mā bhūt» — зупинки різних місць (k/c/ṭ/t/p) однакового prayatna НЕ savarṇa. Модель вимагає рівність sthāna → k і c не savarṇa. ✅
2. **виняток 1.1.10 (ac/hal)** — модель вимагає однакову голосність → a (ac) і h (hal, обидва kaṇṭha) не savarṇa. ✅ (Kāśikā: «avarṇahakārau … savarṇadīrghatvaṃ na bhavati»)
3. **vargīya серії** — k/kh/g/gh (усі kaṇṭha, усі spṛṣṭa) → savarṇa. Збігається з `वर्ग्यो वर्ग्येण` та традицією (голос/придих не виключають savarṇa). ✅

### 3.2 Що модель НЕ виражає / спотворює ❌
1. **Зведення чотиричленного prayatna до одного біта.** Kāśikā (рядок 386) називає ЧОТИРИ внутрішні prayatna: `spṛṣṭatā, īṣat-spṛṣṭatā, saṃvṛtatā, vivṛtatā`. Семіголосні (yavala = īṣat-spṛṣṭa) і ūṣman/голосні (vivṛta) у моделі мають **біт 6 = 0** — модель не розрізняє їх як РІЗНІ prayatna.
2. **«r та ūṣman не мають savarṇa» (рядок 392) не закладено.** У моделі немає жодного захисту цієї статті. Для двох одно-стганних, одноголосих, не-stop звуків модель видасть savarṇa = 1 — навіть коли традиція прямо каже «savarṇa nāsti».
3. **Ризик хибних позитивних:** напр. `śa` (tālavya, vivṛta, ūṣman) і `ya` (tālavya, īṣat-spṛṣṭa) — модель, якщо обидва зареєстровані з однаковим sthāna і бітом 6 = 0 і голосністю 0, визнає їх savarṇa. Це прямо суперечить лініям 392 і 398–399 Kāśikā («icuyasānāṃ tulayasthānānāṃ bhinnajātīyānāṃ mā bhūt»).
4. **Не подано наповненість реєстру.** PVC-16 `REGISTRY` має лише невелику підмножину звуків (a,A,i,I,u,U,f,x + kavarga/tavarga частково). Відсутні: e, o, ai, au, ṛ/ḷ довгі, усі ūṣman (ś, ṣ, s), y/v/r/l санскритської фонетики. Тому порівняльник не можна повно тестувати на класичному наборі.

### 3.3 Відомі граничні випадки (Kāśikā явно окремими статтями)
- `र्कारल्कारयोः सवर्णसञ्ज्ञा वक्तव्या` (рядок 400) — r-kāra і l-kāra (ṛ, ḷ) оголошуються savarṇa **окремою vaktavya-вказівкою**; у моделі `f`(ṛ) = mūrdhanya, `x`(ḷ) = dantya → різні sthāna → не savarṇa. Без окремого спец-випадку модель це «неправильно» (але це традиційна делібератна надбудова, а не частина базового визначення 1.1.9).

---

## 4. Епістемічний висновок

- **REALIZATION-IN-PYTHON = REALIZATION-IN-VERILOG** (звірено — ідентично). Жодного приводу виправляти компаратор.
- **MODEL-vs-SOURCE = PARTIAL.** Модель є коректною, але **неповною** депікцією читаня Kāśikā sūtra 1.1.9. Вона покриває основний вокальний/варговий випадок, але:
  - не розрізняє чотири ābhyantara prayatna;
  - не реалізує «repo/ūṣman не мають savarṇa»;
  - дозволяє хибні savarṇa для одно-стганних не-stop пар.
- **Практичний сенс для проєкту:** вердикт «компаратор працює» або «iverilog PASS» НЕ є доказом того, що модель savarṇa коректна. Для позначення моделі як CONFIRMED потрібно:
  1. розширити prayatna-поле до ≥2 бітів (справжнє кодування 4 значень), або явно зафіксувати еквіваленцію «savarṇa = same sthāna + same varga-class + same vowelness» та задокументувати це як свідоме спрощення;
  2. додати guard «ūṣman/repha → no savarṇa»;
  3. розширити `REGISTRY` на повний санскритський набір і протестувати всі пари.
- **Що НЕ робити:** не правити джерело і не перекваліфіковувати модель у CONFIRMED, поки пункти 1–3 не виконано. Поточний чесний статус: **PARTIAL**, реалізація коректна, модель неповна.

---

## 5. Метрика звітності (owner policy)

```
SOURCE            = kAshikAvRRitti.txt рядки 375–404 (першоджерело, прочитано)
SHIVA/Sakshi      = close reading (цей документ)
SARVAM_WITNESS    = transliterate_text: tulyāsyaprayatnaṃ savarṇam ✅ (збіг з SOURCE)
CONFIRMED         =  Python↔Verilog реалізаційна тотожність; основна варгова коректність
PARTIAL           =  модель проти Kāśikā (чотиричленний prayatna; ūṣman/repha-guard; повнота REGISTRY)
UNRESOLVED        =  точний набір savarṇa-пар для повного REGISTRY (немає реєстру — не тестовано)
```

**Дія для власника:** рішення, розширювати чи полегшувати модель — за власником. Це саме ті межі, які авторитетно належать shiva-sutras/panini domain, а не my-lisp/FPGA.
