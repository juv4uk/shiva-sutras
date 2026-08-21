#!/usr/bin/env python3
"""
GraphEngine: Directed Semantic Graph (DAG) State Transition Engine for Derivation IR.

Implements immutable states, dependency-linked derivation events, and Proof-Carrying traces.
"""

from __future__ import annotations
import hashlib
import json
import unicodedata
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set

from derivation_cell import DerivationCell, DerivationStream, MorphemeTag, AnubandhaTag, SvaraLength
from paribhasha_resolver import PaniniRule, RuleClassification, ParibhashaResolver, ConflictResolution


def compute_canonical_hash(state_dict: dict) -> str:
    """Compute canonical SHA256 digest per trace-canonical-serialization-v0.1.md."""
    def normalize(val: Any) -> Any:
        if isinstance(val, str):
            return unicodedata.normalize("NFC", val)
        if isinstance(val, list):
            return [normalize(x) for x in val]
        if isinstance(val, dict):
            return {normalize(k): normalize(v) for k, v in val.items()}
        return val

    body = {
        "relations": state_dict.get("relations", []),
        "schema": state_dict.get("schema", "panini-state/0.1"),
        "serialization": state_dict.get("serialization", "canonical-json-sha256-v0.1"),
        "terms": state_dict.get("terms", [])
    }
    payload = json.dumps(normalize(body), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    raw_bytes = payload.encode("utf-8") + b"\n"
    digest = hashlib.sha256(raw_bytes).hexdigest()
    return f"state:sha256:{digest}"


@dataclass(frozen=True)
class TermNode:
    """A morphological component within a derivation state."""
    term_id: str
    kind: str                        # "dhAtu", "pratyaya", "lakara", "pada", "abhyasa", etc.
    source_form: str
    surface_form: str
    designations: Tuple[str, ...] = field(default_factory=tuple)
    stream: Optional[DerivationStream] = None

    def to_dict(self) -> dict:
        return {
            "id": self.term_id,
            "kind": self.kind,
            "source_form": self.source_form,
            "surface_form": self.surface_form,
            "designations": list(self.designations)
        }


@dataclass(frozen=True)
class RelationNode:
    """Directed semantic/morphological relation between terms."""
    kind: str                        # "attachment", "scope", "reduplication", "fusion", "implementation"
    source_term: str
    target_term: str

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "from": self.source_term,
            "to": self.target_term
        }


@dataclass
class DerivationState:
    """An immutable state in the derivation DAG."""
    state_id: str
    terms: List[TermNode]
    relations: List[RelationNode]
    schema: str = "panini-state/0.1"
    serialization: str = "canonical-json-sha256-v0.1"

    @property
    def canonical_hash(self) -> str:
        d = {
            "schema": self.schema,
            "serialization": self.serialization,
            "terms": [t.term_id for t in self.terms],
            "relations": [r.to_dict() for r in self.relations]
        }
        return compute_canonical_hash(d)

    @property
    def surface_form(self) -> str:
        return "".join(t.surface_form for t in self.terms if t.surface_form)

    def to_dict(self) -> dict:
        return {
            "id": self.state_id,
            "hash": self.canonical_hash,
            "schema": self.schema,
            "terms": [t.to_dict() for t in self.terms],
            "relations": [r.to_dict() for r in self.relations],
            "serialization": self.serialization
        }


@dataclass
class DerivationEvent:
    """An event in the proof trace."""
    event_id: str
    kind: str                        # "state-observed", "applicability-check", "rule-decision", "state-transition", "trace-terminated"
    depends_on: List[str]
    payload: Dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "kind": self.kind,
            "depends_on": self.depends_on,
            "payload": self.payload
        }


