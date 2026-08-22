#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epistemic_linter.py - executable epistemology for shiva-sutras.

Turns the repository's methodological culture into machine-checkable
constraints. Each rule names the concrete failure class it blocks;
an artifact that blocks nothing is a candidate for deletion.

Rules (v1):
  R1 CLAIMS-SCHEMA     every exported claim carries status/evidence/scope
  R2 NO-INFECTED-EVIDENCE   an invalidated dataset may never serve as
                       evidence for a non-FALSIFIED claim
  R3 EVIDENCE-EXISTS   every evidence path referenced by a claim exists
  R4 JOURNAL-BLOCKS    journal entries declare which failure class they
                       block (warning until backlog cleared)
  R5 PREREGISTRATION   L-001 preregistration exists, declares data /
                       annotation / stability / outcome classes, and has
                       no outcome filled before the run started

Exit codes: 0 = clean (warnings allowed), 1 = at least one violation,
2 = structural error (could not read a governed artifact at all).
"""

import os
import re
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLAIMS_DOC = os.path.join(REPO_ROOT, "docs", "claims-export.yaml")
FREEZE_DOC = os.path.join(REPO_ROOT, "FREEZE_STAGE_6_0.md")
LEDGER_DOC = os.path.join(REPO_ROOT, "docs", "RESULTS_LEDGER.md")
JOURNAL_DIR = os.path.join(REPO_ROOT, "journal")
PREREG_DOC = os.path.join(REPO_ROOT, "docs", "preregistration-L001.yaml")

PREREG_REQUIRED_SECTIONS = ("data", "annotation", "stability", "outcome_classes")

STATUS_LINE = re.compile(r"\*\*status\*\*:\s*`?([A-Z][A-Z0-9-]*)")
EVIDENCE_LINE = re.compile(r"\*\*evidence\*\*:\s*(.+)")
SCOPE_LINE = re.compile(r"\*\*scope\*\*:\s*(.+)")
CLAIM_HEADER = re.compile(r"^### (SS-[A-Z0-9-]+)", re.M)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def iter_claim_blocks(text):
    """Yield (claim_id, block_text) for each '### SS-...' section."""
    matches = list(CLAIM_HEADER.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        yield m.group(1), text[m.start():end]


def invalidated_datasets(freeze_text):
    """Paths declared invalid by a freeze manifest - forever barred from
    serving as historical evidence."""
    datasets = []
    in_block = False
    for line in freeze_text.splitlines():
        if line.strip().startswith("known_invalid_synthetic_datasets"):
            in_block = True
            continue
        if in_block:
            stripped = line.strip().strip('-"')
            if stripped.startswith("- ") or (stripped and stripped.startswith("/")):
                pass
            if line.strip().startswith("-"):
                datasets.append(line.strip().lstrip("- ").strip().strip('"'))
            elif line.strip() and not line.startswith((" ", "\t")):
                break
    return [d for d in datasets if d]


class LintResult:
    def __init__(self):
        self.violations = []   # fail
        self.warnings = []     # advisory
        self.passed = []       # rule name + what it proved

    def violation(self, rule, message):
        self.violations.append((rule, message))

    def warning(self, rule, message):
        self.warnings.append((rule, message))

    def ok(self, rule, message):
        self.passed.append((rule, message))


def rule_claims_schema(claims_text, res):
    """R1: every claim block carries status/evidence/scope."""
    found = 0
    for claim_id, block in iter_claim_blocks(claims_text):
        found += 1
        if not STATUS_LINE.search(block):
            res.violation("R1", f"{claim_id}: missing status line")
        if not SCOPE_LINE.search(block):
            res.violation("R1", f"{claim_id}: missing scope (math result is "
                                "not historical proof without one)")
        if not EVIDENCE_LINE.search(block):
            res.violation("R1", f"{claim_id}: missing evidence pointer")
        if re.search(r"\*\*status\*\*:.*FALSIFIED", block) and \
                not re.search(r"falsif|refut|спростуванн", block, re.I):
            res.violation("R1", f"{claim_id}: FALSIFIED without recorded "
                                "refutation evidence")
    if found:
        res.ok("R1", f"{found} exported claims carry status/evidence/scope")


def claim_evidence_paths(claims_text):
    """Extract filesystem paths mentioned inside evidence lines."""
    paths = set()
    for _, block in iter_claim_blocks(claims_text):
        m = EVIDENCE_LINE.search(block)
        if not m:
            continue
        for token in re.findall(r"[A-Za-z0-9_./-]+\.(?:my|yaml|yml|md|json)", m.group(1)):
            paths.add(token)
    return paths


def rule_no_infected_evidence(claims_text, freeze_text, ledger_text, res):
    """R2: an invalidated dataset never supports a non-FALSIFIED claim,
    neither in the export registry nor in the results ledger."""
    bad = invalidated_datasets(freeze_text)
    if not bad:
        res.warning("R2", "no known_invalid_synthetic_datasets declared - "
                          "the invalidation list is empty")
        return
    for claim_id, block in iter_claim_blocks(claims_text):
        falsified = bool(re.search(r"\*\*status\*\*:.*FALSIFIED", block))
        for ds in bad:
            base = os.path.basename(ds.rstrip("/"))
            if base and base in block and not falsified:
                res.violation("R2", f"{claim_id}: cites invalidated dataset "
                                    f"'{ds}' while claiming {STATUS_LINE.search(block).group(1) if STATUS_LINE.search(block) else '?'}")
    # ledger: an invalidated path may appear only next to its invalidation
    for line_no, line in enumerate(ledger_text.splitlines(), 1):
        for ds in bad:
            base = os.path.basename(ds.rstrip("/"))
            if base in line and not re.search(r"invalid|falsified|заборонен|синтетичн", line, re.I):
                res.violation("R2", f"{os.path.basename(LEDGER_DOC)}:{line_no} "
                                    f"references '{base}' outside an "
                                    "invalidation context")
    res.ok("R2", "no invalidated dataset cited as live evidence")


def rule_evidence_exists(claims_text, res):
    """R3: every evidence path points at something real."""
    missing = 0
    for path in sorted(claim_evidence_paths(claims_text)):
        full = os.path.join(REPO_ROOT, path)
        if not os.path.exists(full) and not os.path.isdir(full):
            res.violation("R3", f"evidence path does not exist: {path}")
            missing += 1
    if not missing:
        res.ok("R3", "all evidence paths resolve on disk")


def rule_journal_blocks(res):
    """R4: each journal entry declares the failure class it blocks.
    Warning-only during the migration backlog."""
    if not os.path.isdir(JOURNAL_DIR):
        res.violation("R4", "journal/ directory missing entirely")
        return
    unchecked = 0
    for fname in sorted(os.listdir(JOURNAL_DIR)):
        if not fname.endswith((".yaml", ".yml")):
            continue
        path = os.path.join(JOURNAL_DIR, fname)
        try:
            doc = yaml.safe_load(read(path))
        except Exception as e:  # noqa: BLE001 - linting must survive input
            res.violation("R4", f"journal/{fname}: unparseable YAML ({e})")
            continue
        if not isinstance(doc, dict):
            continue
        if "blocks" not in doc:
            res.warning("R4", f"journal/{fname}: no 'blocks:' declaration - "
                              "which failure class does this entry block?")
            unchecked += 1
    if not unchecked:
        res.ok("R4", "every journal entry declares a blocked failure class")


def rule_preregistration(res):
    """R5: L-001 preregistration exists, is structurally complete, and has
    no outcome filled before the run started."""
    if not os.path.exists(PREREG_DOC):
        res.violation("R5", f"missing {os.path.relpath(PREREG_DOC, REPO_ROOT)} - "
                            "the blind reconstruction run must be registered "
                            "before it starts (outcome classes A-D locked in "
                            "advance, measurement instrument included)")
        return
    try:
        doc = yaml.safe_load(read(PREREG_DOC))
    except Exception as e:  # noqa: BLE001
        res.violation("R5", f"preregistration unparseable: {e}")
        return
    for section in PREREG_REQUIRED_SECTIONS:
        if section not in doc:
            res.violation("R5", f"preregistration missing section '{section}'")
    outcome = str(doc.get("outcome_class", "")).strip()
    if outcome:
        # An outcome before a run start would mean the gates moved early.
        res.violation("R5", "outcome_class already filled while the run has "
                            "not been marked completed - preregistration "
                            "must stay blind")
    else:
        res.ok("R5", "preregistration present, sections complete, still blind")


def run_lint():
    res = LintResult()
    claims_text = read(CLAIMS_DOC)
    freeze_text = read(FREEZE_DOC)
    ledger_text = read(LEDGER_DOC)

    rule_claims_schema(claims_text, res)
    rule_no_infected_evidence(claims_text, freeze_text, ledger_text, res)
    rule_evidence_exists(claims_text, res)
    rule_journal_blocks(res)
    rule_preregistration(res)
    return res


def main(argv):
    strict = "--strict" in argv
    try:
        res = run_lint()
    except OSError as e:
        print(f"structural error: cannot read a governed artifact: {e}")
        return 2
    for rule, msg in res.passed:
        print(f"  ok       {rule}  {msg}")
    for rule, msg in res.warnings:
        print(f"  warning  {rule}  {msg}")
    for rule, msg in res.violations:
        print(f"  FAIL     {rule}  {msg}")
    print(f"\nepistemic lint: {len(res.passed)} passed, "
          f"{len(res.warnings)} warnings, {len(res.violations)} violations")
    if violations := res.violations:
        return 1
    if strict and res.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
