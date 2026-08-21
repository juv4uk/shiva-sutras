"""Proof-Carrying Derivation IR & Paribhāṣā Conflict Resolver."""

import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DerivationStep:
    step_num: int
    sutra_id: str
    sutra_text: str
    rule_type: str       # vidhi | atideśa | saṁjñā | paribhāṣā
    lhs: str
    rhs: str
    rationale: str
    state_hash: str = ""

    def compute_hash(self, prev_hash: str = "") -> str:
        payload = f"{self.step_num}:{self.sutra_id}:{self.lhs}->{self.rhs}:{prev_hash}"
        self.state_hash = f"state:{hashlib.sha256(payload.encode()).hexdigest()[:16]}"
        return self.state_hash

@dataclass
class DerivationRecord:
    derivation_id: str
    root: str
    gana: int
    intent: Dict[str, str]
    surface_form: str
    steps: List[DerivationStep] = field(default_factory=list)

    def add_step(self, sutra_id: str, sutra_text: str, rule_type: str, lhs: str, rhs: str, rationale: str) -> DerivationStep:
        prev_hash = self.steps[-1].state_hash if self.steps else self.derivation_id
        step = DerivationStep(
            step_num=len(self.steps) + 1,
            sutra_id=sutra_id,
            sutra_text=sutra_text,
            rule_type=rule_type,
            lhs=lhs,
            rhs=rhs,
            rationale=rationale
        )
        step.compute_hash(prev_hash)
        self.steps.append(step)
        return step

    def to_json(self) -> str:
        data = {
            "derivation_id": self.derivation_id,
            "root": self.root,
            "gana": self.gana,
            "intent": self.intent,
            "surface_form": self.surface_form,
            "step_count": len(self.steps),
            "certificate_hash": self.steps[-1].state_hash if self.steps else "",
            "steps": [
                {
                    "step": s.step_num,
                    "sutra": s.sutra_id,
                    "text": s.sutra_text,
                    "type": s.rule_type,
                    "transformation": f"{s.lhs} -> {s.rhs}",
                    "rationale": s.rationale,
                    "state_hash": s.state_hash
                }
                for s in self.steps
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

def resolve_priority(rule_a: str, rule_b: str, priority_table: Dict[str, int]) -> str:
    """Paribhāṣā Conflict Resolver: Apavāda (5) > Nitya (4) > Antaraṅga (3) > Para (2) > Pūrva (1)."""
    p_a = priority_table.get(rule_a, 0)
    p_b = priority_table.get(rule_b, 0)
    return rule_a if p_a >= p_b else rule_b
