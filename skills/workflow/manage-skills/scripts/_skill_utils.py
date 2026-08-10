#!/usr/bin/env python3
"""Shared standard-library helpers for the portable manage-skills package."""

from __future__ import annotations

import ast
import json
import os
import re
import tempfile
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOKEN_PATTERN = re.compile(
    r"\{\{[A-Z][A-Z0-9_]*\}\}|__MANAGE_SKILLS_[A-Z0-9_]+__|"
    r"\*\*MANAGE_SKILLS_[A-Z0-9_]+\*\*|\[TODO(?::[^\]]*)?\]"
)
ALLOWED_FRONTMATTER = {
    "name", "description", "license", "allowed-tools", "metadata", "compatibility"
}
BLOCK_SCALAR_PATTERN = re.compile(r"[|>](?:[+-][1-9]?|[1-9][+-]?)?")


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
    expected = set(re.findall(r"\{\{([A-Z][A-Z0-9_]*)\}\}", content))
    missing = expected - values.keys()
    extra = values.keys() - expected
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing values: {', '.join(sorted(missing))}")
        if extra:
            details.append(f"unknown values: {', '.join(sorted(extra))}")
        raise ValueError("template value mismatch: " + "; ".join(details))
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    residual = TOKEN_PATTERN.findall(content)
    if residual:
        raise ValueError(f"unresolved template markers: {', '.join(residual)}")
    return content


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_openai_yaml(
    skill_path: Path,
    display_name: str,
    short_description: str,
    default_prompt: str,
    skill_name: str | None = None,
) -> Path:
    name = skill_name or skill_path.name
    validate_name(name)
    validate_interface(name, short_description, default_prompt)
    output = skill_path / "agents" / "openai.yaml"
    atomic_write(
        output,
        "interface:\n"
        f"  display_name: {quote_yaml(display_name)}\n"
        f"  short_description: {quote_yaml(short_description)}\n"
        f"  default_prompt: {quote_yaml(default_prompt)}\n",
    )
    return output


def extract_frontmatter(content: str) -> tuple[dict[str, object], list[str]]:
    if not content.startswith("---\n"):
        raise ValueError("document must start with YAML frontmatter")
    end = content.find("\n---", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    lines = content[4:end].splitlines()
    fields: dict[str, object] = {}
    keys: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line[0].isspace():
            index += 1
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9-]*):(?:\s*(.*))?", line)
        if not match:
            raise ValueError(f"invalid top-level frontmatter line: {line}")
        key, raw = match.group(1), (match.group(2) or "").strip()
        keys.append(key)
        continuation = index + 1 < len(lines) and bool(lines[index + 1][:1].isspace())
        if BLOCK_SCALAR_PATTERN.fullmatch(raw) or (not raw and continuation):
            nested: list[str] = []
            index += 1
            while index < len(lines) and (not lines[index] or lines[index][0].isspace()):
                if lines[index].strip():
                    nested.append(lines[index].strip())
                index += 1
            fields[key] = " ".join(nested) if BLOCK_SCALAR_PATTERN.fullmatch(raw) else nested
            continue
        fields[key] = parse_scalar(raw)
        index += 1
    return fields, keys


def parse_scalar(value: str) -> object:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == "'":
            return value[1:-1].replace("''", "'")
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if value in {"true", "false", "null", "~"}:
        return {"true": True, "false": False, "null": None, "~": None}[value]
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", value):
        return float(value) if "." in value else int(value)
    return value


def parse_openai_yaml(path: Path) -> tuple[dict[str, object], list[str]]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0] != "interface:":
        raise ValueError("top-level interface mapping is required")
    values: dict[str, object] = {}
    keys: list[str] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        match = re.fullmatch(r"  ([a-z_]+):\s*(.+)", line)
        if not match:
            raise ValueError(f"invalid interface line: {line}")
        key = match.group(1)
        keys.append(key)
        values[key] = parse_scalar(match.group(2).strip())
    return values, keys
