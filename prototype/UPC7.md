# UPC-7: 7-bit text identities, switchable human layouts

**Status:** experimental engineering prototype for #27 and #29.

UPC-7 is the text domain candidate for SENS Text7. Its identities are the
seven-bit cells of **geometry v2** (`UPC7-GEOMETRY-v2.md`, `upc7_geometry.py`):

```text
CCxxxxx
00xxxxx  varga consonants        25 placed, 7 reserved
01xxxxx  non-varga consonants    13 placed, 19 reserved
10xxxxx  vowels                  28 placed, 4 reserved
11xxxxx  signs / operator glyphs 32 placed
```

98 cells are placed, 30 are reserved. Nothing here renumbers or invents a cell:
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

- a layout is injective: one spelling names one code;
- encoding uses the longest match and never normalises (SLP1 `K` is not `k`);
- a spelling the project knows but the geometry has not placed is rejected **as a
  whole**. `дж` is never silently read as `д` + `ж`;
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

**Ukrainian has 21 letters:** к ґ т д н п б м (varga), і у (vowels) and х ш ж й з с
р л ф в г (non-varga). The 13 letters the donor calls identity aliases of a
Sanskrit sound (`UKRAINIAN_SHARED`) land on the same cell as the Sanskrit sound;
`test_donor_identity_aliases_share_the_sanskrit_code` checks all 13 against the
legacy donor.

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
