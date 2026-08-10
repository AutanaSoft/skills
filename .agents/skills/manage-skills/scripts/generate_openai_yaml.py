#!/usr/bin/env python3
"""Generate or update agents/openai.yaml without changing other skill files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _skill_utils import write_openai_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--short-description", required=True)
    parser.add_argument("--default-prompt", required=True)
    args = parser.parse_args()
    try:
        if not (args.skill_path / "SKILL.md").is_file():
            raise ValueError(f"SKILL.md not found in {args.skill_path}")
        output = write_openai_yaml(
            args.skill_path,
            args.display_name,
            args.short_description,
            args.default_prompt,
        )
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Updated metadata: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
