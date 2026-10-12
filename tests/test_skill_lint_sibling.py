"""skill_lint.py sibling-skills 规则(#8 兄弟 skill 名存在性,opt-in)的单元测试。"""

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


SKILLMD = "---\nname: my-skill\ndescription: \"边界：代码审查用 diting；安全扫描用 tiangang\"\n---\n\n# t\n"


class TestSiblingSkills(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self._tmp.name)
        self.repo = self.workspace / "my-skill"
        self.repo.mkdir()
        _write(self.repo / "SKILL.md", SKILLMD)

    def tearDown(self):
        self._tmp.cleanup()

    def _rule(self, siblings, severity="FAIL"):
        _write(self.repo / "lint-checks.json", json.dumps(
            {"checks": [{"name": "兄弟引用", "type": "sibling-skills",
                         "siblings": siblings, "severity": severity}]},
            ensure_ascii=False))
        return sl.check_repo_rules(self.repo)

    def _sibling(self, name, present=True):
        if present:
            _write(self.workspace / name / "SKILL.md", "---\nname: %s\n---\n" % name)

    def test_referenced_sibling_present_passes(self):
        self._sibling("diting")
        self._sibling("tiangang")
        fails, warns = self._rule(["diting", "tiangang"])
        self.assertEqual((fails, warns), ([], []))

    def test_dangling_sibling_reference_fails(self):
        self._sibling("diting")
        fails, _ = self._rule(["diting", "tiangang"])
        self.assertTrue(any("悬空" in f and "tiangang" in f for f in fails))

    def test_unreferenced_sibling_not_checked(self):
        # description 没提的兄弟不检查(按引用而非按清单全查)
        self._sibling("diting")
        fails, _ = self._rule(["diting", "kueiku"])
        self.assertEqual(fails, [])

    def test_word_boundary_no_partial_match(self):
        # 词边界:ditingx 不算引用 diting
        _write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "用 ditingx 做事"\n---\n')
        fails, _ = self._rule(["diting"])
        self.assertEqual(fails, [])

    def test_severity_warn_goes_to_warns(self):
        _write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "用 tiangang 扫描"\n---\n')
        fails, warns = self._rule(["tiangang"], severity="WARN")
        self.assertEqual(fails, [])
        self.assertTrue(any("悬空" in w for w in warns))

    def test_missing_siblings_key_is_config_fail(self):
        # 配置错误显性化:缺 siblings 必须 FAIL
        _write(self.repo / "lint-checks.json", json.dumps(
            {"checks": [{"name": "兄弟引用", "type": "sibling-skills"}]}))
        fails, _ = sl.check_repo_rules(self.repo)
        self.assertTrue(any("siblings" in f for f in fails))

    def test_description_without_frontmatter_field_is_noop(self):
        _write(self.repo / "SKILL.md", "# 无 frontmatter\n用 diting\n")
        fails, _ = self._rule(["diting"])
        self.assertEqual(fails, [])

    def test_maliang_real_config_accepts_workspace_siblings(self):
        # maliang 仓真实配置在真实工作区应当通过(兄弟仓都在)
        repo = Path(__file__).resolve().parent.parent
        cfg_path = repo / "lint-checks.json"
        if not cfg_path.is_file():
            self.skipTest("lint-checks.json 不存在")
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        rules = [c for c in cfg.get("checks", []) if c.get("type") == "sibling-skills"]
        if not rules:
            self.skipTest("未配置 sibling-skills")
        fails, warns = sl.check_repo_rules(repo)
        self.assertFalse(
            any("悬空兄弟引用" in f for f in fails),
            "maliang 的兄弟引用在真实工作区不应悬空: %s" % fails)


if __name__ == "__main__":
    unittest.main()
