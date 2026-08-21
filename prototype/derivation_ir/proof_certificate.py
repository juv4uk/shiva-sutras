#!/usr/bin/env python3
"""
ProofCertificate: Generator and Cryptographic Validator for Panini Derivations.

Emits verifiable certificates in JSON and S-Expression (.my) formats.
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from graph_engine import DerivationDAG, DerivationState, DerivationEvent, compute_canonical_hash


class ProofCertificateGenerator:
    """Generates verifiable derivation proof certificates."""

    @staticmethod
    def to_json_dict(dag: DerivationDAG) -> Dict[str, Any]:
        return {
            "ir_version": "panini-derivation-ir/0.1",
            "derivation_id": dag.derivation_id,
            "status": "success" if dag.events and dag.events[-1].payload.get("outcome") == "success" else "partial",
            "final_surface_form": dag.states[-1].surface_form if dag.states else "",
            "states": [s.to_dict() for s in dag.states],
            "rules": [
                {
                    "sutra_id": r.sutra_id,
                    "text_deva": r.sutra_text_deva,
                    "text_slp1": r.sutra_text_slp1,
                    "classification": r.classification.name
                }
                for r in dag.rules_applied
            ],
            "events": [e.to_dict() for e in dag.events]
        }

    @staticmethod
    def to_json_str(dag: DerivationDAG, indent: int = 2) -> str:
        return json.dumps(ProofCertificateGenerator.to_json_dict(dag), ensure_ascii=False, indent=indent)

    @staticmethod
    def to_sexpr_str(dag: DerivationDAG) -> str:
        """Render derivation as data-only S-Expression (.my format)."""
        lines = [
            ";; Proof-Carrying Derivation Certificate in My Lisp (.my)",
            f"(derivation-proof (id {dag.derivation_id})",
            f"  (status {dag.events[-1].payload.get('outcome', 'unknown')})",
            f"  (surface-form \"{dag.states[-1].surface_form}\")",
            "  (states"
        ]
        for st in dag.states:
            lines.append(f"    (state (id {st.state_id}) (hash \"{st.canonical_hash}\") (surface \"{st.surface_form}\"))")
        lines.append("  )")
        lines.append("  (rules")
        for r in dag.rules_applied:
            lines.append(f"    (rule (sutra \"{r.sutra_id}\") (type {r.classification.name}) (slp1 \"{r.sutra_text_slp1}\"))")
        lines.append("  )")
        lines.append("  (events")
        for ev in dag.events:
            deps = " ".join(ev.depends_on)
            lines.append(f"    (event (id {ev.event_id}) (kind {ev.kind}) (depends ({deps})))")
        lines.append("  )")
        lines.append(")")
        return "\n".join(lines)


class ProofCertificateVerifier:
    """Validates proof certificates against Panini Derivation IR invariants."""

    @staticmethod
    def verify(cert: Dict[str, Any]) -> List[str]:
        errors: List[str] = []

        # 1. Check required top-level fields
        for req in ("ir_version", "derivation_id", "status", "states", "rules", "events"):
            if req not in cert:
                errors.append(f"Missing required field: {req}")

        if errors:
            return errors

        # 2. Verify state hashes
        state_ids = set()
        for st in cert["states"]:
            sid = st.get("id")
            shash = st.get("hash")
            state_ids.add(sid)
            computed = compute_canonical_hash({
                "schema": st.get("schema", "panini-state/0.1"),
                "serialization": st.get("serialization", "canonical-json-sha256-v0.1"),
                "terms": [t["id"] for t in st.get("terms", [])],
                "relations": st.get("relations", [])
            })
            if shash != computed:
                errors.append(f"State {sid} hash mismatch: got {shash}, computed {computed}")

        # 3. Verify event dependencies
        event_ids = set()
        for ev in cert["events"]:
            eid = ev.get("event_id")
            event_ids.add(eid)
            for dep in ev.get("depends_on", []):
                if dep not in event_ids and dep != eid:
                    errors.append(f"Event {eid} references unknown or future dependency: {dep}")

        # 4. Verify termination
        if not any(ev.get("kind") == "trace-terminated" for ev in cert["events"]):
            errors.append("Proof certificate lacks trace-terminated event")

        return errors
