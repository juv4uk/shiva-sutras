#!/usr/bin/env python3
"""Bounded D14 6.1 application bridge from source-grounded rules to Text7.

This witness reuses:
- typed pratyahara operand edges from #117;
- the merged three-layer Text7 witness from PR #115;
- DerivationDAG event/proof machinery from prototype/derivation_ir.

It does not allocate D14 coordinates and does not make vidyut semantic authority.
Sutra 1.1.9 + 6.1.101 is the asserted specification for layer 1.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import sys
from typing import Optional, Tuple

HERE = Path(__file__).resolve().parent
PROTOTYPE = HERE.parent
SUTRA_GRAPH = PROTOTYPE / "sutra_graph"
for p in (str(HERE), str(PROTOTYPE), str(SUTRA_GRAPH)):
    if p not in sys.path:
        sys.path.insert(0, p)

from graph_engine import DerivationDAG, RelationNode, TermNode  # noqa: E402
from paribhasha_resolver import PaniniRule, RuleClassification  # noqa: E402
from proof_certificate import ProofCertificateGenerator, ProofCertificateVerifier  # noqa: E402
import d14_61_pratyahara_operands as operands  # noqa: E402
import test_savarna_dirgha_layers as layers  # noqa: E402
import upc14v2_sandhi as sd  # noqa: E402
import upc14v2_vowel_sandhi as vs  # noqa: E402


@dataclass(frozen=True)
class RuleApplicationEdge:
    rule_id: str
    relation: str
    input_pair: Tuple[str, str]
    required_classes: Tuple[str, ...]
    specification: Tuple[str, ...]
    status: str
    provenance: Tuple[str, ...]


@dataclass(frozen=True)
class TransformationEdge:
    rule_id: str
    relation: str
    input_pair: Tuple[str, str]
    output: Optional[str]
    operation: str
    status: str


@dataclass(frozen=True)
class ApplicationWitness:
    layer: int
    application: RuleApplicationEdge
    transformation: TransformationEdge
    vidyut_result: str
    vidyut_relation: str


RULE_6_1_101 = PaniniRule(
    "6.1.101",
    "अकः सवर्णे दीर्घः",
    "akaH savarRe dIrGaH",
    RuleClassification.VIDHI,
)

SPECIFICATION = ("1.1.9", "6.1.101")
PROVENANCE = (
    "docs/text7-candidate-d-ratification-2026-10-03.md",
    "prototype/test_savarna_dirgha_layers.py",
    "prototype/upc14v2_vowel_sandhi.py",
)


def _base_name(name: str) -> str:
    code = sd.code_of(name)
    return sd.label_of(sd.base(code))


def _class_requirements(a: str, b: str) -> Tuple[bool, bool]:
    ak = operands.edge_for("6.1.101", "akaḥ")
    ac = operands.edge_for("6.1.101", "aci")
    return _base_name(a) in set(ak.class_node.members), _base_name(b) in set(ac.class_node.members)


def classify(a: str, b: str, vidyut_result: str) -> ApplicationWitness:
    layer = layers.layer_of(a, b)
    left_ak, right_ac = _class_requirements(a, b)
    same = layers.bit_savarna(layers.CELLS[a], layers.CELLS[b])
    out_code = layers.bit_dirgha(layers.CELLS[a], layers.CELLS[b])
    oracle = layers.oracle_is_dirgha(a, b, vidyut_result)

    if layer == 1:
        applicable = left_ak and right_ac and same and out_code is not None
        if applicable:
            output = layers.NAME_OF[out_code]
            if output != vidyut_result or not oracle:
                raise AssertionError((a, b, vidyut_result, output))
            status = "ASSERTED-APPLICABLE"
            vidyut_relation = "AGREES-EVIDENCE"
        else:
            output = None
            if oracle:
                raise AssertionError(("unexpected vidyut dirgha outside asserted applicability", a, b, vidyut_result))
            status = "ASSERTED-NOT-APPLICABLE"
            vidyut_relation = "AGREES-EVIDENCE"

    elif layer == 2:
        output = None
        status = "ANNOTATED-VARTTIKA"
        vidyut_relation = "CLASSIFIED-DISAGREEMENT-WITH-VARTTIKA"

    else:
        output = None
        status = "ANNOTATED-RULE-SCOPE"
        vidyut_relation = "CLASSIFIED-SCOPE-FACT"

    application = RuleApplicationEdge(
        rule_id="6.1.101",
        relation="applies-to" if status == "ASSERTED-APPLICABLE" else "classified-against",
        input_pair=(a, b),
        required_classes=("ak", "ac"),
        specification=SPECIFICATION,
        status=status,
        provenance=PROVENANCE,
    )
    transformation = TransformationEdge(
        rule_id="6.1.101",
        relation="produces" if output is not None else "no-transition",
        input_pair=(a, b),
        output=output,
        operation="savarṇa-dīrgha",
        status=status,
    )
    return ApplicationWitness(
        layer=layer,
        application=application,
        transformation=transformation,
        vidyut_result=vidyut_result,
        vidyut_relation=vidyut_relation,
    )


def replay_corpus() -> Tuple[ApplicationWitness, ...]:
    return tuple(classify(a, b, result) for a, b, result in layers.ROWS)


def summary() -> dict:
    rows = replay_corpus()
    layer1 = [row for row in rows if row.layer == 1]
    asserted_applies = [row for row in layer1 if row.application.status == "ASSERTED-APPLICABLE"]
    layer2 = [row for row in rows if row.layer == 2]
    layer3 = [row for row in rows if row.layer == 3]
    firsts = {a for a, _, _ in layers.ROWS}
    return {
        "schema": "d14-6.1-text7-application-bridge/v1",
        "authority": "research-only",
        "specification": list(SPECIFICATION),
        "vidyut_role": "evidence-not-authority",
        "layer1_rows": len(layer1),
        "layer1_applications": len(asserted_applies),
        "layer2_annotated": len(layer2),
        "layer3_annotated": len(layer3),
        "corpus_first_position_o": "o" in firsts,
        "corpus_first_position_l_vocalic": "ḷ" in firsts,
        "d14_coordinates_allocated": 0,
    }


def build_positive_trace(a: str, b: str, vidyut_result: str) -> dict:
    witness = classify(a, b, vidyut_result)
    if witness.application.status != "ASSERTED-APPLICABLE":
        raise ValueError("positive trace requires an asserted applicable pair")
    assert witness.transformation.output is not None

    dag = DerivationDAG(f"drv:d14-6.1.101:{a}+{b}")
    left = TermNode(
        f"term:text7:left:{a}",
        "text7-vowel",
        a,
        a,
        ("Text7", "ak"),
    )
    right = TermNode(
        f"term:text7:right:{b}",
        "text7-vowel",
        b,
        b,
        ("Text7", "ac"),
    )
    s0 = dag.add_initial_state(
        f"state:d14-6.1.101:{a}+{b}:input",
        [left, right],
        [RelationNode("junction", left.term_id, right.term_id)],
    )

    out = witness.transformation.output
    result = TermNode(
        f"term:text7:result:{out}",
        "text7-vowel",
        f"{a}+{b}",
        out,
        ("Text7", "dīrgha-result"),
    )
    dag.apply_transition(
        RULE_6_1_101,
        s0,
        f"state:d14-6.1.101:{a}+{b}:output",
        [result],
        [],
        "savarṇa-dīrgha",
        policy_decision="selected-by-1.1.9-and-6.1.101",
    )
    dag.terminate_derivation("success")

    cert = ProofCertificateGenerator.to_json_dict(dag)
    errors = ProofCertificateVerifier.verify(cert)
    if errors:
        raise AssertionError(errors)

    return {
        "typed_application": {
            "rule": witness.application.rule_id,
            "relation": witness.application.relation,
            "input": list(witness.application.input_pair),
            "required_classes": list(witness.application.required_classes),
            "specification": list(witness.application.specification),
            "status": witness.application.status,
        },
        "typed_transformation": {
            "rule": witness.transformation.rule_id,
            "relation": witness.transformation.relation,
            "output": witness.transformation.output,
            "operation": witness.transformation.operation,
        },
        "proof_certificate": cert,
        "vidyut": {
            "result": vidyut_result,
            "role": witness.vidyut_relation,
        },
    }


if __name__ == "__main__":
    import json

    s = summary()
    print(json.dumps(s, ensure_ascii=False, sort_keys=True))
    for a, b, result in layers.ROWS:
        w = classify(a, b, result)
        if w.application.status == "ASSERTED-APPLICABLE":
            print(json.dumps(build_positive_trace(a, b, result), ensure_ascii=False, sort_keys=True))
            break
