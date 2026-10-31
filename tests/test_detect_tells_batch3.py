"""detect-tells.py 第三批扩充规则(社区 AI-slop 清单扩充,2026-10-25)的单元测试。

硬通道 4 条(gradient-button / aurora-blob / library-primary / uniform-shadow)
进 findings(退出码 1);告警档 2 条(glass-backdrop-blur / undeclared-font)只报
不拦。既有规则行为由 batch1/batch2 守护,本文件只锁批三扩充面。
"""

import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

dt = load("detect-tells.py")

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "detect_tells")


class TestGradientButton(unittest.TestCase):
    def test_css_gradient_button_reports(self):
        findings, _ = dt.scan_text(
            ".cta-btn { background: linear-gradient(90deg, #10b981, #14b8a6); }", "a.css")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("gradient-button", "major")])

    def test_tailwind_gradient_button_reports(self):
        findings, _ = dt.scan_text(
            '<button class="bg-gradient-to-r from-emerald-400 to-teal-500">Go</button>', "a.html")
        self.assertTrue(any(f["rule"] == "gradient-button" for f in findings))

    def test_solid_button_passes(self):
        findings, _ = dt.scan_text(
            '<button class="btn bg-brand-600 text-white">Go</button>', "a.html")
        self.assertEqual(findings, [])

    def test_gradient_without_cta_passes(self):
        # 渐变背景不在按钮语境:归 purple-cyan-gradient 等规则管,不判 gradient-button
        findings, _ = dt.scan_text(
            ".hero-bg { background: linear-gradient(180deg, #f8fafc, #cbd5e1); }", "a.css")
        self.assertEqual(findings, [])


class TestAuroraBlob(unittest.TestCase):
    def test_tw_blur_3xl_reports(self):
        findings, _ = dt.scan_text(
            '<div class="blob bg-indigo-400 blur-3xl rounded-full"></div>', "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("aurora-blob", "major")])

    def test_css_blur_64px_reports(self):
        findings, _ = dt.scan_text(".glowspot { filter: blur(64px); }", "a.css")
        self.assertTrue(any(f["rule"] == "aurora-blob" for f in findings))

    def test_image_censor_blur_passes(self):
        findings, _ = dt.scan_text('<img src="a.png" class="blur-3xl" alt="打码">', "a.html")
        self.assertEqual(findings, [])

    def test_backdrop_line_not_aurora(self):
        # backdrop-filter 归玻璃拟态告警档,不判 aurora 硬命中
        findings, _ = dt.scan_text(".glass { backdrop-filter: blur(60px); }", "a.css")
        self.assertEqual(findings, [])

    def test_small_blur_passes(self):
        findings, _ = dt.scan_text(".soft { filter: blur(8px); }", "a.css")
        self.assertEqual(findings, [])


class TestLibraryPrimary(unittest.TestCase):
    def test_shadcn_indigo_reports(self):
        findings, _ = dt.scan_text(".btn-primary { background: #6366f1; }", "a.css")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("library-primary", "major")])

    def test_element_plus_blue_reports(self):
        findings, _ = dt.scan_text(":root { --el-color-primary: #409EFF; }", "a.css")
        self.assertTrue(any(f["rule"] == "library-primary" for f in findings))

    def test_tailwind_blue_accent_passes(self):
        # clean 夹具先例:通用 Tailwind blue 作 accent 不机械拦截,留人工对照
        findings, _ = dt.scan_text(":root { --accent: #2563eb; }", "a.css")
        self.assertEqual(findings, [])


class TestUniformShadow(unittest.TestCase):
    def test_four_same_shadow_reports(self):
        text = "\n".join('<div class="tile shadow-lg">%s</div>' % c for c in "ABCD")
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(
            [(f["rule"], f["severity"]) for f in findings],
            [("uniform-shadow", "major")])

    def test_mixed_shadow_levels_pass(self):
        text = ('<div class="a shadow-sm"></div>\n<div class="b shadow-md"></div>\n'
                '<div class="c shadow-lg"></div>\n<div class="d shadow-xl"></div>')
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])

    def test_few_shadows_pass(self):
        findings, _ = dt.scan_text(
            '<div class="a shadow-lg"></div><div class="b shadow-lg"></div>', "a.html")
        self.assertEqual(findings, [])


