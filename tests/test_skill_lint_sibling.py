"""skill_lint.py sibling-skills 规则(#8 兄弟 skill 名存在性,opt-in)的单元测试。"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load, write  # noqa: E402

sl = load("skill_lint.py")




SKILLMD = "---\nname: my-skill\ndescription: \"边界：代码审查用 diting；安全扫描用 tiangang\"\n---\n\n# t\n"


class TestSiblingSkills(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self._tmp.name)
        self.repo = self.workspace / "my-skill"
        self.repo.mkdir()
        write(self.repo / "SKILL.md", SKILLMD)

    def tearDown(self):
        self._tmp.cleanup()

    def _rule(self, siblings, severity="FAIL"):
        write(self.repo / "lint-checks.json", json.dumps(
            {"checks": [{"name": "兄弟引用", "type": "sibling-skills",
                         "siblings": siblings, "severity": severity}]},
            ensure_ascii=False))
        return sl.check_repo_rules(self.repo)

    def _sibling(self, name, present=True):
        if present:
            write(self.workspace / name / "SKILL.md", "---\nname: %s\n---\n" % name)

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
        write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "用 ditingx 做事"\n---\n')
        fails, _ = self._rule(["diting"])
        self.assertEqual(fails, [])

    def test_severity_warn_goes_to_warns(self):
        self._sibling("diting")  # 让兄弟根可定位
        write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "用 tiangang 扫描"\n---\n')
        fails, warns = self._rule(["diting", "tiangang"], severity="WARN")
        self.assertEqual(fails, [])
        self.assertTrue(any("悬空" in w for w in warns))

    def test_missing_siblings_key_is_config_fail(self):
        # 配置错误显性化:缺 siblings 必须 FAIL
        write(self.repo / "lint-checks.json", json.dumps(
            {"checks": [{"name": "兄弟引用", "type": "sibling-skills"}]}))
        fails, _ = sl.check_repo_rules(self.repo)
        self.assertTrue(any("siblings" in f for f in fails))

    def test_description_without_frontmatter_field_is_noop(self):
        write(self.repo / "SKILL.md", "# 无 frontmatter\n用 diting\n")
        fails, _ = self._rule(["diting"])
        self.assertEqual(fails, [])

    def test_env_var_sibling_root_redirects(self):
        # 兄弟根可用 SKILL_SIBLINGS_ROOT 显式指定(部署布局与检出布局解耦)
        env_root = self.workspace / "skills-root"
        write(env_root / "diting" / "SKILL.md", "---\nname: diting\n---\n")
        write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "代码审查用 diting"\n---\n')
        saved = os.environ.get("SKILL_SIBLINGS_ROOT")
        os.environ["SKILL_SIBLINGS_ROOT"] = str(env_root)
        try:
            fails, warns = self._rule(["diting"])
        finally:
            if saved is None:
                os.environ.pop("SKILL_SIBLINGS_ROOT", None)
            else:
                os.environ["SKILL_SIBLINGS_ROOT"] = saved
        self.assertEqual((fails, warns), ([], []))

    def test_unlocatable_sibling_root_warns_instead_of_fails(self):
        # 单仓检出/CI:配置兄弟一个都不在可选根下 → 显式 WARN 跳过,不冒充悬空 FAIL
        write(self.repo / "SKILL.md",
               '---\nname: my-skill\ndescription: "代码审查用 diting"\n---\n')
        fails, warns = self._rule(["diting"])
        self.assertEqual(fails, [])
        self.assertTrue(any("兄弟根不可定位" in w for w in warns))

    def test_maliang_real_config_accepts_workspace_siblings(self):
        # maliang 仓真实配置:兄弟齐时通过;兄弟根不可定位时 WARN 跳过——两者都不得悬空 FAIL
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
