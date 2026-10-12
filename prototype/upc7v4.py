#!/usr/bin/env python3
"""UPC-7 v4: a versioned W7 stream projection of UPC-14 v3 sound identities.

The identity of each phone is the UPC-14 v3 vertex, never an IPA spelling.
The *transport cells* are seven bits. 42 inherited Śiva-sūtra sounds have
one W7 cell derived from the UPC-14 v2 graph. The 37 additional English
reference-accent phonemes use ESC + rank (two W7 cells = exactly 14 bits).
Ranks are numeric-order indices into the pinned UPC-14 v3 feature vertices.

This is NOT a rewrite of pinned UPC-7 v2, candidate UPC-7 v3, SENS D7,
or any language's spelling system. The caller MUST declare v4; raw v4 W7
is not safely interchangeable with older W7 versions. No inline version
header, no invisible byte and no extra binary identity are introduced.
"""

from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path
from typing import Iterable
from dataclasses import dataclass
import upc14v2 as v2
import upc14v3 as v3
from upc7_derive import derive

VERSION = "UPC-7 v4"
PROFILE = "english-reference-44"
WIDTH = 7
ESCAPE = 0b0101111  # free in v3, occupied (l) in pinned v2; version REQUIRED
V3_TABLE_SHA1 = "1270a85616957646f18971133fe4f20c8de0fcde"
UPC14V3_SHA1 = "d40d1eaeecc624f9e7e4b5052fb32c814bdd8211"
ROOT = Path(__file__).resolve().parent


class UPC7V4Error(ValueError):
    """Malformed, version-confused, or non-admitted sound-code stream."""


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def authority_check() -> None:
    """Fail closed if either snapshot changes without an explicit v4 revision."""
    for p, want in ((ROOT / "upc7-table-v3.tsv", V3_TABLE_SHA1),
                    (ROOT / "upc14v3.py", UPC14V3_SHA1)):
        observed = git_blob_sha(p)
        if observed != want:
            raise UPC7V4Error(f"authority drift: {p.name}: {observed}, expected {want}")


def candidate_v3_cells() -> dict[int, dict[str, str]]:
    """Separate 7-bit language-aware v3 candidate table; never rewrite it."""
    authority_check()
    source = (ROOT / "upc7-table-v3.tsv").read_text(encoding="utf-8")
    rows = list(csv.DictReader(io.StringIO(source), delimiter="\t"))
    table: dict[int, dict[str, str]] = {}
    for row in rows:
        bits = row["bits"]
        if len(bits) != 7 or set(bits) - {"0", "1"}:
            raise UPC7V4Error("non-seven-bit candidate coordinate")
        cell = int(bits, 2)
        if cell in table:
            raise UPC7V4Error(f"duplicate v3 cell {bits}")
        table[cell] = row
    if len(table) != 124:
        raise UPC7V4Error(f"unexpected v3 occupancy {len(table)}, expected 124")
    if ESCAPE in table:
        raise UPC7V4Error("v4 ESCAPE is occupied in v3; select a new version")
    return table


def _build_indexes() -> tuple[dict[int, int], dict[int, int], tuple[int, ...]]:
    table = candidate_v3_cells()
    direct_14_to_7: dict[int, int] = {}
    direct_7_to_14: dict[int, int] = {}
    for sound, code14 in v2.SOUNDS.items():
        cell7 = derive(code14)
        row = table.get(cell7)
        if row is None or row["sound"] != sound:
            raise UPC7V4Error(f"v2→v3 ancestry mismatch: {sound} at {cell7:07b}")
        if cell7 in direct_7_to_14:
            raise UPC7V4Error(f"two v2 sounds share {cell7:07b}")
        direct_14_to_7[code14] = cell7
        direct_7_to_14[cell7] = code14
    if len(direct_14_to_7) != 42 or len(direct_7_to_14) != 42:
        raise UPC7V4Error("historical 42 sound identities not injective")

    # The ENGLISH phonemic inventory has 44 values; exactly seven MUST
    # reuse historical v2 codes, 37 are admitted NEW UPC-14 v3 vertices.
    old14 = set(direct_14_to_7)
    reused = {row.code for row in v3.ENGLISH if row.code in old14}
    extra = tuple(sorted(row.code for row in v3.ENGLISH if row.code not in old14))
    if len(reused) != 7 or len(extra) != 37 or len(set(extra)) != 37:
        raise UPC7V4Error("donor reference inventory changed; version bump needed")
    if len(extra) >= 128:
        raise UPC7V4Error("one W7 ordinal can encode at most 128 extensions")
    if any(c >> 12 != 0b11 for c in extra):
        raise UPC7V4Error("unexpected UPC14 v3 extension lane")
    for row in v3.ENGLISH:
        if row.code in reused and direct_14_to_7[row.code] != v3.project_to_legacy_upc7(row.ipa):
            raise UPC7V4Error("UPC14-v3→7 inherited sound law drift")
    return direct_14_to_7, direct_7_to_14, extra


DIRECT_14_TO_7, DIRECT_7_TO_14, EXT_CODES14 = _build_indexes()
EXT_RANK = {code: ordinal for ordinal, code in enumerate(EXT_CODES14)}


