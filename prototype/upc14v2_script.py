#!/usr/bin/env python3
"""Spelling views of the 42 sounds: IAST, Devanagari and Ukrainian Cyrillic.

The graph (`upc14v2`) never needed a spelling: a sound is its code. SLP1, the case-sensitive
ASCII notation (k and K are two sounds) it used before, is gone (owner's decision, 2026-10-01).
The scripts the project keeps are IAST (lowercase Latin with diacritics, for reading), Devanagari
(the native one) and Cyrillic (from a Ukrainian book). They are VIEWS: `to_iast(code)` and the
like read a code, `code_from_iast(text)` and the like read a spelling; `encode_text` and
`decode_text` do the same for a whole sequence, with no ambiguity. Identity stays the code.

Length and nose are coordinates of the code, so they are spelled by a rule, not listed:
long vowel = the long form (ā ī ū ṝ; Devanagari आ ई ऊ ॠ), nasal = a combining tilde
(IAST) or candrabindu (Devanagari). The spelling table is keyed by the IAST name of the sound (the keys of `upc14v2.SOUNDS`).

A consonant in Devanagari is written bare with virama (क्), a vowel as its independent letter.

Cyrillic (`to_cyrillic`, `code_from_cyrillic`) follows the Ukrainian book "Бгаґавад-ґіта як вона є",
section "Як читати санскрит", pp. 810-812 (edition and year: unknown, to be added from the title page),
which says its transliteration is a calque of Judith Tyberg's Latin one: Latin letters replaced by
Cyrillic ones, diacritics kept. From the book (read by the author from the owner's photos): g = ґ and
every aspirate = the stop + г (кг ґг чг джг т̣г д̣г тг дг пг бг), y = й, ai = аі, au = ау, h = х,
ś = ш́, ṣ = ш̣, ṛ = р̣, ḷ = л̣, long vowels with a macron. Not yet read with certainty (photo too
small): the exact marks on ṅ and ñ (this table has н̇ and н̃) and ṇ. The book also gives anusvara ṃ = м̇
and visarga ḥ = х̣ (outside the 42 sounds). It is a VIEW: a sound's identity is its code, not a Cyrillic spelling.
Strings are NFC-normalised on both sides (some marks compose, ӯ).
"""

from __future__ import annotations

import unicodedata

from typing import Dict

import upc14v2 as g
import upc14v2_sandhi as sd

# one row per sound: IAST name -> (IAST, Devanagari, Cyrillic)
_ROWS = {
    "a": ("a", "अ", "а"), "i": ("i", "इ", "і"), "u": ("u", "उ", "у"), "ṛ": ("ṛ", "ऋ", "р̣"), "ḷ": ("ḷ", "ऌ", "л̣"),
    "e": ("e", "ए", "е"), "o": ("o", "ओ", "о"), "ai": ("ai", "ऐ", "аі"), "au": ("au", "औ", "ау"),
    "k": ("k", "क्", "к"), "kh": ("kh", "ख्", "кг"), "g": ("g", "ग्", "ґ"), "gh": ("gh", "घ्", "ґг"), "ṅ": ("ṅ", "ङ्", "н̇"),
    "c": ("c", "च्", "ч"), "ch": ("ch", "छ्", "чг"), "j": ("j", "ज्", "дж"), "jh": ("jh", "झ्", "джг"), "ñ": ("ñ", "ञ्", "н̃"),
    "ṭ": ("ṭ", "ट्", "т̣"), "ṭh": ("ṭh", "ठ्", "т̣г"), "ḍ": ("ḍ", "ड्", "д̣"), "ḍh": ("ḍh", "ढ्", "д̣г"), "ṇ": ("ṇ", "ण्", "н̣"),
    "t": ("t", "त्", "т"), "th": ("th", "थ्", "тг"), "d": ("d", "द्", "д"), "dh": ("dh", "ध्", "дг"), "n": ("n", "न्", "н"),
    "p": ("p", "प्", "п"), "ph": ("ph", "फ्", "пг"), "b": ("b", "ब्", "б"), "bh": ("bh", "भ्", "бг"), "m": ("m", "म्", "м"),
    "y": ("y", "य्", "й"), "r": ("r", "र्", "р"), "l": ("l", "ल्", "л"), "v": ("v", "व्", "в"),
    "ś": ("ś", "श्", "ш́"), "ṣ": ("ṣ", "ष्", "ш̣"), "s": ("s", "स्", "с"), "h": ("h", "ह्", "х"),
}
_N = unicodedata.normalize
# long vowel: the long form of the base spelling (a rule on four vowels; ḷ has none)
_LONG = (
    {"a": "ā", "i": "ī", "u": "ū", "ṛ": "ṝ"},
    {"अ": "आ", "इ": "ई", "उ": "ऊ", "ऋ": "ॠ"},
    {"а": "а\u0304", "і": "і\u0304", "у": "у\u0304", "р\u0323": "р\u0323\u0304"},
)
_NASAL = ("\u0303", "\u0901", "\u0303")   # combining tilde, candrabindu, combining tilde
# pluta: the digit 3 after the vowel (Kasika corpus: bho3i, 6451 uses of the Devanagari digit); the canonical spelling
# writes the LONG form of a i u ṛ first (ā3, ī3: the corpus has ā3 43 times against a3 once), then the nose, then the 3
_PLUTA = ("3", "\u0969", "3")
_SCRIPTS = ("iast", "devanagari", "cyrillic")
_DEV_VIRAMA = "\u094d"


