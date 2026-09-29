#!/usr/bin/env python3
"""
UPC-7: 7-bit text-code prototype derived from UPC-8
====================================================

Status: experimental engineering prototype for shiva-sutras#27.

UPC-7 does not introduce a second phoneme authority. It is an
identity-preserving projection of the currently assigned lower plane of
prototype/upc8.py:

    UPC7(code) = UPC8(code), for 0x00 <= code <= 0x7F

Human layouts are projections over the same code stream. A layout spelling is
not code identity. Host Python str/Unicode exists only at this prototype's
input/output boundary.

This module deliberately fails closed:
- codes above 0x7F are not UPC-7;
- unknown spellings are rejected;
- switching to a layout that lacks a spelling for a code is rejected;
- "near-equivalent" phonemes are not silently merged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence, Tuple

from upc8 import UPC8


UPC7_MIN = 0x00
UPC7_MAX = 0x7F


class UPC7Error(ValueError):
    """Base error for the UPC-7 engineering prototype."""


class UnknownLayout(UPC7Error):
    pass


class UnknownSpelling(UPC7Error):
    pass


class UnrenderableCode(UPC7Error):
    pass


def _checked_code(code: int) -> int:
    if not isinstance(code, int) or isinstance(code, bool):
        raise UPC7Error(f"UPC-7 code must be int, got {type(code).__name__}")
    if not UPC7_MIN <= code <= UPC7_MAX:
        raise UPC7Error(f"UPC-7 code outside 7-bit domain: {code!r}")
    return code


@dataclass(frozen=True)
class Layout:
    """A human projection over UPC-7 identities.

    code_to_spelling can be partial. Partiality is intentional: if a code has
    no honest spelling in a layout, rendering fails instead of inventing an
    equivalence.
    """

    name: str
    code_to_spelling: Mapping[int, str]

    def __post_init__(self) -> None:
        inverse: Dict[str, int] = {}
        for code, spelling in self.code_to_spelling.items():
            _checked_code(code)
            if not spelling:
                raise UPC7Error(f"{self.name}: empty spelling for code {code}")
            previous = inverse.get(spelling)
            if previous is not None and previous != code:
                raise UPC7Error(
                    f"{self.name}: ambiguous spelling {spelling!r} for "
                    f"{previous:#04x} and {code:#04x}"
                )
            inverse[spelling] = code

    @property
    def spelling_to_code(self) -> Dict[str, int]:
        return {spelling: code for code, spelling in self.code_to_spelling.items()}


class UPC7:
    """7-bit identity space with switchable human layouts."""

    def __init__(self, donor: UPC8 | None = None):
        self.donor = donor or UPC8()
        self._prove_donor_fits()
        self.layouts: Dict[str, Layout] = self._build_layouts()

    def _prove_donor_fits(self) -> None:
        offenders = sorted(code for code in self.donor.table if code > UPC7_MAX)
        if offenders:
            rendered = ", ".join(f"0x{code:02X}" for code in offenders[:8])
            raise UPC7Error(
                "current UPC-8 assigned table exceeds UPC-7 lower plane: "
                + rendered
            )

    def _build_layouts(self) -> Dict[str, Layout]:
        sanskrit: Dict[int, str] = {}
        ukrainian: Dict[int, str] = {}

        for code, entry in self.donor.table.items():
            _checked_code(code)
            layer = entry.get("layer")

            if layer == "canonical" and "slp1" in entry:
                sanskrit[code] = entry["slp1"]
            elif layer == "sanskrit_extended" and "iast" in entry:
                # Keep the UPC-8 prototype's ASCII engineering spelling here.
                # A later UPC-7 layout may choose another human projection
                # without changing the code.
                sanskrit[code] = entry["iast"]

            languages = entry.get("languages", {})
            uk = languages.get("ukrainian")
            if uk and "letter" in uk:
                ukrainian[code] = uk["letter"]
            elif layer == "ukrainian_new" and "letter" in entry:
                ukrainian[code] = entry["letter"]

        return {
            "sa-slp1": Layout("sa-slp1", sanskrit),
            "uk": Layout("uk", ukrainian),
        }

    def layout(self, name: str) -> Layout:
        try:
            return self.layouts[name]
        except KeyError as exc:
            raise UnknownLayout(name) from exc

    def assigned_codes(self) -> Tuple[int, ...]:
        return tuple(sorted(self.donor.table))

    def encode(self, text: str, layout: str) -> Tuple[int, ...]:
        """Encode host/UI text into layout-independent UPC-7 identities.

        Greedy longest-match preserves the UPC-8 Ukrainian multi-grapheme
        behavior while also working for single-character SLP1.
        """
        if layout == "bits":
            if not text.strip():
                return ()
            out = []
            for token in text.split():
                if len(token) != 7 or any(ch not in "01" for ch in token):
                    raise UnknownSpelling(
                        f"bits layout expects whitespace-separated 7-bit cells, got {token!r}"
                    )
                out.append(_checked_code(int(token, 2)))
            return tuple(out)

        mapping = self.layout(layout).spelling_to_code
        spellings = sorted(mapping, key=len, reverse=True)

        out = []
        index = 0
        while index < len(text):
            for spelling in spellings:
                if text.startswith(spelling, index):
                    out.append(mapping[spelling])
                    index += len(spelling)
                    break
            else:
                raise UnknownSpelling(
                    f"{layout}: no UPC-7 spelling at host-text offset {index}: "
                    f"{text[index:index + 8]!r}"
                )
        return tuple(out)

    def render(self, codes: Iterable[int], layout: str) -> str:
        checked = tuple(_checked_code(code) for code in codes)
        if layout == "bits":
            return " ".join(f"{code:07b}" for code in checked)

        mapping = self.layout(layout).code_to_spelling
        rendered = []
        for code in checked:
            try:
                rendered.append(mapping[code])
            except KeyError as exc:
                raise UnrenderableCode(
                    f"{layout}: code {code:07b} (0x{code:02X}) has no honest layout spelling"
                ) from exc
        return "".join(rendered)

    def switch_layout(self, text: str, from_layout: str, to_layout: str) -> str:
        """Switch only the human projection; UPC-7 identities stay unchanged."""
        return self.render(self.encode(text, from_layout), to_layout)

    def preserves_codes_when_switching(
        self, text: str, from_layout: str, to_layout: str
    ) -> bool:
        source_codes = self.encode(text, from_layout)
        rendered = self.render(source_codes, to_layout)
        return self.encode(rendered, to_layout) == source_codes


__all__ = [
    "Layout",
    "UPC7",
    "UPC7Error",
    "UPC7_MAX",
    "UPC7_MIN",
    "UnknownLayout",
    "UnknownSpelling",
    "UnrenderableCode",
]
