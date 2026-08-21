#!/usr/bin/env python3
"""
Paribhāṣā Resolver: 5-Tier Conflict Resolution Engine for Panini Sūtras.

Hierarchy of Principles:
1. Apavāda (Special / Exception rule) > Utsarga (General rule)
2. Nitya (Constant / Invariant rule) > Anitya (Non-constant rule)
3. Antaraṅga (Internal / fewer triggers) > Bahiraṅga (External triggers)
4. Para (Later rule in Aṣṭādhyāyī 1.1 - 8.1) > Pūrva (Earlier rule) [1.4.2 vipratiṣedhe paraṁ kāryam]
5. Asiddhatva (Tripādī 8.2.1 pūrvatrāsiddham): Sūtras in 8.2-8.4 are invisible to earlier sections.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Optional, Tuple, Dict, Any


class RuleScope(IntEnum):
    """Rule architectural domain."""
    SAPTA_ADHYAYI = 1   # Adhyāyas 1.1 through 8.1 (siddha domain)
    TRIPADI = 2         # Adhyāya 8.2.1 through 8.4.68 (asiddha domain)


class RuleClassification(IntEnum):
    """Traditional rule types in Vyākaraṇa."""
    VIDHI = 1           # Prescriptive / Operational (e.g. 7.3.84, 6.1.78)
    SAMJNA = 2          # Definitional / Naming (e.g. 1.1.2, 6.1.4, 1.4.14)
    PARIBHASA = 3       # Metarule / Interpretive (e.g. 1.1.3, 1.1.50, 1.4.2)
    ADHIKARA = 4        # Governing Heading / Scope (e.g. 3.1.91, 6.4.1)
    ATIDESA = 5         # Analogy / Transfer (e.g. 1.2.4)
    NIYAMA = 6          # Restriction / Constraint


@dataclass(frozen=True)
class PaniniRule:
    """Represents a formalized rule from the Aṣṭādhyāyī."""
    sutra_id: str                          # e.g. "3.1.68", "2.4.75", "7.3.84"
    sutra_text_deva: str                   # Devanagari text
    sutra_text_slp1: str                   # SLP1 text
    classification: RuleClassification
    is_apavada_for: Optional[str] = None   # Sūtra ID of the utsarga rule it overrides
    is_nitya: bool = False                 # Whether the rule is nitya
    is_antaranga: bool = False             # Whether the rule is antaraṅga
    domain: RuleScope = RuleScope.SAPTA_ADHYAYI
    description: str = ""

    @property
    def chapter_quad(self) -> Tuple[int, int, int]:
        """Parse 'X.Y.Z' into (adhyāya, pāda, sūtra_num)."""
        parts = [int(p) for p in self.sutra_id.split(".")]
        return parts[0], parts[1], parts[2]

    @property
    def is_tripadi(self) -> bool:
        a, p, _ = self.chapter_quad
        return (a == 8 and p >= 2)

    def is_later_than(self, other: PaniniRule) -> bool:
        """True if self appears after other in the linear text of Aṣṭādhyāyī."""
        return self.chapter_quad > other.chapter_quad


@dataclass
class ConflictResolution:
    """Outcome of a conflict resolution between two or more applicable rules."""
    selected_rule: PaniniRule
    rejected_rule: PaniniRule
    winning_principle: str                 # "apavada", "nitya", "antaranga", "para", "asiddhatva"
    explanation: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class ParibhashaResolver:
    """
    Arbitrates conflicts between candidate rules using Panini's canonical paribhāṣā hierarchy.
    """

    def __init__(self):
        self.rules_db: Dict[str, PaniniRule] = {}

    def register_rule(self, rule: PaniniRule) -> None:
        self.rules_db[rule.sutra_id] = rule

    def resolve_binary_conflict(self, rule_a: PaniniRule, rule_b: PaniniRule) -> ConflictResolution:
        """
        Arbitrate between two competing rules applicable to the same derivation state.
        """
        # Tier 1: Apavāda (Special rule overrides General rule)
        if rule_a.is_apavada_for == rule_b.sutra_id:
            return ConflictResolution(
                selected_rule=rule_a,
                rejected_rule=rule_b,
                winning_principle="apavada",
                explanation=f"Rule {rule_a.sutra_id} is an apavāda (special exception) for utsarga {rule_b.sutra_id}."
            )
        if rule_b.is_apavada_for == rule_a.sutra_id:
            return ConflictResolution(
                selected_rule=rule_b,
                rejected_rule=rule_a,
                winning_principle="apavada",
                explanation=f"Rule {rule_b.sutra_id} is an apavāda (special exception) for utsarga {rule_a.sutra_id}."
            )

        # Tier 2: Nitya > Anitya (Constant rule overrides non-constant rule)
        if rule_a.is_nitya and not rule_b.is_nitya:
            return ConflictResolution(
                selected_rule=rule_a,
                rejected_rule=rule_b,
                winning_principle="nitya",
                explanation=f"Rule {rule_a.sutra_id} is nitya (unconditionally persistent) over anitya {rule_b.sutra_id}."
            )
        if rule_b.is_nitya and not rule_a.is_nitya:
            return ConflictResolution(
                selected_rule=rule_b,
                rejected_rule=rule_a,
                winning_principle="nitya",
                explanation=f"Rule {rule_b.sutra_id} is nitya (unconditionally persistent) over anitya {rule_a.sutra_id}."
            )

        # Tier 3: Antaraṅga > Bahiraṅga (Internal / fewer triggers wins)
        if rule_a.is_antaranga and not rule_b.is_antaranga:
            return ConflictResolution(
                selected_rule=rule_a,
                rejected_rule=rule_b,
                winning_principle="antaranga",
                explanation=f"Rule {rule_a.sutra_id} is antaraṅga (internally conditioned) over bahiraṅga {rule_b.sutra_id}."
            )
        if rule_b.is_antaranga and not rule_a.is_antaranga:
            return ConflictResolution(
                selected_rule=rule_b,
                rejected_rule=rule_a,
                winning_principle="antaranga",
                explanation=f"Rule {rule_b.sutra_id} is antaraṅga (internally conditioned) over bahiraṅga {rule_a.sutra_id}."
            )

        # Tier 4 & 5: Asiddhatva (Tripādī vs Sapta-adhyāyī) and Vipratiṣedha (1.4.2 Para > Pūrva)
        if not rule_a.is_tripadi and rule_b.is_tripadi:
            return ConflictResolution(
                selected_rule=rule_a,
                rejected_rule=rule_b,
                winning_principle="asiddhatva",
                explanation=f"Tripādī rule {rule_b.sutra_id} is asiddha (invisible) to Sapta-adhyāyī rule {rule_a.sutra_id} (8.2.1)."
            )
        if rule_a.is_tripadi and not rule_b.is_tripadi:
            return ConflictResolution(
                selected_rule=rule_b,
                rejected_rule=rule_a,
                winning_principle="asiddhatva",
                explanation=f"Tripādī rule {rule_a.sutra_id} is asiddha (invisible) to Sapta-adhyāyī rule {rule_b.sutra_id} (8.2.1)."
            )

        # Within Sapta-adhyāyī: 1.4.2 vipratiṣedhe paraṁ kāryam (later rule wins)
        if rule_a.is_later_than(rule_b):
            return ConflictResolution(
                selected_rule=rule_a,
                rejected_rule=rule_b,
                winning_principle="para",
                explanation=f"By 1.4.2 vipratiṣedhe paraṁ kāryam, later rule {rule_a.sutra_id} prevails over {rule_b.sutra_id}."
            )
        else:
            return ConflictResolution(
                selected_rule=rule_b,
                rejected_rule=rule_a,
                winning_principle="para",
                explanation=f"By 1.4.2 vipratiṣedhe paraṁ kāryam, later rule {rule_b.sutra_id} prevails over {rule_a.sutra_id}."
            )
