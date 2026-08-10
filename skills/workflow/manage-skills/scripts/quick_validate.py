#!/usr/bin/env python3
"""Validate deterministic parts of the portable skill authoring contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _skill_utils import (
    ALLOWED_FRONTMATTER,
    NAME_PATTERN,
    TOKEN_PATTERN,
    extract_frontmatter,
    parse_openai_yaml,
    validate_interface,
)

VALID_IMPACTS = {"CRITICAL", "HIGH", "MEDIUM-HIGH", "MEDIUM", "LOW-MEDIUM"}
CARD_FIELDS = {"title", "impact", "impactDescription", "tags"}
EXACT_CONDITIONAL_HEADINGS = {
    "Rule Categories by Priority",
    "Quick Reference",
    "How to Use",
}


def validate_code_fences(path: Path, content: str) -> list[str]:
    errors: list[str] = []
    opening: str | None = None
    for line in content.splitlines():
        match = re.fullmatch(r"(`{3,})(.*)", line)
        if not match:
            continue
        fence, suffix = match.groups()
        if opening is None:
            if not suffix.strip():
                errors.append(f"{path}: every code block must declare a language")
            else:
                opening = fence
        elif suffix.strip() or len(fence) != len(opening):
            errors.append(f"{path}: inconsistent code fence")
        else:
            opening = None
    if opening is not None:
        errors.append(f"{path}: code block is not closed")
    return errors


def exact_h2_headings(content: str) -> list[str]:
    return re.findall(r"^## ([^#].*)$", content, re.MULTILINE)


def validate_card(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    try:
        fields, keys = extract_frontmatter(content)
    except ValueError as error:
        return [f"{path}: {error}"]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        errors.append(f"{path}: duplicate frontmatter fields: {', '.join(duplicates)}")
    if set(keys) != CARD_FIELDS:
        errors.append(f"{path}: card frontmatter must contain exactly {', '.join(sorted(CARD_FIELDS))}")
    title = fields.get("title")
    headings = exact_h2_headings(content)
    if not isinstance(title, str) or headings != [title]:
        errors.append(f"{path}: title must exactly match the only visible H2 heading")
    if fields.get("impact") not in VALID_IMPACTS:
        errors.append(f"{path}: invalid impact")
    if not isinstance(fields.get("impactDescription"), str) or not fields["impactDescription"].strip():
        errors.append(f"{path}: impactDescription must be a non-empty string")
    raw_tags = fields.get("tags")
    tags = [tag.strip() for tag in raw_tags.split(",")] if isinstance(raw_tags, str) else []
    if not tags or any(not NAME_PATTERN.fullmatch(tag) for tag in tags):
        errors.append(f"{path}: tags must be non-empty lowercase kebab-case strings")
    if len(tags) != len(set(tags)):
        errors.append(f"{path}: tags must not be duplicated")
    for marker in ("Incorrect", "Correct"):
        if not re.search(rf"^\*\*{marker} \(.+\):\*\*$", content, re.MULTILINE):
            errors.append(f"{path}: missing exact {marker} marker with a specific description")
    reference = re.search(r"^Reference:\s*(.+)$", content, re.MULTILINE)
    if not reference:
        errors.append(f"{path}: missing exact Reference marker")
    elif not (
        re.search(r"https://[^\s)]+", reference.group(1))
        or re.search(r"\b(internal|no external|not applicable)\b", reference.group(1), re.IGNORECASE)
    ):
        errors.append(f"{path}: Reference must contain HTTPS or an explicit internal justification")
    errors.extend(validate_code_fences(path, content))
    residual = TOKEN_PATTERN.findall(content)
    if residual:
        errors.append(f"{path}: unresolved template markers: {', '.join(residual)}")
    return errors


def validate_openai_yaml(path: Path, name: str) -> list[str]:
    errors: list[str] = []
    try:
        interface, keys = parse_openai_yaml(path)
    except ValueError as error:
        return [f"{path}: {error}"]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        errors.append(f"{path}: duplicate interface fields: {', '.join(duplicates)}")
    expected = {"display_name", "short_description", "default_prompt"}
    if set(keys) != expected:
        errors.append(f"{path}: interface must contain exactly {', '.join(sorted(expected))}")
        return errors
    if any(not isinstance(interface[key], str) or not interface[key] for key in expected):
        errors.append(f"{path}: interface values must be non-empty strings")
        return errors
    try:
        validate_interface(name, interface["short_description"], interface["default_prompt"])
    except ValueError as error:
        errors.append(f"{path}: {error}")
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
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        errors.append(f"duplicate frontmatter fields: {', '.join(duplicates)}")
    unexpected = sorted(set(keys) - ALLOWED_FRONTMATTER)
    if unexpected:
        errors.append(f"unsupported frontmatter fields: {', '.join(unexpected)}")
    name = fields.get("name")
    if not isinstance(name, str) or len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append("name must be a kebab-case string of no more than 64 characters")
        name = ""
    elif skill_path.name != name:
        errors.append("name must match the skill directory")
    description = fields.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append("description must be a string containing 1 to 1024 characters")
    compatibility = fields.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not compatibility or len(compatibility) > 500
    ):
        errors.append("compatibility must be a non-empty string of no more than 500 characters")
    for optional in ("license", "allowed-tools"):
        if optional in fields and (not isinstance(fields[optional], str) or not fields[optional]):
            errors.append(f"{optional} must be a non-empty string")
    if "metadata" in fields and not isinstance(fields["metadata"], list):
        errors.append("metadata must be a mapping")
    headings = exact_h2_headings(content)
    if "When to Apply" not in headings:
        errors.append("SKILL.md must contain exact heading: When to Apply")
    for expected in EXACT_CONDITIONAL_HEADINGS:
        variants = [heading for heading in headings if heading.lower() == expected.lower()]
        if variants and variants != [expected]:
            errors.append(f"conditional heading must be exact: {expected}")
    references = skill_path / "references"
    cards = sorted(references.glob("*.md")) if references.is_dir() else []
    if references.is_dir() and not cards:
        errors.append("references/ must not be empty")
    if cards and "How to Use" not in headings:
        errors.append("How to Use is required when reference cards exist")
    for card in cards:
        errors.extend(validate_card(card))
    openai_yaml = skill_path / "agents" / "openai.yaml"
    if openai_yaml.exists():
        errors.extend(validate_openai_yaml(openai_yaml, name))
    for path in skill_path.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".txt"}:
            if "assets" in path.relative_to(skill_path).parts:
                continue
            residual = TOKEN_PATTERN.findall(path.read_text(encoding="utf-8"))
            if residual:
                errors.append(f"{path}: unresolved template markers: {', '.join(residual)}")
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
    print("Skill is deterministically valid. Complete the mandatory manual review in the contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
