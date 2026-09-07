#!/usr/bin/env python3
"""
validate_sync.py — Check coordination consistency between shiva-sutras and my-lisp-panini.

Validates:
  1. dependencies.yaml pinned_revision exists in shiva-sutras
  2. shiva_claims.my revision matches dependencies.yaml pin
  3. All claims in shiva_claims.my exist in shiva-sutras claims-export.yaml
  4. No status elevation downstream (downstream status <= upstream status)

Exit codes:
  0 = all checks pass
  1 = drift detected (printed to stdout)
  2 = error (API failure, etc.)

Usage:
  python validate_sync.py --token <GITHUB_TOKEN>
  python validate_sync.py --token <GITHUB_TOKEN> --report json
"""

import argparse
import json
import re
import sys
import requests

SHIVA_OWNER = "juv4uk"
SHIVA_REPO = "shiva-sutras"
DOWNSTREAM_OWNER = "juv4uk"
DOWNSTREAM_REPO = "my-lisp-panini"
API = "https://api.github.com"

# Status hierarchy (lower = stronger)
STATUS_RANK = {
    "proved": 0,
    "proved-in-model": 1,
    "resolved": 2,
    "supported": 3,
    "measured": 4,
    "hypothesis": 5,
    "unresolved": 6,
    "falsified": 7,
}


def fetch_raw(owner, repo, path, ref="master"):
    """Fetch raw file content from GitHub."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def check_commit_exists(token, owner, repo, sha):
    """Check if a commit SHA exists in the repo."""
    short = sha[:7] if len(sha) >= 7 else sha
    # Try to find a commit starting with this prefix
    url = f"{API}/repos/{owner}/{repo}/commits"
    r = requests.get(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }, params={"per_page": 100})
    r.raise_for_status()
    commits = r.json()
    for c in commits:
        if c["sha"].startswith(short):
            return True, c["sha"]
    return False, None


def parse_pin_from_yaml(yaml_text):
    """Extract pinned_revision from dependencies.yaml."""
    m = re.search(r"pinned_revision:\s+([0-9a-f]+)", yaml_text)
    if m:
        return m.group(1)
    return None


def parse_revision_from_claims(claims_text):
    """Extract revision from shiva_claims.my."""
    m = re.search(r'\(revision\s+"([0-9a-f]+)"\)', claims_text)
    if m:
        return m.group(1)
    return None


def parse_claims_from_my(claims_text):
    """Extract claim IDs and statuses from shiva_claims.my."""
    claims = []
    for m in re.finditer(
        r'\(claim\s+(\S+)\s+\(revision\s+"[0-9a-f]+"\)\s+\(status\s+(\S+)\s*\)\)',
        claims_text
    ):
        claims.append({"id": m.group(1), "status": m.group(2)})
    return claims


def parse_claims_from_yaml(yaml_text):
    """Extract claim IDs and statuses from claims-export.yaml."""
    claims = []
    for m in re.finditer(
        r'###\s+(SS-\S+|L-001-\S+)\s+—',
        yaml_text
    ):
        claim_id = m.group(1)
        # Find the status line after this heading
        after = yaml_text[m.end():m.end() + 500]
        status_m = re.search(r'\*\*status\*\*:\s+`(\S+)`', after)
        if status_m:
            claims.append({"id": claim_id, "status": status_m.group(1).lower()})
    return claims


def main():
    parser = argparse.ArgumentParser(description="Validate shiva-sutras ↔ my-lisp-panini sync")
    parser.add_argument("--token", required=True, help="GitHub token")
    parser.add_argument("--report", default="text", choices=["text", "json"])
    args = parser.parse_args()

    issues = []

    try:
        # 1. Fetch dependencies.yaml
        dep_yaml = fetch_raw(DOWNSTREAM_OWNER, DOWNSTREAM_REPO, "coordination/dependencies.yaml")
        pin = parse_pin_from_yaml(dep_yaml)

        if not pin:
            issues.append("CRITICAL: Cannot parse pinned_revision from dependencies.yaml")
        else:
            print(f"Pin: {pin}")

            # 2. Check pin exists in shiva-sutras
            exists, full_sha = check_commit_exists(args.token, SHIVA_OWNER, SHIVA_REPO, pin)
            if not exists:
                issues.append(f"CRITICAL: Pin {pin} does not exist in {SHIVA_OWNER}/{SHIVA_REPO}")
            else:
                print(f"  ✓ Pin exists in shiva-sutras ({full_sha[:7]})")

        # 3. Fetch shiva_claims.my
        claims_my = fetch_raw(DOWNSTREAM_OWNER, DOWNSTREAM_REPO, "ecosystem/imports/shiva_claims.my")
        claims_rev = parse_revision_from_claims(claims_my)

        if not claims_rev:
            issues.append("CRITICAL: Cannot parse revision from shiva_claims.my")
        elif pin and claims_rev[:7] != pin[:7]:
            issues.append(f"DRIFT: shiva_claims.my revision ({claims_rev[:7]}) ≠ dependencies.yaml pin ({pin[:7]})")
        else:
            print(f"  ✓ shiva_claims.my revision matches pin ({claims_rev[:7]})")

        # 4. Fetch claims-export.yaml from shiva-sutras
        claims_yaml = fetch_raw(SHIVA_OWNER, SHIVA_REPO, "docs/claims-export.yaml")

        upstream_claims = parse_claims_from_yaml(claims_yaml)
        downstream_claims = parse_claims_from_my(claims_my)

        # 5. Check all downstream claims exist upstream
        upstream_ids = {c["id"] for c in upstream_claims}
        for dc in downstream_claims:
            if dc["id"] not in upstream_ids:
                issues.append(f"ORPHAN: Downstream claim {dc['id']} not found in upstream claims-export.yaml")

        # 6. Check no status elevation
        upstream_status = {c["id"]: c["status"] for c in upstream_claims}
        for dc in downstream_claims:
            uid = dc["id"]
            if uid in upstream_status:
                u_rank = STATUS_RANK.get(upstream_status[uid], 99)
                d_rank = STATUS_RANK.get(dc["status"], 99)
                if d_rank < u_rank:
                    issues.append(
                        f"ELEVATION: {uid} downstream={dc['status']} (rank {d_rank}) "
                        f"< upstream={upstream_status[uid]} (rank {u_rank})"
                    )

        # 7. Check shiva-sutras HEAD vs pin (drift report)
        r = requests.get(f"{API}/repos/{SHIVA_OWNER}/{SHIVA_REPO}/commits", headers={
            "Authorization": f"token {args.token}",
        }, params={"per_page": 1})
        if r.ok:
            head_sha = r.json()[0]["sha"]
            if pin and head_sha[:7] != pin[:7]:
                issues.append(f"HEAD_DRIFT: shiva-sutras HEAD is {head_sha[:7]}, pin is {pin[:7]} (drift of unknown commits)")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    # Report
    if args.report == "json":
        print(json.dumps({"issues": issues, "count": len(issues)}))
    else:
        if issues:
            print(f"\n{'='*60}")
            print(f"⚠ {len(issues)} issue(s) found:\n")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
            print(f"\n{'='*60}")
        else:
            print(f"\n✓ All checks pass. Repos are in sync.")

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
