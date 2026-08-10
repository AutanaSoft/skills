#!/usr/bin/env python3
"""Validate a skill using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _skill_utils import (
    ALLOWED_FRONTMATTER,
    NAME_PATTERN,
    TEMPLATE_TOKEN_PATTERN,
    extract_frontmatter,
    parse_openai_yaml,
    validate_interface,
)

VALID_IMPACTS = {"CRITICAL", "HIGH", "MEDIUM-HIGH", "MEDIUM", "LOW-MEDIUM"}


def validate_card(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    try:
        fields, _ = extract_frontmatter(content)
    except ValueError as error:
        return [f"{path}: {error}"]
    title = fields.get("title", "")
    if not title or f"## {title}" not in content:
        errors.append(f"{path}: title must match the visible H2 heading")
    if fields.get("impact") not in VALID_IMPACTS:
        errors.append(f"{path}: invalid impact")
    if not fields.get("impactDescription"):
        errors.append(f"{path}: impactDescription is required")
    tags = [tag.strip() for tag in fields.get("tags", "").split(",") if tag.strip()]
    if not tags or any(not NAME_PATTERN.fullmatch(tag) for tag in tags):
        errors.append(f"{path}: tags must be lowercase kebab-case")
    for marker in ("**Incorrect (", "**Correct (", "Reference:"):
        if marker not in content:
            errors.append(f"{path}: missing {marker.rstrip(' (')}")
    if re.search(r"^```\s*$", content, re.MULTILINE):
        errors.append(f"{path}: every code block must declare a language")
    return errors


def validate_skill(skill_path: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md not found"]
    content = skill_md.read_text(encoding="utf-8")
    try:
        fields, keys = extract_frontmatter(content)
    except ValueError as error:
        return [str(error)]
    unexpected = sorted(set(keys) - ALLOWED_FRONTMATTER)
    if unexpected:
        errors.append(f"unsupported frontmatter fields: {', '.join(unexpected)}")
    name = fields.get("name", "")
    if not name or len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append("name must be kebab-case and no more than 64 characters")
    elif skill_path.name != name:
        errors.append("name must match the skill directory")
    description = fields.get("description", "")
    if not description or len(description) > 1024:
        errors.append("description must contain 1 to 1024 characters")
    compatibility = fields.get("compatibility", "")
    if len(compatibility) > 500:
        errors.append("compatibility must not exceed 500 characters")
    unresolved = TEMPLATE_TOKEN_PATTERN.findall(content)
    if unresolved:
        errors.append(f"SKILL.md contains unresolved template tokens: {', '.join(unresolved)}")

    openai_yaml = skill_path / "agents" / "openai.yaml"
    if openai_yaml.exists():
        interface = parse_openai_yaml(openai_yaml)
        missing = {"display_name", "short_description", "default_prompt"} - interface.keys()
        if missing:
            errors.append(f"agents/openai.yaml missing fields: {', '.join(sorted(missing))}")
        elif name:
            try:
                validate_interface(name, interface["short_description"], interface["default_prompt"])
            except ValueError as error:
                errors.append(f"agents/openai.yaml: {error}")

    references = skill_path / "references"
    if references.is_dir():
        for card in sorted(references.glob("*.md")):
            if card.read_text(encoding="utf-8").startswith("---\n"):
                errors.extend(validate_card(card))
    for path in skill_path.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            if "assets" in path.relative_to(skill_path).parts:
                continue
            tokens = TEMPLATE_TOKEN_PATTERN.findall(path.read_text(encoding="utf-8"))
            if tokens:
                errors.append(f"{path}: unresolved template tokens: {', '.join(tokens)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_skill(args.skill_path.resolve())
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
