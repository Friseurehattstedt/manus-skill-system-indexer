#!/usr/bin/env python3
"""Fail if the public bootstrap contains a private graph projection."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_PATHS = {
    "references/graph.json",
    "references/GRAPH_REPORT.md",
    "scripts/build_graph.py",
}
REQUIRED_PATHS = {
    ".gitattributes",
    "README.md",
    "SKILL.md",
    "references/BOOTSTRAP_CONTRACT.md",
    "scripts/verify_bootstrap.py",
}
PRIVATE_MARKERS = (
    '"nodes": [',
    '"links": [',
    "connector:",
    "secret:",
    "system:brain",
    "venture:salon",
)


def main() -> int:
    errors: list[str] = []
    present = {str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file()}
    for path in sorted(FORBIDDEN_PATHS & present):
        errors.append(f"forbidden private projection: {path}")
    for path in sorted(REQUIRED_PATHS - present):
        errors.append(f"required bootstrap file missing: {path}")

    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8") if (ROOT / ".gitattributes").exists() else ""
    for path in sorted(FORBIDDEN_PATHS):
        if f"{path} -diff" not in attributes:
            errors.append(f"public diff guard missing for {path}")

    for relative in sorted(present):
        if relative.startswith(".git/") or relative == "scripts/verify_bootstrap.py":
            continue
        path = ROOT / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in PRIVATE_MARKERS:
            if marker in text:
                errors.append(f"private graph marker {marker!r} in {relative}")

    if errors:
        print(f"PUBLIC BOOTSTRAP INVALID ({len(errors)} errors)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PUBLIC BOOTSTRAP VALID: no private graph projection")
    return 0


if __name__ == "__main__":
    sys.exit(main())
