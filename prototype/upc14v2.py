#!/usr/bin/env python3
"""
UPC-14 v2 — a graph canon (shiva-sutras#44, experiment)
=======================================================

v1 numbered the sounds in the order of the Siva-sutras and hung modifiers on
that number. v2 changes the paradigm: a sound is not a row of a table, it is a
*vertex of a graph*, and the code is the vertex's coordinates. Everything the
grammar needs is an edge or a query on that graph.

The graph
---------
A sound is a point in a product of small graphs (its 14 bits are the fields):

    place     Boolean lattice on 5 atoms  K T M D O   (throat, palate, roof,
              teeth, lips)                              join = bitwise OR
    nasal     one atom, kept apart from place (1.1.8: nose is added to mouth)
    aperture  a PATH  0 stop - 1 semivowel - 2 sibilant - 3 vowel - 4 wide vowel
    length    a PATH  0 short - 1 long - 2 pluta
    voice     an edge  (unvoiced - voiced)
    asp       an edge  (unaspirated - aspirated)

    code (14 bits) = meta(1) | place(5) | nasal(1) | aperture(3) | length(2) | voice(1) | asp(1)

The whole inventory is DERIVED from one seed, `k`, by typed edges (see
`DERIVATION`): asp, voice, nasal, shift (walk the place spine K-T-M-D-O),
lift (raise the aperture), join (union of places). No sound is listed with its
features; each is reached by a path from the seed. What is irreducible input is
the seed, the edge types, and the order of the sutras themselves.

Grammar as graph queries (see `test_upc14v2.py`)
------------------------------------------------
    pratyahara     an interval of the sutra path
    savarna        equal place and aperture   (1.1.9; nasal is a separate atom)
    dirgha         savarna vowels merge to the long one   (6.1.101)
    guna / vrddhi  join of places, aperture lift          (6.1.87, 6.1.88)
    yan / jas      the NEAREST vertex in a target set      (1.1.50: sthane'ntaratamah)

A sound is its code, not a spelling. The names used to refer to the 42 sounds (keys of `SOUNDS`,
the tokens of `SUTRAS`) are lowercase IAST, as a convenience for reading; every written form of a
sound (the scripts) is a view in `upc14v2_script`, and SLP1 is not used anywhere.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Code layout: the fields ARE the graph coordinates
# ---------------------------------------------------------------------------

WIDTH = 14
CODE_MAX = (1 << WIDTH) - 1

META_SHIFT, PLACE_SHIFT, NASAL_SHIFT, AP_SHIFT, LEN_SHIFT, VOICE_SHIFT, ASP_SHIFT = 13, 8, 7, 4, 2, 1, 0
PLACE_MASK = 0b11111
AP_MASK = 0b111
LEN_MASK = 0b11

# place atoms = bits of the place field, in spine order
K, T, M, D, O = 0b00001, 0b00010, 0b00100, 0b01000, 0b10000
PLACE_SPINE = (K, T, M, D, O)  # throat -> palate -> roof -> teeth -> lips

STOP, SEMIVOWEL, SIBILANT, VOWEL, WIDE_VOWEL = 0, 1, 2, 3, 4
SHORT, LONG, PLUTA = 0, 1, 2


class GraphError(ValueError):
    pass


class InvalidCode(GraphError):
    """The bits are not a vertex. Fail closed; never repair."""


class Ambiguous(GraphError):
    """A nearest-vertex query has a tie; the graph does not decide."""


def make(place: int, aperture: int, *, nasal: int = 0, length: int = 0, voice: int = 0,
         asp: int = 0, meta: int = 0) -> int:
    return (meta << META_SHIFT | place << PLACE_SHIFT | nasal << NASAL_SHIFT
            | aperture << AP_SHIFT | length << LEN_SHIFT | voice << VOICE_SHIFT | asp)


@dataclass(frozen=True)
class Vertex:
    place: int
    nasal: int
    aperture: int
    length: int
    voice: int
    asp: int

    @property
    def code(self) -> int:
        return make(self.place, self.aperture, nasal=self.nasal, length=self.length,
                    voice=self.voice, asp=self.asp)


def unpack(code: int) -> Vertex:
    if not 0 <= code <= CODE_MAX:
        raise InvalidCode(f"not a 14-bit code: {code!r}")
    if code >> META_SHIFT:
        raise InvalidCode("meta cell: not a phonetic vertex")
    v = Vertex(
        place=(code >> PLACE_SHIFT) & PLACE_MASK,
        nasal=(code >> NASAL_SHIFT) & 1,
        aperture=(code >> AP_SHIFT) & AP_MASK,
        length=(code >> LEN_SHIFT) & LEN_MASK,
        voice=(code >> VOICE_SHIFT) & 1,
        asp=code & 1,
    )
    if v.place == 0:
        raise InvalidCode("no place atom: a sound needs an articulator")
    if v.aperture > WIDE_VOWEL:
        raise InvalidCode(f"aperture {v.aperture} is off the path")
    if v.length > PLUTA:
        raise InvalidCode(f"length {v.length} is off the path")
    if v.length and v.aperture < VOWEL:
        raise InvalidCode("only a vowel has length")
    return v


def bits(code: int) -> str:
    return format(code, "014b")


# ---------------------------------------------------------------------------
# Edges: each is a function on vertices. A grammar rule is a walk over these.
# ---------------------------------------------------------------------------


def e_asp(c: int) -> int:
    v = unpack(c)
    if v.aperture != STOP:
        raise InvalidCode("asp edge exists on stops only")
    return c ^ (1 << ASP_SHIFT)


def e_voice(c: int) -> int:
    unpack(c)
    return c ^ (1 << VOICE_SHIFT)


def e_nasal(c: int) -> int:
    """voiced, unaspirated, with the nose added (1.1.8)."""
    v = unpack(c)
    return Vertex(v.place, 1, v.aperture, v.length, 1, 0).code


def e_shift(c: int) -> int:
    """Move every atom one step along the place spine K-T-M-D-O."""
    v = unpack(c)
    if v.place & O:
        raise InvalidCode("shift past the end of the spine")
    return Vertex(v.place << 1, v.nasal, v.aperture, v.length, v.voice, v.asp).code


def e_lift(c: int, steps: int = 1) -> int:
    v = unpack(c)
    ap = v.aperture + steps
    if ap > WIDE_VOWEL:
        raise InvalidCode("aperture lift past the end of the path")
    return Vertex(v.place, v.nasal, ap, v.length, v.voice, v.asp).code


def e_join(c: int, atoms: int) -> int:
    v = unpack(c)
    return Vertex(v.place | atoms, v.nasal, v.aperture, v.length, v.voice, v.asp).code


def e_long(c: int) -> int:
    v = unpack(c)
    if v.aperture < VOWEL:
        raise InvalidCode("only a vowel has length")
    return Vertex(v.place, v.nasal, v.aperture, min(v.length + 1, PLUTA), v.voice, v.asp).code


def join_vertices(a: int, b: int, *, length: int, aperture: int) -> int:
    """Two vowels meet: union of places, chosen aperture and length."""
    va, vb = unpack(a), unpack(b)
    return Vertex(va.place | vb.place, va.nasal | vb.nasal, aperture, length, va.voice, 0).code


# ---------------------------------------------------------------------------
# The derivation: 42 sounds from the seed `k`. (label, parent label(s), edge)
# Names are IAST, a convenience for reading only; identity is the code.
# ---------------------------------------------------------------------------

SEED = ("k", make(K, STOP))

VARGA_FIRST = ("k", "c", "ṭ", "t", "p")   # first member of each varga, spine order
VARGA_ROWS = {
    "k": ("k", "kh", "g", "gh", "ṅ"),
    "c": ("c", "ch", "j", "jh", "ñ"),
    "ṭ": ("ṭ", "ṭh", "ḍ", "ḍh", "ṇ"),
    "t": ("t", "th", "d", "dh", "n"),
    "p": ("p", "ph", "b", "bh", "m"),
}


def _derive() -> Tuple[Dict[str, int], List[Tuple[str, str, str]]]:
    """Return ({label: code}, [(label, parent, edge)]) reached from the seed."""
    codes: Dict[str, int] = {SEED[0]: SEED[1]}
    log: List[Tuple[str, str, str]] = []

    def add(label: str, parent: str, edge: str, code: int) -> None:
        codes[label] = code
        log.append((label, parent, edge))

    # 1. a varga row from its first member, then the next varga by `shift`.
    previous = None
    for first in VARGA_FIRST:
        row = VARGA_ROWS[first]
        if previous is not None:
            add(first, previous, "shift", e_shift(codes[previous]))
        first_c = codes[first]
        add(row[1], first, "asp", e_asp(first_c))
        add(row[2], first, "voice", e_voice(first_c))
        add(row[3], row[2], "asp", e_asp(codes[row[2]]))
        add(row[4], row[2], "nasal", e_nasal(codes[row[2]]))
        previous = first

    # 2. semivowels: lift the voiced unaspirated stop of the same place by 1
    for label, parent in (("y", "j"), ("r", "ḍ"), ("l", "d")):
        add(label, parent, "lift1", e_lift(codes[parent], 1))
    add("v", "b", "lift1+joinD", e_join(e_lift(codes["b"], 1), D))

    # 3. sibilants and h: lift the aspirate of the same place by 2
    for label, parent in (("ś", "ch"), ("ṣ", "ṭh"), ("s", "th"), ("h", "gh")):
        add(label, parent, "lift2", e_lift(codes[parent], 2))

    # 4. simple vowels: lift the voiced unaspirated stop by 3
    for label, parent in (("a", "g"), ("i", "j"), ("u", "b"), ("ṛ", "ḍ"), ("ḷ", "d")):
        add(label, parent, "lift3", e_lift(codes[parent], 3))

    # 5. e o: join of two vowels' places, long. ai au: lift of e o.
    add("e", "a+i", "join", join_vertices(codes["a"], codes["i"], length=LONG, aperture=VOWEL))
    add("o", "a+u", "join", join_vertices(codes["a"], codes["u"], length=LONG, aperture=VOWEL))
    add("ai", "e", "lift1", e_lift(codes["e"], 1))
    add("au", "o", "lift1", e_lift(codes["o"], 1))
    return codes, log


SOUNDS, DERIVATION = _derive()
LABELS_BY_CODE = {c: l for l, c in SOUNDS.items()}

# ---------------------------------------------------------------------------
# The sutras: the one input that is not derived. The last token of each sutra
# is its it-marker. Order = the recited order.
# ---------------------------------------------------------------------------

SUTRAS: Tuple[Tuple[str, ...], ...] = (
    ("a", "i", "u", "ṇ"), ("ṛ", "ḷ", "k"), ("e", "o", "ṅ"), ("ai", "au", "c"),
    ("h", "y", "v", "r", "ṭ"), ("l", "ṇ"), ("ñ", "m", "ṅ", "ṇ", "n", "m"),
    ("jh", "bh", "ñ"), ("gh", "ḍh", "dh", "ṣ"), ("j", "b", "g", "ḍ", "d", "ś"),
    ("kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", "v"), ("k", "p", "y"),
    ("ś", "ṣ", "s", "r"), ("h", "l"),
)


@dataclass(frozen=True)
class Node:
    """A position on the sutra path."""

    rank: int
    label: str
    is_marker: bool

    @property
    def code(self) -> Optional[int]:
        return None if self.is_marker else SOUNDS[self.label]


def _path() -> Tuple[Node, ...]:
    out: List[Node] = []
    for sutra in SUTRAS:
        for index, label in enumerate(sutra):
            out.append(Node(len(out), label, index == len(sutra) - 1))
    return tuple(out)


PATH: Tuple[Node, ...] = _path()  # 57 nodes; the edges are (rank, rank+1)


def is_it(rank: int) -> bool:
    """1.3.3 halantyam, for the sutra text: the last consonant (hal) of each sutra is `it`.

    The path already marks a node as a marker exactly when it is the last token of its
    sutra, so this is the rule read off the structure: 14 nodes. That such a node is `it`
    only in the upadesa (here: the sutra text) is 1.3.3 itself ("upadese ity eva"); the
    circularity of `hal` inside 1.3.3 is resolved by the Kasika (a tantra use of hal).
    """
    return PATH[rank].is_marker


def it_ranks() -> Tuple[int, ...]:
    return tuple(n.rank for n in PATH if is_it(n.rank))


def meta_code(rank: int) -> int:
    """A marker is not a sound: a meta cell that names its place on the path."""
    if not 0 <= rank < len(PATH) or not PATH[rank].is_marker:
        raise InvalidCode(f"rank {rank} is not a marker")
    return 1 << META_SHIFT | rank


def first_rank(code: int) -> int:
    """First path position of a sound (h occurs twice; the first is used)."""
    for node in PATH:
        if not node.is_marker and node.code == code:
            return node.rank
    raise GraphError(f"{bits(code)} is not on the sutra path")


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


class AmbiguousStart(GraphError):
    """A start sound that occurs twice on the path needs an explicit occurrence (strict mode)."""


def start_ranks(code: int) -> Tuple[int, ...]:
    """Every path position where the sound `code` is recited (h has two)."""
    ranks = tuple(n.rank for n in PATH if not n.is_marker and n.code == code)
    if not ranks:
        raise GraphError(f"{bits(code)} is not on the sutra path")
    return ranks


def pratyahara(start: int, marker_label: str, nth: int = 1, *, start_occurrence: Optional[int] = None,
               strict: bool = False) -> Tuple[int, ...]:
    """Sounds from `start` up to the `nth` marker named `marker_label` after it.

    `start_occurrence` picks which recitation of a repeated start sound to use
    (1 = the first, the tradition's default: aṭ, aś, haś, iṇ, hal). With `strict`
    a repeated start sound and no explicit occurrence raises `AmbiguousStart`
    instead of silently taking the first, as `pratyahara-exhaustive-v0.1.yaml`
    asks (case `later-h-is-not-initial-h-for-hR`).
    """
    ranks = start_ranks(start)
    if start_occurrence is None:
        if strict and len(ranks) > 1:
            raise AmbiguousStart(f"{bits(start)} is recited {len(ranks)} times: give start_occurrence")
        start_occurrence = 1
    if not 1 <= start_occurrence <= len(ranks):
        raise GraphError(f"{bits(start)} has no recitation number {start_occurrence}")
    begin = ranks[start_occurrence - 1]
    seen = 0
    for node in PATH[begin + 1:]:
        if node.is_marker and node.label == marker_label:
            seen += 1
            if seen == nth:
                return tuple(n.code for n in PATH[begin:node.rank] if not n.is_marker)
    raise GraphError(f"no marker {marker_label!r} (occurrence {nth}) after {bits(start)}")


# ---------------------------------------------------------------------------
# Named pratyahara: name -> (start sound, marker, nth marker after the start, start occurrence)
# ---------------------------------------------------------------------------
# One row per classical name (43). `nth` counts the markers of that letter after the start, as in
# `pratyahara`. The occurrence rules are the Kasika's (preface, kAshikAvRRitti.txt 99-103, 165-176):
# `aṇ` takes the first ṇ, `iṇ` the second, and `aṇ2` is the aṇ of 1.1.69 (the second ṇ); a name that
# starts with h takes the first h. Verified: every row gives the set of the oracle/YAML name
# (docs/upc14-named-pratyahara-2026-10-01.tsv; the preface counts per marker agree for 13 of 14
# markers, see docs/upc14-pratyahara-counts-vs-kasika-2026-10-01.md; `cay` is the exception).

NAMED_PRATYAHARA = {
    "aṇ": ("a", "ṇ", 1, 1),
    "ak": ("a", "k", 1, 1),
    "ac": ("a", "c", 1, 1),
    "aṭ": ("a", "ṭ", 1, 1),
    "aṇ2": ("a", "ṇ", 2, 1),
    "am": ("a", "m", 1, 1),
    "aś": ("a", "ś", 1, 1),
    "al": ("a", "l", 1, 1),
    "ik": ("i", "k", 1, 1),
    "ic": ("i", "c", 1, 1),
    "iṇ": ("i", "ṇ", 2, 1),
    "uk": ("u", "k", 1, 1),
    "eṅ": ("e", "ṅ", 1, 1),
    "ec": ("e", "c", 1, 1),
    "aic": ("ai", "c", 1, 1),
    "yañ": ("y", "ñ", 1, 1),
    "yaṇ": ("y", "ṇ", 1, 1),
    "yam": ("y", "m", 1, 1),
    "yay": ("y", "y", 1, 1),
    "yar": ("y", "r", 1, 1),
    "vaś": ("v", "ś", 1, 1),
    "val": ("v", "l", 1, 1),
    "ral": ("r", "l", 1, 1),
    "may": ("m", "y", 1, 1),
    "ñam": ("ñ", "m", 1, 1),
    "ṅam": ("ṅ", "m", 1, 1),
    "jhaś": ("jh", "ś", 1, 1),
    "jhaṣ": ("jh", "ṣ", 1, 1),
    "jhay": ("jh", "y", 1, 1),
    "jhar": ("jh", "r", 1, 1),
    "jhal": ("jh", "l", 1, 1),
    "bhaṣ": ("bh", "ṣ", 1, 1),
    "jaś": ("j", "ś", 1, 1),
    "baś": ("b", "ś", 1, 1),
    "khay": ("kh", "y", 1, 1),
    "khar": ("kh", "r", 1, 1),
    "chav": ("ch", "v", 1, 1),
    "cay": ("c", "y", 1, 1),
    "car": ("c", "r", 1, 1),
    "śar": ("ś", "r", 1, 1),
    "śal": ("ś", "l", 1, 1),
    "haś": ("h", "ś", 1, 1),
    "hal": ("h", "l", 1, 1),
}


def pratyahara_named(name: str) -> Tuple[int, ...]:
    """The sounds of a classical pratyahara by its name (IAST, e.g. "aṇ", "iṇ", "hal", "bhaṣ")."""
    try:
        start, marker, nth, occurrence = NAMED_PRATYAHARA[unicodedata.normalize("NFC", name)]
    except KeyError:
        raise GraphError(f"{name!r} is not a named pratyahara of the sutra path") from None
    return pratyahara(SOUNDS[start], marker, nth, start_occurrence=occurrence)


def savarna(a: int, b: int, *, vartika: bool = False) -> bool:
    """1.1.9: same place, same aperture. The nose is a separate atom (1.1.8).

    `vartika=True` adds the vartika that makes ṛ and ḷ savarna with each other (the Kasika
    records this: line 53198 of kAshikAvRRitti.txt, as reported by the shiva agent). It is a
    stipulation ON TOP of 1.1.9 (their places differ, so the sutra alone does not give it);
    vidyut's `savarna_str` includes it. The default is the sutra as written.
    """
    va, vb = unpack(a), unpack(b)
    if va.place == vb.place and va.aperture == vb.aperture:
        return True
    if vartika:
        pair = {va.place, vb.place}
        return va.aperture == vb.aperture == VOWEL and pair == {M, D}
    return False


def savarna_status(a: int, b: int, *, vartika: bool = False) -> Optional[bool]:
    """Three-valued 1.1.9: True, False, or None when the Kasika does not decide.

    `savarna` answers a plain bool and says False for e~ai and o~au (their apertures differ: the
    wide-vowel step). That step is ours, taken from the Siksa tradition, not from the Kasika, and
    the Kasika's 1.1.9 does not settle these two pairs (as found by the panini agent's independent
    implementation, 2026-10-01: 861 pairs agree, these 2 do not). So here they are `None`
    (not decided), never True or False. Everything else equals `savarna`.
    """
    if savarna(a, b, vartika=vartika):
        return True
    va, vb = unpack(a), unpack(b)
    if va.place == vb.place and {va.aperture, vb.aperture} == {VOWEL, WIDE_VOWEL}:
        return None
    return False


def dirgha(a: int, b: int) -> int:
    """6.1.101: two savarna simple vowels merge into the long one."""
    va = unpack(a)
    if not savarna(a, b) or va.aperture != VOWEL:
        raise GraphError("dirgha needs two savarna simple vowels")
    if va.place == D:
        raise GraphError("ḷ has no long form (Kasika: lṛvarṇasya dīrghā na santi)")
    return Vertex(va.place, va.nasal, va.aperture, LONG, va.voice, va.asp).code


def guna(a: int, b: int) -> int:
    """6.1.87 (a + i/u): union of places, long."""
    return join_vertices(a, b, length=LONG, aperture=VOWEL)


def vrddhi(a: int, b: int) -> int:
    """6.1.88 (a + e/o): union of places, aperture lifted, long."""
    return join_vertices(a, b, length=LONG, aperture=WIDE_VOWEL)


def _distance(a: Vertex, b: Vertex) -> Tuple[int, int, int, int, int, int]:
    return (
        bin(a.place ^ b.place).count("1"),   # first: how far apart in the place lattice
        abs(a.aperture - b.aperture),
        a.voice ^ b.voice,
        a.asp ^ b.asp,
        a.nasal ^ b.nasal,
        abs(a.length - b.length),
    )


def nearest(source: int, targets: Iterable[int]) -> int:
    """1.1.50 sthane'ntaratamah: the target closest to `source`, place first.

    A tie is not resolved: the graph does not decide, so it raises Ambiguous.
    """
    src = unpack(source)
    scored = sorted((_distance(src, unpack(t)), t) for t in targets)
    if not scored:
        raise GraphError("no targets")
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        raise Ambiguous(f"{bits(source)} is equally near {bits(scored[0][1])} and {bits(scored[1][1])}")
    return scored[0][1]


def neighbors(code: int) -> Dict[str, int]:
    """Labelled edges out of a vertex that land on another canonical sound."""
    out: Dict[str, int] = {}
    for name, edge in (("asp", e_asp), ("voice", e_voice), ("nasal", e_nasal),
                       ("shift", e_shift), ("lift", e_lift), ("long", e_long)):
        try:
            target = edge(code)
        except GraphError:
            continue
        if target != code and target in LABELS_BY_CODE:
            out[name] = target
    return out


def to_dot() -> str:
    """The derivation as a Graphviz digraph: sounds are vertices, typed edges are arrows."""
    lines = ["digraph upc14v2 {", "  rankdir=LR;"]
    for label, code in SOUNDS.items():
        lines.append(f'  "{label}" [tooltip="{bits(code)}"];')
    for label, parent, edge in DERIVATION:
        for one in parent.split("+"):
            lines.append(f'  "{one}" -> "{label}" [label="{edge}"];')
    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if sys.argv[1:] == ["--dot"]:
        print(to_dot())
    else:
        for label, code in SOUNDS.items():
            print(f"{label:>2} {bits(code)}")


__all__ = [
    "NAMED_PRATYAHARA", "pratyahara_named",
    "Ambiguous", "AmbiguousStart", "CODE_MAX", "DERIVATION", "GraphError", "InvalidCode", "LABELS_BY_CODE", "PATH",
    "SOUNDS", "SUTRAS", "Vertex", "WIDTH", "bits", "dirgha", "e_asp", "e_join", "e_lift", "e_long",
    "e_nasal", "e_shift", "e_voice", "first_rank", "guna", "is_it", "it_ranks", "make", "meta_code", "nearest",
    "neighbors", "pratyahara", "savarna", "start_ranks", "to_dot", "unpack", "vrddhi",
]
