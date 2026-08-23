# saṃjñā-kośa — канонічний словник тегів Vault

**Статус:** CANONICAL · **Дата:** 2026-08-23
**Автор:** Volodymyr (дизайн) + Оксі (Vyasa, документація)
**Правило:** кожен термін має ОДНУ стабільну функцію. Санскрит не декор.

---

## Осі

| Функція | Санскрит | Сенс |
|---|---|---|
| project | `kṣetra` | поле, область діяльності |
| type | `rūpa` | форма документа |
| status | `avasthā` | стан |
| domain/topic | `viṣaya` | предметна область |
| source/evidence | `pramāṇa` | засіб достовірного пізнання |

## Типи (rūpa)

| Тег | Санскрит | Сенс |
|---|---|---|
| `rūpa/nirṇaya` | nirṇaya | рішення |
| `rūpa/prastāva` | prastāva | пропозиція |
| `rūpa/prayoga` | prayoga | експеримент |
| `rūpa/phala` | phala | результат |
| `rūpa/viphalatā` | viphalatā | невдача |
| `rūpa/pramāṇa` | pramāṇa | доказ |
| `rūpa/lakṣaṇa` | lakṣaṇa | специфікація |
| `rūpa/racanā` | racanā | архітектура |
| `rūpa/yojanā` | yojanā | план |
| `rūpa/vṛttānta` | vṛttānta | журнал |
| `rūpa/samarpaṇa` | samarpaṇa | handoff |
| `rūpa/mūla` | mūla | джерело |
| `rūpa/saṃvāda` | saṃvāda | діалог |

## Стани (avasthā)

| Тег | Санскрит | Сенс |
|---|---|---|
| `avasthā/prastutā` | prastutā | запропоновано |
| `avasthā/pravṛddha` | pravṛddha | активна |
| `avasthā/siddhā` | siddhā | підтверджена |
| `avasthā/aṃśikī` | aṃśikī | часткова |
| `avasthā/aniścitā` | aniścitā | невизначена |
| `avasthā/khaṇḍitā` | khaṇḍitā | спростована |
| `avasthā/ruddhā` | ruddhā | заблокована |
| `avasthā/atikrāntā` | atikrāntā | замінена |
| `avasthā/saṃgrahītā` | saṃgrahītā | заархівована |

## Джерела (pramāṇa)

| Тег | Сенс |
|---|---|
| `pramāṇa/anubhava` | безпосередній досвід |
| `pramāṇa/śabda` | свідоцтво / звіт іншого |
| `pramāṇa/anumāna` | висновок |
| `pramāṇa/parīkṣā` | експеримент / тест |
| `pramāṇa/grantha` | текст / книга |
| `pramāṇa/saṃvāda` | розмова / сесія |

## Приклад правильної нотатки

```yaml
---
tags:
  - kṣetra/my-lisp
  - rūpa/nirṇaya
  - avasthā/siddhā
  - viṣaya/smṛti
  - pramāṇa/parīkṣā
---
```

---

## Правила

1. Кожен термін має одну стабільну роль. Не використовувати синоніми.
2. Якщо термін незнайомий — дивитись у цей файл, не вигадувати.
3. Нові терміни додаються тільки через власника.
4. Не більше 5–8 тегів на документ.
5. Unknown > invented: краще пропустити вісь ніж вигадати значення.
