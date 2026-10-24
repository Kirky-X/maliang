"""skill_lint.py 的 frontmatter ↔ skill.json 双写对账测试（description/tags/version）。"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

sl = load("skill_lint.py")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestMetaCrossCheck(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "my-skill"
        self.repo.mkdir()
        _write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "同一个描述"\n'
               'metadata:\n  version: "1.0.0"\n  tags: "a, b"\n---\n\n# t\n')
        _write(self.repo / ".gitignore", "specmark/\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _skill_json(self, **kw):
        data = {"name": "my-skill", "description": "同一个描述",
                "version": "1.0.0", "tag": ["a", "b"]}
        data.update(kw)
        _write(self.repo / "skill.json", json.dumps(data, ensure_ascii=False))
        return sl.lint_repo(self.repo)

    def test_matching_desc_and_tags_pass(self):
        fails, _ = self._skill_json()
        self.assertEqual(fails, [])

    def test_description_drift_fails(self):
        # description 双写漂移必须 FAIL,不能单边修改后静默分叉
        fails, _ = self._skill_json(description="另一个描述")
        self.assertTrue(any("description" in f for f in fails))

    def test_tags_drift_fails(self):
        fails, _ = self._skill_json(tag=["a", "c"])
        self.assertTrue(any("tags" in f for f in fails))

    def test_version_drift_still_fails(self):
        fails, _ = self._skill_json(version="9.9.9")
        self.assertTrue(any("version" in f for f in fails))


if __name__ == "__main__":
    unittest.main()
