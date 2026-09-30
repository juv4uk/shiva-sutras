# UPC-7: 7-bit text identities, switchable human layouts

**Status:** experimental engineering prototype for #27 and #29.

UPC-7 is the text domain candidate for SENS Text7. Its identities are the
seven-bit cells of **geometry v2** (`UPC7-GEOMETRY-v2.md`, `upc7_geometry.py`):

```text
CCxxxxx
00xxxxx  varga consonants        25 placed, 7 reserved
01xxxxx  non-varga consonants    18 placed, 14 reserved
10xxxxx  vowels                  32 placed, 0 reserved
11xxxxx  signs / operator glyphs 32 placed
```

107 cells are placed, 21 are reserved. Nothing here renumbers or invents a cell:
a sound the owner has not placed in the geometry stays **unassigned** and fails
closed.

## Two stages, one of them legacy

| stage | files | what it proves | status |
|---|---|---|---|
| **A: legacy donor** | `upc7.py`, `test_upc7.py` | the flat UPC-8 table lives below `0x80`; a layout can change without changing the code stream; near-equivalent sounds fail closed | **legacy**: a layout experiment against the old flat numbers. **Not** the final identity assignment |
| **B: geometry v2** | `upc7_geometry.py`, `test_upc7_geometry.py` | the class geometry partitions all 128 codes and compresses the owner-designed UPC-8 classes injectively | preferred assignment |
| **C: layouts on v2** | `upc7_layouts.py`, `test_upc7_layouts.py`, `upc7_table.py`, `upc7-table.tsv` | human spellings, built on the v2 cells; a generated machine table | current |

New work uses B and C. Stage A stays only as a donor witness.

## Layout law

A layout is a human input/output mapping over a code identity. It does not own
the identity.

```text
host spelling --encode(layout)--> UPC-7 codes --render(layout)--> host spelling
```

Changing the layout leaves the middle sequence unchanged. Host `str` is UI
transport; the value is the tuple of integers 0..127.

Layouts:

- `sa-slp1`: Sanskrit SLP1, complete for the geometry (below);
- `uk`: Ukrainian, partial (below);
- `bits`: exact seven-bit diagnostic cells, e.g. `0100101 0000001`.

Rules, each proved in `test_upc7_layouts.py`:

- the **direct cell spelling map** is injective: one direct spelling names one code;
- encoding uses the longest match and never performs implicit case/Unicode
  normalization (SLP1 `K` is not `k`);
- a layout may define an **explicit sequence normalization** whose spelling lowers
  to multiple already-placed cells; this makes source spelling intentionally
  many-to-one at the code-stream level, without creating a cell collision;
- a spelling the project knows but the geometry has not placed is rejected **as a
  whole**. `дж` has a dedicated cell and is never silently read as `д` + `ж`;
- an unplaced or reserved code cannot be rendered in a spelling layout, only in
  `bits`.

Example:

```text
sa-slp1: kit  ---->  the same code stream  ---->  uk: кіт
```

## Coverage today

**Sanskrit is complete.** All 42 canonical Śiva-sūtra sounds (25 varga, 8
non-varga, and the nine vowels a i u ṛ ḷ e o ai au) plus the long vowels ā ī ū ṝ ḹ,
anusvāra and visarga have a cell and an SLP1 spelling. `ai` and `au` are the long
forms of the `e` and `o` rows (class-10 spec §3.3).

**The base Ukrainian donor mapping has 21 letters:** к ґ т д н п б м (varga), і у
(vowels) and х ш ж й з с р л ф в г (non-varga). The 13 letters the donor calls
identity aliases of a Sanskrit sound (`UKRAINIAN_SHARED`) land on the same cell
as the Sanskrit sound; `test_donor_identity_aliases_share_the_sanskrit_code`
checks all 13 against the legacy donor. The #31 extension adds four vowels, four
affricates and softness `ь` without moving those base assignments.

