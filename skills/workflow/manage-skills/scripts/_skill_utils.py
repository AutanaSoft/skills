#!/usr/bin/env python3
"""Shared portable helpers for manage-skills scripts."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEMPLATE_TOKEN_PATTERN = re.compile(r"__MANAGE_SKILLS_[A-Z][A-Z0-9_]*__|\[TODO(?::[^\]]*)?\]")
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def quote_yaml(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def validate_name(name: str) -> None:
    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        raise ValueError("name must be kebab-case and no more than 64 characters")


def validate_interface(name: str, short_description: str, default_prompt: str) -> None:
    if not 25 <= len(short_description) <= 64:
        raise ValueError("short_description must contain 25 to 64 characters")
    if f"${name}" not in default_prompt:
        raise ValueError(f"default_prompt must mention ${name}")


def render_template(template_name: str, values: dict[str, str]) -> str:
    content = (skill_root() / "assets" / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("__MANAGE_SKILLS_" + key + "__", value)
    unresolved = TEMPLATE_TOKEN_PATTERN.findall(content)
    if unresolved:
        raise ValueError(f"unresolved template tokens: {', '.join(unresolved)}")
    return content


def write_openai_yaml(
    skill_path: Path,
    display_name: str,
    short_description: str,
    default_prompt: str,
) -> Path:
    name = skill_path.name
    validate_name(name)
    validate_interface(name, short_description, default_prompt)
    agents_path = skill_path / "agents"
    agents_path.mkdir(exist_ok=True)
    output = agents_path / "openai.yaml"
    output.write_text(
        "interface:\n"
        f"  display_name: {quote_yaml(display_name)}\n"
        f"  short_description: {quote_yaml(short_description)}\n"
        f"  default_prompt: {quote_yaml(default_prompt)}\n",
        encoding="utf-8",
    )
    return output


def extract_frontmatter(content: str) -> tuple[dict[str, str], list[str]]:
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = content.find("\n---", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    lines = content[4:end].splitlines()
    fields: dict[str, str] = {}
    top_level: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line[0].isspace():
            index += 1
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9-]*):(?:\s*(.*))?", line)
        if not match:
            raise ValueError(f"invalid top-level frontmatter line: {line}")
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        top_level.append(key)
        if raw_value in {">", ">-", "|", "|-"}:
            parts: list[str] = []
            index += 1
            while index < len(lines) and (not lines[index] or lines[index][0].isspace()):
                if lines[index].strip():
                    parts.append(lines[index].strip())
                index += 1
            fields[key] = " ".join(parts)
            continue
        fields[key] = parse_scalar(raw_value)
        index += 1
    return fields, top_level


def parse_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, str) else value
        except (SyntaxError, ValueError):
            return value[1:-1]
    return value


def parse_openai_yaml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"\s{2}(display_name|short_description|default_prompt):\s*(.+)", line)
        if match:
            values[match.group(1)] = parse_scalar(match.group(2).strip())
    return values
