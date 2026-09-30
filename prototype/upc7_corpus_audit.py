#!/usr/bin/env python3
"""Reproducible UPC-7 corpus evidence for shiva-sutras#35.

The corpus snapshots are repository evidence only. Unicode is input transport;
all coverage decisions go through the public UPC7Text layout encoder.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from upc7_layouts import UPC7LayoutError, UPC7Text

HERE = Path(__file__).resolve().parent
CORPUS_DIR = HERE / "corpus"
REPORT = HERE / "upc7-corpus-report.json"

UK_FIXTURE = CORPUS_DIR / "upc7-uk-own.txt"
SA_FIXTURE = CORPUS_DIR / "upc7-sa-slp1.txt"

UK_TOKEN_RE = re.compile(
    r"[А-Яа-яІіЇїЄєҐґ]+(?:['’ʼ-][А-Яа-яІіЇїЄєҐґ]+)*"
)
DIGIT_RE = re.compile(r"[0-9]")

PROVENANCE = {
    "uk": {
        "fixture": "prototype/corpus/upc7-uk-own.txt",
        "sources": [
            {
                "path": "extensions/COMPARATIVE-GRAMMAR-uk-sa.md",
                "git_blob": "44d2c678fe2debd290a210f3289bea443df10a4b",
                "selection": "project-authored Ukrainian grammar prose and examples",
            },
            {
                "path": "docs/sarvam-integration-guide.uk.md",
                "git_blob": "428134bb31302534244292b9e7b3d1b313b3dbee",
                "selection": "project-authored technical Ukrainian prose",
            },
        ],
    },
    "sa-slp1": {
        "fixture": "prototype/corpus/upc7-sa-slp1.txt",
        "sources": [
            {
                "path": "ksetra/canon/siva-sutras-encoded.yaml",
                "git_blob": "746d1a23a15153725beafac870fc287913a2a4a2",
                "selection": "all 14 text_slp1 rows",
            }
        ],
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _body_lines(path: Path) -> Iterable[str]:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#"):
            yield line


def _uk_tokens(path: Path) -> Tuple[List[str], Counter]:
    text = "\n".join(_body_lines(path))
    return UK_TOKEN_RE.findall(text), Counter(DIGIT_RE.findall(text))


def _sa_tokens(path: Path) -> Tuple[List[str], Counter]:
    text = "\n".join(_body_lines(path))
    return text.split(), Counter(DIGIT_RE.findall(text))


def _pct(n: int, d: int) -> float:
    return round((100.0 * n / d) if d else 100.0, 3)


def _audit(tokens: List[str], digits: Counter, layout: str, other: str) -> Dict:
    codec = UPC7Text()
    token_counts = Counter(tokens)
    covered = Counter()
    failures: Dict[Tuple[str, str], int] = Counter()
    used_codes = set()
    emitted_cells = 0
    cross_ok = 0
    cross_fail = 0
    recoverable_by_lowercase = 0

    for token, count in sorted(token_counts.items()):
        try:
            codes = codec.encode(token, layout)
        except UPC7LayoutError as exc:
            failures[(token, type(exc).__name__)] += count
            lower = token.lower()
            if lower != token:
                try:
                    codec.encode(lower, layout)
                    recoverable_by_lowercase += count
                except UPC7LayoutError:
                    pass
            continue

        covered[token] += count
        used_codes.update(codes)
        emitted_cells += len(codes) * count
        try:
            codec.render(codes, other)
            cross_ok += count
        except UPC7LayoutError:
            cross_fail += count

    sequence_occurrences: Dict[str, int] = {}
    sequence_added_cells = 0
    if layout == "uk":
        seqs = codec.layout("uk").sequences
        joined = "\n".join(tokens)
        for spelling, parts in sorted(seqs.items()):
            n = joined.count(spelling)
            sequence_occurrences[spelling] = n
            sequence_added_cells += n * (len(parts) - 1)

    failed_tokens = sum(failures.values())
    unique_failed = len({token for token, _ in failures})
    total = sum(token_counts.values())
    unique_total = len(token_counts)
    covered_total = sum(covered.values())

    failure_rows = [
        {"token": token, "count": count, "error": error}
        for (token, error), count in sorted(
            failures.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
        )
    ]

    return {
        "layout": layout,
        "other_layout": other,
        "tokens": total,
        "unique_tokens": unique_total,
        "covered_tokens": covered_total,
        "failed_tokens": failed_tokens,
        "token_coverage_percent": _pct(covered_total, total),
        "unique_covered_tokens": len(covered),
        "unique_failed_tokens": unique_failed,
        "unique_token_coverage_percent": _pct(len(covered), unique_total),
        "used_code_cells": len(used_codes),
        "used_code_bits": [f"{code:07b}" for code in sorted(used_codes)],
        "emitted_code_cells": emitted_cells,
        "case_projection_recoverable_tokens": recoverable_by_lowercase,
        "cross_layout": {
            "renderable_tokens": cross_ok,
            "unrenderable_tokens": cross_fail,
            "renderable_percent_of_covered": _pct(cross_ok, covered_total),
        },
        "digit_glyphs": {
            "total": sum(digits.values()),
            "by_glyph": {k: digits[k] for k in sorted(digits)},
        },
        "sequence_expansion": {
            "occurrences_by_spelling": sequence_occurrences,
            "added_cells": sequence_added_cells,
        },
        "failures": failure_rows,
    }


def build_report() -> Dict:
    uk_tokens, uk_digits = _uk_tokens(UK_FIXTURE)
    sa_tokens, sa_digits = _sa_tokens(SA_FIXTURE)

    provenance = json.loads(json.dumps(PROVENANCE))
    provenance["uk"]["fixture_sha256"] = _sha256(UK_FIXTURE)
    provenance["sa-slp1"]["fixture_sha256"] = _sha256(SA_FIXTURE)

    return {
        "schema": "upc7-corpus-audit-v1",
        "issue": "shiva-sutras#35",
        "policy": {
            "identity_authority": "UPC7Text encoder only",
            "unicode_role": "input fixture transport only",
            "normalization": "none",
            "case_folding": "not applied; separately counted as diagnostic recoverability",
            "failure": "fail closed; every failed token remains in inventory",
            "digits": "counted as text glyph demand; never coerced to Number",
            "corpus_authority": "evidence only; cannot assign UPC-7 identities",
        },
        "provenance": provenance,
        "uk": _audit(uk_tokens, uk_digits, "uk", "sa-slp1"),
        "sa-slp1": _audit(sa_tokens, sa_digits, "sa-slp1", "uk"),
    }


def render(report: Dict) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    current = render(build_report())
    if args.write:
        REPORT.write_text(current, encoding="utf-8")
        print(REPORT)
        return 0
    if args.check:
        if not REPORT.exists():
            print(f"missing {REPORT}")
            return 1
        if REPORT.read_text(encoding="utf-8") != current:
            print(f"{REPORT.name} is stale; run upc7_corpus_audit.py --write")
            return 1
        print(f"{REPORT.name} is current")
        return 0

    print(current, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
