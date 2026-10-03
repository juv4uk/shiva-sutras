#!/usr/bin/env python3
"""Expose a bounded Paribhasa decision as a typed D14 donor relation (#119).

Real 6.1 control:
- 6.1.78 eco 'yavayavah is the general rule.
- 6.1.109 enah padantad ati is attested by the Kasika as an apavada of
  the ay/av substitutions.

The existing ParibhashaResolver performs the arbitration.  This module makes
the selected/rejected rules, winning principle, context and provenance explicit
as a proof relation.  No D14 coordinate is allocated.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Optional, Tuple

HERE = Path(__file__).resolve().parent
PROTOTYPE = HERE.parent
ROOT = PROTOTYPE.parent
for p in (str(HERE), str(PROTOTYPE)):
    if p not in sys.path:
        sys.path.insert(0, p)

from paribhasha_resolver import (  # noqa: E402
    PaniniRule,
    ParibhashaResolver,
    RuleClassification,
)
import upc14v2_vowel_sandhi as vs  # noqa: E402

KASIKA_6_1_109 = ROOT / "ksetra" / "astadhyayi" / "sources" / "KASIKA-6.1.109.yaml"

GENERAL = PaniniRule(
    "6.1.78",
    "एचोऽयवायावः",
    "eco 'yavAyAvaH",
    RuleClassification.VIDHI,
)
SPECIAL = PaniniRule(
    "6.1.109",
    "एङः पदान्तादति",
    "eNaH padAntAd ati",
    RuleClassification.VIDHI,
    is_apavada_for="6.1.78",
)


@dataclass(frozen=True)
class ParibhashaDecisionEdge:
    """Typed proof relation for one conflict decision."""

    relation: str
    principle: str
    selected_rule: str
    rejected_rule: str
    context: Tuple[str, ...]
    semantic_effect: str
    source_id: str
    evidence_tier: str
    provenance_path: str
    explanation: str


def kasika_attests_apavada() -> bool:
    """Require the checked-in source witness, not the code comment, for authority."""
    raw = KASIKA_6_1_109.read_text(encoding="utf-8")
    required = (
        "source_id: KASIKA-6.1.109",
        "sutra: eṅaḥ padāntād ati",
        "ayavādeśayor ayam apavādaḥ",
        "status: REAL",
        "witness: GRETIL-KASIKA",
    )
    return all(token in raw for token in required)


def context_has_conflict(left: str, right: str, *, padanta: bool) -> bool:
    """The bounded context in which both the general and special rule compete."""
    return padanta and left in {"e", "o"} and right == "a"


def decide(left: str, right: str, *, padanta: bool = True) -> Optional[ParibhashaDecisionEdge]:
    """Return a typed apavada decision when the real conflict is present."""
    if not context_has_conflict(left, right, padanta=padanta):
        return None
    if not kasika_attests_apavada():
        raise RuntimeError("source-grounded apavada evidence missing")

    resolver = ParibhashaResolver()
    result = resolver.resolve_binary_conflict(GENERAL, SPECIAL)
    if result.selected_rule.sutra_id != "6.1.109":
        raise AssertionError(result)
    if result.rejected_rule.sutra_id != "6.1.78":
        raise AssertionError(result)
    if result.winning_principle != "apavada":
        raise AssertionError(result)

    actual = vs.vowel_sandhi(left, right, padanta=padanta)
    if actual.trace != ("6.1.109",):
        raise AssertionError(("application result disagrees with decision", actual))

    return ParibhashaDecisionEdge(
        relation="governs-rule-decision",
        principle="apavada",
        selected_rule="6.1.109",
        rejected_rule="6.1.78",
        context=("padanta", f"left={left}", "right=short-a"),
        semantic_effect=f"{left}+a -> {actual.text}",
        source_id="KASIKA-6.1.109",
        evidence_tier="commentarial-supported",
        provenance_path="ksetra/astadhyayi/sources/KASIKA-6.1.109.yaml",
        explanation=result.explanation,
    )


def falsifier_without_apavada_fact():
    """Removing the explicit apavada relation must change the winning principle."""
    plain_special = PaniniRule(
        SPECIAL.sutra_id,
        SPECIAL.sutra_text_deva,
        SPECIAL.sutra_text_slp1,
        SPECIAL.classification,
    )
    resolver = ParibhashaResolver()
    result = resolver.resolve_binary_conflict(GENERAL, plain_special)
    if result.winning_principle == "apavada":
        raise AssertionError("apavada survived after its semantic fact was removed")
    return result


if __name__ == "__main__":
    edge = decide("e", "a", padanta=True)
    assert edge is not None
    print("RELATION=" + edge.relation)
    print("PRINCIPLE=" + edge.principle)
    print("SELECTED=" + edge.selected_rule)
    print("REJECTED=" + edge.rejected_rule)
    print("EVIDENCE-TIER=" + edge.evidence_tier)
    print("SOURCE=" + edge.source_id)
    print("NO-CONFLICT-INTERNAL=" + str(decide("e", "a", padanta=False) is None))
    control = falsifier_without_apavada_fact()
    print("WITHOUT-APAVADA-PRINCIPLE=" + control.winning_principle)
    print("D14-COORDINATES-ALLOCATED=0")
