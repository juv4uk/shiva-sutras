# Results Ledger

Цей реєстр фіксує строгі твердження (claims), згенеровані під час проєкту. Усі твердження жорстко обмежені своїм Scope. Будь-яке цитування результату поза його Scope вважається епістемічною помилкою.

| Claim ID | Claim | Scope | Status | Artifact / Proof | Depends On | Supersedes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `M-001` | Неможливість унікальної C1P топології. Існує понад 10,000 валідних перестановок. | Within the current 42-class formal model. | `PROVED` | `experiments/ordering/c1p_sat_ablation.py` | `K-001` (42-class definition) | - |
| `M-002` | Глобальний мінімум маркерів ($M_{min}$) дорівнює 14. | Within the current 42-class formal model under standard interval representation. | `PROVED` | CP-SAT UNSAT proof (`experiments/ordering/marker_optimizer.py`) | `M-001`, `K-001` | - |
| `M-003` | Існує рівно 2 структурні класи, що досягають $M_{min}=14$. | Within the current 42-class formal model. | `PROVED` | Exhaustive exclusion proof. | `M-002` | - |
| `M-004` | 15 класів формують MUC (Minimal Unsatisfiable Core), що породжує глобальну складність системи. | Within the current 42-class formal model. | `PROVED` | Greedy deletion algorithm | `M-002` | - |
| `M-005` | Канонічна структура (Class B) є єдиною, що дозволяє безколізійну ідентифікацію маркерів. | Within the 2 optimal structural classes. | `PROVED` | Address Semantics Fingerprint | `M-003` | - |
| `L-001` | Канонічні 42 класи можуть бути "наосліп" виведені з фонологічних правил без попереднього знання Śiva-sūtras. | Aṣṭādhyāyī corpus. | `OPEN (NOT YET)` | Stage 6 (Blind Semantic Reconstruction) | `L-002` | - |
| `L-002` | Доступний незалежний, достовірний лінгвістичний корпус (Provenance). | Kāśikā / Aṣṭādhyāyī texts. | `UNRESOLVED` | External Source Gate blocked by 404/403. | - | `L-000` (Direct Scrape) |
| `E-001` | Відтворюваність (checksum match) доводить історичну автентичність. | Epistemic Pipeline. | `FALSIFIED` | `validator_v2.py` / `EPISTEMIC_CONTRACT.md` | - | - |
| `E-002` | Автоматичний семантичний агент генерує FCR (False Certainty Rate) 83.3% на нестачі доказів. | Synthetic Batch-2 benchmark. | `MEASURED` | `batch_2_synthetic_expert_gain_report.md` | `E-001` | - |
