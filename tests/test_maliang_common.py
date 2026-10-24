"""maliang_common.parse_frontmatter 单元测试(双列 fixture)。"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

mc = load("maliang_common.py")

import unittest  # noqa: E402


class TestParseFrontmatter(unittest.TestCase):
    def test_no_frontmatter_returns_empty(self):
        # 不应报: 无 frontmatter 的普通 markdown
        self.assertEqual(mc.parse_frontmatter("# 标题\n正文"), {})

    def test_simple_kv(self):
        fm = mc.parse_frontmatter("---\nname: home\ndescription: 首页\n---\n正文")
        self.assertEqual(fm["name"], "home")
        self.assertEqual(fm["description"], "首页")

    def test_inline_components_list(self):
        # 应解析为 list
        fm = mc.parse_frontmatter("---\ncomponents: [button, input, icon]\n---\n")
        self.assertEqual(fm["components"], ["button", "input", "icon"])

    def test_empty_components_list(self):
        fm = mc.parse_frontmatter("---\ncomponents: []\n---\n")
        self.assertEqual(fm["components"], [])

    def test_quoted_value_stripped(self):
        fm = mc.parse_frontmatter('---\nbackground: "{surface-base}"\n---\n')
        self.assertEqual(fm["background"], "{surface-base}")

    def test_multiline_string(self):
        text = "---\ndescription: >\n  第一行\n  第二行\n---\n"
        fm = mc.parse_frontmatter(text)
        self.assertEqual(fm["description"], "第一行\n第二行")


if __name__ == "__main__":
    unittest.main()


class TestWcagMath(unittest.TestCase):
    """WCAG 对比度数学(全库唯一实现)的单测:阈值行为、alpha 合成、恒等性质。"""

    def test_srgb_to_linear_boundaries(self):
        self.assertAlmostEqual(mc.srgb_to_linear(0.0), 0.0)
        self.assertAlmostEqual(mc.srgb_to_linear(1.0), 1.0)
        # 阈值 0.04045(WCAG 2.1/sRGB):分界点走线性段
        self.assertAlmostEqual(mc.srgb_to_linear(0.04045), 0.04045 / 12.92)

    def test_eight_bit_threshold_equivalence(self):
        # 旧值 0.03928 与 0.04045 对全部 8-bit 量化值结果全等(历史阈值混用无害的根据)
        old = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        for v in range(256):
            self.assertAlmostEqual(
                mc.srgb_to_linear(v / 255.0), old(v / 255.0), places=12)

    def test_hex_to_rgb255(self):
        self.assertEqual(mc.hex_to_rgb255("#212121"), (33, 33, 33))
        self.assertEqual(mc.hex_to_rgb255("5B7CFA"), (91, 124, 250))
        with self.assertRaises(ValueError):
            mc.hex_to_rgb255("#FFF")

    def test_blend_alpha(self):
        # 不透明:原样返回(0-1 浮点)
        self.assertEqual(mc.blend_alpha((255, 0, 0, 1.0), (0, 0, 255)), (1.0, 0.0, 0.0))
        # 0.5 alpha 合成:红 50% 上蓝底 → (0.5, 0, 0.5)
        r, g, b = mc.blend_alpha((255, 0, 0, 0.5), (0, 0, 255))
        self.assertAlmostEqual(r, 0.5)
        self.assertAlmostEqual(b, 0.5)

    def test_luminance_and_contrast(self):
        self.assertAlmostEqual(mc.relative_luminance((1.0, 1.0, 1.0)), 1.0)
        self.assertAlmostEqual(mc.relative_luminance((0.0, 0.0, 0.0)), 0.0)
        self.assertAlmostEqual(mc.contrast_ratio(1.0, 0.0), 21.0)
        self.assertAlmostEqual(mc.contrast_ratio(0.5, 0.5), 1.0)

    def test_contrast_ratio_hex(self):
        self.assertAlmostEqual(mc.contrast_ratio_hex("#FFFFFF", "#000000"), 21.0)
        # 已知实测:placeholder #9CA3AF on #F7F8FA ≈ 2.39(token.md 记录值)
        self.assertAlmostEqual(mc.contrast_ratio_hex("#9CA3AF", "#F7F8FA"), 2.39, places=2)


class TestEngineParityWithSkillLint(unittest.TestCase):
    """skill_lint(可 vendored 自包含副本)与 maliang_common 共享引擎的孪生一致性:
    同一 fixture 上两套实现必须同判,防止双副本语义漂移(F20)。"""

    def setUp(self):
        import tempfile
        from pathlib import Path
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "INDEX.md").write_text(
            "# INDEX\n\n## 设计语言\n\n| id |\n| --- |\n| [a](a.md) |\n| [b](b.md) |\n\n## 其他\n",
            encoding="utf-8")
        (self.repo / "SKILL.md").write_text("共 3 种设计语言\n", encoding="utf-8")
        import json
        (self.repo / "lint-checks.json").write_text(json.dumps(
            {"checks": [{"name": "计数对账", "type": "count-matches", "source": "INDEX.md",
                         "section": "## 设计语言", "claim_files": ["SKILL.md"],
                         "claim_patterns": ["(\d+)\s*种设计语言"]}]},
            ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_both_engines_flag_same_drift(self):
        rule = {"name": "计数对账", "type": "count-matches", "source": "INDEX.md",
                "section": "## 设计语言", "claim_files": ["SKILL.md"],
                "claim_patterns": ["(\d+)\s*种设计语言"]}
        # 共享引擎:报漂移
        findings = mc.engine_run_rule(str(self.repo), rule)
        self.assertTrue(any("计数漂移" in f["message"] for f in findings))
        # skill_lint vendored 副本:同判
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        sl = load("skill_lint.py")
        fails, _ = sl.check_repo_rules(self.repo)
        self.assertTrue(any("计数漂移" in f for f in fails))

    def test_both_engines_pass_when_consistent(self):
        (self.repo / "SKILL.md").write_text("共 2 种设计语言\n", encoding="utf-8")
        rule = {"name": "计数对账", "type": "count-matches", "source": "INDEX.md",
                "section": "## 设计语言", "claim_files": ["SKILL.md"],
                "claim_patterns": ["(\d+)\s*种设计语言"]}
        self.assertEqual(mc.engine_run_rule(str(self.repo), rule), [])
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        sl = load("skill_lint.py")
        fails, _ = sl.check_repo_rules(self.repo)
        self.assertEqual([f for f in fails if "计数" in f], [])


class TestEngineParityMoreTypes(unittest.TestCase):
    """parity 扩展:forbid / require / consistency 三类双副本同判(L5)。"""

    def setUp(self):
        import tempfile
        from pathlib import Path
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "a.md").write_text("禁止词: 完美\n干净行\n", encoding="utf-8")
        (self.repo / "b.md").write_text("干净行\n", encoding="utf-8")
        (self.repo / "c.md").write_text("正文 纯 Python 标准库\n", encoding="utf-8")
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        self.sl = load("skill_lint.py")

    def tearDown(self):
        self._tmp.cleanup()

    def _both(self, rule):
        eng = mc.engine_run_rule(str(self.repo), rule)
        import json
        (self.repo / "lint-checks.json").write_text(
            json.dumps({"checks": [rule]}, ensure_ascii=False), encoding="utf-8")
        fails, warns = self.sl.check_repo_rules(self.repo)
        sl_msgs = fails + warns
        return eng, sl_msgs

    def test_forbid_parity(self):
        rule = {"name": "禁用", "type": "forbid-pattern", "files": ["a.md"], "pattern": "完美"}
        eng, sl_msgs = self._both(rule)
        self.assertEqual(len(eng), 1)
        self.assertTrue(any("a.md:1" in m for m in sl_msgs))

    def test_require_parity(self):
        rule = {"name": "必现", "type": "require-pattern", "file": "c.md",
                "pattern": "纯 Python 标准库", "min_count": 1}
        eng, sl_msgs = self._both(rule)
        self.assertEqual(eng, [])
        self.assertEqual([m for m in sl_msgs if "必现短语未满足" in m], [])
        # 未满足时两侧同报
        rule2 = dict(rule, file="b.md", pattern="不存在的短语")
        eng2, sl2 = self._both(rule2)
        self.assertEqual(len(eng2), 1)
        self.assertTrue(any("必现短语未满足" in m for m in sl2))

    def test_consistency_parity(self):
        rule = {"name": "一致", "type": "consistency", "files": ["a.md", "b.md"],
                "pattern": "^干净行$"}
        eng, sl_msgs = self._both(rule)
        self.assertEqual(eng, [])
        self.assertEqual([m for m in sl_msgs if "一致性漂移" in m], [])
        # 漂移时两侧同报:b.md 改成不同内容
        (self.repo / "b.md").write_text("另一行\n", encoding="utf-8")
        eng2, sl2 = self._both(rule)
        self.assertTrue(any("未命中一致性 pattern" in f["message"] for f in eng2))
        self.assertTrue(any("未命中一致性 pattern" in m for m in sl2))


class TestParityEdgeCases(unittest.TestCase):
    """M1/L6 回归锁:重复标题节与 YAML 孪生解析的两侧同判。"""

    def setUp(self):
        import tempfile
        from pathlib import Path
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        # 重复标题:两个「## 设计语言」节——两侧都必须取第一次出现
        (self.repo / "INDEX.md").write_text(
            "# INDEX\n\n## 设计语言\n\n| id |\n| --- |\n| [a](a.md) |\n\n"
            "## 其他\n\n## 设计语言\n\n| id |\n| --- |\n| [b](b.md) |\n| [c](c.md) |\n",
            encoding="utf-8")
        (self.repo / "SKILL.md").write_text("共 1 种设计语言\n", encoding="utf-8")
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        self.sl = load("skill_lint.py")

    def tearDown(self):
        self._tmp.cleanup()

    def test_duplicate_heading_same_verdict(self):
        rule = {"name": "计数", "type": "count-matches", "source": "INDEX.md",
                "section": "## 设计语言", "claim_files": ["SKILL.md"],
                "claim_patterns": ["(\d+)\s*种设计语言"]}
        eng = mc.engine_run_rule(str(self.repo), rule)
        import json
        (self.repo / "lint-checks.json").write_text(json.dumps(
            {"checks": [rule]}, ensure_ascii=False), encoding="utf-8")
        fails, _ = self.sl.check_repo_rules(self.repo)
        # 第一次出现的节只有 1 行 → 声称 1 一致,两侧都应通过
        self.assertEqual(eng, [])
        self.assertEqual([f for f in fails if "计数漂移" in f], [])

    def test_yaml_twin_parity(self):
        text = ('---\nname: my-skill\ndescription: "d"\nmetadata:\n  version: "1.0.0"\n'
                '  tags: "a, b"\n---\n\n# t\n')
        import re
        sl_parsed, err = self.sl.parse_frontmatter(text)
        m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
        mc_parsed, mc_err = mc.load_yaml_block(m.group(1))
        self.assertIsNone(err)
        self.assertIsNone(mc_err)
        self.assertEqual(sl_parsed, mc_parsed)
