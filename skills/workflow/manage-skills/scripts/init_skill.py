#!/usr/bin/env python3
"""Initialize a portable skill package from bundled templates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _skill_utils import quote_yaml, render_template, validate_interface, validate_name, write_openai_yaml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--path", required=True, type=Path, help="Existing parent directory")
    parser.add_argument("--description", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--short-description", required=True)
    parser.add_argument("--default-prompt", required=True)
    parser.add_argument("--overview", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        validate_name(args.name)
        validate_interface(args.name, args.short_description, args.default_prompt)
        if not args.path.is_dir():
            raise ValueError(f"parent directory does not exist: {args.path}")
        destination = args.path / args.name
        if destination.exists():
            raise ValueError(f"destination already exists: {destination}")
        skill_content = render_template(
            "skill-template.md",
            {
                "NAME": args.name,
                "DESCRIPTION": quote_yaml(args.description),
                "DISPLAY_NAME": args.display_name,
                "OVERVIEW": args.overview,
            },
        )
        destination.mkdir()
        (destination / "SKILL.md").write_text(skill_content, encoding="utf-8")
        write_openai_yaml(
            destination,
            args.display_name,
            args.short_description,
            args.default_prompt,
        )
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Initialized skill: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
