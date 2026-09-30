#!/usr/bin/env python3
"""PRĀṆA-14 — a 14-bit sound code with a savarṇa mask  (my design).

Design idea
-----------
UPC-14 v2 orders its fields place-first and stores voice and aspiration as two
separate atoms; savarṇa there is a *function* (`place == place and aperture ==
aperture`). PRĀṆA-14 orders the fields **effort-first** and packs
(voice, aspiration) into one Pāṇinian field `prāṇa`. The payoff: the whole
savarṇa test collapses to a single bit-mask AND.

    code (14) = meta(1) | effort(2) | wide(1) | place(5) | nasal(1) | prāṇa(2) | length(2)
                  13        12-11      10        9-5         4         3-2        1-0

    effort   0 spṛṣṭa  1 īṣat-spṛṣṭa  2 ūṣman  3 vivṛta      (Kāśikā, 1.1.9)
    wide     0 normal  1 wide  (distinguishes e/o from ai/au)
    place    Boolean lattice on 5 atoms  throat palate roof teeth lips (join = OR)
    nasal    the nose, apart from place (1.1.8)
    prāṇa    0 aghoṣa-alpa  1 aghoṣa-mahā  2 ghoṣa-alpa  3 ghoṣa-mahā
    length   0 short  1 long  2 pluta

The 42 Śiva-sūtra sounds are DERIVED from one seed `k` by typed edges
(`DERIVATION`); nothing is listed with its features.

The one property this design adds:

    savarna(a, b)  ==  (a & SAVARNA_MASK) == (b & SAVARNA_MASK)

because effort(2) + wide(1) + place(5) are eight *contiguous* bits (5..12).
That is also why the `wide` bit exists: it is what makes `e` and `ai` differ in
the mask (a vṛddhi pair that 1.1.9 does not call savarṇa), while a/ā still share
a mask (1.1.9 *does* call them savarṇa) — the split a length bit alone cannot
make.

Honest limits: the feature assignment is a modelling choice from the traditional
classification, checked for internal consistency only. This is an engineering
code, not evidence about Pāṇini.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

WIDTH = 14
CODE_MAX = (1 << WIDTH) - 1  # 0x3FFF

META_SHIFT, EFFORT_SHIFT, WIDE_SHIFT = 13, 11, 10
PLACE_SHIFT, NASAL_SHIFT, PRANA_SHIFT, LENGTH_SHIFT = 5, 4, 2, 0

EFFORT_MASK = 0b11
PLACE_MASK = 0b11111
PRANA_MASK = 0b11
LENGTH_MASK = 0b11

# --- field vocabularies -----------------------------------------------------

SPRSTA, ISAT_SPRSTA, USMAN, VIVRTA = 0, 1, 2, 3
EFFORT_NAMES = {SPRSTA: "spṛṣṭa", ISAT_SPRSTA: "īṣat-spṛṣṭa",
                USMAN: "ūṣman", VIVRTA: "vivṛta"}

# place lattice atoms (spine order throat -> lips)
K_THROAT, C_PALATE, M_ROOF, D_TEETH, O_LIPS = 0b00001, 0b00010, 0b00100, 0b01000, 0b10000
PLACE_SPINE = (K_THROAT, C_PALATE, M_ROOF, D_TEETH, O_LIPS)

AGHOSA_ALPA, AGHOSA_MAHA, GHOSA_ALPA, GHOSA_MAHA = 0, 1, 2, 3
PRANA_NAMES = {AGHOSA_ALPA: "aghoṣa-alpaprāṇa", AGHOSA_MAHA: "aghoṣa-mahāprāṇa",
               GHOSA_ALPA: "ghoṣa-alpaprāṇa", GHOSA_MAHA: "ghoṣa-mahāprāṇa"}

SHORT, LONG, PLUTA = 0, 1, 2
LENGTH_NAMES = {SHORT: "short", LONG: "long", PLUTA: "pluta"}

# effort + wide + place are eight contiguous bits -> savarṇa is one mask.
SAVARNA_MASK = (EFFORT_MASK << EFFORT_SHIFT) | (1 << WIDE_SHIFT) | (PLACE_MASK << PLACE_SHIFT)
assert SAVARNA_MASK == 0x1FE0


class PranaError(ValueError):
    pass


class InvalidCode(PranaError):
    """The bits are not a vertex. Fail closed; never repair."""


class Ambiguous(PranaError):
    """A nearest-vertex query has a tie; the code does not decide."""


def make(effort: int, place: int, *, wide: int = 0, nasal: int = 0,
         prana: int = 0, length: int = 0, meta: int = 0) -> int:
    return (meta << META_SHIFT | effort << EFFORT_SHIFT | wide << WIDE_SHIFT
            | place << PLACE_SHIFT | nasal << NASAL_SHIFT | prana << PRANA_SHIFT
            | length << LENGTH_SHIFT)


@dataclass(frozen=True)
class Vertex:
    effort: int
    place: int
    wide: int
    nasal: int
    prana: int
    length: int

    @property
    def code(self) -> int:
        return make(self.effort, self.place, wide=self.wide, nasal=self.nasal,
                    prana=self.prana, length=self.length)


def unpack(code: int) -> Vertex:
    if not 0 <= code <= CODE_MAX:
        raise InvalidCode(f"not a 14-bit code: {code!r}")
    if code >> META_SHIFT:
        raise InvalidCode("meta cell: not a phonetic vertex")
    v = Vertex(
        effort=(code >> EFFORT_SHIFT) & EFFORT_MASK,
        place=(code >> PLACE_SHIFT) & PLACE_MASK,
        wide=(code >> WIDE_SHIFT) & 1,
        nasal=(code >> NASAL_SHIFT) & 1,
        prana=(code >> PRANA_SHIFT) & PRANA_MASK,
        length=(code >> LENGTH_SHIFT) & LENGTH_MASK,
    )
    if v.place == 0:
        raise InvalidCode("no place atom: a sound needs an articulator")
    if v.length > PLUTA:
        raise InvalidCode(f"length {v.length} is off the path")
    if v.length and v.effort != VIVRTA:
        raise InvalidCode("only a vowel has length")
    if v.wide and v.effort != VIVRTA:
        raise InvalidCode("only a vowel is wide")
    return v


def bits(code: int) -> str:
    return format(code, "014b")


def fields(code: int) -> str:
    v = unpack(code)
    return (f"effort={EFFORT_NAMES[v.effort]} wide={v.wide} "
            f"place={v.place:05b} nasal={v.nasal} "
            f"prāṇa={PRANA_NAMES[v.prana]} length={LENGTH_NAMES[v.length]}")


# --------------------------------------------------------------------------
# edges: each is a function on vertices
# --------------------------------------------------------------------------


def e_asp(c: int) -> int:
    v = unpack(c)
    if v.effort != SPRSTA:
        raise InvalidCode("the aspiration edge exists on stops only")
    return c ^ (1 << PRANA_SHIFT)  # toggles mahāprāṇa


def e_voice(c: int) -> int:
    v = unpack(c)
    if v.effort != SPRSTA:
        raise InvalidCode("the voice edge exists on stops only")
    return c ^ (0b10 << PRANA_SHIFT)  # toggles ghoṣa


def e_nasal(c: int) -> int:
    """voiced, unaspirated, with the nose added (1.1.8)."""
    v = unpack(c)
    return Vertex(v.effort, v.place, v.wide, 1, GHOSA_ALPA, v.length).code


def e_shift(c: int) -> int:
    """Move every place atom one step along the spine throat->palate->...->lips."""
    v = unpack(c)
    if v.place & O_LIPS:
        raise InvalidCode("shift past the end of the spine")
    return Vertex(v.effort, v.place << 1, v.wide, v.nasal, v.prana, v.length).code


def e_lift(c: int, steps: int = 1) -> int:
    """Raise the effort along spṛṣṭa -> īṣat-spṛṣṭa -> ūṣman -> vivṛta."""
    v = unpack(c)
    eff = v.effort + steps
    if eff > VIVRTA:
        raise InvalidCode("effort lift past vivṛta")
    return Vertex(eff, v.place, v.wide, v.nasal, v.prana, v.length).code


def e_widen(c: int) -> int:
    v = unpack(c)
    if v.effort != VIVRTA:
        raise InvalidCode("only a vowel can be widened")
    return Vertex(v.effort, v.place, 1, v.nasal, v.prana, v.length).code


def e_long(c: int) -> int:
    v = unpack(c)
    if v.effort != VIVRTA:
        raise InvalidCode("only a vowel has length")
    return Vertex(v.effort, v.place, v.wide, v.nasal, v.prana,
                  min(v.length + 1, PLUTA)).code


def e_join(c: int, atoms: int) -> int:
    v = unpack(c)
    return Vertex(v.effort, v.place | atoms, v.wide, v.nasal, v.prana, v.length).code


def join_vowels(a: int, b: int, *, wide: int, length: int) -> int:
    va, vb = unpack(a), unpack(b)
    return Vertex(VIVRTA, va.place | vb.place, wide, va.nasal | vb.nasal,
                  GHOSA_ALPA, length).code


# --------------------------------------------------------------------------
# derivation: 42 sounds from the seed `k`
# --------------------------------------------------------------------------

SEED_LABEL, SEED_CODE = "k", make(SPRSTA, K_THROAT, prana=AGHOSA_ALPA)

# first member of each varga (spine order), and the full row
VARGA_FIRST = ("k", "c", "w", "t", "p")
VARGA_ROWS = {
    "k": ("k", "K", "g", "G", "N"),
    "c": ("c", "C", "j", "J", "Y"),
    "w": ("w", "W", "q", "Q", "R"),
    "t": ("t", "T", "d", "D", "n"),
    "p": ("p", "P", "b", "B", "m"),
}


def _derive() -> Tuple[Dict[str, int], List[Tuple[str, str, str]]]:
    codes: Dict[str, int] = {SEED_LABEL: SEED_CODE}
    log: List[Tuple[str, str, str]] = []

    def add(label: str, parent: str, edge: str, code: int) -> None:
        codes[label] = code
        log.append((label, parent, edge))

    previous = None
    for first in VARGA_FIRST:
        row = VARGA_ROWS[first]
        if previous is not None:
            add(first, previous, "shift", e_shift(codes[previous]))
        f = codes[first]
        add(row[1], first, "asp", e_asp(f))
        add(row[2], first, "voice", e_voice(f))
        add(row[3], row[2], "asp", e_asp(codes[row[2]]))
        add(row[4], row[2], "nasal", e_nasal(codes[row[2]]))
        previous = first

    # semivowels: lift the voiced unaspirated stop of the same place by one
    for label, parent in (("y", "j"), ("r", "q"), ("l", "d")):
        add(label, parent, "lift1", e_lift(codes[parent], 1))
    add("v", "b", "lift1+joinT", e_join(e_lift(codes["b"], 1), D_TEETH))

    # sibilants and h: lift the aspirated stop of the same place by two
    for label, parent in (("S", "C"), ("z", "W"), ("s", "T"), ("h", "G")):
        add(label, parent, "lift2", e_lift(codes[parent], 2))

    # simple vowels: lift the voiced unaspirated stop by three (-> vivṛta)
    for label, parent in (("a", "g"), ("i", "j"), ("u", "b"), ("f", "q"), ("x", "d")):
        add(label, parent, "lift3", e_lift(codes[parent], 3))
    for short, long_ in (("a", "A"), ("i", "I"), ("u", "U"), ("f", "F"), ("x", "X")):
        add(long_, short, "long", e_long(codes[short]))

    # e o: union of two vowel places, long. ai au: the widened form.
    add("e", "a+i", "join", join_vowels(codes["a"], codes["i"], wide=0, length=LONG))
    add("o", "a+u", "join", join_vowels(codes["a"], codes["u"], wide=0, length=LONG))
    add("E", "e", "widen", e_widen(codes["e"]))  # E = ai
    add("O", "o", "widen", e_widen(codes["o"]))  # O = au
    return codes, log


SOUNDS, DERIVATION = _derive()
LABELS_BY_CODE = {c: l for l, c in SOUNDS.items()}


# --------------------------------------------------------------------------
# the sūtras: the one input that is not derived
# --------------------------------------------------------------------------

SUTRAS: Tuple[Tuple[str, ...], ...] = (
    ("a", "i", "u", "R"), ("f", "x", "k"), ("e", "o", "N"), ("E", "O", "c"),
    ("h", "y", "v", "r", "w"), ("l", "R"), ("Y", "m", "N", "R", "n", "m"),
    ("J", "B", "Y"), ("G", "Q", "D", "z"), ("j", "b", "g", "q", "d", "S"),
    ("K", "P", "C", "W", "T", "c", "w", "t", "v"), ("k", "p", "y"),
    ("S", "z", "s", "r"), ("h", "l"),
)


@dataclass(frozen=True)
class Node:
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


PATH: Tuple[Node, ...] = _path()  # 57 nodes


def is_it(rank: int) -> bool:
    """1.3.3 halantyam, read off the structure: the last token of a sūtra is it."""
    return PATH[rank].is_marker


def it_ranks() -> Tuple[int, ...]:
    return tuple(n.rank for n in PATH if n.is_marker)


def meta_code(rank: int) -> int:
    if not 0 <= rank < len(PATH) or not PATH[rank].is_marker:
        raise InvalidCode(f"rank {rank} is not a marker")
    return (1 << META_SHIFT) | rank


# --------------------------------------------------------------------------
# queries
# --------------------------------------------------------------------------


class AmbiguousStart(PranaError):
    pass


def start_ranks(code: int) -> Tuple[int, ...]:
    ranks = tuple(n.rank for n in PATH if not n.is_marker and n.code == code)
    if not ranks:
        raise PranaError(f"{bits(code)} is not on the sūtra path")
    return ranks


def pratyahara(start: int, marker_label: str, nth: int = 1, *,
               start_occurrence: Optional[int] = None, strict: bool = False) -> Tuple[int, ...]:
    """Sounds from `start` up to the `nth` marker named `marker_label` after it."""
    ranks = start_ranks(start)
    if start_occurrence is None:
        if strict and len(ranks) > 1:
            raise AmbiguousStart(f"{bits(start)} is recited {len(ranks)} times")
        start_occurrence = 1
    if not 1 <= start_occurrence <= len(ranks):
        raise PranaError(f"{bits(start)} has no recitation number {start_occurrence}")
    begin = ranks[start_occurrence - 1]
    seen = 0
    for node in PATH[begin + 1:]:
        if node.is_marker and node.label == marker_label:
            seen += 1
            if seen == nth:
                return tuple(n.code for n in PATH[begin:node.rank] if not n.is_marker)
    raise PranaError(f"no marker {marker_label!r} (occurrence {nth}) after {bits(start)}")


def savarna(a: int, b: int) -> bool:
    """1.1.9 as a single mask: same effort, same wide, same place.

    (The nose is a separate atom and does not enter savarṇa; length and prāṇa
    are not part of it either — k and g, a and ā, are savarṇa.)
    """
    return (a & SAVARNA_MASK) == (b & SAVARNA_MASK)


def savarna_key(code: int) -> int:
    return code & SAVARNA_MASK


def dirgha(a: int, b: int) -> int:
    """6.1.101: two savarṇa simple vowels merge into the long one."""
    va = unpack(a)
    if not savarna(a, b) or va.effort != VIVRTA or va.wide:
        raise PranaError("dirgha needs two savarṇa simple vowels")
    if va.place == D_TEETH:
        raise PranaError("ḷ has no long form (Kāśikā: lṛvarṇasya dīrghā na santi)")
    return Vertex(va.effort, va.place, 0, va.nasal, va.prana, LONG).code


def guna(a: int, b: int) -> int:
    """6.1.87: union of places, long (a + i -> e)."""
    return join_vowels(a, b, wide=0, length=LONG)


def vrddhi(a: int, b: int) -> int:
    """6.1.88: union of places, widened, long (a + e -> ai)."""
    return join_vowels(a, b, wide=1, length=LONG)


def _distance(a: Vertex, b: Vertex) -> Tuple[int, int, int, int, int, int]:
    return (
        bin(a.place ^ b.place).count("1"),  # place first (1.1.50)
        abs(a.effort - b.effort),
        a.wide ^ b.wide,
        a.prana ^ b.prana,
        a.nasal ^ b.nasal,
        abs(a.length - b.length),
    )


def nearest(source: int, targets: Iterable[int]) -> int:
    """1.1.50 sthāne'ntaratamaḥ: the target closest to `source`, place first.

    A tie is not resolved: the code does not decide, so it raises Ambiguous.
    """
    src = unpack(source)
    scored = sorted((_distance(src, unpack(t)), t) for t in targets)
    if not scored:
        raise PranaError("no targets")
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        raise Ambiguous(f"{bits(source)} is equally near "
                        f"{bits(scored[0][1])} and {bits(scored[1][1])}")
    return scored[0][1]


def neighbors(code: int) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for name, edge in (("asp", e_asp), ("voice", e_voice), ("nasal", e_nasal),
                       ("shift", e_shift), ("lift", e_lift), ("widen", e_widen),
                       ("long", e_long)):
        try:
            target = edge(code)
        except PranaError:
            continue
        if target != code and target in LABELS_BY_CODE:
            out[name] = target
    return out


def to_dot() -> str:
    lines = ["digraph prana14 {", "  rankdir=LR;"]
    for label, code in SOUNDS.items():
        lines.append(f'  "{label}" [tooltip="{bits(code)}"];')
    for label, parent, edge in DERIVATION:
        for one in parent.split("+"):
            lines.append(f'  "{one}" -> "{label}" [label="{edge}"];')
    lines.append("}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------


def _selftest() -> None:
    # 1. all 42 sūtra sounds + 5 long vowels are derived
    assert len(SOUNDS) == 47, len(SOUNDS)
    # 2. every derived sound is a valid vertex and its code round-trips
    for label, code in SOUNDS.items():
        v = unpack(code)
        assert v.code == code, label
    # 3. savarṇa as a mask — the design claim
    S = SOUNDS
    assert savarna(S["k"], S["g"]) and savarna(S["k"], S["N"])
    assert savarna(S["k"], S["K"]) and savarna(S["g"], S["G"])
    assert not savarna(S["k"], S["c"])
    assert savarna(S["a"], S["A"]) and savarna(S["i"], S["I"])
    assert not savarna(S["i"], S["y"])
    assert not savarna(S["e"], S["E"])   # e vs ai — the `wide` bit does this
    assert not savarna(S["o"], S["O"])
    assert not savarna(S["e"], S["o"])
    # 4. guṇa / vṛddhi reproduce e o ai au by construction
    assert guna(S["a"], S["i"]) == S["e"]
    assert guna(S["a"], S["u"]) == S["o"]
    assert vrddhi(S["a"], S["e"]) == S["E"]
    assert vrddhi(S["a"], S["o"]) == S["O"]
    # 5. dīrgha
    assert dirgha(S["a"], S["a"]) == S["A"]
    # 6. nearest (1.1.50) — yaṇ and jaś, not listed anywhere
    yan_targets = [S[t] for t in ("y", "v", "r", "l")]
    assert {nearest(S[s], yan_targets) for s in ("i", "u", "f", "x")} == {S["y"], S["v"], S["r"], S["l"]}
    jas_targets = [S[t] for t in ("j", "b", "g", "q", "d")]
    for s in ("k", "K", "c", "C", "w", "W", "t", "T", "p", "P"):
        assert nearest(S[s], jas_targets) == S[{"k": "g", "K": "g", "c": "j", "C": "j",
                                                "w": "q", "W": "q", "t": "d", "T": "d",
                                                "p": "b", "P": "b"}[s]], s
    # 7. it-markers: 14 of them, one per sūtra
    assert len(it_ranks()) == 14 == len(SUTRAS)
    # 8. a classical pratyāhāra is an interval of the path
    ac = pratyahara(S["a"], "c")
    assert set(ac) == {S[t] for t in ("a", "i", "u", "f", "x", "e", "o", "E", "O")}
    hal = pratyahara(S["h"], "l")
    assert S["h"] in hal and S["y"] in hal and S["l"] in hal
    # 9. ill-formed codes fail closed
    for bad in (make(SPRSTA, K_THROAT, length=LONG),   # consonant with length
                make(SPRSTA, 0),                        # no place
                1 << META_SHIFT):                       # meta is not a vertex
        try:
            unpack(bad)
            raise AssertionError(f"{bits(bad)} should be rejected")
        except InvalidCode:
            pass
    print("PRĀṆA-14 self-test: OK")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--dot"]:
        print(to_dot())
    elif sys.argv[1:] == ["--fields"]:
        for label, code in SOUNDS.items():
            print(f"{label:>2} {bits(code)}  {fields(code)}")
    else:
        _selftest()
        if not sys.argv[1:]:
            print()
            for label, code in SOUNDS.items():
                print(f"  {label:>2}  {bits(code)}  0x{code:04X}")