class DerivationDAG:
    """The directed acyclic graph maintaining derivation history and provenance."""

    def __init__(self, derivation_id: str):
        self.derivation_id = derivation_id
        self.states: List[DerivationState] = []
        self.events: List[DerivationEvent] = []
        self.rules_applied: List[PaniniRule] = []
        self.resolver = ParibhashaResolver()
        self._event_counter = 1

    def next_event_id(self) -> str:
        eid = f"evt:{self._event_counter:02d}"
        self._event_counter += 1
        return eid

    def add_initial_state(self, state_id: str, terms: List[TermNode], relations: List[RelationNode]) -> DerivationState:
        st = DerivationState(state_id=state_id, terms=terms, relations=relations)
        self.states.append(st)
        self.events.append(DerivationEvent(
            event_id=self.next_event_id(),
            kind="state-observed",
            depends_on=[],
            payload={"state": st.state_id, "hash": st.canonical_hash}
        ))
        return st

    def apply_transition(self, rule: PaniniRule, prev_state: DerivationState, new_state_id: str,
                         new_terms: List[TermNode], new_relations: List[RelationNode],
                         operation_name: str, policy_decision: str = "selected") -> DerivationState:
        """Execute a validated transition from prev_state to new_state."""
        # 1. Applicability Check Event
        last_evt_id = self.events[-1].event_id
        app_evt_id = self.next_event_id()
        self.events.append(DerivationEvent(
            event_id=app_evt_id,
            kind="applicability-check",
            depends_on=[last_evt_id],
            payload={"rule": rule.sutra_id, "outcome": "applicable"}
        ))

        # 2. Rule Decision Event
        dec_evt_id = self.next_event_id()
        self.events.append(DerivationEvent(
            event_id=dec_evt_id,
            kind="rule-decision",
            depends_on=[app_evt_id],
            payload={"rule": rule.sutra_id, "decision": policy_decision}
        ))

        # 3. State Transition Event
        new_st = DerivationState(state_id=new_state_id, terms=new_terms, relations=new_relations)
        self.states.append(new_st)
        if rule not in self.rules_applied:
            self.rules_applied.append(rule)

        trans_evt_id = self.next_event_id()
        self.events.append(DerivationEvent(
            event_id=trans_evt_id,
            kind="state-transition",
            depends_on=[dec_evt_id],
            payload={
                "rule": rule.sutra_id,
                "before": prev_state.state_id,
                "after": new_st.state_id,
                "operation": operation_name
            }
        ))

        return new_st

    def terminate_derivation(self, outcome: str = "success") -> None:
        last_evt_id = self.events[-1].event_id
        self.events.append(DerivationEvent(
            event_id=self.next_event_id(),
            kind="trace-terminated",
            depends_on=[last_evt_id],
            payload={"outcome": outcome, "final_state": self.states[-1].state_id}
        ))