**Extension cells (shiva-sutras#31, proposal awaiting owner sign-off).** Nine of the 30
reserved cells are used; 21 stay reserved:

| sound | cell | why there |
|---|---|---|
| а е о и | class 10, row 7 (4 cells) | the reserved vowel row; its low 2 bits are an *index*, not nasal/length; `ac aṇ ik` read rows 0..6 and never see it |
| ц ч дз дж | class 01, place 7 (4 cells) | the reserved non-varga place, exactly 4 cells |
| ь (softness) | class 01, place 1 (palatal), slot 3 | next to ś ж й, the palatal place; class 11 is full (32/32) |

Everything else is a **sequence of placed cells**, never a cell of its own:
palatalised consonants are consonant + `ь` (`ть`, `ль`); iotated `є ї ю я` are `й` +
`е і у а`; `щ` is `ш` + `ч`. Sequences encode but never render back as one letter
(`я` renders `йа`). `дж` is one cell and is never read as `д`+`ж`.

### Ukrainian normalization law

For the proposed Ukrainian layout, canonical identity is the UPC-7 code stream,
not exact Unicode orthography. Therefore the explicit sequence spellings are
intentional normalizations:

```text
я  == йа
ю  == йу
є  == йе
ї  == йі
щ  == шч
```

The equalities above mean “encode to the same UPC-7 stream”, not “the Unicode
strings are identical”. Rendering uses the placed-cell spellings, so these streams
render as `йа`, `йу`, `йе`, `йі`, `шч`.

This is a boundary/layout rule, not a cell alias and not a Sanskrit identity claim.
A consumer such as SENS Text7 that adopts this layout therefore adopts this
normalization as part of human-source lowering. Exact original orthography, if a
caller needs it for provenance/editor fidelity, must stay outside canonical Text7.

Cost: no previously assigned code moved; the 9 changed table rows were all
`reserved`. The table SHA-256 changes, so consumers must re-pin.

So `кіт`, `привіт`, `мама`, `цар`, `час`, `дзвін`, `тінь` encode, switch layout and
round-trip.

## Open points

- The phonemic identity of а е о (Ukrainian [ɑ ɛ ɔ]) versus the Sanskrit rows is
  **not** claimed: they get their own cells rather than aliases, so no Sanskrit
  code is reinterpreted.
- Long/nasal Ukrainian vowels do not exist, so row 7 needs no such bits.

Other facts a reader should know:

- **Nasal vowel cells exist** (28 = 7 rows × oral/nasal × short/long) but SLP1 has no
  single spelling for them: `aM` is two cells, the vowel and the anusvāra sign. They
  are reachable only through `bits`.
- **Class 11 has both avagraha and apostrophe, danda and dot,** written with the same
  ASCII glyph. `sa-slp1` gives `'` and `.` (and `..`) to the Sanskrit signs; `uk` gives
  them to the apostrophe and the dot. The same glyph is therefore a different code in
  the two layouts.

## Signs are Text codes, not function identities

Class 11 holds `( ) " \ + - * / = < > ? ! ' . , : ; # @` and more. These are UPC-7
**Text** codes. In Text they are data. In SENS operator position the reader may take
`+` as human surface for a Function8 and lower it; the UPC-7 code is never the
function identity. Whether `(` and `)` are structure or text is decided by reader
context, not by this table.

## Machine table and pinning

`upc7-table.tsv` is the complete 128-cell table, **generated** by `upc7_table.py`:

```text
python3 upc7_table.py --write     regenerate
python3 upc7_table.py --check     exit 1 if the file is stale (CI runs this)
python3 upc7_table.py --sha256    print the SHA-256
```

Columns: `bits hex class payload status name sa-slp1 uk`. Spellings are projections; a
blank cell means the layout has no spelling. Letters are written as themselves;
backslash, space and control characters are escaped as `\\` and `\xNN`.

A consumer such as SENS Text7 should **pin the SHA-256 of this file** and regenerate
against a new one, not copy the table by hand. Any change of a cell, a name or a
spelling changes the SHA.

### Independent cold witness

`upc7_cold_verify.c` is a second implementation substrate for the serialized
machine contract. It deliberately imports no Python UPC-7 module and treats
`upc7-table.tsv` as opaque external input.

It independently checks:

- exactly 128 ordered seven-bit cells;
- agreement of binary code, hexadecimal code, 2-bit class and 5-bit payload;
- assigned versus unassigned (`reserved` in the current table vocabulary);
- class-consistent stable machine names;
- no human spelling on an unassigned cell;
- injectivity of the `sa-slp1` and `uk` projections.

`upc7-table.sha256` pins the exact table bytes. CI compiles the verifier with a
plain C11 compiler, checks the pin, runs the cold witness, and proves that both a
mutated identity row and mutated table bytes fail closed.

The C verifier is a conformance witness, not a second UPC-7 authority. Cell
identity still comes from the generated table/geometry and changes only through
an explicit owner-ratified assignment.

## Relation to SENS

```text
SENS
  structure : ( )
  Function  : 8-bit
  Number    : binary
  Text      : sequence of UPC-7 identities
```

Python/Unicode strings in these prototypes are host UI transport only. They are not
UPC-7 identities and are not proposed as SENS Text.

## Storage width

UPC-7 is logically seven bits. The Python prototype returns integer tuples, so host
memory may spend 8+ bits per cell. Bit-packing is a separate transport problem and
must not be confused with the code width; a packed form can store 8 cells in 7 bytes
without changing identity, but it needs its own round-trip tests.

## Non-claim

This is an engineering codec and projection. It is not evidence that Pāṇini used
binary codes, and it does not modify the transmitted Śiva-sūtra canon.

## SENS-native cold witness (second witness for #33)

The C11 witness (`upc7_cold_verify.c`, #36) already closed #33. This is a **second, SENS-native**
witness, so the table is read by three substrates: the Python producer, the C verifier and
SENS itself (the #33 issue text preferred a SENS reader; a SENS consumer of Text7 can run it).

`upc7_cold_witness.lisp` is an independent reader of the generated `upc7-table.tsv`,
written in SENS Lisp. It imports nothing from `upc7_geometry.py`, `upc7_layouts.py` or
`upc7_table.py`; it re-derives every cell's bits, hex, class and payload from the **row
position alone** and checks the table against the geometry laws (25 varga cells, the
vowel nasal/length bits with row 7 as the extension row, class/name agreement), not
against Python output.

```
sens prototype/upc7_cold_witness.lisp        # from the repository root
```

It checks: the table's SHA-256 against a pin in the witness; exactly 128 cells, once each,
in ascending order; bits/hex/class/payload per row; assigned vs reserved (a reserved cell
has no spelling and a canonical `reserved.<class>.<payload>` name); the varga 5x5 law; the
vowel law; uniqueness of stable names and of `sa-slp1`/`uk` spellings among assigned
cells. It then proves it is not vacuous: it rejects a dropped row, a flipped status, a
wrong bits field, a wrong hex field, a name that contradicts the class, and any one-field
change (by the pin).

**The pin is a decision, not a convenience.** When the table changes on purpose, update
`pinned-sha256` in the witness in the same commit as `upc7-table.sha256` and the C witness; a table that changes without the pin
fails.

Evidence on record (local run, `sens` release built from sens `9adb654b`, not CI):
- current table (`8ce2339a…`): all 8 witness lines pass;
- pre-#32 table (`aa46e37f…`) against the current pin: fails on the SHA pin only; with
  its own SHA as the pin it passes every structural witness, i.e. the geometry laws hold
  for both revisions.

Not covered (open, do not read this as done): encoding text through a layout and
round-tripping code streams (the witness reads the table, it does not implement a
layout encoder); a CI job (needs a `sens` checkout, see #26); independence is between two
implementations by the same author, not two parties.