class TestGlassAdvisory(unittest.TestCase):
    def test_backdrop_blur_is_minor_warning(self):
        warnings = dt.scan_advisory_tells(
            '<div class="glass-card backdrop-blur-md bg-white/60">x</div>', "a.html")
        self.assertEqual(
            [(w["rule"], w["severity"]) for w in warnings],
            [("glass-backdrop-blur", "minor")])

    def test_minor_does_not_block_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.html")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write('<div class="glass-card backdrop-blur-md">x</div>')
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = dt.main([path])
            self.assertEqual(code, 0)
            self.assertIn("glass-backdrop-blur", buf.getvalue())


class TestUndeclaredFont(unittest.TestCase):
    def test_undeclared_family_reports(self):
        warnings = dt.scan_undeclared_fonts(
            '.accent { font-family: "Instrument Serif", serif; }', "a.css")
        self.assertEqual(
            [(w["rule"], w["severity"]) for w in warnings],
            [("undeclared-font", "minor")])

    def test_fontface_declared_passes(self):
        text = ('@font-face { font-family: "Instrument Serif"; src: local("x"); }\n'
                '.accent { font-family: "Instrument Serif", serif; }')
        self.assertEqual(dt.scan_undeclared_fonts(text, "a.css"), [])

    def test_googlefonts_link_declared_passes(self):
        text = ('<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400&display=swap" rel="stylesheet">\n'
                'body { font-family: "Public Sans", system-ui, sans-serif; }')
        self.assertEqual(dt.scan_undeclared_fonts(text, "a.html"), [])

    def test_system_stack_passes(self):
        self.assertEqual(
            dt.scan_undeclared_fonts('body { font-family: system-ui, sans-serif; }', "a.css"), [])


class TestReflexFontBatch3(unittest.TestCase):
    def test_geist_is_reflex(self):
        warnings = dt.scan_reflex_fonts('.hero-title { font-family: "Geist", sans-serif; }', "a.css")
        self.assertTrue(any(w["rule"] == "reflex-font" and "geist" in w["message"] for w in warnings))


class TestFixturePairingBatch3(unittest.TestCase):
    def test_slop_fixture_hits_batch3_rules(self):
        with open(os.path.join(FIXTURES, "slop.html"), encoding="utf-8") as fh:
            text = fh.read()
        findings, _ = dt.scan_text(text, "slop.html")
        rules = {f["rule"] for f in findings}
        self.assertIn("gradient-button", rules)
        self.assertIn("aurora-blob", rules)
        self.assertIn("library-primary", rules)
        self.assertIn("uniform-shadow", rules)
        warnings = dt.scan_advisory_tells(text, "slop.html") + dt.scan_undeclared_fonts(text, "slop.html")
        warn_rules = {w["rule"] for w in warnings}
        self.assertIn("glass-backdrop-blur", warn_rules)
        self.assertIn("undeclared-font", warn_rules)

    def test_clean_fixture_still_zero(self):
        with open(os.path.join(FIXTURES, "clean.html"), encoding="utf-8") as fh:
            text = fh.read()
        findings, _ = dt.scan_text(text, "clean.html")
        warnings = (dt.scan_advisory_tells(text, "clean.html")
                    + dt.scan_reflex_fonts(text, "clean.html")
                    + dt.scan_undeclared_fonts(text, "clean.html"))
        self.assertEqual(findings, [], "clean 夹具不得有硬命中: %s" % findings)
        self.assertEqual(warnings, [], "clean 夹具不得有告警档命中: %s" % warnings)

    def test_cli_slop_exits_1(self):
        slop = os.path.join(FIXTURES, "slop.html")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(dt.main([slop]), 1)


if __name__ == "__main__":
    unittest.main()
