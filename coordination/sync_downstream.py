#!/usr/bin/env python3
"""
sync_downstream.py — Auto-sync shiva-sutras → my-lisp-panini.

When shiva-sutras HEAD moves (new journals, claims, or reports), this script:
  1. Updates `pinned_revision` in my-lisp-panini/coordination/dependencies.yaml
  2. Updates revision in my-lisp-panini/ecosystem/imports/shiva_claims.my
  3. Commits the changes to my-lisp-panini via GitHub API

Usage:
  python sync_downstream.py --sha <SHIVA_SUTRAS_SHA> --token <GITHUB_TOKEN>

Designed to run inside GitHub Actions (shiva-sutras repo).
Requires: PyGithub (pip install PyGithub) or raw requests.
Uses raw GitHub API via requests for minimal dependencies.
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
DOWNSTREAM_BRANCH = "master"

API = "https://api.github.com"


def api_get(token, url):
    """GET with auth."""
    r = requests.get(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    })
    r.raise_for_status()
    return r


def api_put(token, url, data):
    """PUT with auth (used for content updates)."""
    r = requests.put(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }, json=data)
    r.raise_for_status()
    return r


def get_file_content(token, owner, repo, path, ref=None):
    """Fetch file content + SHA from GitHub."""
    url = f"{API}/repos/{owner}/{repo}/contents/{path}"
    params = {}
    if ref:
        params["ref"] = ref
    r = requests.get(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }, params=params)
    r.raise_for_status()
    data = r.json()
    import base64
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]


def update_file(token, owner, repo, path, new_content, message, file_sha=None, branch=None):
    """Update a file via GitHub API."""
    import base64
    # If no sha provided, fetch it
    if file_sha is None:
        _, file_sha = get_file_content(token, owner, repo, path)

    url = f"{API}/repos/{owner}/{repo}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(new_content.encode("utf-8")).decode("ascii"),
        "sha": file_sha,
    }
    if branch:
        data["branch"] = branch

    r = api_put(token, url, data)
    return r.json()


def update_dependencies_yaml(content, new_sha):
    """Update pinned_revision in dependencies.yaml."""
    # Replace pinned_revision: <old> with new SHA (short form)
    new_content = re.sub(
        r"pinned_revision:\s+[0-9a-f]+",
        f"pinned_revision: {new_sha[:7]}",
        content,
    )
    # Also handle full 40-char SHA
    new_content = re.sub(
        r"pinned_revision:\s+[0-9a-f]{40}",
        f"pinned_revision: {new_sha}",
        new_content,
    )
    return new_content


def update_shiva_claims_my(content, new_sha):
    """Update revision in shiva_claims.my."""
    short = new_sha[:7]
    # Replace (revision "xxxxxxx") with new SHA
    new_content = re.sub(
        r'\(revision "[0-9a-f]+"\)',
        f'(revision "{short}")',
        content,
    )
    # Update the revision history comment
    # Add a new line if not already present
    today_line = f';; {short} (auto-sync): pin updated by sync_downstream.py'
    if short not in new_content:
        # Find the last revision history line and add after it
        lines = new_content.split("\n")
        last_hist = -1
        for i, line in enumerate(lines):
            if line.startswith(";; ") and "(" in line and "):" in line:
                last_hist = i
        if last_hist >= 0:
            lines.insert(last_hist + 1, today_line)
            new_content = "\n".join(lines)

    return new_content


def main():
    parser = argparse.ArgumentParser(description="Sync shiva-sutras → my-lisp-panini")
    parser.add_argument("--sha", required=True, help="New shiva-sutras HEAD SHA")
    parser.add_argument("--token", required=True, help="GitHub token with repo access")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without pushing")
    args = parser.parse_args()

    new_sha = args.sha
    short = new_sha[:7]
    token = args.token

    print(f"=== sync_downstream: shiva-sutras {short} → my-lisp-panini ===\n")

    # 1. Update dependencies.yaml
    print("1. Fetching dependencies.yaml...")
    dep_content, dep_sha = get_file_content(
        token, DOWNSTREAM_OWNER, DOWNSTREAM_REPO,
        "coordination/dependencies.yaml"
    )

    new_dep = update_dependencies_yaml(dep_content, new_sha)
    dep_changed = new_dep != dep_content

    if dep_changed:
        print(f"   pinned_revision → {short}")
    else:
        print(f"   already at {short}, no change needed")

    # 2. Update shiva_claims.my
    print("2. Fetching shiva_claims.my...")
    claims_content, claims_sha = get_file_content(
        token, DOWNSTREAM_OWNER, DOWNSTREAM_REPO,
        "ecosystem/imports/shiva_claims.my"
    )

    new_claims = update_shiva_claims_my(claims_content, new_sha)
    claims_changed = new_claims != claims_content

    if claims_changed:
        print(f"   revision → {short} (all claims)")
    else:
        print(f"   already at {short}, no change needed")

    # 3. Push changes
    if not dep_changed and not claims_changed:
        print("\n✓ Everything already in sync. No commits needed.")
        return 0

    if args.dry_run:
        print("\n[dry-run] Would commit:")
        if dep_changed:
            print(f"  coordination/dependencies.yaml: pinned_revision → {short}")
        if claims_changed:
            print(f"  ecosystem/imports/shiva_claims.my: revision → {short}")
        return 0

    commit_msg = f"Auto-sync: pin shiva-sutras to {short}"

    if dep_changed:
        print(f"3. Pushing dependencies.yaml...")
        result = update_file(
            token, DOWNSTREAM_OWNER, DOWNSTREAM_REPO,
            "coordination/dependencies.yaml",
            new_dep, commit_msg, dep_sha, DOWNSTREAM_BRANCH
        )
        dep_commit = result["commit"]["sha"]
        print(f"   committed: {dep_commit[:7]}")

    if claims_changed:
        print(f"4. Pushing shiva_claims.my...")
        result = update_file(
            token, DOWNSTREAM_OWNER, DOWNSTREAM_REPO,
            "ecosystem/imports/shiva_claims.my",
            new_claims, commit_msg, claims_sha, DOWNSTREAM_BRANCH
        )
        claims_commit = result["commit"]["sha"]
        print(f"   committed: {claims_commit[:7]}")

    print(f"\n✓ Sync complete: my-lisp-panini pinned to shiva-sutras {short}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
