# UPC-7 geometry candidate v2

Status: executable candidate for #29. This supersedes the idea that final
UPC-7 identity is merely the lower 0x00..0x7F half of the older flat
`prototype/upc8.py` table.

## Why the first projection was insufficient

The older Python UPC-8 donor table assigns its live entries below 0x80, and
that made an identity-preserving 7-bit projection useful as a first layout
experiment. Newer owner-designed UPC-8 work has a stronger geometry:

```text
00xxxxxx varga consonants
01xxxxxx non-varga consonants
10xxxxxx vowels
11xxxxxx signs
```

The vowel design actively uses 0x80..0xBF. Therefore UPC-7 should compress
the class geometry, not preserve the old flat numeric assignment.

## Seven-bit shape

```text
CCxxxxx

00xxxxx  varga consonants
01xxxxx  non-varga consonants
10xxxxx  vowels
11xxxxx  signs / human-surface operator glyphs
```

Every class has 32 cells.

### 00 — varga

Five places × five classical members = 25 cells:

```text
payload = place * 5 + member
```

Seven cells remain reserved.

### 01 — non-varga

```text
payload[4:2] = macro-place
payload[1:0] = local slot
```

This intentionally preserves the currently used Sanskrit/Ukrainian
distinctions, not all 64 hypothetical points of UPC-8 class 01.

The current 13-point union compresses injectively.

### 10 — vowels

Direct compression of the accepted UPC-8 class-10 design:

```text
UPC-8  10 ppp f n l
UPC-7     10 ppp n l
                ^
             remove only FREE bit
```

Rows 0..6 × {plain,nasal} × {short,long} = 28 cells. Row 7 remains four
reserved cells.

### 11 — signs/operators

All 32 cells are named in the executable candidate. These are Text7 code
identities. They are **not SENS Function8 identities**.

A glyph such as `+` can therefore have two distinct roles depending on the
reader context:

```text
inside Text:
    '+' -> UPC-7 sign code -> Text7 data

in human operator position:
    '+' -> surface resolver -> Function8 for plus
```

The UPC-7 code is never the function identity.

The same applies to apostrophe, dot, comma, backquote, hash dispatch-style
glyphs, etc. A SENS canonical core may choose to retain only parentheses as
structural delimiters and lower the rest as human reader sugar.

## Lisp note

Traditional Lisp has more reader syntax than parentheses in many dialects:
apostrophe for quote, dot for dotted pairs, backquote/comma for quasiquote,
`#` dispatch macros, quotes for strings, semicolon comments, and others.
These are reader conventions, not a reason to create extra SENS value
domains. Arithmetic/comparison glyphs are normally names of functions, not
primitive punctuation operators.

## Files

- `upc7_geometry.py` — executable geometry
- `test_upc7_geometry.py` — collision and partition witnesses