def _plain(v: "g.Vertex") -> int:
    return g.Vertex(v.place, 0, v.aperture, v.length, v.voice, v.asp).code


def _vowel_base(v: "g.Vertex") -> int:
    """The plain vowel of this place, aperture, voice and aspiration: the short one if it exists, else the long."""
    for length in (g.SHORT, g.LONG):
        code = g.Vertex(v.place, 0, v.aperture, length, v.voice, v.asp).code
        if code in g.LABELS_BY_CODE:
            return code
    raise g.GraphError(f"{g.bits(g.Vertex(v.place, v.nasal, v.aperture, v.length, v.voice, v.asp).code)} has no spelling")


def _pluta(code: int) -> int:
    v = g.unpack(code)
    return g.Vertex(v.place, v.nasal, v.aperture, g.PLUTA, v.voice, v.asp).code


def _spell_pluta(code: int, column: int) -> str:
    v = g.unpack(code)
    key = g.LABELS_BY_CODE[_vowel_base(v)]
    text = _ROWS[key][column]
    if key in ("a", "i", "u", "ṛ"):
        text = _LONG[column][text]
    if v.nasal:
        text += _NASAL[column]
    text = _N("NFC", text + _PLUTA[column])
    if _FROM[column].get(text) != code:
        raise g.GraphError(f"{g.bits(code)} has no spelling in {_SCRIPTS[column]}")
    return text


def _spell(code: int, column: int) -> str:
    """Spell a code: base sound, then long, then nasal, then pluta (the rule, not a list).

    Fails closed: a code that does not read back to itself (a long ḷ, a short e/o/ai/au,
    a nasal r) raises GraphError instead of being written as some other sound.
    """
    v = g.unpack(code)
    if v.aperture >= g.VOWEL and v.length == g.PLUTA:
        return _spell_pluta(code, column)
    if v.nasal and v.aperture == g.SEMIVOWEL:        # y~ v~ l~ (8.4.45); r has no nasal form (Kasika 391)
        key = g.LABELS_BY_CODE.get(_plain(v))
        if key not in ("y", "v", "l"):
            raise g.GraphError(f"{g.bits(code)} has no spelling")
        return _N("NFC", _ROWS[key][column] + _NASAL[column])
    base = sd.base(code)
    key = g.LABELS_BY_CODE.get(base)
    if key is None:
        raise g.GraphError(f"{g.bits(code)} has no spelling")
    text = _ROWS[key][column]
    if v.aperture >= g.VOWEL and v.length == g.LONG and key in ("a", "i", "u", "ṛ"):
        text = _LONG[column][text]
    if v.nasal and v.aperture >= g.VOWEL:
        text += _NASAL[column]
    text = _N("NFC", text)
    if _FROM[column].get(text) != code:
        raise g.GraphError(f"{g.bits(code)} has no spelling in {_SCRIPTS[column]}")
    return text


def to_iast(code: int) -> str:
    return _spell(code, 0)


def to_devanagari(code: int) -> str:
    return _spell(code, 1)


def to_cyrillic(code: int) -> str:
    return _spell(code, 2)


