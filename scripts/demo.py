#!/usr/bin/env python3
import argparse
import tomllib

from lint_markers import ROOT, check_file


def main():
    profiles = sorted(path.stem for path in (ROOT / "profiles").glob("*.toml"))
    parser = argparse.ArgumentParser(description="Validate and display a prepared research example.")
    parser.add_argument("--profile", choices=profiles, default="semiconductors")
    args = parser.parse_args()

    with (ROOT / "profiles" / f"{args.profile}.toml").open("rb") as file:
        profile = tomllib.load(file)
    if profile["schema_version"] != 1:
        parser.exit(1, "Unsupported profile schema version.\n")

    demo = profile["demo"]
    try:
        pages = [ROOT / demo[key] for key in ("company", "quarter", "answer")]
        paths = [ROOT / demo["source"], *pages]
        contents = [path.read_text(encoding="utf-8") for path in paths]
        violations = [
            f"{path.relative_to(ROOT)}:{line}: {message}"
            for path in pages
            for line, message in check_file(path)
        ]
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Cannot read demo: {error}\n")
    if violations:
        parser.exit(1, "\n".join(violations) + "\n")

    print(f"Prepared synthetic example | {profile['name']}")
    for path, content in zip(paths, contents):
        print(f"\n--- {path.relative_to(ROOT).as_posix()} ---\n{content.rstrip()}")


if __name__ == "__main__":
    main()