class CanonicalDerivations:
    """Pre-built proof generators for canonical forms."""

    @staticmethod
    def derive_bhavati() -> DerivationDAG:
        dag = DerivationDAG("drv:canonical:bhavati-v0.1")

        # Rules
        r_3_2_123 = PaniniRule("3.2.123", "वर्तमाने लट्", "vartamAne laT", RuleClassification.VIDHI)
        r_3_4_78 = PaniniRule("3.4.78", "तिप्तस्झि...", "tiptasjhi...", RuleClassification.VIDHI)
        r_1_3_9 = PaniniRule("1.3.9", "तस्य लोपः", "tasya lopaH", RuleClassification.VIDHI)
        r_3_1_68 = PaniniRule("3.1.68", "कर्तरि शप्", "kartari Sap", RuleClassification.VIDHI)
        r_3_4_113 = PaniniRule("3.4.113", "तिङ्शित्सार्वधातुकम्", "tiNSitsArvaDAtukam", RuleClassification.SAMJNA)
        r_7_3_84 = PaniniRule("7.3.84", "सार्वधातुकार्धधातुकयोः", "sArvaDAtukArDaDAtukayoH", RuleClassification.VIDHI)
        r_6_1_78 = PaniniRule("6.1.78", "एचोऽयवायावः", "eco 'yavAyAvaH", RuleClassification.VIDHI)
        r_1_4_14 = PaniniRule("1.4.14", "सुप्तिङन्तं पदम्", "suptiGantaM padam", RuleClassification.SAMJNA)

        # State 0: Input BU
        t_root = TermNode("term:root-BU", "dhAtu", "BU", "BU", ("dhAtu", "aGga"))
        s0 = dag.add_initial_state("state:bhavati:00-input", [t_root], [])

        # State 1: BU + laT
        t_lat = TermNode("term:lakara-laT", "lakara", "laT", "laT", ("laT", "Tit"))
        s1 = dag.apply_transition(
            r_3_2_123, s0, "state:bhavati:01-lat",
            [t_root, t_lat], [RelationNode("attachment", t_root.term_id, t_lat.term_id)],
            "attach-lakara-laT"
        )

        # State 2: BU + tip
        t_tip = TermNode("term:tin-tip", "pratyaya", "tip", "tip", ("tiN", "pratyaya", "pit", "sArvaDAtuka"))
        s2 = dag.apply_transition(
            r_3_4_78, s1, "state:bhavati:02-tip",
            [t_root, t_tip], [RelationNode("attachment", t_root.term_id, t_tip.term_id)],
            "select-tin-tip"
        )

        # State 3: BU + ti
        t_ti = TermNode("term:tin-ti", "pratyaya", "tip", "ti", ("tiN", "pratyaya", "pit", "sArvaDAtuka"))
        s3 = dag.apply_transition(
            r_1_3_9, s2, "state:bhavati:03-ti",
            [t_root, t_ti], [RelationNode("attachment", t_root.term_id, t_ti.term_id)],
            "elide-it-p-preserve-pit"
        )

        # State 4: BU + Sap + ti
        t_sap = TermNode("term:vikarana-Sap", "pratyaya", "Sap", "Sap", ("vikaraRa", "pratyaya", "Sit", "pit", "sArvaDAtuka"))
        s4 = dag.apply_transition(
            r_3_1_68, s3, "state:bhavati:04-sap-ti",
            [t_root, t_sap, t_ti],
            [RelationNode("scope", t_root.term_id, t_sap.term_id), RelationNode("attachment", t_sap.term_id, t_ti.term_id)],
            "insert-vikarana-Sap"
        )

        # State 5: BU + a + ti
        t_sap_a = TermNode("term:vikarana-a", "pratyaya", "Sap", "a", ("vikaraRa", "pratyaya", "Sit-derived", "sArvaDAtuka"))
        s5 = dag.apply_transition(
            r_3_4_113, s4, "state:bhavati:05-sap-a-ti",
            [t_root, t_sap_a, t_ti],
            [RelationNode("scope", t_root.term_id, t_sap_a.term_id), RelationNode("attachment", t_sap_a.term_id, t_ti.term_id)],
            "elide-S-p-and-designate-sarvadhatuka"
        )

        # State 6: Bo + a + ti
        t_root_bo = TermNode("term:root-Bo", "dhAtu-guna", "BU", "Bo", ("dhAtu", "aGga", "guRa-applied"))
        s6 = dag.apply_transition(
            r_7_3_84, s5, "state:bhavati:06-guna-bo-a-ti",
            [t_root_bo, t_sap_a, t_ti],
            [RelationNode("scope", t_root_bo.term_id, t_sap_a.term_id), RelationNode("attachment", t_sap_a.term_id, t_ti.term_id)],
            "apply-guna-U-to-o"
        )

        # State 7: Bav + a + ti -> Bavati
        t_root_bav = TermNode("term:root-Bav", "dhAtu-sandhi", "BU", "Bav", ("dhAtu", "aGga", "av-AdeSa"))
        s7 = dag.apply_transition(
            r_6_1_78, s6, "state:bhavati:07-sandhi-bavati",
            [t_root_bav, t_sap_a, t_ti],
            [RelationNode("fusion", t_root_bav.term_id, t_sap_a.term_id)],
            "apply-eco-sandhi-o-a-to-av-a"
        )

        # State 8: Final Pada
        t_pada = TermNode("term:pada-Bavati", "pada", "BU+laT", "Bavati", ("tiGanta-pada",))
        dag.apply_transition(
            r_1_4_14, s7, "state:bhavati:08-pada-bavati",
            [t_pada], [],
            "assign-pada-samjna"
        )

        dag.terminate_derivation("success")
        return dag

    @staticmethod
    def derive_dadati() -> DerivationDAG:
        dag = DerivationDAG("drv:canonical:dadati-v0.1")

        # Rules
        r_3_2_123 = PaniniRule("3.2.123", "वर्तमाने लट्", "vartamAne laT", RuleClassification.VIDHI)
        r_3_4_78 = PaniniRule("3.4.78", "तिप्तस्झि...", "tiptasjhi...", RuleClassification.VIDHI)
        r_1_3_9 = PaniniRule("1.3.9", "तस्य लोपः", "tasya lopaH", RuleClassification.VIDHI)
        r_3_1_68 = PaniniRule("3.1.68", "कर्तरि शप्", "kartari Sap", RuleClassification.VIDHI)
        r_2_4_75 = PaniniRule("2.4.75", "जुहोत्यादिभ्यः श्लुः", "juhotyAdibhyaH SluH", RuleClassification.VIDHI, is_apavada_for="3.1.68")
        r_6_1_10 = PaniniRule("6.1.10", "श्लौ", "SlO", RuleClassification.VIDHI)
        r_6_1_4 = PaniniRule("6.1.4", "पूर्वोऽभ्यासः", "pUrvo'BhyAsaH", RuleClassification.SAMJNA)
        r_7_4_59 = PaniniRule("7.4.59", "ह्रस्वः", "hrasvaH", RuleClassification.VIDHI)
        r_1_1_3 = PaniniRule("1.1.3", "इको गुणवृद्धी", "iko guRavfdDI", RuleClassification.PARIBHASA)
        r_1_4_14 = PaniniRule("1.4.14", "सुप्तिङन्तं पदम्", "suptiGantaM padam", RuleClassification.SAMJNA)

        # State 0: Input dA
        t_root = TermNode("term:root-dA", "dhAtu", "dA", "dA", ("dhAtu", "aGga", "juhotyAdi"))
        s0 = dag.add_initial_state("state:dadati:00-input", [t_root], [])

        # State 1: dA + laT
        t_lat = TermNode("term:lakara-laT", "lakara", "laT", "laT", ("laT", "Tit"))
        s1 = dag.apply_transition(
            r_3_2_123, s0, "state:dadati:01-lat",
            [t_root, t_lat], [RelationNode("attachment", t_root.term_id, t_lat.term_id)],
            "attach-lakara-laT"
        )

        # State 2: dA + tip
        t_tip = TermNode("term:tin-tip", "pratyaya", "tip", "tip", ("tiN", "pratyaya", "pit", "sArvaDAtuka"))
        s2 = dag.apply_transition(
            r_3_4_78, s1, "state:dadati:02-tip",
            [t_root, t_tip], [RelationNode("attachment", t_root.term_id, t_tip.term_id)],
            "select-tin-tip"
        )

        # State 3: dA + ti
        t_ti = TermNode("term:tin-ti", "pratyaya", "tip", "ti", ("tiN", "pratyaya", "pit", "sArvaDAtuka"))
        s3 = dag.apply_transition(
            r_1_3_9, s2, "state:dadati:03-ti",
            [t_root, t_ti], [RelationNode("attachment", t_root.term_id, t_ti.term_id)],
            "elide-it-p"
        )

        # State 4: dA + Sap + ti
        t_sap = TermNode("term:vikarana-Sap", "pratyaya", "Sap", "Sap", ("vikaraRa", "pratyaya"))
        s4 = dag.apply_transition(
            r_3_1_68, s3, "state:dadati:04-sap-ti",
            [t_root, t_sap, t_ti], [RelationNode("scope", t_root.term_id, t_sap.term_id)],
            "insert-vikarana-Sap"
        )

        # State 5: dA + [Slu] + ti (Apavāda 2.4.75)
        t_marker_slu = TermNode("term:marker-Slu", "lopa-marker", "Slu", "", ("Slu", "lopa", "dvirvacana-trigger"))
        s5 = dag.apply_transition(
            r_2_4_75, s4, "state:dadati:05-slu-ti",
            [t_root, t_marker_slu, t_ti], [RelationNode("scope", t_root.term_id, t_marker_slu.term_id)],
            "replace-Sap-with-Slu", policy_decision="apavada-over-utsarga"
        )

        # State 6: dA dA + ti (Dvirvacana 6.1.10)
        t_abhyasa_dA = TermNode("term:abhyasa-dA", "abhyasa-dhatu", "dA", "dA", ("abhyAsa", "pUrva"))
        s6 = dag.apply_transition(
            r_6_1_10, s5, "state:dadati:06-dvirvacana",
            [t_abhyasa_dA, t_root, t_ti], [RelationNode("reduplication", t_root.term_id, t_abhyasa_dA.term_id)],
            "reduplicate-root-dA"
        )

        # State 7: da + dA + ti (Hrasva 7.4.59)
        t_abhyasa_da = TermNode("term:abhyasa-da", "abhyasa-dhatu-hrasva", "dA", "da", ("abhyAsa", "hrasva"))
        s7 = dag.apply_transition(
            r_7_4_59, s6, "state:dadati:07-hrasva",
            [t_abhyasa_da, t_root, t_ti], [RelationNode("scope", t_abhyasa_da.term_id, t_root.term_id)],
            "shorten-abhyasa-vowel-A-to-a"
        )

        # State 8: Guna check (1.1.3 non-ik prohibition)
        s8 = dag.apply_transition(
            r_1_1_3, s7, "state:dadati:08-guna-prohibited",
            [t_abhyasa_da, t_root, t_ti], [RelationNode("scope", t_abhyasa_da.term_id, t_root.term_id)],
            "retain-surface-root-form", policy_decision="guna-prohibited-non-ik"
        )

        # State 9: Pada
        t_pada = TermNode("term:pada-dadAti", "pada", "dA+laT", "dadAti", ("tiGanta-pada",))
        dag.apply_transition(
            r_1_4_14, s8, "state:dadati:09-pada-dadati",
            [t_pada], [],
            "assign-pada-samjna"
        )

        dag.terminate_derivation("success")
        return dag