def _reader(column: int) -> Dict[str, int]:
    table = {row[column]: g.SOUNDS[key] for key, row in _ROWS.items()}
    out = dict(table)
    for short, long_ in _LONG[column].items():
        out[long_] = g.e_long(table[short])
    for text, code in list(out.items()):
        if g.unpack(code).aperture >= g.VOWEL:
            out[text + _NASAL[column]] = g.e_nasal(code)
    for text, code in list(out.items()):               # pluta: short or long (+ nose) + 3; only the long form is canonical
        v = g.unpack(code)
        if v.aperture >= g.VOWEL and v.length != g.PLUTA:
            out[text + _PLUTA[column]] = _pluta(code)
    for key in "yvl":                                   # y~ v~ l~ (8.4.45)
        v = g.unpack(g.SOUNDS[key])
        nasal_code = g.Vertex(v.place, 1, v.aperture, v.length, v.voice, v.asp).code
        out[_ROWS[key][column] + _NASAL[column]] = nasal_code
    return {_N("NFC", k): c for k, c in out.items()}


_FROM = tuple(_reader(i) for i in range(3))


def _read(text: str, column: int) -> int:
    try:
        return _FROM[column][_N("NFC", text)]
    except KeyError:
        raise g.GraphError(f"{text!r} is not a {_SCRIPTS[column]} sound of this graph") from None


def code_from_iast(text: str) -> int:
    return _read(text, 0)


def code_from_devanagari(text: str) -> int:
    return _read(text, 1)


def code_from_cyrillic(text: str) -> int:
    return _read(text, 2)


# ---------------------------------------------------------------------------
# Texts: a SEQUENCE of sounds <-> a string, in each script, with no ambiguity.
# ---------------------------------------------------------------------------
#
# `decode_text(encode_text(seq, script), script) == seq` for every sequence, and so
# `encode_text` is injective: two different sequences never give the same string.
#
# IAST and Cyrillic: tokens are written side by side; where the concatenation could be read
# another way (k+h / kh, a+i / ai, а+й / ай) a middle dot "·" (U+00B7) separates them. The
# decoder reads the longest token, and "·" only marks a boundary. (ISO 15919 uses the same
# dot for this; the author's recollection, not checked here.)
#
# Devanagari follows the writing system, which is unambiguous by itself: a consonant is a bare
# letter + virama (क्), or a bare letter alone when the vowel `a` follows (क = k a), or a bare
# letter + a vowel sign (कि = k i); a vowel stands as an independent letter when no consonant
# precedes it; the candrabindu follows the vowel it nasalises and the digit ३ (pluta) follows both.
# Anusvara, visarga and avagraha are not among the 42 sounds and are not part of this codec.

SEPARATOR = "\u00b7"
NASAL_DEV, NASAL_IAST = _NASAL[1], _NASAL[0]
_DEV_SIGN = {"i": "ि", "u": "ु", "ṛ": "ृ", "ḷ": "ॢ", "e": "े", "o": "ो", "ai": "ै", "au": "ौ",
             "ā": "ा", "ī": "ी", "ū": "ू", "ṝ": "ॄ"}


def _is_vowel(code: int) -> bool:
    return g.unpack(code).aperture >= g.VOWEL


def _tokens(column: int):
    return sorted(_FROM[column], key=len, reverse=True)


_TOKENS = {0: _tokens(0), 2: _tokens(2)}   # IAST and Cyrillic: longest first
_DEV_CONS = {row[1][:-1]: g.SOUNDS[key] for key, row in _ROWS.items() if row[1].endswith(_DEV_VIRAMA)}
_DEV_VOWEL = {text: c for text, c in _FROM[1].items() if _is_vowel(c) and len(text) == 1}
_DEV_SIGN_TO_CODE = {}
for _iast, _sign in _DEV_SIGN.items():
    _DEV_SIGN_TO_CODE[_sign] = _FROM[0][_N("NFC", _iast)]


def _decode_latin_like(text: str, column: int) -> tuple:
    text = _N("NFC", text)
    out, i, table, tokens = [], 0, _FROM[column], _TOKENS[column]
    while i < len(text):
        if text[i] == SEPARATOR:
            i += 1
            continue
        for tok in tokens:
            if text.startswith(tok, i):
                out.append(table[tok])
                i += len(tok)
                break
        else:
            raise g.GraphError(f"{text[i:i + 3]!r} at {i} is not a {_SCRIPTS[column]} sound")
    return tuple(out)


def _encode_latin_like(seq, column: int) -> str:
    spelled = [_spell(c, column) for c in seq]
    out = []
    for i, tok in enumerate(spelled):
        if i:
            # a dot only when the plain concatenation of the two would not read back as the two
            try:
                joined = _decode_latin_like(spelled[i - 1] + tok, column)
            except g.GraphError:                 # the greedy reading eats part of the next token (аі + ̄)
                joined = None
            if joined != (seq[i - 1], seq[i]):
                out.append(SEPARATOR)
        out.append(tok)
    return "".join(out)


