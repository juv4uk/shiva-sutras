# Що наука каже про «повну фонетику людства» — і що це означає для UPC

**Автор:** Manus AI  
**Дата:** 18 серпня 2026 року

## Коротка відповідь

Науковці не мають і не очікують мати один остаточний список на кшталт «ось усі 256 звуків, які людство коли-небудь використовує». Причина не в тому, що лінгвістика нічого не знає. Навпаки: вона дуже добре описує звуки, але розрізняє кілька різних рівнів — **фізично можливі звуки**, **фонетичні реалізації**, **фонеми конкретної мови**, **способи транскрипції** та **аналіз певного діалекту в певний час**.

> Для UPC найкраща мета — не «закодувати повну фонетику людства одним байтом», а створити **versioned representation system**: компактне стабільне ядро, language profiles, modifiers і багатобайтні escape extensions для того, що не вміщується в базовий inventory.

## 1. Чому питання не має одного простого числа

Під фразою «повна фонетика людства» можна мати на увазі принаймні п’ять різних речей.

| Рівень | Що він означає | Чи можна отримати остаточний список? |
|---|---|---|
| **Артикуляційний простір** | Усі рухи язика, губ, гортані, струменя повітря та їхні комбінації, які може зробити людина. | Ні: простір значною мірою безперервний. |
| **Phones** | Конкретні вимовлені звуки, наприклад `[k]`, `[kʰ]`, `[k̚]`. | Ні як скінченний остаточний набір: контекст і деталі вимови породжують варіацію. |
| **Phonemes** | Контрастивні одиниці певної мови чи діалекту, наприклад `/k/`. | Лише для конкретного doculect і конкретного аналізу. |
| **IPA symbols** | Символи та діакритики для запису фонетичного аналізу. | Це нотація, а не список фонем світу. |
| **Implementation inventory** | Набір атомів, який обирає конкретна система на кшталт UPC. | Так, але це engineering contract, а не природний закон. |

Найважливіша відмінність: **людина може вимовити безліч фізично різних sounds, але мова не обов’язково вважає ці відмінності різними одиницями.** Англійське `/p/` у *pin* і *spin* може мати помітно різну акустичну реалізацію, але для носія англійської це зазвичай один phoneme. В іншій мові подібна різниця може бути contrastive.

## 2. Фонема — не просто «звук», а результат аналізу

WALS визначає sound inventory через contrastive analysis: треба подивитися, чи мінімальна зміна елемента змінює слово. Але навіть після цього залишаються теоретичні рішення: чи є щось одним сегментом або послідовністю, як рахувати запозичення, довготу, дифтонги, nasalisation тощо [3] [4].

Наприклад, WALS пояснює, що англійське `/tʃ/` у *chip* за певними distributional reasons аналізується як один consonant, тоді як `/kw/` у *quick* — як послідовність двох [3]. Це означає, що два інженери можуть однаково точно записати артикуляцію, але по-різному вирішити, скільки atomic units має їхній format.

Так само long vowel можна трактувати як один `/aː/` або як `/a/ + LONG`; nasal vowel — як один `/ã/` або `/a/ + NASAL`; tone — як частину vowel або як окрему prosodic layer. WALS прямо зазначає, що такі рішення впливають на розмір inventory і що різні аналізи можуть бути добре вмотивованими [4].

> Отже, «скільки фонем існує у світі?» завжди неповне без уточнення: **який рівень аналізу, яка транскрипція, який діалект, яка дата та які правила сегментації?**

## 3. Що ми знаємо емпірично

Найкорисніший сучасний орієнтир — [PHOIBLE 2.0][1], велика база cross-linguistic phonological inventories. Release 2.0 містить **3,020 inventories**, **3,183 segment types** і дані з **2,186 distinct languages** [1].

Але число **3,183 не означає «у світі існує рівно 3,183 людські звуки»**. PHOIBLE itself називає себе searchable convenience sample, збирає inventories із різних описів і нормалізує їх до Unicode IPA [1]. Її FAQ підкреслює, що різні джерела можуть не погоджуватися щодо кількості або ідентичності фонем того самого language variety; тому база працює з поняттям **doculect** — описаного різновиду мови в конкретному місці, часі та джерелі [2].

