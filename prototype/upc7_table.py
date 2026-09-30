#!/usr/bin/env python3
"""
UPC-7 machine table (shiva-sutras#29)
=====================================

Prints the complete 128-cell table as TSV. The table is *generated*, never
edited by hand, so a consumer (for example SENS Text7) can pin it by SHA-256
and detect drift instead of copying it.

    python3 upc7_table.py                 print the table
    python3 upc7_table.py --write         rewrite upc7-table.tsv
    python3 upc7_table.py --check         exit 1 if upc7-table.tsv is stale
    python3 upc7_table.py --sha256        print the SHA-256 of the current table

Columns: bits, hex, class, payload, status, name, sa-slp1, sa-iast, sa-deva, uk.
Spellings are projections; a blank cell means the layout has no spelling.
Control characters are written as escapes (a space is ``\\x20``).
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import List

import upc7_geometry as geo
from upc7_layouts import UPC7Text

TABLE_PATH = Path(__file__).with_name("upc7-table.tsv")
COLUMNS = ("bits", "hex", "class", "payload", "status", "name", "sa-slp1", "sa-iast", "sa-deva", "uk")


def _escape(spelling: str) -> str:
    """A TSV-safe, reversible spelling. Letters stay readable (Cyrillic is
    written as itself); only backslash, space and control characters are
    escaped."""
    out: List[str] = []
    for char in spelling:
        if char == "\\":
            out.append("\\\\")
        elif char == " " or ord(char) < 0x20 or ord(char) == 0x7F:
            out.append(f"\\x{ord(char):02x}")
        else:
            out.append(char)
    return "".join(out)


def render_table() -> str:
    codec = UPC7Text()
    sanskrit = codec.layout("sa-slp1").code_to_spelling
    iast = codec.layout("sa-iast").code_to_spelling
    devanagari = codec.layout("sa-deva").code_to_spelling
    ukrainian = codec.layout("uk").code_to_spelling
    lines: List[str] = ["\t".join(COLUMNS)]
    for cell in codec.cells:
        lines.append(
            "\t".join(
                (
                    cell.bits,
                    f"0x{cell.code:02X}",
                    cell.klass,
                    f"{geo.payload_of(cell.code):05b}",
                    cell.status,
                    cell.name,
                    _escape(sanskrit.get(cell.code, "")),
                    _escape(iast.get(cell.code, "")),
                    _escape(devanagari.get(cell.code, "")),
                    _escape(ukrainian.get(cell.code, "")),
                )
            )
        )
    return "\n".join(lines) + "\n"


def table_sha256() -> str:
    return hashlib.sha256(render_table().encode("utf-8")).hexdigest()


def main(argv: List[str]) -> int:
    text = render_table()
    if not argv:
        sys.stdout.write(text)
        return 0
    if argv == ["--write"]:
        TABLE_PATH.write_text(text, encoding="utf-8")
        print(f"wrote {TABLE_PATH.name} sha256={table_sha256()}")
        return 0
    if argv == ["--check"]:
        current = TABLE_PATH.read_text(encoding="utf-8") if TABLE_PATH.exists() else ""
        if current != text:
            print(f"{TABLE_PATH.name} is stale: run `python3 upc7_table.py --write`", file=sys.stderr)
            return 1
        print(f"{TABLE_PATH.name} is current sha256={table_sha256()}")
        return 0
    if argv == ["--sha256"]:
        print(table_sha256())
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
