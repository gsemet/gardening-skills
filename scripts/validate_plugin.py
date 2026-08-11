#!/usr/bin/env uv run python3
"""Validate the standalone gardening plugin using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read_json(relative_path: str) -> Any | None:
    path = ROOT / relative_path
    if not path.is_file():
        fail(f"Missing JSON file: {relative_path}")
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"Malformed JSON in {relative_path}: {error}")
        return None


def is_object(value: Any) -> bool:
    return isinstance(value, dict)


def require_string(value: Any, field: str, location: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{location}.{field} must be a non-empty string")


def require_array(value: Any, field: str, location: str) -> None:
    if not isinstance(value, list):
        fail(f"{location}.{field} must be an array")


def list_markdown_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.rglob("*.md") if path.is_file())


def parse_frontmatter(content: str, relative_path: str) -> str:
    if not content.startswith("---\n"):
        fail(f"{relative_path} must start with YAML frontmatter")
        return ""

    end = content.find("\n---", 4)
    if end == -1:
        fail(f"{relative_path} has unterminated YAML frontmatter")
        return ""

    return content[4:end]


def validate_skill(skill_directory: Path, expected_name: str) -> None:
    relative_directory = skill_directory.relative_to(ROOT)
    skill_path = skill_directory / "SKILL.md"
    relative_skill_path = relative_directory / "SKILL.md"
    if not skill_path.is_file():
        fail(f"Skill directory {relative_directory} is missing SKILL.md")
        return

    content = skill_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content, str(relative_skill_path))
    name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    description_match = re.search(r"^description:\s*(.*)$", frontmatter, re.MULTILINE)

    if not name_match or not name_match.group(1).strip():
        fail(f"{relative_skill_path} frontmatter needs a non-empty name")
    elif name_match.group(1).strip() != expected_name:
        fail(
            f"{relative_skill_path} frontmatter name must be {expected_name}, "
            f"found {name_match.group(1).strip()}"
        )

    if not description_match or not description_match.group(1).strip():
        fail(f"{relative_skill_path} frontmatter needs a non-empty description")

    private_metadata = (
        re.compile(r"ampere", re.IGNORECASE),
        re.compile(r"ampere\.cars", re.IGNORECASE),
        re.compile(r"renault\s+proprietary", re.IGNORECASE),
        re.compile(r"^\s*skill-id\s*:", re.IGNORECASE | re.MULTILINE),
        re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
            r"[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
    )
    for pattern in private_metadata:
        if pattern.search(frontmatter):
            fail(f"{relative_directory}/SKILL.md frontmatter contains private source metadata ({pattern.pattern})")


def strip_fenced_code_blocks(content: str) -> str:
    visible_lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in content.splitlines():
        fence_match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            continue

        if fence_character is None:
            visible_lines.append(line)

    return "\n".join(visible_lines)


def validate_local_markdown_links(plugin_directory: Path) -> None:
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for markdown_path in list_markdown_files(plugin_directory):
        relative_path = markdown_path.relative_to(ROOT)
        content = strip_fenced_code_blocks(markdown_path.read_text(encoding="utf-8"))

        for match in link_pattern.finditer(content):
            raw_target = match.group(1).strip().strip("<>")
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", raw_target, re.IGNORECASE):
                continue

            target_without_fragment = re.split(r"[?#]", raw_target, maxsplit=1)[0]
            if not target_without_fragment:
                continue

            target_path = (markdown_path.parent / target_without_fragment).resolve()
            if not target_path.exists():
                fail(f"Broken local Markdown link in {relative_path}: {raw_target}")


def main() -> int:
    marketplace = read_json(".github/plugin/marketplace.json")
    plugin = read_json("plugins/gardening/.github/plugin/plugin.json")

    if isinstance(marketplace, dict):
        require_string(marketplace.get("name"), "name", "marketplace")
        metadata = marketplace.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        require_string(metadata.get("version"), "metadata.version", "marketplace")
        require_string(metadata.get("pluginRoot"), "metadata.pluginRoot", "marketplace")
        require_array(marketplace.get("plugins"), "plugins", "marketplace")

    if isinstance(plugin, dict):
        plugin_location = "plugin"
        require_string(plugin.get("name"), "name", plugin_location)
        require_string(plugin.get("description"), "description", plugin_location)
        require_string(plugin.get("version"), "version", plugin_location)
        require_string(plugin.get("license"), "license", plugin_location)
        require_array(plugin.get("skills"), "skills", plugin_location)
        require_array(plugin.get("agents"), "agents", plugin_location)
        require_array(plugin.get("commands"), "commands", plugin_location)
        require_array(plugin.get("hooks"), "hooks", plugin_location)

        author = plugin.get("author")
        if is_object(author):
            require_string(author.get("name"), "author.name", plugin_location)
            require_string(author.get("email"), "author.email", plugin_location)
        else:
            fail("plugin.author must be an object")

        if isinstance(marketplace, dict) and marketplace.get("name") != plugin.get("name"):
            fail(f"marketplace.name ({marketplace.get('name')}) does not match plugin.name ({plugin.get('name')})")

        metadata = marketplace.get("metadata") if isinstance(marketplace, dict) else None
        marketplace_version = metadata.get("version") if isinstance(metadata, dict) else None
        if marketplace_version != plugin.get("version"):
            fail(
                f"marketplace.metadata.version ({marketplace_version}) does not match "
                f"plugin.version ({plugin.get('version')})"
            )

        marketplace_plugins = marketplace.get("plugins", []) if isinstance(marketplace, dict) else []
        marketplace_entry = next(
            (entry for entry in marketplace_plugins if isinstance(entry, dict) and entry.get("name") == plugin.get("name")),
            None,
        )
        if marketplace_entry is None:
            fail(f"marketplace.plugins must contain an entry named {plugin.get('name')}")
        elif marketplace_entry.get("version") != plugin.get("version"):
            fail(f"marketplace plugin entry version must match {plugin.get('version')}")

        plugin_directory = ROOT / "plugins" / str(plugin.get("name", ""))
        if not plugin_directory.is_dir():
            fail(f"Plugin directory does not exist: plugins/{plugin.get('name')}")
        else:
            skill_root = plugin_directory / "skills"
            skill_directories = sorted(path for path in skill_root.iterdir() if path.is_dir()) if skill_root.is_dir() else []
            for skill_directory in skill_directories:
                validate_skill(skill_directory, skill_directory.name)

            for skill_reference in plugin.get("skills", []):
                if not isinstance(skill_reference, str):
                    fail("Every plugin.skills entry must be a relative path string")
                    continue

                skill_path = (plugin_directory / skill_reference).resolve()
                try:
                    skill_path.relative_to(plugin_directory.resolve())
                except ValueError:
                    fail(f"Plugin skill path does not exist inside the plugin: {skill_reference}")
                    continue

                if not skill_path.exists():
                    fail(f"Plugin skill path does not exist inside the plugin: {skill_reference}")
                    continue
                if not skill_path.is_dir():
                    fail(f"Plugin skill path is not a directory: {skill_reference}")
                    continue
                if not (skill_path / "SKILL.md").is_file():
                    fail(f"Plugin skill path is missing SKILL.md: {skill_reference}")

            validate_local_markdown_links(plugin_directory)

    readme_path = ROOT / "README.md"
    if not readme_path.is_file():
        fail("README.md is required")
    else:
        readme = readme_path.read_text(encoding="utf-8")
        for heading in (
            "## Installation",
            "## Usage",
            "## Included Skills",
            "## Compatibility and Tool Boundaries",
            "## Mutation Safety",
            "## Repository Layout",
            "## Validation",
            "## Release and Versioning",
            "## Contributing",
        ):
            if heading not in readme:
                fail(f"README.md is missing required heading: {heading}")

    if ERRORS:
        print(f"Plugin validation failed with {len(ERRORS)} error(s):", file=sys.stderr)
        for error in ERRORS:
            print(f"- {error}", file=sys.stderr)
        return 1

    version = plugin.get("version", "unknown") if isinstance(plugin, dict) else "unknown"
    print(f"Plugin validation passed: gardening {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
