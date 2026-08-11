#!/usr/bin/env uv run python3
"""Update all gardening plugin manifests to a semantic version."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION_PATTERN = re.compile(r'("version"\s*:\s*")[^"]+(\")')
MANIFESTS = (
    (Path(".github/plugin/marketplace.json"), 2),
    (Path("plugins/gardening/.github/plugin/plugin.json"), 1),
)


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        print("version must use the X.Y.Z format", file=sys.stderr)
        return 1

    version = sys.argv[1]
    root = Path(__file__).resolve().parent.parent
    replacements: list[tuple[Path, str]] = []
    failed = False

    for relative_path, expected_count in MANIFESTS:
        path = root / relative_path
        if not path.is_file():
            print(f"Missing version manifest: {relative_path}", file=sys.stderr)
            failed = True
            continue

        content = path.read_text(encoding="utf-8")
        matches = VERSION_PATTERN.findall(content)
        if len(matches) != expected_count:
            print(
                f"Expected {expected_count} version fields in {relative_path}, "
                f"found {len(matches)}",
                file=sys.stderr,
            )
            failed = True
            continue

        updated = VERSION_PATTERN.sub(rf"\g<1>{version}\g<2>", content)
        try:
            json.loads(updated)
        except json.JSONDecodeError as error:
            print(f"Updated {relative_path} is not valid JSON: {error}", file=sys.stderr)
            failed = True
            continue

        replacements.append((path, updated))

    if failed:
        return 1

    for path, content in replacements:
        path.write_text(content, encoding="utf-8")

    print(f"Updated gardening plugin manifests to version {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
