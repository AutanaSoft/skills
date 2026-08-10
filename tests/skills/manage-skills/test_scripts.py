from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ManageSkillsScriptsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.temp_path = Path(self.temporary_directory.name)
        repository_root = Path(__file__).resolve().parents[3]
        source = repository_root / "skills" / "workflow" / "manage-skills"
        self.standalone_root = self.temp_path / "installed" / "manage-skills"
        shutil.copytree(source, self.standalone_root)
        self.destination = self.temp_path / "target"
        self.destination.mkdir()

    def run_script(self, name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.standalone_root / "scripts" / name), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def initialize(self) -> Path:
        result = self.run_script(
            "init_skill.py",
            "review-changes",
            "--path",
            str(self.destination),
            "--description",
            "Review code changes. Use for focused code review requests.",
            "--display-name",
            "Review Changes",
            "--short-description",
            "Review code changes with focused evidence",
            "--default-prompt",
            "Use $review-changes to review this diff.",
            "--overview",
            "Review code changes and report evidence-backed findings.",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.destination / "review-changes"

    def test_creates_skill_from_scratch_without_empty_resources(self) -> None:
        skill = self.initialize()
        self.assertTrue((skill / "SKILL.md").is_file())
        self.assertTrue((skill / "agents" / "openai.yaml").is_file())
        self.assertEqual(sorted(path.name for path in skill.iterdir()), ["SKILL.md", "agents"])
        self.assertNotIn("__MANAGE_SKILLS_", (skill / "SKILL.md").read_text(encoding="utf-8"))

    def test_regenerates_metadata_without_modifying_skill(self) -> None:
        skill = self.initialize()
        original_skill = (skill / "SKILL.md").read_bytes()
        result = self.run_script(
            "generate_openai_yaml.py",
            str(skill),
            "--display-name",
            "Review Changes",
            "--short-description",
            "Review updates using concrete repository evidence",
            "--default-prompt",
            "Use $review-changes to inspect these updates.",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((skill / "SKILL.md").read_bytes(), original_skill)
        metadata = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Review updates using concrete repository evidence", metadata)

    def test_accepts_valid_and_rejects_invalid_skill(self) -> None:
        skill = self.initialize()
        valid = self.run_script("quick_validate.py", str(skill))
        self.assertEqual(valid.returncode, 0, valid.stderr)
        invalid = self.destination / "wrong-directory"
        shutil.copytree(skill, invalid)
        rejected = self.run_script("quick_validate.py", str(invalid))
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("name must match the skill directory", rejected.stderr)

    def test_operates_without_host_docs_or_scripts(self) -> None:
        skill = self.initialize()
        self.assertFalse((self.standalone_root.parent / "docs").exists())
        self.assertFalse((self.standalone_root.parent / "scripts").exists())
        result = self.run_script("quick_validate.py", str(skill))
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