def encode_sound_codes(codes14: Iterable[int]) -> tuple[int, ...]:
    """Encode a sequence of exact W14 sound vertices into canonical W7 cells."""
    out: list[int] = []
    for code in codes14:
        if type(code) is not int or not 0 <= code < (1 << 14):
            raise UPC7V4Error(f"not a 14-bit sound identity: {code!r}")
        if code in DIRECT_14_TO_7:
            out.append(DIRECT_14_TO_7[code])
        elif code in EXT_RANK:
            out.extend((ESCAPE, EXT_RANK[code]))
        else:
            raise UPC7V4Error(f"sound not admitted in {VERSION}: {code:014b}")
    return tuple(out)


def decode_sound_codes(cells7: Iterable[int]) -> tuple[int, ...]:
    """Strict prefix parser. An orphan escape, unknown index or sign is invalid."""
    cells = tuple(cells7)
    out: list[int] = []
    i = 0
    while i < len(cells):
        cell = cells[i]
        if type(cell) is not int or not 0 <= cell < 128:
            raise UPC7V4Error(f"not a seven-bit cell: {cell!r}")
        if cell == ESCAPE:
            if i + 1 >= len(cells):
                raise UPC7V4Error("truncated two-cell UPC7 v4 extension")
            rank = cells[i + 1]
            if type(rank) is not int or not 0 <= rank < len(EXT_CODES14):
                raise UPC7V4Error(f"invalid v4 extension rank {rank!r}")
            out.append(EXT_CODES14[rank])
            i += 2
        elif cell in DIRECT_7_TO_14:
            out.append(DIRECT_7_TO_14[cell])
            i += 1
        else:
            raise UPC7V4Error(f"unadmitted phoneme cell {cell:07b}")
    return tuple(out)


def encode_english_tokens(ipa_tokens: Iterable[str]) -> tuple[int, ...]:
    """An explicit list of IPA phoneme tokens, NEVER an orthographic word."""
    return encode_sound_codes(v3.encode_english_phoneme(tok) for tok in ipa_tokens)


def decode_english_tokens(cells7: Iterable[int]) -> tuple[str, ...]:
    return tuple(v3.decode_english_phoneme(code) for code in decode_sound_codes(cells7))


def pack_w7(cells7: Iterable[int]) -> tuple[bytes, int]:
    """Minimal byte packing of the W7 stream; return explicit cell count.

    The cell count is out-of-band frame metadata. No byte is wasted per
    symbol, and unused padding bits in the final byte MUST equal zero.
    """
    value = 0
    cells = tuple(cells7)
    for c in cells:
        if type(c) is not int or not 0 <= c < 128:
            raise UPC7V4Error(f"not a W7 cell: {c!r}")
        value = (value << 7) | c
    nbits = len(cells) * 7
    pad = (-nbits) % 8
    padded = value << pad
    return padded.to_bytes((nbits + 7) // 8, "big"), len(cells)


def unpack_w7(data: bytes, count: int) -> tuple[int, ...]:
    if not isinstance(data, bytes) or type(count) is not int or count < 0:
        raise UPC7V4Error("expected byte transport and nonnegative W7 count")
    nbits = count * 7
    if len(data) != (nbits + 7) // 8:
        raise UPC7V4Error("incorrect packed length")
    pad = (-nbits) % 8
    value = int.from_bytes(data, "big")
    if pad and value & ((1 << pad) - 1):
        raise UPC7V4Error("nonzero high-level padding, not canonical")
    value >>= pad
    return tuple((value >> (7 * (count - i - 1))) & 0x7F for i in range(count))


@dataclass(frozen=True)
class UPC7V4Frame:
    """Explicit outer transport metadata; NOT new semantic W7 codes."""
    version: str
    profile: str
    cell_count: int
    payload: bytes


def encode_english_frame(ipa_tokens: Iterable[str]) -> UPC7V4Frame:
    packed, count = pack_w7(encode_english_tokens(ipa_tokens))
    return UPC7V4Frame(VERSION, PROFILE, count, packed)


def decode_english_frame(frame: UPC7V4Frame) -> tuple[str, ...]:
    if not isinstance(frame, UPC7V4Frame):
        raise UPC7V4Error("explicit v4 frame metadata required")
    if frame.version != VERSION or frame.profile != PROFILE:
        raise UPC7V4Error("version/profile mismatch; never guess a codec")
    return decode_english_tokens(unpack_w7(frame.payload, frame.cell_count))


def bits(cells7: Iterable[int]) -> str:
    """Diagnostic seven-bit tokens, never a byte count."""
    return " ".join(f"{v:07b}" for v in cells7)


if __name__ == "__main__":
    print(f"{VERSION}: {len(DIRECT_14_TO_7)} old sounds; "
          f"{len(EXT_CODES14)} extra English sounds; ESC={ESCAPE:07b}")
    for phoneme in v3.ENGLISH:
        encoded = encode_english_tokens([phoneme.ipa])
        print(f"{phoneme.ipa:6s} {bits(encoded):18s} 14:{phoneme.code:014b}")