| Дані | Що вони насправді означають |
|---|---|
| 3,183 PHOIBLE segment types | Спостережені й нормалізовані segment labels у вибірці джерел. |
| 2,186 languages у PHOIBLE 2.0 | Охоплені distinct languages, а не всі відомі різновиди або всі мовні стани в історії. |
| Кілька inventories для однієї мови | Не обов’язково «помилка»: різні doculects або analyses можуть legitimately differ. |
| Unicode IPA representation | Спосіб interoperability, а не доказ, що IPA segment = one universal phoneme. |

Це дуже близько до твоєї власної ідеї provenance у `shiva-sutras`: **не приховувати, що representation залежить від джерела та аналітичного рішення.**

## 4. Наскільки різняться inventories мов

Відповідь: іноді дуже сильно. У WALS sample consonant inventories варіюють від **6 до 122**; для 562 мов mean становить **22.7**, mode — **22**, median — **21**. У прикладах WALS Rotokas має шість consonants, а !Xóõ — 122, значною мірою через велику кількість click contrasts [3].

Vowel-quality inventories у WALS sample лежать між **2 та 14**, а average є трохи меншим за шість; найчастіша конфігурація — п’ять basic vowel qualities [4]. WALS при цьому навмисно відокремлює basic quality від long/short variants, nasalisation і diphthongs, щоб не змішувати різні рішення сегментації [4].

| Вимір | Низький край у WALS sample | Типовий рівень | Високий край |
|---|---:|---:|---:|
| Consonants | 6 | приблизно 21–23 | 122 |
| Basic vowel qualities | 2 | приблизно 5–6 | 14 |

Це не означає, що найбільша consonant inventory автоматично має найбільшу фонологічну складність. Наприклад, WALS не виявив значущої кореляції між кількістю consonants і кількістю basic vowel qualities у paired sample of 559 languages; systems можуть бути великими в обох вимірах або малими в обох [4]. А ще існують tone, stress, phonation, vowel harmony, syllable structure, length і phonotactics — вони не зводяться до простого підрахунку segment symbols.

## 5. Що таке IPA — і чому воно не є byte table

International Phonetic Association підтримує official IPA chart через formal process of proposals and Council approval; chart історично змінювався, а поточні chart reissues зберігають revision 2015/2005 [5]. Сам цей факт показує: IPA — жива наукова нотаційна система, яку уточнюють у міру потреби, а не застигла природна таблиця всіх звуків.

IPA є **композиційною системою**. Letter може позначати базовий segment, а diacritics — voicing, aspiration, nasalisation, retraction, tone, stress, duration та інші деталі. Один фонетичний запис може бути кількома Unicode code points. Тому перетворити IPA прямо на UPC-8 як `one IPA symbol = one byte` неможливо без втрати або без багатобайтних sequences.

```text
[a]        → можливий base segment
[aː]       → base + length
[ã]        → base + nasalisation
[kʰ]       → base + aspiration
[t͡ʃ]       → один complex segment або sequence — залежно від profile
```

Це не вада UPC. Це саме причина, чому твоя ідея **8-bit base + 2/3/4-byte extensions** природна і правильна.

## 6. Науково чесна модель для UPC

UPC не повинен намагатися бути «byte version of IPA». Натомість він може бути трьома речами одночасно, але в різних шарах.

```text
Layer A — stable base inventory
    Small, documented set of frequent/important atomic segments.

Layer B — language profiles
    Source-backed rules: orthography/transliteration → UPC sequences;
    UPC sequences → target orthography or phonemic representation.

Layer C — extensions and modifiers
    Rare segments, detailed phonetics, tone, duration, nasalisation,
    experimental namespaces and future research.
```

### Layer A: 8-bit base

Тут 256 values достатньо не для «всіх phones», а для стабільного foundation. Śiva Sūtras можуть бути одним ordered root у цьому foundation, якщо це названо **engineering design choice**, а не claim про complete world inventory.

Базовий byte варто виділяти тоді, коли entity:

