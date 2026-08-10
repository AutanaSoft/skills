#!/usr/bin/env python3
"""Initialize a skill atomically from the bundled canonical skeleton."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

from _skill_utils import render_template, validate_interface, validate_name, write_openai_yaml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--path", required=True, type=Path, help="Existing parent directory")
    parser.add_argument("--description", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--overview", required=True)
    parser.add_argument("--trigger", action="append", required=True)
    parser.add_argument("--license")
    parser.add_argument("--allowed-tools")
    parser.add_argument("--author")
    parser.add_argument("--version")
    parser.add_argument("--compatibility")
    parser.add_argument("--categories", action="store_true")
    parser.add_argument("--references", action="store_true")
    parser.add_argument("--openai-metadata", action="store_true")
    parser.add_argument("--display-name")
    parser.add_argument("--short-description")
    parser.add_argument("--default-prompt")
    return parser


def remove_conditional(content: str, marker: str, keep: bool) -> str:
    if marker in {"LICENSE", "ALLOWED_TOOLS", "METADATA", "COMPATIBILITY"}:
        start = f"# MANAGE_SKILLS_{marker}_BEGIN"
        end = f"# MANAGE_SKILLS_{marker}_END"
    else:
        start = f"<!-- MANAGE_SKILLS_{marker}_BEGIN -->"
        end = f"<!-- MANAGE_SKILLS_{marker}_END -->"
    pattern = re.compile(rf"{re.escape(start)}\n(.*?){re.escape(end)}\n?", re.DOTALL)
    match = pattern.search(content)
    if not match:
        raise ValueError(f"missing conditional template markers for {marker}")
    return pattern.sub(match.group(1) if keep else "", content)


def main() -> int:
    args = build_parser().parse_args()
    destination = args.path / args.name
    staging: Path | None = None
    try:
        validate_name(args.name)
        if not args.path.is_dir():
            raise ValueError(f"parent directory does not exist: {args.path}")
        if destination.exists():
            raise ValueError(f"destination already exists: {destination}")
        if len(args.trigger) != 2 or any(not value.strip() for value in args.trigger):
            raise ValueError("exactly two non-empty --trigger values are required")
        metadata_values = (args.display_name, args.short_description, args.default_prompt)
        if args.openai_metadata:
            if any(value is None for value in metadata_values):
                raise ValueError("--openai-metadata requires all three interface fields")
            validate_interface(args.name, args.short_description, args.default_prompt)
        elif any(value is not None for value in metadata_values):
            raise ValueError("interface fields require --openai-metadata")
        skill_content = render_template(
            "skill-template.md",
            {
                "SKILL_NAME": args.name,
                "DESCRIPTION": args.description.replace("'", "''"),
                "LICENSE": (args.license or "not-applicable").replace("'", "''"),
                "ALLOWED_TOOLS": (args.allowed_tools or "not-applicable").replace("'", "''"),
                "AUTHOR": (args.author or "not-applicable").replace("'", "''"),
                "VERSION": (args.version or "not-applicable").replace("'", "''"),
                "COMPATIBILITY": (args.compatibility or "not-applicable").replace("'", "''"),
                "SKILL_TITLE": args.title,
                "OVERVIEW": args.overview,
                "TRIGGER_1": args.trigger[0],
                "TRIGGER_2": args.trigger[1],
                "CATEGORY_1": "Category 1",
                "CATEGORY_2": "Category 2",
                "PREFIX_1": "category-one",
                "PREFIX_2": "category-two",
                "SLUG_1": "first-rule",
                "SLUG_2": "second-rule",
                "SLUG_3": "third-rule",
                "SLUG_4": "fourth-rule",
                "RULE_DESCRIPTION_1": "First rule or decision description",
                "RULE_DESCRIPTION_2": "Second rule or decision description",
                "RULE_DESCRIPTION_3": "Third rule or decision description",
                "RULE_DESCRIPTION_4": "Fourth rule or decision description",
            },
        )
        skill_content = remove_conditional(skill_content, "LICENSE", bool(args.license))
        skill_content = remove_conditional(skill_content, "ALLOWED_TOOLS", bool(args.allowed_tools))
        skill_content = remove_conditional(skill_content, "METADATA", bool(args.author or args.version))
        skill_content = remove_conditional(skill_content, "COMPATIBILITY", bool(args.compatibility))
        if args.author is None and args.version is not None:
            skill_content = re.sub(r"^  author:.*\n", "", skill_content, flags=re.MULTILINE)
        if args.version is None and args.author is not None:
            skill_content = re.sub(r"^  version:.*\n", "", skill_content, flags=re.MULTILINE)
        skill_content = remove_conditional(skill_content, "CATEGORIES", args.categories)
        skill_content = remove_conditional(skill_content, "REFERENCES", args.references)
        staging = Path(tempfile.mkdtemp(prefix=f".{args.name}.", dir=args.path))
        (staging / "SKILL.md").write_text(skill_content, encoding="utf-8", newline="\n")
        if args.openai_metadata:
            write_openai_yaml(staging, *metadata_values, skill_name=args.name)
        staging.replace(destination)
    except (OSError, ValueError) as error:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Initialized skill: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
