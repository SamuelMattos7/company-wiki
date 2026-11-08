#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile(r"\[(?:direct|synthesis|assessment|unverified)\b[^\]\n]*(?:\]|$)", re.I)
SOURCED = re.compile(r"\[(direct, source|synthesis, from): ([^\[\]]+)\]")
STANDALONE = {"[assessment]", "[unverified]"}


def check_file(path, root=ROOT):
    violations = []
    raw = (root / "raw").resolve()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for marker in MARKER.findall(line):
            if marker in STANDALONE:
                continue
            match = SOURCED.fullmatch(marker)
            if not match or not match[2].strip() or match[2] != match[2].strip():
                violations.append((number, f"malformed marker: {marker}"))
                continue
            references = [part.strip() for part in match[2].split(",")]
            if match[1] == "direct, source" and len(references) != 1:
                violations.append((number, "direct marker requires exactly one source"))
                continue
            for reference in references:
                parts = reference.split("/")
                if (parts[0] != "raw" or len(parts) < 2
                        or any(part in {"", ".", ".."} for part in parts)
                        or re.search(r'[\\:*?"<>|\x00-\x1f]', reference)):
                    violations.append((number, f"invalid source path: {reference!r} (expected raw/...)"))
                    continue
                candidate = root.joinpath(*parts)
                if not candidate.resolve().is_relative_to(raw) or not candidate.is_file():
                    violations.append((number, f"source is not an existing file under raw/: {reference}"))
    return violations


def main():
    parser = argparse.ArgumentParser(description="Check wiki marker syntax and local source paths.")
    parser.add_argument("paths", type=Path, nargs="*", help="Markdown files to check (default: wiki/)")
    args = parser.parse_args()
    paths = args.paths or sorted((ROOT / "wiki").rglob("*.md"))
    if not paths:
        parser.exit(1, "No Markdown files found under wiki/.\n")
    failed = False
    for path in paths:
        try:
            for line, message in check_file(path):
                print(f"{path}:{line}: {message}")
                failed = True
        except (OSError, ValueError, RuntimeError) as error:
            print(f"{path}: cannot validate: {error}")
            failed = True
    if not failed:
        print(f"Markers and source paths valid in {len(paths)} file(s).")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
