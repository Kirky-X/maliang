"""check-copy.py(#32 句型级反模板)的单元测试 + fixture 冒烟。"""

import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

cc = load("check-copy.py")

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "copy")


def _rules(text):
    return [f["rule"] for f in cc.findings_for_text(text, "t")]


class TestTemplatePatterns(unittest.TestCase):
    def test_ten_shapes_recognised(self):
        cases = {
            "The smart way to invoice clients": "copy-template/the-adj-way-to",
            "Built for teams who move fast": "copy-template/built-for-who",
            "Ship your store in seconds": "copy-template/verb-your-noun-in-time",
            "Where design meets code": "copy-template/where-x-meets-y",
            "Simple, powerful analytics.": "copy-template/adj-adj-noun",
            "Everything you need to scale": "copy-template/everything-you-need",
            "Invoicing made easy": "copy-template/noun-made-adj",
            "Say goodbye to busywork": "copy-template/say-goodbye-to",
            "Your workspace, reimagined": "copy-template/noun-reimagined",
            "One platform for all your tools": "copy-template/one-platform-for-all",
        }
        for text, rule in cases.items():
            self.assertIn(rule, _rules(text), text)

    def test_specific_copy_passes(self):
        self.assertEqual(_rules("报销单拍照后按发票号码去重"), [])
        self.assertEqual(_rules("See the query before it runs."), [])


class TestEmDash(unittest.TestCase):
    def test_english_em_dash_reports(self):
        rules = _rules("The platform — built for speed — ships in days.")
        self.assertEqual(rules, ["em-dash", "em-dash"])

    def test_chinese_dash_exempt(self):
        # ai-tells §6:中文破折号「——」是规范用法,豁免
        self.assertEqual(_rules("静默成功通常是对的——效果已在屏上就别庆祝"), [])


class TestScanMarkup(unittest.TestCase):
    def test_visible_text_scanned_style_skipped(self):
        html = ("<style>.x::before { content: 'Say goodbye to slow reports'; }</style>"
                "<body><h1>The smart way to invoice</h1></body>")
        findings = cc.scan_markup(html, "a.html")
        rules = [f["rule"] for f in findings]
        self.assertEqual(rules, ["copy-template/the-adj-way-to"])
        self.assertEqual(findings[0]["where"], "a.html:1")

    def test_comments_skipped(self):
        html = "<body><!-- The smart way to invoice --><p>具体文案</p></body>"
        self.assertEqual(cc.scan_markup(html, "a.html"), [])


class TestCli(unittest.TestCase):
    def _write(self, directory, name, content):
        path = os.path.join(directory, name)
        open(path, "w", encoding="utf-8").write(content)
        return path

    def test_fixture_clean_passes(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cc.main([os.path.join(FIXTURES, "clean.html")])
        self.assertEqual(code, 0, buf.getvalue())

    def test_hit_file_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "bad.html", "<h1>Where design meets code</h1>")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = cc.main([path])
            self.assertEqual(code, 1)
            self.assertIn("copy-template/where-x-meets-y", buf.getvalue())

    def test_headline_flag_mode(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cc.main(["--headline", "Invoicing made easy"])
        self.assertEqual(code, 1)
        self.assertIn("noun-made-adj", buf.getvalue())

    def test_no_target_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = cc.main([])
        self.assertEqual(code, 2)
        self.assertIn("没能检查", err.getvalue())

    def test_missing_path_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = cc.main([os.path.join("no", "such", "dir")])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
