#!/usr/bin/env python3
import re
import sys
from pathlib import Path

WIKI_DIR = Path("wiki")

MARKER_PATTERNS = {
    "direct":     re.compile(r"\[direct, source: [^\[\]]+\]"),
    "synthesis":  re.compile(r"\[synthesis, from: [^\[\]]+\]"),
    "assessment": re.compile(r"\[assessment\]"),
    "unverified": re.compile(r"\[unverified\]"),
}

MARKER_LOOKALIKE = re.compile(r"\[(direct|synthesis|assessment|unverified)[^\]]*\]", re.IGNORECASE)

def check_file(path):
    """Return a list of (line_number, matched_text) violations for one file."""
    violations = []
    with open(path, "r") as f:
        for line_number, line in enumerate(f, start=1):
            for match in MARKER_LOOKALIKE.finditer(line):
                matched_text = match.group(0)
                if not any(pattern.fullmatch(matched_text) for pattern in MARKER_PATTERNS.values()):
                    violations.append((line_number, matched_text))
    return violations

def main():
    all_violations = {}
    errors = {}

    for path in WIKI_DIR.rglob("*.md"):
        try:
            violations = check_file(path)
        except Exception as exc:
            errors[path] = str(exc)
            continue

        if violations:
            all_violations[path] = violations

    if errors:
        for path, error in errors.items():
            print(f"{path}: ERROR: {error}")

    if all_violations:
        for path, violations in all_violations.items():
            for line_number, matched_text in violations:
                print(f"{path}  Line {line_number}: {matched_text}")

    if errors or all_violations:
        sys.exit(1)
    else:
        print("All markers valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()