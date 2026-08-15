# Cross-Witness Diff: GRETIL Kāśikā vs GRETIL Aṣṭādhyāyī (Baums)

Two independent GRETIL transcriptions of the Aṣṭādhyāyī sūtrapāṭha are compared.
This test verifies *transcription fidelity*, NOT historical authenticity.
(Reproducibility of an edition does not prove authenticity of the text — E-001.)

## Method

- Witness A: Kāśikāvṛtti (Sharma ed., GRETIL `jvkasipu.htm`) — sūtra text as cited in Kāśikā.
- Witness B: Aṣṭādhyāyī (Baums transcription, GRETIL `panini_u.htm`).
- Normalization: Unicode NFC, diacritics removed, sandhi/separator characters removed, lowercase.
- Similarity: `difflib.SequenceMatcher.ratio()` on normalized strings.
- Alignment: global sequence alignment (Needleman-Wunsch) per pāda absorbs local
  numbering shifts between the two editions as gaps instead of false conflicts.

## Statuses

| Status | Threshold | Meaning |
| :--- | :--- | :--- |
| `AGREES` | ratio >= 0.9 | The two witnesses essentially agree modulo notation |
| `VARIANTS` | 0.6 <= ratio < 0.9 | Same sūtra, wording/notation differs |
| `CONFLICTS` | ratio < 0.6 | Substantive textual disagreement |
| `MISSING` | - | Sūtra present in only one witness |

## Summary

- Total sūtras considered: 3983
- `AGREES`: 1891
- `VARIANTS`: 2013
- `CONFLICTS`: 22
- `MISSING`: 57

## Interpretation (epistemic, not exhaustive)

The two GRETIL transcriptions use DIFFERENT transliteration conventions:

- **Witness B (Baums)** drops diacritics in some places and uses `=` for
  word-sandhi, `T`/`K`/`C`/`L`/`Ṣ` capitals for the same phonemes that
  Witness A writes as `d`/`k`/`c`/`l`/`ṣ` (marker capitalization).
- **Witness A (Kāśikā/Sharma)** preserves full IAST diacritics and uses `-` for
  internal word-sandhi, plus `//` sentence-end.

Consequently, most `VARIANTS` reflect *notation* (capital markers, `=` vs `-`,
sandhi re-joining) rather than textual disagreement. As an approximate signal,
of the `VARIANTS`, roughly **386** differ only by spacing/letter-case after stripping non-letters.

### What this diff DOES prove

- Both witnesses cover the same overall sūtra corpus (3951–3958 sūtras).
- The two independent digitizations do NOT materially disagree in wording at the
  level of *which sūtra text appears*; they differ in transcription style.
- This is a **transcription-fidelity** check: it confirms the two editions were
  digitized consistently, it does NOT certify that the underlying text is the
  authentic 7th-century Kāśikā (E-001: Reproducibility ≠ Authenticity).

### Known structural discrepancies (edition-level)

- Witness A (Kāśikā/Sharma) does not include sūtras **1.1.46–1.1.75** and
  **8.3.118–8.3.119** in its numbering (they are present in Witness B).
- Witness A includes **2.4.27** which Witness B lacks; numbering offsets exist.
- The pāda 8.3 numbering diverges after sūtra 8.3.98: the Sharma edition omits two
  sūtras that Baums numbers 8.3.99–8.3.100, so Kāśikā 8.3.99 → Baums 8.3.101, etc.
  The sequence alignment above absorbs this shift.
  These are *edition-level* differences and must be resolved by a named critical
  edition before use as `REAL` evidence for those sūtras.

### `CONFLICTS` (22) require expert review

The sūtras listed below fall below the agreement threshold. Some are notation
artifacts (e.g. `ūṃ` vs `oṃ` in 1.1.18), others may indicate genuine variant
readings between the Sharma Kāśikā edition and the Baums transcription.
Each must be adjudicated by an expert against a named critical edition before
being used as evidence.

### `MISSING` (57) — edition-level gaps

Sūtras present in only one witness after alignment. These reflect edition-level
numbering/content differences (see "Known structural discrepancies"), not
necessarily textual loss in either witness.

## Per-Sūtra Detail

| Sūtra | Status | Sim | Kāśikā (Witness A) | Baums (Witness B) |
| :--- | :--- | :--- | :--- | :--- |
| 1.1.1 | VARIANTS | 0.897 | vṛddhir ād-aic | vṛd-dhir āT=aiC |
| 1.1.2 | VARIANTS | 0.857 | adeṅ guṇaḥ | aT=eṄ guṇaḥ |
| 1.1.3 | AGREES | 0.968 | iko guṇa-vṛddhī | iKo guṇa-vṛd-dhī |
| 1.1.4 | AGREES | 0.941 | na dhātu-lopa ārdhadhātuke | na dhātulope=ārdhadhātuke |
| 1.1.5 | VARIANTS | 0.889 | kṅiti ca | K-Ṅ-ITi ca |
| 1.1.6 | AGREES | 1.000 | dīdhī-vevī-iṭām | dīdhī-vevī=iṬām |
| 1.1.7 | VARIANTS | 0.894 | halo 'nantarāḥ saṃyogaḥ | haLaḥ=anantarāḥ saṃyogaḥ |
| 1.1.8 | AGREES | 0.918 | mukha-nāsikā-vacano 'nunāsikaḥ | mukha-nāsikā-vacanaḥ=anunāsikaḥ |
| 1.1.9 | AGREES | 0.931 | tulya-āsya-prayarnaṃ savarṇam | tulya=āsya-prayatnam savarṇam |
| 1.1.10 | VARIANTS | 0.870 | na aj-jhalau | na=aC=haLau |
| 1.1.11 | VARIANTS | 0.862 | īd-ūd-ed-dvivacanaṃ pragṛhyam | īT=ūT-eT=dvivacanam pragṛhyam |
| 1.1.12 | AGREES | 1.000 | adaso māt | adaso māt |
| 1.1.13 | AGREES | 1.000 | śe | Śe |
| 1.1.14 | AGREES | 0.947 | nipāta eka-aj-an-āṅ | nipāta eka=aC=an-āṄ |
| 1.1.15 | AGREES | 1.000 | ot | oT |
| 1.1.16 | AGREES | 0.925 | sambuddhau śākalyasya-itāv anārṣe | sambuddhau śākalyasya itau=an-ārṣe |
| 1.1.17 | AGREES | 1.000 | uñaḥ | uÑaḥ |
| 1.1.18 | CONFLICTS | 0.500 | ūṃ | oṃ |
| 1.1.19 | AGREES | 0.939 | īd-ūtau ca saptamy-arthe | īT=ūT-au ca saptamy-arthe |
| 1.1.20 | AGREES | 0.903 | dā-dhā ghv-adāp | dā-dhā GHU=a-dāP |
| 1.1.21 | AGREES | 0.919 | ādyantavad ekasmin | ādy-antavat=ekasmin |
| 1.1.22 | AGREES | 1.000 | tarap-tamapau ghaḥ | taraP-tamaPau GHAḥ |
| 1.1.23 | AGREES | 0.963 | bahu-gaṇa-vatu-ḍati saṅkhyā | bahu-gaṇa-vatU-Ḍati saṃkhyā |
| 1.1.24 | AGREES | 0.960 | ṣṇa-antā ṣaṭ | ṣ-ṇa=antā ṢAṬ |
| 1.1.25 | AGREES | 1.000 | ḍati ca | Ḍati ca |
| 1.1.26 | AGREES | 1.000 | kta-ktavatū niṣṭhā | Kta-KtavatŪ niṣṭhā |
| 1.1.27 | AGREES | 1.000 | sarva-ādīni sarvanāmāni | sarva-ādīni sarvanāmāni |
| 1.1.28 | AGREES | 0.947 | vibhāṣā dikṣamāse bahuvrīhau | vibhāṣā dik-samāse bahuvrīhau |
| 1.1.29 | AGREES | 1.000 | na bahuvrīhau | na bahuvrīhau |
| 1.1.30 | AGREES | 1.000 | tṛtīyā-samāse | tṛtīyā-samāse |
| 1.1.31 | AGREES | 0.900 | dvandve ca | dvaṃdve ca |
| 1.1.32 | AGREES | 0.917 | vibhāṣā jasi | vibhāṣa Jasi |
| 1.1.33 | AGREES | 1.000 | prathama-carama-taya-alpa-ardha-katipaya-nemāś ca | prathama-carama-taya=alpa=ardha-katipaya-nemāś ca |
| 1.1.34 | AGREES | 0.971 | pūrva-para-avaradakṣiṇa-uttara-apara-adharāṇi vyavasthāyām asañjñāyām | pūrva-para=avara=dakṣiṇa=uttara=apara=adharāṇi vyavasthāyām a-saṃjñāyām |
| 1.1.35 | AGREES | 0.981 | svam ajñāti-dhana-ākhyāyām | svam a-jñāti-dhana=ākhyāyām |
| 1.1.36 | AGREES | 0.969 | antaraṃ bahiryoga-upasaṃvyānayoḥ | antaram bahiryoga=upasaṃvyānayoḥ |
| 1.1.37 | AGREES | 0.979 | svarādi-nipātam avyayam | svar-ādi-nipātam avyayam |
| 1.1.38 | AGREES | 0.983 | taddhitaś ca asarva-vibhaktiḥ | taddhitaś ca a-sarva-vibhaktiḥ |
| 1.1.39 | VARIANTS | 0.857 | kṛn-m-ej-antaḥ | kṛt=m=eC=antaḥ |
| 1.1.40 | AGREES | 0.944 | ktvā-tosun-kasunaḥ | Ktvā-tosuN-KasuNāḥ |
| 1.1.41 | VARIANTS | 0.867 | avyayī-bhāvaś ca | avayībhāvas=ca |
| 1.1.42 | AGREES | 1.000 | śi sarvanāma-sthānam | Śi sarvanāma-sthānam |
| 1.1.43 | AGREES | 0.914 | suḍ anapuṃsakasya | sUṬ a-napuṃsakasya |
| 1.1.44 | AGREES | 1.000 | na vā-iti vibhāṣā | na vā=iti vibhāṣā |
| 1.1.45 | AGREES | 0.955 | ig-yaṇaḥ samprasāraṇam | iK=yaṆaḥ samprasāraṇam |
| 1.1.46 | MISSING | - | - | ādy-antau Ṭa-K-ITau |
| 1.1.47 | MISSING | - | - | M-IT=aCaḥ=antyāt paraḥ |
| 1.1.48 | MISSING | - | - | eCa iK=hrasva=ādeśe |
| 1.1.49 | MISSING | - | - | ṣaṣṭhī sthāne-yogā |
| 1.1.50 | MISSING | - | - | sthāne=antara-tamaḥ |
| 1.1.51 | MISSING | - | - | ur aṆ rA~-paraḥ |
| 1.1.52 | MISSING | - | - | aLaḥ=antyasya |
| 1.1.53 | MISSING | - | - | Ṅ-ITca |
| 1.1.54 | MISSING | - | - | ādeḥ parasya |
| 1.1.55 | MISSING | - | - | aneka=aL ŚIT sarvasya |
| 1.1.56 | MISSING | - | - | sthānivad ādeśaḥ=an-aL-vidhau |
| 1.1.57 | MISSING | - | - | aCaḥ parasmin pūrva-vidhau |
| 1.1.58 | MISSING | - | - | na pada=anta-dvir-vacana-vare-ya-lopa-svara-savarṇa=anusvāra-dīrgha-jaS=caR-vidhiṣu |
| 1.1.59 | MISSING | - | - | dvir-vacane=aCi |
| 1.1.60 | MISSING | - | - | a-darśanaṃ lopaḥ |
| 1.1.61 | MISSING | - | - | pratyayasya luK-Ślu-luPaḥ |
| 1.1.62 | MISSING | - | - | pratyaya-lope pratyaya-lakṣaṇam |
| 1.1.63 | MISSING | - | - | na lumatā=aṛgasya |
| 1.1.64 | MISSING | - | - | aCaḥ=antya=ādi ṬI |
| 1.1.65 | MISSING | - | - | aLaḥ=antyāt pūrva upadhā |
| 1.1.66 | MISSING | - | - | tasmin=iti nirdiṣṭe pūrvasya |
| 1.1.67 | MISSING | - | - | tasmād ity uttarasya |
| 1.1.68 | MISSING | - | - | svaṃ rūpaṃ śabdasya=a-śabda-saṃjñā |
| 1.1.69 | MISSING | - | - | aṆ uT=it savarṇasya ca=a-pratyayaḥ |
| 1.1.70 | MISSING | - | - | Ta-paras tat-kālasya |
| 1.1.71 | MISSING | - | - | ādir antyena saha=ITā |
| 1.1.72 | MISSING | - | - | yena vidhis tad-antasya |
| 1.1.73 | MISSING | - | - | vṛd-dhi-r yasya=aCām ādis tad vṛd-dham |
| 1.1.74 | MISSING | - | - | tyad-ādīni ca |
| 1.1.75 | MISSING | - | - | eṄ prācām deśe |
| 1.2.1 | VARIANTS | 0.692 | gāṅ-kuṭādibhyo 'ñṇinṅit | gāṄ-kuṭādibhyaḥ=a-Ñ-Ṇ-IT=Ṅ-IT |
| 1.2.2 | AGREES | 1.000 | vija iṭ | vija iṬ |
| 1.2.3 | AGREES | 1.000 | vibhāṣā-ūrṇoḥ | vibhāṣā=ūrṇoḥ |
| 1.2.4 | AGREES | 0.947 | sārvadhātukam apit | sārvadhātukam a-P-IT |
| 1.2.5 | VARIANTS | 0.889 | asaṃyogāl liṭ kit | a-saṃyogāt=lIṬ K-IT |
| 1.2.6 | AGREES | 1.000 | indhi-bhavatibhyāṃ ca | indhi-bhavatibhyāṃ ca |
| 1.2.7 | VARIANTS | 0.857 | mṛḍ-amṛda-gudha-kuṣa-kliśa-vada-vasaḥ ktvā | mṛḍḥ-mṛdḥ-gudhḥ-kuṣḥ-kliśA-vadḥ-vasaḥ Krvā |
| 1.2.8 | AGREES | 0.918 | ruda-vida-muṣa-grahi-svapi-pracchaḥ saṃś ca | ruda-vidḥ-muṣḥ-grahi-svapi-pracchaḥ saN=ca |
| 1.2.9 | AGREES | 1.000 | iko jhal | iKo jhaL |
| 1.2.10 | VARIANTS | 0.870 | halantāc ca | haL-antāt=ca |
| 1.2.11 | AGREES | 1.000 | liṅ-sicau ātmanepadeṣu | lIṄ-siCau=ātmanepadeṣu |
| 1.2.12 | VARIANTS | 0.800 | uś ca | us ca |
| 1.2.13 | AGREES | 1.000 | vā gamaḥ | vā gamaḥ |
| 1.2.14 | AGREES | 1.000 | hanaḥ sic | hanaḥ siC |
| 1.2.15 | AGREES | 1.000 | yamo gandhane | yamo gandhane |
| 1.2.16 | AGREES | 1.000 | vibhāṣā-upayamane | vibhāṣā=upayamane |
| 1.2.17 | VARIANTS | 0.867 | sthāghvor icca | sthā-GHVor iT=ca |
| 1.2.18 | AGREES | 1.000 | na ktvā sa-iṭ | na Ktvā sa=iṬ |
| 1.2.19 | AGREES | 1.000 | niṣṭhā śīṅ-svidi-midi-kṣvidi-dhṛṣaḥ | niṣṭhā śīṄ-svidi-midi-kṣvidi-dhṛṣaḥ |
| 1.2.20 | AGREES | 1.000 | mṛṣas titikṣāyām | mṛṣas titikṣāyām |
| 1.2.21 | AGREES | 0.938 | udupadhād bhāva-ādikarmaṇor anyatarasyām | uT=upadhāt=bhāva=ādikarmaṇor anyatarasyām |
| 1.2.22 | AGREES | 1.000 | pūṅaḥ ktvā ca | pūṄaḥ Ktvā ca |
| 1.2.23 | AGREES | 0.963 | na-upadhāt tha-pha-antād vā | na=upadhāt tha-pha=antāt=vā |
| 1.2.24 | VARIANTS | 0.789 | vañci-luñcy-ṛtaś ca | vanci=lunci=ṛtas ca |
| 1.2.25 | AGREES | 1.000 | tṛṣi-mṛṣi-kṛśeḥ kāśyapasya | tṛṣi-mṛṣi-kṛśeḥ kāśyapasya |
| 1.2.26 | VARIANTS | 0.818 | ralo v-y-upadhad-dhal-ādeḥ saṃś ca | raLo u=i=upadhāt=haL-ādeḥ saN=ca |
| 1.2.27 | VARIANTS | 0.852 | ūkālo 'j-jhrasva-dīrgha-plutaḥ | ū-kālaḥ=aC=hrasva-dīrgha-plutaḥ |
| 1.2.28 | AGREES | 1.000 | acaś ca | aCaś ca |
| 1.2.29 | AGREES | 1.000 | uccair udāttaḥ | uccair udāttaḥ |
| 1.2.30 | AGREES | 1.000 | nīcair anudāttaḥ | nīcair anudāttaḥ |
| 1.2.31 | AGREES | 1.000 | samāhāraḥ svaritaḥ | samāhāraḥ svaritaḥ |
| 1.2.32 | AGREES | 1.000 | tasya-ādita udāttam ardha-hrasvam | tasya=ādita udāttam ardha-hrasvam |
| 1.2.33 | AGREES | 1.000 | eka-śruti dūrāt sambuddhau | eka-śruti dūrāt sambuddhau |
| 1.2.34 | AGREES | 0.928 | yajña-karmaṇy-ajapa-nyūṅkha-sāmasu | yajña-karmaṇi=a-japa-nyūṛkha-sāmasu |
| 1.2.35 | AGREES | 1.000 | uccaistarāṃ vā vaṣaṭkāraḥ | uccaistarāṃ vā vaṣaṭkāraḥ |
| 1.2.36 | AGREES | 1.000 | vibhāṣā chandasi | vibhāṣā chandasi |
| 1.2.37 | AGREES | 0.974 | na subrahmaṇyāyāṃ svaritasya tu udāttaḥ | na subrahmaṇyāyām svaritasya tu=udāttaḥ |
| 1.2.38 | AGREES | 1.000 | deva-brahmaṇor anudāttaḥ | deva-brahmaṇor anudāttaḥ |
| 1.2.39 | AGREES | 1.000 | svaritāt saṃhitāyām anudāttānām | svaritāt saṃhitāyām anudāttānām |
| 1.2.40 | AGREES | 1.000 | udātta-svarita-parasya sannataraḥ | udātta-svarita-parasya sannataraḥ |
| 1.2.41 | AGREES | 1.000 | apṛkta eka-al pratyayaḥ | apṛkta eka=aL pratyayaḥ |
| 1.2.42 | AGREES | 1.000 | tatpuruṣaḥ samāna-adhikaraṇaḥ karmadhārayaḥ | tatpuruṣaḥ samāna=adhikaraṇaḥ karmadhārayaḥ |
| 1.2.43 | AGREES | 1.000 | prathamā-nirdiṣṭaṃ samāsa upasarjanam | prathamā-nirdiṣṭaṃ samāsa upasarjanam |
| 1.2.44 | AGREES | 0.931 | eka-vibhākti ca apūrva-nipāte | eka-vibhakti ca=a-ūrva-nipāte |
| 1.2.45 | AGREES | 0.976 | arthavad adhātur apratyayaḥ prātipadikam | arthavad a-dhātur a-pratyayaḥ prātipadikam |
| 1.2.46 | AGREES | 1.000 | kṛt-taddhita-samāsāś ca | kṛt-taddhita-samāsāś ca |
| 1.2.47 | AGREES | 1.000 | hrasvo napuṃsake prātipadikasya | hrasvo napuṃsake prātipadikasya |
| 1.2.48 | AGREES | 0.979 | gostriyor upasarjanasya | go-striyor upasarjanasya |
| 1.2.49 | AGREES | 1.000 | luk taddhita-luki | luK taddhita-luKi |
| 1.2.50 | VARIANTS | 0.889 | id-goṇyāḥ | iT=goṇyāḥ |
| 1.2.51 | AGREES | 0.943 | lupi yuktavad-vyaktivacane | luPi yuktavat=vyakti-vacane |
| 1.2.52 | AGREES | 0.977 | viśeṣaṇānāṃ ca ajāteḥ | viśeṣaṇānāṃ ca=a-jāteḥ |
| 1.2.53 | AGREES | 0.967 | tad aśiṣyaṃ sañjñā-pramāṇatvāt | tad aśiṣyaṃ saṃjñā-pramāṇatvāt |
| 1.2.54 | AGREES | 0.927 | lub yoga-aprakhyānāt | lup=yoga=a-prakhyānāt |
| 1.2.55 | AGREES | 0.940 | yoga-pramāṇe ca tad-abhāve 'darśanam syāt | yoga-pramāṇe ca tad-abhāve=a-darśanaṃ syāt |
| 1.2.56 | AGREES | 0.973 | pradhāna-pratyaya-arthavacanam arthasya anya-pramāṇātvāt | pradhāna-pratyaya=artha-vacanam arthasya=anya-pramāṇatvāt |
| 1.2.57 | AGREES | 1.000 | kāla-upasarjane ca tulyam | kāla=upasarjane ca tulyam |
| 1.2.58 | AGREES | 0.978 | jāty-ākhyāyam ekasmin bahuvacanam anyatarasyām | jāty-ākhyāyām ekasmin bahuvacanam anyatarasyām |
| 1.2.59 | AGREES | 0.938 | asmado dvayoś ca | asmado dvāyoś ca |
| 1.2.60 | AGREES | 1.000 | phalgunī-proṣṭhapadānāṃ ca nakṣatre | phalgunī-proṣṭhapadānāṃ ca nakṣatre |
| 1.2.61 | AGREES | 0.984 | chandasi punarvasvorekavacanam | chandasi punarvasvor ekavacanam |
| 1.2.62 | VARIANTS | 0.846 | viśākhayoś ca | visākhayos ca |
| 1.2.63 | AGREES | 0.970 | tiṣya-punarvasvor nakṣatra-dvandve bahuvacanasya dvivacanaṃ nityam | tiṣya-punarvasvor nakṣatra-dvaṃdve bahuvacanasya dvivacanam nityam |
| 1.2.64 | AGREES | 0.968 | sasūpāṇām ekaśeṣa eka-vibhaktau | sarūpāṇām ekaśeṣa eka-vibhaktau |
| 1.2.65 | AGREES | 0.975 | vṛddho yūnā tal-lakṣaṇaś ced-eva viśeṣaḥ | vṛddho yūnā tad=lakṣaṇaś ced-eva viśeṣaḥ |
| 1.2.66 | AGREES | 0.929 |  strī puṃvac-ca | strī puṃvat=ca |
| 1.2.67 | AGREES | 1.000 | pumān striyā | pumān striyā |
| 1.2.68 | AGREES | 1.000 | bhrātṛ-putrau svasṛ-duhitṛbhyām | bhrātṛ-putrau svasṛ-duhitṛbhyām |
| 1.2.69 | AGREES | 0.950 | napuṃsakam anapuṃsakena-ekavac-ca-asya-anyatarasyām | napuṃsakam a-napuṃsakena=ekavat=a=asya=nyatarasyām |
| 1.2.70 | AGREES | 1.000 | pitā mātrā | pitā mātrā |
| 1.2.71 | AGREES | 0.909 | śvaśuraḥ śvasravā | śvaśuraḥ śvaśrvā |
| 1.2.72 | AGREES | 1.000 | tyad-ādīni sarvair nityam | tyad-ādīni sarvair nityam |
| 1.2.73 | AGREES | 0.901 | grāmya-paśu-saṅgheṣv ataruṇeśu strī | grāmya-paśu-saṃgheṣu=a-taruṇeṣu strī |
| 1.3.1 | AGREES | 1.000 | bhūvādayo dhātavaḥ | bhūvādayo dhātavaḥ |
| 1.3.2 | AGREES | 0.913 | upadeśe 'j-anunāsika it | upadeśe=aC=anunāsika IT |
| 1.3.3 | AGREES | 1.000 | hal-antyam | haL antyam |
| 1.3.4 | AGREES | 0.950 | na vibhaktau tusmāḥ | na vibhaktau tU-s-māḥ |
| 1.3.5 | AGREES | 0.970 | ādir ñi-ṭu-ḍavaḥ | ādir ÑI-ṬU-ḌAV-aḥ |
| 1.3.6 | AGREES | 0.968 | ṣaḥ pratyayasaya | ṣaḥ pratyayasya |
| 1.3.7 | VARIANTS | 0.667 | duṭū | cU-ṭŪ |
| 1.3.8 | AGREES | 0.919 | la-śa-kv ataddhite | la-śa-kU=a-taddhite |
| 1.3.9 | AGREES | 1.000 | tasya lopaḥ | tasya lopaḥ |
| 1.3.10 | AGREES | 0.968 | yathā-saṅkhyam anudeśaḥ samānām | yathā-saṃkhyam anudeśaḥ samānām |
| 1.3.11 | AGREES | 1.000 | svaritena adhikāraḥ | svaritena=adhikāraḥ |
| 1.3.12 | AGREES | 0.960 | anudāttaṅita ātmanepadam | anudātta-Ṅ-ITa ātmanepadam |
| 1.3.13 | AGREES | 1.000 | bhāva-karmaṇoḥ | bhāva-karmaṇoḥ |
| 1.3.14 | AGREES | 0.933 | kartari karma-vyatihāre | kartari karma-vyatiare |
| 1.3.15 | AGREES | 1.000 | na gati-hiṃsā-arthebhyaḥ | na gati-hiṃsā=arthebhyaḥ |
| 1.3.16 | AGREES | 0.966 | itaretara-anyonya-upapadāc ca | itaretara=anyonya=upapadāt=ca |
| 1.3.17 | AGREES | 1.000 | ner viśaḥ | ner viśaḥ |
| 1.3.18 | AGREES | 0.933 | parivy-avebhyaḥ kriyaḥ | pari-vi=avebhyaḥ kriyaḥ |
| 1.3.19 | AGREES | 0.909 | viparābhyāṃ jeḥ | vi-parā-bhyāṃ je-ḥ |
| 1.3.20 | VARIANTS | 0.826 | aṅo do 'nāsya-viharaṇe | āṄo daḥ=an-āsya-viharaṇe |
| 1.3.21 | VARIANTS | 0.868 | krīḍo 'nu-saṃ-paribhyaś ca | krīḍaḥ=anu-sam-paribhyaś ca |
| 1.3.22 | VARIANTS | 0.894 | samavapravibhyaḥ sthaḥ | sam=ava-pra-vibhyaḥ shtaḥ |
| 1.3.23 | VARIANTS | 0.868 | prakāśana-stheya-ākhyahoś ca | prakāśana=stheya=ākhyayoḥ |
| 1.3.24 | VARIANTS | 0.857 | udo 'nūrdhva-karmaṇi | udaḥ=an-ūrdhva-karmaṇi |
| 1.3.25 | AGREES | 0.944 | upān mantra-karaṇe | upāt=mantra-karaṇe |
| 1.3.26 | VARIANTS | 0.880 | akarmakāc ca | a-karmakāt=ca |
| 1.3.27 | AGREES | 0.938 | ud-vibhyāṃ tapaḥ | ud-vibhyām tapaḥ |
| 1.3.28 | AGREES | 1.000 | āṅo yama-hanaḥ | āṄo yama-hanaḥ |
| 1.3.29 | AGREES | 0.940 | samo gamy-ṛcchi-pracchi-svaraty arti-śru-vidighyaḥ | samo gami=ṛcchi-pracchi-svarati=arti-śru-vidibhyaḥ |
| 1.3.30 | AGREES | 0.955 | ni-sam-upa-vibhyo hvaḥ | ni-sam-upa-vihhyo hvaḥ |
| 1.3.31 | AGREES | 1.000 | spardhāyām āṅaḥ | spardhāyām āṄaḥ |
| 1.3.32 | AGREES | 0.980 | gandhana-avakṣepaṇa-sevana-sāhasikya-pratithatna-prakathana-upayogeṣu kṛñaḥ | gandhana=avakṣepaṇa-sevana-sāhasikya-pratiyatna-prakathana=upayogeṣu kṛÑaḥ |
| 1.3.33 | AGREES | 1.000 | adheḥ prasahane | adheḥ prasahane |
| 1.3.34 | AGREES | 1.000 | veḥ śabda-karmaṇaḥ | veḥ śabda-karmaṇaḥ |
| 1.3.35 | AGREES | 0.917 | akarmakāc ca | akarmakāt=ca |
| 1.3.36 | AGREES | 1.000 | sammānana-utsañjana-ācāryakaraṇa-jñāna-bhṛti-vigaṇana-vyayeṣu niyaḥ | sammānana=utsañjana=ācāryakaraṇa-jñāna-bhṛti-vigaṇana-vyayeṣu niyaḥ |
| 1.3.37 | AGREES | 0.964 | kartṛsthe ca śarīre karmaṇi | kartṛsthe ca=a-śarīre karmaṇi |
| 1.3.38 | AGREES | 0.982 | vṛtti-sarga-tāyaneṣu kramaḥ | vṛtti-sarga-tātyaneṣu kramaḥ |
| 1.3.39 | AGREES | 1.000 | upa-parābhyām | upa-parābhyām |
| 1.3.40 | AGREES | 1.000 | āṅa udgamane | āṄa udgamane |
| 1.3.41 | AGREES | 1.000 | veḥ pāda-viharaṇe | veḥ pāda-viharaṇe |
| 1.3.42 | AGREES | 0.926 | pra-upābhyāṃ samarthābhyām | pra=upābhyām sam-arthā-bhyām |
| 1.3.43 | AGREES | 0.966 | anupasargād vā | an-upasargād vā |
| 1.3.44 | AGREES | 1.000 | apahnave jñaḥ | apahnave jñaḥ |
| 1.3.45 | AGREES | 0.917 | akarmakāc ca | a-karmakā=ca |
| 1.3.46 | AGREES | 0.920 | saṃ-pratibhyām anādhyāne | sam-pratibhyām an-ā-dhyāne |
| 1.3.47 | AGREES | 0.983 | bhāsana-upasambhāṣā-jñāna-yatna-vimaty-upamantraṇeṣu vadaḥ | bhāsana=upasambhāṣā-jñāna-yatna-vimati-upamantraṇeṣu vadaḥ |
| 1.3.48 | AGREES | 0.957 | vyaktavācāṃ samuccāraṇe | vyaktavācām samuccāraṇe |
| 1.3.49 | AGREES | 0.966 | anor akarmakāt | anor a-karmakāt |
| 1.3.50 | AGREES | 0.944 | vibhāṣā vipralāpe | vibhāṣā vi-pra-lāpe |
| 1.3.51 | AGREES | 1.000 | avād graḥ | avād graḥ |
| 1.3.52 | AGREES | 1.000 | samaḥ pratijñāne | samaḥ pratijñāne |
| 1.3.53 | AGREES | 0.977 | udaś caraḥ sakarmakāt | udaś caraḥ sa-karmakāt |
| 1.3.54 | AGREES | 0.919 | saṃs tṛtīyā-yuktāt | samas tṛtīyā-yuktāt |
| 1.3.55 | AGREES | 0.915 | dāṇaś ca sā cec caturthy-arthe | dāṆas ca sā cet=caturty-arthe |
| 1.3.56 | AGREES | 0.927 | upād yamaḥ svakarane | upād yamaḥ sva-karaṇe |
| 1.3.57 | AGREES | 0.957 | jñā-śru-smṛ-dṛśāṃ sanaḥ | jñā-śru-smṛ-dṛśām saNaḥ |
| 1.3.58 | AGREES | 1.000 | na anor jñaḥ | na=anor jñaḥ |
| 1.3.59 | AGREES | 0.900 | praty-āṅbhyāṃ śruvaḥ | prati=āṄbhyām śruvaḥ |
| 1.3.60 | AGREES | 0.917 | śadeḥ śitaḥ | śadeḥ Ś-IT-aḥ |
| 1.3.61 | AGREES | 1.000 | mriyater luṅ-liṅoś ca | mriyater lUṄ-lIṄoś ca |
| 1.3.62 | AGREES | 1.000 | pūrvavat sanaḥ | pūrvavat saNaḥ |
| 1.3.63 | AGREES | 0.925 | ām-pratyayavat kṛño 'nuprayogasya | ām-pratyayavat kṛÑaḥ=anuprayogasya |
| 1.3.64 | AGREES | 0.985 | pra-upābhyāṃ yujer ayajña-pātreṣu | pra=upābhyāṃ yujer a-yajña-pātreṣu |
| 1.3.65 | AGREES | 1.000 | samaḥ kṣṇuvaḥ | samaḥ kṣṇuvaḥ |
| 1.3.66 | VARIANTS | 0.786 | bhujo 'navane | bhujaḥ=an-avane |
| 1.3.67 | AGREES | 0.956 | ṇe raṇau yat karma ṇau cet sa kartā 'nādhyāne | Ṇer aṆau yat karma Ṇau cet sa kartā anādhyāne |
| 1.3.68 | AGREES | 0.974 | bhī-smyor hetubhaye | bhī-smyor hetu-bhaye |
| 1.3.69 | AGREES | 0.920 | gṛdhi-vañcyoḥ pralambhane | gṛdhi-vancyoh pralambhane |
| 1.3.70 | AGREES | 0.914 | liyaḥ saṃmānana-śālīnīkaraṇayoś ca | liyaḥ sam-mānana-śālinī-karaṇayoś ca |
| 1.3.71 | AGREES | 0.906 | mithyopapadāt kṛño 'bhyāse | mithyopapadāt kṛÑaḥ=abhyāse |
| 1.3.72 | AGREES | 0.976 | svarita-ñitaḥ kartr-abhiprāye kriyāphale | svarita-Ñ-ITaḥ kartr=abhiprāye kriyā-phale |
| 1.3.73 | AGREES | 1.000 | apād vadaḥ | apād vadaḥ |
| 1.3.74 | AGREES | 1.000 | ṇicaś ca | ṆiCaś ca |
| 1.3.75 | VARIANTS | 0.821 | sam-ud-āṅbhyo yamo 'granthe | sam-ud=āṄbhyah=amaḥ=a-granthe |
| 1.3.76 | AGREES | 0.909 | anupasargāj jñaḥ | an-upasargāt=jñaḥ |
| 1.3.77 | AGREES | 1.000 | vibhāṣā-upapadena pratīyamāne | vibhāṣā=upapadena pratīyamāne |
| 1.3.78 | AGREES | 1.000 | śeṣāt kartari parasmaipadam | śeṣāt kartari parasmaipadam |
| 1.3.79 | AGREES | 1.000 | anu-parābhyāṃ kṛñaḥ | anu-parābhyāṃ kṛÑaḥ |
| 1.3.80 | AGREES | 0.962 | abhi-praty-atibhyaḥ kṣipaḥ | abhi-prati=atibhyaḥ kṣipaḥ |
| 1.3.81 | AGREES | 0.947 | prādvahaḥ | prād vahaḥ |
| 1.3.82 | AGREES | 1.000 | parer mṛṣaḥ | parer mṛṣaḥ |
| 1.3.83 | VARIANTS | 0.878 | vy-āṅ-paribhyo ramaḥ | vi-āṄ-paribhyaḥ=ramaḥ |
| 1.3.84 | VARIANTS | 0.857 | upāc ca | upāt=ca |
| 1.3.85 | VARIANTS | 0.857 | vibhāśā 'karmakāt | vibhāṣā=a-karmakāt |
| 1.3.86 | AGREES | 0.955 | budha-yudha-naśa-jana-iṅ-pru-dru-srubhyo ṇeḥ | budhḥ-yudhA-naśḥ-jana-iṄ-pru-dru-srubhyo Ṇeḥ |
| 1.3.87 | AGREES | 0.909 | nigaraṇa-calana-arthebhyaś ca | nigaraṇa-calana=arthebhyaḥ |
| 1.3.88 | VARIANTS | 0.892 | aṇāv akarmakāc cittavat-kartṛkāt | aṆau=a-karmakāt=cittavat-kartṛkāt |
| 1.3.89 | AGREES | 0.945 | na pādamy-āṅyama-āṅyasa-parimuha-ruci-nṛti-vada-vasaḥ | na pā-dami=āṄ-yamA-āṄ-yasa-pari-muha-ruci-nṛti-vadA-vasaḥ |
| 1.3.90 | AGREES | 1.000 | vā kyaṣaḥ | vā KyaṢaḥ |
| 1.3.91 | AGREES | 0.923 | dhydbhyo luṅi | dyudbhyo lUṄi |
| 1.3.92 | AGREES | 0.971 | vṛdbhyaḥ syasanoḥ | vṛdbhyaḥ sya-saNoḥ |
| 1.3.93 | VARIANTS | 0.857 | luṭi ca klupaḥ | lUṬi ca kḷp-aḥ |
| 1.4.1 | VARIANTS | 0.872 | ā kaḍārādekā sañjñā | ā kaḍārāt=ekā saṃjñā |
| 1.4.2 | AGREES | 0.960 | vipratiṣedhe paraṃ kāryam | vipratiṣedhe param kāryam |
| 1.4.3 | VARIANTS | 0.895 | yū stry-ākhyau nadī | yū strī=akhyau nadī |
| 1.4.4 | AGREES | 0.906 | na-iyaṅ-uvaṅ-sthānāv astrī | na=iyaṄ=uvaṄ-sthānau=a-strī |
| 1.4.5 | VARIANTS | 0.833 | va+āmi | vā=āmi |
| 1.4.6 | AGREES | 0.968 | ṅiti hrasvaś ca | ṄIT-i hrasvaś ca |
| 1.4.7 | VARIANTS | 0.867 | śeṣo ghyasakhi | śeṣo GHI=a-sakhi |
| 1.4.8 | AGREES | 0.938 | patiḥ samāsa eva | patiḥ samāse=eva |
| 1.4.9 | AGREES | 1.000 | ṣaṣṭhī-yuktaś chandasi vā | ṣaṣṭhī-yuktaś chandasi vā |
| 1.4.10 | AGREES | 0.923 | hrasvaṃ laghu | hrasvam laghu |
| 1.4.11 | AGREES | 1.000 | saṃyoge guru | saṃyoge guru |
| 1.4.12 | AGREES | 1.000 | dīrghaṃ ca | dīrghaṃ ca |
| 1.4.13 | AGREES | 0.956 | yasmāt pratyaya-vidhis tad-ādi pratyaye 'ṅgam | yasmāt pratyaya-vidhis tad-ādi pratyaye=aṛgam |
| 1.4.14 | AGREES | 0.947 | sup-tiṅ-antaṃ padam | sUP-tiṄ=antam padam |
| 1.4.15 | AGREES | 1.000 | naḥ kye | naḥ Kye |
| 1.4.16 | VARIANTS | 0.875 | siti ca | S-IT-i ca |
| 1.4.17 | AGREES | 0.902 | svādiṣv a-sarvanamasthāne | sḥ=ādiṣu=a-sarvanamasthāne |
| 1.4.18 | AGREES | 0.947 | yaci bham | y-aCi BHAm |
| 1.4.19 | AGREES | 0.909 | tasau matv-arthe | ta-sau matU=arthe |
| 1.4.20 | AGREES | 1.000 | ayasmaya-ādīni chandasi | ayasmaya=ādīni chandasi |
| 1.4.21 | AGREES | 0.973 | bahuṣu bahuvacanam | bahuṣu bahu-vacanam |
| 1.4.22 | AGREES | 0.903 | dvy-ekayor dvibacana-ekavacane | dvi=ekayor dvi-vacana=eka-vacane |
| 1.4.23 | AGREES | 1.000 | kārake | kārake |
| 1.4.24 | AGREES | 0.930 | dhruvamapāye 'pādānam | dhruvam apāye=apādānam |
| 1.4.25 | AGREES | 0.964 | bhī-trā-arthānāṃ bhaya-hetuḥ | bhī-trā-arthānām bhaya-hetuḥ |
| 1.4.26 | AGREES | 0.970 | parā-jer asoḍhaḥ | parā-jer a-soḍhaḥ |
| 1.4.27 | AGREES | 1.000 | vāraṇa-arthānām īpsitaḥ | vāraṇa=arthānām īpsitaḥ |
| 1.4.28 | AGREES | 0.985 | antardhau yena adarśanam icchati | antardhau yena a-darśanam icchati |
| 1.4.29 | AGREES | 1.000 | ākhyātā-upayoge | ākhyātā=upayoge |
| 1.4.30 | AGREES | 1.000 | jani-kartuḥ prakṛtiḥ | jani-kartuḥ prakṛtiḥ |
| 1.4.31 | AGREES | 1.000 | bhuvaḥ prabhavaḥ | bhuvaḥ prabhavaḥ |
| 1.4.32 | AGREES | 0.987 | karmaṇā yam abhipraiti sa sampradānam | karmaṇā yam abhi-praiti sa sampradānam |
| 1.4.33 | AGREES | 0.958 | rucy-arthānām prīyamāṇaḥ | ruci=arthānām prīyamāṇaḥ |
| 1.4.34 | AGREES | 0.971 | ślāgha-hnuṅ-sthā-śapāṃ jñīpsyamānaḥ | ślāgha-hnuṄ-sthā-śapām jñīpsyamānaḥ |
| 1.4.35 | AGREES | 1.000 | dhārer uttamarṇaḥ | dhārer uttamarṇaḥ |
| 1.4.36 | AGREES | 1.000 | spṛher īpsitaḥ | spṛher īpsitaḥ |
| 1.4.37 | CONFLICTS | 0.597 | krudha-druha-īrṣya-asūya-arthānāṃ yaṃ prati kopaḥ | krudhḥ-druhḥ-īrṣyḥ=asūyān ām |
| 1.4.38 | AGREES | 0.952 | krudha-druhor upasṛṣṭhayoḥ karma | krudhḥ-druhor upasṛṣṭayoḥ karma |
| 1.4.39 | AGREES | 0.963 | rādḥ-īkṣyor yasya vipraśnaḥ | rādh-īkṣyor yasya vipraśnaḥ |
| 1.4.40 | AGREES | 0.971 | praty-āṅbhyāṃ śruvaḥ pūrvasya kartā | prati=āṄbhyāṃ śruvaḥ pūrvasya kartā |
| 1.4.41 | AGREES | 1.000 | anu-prati-gṛṇaś ca | anu-prati-gṛṇaś ca |
| 1.4.42 | AGREES | 0.950 | sādhakatamaṃ karaṇam | sādhakatamam karaṇam |
| 1.4.43 | AGREES | 1.000 | divaḥ karma ca | divaḥ karma ca |
| 1.4.44 | AGREES | 0.959 | parikrayaṇe sampradānam anyatarasyām | pari-krayaṇe sampradānan anyatarasyām |
| 1.4.45 | VARIANTS | 0.865 | ādhāro 'dhikaraṇam | ādhāraḥ=adhikaraṇam |
| 1.4.46 | AGREES | 1.000 | adhi-śīṅ-sthā-āsāṃ karma | adhi-śīṄ-sthā=āsāṃ karma |
| 1.4.47 | AGREES | 0.933 | abhiniviśaś ca | abhi-ni-viśaś ca |
| 1.4.48 | VARIANTS | 0.878 | upa-anv-adhy-āṅ-vasaḥ | upa=anu=adhi-āṄ-asaḥ |
| 1.4.49 | AGREES | 0.939 | kartrur īpsitatamaṃ karma | kartur īpsitatamam karma |
| 1.4.50 | AGREES | 0.902 | tathā-yuktaṃ ca anīpsitam | tathā-yuktaṃ ca=an-ipsītam |
| 1.4.51 | AGREES | 0.960 | akathitaṃ ca | a-kathitaṃ ca |
| 1.4.52 | AGREES | 0.979 | guti-buddhi-pratyavasāna-artha-śabda-karma-akarmakāṇām aṇi kartā sa ṇau | gati-buddhi-pratyavasāna=artha-śabda-karma=a-karmakāṇām aṆi kartā sa Ṇau |
| 1.4.53 | AGREES | 1.000 | hṛ-kror anyatarasyām | hṛ-kror anyatarasyām |
| 1.4.54 | AGREES | 1.000 | svatantraḥ kartā | svatantraḥ kartā |
| 1.4.55 | AGREES | 1.000 | tat-prayojako hetuś ca | tat-prayojako hetuś ca |
| 1.4.56 | VARIANTS | 0.762 | prāg-rīśvarān nipātāḥ | prāk=iśvarāt=nipā taḥ |
| 1.4.57 | AGREES | 0.909 | ca-ādayo 'sattve | ca=ādayo=a-sattve |
| 1.4.58 | AGREES | 1.000 | pra-ādayaḥ | pra=ādayaḥ |
| 1.4.59 | AGREES | 1.000 | upasargāḥ kriyā-yoge | upasargāḥ kriyā-yoge |
| 1.4.60 | AGREES | 1.000 | gatiś ca | gatiś ca |
| 1.4.61 | AGREES | 0.950 | ūry-ādi-cvi-ḍācaś ca | ūrī=ādi-Cvi-ḌāCaś ca |
| 1.4.62 | AGREES | 0.941 | anukaraṇaṃ ca aniti-param | anukaraṇam ca=an=iti-param |
| 1.4.63 | AGREES | 0.926 | ādara-anādarayoḥ sad-asatī | ādara=an-ādarayoḥ sat-asat-ī |
| 1.4.64 | VARIANTS | 0.833 | bhūṣane 'lam | bhūṣaṇe=alam |
| 1.4.65 | AGREES | 0.970 | antar aparigrahe | antar a-parigrahe |
| 1.4.66 | AGREES | 0.984 | kaṇe-manasī śraddhā-pratīghāte | kaṇe-manas-ī śraddhā-pratīghāte |
| 1.4.67 | VARIANTS | 0.800 | puro 'vyayam | puras=avyayam |
| 1.4.68 | AGREES | 1.000 | astaṃ ca | astaṃ ca |
| 1.4.69 | AGREES | 0.957 | accha gaty-artha-vadeṣu | accha gati=artha-vadeṣu |
| 1.4.70 | VARIANTS | 0.759 | ado 'nupadeśe | adaḥ=an-upa-deśe |
| 1.4.71 | VARIANTS | 0.759 | taro 'ntardhau | tiraḥ=antardhau |
| 1.4.72 | AGREES | 0.960 | vibhāṣā kṛñi | vibhāṣā kṛÑ-i |
| 1.4.73 | AGREES | 0.917 | upāje 'nvāje | upāje=anvāje |
| 1.4.74 | AGREES | 1.000 | sākṣāt-prabhṛtīni ca | sākṣāt-prabhṛtīni ca |
| 1.4.75 | AGREES | 0.939 | anatyādhāna urasi-manasī | an-atyādhāne=urasi-manasī |
| 1.4.76 | AGREES | 1.000 | madhye pade nivacane ca | madhye-pade-nivacane ca |
| 1.4.77 | VARIANTS | 0.893 | nityaṃ haste pānāv-upayamane | nityaṃ haste pāṇau=upayamane |
| 1.4.78 | VARIANTS | 0.882 | prādhvaṃ vandhane | prādhvam bandhane |
| 1.4.79 | AGREES | 0.920 | jīvikā-upaniṣadāv aupamye | jīvikā-upaniṣadau=aupamye |
| 1.4.80 | AGREES | 0.929 | te prāg dhātoḥ | te prāg dhātoh |
| 1.4.81 | AGREES | 0.941 | chandasi pare 'pi | chandasi pare=api |
| 1.4.82 | AGREES | 1.000 | vyavahitāś ca | vyavahitāś ca |
| 1.4.83 | AGREES | 0.971 | karmapravacanīyāḥ | karma-pravacanīyāḥ |
| 1.4.84 | AGREES | 1.000 | anur lakṣaṇe | anur lakṣaṇe |
| 1.4.85 | AGREES | 1.000 | tṛtīyā-arthe | tṛtīyā=arthe |
| 1.4.86 | AGREES | 1.000 | hīne | hīne |
| 1.4.87 | VARIANTS | 0.815 | upo 'dhike ca | upaḥ=adhike ca |
| 1.4.88 | AGREES | 1.000 | apa-parī varjane | apa-parī varjane |
| 1.4.89 | AGREES | 1.000 | āṅ maryādā-vacane | āṄ maryādā-vacane |
| 1.4.90 | AGREES | 0.950 | lakṣana-itthaṃ-bhūta-ākhyāna-bhāga-vīpsāsu prati-pary-anavaḥ | lakṣaṇa=ittham-bhūta=ākhyāna-bhāga-vīpsāsu prati-pari-anavaḥ |
| 1.4.91 | AGREES | 0.960 | abhir abhāge | abhir a-bhāge |
| 1.4.92 | AGREES | 1.000 | pratiḥ pratinidhi-pratidānayoḥ | pratiḥ pratinidhi-pratidānayoḥ |
| 1.4.93 | AGREES | 0.974 | adhiparī anarthakau | adhi-parī anarthakau |
| 1.4.94 | AGREES | 1.000 | suḥ pūjāyām | suḥ pūjāyām |
| 1.4.95 | AGREES | 1.000 | atir atikramaṇe ca | atir atikramaṇe ca |
| 1.4.96 | AGREES | 1.000 | apiḥ padārtha-sambhāvana-anvavasarga-garhā-samuccayeṣu | apiḥ padārtha-sambhāvana=anvavasarga-garhā-samuccayeṣu |
| 1.4.97 | AGREES | 1.000 | adhir īśvare | adhir īśvare |
| 1.4.98 | AGREES | 0.960 | vibhāṣā kṛñi | vibhāṣā kṛÑ-i |
| 1.4.99 | AGREES | 1.000 | laḥ parasmaipadam | laḥ parasmaipadam |
| 1.4.100 | VARIANTS | 0.850 | taṅ-ānāv ātmanepadam | taṄ-āmau=ātmanepadam |
| 1.4.101 | AGREES | 1.000 | tiṅas trīṇi trīṇi prathama-madhyama-uttamāḥ | tiṄas trīṇi trīṇi prathama-madhyama=uttamāḥ |
| 1.4.102 | VARIANTS | 0.897 | tāny ekavacanād vivacanabahuvacanāny ekaśaḥ | tāni=ekavacana-dvivacana-bahuvacanāni ekaśaḥ |
| 1.4.103 | AGREES | 1.000 | supaḥ | sUpaḥ |
| 1.4.104 | AGREES | 1.000 | vibhaktiś ca | vibhaktiś ca |
| 1.4.105 | AGREES | 0.973 | yuṣmady-upapade samāna-adhikaraṇe sthāniny api madhyamaḥ | yuṣmadi=upapade samāna=dhikaraṇe sthāniny=api madhyamaḥ |
| 1.4.106 | AGREES | 0.980 | prahāse ca manya-upapade manyater uttama ekavac ca | prahāse ca manya=upapade manyater uttama ekavat=ca |
| 1.4.107 | AGREES | 1.000 | asmady uttamaḥ | asmady uttamaḥ |
| 1.4.108 | AGREES | 1.000 | śeṣe prathamaḥ | śeṣe prathamaḥ |
| 1.4.109 | AGREES | 1.000 | paraḥ saṃnikarṣaḥ saṃhitā | paraḥ saṃnikarṣaḥ saṃhitā |
| 1.4.110 | VARIANTS | 0.839 | virāmo 'vasānam | virāmaḥ avasānam |
| 2.1.1 | AGREES | 0.976 | samarthaḥ padavidhiḥ | samarthaḥ pada-vidhiḥ |
| 2.1.2 | AGREES | 0.938 | sub āmantrite para-aṅgavat svare | sUP āmantrite para=aṛgavat svare |
| 2.1.3 | AGREES | 1.000 | prāk kaḍārāt samāsaḥ | prāk kaḍārāt samāsaḥ |
| 2.1.4 | AGREES | 0.947 | saha supā | saha sUP-ā |
| 2.1.5 | VARIANTS | 0.880 | avyayībhavaḥ | avyayī-bhāvaḥ |
| 2.1.6 | AGREES | 0.956 | avyayaṃ vibhakti-samīpa-samṛddhi-vyṛddhy-arthābhāva-atyaya-asamprati-śabdaprādurbhāva-paścād-yathā-ānupūrvya-yaugapadya-sādṛśya-sampatti-sākalya-antavcaneṣu | avyayam vibhakti-samīpa-samṛddhi-vy-ṛddhi-artha=abhāva=atyaya-a-samprati-śabda-prādurbhāva-paścāt=yathā=ānupūrvya-yaugapadya-sādṛśya-sampatti-sākalya=antavacaneṣu |
| 2.1.7 | VARIANTS | 0.857 | yathā 'sādṛśye | yathā=a-sādṛye |
| 2.1.8 | AGREES | 1.000 | yāvad avadhāraṇe | yāvad avadhāraṇe |
| 2.1.9 | AGREES | 0.957 | sup praitnā mātrā-arthe | sUP pratinā mātrā=arthe |
| 2.1.10 | AGREES | 0.963 | akṣa-śalākā-saṅkhyāḥ pariṇā | akṣa-śalākā-saṃkhyāḥ pariṇā |
| 2.1.11 | AGREES | 1.000 | vibhāṣā | vibhāṣā |
| 2.1.12 | AGREES | 0.968 | apa-pari-bahir añcavaḥ pañcamyā | apa-pari-bahis=añcavaḥ pañcamyā |
| 2.1.13 | AGREES | 0.977 | āṅ maryādā-abhividhyoḥ | āṄ maryādāabhividhyoḥ |
| 2.1.14 | AGREES | 0.984 | lakṣaṇena abhipratī ābhimukhye | lakṣaṇena=abhi-pratī=ābhimukhye |
| 2.1.15 | AGREES | 1.000 | anur yat-samayā | anur yat-samayā |
| 2.1.16 | AGREES | 1.000 | yasya ca āyāmaḥ | yasya ca=āyāmaḥ |
| 2.1.17 | AGREES | 0.979 | tiṣṭhadgu-prabhṛtīni ca | tiṣṭhad-gu-prabhṛtīni ca |
| 2.1.18 | AGREES | 1.000 | pāre madhye ṣaṣṭhyā vā | pāre madhye ṣaṣṭhyā vā |
| 2.1.19 | AGREES | 0.938 | saṅkhyā vaṃśyena | saṃkhyā vaṃśyena |
| 2.1.20 | AGREES | 1.000 | nadībhiś ca | nadībhiś ca |
| 2.1.21 | AGREES | 0.902 | anyapadarthe ca sañjñāyām | anya-padārthe ca saṃjñāyām |
| 2.1.22 | AGREES | 1.000 | tatpuruṣaḥ | tatpuruṣaḥ |
| 2.1.23 | AGREES | 1.000 | dviguś ca | dviguś ca |
| 2.1.24 | AGREES | 0.972 | dvidīyā śrita-atīta-patita-gata-atyasta-prāpta-āpanaiḥ | dvitīyā śrita=atīta=patita-gata=atyasta-prāpta=āpannaiḥ |
| 2.1.25 | AGREES | 1.000 | svayaṃ ktena | svayaṃ Ktena |
| 2.1.26 | AGREES | 1.000 | khaṭvā kṣepe | khaṭvā kṣepe |
| 2.1.27 | AGREES | 1.000 | sāmi | sāmi |
| 2.1.28 | AGREES | 1.000 | kālāḥ | kālāḥ |
| 2.1.29 | AGREES | 0.971 | atyantasaṃyoge ca | atyanta-saṃyoge ca |
| 2.1.30 | AGREES | 0.972 | tṛtīyā tatkṛta-arthena guṇavacanena | tṛtīyā tat-kṛta=arthena guṇa-vacanena |
| 2.1.31 | AGREES | 0.964 | pūrva-sadṛśa-sama-ūnārtha-kalaha-nipuṇa-miśra-ślakṣṇaiḥ | pūrva-sadṛśa-sama=ūna=artha-kalaha-nipuṇa-miśra-ślakṣṇaiḥ |
| 2.1.32 | AGREES | 0.917 | kartṛkarṇe dṛtā bahulam | kartṛ-karaṇe kṛtā bahulam |
| 2.1.33 | AGREES | 1.000 | kṛtyair adhika-ārtha-vacane | kṛtyair adhika=ārtha-vacane |
| 2.1.34 | AGREES | 1.000 | annena vyañjanam | annena vyañjanam |
| 2.1.35 | AGREES | 0.909 | bhakṣyeṇa miśrīkaranam | bhakśyeṇa miśrīkaraṇam |
| 2.1.36 | AGREES | 0.990 | caturthī tadartha-artha-bali-hita-sukha-rakṣitaiḥ | caturthī tad-artha=artha-bali-hita-sukha-rakṣitaiḥ |
| 2.1.37 | AGREES | 1.000 | pañcamī bhayena | pañcamī bhayena |
| 2.1.38 | AGREES | 1.000 | apeta-apoḍha-mukta-patita-apatrastair alpaśaḥ | apeta=apoḍha-mukta-patita=apatrastair alpaśaḥ |
| 2.1.39 | AGREES | 1.000 | stoka-antika-dūra-artha-kṛcchrāṇi ktena | stoka=antika-dūra=artha-kṛcchrāṇi Ktena |
| 2.1.40 | AGREES | 1.000 | saptamī śauṇḍaiḥ | saptamī śauṇḍaiḥ |
| 2.1.41 | AGREES | 1.000 | siddha-śuṣka-pakva-bandhaiś ca | siddha-śuṣka-pakva-bandhaiś ca |
| 2.1.42 | VARIANTS | 0.875 | dhvāṅkṣena kṣepe | dhvāṛkṣeṇa kṣepe |
| 2.1.43 | AGREES | 0.909 | krtyair ṛṇe | kṛtyair ṛṇe |
| 2.1.44 | VARIANTS | 0.889 | sañjñāyām | saṃjñāyām |
| 2.1.45 | AGREES | 1.000 | ktena aho-rātra-avayavāḥ | Ktena=aho-rātra=avayavāḥ |
| 2.1.46 | AGREES | 1.000 | tatra | tatra |
| 2.1.47 | AGREES | 1.000 | kṣepe | kṣepe |
| 2.1.48 | AGREES | 0.930 | pātresamita-ādayaś ca | pātre-samita=ādayas=ca |
| 2.1.49 | AGREES | 0.953 | pūrvakāla-eka-sarva-jarat-purāṇā-nava-kevalāḥ samānādhikaraṇena | pūrva-kāla=eka-sarva-jarat-purāṇa-nava-kevalāḥ samāna=dhikaraṇena |
| 2.1.50 | AGREES | 0.905 | dik-saṅkhye sañjñāyām | dik-saṃkhye saṃjñāyām |
| 2.1.51 | AGREES | 0.959 | taddhitartha-uttarapada-samāhāre ca | taddhita=artha-uttara-pada-samāhāre ca |
| 2.1.52 | AGREES | 0.950 | saṅkhyā-pūrvo dviguḥ | saṃkhyā-pūrvo dviguḥ |
| 2.1.53 | AGREES | 0.974 | kutsitāni kutsanaiḥ | kutsitānai kutsanaiḥ |
| 2.1.54 | VARIANTS | 0.895 | pāpāṇake kutsitaiḥ | pāpa=aṇake kutsitaiḥ |
| 2.1.55 | AGREES | 0.981 | upamānāni sāmānya-vacanaiḥ | upamānāni sāmānaya-vacanaiḥ |
| 2.1.56 | AGREES | 0.940 | upamitaṃ vyāghra-ādibhiḥ sāmānya-aprayoge | upamitam vyāghra=ābibhiḥ sāmānya=a-prayoge |
| 2.1.57 | VARIANTS | 0.889 | viśesanaṃ viśeṣyeṇa bahulam | viśeṣaṇam viśeṣyeṇa bahulam |
| 2.1.58 | AGREES | 1.000 | pūrva-apara-prathama-carama-jaghanya-samāna-madhya-madhyama-vīrāś ca | pūrva=apara-prathama-carama-jaghanya-samāna-madhya-madhyama-vīrāś ca |
| 2.1.59 | AGREES | 0.960 | śreṇy-ādayaḥ kṛta-ādibhiḥ | śreṇi=ādayaḥ kṛta=ādibhiḥ |
| 2.1.60 | AGREES | 0.980 | ktena nañ-viśiṣṭena anañ | Ktena naÑ-viśiṣṭena=a-naÑ |
| 2.1.61 | AGREES | 0.932 | san-mahat-parama-uttama-utkṛṣṭāḥ pūjyamānaiḥ | sat=mahat-parama=uttama=utkrṣṭāḥ pūjyamanaiḥ |
| 2.1.62 | AGREES | 0.971 | vṛndaraka-nāga-kuñjaraiḥ pūjyamānam | vṛndāraka-nāga-kuñjaraiḥ pūjyamānam |
| 2.1.63 | AGREES | 0.967 | katara-katamau jātiparipraśne | katara-katamau jāti-pari-praśne |
| 2.1.64 | AGREES | 1.000 | kiṃ kṣepe | kiṃ kṣepe |
| 2.1.65 | AGREES | 0.990 | poṭā-yuvati-stoka-katipaya-gṛṣṭi-dhenu-vaśā-vehad-baṣkayaṇī-pravaktṛ-śrotriya-adhyāpaka-dhūrtair jātiḥ | poṭā-yuvati-stoka-katipaya-gṛṣṭi-dhenu-vaśā-vehat-baṣkayaṇī-pravaktṛ-śrotriya=adhyāpaka-dhūrtair jātiḥ |
| 2.1.66 | AGREES | 1.000 | praśaṃsā-vacanaiś ca | praśaṃsā-vacanaiś ca |
| 2.1.67 | AGREES | 0.973 | yuvā khalati-pālita-valina-jaratībhiḥ | yuvā khalati-palita-valina-jaratībhiḥ |
| 2.1.68 | AGREES | 0.980 | kṛtya-tulya-ākhyā ajātyā | kṛtya-tulya=ākhyā a-jātyā |
| 2.1.69 | AGREES | 1.000 | varṇo varṇena | varṇo varṇena |
| 2.1.70 | AGREES | 1.000 | kumāraḥ śramaṇā-ādibhiḥ | kumāraḥ śramaṇā=ādibhiḥ |
| 2.1.71 | AGREES | 1.000 | catuṣpādo garbhiṇyā | catuṣpādo garbhiṇyā |
| 2.1.72 | AGREES | 1.000 | mayūra-vyaṃsaka-ādayaś ca | mayūra-vyaṃsaka=ādayaś ca |
| 2.2.1 | AGREES | 0.949 | pūrva-apara-adhara-uttaram ekadeśinā-ekādhikaraṇe | pūrva=apara=adh ara=uttaram ekadeśinā=ka=dhikaraṇe |
| 2.2.2 | AGREES | 0.941 | ardhaṃ napuṃsakam | ardham napuṃsakam |
| 2.2.3 | AGREES | 0.943 | dvitiya-tṛtīya-caturtha-turyāṇy anytarasyām | dvitīya-tṛtīya-caturtha-turyāṇi anyatarasyām |
| 2.2.4 | AGREES | 0.960 | prāptāpanne ca dvitīyayā | prāpta=āpanne ca dvitīyayā |
| 2.2.5 | AGREES | 0.970 | kālāḥ parimāṇinā | kālāḥ partimāṇinā |
| 2.2.6 | AGREES | 1.000 | nañ | naÑ |
| 2.2.7 | VARIANTS | 0.762 | īṣadakṛtā | īṣat=a-kṛt-ā |
| 2.2.8 | AGREES | 1.000 | ṣaṣṭhī | ṣaṣṭhī |
| 2.2.9 | AGREES | 1.000 | yājaka-ādibhiś ca | yājaka=ādibhiś ca |
| 2.2.10 | AGREES | 1.000 | na nirdhāraṇe | na nirdhāraṇe |
| 2.2.11 | AGREES | 0.906 | pūraṇa-guṇa-suhitārtha-sad-avyaya-tavya-samānādhikaranena | pūraṇa-guṇa-suhita=artha-SAT=avyaya-tavya-samāna=dhikaraṇena |
| 2.2.12 | AGREES | 0.970 | kten a ca pūjāyām | Ktena ca pūjāyām |
| 2.2.13 | AGREES | 1.000 | adhikaraṇa-vācinā ca | adhikaraṇa-vācinā ca |
| 2.2.14 | AGREES | 1.000 | karmaṇi ca | karmaṇi ca |
| 2.2.15 | AGREES | 0.900 | tṛj-akābhyāṃ kartari | tṛC=akābhyām kartari |
| 2.2.16 | AGREES | 1.000 | kartari ca | kartari ca |
| 2.2.17 | AGREES | 1.000 | nityaṃ krīḍā-jīvikayoḥ | nityaṃ krīḍā-jīvikayoḥ |
| 2.2.18 | AGREES | 1.000 | ku-gati-pra-ādayaḥ | ku-gati-pra=ādayaḥ |
| 2.2.19 | AGREES | 0.963 | upapadam atiṅ | upapadam a-tiṄ |
| 2.2.20 | AGREES | 1.000 | amā-eva avyayena | amā=eva=avyayena |
| 2.2.21 | VARIANTS | 0.893 | tṛtīyā-prabhṛtīnyatarasyam | tṛtīyā-prabhṛtīni=anyatarasyām |
| 2.2.22 | AGREES | 1.000 | ktvā ca | Ktvā ca |
| 2.2.23 | AGREES | 1.000 | śeṣo bahuvrīhiḥ | śeṣo bahuvrīhiḥ |
| 2.2.24 | VARIANTS | 0.878 | anekam anyapadārthe | anekam anya-pada=arthe |
| 2.2.25 | AGREES | 0.927 | saṅkhyayā 'vyaya-āsanna-adūra-adhika-saṅkhyāḥ saṅkhyeye | saṃkhyayā=avyaya=āsanna=adūra=adhika-saṃkhyāḥ saṃkhyeye |
| 2.2.26 | AGREES | 0.919 | diṅnāmāny antarāle | diṛ-nāmāny antarāle |
| 2.2.27 | AGREES | 1.000 | tatra tena+idam iti sarūpe | tatra tena=idam iti sarūpe |
| 2.2.28 | AGREES | 0.979 | tena saha+iti tulyayoge | tena saha=iti tulya-yoge |
| 2.2.29 | AGREES | 0.941 | ca-arthe dvandvaḥ | ca=arthe dvaṃdvaḥ |
| 2.2.30 | AGREES | 0.944 | upasarjanaṃ pūrvam | upasarjanam pūrvam |
| 2.2.31 | AGREES | 0.977 | rājadanta-ādiṣu param | rāja-danta=ādiṣu param |
| 2.2.32 | AGREES | 0.909 | dvandve ghi | dvaṃdve GHI |
| 2.2.33 | VARIANTS | 0.667 | aj-ādy-ad-antam | aC=adi=aT=antam |
| 2.2.34 | AGREES | 1.000 | alpa-ac-taram | alpa=aC-taram |
| 2.2.35 | AGREES | 0.943 | saptamī-viśeṣane bahuvrīhau | saptamī-viśeṣaṇe bahvrīhau |
| 2.2.36 | AGREES | 1.000 | niṣṭhā | niṣṭhā |
| 2.2.37 | AGREES | 0.923 | vā+āhita-agny-ādiṣu | vā=āhita=agni=ādiṣ u |
| 2.2.38 | AGREES | 0.900 | kaḍārāḥ karmadhāraye | kaḍārāḥ karmadharāye |
| 2.3.1 | AGREES | 1.000 | anabhihite | anabhihite |
| 2.3.2 | AGREES | 1.000 | karmaṇi dvitīyā | karmaṇi dvitīyā |
| 2.3.3 | AGREES | 0.955 | tṛtīyā ca hoś chandasi | tṛtīyā ca hos chandasi |
| 2.3.4 | AGREES | 0.952 | antarā 'ntareṇa yukte | antarā=antareṇa yukte |
| 2.3.5 | AGREES | 1.000 | kāla-adhvanor atyanta-saṃyoge | kāla=adhvanor atyanta-saṃyoge |
| 2.3.6 | AGREES | 1.000 | apavarge tṛtīyā | apavarge tṛtīyā |
| 2.3.7 | AGREES | 1.000 | saptamī-pañcamyau kāraka-madhye | saptamī-pañcamyau kāraka-madhye |
| 2.3.8 | AGREES | 1.000 | karmapravacanīya-yukte dvitīyā | karmapravacanīya-yukte dvitīyā |
| 2.3.9 | AGREES | 0.962 | yasmād adhikaṃ yasya ca+īśvara-vacanaṃ tatra saptamī | yasmād adhikam yasya ca=īśvara-vacanam tatra saptamī |
| 2.3.10 | AGREES | 0.936 | pañcamy-apa-āṅ-paribhiḥ | pañcamī=apa-āṄ-pari-bhiḥ |
| 2.3.11 | AGREES | 1.000 | pratinidhi-pratidāne ca yasmāt | pratinidhi-pratidāne ca yasmāt |
| 2.3.12 | AGREES | 0.982 | gatyartha-karmaṇi dvitīyā-caturthyau ceṣṭāyām anadhvani | gaty-artha-karmaṇi dvitīyā-caturthyau ceṣṭāyām an-adhvani |
| 2.3.13 | AGREES | 1.000 | caturthī sampradāne | caturthī sampradāne |
| 2.3.14 | AGREES | 0.941 | kriya-artha-upapadasya ca karmaṇi sthāninaḥ | kriyā=arthā=upapadasya ca karmaṇi stāninaḥ |
| 2.3.15 | AGREES | 0.943 | tumarthāc ca bhāva-vacanāt | tum-arthāt=ca bhāva-vacanāt |
| 2.3.16 | VARIANTS | 0.876 | namaḥ-svasti-svāhā-svadhā 'laṃ-vaṣaḍ-yogāc ca | namas-svasti-svāhā-svadhā=alam=vaṣaṭ=ogāt=ca |
| 2.3.17 | AGREES | 0.923 | manya-karmaṇy-anādare vibhāṣā 'prāṇiṣu | manya-karmaṇi=an-ādare vibhāṣā=a-prāṇiṣu |
| 2.3.18 | AGREES | 1.000 | kartṛ-karaṇayos tṛtīyā | kartṛ-karaṇayos tṛtīyā |
| 2.3.19 | AGREES | 0.900 | sahayukte 'pradhāne | saha-yukte=a-pradhāne |
| 2.3.20 | AGREES | 0.941 | yena aṅga-vikāraḥ | yena=aṛga-vikāraḥ |
| 2.3.21 | AGREES | 0.950 | ittham-bhūta-lakṣaṇe | ittham-bhūta-laksaṇe |
| 2.3.22 | VARIANTS | 0.821 | sañjño 'nyatarasyāṃ karmaṇi | saṃ-jñaḥ=anyatarasyām karmaṇi |
| 2.3.23 | AGREES | 1.000 | hetau | hetau |
| 2.3.24 | AGREES | 0.927 | akartary-ṛṇe pañcamī | a-kartari=ṛṇe pañcamī |
| 2.3.25 | VARIANTS | 0.884 | vibhāṣā guṇe 'strīyām | vibhāṣā guṇe=a-striyām |
| 2.3.26 | AGREES | 1.000 | ṣaṣṭhī hetu-prayoge | ṣaṣṭhī hetu-prayoge |
| 2.3.27 | AGREES | 1.000 | sarvanāmnas tṛtīyā ca | sarvanāmnas tṛtīyā ca |
| 2.3.28 | AGREES | 1.000 | apādāne pañcamī | apādāne pañcamī |
| 2.3.29 | VARIANTS | 0.870 | anya-ārād-itara-rte-dik-śabda-añcu-uttarapada-aj-āhi-yukte | anya=ārat=itara=ṛte-dik-śabda=ancḥ=uttarapada=āC=āhi-ukte |
| 2.3.30 | AGREES | 0.945 | ṣaṣṭhy-atasartha-pratyayena | ṣaṣṭhī=atas-artha-pratyayena |
| 2.3.31 | AGREES | 1.000 | enapā dvitīyā | enaPā dvitīyā |
| 2.3.32 | AGREES | 0.938 | pṛthag-vinā-nānābhis tṛtīyā 'nyatarasyām | pṛthak-vinā-nānā-ūbhis tṛtīyā=nyatarasyām |
| 2.3.33 | AGREES | 0.948 | kareṇa ca stoka-alpa-kṛcchra-katipayasya asattva-vacanasya | karaṇe ca stoka=alpa-kṛcchra-atipayasya a-sattva-vacanasya |
| 2.3.34 | AGREES | 0.961 | dūra-antika-arthaiḥ ṣaṣṭhy-anyatarasyām | dūra=antika=arthaiḥ ṣaṣṭhī=nyatarasyām |
| 2.3.35 | AGREES | 1.000 | dūra-antika-arthebhyo dvitīyā ca | dūra=antika=arthebhyo dvitīyā ca |
| 2.3.36 | VARIANTS | 0.821 | saptamy-adhikarane ca | saptamī=adhikaraṇe |
| 2.3.37 | AGREES | 1.000 | yasya ca bhāvena bhāva-lakṣaṇam | yasya ca bhāvena bhāva-lakṣaṇam |
| 2.3.38 | AGREES | 0.971 | ṣaṣṭhī ca anādare | ṣaṣṭhī ca=an-ādare |
| 2.3.39 | AGREES | 0.939 | svāmi-īśvar-ādhipati-dāyāda-sākṣi-pratibhū-prasutaiś ca | svāmi(n)=īśvara=adhipati-dāyāda-sākṣi(n)-pratibhū-prasutaiś ca |
| 2.3.40 | AGREES | 0.967 | āyukta-kuśalābhyāṃ ca āsevāyām | āyukta-kuśalābhyām ca=āsevāyām |
| 2.3.41 | AGREES | 0.900 | yataś ca nirdhāranam | yatas ca nirdhāraṇam |
| 2.3.42 | AGREES | 1.000 | pañcamī vibhakte | pañcamī vibhakte |
| 2.3.43 | AGREES | 0.964 | sādhu-nipuṇābhyām arcāyāṃ saptamy aprateḥ | sādhu-nipuṇābhyām arcāyāṃ saptamī a-prateḥ |
| 2.3.44 | AGREES | 0.966 | prasita-utsukābhyāṃ tṛtīyā ca | prasita=utsukābhyām tṛtīyā ca |
| 2.3.45 | AGREES | 1.000 | nakṣatre ca lupi | nakṣatre ca luPi |
| 2.3.46 | AGREES | 0.933 | prātipadikārtha-liṅga-parimāṇavacana-mātre prathamā | prātipadika=artha-liṛga-parimāṇa-vacana-mātre prathamā |
| 2.3.47 | AGREES | 1.000 | sambodhane ca | sambodhane ca |
| 2.3.48 | AGREES | 1.000 | sā+āmantritam | sā=āmantritam |
| 2.3.49 | AGREES | 0.905 | ekavacanaṃ sambuddhiḥ | ekavacanam saṃbuddhiḥ |
| 2.3.50 | AGREES | 1.000 | ṣaṣṭhī śeṣe | ṣaṣṭhī śeṣe |
| 2.3.51 | VARIANTS | 0.840 | jño 'vid-arthasya karaṇe | jnaḥ=a-vid-arthasya karaṇe |
| 2.3.52 | AGREES | 0.968 | adhi-ig-artha-daya-īśām karmaṇi | adhi=iK=artha-dayA=īśām karmaṇi |
| 2.3.53 | AGREES | 1.000 | kṛñaḥ pratiyatne | kṛÑaḥ pratiyatne |
| 2.3.54 | AGREES | 0.960 | rujā-arthānāṃ bhāva-vacanānām ajvareḥ | rujā=arthānām bhāva-vacanānām a-jvareḥ |
| 2.3.55 | AGREES | 1.000 | āśiṣi nāthaḥ | āśiṣi nāthaḥ |
| 2.3.56 | AGREES | 0.952 | jāsi-niprahaṇa-nāṭa-krātha-piṣāṃ hiṃsāyām | jāsi-ni-pra-haṇḥ-nāṭa-krātha-piṣāṃ hiṃsāyām |
| 2.3.57 | AGREES | 0.943 | vyavahṛ-paṇoḥ samarthayoḥ | vy-ava-hṛ-paṇoḥ sam-arthayoḥ |
| 2.3.58 | AGREES | 1.000 | divas tad-arthasya | divas tad-arthasya |
| 2.3.59 | AGREES | 0.938 | vibhāṣa-upasarge | vibhāṣā=upasarge |
| 2.3.60 | AGREES | 1.000 | dvitīyā brāhmaṇe | dvitīyā brāhmaṇe |
| 2.3.61 | AGREES | 1.000 | preṣya-bruvor haviṣo devatā-sampradāne | preṣya-bruvor haviṣo devatā-sampradāne |
| 2.3.62 | AGREES | 0.968 | caturthy-arthe bahulaṃ chandasi | caturthy-arthe bahulam chandasi |
| 2.3.63 | AGREES | 1.000 | yajeś ca karaṇe | yajeś ca karaṇe |
| 2.3.64 | VARIANTS | 0.886 | kṛtvo 'rthaprayoge kāle 'dhikaraṇe | kṛtvas=artha-prayoge kāle=adhikaraṇe |
| 2.3.65 | AGREES | 0.974 | kartṛ-karmaṇoḥ kṛti | kartṛ-karmaṇoḥ kṛt-i |
| 2.3.66 | AGREES | 1.000 | ubhaya-prāptau karmaṇi | ubhaya-prāptau karmaṇi |
| 2.3.67 | AGREES | 1.000 | ktasya ca vartamāne | Ktasya ca vartamāne |
| 2.3.68 | AGREES | 0.952 | adhikaraṇa-vācinaś ca | adhikarana-vācinaś ca |
| 2.3.69 | AGREES | 0.976 | na la-u-uka-avyaya-niṣṭhā-khalartha-tṛnām | na la=u=uka-avyaya-niṣṭhā-KHaL-rtha-tṚNām |
| 2.3.70 | AGREES | 1.000 | aka-inor bhaviṣyad-ādhamarṇyayoḥ | aka=inor bhaviṣyad=ādhamarṇyayoḥ |
| 2.3.71 | AGREES | 1.000 | kṛtyānāṃ kartari vā | kṛtyānāṃ kartari vā |
| 2.3.72 | AGREES | 0.970 | tulya-arthair atulā-upamābhyāṃ tṛtīyā 'nyatarasyām | tulya=arthair a-tulā=upamābhyāṃ tṛtīyā=anyatarasyām |
| 2.3.73 | AGREES | 0.984 | caturthī ca āśiṣy āyuṣya-madra-bhadra-kuśala-sukha-artha-hitaiḥ | caturthī ca=āśiṣi=āyuṣya-madra-bhadra-kuśala-sukha=artha-hitaiḥ |
| 2.4.1 | AGREES | 1.000 | dvigur ekavacanam | dvigur ekavacanam |
| 2.4.2 | AGREES | 0.904 | dvandvaś ca prāṇi-tūrya-senā-aṅgānām | dvaṃdvaś ca prāṇi(n)-tūrya-senā=ṛgānām |
| 2.4.3 | AGREES | 1.000 | anuvāde caraṇānām | anuvāde caraṇānām |
| 2.4.4 | AGREES | 0.982 | adhvaryu-kratur anapuṃsakam | adhvaryu-kratur a-napuṃsakam |
| 2.4.5 | VARIANTS | 0.882 | adhyayanato 'viprakṛṣṭa-ākhyānām | adhyayanataḥ=a-vi-pra-kṛṣṭa=ākhyānām |
| 2.4.6 | AGREES | 0.968 | jātir aprāṇinām | jātir a-prāṇinām |
| 2.4.7 | VARIANTS | 0.875 | viśiṣṭa-liṅgo nadī deśo 'grāmāḥ | viśiṣṭa-liṛgo nadī deśaḥ=a-grāmāḥ |
| 2.4.8 | AGREES | 1.000 | kṣudra-jantavaḥ | kṣudra-jantavaḥ |
| 2.4.9 | AGREES | 1.000 | yeṣāṃ ca virodhaḥ śāśvatikaḥ | yeṣāṃ ca virodhaḥ śāśvatikaḥ |
| 2.4.10 | AGREES | 0.978 | śūdrāṇām aniravasitānām | śūdrāṇām anirvasitānām |
| 2.4.11 | AGREES | 1.000 | gavāśva-prabhṛtīni ca | gavāśva-prabhṛtīni ca |
| 2.4.12 | AGREES | 0.983 | vibhāṣā vṛkṣa-mṛga-tṛṇa-dhānya-vyañjana-paśu-śakuny-aśvavaḍava-pūrvāpara-adharottarāṇām | vibhāṣā vṛkṣa-mṛga-tṛṇa-dhānya-vyañjana-paśu-śakuni-aśva-vaḍava-pūrvāpara=adharottarāṇām |
| 2.4.13 | AGREES | 0.972 | vipratiṣiddhaṃ ca anadhikaraṇa-vāci | vipratiṣiddhaṃ ca=an-adhi-karaṇa-vāci |
| 2.4.14 | AGREES | 0.973 | na dadhipaya-ādīni | na dadhi-paya=ādīni |
| 2.4.15 | AGREES | 0.957 | adhikarana-etāvattve ca | adhikaraṇa=etāvattve ca |
| 2.4.16 | AGREES | 1.000 | vibhāṣā samīpe | vibhāṣā samīpe |
| 2.4.17 | AGREES | 1.000 | sa napuṃsakam | sa napuṃsakam |
| 2.4.18 | AGREES | 1.000 | avyayībhāvaś ca | avyayībhāvaś ca |
| 2.4.19 | VARIANTS | 0.862 | tatpuruṣo 'nañ-karmadhārayaḥ | tatpurusaḥ=a-naÑ-karmadhārayaḥ |
| 2.4.20 | AGREES | 0.941 | sañjñāyāṃ kantā-uśīnareṣu | saṃjñāyāṃ kanthā=uśīnareṣu |
| 2.4.21 | AGREES | 0.946 | upajñā-upakramam tad-ādy-ācikhyāsāyām | upajñā=upakramaṃ tad-ādi=ācikhyāsāyām |
| 2.4.22 | AGREES | 1.000 | chāyā bāhulye | chāyā bāhulye |
| 2.4.23 | VARIANTS | 0.830 | sabhā rājā 'manusya-pūrvā | sabhā rāja(n)=a-manuṣya-pūrvā |
| 2.4.24 | AGREES | 0.941 | aśālā ca | a-śālā ca |
| 2.4.25 | AGREES | 0.932 | vibhāṣā senā-surā-cchāyā-śālā-niśānām | vibhāṣā senā-surā-chāyā-sālā-nisānām |
| 2.4.26 | VARIANTS | 0.886 | paraval-liṅgaṃ dvandva-tatpuruṣayoḥ | paravat=liṛgam dvaṃdva-tatpuruṣayoḥ |
| 2.4.27 | MISSING | - | pūrvavad-aśvava-ḍavau | - |
| 2.4.28 | AGREES | 0.946 | hemanta-śiśirāv aho-rātre ca chandasi | hemanta-śiśirau=aho-rātre ca=chandasi |
| 2.4.29 | AGREES | 1.000 | rātra-ahna-ahāḥ puṃsi | rātra=ahna=ahāḥ puṃsi |
| 2.4.30 | AGREES | 0.944 | apathaṃ napuṃsakam | apathaṃ napuṃsaksm |
| 2.4.31 | AGREES | 1.000 | ardharcāḥ puṃsi ca | ardharcāḥ puṃsi ca |
| 2.4.32 | AGREES | 0.911 | idamo 'nvādeśe 'ś anudāttas tṛtīyā-ādau | idamaḥ=anvādeśe=aŚ=anudāttas tṛtīyā=ādau |
| 2.4.33 | AGREES | 0.987 | etadas tra-tasos tra-tasau ca anudātau | etadas tra-tasos tra-tasau ca=anudāttau |
| 2.4.34 | VARIANTS | 0.878 | dvitīyā-ṭā-ossv enaḥ | dvitīyā-Tā=os-su=enaḥ |
| 2.4.35 | AGREES | 0.960 | ārdhadhātuke | ārdha-dhātuke |
| 2.4.36 | AGREES | 0.960 | ado jagdhir lyap ti kiti | ado jagdhir LyaP ti K-IT-i |
| 2.4.37 | AGREES | 1.000 | luṅ-sanor ghasḷ | lUṄ-saNor ghasḶ |
| 2.4.38 | AGREES | 1.000 | ghañ-apoś ca | GHaÑ-aPoś ca |
| 2.4.39 | AGREES | 0.938 | bahulaṃ chandasi | bahulam Chandasi |
| 2.4.40 | AGREES | 0.938 | liṭy antarasyām | lIṬy anyatarasyām |
| 2.4.41 | AGREES | 1.000 | veño vayiḥ | veÑo vayiḥ |
| 2.4.42 | AGREES | 0.968 | hano vadha liṅi | hano vadha lIṄ-i |
| 2.4.43 | AGREES | 0.933 | luṅi ca | lUṄ-i ca |
| 2.4.44 | AGREES | 0.960 | ātmanepadeṣv anyatarasyām | ātmanepadeṣu=anyatarasyām |
| 2.4.45 | AGREES | 0.957 | iṇo gā luṅi | iṆo gā lUṄ-i |
| 2.4.46 | AGREES | 0.973 | ṇau gamir abodhane | Ṇau gamir a-bodhane |
| 2.4.47 | AGREES | 0.933 | sani ca | saN-i ca |
| 2.4.48 | AGREES | 0.933 | iṅaś ca | iṄ-aś ca |
| 2.4.49 | AGREES | 0.941 | gāṅ liṭi | gāṄ lIṬ-i |
| 2.4.50 | VARIANTS | 0.848 | vibhāṣā luṅḷṅoḥ | vibhāṣā lUṄ-lṚṄ-oḥ |
| 2.4.51 | VARIANTS | 0.882 | ṇau ca saṃś-caṅoḥ | Ṇau ca saN=CaṄ-oḥ |
| 2.4.52 | AGREES | 1.000 | aster bhūḥ | aster bhūḥ |
| 2.4.53 | VARIANTS | 0.870 | bruvo baciḥ | bruvo vaci-ḥ |
| 2.4.54 | AGREES | 1.000 | cakṣiṅaḥ khyāñ | cakṣiṄaḥ khyāÑ |
| 2.4.55 | AGREES | 0.933 | vā liṭi | vā lIṬ-i |
| 2.4.56 | VARIANTS | 0.895 | ajer vy aghañ-apoḥ | ajer vī=a-GHaÑ-aP-oḥ |
| 2.4.57 | AGREES | 1.000 | vā yau | vā yau |
| 2.4.58 | AGREES | 0.938 | ṇya-kṣatriya-ārṣa-ñito yūni lug aṇ-iñoḥ | Ṇya-kṣatriya-ārṣa-Ñ-IT-o yūni luK=aṆ-iÑ-oḥ |
| 2.4.59 | AGREES | 0.909 | paila-ādibyaś ca | paila=ādibhyas=ca |
| 2.4.60 | AGREES | 0.917 | iñaḥ prācām | iÑ-aḥ prāc-ām |
| 2.4.61 | AGREES | 0.970 | na taulvalibhyaḥ | na taulvali-bhyaḥ |
| 2.4.62 | AGREES | 0.986 | tadrājasya bahuṣu tena+eva astriyām | tad-rājasya bahuṣu tena=eva=astriyām |
| 2.4.63 | AGREES | 1.000 | yaska-ādibhyo gotre | yaska=ādibhyo gotre |
| 2.4.64 | AGREES | 0.957 | yañ-añoś ca | yaÑ-aÑ-oś ca |
| 2.4.65 | AGREES | 0.979 | atri-bhṛgu-kutsa-vasiṣṭha-gotama-aṅgirobhyaś ca | atri-bhṛgu-kutsa-vasiṣṭha-gotama=aṛgirobhyaś ca |
| 2.4.66 | VARIANTS | 0.881 | bahvac iñaḥ prācya-bhrateṣu | bahu=aCaḥ=iÑ-aḥ prācya-bharateṣu |
| 2.4.67 | AGREES | 0.927 | na gopavana-ādibhyaḥ | na gopav-ana=ādibhyah |
| 2.4.68 | AGREES | 0.963 | tika-kitava-ādibhyo dvandve | tika-kitava=ādibhyo dvaṃdve |
| 2.4.69 | VARIANTS | 0.889 | upaka-ādibhyo 'nyatarasyām advandve | upaka=ādibhyaḥ=anyatarasyām a-dvaṃdve |
| 2.4.70 | AGREES | 0.986 | āgastya-kauṇḍinyayor agasti-kuṇḍinac | āgastya-kauṇḍinyay-or agasti-kuṇḍinaC |
| 2.4.71 | AGREES | 0.980 | supo dhātu-prātipadikayoḥ | suPo dhātu-prātipadikay-oḥ |
| 2.4.72 | AGREES | 0.957 | adiprabhṛtibhyaḥ śapaḥ | adi-prabhṛtibhyaḥ ŚaP-aḥ |
| 2.4.73 | AGREES | 0.938 | bahulaṃ chandasi | bahulam chandasi |
| 2.4.74 | VARIANTS | 0.750 | yaṅo 'ci ca | yaṄ-aḥ=aCi ca |
| 2.4.75 | AGREES | 0.905 | juhoty-ādibhyaḥ śluḥ | ju-ho-ti=ādibhyaḥ Śluḥ |
| 2.4.76 | AGREES | 1.000 | bahulaṃ chandasi | bahulaṃ chandasi |
| 2.4.77 | AGREES | 0.957 | gāti-sthā-ghu-pā-bhūbhyaḥ sicaḥ parasmaipadeṣu | gāti-sthā-GHU-pā-bhū-yaḥ siC-aḥ parasmaipadeṣu |
| 2.4.78 | AGREES | 0.982 | vibhāṣā ghrā-dheṭ-śāc-chā-saḥ | vibhāṣā ghrā-dheṬ-śā=chā-saḥ |
| 2.4.79 | AGREES | 0.933 | tan-ādibhyas ta-thāsoḥ | tan=ādibhyaḥ=ta-thās-oḥ |
| 2.4.80 | AGREES | 0.924 | mantre ghasa-hvara-naśa-vṛ-daha-ād-vṛc-kṛ-gami-janibhyo leḥ | mantre ghasa-hvara-ṇaśḥ-vṛ-dahḥ=āT-vṛc-kṛ-gami-jani-bhyo lEḥ |
| 2.4.81 | AGREES | 1.000 | āmaḥ | āmaḥ |
| 2.4.82 | AGREES | 0.909 | avyayād āp-supaḥ | avyayāt=āP-sUP-aḥ |
| 2.4.83 | VARIANTS | 0.865 | na avyayībhāvād ato 'm tv apañcamyāḥ | na=avyayībhāvāt=aTaḥ=am tu=a-pañcamyāḥ |
| 2.4.84 | AGREES | 1.000 | tṛtīyā-saptamyor bahulam | tṛtīyā-saptamyor bahulam |
| 2.4.85 | AGREES | 0.918 | luṭaḥ prathamasya ḍāraurasaḥ | lUṬ-aḥ prathama-sya Ḍā-rau-ras-aḥ |
| 3.1.1 | AGREES | 1.000 | pratyayaḥ | pratyayaḥ |
| 3.1.2 | AGREES | 1.000 | paraś ca | paraś ca |
| 3.1.3 | AGREES | 0.929 | ādy-udāttaś ca | ādy=udāttas ca |
| 3.1.4 | AGREES | 0.900 | anudāttau sup-pitau | anudattau sUP-P-IT-au |
| 3.1.5 | AGREES | 0.927 | gup-tij-kidbhyaḥ san | gup-tij-kit=bhyaḥ saN |
| 3.1.6 | AGREES | 0.989 | mān-badha-dān-śānbhyo dīrghaś ca abhyāsasya | mān-badhA-dān-śān-bhyo dīrghaś ca=abhyāsasya |
| 3.1.7 | AGREES | 0.932 | dhātoḥ karmaṇaḥ samāna-kartṛkād icchāyāṃ vā | dhātoḥ karmaṇ-aḥ samāna-kartṛk-āt icchāyām vā |
| 3.1.8 | AGREES | 0.944 | supa ātmanaḥ kyac | sUPaḥ=ātman-aḥ KyaC |
| 3.1.9 | AGREES | 1.000 | kāmyac ca | kāmyaC ca |
| 3.1.10 | AGREES | 0.929 | upamānād ācāre | upamānāt=ācāre |
| 3.1.11 | AGREES | 0.913 | kartuḥ kyaṅ salopaś ca | kart-uḥ KyaṄ sā-lopaś=ca |
| 3.1.12 | VARIANTS | 0.864 | bhṛśādibhyo bhuvy-acver lopaś ca halaḥ | bhṛśa=ādibhyaḥ=bhuvi=a-Cveḥ lopaś ca haL-aḥ |
| 3.1.13 | VARIANTS | 0.894 | lohitādi-ḍājbhyaḥ kyaṣ | lohita=ādi-ḌāC=bhyaḥ KyaṢ |
| 3.1.14 | AGREES | 0.968 | kaṣṭāya kramaṇe | kaṣṭā-ya kramaṇe |
| 3.1.15 | AGREES | 0.925 | karmaṇo romantha-tapobhyāṃ varti-caroḥ | karmaṇ-aḥ=romantha-tapo-bhyāṃ varti-car-oḥ |
| 3.1.16 | AGREES | 0.920 | bāṣpa-ūṣmabhyām udvamane | bāṣpa=ūṣmā-bhyām ud-vamane |
| 3.1.17 | AGREES | 0.979 | śabda-vaira-kalaha-abhra-kaṇva-meghebhyaḥ karaṇe | śabda-vaira-kalaha=abhra-kaṇva-meghe-hyaḥ karaṇe |
| 3.1.18 | AGREES | 0.966 | sukhādibhyaḥ kartṛ-vedanāyām | sukha=ādibhyaḥ kartṛ-vedanāyām |
| 3.1.19 | VARIANTS | 0.889 | namo-varivaś-citraṅaḥ kyac | namas=varivas=citraṄ-aḥ KyaC |
| 3.1.20 | AGREES | 0.920 | puccha-bhānḍa-cīvarāṇ ṇiṅ | puccha-bhāṇḍa-cīvarāt=ṆiṄ |
| 3.1.21 | AGREES | 0.964 | muṇḍa-miśra-ślakṣṇa-lavaṇa-vrata-vastra-hala-kala-kṛta-tūstebhyo ṇic | muṇḍa-miśra-slakṣṇa-lavaṇa-vrata-vastra-hala-kala-kṛta-tūstebhyaḥ=ṆiC |
| 3.1.22 | AGREES | 0.913 | dhātor eka-aco hala-ādeḥ kriyāsamabhihāre yaṅ | dhātor eka=aCaḥ=haL-ādeḥ kriyā-sam-bhi-hāre yaṄ |
| 3.1.23 | AGREES | 1.000 | nityaṃ kauṭilye gatau | nityaṃ kauṭilye gatau |
| 3.1.24 | AGREES | 0.922 | lupa-sada-cara-japa-jabha-daha-daśa-gṝbhyo bhāva-garhāyām | lupa-sada-carḥ-japḥ-jabhA-dahḥ-daśḥ-gṝ-bhyo bhāva-garhāyām |
| 3.1.25 | AGREES | 0.970 | satyāpa-pāśa-rūpa-vīṇā-tūla-śloka-senā-loma-tvaca-varma-varṇa-cūrṇa-curādibhyo ṇic | satyāpa-pāśa-rūpa-vīṇā-tūla-śloka-senā-loma(n)=tvaca=varma(n)=varṇa-cūrṇa-cur=ādibhyo ṆiC |
| 3.1.26 | AGREES | 0.957 | hetumati ca | hetumat-i ca |
| 3.1.27 | AGREES | 0.941 | kaṇḍv-ādibhyo yak | kaṇḍū=ādibhyo yaK |
| 3.1.28 | AGREES | 0.959 | gupū-dhūpa-vicchi-paṇi-panibhya āyaḥ | gupŪ-dhūpḥ-vicchi-paṇi-pani-bhya āyaḥ |
| 3.1.29 | AGREES | 1.000 | ṛter īyaṅ | ṛter īyaṄ |
| 3.1.30 | AGREES | 1.000 | kamer ṇiṅ | kamer ṆiṄ |
| 3.1.31 | AGREES | 0.920 | āyādaya ārdhadhātuke vā | āya=ādayaḥ=ārdhad hātuke vā |
| 3.1.32 | VARIANTS | 0.884 | san-ādyantā dhātavaḥ | saN=ādi=antāḥ=dhātav-aḥ |
| 3.1.33 | VARIANTS | 0.750 | syatāsī ḷluṭoḥ | sya-tāsī lṚ-lḥṬ-oḥ |
| 3.1.34 | VARIANTS | 0.848 | sib-bahulaṃ leti | siP=bahulaṃ lEṬ-i |
| 3.1.35 | AGREES | 0.933 | kās-pratyayād ām amantre liṭi | kās-pratyayāt=ām=a-mantre lIṬ-i |
| 3.1.36 | VARIANTS | 0.847 | ij-ādeś ca gurumato 'nṛcchaḥ | iC=ādeś ca gurumataḥ=an-ṛcch-aḥ |
| 3.1.37 | AGREES | 0.909 | daya-aya-āsaś ca | dayḥ=ayA=ās -aś ca |
| 3.1.38 | VARIANTS | 0.852 | uṣa-vida-jāgṛbhyo 'nyatarasyām | uṣḥ-vidḥ-jāgṛ-bhyaḥ=nyatarasyām |
| 3.1.39 | AGREES | 0.929 | bhī-hrī-bhṛ-huvāṃ śluvac ca | bhī-hrī-bhṛ-huv-āṃ Ślu-vat=ca |
| 3.1.40 | AGREES | 0.909 | kṛñ ca anuprayujyate liṭi | kṛÑ ca=anu-pra-yuj-ya-te lIṬ-i |
| 3.1.41 | VARIANTS | 0.862 | vidāṅ-kurvantv ity anyatarasyām | vid-āṃ=kur-v-antu=iti=anyatarasyām |
| 3.1.42 | VARIANTS | 0.856 | abhyutsādayāṃ-prajanayām-cikayāṃ-ramayām-akaḥ pāvayām-kriyād vidām-akrann iti cchandasi | abhy-ut-sād-ay-ām=pra-jan-ay-ām-ci-kay-ām-ram-ay-ām+akaḥpāv-ay-āṃ+kri-yāt-vid-ām+akrann iti=chandssi |
| 3.1.43 | VARIANTS | 0.824 | cli luḍi | Cli lUṄ-i |
| 3.1.44 | AGREES | 1.000 | cleḥ sic | Cleḥ siC |
| 3.1.45 | VARIANTS | 0.800 | śala ig-upadhād aniṭaḥ kṣaḥ | śaL-aḥ=iK=upadh-āt=an-iṬ-aḥ Ksa-ḥ |
| 3.1.46 | VARIANTS | 0.839 | śliṣa āliṅgane | śliṣ-aḥ=ā-liṛgane |
| 3.1.47 | AGREES | 0.941 | na dṛśaḥ | na dṛś-aḥ |
| 3.1.48 | AGREES | 0.984 | ṇi-śri-dru-srubhyaḥ kartari caṅ | Ṇi-śri-dru-sru-bhyaḥ kartari CaṄ |
| 3.1.49 | AGREES | 0.973 | vibhāṣā dheṭ-śvyoḥ | vibhāṣā dheṬ-śvy-oḥ |
| 3.1.50 | AGREES | 1.000 | gupeś chandasi | gupeś chandasi |
| 3.1.51 | VARIANTS | 0.808 | na-unayati-dhvanayaty-elayaty-ardayatibhyaḥ | na=ūn-ay-a-ti-dhvan-ay-a-ti=el-ay-a-ti=ard-ay-a-ti-bhyaḥ |
| 3.1.52 | VARIANTS | 0.889 | asyati-vakti-khyātibhyo 'ṅ | asyati-vakti-khyāti-bhyaḥ=aṄ |
| 3.1.53 | AGREES | 0.971 | lipi-sici-hvaś ca | lipi-sici-hv-aś ca |
| 3.1.54 | AGREES | 0.960 | ātmanepadeṣv anyatarasyām | ātmanepadeṣu=anyatarasyām |
| 3.1.55 | VARIANTS | 0.880 | puṣādi-dyutādy-ḷditaḥ prasmaipadeṣu | puṣ=ādi-dyut-ādi=ḷT=IT-aḥ parasmaipadeṣu |
| 3.1.56 | VARIANTS | 0.885 | sarti-śāsty-artibhyaś ca | sar-ti-śās-ti-ar-ti-bhyaś ca |
| 3.1.57 | VARIANTS | 0.889 | irito vā | IR=IT-o vā |
| 3.1.58 | VARIANTS | 0.860 | jṝ-stambhu-mrucu-mlucu-grucu-glucu-gluñcu-śvibhyaś ca | jṝ-stanbhU-mrucḥ-mlucḥ-grucḥ-glucḥ-gluncḥ-śvi-bhyaś ca |
| 3.1.59 | AGREES | 0.982 | kṛ-mṛ-dṛ-ruhibhyaś chandasi | kṛ-mṛ-dṛ-ruhi-bhyaś chandasi |
| 3.1.60 | AGREES | 0.960 | ciṇ te padaḥ | CiṆ te pad-aḥ |
| 3.1.61 | AGREES | 0.938 | dīpa-jana-budha-pūri-tāyi-pyāyibhyo 'nyatarasyām | dīpa-jana-budhA-pūri-tāyi-pyāyi-hyaḥ=nyatarasyām |
| 3.1.62 | AGREES | 0.919 | acaḥ karmakartari | aC-aḥ karma-kartar-i |
| 3.1.63 | AGREES | 0.941 | duhaś ca | duh-aś ca |
| 3.1.64 | AGREES | 0.947 | na rudhaḥ | na rudh-aḥ |
| 3.1.65 | VARIANTS | 0.839 | tapo 'nutāpe ca | tapaḥ=anutāpe ca |
| 3.1.66 | AGREES | 0.944 | ciṇ bhāvakarmaṇoḥ | CiṆ bhāva-karmaṇ-oḥ |
| 3.1.67 | AGREES | 1.000 | sārvadhātuke yak | sārvadhātuke yak |
| 3.1.68 | AGREES | 0.957 | kartari śap | kartar-i ŚaP |
| 3.1.69 | AGREES | 1.000 | div-ādibhyaḥ śyan | div-ādibhyaḥ ŚyaN |
| 3.1.70 | AGREES | 0.916 | vā bhrāśa-bhlāśa-bhramu-kramu-klamu-trasi-truti-laṣaḥ | vā bhrāśa-bhlāśa-bhramḥ-kramḥ-klamḥ-trasi-truṭi-laṣ-aḥ |
| 3.1.71 | VARIANTS | 0.800 | yaso 'nupasargāt | yas-aḥ=an-upasargāt |
| 3.1.72 | AGREES | 0.917 | saṃyasaś ca | saṃ-yas-aś ca |
| 3.1.73 | VARIANTS | 0.875 | sv-ādibhyaḥ śnuḥ | su=ādibhyah Śnuḥ |
| 3.1.74 | AGREES | 0.960 | śruvaḥ śṛ ca | śruv-aḥ śṛ ca |
| 3.1.75 | VARIANTS | 0.833 | akṣo 'nyatarasyām | akṣ-aḥ=anyatarasyām |
| 3.1.76 | AGREES | 0.973 | tanū-karaṇe takṣaḥ | tanū-karaṇe takṣ-aḥ |
| 3.1.77 | AGREES | 0.970 | tud-ādibhyaḥ śaḥ | tud-ādibhyaḥ Śa-ḥ |
| 3.1.78 | AGREES | 0.944 | rudḥ-ādibhyaḥ śnam | rudh-ādibhyaḥ ŚnaM |
| 3.1.79 | AGREES | 0.950 | tan-ādi-kṛñbhyaḥ uḥ | tan-ādi-kṛÑ-bhyaḥ=u-ḥ |
| 3.1.80 | AGREES | 0.974 | dhinvi-kṛṇvyor a ca | dhinvi=kṛṇvy-or a ca |
| 3.1.81 | AGREES | 0.938 | kry-ādibhyaḥ śnā | krī-ādibhyaḥ Śnā |
| 3.1.82 | VARIANTS | 0.828 | stambhu-stumbhu-skambhu-skumbhu-skuñbhyaḥ śnuś ca | stanbhḥ-stunbhḥ-skanbhḥ-skunbhḥ-skuÑ-bhyaḥ Śnuś ca |
| 3.1.83 | VARIANTS | 0.810 | halaḥ śnaḥ śānajjñau | haL-aḥ Śn-aḥ ŚānaC=hau |
| 3.1.84 | AGREES | 0.919 | chandasi śāyaj api | chandas-i ŚāyaC=api |
| 3.1.85 | AGREES | 1.000 | vyatyayo bahulam | vyatyayo bahulam |
| 3.1.86 | VARIANTS | 0.786 | liṅy āśiṣy aṅ | lIṄ-i=āśiṣ-i=aṄ |
| 3.1.87 | AGREES | 0.966 | karmavat karmaṇā tulyakriyaḥ | karmavat karmaṇ-ā tulya-kriyaḥ |
| 3.1.88 | AGREES | 0.981 | tapas tapaḥ-karmakasya+eva | tap-as tapaḥ-karmakasya=eva |
| 3.1.89 | AGREES | 0.909 | na duha-snu-namāṃ yak-ciṇau | na duhḥ-snu-namām yaK-CiṆ-au |
| 3.1.90 | AGREES | 0.962 | kuṣi-rajoḥ prācāṃ śyan parasmaipadaṃ ca | kuṣi-raj-oḥ prācām ŚyaN parasmaipadaṃ ca |
| 3.1.91 | AGREES | 0.923 | dhātoḥ | dhāto-ḥ |
| 3.1.92 | AGREES | 0.929 | tatra+upapadaṃ saptamīstham | ta-tra=upapadam saptamī-stham |
| 3.1.93 | VARIANTS | 0.824 | kṛd atiṅ | kṛt=a-tiṄ |
| 3.1.94 | VARIANTS | 0.762 | vā 'sarūpo 'striyām | vā=a-sarūpa-ḥ=a-striyām |
| 3.1.95 | VARIANTS | 0.811 | kṛtyāḥ pragṇ vulaḥ | kṛtyāḥ prāṛ ṆvuL-aḥ |
| 3.1.96 | AGREES | 0.977 | tavyat-tavya-anīyaraḥ | tavyaT-tavya=anīyaR-aḥ |
| 3.1.97 | VARIANTS | 0.750 | aco yat | aC-aḥ=yaT |
| 3.1.98 | AGREES | 0.929 | por ad-upadhāt | pOr aT=upadhāt |
| 3.1.99 | VARIANTS | 0.889 | śaki-sahoś ca | śaki-śah-oś ca |
| 3.1.100 | AGREES | 0.943 | gada-mada-cara-yamaś ca anupasarge | gadA-mada-carḥ-yamaś ca=an-upa-sarge |
| 3.1.101 | AGREES | 0.979 | avadya-paṇya-varyā garhya-paṇitavya-anirodheṣu | avadya-paṇya-varyāḥ garhya-paṇitavya=a-nirodheṣu |
| 3.1.102 | AGREES | 0.929 | vahyaṃ karaṇam | vahyam karaṇam |
| 3.1.103 | VARIANTS | 0.889 | aryaḥ svami-vaiśyayoḥ | arya-ḥ svāmi(n)=vaiśyayoḥ |
| 3.1.104 | AGREES | 0.957 | upasaryā kālyā prajane | upa-saryā kālyā pra-jane |
| 3.1.105 | VARIANTS | 0.743 | ajaryaṃ saṅgatam | a-jar-yam saṃ-gatam |
| 3.1.106 | AGREES | 0.947 | vadaḥ supi kyap ca | vad-aḥ sUP-i KyaP ca |
| 3.1.107 | AGREES | 0.957 | bhuvo bhāve | bhuv-o bhāve |
| 3.1.108 | AGREES | 0.957 | hanas ta ca | han-as ta ca |
| 3.1.109 | AGREES | 0.947 | eti-stu-śās-vṛ-dṛ-juṣaḥ kyap | eti-stu-sās=vṛ-dṛ-juṣ-aḥ KyaP |
| 3.1.110 | VARIANTS | 0.868 | ṛd upadhāc ca akḷpi-cṛteḥ | ṛT=upadh-āt=ca=a-kḷpi-cṛte-ḥ |
| 3.1.111 | AGREES | 0.957 | ī ca khanaḥ | ī ca khan-aḥ |
| 3.1.112 | VARIANTS | 0.743 | bhṛño 'sañjñāyām | bhṛÑ-aḥ=a-saṃjñāyām |
| 3.1.113 | AGREES | 0.963 | mṛjer vibhāṣā | mṛje-r vibhāṣā |
| 3.1.114 | AGREES | 1.000 | rājasūya-sūrya-mṛṣodya-rucya-kupya-kṛṣṭapacya-avyathyāḥ | rājasūya-sūrya-mṛṣodya-rucya-kupya-kṛṣṭapacya=avyathyāḥ |
| 3.1.115 | AGREES | 0.950 | bhidya-uddhyau nade | bhid-ya=uddh-yau nade |
| 3.1.116 | AGREES | 0.936 | puṣya-siddhyau nakṣatre | puṣ-ya-sidh-yau nakṣatre |
| 3.1.117 | AGREES | 0.961 | vipūya-vinīya-jityā muṅja-kalka-haliṣu | vipūya-vinīya-jityāḥ muñja-kalka-haliṣu |
| 3.1.118 | AGREES | 0.903 | praty-apibhyāṃ graheś chandasi | prati=api-bhyām graheś chandas-i |
| 3.1.119 | AGREES | 0.935 | pada-asvairi-bāhyā-pakṣyeṣu ca | pada=asvairi(n)-bāhyā-paksyeṣu ca |
| 3.1.120 | AGREES | 1.000 | vibhāṣā kṛ-vṛṣoḥ | vibhāṣā kṛ-vṛṣoḥ |
| 3.1.121 | VARIANTS | 0.875 | yugyaṃ ca patre | yug-yam ca pattre |
| 3.1.122 | AGREES | 0.955 | amāvasyad-anyatarasyām | amāvasyaT=anyatarasyām |
| 3.1.123 | AGREES | 0.987 | chandasi niṣṭarkya-devahūya-praṇīya-unnīya-ucchiṣya-marya-starya-dhvarya-khanya-khānya-devayajyā-āpṛcchya-pratiṣīvya-brahmavādya-bhāvya-stāvya-upacāyyapṛḍāni | chandas-i niṣṭarkya-devahūya-praṇīya=unnīya=ucchiṣya-marya-staryā-dhvarya-khanya-khānya-devayajyā-āpṛcchya-pratiṣīvya-brahmavādya-bhāvya-stāvya=upacāyya-pṛḍāni |
| 3.1.124 | AGREES | 0.960 | ṛ-halor ṇyat | ṛ-haL-or ṆyaT |
| 3.1.125 | AGREES | 0.957 | or āvaśyake | o-r āvaśyake |
| 3.1.126 | AGREES | 0.986 | āsu-yu-vapi-rapi-lapi-trapi-camaś ca | ā-su-yu-vapi-rapi-lapi-trapi-camaś ca |
| 3.1.127 | VARIANTS | 0.786 | ānāyyo 'nitye | ānāyyaḥ=a-nitye |
| 3.1.128 | VARIANTS | 0.769 | praṇāyyo 'sammatau | praṇāyyaḥ=a-saṃ-matau |
| 3.1.129 | AGREES | 0.943 | pāyya-sān-nāyya-nikāyya-dhāyyā māna-havir-nivāsa-sāmidhenīṣu | pāyya-sāṃ-nāyya-ni-kāyya-dhāyyāḥ māna-havis=nivāsa-sāmidhenī-ṣu |
| 3.1.130 | AGREES | 0.912 | kratau kuṇḍapāyya-sañcāyyau | kratau kuṇḍa-pāy-ya-saṃ-cāyyau |
| 3.1.131 | AGREES | 0.943 | agnau paricāyya-upacāyya-samūhyāḥ | agnau pari-cāy-ya=upa-cāy-ya-samūhyāḥ |
| 3.1.132 | AGREES | 0.923 | citya-agnicitye ca | cit-ya=agni-cit-ye ca |
| 3.1.133 | AGREES | 0.952 | ṇvul-tṛcau | ṆvuL-tṛC-au |
| 3.1.134 | VARIANTS | 0.895 | nandi-grahi-pacādibhyo lyu-ṇiny-acaḥ | nandi-grahi-paca=ādibhyaḥ Lyu-Ṇini-aC-aḥ |
| 3.1.135 | AGREES | 0.909 | igupadha-jñā-prī-kiraḥ kaḥ | iK=upadha=jñā-prī-kir-aḥ Ka-ḥ |
| 3.1.136 | AGREES | 0.970 | ātaś ca+upasarge | āT-aś ca=upasarge |
| 3.1.137 | AGREES | 0.982 | pā-ghrā-dhmā-dheṭ-dṛśaḥ śaḥ | pā-ghrā-dhmā-dheṬ-dṛś-aḥ Śaḥ |
| 3.1.138 | AGREES | 0.903 | anupasargāl limpa-vinda-dhāri-pāri-vedy-udeji-ceti-sāti-sāhibhyaś ca | an-upasargāt=limpA-vinda-dhār-i-pār-i-vedi-ud-ej-i-cet-i-sāt-i-sāh-i-hyaś ca |
| 3.1.139 | AGREES | 0.906 | dadāti-dadhātyor vibhāṣā | da-dā-ti=da-dhā-ty-or vibhāṣā |
| 3.1.140 | VARIANTS | 0.898 | jvaliti-kasantebhyo ṇaḥ | jval-iti=kas-antebhyaḥ=Ṇaḥ |
| 3.1.141 | VARIANTS | 0.857 | śyā-ād-vyadha-āsru-saṃsrv-atīṇ-avasā-avahṛ-liha-śliṣa-śvasaś ca | śyā-āT=vyadhḥ=ā-sru-saṃ-sru-ati-iṆ=ava-sā=ava-hṛ-lihḥ-śliṣḥ-śvas-aś ca |
| 3.1.142 | AGREES | 0.947 | du-nyor anupasarge | du-ny-or an-upasarge |
| 3.1.143 | VARIANTS | 0.857 | vibhāśā grahaḥ | vibhāṣā graheḥ |
| 3.1.144 | AGREES | 1.000 | gehe kaḥ | gehe Kaḥ |
| 3.1.145 | AGREES | 0.960 | śilpini ṣvun | śilpin-i ṢvuN |
| 3.1.146 | AGREES | 0.947 | gasthakan | gas thakaN |
| 3.1.147 | AGREES | 1.000 | ṇyuṭ ca | ṆyuṬ ca |
| 3.1.148 | AGREES | 1.000 | haś ca vrīhi-kālayoḥ | haś ca vrīhi-kālayoḥ |
| 3.1.149 | AGREES | 0.947 | pru-sṛ-lvaḥ samabhihāre vun | pru-sṛ-lv-aḥ sam-abhi-hāre vuN |
| 3.1.150 | AGREES | 0.941 | āśiṣi ca | āśiṣ-i ca |
| 3.2.1 | VARIANTS | 0.857 | karmaṇy aṇ | karmaṇ-i=aṆ |
| 3.2.2 | AGREES | 1.000 | hvā-vā-amaś ca | hvā-vā-amaś ca |
| 3.2.3 | VARIANTS | 0.821 | āto 'nupasarge kaḥ | āTaḥ=an-upa-sarge Kaḥ |
| 3.2.4 | AGREES | 0.952 | supi sthaḥ | sUP-i sthaḥ |
| 3.2.5 | AGREES | 0.939 | tunda-śokayoḥ parimṛja-apanudoḥ | tunda-śokay-oḥ pari-mṛja=apa-nud-oḥ |
| 3.2.6 | AGREES | 0.957 | pre dā-jñaḥ | pre dā-jñ-aḥ |
| 3.2.7 | AGREES | 0.952 | sami khyaḥ | sam-i khyaḥ |
| 3.2.8 | VARIANTS | 0.842 | gā-poṣ ṭak | gāpoḥ=ṬaK |
| 3.2.9 | VARIANTS | 0.870 | harater anudyamane 'c | har-a-ter an-ud-yamane=aC |
| 3.2.10 | AGREES | 0.947 | vayasi ca | vayas-i ca |
| 3.2.11 | AGREES | 0.929 | āṅi tācchīlye | āṄ-i tāc-chīlye |
| 3.2.12 | AGREES | 0.909 | arhaḥ | arh-aḥ |
| 3.2.13 | AGREES | 0.943 | stamba-karṇayo rami-japoḥ | stamba-karṇay-oḥ rami-jap-oḥ |
| 3.2.14 | VARIANTS | 0.870 | śami dhātoḥ sañjñāyām | śam-i dhāt-oḥ saṃjñā-y-ām |
| 3.2.15 | AGREES | 1.000 | adhikaraṇe śeteḥ | adhikaraṇe śeteḥ |
| 3.2.16 | VARIANTS | 0.889 | careṣ ṭaḥ | careś Ṭaḥ |
| 3.2.17 | AGREES | 0.933 | bhikṣā-senā-ādāyeṣu ca | bhikṣā-śenā=ādāye-ṣu ca |
| 3.2.18 | VARIANTS | 0.778 | puro 'grato 'greṣu sarteḥ | puras=agratas=agre-ṣu sart-eḥ |
| 3.2.19 | AGREES | 0.929 | pūrve kartari | pūrv-e kartar-i |
| 3.2.20 | AGREES | 0.921 | kṛño hetu-tācchīlya-ānulomyeṣu | kṛÑ-aḥ=hetu-tācchīlya-ānulomye-ṣu |
| 3.2.21 | AGREES | 0.944 | divā-vibhā-niśā-prabhā-bhās-kāra-anta-ananta-ādi-bahu-nāndī-kiṃ-lipi-libi-bali-bhakti-kartṛ-citra-kṣetra-saṅkhyā-jaṅghā-bāhv-ahar-yat-tad-dhanur-aruṣṣu | divā-vibbhā-niśā-prabhā-bhās-kāra=anta=an-anta=ādi-bahu-nāndī-kim-lipi-libi-bali-bhakti-kartṛ-citra-kṣetra-saṃkhyā-jaṛghā-bāhu-ahan=yad=tad= dhanus=aruṣ-ṣu |
| 3.2.22 | AGREES | 0.933 | karmaṇi bhṛtau | karmaṇ-i bhṛt-au |
| 3.2.23 | AGREES | 0.974 | na śabda-śloka-kalaha-gāthā-vaira-cāṭu-sūtra-mantra-padeṣu | na śabda-sloka-kalaha-gāthā-vaira-cāṭu-sūtra-mantra-pade-ṣu |
| 3.2.24 | AGREES | 0.971 | stamba-śakṛtor in | stamba-śakṛt-or iN |
| 3.2.25 | AGREES | 0.945 | harater dṛti-nāthayoḥ paśau | harateḥ=dṛti-nāthay-oḥ paśau |
| 3.2.26 | AGREES | 0.945 | phalegrahir-ātmambhariś ca | phale-grah-ir-ātmam-bhariś ca |
| 3.2.27 | AGREES | 0.906 | chandasi vana-sana-rakṣi-mathām | chandas-i vanḥ-sanḥ-rakṣi-math-ām |
| 3.2.28 | AGREES | 1.000 | ejeḥ khaś | ejeḥ KHaŚ |
| 3.2.29 | AGREES | 0.929 | nāsikā-stanayor dhmā-dheṭoḥ | nāsikā-stanay-oḥ=dhmā-dheṬ-oḥ |
| 3.2.30 | AGREES | 0.968 | nāḍī-muṣṭyoś ca | nāḍī-muṣṭy-oś ca |
| 3.2.31 | AGREES | 0.927 | udi kūle ruji-vahoḥ | ud-i kūl-e ruji-vah-oḥ |
| 3.2.32 | AGREES | 0.941 | vaha-abhre lihaḥ | vaha=abhr-e lih-aḥ |
| 3.2.33 | AGREES | 0.933 | parimāṇe pacaḥ | parimāṇ-e pac-aḥ |
| 3.2.34 | AGREES | 0.963 | mita-nakhe ca | mita-nakh-e ca |
| 3.2.35 | VARIANTS | 0.842 | vidhv-aruṣos tudaḥ | vidhu=aruṣ-oḥ=tud-aḥ |
| 3.2.36 | AGREES | 0.912 | asūrya-lalāṭayor dṛśi-tapoḥ | a-sūrya-lalāṭay-oḥ-dṛśi-tap-oḥ |
| 3.2.37 | VARIANTS | 0.795 | ugrampaśya-irammada-pāṇindhamāś ca | ugra-m-paśy-a=ira-m-mad-a-pāṇi-ṃ-dhamāḥ |
| 3.2.38 | AGREES | 0.930 | priyavaśe vadaḥ khac | priya-vaś-e vad-aḥ KHaC |
| 3.2.39 | AGREES | 0.952 | dviṣat-parayos tāpeḥ | dviṣatt-paray-os=tāpeḥ |
| 3.2.40 | VARIANTS | 0.824 | vāci yamo vrate | vāc-i yama-ḥ=vrat-e |
| 3.2.41 | VARIANTS | 0.816 | pūḥ-sarvayor dāri-sahoḥ | pur=sarvay-oḥ dār-i-sah-oḥ |
| 3.2.42 | AGREES | 0.969 | sarva-kūla-abhra-karīṣeṣu kaṣaḥ | sarva-kūla=abhra-karīṣe-ṣu kaṣ-aḥ |
| 3.2.43 | AGREES | 0.917 | megha-rti-bhayeṣu kṛñaḥ | megha=ṛti-bhaye-ṣu kṛÑ-aḥ |
| 3.2.44 | AGREES | 0.917 | kṣema-priya-madre 'ṇ ca | kṣema-priya-madre-e aṆ ca |
| 3.2.45 | AGREES | 0.949 | āśite bhuvaḥ karaṇa-bhāvayoḥ | āśit-e bhuv-aḥ karaṇa-bhāvay-oḥ |
| 3.2.46 | AGREES | 0.901 | sañjñāyāṃ bhṛ-tṝ-vṛ-ji-dhāri-sahi-tapi-damaḥ | saṃjñā yām bhṛ-tṝ=vṛ-ji-dhār-i-śahi-tapi-dam-aḥ |
| 3.2.47 | AGREES | 0.941 | gamaś ca | gam-aś ca |
| 3.2.48 | AGREES | 0.940 | anta-atyanta-adhva-dūra-pāra-sarva-ananteṣu ḍaḥ | anta=aty-anta=adhva(n)-dūra-pāra-sarva-an-ante-ṣu Ḍa-ḥ |
| 3.2.49 | AGREES | 0.917 | āśiṣi hanaḥ | āśiṣ-i han-aḥ |
| 3.2.50 | AGREES | 0.944 | ape kleśa-tamasoḥ | ap-e kleśa-tamas-oḥ |
| 3.2.51 | AGREES | 0.909 | kumāra-śīrṣayor ṇiniḥ | kumāra-śīrṣay-oh=Ṇini-ḥ |
| 3.2.52 | AGREES | 0.917 | lakṣaṇe jāyā-patyoṣ ṭak | lakṣaṇ-e jāyā-paty-oḥ=ṬaK- |
| 3.2.53 | AGREES | 0.923 | amanuṣyakartṛke ca | a-manuṣya-kartṛk-e ca |
| 3.2.54 | AGREES | 0.917 | śaktau hasti kapāṭayoḥ | śakt-au hasti(n)=kapāṭay-oḥ |
| 3.2.55 | AGREES | 0.906 | pāṇigha-tāḍaghau śilpini | pāṇi-gh-a-tāḍa-gh-au śilpin-i |
| 3.2.56 | AGREES | 0.942 | āḍhya-subhaga-sthūla-palita-nagna-andha-priyeṣu cvy-artheṣv acvau kṛñaḥ karaṇe khyun | āḍhya-subhaga-sthūla-palita-nagna=andha-priye-ṣu Cvi=rthe-ṣu=a-Cvau kṛÑ-aḥ karaṇ-e KHyuN |
| 3.2.57 | AGREES | 0.954 | kartari bhuvaḥ khiṣṇuc-khukañau | kartar-i bhuv-aḥ KHiṣṇuC-KHukaÑ-au |
| 3.2.58 | VARIANTS | 0.800 | spṛśo 'nudake kvin | spṛś-aḥ=an-udak-e KviN |
| 3.2.59 | VARIANTS | 0.878 | ṛtvig-dadhṛk-srag-dig-uṣṇig-añcu-yuji-kruñcāṃ ca | ṛtv-ij=dadhṛṣ=sraj=diś=uṣṇih=añcU=yuji-kruñc-āṃ ca |
| 3.2.60 | VARIANTS | 0.866 | tyadādiṣu dṛśo 'nālocane kañ ca | tyad-ādi-ṣu dṛś-aḥ=an-ālocane KaÑ ca |
| 3.2.61 | AGREES | 0.901 | sat-sū-dviṣa-druha-duha-yuja-vida-bhidac-chida-ji-nī-rājām uasarge 'pi kvip | sad=sū-dviṣḥ-druhḥ-duhḥ-yujA-vidḥ-bhida-chida-ji-nī-rāj-ām upasarge=api KviP |
| 3.2.62 | VARIANTS | 0.783 | bhajo ṇviḥ | bhaj-aḥ=Ṇvi-ḥ |
| 3.2.63 | AGREES | 0.933 | chandasi sahaḥ | chandas-i sah-aḥ |
| 3.2.64 | AGREES | 0.941 | vahaś ca | vah-aś ca |
| 3.2.65 | AGREES | 0.982 | kavya-purīṣa-purīṣyeṣu ñyuṭ | kavya-purīṣa-purīṣye-ṣu ÑyuṬ |
| 3.2.66 | VARIANTS | 0.821 | havye 'nantaḥpādām | havy-e=an-antaḥ-pādam |
| 3.2.67 | AGREES | 0.951 | jana-sana-khana-krama-gamo viṭ | janA-sanḥ-khana-krama-gam-o viṬ |
| 3.2.68 | VARIANTS | 0.696 | ado 'nanne | ad-aḥ=an=anne |
| 3.2.69 | AGREES | 0.947 | kravye ca | kravy-e ca |
| 3.2.70 | VARIANTS | 0.889 | duhaḥ kab ghaś ca | duh-aḥ KaP=gha-ś ca |
| 3.2.71 | AGREES | 0.952 | mantre śveta-vaha-ukthaśas-puroḍāśo ṇvin | mantre śveta-vah-a-uktha-śas=puro-ḍāś-o ṆviN |
| 3.2.72 | AGREES | 0.900 | ave yajaḥ | av-e yaj-aḥ |
| 3.2.73 | VARIANTS | 0.882 | vij upe chandasi | viC=up-e chandas-i |
| 3.2.74 | VARIANTS | 0.877 | āto manin-kvanib-vanipaś ca | āT-aḥ maniN=KvaniP-vaniP-aś ca |
| 3.2.75 | VARIANTS | 0.844 | anyebhyo 'pi dṛśyante | anye-bhyaḥ=api dṛś-yante |
| 3.2.76 | AGREES | 1.000 | kvip ca | KviP ca |
| 3.2.77 | AGREES | 0.957 | sthaḥ ka ca | sth-aḥ Ka ca |
| 3.2.78 | VARIANTS | 0.897 | supy ajātau ṇinis tācchīlye | sUPy a-jāt-au Ṇini-s tācchily-e |
| 3.2.79 | VARIANTS | 0.788 | kartary upamāme | kartar-i=upa-mān-e |
| 3.2.80 | AGREES | 0.909 | vrate | vrat-e |
| 3.2.81 | AGREES | 0.971 | bahulam ābhīkṣṇye | bahulam ābhīkṣṇy-e |
| 3.2.82 | AGREES | 0.909 | manaḥ | man-aḥ |
| 3.2.83 | AGREES | 0.941 | ātmamāne khaś ca | ātma-mān-e KHaŚ=ca |
| 3.2.84 | AGREES | 0.909 | bhūte | bhūt-e |
| 3.2.85 | AGREES | 0.923 | karaṇe yajaḥ | karaṇ-e yaj-aḥ |
| 3.2.86 | VARIANTS | 0.897 | karamaṇi hanaḥ | karmaṇ-i han-aḥ |
| 3.2.87 | AGREES | 0.926 | brahma-bhrūṇa-vṛtreṣu kvip | brahm(n)-bhrūṇa-vṛtre-ṣu KviP |
| 3.2.88 | AGREES | 0.909 | bahulaṃ chandasi | bahulam chandas-i |
| 3.2.89 | AGREES | 0.930 | su-karma-pāpa-mantra-puṇyeṣu kṛñaḥ | su-karma(n)-pāpa-mantra-puṇye-su kṛÑaḥ |
| 3.2.90 | AGREES | 0.909 | some suñaḥ | som-e suÑ-aḥ |
| 3.2.91 | AGREES | 0.900 | agnau ceḥ | agn-au ce-ḥ |
| 3.2.92 | VARIANTS | 0.864 | karmaṇy-agny-ākhyāyām | karmaṇ-i=agni=ākhyā-yām |
| 3.2.93 | VARIANTS | 0.889 | karmaṇi inir vikriyaḥ | karmaṇ-i=iniḥ=vi-kriy-aḥ |
| 3.2.94 | AGREES | 0.960 | dṛśeḥ kvanip | dṛśe-ḥ KvaniP |
| 3.2.95 | VARIANTS | 0.895 | rājani yudhikṛñaḥ | rājan-i yudh-i-kṛÑ-aḥ |
| 3.2.96 | AGREES | 0.933 | sahe ca | sah-e ca |
| 3.2.97 | AGREES | 0.900 | saptamyāṃ janer ḍaḥ | saptamy-ām jane-r Ḍaḥ |
| 3.2.98 | AGREES | 0.914 | pañcamyām ajātau | pañcamy-ām a-jāt-au |
| 3.2.99 | VARIANTS | 0.889 | upasarge ca sañjñāyām | upa-sarg-e ca saṃjñā-yām |
| 3.2.100 | AGREES | 0.923 | anau karmaṇi | an-au karmaṇ-i |
| 3.2.101 | VARIANTS | 0.872 | anyeṣv api dṛśyate | anye-ṣu=api dṛś-ya-te |
| 3.2.102 | AGREES | 1.000 | niṣṭhā | niṣṭhā |
| 3.2.103 | AGREES | 0.968 | su-yajor ṅvanip | su-yaj-or ṄvaniP |
| 3.2.104 | VARIANTS | 0.897 | jīryater atṛn | jīr-ya-te-r atṚN |
| 3.2.105 | AGREES | 0.960 | chandasi liṭ | chandas-i lIṬ |
| 3.2.106 | VARIANTS | 0.897 | liṭaḥ kānaj vā | lIṬ-aḥ KānaC=vā |
| 3.2.107 | VARIANTS | 0.842 | kvasuś ca | KvasU-s=ca |
| 3.2.108 | VARIANTS | 0.885 | bhāṣāyāṃ sada-vasa-śruvaḥ | bhāṣā-yām sada-vasḥ-śruv-aḥ |
| 3.2.109 | VARIANTS | 0.885 | upeyivān anāśvān anūcānaś ca | upey-i-vān=anāś-vān=anūcānas-s=ca |
| 3.2.110 | AGREES | 1.000 | luṅ | lUṄ |
| 3.2.111 | AGREES | 0.933 | anadyatane laṅ | an-adya-tane lAṄ |
| 3.2.112 | AGREES | 1.000 | abhijñā-vacane lṛṭ | abhijñā-vacane lṚṬ |
| 3.2.113 | AGREES | 0.933 | na yadi | na yad-i |
| 3.2.114 | AGREES | 0.909 | vibhāṣā sākāṅkṣe | vibhāṣā sākāṛkṣ-e |
| 3.2.115 | AGREES | 0.957 | parokṣe liṭ | parokṣ-e lIṬ |
| 3.2.116 | AGREES | 0.973 | ha-śaśvator laṅ ca | ha-śaśvat-or lAṄ ca |
| 3.2.117 | VARIANTS | 0.889 | praśne ca āsanna-kale | praśn-e ca=ā-sanna-kāl-e |
| 3.2.118 | AGREES | 0.933 | laṭ sme | lAṬ sm-e |
| 3.2.119 | AGREES | 0.917 | aparokṣe ca | a-parokṣ-e ca |
| 3.2.120 | AGREES | 0.960 | nanau pṛṣṭa-prati-vacane | nan-au pṛṣṭa-prati-vacan-e |
| 3.2.121 | AGREES | 0.968 | na-nvor vibhāṣā | na-nv-or vibhāṣā |
| 3.2.122 | AGREES | 0.914 | puri luṅ ca asme | pur-i lUṄ ca=a-sm-e |
| 3.2.123 | AGREES | 0.963 | vartamāne laṭ | vartamān-e lAṬ |
| 3.2.124 | VARIANTS | 0.813 | laṭaḥ śatṛ-śānacāv aprathamā-samānādhikaraṇe | lAṬ-aḥ ŚatṚ-ŚanaC-au=a-rathamā-amāna=dhi-araṇ-e |
| 3.2.125 | AGREES | 0.929 | sambodhane ca | sam-bodhan-e ca |
| 3.2.126 | AGREES | 0.958 | lakṣaṇa-hetvoḥ kriyāyāḥ | lakṣaṇa-hetv-oḥ kriyā-yāḥ |
| 3.2.127 | AGREES | 0.933 | tau sat | t-au SAT |
| 3.2.128 | AGREES | 0.968 | pūṅ yajoḥ śānan | pūṄ-yaj-oḥ ŚānaN |
| 3.2.129 | AGREES | 0.971 | tācchīya-vayovacana-śaktiṣu cānaś | tācchīlya-vayovacana-śakti-ṣu CānaŚ |
| 3.2.130 | VARIANTS | 0.885 | iṅ-dhāryoḥ śatra-kṛcchriṇi | iṄ=dhāry-oḥ ŚatṚ=ṛcchriṇ-i |
| 3.2.131 | VARIANTS | 0.714 | dviṣo 'mitre | dviṣ-aḥ=a-mitr-e |
| 3.2.132 | VARIANTS | 0.821 | suño yajñasaṃyoge | suÑ-aḥ=yajña-saṃ-yog-e |
| 3.2.133 | VARIANTS | 0.688 | arhaḥ praśaṃsāyām | arh-aḥ pūjā-yām |
| 3.2.134 | AGREES | 0.930 | ā kveḥ tacchīla-taddharma-tatsādhukāriṣu | ā-kve-ḥ tac-chīla-tad-dharma-tat-sādhu-kāri-ṣu |
| 3.2.135 | AGREES | 1.000 | tṛn | tṛN |
| 3.2.136 | AGREES | 0.927 | alaṅ-kṛñ-nirākṛñ-prajana-utpaca-utpata-unmada-rucy-apatrapa-vṛtu-vṛdhu-saha-cara iṣṇuc | alaṃ-kṛÑ-nir-ā-kṛÑ-pra-jana=ut-pacA=ut-pata=un-mada-ruci-apa-trapa-vṛtU-vṛdhU-sahA-carḥ iṣṇuC |
| 3.2.137 | AGREES | 0.923 | ṇeś chandasi | Ṇe-ś chandas-i |
| 3.2.138 | AGREES | 0.947 | bhuvaś ca | bhuv-aś ca |
| 3.2.139 | AGREES | 0.930 | glā-ji-sthaś ca kṣnuḥ | glā-ji-sthaś ca Ksnu-ḥ |
| 3.2.140 | AGREES | 0.967 | trasi-gṛdhi-dhṛṣi-kṣipeḥ knuḥ | trasi-gṛdhi-dhṛṣi-kṣip-eḥ Knu-ḥ |
| 3.2.141 | VARIANTS | 0.875 | śam-ity aṣṭābhyo ghinuṇ | śam-iti=aṣṭā-bhyaḥ GHinuṆ |
| 3.2.142 | CONFLICTS | 0.436 | saṃpṛca-anurudha-āṅyama-āṅyasa-parisṛ-saṃsṛja-paridevi-saṃjvara-parikṣipa-pariraṭa-parivada-paridaha-parimuha-duṣa-dviṣa-druha-duha-yuja-ākrīḍa-vivica-tyaja-raja-bhaja-aticara-apacara-āmuṣa-abhyāhanaś ca | saṃ-pṛca=anu-rudha=āṄ-yamḥ=āṄ-yasa-pari-sṛ-saṃ-sṛjḥ-pari-devi-saṃ-jvarḥ=pari-kṣipḥ-pari-vadḥ-pari-dahḥ-pari-muhḥ-duṣḥ-dviṣḥ-druhḥ-duhḥ-yuja-ā-krīḍa-vi-vica-tyajḥ-rajḥ-bhajḥ=ati-carḥ=apa-carḥ=ā-muṣḥ=abhy-ā-han-aś ca |
| 3.2.143 | AGREES | 0.900 | vau kaṣa-lasa-kattha-srambhaḥ | v-au kaṣḥ-lasḥ-katthA-srambh-aḥ |
| 3.2.144 | AGREES | 0.923 | ape ca laṣaḥ | ap-e ca laṣ-aḥ |
| 3.2.145 | AGREES | 0.909 | pre lapa-sṛ-dru-matha-vada-vasaḥ | pr-e lapḥ-sṛ-dru-matha-vadḥ-vas-aḥ |
| 3.2.146 | VARIANTS | 0.889 | ninda-hiṃsa-kliśa-khāda-vināśa-parikṣipa-pariraṭa-parivādi-vyābhāṣa-asūyo vuñ | ninda-hiṃsa-kliśA-khāda-vi-nāśa-pari-kliśḥ-pari-raṭḥ-pari-vād-i-vyā-bhāṣA=asūy-aḥ vUÑ |
| 3.2.147 | VARIANTS | 0.875 | devi-kraśoś ca+upasarge | dev-i-kruś-os=ca=upasarge |
| 3.2.148 | VARIANTS | 0.831 | calana-śabdārthād akarmakād yuc | calana-śabda=rth-āt=a-karmak-āt=uC |
| 3.2.149 | AGREES | 0.902 | anudātta-itaś ca halādeḥ | anudātta=IT-as=ca haL-āde-ḥ |
| 3.2.150 | AGREES | 0.909 | ju-caṅkramya-dandramya-sṛ-gṛdhi-jvala-śuca-laṣa-pata-padaḥ | ju-caṛ-kram-ya-dan-dram-ya-sṛ-gṛdhi-jvalḥ-śucḥ-laṣA-pata-pad-aḥ |
| 3.2.151 | AGREES | 0.906 | krudha-maṇḍa-arthebhyaś ca | krudhḥ-maṇḍa=arthe-bhyas=ca |
| 3.2.152 | AGREES | 0.923 | na yaḥ | na y-aḥ |
| 3.2.153 | AGREES | 0.923 | sūda-dīpa-dīkṣaś ca | sūdA-dīpa-dīkṣ-as=ca |
| 3.2.154 | AGREES | 0.964 | laṣa-pata-pada-sthā-bhū-vṛṣa-hana-kama-gama-śṝbhya ukañ | laṣA-pata-padA-sthā-bhū-vṛṣa-hanḥ-kama-gama-śṝ-bhyaḥ=ukaÑ |
| 3.2.155 | VARIANTS | 0.865 | jalpa-bhikṣa-kuṭṭa-luṇṭa-vṛṅaḥ ṣākan | jalpḥ-bhikṣA-kuṭṭḥ-luṇṭḥ-vṛṄ-hyḥ=ṢākaN |
| 3.2.156 | VARIANTS | 0.880 | prajor iniḥ | pra-jo-r ini-ḥ |
| 3.2.157 | AGREES | 0.906 | ji-dṛ-kṣi-viśri-iṇ-vama-avyatha-abhyama-paribhū-prasūbhyaś ca | ji-dṛ-kṣi-vi-śri=iṆ-vamḥ=a-vyathA=abhḥ-amA-pari-bhū-pra-sū-bhyas=ca |
| 3.2.158 | AGREES | 0.916 | spṛhi-gṛhi-pati-dayi-nidrā-dandrā-śraddhābhya āluc | spṛh-i-gṛh-i-pat-i-dayi-ni-drā-tandrā-śrad-dhā-bhyaḥ=āluC |
| 3.2.159 | VARIANTS | 0.880 | dā-dheṭ-si-śada-sado ruḥ | dā-dheṬ-si-śada-sad-aḥ=u-ḥ |
| 3.2.160 | AGREES | 0.927 | sṛ-ghasy-adaḥ kmarac | sṛ-ghasi=ad-aḥ KmaraC |
| 3.2.161 | VARIANTS | 0.880 | bhañja-bhāsa-mido ghurac | bhanja-bhāsa-mid-aḥ=GHuraC |
| 3.2.162 | AGREES | 0.980 | vidi-bhidi-cchideḥ kurac | vidi-bhidi-cchide-ḥ KuraC |
| 3.2.163 | AGREES | 0.964 | iṇ-naś-ji-sartibhyaḥ kvarap | iṆ-naś-ji-sar-ti-bhyaḥ KvaraP |
| 3.2.164 | VARIANTS | 0.800 | gatvaraś ca | ga-t-vara-s=ca |
| 3.2.165 | AGREES | 0.909 | jāgur ūkaḥ | jāgu-r ūka-ḥ |
| 3.2.166 | VARIANTS | 0.818 | yaja-japa-daśāṃ yaṅaḥ | yajḥ-japḥ-daś-ām yaṄ-aḥ |
| 3.2.167 | AGREES | 0.905 | nami-kampi-smy-ajasa-kama-hiṃsa-dīpo raḥ | nami-kampi-smi=a-jasa-kama-hiṃsa-dīp-aḥ=ra-ḥ |
| 3.2.168 | AGREES | 0.909 | san-āśaṃsa-bhikṣa uḥ | saN=ā-śaṃsa-bhikṣ-aḥ=u-ḥ |
| 3.2.169 | VARIANTS | 0.867 | vindur icchuḥ | vind-u-r icch-u-ḥ |
| 3.2.170 | VARIANTS | 0.889 | kyāc chandasi | Kyāt=chandas-i |
| 3.2.171 | AGREES | 0.919 | ād-ṛ-gama-hana-janaḥ ki-kinau liṭ ca | āṭ=ṛ-gama-hanḥ-jan-aḥ Ki-Kin-au=lIṬ ca |
| 3.2.172 | VARIANTS | 0.848 | svapitṛṣornajiṅ | svapi-tṛṣ-oḥ=najiṄ |
| 3.2.173 | AGREES | 0.938 | śṝ-vandyor āruḥ | śṝ-vandy-or āru-ḥ |
| 3.2.174 | AGREES | 0.950 | bhiyaḥ kru-klukanau | bhiy-aḥ Kru-KlukaN-au |
| 3.2.175 | AGREES | 0.935 | sthā-īśa-bhāsa-pisa-kaso varac | sthā-īśA-bhāsA-pisa-kas-aḥ=varaC |
| 3.2.176 | VARIANTS | 0.846 | yaś ca yaṅaḥ | y-as=ca yaṄ-aḥ |
| 3.2.177 | AGREES | 0.953 | bhrāja-bhāsa-dhurvi-dyuta-urji-pṝ-jugrāvastuvaḥ kvip | bhrāja-bhāsa-dhurvi-dyutA=ūrji-pṝ-ju-grāva-stuv-aḥ KviP |
| 3.2.178 | VARIANTS | 0.818 | anyebhyo 'pi dṛśyate | anye-bhyaḥ=api dṛś-ya-te |
| 3.2.179 | AGREES | 0.917 | bhuvaḥ sañjñā-antarayoḥ | bhuv-aḥ saṃjñā=antaray-oḥ |
| 3.2.180 | VARIANTS | 0.833 | vi-pra-sambhyo ḍv-asañjñāyām | vi-pra-sam-bhyaḥ=Ḍu=a-saṃjñā-yām |
| 3.2.181 | VARIANTS | 0.895 | dhaḥ karamṇi ṣṭran | dh-aḥ karmaṇ-i ṢṭraN |
| 3.2.182 | AGREES | 0.930 | dām-nī-śasa-yu-yuja-stu-tuda-si-sica-miha-pata-daśa-nahaḥ karaṇe | dāP-nī-śasa-yu-yuja-stu-tudḥ-si-sicA-mihḥ-pata-daśḥ-nah-aḥ karaṇe |
| 3.2.183 | AGREES | 0.952 | hala-sūkarayoḥ puvaḥ | hala-sūkaray-oḥ puv-aḥ |
| 3.2.184 | AGREES | 0.921 | arti-lū-dhū-sū-khana-saha-cara itraḥ | ar-ti-lū-dhū-sū-khana-śahA-car-aḥ=itra-ḥ |
| 3.2.185 | VARIANTS | 0.875 | puvaḥ sañjñāyām | puv-aḥ saṃjñā-yām |
| 3.2.186 | VARIANTS | 0.875 | kartari carṣidevatayoḥ | kartar-i ca=ṛṣi-devatay-oḥ |
| 3.2.187 | VARIANTS | 0.750 | ñītaḥ ktaḥ | ÑI=IT-aḥ Kta-ḥ |
| 3.2.188 | AGREES | 0.951 | mati-buddhi-pūjā-arthebhyaś ca | mati-buddhi-pūjā=arthe-bhyas=ca |
| 3.3.1 | VARIANTS | 0.848 | uṇādayo bahulam | uṆ=āday-aḥ=bahulam |
| 3.3.2 | VARIANTS | 0.895 | bhūte 'pi dṛśyante | bhūt-e=api dṛś-yante |
| 3.3.3 | VARIANTS | 0.851 | bhaviṣyati gamyādayaḥ | bhaviṣyat-i gami(n)=āday-aḥ |
| 3.3.4 | AGREES | 0.939 | yāvat-purā-nipātayor laṭ | yāvat-purā-nipātay-oḥ=lAṬ |
| 3.3.5 | AGREES | 0.976 | vibhāṣā kadā-karhyoḥ | vibhāṣā kadā-karhy-oḥ |
| 3.3.6 | AGREES | 0.919 | kiṃvṛtte lipsāyām | kiṃ-vṛtt-e lipsā-yām |
| 3.3.7 | AGREES | 0.913 | lipsyamāna-siddhau ca | lip-sya-m-āna-siddh-au ca |
| 3.3.8 | VARIANTS | 0.850 | loḍ-arthalakṣane ca | lOṬ=artha-lakṣaṇ-e ca |
| 3.3.9 | AGREES | 0.980 | liṅ ca+ūrdhva-mauhūrtike | lIṄ ca=ūrdhva-mauhūrtik-e |
| 3.3.10 | AGREES | 0.907 | tumun-ṇvulau kriyāyāṃ kriya-arthāyām | tumuN=ṆvuL-au kriyā-yām kriyā-arthā-yām |
| 3.3.11 | AGREES | 1.000 | bhāva-vacanāś ca | bhāva-vacanāś ca |
| 3.3.12 | AGREES | 0.963 | aṇ karmaṇi ca | aṆ karmaṇ-i ca |
| 3.3.13 | AGREES | 0.957 | lṛṭ śeṣe ca | lṚṬ śeṣ-e ca |
| 3.3.14 | VARIANTS | 0.833 | lṛṭaḥ sadvā | lṚṬ-aḥ SAT=vā |
| 3.3.15 | AGREES | 0.903 | anadyatane luṭ | an-adya-tan-e lUṬ |
| 3.3.16 | VARIANTS | 0.885 | pada-ruja-viśa-spṛśo ghañ | padA-ruja-viśḥ-spṛś-aḥ=GHaÑ |
| 3.3.17 | AGREES | 0.947 | sṛ sthire | sṛ sthir-e |
| 3.3.18 | AGREES | 0.909 | bhāve | bhāv-e |
| 3.3.19 | AGREES | 0.900 | akartari ca kārake sañjñāyām | a-kartar-i ca kārak-e saṃjñā-yām |
| 3.3.20 | VARIANTS | 0.897 | parimāṇa-ākhyāyāṃ sarvebhyaḥ | parimaṇa=ākhyā-yām sarve-bhyaḥ |
| 3.3.21 | VARIANTS | 0.800 | iṅaś ca | iṄ-as=ca |
| 3.3.22 | AGREES | 0.933 | upasarge ruvaḥ | upasarg-e ruv-aḥ |
| 3.3.23 | AGREES | 0.944 | sami yu-dru-duvaḥ | sam-i yu-dru-duv-aḥ |
| 3.3.24 | VARIANTS | 0.627 | śri-ṇī-bhuvo 'nupasarge | śri-ṇī-bhuv-aḥ=anyatara-syām |
| 3.3.25 | VARIANTS | 0.867 | vau kṣu-śruvaḥ | v-au kṣu-sruv-aḥ |
| 3.3.26 | AGREES | 0.933 | ava-udor niyaḥ | ava=ud-or niy-aḥ |
| 3.3.27 | AGREES | 0.947 | pre dru-stu-sruvaḥ | pr-e dru-stu-sruv-aḥ |
| 3.3.28 | VARIANTS | 0.895 | nir-abhyoḥ pū-lvoḥ | nis=abhy-oḥ pū-lv-oḥ |
| 3.3.29 | VARIANTS | 0.846 | un-nyor graḥ | ud=ny-or gr-aḥ |
| 3.3.30 | AGREES | 0.947 | kṝ dhānye | kṝ dhāny-e |
| 3.3.31 | AGREES | 0.919 | yajñe sami stuvaḥ | yajñ-e sam-i stuv-aḥ |
| 3.3.32 | VARIANTS | 0.743 | pre stro 'yajñe | pr-e str-aḥ=a-yajñ-e |
| 3.3.33 | VARIANTS | 0.810 | prathane vāv aśabde | prathan-e v-au=a-śabd-e |
| 3.3.34 | AGREES | 0.933 | chandonāmni ca | chando-nāmn-i ca |
| 3.3.35 | AGREES | 0.909 | udi grahaḥ | ud-i grah-aḥ |
| 3.3.36 | AGREES | 0.917 | sami muṣṭau | sam-i muṣṭ-au |
| 3.3.37 | AGREES | 0.943 | pari-nyor nī-ṇor dyūta-abhreṣayoḥ | pari-ny-or nī-iṆ-or dyūta-abhreṣa-yoḥ |
| 3.3.38 | VARIANTS | 0.708 | parāv anupātyaya iṇaḥ | par-au=an-upa=atyay-e=iṆ-aḥ |
| 3.3.39 | VARIANTS | 0.880 | vy-upayoḥ śeteḥ paryāye | vi=upay-oḥ śete-ḥ pary-āy-e |
| 3.3.40 | VARIANTS | 0.857 | hasta-adāne cer asteye | hasta=ā-dān-e ce-r a-stey-e |
| 3.3.41 | AGREES | 0.905 | nivāsa-citi-śarīra-upasamādhāneṣv ādeś ca kaḥ | nivāsa-citi-śarīra-upa-sam-ā-dhāne-ṣu ādes=ca ka-ḥ |
| 3.3.42 | AGREES | 0.906 | saṅghe ca anauttarādharye | saṃgh-e ca=an-auttarādhary-e |
| 3.3.43 | AGREES | 0.931 | karma-vyatihāre ṇac striyām | karma-vy-ati-hār-e ṆaC striy-ām |
| 3.3.44 | AGREES | 0.933 | abhividhau bhāve inuṇ | abhi-vidh-au bhāv-e=inuṆ |
| 3.3.45 | VARIANTS | 0.851 | ākrośe 'vanyor grahaḥ | ā-kroś-e=ava-ny-or grah-aḥ |
| 3.3.46 | AGREES | 0.923 | pre lipsāyām | pr-e lipsā-yām |
| 3.3.47 | AGREES | 0.917 | parau yajñe | par-au yajñ-e |
| 3.3.48 | AGREES | 0.929 | nau vṛ dhānye | n-au vṛ dhāny-e |
| 3.3.49 | AGREES | 0.915 | udi śrayati-yauti-pū-druvaḥ | ud-i śray-a-ti-yau-ti-pū-druv-aḥ |
| 3.3.50 | AGREES | 0.955 | vibhāṣā+āṅi ru-pluvoḥ | vibhāṣā=āṄ-i ru-pluv-oḥ |
| 3.3.51 | VARIANTS | 0.881 | ave graho varṣa-pratibandhe | av-e grah-aḥ=varṣa-prati-bandh-e |
| 3.3.52 | AGREES | 0.917 | pre vaṇijām | pr-e vaṇij-ām |
| 3.3.53 | AGREES | 0.947 | raśmau ca | raśm-au ca |
| 3.3.54 | VARIANTS | 0.872 | vṛṇoter ācchādane | vṛ-ṇo-te-r ā-cchādan-e |
| 3.3.55 | VARIANTS | 0.773 | prau bhuvo 'vajñāne | par-au bhuv-aḥ=ava-jñān-e |
| 3.3.56 | AGREES | 0.909 | er ac | e-r aC |
| 3.3.57 | VARIANTS | 0.875 | ṝdor ap | ṝd-o-r aP |
| 3.3.58 | VARIANTS | 0.830 | graha-vṛ-dṛ-niścigamaś ca | grahḥ-vṛ-dṛ-nis=ci-gam-aḥ=ca |
| 3.3.59 | VARIANTS | 0.857 | upasarge 'daḥ | upasarg-e ad-aḥ |
| 3.3.60 | AGREES | 0.947 | nau ṇa ca | n-au Ṇa ca |
| 3.3.61 | VARIANTS | 0.898 | vyadha-japor anupasarge | vyadhḥ-jap-or an-upasarg-e |
| 3.3.62 | VARIANTS | 0.897 | svana-hasor vā | svanḥ-has-or vā |
| 3.3.63 | VARIANTS | 0.894 | yamaḥ sam-upa-ni-viṣu ca | yam-aḥ sam-upa-ni-vi-ṣu |
| 3.3.64 | VARIANTS | 0.852 | nau gada-nada-paṭha-svanaḥ | n-au gadḥ-nadḥ-paṭhḥ-svan-aḥ |
| 3.3.65 | VARIANTS | 0.857 | kvaṇo vīṇāyāṃ ca | kvaṇ-aḥ=vīṇā-yāṃ=ca |
| 3.3.66 | VARIANTS | 0.889 | nityaṃ paṇaḥ parimāṇe | nityam paṇ-aḥ pari-māṇ-e |
| 3.3.67 | VARIANTS | 0.765 | mado 'nupasarge | mad-aḥ=an=upasarg-e |
| 3.3.68 | VARIANTS | 0.898 | pramada-sammadau harṣe | pra-mad-a-sam-mad-au harṣ-e |
| 3.3.69 | AGREES | 0.930 | sam-udor ajaḥ paśuṣu | sam-ud-or aj-aḥ paśu-ṣu |
| 3.3.70 | AGREES | 0.929 | akṣeṣu glahaḥ | akṣe-ṣu glah-aḥ |
| 3.3.71 | VARIANTS | 0.875 | prajane sarteḥ | pra-jan-e sar-te-ḥ |
| 3.3.72 | AGREES | 0.900 | hvaḥ samprasāraṇaṃ ca ny-abhy-upa-viṣu | hv-aḥ sam-pra-sāraṇaṃ ca ni=abhi=upa-vi-ṣu |
| 3.3.73 | AGREES | 0.909 | āṅi yuddhe | āṄ-i yuddh-e |
| 3.3.74 | VARIANTS | 0.848 | nipānam āhāvaḥ | ni-pān-am ā-hāv-a-ḥ |
| 3.3.75 | VARIANTS | 0.857 | bhāve 'nupasargasya | bhāv-e=an-upa-sarga-sya |
| 3.3.76 | VARIANTS | 0.848 | hanaś ca vadhaḥ | han-as=ca vadh-a-ḥ |
| 3.3.77 | AGREES | 0.929 | mūrtau ghanaḥ | mūrt-au ghana-ḥ |
| 3.3.78 | VARIANTS | 0.800 | antarghano deśe | antar-ghan-a-ḥ=deś-e |
| 3.3.79 | VARIANTS | 0.857 | agāra-ekadeśe praghaṇaḥ praghāṇāś ca | agāra=eka-deś-e pra-ghaṇ-a=pra-ghāṇ-au ca |
| 3.3.80 | VARIANTS | 0.744 | udghano 'tyādhānam | ud-ghan-a-ḥ aty-ā-dhāna-m |
| 3.3.81 | VARIANTS | 0.667 | apaghano 'ṅgam | apa-ghan-a-ḥ=aṛga-m |
| 3.3.82 | VARIANTS | 0.800 | karaṇe 'yo-vidruṣu | karaṇ-e ayas=vi-dru-ṣu |
| 3.3.83 | AGREES | 0.960 | stambe ka ca | stamb-e Ka ca |
| 3.3.84 | AGREES | 0.909 | parau ghaḥ | par-au gha-ḥ |
| 3.3.85 | VARIANTS | 0.824 | upaghna āśraye | upa-ghn-a-ḥ ā-śray-e |
| 3.3.86 | VARIANTS | 0.879 | saṅgha-udghau gaṇa-praśaṃsayoḥ | saṃ-gh-a=ud-gh-au gaṇa-pra-śaṃsay-oḥ |
| 3.3.87 | VARIANTS | 0.750 | nigho nimitam | ni-gh-a-ḥ=niimita-m |
| 3.3.88 | VARIANTS | 0.815 | ḍvitaḥ ktriḥ | ḌU=IT=aḥ=Ktri-ḥ |
| 3.3.89 | VARIANTS | 0.640 | ṭvito 'thuc | ṬU-IT-aḥ=athuC |
| 3.3.90 | VARIANTS | 0.872 | yaja-yāca-yata-viccha-praccha-rakṣo naṅ | yajA-yāca-yata-vichḥ-prachḥ-rakṣ-aḥ=naṄ |
| 3.3.91 | VARIANTS | 0.800 | svapo nan | svap-aḥ=naN |
| 3.3.92 | VARIANTS | 0.895 | upasarge ghoḥ kiḥ | upa-sarg-e GHO-ḥ Ki-ḥ |
| 3.3.93 | VARIANTS | 0.889 | karmaṇy adhikaraṇe ca | karmaṇ-i=adhi-karaṇ-e ca |
| 3.3.94 | VARIANTS | 0.880 | striyāṃ ktin | striy-ām KtiN |
| 3.3.95 | VARIANTS | 0.864 | sthā-gā-pāpaco bhāve | sthā-gā-pā-pac-ām bhāv-e |
| 3.3.96 | AGREES | 0.940 | mantre vṛṣa-iṣa-paca-mana-vida-bhū-vī-rā udāttaḥ | mantr-e vṛṣa=iṣA-pacA-manA-vidḥ-bhū-vī-rā-ḥ udātta-ḥ |
| 3.3.97 | VARIANTS | 0.883 | ūti-yūti-jūti-sāti-heti-kīrtayaś ca | ū-ti-yū-ti-jū-ti-sā-ti-he-ti-kīr-tay-as=ca |
| 3.3.98 | AGREES | 0.913 | vraja-yajor bhāve kyap | vrajḥ-yaj-or bhāv-e KyaP |
| 3.3.99 | AGREES | 0.902 | sañjñāyāṃ sam-aja-niṣada-nipata-mana-vida-ṣuñ-śīṅ-bhṛñ-iṇaḥ | saṃjñā-yām sam-ajḥ-ni-ṣada-ni-pata-manA-vidḥ-ṣuÑ-śīṄ-bhṛÑ=iṆ-aḥ |
| 3.3.100 | AGREES | 0.957 | kṛñaḥ śa ca | kṛÑ-aḥ Śa ca |
| 3.3.101 | VARIANTS | 0.727 | iccyā | icch-ā |
| 3.3.102 | AGREES | 0.917 | a pratyayāt | a praty-ay-āt |
| 3.3.103 | VARIANTS | 0.867 | guroś ca halaḥ | guro-s=ca haL-aḥ |
| 3.3.104 | VARIANTS | 0.714 | ṣid-bhidādibhyo 'ṅ | Ṣ-IT=bhid-ā=ādi-bhyaḥ=aṄ |
| 3.3.105 | VARIANTS | 0.899 | cinti-pūji-kathi-kumbi-carcaś ca | cint-i-pūj-i-kath-i-kumb-i-carc-as=ca |
| 3.3.106 | VARIANTS | 0.857 | ātaś ca+upasarge | āT=as=ca=upa-sarg-e |
| 3.3.107 | VARIANTS | 0.789 | ṇy-āsa-śrantho yuc | Ṇi=āsA-sranth-aḥ=yuC |
| 3.3.108 | AGREES | 0.943 | roga-ākhyāyaṃ ṇvul bahulam | roga=ākhyā-yāṃ ṆvuL bahulam |
| 3.3.109 | VARIANTS | 0.842 | sañjñāyām | saṃjñā-yām |
| 3.3.110 | AGREES | 0.917 | vibhā-āṣakhyāna-paripraśnayor iñ ca | vibhāṣā=ākhyāna-pari-praśna-yor iÑ ca |
| 3.3.111 | AGREES | 0.923 | paryāya-arha-rṇa-utpattiṣu ṇvuc | pary-āya=arha=ṛṇa=ut-patti-ṣu ṆvuC |
| 3.3.112 | VARIANTS | 0.778 | ākrośe nañy atiḥ | ā-kroś-e naÑ-i=ani-ḥ |
| 3.3.113 | AGREES | 0.900 | kṛtya-lyuṭo bahulam | kṛtya-Lyuṭ-aḥ=bahulam |
| 3.3.114 | AGREES | 0.930 | napuṃsake bhāve ktaḥ | napuṃsak-e bhāv-e Kta-ḥ |
| 3.3.115 | AGREES | 1.000 | lyuṭ ca | LyuṬ ca |
| 3.3.116 | AGREES | 0.920 | karmaṇi ca yena saṃsparśāt kartuḥ śarīra-sukham | karmaṇ-i ca y-ena saṃ-spraś-āt kart-uḥ śarīra-sukha-m |
| 3.3.117 | AGREES | 0.917 | karaṇa-adhikaraṇayoś ca | karaṇa-adhi-karaṇay-os=ca |
| 3.3.118 | VARIANTS | 0.867 | puṃsi sañjñāyāṃ ghaḥ prāyeṇa | puṃs-i saṃjñā-yām GHa-ḥ prāy-eṇa |
| 3.3.119 | AGREES | 0.902 | gocara-sañcara-vaha-vraja-vyaja-āpaṇa-nigamāś ca | go-cara-saṃ-cara-vaha-vraja=vyaj-a=ā-paṇ-a-ni-gamās=ca |
| 3.3.120 | AGREES | 0.944 | ave tṝ-stror ghañ | av-e tṝ-str-or GHaÑ |
| 3.3.121 | VARIANTS | 0.824 | halaś ca | haL-as=ca |
| 3.3.122 | VARIANTS | 0.851 | adhyāya-nyāya-udyāva-saṃhāra-ādhāra-āvāyāś ca | adhy-āy-a-ny-āy-a-ud-yāv-a-saṃ-hār-a=ā-dhār-a=ā-vayās=ca |
| 3.3.123 | VARIANTS | 0.647 | udaṅko 'nudake | ud-aṛk-a-ḥ=an-udak-e |
| 3.3.124 | VARIANTS | 0.857 | jālam ānāyaḥ | jāl-am ā-nāy-a-ḥ |
| 3.3.125 | VARIANTS | 0.846 | khano gha ca | khan-aḥ=GHa ca |
| 3.3.126 | AGREES | 0.953 | īṣad-duḥ-suṣu kṛcchra-akṛccra-artheṣu khal | īṣad-dus-su-ṣu kṛcchra=akṛcchra=artheṣu KHaL |
| 3.3.127 | VARIANTS | 0.893 | kartṛ-karmaṇoś ca bhū-krñoḥ | kartṛ-karmaṇ-os=ca bhū-kṛÑ-oḥ |
| 3.3.128 | VARIANTS | 0.750 | āto yuc | āT-aḥ=yuC |
| 3.3.129 | AGREES | 0.960 | chandasi gaty-arthebhyaḥ | chandas-i gaty-arthe-bhyaḥ |
| 3.3.130 | VARIANTS | 0.818 | anyebhyo 'pi dṛśyate | anye-bhyaḥ=api dṛś-ya-te |
| 3.3.131 | AGREES | 0.925 | vartamāna-sāmīpye vartamānavad vā | vartamāna-sāmīpy-e vartamāna-at=vā |
| 3.3.132 | VARIANTS | 0.844 | āśaṃsāyāṃ bhūtavac ca | ā-śaṃsā-yām bhūta-vat=ca |
| 3.3.133 | AGREES | 0.971 | kṣipra-vacane lṛṭ | kṣipra-vacan-e lṚṬ |
| 3.3.134 | AGREES | 0.944 | āśaṃsā-vacane liṅ | ā-śaṃsā-vacan-e lIṄ |
| 3.3.135 | AGREES | 0.944 | na anadyatanavat kriyāprabandha-sāmīpyayoḥ | na=an-adya-tana-vat kriyā-prabandha-sāmīpyay-oḥ |
| 3.3.136 | VARIANTS | 0.892 | bhaviṣyati maryādā-vacane 'varasmin | bhav-i-ṣyat-i maryādā-acan-e=avara-smin |
| 3.3.137 | AGREES | 0.906 | kāla-vihbhāge ca anahorātrāṇām | kāla-vi-bhāg-e ca=an-aho-rātrā-ṇām |
| 3.3.138 | AGREES | 0.970 | parasmin vibhāṣā | para-smin vibhāṣā |
| 3.3.139 | AGREES | 0.954 | liṅ-nimitte lṛṅ kriyā-atipattau | lIṄ-nimitt-e lṚṄ kriyā=ati-patt-au |
| 3.3.140 | AGREES | 0.941 | bhūte ca | bhūt-e ca |
| 3.3.141 | VARIANTS | 0.897 | vā-ū-uta-apyoḥ | vā=ā=uta=apy-oḥ |
| 3.3.142 | VARIANTS | 0.875 | garhāyāṃ laḍ-api-jātvoḥ | garhā-yām lAṬ=api-jātv-oḥ |
| 3.3.143 | AGREES | 0.933 | vibhāṣa kathami liṅ ca | vibhāṣā katham-i lIṄ ca |
| 3.3.144 | AGREES | 0.923 | kiṃvṛtte liṅ-lṛṭau | kiṃ-vṛtt-e lIṄ-lṚṬ-au |
| 3.3.145 | VARIANTS | 0.816 | anavaklṛpty-amarṣayor akiṃvṛtte 'pi | an-ava-kḷpti=a-marṣay-or a-kiṃ-vṛtt-e=api |
| 3.3.146 | AGREES | 0.920 | kiṃkila-asty-artheṣu lṛṭ | kiṃ=kila=asti=arthe-ṣu lṚṬ |
| 3.3.147 | AGREES | 0.966 | jātu-yador liṅ | jātu-yad-or lIṄ |
| 3.3.148 | VARIANTS | 0.828 | yaccayatrayoḥ | yat=ca-yatray-oḥ |
| 3.3.149 | AGREES | 0.957 | garhāyāṃ ca | garhā-yāṃ ca |
| 3.3.150 | AGREES | 0.933 | citrīkaraṇe ca | citrī-karaṇ-e ca |
| 3.3.151 | VARIANTS | 0.848 | śeṣe lṛḍ-ayadau | śeṣ-e lṚṬ=a-yad-au |
| 3.3.152 | AGREES | 0.906 | uta-apyoḥ samarthayor liṅ | uta-apy-oḥ sam-arthay-oḥ=lIṄ |
| 3.3.153 | VARIANTS | 0.880 | kāma-pravedane 'kacciti | kāma-pra-vedan-e=a-kaccit-i |
| 3.3.154 | VARIANTS | 0.878 | sambhāvane 'lam iti cet siddha-aprayoge | sam-bhavān-e=alam iti cet siddha=a-prayog-e |
| 3.3.155 | AGREES | 0.911 | vibhāṣā dhātau sambhāvana-vacane 'yadi | vibhāṣā dhāt-au sam-bhāvana-acan-e=a-yadi |
| 3.3.156 | AGREES | 0.947 | hetu-hetumator liṅ | hetu-hetu-mat-or lIṄ |
| 3.3.157 | AGREES | 0.958 | icchā-artheṣu liṅ-loṭau | icchā=arthe-ṣu lIṄ-lOṬ-au |
| 3.3.158 | AGREES | 0.978 | samāna-kartṛkeṣu tumun | samāna-kartṛke-ṣu tumuN |
| 3.3.159 | AGREES | 1.000 | liṅ ca | lIṄ ca |
| 3.3.160 | VARIANTS | 0.857 | icchārthebhyo vibhāṣā vartamāne | icchā-arthe-bhyaḥ=vibhāṣā vart-a-m-ān-e |
| 3.3.161 | VARIANTS | 0.864 | vidhi-nimantraṇa-āmantraṇa-adhīṣṭa-saṃpraśna-prārthaneṣu liṅ | vidhi-ni-mantr-aṇa-ā-mantr-aṇa=adhi=iṣṭa-sam-praś-na-pra=arth-ane-ṣu lIṄ |
| 3.3.162 | AGREES | 1.000 | loṭ ca | lOṬ ca |
| 3.3.163 | AGREES | 0.925 | praiṣa-atisarga-prāptakāleṣu kaṛtyāś ca | praiṣa=ati-sarga-prāpta-kāle-ṣu kṛtyās=ca |
| 3.3.164 | AGREES | 0.939 | liṅ ca+ūrdhva-mauhūrtike | lIṄ ca=ūrdhva-mauhurtik-e |
| 3.3.165 | AGREES | 0.933 | sme loṭ | sm-e lOṬ |
| 3.3.166 | AGREES | 0.952 | adhīṣṭe ca | adhīṣṭ-e ca |
| 3.3.167 | AGREES | 0.980 | kāla-samaya-velāsu tumun | kāla-samaya-velā-su tumuN |
| 3.3.168 | AGREES | 0.941 | liṅ yadi | lIṄ yad-i |
| 3.3.169 | AGREES | 0.900 | arhe kṛtya-tṛcaś ca | arh-e kṛtya-tṛC-as=ca |
| 3.3.170 | AGREES | 0.931 | āvaśyaka-ādhamarṇyayor ṇiniḥ | āvaśyaka=ādhamarṇyay-oḥ=Ṇini-ḥ |
| 3.3.171 | VARIANTS | 0.889 | kṛtyāś ca | kṛtyās=ca |
| 3.3.172 | AGREES | 0.957 | śaki liṅ ca | śak-i lIṄ ca |
| 3.3.173 | AGREES | 0.938 | āśiṣi liṅ loṭau | āśiṣ-i lIṄ-lOṬ-au |
| 3.3.174 | AGREES | 0.913 | ktic-ktau ca sañjñāyām | KtiC=Kt-au ca saṃjñā-yām |
| 3.3.175 | AGREES | 0.941 | māṅi luṅ | māṄ-i lUṄ |
| 3.3.176 | AGREES | 0.971 | sma-uttare laṅ ca | sma=uttar-e lAṄ ca |
| 3.4.1 | AGREES | 0.943 | dhātu-sambandhe pratyayāḥ | dhātu-sam-bandh-e praty-ayāḥ |
| 3.4.2 | AGREES | 0.917 | kriyāsam-abhihāre loṭ loṭo hi-svau vā ca ta-dhvamoḥ | kriyā-sam-abhi-hār-e lOṬ, lOṬ-aḥ=hi-sv-au vā ca ta-dhvam-oḥ |
| 3.4.3 | VARIANTS | 0.816 | sayuccaye 'nyatarasyām | sam-uc-cay-e=anya-tara-syām |
| 3.4.4 | VARIANTS | 0.886 | yathāvidhy-anuprayogaḥ pūrvasmin | yathā-vidhi=anu-pra-yog-a-ḥ pūrva-smin |
| 3.4.5 | VARIANTS | 0.897 | samuccaye sāmānya-vacanasya | sam=ut=cay-e sāmānya-vacana-sya |
| 3.4.6 | AGREES | 0.957 | chandasi luṅ-laṅ-liṭaḥ | chandas-i lUṄ-lAṄ-lIṬ-aḥ |
| 3.4.7 | AGREES | 0.963 | liṅ-arthe leṭ | lIṄ=arth-e lEṬ |
| 3.4.8 | VARIANTS | 0.840 | upasaṃvāda-āśaṅkayoś ca | upa-saṃ-vāda=ā-śaṛkay-os=ca |
| 3.4.9 | AGREES | 0.976 | tumarthe se-sen-ase-asen-kṣe-kasen-adhyai-adhyain-kadhyai-kadhyain-śadhyai-śadhyain-tavai-taveṅ-tavenaḥ | tum=arth-e se-seN-ase=aseN-Kse-KaseN+adhyai=adhyaiN-Kadhyai-KadhyaiN-Śadhyai-ŚadhyaiN-tavai-taveṄ-taveN-aḥ |
| 3.4.10 | AGREES | 0.982 | prayai rohiṣyai avyathiṣyai | prayai rohiṣyai a-vyathiṣyai |
| 3.4.11 | AGREES | 1.000 | dṛśe vikhye ca | dṛśe vikhye ca |
| 3.4.12 | AGREES | 0.919 | śaki ṇamulkamulau | śak-i ṆamuL-KamuL-au |
| 3.4.13 | AGREES | 0.952 | īśvare tosun-kasunau | īśvar-e tosuN-KasuN-au |
| 3.4.14 | AGREES | 0.971 | kṛtya-arthe tavai-ken-kenya-tvanaḥ | kṛtya=arth-e tavai-Ken-Kenya-tvaN-aḥ |
| 3.4.15 | AGREES | 0.917 | avacakṣe ca | ava-cakṣ-e ca |
| 3.4.16 | AGREES | 0.924 | bhāval-akṣane sthā-iṇ-kṛñ-vadi-cari-hu-tami-janibhyas tosun | bhāva-laksaṇ-e sthā=iṆ-kṛ-vadi-cari-hu-tami-jani-bhyas tosuN |
| 3.4.17 | AGREES | 0.970 | sṛpi-tṛdoḥ kasun | sṛpi-tṛd-oḥ KasuN |
| 3.4.18 | AGREES | 0.911 | alaṃ-khalvoḥ pratiṣedhayoḥ prācāṃ ktvā | alam=khalv-oḥ prati-ṣedhay-oḥ prācām Ktvā |
| 3.4.19 | VARIANTS | 0.809 | udīcāṃ māṅo vyatīhāre | udīc-ām māṄ-aḥ=vy-atīhār-e |
| 3.4.20 | AGREES | 0.973 | para-avara-yoge ca | para=avara-yog-e ca |
| 3.4.21 | AGREES | 0.931 | samāna-kartuṛkayoḥ pūrvakāle | samāna-kartṛkay-oḥ pūrva-kāl-e |
| 3.4.22 | AGREES | 0.973 | ābhīkṣṇye ṇamul ca | ābhīkṣṇy-e ṆamuL ca |
| 3.4.23 | VARIANTS | 0.789 | na yady anākāṅkṣe | na yad-i=an-ā-kāṛkṣ-e |
| 3.4.24 | AGREES | 0.933 | vibhāṣā 'gre prathama-pūrveṣu | vibhāṣā=agr-e=prathama-pūrve-ṣu |
| 3.4.25 | VARIANTS | 0.897 | karmaṇy ākrośe kṛñaḥ khamuñ | karmaṇ-i=ā-kroś-e kṛÑ-aḥ KHamuÑ |
| 3.4.26 | AGREES | 0.963 | svādumi ṇamul | svādum-i ṆamuL |
| 3.4.27 | AGREES | 0.900 | anyathā-evaṃ-katham-itthaṃsu siddha-aprayogaś-cet | anyathā=evam=katham=ittham-su siddha=a=rayoga-s=cet |
| 3.4.28 | AGREES | 0.955 | yathā-tathayor asūyā-prativacane | yathā-tathay-or asūyā-prati-vacan-e |
| 3.4.29 | AGREES | 0.909 | karmaṇi dṛśi-vidoḥ sākalye | karman-i dṛśi-vid-oḥ sākaly-e |
| 3.4.30 | AGREES | 0.923 | yāvati vinda-jīvoḥ | yā-vat-i vinda-jīv-oḥ |
| 3.4.31 | VARIANTS | 0.889 | carma-udarayoḥ pūreḥ | carma(n)=udaray-oḥ pūr-e-ḥ |
| 3.4.32 | VARIANTS | 0.732 | varṣa-pramāṇa ūlopaś ca asya anyatrasyām | varṣa-pra-māṇ-e=ū-lpa-s=ca=sya=nyatarāsyam |
| 3.4.33 | VARIANTS | 0.880 | cele knopeḥ | cel-e knop-e-ḥ |
| 3.4.34 | AGREES | 0.917 | nimūla-samūlayoḥ kaṣaḥ | ni-mūla-sa-mūlay-oḥ kaṣ-aḥ |
| 3.4.35 | AGREES | 0.943 | śuṣka-cūrṇa-rūkṣeṣu piṣaḥ | śuṣ-ka-cūrṇa-rūkṣe-ṣu piṣ-aḥ |
| 3.4.36 | AGREES | 0.930 | samūla-akṛta-jīveṣu han-kṛñ-grahaḥ | sa-mūla=a-kṛta-jīve-ṣu han-kṛÑ-grah-ḥ |
| 3.4.37 | VARIANTS | 0.889 | karaṇe hanaḥ | kar-aṇ-e han-aḥ |
| 3.4.38 | VARIANTS | 0.897 | snehane piṣaḥ | sneh-an-e piṣ-aḥ |
| 3.4.39 | AGREES | 0.923 | haste varti-grahoḥ | hast-e vart-i-grah-oḥ |
| 3.4.40 | AGREES | 0.900 | sve puṣaḥ | sv-e puṣ-aḥ |
| 3.4.41 | VARIANTS | 0.850 | adhikaraṇe vandhaḥ | adhi-kar-aṇ-e bandh-aḥ |
| 3.4.42 | VARIANTS | 0.842 | sañjñāyām | saṃjñā-yām |
| 3.4.43 | AGREES | 0.941 | kartor jīva-puruṣayor naśi-vahoḥ | kartr-or jīva-puruṣay-or naśi-vah-oḥ |
| 3.4.44 | AGREES | 0.944 | ūrdhve śuṣi-pūroḥ | ūrdhv-e śuṣi-pūr-oḥ |
| 3.4.45 | AGREES | 0.923 | upamāne karmaṇi ca | upa-mān-e karmaṇ-i ca |
| 3.4.46 | VARIANTS | 0.866 | kaṣādiṣu yathāvidhy-anuprayogaḥ | kaṣ-ādi-ṣu yathā-vidhi=nu-pra-yoga-ḥ |
| 3.4.47 | AGREES | 0.927 | upadaṃśas tṛtīyāyām | upa-daṃś-as tṛtīyā-yām |
| 3.4.48 | VARIANTS | 0.886 | hiṃsā-arthānāṃ ca samānakarmakāṇām | hiṃsā=arthānāṃ ca sa-māna-artṛkā-ṇām |
| 3.4.49 | AGREES | 0.928 | saptamyāṃ ca+upapīḍa-rudha-karṣaḥ | saptamy-ām ca=upa-pīḍA-rudha-karṣ-aḥ |
| 3.4.50 | VARIANTS | 0.870 | samāsattau | sam-ā-satt-au |
| 3.4.51 | AGREES | 0.909 | pramāṇe ca | pra-māṇ-e ca |
| 3.4.52 | VARIANTS | 0.878 | apādāne parīpsāyām | apa=ā-dān-e parīpsā-yām |
| 3.4.53 | VARIANTS | 0.889 | dvitiyāyāṃ ca | dvitīyā-yāṃ ca |
| 3.4.54 | VARIANTS | 0.667 | svāṅge 'dhruve | sva=aṛg-e=a-dhruv-e |
| 3.4.55 | VARIANTS | 0.821 | pariklaśyamāne ca | pari-kliś-ya-m-ān-e ca |
| 3.4.56 | VARIANTS | 0.885 | viśi-pati-padi-skandām vyāpyamāna-āsevyamānayoḥ | viśi-pati-padi-skand-āṃ vy-āp-ya-m-āna-ā-sev-ya-m-ānay-oḥ |
| 3.4.57 | VARIANTS | 0.866 | asyati-tṛṣoḥ kriyāntare kāleṣu | as-ya-ti-tṛṣ-aḥ kriyā=antar-e kāle-ṣu |
| 3.4.58 | VARIANTS | 0.872 | nāmny-ādiśi-grahoḥ | nāmn-i=ā-diśi-grah-oḥ |
| 3.4.59 | AGREES | 0.931 | avyaye 'yathābhipreta-ākhyāne kṛñaḥ ktvā-ṇamulau | avyay-e=a-yathābhipreta=ākhyān-e kṛÑ-aḥ Ktvā-ṆamuL-au |
| 3.4.60 | VARIANTS | 0.857 | tiryacy apavarge | tiryac-i=apa-varg-e |
| 3.4.61 | VARIANTS | 0.833 | svāṅge tas-pratyaye kṛbhvoḥ | sva=aṛg-e tas-pratyay-e kṛ-bhv-oḥ |
| 3.4.62 | AGREES | 0.921 | nā-dhā-arthapratyaye cvy-arthe | nā-dhā-artha-pratyay-e Cvi=arth-e |
| 3.4.63 | AGREES | 0.933 | tūṣṇīmi bhuvaḥ | tūṣṇīm-i bhuv-aḥ |
| 3.4.64 | VARIANTS | 0.824 | anvacy ānulomye | anv-ac-i ānu-lomy-e |
| 3.4.65 | AGREES | 0.944 | śaka-dhṛṣa-jñā-glā-ghaṭa-rabha-labha-krama-saha-arha-asty-artheṣu tumun | śaka-dhṛṣḥ-jñā-glāghaṭA-rabhA-labhA-krama-sahA-arhḥ-asti=arthe-ṣu tumuN |
| 3.4.66 | AGREES | 0.906 | paryāpti-vacaneṣv alam-artheṣu | pary-āp-ti-vacane-ṣu=alam-arthe-ṣu |
| 3.4.67 | AGREES | 0.957 | kartari kṛt | kartar-i kṛt |
| 3.4.68 | AGREES | 0.922 | bhavya-geya-pravacanīya-upasthānīya-janya-āplāvya-āpātyā vā | bhav-ya-ge-ya-pra-vac-anīya=upa-sthān-īya-jan-ya=āplāv-ya=ā-pāt-yā vā |
| 3.4.69 | AGREES | 0.911 | laḥ karmaṇi ca bhāve ca akramakebhyaḥ | l-aḥ karmaṇ-i ca bhāv-e ca=a-karmake-bhyaḥ |
| 3.4.70 | AGREES | 0.984 | tayor eva kṛtya-kta-khal-arthāḥ | tay-or eva kṛtya-Kta-KHaL-arthāḥ |
| 3.4.71 | VARIANTS | 0.893 | ādikarmaṇi ktaḥ kartari ca | adi-karmaṇ-i Kta-ḥ kartar-i ca |
| 3.4.72 | VARIANTS | 0.857 | gaty-artha-akramaka-śliṣa-śīṅ-sthā-āsa-vasa-jana-ruha-jīryatibhyaś ca | gaty=arthaa-karma-ka=śliṣḥ-śīṄ=shthā=āsA-vasḥ-jana-ruhḥ-jīr-ya-ti-bhyaḥ |
| 3.4.73 | VARIANTS | 0.898 | dāśa-goghnau sampradāne | dāśa-goghn-au sam-pra-dā-e |
| 3.4.74 | MISSING | - | bhīma-ādayo 'pādāne | - |
| 3.4.75 | AGREES | 0.923 | tābhyām anyatra-uṇādayaḥ | tā-bhyām anya-tra=uṆ=āday-aḥ |
| 3.4.76 | VARIANTS | 0.872 | kto 'dhikaraṇe ca dhrauvya-gati-pratyavasāna-arthebhyaḥ | Kta-ḥ=adhi-kar-aṇ-e ca dhrauvya-gati-prati=ava-sāna=rthe-bhyaḥ |
| 3.4.77 | AGREES | 0.909 | lasya | la-sya |
| 3.4.78 | AGREES | 0.962 | tip-tas-jhi-sip-thas-tha-mib-vas-mas-ta-ātāṃ-jha-thās-āthām-dhvam-iḍ-vahi-mahiṅ | tiP-tas-jhi=siP-thas-tha=miP-vas-mas=ta=ātām=jha=thās-āthām-dhvam=iṬ-vahi-mahiṄ |
| 3.4.79 | VARIANTS | 0.846 | ṭita ātmanepadānāṃ ṭere | Ṭ-IT-aḥ=ātmanepadā-nām ṬE-r e |
| 3.4.80 | VARIANTS | 0.889 | thāsaḥ se | thā-aḥ=se |
| 3.4.81 | AGREES | 0.958 | liṭas ta-jhayor eś-irec | lIṬ-as ta-jhay-or eŚ-ireC |
| 3.4.82 | AGREES | 0.929 | prasmaipadānāṃ ṇal-atus-us-thal-thus-aṇal-va-māḥ | parsmaipadā-nām ṆaL-atus-us-thaL-athus-a-ṆaL-va-māḥ |
| 3.4.83 | VARIANTS | 0.714 | vido laṭo vā | vid-aḥ=lAṬ-aḥ=vā |
| 3.4.84 | VARIANTS | 0.873 | bruvaḥ pañcānām ādita āho bruvaḥ | bruv-aḥ pañcā-nām ādi-taḥ=āha-ḥ=bruv-aḥ |
| 3.4.85 | VARIANTS | 0.800 | loṭo laṅvat | lOṬ-aḥ=lAṄ-vat |
| 3.4.86 | VARIANTS | 0.833 | er uḥ | e-r u-ḥ |
| 3.4.87 | VARIANTS | 0.774 | ser hy apic ca | se-r hi=a-P-IT=ca |
| 3.4.88 | AGREES | 0.957 | vā chandasi | vā chandas-i |
| 3.4.89 | VARIANTS | 0.875 | mer niḥ | me-r ni-ḥ |
| 3.4.90 | AGREES | 0.933 | ām etaḥ | ām eT-aḥ |
| 3.4.91 | VARIANTS | 0.833 | sa-vābhyām vāmau | sa-vā-bhyām va=am-au |
| 3.4.92 | VARIANTS | 0.850 | āḍ uttamasya pic ca | āṬ=uttama-sya P-IT=ca |
| 3.4.93 | VARIANTS | 0.857 | eta ai | eT-aḥ=ai |
| 3.4.94 | VARIANTS | 0.667 | leṭo 'ḍ-āṭau | lEṬ-aḥ aṬ-āṬ-au |
| 3.4.95 | VARIANTS | 0.857 | āta ai | āT-aḥ=ai |
| 3.4.96 | VARIANTS | 0.774 | vā-eto 'nyatra | vā=eT-aḥ=anya-tra |
| 3.4.97 | VARIANTS | 0.881 | itaś ca lopaḥ parasmaipadesu | iT-as=ca lopa-ḥ parasmaipade-ṣu |
| 3.4.98 | VARIANTS | 0.889 | sa uttamasya | s-aḥ=uttama-sya |
| 3.4.99 | VARIANTS | 0.846 | nityaṃ ḍitaḥ | nityaṃ Ṅ-IT-aḥ |
| 3.4.100 | VARIANTS | 0.800 | itaś ca | iT-as=ca |
| 3.4.101 | AGREES | 0.914 | tas-thas-tha-mipām tāṃ-taṃ-ta-amaḥ | tas-thas-tha-miP-ām tām-tam-ta=am-aḥ |
| 3.4.102 | AGREES | 0.957 | liṅaḥ sīyuṭ | lIṄ-aḥ sīyuṬ |
| 3.4.103 | VARIANTS | 0.812 | yāsuṭ parasmaipadesu udātto ṅic ca | yāsuṬ parasipade-ṣu=dātta-ḥ=Ṅ-IT=ca |
| 3.4.104 | VARIANTS | 0.700 | kid āśisi | K-IT=āśiṣ-i |
| 3.4.105 | AGREES | 0.952 | jhasya ran | jha-sya raN |
| 3.4.106 | CONFLICTS | 0.571 | iṭo 't | iṬ-aḥ=aT |
| 3.4.107 | AGREES | 0.909 | suṭ tithoḥ | suṬ ti-th-oḥ |
| 3.4.108 | VARIANTS | 0.889 | jher jusū | jhe-r Jus |
| 3.4.109 | VARIANTS | 0.863 | sij-abhyasta-vidibhyaś ca | sīC=abhyasta-vidi-bhyas=ca |
| 3.4.110 | VARIANTS | 0.889 | ātaḥ | āT-aḥ |
| 3.4.111 | AGREES | 0.958 | laṅaḥ śākaṭāyanasya+eva | lAṄ-aḥ śākaṭāyana-sya=eva |
| 3.4.112 | VARIANTS | 0.842 | dviṣaś ca | dviṣ-as=ca |
| 3.4.113 | AGREES | 0.977 | tiṅ-śit-sārvadhātukam | tiṄ-Ś-IT sārvadhātukam |
| 3.4.114 | AGREES | 0.900 | ārdhadhātukaṃ śeṣaḥ | ārdhadhātuka-m śeṣa-ḥ |
| 3.4.115 | AGREES | 1.000 | liṭ ca | lIṬ ca |
| 3.4.116 | AGREES | 0.947 | liṅ āśiṣi | lIṄ āśiṣ-i |
| 3.4.117 | MISSING | - | chandasy ubhayathā | - |
| 4.1.1 | VARIANTS | 0.865 | ṅy-āp-prātipadikāt | Nī-āP-prātipadik-āt |
| 4.1.2 | AGREES | 0.919 | sv-au-jas-am-auṭ-chaṣ-ṭā-bhyāṃ-bhis-ṅebhyām-bhyas-ṅasi-bhyāṃ-bhyas-ṅas-os-ām-ṅy-os-sup | sU=au-Jas=am-auṬ=Śas=Ṭā-bhyām-bhis=Ṅe-bhyām-bhyas=ṄasI-bhyām-bhyas-Ṅas-os-ām=Ṅi-os-suP |
| 4.1.3 | AGREES | 0.933 | striyām | striy-ām |
| 4.1.4 | VARIANTS | 0.800 | ajādy-ataṣ ṭāp | aja=ādi=aTas=ṬāP |
| 4.1.5 | VARIANTS | 0.786 | ṛn-nebhyo ṅīp | ṛT=ne-bhyaḥ=ṄīP |
| 4.1.6 | VARIANTS | 0.700 | ugitaś ca | uK=IT-as=ca |
| 4.1.7 | VARIANTS | 0.818 | vano ra ca | van-aḥ=ra ca |
| 4.1.8 | VARIANTS | 0.789 | pādo 'nyatarasyām | pād-aḥ=anya-tara-syām |
| 4.1.9 | VARIANTS | 0.800 | ṭāb ṛci | ṬāP=ṛc-i |
| 4.1.10 | VARIANTS | 0.878 | na ṣaṭsvasrādibhyaḥ | na ṣaṭ-svasṛ=ādi-bhyaḥ |
| 4.1.11 | AGREES | 0.909 | manaḥ | man-aḥ |
| 4.1.12 | VARIANTS | 0.839 | ano bahuvrīheḥ | an-aḥ=bahuvrīhe-ḥ |
| 4.1.13 | AGREES | 0.909 | ḍāb ubhābhyām anyatarasyām | ḌāP=ubhā-bhyām anya-tara-syām |
| 4.1.14 | VARIANTS | 0.897 | anupasarjanāt | an-upa-sarjan-āt |
| 4.1.15 | VARIANTS | 0.836 | ṭiḍ-ḍha-aṇ-añ-dvayasaj-daghnañ-mātrac-tayap-ṭhak-ṭhañ-kañ-kvarapkhyunām | Ṭ-IT=ḍha=aṆ= aÑ=dvayasaC=daghnaC-mātraC=tayaP--ṭhaÑ-kaÑ-KvaraP-aḥ |
| 4.1.16 | VARIANTS | 0.824 | yañaś ca | yaÑ=as=ca |
| 4.1.17 | AGREES | 0.909 | prācāṃ ṣpha taddhitaḥ | prāc-ām Ṣpha taddhita-ḥ |
| 4.1.18 | AGREES | 0.923 | sarvatra lohitādi-katantebhyaḥ | sarvatra lohita=ādi=kata=ante-bhyaḥ |
| 4.1.19 | AGREES | 0.980 | kauravya-māṇḍūkābhyāṃ ca | kauravya-māṇḍūkā-bhyāṃ ca |
| 4.1.20 | AGREES | 0.938 | vayasi prathame | vayas-i pratham-e |
| 4.1.21 | AGREES | 0.923 | dvigoḥ | dvigo-ḥ |
| 4.1.22 | AGREES | 0.907 | aparimāṇa-bista-ācita-kambalyebhyo na taddhitaluki | a-pari-māṇa-bista=ā-cita-kambalye-bhya-ḥ na taddhita-luK-i |
| 4.1.23 | AGREES | 0.947 | kāṇḍa-antāt kṣetre | kāṇḍa=ant-āt kṣetr-e |
| 4.1.24 | VARIANTS | 0.885 | puruṣāt pramāṇe 'nyatarasyām | puruṣ-āt pra-māṇ-e=anya-tara-syām |
| 4.1.25 | VARIANTS | 0.889 | bahuvrīher ūdhaso ṅīṣ | bahuvrīhe-r ūdhas-aḥ=ṄīṢ |
| 4.1.26 | VARIANTS | 0.791 | saṅkhyāvyayāderṅīp | saṃkhyā=avyaya=ād e-r ṄīP |
| 4.1.27 | VARIANTS | 0.857 | dāma-hāyana-anāc ca | dāma(n)=hāyana=ant-āt=ca |
| 4.1.28 | VARIANTS | 0.787 | ana upadhālopino 'nyatarasyām | an-aḥ=upadhā-opin-aḥ=nya-ara-yām |
| 4.1.29 | VARIANTS | 0.894 | nityaṃ sañjñā-chandasoḥ | nityam saṃjñā-chandas-oḥ |
| 4.1.30 | AGREES | 0.947 | kevala-māmaka-bhāgadheya-pāpa-apara-samāna-āryakṛta-sumaṅgala-bheṣajāc ca | kevala-māmaka-bhāga-dheya-pāpa=apara-samāna=ārya-kṛta-su-maṛgala-bheṣaj-āt=ca |
| 4.1.31 | VARIANTS | 0.857 | rātreś ca ajasau | rātre-s=ca a-Jas-au |
| 4.1.32 | AGREES | 0.957 | antarvat-pativator nuk | antar-vat-pativat-or nuK |
| 4.1.33 | VARIANTS | 0.840 | patyur no yajñasaṃyoge | patyu-r na-ḥ=yajña-saṃ-yog-e |
| 4.1.34 | AGREES | 0.947 | vibhāṣā sapūrvasya | vibhāṣā sa-pūrva-sya |
| 4.1.35 | VARIANTS | 0.857 | nityaṃ sapatnyādiṣu | nitya-ṃ sa-patnī=ādi-ṣu |
| 4.1.36 | AGREES | 0.941 | pūtakrator ai ca | pūta-krato-r ai ca |
| 4.1.37 | AGREES | 0.911 | vṛṣākapy-agni-kusita-kusidānām udāttaḥ | vṛṣā-kapi=agni-kusita-kusīdā-nām udātta-ḥ |
| 4.1.38 | AGREES | 1.000 | manor au vā | manor au vā |
| 4.1.39 | VARIANTS | 0.789 | varṇād anudāttāt topadhātto naḥ | varṇ-āt=anudātt-āt ta=upadh-āt t-aḥ na-ḥ |
| 4.1.40 | VARIANTS | 0.818 | anyato ṅīṣ | anya-taḥ=ṄīṢ |
| 4.1.41 | VARIANTS | 0.718 | ṣid-gaurādibhyaś ca | Ṣ-IT=gaura=ādi-bhyaḥ |
| 4.1.42 | AGREES | 0.953 | jānapada-kuṇḍa-goṇa-sthala-bhāja-nāga-kāla-nīla-kuśa-kāmuka-kabarād vṛtty-amatra-āvapana-akṛtrimā-śrāṇā-sthaulya-varṇa-anācchādana-ayovikāra-maithunecchā-keśaveśeṣu | jānapada-kuṇḍa-goṇa-sthala-bhāja-nāga-kāla-nīla-kuśa-kāmuka-kabar-āt vṛtti=amatra=ā-vapana=a-kṛtrimā-śrāṇā-sthaulya-varṇa=an-ā-cchādana=ayo-vikāra-maithuna=icchā-keśa-veśe-ṣu |
| 4.1.43 | VARIANTS | 0.880 | śoṇāt prācām | śoṇ-āt prā-ām |
| 4.1.44 | VARIANTS | 0.850 | vā+uto guṇavacanāt | vā=uT-aḥ=guṇa-vacan-āt |
| 4.1.45 | VARIANTS | 0.824 | bahva-ādibhyaś ca | bahu=ādi-bhyas=ca |
| 4.1.46 | AGREES | 0.938 | nityaṃ chandasi | nitya-ṃ chandas-i |
| 4.1.47 | VARIANTS | 0.842 | bhuvaś ca | bhuv-as=ca |
| 4.1.48 | VARIANTS | 0.865 | puṃyogād ākhyāyām | puṃ-yog-āt=ākhyā-yām |
| 4.1.49 | AGREES | 0.988 | indra-varuṇa-bhava-śarva-rudra-mṛḍa-hima-araṇya-yava-yavana-mātula-ācāryāṇāmānuk | indra-varuṇa-bhava-śarva-rudra-mṛḍa-hima=araṇya-yava-yavana-mātula-ācāryā-ṇām ānuK |
| 4.1.50 | AGREES | 0.930 | krītāt karaṇa-pūrvāt | krī-t-āt karaṇa-pūrv-āt |
| 4.1.51 | VARIANTS | 0.811 | ktād alpāakhyāyām | Kt-āt alpa=ākhyā-yām |
| 4.1.52 | VARIANTS | 0.808 | bahuvrīheś ca antodattāt | bahuvrīhe-s=ca=anta=udātt-āt |
| 4.1.53 | VARIANTS | 0.844 | asvāṅga-pūrvapadād vā | a-svāṛga-pūrva-pad-āt=vā |
| 4.1.54 | VARIANTS | 0.829 | svāṅgāc ca+upasarjanād asaṃyoga-upadhāt | svāṛg-āt=ca=upa-sarj-an-āt=a-aṃyoga=padh-āt |
| 4.1.55 | AGREES | 0.926 | nāsikā-udara-oṣṭha-jaṅghā-danta-karṇa-śṛṅgāc ca | nāsikā=udara=oṣṭha-jaṛghā-danta-karṇa-śṛṛg-āt=ca |
| 4.1.56 | AGREES | 0.905 | na kroḍādi-bahvacaḥ | na kroḍa=ādi-bahv-aC-aḥ |
| 4.1.57 | VARIANTS | 0.842 | saha-nañ-vidyamāna-pūrvāc ca | saha-naÑ-vid-ya-m-āna-pūrv-āt |
| 4.1.58 | AGREES | 0.913 | nakha-mukhāt sañjñāyām | nakha-mukh-āt saṃjñā-yām |
| 4.1.59 | AGREES | 0.920 | dīrghajihvī ca cchandasi | dīrgha-jihv-ī ca=chandas-i |
| 4.1.60 | VARIANTS | 0.895 | dik-pūrvapadān ṅīp | dik-pūrva-pad-āt ṄīP |
| 4.1.61 | AGREES | 0.909 | vāhaḥ | vāh-aḥ |
| 4.1.62 | VARIANTS | 0.868 | sakhy aśiṣvī iti bhāṣāyām | sakhī=a-śiśv-ī=iti bhāṣā-yām |
| 4.1.63 | VARIANTS | 0.879 | jāter astrīviṣayād aya-upadhāt | jāte-r a-strī-viṣay-āt=a-ya=upadh-āt |
| 4.1.64 | AGREES | 0.963 | pāka-karṇa-parṇa-puṣpa-phala-mūla-vāla-uttarapadāc ca | pāka-karṇa-parṇa-puṣpa-phala-mūla-vāla=uttara-pad-āt=ca |
| 4.1.65 | VARIANTS | 0.811 | ito manusya-jāteḥ | iT-aḥ=manuṣya-jāte-ḥ |
| 4.1.66 | AGREES | 0.933 | ūṅ utaḥ | ūṄ uT-aḥ |
| 4.1.67 | VARIANTS | 0.829 | bāhvantāt sañjñāyām | bāhu=ant-āt saṃjñā-yām |
| 4.1.68 | VARIANTS | 0.737 | paṅgoś ca | paṛgo-s=ca |
| 4.1.69 | VARIANTS | 0.898 | ūru-uttarapadād aupamye | ūru-uttara-pad-āt=aupamy-e |
| 4.1.70 | AGREES | 0.943 | saṃhita-śapha-lakṣaṇa-vāma-ādeś ca | saṃ-hita-śapha-lakṣaṇa-vāma=āde-s=ca |
| 4.1.71 | AGREES | 0.926 | kadru-kamaṇḍalvoś chandasi | kadru-kamaṇḍalv-os=chandas-i |
| 4.1.72 | VARIANTS | 0.842 | sañjñāyām | saṃjñā-yām |
| 4.1.73 | VARIANTS | 0.826 | śārṅgarava-ādy-año ṅīn | śārṛgarava=ādi=aÑ-aḥ=ṄīN |
| 4.1.74 | VARIANTS | 0.842 | yaṅaś cāp | yaṄ-as=CāP |
| 4.1.75 | VARIANTS | 0.762 | āvaṅyāc ca | āvaṭy-āt=ca |
| 4.1.76 | AGREES | 0.947 | taddhitāḥ | taddhit-āḥ |
| 4.1.77 | VARIANTS | 0.800 | yūnas tiḥ | yūn-as ti-h |
| 4.1.78 | AGREES | 0.915 | aṇ-iñor anārṣayor guru-upottamayoḥ ṣyaṅ gotre | aṆ-iÑ-or an-ārṣay-or guru=pottamay-os=ṢyaṄ gotr-e |
| 4.1.79 | AGREES | 0.929 | gora-avayavāt | gotra=avayav-āt |
| 4.1.80 | VARIANTS | 0.865 | krauḍy-ādibhyaś ca | krauḍi=ādi-bhyas=ca |
| 4.1.81 | AGREES | 0.909 | daivayajñi-śaucivṛkṣi-sātyamugri-kāṇṭheviddhibhyo 'nyatarasyām | daiva-yajñi-śauci-vṛkṣi-sātya-m-ugri-kāṇṭhe-viddhi-bhyaḥ=nya-tara-syām |
| 4.1.82 | VARIANTS | 0.880 | samarthānāṃ prathamād vā | samarthā-nām pratham-āt=vā |
| 4.1.83 | VARIANTS | 0.812 | prāg dīvyato 'ṇ | prāg dīvyat-aḥ=aṆ |
| 4.1.84 | VARIANTS | 0.829 | aśvapatyādibhyaś ca | aśva-pati=ādi-bhyas=ca |
| 4.1.85 | VARIANTS | 0.864 | dity-adity-āditya-paty-uttarapadāṇ ṇyaḥ | diti=aditi-āditya-pati=uttara-pad-āt Ṇya-ḥ |
| 4.1.86 | VARIANTS | 0.812 | utsa-ādibhyo 'ñ | utsa-ādi-bhyaḥ=aÑ |
| 4.1.87 | AGREES | 0.932 | strī-puṃsābhyāṃ nañ-snañau bhavanāt | strī-puṃsā-bhyām naÑ-snaÑ-au bhavan-āt |
| 4.1.88 | VARIANTS | 0.878 | dvigor lug-anapatye | dvigo-r luK=an-apaty-e |
| 4.1.89 | VARIANTS | 0.774 | gotre 'lug-aci | gotr-e=a-luK=aC-i |
| 4.1.90 | AGREES | 0.941 | yūni luk | yūn-i luK |
| 4.1.91 | AGREES | 0.941 | phak-phiñor anyatarasyām | phaK-phiÑ-or anya-tara-syām |
| 4.1.92 | AGREES | 0.929 | tasya apatyam | ta-sya=apatya-m |
| 4.1.93 | VARIANTS | 0.762 | eko gotre | eka-ḥ=gotr-e |
| 4.1.94 | VARIANTS | 0.773 | gotrād yūny astriyāṃ | gotr-āt=yūn-i=a-striy-ām |
| 4.1.95 | VARIANTS | 0.857 | ata iñ | aT-aḥ=iÑ |
| 4.1.96 | VARIANTS | 0.848 | bāhv-ādibhyaś ca | bāhu=ādi-bhyas=ca |
| 4.1.97 | AGREES | 0.941 | sudhātur akaṅ ca | su-dhātu-r akaṄ ca |
| 4.1.98 | AGREES | 0.926 | gotre kuñja-ādibhyaś cphañ | gotr-e kuñja=ādi-bhyas=CphaÑ |
| 4.1.99 | AGREES | 0.914 | naḍādibhyaḥ phak | naḍa=ādi-bhyaḥ phaK |
| 4.1.100 | VARIANTS | 0.750 | harita-ādibhyo 'ñaḥ | harita=ādibhyaḥ=aÑ-aḥ |
| 4.1.101 | VARIANTS | 0.870 | yañ-iñoś ca | yaÑ=iÑ-os=ca |
| 4.1.102 | VARIANTS | 0.896 | śaradvac-chunaka-darbhād bhṛgu-vatsa-āgrāyaṇeṣu | śarad-vat-śunaka-darbh-āt bhṛgu-vatsa=āgrāyaṇe-ṣu |
| 4.1.103 | VARIANTS | 0.886 | droṇa-parvata-jīvantād anyatarasyām | droṇa-parvata-jīvant-āt=nya-ara-yām |
| 4.1.104 | VARIANTS | 0.862 | anṛṣy-ānantarye bida-ādibhyo 'ñ | an-ṛṣi=ānantary-e bida=ādibhyaḥ=aÑ |
| 4.1.105 | AGREES | 0.914 | garga-ādibhyo yañ | garga=ādibhyaḥ=yaÑ |
| 4.1.106 | VARIANTS | 0.841 | madhu-babhvror brāhmaṇa-kauśikayoḥ | madhu-babhrv-or brāhmaṇa-kauśike-ṣu |
| 4.1.107 | VARIANTS | 0.810 | kapi-bodhād āṅgirase | kapi-bodh-āt=āṛgiras-e |
| 4.1.108 | VARIANTS | 0.870 | vataṇḍāc ca | vataṇḍ-āt=ca |
| 4.1.109 | AGREES | 0.957 | luk striyām | luK striy-ām |
| 4.1.110 | VARIANTS | 0.882 | aśvādibhyaḥ phañ | aśva=ādibhyaḥ phaK |
| 4.1.111 | AGREES | 0.944 | bhargāt traigarte | bharg-āt traigart-e |
| 4.1.112 | VARIANTS | 0.839 | śiva-ādibhyo 'ṇ | śiva=ādibhyaḥ=aṆ |
| 4.1.113 | VARIANTS | 0.841 | avṛddhābhyo nadī-mānuṣībhyas tannāmikābhyaḥ | a-vṛddhā-bhyaḥ=nadī-mānuṣī-hyaḥ=an-āmikā-hyaḥ |
| 4.1.114 | AGREES | 0.918 | ṛṣy-andhaka-vṛṣṇi-kurubhyaś ca | ṛṣi=andhaka-vṛṣṇi-kuru-bhyas=ca |
| 4.1.115 | AGREES | 0.919 | mātur ut saṅkhyā-saṃ-bhadra-pūrvāyāḥ | mātu-r uT saṃkhyā-sam=bhadra-pūrvā-yāḥ |
| 4.1.116 | AGREES | 0.973 | kanyāyāḥ kanīna ca | kanyā-yāḥ kanīna ca |
| 4.1.117 | AGREES | 0.926 | vikarṇa-śuṅga-chaṅgalād vatsa-bharadvāja-atriṣu | vikarṇa-śuṛga-chagal-āt vatsa-bharadvāja=atri-ṣu |
| 4.1.118 | AGREES | 0.900 | pīlāyā vā | pīlā-yāḥ=vā |
| 4.1.119 | AGREES | 0.909 | ṭhak ca maṇḍūkāt | ḍhaK ca maṇḍūk-āt |
| 4.1.120 | VARIANTS | 0.857 | strībhyo ḍhak | strī-bhyaḥ=ḍhaK |
| 4.1.121 | VARIANTS | 0.875 | dvyacaḥ | dvy-aC-aḥ |
| 4.1.122 | VARIANTS | 0.839 | itaś-ca-aniñaḥ | iT=as=ca=an-iÑ=aḥ |
| 4.1.123 | AGREES | 0.919 | śubhra-ādibhyaś ca | śubhra=ādi-bhyas=ca |
| 4.1.124 | VARIANTS | 0.885 | vikarṇa-kuṣītakāt kāṣyape | vikarṇa-kuśītak-āt kāśyap-e |
| 4.1.125 | VARIANTS | 0.786 | bhravo vuk ca | bhruv-aḥ=vuK ca |
| 4.1.126 | VARIANTS | 0.895 | kalyāṇyādīnām inaṅ | kalyāṇī=ādī-nām inaṄ |
| 4.1.127 | VARIANTS | 0.762 | kulaṭāyā | kulaṭā-yāḥ=vā |
| 4.1.128 | AGREES | 0.966 | caṭakāyā airak | caṭakāyāḥ=airaK |
| 4.1.129 | AGREES | 0.929 | godhāyā ḍhrak | godhā-yāḥ=ḍhraK |
| 4.1.130 | VARIANTS | 0.870 | ārag udīcām | āraK udīc-ām |
| 4.1.131 | VARIANTS | 0.857 | kṣudrābhyo vā | kṣudrā-bhyaḥ=vā |
| 4.1.132 | VARIANTS | 0.839 | pitṛṣvasuś chaṇ | pitṛ-ṣva-us=chaṆ |
| 4.1.133 | VARIANTS | 0.833 | ṭhaki lopaḥ | ḍhaK-i lopa-ḥ |
| 4.1.134 | VARIANTS | 0.897 | mātṛ-ṣvasuś ca | mātṛ-ṣvas-us=ca |
| 4.1.135 | VARIANTS | 0.865 | catuṣpādbhyo ḍhañ | catuṣ-pād-bhyaḥ=ḍhaÑ |
| 4.1.136 | VARIANTS | 0.857 | gṛṣṭy-ādibhyaś ca | gṛṣṭi=ādi-bhyas=ca |
| 4.1.137 | VARIANTS | 0.811 | rāja-śvaśurād yat | rāja(n)-śvasur-āt=yaT |
| 4.1.138 | VARIANTS | 0.846 | kṣatrād ghaḥ | kṣatr-āt gha-ḥ |
| 4.1.139 | AGREES | 0.909 | kulāt khaḥ | kul-āt kha-ḥ |
| 4.1.140 | VARIANTS | 0.810 | apūrvapadād anyatrasyāṃ yaṅ-ḍhakañau | a-pūrva-pad-āt=anya-tara-syām yḥt=ḍhakaÑ-au |
| 4.1.141 | VARIANTS | 0.878 | mahākulād añ-khañau | mahā-kul-āt=aÑ-khaÑ-au |
| 4.1.142 | VARIANTS | 0.857 | duṣkulāḍ ḍhak | duṣ-kul-āt ḍhaK |
| 4.1.143 | VARIANTS | 0.833 | svasuś chaḥ | svas-us=cha-ḥ |
| 4.1.144 | AGREES | 0.903 | bhrātur vyac ca | bhrāt-ur vyaT=ca |
| 4.1.145 | AGREES | 0.960 | vyan sapatne | vyaN sapatn-e |
| 4.1.146 | VARIANTS | 0.878 | revaty-ādibhyaṣ ṭhak | revatī=ādi-bhyaḥ=ṭhaK |
| 4.1.147 | AGREES | 0.964 | gotra-striyāḥ kutsane ṇa ca | gotra-striy-āḥ kutsan-e Ṇa ca |
| 4.1.148 | AGREES | 0.935 | vṛddhāṭ ṭhak sauvīreṣu bahulam | vṛddh-āt=ṭhaK sauvīre-ṣu bahulam |
| 4.1.149 | VARIANTS | 0.870 | pheś cha ca | phe-s=cha ca |
| 4.1.150 | AGREES | 0.909 | phāṇḍāhṛti-mimatābhyāṃ ṇa-phiñau | phāṇṭāhṛti-mimatā-bhyām Ṇa-phiÑ-au |
| 4.1.151 | VARIANTS | 0.778 | kurvādibhyo ṇyaḥ | kuru=ādi-bhyaḥ=Ṇya-ḥ |
| 4.1.152 | AGREES | 0.915 | senānta-lakṣaṇa-kāribhyaś ca | senā=anta-lakṣaṇa-kāri-bhyas=ca |
| 4.1.153 | AGREES | 0.947 | udīcām iñ | udīc-ām iÑ |
| 4.1.154 | AGREES | 0.914 | tikādibhyaḥ phiñ | tika=ādi-bhyaḥ phiÑ |
| 4.1.155 | AGREES | 0.941 | kauśalya-kārmāryābhyāṃ ca | kausalya-kārmāryā-bhyāṃ ca |
| 4.1.156 | VARIANTS | 0.769 | aṇo dvyacaḥ | aṆ-aḥ=dvy-aC-aḥ |
| 4.1.157 | VARIANTS | 0.833 | udīcāṃ vṛddhād agotrāt | udīc-ām vṛddh-āt=a-gotr-āt |
| 4.1.158 | VARIANTS | 0.878 | vākina-adīnāṃ kuk ca | vākina=ādī-nām kuK ca |
| 4.1.159 | VARIANTS | 0.816 | putrāntād anyatarasyām | putra=ant-āt=anya-tara-syām |
| 4.1.160 | AGREES | 0.949 | prācām avṛddhāt phin bahulam | prāc-ām a-vṛddh-āt phiN bahulam |
| 4.1.161 | VARIANTS | 0.862 | manor jātāv añ-ayatau ṣuk ca | mano-r jāt-au aÑ-yaT-au ṣuK ca |
| 4.1.162 | AGREES | 0.933 | apatyeaṃ pautraprabhṛti gotram | apatyam pautra-prabhṛti gotram |
| 4.1.163 | AGREES | 0.955 | jīvati tu vaṃśye yuvā | jīvat-i tu vaṃśy-e yuvā |
| 4.1.164 | AGREES | 0.950 | bhrātari ca jyāyasi | bhrātar-i ca jyāyas-i |
| 4.1.165 | AGREES | 0.916 | vā anyasmin sapiṇḍe sthaviratare jivati | vā=anya-smin sa-piṇḍ-e sthavira-tare jīvat-i |
| 4.1.166 | AGREES | 0.952 | vṛddhasya ca pūjāyām | vṛddha-sya ca pūjā-yām |
| 4.1.167 | VARIANTS | 0.889 | yūnaś ca kutsāyām | yūn-as=ca kutsā-yām |
| 4.1.168 | AGREES | 0.915 | janapada-śabdāt kṣatriyād añ | jana-pada-śabd-āt kṣatriy-āt=aÑ |
| 4.1.169 | AGREES | 0.980 | sālveya-gāndhāribhyāṃ ca | sālveya-gāndhāri-bhyāṃ ca |
| 4.1.170 | VARIANTS | 0.845 | dvy-añ-magadha-kaliṅg-asūramasād aṇ | dvi=aC-magadha-kaliṛga-sūramas-āt=aṆ |
| 4.1.171 | AGREES | 0.947 | vṛddha-it-kosala-ajādāñ ñyaṅ | vṛddha=iT-kosala=ajād-āt=ÑyaṄ |
| 4.1.172 | VARIANTS | 0.850 | kuru-nādibhyo ṇyaḥ | kuru-n-ādi-bhyaḥ=Ṇya-ḥ |
| 4.1.173 | AGREES | 0.923 | sālvāvayava-pratyagratha-kalakūṭa-aśmakād iñ | sālva=avayava-pratyagratha-kalakūṭa=aśmak-āt=iÑ |
| 4.1.174 | AGREES | 0.917 | te tadrājāḥ | te tad-rāj-āḥ |
| 4.1.175 | VARIANTS | 0.880 | kambojāl luk | kamboj-āt=luK |
| 4.1.176 | AGREES | 0.941 | striyām avanti-kunti-kurubhyaś ca | striy-ām avanti-kunti-kuru-bhyas=ca |
| 4.1.177 | VARIANTS | 0.800 | ataś ca | aT-as=ca |
| 4.1.178 | AGREES | 0.923 | na prācya-bharga-ādi-yaudheya-ādibhyaḥ | na prācya-bharga=ādi-yaudheya-ādi-hyas=a |
| 4.2.1 | VARIANTS | 0.895 | tena raktaṃ rāgāt | t-ena ra-kt-aṃ rāg-āt |
| 4.2.2 | AGREES | 0.955 | lākṣā-rocanā-śakala-kardamāṭ ṭhak | lākṣā-rocanā-(śakala-kardam-)āt ṭhaK |
| 4.2.3 | VARIANTS | 0.880 | nakṣatreṇa yuktaṃ kālaḥ | nakṣatr-eṇa yuk-ta-ḥ kāla-ḥ |
| 4.2.4 | VARIANTS | 0.833 | lub aviśeṣe | luP=a-viśeṣ-e |
| 4.2.5 | AGREES | 0.906 | sañjñāyāṃ śravaṇa-aśvatthābhyām | saṃjñā-yām śravaṇa-aśvatthā-bhyām |
| 4.2.6 | VARIANTS | 0.741 | dvanvāc chaḥ | dvaṃdv-āt=cha-ḥ |
| 4.2.7 | AGREES | 0.917 | dṛṣṭaṃ sāma | dṛṣ-ṭa-ṃ sāma |
| 4.2.8 | AGREES | 0.952 | kaler ḍhak | kale-r ḍhaK |
| 4.2.9 | VARIANTS | 0.850 | vāmadevāḍ ḍyaḍ-ḍyau | vāmadev-āt=ḌyaT=Ḍy-au |
| 4.2.10 | VARIANTS | 0.800 | parivṛto rathaḥ | pari-vṛ-ta-ḥ=ratha-ḥ |
| 4.2.11 | VARIANTS | 0.895 | pāṇḍukambalād iniḥ | pāṇḍu-kambalāt=ini-ḥ |
| 4.2.12 | AGREES | 0.927 | dvaipa-vaiyāghrād añ | dvaipa-vaiyāghr-āt=aÑ |
| 4.2.13 | AGREES | 0.909 | kaumāra-apūrvavacane | kaumār-a=a-pūrva-vacan-e |
| 4.2.14 | AGREES | 0.912 | tatra+uddhṛtam amatrebhyaḥ | ta-tra=ud-dhṛ-ta-m amatre-bhyaḥ |
| 4.2.15 | VARIANTS | 0.852 | sthaṇḍilāc chayitari vrate | sthaṇḍil-āt śayitar-i vrat-e |
| 4.2.16 | VARIANTS | 0.821 | saṃskṛtaṃ bhakṣāḥ | saṃ-s-kṛ-ta-m bhakṣ-āḥ |
| 4.2.17 | VARIANTS | 0.897 | śūla-ukhād yat | śūla=ukh-āt=yaT |
| 4.2.18 | VARIANTS | 0.880 | dadhnaṣ ṭhak | dadhn-aḥ=ṭhaK |
| 4.2.19 | VARIANTS | 0.826 | udaśvito 'nyatarasyām | udaśvit-aḥ=anya-tara-syām |
| 4.2.20 | VARIANTS | 0.870 | kṣīrāḍ ḍhañ | kṣīr-āt=ḍhaÑ |
| 4.2.21 | AGREES | 0.912 | sā 'smin paurṇamāsī iti sañjñāyām | sā=a-smin paurṇamāsī=iti (saṃjñā-yām) |
| 4.2.22 | AGREES | 0.902 | āgrahāyaṇy-aśvatthāṭ ṭhak | āgrahāyaṇī=aśvatth-āt=ṭhaK |
| 4.2.23 | AGREES | 0.956 | vibhāṣā phālgunī-śravaṇā-kārtikī-caitrībhyaḥ | vibhāṣā phālgunī-sravaṇā-kārttikī-caitrī-bhyaḥ |
| 4.2.24 | VARIANTS | 0.867 | sā 'sya devatā | sā=a-sya deva-tā |
| 4.2.25 | AGREES | 0.941 | kasya+it | ka-sya iT |
| 4.2.26 | VARIANTS | 0.870 | śukrād ghan | śukr-āt=ghaN |
| 4.2.27 | AGREES | 0.900 | aponaptr-apāṃnaptṛbhyāṃ ghaḥ | apo-naptṛ=apāṃ-naptṛ-bhyāṃ gha-ḥ |
| 4.2.28 | AGREES | 1.000 | cha ca | cha ca |
| 4.2.29 | VARIANTS | 0.810 | mahendrād ghāṇau ca | mahendr-āt=gha=aṆ-au ca |
| 4.2.30 | VARIANTS | 0.857 | somāṭ ṭyaṇ | som-āt=ṬyaṆ |
| 4.2.31 | VARIANTS | 0.833 | vāyv-ṛtu-pitr-uṣaso yat | vāyu=ṛtu-pitṛ=uṣas-aḥ=yaT |
| 4.2.32 | AGREES | 0.936 | dyāvāpṛthivī-śunāsīra-marutvad-agnīṣoma-vāstoṣpati-gṛhamedhāc cha ca | dyāvā-pṛthivī-śunāsīra-marutvat=agnī-ṣoma-vāstoṣ-pati-gṛha-medh-āt=cha ca |
| 4.2.33 | AGREES | 0.952 | agner ḍhak | agne-r ḍhaK |
| 4.2.34 | VARIANTS | 0.865 | kālebhyo bhavavat | kāle-bhyaḥ=bhava-vat |
| 4.2.35 | AGREES | 0.909 | mahārāja-proṣṭhapadāṭ ṭhañ | mahā-rāja-proṣṭha-pad-āt=ṭhaÑ |
| 4.2.36 | AGREES | 0.985 | pitṛvya-mātula-mātāmaha-pitāmahāḥ | pitṛvya-mātula-mātāmaha-pitāmah-āḥ |
| 4.2.37 | VARIANTS | 0.897 | tasya samūhaḥ | ta-sya sam-ūha-ḥ |
| 4.2.38 | VARIANTS | 0.833 | bhikṣā-ādibhyo 'ṇ | bhikṣā=ādi-bhyaḥ=aṆ |
| 4.2.39 | AGREES | 0.952 | gotra-ukṣa-uṣṭra-urabhra-rāja-rājanya-rājaputra-vatsa-manuṣya-ajād vuñ | gotra=ukṣa(n)=uṣṭra=urabhra-rājan-rājanya-rāja-putra-vatsa-manuṣya=aj-āt=vuÑ |
| 4.2.40 | VARIANTS | 0.897 | kedārād yañ ca | kedār-āt=yaÑ=ca |
| 4.2.41 | AGREES | 0.914 | ṭhañ kavacinaś ca | ṭhaÑ kavacin-as=ca |
| 4.2.42 | AGREES | 0.945 | brāhmaṇa-māṇava-vāḍavād yan | brāhmaṇa-māṇava-vāḍav-āt=yaN |
| 4.2.43 | AGREES | 0.985 | grāma-jana-bandhu-sahāyebhyas tal | grāma-jana-bandhu-sahāye-bhyas=taL |
| 4.2.44 | AGREES | 0.903 | anudāttāder añ | an-udātt-āde-r aÑ |
| 4.2.45 | AGREES | 0.927 | khaṇḍika-ādibhyaś ca | khaṇḍika=ādi-bhyas=ca |
| 4.2.46 | VARIANTS | 0.884 | caraṇebhyo dharmavat | caraṇe-bhyaḥ=dharma-vat |
| 4.2.47 | VARIANTS | 0.885 | acitta-hasti-dhenoṣ ṭhak | a-citta-hasti(n)-dheno-s=ṭhaK |
| 4.2.48 | VARIANTS | 0.895 | keśa-aśvābhyāṃ yañ-chāv anyatarasyām | keśa=aśvā-bhyāṃ yaÑ=ch-au=anya-tara-syām |
| 4.2.49 | VARIANTS | 0.788 | pāśādibhyo yaḥ | pāśa=ādi-bhyaḥ=ya-ḥ |
| 4.2.50 | AGREES | 0.968 | khala-go-rathāt | khala-go-rath-āt |
| 4.2.51 | AGREES | 0.923 | ini-tra-kaṭyacaś ca | ini-tra-kaṭyaC-as=ca |
| 4.2.52 | VARIANTS | 0.800 | viṣayo deśe | viṣaya-ḥ=deś-e |
| 4.2.53 | VARIANTS | 0.842 | rājanyādibhyo vuñ | rājanya=ādi-bhyaḥ=vuÑ |
| 4.2.54 | VARIANTS | 0.848 | bhaurikyādy-aiṣukāryādibhyo vidhalbhaktalau | bhauriki=ādi-aiṣukāri=ādi-bhyaḥ vidhaL=bhaktaL-au |
| 4.2.55 | VARIANTS | 0.864 | so 'sya-ādir iti cchandasaḥ pragātheṣu | sa-ḥ=a-sya=ādi-r iti=chandas-aḥ pragāthe-ṣu |
| 4.2.56 | VARIANTS | 0.879 | saṅgrāme prayojana-yoddhṛbhyaḥ | saṃ-grām-e pra-yoj-ana-yod-dhṛ-bhyaḥ |
| 4.2.57 | VARIANTS | 0.875 | tad asyāṃ praharaṇam iti krīḍāyāṃ ṇaḥ | tad a-syām pra-har-aṇa-m iti krīḍā-yām Ṇa-ḥ |
| 4.2.58 | VARIANTS | 0.807 | ghañaḥ sāsyāṃ kriyeti ñaḥ | GHaÑ-aḥ sā=a-syām kriyā=iti Ña-ḥ |
| 4.2.59 | AGREES | 1.000 | tad adhīte tad veda | tad adhīte tad veda |
| 4.2.60 | VARIANTS | 0.867 | kratu-ukthādi-sūtrāntāṭ ṭhak | kratu=uktha=ādi-sūtra=nt-āt=ṭhaK |
| 4.2.61 | VARIANTS | 0.824 | kramādibhyo vun | krama=ādi-bhyaḥ=vuN |
| 4.2.62 | VARIANTS | 0.811 |  anubrāhmaṇād iniḥ | anu-brāhmaṇ-āt=inī-ḥ |
| 4.2.63 | VARIANTS | 0.878 |  vasantādibhyaṣ ṭhak | vasanta=ādi-bhyaḥ=ṭhaK |
| 4.2.64 | AGREES | 0.909 | proktāl luk | proktāt=luK |
| 4.2.65 | AGREES | 0.905 |  sūtrāc ca ka+upadhāt | sūtr-āt=ca ka=upadh-āt |
| 4.2.66 | AGREES | 0.901 |  chando-brāhamaṇāni ca tad-viṣayāṇi | chandas=brāhmaṇā-n-i ca tad-viṣayā-ṇi |
| 4.2.67 | AGREES | 0.914 | tad asminn asti iti deśe tannāmni | tad a-smin as-ti=iti deś-e tan-nāmn-i |
| 4.2.68 | VARIANTS | 0.875 | tena nirvṛttam | t-ena nir-vṛt-ta-m |
| 4.2.69 | VARIANTS | 0.867 | tasya nivāsaḥ | ta-sya ni-vās-a-ḥ |
| 4.2.70 | VARIANTS | 0.839 | adūrabhavaś ca | a-dūra-bhava-s=ca |
| 4.2.71 | AGREES | 0.909 | or añ | o-r aÑ |
| 4.2.72 | VARIANTS | 0.783 | matoś ca bahv-aj-aṅgāt | matO-s=ca bahu=aC=aṛg-āt |
| 4.2.73 | VARIANTS | 0.882 | bahv-acaḥ kūpeṣu | bahu=aC-aḥ kūpe-ṣu |
| 4.2.74 | AGREES | 0.968 | udak ca vipāśaḥ | udak ca vipāś-aḥ |
| 4.2.75 | VARIANTS | 0.789 | saṅkalādibhyaś ca | saṃ-kala=ādi-bhyas=ca |
| 4.2.76 | AGREES | 0.982 | strīṣu sauvīra-sālva-prākṣu | strīṣu sauvīra-sālva-prāk-ṣu |
| 4.2.77 | VARIANTS | 0.789 | suvāstv-ādibhyo 'ṇ | suvāstu=ādi-bhyaḥ=aṆ |
| 4.2.78 | AGREES | 1.000 | roṇī | roṇī |
| 4.2.79 | VARIANTS | 0.889 | ka-upadhāc ca | kA=upadh-āt=ca |
| 4.2.80 | AGREES | 0.949 | vuñ-chaṇ-ka-ṭhaj-ila-sa-ini-ra-ḍha ṇya-ya-phak-phiñ-iñ-ñya-kak-ṭhako 'rīhaṇa-kṛśāśva-rśya-kumuda-kāśa-tṛṇa-prekṣā-aśma-sakhi-saṅkāśa-bala-pakṣa-karṇa-sutaṅgama-pragadin-varāha-kumuda-ādibhyaḥ | vuÑ-chaṆ-ka-ṭhaC=ila-sa-ini-ra-ḍhaÑ-Ṇya-ya-phaK-phiÑ-iÑ-Ñya-kaK-ṭhaK-aḥ arīhaṇa-kṛśāśva=ṛśya-kumuda-kāśa-tṛṇa-prekṣā-aśma(n)-sakhi-saṃ-kāśa-bala-pakṣa-karṇa-sutaṃ-gama-pragadin-varāha-kumuda=ādi-bhyaḥ |
| 4.2.81 | AGREES | 0.960 | janapade lup | janapad-e luP |
| 4.2.82 | VARIANTS | 0.865 | varaṇa-ādibhyaś ca | varaṇā=ādi-bhyas=ca |
| 4.2.83 | AGREES | 0.923 | śarkarāyā vā | śarkarā-yāḥ=vā |
| 4.2.84 | AGREES | 0.960 | ṭhak-chau ca | ṭhaK-ch-au ca |
| 4.2.85 | VARIANTS | 0.880 | nadyāṃ matup | nady-ām matUP |
| 4.2.86 | VARIANTS | 0.824 | madhvādibhyaś ca | madhu=ādi-bhyas=ca |
| 4.2.87 | AGREES | 0.915 | kumuda-naḍa-vetasebhyo ḍmatup | kumuda-naḍa-vetase-hyaḥ=ḌmatUP |
| 4.2.88 | AGREES | 0.914 | naḍa-śādāḍ ḍvalac | naḍa-śād-āt=ḌvalaC |
| 4.2.89 | AGREES | 0.929 | śikhāyā valac | śikhā-yāḥ=valaC |
| 4.2.90 | VARIANTS | 0.850 | utkarādibhyaś chaḥ | utkara=ādi-bhyas=cha-ḥ |
| 4.2.91 | AGREES | 0.914 | naḍādīnāṃ kuk ca | naḍa=ādī-nāṃ kuK ca |
| 4.2.92 | VARIANTS | 0.889 | śeṣe | śeṣ-e |
| 4.2.93 | AGREES | 0.909 | rāṣṭra-avārapārād gha-khau | rāṣṭra=avāra-pār-āt=gha=kh-au |
| 4.2.94 | CONFLICTS | 0.500 | rāṣṭra-avārapārād gha-khau | grām-āt=ya-khaÑ-au |
| 4.2.95 | VARIANTS | 0.837 | katry-ādibhyo ḍhakañ | kattri=ādi-bhyas=ḍhakaÑ |
| 4.2.96 | VARIANTS | 0.843 | kula-kukṣi-grīvābhyaḥ śva-asy-alaṅkāreṣu | kula-kukṣi-grīvā-hyas=śva(n)=asi= alaṃ-āre-ṣu |
| 4.2.97 | VARIANTS | 0.833 | nady-ādibhyo ḍhak | nadī=ādi-bhyas=ḍhaK |
| 4.2.98 | AGREES | 0.982 | dakṣiṇā-paścāt-purasas tyak | dakṣiṇā-paścāt-puras-as=tyaK |
| 4.2.99 | VARIANTS | 0.897 | kāpiśyāḥ ṣphak | kāpiśy-ās=ṢphaK |
| 4.2.100 | VARIANTS | 0.864 | raṅkor amanuṣye 'ṇ ca | ranko-r a-manuṣye=aṆ ca |
| 4.2.101 | VARIANTS | 0.825 | dyu-prāg-apāg-udak-pratīco yat | dyu-prāc=apāc=u dac-pratīc-aḥ=yaT |
| 4.2.102 | VARIANTS | 0.857 | kanthāyāṣṭhak | kanthā-yās=ṭhaK |
| 4.2.103 | AGREES | 0.952 | varṇau vuk | varṇ-au vuK |
| 4.2.104 | AGREES | 0.960 | avyayāt tyap | avyay-āt tyaP |
| 4.2.105 | VARIANTS | 0.762 | aiṣameo-hyaḥ-śvaso 'nyatarasyām | aiṣamas=hyas=śvas-aḥ=nya-ara-yām |
| 4.2.106 | AGREES | 0.933 | tīra-rūpya-uttarapadād añ-ñau | tīra-rūpya=uttarapad-āt aÑ-Ñ-au |
| 4.2.107 | VARIANTS | 0.794 | dik-pūrvapadād asañjñāyāṃ ñaḥ | dik-pūrva-pad-āt=a-saṃjñā-yam Ña-ḥ |
| 4.2.108 | VARIANTS | 0.769 | madrebhyo 'ñ | madre-bhyaḥ=aÑ |
| 4.2.109 | VARIANTS | 0.763 | udīcyagrāmāc ca bahvaco 'ntodāttāt | udīcya-grām-āt=ca bahu=aC-aḥ=anta=udātt-āt |
| 4.2.110 | VARIANTS | 0.894 | prastha-uttarapada-paladyādi-ka-upadhādaṇ | prastha=uttara-pada=paladī=ādi-ka=padh-āt=aṆ |
| 4.2.111 | VARIANTS | 0.878 | kaṇva-ādibhyo gotre | kaṇva=ādi-bhyaḥ=gotr-e |
| 4.2.112 | VARIANTS | 0.800 | iñaś ca | iÑ-as=ca |
| 4.2.113 | VARIANTS | 0.897 | na dvy-acaḥ prācya-bharatesu | na dvi=aC-aḥ prācya-bharate-ṣu |
| 4.2.114 | VARIANTS | 0.846 | vṛddhāc chaḥ | vṛddh-āt=cha-ḥ |
| 4.2.115 | AGREES | 0.905 | bhavataṣ ṭhak-chasau | bhavat-as=ṭhaK=chaS-au |
| 4.2.116 | VARIANTS | 0.863 | kāśyādibhyaṣ ṭhañ-ñiṭhau | kāśi=ādi-bhyas=ṭhaÑ-Ñiṭh-au |
| 4.2.117 | AGREES | 0.900 | vāhīkagrāmebhyaś ca | vāhīka-grāme-bhyas=ca |
| 4.2.118 | AGREES | 0.971 | vibhāṣā+uśīnareṣu | vibhāṣā=uśīnare-ṣu |
| 4.2.119 | AGREES | 0.923 | or deśe ṭhañ | o-r deś-e ṭhaÑ |
| 4.2.120 | VARIANTS | 0.867 | vṛddhat prācām | vṛddh-āt prāc-ām |
| 4.2.121 | VARIANTS | 0.844 | dhanva-ya-upadhād vuñ | dhanva(n)=ya=upadh-at=vuÑ |
| 4.2.122 | VARIANTS | 0.880 | prastha-pura-vahāntāc ca | prastha-pura-vaha=nt-āt=ca |
| 4.2.123 | AGREES | 0.909 | ra-upadha-itoḥ prācām | ra=upadha=īT-oḥ prāc-ām |
| 4.2.124 | AGREES | 0.917 | janapada-tadavadhyoś ca | janapada-tad-avadhy-os=ca |
| 4.2.125 | AGREES | 0.909 | avṛddhād api bahuvacana-viṣayāt | a-vṛddh-āt=api bahu-vacana-viṣay-āt |
| 4.2.126 | AGREES | 0.919 | kaccha-agni-vaktra-garta-uttarapadāt | kaccha=agni-vaktra-vartta=ttara-pad-āt |
| 4.2.127 | VARIANTS | 0.848 | dhūmādibhyaś ca | dhūma=ādi-bhyas=ca |
| 4.2.128 | AGREES | 0.964 | nagarāt kutsana-prāvīṇyayoḥ | nagar-āt kutsana-prāvīṇyay-oḥ |
| 4.2.129 | VARIANTS | 0.812 | araṇyān manusye | araṇy-āt=manuṣy-e |
| 4.2.130 | AGREES | 0.982 | vibhāṣā kuru-yugandharābhyām | vibhāṣā kuru-yugandharā-bhyām |
| 4.2.131 | AGREES | 0.970 | madra-vṛjyoḥ kan | madra=vṛjy-oḥ kaN |
| 4.2.132 | VARIANTS | 0.720 | kopadhād aṇ | ka=upadh-āt=aṆ |
| 4.2.133 | AGREES | 0.919 | kaccha-ādibhyaś ca | kaccha=ādi-bhyas=ca |
| 4.2.134 | AGREES | 0.913 | manusya-tatsthayor vuñ | manuṣya-tat-sthay-or vuÑ |
| 4.2.135 | AGREES | 0.909 | apadātau sālvāt | a-padāt-au sālv-āt |
| 4.2.136 | VARIANTS | 0.828 | go-yavagvoś ca | go-yavāgv-os=ca |
| 4.2.137 | VARIANTS | 0.894 | garta-uttarapadāc chaḥ | garta=uttara-pad-āt=cha-ḥ |
| 4.2.138 | AGREES | 0.909 | gaha-ādibhyaś ca | gaha=ādi-bhyas=ca |
| 4.2.139 | VARIANTS | 0.875 | prācāṃ kaṭādeḥ | prāc-āṃ kaṭa=āde-ḥ |
| 4.2.140 | AGREES | 0.960 | rājñaḥ ka ca | rājñ-aḥ ka ca |
| 4.2.141 | VARIANTS | 0.882 | vṛddhād aka-ika-anta-kha-upadhāt | vṛddh-āt=aka=ika=ant -āt kha=upadh-āt |
| 4.2.142 | AGREES | 0.978 | kanthā-palada-nagara-grāma-hrada-uttarapadāt | kanthā-palada-nagara-grāma-hrada=uttara-pad-āt |
| 4.2.143 | VARIANTS | 0.870 | parvatāc ca | parvat-āt=ca |
| 4.2.144 | VARIANTS | 0.882 | vibhāṣā 'manuṣye | vibhāṣā=a-manuṣy-e |
| 4.2.145 | AGREES | 0.920 | kṛkaṇa-parṇād bharadvāje | kṛkaṇa--parṇ-āt bharadvāj-e |
| 4.3.1 | AGREES | 0.932 | yuṣmad-asmador anyatarasyāṃ khañ ca | yuṣmad-asmad-or anya-tara-syām khaÑ=ca |
| 4.3.2 | AGREES | 0.935 | tasminn aṇi ca yuṣmāka-asmākau | ta-smin=aṆ-i ca yuṣmāka=asmāk=au |
| 4.3.3 | VARIANTS | 0.863 | tavaka-mamakāv ekavacane | tavaka-mamak-au=eka-vacan-e |
| 4.3.4 | VARIANTS | 0.857 | ardhād yat | ardh-āt=yaT |
| 4.3.5 | AGREES | 0.957 | para-avara-adhama-uttama-pūrvāc ca | para=avara=adhama=uttama-pūrv-āt=ca |
| 4.3.6 | AGREES | 0.913 | dik-pūrvapadāṭ ṭhañ ca | dik-pūrva-pad-āt=ṭhaÑ=ca |
| 4.3.7 | AGREES | 0.912 | grāma-janapada+ekadeśād añ-ṭhañau | grāma-janapada=eka-deś-āt=aÑ-ṭhaÑ-u |
| 4.3.8 | VARIANTS | 0.750 | madhyānamaḥ | madhy-āt ma-ḥ |
| 4.3.9 | VARIANTS | 0.889 | a sāmpratike | a sām-prati-k-e |
| 4.3.10 | VARIANTS | 0.851 | dvīpād anusamudraṃ yañ | dvīp-āt=anu-samudr-am yaÑ |
| 4.3.11 | VARIANTS | 0.857 | kālāṭ ṭhañ | kāl-āt=ṭhaÑ |
| 4.3.12 | AGREES | 0.938 | śrāddhe śaradaḥ | śrāddh-e śarad-aḥ |
| 4.3.13 | AGREES | 0.977 | vibhāṣā roga-ātapayoḥ | vibhāṣā roga-ātapay-oḥ |
| 4.3.14 | AGREES | 0.976 | niśā-pradoṣābhyāṃ ca | niśā-pradoṣā-bhyāṃ ca |
| 4.3.15 | AGREES | 0.963 | śvasas tuṭ ca | śvas-as tuṬ ca |
| 4.3.16 | VARIANTS | 0.789 | sandhivela-ādy-ṛtu-nakṣatrebhyo 'ṇ | saṃ-dhi+velā=ādi=ṛtu-nakṣatre-hyaḥ=aṆ |
| 4.3.17 | VARIANTS | 0.897 | prāvṛṣa eṇyaḥ | prāvṛṣ-aḥ=eṇya-ḥ |
| 4.3.18 | VARIANTS | 0.867 | varṣābhyaṣṭhak | varṣā-bhyas=ṭhaK |
| 4.3.19 | AGREES | 0.963 | chandasi ṭhañ | chandas-i ṭhaÑ |
| 4.3.20 | VARIANTS | 0.870 | vasantāc ca | vasant-āt=ca |
| 4.3.21 | VARIANTS | 0.870 | hemantāc ca | hemant-āt=ca |
| 4.3.22 | AGREES | 0.906 | sarvatra aṇ ca talopaś ca | sarva-tra=aṆ ca ta-lopa-s=ca |
| 4.3.23 | VARIANTS | 0.883 | sāyaṃ-ciraṃ-prāhṇe-prage 'vyayebhyaṣ ṭyu-ṭyulau tuṭ ca | sāyam=ciram=prāhṇ-e=prage=avyaye-hyaḥ Ṭyu-ṬyuL-au tu-Ṭ ca |
| 4.3.24 | AGREES | 0.984 | vibhāṣā pūrvāhṇa-aparāhṇābhyām | vibhāṣā pūrvāhṇa=aparāhṇā-bhyām |
| 4.3.25 | VARIANTS | 0.880 | tatra jātaḥ | ta-tra jā-ta-ḥ |
| 4.3.26 | VARIANTS | 0.846 | prāvṛṣaṣṭhap | prāvṛṣ-as=ṭhaP |
| 4.3.27 | VARIANTS | 0.818 | sañjñāyāṃ śarado vuñ | saṃjñā-y-āṃ śarad-aḥ=vuÑ |
| 4.3.28 | AGREES | 0.970 | pūrvāhṇa-aparāhṇa-ārdrā-mūla-pradoṣa-avaskarād vun | pūrvāhṇa=aparāhṇa=ārdrā=mūla-pradoṣa=avaskar-āt=vuN |
| 4.3.29 | AGREES | 0.970 | pathaḥ pantha ca | path-aḥ pantha ca |
| 4.3.30 | VARIANTS | 0.897 | amāvāsyāyā vā | amāvāsyā-y-āḥ=vā |
| 4.3.31 | AGREES | 1.000 | a ca | a ca |
| 4.3.32 | VARIANTS | 0.894 | sindhv-apakarābhyāṃ kan | sindhu=apakarā-bhyām kaN |
| 4.3.33 | AGREES | 0.900 | aṇañau ca | aṆ=aÑ-au ca |
| 4.3.34 | AGREES | 0.970 | śraviṣṭhā-phalguny-anurādhā-svāti-tiṣya-punarvasu-hasta-viśākhā-aṣāḍhā-bahulāl luk | śraviṣṭhā-phalgunī=anurādhā=svāti-tiṣya-punarvasu-hasta-viśākhā=aṣāḍhā-bahul-āt=luK |
| 4.3.35 | VARIANTS | 0.848 | sthānānata-gośāla-kharaśālāc ca | sthāna=anta-go-śāla-khara-śāl-āt=ca |
| 4.3.36 | VARIANTS | 0.824 | vatsaśālā-abhijid-aśvayuk-chatabhiṣajo vā | vatsa-śālā=abhijit=aśva-yuj=śata-hiṣaj-aḥ=vā |
| 4.3.37 | AGREES | 0.905 | nakṣatrebhyo bahulam | nakṣatre-bhyaḥ=bahulam |
| 4.3.38 | AGREES | 0.926 | kṛta-labdha-krīta-kuśalāḥ | kṛ-ta-lab-dha-krī-ta-kuśal-āḥ |
| 4.3.39 | AGREES | 0.917 | prāyabhavaḥ | prāya-bhava-ḥ |
| 4.3.40 | AGREES | 0.906 | upajānu-upakarṇa-upanīveṣ ṭhak | upa-jānu=upa-karṇa=upa-nīve-s=ṭhaK |
| 4.3.41 | VARIANTS | 0.737 | sambhūte | saṃ-bhū-t-e |
| 4.3.42 | VARIANTS | 0.857 | kośāḍ ḍhañ | koś-āt=ḍhaÑ |
| 4.3.43 | AGREES | 0.939 | kālāt sādhu-puṣpyat-pacyamāneṣu | kāl-āt sādhu-puṣpyat-pacya-m-āne-ṣu |
| 4.3.44 | VARIANTS | 0.875 | upte ca | up-t-e ca |
| 4.3.45 | VARIANTS | 0.897 | āśvayujyā vuñ | āśva-yujy-āḥ=vuÑ |
| 4.3.46 | VARIANTS | 0.897 | grīṣma-vasantād anyatrasyām | grīṣma-vasant-āt=anya-tara-syām |
| 4.3.47 | AGREES | 0.900 | deyam ṛṇe | deya-m ṛṇ-e |
| 4.3.48 | VARIANTS | 0.852 | kalāpy-aśvattha-yavabusād vun | kalāpi(n)=aśvattha=yava -bus-āt=uN |
| 4.3.49 | AGREES | 0.909 | grīṣma-avarasamād vuñ | grīṣma=avara-sam-āt=vuÑ |
| 4.3.50 | AGREES | 0.943 | saṃvatsara-āgrahāyaṇībhyāṃ ṭhañ ca | saṃvatsara=āgra-hāyaṇī-bhyām ṭhaÑ=ca |
| 4.3.51 | VARIANTS | 0.857 | vyāharati mṛgaḥ | vy-ā-har-a-ti mṛga-ḥ |
| 4.3.52 | AGREES | 0.938 | tad asya soḍham | tad a-sya soḍha-m |
| 4.3.53 | AGREES | 0.923 | tatra bhavaḥ | ta-tra bhava-ḥ |
| 4.3.54 | VARIANTS | 0.812 | dig-ādibhyo yat | diś=ādi-bhyaḥ=yaT |
| 4.3.55 | AGREES | 0.919 | śarīra-avayavāc ca | śarīra=avayav-āt=ca |
| 4.3.56 | AGREES | 0.947 | dṛti-kukṣi-kalaśi-vasty-asty-aher ḍhañ | dṛti-kukṣi-kalaśi-vasti=asti=aher ḍhaÑ |
| 4.3.57 | VARIANTS | 0.812 | grīvābhyo 'ṇ ca | grīvā-bhyaḥ=aṆ ca |
| 4.3.58 | VARIANTS | 0.867 | gambhīrāñ ñyaḥ | gambhīr-āt=Ñya-ḥ |
| 4.3.59 | VARIANTS | 0.875 | avyayībhāvāc ca | avyayī-bhāv=āt=ca |
| 4.3.60 | AGREES | 0.909 | antaḥ-pūrvapadāṭ ṭhañ | antaḥ-pūrva-pad-āt=ṭhaÑ |
| 4.3.61 | AGREES | 0.913 | grāmāt pary-anu-pūrvāt | grām-āt pari=anu-pūrv-āt |
| 4.3.62 | VARIANTS | 0.851 | jihvāmūla-aṅguleś chaḥ | jihvā-mūla=aṛgule-s=cha-ḥ |
| 4.3.63 | VARIANTS | 0.741 | vargāntāc ca | varga=ant-āt=ca |
| 4.3.64 | VARIANTS | 0.867 | aśabde yat-khāv anyatarasyām | a-śabd-e yaT-kh-au=nya-tara-syām |
| 4.3.65 | AGREES | 0.909 | karṇa-lalāṭāt kan alaṅkāre | karṇa-lalāṭ-āt kaN alaṃ-kār-e |
| 4.3.66 | VARIANTS | 0.854 | tasya vyākhyāna iti ca vyākhyātavyanāmnaḥ | ta-sya vy-ā-khyān-e=iti ca vy-ā-khyā-avya-āmn-aḥ |
| 4.3.67 | VARIANTS | 0.667 | bahvaco 'ntodāttāṭa ṭhañ | bahu=aC=aḥ=anta=udā tt-āt=ṭhaÑ |
| 4.3.68 | AGREES | 0.923 | kratu-yajñebhyaś ca | kratu-yajñe-bhyas=ca |
| 4.3.69 | VARIANTS | 0.821 | adhyāyeṣv eva rṣeḥ | adhy-āye-ṣu=eva=ṛṣe-ḥ |
| 4.3.70 | AGREES | 0.941 | paurāḍāśa-puroḍāśāt ṣṭhan | pauroḍāśa-puroḍāś-āt=ṢṭhaN |
| 4.3.71 | VARIANTS | 0.778 | chandaso yadaṇau | chandas-aḥ=yaT=aṆ-au |
| 4.3.72 | VARIANTS | 0.889 | dvyaj-ṛd-brāhmaṇa-rk-prathama-adhvara-puraścaraṇa-nāmākhyātāṭ ṭhak | dvy-aC=ṛT=brāhmaṇa=ṛc-prathama=adhvara-puraṣ-caraṇa-nāmākhyāt-āt ṭhaK |
| 4.3.73 | AGREES | 0.950 | aṇ ṛgayana-ādibhyaḥ | aṆ ṛg-ayana=ādi-bhyaḥ |
| 4.3.74 | CONFLICTS | 0.444 | tata āgataḥ | ta-taḥ=ā-ga-ta-ḥ |
| 4.3.75 | AGREES | 0.900 | ṭhag āyasthānebhyaḥ | ṭhaK=āya-sthāne-bhyaḥ |
| 4.3.76 | VARIANTS | 0.778 | śuṇḍikādibhyo 'ṇ | śuṇḍika=ādi-bhyaḥ=aṆ |
| 4.3.77 | VARIANTS | 0.881 | vidyā-yoni-sambandhebhyo vuñ | vidyā-yoni-saṃ-bandhe-bhyaḥ=vuÑ |
| 4.3.78 | VARIANTS | 0.842 | ṛtaṣ-ṭhañ | ṛT=as=ṭhaÑ |
| 4.3.79 | AGREES | 0.917 | pitur yac ca | pitur yaT=ca |
| 4.3.80 | VARIANTS | 0.800 | gotrād aṅkavat | gotr-āt=aṛka-vat |
| 4.3.81 | VARIANTS | 0.857 | hetu-manuṣyebhyo 'nyatarasyāṃ rūpyaḥ | hetu-manuṣye-bhyaḥ=anya-tara-syām rūpya-ḥ |
| 4.3.82 | AGREES | 1.000 | mayaṭ ca | mayaṬ=ca |
| 4.3.83 | VARIANTS | 0.870 | prabhavati | pra-bhav-a-ti |
| 4.3.84 | VARIANTS | 0.846 | vidūrāñ ñyaḥ | vidūr-āt=Ñya-ḥ |
| 4.3.85 | AGREES | 0.912 | tad gacchati pathi-dūtayoḥ | tad gacch-a-ti pathi(n)-dūtay-oḥ |
| 4.3.86 | VARIANTS | 0.894 | abhiniṣkrāmati dvāram | abhi-niṣ-krām-a-ti dvār-am |
| 4.3.87 | VARIANTS | 0.880 | adhikṛtya kṛte granthe | adhi-kṛ-t-ya kṛ-t-e granth-e |
| 4.3.88 | AGREES | 0.920 | śiśukranda-yamasabha-dvandva-indrajanana-ādibhyaś chaḥ | śiśu-kranda-yama-sabha-dvaṃdva=indra-janana=ādi-bhyas=cha-ḥ |
| 4.3.89 | VARIANTS | 0.743 | so 'sya nivāsaḥ | sa-ḥ=a-sya ni-vāsa-ḥ |
| 4.3.90 | VARIANTS | 0.846 | abhijanaś ca | abhi-jana-s=ca |
| 4.3.91 | AGREES | 0.900 | āyudhajīvibhyaś chaḥ parvate | āyudha-jīvi-bhyas=cha-ḥ parvat-e |
| 4.3.92 | VARIANTS | 0.837 | śaṇdika-ādibhyo ñyaḥ | śaṇḍika=ādi-bhyaḥ=Ñya-ḥ |
| 4.3.93 | VARIANTS | 0.848 | sindhu-takṣaśilā-ādibhyo 'ṇ-añau | sindhu-takṣa-śilā=ādi-hyaḥ=aṆ=aÑ-u |
| 4.3.94 | AGREES | 0.943 | tūdī-śalātura-varmatī-kūcavārāḍ ṭhak-chaṇ-ḍhañ-yakaḥ | tūdī-śalātura-varmatī-kūcavār-āt ḍhaK-chaṆ-ḍhaÑ-yaK-aḥ |
| 4.3.95 | VARIANTS | 0.875 | bhaktiḥ | bhak-ti-ḥ |
| 4.3.96 | VARIANTS | 0.846 | acittād adeśa-kālāṭ ṭhak | a-citt-āt a-deśa-kāl-āt=ṭhaK |
| 4.3.97 | VARIANTS | 0.897 | mahārājāṭ ṭhañ | mahārāj-āt=ṭhaÑ |
| 4.3.98 | AGREES | 0.939 | vāsudeva-arjunābhyāṃ vun | vāsudeva= arjunā-bhyām vuN |
| 4.3.99 | VARIANTS | 0.889 | gotra-kṣatriya-ākhyebhyo bahulaṃ vuñ | gotra-kṣatriya=ākhye-hyaḥ=ahulam vuÑ |
| 4.3.100 | AGREES | 0.917 | janapadināṃ janapadavat sarvaṃ janapadena samānaśabdānāṃ bahuvacane | jana-padin-āṃ jana-pada-vat sarvaṃ jana-pad-ena samāna-śabdā-nām bahu-vacan-e |
| 4.3.101 | AGREES | 0.923 | tena proktam | t-ena prokta-m |
| 4.3.102 | AGREES | 0.935 | tittiri-varatantu-khaṇḍika-ukhāc chaṇ | tittiri-vara-tantu-khaṇḍika=ukh-āt=cha-Ṇ |
| 4.3.103 | AGREES | 0.932 | kāśyapa-kauśikābhyām ṛṣibhyāṃ ṇiniḥ | kāśyapa-kauśikā-bhyām ṛṣi-bhyām Ṇini-ḥ |
| 4.3.104 | VARIANTS | 0.849 | kalāpi-vaiśampāyana-antevāsibhyaś ca | kalāpi(n)=vaisampāyana=nte-āsi-hyas=ca |
| 4.3.105 | AGREES | 0.954 | purāṇa-prokteṣu brāhmaṇa-kalpeṣu | purāṇa-pro-kteṣu brāhmaṇa-alpe-ṣu |
| 4.3.106 | AGREES | 0.923 | śaunaka-ādibhyaś chandasi | śaunaka=ādi-bhyas=chandas-i |
| 4.3.107 | AGREES | 0.914 | kaṭha-carakāl luk | kaṭha-carak-āt=luK |
| 4.3.108 | VARIANTS | 0.750 | kalāpino 'ṇ | kalāpin-aḥ=aṆ |
| 4.3.109 | VARIANTS | 0.882 | chagalino ḍhinuk | chagalin-aḥ=ḍhinuK |
| 4.3.110 | AGREES | 0.941 | pārāśarya-śilālibhyāṃ bhikṣu-naṭasūtrayoḥ | pārāśarya-śilāli-bhyām bhikṣu-naṭa-sūtray-oḥ |
| 4.3.111 | AGREES | 0.913 | karmanda-kṛśāśvād iniḥ | karmanda-kṛśāśv-āt=ini-ḥ |
| 4.3.112 | AGREES | 0.917 | tena+ekadik | t-ena=eka-dik |
| 4.3.113 | VARIANTS | 0.824 | tasiś ca | tasi-s=ca |
| 4.3.114 | VARIANTS | 0.769 | uraso yac ca | uras-aḥ=yaT=ca |
| 4.3.115 | VARIANTS | 0.842 | upajñāte | upa-jñā-t-e |
| 4.3.116 | VARIANTS | 0.889 | kṛte granthe | kṛ-t-e granth-e |
| 4.3.117 | VARIANTS | 0.700 | sañjñāyām | saṃjña-y-ām |
| 4.3.118 | VARIANTS | 0.895 | kulāla-ādibhyo vuñ | kulāla=ādi-bhyaḥ=vuÑ |
| 4.3.119 | AGREES | 0.955 | kṣudrā-bhramara-vaṭara-pādapād añ | kṣudrā-bhramara-vaṭara-pādap-āt=aÑ |
| 4.3.120 | AGREES | 0.952 | tasya+idam | ta-sya=idam |
| 4.3.121 | VARIANTS | 0.800 | rathādyat | rath-āt=yaT |
| 4.3.122 | VARIANTS | 0.839 | patrapūrvā dañ | pattra-pūrv-āt=aÑ |
| 4.3.123 | AGREES | 0.929 | patra-adhvaryu-pariṣadaś ca | pattra=adhvaryu-pariṣad-as=ca |
| 4.3.124 | AGREES | 0.903 | hala-sīrāṭ ṭhak | hala-sīr-āt=ṭhaK |
| 4.3.125 | AGREES | 0.909 | dvandvād vun vaira-maithunikayoḥ | dvaṃdv-āt=vuN vaira-maithunikay-oḥ |
| 4.3.126 | AGREES | 0.914 | gotra-caraṇād vuñ | gotra-caraṇ-āt=vuÑ |
| 4.3.127 | VARIANTS | 0.892 | saṅgha-aṅka-lakṣaṇeṣv añ-yañ-iñām aṇ | saṃgha=aṛka-lakṣaṇe-ṣu=aÑ-yaÑ-iÑ-ām aṆ |
| 4.3.128 | VARIANTS | 0.857 | śākalād vā | śākal-āt=vā |
| 4.3.129 | AGREES | 0.945 | chandoga-aukthika-yājñika-bahvṛca-naṭāj ñyaḥ | chandoga=aukthika-yājñika-bahv-ṛca-naṭ-āt=Ñya-ḥ |
| 4.3.130 | AGREES | 0.943 | na daṇḍamāṇava-antevāsiṣu | na daṇḍa-māṇava=ante-vāsi-ṣu |
| 4.3.131 | AGREES | 0.917 | raivatika-ādibhyaś chaḥ | raivatika=ādi-bhyas=cha-ḥ |
| 4.3.132 | VARIANTS | 0.840 | kaupiñjala-hāsitapadādaṇ | kaupiñjala-hāsti-pad-āt=aṆ |
| 4.3.133 | AGREES | 0.945 | ātharvaṇikasya+ika-lopaś ca | ātharvaṇika-sya=ika-lopas=ca |
| 4.3.134 | VARIANTS | 0.867 | tasya vikāraḥ | ta-sya vi-kār-a-ḥ |
| 4.3.135 | MISSING | - | avayave ca prāṇy-oṣadhi-vṛkṣebhyaḥ | - |
| 4.3.136 | VARIANTS | 0.800 | bilva-ādibhyo 'ṇ | bilva=ādi=bhyyaḥ=aṆ |
| 4.3.137 | VARIANTS | 0.846 | ka-upādhāc ca | ka=upadhāt=ca |
| 4.3.138 | AGREES | 0.944 | trapu-jatunoḥ ṣuk | trapu-jatu-n-oḥ ṣuK |
| 4.3.139 | VARIANTS | 0.800 | orañ | o-r aÑ |
| 4.3.140 | AGREES | 0.909 | anudātta-ādeś ca | an-udātta=ādes=ca |
| 4.3.141 | VARIANTS | 0.889 | palāśa-ādibhyo vā | palāśa=ādi-bhyaḥ=vā |
| 4.3.142 | VARIANTS | 0.833 | śamyāṣ ṭlañ | śamy-ā-s=ṬlaÑ |
| 4.3.143 | AGREES | 0.918 | mayaḍ vaā+etayor bhāṣāyām abhakṣya ācchādanayoḥ | mayaṬ=vā=etay-or bhāṣā-y-ām a-bhakṣya=ācchādanay-oḥ |
| 4.3.144 | AGREES | 0.945 | nityaṃ vṛddha-śara-ādibhyaḥ | nityam vṛddha-śara=ādi-bhyaḥ |
| 4.3.145 | VARIANTS | 0.786 | goś ca purīṣe | go-s=ca pūrīṣ-e |
| 4.3.146 | VARIANTS | 0.842 | piṣṭāc ca | piṣṭ-āt=ca |
| 4.3.147 | VARIANTS | 0.857 | sañjñāyāṃ kan | saṃjñā-y-āṃ kaN |
| 4.3.148 | AGREES | 0.938 | vrīheḥ puroḍāśe | vrīhe-ḥ puroḍāś-e |
| 4.3.149 | VARIANTS | 0.778 | asañjñāyāṃ tila-yavābhyām | a-saṃjña-y-ām tila-yavā-bhyām |
| 4.3.150 | VARIANTS | 0.857 | dvyacaś chandasi | dvy-aC-as=chandas-i |
| 4.3.151 | VARIANTS | 0.898 | na+uttvad-vardhra-bilvāt | na=uT-vat=vardhra-bilv-āt |
| 4.3.152 | VARIANTS | 0.812 | tāla-ādibhyo 'ṇ | tāla=ādi-bhyaḥ=aṆ |
| 4.3.153 | AGREES | 0.917 | jātarūpebhyaḥ parimāṇe | jāta-rūpe-bhyaḥ pari-māṇ-e |
| 4.3.154 | MISSING | - | prāṇi-rajata-ādibhyo 'ñ | - |
| 4.3.155 | VARIANTS | 0.870 | ñitaś ca tatpratyayāt | Ñ-IT-as=ca tat-pratyay-āt |
| 4.3.156 | VARIANTS | 0.895 | krītavat praimāṇāt | krīta-vat parimāṇ-āt |
| 4.3.157 | VARIANTS | 0.857 | uṣṭrād vuñ | uṣṭr-āt=vuÑ |
| 4.3.158 | AGREES | 0.966 | umā-ūrṇayor vā | umā=ūrṇay-or vā |
| 4.3.159 | AGREES | 0.900 | eṇyā ḍhañ | eṇy-āḥ=ḍhaÑ |
| 4.3.160 | AGREES | 0.929 | gopayasor yat | go-payas-or yaT |
| 4.3.161 | VARIANTS | 0.800 | droś ca | dro-s=ca |
| 4.3.162 | AGREES | 0.909 | māne vayaḥ | mān-e vaya-ḥ |
| 4.3.163 | AGREES | 0.947 | phale luk | phal-e luK |
| 4.3.164 | VARIANTS | 0.865 | plakṣa-ādi-bhyo 'ṇ | plakṣa=ādi-bhyaḥ=aṆ |
| 4.3.165 | AGREES | 0.900 | jambvā vā | jambv-āḥ=vā |
| 4.3.166 | AGREES | 1.000 | lup ca | luP ca |
| 4.3.167 | VARIANTS | 0.878 | harītaky-ādibhya śca | harītakī=ādi-bhyas=ca |
| 4.3.168 | AGREES | 0.973 | kaṃsīya-paraśavyayor yañ-añau luk ca | kaṃsīya-paraśavyay-or yaÑ=aÑ=au luK ca |
| 4.4.1 | VARIANTS | 0.857 | prāg vahateṣ ṭhak | prāk=vahate-s=ṭhaK |
| 4.4.2 | VARIANTS | 0.880 | tena dīvyati khanati jayati jitam | t-ena dīv-ya-ti khan-a-ti jay-a-ti ji-ta-m |
| 4.4.3 | VARIANTS | 0.818 | saṃskṛtam | saṃ-s-kṛ-ta-m |
| 4.4.4 | AGREES | 0.933 | kulattha-ka-upadhād aṇ | kulattha-ka=upadh-āt=aṆ |
| 4.4.5 | VARIANTS | 0.857 | tarati | tar-a-ti |
| 4.4.6 | VARIANTS | 0.867 | gopucchāṭ ṭhañ | go-pucch-āt=ṭhaÑ |
| 4.4.7 | VARIANTS | 0.882 | nau-dvyacaṣ ṭhan | nau-dvy-aC-as=ṭhaN |
| 4.4.8 | VARIANTS | 0.714 | parati | car-a-ti |
| 4.4.9 | AGREES | 0.929 | ākarṣāt ṣṭhal | ā-karṣ-āt=ṢṭhaL |
| 4.4.10 | AGREES | 0.927 | parpa-ādibhyaḥ ṣṭhan | parpa=ādi-bhyas=ṢṭhaN |
| 4.4.11 | VARIANTS | 0.848 | śvagaṇāṭ ṭhañca | śva-gaṇ-āt=ṭhaÑ=ca |
| 4.4.12 | VARIANTS | 0.870 | vetana-ādibhyo jīvati | vetana=ādi-bhyaḥ=jīv-a-ti |
| 4.4.13 | AGREES | 0.941 | vasna-kraya-vikrayāṭ ṭhan | vasna-kraya-vikray-āt=ṭhaN |
| 4.4.14 | VARIANTS | 0.800 | āyudhac cha ca | ā-yudh-āt=cha ca |
| 4.4.15 | VARIANTS | 0.840 | haraty utsaṅga-ādibhyaḥ | har-a-ti=ut-saṛga=ādi-bhyaḥ |
| 4.4.16 | VARIANTS | 0.884 | bhastrādibhyaḥ ṣṭhan | bhastrā=ādi-bhyas=ṢṭhaN |
| 4.4.17 | AGREES | 0.980 | vibhāṣā vivadha-vīvadhāt | vibhāṣā vivadha-vīvadh-āt |
| 4.4.18 | VARIANTS | 0.867 | aṇ kuṭilikāyāḥ | aṆ kūṭilikā-y-āḥ |
| 4.4.19 | VARIANTS | 0.881 | nirvṛtte 'kṣadyūta-ādibhyaḥ | nir-vṛt-t-e=akṣa-dyūta=ādi-bhyaḥ |
| 4.4.20 | VARIANTS | 0.812 | trermam nityam | Ktre-r maP=nitya-m |
| 4.4.21 | AGREES | 0.938 | apamitya-yācitābhyāṃ kak kanau | apa-mi-t-ya-yācitā-bhyāṃ kaK= kaNau |
| 4.4.22 | VARIANTS | 0.842 | saṃsṛṣṭe | saṃ-sṛṣ-ṭ-e |
| 4.4.23 | VARIANTS | 0.783 | cūrṇādiniḥ | cūrṇ-āt=ini-ḥ |
| 4.4.24 | VARIANTS | 0.870 | lavaṇāl luk | lavaṇ-āt=luK |
| 4.4.25 | VARIANTS | 0.842 | mudgād aṇ | mudg-āt=aṆ |
| 4.4.26 | VARIANTS | 0.884 | vyañjanair upasikte | vy-añjan-air upa-sik-t-e |
| 4.4.27 | VARIANTS | 0.792 | ojaḥsaho 'mbhasā vartate | ojas=sahas=ambhas-ā vart-a-te |
| 4.4.28 | MISSING | - | tat praty-anu-pūrvam īpa-loma-kūlam | - |
| 4.4.29 | AGREES | 0.929 | parimukhaṃ ca | pari-mukha-ṃ=ca |
| 4.4.30 | AGREES | 0.905 | prayacchati garhyam | pra-yacch-a-ti garhya-m |
| 4.4.31 | AGREES | 0.957 | kusīda-daśa-ekādaśāt ṣṭhanṣṭhacau | kusīda-daśa=ekādaś-āt ṢṭhaN=ṢṭhaC-au |
| 4.4.32 | VARIANTS | 0.750 | ucchati | uñch-a-ti |
| 4.4.33 | VARIANTS | 0.875 | rakṣati | rakṣ-a-ti |
| 4.4.34 | AGREES | 0.933 | śabda-darduraṃ karoti | śabda-dardura-ṃ kar-o-ti |
| 4.4.35 | MISSING | - | pakṣi-matsya-mṛgān hanti | - |
| 4.4.36 | AGREES | 0.920 | paripanthaṃ ca tiṣṭhati | pari-pantha-ṃ=ca tiṣṭh-a-ti |
| 4.4.37 | AGREES | 0.929 | mātha-uttarapada-padavy-anupadaṃ dhāvati | mātha=uttara-pada-padavī=anupada-ṃ dhāv-a-ti |
| 4.4.38 | VARIANTS | 0.824 | ākrandāṭ ṭhañ ca | ā-krand-āt=thaÑ ca |
| 4.4.39 | AGREES | 0.923 | pada-uttarapadaṃ gṛhṇāti | pada=uttara-pada-ṃ gṛh-ṇā-ti |
| 4.4.40 | AGREES | 0.966 | pratikaṇṭha-artha-lalāmaṃ ca | prati-kaṇṭha=artha=lalāma-ṃ ca |
| 4.4.41 | AGREES | 0.903 | dharmaṃ carati | dharma-ṃ car-a-ti |
| 4.4.42 | VARIANTS | 0.880 | pratipatham eti ṭhaṃś ca | prati-path-am e-ti ṭhaN=ca |
| 4.4.43 | AGREES | 0.927 | samavāyān samavaiti | samavāyā-n sam-a-vaiti |
| 4.4.44 | VARIANTS | 0.800 | pariṣado ṇyaḥ | pari-ṣad-aḥ=Ṇya-ḥ |
| 4.4.45 | VARIANTS | 0.857 | senāyā vā | senā-y-āḥ=vā |
| 4.4.46 | AGREES | 0.904 | sañjñāyāṃ lalāṭa-kukkuṭyau paśyati | saṃjñā-y-āṃ lalāṭa-kukkuṭy-au paśy-a-ti |
| 4.4.47 | AGREES | 0.903 | tasya dharmyam | ta-sya dharm-ya-m |
| 4.4.48 | AGREES | 0.919 | aṇ mahiṣy-ādibhyaḥ | aṆ mahiṣī=ādi-bhyaḥ |
| 4.4.49 | CONFLICTS | 0.571 | ṛto 'ñ | ṛT-aḥ=aÑ |
| 4.4.50 | VARIANTS | 0.857 | avakrayaḥ | ava-kray-a-ḥ |
| 4.4.51 | AGREES | 0.938 | tad asya paṇyam | tad a-sya paṇya-m |
| 4.4.52 | VARIANTS | 0.880 | lavaṇāṭ ṭhañ | lavaṇ-āt=ṭhaÑ |
| 4.4.53 | VARIANTS | 0.878 | kiśarādibhyaḥ ṣṭhan | kiśara=ādi-bhyas=ṢṭhaN |
| 4.4.54 | VARIANTS | 0.792 | śalāluno 'nyatarasyām | śalālu-n-aḥ=anya-taras-syām |
| 4.4.55 | AGREES | 0.923 | śilpam | śilpa-m- |
| 4.4.56 | VARIANTS | 0.899 | maḍḍuka-jharjharād aṇ anyatarasyām | maḍḍuka-jharjar-āt=aṆ=nya-tara-syām |
| 4.4.57 | VARIANTS | 0.870 | praharaṇam | pra-har-aṇa-m |
| 4.4.58 | AGREES | 0.923 | paraśvadhāṭ ṭhañ ca | paraśvadh-āt=ṭhaÑ ca |
| 4.4.59 | AGREES | 0.973 | śakti-yaṣṭyor īkak | śakti-yaṣṭy-or īkaK |
| 4.4.60 | AGREES | 0.917 | asti-nāsti-diṣṭaṃ matiḥ | asti-nāsti-diṣṭa-m mati-ḥ |
| 4.4.61 | VARIANTS | 0.727 | śīlaṃ | śīla-m |
| 4.4.62 | VARIANTS | 0.789 | chatrādibhyo ṇaḥ | chattra=ādi-bhyaḥ=Ṇa-ḥ |
| 4.4.63 | VARIANTS | 0.826 | karmādhyayane vṛttam | karma=adhy-ayan-e vṛt-ta-m |
| 4.4.64 | VARIANTS | 0.875 | bahv-ac-pūrvapadāṭ ṭhac | bahu=aC-pūrva-pad-āt=ṭhaC |
| 4.4.65 | VARIANTS | 0.828 | hitaṃ bhakṣāḥ | hi-ta-m bhakṣā-ḥ |
| 4.4.66 | VARIANTS | 0.857 | ta dasmai dīyate niyuktam | tad a-smai dī-ya-te ni-yuk-ta-m |
| 4.4.67 | AGREES | 0.941 | śrāṇā-māṃsa-odanāṭ ṭiṭhan | śrāṇā-māṃsa=odan-āt=ṬiṭhaN |
| 4.4.68 | VARIANTS | 0.800 | bhakṭād aṇ ānyatarasyām | bhak-t-āt=aṆ=anya-tara-syām |
| 4.4.69 | VARIANTS | 0.875 | tatra niyuktaḥ | ta-tra ni-yuk-ta-ḥ |
| 4.4.70 | AGREES | 0.909 | agāra-antāṭ ṭhan | agāra=ant-āt=ṭhaN |
| 4.4.71 | VARIANTS | 0.851 | adhyāyiny adeśa-kālāt | adhy-āy-in-i=a-deśa-kāl-āt |
| 4.4.72 | VARIANTS | 0.851 | kaṭhinānta-prastāra-saṃsthāneṣu vyavaharati | kaṭhina=anta-pra-stār-a-saṃ-thāne-ṣu vy-ava-ar-a-ti |
| 4.4.73 | VARIANTS | 0.867 | nikaṭe vasati | ni-kaṭ-e vas-a-ti |
| 4.4.74 | AGREES | 0.909 | āvasathāt ṣṭhal | ā-vas-ath-āt=ṢṭhaL |
| 4.4.75 | VARIANTS | 0.774 | prāg ghitād yat | prāk=hi-t-āt=yaT |
| 4.4.76 | VARIANTS | 0.871 | tadvahati rathayugaprāsaṅgam | tad vah-a-ti ratha-yuga-prāsaṛga-m |
| 4.4.77 | VARIANTS | 0.800 | dhuro yaḍ-ḍhakau | dhur-aḥ=yaT= ḍhaK-au |
| 4.4.78 | AGREES | 0.914 | khaḥ sarvadhurāt | kha-ḥ sarva-dhur-āt |
| 4.4.79 | VARIANTS | 0.882 | ekadhurāl luk ca | eka-dhur-āt=luK ca |
| 4.4.80 | VARIANTS | 0.857 | śakaṭād aṇ | śakaṭ-āt=aṆ |
| 4.4.81 | VARIANTS | 0.867 | halasīrāṭ ṭhak | hala-sīr-āt=ṭhaK |
| 4.4.82 | VARIANTS | 0.857 | sañjñāyāṃ janyāḥ | saṃjñā-y-āṃ jany-āḥ |
| 4.4.83 | VARIANTS | 0.811 | vidhyatyadhanuṣā | vidh-ya-ti=a-dhanuṣ-ā |
| 4.4.84 | VARIANTS | 0.895 | dhana-gaṇaṃ labdhā | dhana-gaṇa-m lab-dhā |
| 4.4.85 | VARIANTS | 0.800 | annāṇ ṇaḥ | ann-āt=Ṇa-ḥ |
| 4.4.86 | VARIANTS | 0.880 | vaśaṃ gataḥ | vaśa-ṃ ga-ta-ḥ |
| 4.4.87 | AGREES | 0.900 | padam asmin dṛśyam | pada-m a-smin dṛś-ya-m |
| 4.4.88 | VARIANTS | 0.865 | mūlam asya āvarhi | mūla-m a-sya=ā-barhi |
| 4.4.89 | VARIANTS | 0.842 | sañjñāyāṃ dhenuṣyā | saṃjñā-y-ām dhenuṣyā |
| 4.4.90 | VARIANTS | 0.889 | gṛhapatinā saṃyukte ñyaḥ | gṛha-pati-nā saṃ-yuk-t-e Ñya-ḥ |
| 4.4.91 | AGREES | 0.915 | nau-vayo-dharma-viṣa-mūla-mūla-sītā-tulābhyas tārya-tulya-prāpya-vadhya-ānāmya-sama-samita-saṃmiteṣu | nau-vayas=dharma-visa-mūla-mūla-sītā-tulā-bhyas=tār-ya-tul-ya-prāp-ya-vadh-ya=ā-nām-ya-sama-sa-mita-sam-mi-te-ṣu |
| 4.4.92 | MISSING | - | dharma-pathy-artha-nyāyād anapete | - |
| 4.4.93 | VARIANTS | 0.889 | chandaso nirmite | chandas-o nir-mi-t-e |
| 4.4.94 | VARIANTS | 0.720 | uraso 'ṇ ca | urasa-aḥ=aṆ ca |
| 4.4.95 | AGREES | 0.914 | hṛdayasya priyaḥ | hṛdaya-sya priy-a-ḥ |
| 4.4.96 | VARIANTS | 0.824 | bandhane carṣau | bandh-an=e ca=ṛṣ-au |
| 4.4.97 | VARIANTS | 0.886 | matajanahalāt karaṇajalpakarṣeṣu | mata-jana-hal-āt karaṇa-jalpa-karṣe-su |
| 4.4.98 | VARIANTS | 0.846 | tatra sādhuḥ | ta-tra sādhū-ḥ |
| 4.4.99 | AGREES | 0.957 | pratijana-ādibhyaḥ khañ | pratijana=ādi-bhyḥ khaÑ |
| 4.4.100 | VARIANTS | 0.800 | bhaktāṇ ṇaḥ | bhak-t-āt=Ṇa-ḥ |
| 4.4.101 | VARIANTS | 0.800 | pariṣado ṇyaḥ | pari-ṣad-aḥ=Ṇya-ḥ |
| 4.4.102 | VARIANTS | 0.865 | kathādibhyaṣ ṭhak | kathā-ādi-bhyas=ṭhaK |
| 4.4.103 | AGREES | 0.919 | guḍa-ādibhyaṣ ṭhañ | guḍa=ādi-bhyas=ṭhaÑ |
| 4.4.104 | MISSING | - | pathy-atithi-vasati-svapater ḍhañ | - |
| 4.4.105 | VARIANTS | 0.889 | sabhāyāḥ yaḥ | sabhā-y-āḥ=ya-ḥ |
| 4.4.106 | VARIANTS | 0.857 | ḍhaś chandasi | ḍha-s=chandas-i |
| 4.4.107 | VARIANTS | 0.821 | samānātīrthe vāsī | sa-mān-a-tīrth-e vās-ī |
| 4.4.108 | VARIANTS | 0.853 | samāna-udare śayita o codāttaḥ | sa-māna=udar-e śay-ita-s=o ca=udātta-ḥ |
| 4.4.109 | VARIANTS | 0.833 | sodarād yaḥ | sodar-āt=ya-ḥ |
| 4.4.110 | AGREES | 0.933 | bhave chandasi | bhav-e chandas-i |
| 4.4.111 | VARIANTS | 0.857 | pātho-nadībhyāṃ ḍyaṇ | pāthas=nadī-bhyām ḌyaṆ |
| 4.4.112 | AGREES | 0.979 | veśanta-himavadbhyām aṇ | veśanta-himavad-bhyām aṆ |
| 4.4.113 | VARIANTS | 0.830 | srotaso vibhāṣā ḍyaḍ-ḍyau | srotas-aḥ=vibhāṣā ḌyaT=Ḍy-aū |
| 4.4.114 | VARIANTS | 0.885 | sagarbha-sayūtha-sanutād yan | sa-garbha-sa-yūtha-sa-nu-t-āt=yaN |
| 4.4.115 | VARIANTS | 0.870 | tugrād ghan | tugr-āt=ghaN |
| 4.4.116 | VARIANTS | 0.842 | agrād yat | agr-āt=yaT |
| 4.4.117 | AGREES | 0.917 | gha-cchau ca | gha=ch-au ca |
| 4.4.118 | AGREES | 0.900 | samudra-abhrād ghaḥ | samudra=abhr-āt=gha-ḥ |
| 4.4.119 | AGREES | 0.903 | barhiṣi dattam | barhiṣ-i dat-ta-m |
| 4.4.120 | VARIANTS | 0.837 | dutasya bhāga-karmaṇī | dūta-syabhāga-karman-ī |
| 4.4.121 | VARIANTS | 0.844 | rakṣo-yātūnāṃ hananī | rakṣas=yātū-n-āṃ han-an-ī |
| 4.4.122 | AGREES | 0.946 | revatī-jagatī-haviṣyābhyaḥ praśasye | revatī-jagatī-haviṣyā-bhyaḥ pra-śas-y-e |
| 4.4.123 | AGREES | 0.929 | asurasya svam | asura-sya sva-m |
| 4.4.124 | AGREES | 0.909 | māyāyām aṇ | māyā-y-ām aṆ |
| 4.4.125 | AGREES | 0.938 | tadvān āsām upadhāno mantra iti iṣṭakāsu luk ca matoḥ | tad-vān ā-sām upa-dhā-n-o mantra=iti iṣṭakā-su luK ca matO-ḥ |
| 4.4.126 | AGREES | 0.900 | aśvimānaṇ | aśvi-mān aṆ |
| 4.4.127 | AGREES | 0.939 | vayasyāsu mūrdhno matup | vayasyā-su mūrdh-n-o matUP |
| 4.4.128 | VARIANTS | 0.889 |  matv-arhe māsa-tanvoḥ | matU=arth-e māsa-tanv-oḥ |
| 4.4.129 | AGREES | 0.960 | madhor ña ca | madho-r Ña ca |
| 4.4.130 | VARIANTS | 0.791 | ojaso 'hani yatkhau | ojas-aḥ=ahan-i yaT-kh-au |
| 4.4.131 | MISSING | - | veśo-yaśa-āder bhagād yal | - |
| 4.4.132 | AGREES | 1.000 | kha ca | kha ca |
| 4.4.133 | VARIANTS | 0.885 | pūrvaiḥ kṛtam ina-yau ca | pūrv-aiḥ kṛ-ta-m ini-y-au ca |
| 4.4.134 | VARIANTS | 0.865 | adbhiḥ saṃskṛtam | ad-bhiḥ saṃ-s-kṛ-ta-m |
| 4.4.135 | VARIANTS | 0.880 | sahasreṇa saṃmitau ghaḥ | sahasr-eṇa saṃ-mit-aū gha-ḥ |
| 4.4.136 | AGREES | 0.941 | matau ca | mat-AU ca |
| 4.4.137 | VARIANTS | 0.889 | somam arhati yaḥ | soma-m arh-a-ti ya-ḥ |
| 4.4.138 | AGREES | 0.933 | maye ca | may-e ca |
| 4.4.139 | AGREES | 0.923 | madhoḥ | madho-ḥ |
| 4.4.140 | AGREES | 0.909 | vasoḥ samūhe ca | vaso-ḥ sam-ūh-e ca |
| 4.4.141 | VARIANTS | 0.867 | nakṣatrād ghaḥ | nakṣatr-āt=gha-ḥ |
| 4.4.142 | AGREES | 0.941 | sarvadevāt tātil | sarva-dev-āt tātiL |
| 4.4.143 | AGREES | 0.936 | śiva-śam-ariṣṭasya kare | śiva-śam=ariṣṭa-ya kar-e |
| 4.4.144 | AGREES | 0.941 | bhāve ca | bhāv-e ca |
| 5.1.1 | VARIANTS | 0.882 | prāk-krītāc chaḥ | prāk=krīt-āt=cha-ḥ |
| 5.1.2 | VARIANTS | 0.788 | u-gavādibhyo yat | u-gav=ādi-hyaḥ=aT |
| 5.1.3 | VARIANTS | 0.756 | kaṃvalāc ca sañjñāyām | kambal-āt=ca saṃjñā-y-ām |
| 5.1.4 | AGREES | 0.929 | vibhāṣā havir-apūpa-ādibhyaḥ | vibhāṣā havis=apūpa=ādi-hyaḥ |
| 5.1.5 | AGREES | 0.923 | tasmai hitam | ta-smai hi-tam |
| 5.1.6 | AGREES | 0.923 | śarīra-avayavād yat | śarīra=avayav=āt=yaT |
| 5.1.7 | AGREES | 0.933 | khala-yava-māṣa-tila-vṛṣa-brahmaṇaś ca | khala-yava-māṣa-tilavṛṣa-brahmaṇ-s=ca |
| 5.1.8 | VARIANTS | 0.800 | ajāvibhyāṃ thyan | aja=avi-bhyām thyaN |
| 5.1.9 | AGREES | 0.923 | ātman-viśvajana-bhoga-uttarapadāt khaḥ | ātman=viśva-jana-bhoga=ttara-ad-āt kha-ḥ |
| 5.1.10 | AGREES | 0.909 | sarva-puruṣābhyāṃ ṇa-ḍhañau | sarva-puruṣā-hyām Ṇa-ḍhaÑ-au |
| 5.1.11 | AGREES | 0.936 | māṇava-carakābhyāṃ khañ | māṇava-carakā-bhyām khaÑ |
| 5.1.12 | VARIANTS | 0.885 | tad-arthaṃ vikṛteḥ prakṛtau | tad-artha-ṃ vi-kṛ-te-ḥ pra-kṛ-t-au |
| 5.1.13 | VARIANTS | 0.880 | chadir-upadhi-baler ḍhañ | chadis=upa-dhi-bale-ḥ=ḍhaÑ |
| 5.1.14 | AGREES | 0.952 | ṛṣabha-upānahor ñyaḥ | ṛṣabha-upānah-or Ñya-ḥ |
| 5.1.15 | VARIANTS | 0.727 | carmaṇo 'ñ | carmaṇ-aḥ=aÑ |
| 5.1.16 | AGREES | 0.912 | tad asya tad asmin syād iti | tad a-sya tad a-smin s-yāt=iti |
| 5.1.17 | VARIANTS | 0.839 | parikhāyā ṭhañ | parikhā-y-āḥ=ḍhaÑ |
| 5.1.18 | VARIANTS | 0.839 | prāg-vateṣ ṭhañ | prāk=vate-s=ṭhaÑ |
| 5.1.19 | VARIANTS | 0.871 | ā-arhād a-gopuccha-saṅkhyā-parimāṇāṭ ṭhak | ā=arh-āt=a-go-puccha-saṃkhyā-pari-āṇ-āt=ṭhaK |
| 5.1.20 | AGREES | 0.917 | asamāse niṣka-ādibhyaḥ | a-sam-ās-e niṣka=ādi-bhyaḥ |
| 5.1.21 | VARIANTS | 0.808 | śatāc ca ṭhanyatāv aśate | śat-āt=ca ṭhaN-yaT-u=a-śat-e |
| 5.1.22 | VARIANTS | 0.825 | saṅkhyāyā ati-śad-antāyāḥ kan | saṃkhyā-y-āḥ=a-ti-śat=ntā-y-āḥ kaN |
| 5.1.23 | VARIANTS | 0.870 | vator iḍ vā | vatO-r iṬ=vā |
| 5.1.24 | VARIANTS | 0.833 | viṃśati-triṃśadbhyāṃ ḍvun asañjñāyām | viṃśati-triṃśat=hyām ḌvuN a-aṃjñā--ām |
| 5.1.25 | VARIANTS | 0.815 | kaṃsāṭ ṭiṭhaṇ | kaṃs-āt=ṬiṭhaN |
| 5.1.26 | AGREES | 0.936 | śūrpād añ anyatarasyām | śūrp-ād aÑ anya-tara-syām |
| 5.1.27 | AGREES | 0.947 | śatamāna-viṃśatika-sahasra-vasanād aṇ | śata-māna-viṃśatika-sahasra-vasan-āt=aṆ |
| 5.1.28 | VARIANTS | 0.827 | adhyardhapūrva-dvigor lug asañjñāyām | adhi=ardha-pūrva-dvigo-r luK a-aṃjñā--ām |
| 5.1.29 | AGREES | 0.951 | vibhāṣā kārṣāpaṇa-sahasrābhyām | vibhāsā kārṣāpaṇa-sahasrā-bhyām |
| 5.1.30 | AGREES | 0.909 | dvi-tri-pūrvān niṣkāt | dvi-tri-pūrv-āt niṣk-āt |
| 5.1.31 | VARIANTS | 0.842 | bistāc ca | bist-āt=ca |
| 5.1.32 | AGREES | 0.938 | viṃśatikāt khaḥ | viṃśatik-āt kha-ḥ |
| 5.1.33 | AGREES | 0.917 | khāryā īkan | khāry-āḥ=īkaN |
| 5.1.34 | AGREES | 0.917 | paṇa-pāda-māṣa-śatād yat | paṇa-pāda-māṣa-śat-āt=aT |
| 5.1.35 | VARIANTS | 0.824 | śāṇād vā | śāṇ-āt=vā |
| 5.1.36 | AGREES | 0.927 | dvi-tri-pūrvād aṇ ca | dvi-tri-pūrv-āt=aṆ ca |
| 5.1.37 | VARIANTS | 0.880 | tena krītam | t-ena krī-ta-m |
| 5.1.38 | VARIANTS | 0.875 | tasya nimittaṃ saṃyoga-utpātau | ta-sya nimitta-m saṃ-yoga=ut-āt-au |
| 5.1.39 | VARIANTS | 0.824 | godvyaco 'saṅkhyā-parimāṇa-aśva-ader yat | go-dvy-aC-aḥ=a-saṃkhyā-pari-āṇa=aśva=de-r yaT |
| 5.1.40 | VARIANTS | 0.889 | putrāc cha ca | putr-āt=cha=ca |
| 5.1.41 | AGREES | 0.952 | sarvabhūmi-pṛthivībhyām aṇañau | sarva-bhūmi-pṛthivī bhyām aṆaÑ-au |
| 5.1.42 | VARIANTS | 0.897 | tasya+īśvaraḥ | ta-sya=īś-vara-ḥ |
| 5.1.43 | AGREES | 0.927 | tatra vidita iti ca | ta-tra vid-i-ta iti ca |
| 5.1.44 | AGREES | 0.905 | loka-sarvalokāṭ ṭhañ | loka-sarva-lok-āt=ṭhaÑ |
| 5.1.45 | VARIANTS | 0.880 | tasya vāpaḥ | ta-sya vāp-a-ḥ |
| 5.1.46 | AGREES | 0.960 | pātrāt ṣṭhan | pātr-āt=ṢṭhaN |
| 5.1.47 | AGREES | 0.915 | tad asmin vṛddhy-āya-lābha-śulka-upadā dīyate | tad a-smin vṛd-dhi=āya-lābha-śulka=upa-dā dī-a-te |
| 5.1.48 | AGREES | 0.919 | pūraṇa-ardhāṭ ṭhan | pūraṇa=ardh-āt=ṭhaN |
| 5.1.49 | VARIANTS | 0.815 | bhāgād yac ca | bhāg-āt=yaT=ca |
| 5.1.50 | VARIANTS | 0.835 | tad dharati vahavty āvahati bhārād vaṃśādibhyaḥ | tad=har-a-ti-vah-a-ti=ā-vah-a-ti bhār-āt=vaṃśa=ādi-bhyaḥ |
| 5.1.51 | AGREES | 0.966 | vasna-dravyābhyāṃ ṭhan-kanau | vasna-dravyā-bhyāṃ ṭhaN-kaN-au |
| 5.1.52 | VARIANTS | 0.820 | sambhavaty avaharati pacati | sam-bhav-a-ti=ava-har-a-ti-pac-a-i |
| 5.1.53 | VARIANTS | 0.880 | āḍhaka-ācita-pātrāt kho 'nyatarasyām | āḍhaka=ācita-pātr-āt kha-ḥ=nya-tara-yām |
| 5.1.54 | VARIANTS | 0.812 | dvigoḥ ṣṭhaṃś ca | dvigo-s=ṢṭhaN=ca |
| 5.1.55 | VARIANTS | 0.872 | kulijāl lukkhau ca | kulij-āt=luK-kh-au ca |
| 5.1.56 | VARIANTS | 0.842 | so 'sya aṃśa-vasna-bhṛtayaḥ | sa-ḥ=a-sya=aṃśa-vasna-bhṛtay-ḥ |
| 5.1.57 | AGREES | 0.923 | tad asya parimāṇam | tad a-sya pari-māṇa-m |
| 5.1.58 | VARIANTS | 0.864 | saṅkhyāyāḥ sañjñā-saṅgha-sūtra-adhyayaneṣu | samkhyā-y-āḥ saṃjñā-saṃgha-sūtra-adhy-ay-ne-ṣu |
| 5.1.59 | AGREES | 0.954 | paṅkti-viṃśati-triṃśac-catvāriṃśat-pañcāśat-ṣaṣṭi-saptaty-aśīti-navati-śatam | paṛkti-viṃśati-triṃśat-catvāriṃśat-pañcāśat-ṣaṣṭi-saptati=aśīti-navati-śata-m |
| 5.1.60 | AGREES | 0.917 | pañcad-daśatau varge vā | pañcat=daśat-au varg-e vā |
| 5.1.61 | VARIANTS | 0.829 | saptano 'ñ chandasi | saptan-aḥ=aÑ chandas-i |
| 5.1.62 | VARIANTS | 0.889 | triṃśac-catvāriṃśator brāhmaṇe sañjñāyāṃ ḍaṇ | triṃśat=catvāriṃśat-or brāhmaṇ-e saṃjñā--ām ḌaṆ |
| 5.1.63 | AGREES | 0.909 | tad arhati | tad arh-a-ti |
| 5.1.64 | AGREES | 0.905 | cheda-ādibhyo nityam | cheda=ādi-bhyaḥ nityam |
| 5.1.65 | VARIANTS | 0.850 | śīrṣacchedād yac ca | śīrṣa-cched-āt=yaT=ca |
| 5.1.66 | VARIANTS | 0.815 | daṇdādibhyaḥ | daṇḍa=ādi-bhyaḥ |
| 5.1.67 | AGREES | 0.957 | chandasi ca | chandas-i ca |
| 5.1.68 | VARIANTS | 0.800 | pātrād ghaṃś ca | pātr-āt=ghaN=ca |
| 5.1.69 | VARIANTS | 0.880 | kaḍaṅkaradakṣiṇāc cha ca | kaḍaṛkara-dakṣiṇ-āt=cha ca |
| 5.1.70 | AGREES | 0.917 | sthālībilāt | sthālī-bil-āt |
| 5.1.71 | AGREES | 0.912 | yajña-rtvigbhyāṃ gha-khañau | yajña=ṛtv-ig-bhyāṃ gha-khaÑ-au |
| 5.1.72 | AGREES | 0.927 | pārāyaṇa-turāyaṇa-cādnrāyaṇaṃ vartayati | pārāyaṇa-turāyaṇa-cāndrāyaṇa-ṃ vart-ay-a-ti |
| 5.1.73 | VARIANTS | 0.857 | saṃśayamāpannaḥ | saṃ-śay-am ā-panna-ḥ |
| 5.1.74 | AGREES | 0.914 | yojanaṃ gacchati | yojana-ṃ gacch-a-ti |
| 5.1.75 | AGREES | 0.957 | pathaḥ ṣkan | path-aḥ=ṢkaN |
| 5.1.76 | AGREES | 0.941 | pantho ṇa nityam | panth-o Ṇa nitya-m |
| 5.1.77 | VARIANTS | 0.863 | uttarapathen āhṛtaṃ ca | ut-tara-path-ena=ā-hṛ-ta-ṃ ca |
| 5.1.78 | AGREES | 0.909 | kālāt | kāl-āt |
| 5.1.79 | VARIANTS | 0.812 | tena virvṛttam | t-ena nir-vṛt-ta-m |
| 5.1.80 | VARIANTS | 0.750 | tam adhīṣṭo bhṛto bhūto bhāvī | tam adhīṣṭa-ḥ bhṛ-ta-ḥ=hū-ta-ḥ=hāvī |
| 5.1.81 | VARIANTS | 0.826 | māsād vayasi yatkhañau | mās-āt=vayas-i yaT-kh-au |
| 5.1.82 | AGREES | 0.952 | dvigor yap | dvigo-r yaP |
| 5.1.83 | VARIANTS | 0.824 | ṣaṇmāsāṇ ṇyac ca | ṣaṇ-mās-āt=ṆyaT=ca |
| 5.1.84 | VARIANTS | 0.848 | avayasi ṭhaṃś ca | a-vayas-i ṭhaN=ca |
| 5.1.85 | VARIANTS | 0.889 | samāyāḥ khaḥ | samā-y-āḥ kha-ḥ |
| 5.1.86 | AGREES | 0.947 | dvigor vā | dvigo-r vā |
| 5.1.87 | MISSING | - | rātry-ahaḥ-saṃvatsarāc ca | - |
| 5.1.88 | VARIANTS | 0.889 | varṣāl luk ca | varṣ-āt=luK ca |
| 5.1.89 | AGREES | 0.914 | cittavati nityam | citta-vat-i nitya-m |
| 5.1.90 | AGREES | 0.909 | ṣaṣṭikāḥ ṣaṣṭirātreṇa pacyante | ṣaṣṭi-k-āḥ ṣaṣṭi-rātr-eṇa pac-y-ante |
| 5.1.91 | VARIANTS | 0.800 | vatsarāntāc chaś chandasi | vatsara=ant=āt=cha-s=chandas-i |
| 5.1.92 | VARIANTS | 0.857 | saṃparipūrvāt kha ca | sam-pari-ūrv-āt kha ca |
| 5.1.93 | VARIANTS | 0.895 | tena parijayya-labhya-kārya-sukaram | t-ena pari-jay-ya-labh-ya-kār-ya-su-ar-am |
| 5.1.94 | AGREES | 0.913 | tad asya brahmacaryam | tad a-sya brahma-car-ya-m |
| 5.1.95 | AGREES | 0.939 | tasya ca dakṣiṇā yajñākhyebhyaḥ | ta-sya ca dakṣiṇā yajña=ākhye-bhyaḥ |
| 5.1.96 | VARIANTS | 0.870 | tatra ca dīyate kāryaṃ bhavavat | ta-tra ca dī-ya-te kār-ya-m bhav-a-vat |
| 5.1.97 | VARIANTS | 0.811 | vyuṣṭa-ādibhyo 'ṇ | vy-uṣṭa=ādi-bhyaḥ=aṆ |
| 5.1.98 | AGREES | 0.909 | tena yathākathāca-hastābhyāṃ ṇa-yatau | t-enayathā-kathā-ca-hastā-hyāṃ Ṇa-yaT-au |
| 5.1.99 | VARIANTS | 0.857 | sampādini | sam-pād-in-i |
| 5.1.100 | MISSING | - | karma-veṣād yat | - |
| 5.1.101 | VARIANTS | 0.838 | tasmai prathavati santāpa-ādibhyāḥ | ta-smai pra-bhav-a-ti saṃ-tāpa=ādi-bhyaḥ |
| 5.1.102 | VARIANTS | 0.800 | yogād yac ca | yog-āt=yaT=ca |
| 5.1.103 | AGREES | 0.923 | karmaṇa ukañ | karmaṇ-aḥ=ukaÑ |
| 5.1.104 | AGREES | 0.906 | samayas tad asya prāptam | samaya-s tad a-sya prā-p-ta-m |
| 5.1.105 | VARIANTS | 0.857 | ṛtoraṇ | ṛto-r aṆ |
| 5.1.106 | AGREES | 0.963 | chandasi ghas | chandas-i ghaS |
| 5.1.107 | VARIANTS | 0.842 | kālād yat | kāl-āt=yaT |
| 5.1.108 | VARIANTS | 0.897 | prakṛṣṭe ṭhañ | pra-kṛṣ-ṭ-e ṭhaÑ |
| 5.1.109 | VARIANTS | 0.870 | prayojanam | pra-yoj-ana-m |
| 5.1.110 | AGREES | 0.914 | viśākhā-aṣāḍhād aṇ mantha-daṇḍayoḥ | vi-śākhā=aṣāḍh-āt aṆ mantha-daṇḍay-ḥ |
| 5.1.111 | VARIANTS | 0.877 | anupravacana-ādibhyaś chaḥ | anu-pra-vac-ana=ādi-bhyaḥ=cha-ḥ |
| 5.1.112 | VARIANTS | 0.880 | samāpanāt sapūrvapadāt | sam-āp-an-āt sa-pūrva-pad-āt |
| 5.1.113 | AGREES | 0.971 | aikāgārikaṭ caure | aikāgārikaṬ caur-e |
| 5.1.114 | VARIANTS | 0.824 | ākālikaḍ-ādyantavacane | ā-kāl-ika-Ṭ=ādy-anta-vac-an-e |
| 5.1.115 | AGREES | 0.931 | tena tulyaṃ kriyā ced vatiḥ | t-ena tul-ya-ṃ kriyā ced vati-ḥ |
| 5.1.116 | AGREES | 0.938 | tatra tasya+iva | ta-tra ta-sya=iva |
| 5.1.117 | AGREES | 0.900 | tad arham | tad arh-a-m |
| 5.1.118 | AGREES | 0.906 | upasargāc chandasi dhātv-arthe | upa-sarg-āt=chandas-i dhātv-arth-e |
| 5.1.119 | VARIANTS | 0.851 | tasya bhāvas tva-talau | ta-sya bhāv-a-ḥ=tva-taL-u |
| 5.1.120 | AGREES | 0.947 | ā ca tvāt | ā ca tv-āt |
| 5.1.121 | AGREES | 0.912 | na nañpūrvāt tatpuruṣād acatura-saṅgatal-avaṇa-vaṭa-budha-kata-rasa-lasebhyaḥ | na naÑ-pūrv-āt tatpuruṣ-āt=a-catura-saṃ-gata-lavaṇa-vaṭa-yudha-kata-rasa-lase-bhyaḥ |
| 5.1.122 | VARIANTS | 0.826 | pṛthv-ādibhya imanij vā | pṛthu=ādi-bhyaḥ=maniC=ā |
| 5.1.123 | AGREES | 0.964 | varṇa-dṛḍha-ādibhyaḥ ṣyañ ca | varṇa-dṛḍha-ādi-hyaḥ ṢyaÑ ca |
| 5.1.124 | AGREES | 0.923 | guṇavacana-brāhmaṇādibhyaḥ karmaṇi ca | guṇa-vac-ana-brāhmaṇa=ādihyaḥ karmaṇ-i ca |
| 5.1.125 | VARIANTS | 0.756 | stonād yan nalopaś ca | sten-āt=yaT=na-lopa-s=ca |
| 5.1.126 | AGREES | 0.917 | sakhyur yaḥ | sakhy-ur ya-ḥ |
| 5.1.127 | AGREES | 0.971 | kapi-jñātyor ḍhak | kapi-jñāty-or ḍhaK |
| 5.1.128 | VARIANTS | 0.772 | patyantapurohitādibhyo yak | pati=anta-puro-hita=ādi-hyaḥ=aK |
| 5.1.129 | VARIANTS | 0.800 | prāṇabhṛjjāti-vayovacana-udgātrādibhyo 'ñ | prāṇa-bhṛt=jāti-vayo-vac-ana=ud-gā-tṛ=ādi-hyaḥ=aÑ |
| 5.1.130 | MISSING | - | hāyanānta-yuvādibhyo 'ṇ | - |
| 5.1.131 | VARIANTS | 0.880 | ig-antāś ca laghu-pūrvāt | iK=ant-āt=ca laghu-pūrv-āt |
| 5.1.132 | VARIANTS | 0.862 | ya-upadhād guru-upottamād vuñ | ya=upadh-āt=guru=pottam-āt=uÑ |
| 5.1.133 | VARIANTS | 0.852 | dvandva-manojña-ādibhyaś ca | dvaṃdva-mano-jña=ādi-hyas=a |
| 5.1.134 | VARIANTS | 0.837 | gotracaraṇāc chlāghā-atyākāra-tadaveteṣu | go-tra-caraṇ-āt ślāghā=aty-ā-kāra-tad-ve-te-ṣu |
| 5.1.135 | VARIANTS | 0.875 | hotrābhyaś chaḥ | hotrā-bhyas=cha-ḥ |
| 5.1.136 | AGREES | 0.933 | brahmaṇas tvaḥ | brahmaṇ-as tva-ḥ |
| 5.2.1 | VARIANTS | 0.889 | dhānyānāṃ bhavane kṣetre khañ | dhānyā-n-ām bhav-an-e kṣetr-e khaÑ |
| 5.2.2 | AGREES | 0.941 | vrīhi-śālyor ḍhak | vrīhiśāly-or ḍhaK |
| 5.2.3 | VARIANTS | 0.875 | yava-yavaka-ṣaṣṭikād yat | yava-yava-ka-ṣaṣṭi--āt=aT |
| 5.2.4 | AGREES | 0.946 | vibhāṣā tila-māṣa-umā-bhaṅgā-aṇubhyaḥ | vibhāṣā tila-māṣa=umā-bhaṛgā-aṇu=hyaḥ |
| 5.2.5 | AGREES | 0.923 | sarvacarmaṇaḥ kṛtaḥ kha-khañau | sarva-carmaṇ-aḥ kṛ-ta-ḥ kha-khaÑ-au |
| 5.2.6 | VARIANTS | 0.897 | yathāmukha-sammukhasya darśanaḥ khaḥ | yathā-mukha- saṃ-mukha-sya darś-ana-ḥ kha-ḥ |
| 5.2.7 | MISSING | - | tat sarva-ādeḥ pathy-aṅga-karma-patra-pātraṃ vyāpnoti | - |
| 5.2.8 | VARIANTS | 0.810 | āprapadaṃ prāpnoti | ā-pra-pada-m pr-āp-no-ti |
| 5.2.9 | VARIANTS | 0.885 | anupada-sarvānna-aya-anayaṃ baddhā-bhakṣayati-neyeṣu | anu-pada-sarva-anna=aya=an-ay-am baddhā-bhakṣ-ay-a-ti-neye-ṣu |
| 5.2.10 | AGREES | 0.933 | parovara-parampara-putrapautram anubhavati | parovara-param-para-putra-pautra-m anu-bhav-a-ti |
| 5.2.11 | VARIANTS | 0.879 | avārapāra-atyanta-anukāmaṃ gāmī | avāra-pāra=aty-anta=anu-āma-m gām-ī |
| 5.2.12 | VARIANTS | 0.818 | samāṃsamāṃ vijāyate | samā-ṃ-samā-m vi-jā-ya-te |
| 5.2.13 | VARIANTS | 0.870 | adyaśvīnā avaṣṭabdhe | adya-śv-īn-ā ava-ṣṭab-dh-e |
| 5.2.14 | VARIANTS | 0.842 | āgavīnaḥ | ā-gav-īna-ḥ |
| 5.2.15 | VARIANTS | 0.774 | anugv-alaṅgāmī | anu-gu=alaṃ-gām-ī |
| 5.2.16 | VARIANTS | 0.857 | adhvano yat-khau | adhvan-aḥ=yaT-kh-au |
| 5.2.17 | VARIANTS | 0.872 | abhyamitrāc cha ca | abhy-a-mitr-āt=cha ca |
| 5.2.18 | AGREES | 0.920 | goṣṭhāt khañ bhūtapūrve | goṣṭh-āt khaÑ bhū-ta-pūrv-e |
| 5.2.19 | VARIANTS | 0.750 | aśvasyaikāhagamaḥ | aśva-sya=eka=aha=gama-ḥ |
| 5.2.20 | VARIANTS | 0.870 | śālīna-kaupīne adhṛṣṭa-akāryayoḥ | śāl-īna-kaup-īn-e a-hṛṣ-ṭa-a-āryay-oḥ |
| 5.2.21 | AGREES | 0.903 | vrātena jīvati | vrāt-ena jīv-a-ti |
| 5.2.22 | VARIANTS | 0.889 | sāptapadīnaṃ sakhyam | sāpta-pad-īna-ṃ sakh-ya-m |
| 5.2.23 | VARIANTS | 0.800 | haiyaṅgavīnaṃ sañjñāyām | haiyaṃ-gav-īna-ṃ saṃjñā-y-ā |
| 5.2.24 | VARIANTS | 0.887 | tasya pāka-mūle pīlvadi-karṇādibhyaḥ kuṇab-jāhacau | ta-sya pāka-mūl-e pīlu=adi-karṇa=ādi-hyaḥ kuṇaP=jāhaC-au |
| 5.2.25 | AGREES | 0.909 | pakṣāt tiḥ | pakṣ-āt ti-ḥ |
| 5.2.26 | VARIANTS | 0.893 | tena vittaś cuñcup-caṇapau | t-ena vit-ta-ḥ cuñcuP-caṇaP-au |
| 5.2.27 | AGREES | 0.912 | vi-nañbhyāṃ nā-nāñau nasaha | vi-naÑ-bhyām nā-nāÑ-au na-saha |
| 5.2.28 | VARIANTS | 0.837 | veḥ śālac-chaṅkaṭacau | ve-ḥ śālaC-śaṛkaṭaC-au |
| 5.2.29 | VARIANTS | 0.884 | saṃ-pra-udaś ca kaṭac | sam-pra=ud-as=ca kaṭaC |
| 5.2.30 | AGREES | 0.968 | avāt kuṭārac ca | av-āt kuṭāraC ca |
| 5.2.31 | VARIANTS | 0.833 | nate nāsikāyāḥ sañjñāyāṃ ṭīṭañ-nāṭaj-bhraṭacaḥ | na-t-e nāsikā-y-āḥ saṃjñā--āṃ ṭīṭaC-nāṭaC-bhrāṭaC-ḥ |
| 5.2.32 | VARIANTS | 0.842 | nerbiḍajbirīsacau | ne-r biḍaC-birīsaC-au |
| 5.2.33 | AGREES | 1.000 | inac piṭac cika ci ca | inaC-piṭaC-cika-ci ca |
| 5.2.34 | VARIANTS | 0.875 | upa-adhibhyāṃ tyakann āsanna-ārūḍhayoḥ | upa=adhi-bhyām tyakaN ā-san-na=ā-ū-ḍhay-oḥ |
| 5.2.35 | VARIANTS | 0.829 | karmaṇi ghaṭo 'ṭhac | karmaṇ-i ghaṭa-ḥ=aṭhaC |
| 5.2.36 | AGREES | 0.911 | tad asya sañjātaṃ tārakā-ādibhya itac | tad a-sya saṃ-jā-ta-ṃ-tārakā=ādibhyaḥ itaC |
| 5.2.37 | VARIANTS | 0.899 | pramāṇe dvayasaj-daghnañ-mātracaḥ | pra-māṇ-e dvayasaC-daghnaC-mātraC-aḥ |
| 5.2.38 | AGREES | 0.979 | puruṣa-hastibhyām aṇ ca | puruṣa-hasti-bhyām aṆ ca |
| 5.2.39 | VARIANTS | 0.889 | yat-tad-etebhyaḥ parimāṇe vatup | yad=tad=ete-hyaḥ pari-āṇ-e vatUP |
| 5.2.40 | VARIANTS | 0.851 | kim-idam-bhyāṃ vo ghaḥ | kim=idam-bhyām v-aḥ gha-ḥ |
| 5.2.41 | AGREES | 0.903 | kimaḥ saṅkhyāparimāṇe ḍati ca | kim-aḥ saṃkhyā-pari-māṇ-e Ḍati ca |
| 5.2.42 | VARIANTS | 0.863 | saṅkhyāyā avayave tayap | saṃkhyā-y-āḥ=ava-yav-e tayaP |
| 5.2.43 | VARIANTS | 0.857 | dvi-tribhyāṃ tayasya ayaj vā | dvi-tri-bhyām taya-ya=yaC=vā |
| 5.2.44 | VARIANTS | 0.829 | ubhād udātto nityam | ubh-āt udāttaḥ nitya-m |
| 5.2.45 | VARIANTS | 0.868 | tad asminn adhikam iti daśāntāḍ ḍaḥ | tad a-sminn adhi-ka-m iti daśa=nt-āt Ḍa-ḥ |
| 5.2.46 | VARIANTS | 0.895 | śadanta-viṃśateś ca | śat=anta=viṃśate-=ca |
| 5.2.47 | VARIANTS | 0.879 | saṅkhyāyā guṇasya nimāne mayaṭ | saṃkhyā-y-āḥ=guṇa-sya ni-mān-e mayaṬ |
| 5.2.48 | AGREES | 0.914 | tasya pūraṇe ḍaṭ | ta-sya pūr-aṇ-e ḌaṬ |
| 5.2.49 | VARIANTS | 0.873 | na antād asaṅkhyā-āder maṭ | na=ant-āt=a-saṃkhyā=āde-r maṬ |
| 5.2.50 | AGREES | 0.970 | thaṭ ca chandasi | thaṬ ca chandas-i |
| 5.2.51 | AGREES | 0.984 | ṣaṭ-kati-katipaya-caturāṃ thuk | ṣaṭ-kati-katipaya-catur-āṃ thuK |
| 5.2.52 | AGREES | 0.952 | bahu-pūga-gaṇa-saṅghasya tithuk | bahu-pūga-gaṇa-saṃgha-sya tithuK |
| 5.2.53 | MISSING | - | vator ithuk | - |
| 5.2.54 | AGREES | 0.909 | dves tīyaḥ | dve-s tīya-ḥ |
| 5.2.55 | VARIANTS | 0.818 | treḥ samprasāraṇaṃ ca | tre-ḥ sam-pra-sār-aṇa-m |
| 5.2.56 | VARIANTS | 0.865 | viṃśaty-ādibhyas tamaḍ anyatarasyām | viṃ-śati=ādi-bhyaḥ tamaṬ=anya-tara-syām |
| 5.2.57 | AGREES | 0.901 | nityaṃ śatādi-māsa-ardhamāsa-saṃvatsarāc ca | nitya-ṃ śata=ādi-māsa=ardha-māsa-saṃ-atsar-āt=ca |
| 5.2.58 | VARIANTS | 0.778 | ṣaṣṭyādeś ca asaṅkhyādeḥ | ṣaṣṭi-āde-s=ca=a-saṃkhyā-āde-ḥ |
| 5.2.59 | AGREES | 0.936 | matau chaḥ sūkta-sāmnoḥ | matAU cha-ḥ sūkta-sāmn-ḥ |
| 5.2.60 | AGREES | 0.936 | adhyāya-anuvākayor luk | adhy-āya-anu-vākay-or luK |
| 5.2.61 | VARIANTS | 0.800 | vimukta-ādibhyo 'ṇ | vi-muk-ta=ādi-bhyaḥ=aṆ |
| 5.2.62 | VARIANTS | 0.833 | goṣadādibhyo vun | go-ṣad=ādi-bhyaḥ vuN |
| 5.2.63 | AGREES | 0.930 | tatra kuśalaḥ pathaḥ | ta-tra kuśala-ḥ path-aḥ |
| 5.2.64 | VARIANTS | 0.842 | ākarśādibhyaḥ kan | ā-karṣa=ādi-bhyaḥ kaN |
| 5.2.65 | AGREES | 0.950 | dhana-hiraṇyāt kāme | dhana-hiraṇy-āt kām-e |
| 5.2.66 | VARIANTS | 0.773 | svāṅgebhyaḥ prasite | sva=aṛge-bhyaḥ pra-si-t-e |
| 5.2.67 | VARIANTS | 0.769 | udarāṭ ṭhagādyūne | udar-āt=ṭhaK=ā-dyū-n-e |
| 5.2.68 | VARIANTS | 0.895 | sasyena parijātaḥ | sasy-ena pari-jā-ta-ḥ |
| 5.2.69 | VARIANTS | 0.818 | aṃśaṃ hāri | aṃśa-ṃ hār-ī |
| 5.2.70 | VARIANTS | 0.851 | tantrād-acira-apahṛte | tantr-āt=a-cira=apa-hṛ-t-e |
| 5.2.71 | VARIANTS | 0.877 | brāhmaṇaka-uṣṇike sañjñāyām | brāhmaṇa-ka=uṣṇi-k-e saṃjñā--ām |
| 5.2.72 | VARIANTS | 0.762 | śītoṣṇābhyāṃ kāriṇi | śīta=uṣṇa-bhyām kāriṇ-i |
| 5.2.73 | VARIANTS | 0.875 | adhikam | adhi-ka-m |
| 5.2.74 | VARIANTS | 0.862 | anuka-abhika-abhīkaḥ kamitā | anu-ka=abhi-ka=abhī-a-ḥ kam-i-ā |
| 5.2.75 | AGREES | 0.905 | pārśvena anvicchati | pārśv-ena=anv-icch-a-ti |
| 5.2.76 | AGREES | 0.933 | ayaḥśūla-daṇḍa-ajinābhyāṃ ṭhak-ṭhañau | ayaḥ-śūla-daṇḍa=jinā-hyāṃ ṭhaK-ṭhaÑ-au |
| 5.2.77 | AGREES | 0.906 | tāvatithaṃ grahaṇam iti lug vā | tāva-titha-ṃ grah-aṇa-m iti luK=vā |
| 5.2.78 | VARIANTS | 0.857 | sa eṣāṃ grāmaṇīḥ | sa e-ṣām grāma-ṇī-ḥ |
| 5.2.79 | VARIANTS | 0.899 | śṛṅkhalam asya bandhanaṃ karabhe | śṛṛkhala-m a-sya bandh-ana-ṃ karabh-e |
| 5.2.80 | VARIANTS | 0.828 | utka unamanāḥ | ut-ka-ḥ un-manāḥ |
| 5.2.81 | VARIANTS | 0.837 | kāla-prayojanād roge | kāla-pra-yoj-an-āt=og-e |
| 5.2.82 | VARIANTS | 0.870 | tad asminn annaṃ prāye sañjñāyām | tad a-sminn anna-m prāy-e saṃjñā-y-ām |
| 5.2.83 | VARIANTS | 0.870 | kulmāṣād añ | kulmāṣ-āt=aÑ |
| 5.2.84 | VARIANTS | 0.816 | śrotriyaṃ śchando 'dhīte | śrotriyaN=chandaḥ=adhī-te |
| 5.2.85 | AGREES | 0.917 | śrāddham anenan bhuktam ini-ṭhanau | śrāddha-m an-ena bhuk-ta-m ini-ṭhaN-au |
| 5.2.86 | VARIANTS | 0.783 | pūrvādiniḥ | pūrv-āt=ini-ḥ |
| 5.2.87 | VARIANTS | 0.833 | sapūrvāc ca | sa-pūrv-āt=ca |
| 5.2.88 | VARIANTS | 0.882 | iṣṭa-ādibhyaś ca | iṣ-ṭa=ādi-bhyas=ca |
| 5.2.89 | MISSING | - | chandasi paripanthi-paripariṇau paryavasthātari | - |
| 5.2.90 | VARIANTS | 0.824 | anupady-anveṣṭā | anu-pad-ī=anv-eṣ-ṭā |
| 5.2.91 | VARIANTS | 0.852 | sākṣād draṣṭari sañjñāyām | sākṣ-āt draṣṭar-i saṃjñā-y-ām |
| 5.2.92 | AGREES | 0.909 | kṣetriyac parakṣetre cikitsyaḥ | kṣetr-iyaC para-kṣetr-e cikit-s-ya-ḥ |
| 5.2.93 | VARIANTS | 0.871 | indriyam-indraliṅgam-indradṛṣṭam-indrasṛṣṭam-indrajuṣṭam-indradattam iti vā | indr-iya-m=indra-linga-m=indra-dṛṣ-ṭa-m-indra-ṛṣ-ṭa-m-indra-uṣ-ṭa-m-indra-at-ta-m iti vā |
| 5.2.94 | AGREES | 0.903 | tad asya asty asminn iti matup | tad a-sya=as-ti=a-smin=iti matUP |
| 5.2.95 | VARIANTS | 0.839 | rasādibhyaś ca | rasa=ādi-bhyas=ca |
| 5.2.96 | VARIANTS | 0.879 | prāṇisthād āto laj anyatarasyām | prāṇi-sth-āt=āTo laC=anya-tara-syām |
| 5.2.97 | AGREES | 0.919 | sidhma-ādibhyaś ca | sidhma=ādi-bhyas=ca |
| 5.2.98 | VARIANTS | 0.816 | vatsāṃsābhyāṃ kāmabale | vatsa=aṃsā-bhyām kāma-bal-e |
| 5.2.99 | VARIANTS | 0.897 | phenād ilac ca | phen-āt=ilaC ca |
| 5.2.100 | MISSING | - | lomādi-pāmādi-picchādibhyaḥ śa-na-ilacaḥ | - |
| 5.2.101 | VARIANTS | 0.873 | prajñā-śraddhā-arcā-vṛttibhyo ṇaḥ | pra-jñā-śrad-dhā=arc-ā-vṛtti-hyaḥ Ṇa-ḥ |
| 5.2.102 | VARIANTS | 0.873 | tapaḥ-sahasrābhyāṃ vini-inī | tapas-sahasrā-bhyām vini=ini |
| 5.2.103 | AGREES | 1.000 | aṇ ca | aṆ ca |
| 5.2.104 | VARIANTS | 0.837 | sikatā-śarkarābhyāṃ ca | sikatā-śarkara-hyām=a |
| 5.2.105 | VARIANTS | 0.895 | deśe lub-ilacau ca | deś-e luP=ilaC=au ca |
| 5.2.106 | AGREES | 0.944 | danta unnata urac | danta un-na-ta uraC |
| 5.2.107 | AGREES | 0.941 | ūṣa-suṣi-muṣka-madho raḥ | ūṣa-suṣi-muṣka-madho-ḥ ra-ḥ |
| 5.2.108 | VARIANTS | 0.882 | dyu-drubhyāṃ maḥ | dyu-dru-bhyām ma-ḥ |
| 5.2.109 | VARIANTS | 0.766 | keśād vo 'nyatarasyām | keś-āt=va-ḥ=anya-tara-syām |
| 5.2.110 | VARIANTS | 0.826 | gāṇḍyajagāt sañjñāyām | gāṇḍī=ajag-āt saṃjñā-y-ām |
| 5.2.111 | VARIANTS | 0.898 | kāṇḍa-āṇḍād īrann-īracau | kāṇḍa=āṇḍ-āt īraN=īraC-au |
| 5.2.112 | VARIANTS | 0.831 | rajaḥ-kṛṣy-āsuti-pariṣado valac | rajas=kṛṣi=ā-uti-pari-ṣad-aḥ valaC |
| 5.2.113 | VARIANTS | 0.894 | danta-śikhāt sañjñāyām | danta-śikh-āt saṃjñā-y-ām |
| 5.2.114 | AGREES | 0.917 | jyotsnā-tamisrā-śṛṅgiṇa-ūrjasvinn-ūrjasvala-gomin-malina-malīmasāḥ | jyotsnā-tamisrā-śṛṛg-ṇa-ūrjas-in=ūrjas-ala-go-min-malina-malīmas-āḥ |
| 5.2.115 | VARIANTS | 0.867 | ata iniṭhanau | aT-aḥ=ini-ṭhaN-au |
| 5.2.116 | VARIANTS | 0.824 | vrīhyādibhyaś ca | vrīhi=ādi-bhyas=ca |
| 5.2.117 | AGREES | 0.905 | tundādibhya ilac ca | tunda=ādi-bhyaḥ=ilaC ca |
| 5.2.118 | AGREES | 0.923 | eka-go-pūrvāṭ ṭhañ nityam | eka-go-pūrv-āt=ṭhaÑ nitya-m |
| 5.2.119 | AGREES | 0.912 | śata-sahasra-antāc ca niṣkāt | śata-sahasra=ant-āt=a niṣk-āt |
| 5.2.120 | VARIANTS | 0.772 | rūpād āhata-praśaṃsayor yap | rūp-at=ā-ha-ta-pra-śaṃsay-ḥ=aP |
| 5.2.121 | VARIANTS | 0.885 | as-māyā-medhā-srajo viniḥ | as-māyā-medhā-sraj-aḥ=ini-ḥ |
| 5.2.122 | AGREES | 0.941 | bahulaṃ chandasi | bahula-ṃ chandas-i |
| 5.2.123 | VARIANTS | 0.870 | ūrṇāyā yus | ūrṇā-y-āḥ=yuS |
| 5.2.124 | AGREES | 0.917 | vāco gminiḥ | vāc-o gmini-ḥ |
| 5.2.125 | VARIANTS | 0.833 | ālajāṭacau bahubhāṣiṇi | ālaC=āṭaC-au bahu-hāṣ-iṇ-i |
| 5.2.126 | VARIANTS | 0.857 | svāminn-aiśvarye | sv-ām-in=aiśvar-y-e |
| 5.2.127 | VARIANTS | 0.765 | arśa-ādibhyo 'c | arś-as=ādi-bhyaḥ=aC |
| 5.2.128 | VARIANTS | 0.857 | dvandva-upatāpa-garhyāt prāṇisthād iniḥ | dvaṃdva=upa-tāp-a-garh-y-āt prāṇi-th-āt ini-ḥ |
| 5.2.129 | VARIANTS | 0.863 | vāta-atisārābhyāṃ kuk ca | vāta=atī-sār-ā-bhyām kuK ca |
| 5.2.130 | AGREES | 0.903 | vayasi pūraṇāt | vayas-i pūr-aṇ-āt |
| 5.2.131 | AGREES | 0.914 | sukha-ādibhyaś ca | sukha=ādi-bhyas=ca |
| 5.2.132 | VARIANTS | 0.857 | dharma-śīla-varṇāntāc ca | dharma-śīla-varṇa=nt-āt=a |
| 5.2.133 | VARIANTS | 0.846 | hastāj jātau | hast-āt=jāt-au |
| 5.2.134 | VARIANTS | 0.810 | varṇād brāhmacāriṇi | varṇ-āt=brahma-cār-iṇ-i |
| 5.2.135 | VARIANTS | 0.884 | puṣkara-ādibhyo deśe | puṣkara=ādi=bhyaḥ=deś-e |
| 5.2.136 | VARIANTS | 0.787 | balādibhyo matub anyatarasyām | bala=ādi-bhyaḥ matUP=nya-ara-yām |
| 5.2.137 | VARIANTS | 0.818 | sañjñāyāṃ man-mābhyām | saṃjñā-y-ām man-mā-hyām |
| 5.2.138 | AGREES | 0.909 | kaṃ-śaṃbhyāṃ ba-bha-yus-ti-tu-ta-yasaḥ | kam=śam=hyāṃ ba-bha-yuS=ti-tu-ta-yaS-aḥ |
| 5.2.139 | AGREES | 0.909 | tundi-bali-vaṭer bhaḥ | tundi-vali-vaṭe-r bha-ḥ |
| 5.2.140 | VARIANTS | 0.857 | ahaṃ-śubhamor yus | aham=subham-or yuS |
| 5.3.1 | VARIANTS | 0.791 | prāg-diśo vibhaktiḥ | prāk=diś-aḥ=vi-bhak-ti-ḥ |
| 5.3.2 | MISSING | - | kiṃ-sarvanāma-bahubhyo 'dvy-ādibhyaḥ | - |
| 5.3.3 | VARIANTS | 0.824 | idam iś | idam-aḥ=iŚ |
| 5.3.4 | AGREES | 0.941 | eta-itau ra-thoḥ | eta=it-au ra-th-oḥ |
| 5.3.5 | CONFLICTS | 0.556 | etado 'ś | etad-aḥ=an |
| 5.3.6 | VARIANTS | 0.800 | sarvasya so 'nyatarasyāṃ di | sarva-sya sa-ḥ=anya-tara-syām d-i |
| 5.3.7 | AGREES | 0.968 | pañcamyās tasil | pañcamy-ās=tasiL |
| 5.3.8 | VARIANTS | 0.824 | taseś ca | tase-s=ca |
| 5.3.9 | VARIANTS | 0.788 | pary-abhibhyāṃ ca | pari=abhi-hyām=a |
| 5.3.10 | AGREES | 0.966 | saptamyās tral | saptamy-ās=traL |
| 5.3.11 | VARIANTS | 0.762 | idamo haḥ | idam-aḥ=ha-ḥ |
| 5.3.12 | VARIANTS | 0.625 | kimo 't | kim-aḥ=aT |
| 5.3.13 | AGREES | 0.944 | vā ha ca cchandasi | vā ha ca=chandas-i |
| 5.3.14 | VARIANTS | 0.816 | itarābhhyo 'pi dṛśyante | itarā-bhyaḥ=api dṛś-y-ante |
| 5.3.15 | AGREES | 0.919 | sarva-eka-anya-kiṃ-yat-tadaḥ kāle dā | sarva=eka=anya=kim-yad=tad-aḥ kāl-e dā |
| 5.3.16 | VARIANTS | 0.818 | idamo rhil | idam-aḥ=rhiL |
| 5.3.17 | AGREES | 1.000 | adhunā | adhunā |
| 5.3.18 | VARIANTS | 0.875 | dānīṃ ca | dānīm ca |
| 5.3.19 | VARIANTS | 0.818 | tado dā ca | tad-aḥ=dā ca |
| 5.3.20 | AGREES | 0.964 | tayor dā-rhilau ca chandasi | tayor dā-rhiL-au ca=chandas-i |
| 5.3.21 | AGREES | 0.918 | anadyatane rhil anyatarasyām | an-adya-tan-e rhiL anya-tara-syām |
| 5.3.22 | VARIANTS | 0.849 | sadyaḥ parut parāry-auṣamaḥ paredyavy-adya-pūrvedyur-anyedyur-anyataredyur-itaredyur-aparedyur-adharedyur-ubhayedyur-uttaredyuḥ | sadyas=parut-parāri-aiṣamas=pare-dyav-i=adya=pūrve-dyus=anye-dyus=anya-tar-e-dyus=itar-e-dyus=apar-e-dyus=adhar-e-dyus=ubhay-e-dyus=uttar-e-dyuḥ |
| 5.3.23 | VARIANTS | 0.878 | prakāravacane thāl | pra-kār-a-vac-an-e thāL |
| 5.3.24 | AGREES | 0.929 | idamas thamuḥ | idam-as thamu-ḥ |
| 5.3.25 | VARIANTS | 0.824 | kimaś ca | kim-as=ca |
| 5.3.26 | AGREES | 0.933 | thā hetau ca cchandasi | thā het-au ca=chandas-i |
| 5.3.27 | AGREES | 0.900 | dik-śabdebhyaḥ saptamī-pañcamī-prathamābhyo dig-deśa-kāleṣv astātiḥ | dik=śabde-bhyaḥ sapta-mī-pañca-mī-prathamā-hyaḥ=diś-deśa-kāle-ṣu=astāti-ḥ |
| 5.3.28 | AGREES | 0.943 | dikṣiṇa-uttarābhyām atasuc | dakṣiṇa=uttarā-bhyām atasuC |
| 5.3.29 | AGREES | 0.957 | vibhāṣā para-avarābhyām | vibhāṣā para=avarā-bhyā |
| 5.3.30 | AGREES | 0.947 | añcer luk | añce-r luK |
| 5.3.31 | AGREES | 0.933 | upary-upariṣṭāt | upari=upariṣṭāt |
| 5.3.32 | AGREES | 1.000 | paścāt | paścāt |
| 5.3.33 | AGREES | 0.979 | paśca paścā ca chandasi | paśca-paścā ca=chandas-i |
| 5.3.34 | AGREES | 0.929 | uttara-adhara-dakṣiṇād ātiḥ | uttara=adhara=dakṣiṇ-āt=āti-ḥ |
| 5.3.35 | VARIANTS | 0.861 | enav anyatarasyām adūre 'pañcamyāḥ | enaP=anya-tara-syām a-dūre=a-añcamy-āḥ |
| 5.3.36 | VARIANTS | 0.870 | dakṣiṇād āc | dakṣiṇ-āt āC |
| 5.3.37 | AGREES | 0.957 | āhi ca dūre | āhi ca dūr-e |
| 5.3.38 | VARIANTS | 0.857 | uttarāc ca | uttar-āt=ca |
| 5.3.39 | AGREES | 0.907 | pūrva-adhara-avarānām asi pur-adḥ-avaś ca+eṣām | pūrva=adhara=av arā-n-ām asi pur=adh=av-as=ca=e-ṣām |
| 5.3.40 | AGREES | 0.947 | astāti ca | astāt-i ca |
| 5.3.41 | AGREES | 0.909 | vibhāṣā 'varasya | vibhāṣā=avara-sya |
| 5.3.42 | VARIANTS | 0.846 | saṅkhyāyā vidhārthe dhā | saṃkhyā-y-āḥ=-vidhā=arth-e dhā |
| 5.3.43 | VARIANTS | 0.884 | adhikaraṇavicāle ca | adhi-kar-aṇa-vi-cāl-e ca |
| 5.3.44 | VARIANTS | 0.780 | ekād dho dyamuñ anyatarasyām | ek-āt=dh-aḥ=dhyamuÑ=nya-ara-yām |
| 5.3.45 | AGREES | 0.923 | dvi-tryoś ca dhamuñ | dvi-try-os=ca dhamuÑ |
| 5.3.46 | AGREES | 1.000 | edhāc ca | edhāC ca |
| 5.3.47 | AGREES | 0.917 | yāpye pāśap | yāp-y-e pāśaP |
| 5.3.48 | VARIANTS | 0.870 | pūraṇād bhāge tīyād an | pūraṇāt=bhāg-e tīy-āt=aN |
| 5.3.49 | VARIANTS | 0.814 | prāg ekādaśabhyo 'cchandasi | prāk=ekā-daśa-bhyaḥ=a-cchandas-i |
| 5.3.50 | VARIANTS | 0.875 | ṣaṣṭha-aṣṭamābhyāṃ ña ca | ṣaṣṭha=aṣṭa-ā-hyām Ña ca |
| 5.3.51 | VARIANTS | 0.774 | māna-paśv-aṅgayoḥ kan-lukau ca | māna-paśu=ṛge-hyaḥ kaN-luK-au ca |
| 5.3.52 | VARIANTS | 0.894 | ekād ākinic ca asahāye | ek-āt=ākiniC ca=a-sahāy-e |
| 5.3.53 | AGREES | 0.914 | bhūtapūrve caraṭ | bhū-ta-pūrv-e caraṬ |
| 5.3.54 | AGREES | 0.970 | ṣaṣṭhyā rūpya ca | ṣaṣṭhy-ā rūpya ca |
| 5.3.55 | VARIANTS | 0.863 | atiśāyane tamabiṣṭhanau | ati-śāy-an-e tamaP=iṣṭhaN-au |
| 5.3.56 | VARIANTS | 0.824 | tiṅaś ca | tiṄ-as=ca |
| 5.3.57 | VARIANTS | 0.886 | dvivacana-vibhajya-upapade tarab-īyasunau | dvi-vac-ana-vi-bhaj-ya=pa-pad-e taraP=īyasuN-au |
| 5.3.58 | VARIANTS | 0.766 | ajādi guṇavacanād eva | aC=ād-ī guṇa-vac-an-āt=eva |
| 5.3.59 | VARIANTS | 0.846 | tuś chandasi | tu-s=chandas-i |
| 5.3.60 | VARIANTS | 0.889 | praśasyasya śraḥ | pra-śas-ya-sya śra-ḥ |
| 5.3.61 | AGREES | 1.000 | jya ca | jya ca |
| 5.3.62 | AGREES | 0.960 | vṛddhasya ca | vṛddha-sya ca |
| 5.3.63 | AGREES | 0.964 | antika-bāḍhayor neda-sādhau | antika-bāḍhay-or neda-sādh-au |
| 5.3.64 | MISSING | - | yuva-alpayoḥ kan anyatarasyām | - |
| 5.3.65 | AGREES | 1.000 | vin-mator luk | vin-matOr luK |
| 5.3.66 | VARIANTS | 0.842 | praśaṃsāyāṃ rūpap | pra-śaṃs-ā-y-ām rūpaP |
| 5.3.67 | VARIANTS | 0.897 | īṣadasamāptau kalpab-deśya-deśīyaraḥ | īṣad-a-sam-āp-t-au kalpaP-deśya-deśīyaR-aḥ |
| 5.3.68 | VARIANTS | 0.889 | vibhāṣā supo bahuc parastāt tu | vibhāṣā sUP-aḥ=bahuC pur-astāt tu |
| 5.3.69 | VARIANTS | 0.894 | prakāravacane jātīyar | pra-kār-a-vac-an-e jātīyaR |
| 5.3.70 | VARIANTS | 0.857 | prāg-ivāt kaḥ | prāk=iv-āt ka-ḥ |
| 5.3.71 | AGREES | 0.955 | avyaya-sarvanāmnām akac prāk ṭeḥ | avyaya-sarva-nāmn-ām akaC prāk ṬE-ḥ |
| 5.3.72 | AGREES | 0.923 | kasya ca daḥ | ka-sya ca da-ḥ |
| 5.3.73 | VARIANTS | 0.667 | ajñāte | a-jña-t-e |
| 5.3.74 | VARIANTS | 0.824 | kutsite | kuts-i-t-e |
| 5.3.75 | VARIANTS | 0.857 | sañjñāyāṃ kan | saṃjñā-y-āṃ kaN |
| 5.3.76 | VARIANTS | 0.800 | anuampāyām | anu-kamp-ā-y-ām |
| 5.3.77 | VARIANTS | 0.878 | nītau ca tadyuktāt | nī-t-au ca tad-yuk-t-āt |
| 5.3.78 | VARIANTS | 0.794 | bahvaco manusyanāmnaṣ ṭhaj vā | bahv-aC-aḥ manuṣya-nāmn=aḥ ṭhaC=vā |
| 5.3.79 | AGREES | 0.966 | ghan-ilacau ca | ghaN-ilaC-au ca |
| 5.3.80 | VARIANTS | 0.881 | prācām upāder aḍaj-vucau ca | prāc-ām upa=āde-r aḍaC=vuC-au ca |
| 5.3.81 | AGREES | 0.933 | jātināmnaḥ kan | jāti-nāmn-aḥ kaN |
| 5.3.82 | VARIANTS | 0.825 | ajināntasya+uttarapadalopaś ca | ajina=anta-sya=uttara-ada-opas=ca |
| 5.3.83 | VARIANTS | 0.754 | ṭha-aj-ādāv ūrdhvaṃ dvitīyād acaḥ | ṭha=aC=ād-au=ūrdhva-ṃ dvi-īy-āt=C-aḥ |
| 5.3.84 | AGREES | 0.913 | śevala-supari-viśālā-varuṇa-aryama-ādināṃ tṛtīyāt | śevala-supari-viśāla-varuṇa-aryaman=ādī-n-āṃ tṛ-tīy-āt |
| 5.3.85 | VARIANTS | 0.889 | alpe | alp-e |
| 5.3.86 | AGREES | 0.923 | hrasve | hrasv-e |
| 5.3.87 | VARIANTS | 0.786 | sañjñāyāṃ kan | saṃjñā-y-ām kaN |
| 5.3.88 | VARIANTS | 0.875 | kuṭī-śamī-śuṇḍābhyo raḥ | kuṭī-śamī-śuṇḍā-hyaḥ ra-ḥ |
| 5.3.89 | AGREES | 0.917 | kutvā ḍupac | kutv-āḥ ḌupaC |
| 5.3.90 | AGREES | 0.977 | kāsū-goṇībhyāṃ ṣṭarac | kāsū-goṇī-bhyāṃ ṢṭaraC |
| 5.3.91 | MISSING | - | vatsa-ukṣa-aśva-rṣabhebhyaś ca tanutve | - |
| 5.3.92 | VARIANTS | 0.854 | kiṃ-yat-tado nirdhāraṇe dvayor ekasya ḍatarac | kim=yad-tad-aḥ nir-hār-aṇ-e dvay-or eka-sya ḌataraC |
| 5.3.93 | AGREES | 0.901 | vā bahūnāṃ jātiparipraśno ḍatamac | vā bahū-n-āṃ jāti-pari-praśn-e ḌatamaC |
| 5.3.94 | VARIANTS | 0.867 | ekāc ca prācām | ek-āt=ca prāc-ām |
| 5.3.95 | AGREES | 0.903 | avakṣepaṇe kan | ava-kṣep-aṇ-e kaN |
| 5.3.96 | VARIANTS | 0.875 | ive pratikṛtau | iv-e prati-kṛ-t-au |
| 5.3.97 | VARIANTS | 0.846 | sañjñāyāṃ ca | saṃjñā-y-āṃ ca |
| 5.3.98 | VARIANTS | 0.783 | lum-manusye | lup=manuṣy-e |
| 5.3.99 | VARIANTS | 0.773 | jīvikārthe cāpaṇye | jīvikā=arth-e ca-a-paṇ-y-e |
| 5.3.100 | VARIANTS | 0.857 | devapathādibhyaś ca | deva-patha=ādi-bhyas=ca |
| 5.3.101 | VARIANTS | 0.870 | vaster dhañ | vaste-r ḍhaÑ |
| 5.3.102 | VARIANTS | 0.846 | śilāyā ḍhaḥ | śilā-y-āḥ ḍha-ḥ |
| 5.3.103 | VARIANTS | 0.824 | śākhādibhyo yat | śākhā=ādi-bhyaḥ yaT |
| 5.3.104 | VARIANTS | 0.895 | dravyaṃ ca bhavye | drav-ya-ṃ ca bhav-y-e |
| 5.3.105 | VARIANTS | 0.667 | kuśāgrāc chaḥ | kuśa=agr-at=cha-ḥ |
| 5.3.106 | VARIANTS | 0.851 | samāsāc ca tadviṣayāt | sam=ās=āt=ca tad-vi-ṣay-āt |
| 5.3.107 | VARIANTS | 0.842 | śarkarā-ādibhyo 'ṇ | śarkarā=ādi-bhyaḥ=aṆ |
| 5.3.108 | VARIANTS | 0.800 | aṅgulyādibhyaṣ ṭhak | aṛguli=ādi-bhyas=ṭhaK |
| 5.3.109 | VARIANTS | 0.852 | ekaśālāyāṣ ṭhaj anyatarasyām | eka-śālā-yā-s=ṭhaC=anya-tara-syām |
| 5.3.110 | AGREES | 0.919 | karka-lohitād īkak | karka-lohit-āt=īkaK |
| 5.3.111 | AGREES | 0.974 | pratna-pūrva-viśva-imāt thāl chandasi | pratna-pūrva-viśva-im-āt thāL chandas-i |
| 5.3.112 | VARIANTS | 0.778 | pūgāñ ñyo 'grāmaṇīpūrvāt | pūg-āt=Ñya-ḥ=a-grāmaṇī-pūrv-āt |
| 5.3.113 | AGREES | 0.913 | vrāta-cphañor astriyām | vrāta-CphaÑ-r a-striy-ām |
| 5.3.114 | VARIANTS | 0.811 | āyudha-jīvisaṅkghāññyaḍ-vāhīkeṣv abrāhmaṇa-rājanyāt | ā-yudh-a=jīv-i-saṃ-gh-āt-ÑyaṬ=āhīke-ṣu a-brāhmaṇa-rājan-y-āt |
| 5.3.115 | VARIANTS | 0.880 | vṛkāṭ ṭeṇyaṇ | vṛk-āt=ṬeṇyaṆ |
| 5.3.116 | VARIANTS | 0.806 | dāmanyādi-trigartaṣṭhāc chaḥ | dāmani=ādi-tri-garta-ṣaṣṭh-āt=ha-ḥ |
| 5.3.117 | VARIANTS | 0.882 | parśvādi-yaudheyādibhyām aṇ-añau | parśu=ādi-yaudheya=ādi-hyām aṆ=aÑ-au |
| 5.3.118 | VARIANTS | 0.732 | abhijid-vidabhṛc-chālāvac-chikhāvac-chamīvad-ūrṇāvac-charumad-aṇo yañ | abhi-jit=vida-bhṛt-śālā-vat=śikhā-vat=śamī-vat=ūrṇā-vat=śru-mat=aṆ-aḥ yaÑ |
| 5.3.119 | VARIANTS | 0.872 | ñyādayas tadrājāḥ | Ñya-āday-as tad-rājā-ḥ |
| 5.4.1 | VARIANTS | 0.854 | pādaśatasya saṅkhyāder vīpsāyāṃ vun lopaś ca | pāda-śata-sya saṃkhyā=āde-r vīpsā-y-ām vuN lopa-s=ca |
| 5.4.2 | VARIANTS | 0.875 | daṇḍa-vyavasargayoś ca | daṇḍa-vy-ava-sarg-ay-os=ca |
| 5.4.3 | VARIANTS | 0.886 | sthūlādibhyaḥ prakāravacane kan | sthūla=ādi-bhyaḥ pra-kār-a-vac-an-e kaN |
| 5.4.4 | VARIANTS | 0.864 | anatyantagatau ktāt | an-aty-anta-ga-t-au Kt-āt |
| 5.4.5 | VARIANTS | 0.897 | na sāmivacane | na sāmi-vac-an-e |
| 5.4.6 | VARIANTS | 0.895 | bṛhatyā ācchādane | bṛhaty-ā ā-cchād-an-e |
| 5.4.7 | VARIANTS | 0.833 | aṣaḍakṣa-āśitaṅgv-alaṅkarma-alampuruṣa-adhyuttarapadāt khaḥ | a-ṣaḍ-aks-a=āś-i-ta-ṃ-gu=alaṃ-karman=alam-puruṣa=adhy-uttara-pad-āt kha-ḥ |
| 5.4.8 | VARIANTS | 0.889 | vibhāṣā-añcer adikṣtriyām | vibhāṣā=añce-r a-dik-striy-ām |
| 5.4.9 | VARIANTS | 0.833 | jātyantāc cha bandhuni | jāti=ant-āt=cha bandhu-n-i |
| 5.4.10 | VARIANTS | 0.886 | sthānāntād vibhāṣā sasthānena+iti cet | sthāna=ant-āt=vibhāṣā sa-sthān-ena=iti cet |
| 5.4.11 | VARIANTS | 0.814 | kim-et-tiṅ-avyaya-ghād-āṃv-adravyaprakarṣe | kim=eT=tiṄ=avyaya=GH-ĀT=āmu=a-ravya-ra-arṣ-e |
| 5.4.12 | AGREES | 0.938 | amu ca cchandasi | amu ca=chandas-i |
| 5.4.13 | VARIANTS | 0.848 | anugādinaṣ ṭhak | anu-gād-in-as=ṭhaK |
| 5.4.14 | VARIANTS | 0.882 | ṇacaḥ striyām añ | ṆaC-as striy-ām aÑ |
| 5.4.15 | AGREES | 0.947 | aṇ inuṇaḥ | aṆ inuṆ-aḥ |
| 5.4.16 | VARIANTS | 0.800 | visāriṇo matsye | vi-sār-iṇ-aḥ matsy-e |
| 5.4.17 | VARIANTS | 0.844 | saṅkyāyāḥ kriyā-abhyāvṛttigaṇane kṛtvasuc | saṃ-khyā-y-āḥ kriyā=bhy-ā-ṛt-ti-gaṇ-an-e kṛtvasuC |
| 5.4.18 | VARIANTS | 0.889 | dvi-tri-caturbhyaḥ suc | dvi-tri-catur-bhyām suC |
| 5.4.19 | AGREES | 0.903 | ekasya sakṛc ca | eka-sya sakṛt=ca |
| 5.4.20 | VARIANTS | 0.857 | vibhāṣā bahor dhā 'viprakrṣṭakāle | vibhāṣā baho-r dhā=-vi-pra-ṛṣ-ṭa-kāl-e |
| 5.4.21 | AGREES | 0.902 | tat prakṛtavacane mayaṭ | tat pra-kṛ-ta-vac-an-e mayaṬ |
| 5.4.22 | VARIANTS | 0.878 | samūhavac ca bahuṣu | sam-ūha-vat=ca bahu-ṣu |
| 5.4.23 | AGREES | 0.919 | ananta-āvasatha-itiha-bheṣajāñ ñyaḥ | an-anta=ā-vas-atha=itiha=bheṣaj-āt=Ñyaḥ |
| 5.4.24 | VARIANTS | 0.852 | devatāntāt tādarthye yat | devata=ant-āt tād-arth-y-e yaT |
| 5.4.25 | AGREES | 0.973 | pāda-arghābhyāṃ ca | pāda=arghā-bhyāṃ ca |
| 5.4.26 | AGREES | 0.923 | atither ñyaḥ | atithe-r Ñya-ḥ |
| 5.4.27 | AGREES | 0.947 | devāt tal | dev-āt taL |
| 5.4.28 | VARIANTS | 0.889 | aveḥ kaḥ | ave-ḥ ka-ḥ |
| 5.4.29 | AGREES | 0.909 | yāvādibhyaḥ kan | yāva=ādi-bhyaḥ kaN |
| 5.4.30 | VARIANTS | 0.857 | lohitān maṇau | lohit-āt=maṇ-au |
| 5.4.31 | AGREES | 0.909 | varṇe ca anitye | varṇ-e ca=a-nity-e |
| 5.4.32 | VARIANTS | 0.833 | rakte | rak-t-e |
| 5.4.33 | VARIANTS | 0.824 | kālāc ca | kāl-āt=ca |
| 5.4.34 | VARIANTS | 0.829 | vinayādibhyaṣ ṭhak | vi-nay-a=ādi-bhyas=ṭhaK |
| 5.4.35 | VARIANTS | 0.816 | vāco vyāhṛta-arthāyām | vāc-aḥ vy-ā-hṛ-ta=arthā-y-ām |
| 5.4.36 | VARIANTS | 0.800 | tadyuktāt karmaṇo 'ṇ | tad-yuk-t-āt karmaṇ-aḥ=aṆ |
| 5.4.37 | VARIANTS | 0.875 | oṣadher ajātau | oṣadhe-r a-jā-t-au |
| 5.4.38 | VARIANTS | 0.833 | prajñādibhyaś ca | pra-jña=ādi-bhyas=ca |
| 5.4.39 | AGREES | 0.957 | mṛdas tikan | mṛd-as tikaN |
| 5.4.40 | VARIANTS | 0.810 | sasnau praśaṃsāyāṃ | sa-sn-au pra-śaṃs-ā-y-ām |
| 5.4.41 | AGREES | 0.952 | vṛka-jyeṣṭhābhyāṃ til-tātilau ca chandasi | vṛka-jyeṣṭhā-hyāṃ tiL-tātiL-au ca=chandas-i |
| 5.4.42 | VARIANTS | 0.833 | bahv-alpa-arthāc chaskārakād anyatarasyām | bahu=alpa=arth-āt=śas kārak-ād anya-ara-yām |
| 5.4.43 | VARIANTS | 0.871 | saṅkhyā-ekavacanāc ca vīpsāyām | saṃkhyā=ekavacan-āt=a vīpsā-y-ām |
| 5.4.44 | AGREES | 0.926 | pratiyoge pañcamyās tasiḥ | prati-yog-e pañcamy-ās tasi-ḥ |
| 5.4.45 | VARIANTS | 0.857 | apādāne ca ahīya-ruhoḥ | apa=ā-dān-e ca=a-hīya-ruh-ḥ |
| 5.4.46 | VARIANTS | 0.871 | atigraha-avyathana-kṣepeṣv akartari tṛtīyāyāḥ | ati-grah-a=a-vyath-ana=kṣepe-ṣu a-kar-tar-i tṛ-tīyā-y-āḥ |
| 5.4.47 | VARIANTS | 0.851 | hīyamāna-pāpayogāc ca | hī-ya-m-āna-pāpa-yog-āt=ca |
| 5.4.48 | VARIANTS | 0.865 | ṣaṣṭhyā vyāśraye | ṣaṣ-ṭhy-ā vy-ā-śray-e |
| 5.4.49 | VARIANTS | 0.850 | rogāc ca apanayane | rog-āt=ca=apa-nay-an-e |
| 5.4.50 | VARIANTS | 0.723 | abhūtatadbhāve kṛ-bhv-astiyoge sampadyakartari cviḥ | kṛ=bhū=as-ti-yog-e sam-pad-ya-ar-tar-i Cviḥ |
| 5.4.51 | VARIANTS | 0.826 | arur-manaś-cakṣuś-ceto-raho-rajasāṃ lopaś ca | arus=manas=cakṣus=cetas=rahas=rajas-āṃ lopa-s=ca |
| 5.4.52 | AGREES | 0.933 | vibhāṣā sāti kārtsnye | vibhāṣā sāti kārt-sn-y-e |
| 5.4.53 | VARIANTS | 0.894 | abhividhau sampadā ca | abhi-vi-dh-au sam-pad-ā ca |
| 5.4.54 | VARIANTS | 0.857 | tadadhīnavacane | tad-adh-īna-vac-an-e |
| 5.4.55 | AGREES | 0.917 | deye trā ca | de-y-e trā ca |
| 5.4.56 | AGREES | 0.903 | deva-manuṣya-puruṣa-puru-martyebhyo dvitīyāsaptamyor bahulam | deva-manuṣya-puruṣa-puru-martye-hyaḥ dvi-tīy-ā-apta-y-or bahulam |
| 5.4.57 | VARIANTS | 0.707 | avyaktānukaraṇād dvyajavarārdhād anitau ḍāc | a-vy-ak-ta-anu-kar-aṇ-āt=vi-aC=vara=ardh-āt an-it-au ḌāC |
| 5.4.58 | AGREES | 0.900 | kṛño dvitīya-tṛtīya-śamba-bījāt kṛṣau | kṛñ-aḥ dvi-tīya-tṛ-tīya-śamba-bīj-āt kṛṣ-au |
| 5.4.59 | VARIANTS | 0.706 | saṅkhyāyāś ca guṇāntāyāḥ | saṃkhyā-y-aḥ guṇa=anta-y-āḥ |
| 5.4.60 | VARIANTS | 0.844 | samayāc ca yāpanāyām | sam-ay-āt=ca yāp-anā-y-ām |
| 5.4.61 | VARIANTS | 0.781 | sapatra-niṣpatrād ativyathane | sa-pat-tra-niṣ-pat-r-āt=ti-yath-n-e |
| 5.4.62 | VARIANTS | 0.829 | niṣkulān niṣkoṣaṇe | niṣ-kul-āt=niṣ-koṣ-aṇ-e |
| 5.4.63 | VARIANTS | 0.851 | sukha-priyād ānulomye | sukha-pri-y-āt ānu-lom-y-e |
| 5.4.64 | VARIANTS | 0.878 | duḥkhāt prātilomye | duḥ-kh-āt prāti-lom-y-e |
| 5.4.65 | AGREES | 0.909 | śūlāt pāke | śūl-āt pāk-e |
| 5.4.66 | VARIANTS | 0.800 | satyād aśapathe | sat-y-āt a-śap-ath-e |
| 5.4.67 | VARIANTS | 0.800 | madrāt parivāpaṇe | mad-r-āt pari-vā-p-an-e |
| 5.4.68 | VARIANTS | 0.750 | samāsāntāḥ | sam-āsa=ant-āḥ |
| 5.4.69 | AGREES | 0.909 | na pūjanāt | na pūj-an-āt |
| 5.4.70 | AGREES | 0.917 | kimaḥ kṣepe | kim-aḥ kṣep-e |
| 5.4.71 | AGREES | 0.941 | nañas tatpuruṣāt | naÑ-as tatpuruṣ-āt |
| 5.4.72 | VARIANTS | 0.857 | patho vibhāṣā | path-aḥ=vibhāṣā |
| 5.4.73 | VARIANTS | 0.868 | bahuvrīhau saṅkhyeye ḍaj abahu-gaṇāt | bahvrīh-au saṃkhy-ey-e ḌaC a-bahu-gaṇ-āt |
| 5.4.74 | VARIANTS | 0.721 | ṛk-pūr-ab-dhūḥ-pathām ānakṣe | ṛc=pur=ap=dhur-path-ām a=an-akṣ-e |
| 5.4.75 | MISSING | - | ac praty-anv-avapūrvāt sāma-lomnaḥ | - |
| 5.4.76 | VARIANTS | 0.743 | akṣṇo 'darśanāt | akṣṇ-aḥ=a-darś-an-āt |
| 5.4.77 | CONFLICTS | 0.123 | acatura-vicatura-sucatura-strīpuṃsa-dhenvanaḍuha-rkṣāma-vāṅmanasa-akṣibhruva-dāragava-ūrvaṣṭhīva-padaṣṭhīva-naktaṃdiva-rātriṃdiva-ahardiva-sarajasa-niḥśreyasa-puruṣāyuṣa-dvyāyuṣa-tryāyuṣa-rgyajuṣa-jātokṣa-mahokṣa-vṛddhokṣa-upaśuna-goṣṭhaśvāḥ | a-catur-a=vi-catur-a-su-catur-a-strī-uṃs-a-dhenv-naḍuh-a=ṛk-ām-a=vāṛ-anas-a=akṣibhruv-a=dāra-gav-a=ūrv-ṣṭhīv-a-pad-aṣṭhīv-a-nakta-ṃ-iv-a-ratri-ṃ-div-a=ahar-div-a-sa-rajas-a-niḥ-śreyas-a-puruṣāyus-a-dvy-āyuṣ-a-try-āyuṣ-a=ṛg-ajuṣ-a-jātokṣ-a-mahokṣ-a-vṛddhokṣ-a=upa-śun-a-goṣṭha-śv-āḥ |
| 5.4.78 | MISSING | - | brahmahastibhyāṃ varcasaḥ | - |
| 5.4.79 | AGREES | 0.943 | ava-sam-andhebhyas tamasaḥ | ava-sam-andhe-hyas tamas-aḥ |
| 5.4.80 | VARIANTS | 0.826 | śvaso vasīyaḥ-śreyasaḥ | śvas-aḥ vasīyas=śreyas-ḥ |
| 5.4.81 | VARIANTS | 0.851 | anv-ava-taptād rahasaḥ | anu=ava-tap-t-āt rahas-aḥ |
| 5.4.82 | VARIANTS | 0.897 | prater urasaḥ saptamīsthāt | prate-r ur-as-aḥ sapta-mī-sth-āt |
| 5.4.83 | VARIANTS | 0.848 | anugavam āyāme | anu-gav-a-m ā-yām-e |
| 5.4.84 | VARIANTS | 0.898 | dvistāvā tirstāvā vediḥ | dvi-stāvā tri-stāvā vedi-ḥ |
| 5.4.85 | VARIANTS | 0.872 | upasargād adhvanaḥ | upa-sarg-āt adhvan-aḥ |
| 5.4.86 | VARIANTS | 0.875 | tatpuruṣasya aṅguleḥ saṅkhyā-avyayādeḥ | tatpuruṣa-sya=ṛgule-ḥ saṃkhyā-avyaya-āde-ḥ |
| 5.4.87 | VARIANTS | 0.884 | ahaḥ-sarva-ekadeśa-saṅkhyāta-puṇyāc ca rātreḥ | ahan=sarva=eka-deśa-saṃ-khyā-ta-puṇy-āt=ca rātre-ḥ |
| 5.4.88 | VARIANTS | 0.780 | ahno 'hna etebhyaḥ | ahn-aḥ ahna-ḥ=ete-bhyaḥ |
| 5.4.89 | VARIANTS | 0.840 | na saṅkhyādeḥ samāhāre | na saṃkhyā=āde-ḥ sam-ā-hār-e |
| 5.4.90 | AGREES | 0.947 | uttama-ekābhyāṃ ca | ut-tama=ekā-bhyāṃ ca |
| 5.4.91 | MISSING | - | rāja-ahaḥ-sakhibhyaṣ ṭac | - |
| 5.4.92 | AGREES | 0.923 | gor ataddhita-luki | go-r a-taddhita-luK-i |
| 5.4.93 | AGREES | 0.909 | agra-ākhyāyām urasaḥ | agra=ā-khyā-y-ām uras-aḥ |
| 5.4.94 | MISSING | - | ano 'śma-ayas-sarasāṃ jāti-sañjñāyoḥ | - |
| 5.4.95 | AGREES | 0.945 | grāma-kauṭābhyāṃ ca takṣṇaḥ | grāma-kauṭā-hyāṃ ca takṣṇ-aḥ |
| 5.4.96 | VARIANTS | 0.870 | ateḥ śunaḥ | at-eḥ śuun-aḥ |
| 5.4.97 | VARIANTS | 0.769 | uapmānād aprāṇiṣu | upa-mā-n-āt a-prāṇi-ṣu |
| 5.4.98 | VARIANTS | 0.852 | uttaramṛgapūrvāc ca sakthnaḥ | ut-tara=mṛga-ūrv-āt=ca sakth-n-aḥ |
| 5.4.99 | VARIANTS | 0.800 | nāvo dvigoḥ | nāv-aḥ=dvigo-ḥ |
| 5.4.100 | VARIANTS | 0.842 | ardhāc ca | ardh-āt=ca |
| 5.4.101 | AGREES | 0.933 | khāryāḥ prācām | khāry-āḥ prāc-ām |
| 5.4.102 | AGREES | 0.927 | dvi-tribhyām añjaleḥ | dvi-tri-hyām añjale-ḥ |
| 5.4.103 | VARIANTS | 0.892 | an-as-antān napuṃsakāc chandasi | an-as-ant-āt napuṃsak-āt=chandas-i |
| 5.4.104 | VARIANTS | 0.836 | brahmaṇo jānapadākhyāyām | brahmaṇ-aḥ jāna-pada=ākhyā-y-ām |
| 5.4.105 | VARIANTS | 0.868 | ku-mahadbhyām anyatarasyām | ku-mahat=bhyām anya-ara-yām |
| 5.4.106 | VARIANTS | 0.849 | dvandvāc cu-da-ṣa-ha-antāt samāhāre | dvaṃdv-āt cU-da-ṣa=ha-nt-āt sam-ā-ār-e |
| 5.4.107 | AGREES | 0.906 | avyayībhāve śarat-prabhṛtibhyaḥ | avyayībhāv-e śarad=ra-bhṛti-bhyaḥ |
| 5.4.108 | VARIANTS | 0.800 | anaś ca | an-as=ca |
| 5.4.109 | VARIANTS | 0.875 | napuṃsakād anyatarasyām | napuṃsak-āt=any-tara-syām |
| 5.4.110 | VARIANTS | 0.875 | nadī paurṇamāsy-āgrahāyaṇībhyaḥ | nadī-paurṇa-māsī-āgra-āy-aṇī-hyaḥ |
| 5.4.111 | VARIANTS | 0.769 | jñayaḥ | jhaY-aḥ |
| 5.4.112 | CONFLICTS | 0.500 | gireś ca | gire-s=ca senaka-sya |
| 5.4.113 | VARIANTS | 0.868 | bahuvrīhau sakthy-akṣṇoḥ svāṅgāt ṣac | bahuvrīh-au sakthi=akṣṇo-ḥ sva=ṛg-āt ṢaC |
| 5.4.114 | VARIANTS | 0.839 | aṅguler dāruṇi | aṛgule-r dāru-ṇ-i |
| 5.4.115 | AGREES | 0.960 | dvi-tribhyāṃ ṣa mūrdhnaḥ | dvi-tri-bhyāṃ Ṣa mūrdhn-aḥ |
| 5.4.116 | AGREES | 0.905 | ap pūraṇī-pramāṇyoḥ | aP pūr-aṇ-ī-pra-māṇy-oḥ |
| 5.4.117 | AGREES | 0.963 | antar-bahirbhyāṃ ca lomnaḥ | antar-bahir-bhyāṃ ca lomn-aḥ |
| 5.4.118 | VARIANTS | 0.828 | añ nāsikāyāḥ sañjñāyāṃ nasaṃ ca asthūlāt | aC=nāsikā-y-āḥ saṃjñā-y-āṃ nas-aṃ ca a-sthū-l-e |
| 5.4.119 | VARIANTS | 0.846 | upasargāc ca | upa-sarg-āt=ca |
| 5.4.120 | VARIANTS | 0.855 | suprāta-suśva-sudiva-śārikukṣa-caturaśra-eṇīpadājapada-proṣṭhapadāḥ | su-prāt-a-su-śv-a-su-div-a-śāri-kukṣ-a-catur-aśr-a=eṇī-pad-a=aja-pad-a-proṣṭha-ad-ā-ḥ |
| 5.4.121 | VARIANTS | 0.819 | nañ-duḥ-subhyo hali-sakthyor anyārasyām | naÑ-dus-su-hyaḥ hali-sakthy-or anya-tara-yām |
| 5.4.122 | AGREES | 0.963 | nityam asic prajā-medhayoḥ | nitya-m asiC prajā-medhay-oḥ |
| 5.4.123 | VARIANTS | 0.878 | bahuprajāśc chandasi | bahu-prajās=chandas-i |
| 5.4.124 | AGREES | 0.905 | dharmād anic kevalāt | dharm-āt=aniC keval-āt |
| 5.4.125 | VARIANTS | 0.885 | jambhā suharitatṛṇasomebhyaḥ | jambhā su-har-i-ta-tṛṇa-some-hyaḥ |
| 5.4.126 | AGREES | 0.913 | dakṣiṇer mā lubdhayoge | dakṣiṇermā lub-dha-yog-e |
| 5.4.127 | VARIANTS | 0.895 | ic karmavyatihāre | iC karma-vy-ati-hār-e |
| 5.4.128 | VARIANTS | 0.810 | dvidaṇḍyādibhyaś ca | dvi-daṇḍ-i=ādi-bhyas=ca |
| 5.4.129 | VARIANTS | 0.889 | pra-saṃbhyāṃ jānunor jñuḥ | pra-sam-bhyāṃ jānu-n-or jñu-ḥ |
| 5.4.130 | AGREES | 0.903 | ūrdhvād vibhāṣā | ūrdhv-āt vibhāṣā |
| 5.4.131 | VARIANTS | 0.750 | ūdhaso 'naṅ | ūdhas-aḥ=anaṄ |
| 5.4.132 | VARIANTS | 0.870 | dhanuṣaś ca | dhanuṣ-as=ca |
| 5.4.133 | VARIANTS | 0.846 | vā sañjñāyām | vā saṃjñā-y-ām |
| 5.4.134 | VARIANTS | 0.870 | jāyāyā niṅ | jāyā-y-āḥ niṄ |
| 5.4.135 | AGREES | 0.904 | gandhasya+id ut-pūti-su-surabhibhyaḥ | gandha-sya iT ud=pūti-su-surabhi-hyaḥ |
| 5.4.136 | VARIANTS | 0.897 | alpa-ākhyāyām | alpa=ā-khyā-y-ām |
| 5.4.137 | VARIANTS | 0.833 | upamānāc ca | upa-mān-āt=ca |
| 5.4.138 | MISSING | - | pādasya lopo 'hastyādibhyaḥ | - |
| 5.4.139 | AGREES | 0.909 | kumbhapadīṣu ca | kumbha-pad-ī-ṣu ca |
| 5.4.140 | VARIANTS | 0.872 | saṅkhyā-supūrvasya | saṃ-khyā-su-pūrva-sya |
| 5.4.141 | AGREES | 0.952 | vayasi dantasya datṛ | vayas-i danta-sya datṚ |
| 5.4.142 | AGREES | 0.957 | chandasi ca | chandas-i ca |
| 5.4.143 | VARIANTS | 0.865 | striyāṃ sañjñāyām | striy-āṃ saṃjñā-y-ām |
| 5.4.144 | AGREES | 0.980 | vibhāṣā śyāva-arokābhyām | vibhāṣā śyāva=arokā-bhyām |
| 5.4.145 | VARIANTS | 0.892 | agrānta-śuddha-śubhra-vṛṣa-varāhebhyaś ca | agra=anta-śuddha-śubhra-vṛṣa-varāhe-hyas=a |
| 5.4.146 | AGREES | 0.912 | kakudasya avasthāyāṃ lopaḥ | kakuda-sya=ava-sthā-y-āṃ lopa-ḥ |
| 5.4.147 | VARIANTS | 0.882 | trikakut parvate | tri-kakud=parvat-e |
| 5.4.148 | AGREES | 0.905 | ud-vibhyāṃ kākudasya | ud=vi-bhyām kākuda-sya |
| 5.4.149 | VARIANTS | 0.897 | pūrṇād vibhāṣā | pūrṇ-āt vibhāṣā |
| 5.4.150 | AGREES | 0.923 | suhṛd-durhṛdau mitra-amitrayoḥ | su-hṛd=dur-hṛd-au mitra=a-mitray-oḥ |
| 5.4.151 | VARIANTS | 0.870 | uraḥprabhṛtibhyaḥ kap | uras=pra-bhṛ-ti-bhyaḥ kaP |
| 5.4.152 | AGREES | 0.923 | inaḥ striyām | in-aḥ striy-ām |
| 5.4.153 | VARIANTS | 0.800 | nady-ṛtaś ca | nadī=ṛT-as=ca |
| 5.4.154 | VARIANTS | 0.889 | śeṣād vibhāṣā | śeṣ-āt vibhāṣā |
| 5.4.155 | VARIANTS | 0.846 | na sañjñāyām | na saṃjñā-y-ām |
| 5.4.156 | VARIANTS | 0.842 | īyasaś ca | īyas-as=ca |
| 5.4.157 | VARIANTS | 0.882 | vandite bhrātuḥ | vand-i-t-e bhrātu-ḥ |
| 5.4.158 | VARIANTS | 0.857 | ṛtaś chandasi | ṛT-as=chandas-i |
| 5.4.159 | VARIANTS | 0.818 | nāḍī-tantryoḥ svāṅge | nāḍī-tantry-oḥ sva=aṛg-e |
| 5.4.160 | VARIANTS | 0.839 | niṣpravāṇiś ca | niṣ-pra-vāṇi-s=ca |
| 6.1.1 | VARIANTS | 0.880 | eka-aco dve prathamasya | eka=aC-aḥ=dv-e prathama-sya |
| 6.1.2 | VARIANTS | 0.842 | ajāder dvitīyasya | aC=āde-r dvi-tīya-sya |
| 6.1.3 | VARIANTS | 0.840 | na ndrāḥ saṃyogādayaḥ | na=n-d-r-āḥ saṃ-yog-a=āday-aḥ |
| 6.1.4 | VARIANTS | 0.727 | pūrvo 'bhyāsaḥ | pūrva-ḥ abhy-ās-a-ḥ |
| 6.1.5 | VARIANTS | 0.875 | ubhe abhyastam | ubh-e abhy-as-ta-m |
| 6.1.6 | VARIANTS | 0.872 | jakṣity-ādayaḥ ṣaṭ | jakṣ-i-ti=āday-aḥ ṣaṭ |
| 6.1.7 | VARIANTS | 0.820 | tujādīnāṃ dīrgho 'bhyāsasya | tuj-ādī-nāṃ dīrgha-ḥ=abhy-ās-a-sya |
| 6.1.8 | AGREES | 0.906 | liṭi dhātor anabhyāsasya | lIṬ-i dhātor an-abhy-ās-a-sya |
| 6.1.9 | AGREES | 0.947 | san-yaṅoḥ | saN-yaṄ-oḥ |
| 6.1.10 | VARIANTS | 0.889 | ślau | Śl-au |
| 6.1.11 | VARIANTS | 0.889 | caṅi | CaṄ-i |
| 6.1.12 | VARIANTS | 0.863 | dāśvān sāhvān mīḍvāṃś ca | dāś-vān sāh-vān mīḍh-vān=ca |
| 6.1.13 | AGREES | 0.903 | ṣyaṅaḥ samprasāraṇaṃ putra-patyos tatpuruṣe | ṢyaṄ-aḥ sam-pra-sār-aṇa-m putra-paty-os tatpuruṣ-e |
| 6.1.14 | AGREES | 0.927 | bandhuni bahuvrīhau | bandhu-n-i bahuvrīh-au |
| 6.1.15 | VARIANTS | 0.857 | vaci-svapi-yajādīnāṃ kiti | vaci-svapi-yajA=ādi-n-āṃ K-IT-i |
| 6.1.16 | VARIANTS | 0.890 | grahi-jyā-vayi-vyadhi-vaṣṭi-vicati-vṛścati-pṛcchati-bhṛjjatīnāṃ ṅiti ca | grahi-jyā-vayi-vyadhi-vaṣ-ṭi-vic-a-ti-vṛśc-a-ti-pṛchh-a-ti-bhṛjj-a-tī-n-ām Ṅ-IT-i ca |
| 6.1.17 | VARIANTS | 0.873 | liṭy abhyāsasya+ubhayeṣām | lIṬ-i=abhy-ās-a-sya=ubhaye-ṣām |
| 6.1.18 | VARIANTS | 0.800 | svāpeś caṅi | svāp-e-s=CaṄ-i |
| 6.1.19 | AGREES | 0.917 | svapi-syami-vyeñāṃ yaṅi | svapi-syami-vyeÑ-ām yaṄ-i |
| 6.1.20 | AGREES | 0.941 | na vaśaḥ | na vaś-aḥ |
| 6.1.21 | AGREES | 0.941 | cāyaḥ kī | cāy-aḥ kī |
| 6.1.22 | AGREES | 0.917 | sphāyaḥ sphī niṣṭhāyām | sphsāy-aḥ sphī niṣṭhā-y-ām |
| 6.1.23 | AGREES | 0.919 | styaḥ prapūrvasya | sty-aḥ pra-pūrva-sya |
| 6.1.24 | AGREES | 0.943 | dravamūrti-sparśayoḥ śyaḥ | drava-mūrti-sparśay-oḥ śy-aḥ |
| 6.1.25 | VARIANTS | 0.889 | prateś ca | prates=ca |
| 6.1.26 | AGREES | 0.902 | vibhāṣā 'bhy-ava-pūrvasya | vibhāṣā abhi=ava-pūrva-sya |
| 6.1.27 | VARIANTS | 0.783 | śṛtaṃ pāke | śṛ-ta-m pāk-e |
| 6.1.28 | AGREES | 0.947 | pyāyaḥ pī | pyāy-aḥ pī |
| 6.1.29 | VARIANTS | 0.800 | liḍ-yaṅoś ca | lIṬ=yaṄ-os=ca |
| 6.1.30 | AGREES | 0.960 | vibhāṣā śveḥ | vibhāṣā śve-ḥ |
| 6.1.31 | VARIANTS | 0.857 | ṇau ca saṃś-caṅoḥ | Ṇ-au ca saN=CaṄ-oḥ |
| 6.1.32 | AGREES | 0.919 | hvaḥ saṃprasāraṇam | hv-aḥ samprasāraṇam |
| 6.1.33 | AGREES | 0.903 | abhyastasya ca | abhy-as-ta-sya ca |
| 6.1.34 | VARIANTS | 0.882 | bahulaṃ chandasi | bahula-m chandas-i |
| 6.1.35 | AGREES | 0.941 | cāyaḥ kī | cāy-aḥ kī |
| 6.1.36 | VARIANTS | 0.830 | apaspṛdhethām-ānṛcur-ānṛhuś-cicyuṣetityāja-śrātāḥ śritam-āśīrāśīrtāḥ | apa-spṛdh-e-thām=ān-ṛc-us=ān-ṛh-us-ci-cyu-ṣe-ti-tyāj-a-śrātā-ḥ-śri-tam=āśīr-taḥ |
| 6.1.37 | VARIANTS | 0.879 | na samprasāraṇe samprasāraṇam | na sam-pra-sār-aṇ-e sam-pra-sār-aṇa-m |
| 6.1.38 | VARIANTS | 0.857 | liṭi vyo yaḥ | lIṬ-i vay-o y-aḥ |
| 6.1.39 | VARIANTS | 0.844 | vaś ca asya anyatarasyāṃ kiti | va-s=ca=a-sya=anya-tara-syām K-IT-i |
| 6.1.40 | AGREES | 0.909 | veñaḥ | veÑ-aḥ |
| 6.1.41 | AGREES | 0.941 | lyapi ca | LyaP-i ca |
| 6.1.42 | VARIANTS | 0.800 | jyaś ca | jy-as=ca |
| 6.1.43 | VARIANTS | 0.800 | vyaś ca | vy-as=ca |
| 6.1.44 | AGREES | 0.963 | vibhāṣā pareḥ | vibhāṣā pare-ḥ |
| 6.1.45 | VARIANTS | 0.783 | ād eca upadeśe 'śiti | āT=eC-aḥ=upa-deś-e=aŚ-IT-i |
| 6.1.46 | VARIANTS | 0.800 | na vyo liṭi | na vy-aḥ=lIṬ-i |
| 6.1.47 | VARIANTS | 0.893 | sphurati-sphulatyor ghañi | sphur-a-ti-sphul-a-ty-or GHaÑ-i |
| 6.1.48 | VARIANTS | 0.857 | krī-iṅ-jīnāṃ ṇau | krī-iṄ-jī-n-ām Ṇ-au |
| 6.1.49 | VARIANTS | 0.880 | sidhyater apāralaukike | sidh-ya-te-r a-pāra-laukik-e |
| 6.1.50 | AGREES | 0.903 | mīnāti-minoti-dīṅāṃ lyapi ca | mī-nā-ti-mi-no-ti-dīṄ-āṃ LyaP-i ca |
| 6.1.51 | AGREES | 0.909 | vibhāṣā līyateḥ | vibhāṣā lī-ya-te-ḥ |
| 6.1.52 | VARIANTS | 0.875 | khideś chandasi | khide-s=chandas-i |
| 6.1.53 | AGREES | 0.903 | apaguro ṇamuli | apa-gur-o ṆamuL-i |
| 6.1.54 | AGREES | 0.933 | ci-sphuror ṇau | ci-sphur-or Ṇ-au |
| 6.1.55 | VARIANTS | 0.857 | prajane vīyateḥ | pra-jan-e vī-ya-te-ḥ |
| 6.1.56 | VARIANTS | 0.878 | bibheter hetubhaye | bi-bhe-te-r hetu-bhay-e |
| 6.1.57 | VARIANTS | 0.882 | nityaṃ smayateḥ | nitya-ṃ smay-a-te-ḥ |
| 6.1.58 | VARIANTS | 0.836 | sṛji-dṛśor jñaly am akiti | sṛji-dṛś-or jhaL-i=aM=a-K-IT-i |
| 6.1.59 | VARIANTS | 0.850 | anudāttasya ca rdupadhasya anyatarsyām | anudātta-sya ca=ṛT=padha-sya=nya-tara-syām |
| 6.1.60 | VARIANTS | 0.875 | śīrṣaṃś chandasi | śīrṣan=chandas-i |
| 6.1.61 | AGREES | 0.933 | ye ca taddhite | y-e ca taddhit-e |
| 6.1.62 | AGREES | 0.909 | aci śīrṣaḥ | aC-i śīrṣa-ḥ |
| 6.1.63 | VARIANTS | 0.855 | pad-dan-no-mās-hṛn-niś-asan-yūṣan-doṣan-yakañ-chakann-udann-āsañ chasprabhṛtiṣu | pad-dat=nas=mās=hṛd=niś=asan=yūṣan=doṣan=yakan=śakan-udan=āsan Śas-pra-bhṛ-ti-ṣu |
| 6.1.64 | AGREES | 0.919 | dhātvādeḥ ṣaḥ saḥ | dhātv=ādeḥ ṣ-aḥ sa-ḥ |
| 6.1.65 | VARIANTS | 0.667 | ṇo naḥ | ṇ-aḥ na-ḥ |
| 6.1.66 | AGREES | 0.903 | lopo vyor vali | lopo v-y-or vaL-i |
| 6.1.67 | VARIANTS | 0.867 | ver apṛktasya | ve-r a-pṛk-ta-sya |
| 6.1.68 | VARIANTS | 0.813 | hal-ṅy-ābbhyo dīrghāt su-ti-sy-apṛktaṃ hal | haL=Ṅī=āP=bh yaḥ dīrgh-āt sU-ti-si=a-pṛk-ta-m haL |
| 6.1.69 | AGREES | 0.913 | eṅ hrasvāt sambuddheḥ | eṄ=hrasv-āt sam-bud-dhe-ḥ |
| 6.1.70 | VARIANTS | 0.884 | śeḥ chandasi bahulam | Śe-s=chandas-i bahula-m |
| 6.1.71 | AGREES | 0.920 | hrasvasya piti kṛti tuk | hrasva-sya P-IT-i kṛt-i tuK |
| 6.1.72 | VARIANTS | 0.870 | saṃhitāyām | saṃ-hitā-y-ām |
| 6.1.73 | AGREES | 0.923 | che ca | ch-e ca |
| 6.1.74 | VARIANTS | 0.870 | āṅ-māṅoś ca | āṄ-māṄ-os=ca |
| 6.1.75 | AGREES | 0.933 | dīrghāt | dīrgh-āt |
| 6.1.76 | VARIANTS | 0.720 | padāntād vā | pada=ant-āt=vā |
| 6.1.77 | VARIANTS | 0.750 | iko yaṇaci | iK-aḥ yaṆ aC-i |
| 6.1.78 | VARIANTS | 0.811 | eco 'y-av-āy-āvaḥ | eC-aḥ=ay-av-āy-āv-aḥ |
| 6.1.79 | VARIANTS | 0.732 | vānto yi pratyaye | va=anta-ḥ y-i praty-ay-e |
| 6.1.80 | AGREES | 0.941 | dhātos tannimittasya+eva | dhāto-s tan-nimitta-sya=eva |
| 6.1.81 | VARIANTS | 0.830 | kṣayya-jayyau śakyārthe | kṣay-ya-jay-ya-au śakya=arth-e |
| 6.1.82 | VARIANTS | 0.889 | krayyas tadarthe | kray-ya-s tad-arth-e |
| 6.1.83 | VARIANTS | 0.862 | bhyyapravayye ca cchandasi | bhay-ya- pra-vay-y-e ca=chandas-i |
| 6.1.84 | AGREES | 0.919 | ekaḥ pūrvaparayoḥ | eka-ḥ pūrva-paray-oḥ |
| 6.1.85 | VARIANTS | 0.815 | antādivac ca | anta=ādi-vat=ca |
| 6.1.86 | VARIANTS | 0.889 | ṣatva-tukor asiddhaḥ | ṣa-tva-tuK-or a-sid-dha-ḥ |
| 6.1.87 | VARIANTS | 0.750 | ādguṇaḥ | āt=guṇa-ḥ |
| 6.1.88 | VARIANTS | 0.880 | vṛddhir eci | vṛd-dhi-r eC-i |
| 6.1.89 | VARIANTS | 0.778 | ety-edhaty-ūṭhsu | e-ti=edh-a-ti=ūṬH-su |
| 6.1.90 | VARIANTS | 0.800 | āṭaś ca | āṬ-as=ca |
| 6.1.91 | VARIANTS | 0.864 | upasargād ṛti dhātau | upa-sarg-āt ṛT-i dhāt-au |
| 6.1.92 | AGREES | 0.909 | vā supyāpiśaleḥ | vā sUP-y āpiśale-ḥ |
| 6.1.93 | VARIANTS | 0.774 | ā-oto 'm-śasoḥ | ā=oT-aḥ=am-Śas-oḥ |
| 6.1.94 | VARIANTS | 0.897 | eṅi pararūpam | eṄ-i para-rūpa-m |
| 6.1.95 | VARIANTS | 0.857 | om-āṅoś ca | om=āṄ-os=ca |
| 6.1.96 | VARIANTS | 0.710 | usy apadāntāt | us-i a-pada=ant-āt |
| 6.1.97 | VARIANTS | 0.737 | ato guṇe | aT-aḥ=guṇ-e |
| 6.1.98 | VARIANTS | 0.879 | avyakta-anukaraṇasya ata itau | a-vyak-ta=anu-kar-aṇa-sya=at-aḥ it-au |
| 6.1.99 | VARIANTS | 0.892 | na āmreḍitasya anatyasya tu vā | na=ā-mreḍ-i-ta-sya=ant-ya-sya tu vā |
| 6.1.100 | VARIANTS | 0.870 | nityam āmreḍite ḍāci | nitya-m ā-mreḍ-i-t-e ḌāC-i |
| 6.1.101 | AGREES | 0.909 | akaḥ savarṇe dīrghaḥ | aK-aḥ sa-varṇ-e dīrgha-ḥ |
| 6.1.102 | AGREES | 0.943 | prathamayoḥ pūrvasavarṇaḥ | prathamay-oḥ pūrva-savarṇa-ḥ |
| 6.1.103 | VARIANTS | 0.750 | tasmāc chaso naḥ puṃsi | ta-smāt=Śas-aḥ=na-ḥ puṃs-i |
| 6.1.104 | VARIANTS | 0.706 | nād ici | na=āt=iC-i |
| 6.1.105 | VARIANTS | 0.875 | dīrghāj jasi ca | dīrgh-āt=Jas-i ca |
| 6.1.106 | AGREES | 0.957 | vā chandasi | vā chandas-i |
| 6.1.107 | AGREES | 0.909 | ami pūrvaḥ | am-i pūrva-ḥ |
| 6.1.108 | VARIANTS | 0.833 | samprasāraṇāc ca | sam-pra-sār-aṇ-āt=ca |
| 6.1.109 | VARIANTS | 0.769 | eṅaḥ padāntād ati | eṄ-aḥ pada=ant-āt=aT-i |
| 6.1.110 | VARIANTS | 0.846 | ṅasiṅasoś ca | ṄasI-Ṅas-os=ca |
| 6.1.111 | VARIANTS | 0.857 | ṛta ut | ṛT-aḥ=uT |
| 6.1.112 | AGREES | 0.914 | khyatyāt parasya | khya-ty-āt para-sya |
| 6.1.113 | VARIANTS | 0.745 | ato ror aplutād aplute | aT-aḥ=rO-ḥ=a-plut-āt=a-plut-e |
| 6.1.114 | AGREES | 0.933 | haśi ca | haŚ-i ca |
| 6.1.115 | VARIANTS | 0.818 | prakṛtyā 'ntaḥpādam avyapare | pra-kṛ-ty-ā=antaḥ-pāda-m a-v-y-a-par-e |
| 6.1.116 | VARIANTS | 0.818 | avyād-avadyād-avakramur-avrata-ayam-avantv-avasyusu ca | avyāt=avadyāt=ava-kramus=a-vrata=ayam=avantu=av as-yu-ṣu |
| 6.1.117 | VARIANTS | 0.870 | yajuṣy uraḥ | yajuṣ-i=uraḥ |
| 6.1.118 | VARIANTS | 0.874 | āpo-juṣaṇo-vṛṣṇo-varṣiṣṭhe 'mbe 'mbāle 'mbikepūrve | āpo=jusāṇo=vṛṣṇo=varṣ-iṣṭhe=ambe=ambāle=ambike-pūrv-e |
| 6.1.119 | AGREES | 0.909 | aṅga ity ādau ca | aṛga ity-ād-au ca |
| 6.1.120 | VARIANTS | 0.894 | anudātte ca kudhapare | anu-dātt-e ca kU-dha-par-e |
| 6.1.121 | VARIANTS | 0.867 | avapathāsi ca | a-vap-a-thās-i ca |
| 6.1.122 | AGREES | 0.952 | sarvatra vibhāṣā goḥ | sarva-tra vibhāṣā go-ḥ |
| 6.1.123 | AGREES | 0.973 | avaṅ sphoṭāyanasya | avaṄ sphoṭāyana-sya |
| 6.1.124 | VARIANTS | 0.828 | indre ca nityam | indr-e (nitya-m*) |
| 6.1.125 | VARIANTS | 0.706 | pluta-pragṛhyā aci | plu-ta=pra-gṛh-y-ā-ḥ aC-i nitya-m |
| 6.1.126 | VARIANTS | 0.769 | āṅo 'nunāsikaś chandasi | āṄ-aḥ=anu-nās-ika-s=chandas-i |
| 6.1.127 | VARIANTS | 0.853 | iko 'savarṇe śākalyasya hrasvaś ca | iK-aḥ=a-sa-varṇ-e śākalya-sya hrasvaśs=ca |
| 6.1.128 | VARIANTS | 0.889 | ṛty akaḥ | ṛT-y aK-aḥ |
| 6.1.129 | VARIANTS | 0.818 | aplutavad-upasthite | a-plu-ta-vat=upa-sthi-t-e |
| 6.1.130 | AGREES | 0.923 | ī3 cākravarmaṇasya | ī3 cākra-varmaṇ-a-sya |
| 6.1.131 | VARIANTS | 0.875 | diva ut | div-aḥ=uT |
| 6.1.132 | VARIANTS | 0.736 | etat-tadoḥ sulopo 'kor anañsamāse hali | etad=tad-oḥ sU-lopa-ḥ=a-k-oḥ a-naÑ-sam-ās-e haL-i |
| 6.1.133 | AGREES | 0.933 | syaś chandasi bahulam | sya-ś chandas-i bahula-m |
| 6.1.134 | VARIANTS | 0.820 | so 'ci lope cet pādapūraṇam | s-aḥ=aC-i lop-e cet pāda-pūr-aṇa-m |
| 6.1.135 | VARIANTS | 0.867 | suṭ kāt pūrvaḥ | suṬ k-at pūrva-ḥ |
| 6.1.136 | VARIANTS | 0.851 | aḍ-abhyāsa-vyavāye 'pi | aṬ=abhyāsa-vy-av-āy-e=api |
| 6.1.137 | VARIANTS | 0.841 | samparyupebhyaḥ karotau bhūṣaṇe | sam-pari=upe-bhyḥ kar-o-t-au bhūṣ-aṇ-e |
| 6.1.138 | VARIANTS | 0.880 | samavāye ca | sam-av-āy-e ca |
| 6.1.139 | VARIANTS | 0.867 | upāt pratiyatna-vaikṛta-vākya-adhyāhāresu | up-āt prati-yat-na-vai-kṛ-ta-vākya=dhy-ā-hār-e-ṣu |
| 6.1.140 | VARIANTS | 0.848 | kiratau lavane | kir-a-t-au lav-an-e |
| 6.1.141 | VARIANTS | 0.821 | hiṃsāyāṃ prateś ca | hiṃsā-y-ām prate-s=ca |
| 6.1.142 | VARIANTS | 0.783 | apāc catuṣpāc-chakuniṣv ālekhane | ap-āt=catuṣ-pād=śakuni-ṣu=ā-lekh-an-e |
| 6.1.143 | VARIANTS | 0.857 | kustumburūṇi jātiḥ | ku-s-tumburū-ṇ-i jā-ti-ḥ |
| 6.1.144 | VARIANTS | 0.842 | aparasparāḥ kriyāsātatye | a-para-s-par-ā-ḥ kriy-ā-sātat-y-e |
| 6.1.145 | VARIANTS | 0.873 | goṣpadaṃ sevita-asevita-pramāṇesu | go-ṣ-pada-m sevita=a-sevita-pramāṇe-ṣu |
| 6.1.146 | VARIANTS | 0.826 | āspadaṃ pratiṣṭhāyām | ā-s-pada-m prati-ṣṭhā-y-ām |
| 6.1.147 | VARIANTS | 0.811 | āścaryam anitye | ā-ś-car-ya-m a-ni-ty-e |
| 6.1.148 | VARIANTS | 0.791 | varcaske 'vaskaraḥ | varc-as-k-e=ava-s-kar-a-ḥ |
| 6.1.149 | VARIANTS | 0.762 | apaskaro rathāṅgam | apa-s-kar-o ratha=aṛga-m |
| 6.1.150 | VARIANTS | 0.720 | viṣkiraḥ śukumnirvikiro vā | vi-ṣ-kir-a-ḥ śakuni-r vā |
| 6.1.151 | VARIANTS | 0.870 | hvasvāc candra-uttarapade mantre | hrasv-āt=candra=ut-tara-pad-e mantr-e |
| 6.1.152 | VARIANTS | 0.864 | pratiṣkaśaś ca kaśeḥ | prati-ṣ-kaśa-s=ca kaśe-ḥ |
| 6.1.153 | VARIANTS | 0.793 | praskaṇva-hariścandrāv ṛṣī | pra-s-kaṇva-hari-s-candr-au=ṛṣ-ī |
| 6.1.154 | VARIANTS | 0.857 | maskaramaskariṇau veṇuparivrājakayoḥ | ma-s-kar-a-ma-s-kar-iṇ-au veṇu-pari-vrāj-akay-oḥ |
| 6.1.155 | VARIANTS | 0.808 | kāstīrājastunde nagare | kā-s-tīra=aja-s-tund-e nagar-e |
| 6.1.156 | VARIANTS | 0.865 | kāraskaro vṛkṣaḥ | kār-a-s-kar-o vṛkṣa-ḥ |
| 6.1.157 | VARIANTS | 0.838 | pāraskaraprabhṛtīni ca sañjñāyām | pāra-s-kar-a=pra-bhṛ-tī-n-i ca saṃjñā-y-ām |
| 6.1.158 | VARIANTS | 0.836 | anudāttaṃ padam ekavarjam | an-udatta-m pada-m eka-varja-m |
| 6.1.159 | VARIANTS | 0.794 | karṣa-ātvato ghaño 'nta udāttaḥ | karṣ-a=āT-vat-aḥ GHaÑ-aḥ=anta=dātta-ḥ |
| 6.1.160 | VARIANTS | 0.774 | ucchādīnāṃ ca | uñch-a=ādī-n-āṃ ca |
| 6.1.161 | AGREES | 0.941 | anudāttasya ca yatra+udāttalopaḥ | an-udātta-sya ca yatra=udātta-lopa-ḥ |
| 6.1.162 | AGREES | 0.923 | dhātoḥ | dhāto-ḥ |
| 6.1.163 | VARIANTS | 0.833 | citaḥ | C-IT=aḥ |
| 6.1.164 | AGREES | 0.957 | taddhitasya | taddhita-sya |
| 6.1.165 | VARIANTS | 0.833 | kitaḥ | K-IT-aḥ |
| 6.1.166 | VARIANTS | 0.839 | tisṛbhyo jasaḥ | tisṛ-bhyaḥ Jas-aḥ |
| 6.1.167 | AGREES | 0.923 | caturaḥ śasi | catur-aḥ Śas-i |
| 6.1.168 | VARIANTS | 0.865 | sāv eka-acas tṛtīyā-ādir vibhaktiḥ | s-au eka=aC-as=tṛ-tīyā=ādir vi-bhak-ti-ḥ |
| 6.1.169 | VARIANTS | 0.769 | anta-udāttād uttarapadādanyatarasyām anityasamāse | anta=datt-āt=ittara-pad-āt=nya-tara-yām a-nitya-am-ās-e |
| 6.1.170 | VARIANTS | 0.794 | añceś chandasy asarvanāmasthānam | añce-s=chandas-i=a-sarva-āma-sthā-ne |
| 6.1.171 | VARIANTS | 0.873 | ūḍ-idaṃ-padādy-ap-pum-rai-dyubhyaḥ | ūṬH=idam=pad-ādi=ap-pum-rai-dyu-bhyaḥ |
| 6.1.172 | AGREES | 0.933 | aṣṭano dīrghāt | aṣṭan-o dīrgh-āt |
| 6.1.173 | VARIANTS | 0.800 | śatur anumo nady-aj-ādī | Śatu-r a-nuM-aḥ nadī=aC=ādī |
| 6.1.174 | VARIANTS | 0.844 | udāttayaṇo halpūrvāt | udātta-yaṆ-aḥ haL-pūrv-āt |
| 6.1.175 | VARIANTS | 0.889 | na+uṅ-dhātvoḥ | na=ūṄ-dhātv-oḥ |
| 6.1.176 | VARIANTS | 0.884 | hrasva-nuḍbhyāṃ matup | hrasva-nuṬ=bhyām matUP |
| 6.1.177 | AGREES | 0.914 | nām anyatarasyām | n-ām anya-tara-syām |
| 6.1.178 | VARIANTS | 0.889 | ṅyāś chandasi bahulam | Ṅy-ās=chandas-i bahula-m |
| 6.1.179 | VARIANTS | 0.808 | ṣaṭtricaturbhyo halādiḥ | ṣaṣ-tri-catur-bhyaḥ haL=ādi-ḥ |
| 6.1.180 | VARIANTS | 0.812 | jñaly upottamam | jhaL-i upottama-m |
| 6.1.181 | AGREES | 0.941 | vibhāṣā bhāṣāyām | vibhāṣā bhāṣā-y-ām |
| 6.1.182 | VARIANTS | 0.847 | na go-śvan-sāvavarṇa-rāḍ-aṅ-kruṅ-kṛdbhyaḥ | na go-śvan-sAU=a-varṇa=rāj=aṛ=kruṛ=kṛd-bhyaḥ |
| 6.1.183 | AGREES | 0.947 | divo jhal | div-o jhaL |
| 6.1.184 | AGREES | 0.947 | nṛ ca anyatarasyām | nṛ ca=anya-tara-syām |
| 6.1.185 | VARIANTS | 0.857 | tit svaritam | T=IT svar-i-ta-m |
| 6.1.186 | VARIANTS | 0.823 | tāsy-anudāten-ṅid-ad-upadeśāl la-sārvadhātukam anudāttam ahnviṅoḥ | tāsi=an-udātta=IT=ṄIT=aT=upa-deś-āt la-sārvadhātuka-m anu-dāttam a-hnu=iṄ-oḥ |
| 6.1.187 | VARIANTS | 0.816 | ādiḥ sico 'nyatarasyām | ādi-ḥ siC-aḥ=anya-tara-syām |
| 6.1.188 | VARIANTS | 0.868 | svapādi-hiṃsām acy aniṭi | svap=ādi=hiṃs-ām aC-i=an-iṬ-i |
| 6.1.189 | VARIANTS | 0.865 | abhyastānām ādiḥ | abhy-as-tā-n-ām ādi-ḥ |
| 6.1.190 | VARIANTS | 0.870 | anudāte ca | an-udātt-e ca |
| 6.1.191 | AGREES | 0.929 | sarvasya supi | sarva-sya sUP-i |
| 6.1.192 | VARIANTS | 0.862 | bhī-hrī-bhṛ-hu-mada-jana-dhana-daridrā-jāgarāṃ pratyayāt pūrvaṃ piti | bhī-hrī-bhṛ-hu-mada-janA-dhanA-daridrā-jāgar-ām pūrva-m P-IT-i |
| 6.1.193 | VARIANTS | 0.800 | liti | L-IT-i |
| 6.1.194 | VARIANTS | 0.885 | ādir ṇamuly anyatarasyām | ādi-r ṆamuL-i=anya-tara-syām |
| 6.1.195 | VARIANTS | 0.875 | acaḥ kartṛyaki | aC-aḥ kar-tṛ-yaK-i |
| 6.1.196 | VARIANTS | 0.667 | thali ca seṭīḍanto vā | thaL-i ca sa-iṬ-i=iṬ=anta-ḥ=vā |
| 6.1.197 | VARIANTS | 0.842 | ñnityādir nityam | Ñ-N-IT-y ādi-r nitya-m |
| 6.1.198 | AGREES | 0.909 | āmantritasya ca | ā-mantr-ita-sya ca |
| 6.1.199 | AGREES | 0.966 | pathi-mathoḥ sarvanāmasthāne | pathi-math-oḥ sarvanāmasthān-e |
| 6.1.200 | AGREES | 0.955 | antaś ca tavai yugapat | antas=ca tavai yugapat |
| 6.1.201 | VARIANTS | 0.759 | kṣayo nivāse | kṣay-a-ḥ ni-vās-e |
| 6.1.202 | VARIANTS | 0.867 | jayaḥ karaṇam | jay-a-ḥ kar-aṇa-m |
| 6.1.203 | AGREES | 0.933 | vṛṣa-ādīnāṃ ca | vṛṣa=ādī-n-āṃ ca |
| 6.1.204 | VARIANTS | 0.829 | sañjñāyām upamānam | saṃjñā-y-ām upa-mā-na-m |
| 6.1.205 | AGREES | 0.905 | niṣṭhā ca dvyaj anāt | niṣṭhā ca dvy-aC an-āT |
| 6.1.206 | VARIANTS | 0.828 | śuṣka-dhṛṣtau | śuṣ-ka=dhṛṣ-ṭ-au |
| 6.1.207 | VARIANTS | 0.857 | āśitaḥ kartā | āś-i-ta-ḥ kar-tā |
| 6.1.208 | AGREES | 0.929 | rikte vibhāṣā | rik-t-e vibhāṣā |
| 6.1.209 | VARIANTS | 0.873 | juṣṭa-arpite ca cchandasi | juṣ-ṭa=ar-p-i-t-e ca=chandas-i |
| 6.1.210 | AGREES | 0.929 | nityaṃ mantre | nitya-ṃ mantr-e |
| 6.1.211 | AGREES | 0.950 | yuṣmad-asmador ṅasi | yuṣmad=asmad-or Ṅas-i |
| 6.1.212 | AGREES | 0.933 | ṅayi ca | Ṅay-i ca |
| 6.1.213 | VARIANTS | 0.692 | yato 'nāvaḥ | yaT-aḥ=a-nāv-aḥ |
| 6.1.214 | AGREES | 0.969 | īḍa-vanda-vṛ-śaṃsa-duhāṃ ṇyataḥ | īḍA-vanda-vṛ-śaṃsa-duh-āṃ ṆyaT-aḥ |
| 6.1.215 | AGREES | 0.936 | vibhāṣā veṇv-indhānayoḥ | vibhāṣā veṇu=indhānay-oḥ |
| 6.1.216 | AGREES | 0.902 | tyāga-rāga-hāsa-kuha-śvaṭha-krathānām | tyāg-a-rāg-a=hās-a-kuh-a-śvaṭh-a-krath-ā-n-ām |
| 6.1.217 | VARIANTS | 0.706 | upottamaṃ riti | upa=ut-tama-m R-IT-i |
| 6.1.218 | VARIANTS | 0.865 | caṅy anyatarasyām | CaṄ-i=anya-tara-syām |
| 6.1.219 | VARIANTS | 0.886 | matoḥ pūrvamāt sañjñāyāṃ striyām | matO-ḥ pūrva-m āT saṃjñā-y-āṃ striy-ām |
| 6.1.220 | VARIANTS | 0.741 | anto 'vatyāḥ | anta-ḥ=avaty-āḥ |
| 6.1.221 | VARIANTS | 0.875 | īvatyāḥ | ī-vaty-āḥ |
| 6.1.222 | VARIANTS | 0.857 | cau | c-au |
| 6.1.223 | VARIANTS | 0.857 | samāsasya | sam-ās-a-sya |
| 6.2.1 | VARIANTS | 0.896 | bahuvrīhau prakṛtyā pūrvapadam | bahu-vrīh-au pra-kṛ-ty-ā pūrva-pada-m |
| 6.2.2 | AGREES | 0.925 | tatpuruṣe tulyārtha-tṛtīyā-saptamy-upamāna-avyaya-dvitīyā-kṛtyāḥ | tatpuruṣ-e tulya=artha-tṛ-tīyā-saptamī-upamāna=avyaya-dvi-tīyā-kṛtyā-ḥ |
| 6.2.3 | VARIANTS | 0.744 | varṇo varneṣv anete | varṇa-ḥ varṇe-ṣu=an-et-e |
| 6.2.4 | VARIANTS | 0.880 | gādha-lavanayoḥ pramāṇe | gādha-lavaṇay-oḥ pra-mā-ṇ-e |
| 6.2.5 | VARIANTS | 0.857 | dāyādyaṃ dāyāde | dāyād-ya-ṃ dāy-ā-d-e |
| 6.2.6 | AGREES | 0.947 | pratibandhi cira-kṛcchrayoḥ | prati-bandh-i cira-kṛcchray-oḥ |
| 6.2.7 | VARIANTS | 0.815 | pade 'padeśe | pad-e=apa-deś-e |
| 6.2.8 | VARIANTS | 0.865 | nivāte vātatrāṇe | ni-vāt-e vāta-trā-ṇ-e |
| 6.2.9 | VARIANTS | 0.848 | śārade 'nārtave | śārad-e an-ārtav-e |
| 6.2.10 | AGREES | 0.941 | adhvaryu-kaṣāyayor jātau | adhvaryu-kaṣāyay-or jā-t-au |
| 6.2.11 | AGREES | 0.933 | sa-dṛśa-pratirūpayoḥ sādṛśye | sa-dṛś-a-prati-rūpay-oḥ sādṛśy-e |
| 6.2.12 | VARIANTS | 0.875 | dvigau pramāṇe | dvig-au pra-mā-ṇ-e |
| 6.2.13 | VARIANTS | 0.894 | gantavya-paṇya vāṇije | gan-tavya-paṇ-ya-ṃ vāṇij-e |
| 6.2.14 | VARIANTS | 0.779 | mātropajñopakramacchāye napuṃsake | mātrā=upa-jñā=upa-kram-a=chāy-e na-puṃs-ak-e |
| 6.2.15 | AGREES | 0.927 | sukha-priyayor hite | sukha-priyay-or hi-t-e |
| 6.2.16 | AGREES | 0.900 | prītau ca | prī-t-au ca |
| 6.2.17 | VARIANTS | 0.846 | svaṃ svāmini | sva-m svāmin-i |
| 6.2.18 | VARIANTS | 0.765 | patyāv aiśvarye | paty-au=aiś-var-y-e |
| 6.2.19 | AGREES | 0.909 | na bhū-vāk-cid-didhiṣu | na bhū-vāc=cit=didhiṣu |
| 6.2.20 | VARIANTS | 0.833 | vā bhūvanam | vā bhuv-ana-m |
| 6.2.21 | VARIANTS | 0.880 | āśaṅka-ābādha-nedīyassu sambhāvane | ā-śaṛka=ā-bādha-ned-īyas-su sam-bhāv-an-e |
| 6.2.22 | VARIANTS | 0.889 | pūrve bhūtapūrve | pūrv-e bhū-ta-pūrv-e |
| 6.2.23 | AGREES | 0.914 | savidha-sanīḍa-samaryāda-saveśa-sadeśeṣu sāmīpye | sa-vidha-sa-nīḍa-sa-mar-yāda-sa-veśa-sa-deśe-ṣu sāmīp-y-e |
| 6.2.24 | VARIANTS | 0.885 | vispaṣṭa-ādīni guṇavacaneṣu | vi-spaṣ-ṭa=ādī-n-i guṇa-vac-ane-ṣu |
| 6.2.25 | AGREES | 0.949 | śra-jya-avama-kan-pāpa-vatsu bhāve karmadhāraye | śra-jya=avama-kan-pāpa-vat-su bhāv-e karma-dhār-ay-e |
| 6.2.26 | VARIANTS | 0.857 | kumāraś ca | kumāra-s=ca |
| 6.2.27 | AGREES | 0.909 | ādiḥ pratyenasi | ādi-ḥ praty-enas-i |
| 6.2.28 | VARIANTS | 0.878 | pūgeṣv anyatarasyām | pūge-ṣu=anya-tara-syām |
| 6.2.29 | AGREES | 0.943 | iganta-kāla-kapāla-bhagāla-śarāveṣu dvigau | iK=anta=kāla-kapāla-bhagāla-śarāve-ṣu dvig-au |
| 6.2.30 | VARIANTS | 0.889 | bahv-anyatarasyām | bahu=anya-tara-syām |
| 6.2.31 | VARIANTS | 0.850 | diṣṭi-vitastyoś ca | diṣ-ṭi-vi-tas-ty-os=ca |
| 6.2.32 | VARIANTS | 0.891 | saptamī siddha-śuṣka-pakva-bandheṣv akālāt | sapta-m-ī sid-dha-śuṣ-ka-pak-va-bandhe-ṣu=a-kāl-āt |
| 6.2.33 | VARIANTS | 0.885 | pari-praty-upa-apā varjyamāna-ahorātra-avayaveṣu | pari-prati=upa=ap-ā-ḥ varj-ya-m-āna=aho-rātra=va-yave-ṣu |
| 6.2.34 | VARIANTS | 0.899 | rājanya-bahuvacana-dvandve 'ndhaka-vṛṣṇiṣu | rājan-ya-bahu-vac-ana-dvaṃdv-e andhaka-vṛṣṇi-ṣu |
| 6.2.35 | VARIANTS | 0.750 | saṅkhyā | saṃ-khy-ā |
| 6.2.36 | VARIANTS | 0.862 | ācārya-upasarjanaś ca antevāsī | ā-cār-ya=upa-sarj-anas=ca=nte-vās-ī |
| 6.2.37 | VARIANTS | 0.864 | kārta-kaujapa-ādayaś ca | kārta-kaujapa=āday-aḥ |
| 6.2.38 | AGREES | 0.954 | mahān vrīhy-aparāhṇa-gṛṣṭi-iṣvāsa-jābāla-bhāra-bhārata-hailihila-raurava-pravṛddheṣu | mahān vrīhi=apar-ā-hṇa=gṛṣṭi=iṣv-āsa-jābāla-bhāra-bhārata-hailihila-raurava-pra-vṛd-dhe-ṣu |
| 6.2.39 | VARIANTS | 0.898 | kṣullakaś ca vaiśvadeve | kṣullaka-s=ca vaiśva-dev-e |
| 6.2.40 | AGREES | 0.947 | uṣṭraḥ sādi-vāmyoḥ | uṣṭra-ḥ sādi-vāmy-oḥ |
| 6.2.41 | AGREES | 0.923 | gauḥ sāda-sādi-sārathiṣu | gau-ḥ sād-a-sād-i-sārathi-ṣu |
| 6.2.42 | VARIANTS | 0.850 | kurugārhapata-riktagurv-asūtajaraty-aślīladṛḍharūpā-pārevaḍavā-taitilakadrū-paṇyakambalo dāsībhārāṇāṃ ca | kuru-gārha-pat-a-rik-ta-guru=a-sū-ta-jar-at-ī=a-ślī-la-dṛ-ḍha-rūp-ā-pāre-vaḍavā-taittila-kadrū-ḥ-paṇya=ambala-ḥ=āsī-bhārā-ṇ-āṃ ca |
| 6.2.43 | AGREES | 0.971 | caturthī tadarthe | caturthī tad-arthe |
| 6.2.44 | AGREES | 0.909 | arthe | arth-e |
| 6.2.45 | AGREES | 0.923 | kte ca | Kt-e ca |
| 6.2.46 | VARIANTS | 0.884 | karmadhāraye 'niṣṭhā | karma-dhāray-e=a-niṣṭhā |
| 6.2.47 | VARIANTS | 0.867 | ahīne dvitīyā | a-hī-n-e dvi-tīyā |
| 6.2.48 | AGREES | 0.903 | tṛtīyā karmaṇi | tṛ-tīyā kar-maṇ-i |
| 6.2.49 | VARIANTS | 0.848 | gatiranantaraḥ | ga-ti-r an-antara-ḥ |
| 6.2.50 | VARIANTS | 0.857 | ta-ādau ca niti kṛty-atau | ta=ād-au ca N-IT-i kṛt-i=a-t-au |
| 6.2.51 | AGREES | 0.941 | tavai ca antaś ca yugapat | tavai ca=anta-s=ca yugapat |
| 6.2.52 | VARIANTS | 0.750 | aniganto 'ñcatau vapratyaye | an-iK=anta-ḥ=añc-a-t-au va-praty-ay-e |
| 6.2.53 | VARIANTS | 0.857 | ny-adhī ca | ni=adh-ī ca |
| 6.2.54 | VARIANTS | 0.889 | īṣad anyatarasyām | īṣat=anya-tara-syām |
| 6.2.55 | VARIANTS | 0.898 | hiraṇyaparimāṇaṃ dhane | hiraṇya-pari-mā-ṇa-ṃ dhan-e |
| 6.2.56 | VARIANTS | 0.759 | prathamo 'cira-upasampattau | prathama-ḥ=a-cira=pa-am-at-t-au |
| 6.2.57 | AGREES | 0.931 | katara-katamau karmadhāraye | k-atara- k-atam-au karmadhāray-e |
| 6.2.58 | VARIANTS | 0.898 | āryo brāhmaṇa-kumārayoḥ | ārya-ḥ brāhmaṇa-kumāray-oḥ |
| 6.2.59 | AGREES | 1.000 | rājā ca | rājā ca |
| 6.2.60 | AGREES | 0.944 | ṣaṣṭhī pratyenasi | ṣaṣṭhī praty-enas-i |
| 6.2.61 | AGREES | 0.938 | kte nitya-arthe | Kt-e nitya=arth-e |
| 6.2.62 | AGREES | 0.933 | grāmaḥ śilpini | grāma-ḥ śilpin-i |
| 6.2.63 | AGREES | 0.927 | rājā ca praśaṃsāyām | rājā ca pra-śaṃsā-y-ām |
| 6.2.64 | AGREES | 0.923 | ādir udāttaḥ | ādi-r udātta-ḥ |
| 6.2.65 | VARIANTS | 0.853 | saptamīhāriṇau dharmye 'haraṇe | saptamī-hār-iṇ-au dharm-y-e=a-har-aṇ-e |
| 6.2.66 | VARIANTS | 0.889 | yukte ca | yuk-t-e ca |
| 6.2.67 | AGREES | 0.941 | vibhāṣā adhyakṣe | vibhāṣā=adhy-akṣ-e |
| 6.2.68 | AGREES | 0.914 | pāpaṃ ca śilpini | pāpa-ṃ ca śilp-in-i |
| 6.2.69 | AGREES | 0.900 | gotra-antevāsi-mānava-brāhmaṇesu kṣepe | gotra=antevāsi(n)=māṇava-brāhmaṇe-ṣu kṣep-e |
| 6.2.70 | VARIANTS | 0.812 | aṅgāni maireye | aṛgā-n-i mair-ey-e |
| 6.2.71 | AGREES | 0.906 | bhakta-ākhyās tadartheṣu | bhak-ta=ā-khy-ās tad-arthe-ṣu |
| 6.2.72 | AGREES | 0.946 | go-biḍāla-siṃha-saindhaveṣu upamāne | go-biḍāla-siṃha-saindhave-ṣu upa-mā-n-e |
| 6.2.73 | VARIANTS | 0.889 | ake jīvikā-arthe | ak-e jīv-ik-ā=arth-e |
| 6.2.74 | VARIANTS | 0.848 | prācāṃ krīḍāyāṃ | prāc-āṃ krīḍā-y-ām |
| 6.2.75 | VARIANTS | 0.846 | aṇi niyukte | aṆ-i ni-yuk-t-e |
| 6.2.76 | VARIANTS | 0.895 | śilpini ca akṛñaḥ | śilp-in-i ca a-kṛÑ-aḥ |
| 6.2.77 | VARIANTS | 0.846 | sañjñāyāṃ ca | saṃjñā-y-āṃ ca |
| 6.2.78 | VARIANTS | 0.842 | gotantiyavaṃ pāle | go-tanti-yava-m pāl-e |
| 6.2.79 | VARIANTS | 0.889 | ṇini | Ṇin-i |
| 6.2.80 | VARIANTS | 0.783 | upamanaṃ śabda-artha-prakṛtāv eva | upa-mā-nam śabda=rtha-pra-kṛ-t-au=va |
| 6.2.81 | VARIANTS | 0.739 | yuktārohy-ādayaś ca | yuk-ta=ā=roh-i(n)=āday-as=ca |
| 6.2.82 | AGREES | 0.943 | dīrgha-kāśa-tuṣa-bhrāṣṭra-vaṭaṃ je | dīrgha-kāśa-tuṣa-bhrāṣṭra-vaṭa-m j-e |
| 6.2.83 | VARIANTS | 0.880 | antyāt pūrvaṃ bahv-acaḥ | ant-y-āt pūrva-m bahv-aC-aḥ |
| 6.2.84 | VARIANTS | 0.821 | grāme 'nivasantaḥ | grām-e a-ni-vas-ant-aḥ |
| 6.2.85 | VARIANTS | 0.846 | ghoṣa-ādiṣu ca | ghoṣa=ādi-ṣu |
| 6.2.86 | VARIANTS | 0.826 | chātry-ādayaḥ śālāyām | chāttri=āday-as śālā-y-ām |
| 6.2.87 | VARIANTS | 0.824 | prasthe 'vṛddham akarky-ādīnām | pra-sth-e=a-vṛd-dha-m a-karkī=ādī-n-ām |
| 6.2.88 | VARIANTS | 0.857 | mālādīnāṃ ca | mālā=ādī-n-āṃ ca |
| 6.2.89 | VARIANTS | 0.852 | amahan-navaṃ nagare 'nudīcām | a-mahat=nava-ṃ nagar-e=an-udīc-ām |
| 6.2.90 | AGREES | 0.915 | arme ca avarṇam dvyac tryac | arm-e ca a-varṇa-m dvy-aC try-aC |
| 6.2.91 | AGREES | 0.913 | na bhūta-adhika-sañjīva-madra-aśma-kajjalam | na bhū-ta=adhi-ka-saṃ-jīva-madra=aśma(n)=kajjala-m |
| 6.2.92 | AGREES | 0.909 | antaḥ | anta-ḥ |
| 6.2.93 | VARIANTS | 0.760 | vkṣyati - sarvaṃ guṇakārtsnye | sarva-ṃ guṇa-kārtsn-y-e |
| 6.2.94 | VARIANTS | 0.863 | sañjñāyāṃ girinikāyayoḥ | saṃjñā-y-āṃ giri-ni-kāyay-oḥ |
| 6.2.95 | VARIANTS | 0.875 | kumāryām vayasi | kumāry-āṃ vayas-i |
| 6.2.96 | VARIANTS | 0.750 | udake 'kevale | udak-e=Ac(a)-keval-e |
| 6.2.97 | AGREES | 0.929 | dvigau kratau | dvig-au krat-au |
| 6.2.98 | AGREES | 0.923 | sabhāyāṃ napuṃsake | sabhā-y-āṃ napuṃsak-e |
| 6.2.99 | AGREES | 0.917 | pure prācām | pur-e prāc-ām |
| 6.2.100 | AGREES | 0.933 | ariṣṭa-gauḍa-pūrve ca | a-riṣ-ṭa-gauḍa-pūrv-e ca |
| 6.2.101 | AGREES | 0.947 | na hāstina-phalaka-mārdeyāḥ | na hāstina-phala-ka-mārdey-ā-ḥ |
| 6.2.102 | AGREES | 0.933 | kusūla-kūpa-kumbha-śālaṃ bile | kusūla-kūpa-kumbha-śāla-m bil-e |
| 6.2.103 | AGREES | 0.925 | dik-śabdā grāma-janapada-ākhyāna-cānarāṭeṣu | dik=śabd-ā-ḥ grāma-jana-pada=ā-khyā-na-cānarāṭe-ṣu |
| 6.2.104 | VARIANTS | 0.818 | ācārya-upasarjanaś ca antevāsini | ā-cār-ya=upa-sarj-anas=ca=nte-vāsī |
| 6.2.105 | AGREES | 0.900 | uttarapadavṛddhau sarvaṃ ca | ut-tara-pada-vṛd-dh-au sarva-ṃ ca |
| 6.2.106 | VARIANTS | 0.828 | bahuvrīhau viśvaṃ sañjñāyāṃ | bahu-vrīh-au viśva-ṃ saṃjña-yām |
| 6.2.107 | AGREES | 0.970 | udara-aśva-iṣuṣu | udara=aśva=iṣu-ṣu |
| 6.2.108 | AGREES | 0.909 | kṣepe | kṣep-e |
| 6.2.109 | AGREES | 0.929 | nadī bandhuni | nadī bandhu-n-i |
| 6.2.110 | AGREES | 0.919 | niṣṭhā-upasargapūrvam anyatarasyām | niṣṭhā=upa-sarg-a-pūrva-m anya-tara-syām |
| 6.2.111 | AGREES | 0.968 | uttarapada-ādiḥ | uttara-pada=ādiḥ |
| 6.2.112 | VARIANTS | 0.857 | karṇo varṇalakṣaṇāt | karṇa-ḥ varṇa-lakṣaṇ-āt |
| 6.2.113 | VARIANTS | 0.857 | sañjñā-aupamyayoś ca | saṃjñā=aupam-yay-os=ca |
| 6.2.114 | AGREES | 0.918 | kaṇṭha-pṛṣtha-grīvā-jaṅghaṃ ca | kaṇṭha-pṛṣṭha-grīvā-jangha-ṃ ca |
| 6.2.115 | VARIANTS | 0.864 | śṛṅgam avasthāyāṃ ca | śṛṛga-m ava-sthā-y-āṃ ca |
| 6.2.116 | VARIANTS | 0.833 | naño jara-mara-mitra-mṛtāḥ | naÑ-aḥ=jar-a-mar-a-mi-tra-mṛ-t-ā-ḥ |
| 6.2.117 | VARIANTS | 0.885 | sor man-asī aloma-uṣasī | so-r man-as-ī=a-loma(n)=uṣas-ī |
| 6.2.118 | VARIANTS | 0.714 | kratv-ādayaś ca | kratu=āday-aḥ |
| 6.2.119 | AGREES | 0.926 | ādy-udāttaṃ dvyac chandasi | ādi=udāttaṃ dvy-aC chandas-i |
| 6.2.120 | AGREES | 0.933 | vīra-vīryau ca | vīra-vīr-y-au ca |
| 6.2.121 | AGREES | 0.969 | kūla-tīra-tūla-mūla-śālā-akṣa-samam avyayībhāve | kūla-tīra-tūla-mūla-śālā=akṣa-sama-m avyayī-bhāv-e |
| 6.2.122 | AGREES | 0.949 | kiṃsa-mantha-śūrpa-pāyya-kāṇḍaṃ dvigau | kaṃsa-mantha-śūrpa-pāyya-kāṇḍa-ṃ dvig-au |
| 6.2.123 | AGREES | 0.900 | tatpuruṣe śālāyāṃ napuṃsake | tatpuruṣ-e śālā-y-āṃ na-puṃs-ak-e |
| 6.2.124 | AGREES | 1.000 | kanthā ca | kanthā ca |
| 6.2.125 | VARIANTS | 0.722 | ādiścihaṇādīnāṃ | ādi-s=cihaṇa=ādī-n-ām |
| 6.2.126 | AGREES | 0.957 | cela-kheṭa-kaṭuka-kāṇḍaṃ garhāyām | cela-kheṭa-kaṭuka-kāṇḍa-ṃ garhā-y-ām |
| 6.2.127 | VARIANTS | 0.875 | cīram upamānam | cīra-m upa-mā-na-m |
| 6.2.128 | AGREES | 0.917 | palala-sūpa-śākaṃ miśre | palala-sūpa-śāka-m miśr-e |
| 6.2.129 | VARIANTS | 0.866 | kūlasūdasthalakarṣāḥ sañjñāyām | kūla-sūda-sthala-karṣ-ā-ḥ saṃjñā-y-ām |
| 6.2.130 | VARIANTS | 0.884 | akamadhāraye rājyam | a-karmadhāray-e rāj-ya-m |
| 6.2.131 | AGREES | 0.909 | vargya-ādayaś ca | vargya=āday-as=ca |
| 6.2.132 | VARIANTS | 0.848 | putraḥ pumbhyaḥ | put-ra-ḥ puṃ-bhyaḥ |
| 6.2.133 | VARIANTS | 0.693 | na ācārya-rāja-rtvik-saṃyukta-jñāty-ākhyebhyaḥ | na=ā-cār-ya-rāja(n)=ṛtv-ij-saṃ-yuk-ta-jñā-ti=ā-khyā-y-ām |
| 6.2.134 | VARIANTS | 0.877 | cūrṇa-ādīny aprāṇiṣaṣṭhyāḥ | cūrṇa-ādī-n-i=a-prāṇi-ṣaṣṭhy-āḥ |
| 6.2.135 | VARIANTS | 0.889 | ṣaṭ ca kāṇḍādīni | ṣaṭ ca kāṇḍa-ādī-n-i |
| 6.2.136 | AGREES | 0.923 | kuṇḍaṃ vanam | kuṇḍa-ṃ vana-m |
| 6.2.137 | VARIANTS | 0.895 | prakṛtyā bhagālam | pra-kṛ-ty-ā bhagāla-m |
| 6.2.138 | VARIANTS | 0.840 | śiter nitya-abahv-ajb-ahuvrīhāv abhasat | śite-r nitya=a=bah-v=C=ahuvrīh-au=a-bhasat |
| 6.2.139 | AGREES | 0.923 | gati-kāraka-upapadāt kṛt | ga-ti-kār-aka=upa-pad-āt kṛt |
| 6.2.140 | VARIANTS | 0.897 | ubhe vanaspatyādiṣu yugapat | ubh-e vanas-pati-ādi-ṣu yugapat |
| 6.2.141 | VARIANTS | 0.857 | devatādvandve ca | deva-tā-dvaṃdv-e ca |
| 6.2.142 | VARIANTS | 0.872 | na+uttarapade 'nudāttādāv apṛthivī-rudra-pūṣa-manthiṣu | na=uttara-pad-e=anudātta=ād-au=a-pṛthivī-rudra-pūṣa(n)=manthi-ṣu |
| 6.2.143 | AGREES | 0.909 | antaḥ | anta-ḥ |
| 6.2.144 | AGREES | 0.914 | tha-atha-ghañ-kta-aj-ab-itra-kāṇām | tha=atha-GHaÑ-Kta=aC=aP=itra-Kā-ṇ-ām |
| 6.2.145 | VARIANTS | 0.889 | su-upamānāt ktaḥ | su=upa-mā-n-āt Kta-ḥ |
| 6.2.146 | VARIANTS | 0.792 | sañjñāyām anācitādīnām | saṃjñā-y-ām an-ā-ci-ta=ādī-n-ām |
| 6.2.147 | VARIANTS | 0.850 | pravṛddhādīnāṃ ca | pra-vṛd-dha-ādī-n-āṃ ca |
| 6.2.148 | AGREES | 0.912 | kārakād datta-śrutayor eva āśiṣi | kārak-āt=datta=śru-tay-or eva āśiṣ-i |
| 6.2.149 | VARIANTS | 0.893 | itthaṃbhūtena kṛtam iti ca | ittham-bhūt-ena kṛ-ta-m iti ca |
| 6.2.150 | VARIANTS | 0.880 | ano bhāva-karma-vacanaḥ | ana-ḥ bhāva-karma-vac-ana-ḥ |
| 6.2.151 | AGREES | 0.926 | man-ktin-vyākhyāna-śayana-āsana-sthāna-yājaka-ādi-krītāḥ | man-KtiN=vyā-khyā-na-śay-ana=ās-ana-sthā-na-yāj-aka=ādi-krī-t-ā-ḥ |
| 6.2.152 | AGREES | 0.941 | saptamyāḥ puṇyam | saptamy-āḥ puṇya-m |
| 6.2.153 | VARIANTS | 0.764 | ūnārtha-kalahaṃ tṛtīāyāḥ | ūna=artha-kalaha-m tṛ-tīya-y-āḥ |
| 6.2.154 | VARIANTS | 0.866 | miśraṃ ca anupasargam asandhau | miśra-ṃ ca=an-upa-sarga-m a-saṃ-dh-au |
| 6.2.155 | VARIANTS | 0.855 | naño guṇapratiṣedhe sampādy-arha-hita-alamarthās taddhitāḥ | naÑ-aḥ guṇa-prati-ṣedh-e sam-pād-i(n)=arha-hi-ta=alam-arth-ā-s taddhit-ā-ḥ |
| 6.2.156 | VARIANTS | 0.870 | ya-yatoś ca atadarthe | ya-yaT-os=ca a-tad-arth-e |
| 6.2.157 | VARIANTS | 0.645 | ac-kāv aśaktau | aC=K-au=a-śak-t-e |
| 6.2.158 | AGREES | 0.900 | ākrośe ca | ā-kroś-e ca |
| 6.2.159 | VARIANTS | 0.762 | sañjñāyām | saṃ-jñā-y-ām |
| 6.2.160 | VARIANTS | 0.847 | kṛtya-uka-iṣṇuc-cārv-ādayaś ca | kṛt-ya=uka=iṣṇuC-cāru=āday-aḥ |
| 6.2.161 | AGREES | 0.952 | vibhāṣā tṛnn-anna-tīkṣṇa-śuciṣu | vibhāṣā tṛN=anna-tīkṣ-ṇa-śuci-ṣu |
| 6.2.162 | VARIANTS | 0.873 | bahuvrīhāv idam-etat-tadbhyaḥ prathama-pūranayoḥ kriyāgaṇane | bahuvrīh-au=idam=etad=tad-hyaḥ prathama-pūr-aṇay-oḥ kriyā-gaṇ-an-e |
| 6.2.163 | VARIANTS | 0.842 | saṅkhyāyāḥ stanaḥ | saṃ-khyā-y-āḥ stana-ḥ |
| 6.2.164 | CONFLICTS | 0.583 | vibhāṣā | vibhāṣā chandas-i |
| 6.2.165 | VARIANTS | 0.863 | sañjñāyāṃ mitra-ajinayoḥ | saṃjñā-y-ām mitra=ajinay-oḥ |
| 6.2.166 | VARIANTS | 0.750 | vyavāyino 'ntaram | vy-av-ā-y-in-aḥ=antaram |
| 6.2.167 | VARIANTS | 0.688 | mukhaṃ svāṅgaṃ | mukha-ṃ sva=aṛga-m |
| 6.2.168 | AGREES | 0.958 | na avyaya-dikśabda-go-mahat-sthūla-muṣṭi-pṛthu-vatsebhyaḥ | na=a-vy-aya=dik=śabda-go-mahat-sthū-la-muṣṭi-pṛthu-vatse-bhyaḥ |
| 6.2.169 | VARIANTS | 0.867 | niṣṭhā-upamānād anyatarasyām | niṣṭhā=upa-mā-n-āt=nya-tara-syām |
| 6.2.170 | VARIANTS | 0.831 | jāti-kāla-sukha-ādibhyo 'nācchādanāt kto 'kṛta-mita-pratipannāḥ | jā-ti-kāla-sukha=ādi-bhyaḥ=an-ā-cchād-an-āt Kta-ḥ=a-kṛ-ta-mi-ta-prati-pan-n-ā-ḥ |
| 6.2.171 | VARIANTS | 0.875 | vā jāte | vā jā-t-e |
| 6.2.172 | AGREES | 0.909 | nañ-subhyām | naN-subhyām |
| 6.2.173 | AGREES | 0.917 | kapi pūrvam | kaP-i pūrva-m |
| 6.2.174 | VARIANTS | 0.808 | hrasvānte 'ntyāt pūrvam | hrasva=ant-e ant-y-āt pūrva-m |
| 6.2.175 | VARIANTS | 0.839 | bahor nañvad uttarapadabhūmni | baho-r naÑ-vat=t-tara-pada-hūmn-i |
| 6.2.176 | VARIANTS | 0.783 | na guṇādayo 'vayavāḥ | na guṇa=āday-aḥ=ava-yav-āḥ |
| 6.2.177 | VARIANTS | 0.829 | upasargāt svāṅgaṃ dhruvam aparśu | upa-sarg-āt sva=aṛgam dhruva-m a-parśu |
| 6.2.178 | VARIANTS | 0.889 | vanaṃ samāse | vana-ṃ sam-ās-e |
| 6.2.179 | AGREES | 1.000 | antaḥ | antaḥ |
| 6.2.180 | VARIANTS | 0.824 | antaś ca | anta-s=ca |
| 6.2.181 | AGREES | 1.000 | na ni-vi-bhyām | na ni-vi-bhyām |
| 6.2.182 | AGREES | 0.929 | parer abhitobhāvi maṇḍalam | pare-r abhito-bhāv-i-maṇḍala-m |
| 6.2.183 | VARIANTS | 0.741 | prād-asvaṅgaṃ sañjñāyām | pr-ā-t=a-sva=aṛga-ṃ saṃjñā-y-ām |
| 6.2.184 | VARIANTS | 0.857 | nirudakādīni ca | nir-udaka=ādī-n-i ca |
| 6.2.185 | AGREES | 0.923 | abher mukham | abhe-r mukha-m |
| 6.2.186 | VARIANTS | 0.800 | apāc ca | ap-āt=ca |
| 6.2.187 | AGREES | 0.914 | sphiga-pūta-vīṇā-añjo 'dhva-kukṣi-sīranāma-nāma ca | sphiga-pū-ta-vīṇā-añjas=adhva(n)=kukṣi-sīra-nāma-nāma ca |
| 6.2.188 | AGREES | 0.914 | adher uparistham | adhe-r upari-stha-m |
| 6.2.189 | VARIANTS | 0.863 | anor apradhānakanīyasī | ano-r a-pra-dhā-na-kan-īyas-ī |
| 6.2.190 | VARIANTS | 0.870 | puruṣaś ca anvādiṣṭaḥ | puruṣas=ca anv=ā-diṣ-ṭa-ḥ |
| 6.2.191 | AGREES | 0.903 | ater akṛt-pade | ate-r a-kṛt-pad-e |
| 6.2.192 | VARIANTS | 0.828 | ner anidhāne | ne-r a-ni-dhā-n-e |
| 6.2.193 | AGREES | 0.915 | prater aṃśv-ādayas tatpuruṣe | prate-r aṃśu=āday-as tatpuruṣ-e |
| 6.2.194 | VARIANTS | 0.831 | upād dvyaj-ajinam agaurādayaḥ | up-āt dvy-aC=ajina-m a-gaura-āday-aḥ |
| 6.2.195 | VARIANTS | 0.848 | sor avakṣepaṇe | so-r ava-kṣep-a-ṇ-e |
| 6.2.196 | AGREES | 0.941 | vibhāṣā+utpucche | vibhāṣā=ut-pucch-e |
| 6.2.197 | VARIANTS | 0.892 | dvi-tribhyāṃ pād-dan-mūrdhasu bahuvrīhau | dvi-tri-bhyām pad-dat=mūrdha-su bahuvrīh-au |
| 6.2.198 | VARIANTS | 0.837 | sakthaṃ ca akrāntāt | saktha-ṃ ca=a-kra=ant-āt |
| 6.2.199 | VARIANTS | 0.868 | parādiś chandasi bahulam | para=ādi-s=chandas-i bahula-m |
| 6.3.1 | VARIANTS | 0.824 | alug uttarapade | a-luK=udttara-pad-e |
| 6.3.2 | AGREES | 0.917 | pañcamyāḥ stokādibhyaḥ | pañcamy-āḥ stoka=ādi-bhyaḥ |
| 6.3.3 | VARIANTS | 0.849 | ojaḥ-saho 'mbhas-tamasas tṛtīyayāḥ | ojas=sahas=ambhas=tamas-as tṛ-tīya-y-āḥ |
| 6.3.4 | VARIANTS | 0.789 | manasaḥ sañjñāyām | man-as-as=saṃjñā-y-ām |
| 6.3.5 | VARIANTS | 0.846 | ājñāyini ca | ā-jñā-y-in-i ca |
| 6.3.6 | VARIANTS | 0.842 | ātmanaś ca pūraṇe | āt-man-as=ca pūr-aṇ-e |
| 6.3.7 | VARIANTS | 0.824 | vaiyākaraṇākhyāyāṃ caturthyāḥ | vai-y-ā-kar-aṇa=ā-khyā-y-ām caturthy-āḥ |
| 6.3.8 | AGREES | 0.952 | parasya ca | para-sya ca |
| 6.3.9 | VARIANTS | 0.866 | hal-adantāt saptamyāḥ sañjñāyām | haL=aT=ant-āt saptamy-āḥ saṃjñā-y-ām |
| 6.3.10 | AGREES | 0.933 | kāranāmni ca prācāṃ hal-ādau | kāra-nāmn-i ca prāc-āṃ haL=ād-au |
| 6.3.11 | AGREES | 0.929 | madhyād gurau | madhy-ād gur-au |
| 6.3.12 | VARIANTS | 0.725 | amūrdha-mastakāt svāṅgād akāme | a-mūrdha(n)=mastak-āt sva=aṛg-āt a-kām-e |
| 6.3.13 | AGREES | 0.944 | bhandhe ca vibhāṣā | bandh-e ca vibhāṣā |
| 6.3.14 | AGREES | 0.936 | tatpuruṣe kṛti bahulam | tatpuruṣ-e kṛt-i bahula-m |
| 6.3.15 | VARIANTS | 0.873 | prāvṛṭ-śarat-kāla-divāṃ je | prā-vṛṣ=śarad-kāla-div-āṃ j-e |
| 6.3.16 | CONFLICTS | 0.263 | vibhāṣā | vibhaṣa varṣa-kṣara-śara-var-āt |
| 6.3.17 | AGREES | 0.909 | gha-kāla-tanesu kālanāmnaḥ | GHA-kāla-tane-ṣu kāla-nāmn-aḥ |
| 6.3.18 | VARIANTS | 0.857 | śaya-vāsa-vāsiṣv akalāt | śaya-vāsa-vāsi-ṣu=a-kāl-āt |
| 6.3.19 | VARIANTS | 0.868 | na-in-siddha-badhnātiṣu ca | na=in=sid-dha-badh-nā-ti-ṣu |
| 6.3.20 | AGREES | 0.914 | sthe ca bhāṣāyām | sth-e ca bhāṣā-y-ām |
| 6.3.21 | VARIANTS | 0.812 | ṣaṣṭhyā ākrośe | ṣaṣṭhy-āḥ=ā-kroś-e |
| 6.3.22 | VARIANTS | 0.872 | putre 'nyatarasyām | putr-e anya-tara-syām |
| 6.3.23 | VARIANTS | 0.867 | ṛto vidyāyonisambandhebhyaḥ | ṛT-o vid-y-ā-yoni-sam-bandhe-hyaḥ |
| 6.3.24 | AGREES | 0.976 | vibhāṣā svasṛ-patyoḥ | vibhāṣā svasṛ=paty-oḥ |
| 6.3.25 | VARIANTS | 0.743 | anaṅ ṛto dvandve | ānaṄ ṛT-aḥ=dvaṃdv-e |
| 6.3.26 | VARIANTS | 0.857 | devatādvandve ca | deva-tā-dvaṃdv-e ca |
| 6.3.27 | VARIANTS | 0.870 | īdagneḥ somavaruṇayoḥ | īT=agne-ḥ soma-varuṇay-oḥ |
| 6.3.28 | VARIANTS | 0.818 | id vṛddhau | iT=vṛd-dh-au |
| 6.3.29 | VARIANTS | 0.727 | devo dyāvā | div-aḥ=dyāvā |
| 6.3.30 | AGREES | 0.905 | divasaś ca pṛthivyām | divasa-s=ca pṛthivy-ām |
| 6.3.31 | AGREES | 0.960 | uṣāsā-uṣasaḥ | uṣāsā=uṣas-aḥ |
| 6.3.32 | VARIANTS | 0.818 | mātara-pitarāv udīcam | mātara-pitar-au udīc-ām |
| 6.3.33 | AGREES | 0.962 | pitarā-mātarā ca cchandasi | pitarā-mātarā ca=chandas-i |
| 6.3.34 | VARIANTS | 0.824 | striyāḥ puṃvad-bhāṣītapuṃskādanūṅ samānādhikaraṇe striyām apūraṇī-priyādiṣu | striy-āḥ puṃ-vat=hāṣ-i-ta-puṃsk-āt an-ūṄ sa-mā-na=adhi-kar-aṇ-e striy-ām a-pūr-aṇī-priyā=ādi-ṣu |
| 6.3.35 | AGREES | 0.920 | tasil-ādiṣv ā kṛtvasucaḥ | tasiL=ādi-ṣu ā kṛtvasuC-aḥ |
| 6.3.36 | VARIANTS | 0.875 | kyaṅ-māninoś ca | KyaṄ=mān-in-os=ca |
| 6.3.37 | VARIANTS | 0.774 | na kopadhāyāḥ | na ka=upa-dhā-y-āḥ |
| 6.3.38 | VARIANTS | 0.865 | sañjñā-pūraṇyoś ca | saṃjñā-pūraṇy-os=ca |
| 6.3.39 | VARIANTS | 0.845 | vṛddhinimittasya ca taddhitasyāraktavikāre | vṛd-dhi-ni-mit-ta-sya ca taddhita-sya a-rak-ta-vi-kār-e |
| 6.3.40 | CONFLICTS | 0.577 | svāṅgāc ca+ito 'mānini | sva=aṛg-āt=ca īT-aḥ=a-mān-in-i |
| 6.3.41 | VARIANTS | 0.824 | jāteś ca | jāte-s=ca |
| 6.3.42 | AGREES | 0.959 | puṃvat karmadhāraya-jātīya-deśīyeṣu | puṃ-vat karma-dhāraya-jātīya-deśīye-ṣu |
| 6.3.43 | VARIANTS | 0.791 | gharūpakalpacelaḍbrūvagotramatahateṣu ṅyo 'nekāco hrasvaḥ | GHA-rūpa-kalpa-celaṬ-bruva-gotra-mata-hate-ṣu Ṅyaḥ=an-eka=aC-aḥ hrasva-ḥ |
| 6.3.44 | AGREES | 0.931 | nadyāḥ śeṣasya anyatarasyām | nady-āḥ śeṣa-sya=anya-tara-syām |
| 6.3.45 | VARIANTS | 0.762 | ug-itaś ca | uK=IT-as=ca |
| 6.3.46 | VARIANTS | 0.769 | ānmahataḥ samānādhikaranajātīyayoḥ | āT=mahat-aḥ sa-mā-na=adhi-kar-aṇa-jatīyay-oḥ |
| 6.3.47 | VARIANTS | 0.884 | dvyaṣṭanaḥ saṅkhyāyām abahuvrīhy-aśītyoḥ | dvy-aṣṭan-aḥ saṃkhyā-y-ām a-bahuvrīhi=aśīty-oḥ |
| 6.3.48 | AGREES | 0.957 | tres trayaḥ | tre-s trayaḥ |
| 6.3.49 | AGREES | 0.937 | vibhāṣā catvāriṃśatprabhṛtau sarveṣām | vibhāṣā catvāriṃśat-pra-bhṛ-t-au sarve-ṣām |
| 6.3.50 | AGREES | 0.912 | hṛdayasya hṛl lekha-yad-aṇ-lāseṣu | hṛdaya-sya hṛd=lekha-yaT=aṆ-lāse-ṣu |
| 6.3.51 | AGREES | 0.974 | vā śoka-ṣyañ-rogeṣu | vā śoka-ṢyaÑ-roge-ṣu |
| 6.3.52 | VARIANTS | 0.886 | pādasya pada-ājy-āti-ga-upahatesu | pāda-sya pada=āji=āti=ga-upa-ha-te-ṣu |
| 6.3.53 | VARIANTS | 0.850 | pad yaty atadarthe | pad yaT-i=a-tad-arth-e |
| 6.3.54 | AGREES | 0.900 | hima-kāṣi-hatisu ca | hima-kāṣi-ha-ti-ṣu ca |
| 6.3.55 | VARIANTS | 0.875 | ṛcaḥ śe | ṛc-aḥ ś-e |
| 6.3.56 | AGREES | 0.930 | vā ghoṣamiśraśabdeṣu | vā ghoṣa-miśra-śabde-ṣu |
| 6.3.57 | VARIANTS | 0.880 | udakasya+udaḥ sañjñāyām | udaka-sya uda-ḥ saṃjñā-y-ām |
| 6.3.58 | VARIANTS | 0.885 | peṣam-vāsa-vāhana-dhiṣu ca | peṣam-vās-a-vāh-ana-dhi-ṣu |
| 6.3.59 | VARIANTS | 0.868 | ekahal-ādau pūrayitavye 'nyatarasyām | eka-haL=ād-au pūr-ay-i-tavye=nya-ara-yām |
| 6.3.60 | AGREES | 0.983 | mantha-odana-saktu-bindu-vajra-bhāra-hāra-vīvadha-gāheṣu ca | mantha=odana-saktu-bindu-vajra-bhāra-hār-a-vīvadha-gāhe-ṣu ca |
| 6.3.61 | VARIANTS | 0.724 | iko hrasvo 'ṅyo gālavasya | iK-aḥ=hrasva-ḥ=a-Ṅy-aḥ gālava-sya |
| 6.3.62 | AGREES | 0.968 | eka taddhite ca | eka taddhit-e ca |
| 6.3.63 | VARIANTS | 0.812 | ṅyāpoḥ sañjñāchandasor bahulam | Ṅī=āP-oḥ saṃjñā-chandas-oḥ=ahula-m |
| 6.3.64 | AGREES | 0.923 | tve ca | tv-e ca |
| 6.3.65 | AGREES | 0.900 | iṣṭakā-iṣīkā-mālānāṃ citatūlabhāriṣu | iṣṭa-kā=iṣī-kā-mālā-n-āṃ cita-tūla-bhār-i-ṣu |
| 6.3.66 | VARIANTS | 0.600 | khity anavyayasya | KH-IT-i=an-a-vy-aya-sya |
| 6.3.67 | VARIANTS | 0.824 | arur-dviṣad-ajantasya mum | arus=dviṣat=aC=nta=sya muM |
| 6.3.68 | VARIANTS | 0.679 | ica ekāco 'mpratyayavac ca | iC-aḥ=eka=aC-aḥ=m-ratyaya-at=a |
| 6.3.69 | VARIANTS | 0.776 | vācaṃyama-purandarau ca | vāca-ṃ-yam-a-pura-ṃ-dar-au |
| 6.3.70 | AGREES | 0.950 | kāre satya-agadasya | kār-e sat-ya=agadasya |
| 6.3.71 | AGREES | 0.933 | śyena-tilasya pāte ñe | śyena-tila-sya pāt-e Ñ-e |
| 6.3.72 | AGREES | 0.950 | rātreḥ kṛti vibhāṣā | rātre-ḥ kṛt-i vibhāṣā |
| 6.3.73 | VARIANTS | 0.786 | nalopo nañaḥ | na-lop-aḥ naÑ-aḥ |
| 6.3.74 | VARIANTS | 0.828 | tasmān nuḍ aci | ta-smāt=nuṬ=aCi |
| 6.3.75 | VARIANTS | 0.878 | nabhrāṇ-napān-navedā-nāsatyā-namuci-nakula-nakha-napuṃsaka-nakṣatra-nakra-nākeṣu prakṛtyā | na-bhrāj=na-pāt=na-vedas=nā-satyā-na-muc-i-na-kula-na-kha-na-puṃs-aka-na-kṣatra-na-kra-nā-ke-ṣu pra-kṛ-ty-ā |
| 6.3.76 | VARIANTS | 0.885 | ekādiś ca+ekasya ca āduk | eka=ādi-s=ca=eka-sya ca=āduK |
| 6.3.77 | VARIANTS | 0.714 | nago 'prāṇiṣv anyatarasyām | na-ga-ḥ=a-prāṇi-ṣu=nya-ara-yām |
| 6.3.78 | VARIANTS | 0.870 | sahasya saḥ sañjñāyām | saha-sya sa-ḥ saṃjñā-y-ām |
| 6.3.79 | VARIANTS | 0.864 | granthānta-adhike ca | grantha=anta=adhi-k-e ca |
| 6.3.80 | VARIANTS | 0.708 | dvitīye ca anupākhye | dvi-tīy-e ca=an-upa=aty-ay-e |
| 6.3.81 | VARIANTS | 0.810 | avyayībhāve cākāle | avyayī-bhāv-e ca=a-kāl-e |
| 6.3.82 | AGREES | 0.914 | vā+upasarjanasya | vā=upa-sarj-ana-sya |
| 6.3.83 | VARIANTS | 0.879 | prakṛtyā āśiṣy ago-vatsa-haleṣu | pra-kṛ-ty-ā āśiṣ-i=-go-vatsa-hale-ṣu |
| 6.3.84 | VARIANTS | 0.854 | samānasya chandasy apūrdha-prabhṛty-udarkeṣu | samāna-sya chandas-i a-mūrdha(n)=pra-bhṛ-ti=udarke-ṣu |
| 6.3.85 | AGREES | 0.938 | jyotir-janapada-rātri-nābhi-nāma-gotra-rūpa-sthāna-varṇa-varyo-vacana-bandhuṣu | jyotis-janapada-rātri-nābhi-nāma(n)=gotra-rūpa-sthāna-varṇa-vayas-vac-ana-bandhu-ṣu |
| 6.3.86 | VARIANTS | 0.884 | caraṇe brahmacāriṇi | car-aṇ-e brahma-cār-iṇ-i |
| 6.3.87 | AGREES | 0.900 | tīrthe ye | tīrth-e y-e |
| 6.3.88 | AGREES | 0.963 | vibhāṣā+udare | vibhāṣā=udar-e |
| 6.3.89 | AGREES | 0.903 | dṛg-dṛśa-vatuṣu | dṛś=dṛśa=vatU-ṣu |
| 6.3.90 | VARIANTS | 0.875 | idaṃ kimor īśkī | idam-kim-or īŚ-kī |
| 6.3.91 | AGREES | 0.929 | ā sarvanāmnaḥ | ā sarva-nāmn-aḥ |
| 6.3.92 | VARIANTS | 0.840 | viṣvag-devayoś ca ṭer adry añcatau vapratyaye | viṣva(ñ)c-devay-os=ca ṬE-r adri=añc-a-tau va-praty-ay-e |
| 6.3.93 | AGREES | 0.952 | samaḥ sami | sam-aḥ sami |
| 6.3.94 | VARIANTS | 0.872 | tirasas tiry alope | tiras-as tiri=a-lop-e |
| 6.3.95 | AGREES | 0.938 | sahasya sadhriḥ | saha-sya sadhri-ḥ |
| 6.3.96 | AGREES | 0.909 | sadha māda-sthayoś chandasi | sadha māda-sthay-os=handas-i |
| 6.3.97 | VARIANTS | 0.794 | dvy-antar-upasargebhyo 'pa īt | dvi=antar=upa-sarg-e-hyaḥ ap-aḥ īT |
| 6.3.98 | VARIANTS | 0.846 | ūd anor deśe | ūT=an-or deś-e |
| 6.3.99 | VARIANTS | 0.848 | aṣaṣthy-atṛtīyāsthasya anayasya dug āśīr-āśā-āsthā-āsthita-utsuka-ūti-kāraka-rāga-ccheṣu | a-ṣaṣṭhī=a-tṛ-tīya-sthasya=nya-sya duKāśis=āśā=ā-sthā=ā-sthi-ta=ut-su-ka=ūti-kār-aka-rāga=che-ṣu |
| 6.3.100 | AGREES | 0.963 | arthe vibhāṣā | arth-e vibhāṣā |
| 6.3.101 | VARIANTS | 0.889 | koḥ kat tatpuruṣe 'ci | ko-ḥ kat tatpuruṣ-e=aC-i |
| 6.3.102 | AGREES | 0.909 | ratha-vadayoś ca | ratha-vaday-os=ca |
| 6.3.103 | VARIANTS | 0.828 | dṛṇe ca jātau | tṛṇ-e ca jā-t-au |
| 6.3.104 | VARIANTS | 0.857 | kā pathy-akṣayoḥ | kā pathi(n)=akṣay-oḥ |
| 6.3.105 | VARIANTS | 0.783 | īṣadarthe ca | īṣad-arth-e |
| 6.3.106 | AGREES | 0.966 | vibhāṣā puruṣe | vibhāṣā puruṣ-e |
| 6.3.107 | VARIANTS | 0.615 | kavañcoṣṇe | kava-ṃ ca=uṣ-ṇ-e |
| 6.3.108 | AGREES | 0.919 | pathi ca cchandasi | path-i ca=chandas-i |
| 6.3.109 | VARIANTS | 0.831 | pṛṣodara-ādīni yathopadiṣṭam | pṛṣ-o-dara=ādī-n-i yath-o-pa-diṣ-ta-m |
| 6.3.110 | AGREES | 0.904 | saṅkhyā-vi-sāya-pūrvasya ahnasya ahann anyatarasyāṃ ṅau | saṃ-khyā-vi-sāy-a=ūrva-sya ahna-sya ahan anya-tara-syāṃ Ṅ-au |
| 6.3.111 | VARIANTS | 0.844 | ḍhralope pūrvasya dīrgho 'ṇaḥ | ḍh-ra-lop-e pūrva-sya dīrgha-ḥ=Ṇ-aḥ |
| 6.3.112 | VARIANTS | 0.898 | sahi-vahor od avarṇasya | sahi-vah-or oT=a-varṇa-sya |
| 6.3.113 | AGREES | 0.912 | sāḍhyai sāḍhvā sāḍha+iti nigame | sā-ḍhyai sā-ḍvhvā sā-ḍha=iti ni-gam-e |
| 6.3.114 | VARIANTS | 0.800 | saṃhitāyām | saṃ-hi-t-ā-y-ām |
| 6.3.115 | AGREES | 0.901 | karṇe lakṣaṇasya aviṣṭa-aṣṭa-pañca-maṇi-bhinna-cchinna-cchidra-sruva-svastikasya | karṇ-e lakṣana-sya a-viṣ-ṭa-aṣṭa(n)-pañca(n)=maṇi-bhin-na-chin-na-chid-ra-sruva-svasti-ka-sya |
| 6.3.116 | AGREES | 0.977 | nahi-vṛti-vṛṣi-vyadhi-ruci-sahi-taniṣu kvau | nahi-vṛti-vṛṣi-vyadhi-ruci-sahi-tani-ṣu Kv-au |
| 6.3.117 | VARIANTS | 0.891 | vana-giryoḥ sajñāyāṃ koṭara-kiṃśulukādīnām | vana-giry-oḥ saṃjñā-y-āṃ koṭara-kiṃśulaka=ādī-n-ām |
| 6.3.118 | VARIANTS | 0.889 | vale | val-e |
| 6.3.119 | VARIANTS | 0.787 | matau bahvaco 'najirādīnām | mat-AU bahv-aC-aḥ=an-ajira=ādī-n-ām |
| 6.3.120 | VARIANTS | 0.786 | śarādīnām ca | śara=ādī-n-āṃ ca |
| 6.3.121 | VARIANTS | 0.743 | iko vahe 'pīloḥ | iK-aḥ=vah-e=a-pīl-oḥ |
| 6.3.122 | VARIANTS | 0.865 | upasargasya ghañyamanuṣye bahulam | upa-sarg-a-sya GHaÑ-i=a-manuṣy-e bahula-m |
| 6.3.123 | AGREES | 0.900 | ikaḥ kāśe | iK-aḥ kāś-e |
| 6.3.124 | VARIANTS | 0.857 | das ti | d-as t-i |
| 6.3.125 | VARIANTS | 0.865 | aṣṭanaḥ sañjñāyām | aṣṭan-aḥ saṃjñā-y-ām |
| 6.3.126 | AGREES | 0.957 | chandasi ca | chandas-i ca |
| 6.3.127 | AGREES | 0.909 | citeḥ kapi | cite-ḥ kaP-i |
| 6.3.128 | AGREES | 0.950 | viśvasya vasu-rāṭoḥ | viśva-sya vasu-rāṭ-oḥ |
| 6.3.129 | VARIANTS | 0.839 | nare sañjñāyām | nar-e saṃjñā-y-ām |
| 6.3.130 | VARIANTS | 0.815 | mitre carṣau | mitr-e ca=ṛṣ-au |
| 6.3.131 | AGREES | 0.933 | mantre soma-aśva-indriya-viśvadevyasya matau | mantr-e soma=aśva=indriya=viśva-evya-ya mat-AU |
| 6.3.132 | VARIANTS | 0.806 | oṣadheś ca vibhaktāv aprathamāyām | oṣsadhe-s=ca vi-bhak-t-au=a-prathamā--ām |
| 6.3.133 | VARIANTS | 0.816 | ṛci tunughamakṣutaṅkutroruṣyāṇām | ṛc-i tu-nu-gha-makṣu-taṄ-ku-tra=uruṣ-yā-ṇ-ām |
| 6.3.134 | AGREES | 0.900 | ikaḥ suñi | iK-aḥ suÑ-i |
| 6.3.135 | VARIANTS | 0.737 | dvyaco 'tastiṅaḥ | dvy-aC-aḥ=aT-as tiṄ-aḥ |
| 6.3.136 | VARIANTS | 0.889 | nipātasya ca | ni-pāt-a-sya ca |
| 6.3.137 | AGREES | 0.927 | anyeṣām api dṛśyate | anye-ṣām api dṛś-ya-te |
| 6.3.138 | VARIANTS | 0.857 | cau | c-au |
| 6.3.139 | VARIANTS | 0.882 | samprasāraṇasya | sam-pra-sār-aṇa-sya |
| 6.4.1 | VARIANTS | 0.800 | aṅgasya | aṛga-sya |
| 6.4.2 | AGREES | 0.909 | halaḥ | haL-aḥ |
| 6.4.3 | VARIANTS | 0.889 | nāmi | nām-i |
| 6.4.4 | AGREES | 1.000 | na tisṛ-catasṛ | na tisṛ-catasṛ |
| 6.4.5 | VARIANTS | 0.895 | chandasy ubhayathā | chandas-i ubhaya-thā |
| 6.4.6 | AGREES | 1.000 | nṛ ca | nṛ ca |
| 6.4.7 | VARIANTS | 0.889 | na-upadhāyāḥ | na=upa-dhā-y-āḥ |
| 6.4.8 | VARIANTS | 0.896 | sarvanāmasthāne ca asambuddhau | sarva-nāma-sthān-e ca=a-sam-bud-dh-au |
| 6.4.9 | AGREES | 0.909 | vā ṣapūrvasya nigame | vā ṣa-pūrva-sya ni-gam-e |
| 6.4.10 | VARIANTS | 0.830 | sāntamahataḥ saṃyogasya | sa=anta-mahat-aḥ saṃ-yog-a-sya |
| 6.4.11 | AGREES | 0.921 | ap-tṛn-tṛc-svasṛ-naptṛ-neṣṭṛ-tvaṣṭṛ-kṣattṛ-hotṛ-potṛ-praśāstṝṇām | ap-tṛN-tṛC-svasṛ-nap-tṛ-neṣ-ṭṛ-tvaṣ-ṭṛ-kṣat-tṛ=ho-tṛ-po-tṛ-pra-śās-t ṝ-ṇ-ām |
| 6.4.12 | AGREES | 0.906 | in-han-pūṣa-aryamṇāṃ śau | in-han-pūṣa(n)=arya-mṇ-āṃ Ś-au |
| 6.4.13 | AGREES | 0.923 | sau ca | s-AU ca |
| 6.4.14 | VARIANTS | 0.885 | atv-asantasya ca adhātoḥ | atU=as-anta-sya ca=a-dhāto-ḥ |
| 6.4.15 | VARIANTS | 0.892 | anunāsikasya kvi-jhaloḥ kṅiti | anu-nās-ika-sya Kvi-jhaL-oḥ K-Ṅ-IT-i |
| 6.4.16 | VARIANTS | 0.821 | aj-jhana-gamāṃ sani | aC=hanḥ-gam-āṃ saN-i |
| 6.4.17 | AGREES | 0.909 | tanoter vibhāṣā | tan-o-te-r vibhāṣā |
| 6.4.18 | VARIANTS | 0.867 | kramaś ca ktvi | kram-as=ca Ktv-i |
| 6.4.19 | VARIANTS | 0.807 | ccḥ-voḥ ś-ūḍḥ-anunāsike ca | c-ch-v-oḥ ś-ūṬH=anu-nās-ik-e ca |
| 6.4.20 | VARIANTS | 0.867 | jvara-tvara-srivy-avi-mavām upadhāyāś ca | jvarḥ-tvara-srivi=avi-mav-ām upa-hā-y-ās=ca |
| 6.4.21 | VARIANTS | 0.800 | rāl lopaḥ | r-āt=lopa-ḥ |
| 6.4.22 | VARIANTS | 0.800 | asiddhavatra-ā bhāt | a-sid-ha-vat=a-tra=ā bh-āt |
| 6.4.23 | VARIANTS | 0.815 | śnān nalopaḥ | Śn-āt=na-lopa-ḥ |
| 6.4.24 | VARIANTS | 0.765 | aniditāṃ hala upadhāyāḥ kṅiti | an-iT=IT-ām haL-aḥ=upa-dhā-y-āḥ K-Ṅ-ITi |
| 6.4.25 | VARIANTS | 0.760 | daṃśa-sañja-svañjām śapi | danśḥ-sanjḥ-svanj-ām Śap-i |
| 6.4.26 | VARIANTS | 0.737 | rañjeś ca | ranje-s=ca |
| 6.4.27 | VARIANTS | 0.863 | ghañi ca bhāvakaranayoḥ | GHaÑ-i ca bhāv-a-kar-aṇay-oḥ |
| 6.4.28 | VARIANTS | 0.783 | syado jave | syada-ḥ jav-e |
| 6.4.29 | VARIANTS | 0.833 | avoda-edḥ-odma-praśratha-himaśrathāḥ | av-o-d-a=edh-a=od-ma(n)-pra-śrath-a-hima-śrath-āḥ |
| 6.4.30 | VARIANTS | 0.857 | na añceḥ pūjāyām | na=ance-ḥ pūjā-y-ām |
| 6.4.31 | AGREES | 0.927 | ktvi skandi-syandoḥ | Ktv-i skandi-syandy-oḥ |
| 6.4.32 | VARIANTS | 0.829 | jānta-naśāṃ vibhāṣā | ja=anta-naś-ām vibhāṣā |
| 6.4.33 | VARIANTS | 0.839 | bhañjeś ca ciṇi | bhanjes=ca CiṆ-i |
| 6.4.34 | VARIANTS | 0.788 | śāsa idaṅhaloḥ | śās-aḥ=iT=aṄ-haL-oḥ |
| 6.4.35 | AGREES | 0.923 | śā hau | śā h-au |
| 6.4.36 | VARIANTS | 0.818 | hanterjaḥ | han-te-r ja-ḥ |
| 6.4.37 | VARIANTS | 0.823 | anudātta-upadeśa-vanati-tanoty-ādīnām anunāsikalopo jhali kṅiti | an-udātta=upa-deś-a-van-a-ti-tan-o-ti=ādī-n-ām anu-ās-ka-opa-ḥ jhaL-i K-Ṅ-IT-i |
| 6.4.38 | AGREES | 0.941 | vā lyapi | vā LyaP-i |
| 6.4.39 | AGREES | 0.900 | na ktici dīrghaś ca | na KtiC-i dīrgha-s=ca |
| 6.4.40 | AGREES | 0.909 | gamaḥ kvau | gam-aḥ Kv-au |
| 6.4.41 | VARIANTS | 0.889 | viḍ-vanor anunāsikasya āt | viṬ=van-or anu-nās-ika-sya=āT |
| 6.4.42 | VARIANTS | 0.857 | jana-sana-khanāṃ sañ-jhaloḥ | janḥ-sanḥ-khan-āṃ saN=jhaL-oḥ |
| 6.4.43 | AGREES | 0.952 | ye vibhāṣā | y-e vibhāṣā |
| 6.4.44 | VARIANTS | 0.815 | tanoteryaki | tan-o-te-r yaK-i |
| 6.4.45 | VARIANTS | 0.872 | sanaḥ ktici lopaś ca asya anyatarasyām | san-aḥ KtiC-i lopa-s=ca asya=nya-ara-yām |
| 6.4.46 | VARIANTS | 0.889 | ārdhadhātuke | ārdha-dhātu-k-e |
| 6.4.47 | VARIANTS | 0.857 | bhrasjo ra-upadhayo ram anyatarasyām | bhrasj-aḥ ra=upa-dhay-oḥ raM anya-ara-yām |
| 6.4.48 | VARIANTS | 0.762 | ato lopaḥ | aT-aḥ lopa-ḥ |
| 6.4.49 | AGREES | 0.917 | yasya halaḥ | ya-sya haL-aḥ |
| 6.4.50 | AGREES | 0.966 | kyasya vibhāṣā | Kya-sya vibhāṣā |
| 6.4.51 | VARIANTS | 0.857 | ṇer aniṭi | Ṇe-r an-iṬ-i |
| 6.4.52 | VARIANTS | 0.848 | niṣṭhāyāṃ seṭi | niṣṭhā-y-āṃ s-e-Ṭ-i |
| 6.4.53 | VARIANTS | 0.897 | janitā mantre | jan-i-tā mantr-e |
| 6.4.54 | VARIANTS | 0.889 | śamitā yajñe | śam-i-tā yajñ-e |
| 6.4.55 | AGREES | 0.921 | ay ām-anta-ālv-āyya-itnv-iṣṇuṣu | ay ām=anta=ālu =āyya=itnu=iṣṇu-ṣu |
| 6.4.56 | AGREES | 0.919 | lyapi laghupūrvāt | LyaP-i laghu-pūrv-āt |
| 6.4.57 | AGREES | 0.960 | vibhāṣā+āpaḥ | vibhāṣā āp-aḥ |
| 6.4.58 | AGREES | 0.909 | yu-pluvor dīrghaś chandasi | yu-pluv-or dīrgha-s=chandas-i |
| 6.4.59 | AGREES | 0.923 | kṣiyaḥ | kṣiy-aḥ |
| 6.4.60 | VARIANTS | 0.800 | naṣṭhāyām aṇyadarthe | niṣṭhā-y-ām a-ṆyaT=arth-e |
| 6.4.61 | VARIANTS | 0.884 | vā+ākrośa-dainyayoḥ | vā ā-kroś-a-dai-n-yay-oḥ |
| 6.4.62 | VARIANTS | 0.854 | sya-sic-sīyuṭ-tāsiṣu bhāva-karmaṇor upadeśe 'j-jhana-graha-dṛśāṃ vā ciṇvad-iṭ ca | sya-siC-sīyuṬ-tāsi-su bhāv-a-kar-maṇ-oḥ upa-deś-e aC=hanḥ-grahA-dṛś-āṃ CiṆ-vat=iṬ ca |
| 6.4.63 | VARIANTS | 0.732 | dīṅo yuḍaci kṅiti | dīṄ-aḥ yuṬ=aC-i K-Ṅ-IT-i |
| 6.4.64 | VARIANTS | 0.800 | āto lopa iṭi ca | āT-aḥ lopa-ḥ iṬ-i ca |
| 6.4.65 | VARIANTS | 0.714 | īdyati | īT=yaT-i |
| 6.4.66 | AGREES | 0.928 | ghu-mā-sthā-gā-pā-jahāti-sā hali | GHU-mā-sthā-gā-pā-ja-hā-ti-s-āṃ haL-i |
| 6.4.67 | VARIANTS | 0.875 | er liṅi | e-r lIṄ-i |
| 6.4.68 | VARIANTS | 0.880 | vā 'nyasya saṃyoga-ādeḥ | vā anya-sya saṃ-yog-a=āde-ḥ |
| 6.4.69 | AGREES | 0.941 | na lyapi | na LyaP-i |
| 6.4.70 | VARIANTS | 0.863 | mayater id-anyatarasyām | may-a-te-r iT=anya-tara-syām |
| 6.4.71 | VARIANTS | 0.852 | luṅ-laṅ-lṛṅ-kṣv aḍ-udāttaḥ | lUṄ-lIṄ=lṚṄ-k-ṣu=aṬ=udātta-ḥ |
| 6.4.72 | VARIANTS | 0.769 | āḍ aj-ādīnām | āṬ aC=ādī-n-ām |
| 6.4.73 | VARIANTS | 0.884 | chandasy api dṛśyate | chandas-i=api dṛś-ya-te |
| 6.4.74 | AGREES | 0.909 | na māṅyoge | na māṄ-yog-e |
| 6.4.75 | VARIANTS | 0.889 | bahulaṃ chandasy amāṅyoge 'pi | bahula-ṃ chandas-y a-māṄ-yog-e=api |
| 6.4.76 | VARIANTS | 0.778 | irayo re | iray-aḥ re |
| 6.4.77 | AGREES | 0.902 | aci śnu-dhātu-bhruvāṃ y-vor iyaṅ-uvaṅau | aC-i Śnu-dhātu-bhruv-ām y-v-or iyaṄ=unaṄ-au |
| 6.4.78 | VARIANTS | 0.864 | abhyāsasya asavarṇe | abhy-ās-a-sya=a-sa-varṇ-e |
| 6.4.79 | AGREES | 0.933 | striyāḥ | striy-āḥ |
| 6.4.80 | VARIANTS | 0.727 | vā 'ṃśasoḥ | vā am-Śas-oḥ |
| 6.4.81 | VARIANTS | 0.750 | iṇo yaṇ | iṆ-aḥ yaṆ |
| 6.4.82 | VARIANTS | 0.635 | er anekāco 'samyogapūrvasya | e-ḥ an-eka=aC-aḥ=a-saṃ-og-a-ūrva-sya |
| 6.4.83 | VARIANTS | 0.875 | oḥ supi | o-ḥ sUP-i |
| 6.4.84 | VARIANTS | 0.857 | varṣābhvaś ca | varṣā-bhv-as=ca |
| 6.4.85 | AGREES | 0.903 | na bhūsudhiyoḥ | na bhū-su-dhiy-oḥ |
| 6.4.86 | VARIANTS | 0.872 | chandasy ubhayathā | chandas-i ubha-ya-thā |
| 6.4.87 | VARIANTS | 0.894 | huśnuvoḥ sārvadhātuke | hu-Śnuv-oḥ sārva-dhātu-k-e |
| 6.4.88 | VARIANTS | 0.800 | bhuvo vug luṅliṭoḥ | bhuv-aḥ vuK lUṄ-lIṬ-oḥ |
| 6.4.89 | VARIANTS | 0.821 | ūd upadhāyā gohaḥ | ūT=upa-dhā-y-āḥ goh-aḥ |
| 6.4.90 | VARIANTS | 0.737 | doṣo ṇau | doṣ-aḥ Ṇ-au |
| 6.4.91 | VARIANTS | 0.875 | vā cittavirāge | vā cit-ta-vi-rāg-e |
| 6.4.92 | VARIANTS | 0.897 | mitāṃ hrasvaḥ | M-IT-āṃ hrasva-ḥ |
| 6.4.93 | VARIANTS | 0.866 | ciṇ-ṇamulor dīrgho 'nyatarasyām | CiṆ- ṆamuL-or dīrgha-ḥ=anya-tara-syām |
| 6.4.94 | AGREES | 0.929 | khaci hrasvaḥ | KHaC-i hrasva-ḥ |
| 6.4.95 | VARIANTS | 0.824 | hlādo niṣṭhāyām | hlād-aḥ niṣṭhā-y-ām |
| 6.4.96 | VARIANTS | 0.833 | chāder ghe 'dvy-upasargasya | chād-e-r GHe a-dvi=upa-sarg-a-sya |
| 6.4.97 | AGREES | 0.976 | is-man-tran-kviṣu ca | is-man-traN-kvi-ṣu ca |
| 6.4.98 | VARIANTS | 0.887 | gama-hana-jana-khana-ghasāṃ lopaḥ kṅity anaṅi | gama-hanḥ-jana-khana-ghas-āṃ lopa-ḥ K-Ṅ-IT-i an-aṄ-i |
| 6.4.99 | AGREES | 0.905 | tani-patyoś chandasi | tani-paty-os=chandas-i |
| 6.4.100 | AGREES | 0.952 | ghasi-bhasor hali ca | ghasi-bhas-or haL-i ca |
| 6.4.101 | VARIANTS | 0.864 | hu-jhalbhyo her dhiḥ | hu-jhaL-bhyaḥ=he-r dhi-ḥ |
| 6.4.102 | AGREES | 0.923 | śru-śṛṇu-pṝ-kṛ-vṛbhyaś chandasi | śru-śṛ-ṇu-pṝ-kṛ-vṛ-bhyas=chandas-i |
| 6.4.103 | VARIANTS | 0.762 | aṅitaś ca | a-Ṅ-IT=as=ca |
| 6.4.104 | VARIANTS | 0.778 | ciṇo luk | CiṆ-aḥ luK |
| 6.4.105 | VARIANTS | 0.706 | ato heḥ | aT-aḥ he-ḥ |
| 6.4.106 | VARIANTS | 0.829 | utaś ca pratyayād asaṃyogapūrvāt | uT-as=ca praty-ay-āt=a-saṃyog-a-ūrv-āt |
| 6.4.107 | VARIANTS | 0.824 | lopaś ca asya anyatarasyāṃ ṃvoḥ | lopa-s=ca=a-sya=anya-tara-syām m-v-oḥ |
| 6.4.108 | VARIANTS | 0.875 | nityaṃ karoteḥ | nitya-ṃ kar-o-te-ḥ |
| 6.4.109 | AGREES | 0.909 | ye ca | y-e ca |
| 6.4.110 | VARIANTS | 0.884 | ata ut sārvadhātuke | aT-aḥ uT sārva-dhātu-k-e |
| 6.4.111 | VARIANTS | 0.750 | śnasorallopaḥ | Śna=as-or aT=lopa-ḥ |
| 6.4.112 | AGREES | 0.933 | śnā-abhyas tayor ātaḥ | Śnā=abhy-as-tay-or āT-aḥ |
| 6.4.113 | VARIANTS | 0.692 | ī halyadhoḥ | ī haL-i=a-GHO-ḥ |
| 6.4.114 | VARIANTS | 0.889 | id daridrasya | iT=daridra-sya |
| 6.4.115 | VARIANTS | 0.750 | bhiyo 'nyatarasyam | bhiy-aḥ=anya-tara-syām |
| 6.4.116 | VARIANTS | 0.783 | jahāteś ca | ja-hā-te-s=ca |
| 6.4.117 | AGREES | 0.941 | ā ca hau | ā ca h-au |
| 6.4.118 | VARIANTS | 0.706 | lopo yi | lopa-ḥ=y-i |
| 6.4.119 | VARIANTS | 0.746 | ghv-asor ed-dhāv abhyāsalopaś ca | GHU=as-or eT=h-au=bhy-ās-a-opa-s=ca |
| 6.4.120 | VARIANTS | 0.838 | ata ekahalmadhye 'nādeśāder liṭi | aT-aḥ eka-haL-madhy-e=an-ādeśa=āde-r lIṬ-i |
| 6.4.121 | VARIANTS | 0.733 | thali ca seti | thaL-i ca sa=iṬ-i |
| 6.4.122 | VARIANTS | 0.857 | tṝ-phala-bhaja-trapaś ca | tṝ-phalḥ-bhajḥ-trap-as=ca |
| 6.4.123 | VARIANTS | 0.750 | radho hiṃsāyām | rādh-aḥ hiṃsā-y-ām |
| 6.4.124 | AGREES | 0.923 | vā jṝ-bhramu-trasām | vā jṝ-bhramḥ-tras-ām |
| 6.4.125 | AGREES | 0.923 | phaṇāṃ ca saptānām | phaṇ-āṃ ca saptā-n-ām |
| 6.4.126 | AGREES | 0.926 | na śasa-dada-v-ādi-guṇānām | na śasa-dadA-v=ādi-guṇā-ṇ-ām |
| 6.4.127 | VARIANTS | 0.792 | arvaṇas tr-asāv-anañaḥ | arvaṇ-as tṚ=a-sAU=a-naÑ-aḥ |
| 6.4.128 | AGREES | 0.968 | maghavā bahulam | maghavā bahula-m |
| 6.4.129 | AGREES | 0.923 | bhasya | BHA-sya |
| 6.4.130 | VARIANTS | 0.842 | vakṣyati - pādaḥ pat | pād-aḥ pad- |
| 6.4.131 | VARIANTS | 0.837 | vasoḥ samprasāraṇaṃ | vasO-ḥ sam-pra-sār-aṇa-m |
| 6.4.132 | VARIANTS | 0.778 | vāha ūṭḥ | vāh-aḥ ūṬH |
| 6.4.133 | VARIANTS | 0.885 | śva-yuva-maghonām ataddhite | śva(n)=yuva(n)=maghon-ām a-taddhit-e |
| 6.4.134 | CONFLICTS | 0.593 | al-lopo 'naḥ | aT=lupa-ḥ an-aḥ |
| 6.4.135 | AGREES | 0.915 | ṣapūrva-han-dhṛtarājñām aṇi | ṣa-pūrva-han-dhṛ-ta-rājñ-ām aṆ-i |
| 6.4.136 | AGREES | 0.933 | vibhāṣā ṅiśyoḥ | vibhāṣā Ṅi-Śy-oḥ |
| 6.4.137 | VARIANTS | 0.894 | na saṃyogād va-m-antāt | na saṃ-yog-āt=va=m=ant-āt |
| 6.4.138 | VARIANTS | 0.889 | acaḥ | ac-aḥ |
| 6.4.139 | VARIANTS | 0.857 | uda īt | ud-aḥ īT |
| 6.4.140 | VARIANTS | 0.783 | āto dhātoḥ | āT-aḥ dhāto-ḥ |
| 6.4.141 | VARIANTS | 0.784 | mantreṣvāṅyāderātmanaḥ | mantre-ṣu āṄ-i āde-r ātman-aḥ |
| 6.4.142 | AGREES | 0.914 | ti viṃśater ḍiti | ti viṃśate-r Ḍ-IT-i |
| 6.4.143 | VARIANTS | 0.857 | ṭeḥ | ṬE-ḥ |
| 6.4.144 | AGREES | 0.923 | nas taddhite | n-as taddhit-e |
| 6.4.145 | VARIANTS | 0.833 | ahnaṣ ṭa-kher eva | ahn-as=Ṭa-kh-or eva |
| 6.4.146 | VARIANTS | 0.824 | orguṇaḥ | o-r guṇa-ḥ |
| 6.4.147 | VARIANTS | 0.769 | ḍhe lopo 'kadrvāḥ | ḍh-e lopa-ḥ a-kadrv-āḥ |
| 6.4.148 | VARIANTS | 0.815 | yasya+iti ca | y-a-sya īT-i ca |
| 6.4.149 | AGREES | 0.923 | sūrya-tiṣya-agastya-matsyānāṃ ya upadhāyāḥ | sūrya-tiṣya-agastya-matsyā-n-āṃ y-aḥ upa-dhā-y-āḥ |
| 6.4.150 | AGREES | 0.944 | halas taddhitasya | haL-as taddhita-sya |
| 6.4.151 | VARIANTS | 0.881 | āpatyasya ca taddhite 'nāti | āpat-ya-sya ca taddhit-e=an-āT-i |
| 6.4.152 | VARIANTS | 0.833 | kyacvyoś ca | Kya-Cvy-os=ca |
| 6.4.153 | AGREES | 0.912 | bilvaka-ādibhyaś chasya luk | bilva-ka=ādi-bhyas=cha-sya luK |
| 6.4.154 | VARIANTS | 0.833 | tur iṣṭha-ima-īyassu | tu-r iṣṭha(N)=ima(niC)-īyas-su |
| 6.4.155 | VARIANTS | 0.857 | ṭeḥ | ṬE-ḥ |
| 6.4.156 | AGREES | 0.919 | sthūla-dūra-yuva-hrasva-kṣiprakṣudrāṇāṃ yaṇādiparaṃ pūrvasya ca guṇaḥ | sthūla-dūra-yuva(n)=hrasva-kṣip-ra-kṣudrā-ṇ-āṃ yaṆ=ādi param pūrva-sya ca guṇa-ḥ |
| 6.4.157 | AGREES | 0.944 | priya-sthira-sphira-uru-bahula-guru-vṛddha-tṛpra-dīrgha-vṛndārakāṇāṃ pra-stha-spha-var-baṃhi-gar-varṣi-trab-drāghi-vṛndāḥ | priy-a-sthi-ra-sphi-ra-uru-bahu-la-guru-vṛd-dha-tṛp-ra-dīrgha-vṛndārakā-ṇ-ām pra-stha-spha-var-baṃhi-gar-varṣi-trap-drāghi-vṛnd-ā-ḥ |
| 6.4.158 | VARIANTS | 0.880 | bahor lopo bhū ca bahoḥ | baho-r lopa-ḥ=bhū ca baho-ḥ |
| 6.4.159 | AGREES | 0.968 | iṣṭhasya yiṭ ca | iṣṭha-sya yiṬ ca |
| 6.4.160 | VARIANTS | 0.733 | jyād ād īyasaḥ | jy-āt=āt=īyas-aḥ |
| 6.4.161 | VARIANTS | 0.851 | ra ṛto halāder laghoḥ | ra ṛT=aḥ=haL-āde-r lagho-ḥ |
| 6.4.162 | VARIANTS | 0.864 | vibhāṣā rjoś chandasi | vibhāṣā=ṛj-os=chandas-i |
| 6.4.163 | AGREES | 0.909 | prakṛtyā+eka-ac | pra-kṛ-ty-ā eka=aC |
| 6.4.164 | VARIANTS | 0.848 | in aṇy-anapatye | in aṆ-i=an-apaty-e |
| 6.4.165 | VARIANTS | 0.805 | gāthi-vidathi-keśi-gaṇi-paṇinaś ca | gāth-i(n)=vidath-i(n)=keś-i(n)-gaṇ-i(n)=paṇ-in-as=ca |
| 6.4.166 | VARIANTS | 0.848 | saṃyoga-ādiś ca | saṃ-yog-a=ādi-s=ca |
| 6.4.167 | AGREES | 1.000 | an | an |
| 6.4.168 | AGREES | 0.913 | ye ca abhāva-karmaṇoḥ | y-e ca a-bhāva-kar-maṇ-oḥ |
| 6.4.169 | VARIANTS | 0.872 | ātma-adhvānau khe | ātma(n)=adh-vān-au kh-e |
| 6.4.170 | VARIANTS | 0.787 | na mapūrvo 'patye 'varmaṇaḥ | na ma-pūrva-ḥ=apaty-e=a-var-maṇ-aḥ |
| 6.4.171 | VARIANTS | 0.688 | brāhmo 'jātau | brāhm-a-ḥ=a-jā-t-au |
| 6.4.172 | VARIANTS | 0.811 | kārmas tācchīlye | kārm-a-ḥ tāc-chīl-y-e |
| 6.4.173 | VARIANTS | 0.848 | aukṣam anapatye | aukṣ-a-m an-apty-e |
| 6.4.174 | AGREES | 0.944 | dāṇḍināyana-hāstināyana-ātharvaṇika-jaihmāśineya-vāsināyani-bhrauṇahatya-dhaivatya-sārava-aikṣvāka-maitreya-hiraṇmayāni | dāṇḍin-āyana-hāstin-āyana-ātharvaṇ-ika-jaihmāśin-eya-vāsin-eyani-bhrauṇa-hat-ya-dhai-vat-ya-sārava-aikṣvāka-maitreya-hiraṇ-mayā-n-i |
| 6.4.175 | AGREES | 0.914 | ṛtvya-vāstvya-vāstva-mādhvī-hiraṇyayāni cchandasi | ṛtv-ya-vāstv-ya=vāstv-a-mādhv-ī-hiraṇya-yā-n-i chandas-i |
| 7.1.1 | AGREES | 0.938 | yu-vor ana-akau | yu-vo-r ana-ak-au |
| 7.1.2 | AGREES | 0.904 | āyan-ey-īn-īy-iyaḥ pha-ḍha-kha-cha-ghāṃ pratyayāadīnām | āyan-ey-īn-īy-iy-aḥ pha-ḍha-kha-cha-gh-ām praty-ay-a=ādī-n-ām |
| 7.1.3 | VARIANTS | 0.667 | jho 'ntaḥ | jh-aḥ=anta-ḥ |
| 7.1.4 | VARIANTS | 0.815 | ad abhyastāt | at=abhy-as-t-āt |
| 7.1.5 | VARIANTS | 0.857 | ātmanepadeṣv anataḥ | ātmane-pade-ṣu=an-aT-aḥ |
| 7.1.6 | VARIANTS | 0.778 | śīṅo ruṭ | śīṄ-aḥ=ruṬ |
| 7.1.7 | AGREES | 0.933 | vetter vibhāṣā | vet-te-r vibhāṣā |
| 7.1.8 | AGREES | 0.941 | bahulaṃ chandasi | bahu-laṃ chandas-i |
| 7.1.9 | VARIANTS | 0.800 | ato bhisa ais | aT-aḥ=bhis-aḥ=ais |
| 7.1.10 | AGREES | 0.914 | bahulaṃ chandasi | bahu-la-ṃ chandas-i |
| 7.1.11 | AGREES | 0.927 | na+idam-adasor akoḥ | na=idam=adas-or a-k-oḥ |
| 7.1.12 | AGREES | 0.962 | ṭā-ṅasi-ṅasām ina-āt-syāḥ | Ṭā-ṄasI-Ṅas-ām ina=āt=sy-āḥ |
| 7.1.13 | VARIANTS | 0.875 | ṅer yaḥ | Ṅe-r ya-ḥ |
| 7.1.14 | AGREES | 0.941 | sarvanāmnaḥ smai | sarva-nāmn-aḥ smai |
| 7.1.15 | AGREES | 0.933 | ṅasi-ṅyoḥ samāt-sminau | ṄasI-Ṅy-oḥ smāt-smin-au |
| 7.1.16 | VARIANTS | 0.808 | pūrva-ādibhyo navabhyo vā | pūrva=ādi-bhyaḥ=nava-hyaḥ=ā |
| 7.1.17 | AGREES | 0.941 | jasaḥ śī | Jas-aḥ Śī |
| 7.1.18 | VARIANTS | 0.857 | auṅa āpaḥ | auṄ-aḥ āP-aḥ |
| 7.1.19 | VARIANTS | 0.828 | napuṃsakāc ca | na-puṃs-ak-āt=ca |
| 7.1.20 | VARIANTS | 0.857 | jaś-śasoḥ śiḥ | Jas=Śas-oḥ Śi-ḥ |
| 7.1.21 | AGREES | 0.923 | aṣṭābhya auś | aṣṭā-bhyaḥ=auŚ |
| 7.1.22 | VARIANTS | 0.833 | ṣaḍbhyo luk | ṣaḍ-bhyaḥ=luK |
| 7.1.23 | VARIANTS | 0.850 | sv-amor napuṃsakāt | sU=am-or na-puṃs-ak-āt |
| 7.1.24 | CONFLICTS | 0.571 | ato 'm | aT-aḥ=am |
| 7.1.25 | AGREES | 0.968 | adḍ ḍatara-ādibhyaḥ pañcabhyaḥ | adḌ Ḍatara=ādi-bhyaḥ pañca-bhyaḥ |
| 7.1.26 | VARIANTS | 0.895 | na+itarāc chandasi | na=itar-āt=chandas-i |
| 7.1.27 | VARIANTS | 0.830 | yuṣmad-asmadbhyāṃ ṅaso 'ś | yuṣmad=asmad-bhyām Ṅas-aḥ=aŚ |
| 7.1.28 | AGREES | 0.971 | ṅe prathamayor am | Ṅe-prathamay-or am |
| 7.1.29 | VARIANTS | 0.750 | śaso na | Śas-aḥ na |
| 7.1.30 | VARIANTS | 0.846 | bhyaso bhyam | bhyas-aḥ=bhyam |
| 7.1.31 | AGREES | 0.917 | pañcamyā at | pañcamy-āḥ=at |
| 7.1.32 | AGREES | 0.909 | ekavacanasya ca | eka-vac-ana-sya ca |
| 7.1.33 | AGREES | 0.900 | sāma ākam | sām-aḥ=ākam |
| 7.1.34 | VARIANTS | 0.889 | āta au ṇalaḥ | āT-aḥ au ṆaL-aḥ |
| 7.1.35 | VARIANTS | 0.862 | tu-hyos tātaṅ āśiṣy anyatarasyām | tu-hy-os tātaṄ āśiṣ-i=nya-ara-yām |
| 7.1.36 | AGREES | 0.919 | videḥ śatur vasuḥ | vide-ḥ Śatu-r vasU-ḥ |
| 7.1.37 | VARIANTS | 0.833 | samāse 'nañ-pūrve ktvo lyap | sam-ās-e a-naÑ-pūrv-e Ktv-aḥ=LyaP |
| 7.1.38 | AGREES | 0.971 | ktvā api chandasi | Ktvā=api chandas-i |
| 7.1.39 | VARIANTS | 0.889 | supāṃ su-luk-pūrvasavarna-ā-āc-che-yā-ḍā-ḍyā-yāj-ālaḥ | sUP-āṃ sU-luK-pūrva-savarṇa=ā-āt=Śe-yā-Ḍā-Ḍyā-yāC=āL-aḥ |
| 7.1.40 | VARIANTS | 0.750 | amo maś | am-aḥ maŚ |
| 7.1.41 | VARIANTS | 0.894 | lopas ta ātmanepadeṣu | lopa-s t-aḥ ātmane-pade-ṣu |
| 7.1.42 | VARIANTS | 0.846 | dhvamo dhvāt | dhvam-aḥ dhvāt |
| 7.1.43 | AGREES | 0.950 | yajadhvainam iti ca | yaj-a-dhvainam iti ca |
| 7.1.44 | AGREES | 0.947 | tasya tāt | ta-sya tāt |
| 7.1.45 | VARIANTS | 0.851 | taptanaptanathanāś ca | taP-tanaP-tana-than-ā-s=ca |
| 7.1.46 | VARIANTS | 0.769 | id-anto masi | iT=anta-ḥ masi |
| 7.1.47 | VARIANTS | 0.778 | ktvo yak | Ktv-aḥ yaK |
| 7.1.48 | AGREES | 0.938 | iṣṭvīnam iti ca | iṣ-ṭv-īnam iti ca |
| 7.1.49 | VARIANTS | 0.788 | snātvyādayaś ca | snā-tvī=āday-as=ca |
| 7.1.50 | VARIANTS | 0.889 | āj jaser asuk | āt=Jase-r asuK |
| 7.1.51 | AGREES | 0.933 | aśva-kṣīra-vṛṣa-lavaṇānām ātmaprītau kyaci | aśva-kṣīra-vṛṣa-lavaṇā-n-ām ātma-prī-t-au KyaC-i |
| 7.1.52 | AGREES | 0.927 | āmi sarvanāmnaḥ suṭ | ām-i sarva-nāmn-aḥ suṬ |
| 7.1.53 | AGREES | 0.917 | tres trayaḥ | tre-s traya-ḥ |
| 7.1.54 | VARIANTS | 0.789 | hrasvanadyāpo nuṭ | hrasva-nadī=āP-aḥ nuṬ |
| 7.1.55 | AGREES | 0.914 | ṣaṭ-caturbhyaś ca | ṣaṭ-catur-bhyas=ca |
| 7.1.56 | VARIANTS | 0.894 | śrī-grāmaṇyoś chandasi | śrī-grāma-ṇy-os=chandas-i |
| 7.1.57 | VARIANTS | 0.769 | goḥ pādānte | go-ḥ pāda=ant-e |
| 7.1.58 | VARIANTS | 0.722 | idato num dhātoḥ | iT=IT-aḥ nuM dhāto-ḥ |
| 7.1.59 | VARIANTS | 0.857 | śe mucādīnām | Ś-e muc-ādī-n-ām |
| 7.1.60 | AGREES | 0.944 | masji-naśor jhali | masji-naś-or jhaL-i |
| 7.1.61 | AGREES | 0.941 | radhi-jabhor aci | radhi-jabh-or aC-i |
| 7.1.62 | VARIANTS | 0.718 | neṭyaliṭi radheḥ | na=iṬ-i=a-lIṬ-i radhe-ḥ |
| 7.1.63 | VARIANTS | 0.865 | rabher aśab-liṭoḥ | rabhe-r a-ŚaP=lIṬ-oḥ |
| 7.1.64 | VARIANTS | 0.842 | labheś ca | labhe-s=ca |
| 7.1.65 | VARIANTS | 0.667 | āṅo yi | āṄ-aḥ y-i |
| 7.1.66 | VARIANTS | 0.778 | upāt praśaṃsāyām | up-āt pra-śamśā-y-ām |
| 7.1.67 | AGREES | 0.933 | upasargāt khal-ghañoḥ | upa-sarg-āt KHaL-GHaÑ-oḥ |
| 7.1.68 | AGREES | 0.963 | na su-durbhyāṃ kevalābhyām | na su-dur-bhyāṃ kevalā-bhyām |
| 7.1.69 | AGREES | 0.974 | vibhāṣā ciṇ-ṇamuloḥ | vibhāṣā CiṆ-ṆamuL-oḥ |
| 7.1.70 | VARIANTS | 0.806 | ugidacāṃ sarvanāmasthāne 'dhātoḥ | uK=IT-ac-āṃ sarva-nāma-sthān-e=a-dhāt-oḥ |
| 7.1.71 | VARIANTS | 0.867 | yujer asamāse | yuje-r a-sam-ās-e |
| 7.1.72 | AGREES | 0.917 | napuṃsakasya jhal-acaḥ | na-puṃs-aka-sya jhaL=aC-aḥ |
| 7.1.73 | VARIANTS | 0.750 | iko 'ci vibhaktau | iK-aḥ=aC-i vi-bhak-t-au |
| 7.1.74 | VARIANTS | 0.809 | tṛtīyādiṣu bhāṣitapuṃskaṃ puṃvad gālavasya | tṛ-tīyā=ādi-ṣu bhāṣ-i-ta-puṃs-k-āt puṃ-vat=ālava-sya |
| 7.1.75 | AGREES | 0.937 | asthi-dadhi-sakthy-akṣṇām anaṅ udāttaḥ | asthi-dadhi-sakthi=akṣ-ṇ-ām anaṄ udātta-ḥ |
| 7.1.76 | VARIANTS | 0.884 | chandasy api dṛśyate | chandas-i=api dṛś-ya-te |
| 7.1.77 | AGREES | 0.903 | ī ca dvivacane | ī ca dvi-vac-an-e |
| 7.1.78 | VARIANTS | 0.800 | na abhyastāc chatuḥ | na=abhy-as-t-āt=Śatuḥ |
| 7.1.79 | AGREES | 0.909 | vā napuṃsakasya | vā na-puṃs-aka-sya |
| 7.1.80 | VARIANTS | 0.800 | āc chī-nadyor num | ā-t Śī-nady-or nuM |
| 7.1.81 | AGREES | 0.944 | śap-śyanor nityam | ŚaP-ŚyaN-or nitya-m |
| 7.1.82 | VARIANTS | 0.720 | sāv anaḍuha | s-AU anaḍuh-aḥ |
| 7.1.83 | AGREES | 0.906 | dṛk-svavas-svatavasāṃ chandasi | dṛś=sv-avas=sva-tavas-āṃ chandas-i |
| 7.1.84 | VARIANTS | 0.889 | diva aut | div-aḥ=auT |
| 7.1.85 | VARIANTS | 0.863 | pathi-mathy-ṛbhukṣām āt | pathi(n)mathi(n)=ṛbhukṣ-ām āT |
| 7.1.86 | VARIANTS | 0.816 | ito 't sarvanāmasthāne | iT-aḥ=aT sarva-nāma-sthān-e |
| 7.1.87 | VARIANTS | 0.762 | tho nthaḥ | th-aḥ nth-aḥ |
| 7.1.88 | AGREES | 0.914 | bhasya ṭer lopaḥ | bha-sya ṬE-r lopa-ḥ |
| 7.1.89 | VARIANTS | 0.727 | puṃso 'suṅ | puṃs-aḥ=asUṄ |
| 7.1.90 | VARIANTS | 0.737 | goto ṇit | go-taḥ=Ṇ-IT |
| 7.1.91 | VARIANTS | 0.857 | ṇal uttamo vā | ṆaL uttama-ḥ vā |
| 7.1.92 | VARIANTS | 0.884 | sakhyur asambuddhau | sakhy-ur a-sam-bud-dh-au |
| 7.1.93 | AGREES | 0.941 | anaṅ sau | anaṄ s-AU |
| 7.1.94 | VARIANTS | 0.841 | ṛd-uśanas-puru-daṃso 'nehasāṃ ca | ṛT=uśanas=puru-daṃś-as=an-eh-as-āṃ ca |
| 7.1.95 | VARIANTS | 0.875 | tṛj-vat kroṣṭuḥ | tṛC=vat kroṣ-ṭu-ḥ |
| 7.1.96 | AGREES | 0.952 | striyāṃ ca | striy-āṃ ca |
| 7.1.97 | VARIANTS | 0.857 | vibhāṣā tṛtīyādiṣv aci | vibhāṣā tṛ-tīyā-ādi-ṣu=aC-i |
| 7.1.98 | AGREES | 0.923 | catur-anaḍuhor āmudāttaḥ | catur-anaḍ-uh-or āM udātta-ḥ |
| 7.1.99 | VARIANTS | 0.897 | am sambuddhau | aM sam-bud-dh-au |
| 7.1.100 | VARIANTS | 0.759 | ṝta id-dhatoḥ | ṝT-aḥ iT=dhāto-ḥ |
| 7.1.101 | VARIANTS | 0.815 | upadhāyāś ca | upa-dhā-y-ās=ca |
| 7.1.102 | VARIANTS | 0.865 | ud oṣṭhyapūrvasya | uT oṣṭh-ya-pūrva-sya |
| 7.1.103 | AGREES | 0.941 | bahulaṃ chandasi | bahula-ṃ chandas-i |
| 7.2.1 | AGREES | 0.915 | sici vṛddhiḥ parasmaipadeṣu | siC-i vṛd-dhi-ḥ parasmai-pade-ṣu |
| 7.2.2 | VARIANTS | 0.625 | ato lrāntasya | aT-aḥ r-la=anta-sya |
| 7.2.3 | VARIANTS | 0.873 | vada-vraja-halantasya acaḥ | vadḥ-vrajḥ-haL-anta-sya aC-aḥ |
| 7.2.4 | CONFLICTS | 0.545 | neṭi | na=iṬ-i |
| 7.2.5 | AGREES | 0.905 | h-m-yanta-kṣaṇa-śvasa-jāgṛ-ṇi-śvy-ed-itām | h-m-y=anta=kṣaṇa-śvasḥ-jāgṛ-Ṇi-śvi=eT=IT-ām |
| 7.2.6 | AGREES | 0.909 | ūrṇoter vibhāṣā | ūrṇ-o-te-r vibhāṣā |
| 7.2.7 | VARIANTS | 0.829 | ato halāder laghoḥ | aT-aḥ haL-āde-r lagho-ḥ |
| 7.2.8 | VARIANTS | 0.875 | na-iḍ vaśi kṛti | na=iṬ vaŚ-i kṛt-i |
| 7.2.9 | AGREES | 0.987 | ti-tu-tra-ta-tha-si-su-sara-ka-seṣu ca | ti-tu-tra-ta-tha-si-su-sara-ka-se-ṣu ca |
| 7.2.10 | VARIANTS | 0.778 | ekāca upadeśe 'nudāttāt | eka=aC-aḥ upa-deś-e=an-udātt-āt |
| 7.2.11 | VARIANTS | 0.828 | śry-ukaḥ kiti | śri=uK-aḥ K-IT-i |
| 7.2.12 | VARIANTS | 0.850 | sani graha-guhoś ca | saN-i grahḥ-guh-os=ca |
| 7.2.13 | AGREES | 0.932 | kṛ-sṛ-bhṛ-vṛ-stu-dru-sru-śruvo liṭi | kṛ-sṛ-bhṛ-vṛ-stu-dru-sru-śruv-aḥ lIṬ-i |
| 7.2.14 | VARIANTS | 0.698 | śvi-idito niṣthāyām | śvi=īT=IT -aḥ niṣṭhā-y-ām |
| 7.2.15 | AGREES | 0.963 | yasya vibhāṣā | ya-sya vibhāṣā |
| 7.2.16 | VARIANTS | 0.700 | āditaś ca | āT=IT=as=ca |
| 7.2.17 | AGREES | 0.943 | vibhāṣā bhāva-ādikarmaṇoḥ | vibhāṣā bhāva=ādi-kar-maṇ-oḥ |
| 7.2.18 | AGREES | 0.920 | kṣubdha-svānta-dhvānta-lagna-mliṣṭa-viribdha-phāṇṭa-bāḍhāni mantha-manas-tamaḥ-sakta-avispaṣṭa-svara-anāyāsa-bhṛśeṣu | kṣub-dha-svān-ta-dhvān-ta-lag-na-mliṣ-ṭa-vi-rib-dha-phāṇ-ṭa-bā-ḍhā-n-i mantha-manas=tamas=sakta=a-vi-spaṣ-ṭa-svara=an-ā-yās-a-bhṛśe-ṣu |
| 7.2.19 | VARIANTS | 0.829 | dhṛṣī śasī vaiyātye | dhṛsi-śas-ī vaiyāt-y-e |
| 7.2.20 | VARIANTS | 0.870 | dṛḍhaḥ sthūlabalayoḥ | dṛ-ḍha-ḥ sthū-la-bal-ay-oḥ |
| 7.2.21 | VARIANTS | 0.878 | prabhau parivṛḍhaḥ | pra-bh-au pari-vṛ-ḍha-ḥ |
| 7.2.22 | AGREES | 0.920 | kṛcchra-gahanayoḥ kaṣaḥ | kṛcch-ra=gah-anay-oḥ kaṣ-aḥ |
| 7.2.23 | VARIANTS | 0.842 | ghuṣir aviśabdane | ghuṣḥR a-vi-śabd-an-e |
| 7.2.24 | VARIANTS | 0.884 | ardeḥ saṃ-ni-vibhyaḥ | ard-e-ḥ sam=ni-vi-bhyaḥ |
| 7.2.25 | VARIANTS | 0.821 | abheś ca āvidūrye | abhe-s=ca ā-vi-dūr-y-e |
| 7.2.26 | VARIANTS | 0.870 | ṇer adhyayane vṛttam | Ṇe-r adhy-ay-an-e vṛt-ta-m |
| 7.2.27 | AGREES | 0.906 | vā dānta-śānta-pūrṇa-dasta-spaṣṭa-cchanna-jñaptāḥ | vā dān-ta-śān-ta-pūr-ṇa-das-ta-spaṣ-ṭa-chan-na-jña-p-tā-ḥ |
| 7.2.28 | VARIANTS | 0.862 | ruṣy-ama-tvara-saṅghuṣa-āsvanām | ruṣi=amḥ-tvara-saṃ-ghuṣa=ā-svan-ām |
| 7.2.29 | AGREES | 0.923 | hṛṣer lomasu | hṛṣe-r loma-su |
| 7.2.30 | VARIANTS | 0.800 | apacitaś ca | apa-ci-ta-s=ca |
| 7.2.31 | AGREES | 0.900 | hru hvareś chandasi | hru hvare-s=chandas-i |
| 7.2.32 | VARIANTS | 0.750 | aparihvṛtāś ca | a-pari-hvṛ-ta-s ca |
| 7.2.33 | VARIANTS | 0.867 | some hvaritaḥ | som-e hva-r-ita-ḥ |
| 7.2.34 | VARIANTS | 0.884 | grasita-skabhita-stabhita-uttabhita-catta-vikastā viśastṛ-śaṃstṛ-śāstṛ-tarutṛ-tarūtṛ-varutṛ-varūtṛ-varūtrīr-ujjvaliti-kṣariti-kṣamiti-vamity-amiti iti ca | gras-i-ta-skabh-i-ta-stabh-i-ta=ut-tabh-i-ta=cat-ta-vi-kas-ta-vi-śas-tṛ-śaṃs-tṛ-śās-tṛ-taru-tṛ-tarū-tṛ-varutṛ-varū-tṛ-varu-trī-r=uj-jval-i-ti-kṣar-i-ti-kṣam-i-ti-vam-i-ti=am-i-ti=itica |
| 7.2.35 | VARIANTS | 0.893 | ārdhadhātukasya+iḍ valādeḥ | ārdha-dhātuka-sya iṬ=vaL-āde-ḥ |
| 7.2.36 | VARIANTS | 0.896 | snu-kramor anātmanepadanimitte | snu-kramo-r an-ātmane-pada-ni-mit-t-e |
| 7.2.37 | VARIANTS | 0.791 | graho 'liṭi dīrghaḥ | grah-aḥ=a-lIṬ-i dīrgha-ḥ |
| 7.2.38 | VARIANTS | 0.667 | vṝto vā | vṛ=ṝT-aḥ vā |
| 7.2.39 | AGREES | 0.933 | na liṅi | na lIṄ-i |
| 7.2.40 | AGREES | 0.936 | sici ca parasmaipadeṣu | siC-i ca parasmai-pade-ṣu |
| 7.2.41 | AGREES | 0.952 | iṭ sani vā | iṬ saN-i vā |
| 7.2.42 | AGREES | 0.913 | liṅsicor ātmanepadeṣu | lIṄ-siC-or ātmane-pade-ṣu |
| 7.2.43 | VARIANTS | 0.810 | ṛtaś ca saṃyogādeḥ | ṛT-as=ca saṃ-yog-a=āde-ḥ |
| 7.2.44 | VARIANTS | 0.838 | svarati-sūti-sūyati-dhūñ-ūdito vā | svar-a-ti-sū-ti-sū-ya-ti-dhūÑ=ūT=IT-aḥ vā |
| 7.2.45 | VARIANTS | 0.848 | radhādibhyaś ca | radhḥ=ādi-bhyas=ca |
| 7.2.46 | AGREES | 0.917 | niraḥ kuṣaḥ | nir-aḥ kuṣ-aḥ |
| 7.2.47 | VARIANTS | 0.846 | iṇ niṣṭhāyām | iṬ niṣṭhā-y-ām |
| 7.2.48 | AGREES | 0.912 | ti-iṣa-saha-lubha-ruṣa-riṣaḥ | ti=iṣḥ-sahA-lubhḥ-ruṣA-riṣ-aḥ |
| 7.2.49 | AGREES | 0.947 | sani ivanta-rdha-bhrasja-dambhu-śri-svṛ-yu-ūrṇu-bhara-jñapi-sanām | saN-i iv=anta=ṛdha-bhrasjA-danbhU-śri-svṛ-yu=ūrṇu-bhara-jñapi-san-ām |
| 7.2.50 | AGREES | 0.930 | kliśaḥ ktvāniṣṭhayoḥ | kliś-aḥ Ktvā-niṣṭhay-oḥ |
| 7.2.51 | VARIANTS | 0.824 | pūṅaś ca | pūṄ-as=ca |
| 7.2.52 | AGREES | 0.919 | vasati-kṣudhor iṭ | vas-a-ti=kṣudh-or iṬ |
| 7.2.53 | VARIANTS | 0.828 | añceḥ pūjāyām | ance-ḥ pūjā-y-ām |
| 7.2.54 | VARIANTS | 0.727 | lubho vimohane | lubh-aḥ vi-moc-an-e |
| 7.2.55 | AGREES | 0.941 | jṝ-vraścyoḥ ktvi | jṝ-vraścy-oḥ Ktv-i |
| 7.2.56 | VARIANTS | 0.632 | udito vā | uT=IT-aḥ vā |
| 7.2.57 | AGREES | 0.919 | se 'sici kṛta-cṛta-cchṛda-tṛda-nṛtaḥ | se=a-siC-i kṛta-cṛta-chṛda-tṛda-nṛt-aḥ |
| 7.2.58 | AGREES | 0.958 | gamer iṭ parasmaipadeṣu | game-r iṬ parasmaipade-ṣu |
| 7.2.59 | AGREES | 0.913 | na vṛdbhyaś caturbhyaḥ | na vṛt=bhyaś catur-bhyaḥ |
| 7.2.60 | AGREES | 0.929 | tāsi ca kḷpaḥ | tās-i ca kḷp-aḥ |
| 7.2.61 | VARIANTS | 0.806 | acas tāsvat thaly aniṭo nityam | aC-as tas-vat thaL-i=an-iṬ-aḥ=nitya-m |
| 7.2.62 | VARIANTS | 0.824 | upadeśe 'tvataḥ | upa-deś-e aT=vat-aḥ |
| 7.2.63 | VARIANTS | 0.865 | ṛto bhāradvājasya | ṛT-aḥ bhāradvāja-sya |
| 7.2.64 | VARIANTS | 0.865 | vabhūtha-ātatantha-jagṛbhma-vavartha+iti nigame | ba-bhū-tha=ā-ta-tan-tha-ja-gṛbh-ma-va-var-tha=ti ni-gam-e |
| 7.2.65 | VARIANTS | 0.889 | vibhāṣā sṛjidṛśoḥ | vibhāṣā sṛji-dṛṣ-oḥ |
| 7.2.66 | VARIANTS | 0.769 | iḍ atty-arti-vyayatīnām | iṬ at-ti=ar-ti=vyay-a-ti-n-ām |
| 7.2.67 | VARIANTS | 0.732 | vasv ekāj-ād-ghasām | vasU eka=aC=āT=ghas-ām |
| 7.2.68 | AGREES | 0.912 | vibhāṣā gama-hana-vida-viśām | vibhāṣā gama-hanḥ-vidḥ-viś-ām |
| 7.2.69 | VARIANTS | 0.872 | saniṃsasanivāṃsam | saniṃ-sa-san-i-vāṃs-am |
| 7.2.70 | VARIANTS | 0.769 | ṛddhanoḥ sye | ṛT=han-oḥ sy-e |
| 7.2.71 | VARIANTS | 0.818 | ajñeḥ sici | anje-ḥ siC-i |
| 7.2.72 | AGREES | 0.954 | stu-su-dhūñbhyaḥ parasmaipadeṣu | stu-su-dhūÑ-bhyaḥ parasmai-pade-ṣu |
| 7.2.73 | VARIANTS | 0.868 | yama-rama-nama-ātāṃ sak ca | yamḥ-ramA-namḥ=āT-ām saK ca |
| 7.2.74 | VARIANTS | 0.800 | smi-pūṅ-r-añjv-aśāṃ sani | smi-pūṄ=ṛ=anjŪ=aś-ām saN-i |
| 7.2.75 | AGREES | 0.900 | kiraś ca pañcabhyaḥ | kir-as=ca pañca-bhyaḥ |
| 7.2.76 | AGREES | 0.902 | rudādibhyaḥ sārvadhātuke | rud-ādi-bhyaḥ sārvadhatuk-e |
| 7.2.77 | AGREES | 0.933 | īśaḥ se | īś-aḥ se |
| 7.2.78 | AGREES | 0.971 | īḍa-janor dhve ca | īḍA=jan-or dhve ca |
| 7.2.79 | VARIANTS | 0.792 | liṅaḥ salopo 'nantyasya | lIṄ-aḥ sa-lopa-ḥ=an-ant-ya-sya |
| 7.2.80 | VARIANTS | 0.609 | ato yeyaḥ | aT-aḥ yā=iya-ḥ |
| 7.2.81 | VARIANTS | 0.727 | āto ṅitaḥ | āT-aḥ Ṅ-IT-aḥ |
| 7.2.82 | AGREES | 0.933 | āne muk | ān-e muK |
| 7.2.83 | VARIANTS | 0.714 | īdāsaḥ | īT ās-aḥ |
| 7.2.84 | VARIANTS | 0.829 | aṣṭana ā vibhaktau | aṣtan-aḥ ā vi-bhak-t-au |
| 7.2.85 | VARIANTS | 0.762 | rāyo hali | rāy-aḥ=haL-i |
| 7.2.86 | AGREES | 0.917 | yuṣmad-asmador anādeśe | yuṣmad=asmad-or an-ā-deś-e |
| 7.2.87 | VARIANTS | 0.897 | dvitīyāyāṃ ca | dvi-tīyā-y-āṃ ca |
| 7.2.88 | VARIANTS | 0.877 | prathamāyāś ca dvivacane bhāṣāyām | prathamā-y-ās=ca dvi-vac-an-e bhāṣā-y-ām |
| 7.2.89 | CONFLICTS | 0.533 | yo 'ci | ya-ḥ=aC-i |
| 7.2.90 | AGREES | 0.909 | śeṣe lopaḥ | śeṣ-e lopa-ḥ |
| 7.2.91 | VARIANTS | 0.897 | maparyantasya | ma-pary-anta-sya |
| 7.2.92 | VARIANTS | 0.850 | vakṣyati - yuvāvau dvivacane | yuva=āv-au dvi-vac-an-e |
| 7.2.93 | VARIANTS | 0.839 | yūyavayau jasi | yūva-vay-au Jas-i |
| 7.2.94 | VARIANTS | 0.750 | tvāhau sau | tva=ah-au s-AU |
| 7.2.95 | AGREES | 0.947 | tubhya-mahyau ṅayi | tubhya-mahy-au Ṅay-i |
| 7.2.96 | AGREES | 0.938 | tava-mamau ṅasi | tava-mam-au Ṅas-i |
| 7.2.97 | VARIANTS | 0.789 | tva-māv ekavacane | tva-m-au eka-vac-an-e |
| 7.2.98 | VARIANTS | 0.868 | pratyaya-uttarapadayoś ca | prat-ay-a=uttara-paday-os=ca |
| 7.2.99 | AGREES | 0.921 | tri-caturoḥ striyāṃ tisṛ-catasṛ | tri-catur-oḥ striy-ām tisṛ-catsṛ |
| 7.2.100 | AGREES | 0.917 | aci ra ṛtaḥ | aC-i ra ṛT-aḥ |
| 7.2.101 | AGREES | 0.909 | jarāyā jaras anyatarasyām | jarā-y-āḥ jaras anya-tara-syām |
| 7.2.102 | VARIANTS | 0.867 | tyadādīnām aḥ | tyad-ādī-n-ām a-ḥ |
| 7.2.103 | AGREES | 0.900 | kimaḥ kaḥ | kim-aḥ ka-ḥ |
| 7.2.104 | AGREES | 0.947 | ku ti-hoḥ | ku ti-h-oḥ |
| 7.2.105 | AGREES | 0.933 | kva ati | kva aT-i |
| 7.2.106 | VARIANTS | 0.792 | tadoḥ saḥ sāvanantyayoḥ | ta-d-oḥ sa-ḥ s-AU an-antyay-oḥ |
| 7.2.107 | VARIANTS | 0.857 | adasa au sulopaś ca | adas-aḥ au sU-lopa-s=ca |
| 7.2.108 | VARIANTS | 0.762 | idamo maḥ | idam-aḥ ma-ḥ |
| 7.2.109 | VARIANTS | 0.769 | daś ca | d-as=ca |
| 7.2.110 | VARIANTS | 0.875 | yaḥ sau | y-aḥ s-AU |
| 7.2.111 | VARIANTS | 0.741 | ido 'y puṃsi | id-aḥ=ay puṃs-i |
| 7.2.112 | VARIANTS | 0.815 | ana-āpy akaḥ | ana=āP-i a-k-aḥ |
| 7.2.113 | AGREES | 0.909 | hali lopaḥ | haL-i lopa-ḥ |
| 7.2.114 | VARIANTS | 0.897 | mṛjer vṛddhiḥ | mṛje-r vṛd-dhi-ḥ |
| 7.2.115 | VARIANTS | 0.696 | aco ñṇiti | aC-aḥ=Ñ-Ṇ-IT-i |
| 7.2.116 | VARIANTS | 0.839 | ata upadhāyāḥ | aT-aḥ upa-dhā-y-āḥ |
| 7.2.117 | VARIANTS | 0.884 | taddhiteṣv acām ādeḥ | taddhite-ṣu aC-ām āde-ḥ |
| 7.2.118 | VARIANTS | 0.875 | kiti ca | K-IT-i ca |
| 7.3.1 | AGREES | 0.939 | devikā-śiṃśapā-dityavāḍ-dīrghasatra-śreyasām āt | devikā-śiṃśapā-ditya-vāh-dīrgha-sattra-śreyas-ām āT |
| 7.3.2 | AGREES | 0.927 | kekaya-mitrayu-pralayānāṃ ya-āder iyaḥ | kekaya-mitray-u-pra-layā-n-āṃ ya=āde-r iy-aḥ |
| 7.3.3 | VARIANTS | 0.880 | na y-vābhyāṃ padāntābhyāṃ pūrvau tu tābhyām aic | na y-vā-bhyām pada=antā-bhyām pūrv-au tu tā-bhyām aiC |
| 7.3.4 | VARIANTS | 0.867 | dvārādīnāṃ ca | dvāra=ādī-n-āṃ ca |
| 7.3.5 | AGREES | 0.926 | nyagrodhasya ca kevalasya | ny-ag-rodha-sya ca kevala-sya |
| 7.3.6 | VARIANTS | 0.895 | na karmavyatihāre | na karma-vy-ati-hār-e |
| 7.3.7 | VARIANTS | 0.850 | sv-āgata-ādīnāṃ ca | su=ā-ga-ta=ādī-n-āṃ ca |
| 7.3.8 | VARIANTS | 0.857 | śva-āder iñi | śva(n)=āde-r iÑ-i |
| 7.3.9 | VARIANTS | 0.863 | padāntasya anyatarasyām | pada=anta-sya anya-tara-syām |
| 7.3.10 | AGREES | 0.929 | uttarapadasya | uttara-pada-sya |
| 7.3.11 | VARIANTS | 0.786 | vakṣyati - avayavādṛtoḥ | ava-yav-āt ṛto-ḥ |
| 7.3.12 | AGREES | 0.912 | su-sarva-ardhāj janapadasya | su-sarva=ardh-āt jana-pada-sya |
| 7.3.13 | VARIANTS | 0.727 | diśo 'madrāṇām | diś-aḥ=a-madrā-ṇ-ām |
| 7.3.14 | AGREES | 0.936 | prācāṃ grāma-nagarāṇām | prāc-āṃ grāma-nagarā-ṇ-ām |
| 7.3.15 | VARIANTS | 0.880 | saṅkhyāyāḥ saṃvatsara-saṅkhyasya ca | saṃ-khyā-y-āḥ saṃ-vatsara-saṃkhya-sya ca |
| 7.3.16 | VARIANTS | 0.870 | varṣasya abhaviṣyati | varṣa-sya=a-bhav-i-ṣy-at-i |
| 7.3.17 | VARIANTS | 0.848 | parimāṇāntasya asañjñā-śāṇayoḥ | pari-māṇa=anta-sya a-saṃjñā-śāṇay-oḥ |
| 7.3.18 | VARIANTS | 0.895 | je proṣṭhapadānām | j-e proṣṭha-padā-n-ām |
| 7.3.19 | AGREES | 0.904 | hṛd-bhaga-sindhvante pūrvapadasya ca | hṛd-bhaga-sindhu=ante pūrva-ada-ya ca |
| 7.3.20 | VARIANTS | 0.878 | anuśatika-ādīnām ca | anu-śat-ika=ādī-nāṃ ca |
| 7.3.21 | VARIANTS | 0.857 | devatādvandve ca | deva-tā-dvaṃdv-e ca |
| 7.3.22 | AGREES | 0.974 | na+indrasya parasya | na indra-sya parasya |
| 7.3.23 | VARIANTS | 0.857 | dirghāc ca varuṇasya | dīrgh-āt=ca varuṇa-sya |
| 7.3.24 | VARIANTS | 0.833 | prācāṃ nagarānte | prāc-āṃ nagara=ant-e |
| 7.3.25 | AGREES | 0.915 | jaṅgala-dhenu-valajāntasya vibhāṣitam uttaram | jaṛgala-dhenu-vala-ja=anta-sya vibhāṣitam uttaram |
| 7.3.26 | AGREES | 0.901 | ardhāt parimāṇasya pūrvasya tu vā | ardh-āt pari-mā-ṇa-sya pīrva-sya tu vā |
| 7.3.27 | VARIANTS | 0.800 | nātaḥ parasya | na=aT-aḥ para-sya |
| 7.3.28 | AGREES | 0.914 | pravāhaṇasya ḍhe | pra-vāhaṇa-sya ḍh-e |
| 7.3.29 | VARIANTS | 0.895 | tatpratyayasya ca | tat-praty-ay-a-sya ca |
| 7.3.30 | AGREES | 0.917 | nañaḥ śuci-īśvara-kṣetrajña-kuśala-nipuṇānām | naÑ-aḥ śuc-i=īś-vara-kṣe-tra-jña-kuśa-la-nipuṇā-n-ām |
| 7.3.31 | VARIANTS | 0.899 | yathātatha-yathāpurayoḥ paryāyeṇa | yathā-tatha-yathā-puray-oḥ pary-āy-e |
| 7.3.32 | VARIANTS | 0.791 | hanas to 'ciṇ-ṇaloḥ | han-as ta-ḥ a-CiṆ-ṆaL-oḥ |
| 7.3.33 | VARIANTS | 0.865 | āto yuk ciṇ-kṛtoḥ | āT-aḥ yuK CiṆ-kṛt-oḥ |
| 7.3.34 | VARIANTS | 0.881 | na+udātta-upadeśasya ma-antasya anācameḥ | na=udātta=upa-deś-a-sya ma=nta-ya an-ā-ame-ḥ |
| 7.3.35 | AGREES | 0.903 | jani-vadhyoś ca | jani-vadhyo-s=ca |
| 7.3.36 | VARIANTS | 0.847 | arti-hvī-vlī-rī-knūyī-kṣmāyy-ātāṃ pug ṇau | ar-ti-hrī-vlī-rī-knūyī-ksmāyī=āT-ām puK=Ṇ-au |
| 7.3.37 | AGREES | 0.966 | śā-cchā-sā-hvā-vyā-ve-pāṃ yuk | śā-chā-sā-hvā-vyā-ve-p-āṃ yuK |
| 7.3.38 | VARIANTS | 0.811 | vo vidhūnane juk | v-aḥ vi-dhū-n-ane juK |
| 7.3.39 | VARIANTS | 0.828 | lī-lor nug-lukāv anyatarasyāṃ snehavipātane | lī-l-or nuK=luK-au=nya-ara-yām sneha-ipātane |
| 7.3.40 | VARIANTS | 0.857 | bhiyo hetubhaye ṣuk | bhiy-aḥ hetu-bhay-e ṣuK |
| 7.3.41 | VARIANTS | 0.783 | sphāyo vaḥ | sphāy-aḥ va-ḥ |
| 7.3.42 | VARIANTS | 0.865 | śader agatau taḥ | śade-r a-ga-t-au ta-ḥ |
| 7.3.43 | VARIANTS | 0.809 | ruhaḥ po 'nyatarasyām | ruh-aḥ pa-ḥ anya-tara-syām |
| 7.3.44 | VARIANTS | 0.816 | pratyayasthāt kāt pūrvasya ata id āpy asupaḥ | praty-ay-a-sth-āt k-āt pūrva-sya=T-aḥ iT āP-i a-sUP-aḥ |
| 7.3.45 | AGREES | 0.957 | na yā-sayoḥ | na yā-say-oḥ |
| 7.3.46 | VARIANTS | 0.882 | udīcāmātaḥ sthāne yakapūrvāyāḥ | udīc-ām āT-aḥ sthān-e ya-ka-pūrvā-y-āḥ |
| 7.3.47 | AGREES | 0.955 | bhastrā-eṣā-ajā-jñā-dvā-svā nañpūrvāṇām api | bhastrā=eṣā=ajā-jñā-dvā-svā naÑ-ūrvā-ṇ-ām api |
| 7.3.48 | VARIANTS | 0.810 | abhāṣitapuṃskāc ca | a-bhāṣ-i-ta-puṃs-k-āt=ca |
| 7.3.49 | VARIANTS | 0.846 | ād-ācāryāṇām | āT=ācāryā-ṇ-ām |
| 7.3.50 | AGREES | 0.917 | ṭhasya+ikaḥ | ṭha-sya ika-ḥ |
| 7.3.51 | VARIANTS | 0.857 | is-us-uk-tāntāt kaḥ | is=us=uK-ta=ant-āt ka-ḥ |
| 7.3.52 | AGREES | 0.909 | ca-joḥ ku ghiṇ-ṇyatoḥ | ca-j-oḥ kU GHIT=ṆyaT-oḥ |
| 7.3.53 | VARIANTS | 0.800 | nyaṅkv-ādīnāṃ ca | ny-aṛku=ādī-n-āṃ ca |
| 7.3.54 | VARIANTS | 0.783 | ho hanter ñ-ṇin-neṣu | h-aḥ han-te-r Ñ-Ṇ-IT-ne-ṣu |
| 7.3.55 | VARIANTS | 0.833 | abhyāsāc ca | abhy-ās-āt=ca |
| 7.3.56 | VARIANTS | 0.857 | her acaṅi | he-r a-CaṄ-i |
| 7.3.57 | AGREES | 0.929 | san-liṭor jeḥ | saN-lIṬ-or je-ḥ |
| 7.3.58 | AGREES | 0.957 | vibhāṣā ceḥ | vibhāṣā ce-ḥ |
| 7.3.59 | VARIANTS | 0.857 | na kv-ādeḥ | na kU=āde-ḥ |
| 7.3.60 | VARIANTS | 0.786 | aji-vrajyoś ca | aji-vṛjy-os=ca |
| 7.3.61 | VARIANTS | 0.875 | bhuja-nyubjau pāṇy-upatāpayoḥ | bhuj-a-ny-ubj-au pāṇi=upa-tāp-ay-oḥ |
| 7.3.62 | VARIANTS | 0.821 | prayāja-anuyājau yajñāṅge | pra-yāj-a=anu-yāj-au yajña=ṛg-e |
| 7.3.63 | VARIANTS | 0.815 | vañcer gatau | vance-r ga-t-au |
| 7.3.64 | VARIANTS | 0.846 | oka ucaḥ ke | oka-ḥ=uc-aḥ K-e |
| 7.3.65 | CONFLICTS | 0.414 | ṇya āvaśyake | Ṇy-e ā-vaś-ya-k-e |
| 7.3.66 | VARIANTS | 0.806 | yaja-yāca-ruca-pravaca-rcaś ca | yajA-yāca-rucA-pra-vacḥ=ṛc-as=ca |
| 7.3.67 | VARIANTS | 0.652 | vaco 'śabdasañjñāyāṃ | vac-aḥ a-śabda-saṃjnā-y-ām |
| 7.3.68 | VARIANTS | 0.825 | prayojya-niyojyau śakyārthe | pra-yoj-ya-ni-yoj-y-au śak-ya=arth-e |
| 7.3.69 | VARIANTS | 0.824 | bhojyaṃ bhakṣye | bhoj-ya-m bhakṣ-y-e |
| 7.3.70 | VARIANTS | 0.842 | ghor lopo leṭi vā | GHO-r lopa-ḥ lEṬ-i vā |
| 7.3.71 | AGREES | 0.909 | otaḥ śyani | oT-aḥ ŚyaN-i |
| 7.3.72 | VARIANTS | 0.818 | kṣasya aci | Ksa-sya aC-i |
| 7.3.73 | AGREES | 0.905 | lug vā duha-diha-liha-guhām ātmanepade dantye | luK=vā duhA-dihA-lihA-guh-ām ātman-e-ad-e dant-y-e |
| 7.3.74 | AGREES | 0.915 | śamām aṣṭānāṃ dīrghaḥ śyani | śam-ām aṣṭā-n-āṃ dīrgha-ḥ ŚyaN-i |
| 7.3.75 | VARIANTS | 0.846 | ṣṭhivu-klamy-ācamāṃ śiti | ṣṭhivḥ-klami-ā-cam-āṃ Ś-IT-i |
| 7.3.76 | AGREES | 0.909 | kramaḥ parasmaipadeṣu | kram-aḥ parasma-pade-ṣu |
| 7.3.77 | AGREES | 0.900 | iṣu-gami-yamāṃ chaḥ | iṣḥ-gami-yam-āṃ cha-ḥ |
| 7.3.78 | AGREES | 0.958 | pā-ghrā-dhmā-shā-mnā-dāṇ-dṛśy-arti-sarti-śada-sadāṃ piba-jighra-dhama-tiṣtha-mana-yaccha-paśya-rccha-dhau-śīya-sīdāḥ | pā-ghrā-dhmā-sthā-mnā-dāṆ-dṛśi=arti-sarti-śada-sad-ām piba-jighra-dhama-tiṣtha-mana-yaccha-paśya-ṛccha-dhau-śīya-sīd-ā-ḥ |
| 7.3.79 | AGREES | 0.960 | jñā-janor jā | jñā-jan-or jā |
| 7.3.80 | VARIANTS | 0.811 | pv-ādīnāṃ hrasvaḥ | pū-ādī-n-ām hrasva-ḥ |
| 7.3.81 | VARIANTS | 0.848 | mīnāter nigame | mī-nā-te-r ni-gam-e |
| 7.3.82 | AGREES | 0.917 | mider guṇaḥ | mid-er guṇa-ḥ |
| 7.3.83 | AGREES | 0.933 | jusi ca | Jus-i ca |
| 7.3.84 | VARIANTS | 0.862 | sārvadhātuka-ārdhadhātukayoḥ | sārva-dhātu-ka=ārdha-hātu-ay-ḥ |
| 7.3.85 | VARIANTS | 0.824 | jāgro 'vi-ciṇ-ṇal-ṅitsu | jāgr-aḥ a-vi-CiṆ-ṆaL-Ṅ-IT-su |
| 7.3.86 | VARIANTS | 0.830 | puganta-laghūpadhasya ca | puK=anta-laghu=upa-dha-sya ca |
| 7.3.87 | AGREES | 0.923 | na abhyastasya aci piti sārvadhātuke | na=abhy-asta-sya=aC-i P-IT-i sārvadhātuk-e |
| 7.3.88 | AGREES | 0.933 | bhū-suvos tiṅi | bhū-suv-os tiṄ-i |
| 7.3.89 | VARIANTS | 0.833 | uto vṛddhir luki hali | uT-aḥ vṛd-dhi-r luK-i haL-i |
| 7.3.90 | AGREES | 0.909 | ūrṇoter vibhāṣā | ūrṇ-o-te-r vibhāṣā |
| 7.3.91 | CONFLICTS | 0.593 | guṇo 'pṛkto | guṇa-ḥ a-pṛk-t-e |
| 7.3.92 | AGREES | 0.900 | tṛṇaha im | tṛṇah-aḥ iM |
| 7.3.93 | VARIANTS | 0.889 | bruva īṭ | bruv-aḥ īṬ |
| 7.3.94 | VARIANTS | 0.750 | yaṅo vā | yaṄ-aḥ vā |
| 7.3.95 | AGREES | 0.939 | tu-ru-stu-śamy-amaḥ sārvadhātuke | tu-ru-stu-śami=am-aḥ sārvadhātuk-e |
| 7.3.96 | VARIANTS | 0.737 | asti-sico 'pṛkte | as-ti-siC-aḥ=a-pṛk-t-e |
| 7.3.97 | AGREES | 0.941 | bahulaṃ chandasi | bahula-ṃ chandas-i |
| 7.3.98 | AGREES | 0.900 | rudaś ca pañcabhyaḥ | rud-as ca pañca-bhyaḥ |
| 7.3.99 | VARIANTS | 0.872 | aḍ gārgyagālavayoḥ | aṬ gārg-ya-gālavay-oḥ |
| 7.3.100 | AGREES | 0.929 | adaḥ sarveṣām | ad-aḥ sarve-ṣām |
| 7.3.101 | VARIANTS | 0.743 | ato dīrgho yañi | aT-aḥ dīrgha-ḥ yaÑ-i |
| 7.3.102 | AGREES | 0.933 | supi ca | sUP-i ca |
| 7.3.103 | VARIANTS | 0.850 | bahuvacane jhalyet | bahu-vacan-e jhaL-i eT |
| 7.3.104 | AGREES | 0.923 | osi ca | os-i ca |
| 7.3.105 | VARIANTS | 0.818 | āṅi cāpaḥ | āṄ-i ca=āP-aḥ |
| 7.3.106 | VARIANTS | 0.897 | sambuddhau ca | sam-bud-dh-au ca |
| 7.3.107 | VARIANTS | 0.898 | ambārthanadyor hrasvaḥ | ambā=artha-nady-or hrasva-ḥ |
| 7.3.108 | AGREES | 0.938 | hrasvasya guṇaḥ | hrasva-sya guṇa-ḥ |
| 7.3.109 | AGREES | 0.933 | jasi ca | Jas-i ca |
| 7.3.110 | AGREES | 0.906 | ṛto ṅi-sarvanāmasthānayoḥ | ṛT-aḥ Ṅi-sarvanāmasthānay-oḥ |
| 7.3.111 | VARIANTS | 0.857 | gher ṅiti | GHE-r Ṅ-IT-i |
| 7.3.112 | VARIANTS | 0.842 | āṇ nadyāḥ | āṬ=nady-āḥ |
| 7.3.113 | VARIANTS | 0.824 | yāḍ āpaḥ | yāṬ āP-aḥ |
| 7.3.114 | VARIANTS | 0.833 | sarvanāmnaḥ syāḍ ḍhrasvaś ca | sarva-nāmn-aḥ syāṬ hrasva-s=h ca |
| 7.3.115 | AGREES | 0.909 | vibhāṣā dvitīyā-tṛtīyābhyām | vibhāṣā dvi-tīyā-tṛ-īyā-hyām |
| 7.3.116 | VARIANTS | 0.844 | ṅerām nady-ām-nībhyaḥ | Ṅe-r ām nadī=āP=nī-bhyaḥ |
| 7.3.117 | VARIANTS | 0.762 | id-udbhyām | iT=uT=bhyām |
| 7.3.118 | AGREES | 1.000 | aut | auT |
| 7.3.119 | VARIANTS | 0.857 | ac ca gheḥ | aT=ca GHE-ḥ |
| 7.3.120 | VARIANTS | 0.765 | āṅo nā 'striyām | āṄ-aḥ nā a-striy-ām |
| 7.4.1 | VARIANTS | 0.842 | ṇau caṅy upadhāyā hrasvaḥ | Ṇ-au CaṄ-i upa-dhā-y-āḥ hrasva-ḥ |
| 7.4.2 | VARIANTS | 0.766 | na aglopi-śāsv-ṛditām | na aC=lopi(n)=śāsḥ=ṛT=IT-ām |
| 7.4.3 | AGREES | 0.914 | bhrāja-bhāsa-bhāṣa-dīpa-jīva-mīla-pīḍām anyatarasyām | bhrāja-bhāsa-bhāṣA-dīpa-jīvḥ-mīlḥ-pīḍ-ām anya-ara-yām |
| 7.4.4 | VARIANTS | 0.848 | lopaḥ pibater īcca abhyāsasya | lopa-ḥ pib-a-te-r īT=ca abhy-ās-a-sya |
| 7.4.5 | VARIANTS | 0.857 | tiṣṭhater it | ti-ṣṭh-a-te-r iT |
| 7.4.6 | VARIANTS | 0.857 | jighrater vā | ji-ghr-a-te-r vā |
| 7.4.7 | AGREES | 1.000 | ur ṛt | ur ṛT |
| 7.4.8 | AGREES | 0.938 | nityaṃ chandasi | nitya-ṃ chandas-i |
| 7.4.9 | VARIANTS | 0.895 | dayater digi liṭi | day-a-te-r digi lIṬ-i |
| 7.4.10 | VARIANTS | 0.852 | ṛtaś ca saṃyogāder guṇaḥ | ṛT-as ca saṃ-yoga=āde-r guṇa-ḥ |
| 7.4.11 | VARIANTS | 0.774 | ṛcchaty-ṛ-ṛtām | ṛcch-a-ti=ṛ=ṝT-ām |
| 7.4.12 | VARIANTS | 0.837 | śṝ-dṝ-prāṃ hrasvo vā | śṝ-dṝ-pṝ-āṃ hrasva-ḥ vā |
| 7.4.13 | VARIANTS | 0.750 | ke 'ṇaḥ | k-e=aṆ-aḥ |
| 7.4.14 | AGREES | 0.933 | na kapi | na kaP-i |
| 7.4.15 | VARIANTS | 0.722 | apo 'nyatarasyām | āP-aḥ anya-tara-syām |
| 7.4.16 | VARIANTS | 0.778 | ṛ-dṛśo 'ṅi guṇaḥ | ṛ-dṛś-aḥ aṄ-i guṇa-ḥ |
| 7.4.17 | VARIANTS | 0.889 | asyates thuk | as-ya-te-s thuK |
| 7.4.18 | VARIANTS | 0.846 | śvayater aḥ | śvay-a-te-r a-ḥ |
| 7.4.19 | AGREES | 0.947 | pataḥ pum | pat-aḥ puM |
| 7.4.20 | VARIANTS | 0.875 | vaca um | vac-aḥ uM |
| 7.4.21 | AGREES | 0.906 | śīṅaḥ sārvadhātuke guṇaḥ | śīṄ-aḥ sārva-dhdātu-ke guṇa-ḥ |
| 7.4.22 | VARIANTS | 0.867 | ayaṅ yi kṅiti | ayaṄ y-i K-Ṅ-IT-i |
| 7.4.23 | VARIANTS | 0.815 | upasargād dhrasva ūhateḥ | upa-sarg-āt hrasva-ḥ ūh-a-te-ḥ |
| 7.4.24 | VARIANTS | 0.762 | eter ligi | e-te-r lIṄ-i |
| 7.4.25 | VARIANTS | 0.885 | akṛt-sārvadhātukayor dīrghaḥ | a-kṛt-sārva-dhātu-kay-oḥ dīrgha-ḥ |
| 7.4.26 | AGREES | 0.933 | cvau ca | Cv-AU ca |
| 7.4.27 | AGREES | 0.941 | rīṅ ṛtaḥ | rīṄ ṛT-aḥ |
| 7.4.28 | VARIANTS | 0.800 | riṅ śayagliṅkṣu | riṄ Śsa-yaK-lIṄ-k-ṣu |
| 7.4.29 | VARIANTS | 0.760 | guṇo 'rti-saṃyogād yoḥ | guṇa-ḥ arti-saṃ-yog-a-ādy-oḥ |
| 7.4.30 | AGREES | 0.933 | yaṅi ca | yaṄ-i ca |
| 7.4.31 | AGREES | 0.960 | ī ghrā-dhmoḥ | ī ghrā-dhm-oḥ |
| 7.4.32 | AGREES | 0.900 | asya cvau | a-sya Cv-au |
| 7.4.33 | VARIANTS | 0.824 | kyaci ca | KhaC-i ca |
| 7.4.34 | VARIANTS | 0.865 | aśanāya-udanya-dhānāyā bubhukṣā-pipāsā-gardheṣu | aśanā-ya=udan-ya-dhdanā-y-āḥ bu-bhk-ṣā-pi-pā-sā-gardhe-ṣu |
| 7.4.35 | VARIANTS | 0.870 | na cchandasy aputrasya | na=chandas-i a-putra-sya |
| 7.4.36 | VARIANTS | 0.889 | durasyur-draviṇasyur-vṛṣaṇyati riṣaṇyati | duras-y-u-r-draviṇas-y-u-r=vṛṣaṇ-ya-ti-riṣaṇ-ya-ti |
| 7.4.37 | AGREES | 0.968 | aśva-aghasya āt | aśva=agha-sya āT |
| 7.4.38 | AGREES | 0.949 | deva-sumnayor yajuṣi kāṭhake | deva-sumnay-or yajuṣ-i kāṭhak-e |
| 7.4.39 | VARIANTS | 0.882 | kavy-adhavara-pṛtanasya-rci lopaḥ | kavi=adhvara-pṛtana-sya=ṛc-i lopa-ḥ |
| 7.4.40 | AGREES | 0.912 | dyati-syati-mā-sthām it ti kiti | dya-ti-sya-ti-mā-sth-ām iT t-i K-IT-i |
| 7.4.41 | AGREES | 0.930 | śā-chor anyatarasyām | śā-ch-or anya-tara-syām |
| 7.4.42 | VARIANTS | 0.857 | dadhāter hiḥ | da-dhā-te-r hi-ḥ |
| 7.4.43 | VARIANTS | 0.882 | jahāteś ca ktvi | ja-hā-te-ś ca Ktv-i |
| 7.4.44 | AGREES | 0.970 | vibhāṣā chandasi | vibhāṣā chandas-i |
| 7.4.45 | AGREES | 0.909 | sudhita-vasudhita-nemadhita-dhiṣva-dhiṣīya ca | su-dhi-ta-vasu-dhi-ta-nema-dhi-ta-dhi-ṣva-dhi-ṣīy-a ca |
| 7.4.46 | VARIANTS | 0.800 | do dad ghoḥ | d-aḥ dad GHO-ḥ |
| 7.4.47 | VARIANTS | 0.872 | aca upasargāt taḥ | aC-aḥ upa-sarg-āt ta-ḥ |
| 7.4.48 | VARIANTS | 0.706 | apo bhi | ap-aḥ bh-i |
| 7.4.49 | VARIANTS | 0.837 | saḥ sy ārdhadhātuke | s-aḥ s-i ārdha-dhātu-k-e |
| 7.4.50 | AGREES | 0.914 | tās-astyor lopaḥ | tās=as-ty-or lopa-ḥ |
| 7.4.51 | AGREES | 0.909 | ri ca | r-i ca |
| 7.4.52 | AGREES | 0.923 | ha eti | ha eT-i |
| 7.4.53 | VARIANTS | 0.889 | yi-ivarnayor dīdhī-vevyoḥ | y-i=i-varṇay-or dīdhī-vevy-oḥ |
| 7.4.54 | AGREES | 0.961 | sani mī-mā-ghu-rabha-labha-śaka-pata-padām aca is | saN-i mī-mā-GHU-rabhA-labhA-śaka-pata-pad-ām aC-aḥ is |
| 7.4.55 | AGREES | 0.914 | āp-jñapy-ṛdhām īt | āp-jñapi=ṛdh-ām īT |
| 7.4.56 | VARIANTS | 0.846 | dambha ic-ca | dambh-aḥ iT=ca |
| 7.4.57 | VARIANTS | 0.764 | muco 'karmakasya guṇo vā | muc-aḥ a-karma-ka-sya guṇa-ḥ=vā |
| 7.4.58 | VARIANTS | 0.783 | atra lopo 'bhyāsasya | a-tra lopa-ḥ abhy-ās-a-sya |
| 7.4.59 | AGREES | 0.933 | hrasvaḥ | hrasva-ḥ |
| 7.4.60 | VARIANTS | 0.897 | halādiḥ śeṣaḥ | haL-ādi-ḥ śeṣa-ḥ |
| 7.4.61 | VARIANTS | 0.889 | śarpūrvāḥ khayaḥ | śaR-pūrv-ā-ḥ khaY-aḥ |
| 7.4.62 | VARIANTS | 0.818 | ku-hoś cuḥ | kU-h-os=cU-ḥ |
| 7.4.63 | VARIANTS | 0.882 | na kavater yaṅi | na kav-a-te-r yaṄ-i |
| 7.4.64 | VARIANTS | 0.897 | kṛṣeśchandasi | kṛṣe-ś chandas-i |
| 7.4.65 | CONFLICTS | 0.307 | dādharti-dardharti-dardharṣi-bobhūtu-tetikte 'larṣy-āpanīphaṇat-saṃsaniṣyadat-karikrat-kanikradat-bharibhrad-davidhvato-davidyutat-taritrataḥ-sarīsṛpataṃ-varīvṛjan-marmṛjya-āganīganti iti ca | dā-dhar-ti-dar-dhar-ti-dar-dhar-ṣi-bo-bhū-tu-te-tik-te=al-ar-ṣi-ā-paṇī-phaṇ-at-saṃ-sani-ṣyad-at-kari-kr-at-kani-krad-at-bhari-bhr-at-davi-dhv-at-aḥ=davi-dyut-at-tari-tr-at-aḥ=sarī-sṛp-at-am-varī-vṛj-at-mar-mṛjy-a=ā-ganī-gan-ti iti ca |
| 7.4.66 | VARIANTS | 0.800 | urat | u-r aT |
| 7.4.67 | AGREES | 0.915 | dyuti-svāpyoḥ samprasāraṇam | dyuti-svāpy-oḥ sam-pra-sār-aṇa-m |
| 7.4.68 | VARIANTS | 0.800 | vyatho liṭi | vyath-aḥ lIṬ-i |
| 7.4.69 | VARIANTS | 0.865 | dīrgha iṇaḥ kiti | dīrgha-ḥ iṆ-aḥ K-IT-i |
| 7.4.70 | VARIANTS | 0.842 | ata ādeḥ | aT-aḥ āde-ḥ |
| 7.4.71 | VARIANTS | 0.829 | tasmān nuḍ dvihalaḥ | ta-smāt nuṬ dvi-haL-aḥ |
| 7.4.72 | VARIANTS | 0.783 | aśnoteś ca | aś-no-te-s=ca |
| 7.4.73 | VARIANTS | 0.846 | bhavater aḥ | bhav-a-te-r a-ḥ |
| 7.4.74 | VARIANTS | 0.800 | sasūveti nigame | sa-sūv-a iti nigam-e |
| 7.4.75 | VARIANTS | 0.873 | ṇijāṃ trayāṇāṃ guṇaḥ ślau | nij-āṃ trayā-ṇ-āṃ guṇa-ḥ Śl-au |
| 7.4.76 | VARIANTS | 0.889 | bhṛñāmit | bhṛÑ-ām iT |
| 7.4.77 | AGREES | 0.919 | arti-pipartyoś ca | arti-pi-par-ty-oś ca |
| 7.4.78 | AGREES | 0.941 | bahulaṃ chandasi | bahula-ṃ chandas-i |
| 7.4.79 | VARIANTS | 0.737 | sanyataḥ | saN-i aT-aḥ |
| 7.4.80 | VARIANTS | 0.850 | oḥ pu-yaṇ-jy-apare | o-ḥ pU-yaṆ=j-i=a-par-e |
| 7.4.81 | VARIANTS | 0.864 | stravati-śṛṇoti-dravati-pravati-plavati-cyavatīnāṃ vā | srav-a-ti-śṛ-ṇo-ti-drav-a-ti-prav-a-ti-plav-a-ticyav-a-tī-n-āṃ vā |
| 7.4.82 | VARIANTS | 0.839 | guṇo yaṅ-lukoḥ | guṇa-ḥ yaṄ-luK-oḥ |
| 7.4.83 | VARIANTS | 0.710 | dīrgho 'kitaḥ | dīrgha-ḥ a-K-IT-aḥ |
| 7.4.84 | VARIANTS | 0.865 | nīg vañcu-sraṃsu-dhvaṃsu-bhraṃsu-kasa-pata-pada-skandām | nīK vancU-sransU-dhvansU-bhranśU-kasḥ-pata-padA-skand-ām |
| 7.4.85 | VARIANTS | 0.745 | nug ato 'nunāsikāntasya | nuK aT-aḥ anu-nāsika=nta-sya |
| 7.4.86 | VARIANTS | 0.838 | japa-jabha-daha-daśa-bhañja-paśāṃ ca | japḥ-jabhḥ-dahḥ-daśḥ-bhanja-paś-sāṃ ca |
| 7.4.87 | VARIANTS | 0.828 | cara-phaloś ca | carḥ-phal-os=ca |
| 7.4.88 | AGREES | 0.938 | ut parasya ataḥ | uT para-sya aT-aḥ |
| 7.4.89 | AGREES | 0.909 | ti ca | t-i ca |
| 7.4.90 | VARIANTS | 0.789 | rīgṛdupadhasya ca | rīK ṛT=upa-dha-sya ca |
| 7.4.91 | VARIANTS | 0.889 | rug-rikau ca luki | ruK=riK-au ca luK-i |
| 7.4.92 | VARIANTS | 0.800 | ṛtaś ca | ṛT-as ca |
| 7.4.93 | VARIANTS | 0.841 | sanval laghuni caṅpare 'nag lope | saN-vat laghu-n-i CaṄpare an-aC=lop-e |
| 7.4.94 | VARIANTS | 0.828 | dīrgho laghoḥ | dīrgha-ḥ lagho-ḥ |
| 7.4.95 | AGREES | 0.963 | at smṛ-dṝ-tvara-pratha-mrada-stṝ-spaśām | aT smṛ-d ṝ-tvara-prathA-mradA-st ṝ-spaś-ām |
| 7.4.96 | AGREES | 0.952 | vibhāṣā veṣṭiceṣṭyoḥ | vibhāṣā veṣṭi-ceṣṭy-oḥ |
| 7.4.97 | AGREES | 0.952 | ī ca gaṇaḥ | ī ca gaṇ-aḥ |
| 8.1.1 | AGREES | 0.923 | sarvasya dve | sarva-sya dv-e |
| 8.1.2 | VARIANTS | 0.875 | tasya param āmreḍitam | ta-sya para-m ā-mreḍ-i-ta-m |
| 8.1.3 | VARIANTS | 0.800 | anudāttaṃ ca | anudattā-ṃ ca |
| 8.1.4 | AGREES | 0.903 | nitya-vīpsayoḥ | nit-ya-vīpsa-y-oḥ |
| 8.1.5 | VARIANTS | 0.897 | parer varjane | pare-r varj-an-e |
| 8.1.6 | AGREES | 0.931 | pra-sam-upa-udaḥ pādapūraṇe | pra-sam=upa=ud-aḥ pāda-pūr-aṇ-e |
| 8.1.7 | VARIANTS | 0.815 | uparyadhyadhasaḥ sāmīpye | upari-adhi-adhas-aḥ sām-ī-py-e |
| 8.1.8 | VARIANTS | 0.889 | vākyāder āmantritasya asūyā-sammati-kopa-kutsana-bhartsaneṣu | vāk-ya=āde-r ā-mantr-i-ta-sya asūyā-sam-ma-ti-kop-a-kuts-ana-bharts-an-e-ṣu |
| 8.1.9 | VARIANTS | 0.889 | ekaṃ bahuvrīhivat | eka-m bahuvrīhi-vat |
| 8.1.10 | AGREES | 0.900 | ābādhe ca | ā-bādh-e ca |
| 8.1.11 | VARIANTS | 0.885 | karmadhārayavad uttareṣu | karma-dhār-aya-vat uttare-ṣu |
| 8.1.12 | VARIANTS | 0.894 | prakāre guṇavacanasya | pra-kār-e guṇa-vac-ana-sya |
| 8.1.13 | AGREES | 0.923 | akṛcchre priya-sukhayor anyatarasyām | a-kṛcchr-e priy-a-sukhay-or anya-tara-syām |
| 8.1.14 | VARIANTS | 0.851 | yathāsve yathāyatham | ya-thā-sv-e ya-thā-ya-tha-m |
| 8.1.15 | VARIANTS | 0.848 | dvandvaṃ rahasya-maryādāvacana-vyutkramaṇa-yajñapātraprayoga-abhivyaktiṣu | dvaṃ-dva-m rahas-ya-maryādā-acana-vy-ut-kram-aṇa-yajña-pātra-ra-yog-a=abhi-vyak-ti-ṣu |
| 8.1.16 | AGREES | 0.933 | padasya | pada-sya |
| 8.1.17 | AGREES | 0.909 | padāt | pad-āt |
| 8.1.18 | VARIANTS | 0.821 | anudāttaṃ sarvam apādādau | anudātta-ṃ sarva-m a-pada-ād-au |
| 8.1.19 | VARIANTS | 0.882 | āmantritasya ca | ā-mantr-i-ta-sya ca |
| 8.1.20 | AGREES | 0.922 | yuṣmad-asmadoḥ ṣaṣṭhī-caturthī-dvitīyāsthayor vān-nāvau | yuṣmad-asmad-oḥ ṣaṣṭhī-caturthī-dvi-tīyā-sthāy-or vām-nāv-au |
| 8.1.21 | VARIANTS | 0.766 | bahuvacanasya vas-nasau | bahu-vac-an-e vas-nas-su |
| 8.1.22 | VARIANTS | 0.800 | temayāv ekavacanasya | te-may-au=eka-vac-ana-sya |
| 8.1.23 | VARIANTS | 0.872 | tvāmau dvitīyāyāḥ | tvā-m-au dvi-tīyā-y-āḥ |
| 8.1.24 | AGREES | 0.941 | na ca-vā-ha-aha-evayukte | na ca-vā-ha=aha=eva-yuk-t-e |
| 8.1.25 | VARIANTS | 0.800 | paśyārthaiś ca anālocane | paśya=arth-ais=ca=an-ā-loc-an-e |
| 8.1.26 | AGREES | 0.906 | sapūrvāyāḥ prathamāyā vibhāṣā | sa-pūrvā-y-āḥ prathamā-y-āḥ vibhāṣā |
| 8.1.27 | VARIANTS | 0.861 | tiṅo gotrādīni kutsana-ābhīkṣṇyayoḥ | tiṄ-aḥ gotra-ādī-n-i kuts-ana=ābhīkṣṇ-yay-oḥ |
| 8.1.28 | VARIANTS | 0.609 | tiṅṅ atiṅaḥ | tiṄ a-tiṄ-aḥ |
| 8.1.29 | AGREES | 1.000 | na luṭ | na lUṬ |
| 8.1.30 | VARIANTS | 0.896 | nipātair yad-yadi-hanta-kuvin-nec-cec-caṇ-kaccid-yatrayutam | ni-pāt-air yad-yadi-hanta-kuvid-ned-ced-caṆ-kaccid-ya-tra-yuk-ta-m |
| 8.1.31 | AGREES | 0.919 | naha pratyārambhe | naha praty-ā-rambh-e |
| 8.1.32 | VARIANTS | 0.857 | satyaṃ praśne | satya-m praśn-e |
| 8.1.33 | VARIANTS | 0.706 | aṅgāprātilomye | aṛga a-prāti-lom-y-e |
| 8.1.34 | AGREES | 1.000 | hi ca | hi ca |
| 8.1.35 | VARIANTS | 0.831 | chandasy anekam api sākāṅkṣam | chandas-i an-eka-m api sa=ā-kāṛkṣ-am |
| 8.1.36 | AGREES | 0.914 | yāvad-yathābhyām | yā-vad-ya-thā-bhyām |
| 8.1.37 | AGREES | 0.909 | pūjāyāṃ na anantaram | pūjā-y-āṃ na=an-antara-m |
| 8.1.38 | VARIANTS | 0.864 | upasargavyapetaṃ ca | upa-sarg-a-vy-ap-e-taṃ ca |
| 8.1.39 | AGREES | 0.921 | tu-paśyapaśyata-ahaiḥ pūjāyām | tu-paśya-paśya-ta=ah-aiḥ pūjā-y-ām |
| 8.1.40 | AGREES | 1.000 | aho ca | aho ca |
| 8.1.41 | AGREES | 0.960 | śeṣe vibhāṣā | śeṣ-e vibhāṣā |
| 8.1.42 | AGREES | 0.900 | purā ca parīpsāyām | purā ca par-ī-psā-y-ām |
| 8.1.43 | VARIANTS | 0.846 | nanv ity anujñā-eṣaṇāyām | nanu iti anu-jñā=eṣ-aṇā-y-ām |
| 8.1.44 | VARIANTS | 0.870 | kiṃ kriyāpraśne 'nupasargam apratiṣiddham | kiṃ kriyā-praś-n-e an-upa-sarg-am a-prati-ṣid-dha-m |
| 8.1.45 | AGREES | 0.960 | lope vibhāṣā | lop-e vibhāṣā |
| 8.1.46 | VARIANTS | 0.894 | ehi manye prahāse lṛṭ | e-hi-man-y-e pra-hās-e lṚṬ |
| 8.1.47 | VARIANTS | 0.800 | jātvapūrvam | jātu a-pūrva-m |
| 8.1.48 | VARIANTS | 0.846 | kiṃvṛttaṃ ca ciduttaram | kim-vṛt-ta-ṃ ca cid-ut-tara-m |
| 8.1.49 | AGREES | 0.957 | āho utāho ca anantaram | āho=utāho ca=an-antara-m |
| 8.1.50 | AGREES | 0.960 | śeṣe vibhāṣā | śeṣ-e vibhāṣā |
| 8.1.51 | AGREES | 0.901 | gatyartha-loṭā lṛṇ na cet kārakaṃ sarvānyat | gaty-artha-lOṬ-ā lṚṬ na cet kār-aka-ṃ sarva=nyat |
| 8.1.52 | AGREES | 1.000 | loṭ ca | lOṬ ca |
| 8.1.53 | VARIANTS | 0.845 | vibhāṣitaṃ sopasargam anuttamam | vi-bhāṣ-i-taṃ sa=upa-sarg-am an-uttama-m |
| 8.1.54 | AGREES | 1.000 | hanta ca | hanta ca |
| 8.1.55 | VARIANTS | 0.842 | āma ekāntaram āmantritam anantike | ām-aḥ eka=antara-m ā-mantr-i-tam an-antik-e |
| 8.1.56 | AGREES | 0.920 | yad-dhi-tuparaṃ chandasi | yad=hi-tu-para-ṃ chandas-i |
| 8.1.57 | VARIANTS | 0.893 | cana-cid-iva-gotrādi-taddhita-āmreḍiteṣv agateḥ | cana-cid=iva-go-tra=ādi-taddhita=ā-mreḍ-i-te-ṣu=a-gate-ḥ |
| 8.1.58 | VARIANTS | 0.857 | cādiṣu ca | ca=ādi-ṣu ca |
| 8.1.59 | AGREES | 0.974 | ca-vā-yoge prathamā | ca-vā-yog-e prathamā |
| 8.1.60 | VARIANTS | 0.774 | heti kṣiyāyām | ha=iti kṣi-yā-y-ām |
| 8.1.61 | AGREES | 0.927 | aha+iti viniyoge ca | aha iti vi-ni-yog-e ca |
| 8.1.62 | VARIANTS | 0.879 | ca-aha-lopa eva+ity avadhāraṇam | ca=aha-lop-e eva iti ava-dhār-aṇa-m |
| 8.1.63 | VARIANTS | 0.889 | cadilope vibhāṣā | ca=ādi-lop-e vibhāṣā |
| 8.1.64 | AGREES | 0.960 | vai-vāva+iti ca cchandasi | vai-vāva iti ca=chandas-i |
| 8.1.65 | VARIANTS | 0.873 | ekānyābhyāṃ samarthābhyām | eka=anyā-bhyāṃ sam-arthā-bhyām |
| 8.1.66 | VARIANTS | 0.833 | yadvṛttān nityam | yad-vṛt-t-āt nitya-m |
| 8.1.67 | VARIANTS | 0.884 | pūjanāt pūjitam anudāttaṃ kāṣṭhādibhyaḥ | pūj-an-āt pūj-i-ta-m anudāttam (kāṣṭha=ādi-bhyaḥ) |
| 8.1.68 | AGREES | 0.909 | sagatir api tiṅ | sa-ga-ti-r api tiṄ |
| 8.1.69 | VARIANTS | 0.842 | kutsane ca supy agotrādau | kuts-an-e ca sUPi=a-go-tra-ād-au |
| 8.1.70 | VARIANTS | 0.846 | gatir gatau | ga-ti-r ga-t-au |
| 8.1.71 | AGREES | 0.923 | tiṅi ca+udāttavati | tiṄ-i ca udātta-vat-i |
| 8.1.72 | VARIANTS | 0.841 | āmantritaṃ pūrvam avidyamānavat | ā-mantr-ita-m pūrva-m a-vid-ya-āna-vat |
| 8.1.73 | VARIANTS | 0.848 | na āmantrite samānādhikaraṇe sāmānyavacanam | na ā-mantr-it-e sa-māna=dhi-kar-aṇ-e (sā-mān-ya-vac-ana-m) |
| 8.1.74 | VARIANTS | 0.667 | vibhāṣitaṃ viśeṣavacane bahuvacanam | (sāmānya-vac-ana-ṃ) vi-bhāṣ-i-ta-ṃ vi-śeṣ-a-vac-an-e (bahu-vac-an-e) |
| 8.2.1 | VARIANTS | 0.895 | pūrvatra asiddham | pūrva-tra=a-sid-dha-m |
| 8.2.2 | VARIANTS | 0.874 | nalopaḥ sup-svara-sañjñā-tug-vidhiṣu kṛti | na-lopa-ḥ sUP-svara-saṃ-jñā-tuK=i-dhi-ṣu kṛt-i |
| 8.2.3 | AGREES | 0.941 | na mu ne | na mu n-e |
| 8.2.4 | VARIANTS | 0.872 | udātta-svaritayor yaṇaḥ svarito 'nudāttasya | udātta-svar-itay-or yaṆ-aḥ svar-i-ta-ḥ anudātta-sya |
| 8.2.5 | VARIANTS | 0.836 | ekādeśa udātena+udāttaḥ | eka=ā-deś-a-ḥ udātt-ena udātta-ḥ |
| 8.2.6 | VARIANTS | 0.806 | svarito vā 'nudātte padādau | svar-i-ta-ḥ vā anudātt-e pada=ād-au |
| 8.2.7 | VARIANTS | 0.828 | nalopaḥ prātipadikāntasya | na-lop-a-ḥ prāti-pad-ika=anta-sya |
| 8.2.8 | AGREES | 0.919 | na ṅi-sambuddhyoḥ | na Ṅi-sam-bud-dhy-oḥ |
| 8.2.9 | VARIANTS | 0.831 | m-ād-upadhāyāś ca mator vo 'yava-ādibhyaḥ | m-āt=pa-dhā-y-āś ca mat-Or va-ḥ a-yava=ādi-bhyaḥ |
| 8.2.10 | AGREES | 0.923 | jhayaḥ | jhaY-aḥ |
| 8.2.11 | VARIANTS | 0.762 | sañjñāyām | saṃ-jñā-y-ām |
| 8.2.12 | VARIANTS | 0.881 | āsandīvad-aṣṭhīvac-cakrīvat-kakṣīvad-rumaṇvac-carmaṇvatī | āsandī-vat=aṣṭhī-vat-cakrī-vat-kakṣī-vat=rumaṇ-vat=carmaṇ-vatī |
| 8.2.13 | VARIANTS | 0.872 | udanvan udadhau ca | udan-vān uda-dh-au ca |
| 8.2.14 | VARIANTS | 0.895 | rājanvān saurājye | rājan-vān sau-rāj-y-e |
| 8.2.15 | VARIANTS | 0.897 | chandasi iraḥ | chandas-i i-r-aḥ |
| 8.2.16 | VARIANTS | 0.750 | ano nuṭ | an-aḥ nuṬ |
| 8.2.17 | VARIANTS | 0.818 | nād ghasya | n-āt GHA-sya |
| 8.2.18 | VARIANTS | 0.667 | kṛpo ro laḥ | kṛp-aḥ r-aḥ la-ḥ |
| 8.2.19 | VARIANTS | 0.829 | upasargaya ayatau | upa-sarg-a-sya ay-a-t-au |
| 8.2.20 | VARIANTS | 0.737 | gro yaṅi | gr-aḥ yaṄ-i |
| 8.2.21 | AGREES | 0.957 | aci vibhāṣā | aC-i vibhāṣā |
| 8.2.22 | AGREES | 0.905 | pareś ca gha-aṅkayoḥ | pare-ś ca gha=aṛkay-oḥ |
| 8.2.23 | VARIANTS | 0.818 | saṃyogāntasya lopaḥ | saṃ-yog-a=anta-sya lopa-ḥ |
| 8.2.24 | VARIANTS | 0.857 | rāt sasya | r-aāt sa-sya |
| 8.2.25 | AGREES | 0.923 | dhi ca | dh-i ca |
| 8.2.26 | VARIANTS | 0.800 | jhalo jhali | jhaL-aḥ jhaL-i |
| 8.2.27 | VARIANTS | 0.857 | hrasvād aṅgāt | hrasv-ād aṛg-āt |
| 8.2.28 | VARIANTS | 0.824 | iṭa īṭi | iṬ-aḥ īṬ-i |
| 8.2.29 | VARIANTS | 0.881 | s-koḥ saṃyoga-ādyor ante ca | s-k-oḥ saṃ-yog-a=ādy-oḥ ant-e ca |
| 8.2.30 | VARIANTS | 0.875 | coḥ kuḥ | cO-ḥ kU-ḥ |
| 8.2.31 | VARIANTS | 0.706 | ho ḍhaḥ | h-aḥ ḍha-ḥ |
| 8.2.32 | VARIANTS | 0.895 | dāder dhātor ghaḥ | d-āde-r dhāto-r gha-ḥ |
| 8.2.33 | VARIANTS | 0.868 | vā druha-muha-ṣṇuha-ṣṇihām | vā druhḥ-muhḥ-ṣṇuhḥ-ṣṇih-ām |
| 8.2.34 | VARIANTS | 0.762 | naho dhaḥ | nah-aḥ dha-ḥ |
| 8.2.35 | VARIANTS | 0.842 | āhasthaḥ | āh-as tha-ḥ |
| 8.2.36 | AGREES | 0.917 | vraśca-bhrasja-sṛja-mṛja-yaja-rāja-bhrāja-ccha-śāṃ ṣaḥ | vraśca-bhrasjA-sṛjḥ-mṛjḥ-yajA-rāja-bhrāja=cha-ś-ām ṣa-ḥ |
| 8.2.37 | VARIANTS | 0.810 | ekāco baśo bhaṣ jhaṣantasya s-dhvoḥ | eka=aC-aḥ baŚ-aḥ bhaṢ jhaṢ-anta-sya s-dhv-oḥ |
| 8.2.38 | AGREES | 0.944 | dadhas ta-thoś ca | dadh-as ta-th-oś ca |
| 8.2.39 | VARIANTS | 0.778 | jhalāṃ jaśo 'nte | jhaL-āṃ jaŚ-aḥ ant-e |
| 8.2.40 | VARIANTS | 0.815 | jhaṣas ta-thor dho 'dhaḥ | jhaṢ-as ta-th-or dha-ḥ a-dh-aḥ |
| 8.2.41 | AGREES | 0.903 | ṣa-ḍhoḥ kaḥ si | ṣa-ḍh-oḥ ka-ḥ s-i |
| 8.2.42 | VARIANTS | 0.824 | ra-dābhyāṃ niṣthāto naḥ pūrvasya ca daḥ | ra-dā-bhyāṃ niṣṭhā-t-aḥ na-ḥ pūrva-sya tu d-aḥ |
| 8.2.43 | VARIANTS | 0.829 | saṃyogāder āto dhātor yaṇvataḥ | saṃ-yog-a=āde-r āT-aḥ dhāto-r yaṆ-vat-aḥ |
| 8.2.44 | VARIANTS | 0.818 | lvādibhyaḥ | lū=ādi-bhyaḥ |
| 8.2.45 | VARIANTS | 0.800 | oditaś ca | oT=IT-aś ca |
| 8.2.46 | VARIANTS | 0.828 | kṣiyo dīrghāt | kṣiy-aḥ dīrgh-āt |
| 8.2.47 | VARIANTS | 0.692 | śyo 'sparśe | śy-aḥ a-sparś-e |
| 8.2.48 | VARIANTS | 0.629 | añco 'napādāne | anc-aḥ an-ap-ā-dā-n-e |
| 8.2.49 | VARIANTS | 0.683 | divo 'vijigīṣāyām | div-aḥ a-v-ji-gī-ṣā-y-ām |
| 8.2.50 | VARIANTS | 0.688 | nirvāṇo 'vāte | nir-vā-ṇaḥ a-vā-t-e |
| 8.2.51 | AGREES | 0.900 | śuṣaḥ kaḥ | śuṣ-aḥ ka-ḥ |
| 8.2.52 | VARIANTS | 0.737 | paco vaḥ | pac-aḥ va-ḥ |
| 8.2.53 | VARIANTS | 0.762 | kṣāyo maḥ | kṣāy-aḥ ma-ḥ |
| 8.2.54 | VARIANTS | 0.800 | prastyo 'nyatarasyām | pra-sty-aḥ anya-tara-syām |
| 8.2.55 | VARIANTS | 0.894 | anupasargāt phulla-kṣība-kṛśa-ullāghāḥ | an-upa-sarg-āt phul-la-kṣīb-a-kṛś-a-ul-lāgh-ā-ḥ |
| 8.2.56 | VARIANTS | 0.867 | nuda-vida-unda-trā-ghrā-hrībhyo 'nyatarasyām | nudḥ-vidA=unda-trā-ghrā-hrī-bhyaḥ anya-ara-yām |
| 8.2.57 | AGREES | 0.966 | na dhyā-khyā-pṝ-mūrcchi-madām | na dhyā-khyā-pṝ-mūrchi-mad-ām |
| 8.2.58 | VARIANTS | 0.846 | vitto bhoga-pratyayayoḥ | vit-ta-ḥ bhog-a-praty-ayay-oḥ |
| 8.2.59 | AGREES | 0.909 | bhittaṃ śakalam | bhit-ta-ṃ śakala-m |
| 8.2.60 | VARIANTS | 0.882 | ṛṇam ādhamarṇye | ṛ-ṇa-m ādhamarṇ-y-e |
| 8.2.61 | AGREES | 0.900 | nasatta-niṣatta-anutta-pratūrta-sūrta-gūrtāni chandasi | na-sat-ta-ni-ṣat-ta=a-nut-ta-pra-tūr-ta-sūr-ta-gūrtā-n-i chandas-i |
| 8.2.62 | AGREES | 0.905 | kvinpratyayasya kuḥ | KviN-praty-aya-sya kU-ḥ |
| 8.2.63 | AGREES | 0.941 | naśer vā | naśe-r vā |
| 8.2.64 | VARIANTS | 0.690 | mo no dhātoḥ | m-aḥ na-ḥ dhāto-ḥ |
| 8.2.65 | AGREES | 0.941 | m-voś ca | m-v-oś ca |
| 8.2.66 | VARIANTS | 0.897 | sa-sajuṣo ruḥ | sa-sajuṣ-oḥ rU-ḥ |
| 8.2.67 | VARIANTS | 0.889 | avayāḥ śvetavāḥ pūroḍāś ca | ava-yāḥ=śveta-vāḥ=uro-ḍāś ca |
| 8.2.68 | AGREES | 1.000 | ahan | ahan |
| 8.2.69 | VARIANTS | 0.600 | ro 'supi | ra-ḥ a-sUP-i |
| 8.2.70 | AGREES | 0.900 | amnar-ūdhar-avar ity ubhayathā chandasi | amnas=ūdhas=ava s=ity ubhayathā chandas-i |
| 8.2.71 | VARIANTS | 0.857 | bhuvaś ca mahāvyāhṛteḥ | bhuvas=ca mahā-vy-ā-hṛ-te-ḥ |
| 8.2.72 | AGREES | 0.909 | vasu-sraṃsu-dhvaṃsv-anaḍuhāṃ daḥ | vasU-sraṃsU-dhvaṃsU=anaḍuh-ām da-ḥ |
| 8.2.73 | VARIANTS | 0.786 | tipy anasteḥ | tiP-i an-as-te-ḥ |
| 8.2.74 | VARIANTS | 0.811 | sipi dhāto rurvā | siP-i dhāto-r=rU-ḥ=vā |
| 8.2.75 | VARIANTS | 0.769 | daś ca | d-as=ca |
| 8.2.76 | VARIANTS | 0.833 | r-vor upadhāyā dīrgha ikaḥ | r-v-oḥ upa-dhā-y-āḥ dīrgha-ḥ iK-aḥ |
| 8.2.77 | AGREES | 0.933 | hali ca | haL-i ca |
| 8.2.78 | VARIANTS | 0.889 | upadhāyāṃ ca | upa-dhā-y-āṃ ca |
| 8.2.79 | AGREES | 0.971 | na bha-kur-churām | na BHA-kur-chur-ām |
| 8.2.80 | VARIANTS | 0.704 | adaso 'ser dād u do maḥ | adas-aḥ=a-se-r d-āt=u d-aḥ=ma-ḥ |
| 8.2.81 | VARIANTS | 0.821 | eta īd bahuvacane | eT-aḥ=īT bahu-vac-an-e |
| 8.2.82 | VARIANTS | 0.881 | vākyasya ṭeḥ pluta udāttaḥ | vāk-ya-sya ṬE-ḥ plu-ta-ḥ=udātta-ḥ |
| 8.2.83 | VARIANTS | 0.844 | vakṣyati - pratyabhivāde 'śūdre | praty-abhi-vād-e=a-śūdr-e |
| 8.2.84 | VARIANTS | 0.800 | dūrād dhūte ca | dūr-āt=hū-t-e ca |
| 8.2.85 | AGREES | 0.920 | hai-heprayoge hai-hayoḥ | hai-he-pra-yog-e hai-hay-oḥ |
| 8.2.86 | VARIANTS | 0.821 | guror anṛto 'nantyasya apy ekaikasya prācām | guro-r an-ṛT-aḥ an-anty-ya-sya=api ekaika-ya prāc-ām |
| 8.2.87 | VARIANTS | 0.857 | om abhyādāne | om abhy-ā-dā-n-e |
| 8.2.88 | VARIANTS | 0.857 | ye yajñakarmaṇi | y-e yaj-ña-kar-maṇ-i |
| 8.2.89 | VARIANTS | 0.857 | praṇavaṣ ṭeḥ | pra-ṇav-a-ṣ ṬE-ḥ |
| 8.2.90 | VARIANTS | 0.818 | yājyāntaḥ | yāj-yā=anta-ḥ |
| 8.2.91 | VARIANTS | 0.864 | brūhi-preṣya-śrauṣaḍ-vauṣaḍ-āvahānām ādeḥ | brū-hi-pr-e-sya-śrauṣaṭ-vauṣaṭ-ā-vahā-nām āde-ḥ |
| 8.2.92 | VARIANTS | 0.836 | agnīt-preṣaṇe parasya ca | agn-ī-dh=pr-e-ṣ-aṇe para-sya ca |
| 8.2.93 | AGREES | 0.903 | vibhāṣā pṛṣṭaprativacane heḥ | vibhāṣā pṛṣ-ṭa-prati-vac-an-e he-ḥ |
| 8.2.94 | AGREES | 0.900 | nigṛhya-anuyoge ca | ni-gṛh-ya=anu-yog-e ca |
| 8.2.95 | VARIANTS | 0.818 | āmreḍitaṃ bhartsane | ā-mreḍ-i-ta-m bharts-an-e |
| 8.2.96 | VARIANTS | 0.808 | aṅgayuktaṃ tiṅ ākāṅkṣam | aṛga-yuk-ta-ṃ tiṄ ā-kāṛkṣ-a-m |
| 8.2.97 | VARIANTS | 0.824 | vicāryamāṇānām | vi-cār-ya-m-āṇā-n-ām |
| 8.2.98 | AGREES | 0.923 | pūrvaṃ tu bhāṣāyām | pūrva-ṃ tu bhāṣā-y-ām |
| 8.2.99 | AGREES | 0.909 | pratiśravaṇe ca | prati-śrav-aṇ-e ca |
| 8.2.100 | VARIANTS | 0.838 | anudāttaṃ praśnānta-abhipūjitayoḥ | an-udāttam praś-na=anta=abhi-pūj-i-tay-oḥ |
| 8.2.101 | VARIANTS | 0.880 | cid iti ca+upamārthe prayujyamāne | cid iti ca upa-mā=arth-e pra-yuj-ya-m-ān-e |
| 8.2.102 | VARIANTS | 0.870 | uparisvid āsīd iti ca | upari-svid ās-ī3-t=iti ca |
| 8.2.103 | VARIANTS | 0.882 | svaritam āmreḍite 'sūyā-sammati-kopa-kutsaneṣu | svar-i-tam ā-mreḍ-i-t-e asūyā=sam-ma-ti-kopa-kuts-ane-ṣu |
| 8.2.104 | VARIANTS | 0.853 | kṣiyā-āśīḥ-praiṣeṣu tiṅ ākāṅkṣam | kṣiyā=āśis-praiṣe-ṣu tiṄ ā-kāṛkṣ-a-m |
| 8.2.105 | VARIANTS | 0.896 | anantyasya api praśnākhyānayoḥ | an-ant-ya-sya=api praśna=ā-khyānay-oḥ |
| 8.2.106 | VARIANTS | 0.714 | plutāv aica idutau | plu-t-au aiC-aḥ iT=uT-au |
| 8.2.107 | VARIANTS | 0.795 | eco 'pragṛhyasya adūrādhdūte pūrvasya ardhasya ad uttarasya+idutau | eC-aḥ a-pra-gṛh-ya-sya=a-dūr-āt=ū-t-e pūrva-sya ardha-sya=āT=uttara-sya iT=uT-au |
| 8.2.108 | VARIANTS | 0.833 | tayor y-v-āv aci saṃhitāyām | tay-or y-v-au aC-i saṃ-hi-tā-y-ām |
| 8.3.1 | AGREES | 0.914 | matu-vaso ru sambuddhau chandasi | matU-vasO-ḥ rU sam-bud-dh-au chandas-i |
| 8.3.2 | VARIANTS | 0.871 | atrānunāsikaḥ pūrvasya tu vā | a-tra anu-nāsika-ḥ pūrva-sya tu vā |
| 8.3.3 | VARIANTS | 0.688 | ato 'ṭi nityam | āT-aḥ=aṬ-i nitya-m |
| 8.3.4 | VARIANTS | 0.807 | anunāsikāt paro 'nusvāraḥ | anu-nāsik-āt para-ḥ anu-svār-a-ḥ |
| 8.3.5 | VARIANTS | 0.818 | vakṣyati - samaḥ suti | sam-aḥ suṬ-i |
| 8.3.6 | VARIANTS | 0.821 | pumaḥ khayyampare | pum-aḥ khaY-i=aM-par-e |
| 8.3.7 | VARIANTS | 0.722 | naśchavyapraśān | n-as=chaV-i a-pra-śān |
| 8.3.8 | VARIANTS | 0.774 | ubhayatha rkṣu | ubha-ya-thā ṛk-ṣu |
| 8.3.9 | VARIANTS | 0.816 | dīrghād aṭi samānapāde | dīrgh-āt aṬ-i sa-māna-pad-e |
| 8.3.10 | VARIANTS | 0.857 | nṝn pe | nṝ-n p-e |
| 8.3.11 | AGREES | 0.966 | svatavān pāyau | svatavān pāy-au |
| 8.3.12 | AGREES | 0.960 | kān āmreḍite | kān āmreḍit-e |
| 8.3.13 | VARIANTS | 0.774 | ḍho ḍhe lopaḥ | ḍh-aḥ ḍh-e lop-a-ḥ |
| 8.3.14 | VARIANTS | 0.615 | ro ri | r-aḥ r-i |
| 8.3.15 | AGREES | 0.903 | khar-avasānayor visarjanīyaḥ | khaR=ava-sā-nayo-r vi-sarj-anīya-ḥ |
| 8.3.16 | VARIANTS | 0.889 | roḥ supi | rO-ḥ suP-i |
| 8.3.17 | VARIANTS | 0.866 | bho-bhago-agho-apūrvasya yo 'śi | bho=bhago=agho=a-pūrva-sya ya-ḥ aŚ-i |
| 8.3.18 | AGREES | 0.916 | v-yor laghuprayatnataraḥ śākaṭāyanasya | v-y-or laghu-pra-yat-na-tara-ḥ śākaṭāyana-sya |
| 8.3.19 | AGREES | 0.914 | lopaḥ śākalyasya | lop-a-ḥ śākalya-sya |
| 8.3.20 | VARIANTS | 0.733 | oto gargyasya | oT-aḥ gārg-ya-sya |
| 8.3.21 | AGREES | 0.917 | uñi ca pade | uÑ-i ca pad-e |
| 8.3.22 | VARIANTS | 0.857 | hali sarveṣāṃ | haL-i sarve-ṣām |
| 8.3.23 | VARIANTS | 0.690 | mo 'nusvāraḥ | m-aḥ anu-svār-a-ḥ |
| 8.3.24 | VARIANTS | 0.852 | naś ca apadāntasya jhali | n-aś ca a-pada=anta-sya jhaL-i |
| 8.3.25 | VARIANTS | 0.829 | mo rāji samaḥ kvau | ma-ḥ rāj-i sam-aḥ Kv-au |
| 8.3.26 | VARIANTS | 0.889 | he mapare vā | h-e ma-par-e vā |
| 8.3.27 | VARIANTS | 0.870 | napare naḥ | na-par-e na-ḥ |
| 8.3.28 | VARIANTS | 0.895 | ṅ-ṇoḥ kuk-ṭuk śari | ṛ-ṇ-oḥ kuK-ṭuK śaR-i |
| 8.3.29 | VARIANTS | 0.833 | ḍaḥ si ḍhuṭ | ḍ-aḥ s-i dhuṬ |
| 8.3.30 | AGREES | 0.923 | naś ca | n-aś ca |
| 8.3.31 | AGREES | 0.923 | śi tuk | ś-i tuK |
| 8.3.32 | VARIANTS | 0.762 | ṅamo hrasvād aci ṅamuṇ nityam | ṛaM-aḥ=hrasv-āt aC-i ṛaMuṬ nitya-m |
| 8.3.33 | VARIANTS | 0.706 | maya uño vo vā | maY-aḥ uÑ-aḥ va-ḥ vā |
| 8.3.34 | AGREES | 0.900 | visarjanīyasya saḥ | vi-sarj-anīya-sya sa-ḥ |
| 8.3.35 | VARIANTS | 0.889 | śarpare visarjanīyaḥ | śaR-par-e vi-sarj-anīya-ḥ |
| 8.3.36 | AGREES | 0.933 | vā śari | vā śaR-i |
| 8.3.37 | VARIANTS | 0.757 | kupvoḥ ḥkaḥpau ca | kU-pV-oḥ Xk-Xp-au ca |
| 8.3.38 | VARIANTS | 0.643 | so 'padādau | sa-ḥ a-pada-ād-au |
| 8.3.39 | VARIANTS | 0.889 | iṇaḥ ṣaḥ | iṆ-aḥ ṣa-ḥ |
| 8.3.40 | AGREES | 0.952 | namas-purasor gatyoḥ | namas-puras-or gaty-oḥ |
| 8.3.41 | VARIANTS | 0.853 | id-ud-upadhasya ca apratyayasya | iT=uT=upa-dha-sya ca a-praty-ay-a-sya |
| 8.3.42 | VARIANTS | 0.810 | tiraso 'nyatarasyām | tiras-aḥ anya-tara-syām |
| 8.3.43 | VARIANTS | 0.875 | dvis-triś-catur iti kṛtvo 'rthe | dvis-tris-catur iti kṛtvas=arth-e |
| 8.3.44 | AGREES | 0.919 | is-usoḥ sāmarthye | is=us-oḥ sāmarth-y-e |
| 8.3.45 | VARIANTS | 0.829 | nityaṃ samāse 'nuttarapadasthasya | nitya-ṃ sam-ās-e an-uttara-ada-tha-ya |
| 8.3.46 | AGREES | 0.924 | ataḥ kṛ-kami-kaṃsa-kumbha-pātra-kuśā-karṇīṣv anavyayasya | aT-aḥ kṛ-kami-kaṃsa-kumbha-pātra-kuśā-karṇī-ṣu an-a-vy-ay-a-sya |
| 8.3.47 | VARIANTS | 0.889 | adhaḥ-śirasī pade | adhas=śiras-ī pad-e |
| 8.3.48 | VARIANTS | 0.857 | kaskādiṣu ca | kas-ka=ādi-ṣu ca |
| 8.3.49 | AGREES | 0.931 | chandasi vā 'pra-āmreḍitayoḥ | chandas-i vā apra=āmreḍitay-oḥ |
| 8.3.50 | VARIANTS | 0.790 | kaḥkaratkaratikṛdhikṛteṣvanaditeḥ | ka-ḥ-kar-a-t-kar-a-ti-kṛ-dhi-kṛ-te-ṣu an-adite-ḥ |
| 8.3.51 | VARIANTS | 0.830 | pañcamyāḥ parāvadhyarthe | pañcamy-āḥ par-au adhy-arth-e |
| 8.3.52 | AGREES | 0.914 | pātau ca bahulam | pā-t-au ca bahula-m |
| 8.3.53 | AGREES | 0.960 | ṣaṣṭhyāḥ pati-putra-pṛṣṭha-pāra-pada-payas-poṣeṣu | ṣaṣthy-āḥ pati-putra-pṛṣṭha-pāra-pada-payas-poṣe-ṣu |
| 8.3.54 | VARIANTS | 0.842 | iḍāyā vā | iḍā-y-āḥ vā |
| 8.3.55 | VARIANTS | 0.840 | apadāntasya mūrdhanyaḥ | a-pada=anta-sya mūrdhan-ya-ḥ |
| 8.3.56 | AGREES | 0.909 | saheḥ sāḍaḥ saḥ | sahe-ḥ sāḍ-aḥ s-aḥ |
| 8.3.57 | AGREES | 0.923 | iṇ-koḥ | iṆ-kO-ḥ |
| 8.3.58 | VARIANTS | 0.848 | nam-visarjanīya-śarvyavāye 'pi | nuM-vi-sarj-anīya-śaR-vy-av-āy-e=api |
| 8.3.59 | VARIANTS | 0.865 | ādeśapratyayayoḥ | ā-deś-a-praty-ayay-oḥ |
| 8.3.60 | AGREES | 0.955 | śāsi-vasi-ghasīnāṃ ca | śāsi-vasi-ghasī-n-āṃ ca |
| 8.3.61 | VARIANTS | 0.889 | stauti-ṇyor eva ṣaṇy abhyāsāt | stau-ti-Ṇy-or eva ṣaṆ-i abhy-ās-āt |
| 8.3.62 | AGREES | 0.945 | saḥ svidi-svadi-sahīnāṃ ca | sa-ḥ svidi-svadi-sahī-n-āṃ ca |
| 8.3.63 | VARIANTS | 0.815 | prāk sitād aḍ vyavāye 'pi | prāk sit-āt aṬ=vy-av-āy-e api |
| 8.3.64 | VARIANTS | 0.800 | svādiṣv abhyāsena ca abhyāsasya | sthā=ādi-ṣu abhy-ās-ena ca abhy-ās-a-ya |
| 8.3.65 | VARIANTS | 0.899 | upasargāt sunoti-suvati-syati-stauti-stobhati-sthā-senaya-sedha-sica-sañja-svañjām | upa-sarg-āt su-no-ti-suv-a-ti-s-ya-ti-stau-ti-stobh-a-ti-sthā-sen-ay-a-sedha-sicA-sanjA-svanj-ām |
| 8.3.66 | VARIANTS | 0.897 | sadir aprateḥ | sadi-r a-prate-ḥ |
| 8.3.67 | AGREES | 0.941 | stanbheḥ | stanbhe-ḥ |
| 8.3.68 | VARIANTS | 0.781 | avāc ca ālaṃvana-āvidūryayoḥ | av-āt ca ā-lamb-ana-ā-vi-dūr-yaya-oḥ |
| 8.3.69 | VARIANTS | 0.844 | veś ca svano bhojane | ve-ś ca svan-aḥ bhoj-an-e |
| 8.3.70 | VARIANTS | 0.875 | parinivibhyaḥ seva-sita-saya-sivu-saha-suṭ-stu-svañjām | pari-ni-vi-bhyah sevasi-ta-say-a-sivḥ-sahA-suṬ-stu-sanj-ām |
| 8.3.71 | VARIANTS | 0.814 | sivādīnāṃ vā aḍvyavāye 'pi | siv-ādī-n-āṃ vā aṬ=vy-av-āy-e api |
| 8.3.72 | AGREES | 0.913 | anu-vi-pary-abhi-nibhyaḥ syandater aprāṇiṣu | anu-vi-pari-abhi-ni-bhyaḥ syand-a-te-r a-prāṇi-ṣu |
| 8.3.73 | VARIANTS | 0.898 | veḥ skander aniṣṭhāyām | ve-ḥ skande-r a-niṣṭhā-y-ām |
| 8.3.74 | AGREES | 0.941 | pareś ca | pare-ś ca |
| 8.3.75 | AGREES | 0.900 | pariskandaḥ prācyabharateṣu | pari-skand-a-ḥ prāc-ya-bharate-ṣu |
| 8.3.76 | AGREES | 0.919 | sphurati-sphulatyor nir-ni-vibhyaḥ | sphur-a-ti-sphul-a-ty-or nir-ni-vi-bhyaḥ |
| 8.3.77 | VARIANTS | 0.894 | veḥ skabhnāter nityam | ve-ḥ skabh-nā-te-r nitya-m |
| 8.3.78 | VARIANTS | 0.800 | iṇaḥ ṣīdhvaṃ-luṅ-liṭāṃ dho 'ṅgāt | iṆ-aḥ ṣī-dhvam-lUṄ-lIṬ-āṃ dh-aḥ aṛg-āt |
| 8.3.79 | AGREES | 0.960 | vibhāṣā+iṭaḥ | vibhāṣā iṬ-aḥ |
| 8.3.80 | VARIANTS | 0.783 | samāse 'ṅguleḥ saṅgaḥ | sam-ās-e aṛgule-ḥ saṛga-ḥ |
| 8.3.81 | AGREES | 0.933 | bhīroḥ sthānam | bhīro-ḥ sthāna-m |
| 8.3.82 | AGREES | 0.917 | agneḥ stut-stoma-somāḥ | agne-ḥ stu-t-stoma-som-ā-ḥ |
| 8.3.83 | VARIANTS | 0.857 | jyotir-āyuṣaḥ stomaḥ | jyotis=āyus-aḥ stoma-ḥ |
| 8.3.84 | AGREES | 0.905 | mātṛ-pitṛbhyāṃ svasā | mātṛ-pitṛ-bhyāṃ svasuḥ |
| 8.3.85 | VARIANTS | 0.842 | mātuḥpiturbhyāmanyatarasyām | mātur=pitur-bhyām anya-ara-yām |
| 8.3.86 | VARIANTS | 0.866 | abhinisaḥ stanaḥ śabdasañjñāyām | abhi+nis-aḥ stan-aḥ śabda-aṃjñā-y-ām |
| 8.3.87 | AGREES | 0.911 | upasarga-prādurbhyām astir y-ac-paraḥ | upa-sarg-a-prādur-bhyām as-ti-r y-aC-ara-ḥ |
| 8.3.88 | AGREES | 0.917 | su-vi-nir-durbhyaḥ supi-sūti-samāḥ | su-vi-nis-dur-bhyaḥ supi-sū-ti-sam-ā-ḥ |
| 8.3.89 | AGREES | 0.931 | ni-nadībhyāṃ snāteḥ kauśale | ni-nadī-bhyāṃ snā-te-ḥ kauśal-e |
| 8.3.90 | VARIANTS | 0.850 | sūtraṃ pratiṣṇātam | sūtra-m prati-ṣṇā-ta-m |
| 8.3.91 | VARIANTS | 0.833 | kapiṣṭhalo gotre | kapi-ṣṭhala-ḥ gotr-e |
| 8.3.92 | VARIANTS | 0.762 | praṣṭho 'gragāmini | pra-ṣṭha-ḥ agra-gām-in-i |
| 8.3.93 | AGREES | 0.902 | vṛkṣa-āsanayor viṣṭaraḥ | vṛkṣa=ās-anay-or vi-ṣṭar-a-ḥ |
| 8.3.94 | VARIANTS | 0.839 | chandonāmni ca | chandaḥ-nāmn-i ca |
| 8.3.95 | AGREES | 0.902 | gavi-yudhibhyāṃ sthiraḥ | gav-i-yudh-i-bhyāṃ sthi-ra-ḥ |
| 8.3.96 | AGREES | 0.949 | vi-ku-śami-paribhyaḥ sthalam | vi-ku-śami-pari-bhyaḥ sthal-a-m |
| 8.3.97 | AGREES | 0.918 | amba-āmba-go-bhūmi-savya-apa-dvi-tri-ku-śeku-śaṅkv-aṅgu-mañji-puñji-parame-barhir-divy-agnibhyaḥ sthaḥ | amba-āmba-go-bhūmi-savya-apa-dvi-tri-kuśe-ku-śaṛku-aṛgu-mañji-puñji-param-e-barhis=div-i=agni-bhyaḥ sta-ḥ |
| 8.3.98 | VARIANTS | 0.812 | suṣāmādiṣu ca | su-ṣāma(n)=ādi-ṣu ca |
| 8.3.99 | MISSING | - | - | eT-i saṃjñā-y-ām a-g-āt |
| 8.3.100 | MISSING | - | - | nakṣatr-āt vā |
| 8.3.99 (=B 8.3.101) | AGREES | 0.917 | hrasvāt tādau taddhite | hrasv-āt t-ād-au taddhit-e |
| 8.3.100 (=B 8.3.102) | VARIANTS | 0.630 | nisas tapatāv anasevane | nis-as tap-a-t-au an-ā-sev-an-e |
| 8.3.101 (=B 8.3.103) | VARIANTS | 0.848 | yuṣmat-tat-tatakṣuḥṣv antaḥpādam | yuṣmad=tad=tatakṣuḥ-ṣu antaḥ-āda-m |
| 8.3.102 (=B 8.3.104) | VARIANTS | 0.786 | yujuṣy ekeṣām | yajuṣ-i eke-ṣām |
| 8.3.103 (=B 8.3.105) | AGREES | 0.939 | stuta-stomayoś chandasi | stu-ta-stomay-oś chandas-i |
| 8.3.104 (=B 8.3.106) | AGREES | 0.909 | pūrvapadāt | pūrva-pad-āt |
| 8.3.105 (=B 8.3.107) | AGREES | 0.909 | suñaḥ | suÑ-aḥ |
| 8.3.106 (=B 8.3.108) | VARIANTS | 0.828 | sanoter anaḥ | san-o-te-r a-n-aḥ |
| 8.3.107 (=B 8.3.109) | VARIANTS | 0.863 | saheḥ pṛtana-rtābhyāṃ ca | sahe-ḥ pṛtanā=ṛ-tā-bhyāṃ ca |
| 8.3.108 (=B 8.3.110) | AGREES | 0.936 | na rapara-sṛpi-sṛji-spṛśi-spṛhi-savana-ādīnām | na ra-para-sṛpi-sṛji-spṛsi-spṛhi-sav-ana=ādī-n-ām |
| 8.3.109 (=B 8.3.111) | VARIANTS | 0.889 | sāt padādyoḥ | sāt-pada=ādy-oḥ |
| 8.3.110 (=B 8.3.112) | VARIANTS | 0.762 | sico yaṅi | sic-aḥ yaṄ-i |
| 8.3.111 (=B 8.3.113) | VARIANTS | 0.875 | sedhater gatau | sedh-a-ter ga-t-au |
| 8.3.112 (=B 8.3.114) | AGREES | 0.912 | pratistabdha-nistabdhau ca | prati-stab-dha- ni-stab-dh-au ca |
| 8.3.113 (=B 8.3.115) | AGREES | 0.923 | soḍhaḥ | soḍh-aḥ |
| 8.3.114 (=B 8.3.116) | VARIANTS | 0.783 | stambhusivusahāṃ caṅi | stanbhU-śivḥ-sah-āṃ CaṄ-i |
| 8.3.115 (=B 8.3.117) | VARIANTS | 0.842 | sanoteḥ sya-sanoḥ | su-no-te-ḥ sya-saN-oḥ |
| 8.3.116 (=B 8.3.118) | VARIANTS | 0.846 | sadiṣvañjoḥ parasya liṭi | sadi-svanj-oḥ para-sya lIṬ-i |
| 8.3.117 (=B 8.3.119) | VARIANTS | 0.684 | nivyabhibhyo 'ḍvyavāye vā chandasi | ni-vi=abhi-bhyaḥ aṬ=y-āv-ay-e vā chandas-i |
| 8.4.1 | VARIANTS | 0.820 | ra-ṣābhyāṃ no ṇaḥ samānapade | ra-ṣā-bhyām n-aḥ ṇa-ḥ samāna-ad-e |
| 8.4.2 | VARIANTS | 0.877 | aṭ-ku-pv-āṅ-num-vyavāye 'pi | aṬ-kU-pU=āṄ-nuM-vy-av-āy-e api |
| 8.4.3 | VARIANTS | 0.842 | pūrvapadāt sañjñāyām agaḥ | pūrva-pad-āt saṃ-jñā-y-ām a-g-aḥ |
| 8.4.4 | AGREES | 0.963 | vanaṃ puragā-miśrakā-sidhrakā-śārikā-koṭara-agrebhyaḥ | vana-m puragā-miśrakā-sidhrakā-śārikā-koṭara=agre-bhyaḥ |
| 8.4.5 | VARIANTS | 0.887 | pra-nir-antaḥ-śara-ikṣu-plakṣa-āmra-kārṣya-khadira-pīyūkṣābhyo 'sañjñāyām api | pra-nir=antar-śara=ikṣu-plakṣa-āmra-kārṣ-ya-khadira-piyūkṣā-bhyaḥ a-saṃ-ñā-y-ām api |
| 8.4.6 | VARIANTS | 0.862 | vibhāṣauṣadhivanaspatibhyaḥ | vibhāṣā oṣadhi-vanas-pati-bhyaḥ |
| 8.4.7 | VARIANTS | 0.643 | ahno 'dantāt | ahna-ḥ aT=ant-āt |
| 8.4.8 | VARIANTS | 0.848 | vāhanam āhitāt | vāh-ana-m ā-hi-t-āt |
| 8.4.9 | AGREES | 0.909 | pānaṃ deśe | pāna-ṃ deś-e |
| 8.4.10 | AGREES | 0.923 | vā bhāva-karaṇayoḥ | vā bhāv-a-kar-aṇay-oḥ |
| 8.4.11 | VARIANTS | 0.857 | prātipadikānta-num-vibhaktiṣu ca | prāti-pad-ika=anta-nuM-vi-hak-ti-ṣu ca |
| 8.4.12 | VARIANTS | 0.762 | ekājuttarapade ṇaḥ | eka=aC=uttara-pad-e ṇa-ḥ |
| 8.4.13 | AGREES | 0.900 | kumati ca | kU-mat-i ca |
| 8.4.14 | VARIANTS | 0.800 | upasargād asamāse 'pi ṇa-upadeśasya | upa-sarg-āt a-sam-ās-e api ṇa=pa-eś-a-ya |
| 8.4.15 | AGREES | 0.900 | hinu-mīnā | hi-nu=mī-nā |
| 8.4.16 | AGREES | 1.000 | āni loṭ | āni lOṬ |
| 8.4.17 | AGREES | 0.903 | ner gada-nada-pata-pada-ghu-mā-syati-hanti-yāti-vāti-drāti-psāti-vapati-vahati-śāmyati-cinoti-degdhiṣu ca | ne-rgadḥ-nadḥ-pata-padA-GHU-mā-sya-ti-han-ti-yā-ti-vā-ti-drā-ti-psā-ti-vap-a-ti-vah-a-ti-śām-ya-ti-ci-no-ti-deg-dhi-ṣu ca |
| 8.4.18 | VARIANTS | 0.729 | śeṣe vibhāṣā 'ka-khādāv-aṣānta upadeśe | śeṣ-e vibhāṣā a-ka-kha=ād-au-a-ṣa-nt-e=pa-deś-e |
| 8.4.19 | VARIANTS | 0.800 | aniteḥ | an-i-te-ḥ |
| 8.4.20 | AGREES | 0.909 | antaḥ | anta-ḥ |
| 8.4.21 | VARIANTS | 0.800 | ubhau sābhyāsasya | ubh-au sa=abhy-ās-a-sya |
| 8.4.22 | VARIANTS | 0.895 | hanter atpūrvasya | han-te-r aT-pūrva-sya |
| 8.4.23 | AGREES | 0.947 | va-mor vā | va-m-or vā |
| 8.4.24 | AGREES | 0.917 | antar adeśe | antar a-deś-e |
| 8.4.25 | AGREES | 0.900 | ayanaṃ ca | ay-ana-ṃ ca |
| 8.4.26 | VARIANTS | 0.818 | chandasy ṛdavagrahāt | chandas-i ṛT=ava-grah-āt |
| 8.4.27 | AGREES | 0.912 | naś ca dhātustha-uru-ṣubhyaḥ | nas=ca dhātu-stha=uru-ṣu-hyaḥ |
| 8.4.28 | CONFLICTS | 0.537 | upasargād bahulam | upa-sarg-āt an-oT-para=ḥ |
| 8.4.29 | VARIANTS | 0.800 | kṛty acaḥ | kṛt-i=aC-aḥ |
| 8.4.30 | AGREES | 0.957 | ṇer vibhāṣā | Ṇe-r vibhāṣā |
| 8.4.31 | VARIANTS | 0.703 | halaścejupadhāt | haL-aś ca iC=upa=dh-āt |
| 8.4.32 | VARIANTS | 0.812 | ijādeḥ sanumaḥ | iC=āde-ḥ sa-nuM-aḥ |
| 8.4.33 | AGREES | 0.977 | vā niṃsa-nikṣa-nindām | vā niṃsa-nikṣA-nind-ām |
| 8.4.34 | AGREES | 0.986 | na bhā-bhū-pū-kami-gami-pyāyī-vepām | na bhā-bhū-pū-kami-gami-pyāyĪ-vep-ām |
| 8.4.35 | VARIANTS | 0.786 | ṣāt padāntāt | ṣ-āt pada=ant-āt |
| 8.4.36 | VARIANTS | 0.812 | naśeḥ ṣāntasya | naś-eḥ ṣa-anta-sya |
| 8.4.37 | VARIANTS | 0.783 | padāntasya | pada=anta-sya |
| 8.4.38 | VARIANTS | 0.824 | padavyavāye 'pi | pada-vy-av-āy-e api |
| 8.4.39 | VARIANTS | 0.812 | kṣubhnādiṣu ca | kṣubh-nā=ādi-su ca |
| 8.4.40 | AGREES | 0.923 | s-toḥ ś-cunā ś-cuḥ | s-tO-ḥ ś-cU-nā ś-cU-ḥ |
| 8.4.41 | VARIANTS | 0.783 | ṣṭunā ṣuḥ | ṣ-ṭU-nā ṣ-ṭU-ḥ |
| 8.4.42 | VARIANTS | 0.783 | na padāntāṭ ṭor anām | na pada=ant-āt=ṭO-r a-n-ām |
| 8.4.43 | VARIANTS | 0.857 | toḥ ṣi | tO-ḥ ṣ-i |
| 8.4.44 | VARIANTS | 0.857 | śāt | ś-āt |
| 8.4.45 | VARIANTS | 0.742 | yaro 'nunāsike 'nunāsiko vā | yaR-aḥ anu-nāsik-e anu-nāskika-ḥ vā |
| 8.4.46 | VARIANTS | 0.800 | aco ra-hābhyāṃ dve | aC-aḥ ra-hā-bhyām dv-e |
| 8.4.47 | VARIANTS | 0.889 | anaci ca | an-aC-i ca |
| 8.4.48 | VARIANTS | 0.868 | na ādiny-ākrośe putrasya | na=ād-in-ī=ā-kroś-e putra-sya |
| 8.4.49 | VARIANTS | 0.632 | śaro 'ci | śaR-aḥ aC-i |
| 8.4.50 | AGREES | 0.900 | triprabhṛtiṣu śākaṭāyanasya | tri-pra-bhṛ-ti-ṣu śākaṭ-āyana-sya |
| 8.4.51 | AGREES | 0.927 | sarvatra śākalyasya | sarva-tra śākal-ya-sya |
| 8.4.52 | VARIANTS | 0.769 | dīrghād ācāryāṇām | dīrgh-āt ā-cār-yā-ṇ-ām |
| 8.4.53 | VARIANTS | 0.882 | jhalaṃ jaś jhaśi | jhaL-āṃ jaŚ jhaŚ-i |
| 8.4.54 | VARIANTS | 0.897 | abhyāse carca | abhy-ās-e caR ca |
| 8.4.55 | AGREES | 0.941 | khari ca | khaR-i ca |
| 8.4.56 | VARIANTS | 0.833 | vā+avasāne | vā ava-s-ā-n-e |
| 8.4.57 | VARIANTS | 0.787 | aṇo 'pragṛhyasya anunāsikaḥ | aṆ-aḥ a-pra-gṛh-ya-sya anu-āsika-ḥ |
| 8.4.58 | VARIANTS | 0.844 | anusvārasya yayi parasavarṇaḥ | anu-svār-a-sya yāY-i para-sa-arṇa-ḥ |
| 8.4.59 | VARIANTS | 0.828 | vā padāntasya | vā pada=anta-sya |
| 8.4.60 | VARIANTS | 0.857 | tor li | tO-r l-i |
| 8.4.61 | VARIANTS | 0.893 | udaḥ sthāstambhoḥ pūrvasya | ud-aḥ sthā-stanbhO-ḥ pūrva-sya |
| 8.4.62 | VARIANTS | 0.750 | jhayo ho 'nyatarasyām | jhaY-aḥ ha-ḥ anya-tara-syām |
| 8.4.63 | CONFLICTS | 0.560 | śaścho 'ṭi | ś-as cha-ḥ aṬ-i |
| 8.4.64 | VARIANTS | 0.809 | halo yamāṃ yami lopaḥ | haL-aḥ yaM-ām yaM-i lopa-ḥ |
| 8.4.65 | VARIANTS | 0.837 | jharo jhari savarṇe | jhaR-aḥ jhaR-i sa-varṇ-e |
| 8.4.66 | VARIANTS | 0.881 | udattād anudāttasya svaritaḥ | udātt-āt anudātta-sya svarita-ḥ |
| 8.4.67 | AGREES | 0.902 | na+udāttasvaritodayam a-gārghya-kāśyapa-gālavānām | na=udātta-svarita=udayam a-gārgya-kāśyapa-gālava-n-ām |
| 8.4.68 | AGREES | 1.000 | a a iti | a a iti |