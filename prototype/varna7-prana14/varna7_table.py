#!/usr/bin/env python3
"""
VARṆA-7 machine table (my design)
=================================

Prints the complete 128-cell VARṆA-7 table as TSV. The table is *generated*,
never edited by hand, so a consumer can pin it by SHA-256 and detect drift
instead of copying it.

    python3 varna7_table.py                 print the table
    python3 varna7_table.py --write         rewrite varna7-table.tsv
    python3 varna7_table.py --check         exit 1 if varna7-table.tsv is stale
    python3 varna7_table.py --sha256        print the SHA-256 of the current table

Columns: bits, hex, region, payload, status, name, sa-slp1.
Spellings are projections; a blank cell means the cell has no SLP1 spelling.
A reserved cell has no spelling and a canonical ``reserved.<region>.<payload>``
name.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Dict, List

import varna7 as V

TABLE_PATH = Path(__file__).with_name("varna7-table.tsv")
COLUMNS = ("bits", "hex", "region", "payload", "status", "name", "sa-slp1")

REGION_SLUG = {
    V.SPARSA: "sparsa",
    V.ANTAS: "antas",
    V.SVARA: "svara",
    V.SAMJNA: "samjna",
}

# spelling -> code, inverted to code -> spelling (the table's sa-slp1 column)
CODE_TO_SLP1: Dict[int, str] = {c: s for s, c in V.SOUND_SLP1.items()}


def cell_name(code: int) -> str:
    region = V.region_of(code)
    payload = V.payload_of(code)
    if region == V.SPARSA:
        if payload < 25:
            place, member = divmod(payload, 5)
            return f"sparsa.{V.SPARSA_PLACES[place]}.{V.SPARSA_MEMBERS[member]}"
    elif region == V.ANTAS:
        if code in CODE_TO_SLP1:
            place, kind = V.decode_antas(code)
            return f"antas.{V.ANTAS_PLACES[place]}.{V.ANTAS_KINDS[kind]}"
    elif region == V.SVARA:
        if payload >> 2 < 7:
            row, nasal, length = V.decode_svara(code)
            return (f"svara.{V.SVARA_ROWS[row]}.{'nasal' if nasal else 'oral'}."
                    f"{'long' if length else 'short'}")
    elif region == V.SAMJNA:
        return f"samjna.{V.SAMJNA_NAMES[payload]}"
    return f"reserved.{REGION_SLUG[region]}.{payload:05b}"


def is_assigned(code: int) -> bool:
    region = V.region_of(code)
    if region == V.SPARSA:
        return V.payload_of(code) < 25
    if region == V.ANTAS:
        return code in CODE_TO_SLP1
    if region == V.SVARA:
        return V.payload_of(code) >> 2 < 7
    return True  # every samjna cell is named


def render_table() -> str:
    lines: List[str] = ["\t".join(COLUMNS)]
    for code in range(128):
        lines.append("\t".join((
            V.bits(code),
            f"0x{code:02X}",
            REGION_SLUG[V.region_of(code)],
            f"{V.payload_of(code):05b}",
            "assigned" if is_assigned(code) else "reserved",
            cell_name(code),
            CODE_TO_SLP1.get(code, ""),
        )))
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
            print(f"{TABLE_PATH.name} is stale: run `python3 varna7_table.py --write`", file=sys.stderr)
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
