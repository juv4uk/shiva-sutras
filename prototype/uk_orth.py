#!/usr/bin/env python3
"""Ukrainian orthography <-> a sequence of sound tokens (research, hypothesis).

The 7-bit cells hold SOUNDS; a layout is how a language writes them. The Ukrainian layout used to render
iotated vowels as `йа йу йе йі` and `щ` as `шч`; here the layout writes Ukrainian words. The rules are the
orthographic ones, stated as code:

    я ю є   after a consonant   = the consonant + `ь` (softness) + а у е            дя  -> д ь а
    я ю є   at a word start or after a vowel = й + а у е                            яма -> й а м а
    ї       = й + і                                                                 їжа -> й і ж а
    щ       = ш + ч
    ь       = softness (a token of its own); `ьо` = ь + о, `йо` = й + о             льон, йод
    '       an apostrophe before я ю є ї after a consonant = the consonant + й + vowel   об'єкт -> о б й е к т
    дз дж ц ч  one token each (maximal match)

Rendering inverts that. Case is not part of a sound: output is lowercase (a limitation, stated in the doc).
A token is a Ukrainian letter or digraph; the shared ones (к ґ т д н п б м і у й с р л в ш) name the same sound as the
Sanskrit letter of the same cell, see `upc7_lang`.
"""

from __future__ import annotations

from typing import List

CONSONANTS = ("дз", "дж", "к", "ґ", "т", "д", "н", "п", "б", "м", "х", "ш", "ж", "с", "з", "р", "л", "ф", "в", "г", "ц", "ч")
VOWELS = ("а", "е", "о", "и", "і", "у")
STRESS = "\u0301"                      # a combining acute after a vowel: the stress mark (a token of its own)
OTHER = ("й", "ь", STRESS)
TOKENS = frozenset(CONSONANTS) | frozenset(VOWELS) | frozenset(OTHER)
CONSONANT_SET = frozenset(CONSONANTS)
VOWEL_SET = frozenset(VOWELS)
APOSTROPHES = "'’ʼ"        # the backtick is a sign cell of the 7-bit table, not an apostrophe
IOTATED = {"я": "а", "ю": "у", "є": "е"}
GLYPH_OF = {"а": "я", "у": "ю", "е": "є"}


class UkOrthError(ValueError):
    pass


def to_tokens(word: str) -> List[str]:
    """Sound tokens of a lowercase Ukrainian word (letters and apostrophes only)."""
    text = word.lower()
    out: List[str] = []
    i = 0
    apos = False
    while i < len(text):
        ch = text[i]
        if ch in APOSTROPHES:
            if i == 0 or i + 1 >= len(text) or text[i + 1] not in "яюєї" or not out or out[-1] not in CONSONANT_SET:
                raise UkOrthError(f"an apostrophe is only written before я ю є ї after a consonant: {word!r} at {i}")
            apos = True
            i += 1
            continue
        pair = text[i:i + 2]
        if pair in ("дз", "дж"):
            out.append(pair)
            i += 2
            apos = False
            continue
        if ch in IOTATED or ch == "ї":
            vowel = "і" if ch == "ї" else IOTATED[ch]
            prev = out[-1] if out else None
            if apos or ch == "ї" or prev is None or prev in VOWEL_SET or prev in ("й", "ь"):
                out.extend(["й", vowel])
            elif prev in CONSONANT_SET:
                out.extend(["ь", vowel])
            else:
                out.extend(["й", vowel])
            apos = False
            i += 1
            continue
        if ch == STRESS:
            if not out or out[-1] not in VOWEL_SET:
                raise UkOrthError(f"a stress mark follows a vowel: {word!r} at {i}")
            out.append(STRESS)
        elif ch == "щ":
            out.extend(["ш", "ч"])
        elif ch in TOKENS:
            out.append(ch)
        else:
            raise UkOrthError(f"{ch!r} in {word!r} is not a Ukrainian letter")
        apos = False
        i += 1
    return out


def to_orth(tokens: List[str]) -> str:
    """Ukrainian spelling of a token sequence."""
    return to_orth_mapped(tokens)[0]


def to_orth_mapped(tokens: List[str]) -> "tuple[str, List[int]]":
    """(spelling, origin): `origin[i]` is the index in the spelling of the character that token `i` writes (the glyph, for a
    token inside я ю є ї щ), so a capital can be put on the right letter."""
    out: List[str] = []
    origin: List[int] = [0] * len(tokens)
    pos = 0                                              # characters written so far

    def emit(text: str) -> None:
        nonlocal pos
        out.append(text)
        pos += len(text)

    i, n = 0, len(tokens)
    while i < n:
        t = tokens[i]
        nxt = tokens[i + 1] if i + 1 < n else None
        nxt2 = tokens[i + 2] if i + 2 < n else None
        if t == "ш" and nxt == "ч":
            origin[i] = origin[i + 1] = pos
            emit("щ")
            i += 2
        elif t in CONSONANT_SET and nxt == "ь" and nxt2 in GLYPH_OF:
            origin[i] = pos
            origin[i + 1] = origin[i + 2] = pos + len(t)
            emit(t + GLYPH_OF[nxt2])
            i += 3
        elif t in CONSONANT_SET and nxt == "ь":
            origin[i] = pos
            origin[i + 1] = pos + len(t)
            emit(t + "ь")                                # `ь` before о, й or a consonant, or word-final: written as the letter
            i += 2
        elif t == "й" and nxt in GLYPH_OF:
            prev = tokens[i - 1] if i else None
            apos = "'" if prev in CONSONANT_SET else ""
            origin[i] = origin[i + 1] = pos + len(apos)
            emit(apos + GLYPH_OF[nxt])
            i += 2
        elif t == "й" and nxt == "і":
            prev = tokens[i - 1] if i else None
            apos = "'" if prev in CONSONANT_SET else ""
            origin[i] = origin[i + 1] = pos + len(apos)
            emit(apos + "ї")
            i += 2
        else:
            origin[i] = pos
            emit(t)
            i += 1
    return "".join(out), origin