1. frequently reappears across profiles;
2. має стабільну semantic identity у твоєму contract;
3. потрібна як atomic unit у інференсі або hardware fast path;
4. не є просто predictable combination of already represented features.

### Layer B: language profiles

Мова не повинна отримувати «свій block bytes». Вона має отримувати profile, який reuse-ить shared units.

```yaml
profile_id: example-language-phonemic-v1
inventory_version: upc-base-v1
source_ref: source-document@revision
normalization: NFC

encode:
  grapheme_or_token: [UPC sequence]
```

Тоді English, Ukrainian, Sanskrit, Polish і dozens of other profiles можуть використовувати той самий `/k/`, `/m/`, `/s/`, `/a/` і додавати тільки distinct contrasts. Саме profiles, а не base byte table, мають вирішувати, чи `kh` є `[k, h]`, `[kʰ]` або orthographic convention.

### Layer C: multi-byte extensions

Твоя ідея extensions 2, 3 і 4 bytes відповідає реальному стану фонетичної науки. Вона дозволяє:

- не витрачати base byte на рідкісну комбінацію;
- зберігати uncommon segment as explicit extension;
- кодувати modifiers compositionally;
- додавати нові namespaces без зміни old byte meanings;
- лишити unknown extension opaque для старого decoder-а замість хибного розбору.

Ілюстративна, а не остаточна, схема могла б бути такою:

| Простір | Роль |
|---|---|
| Ordinary base values | Frequently used stable segments and controls. |
| Reserved prefix values | Unambiguous introducers for 2/3/4-byte extension forms. |
| Profile frame / manifest | Assignment version, profile ID, source revision, normalisation. |
| Escape namespace | Rare segment, research-only feature, private experiment or future standard. |

Найважливіше правило: **prefix must determine parse length unambiguously**. Інакше старий decoder помилково прочитає один novel extension як кілька familiar base segments.

## 7. Чого не слід обіцяти UPC

Науково сильна позиція UPC не потребує надмірних тверджень. Він може чесно сказати:

> UPC provides a versioned, profile-aware representation for selected phonological and phonetic units. It does not claim to be a final enumeration of all human speech sounds or a replacement for IPA.

Не варто обіцяти:

- «усі звуки всіх мов уміщаються в 256 bytes»;
- «один UCS/UPC code автоматично є одним фонемом у кожній мові»;
- «Śiva Sūtras already contain a universal inventory»;
- «один physical sound has one universally correct segmentation».

Натомість можна обіцяти те, що реально можна перевірити:

- mapping is versioned;
- every profile has source and scope;
- base assignments remain stable;
- unknown extensions fail safely;
- same profile + same input produce same UPC sequence;
- profiles can disagree without corrupting each other.

## 8. Висновок для твоєї ідеї

Наука не каже: «усі мови надто різні, тому 8-bit core безнадійний». Вона каже тонше:

> **Немає одного природно заданого finite list of phonemes that applies identically to every language. Але є великі перетини, типологічні регулярності, добре описані inventories і дуже корисні feature systems.**

Тому твоя архітектура має сенс саме в такій формі:

```text
8-bit UPC core
  + immutable assignment/version contract
  + source-aware language profiles
  + modifiers for compositional detail
  + 2/3/4-byte extension namespaces
  + explicit epistemic status for experimental mappings
```

Тобто не «я створю остаточний код усієї людської фонетики», а:

> **Я створю систему, у якій компактні базові одиниці можуть стабільно рости в напрямку дедалі ширшого, provenance-aware опису людських мов — без того, щоб ранні спрощення вдавали остаточну істину.**

## References

[1]: https://phoible.org/ "PHOIBLE 2.0 — phonological inventory database"
[2]: https://phoible.org/faq "PHOIBLE FAQ — doculects, source variation and phoneme analysis"
[3]: https://wals.info/chapter/1 "WALS: Consonant Inventories, Ian Maddieson"
[4]: https://wals.info/chapter/2 "WALS: Vowel Quality Inventories, Ian Maddieson"
[5]: https://www.internationalphoneticassociation.org/content/ipa-chart "International Phonetic Association: IPA chart and revisions"