def _encode_devanagari(seq) -> str:
    out, i = [], 0
    while i < len(seq):
        c = seq[i]
        if _is_vowel(c):
            out.append(_spell(c, 1))                # independent letter (+ candrabindu)
            i += 1
            continue
        if g.unpack(c).nasal and g.unpack(c).aperture == g.SEMIVOWEL:   # y~ v~ l~: bare + virama + candrabindu
            out.append(to_devanagari(c))
            i += 1
            continue
        bare = to_devanagari(c)[:-1]
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        if nxt is not None and _is_vowel(nxt):
            v = g.unpack(nxt)
            key = g.LABELS_BY_CODE[_vowel_base(v)]
            iast = _ROWS[key][0]
            if v.length >= g.LONG and key in ("a", "i", "u", "ṛ"):
                iast = _LONG[0][iast]                    # long or pluta: the long sign
            sign = "" if iast == "a" else _DEV_SIGN[iast]
            out.append(bare + sign + (NASAL_DEV if v.nasal else "") + (_PLUTA[1] if v.length == g.PLUTA else ""))
            i += 2
        else:
            out.append(bare + _DEV_VIRAMA)
            i += 1
    return "".join(out)


def _decode_devanagari(text: str) -> tuple:
    text = _N("NFC", text)
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        i += 1
        if ch in _DEV_CONS:
            out.append(_DEV_CONS[ch])
            if i < len(text) and text[i] == _DEV_VIRAMA:
                i += 1
                if i < len(text) and text[i] == NASAL_DEV:      # y~ v~ l~
                    nasal_code = _FROM[1].get(_N("NFC", ch + _DEV_VIRAMA + NASAL_DEV))
                    if nasal_code is None:
                        raise g.GraphError(f"{ch!r}+virama+candrabindu is not a sound of this graph")
                    out[-1] = nasal_code
                    i += 1
                continue
            if i < len(text) and text[i] in _DEV_SIGN_TO_CODE:
                vowel = _DEV_SIGN_TO_CODE[text[i]]
                i += 1
            else:
                vowel = g.SOUNDS["a"]                   # the inherent a
            if i < len(text) and text[i] == NASAL_DEV:
                vowel = g.e_nasal(vowel)
                i += 1
            if i < len(text) and text[i] == _PLUTA[1]:
                vowel = _pluta(vowel)
                i += 1
            out.append(vowel)
        elif ch in _DEV_VOWEL:
            vowel = _DEV_VOWEL[ch]
            if i < len(text) and text[i] == NASAL_DEV:
                vowel = g.e_nasal(vowel)
                i += 1
            if i < len(text) and text[i] == _PLUTA[1]:
                vowel = _pluta(vowel)
                i += 1
            out.append(vowel)
        else:
            raise g.GraphError(f"{ch!r} at {i - 1} is not a Devanagari sound")
    return tuple(out)


def encode_text(seq, script: str) -> str:
    """Spell a sequence of sound codes in `script` ("iast", "devanagari", "cyrillic")."""
    seq = tuple(seq)
    if script == "devanagari":
        return _encode_devanagari(seq)
    if script in ("iast", "cyrillic"):
        return _encode_latin_like(seq, _SCRIPTS.index(script) if script == "iast" else 2)
    raise g.GraphError(f"unknown script {script!r}")


def decode_text(text: str, script: str, *, strict: bool = True) -> tuple:
    """Read a string back to the sequence of sound codes (inverse of `encode_text`).

    `strict` (default): the text must be exactly what `encode_text` writes for the sequence it reads
    (no extra dots, no `क्अ` for `क`), so text <-> sequence is a bijection on the accepted strings.
    `strict=False` accepts those other spellings of the same sequence.
    """
    if script == "devanagari":
        seq = _decode_devanagari(text)
    elif script in ("iast", "cyrillic"):
        seq = _decode_latin_like(text, 0 if script == "iast" else 2)
    else:
        raise g.GraphError(f"unknown script {script!r}")
    if strict and encode_text(seq, script) != _N("NFC", text):
        raise g.GraphError(f"{text!r} is not the canonical {script} spelling of its sounds")
    return seq


def transcode(text: str, src: str, dst: str) -> str:
    """Rewrite a text from one script to another, through the codes."""
    return encode_text(decode_text(text, src), dst)


__all__ = ["SEPARATOR", "code_from_cyrillic", "code_from_devanagari", "code_from_iast", "decode_text", "encode_text", "to_cyrillic", "to_devanagari", "to_iast", "transcode"]
