# Проєкт дослідження Śiva-sūtras

Цей репозиторій призначений для фундаментального дослідження системи **Śiva-sūtras** (елемента граматики Паніні).

## Головне правило
Ми діємо як **дослідники, а не знавці**. Наша мета — не довести, що Śiva-sūtras є "давнім машинним кодуванням", а зменшити область невідомого щодо їхньої внутрішньої логіки та властивостей. Будь-який негативний результат (спростування красивої гіпотези) є успішним розширенням карти знань.

## Структура репозиторію

- `/ksetra`: Суворі епістемічні шари (канон, використання Паніні, традиційні коментарі, сучасна лінгвістика).
- `/journal`: Незмінний журнал досліджень (Immutable Research Journal). Усі гіпотези, експерименти та результати фіксуються тут.
- `/experiments`: Експериментальні майданчики (напр., перестановка звуків, відтворення механіки pratyāhāra).
- `/hypotheses`: Гіпотези. Ранні інженерні ідеї (Śabda) заморожені у `/hypotheses/shabda`.

## Методологія
1. Встановити канон (джерелознавство).
2. Дослідити функцію в Aṣṭādhyāyī (усі випадки використання pratyāhāra).
3. Відновити механіку без сучасних комп'ютерних аналогій.
4. Дослідити властивості порядку звуків через експерименти.
5. Провести adversarial тестування ("hostile review").

## Поточний статус (Етап 6: Blind Semantic Reconstruction)
Ми завершили створення найстрогішого в історії пайплайну для сліпої реконструкції фонологічних правил (без оглядки на цільові класи Śiva-sūtras). Дослідження розділилося на підготовку доказового шару та експертну верифікацію.

### Ключові досягнення:
- **High-Recall Candidate Annotation**: Створено алгоритм для виявлення кандидатів на фонологічні правила. Відсіяно 3983 сутри, заморожено список-кандидатів.
- **Епістемічний Evidence Layer (Validator v2)**: Впроваджено строгий контроль доказів. Валідатор блокує будь-яке автоматичне привласнення статусу `RESOLVED` без чітких текстових доказів з Kāśikā (Authentic Source Gate).
- **Відкриття: Reproducibility ≠ Authenticity**: Виявлено фундаментальний методологічний факт, що криптографічна відтворюваність (checksum) доводить лише тотожність байтів, а не їхнє історичне походження. Зроблено розподіл осей `integrity` та `provenance`.

### Головні артефакти та звіти:
- **Blind Expert Pilot (Batch 2)**: 30 сутр, розібраних експертом на синтетичному (але криптографічно відтворюваному) корпусі.
  - [batch_2_expert_blind_30.yaml](file:///C:/GitHub/shiva-sutras/ksetra/astadhyayi/blind/semantic_batch_2/batch_2_expert_blind_30.yaml)
  - [simulate_expert_reconstruction.py](file:///C:/GitHub/shiva-sutras/experiments/blind_reconstruction/simulate_expert_reconstruction.py)
  - [compare_auto_expert.py](file:///C:/GitHub/shiva-sutras/experiments/blind_reconstruction/compare_auto_expert.py)
- **Звіти Експертного Виграшу (Expert Gain)**:
  - [batch_2_synthetic_expert_gain_report.md](file:///C:/Users/user/.gemini/antigravity-ide/brain/09507e3f-a04d-486e-ae1f-f594c1b203bd/batch_2_synthetic_expert_gain_report.md) — фіксує `EG_{synthetic-evidence}` та FCR (False Certainty Rate: 83.3%).
  - [batch_1_epistemic_report.md](file:///C:/Users/user/.gemini/antigravity-ide/brain/09507e3f-a04d-486e-ae1f-f594c1b203bd/batch_1_epistemic_report.md)
  - [track_ab_audit_report.md](file:///C:/Users/user/.gemini/antigravity-ide/brain/09507e3f-a04d-486e-ae1f-f594c1b203bd/track_ab_audit_report.md)
- **Автентифікація Джерел**:
  - [source_collector.py](file:///C:/GitHub/shiva-sutras/experiments/blind_reconstruction/source_collector.py) та [source_authenticator.py](file:///C:/GitHub/shiva-sutras/experiments/blind_reconstruction/source_authenticator.py)
  - [validator_v2.py](file:///C:/GitHub/shiva-sutras/experiments/blind_reconstruction/validator_v2.py)
- **Історичний Walkthrough**: [walkthrough.md](file:///C:/Users/user/.gemini/antigravity-ide/brain/09507e3f-a04d-486e-ae1f-f594c1b203bd/walkthrough.md) (повний хронологічний літопис відкриттів).
