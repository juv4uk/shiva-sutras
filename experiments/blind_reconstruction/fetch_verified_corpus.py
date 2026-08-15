# Verified Corpus Acquisition

Цей скрипт є частиною гейту достовірних даних для Blind Reconstruction.

## Статус: REPLACED

Колишній плейсхолдер `verified_ashtadhyayi.txt` (фіктивна заявка `AUTHENTICITY-VERIFIED`)
**не існує** у репозиторії та був видалений з git. Заявка про нього в README була
False Certainty — саме та епістемічна помилка, проти якої виступає проєкт (E-001).

Справжній механізм придбання корпусу тепер:

1. `fetch_gretil_corpus.py` — завантажує GRETIL-джерела (Kāśikāvṛtti Sharma ed.,
   Aṣṭādhyāyī Baums transcription) і фіксує provenance: URL, sha256, розмір, дата,
   редакція, ліцензія → `external_data/gretil_raw/manifest.json`.
2. `parse_gretil.py` — парсить HTML у структурований корпус
   (`external_data/gretil_kasika_corpus.json`, `gretil_astadhyayi.json`).
3. `cross_witness_diff.py` — порівнює два незалежні свідки та видає звіт.
4. `generate_real_sources.py` — генерує `ksetra/astadhyayi/sources/KASIKA-*.yaml`
   зі статусом `REAL` / `AUTHENTICITY-VERIFIED (Attributed)`.

Жоден з етапів не виконується, поки попередній не створив артефакт із sha256.
FAIL-CLOSED: без `external_data/gretil_raw/manifest.json` корпус вважається відсутнім.
