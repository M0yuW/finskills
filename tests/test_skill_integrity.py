import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillIntegrityTests(unittest.TestCase):
    def _skill_files(self):
        return sorted((ROOT / "US-market").glob("*/SKILL.md")) + sorted(
            (ROOT / "China-market").glob("*/SKILL.md")
        )

    def test_skill_names_are_unique(self):
        names = []
        for path in self._skill_files():
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
            self.assertIsNotNone(match, f"Missing name in {path}")
            names.append(match.group(1).strip())

        dupes = [name for name, count in Counter(names).items() if count > 1]
        self.assertEqual([], dupes, f"Duplicate skill names found: {dupes}")

    def test_local_markdown_links_exist(self):
        files = self._skill_files() + [ROOT / "README.md", ROOT / "README.zh.md"]
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        missing = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            for raw_target in link_re.findall(text):
                target = raw_target.strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                target = target.split("#", 1)[0]
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    missing.append((str(path.relative_to(ROOT)), target))

        self.assertEqual([], missing, f"Broken local markdown links: {missing}")


if __name__ == "__main__":
    unittest.main()
