from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


class ManageSkillsScriptsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.temp_path = Path(self.temporary_directory.name)
        self.repository_root = Path(__file__).resolve().parents[3]
        source = self.repository_root / "skills" / "workflow" / "manage-skills"
        self.standalone_root = self.temp_path / "installed" / "manage-skills"
        shutil.copytree(source, self.standalone_root)
        self.destination = self.temp_path / "target"
        self.destination.mkdir()
        scripts_path = self.standalone_root / "scripts"
        sys.path.insert(0, str(scripts_path))
        self.addCleanup(lambda: sys.path.remove(str(scripts_path)))
        sys.modules.pop("_skill_utils", None)
        self.addCleanup(lambda: sys.modules.pop("_skill_utils", None))
        spec = importlib.util.spec_from_file_location(
            "portable_quick_validate", scripts_path / "quick_validate.py"
        )
        assert spec and spec.loader
        self.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.validator)

    def run_script(self, name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.standalone_root / "scripts" / name), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def init_arguments(self, name: str = "review-changes") -> list[str]:
        return [
            name,
            "--path",
            str(self.destination),
            "--description",
            "Review code changes. Use for focused code review requests.",
            "--title",
            "Review Changes",
            "--overview",
            "Review code changes and report evidence-backed findings.",
            "--trigger",
            "Reviewing a pull request",
            "--trigger",
            "Inspecting a repository diff",
        ]

    def initialize(self, *extra: str, name: str = "review-changes") -> Path:
        result = self.run_script("init_skill.py", *self.init_arguments(name), *extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.destination / name

    def normalize_skeleton(self, content: str, asset: bool = False) -> list[str]:
        if asset:
            content = re.sub(
                r"<!-- MANAGE_SKILLS_SUPPORTING_SECTIONS_BEGIN -->.*?"
                r"<!-- MANAGE_SKILLS_SUPPORTING_SECTIONS_END -->\n?",
                "",
                content,
                flags=re.DOTALL,
            )
            content = re.sub(r"^# MANAGE_SKILLS_[A-Z_]+$", "", content, flags=re.MULTILINE)
            content = re.sub(r"<!-- MANAGE_SKILLS_[A-Z_]+ -->", "", content)
            content = re.sub(
                r"^(?:allowed-tools|compatibility):.*$", "", content, flags=re.MULTILINE
            )
        content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        content = re.sub(r"\{\{[A-Z][A-Z0-9_]*\}\}", "<value>", content)
        content = re.sub(r"<[^>\n]+>", "<value>", content)
        content = re.sub(r"https://[^)\s]+", "https://<value>", content)
        content = content.replace("'<value>'", "<value>")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        normalized = [re.sub(r"\s*\|\s*", "|", line) if line.startswith("|") else line for line in lines]
        return [re.sub(r"-+", "---", line) if re.fullmatch(r"\|[-|]+\|", line) else line for line in normalized]

    def canonical_skeleton(self, name: str) -> str:
        path = self.repository_root / "docs" / "skill-development" / name
        content = path.read_text(encoding="utf-8")
        return content.split("````markdown\n", 1)[1].rsplit("\n````", 1)[0]

    def test_assets_are_normalized_structural_transpositions(self) -> None:
        skill_asset = (self.standalone_root / "assets" / "skill-template.md").read_text(
            encoding="utf-8"
        )
        card_asset = (self.standalone_root / "assets" / "reference-card-template.md").read_text(
            encoding="utf-8"
        )
        canonical_skill = self.canonical_skeleton("skill-template.md")
        canonical_card = self.canonical_skeleton("reference-card-template.md")
        skill_lines = self.normalize_skeleton(skill_asset, asset=True)
        canonical_skill_lines = self.normalize_skeleton(canonical_skill)
        self.assertEqual(skill_lines, canonical_skill_lines)
        card_lines = self.normalize_skeleton(card_asset, asset=True)
        self.assertEqual(card_lines, self.normalize_skeleton(canonical_card))
        for heading in (
            "## When to Apply",
            "## Rule Categories by Priority",
            "## Quick Reference",
            "## How to Use",
        ):
            self.assertEqual(skill_asset.count(heading), canonical_skill.count(heading))
        for marker in ("title:", "impact:", "impactDescription:", "tags:", "Incorrect", "Correct", "Reference:"):
            self.assertEqual(card_asset.count(marker), canonical_card.count(marker))
        self.assertIn("MANAGE_SKILLS_CATEGORIES_BEGIN", skill_asset)
        self.assertIn("MANAGE_SKILLS_REFERENCES_BEGIN", skill_asset)
        self.assertIn("{{SUPPORTING_SECTIONS}}", card_asset)

    def test_generates_minimal_skill_without_metadata_or_empty_directories(self) -> None:
        skill = self.initialize()
        self.assertEqual([path.name for path in skill.iterdir()], ["SKILL.md"])
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("Rule Categories by Priority", content)
        self.assertNotIn("How to Use", content)
        self.assertFalse(self.validator.TOKEN_PATTERN.search(content))
        self.assertEqual(self.validator.validate_skill(skill), [])

    def test_preserves_apostrophes_in_generated_yaml_strings(self) -> None:
        arguments = self.init_arguments("apostrophe-skill")
        description_index = arguments.index("--description") + 1
        arguments[description_index] = "Review a user's changes. Use for focused review."
        result = self.run_script("init_skill.py", *arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        skill = self.destination / "apostrophe-skill"
        fields, _ = self.validator.extract_frontmatter(
            (skill / "SKILL.md").read_text(encoding="utf-8")
        )
        self.assertEqual(fields["description"], "Review a user's changes. Use for focused review.")

    def test_generates_each_optional_frontmatter_field(self) -> None:
        skill = self.initialize(
            "--license", "MIT", "--allowed-tools", "Read Grep", "--author", "Maintainer",
            "--version", "1.0.0", "--compatibility", "Requires Python 3.11"
        )
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
        for field in ("license:", "allowed-tools:", "metadata:", "author:", "version:", "compatibility:"):
            self.assertIn(field, content)
        self.assertEqual(self.validator.validate_skill(skill), [])

    def test_generates_conditional_sections_independently(self) -> None:
        cases = (((), False, False), (("--categories",), True, False), (("--references",), False, True))
        for index, (flags, categories, references) in enumerate(cases):
            with self.subTest(flags=flags):
                skill = self.initialize(*flags, name=f"conditional-{index}")
                content = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual("Rule Categories by Priority" in content, categories)
                self.assertEqual("Quick Reference" in content, categories)
                self.assertEqual("How to Use" in content, references)

    def test_openai_metadata_is_optional_and_validated_when_requested(self) -> None:
        skill = self.initialize(
            "--openai-metadata", "--display-name", "Review Changes", "--short-description",
            "Review changes with focused evidence", "--default-prompt",
            "Use $review-changes to review this diff."
        )
        self.assertTrue((skill / "agents" / "openai.yaml").is_file())
        self.assertEqual(self.validator.validate_skill(skill), [])
        rejected = self.run_script("init_skill.py", *self.init_arguments("bad-metadata"), "--display-name", "Bad")
        self.assertNotEqual(rejected.returncode, 0)
        self.assertFalse((self.destination / "bad-metadata").exists())

    def write_skill(self, name: str = "sample-skill") -> Path:
        skill = self.destination / name
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Review focused changes.\n---\n\n# Sample\n\n## When to Apply\n",
            encoding="utf-8",
        )
        return skill

    def write_card(self, skill: Path, **replacements: str) -> Path:
        references = skill / "references"
        references.mkdir(exist_ok=True)
        card = references / "rule-card.md"
        content = (
            "---\ntitle: Rule Card\nimpact: HIGH\nimpactDescription: Prevents invalid boundaries.\n"
            "tags: architecture, nestjs\n---\n\n## Rule Card\n\nApply one boundary.\n\n"
            "**Incorrect (bypasses the boundary):**\n\n```typescript\nconst invalid = true;\n```\n\n"
            "**Correct (uses the boundary):**\n\n```typescript\nconst valid = true;\n```\n\n"
            "Reference: [NestJS](https://docs.nestjs.com/)\n"
        )
        for old, new in replacements.items():
            content = content.replace(old, new)
        card.write_text(content, encoding="utf-8")
        skill_md = skill / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\n## How to Use\n", encoding="utf-8")
        return card

    def test_accepts_external_and_internal_card_references(self) -> None:
        for index, reference in enumerate((
            "Reference: [NestJS](https://docs.nestjs.com/)",
            "Reference: Internal policy; no external authority applies.",
        )):
            skill = self.write_skill(f"valid-card-{index}")
            card = self.write_card(skill, **{"Reference: [NestJS](https://docs.nestjs.com/)": reference})
            self.assertEqual(self.validator.validate_card(card), [])

    def test_rejects_invalid_cards(self) -> None:
        cases = {
            "duplicate-tags": ("architecture, nestjs", "architecture, architecture"),
            "wrong-heading": ("## Rule Card", "## Different Card"),
            "wrong-marker": ("**Incorrect (", "**Wrong ("),
            "missing-language": ("```typescript", "```"),
            "bad-reference": ("[NestJS](https://docs.nestjs.com/)", "unverified source"),
            "residual-token": ("Apply one boundary.", "Apply {{RULE}}."),
        }
        for index, (label, replacement) in enumerate(cases.items()):
            with self.subTest(label=label):
                skill = self.write_skill(f"invalid-card-{index}")
                card = self.write_card(skill, **{replacement[0]: replacement[1]})
                self.assertNotEqual(self.validator.validate_card(card), [])

    def test_rejects_every_malformed_markdown_file_in_references(self) -> None:
        cases = {
            "bom": "\ufeff---\ntitle: Broken\n---\n",
            "missing-frontmatter": "# Documentation without card metadata\n",
            "unclosed-frontmatter": "---\ntitle: Broken\nimpact: HIGH\n",
        }
        for index, (label, content) in enumerate(cases.items()):
            with self.subTest(label=label):
                skill = self.write_skill(f"malformed-reference-{index}")
                references = skill / "references"
                references.mkdir()
                (references / "invalid.md").write_text(content, encoding="utf-8")
                errors = self.validator.validate_skill(skill)
                self.assertTrue(any("invalid.md" in error for error in errors), errors)

    def test_rejects_duplicate_fields_wrong_types_headings_and_tokens(self) -> None:
        cases = {
            "duplicate": "name: sample-skill\nname: sample-skill",
            "type": "description: false",
            "heading": "## when to apply",
            "token": "{{UNRESOLVED}}",
        }
        for index, fragment in enumerate(cases.values()):
            skill = self.write_skill(f"invalid-skill-{index}")
            content = (skill / "SKILL.md").read_text(encoding="utf-8")
            if index == 0:
                content = content.replace(f"name: invalid-skill-{index}", fragment)
            elif index == 1:
                content = content.replace("description: Review focused changes.", fragment)
            elif index == 2:
                content = content.replace("## When to Apply", fragment)
            else:
                content += fragment
            (skill / "SKILL.md").write_text(content, encoding="utf-8")
            self.assertNotEqual(self.validator.validate_skill(skill), [])

    def test_initializer_rolls_back_after_write_failure(self) -> None:
        scripts_path = self.standalone_root / "scripts"
        spec = importlib.util.spec_from_file_location("portable_init", scripts_path / "init_skill.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        argv = ["init_skill.py", *self.init_arguments("rollback-skill")]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(
            module, "write_openai_yaml", side_effect=OSError("forced failure")
        ):
            argv.extend([
                "--openai-metadata", "--display-name", "Rollback", "--short-description",
                "Rollback metadata generation safely", "--default-prompt",
                "Use $rollback-skill to test rollback."
            ])
            self.assertEqual(module.main(), 1)
        self.assertFalse((self.destination / "rollback-skill").exists())
        self.assertFalse(any(path.name.startswith(".rollback-skill.") for path in self.destination.iterdir()))

    def test_metadata_update_preserves_intentional_content(self) -> None:
        skill = self.initialize()
        intentional = skill / "intentional.txt"
        intentional.write_text("preserve me\n", encoding="utf-8")
        before_skill = (skill / "SKILL.md").read_bytes()
        result = self.run_script(
            "generate_openai_yaml.py", str(skill), "--display-name", "Review Changes",
            "--short-description", "Review changes with concrete evidence", "--default-prompt",
            "Use $review-changes to review these changes."
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((skill / "SKILL.md").read_bytes(), before_skill)
        self.assertEqual(intentional.read_text(encoding="utf-8"), "preserve me\n")

    def test_operates_without_host_docs_or_scripts(self) -> None:
        skill = self.initialize()
        self.assertFalse((self.standalone_root.parent / "docs").exists())
        result = self.run_script("quick_validate.py", str(skill))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_repository_installation_matches_source_when_repository_is_present(self) -> None:
        source = self.repository_root / "skills" / "workflow" / "manage-skills"
        installed = self.repository_root / ".agents" / "skills" / "manage-skills"
        if not installed.exists():
            if (self.repository_root / "docs" / "skill-development").is_dir():
                self.fail("repository installation is required at .agents/skills/manage-skills")
            self.skipTest("standalone installation has no repository-local installed copy")

        def snapshot(root: Path) -> dict[str, bytes]:
            return {
                str(path.relative_to(root)): path.read_bytes()
                for path in sorted(root.rglob("*"))
                if path.is_file() and "__pycache__" not in path.relative_to(root).parts
            }

        self.assertEqual(snapshot(installed), snapshot(source))


if __name__ == "__main__":
    unittest.main()
