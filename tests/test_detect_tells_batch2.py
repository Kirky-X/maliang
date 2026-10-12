"""detect-tells.py 第二批扩充规则(#21)的单元测试 + slop/clean 夹具对拍。

四档对齐:critical/major 进硬命中(findings,退出码 1);minor/warn 进告警档
(warnings,不拦截)。既有五规则行为由 tests/test_detect_tells.py 守护,本文件
只锁扩充面。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

dt = load("detect-tells.py")

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "detect_tells")


class TestPurpleCyanGradient(unittest.TestCase):
    def test_tailwind_purple_pink_reports(self):
        # 裁决翻转面:紫粉渐变背景是 ai-tells §1 tell(不必有蓝端)
        text = '<div class="bg-gradient-to-r from-purple-600 to-pink-500"></div>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("purple-cyan-gradient", "critical")])

    def test_tailwind_purple_cool_reports(self):
        text = '<div class="bg-gradient-to-br from-indigo-500 via-purple-500 to-cyan-400"></div>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertTrue(any(f["rule"] == "purple-cyan-gradient" for f in findings))

    def test_raw_css_gradient_by_value_reports(self):
        # 按值判定补齐「只认 Tailwind class」逃逸通道:紫 271° + 青 190°
        text = ".hero { background: linear-gradient(135deg, #9333ea, #06b6d4); }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertTrue(any(f["rule"] == "purple-cyan-gradient" for f in findings))

    def test_single_family_gradient_passes(self):
        # 不应报: 品牌色相内 2 阶梯度(紫→深紫)与中性梯度(ai-tells §1 替代方案)
        text = (".a { background: linear-gradient(180deg, #4c1d95, #7c3aed); }\n"
                ".b { background: linear-gradient(180deg, #f8fafc, #cbd5e1); }")
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])

    def test_css_hue_helper(self):
        self.assertAlmostEqual(dt.css_hue("#ff0000"), 0.0, delta=1)
        self.assertAlmostEqual(dt.css_hue("#00ff00"), 120.0, delta=1)
        self.assertAlmostEqual(dt.css_hue("#0000ff"), 240.0, delta=1)
        self.assertIsNone(dt.css_hue("#111111"))  # 近灰无有效色相
        self.assertAlmostEqual(dt.css_hue("hsl(300, 50%, 50%)"), 300.0, delta=1)


class TestTransitionAll(unittest.TestCase):
    def test_css_transition_all_reports(self):
        findings, _ = dt.scan_text(".card { transition: all 0.3s; }", "a.css")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("transition-all", "critical")])

    def test_tailwind_transition_all_reports(self):
        findings, _ = dt.scan_text('<div class="transition-all">x</div>', "a.html")
        self.assertTrue(any(f["rule"] == "transition-all" for f in findings))

    def test_specific_properties_pass(self):
        text = ".card { transition: transform 0.2s, opacity 0.2s; }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])


class TestUppercaseHeading(unittest.TestCase):
    def test_uppercase_heading_reports(self):
        findings, _ = dt.scan_text('<h2 class="uppercase">Ship Faster</h2>', "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("uppercase-heading", "critical")])

    def test_small_tracked_label_passes(self):
        # 文档化例外: ≤13px 小标签 + 宽字距
        text = '<h4 class="uppercase text-xs tracking-widest">Category</h4>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])


class TestCelebrationMotion(unittest.TestCase):
    def test_confetti_class_reports(self):
        findings, _ = dt.scan_text('<button class="btn confetti-burst">OK</button>', "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("celebration-motion", "major")])

    def test_plain_class_passes(self):
        findings, _ = dt.scan_text('<button class="btn">OK</button>', "a.html")
        self.assertEqual(findings, [])


class TestEmojiIcon(unittest.TestCase):
    def test_emoji_only_element_reports(self):
        findings, _ = dt.scan_text("<span>\U0001F680</span>", "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("emoji-icon", "major")])

    def test_emoji_prefix_heading_reports(self):
        # 外部原式: emoji 紧前缀标题(emoji + 空白 + <h2>)
        findings, _ = dt.scan_text("<section>\U0001F680 <h2>Features</h2></section>", "a.html")
        self.assertTrue(any(f["rule"] == "emoji-icon" for f in findings))

    def test_emoji_in_sentence_passes(self):
        findings, _ = dt.scan_text("<p>发布成功 \U0001F389 大家辛苦了。</p>", "a.html")
        self.assertEqual(findings, [])


class TestLineRules(unittest.TestCase):
    def test_placeholder_copy_reports(self):
        findings, _ = dt.scan_text("<p>Get started with Lorem ipsum today</p>", "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("placeholder-copy", "major")])

    def test_lilac_purple_reports(self):
        findings, _ = dt.scan_text(".btn { background: #a78bfa; }", "a.css")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("lilac-purple", "major")])

    def test_numbered_eyebrow_is_minor_warning(self):
        warnings = dt.scan_advisory_tells("<div><span>01 · About</span></div>", "a.html")
        self.assertEqual(
            [(w["rule"], w["severity"]) for w in warnings],
            [("numbered-eyebrow", "minor")])

    def test_minor_does_not_block_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.html")
            open(path, "w", encoding="utf-8").write("<div><span>01 · About</span></div>")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = dt.main([path])
            self.assertEqual(code, 0)  # 告警档不拦截
            self.assertIn("numbered-eyebrow", buf.getvalue())

    def test_new_rule_exempt_still_works(self):
        text = ("/* tell-exempt: transition-all, 老代码保守迁移 */\n"
                ".card { transition: all 0.3s; }")
        findings, exempted = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])
        # 注释行自带的 transition-all 字样与声明行各算一次裸命中,均被豁免
        self.assertGreaterEqual(exempted, 1)


class TestFixturePairing(unittest.TestCase):
    """slop/clean 双夹具对拍:slop 必须命中,clean 必须零命中(含告警档)。"""

    def test_slop_fixture_hits_multiple_rules(self):
        findings, warnings = self._run_fixture("slop.html")
        rules = {f["rule"] for f in findings}
        self.assertIn("purple-cyan-gradient", rules)
        self.assertIn("transition-all", rules)
        self.assertIn("uppercase-heading", rules)
        self.assertIn("emoji-icon", rules)
        self.assertIn("placeholder-copy", rules)
        self.assertIn("lilac-purple", rules)
        self.assertIn("celebration-motion", rules)
        self.assertIn("numbered-eyebrow", {w["rule"] for w in warnings})

    def test_clean_fixture_zero_findings_and_warnings(self):
        findings, warnings = self._run_fixture("clean.html")
        self.assertEqual(findings, [], "clean 夹具不得有硬命中: %s" % findings)
        self.assertEqual(warnings, [], "clean 夹具不得有告警档命中: %s" % warnings)

    def _run_fixture(self, name):
        with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
            text = fh.read()
        findings, _ = dt.scan_text(text, name)
        warnings = dt.scan_advisory_tells(text, name) + dt.scan_reflex_fonts(text, name)
        return findings, warnings

    def test_cli_slop_exits_1_clean_exits_0(self):
        slop = os.path.join(FIXTURES, "slop.html")
        clean = os.path.join(FIXTURES, "clean.html")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(dt.main([slop]), 1)
            self.assertEqual(dt.main([clean]), 0)


if __name__ == "__main__":
    unittest.main()
