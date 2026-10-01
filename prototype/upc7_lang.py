#!/usr/bin/env python3
"""A language-faithful text layer over the saṅkṣepa7 cells (research, hypothesis; the pinned UPC-7 table is NOT changed).

A cell is a SOUND. A layout is how one language writes it:

    sa-iast   IAST            (Sanskrit, the scientific spelling)
    sa-deva   Devanagari      (Sanskrit, native: consonant + virama, vowel signs, inherent a)
    sa-cyr    Cyrillic        (Sanskrit in Ukrainian letters, the scheme of «Бгаґавад-ґіта як вона є»)
    uk        Ukrainian       (Ukrainian orthography: я ю є ї щ, ь, the apostrophe; `uk_orth`)

Switch to the Ukrainian layout and you write Ukrainian words; switch to a Sanskrit one and you write Sanskrit words. The code
stream is the same cells. A sound that the other language does not have has no spelling there and is REFUSED, never
approximated (`UnrenderableCode`).

Which Ukrainian letter names the same sound as which Sanskrit letter is the project's existing decision (the pinned table):
к ґ т д н п б м і у й с р л в ш share the cell of k g t d n p b m i u y s r l v ś; ж з ф х г ц ч дз дж ь а е о и have cells of their own.
Sanskrit sounds come from the UPC-14 graph (`upc7_derive`); the Ukrainian-only cells keep their pinned numbers.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import uk_orth
import upc14v2 as g
import upc14v2_script as sc
import upc14v2_sandhi as sd
import upc7_derive as derive
import upc7_geometry as geo
import upc7_layouts as pinned

LAYOUTS = ("sa-iast", "sa-deva", "sa-cyr", "uk")
SCRIPT_OF = {"sa-iast": "iast", "sa-deva": "devanagari", "sa-cyr": "cyrillic"}


class LangError(ValueError):
    pass


class UnknownSpelling(LangError):
    pass


class UnrenderableCode(LangError):
    pass


# ---- the sounds Sanskrit names ---------------------------------------------------------------------------------------
def _sanskrit_vertices() -> Dict[str, int]:
    names = list(g.SOUNDS) + ["ā", "ī", "ū", "ṝ"] + [n + "̃" for n in ("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au")]
    out: Dict[str, int] = {}
    for name in names:
        try:
            out[name] = sd.code_of(name)
        except g.GraphError:
            continue
    return out


SANSKRIT_VERTEX = _sanskrit_vertices()
SANSKRIT_CELL = {name: derive.derive(vertex) for name, vertex in SANSKRIT_VERTEX.items()}
VERTEX_OF_CELL = {cell: SANSKRIT_VERTEX[name] for name, cell in SANSKRIT_CELL.items()}
if len(VERTEX_OF_CELL) != len(SANSKRIT_CELL):
    raise LangError("two Sanskrit sounds derive to one cell")

# ---- the sounds Ukrainian names --------------------------------------------------------------------------------------
SHARED = {"к": "k", "ґ": "g", "т": "t", "д": "d", "н": "n", "п": "p", "б": "b", "м": "m", "і": "i", "у": "u",
          "й": "y", "с": "s", "р": "r", "л": "l", "в": "v", "ш": "ś"}


def _ukrainian_only() -> Dict[str, int]:
    cells: Dict[str, int] = {}
    for legacy_code, forms in pinned.CURRENT_UPC8_NONVARGA.items():
        for form in forms:
            if form in ("х", "ж", "з", "ф", "г"):
                cells[form] = geo.compress_upc8_nonvarga(legacy_code)
    for letter, index in pinned._UK_EXT_VOWELS.items():
        cells[letter] = geo.uk_ext_vowel_code(index)
    for letter, index in pinned._UK_EXT_AFFRICATES.items():
        cells[letter] = geo.uk_affricate_code(index)
    cells["ь"] = geo.softness_code()
    return cells


UK_ONLY_CELL = _ukrainian_only()
UK_CELL = {**{tok: SANSKRIT_CELL[sk] for tok, sk in SHARED.items()}, **UK_ONLY_CELL}
TOKEN_OF_CELL = {cell: tok for tok, cell in UK_CELL.items()}
if len(TOKEN_OF_CELL) != len(UK_CELL):
    raise LangError("two Ukrainian sounds share one cell")

# ---- signs (the same in every layout) --------------------------------------------------------------------------------
SIGN_CELL = {glyph: geo.sign_code(name) for name, glyph in geo.ASCII_SURFACE_GLYPHS.items()}
SIGN_OF_CELL = {cell: glyph for glyph, cell in SIGN_CELL.items()}

_all = list(SANSKRIT_CELL.values()) + list(UK_ONLY_CELL.values()) + list(SIGN_CELL.values())
if len(set(_all)) != len(_all):
    raise LangError("a cell is claimed twice")


def _is_sign(ch: str) -> bool:
    return ch in SIGN_CELL


def _split(text: str, letter_ok) -> List[Tuple[str, str]]:
    """[(kind, chunk)]: kind 'sign' for one sign character, 'word' for a run of letters."""
    out: List[Tuple[str, str]] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch in SIGN_CELL and not letter_ok(text, i):
            out.append(("sign", ch))
            i += 1
            continue
        j = i
        while j < len(text) and (text[j] not in SIGN_CELL or letter_ok(text, j)):
            j += 1
        out.append(("word", text[i:j]))
        i = j
    return out


def _apostrophe_in_word(text: str, i: int) -> bool:
    return text[i] == "'" and 0 < i < len(text) - 1 and text[i - 1].isalpha() and text[i + 1].isalpha()


class LangText:
    """encode / render / switch over the language-faithful layouts."""

    def encode(self, text: str, layout: str) -> Tuple[int, ...]:
        if layout not in LAYOUTS:
            raise LangError(f"unknown layout {layout!r}")
        cells: List[int] = []
        ok = _apostrophe_in_word if layout == "uk" else (lambda t, i: False)
        for kind, chunk in _split(text, ok):
            if kind == "sign":
                cells.append(SIGN_CELL[chunk])
            elif layout == "uk":
                try:
                    cells.extend(UK_CELL[tok] for tok in uk_orth.to_tokens(chunk))
                except uk_orth.UkOrthError as exc:
                    raise UnknownSpelling(str(exc)) from None
            else:
                try:
                    vertices = sc.decode_text(chunk, SCRIPT_OF[layout], strict=False)
                    cells.extend(derive.derive(v) for v in vertices)
                except (g.GraphError, derive.DeriveError) as exc:
                    raise UnknownSpelling(f"{layout}: {chunk!r}: {exc}") from None
        return tuple(cells)

    def render(self, cells: Iterable[int], layout: str) -> str:
        if layout not in LAYOUTS:
            raise LangError(f"unknown layout {layout!r}")
        out: List[str] = []
        run: List[int] = []

        def flush() -> None:
            if not run:
                return
            if layout == "uk":
                tokens = []
                for c in run:
                    if c not in TOKEN_OF_CELL:
                        raise UnrenderableCode(f"uk: {geo.code_bits(c)} is not a Ukrainian sound")
                    tokens.append(TOKEN_OF_CELL[c])
                out.append(uk_orth.to_orth(tokens))
            else:
                vertices = []
                for c in run:
                    if c not in VERTEX_OF_CELL:
                        raise UnrenderableCode(f"{layout}: {geo.code_bits(c)} is not a Sanskrit sound")
                    vertices.append(VERTEX_OF_CELL[c])
                out.append(sc.encode_text(vertices, SCRIPT_OF[layout]))
            run.clear()

        for c in cells:
            geo.checked_code(c)
            if c in SIGN_OF_CELL:
                flush()
                out.append(SIGN_OF_CELL[c])
            else:
                run.append(c)
        flush()
        return "".join(out)

    def switch(self, text: str, from_layout: str, to_layout: str) -> str:
        """Change only the human projection; the cell stream is untouched."""
        return self.render(self.encode(text, from_layout), to_layout)

    @staticmethod
    def shared_sounds() -> List[Tuple[str, str]]:
        """(Ukrainian letter, Sanskrit IAST name) pairs that are one sound."""
        return sorted(SHARED.items())


__all__ = ["LAYOUTS", "LangError", "LangText", "SANSKRIT_CELL", "SHARED", "UK_CELL", "UK_ONLY_CELL", "SIGN_CELL",
           "UnknownSpelling", "UnrenderableCode"]
