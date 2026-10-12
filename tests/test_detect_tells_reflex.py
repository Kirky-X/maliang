"""detect-tells.py 的 reflex-font 告警档(#35)测试。

单独成文件:告警档与硬命中通道是两条出口,本文件只锁告警档行为
(硬命中与豁免主通道仍由 tests/test_detect_tells.py 守护)。
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

DISPLAY_FRAUNCES = '<style>h1 { font-family: "Fraunces", serif; }</style>'
DISPLAY_VAR = ('<style>:root { --font-display: "Space Grotesk", sans-serif; }'
               'h2 { font-family: var(--font-display); }</style>')
BODY_INTER = '<style>body { font-family: "Inter", system-ui, sans-serif; }</style>'
SYSTEM_DISPLAY = '<style>h1 { font-family: "Public Sans", system-ui, sans-serif; }</style>'


class TestReflexFontWarning(unittest.TestCase):
    def test_display_heading_reflex_reports_warning(self):
        warnings = dt.scan_reflex_fonts(DISPLAY_FRAUNCES, "a.html")
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["rule"], "reflex-font")
        self.assertIn("fraunces", warnings[0]["message"])

    def test_display_var_redefinition_reports(self):
        warnings = dt.scan_reflex_fonts(DISPLAY_VAR, "a.html")
        self.assertTrue(any("space grotesk" in w["message"] for w in warnings))

    def test_body_font_not_in_scope(self):
        # Inter 只在「当 display 用」时命中;正文/UI 字族不在扫描范围
        self.assertEqual(dt.scan_reflex_fonts(BODY_INTER, "a.html"), [])

    def test_non_reflex_display_font_passes(self):
        self.assertEqual(dt.scan_reflex_fonts(SYSTEM_DISPLAY, "a.html"), [])

    def test_tell_exempt_file_scope_suppresses_warning(self):
        text = "/* tell-exempt: reflex-font file, 品牌既有规范 */\n" + DISPLAY_FRAUNCES
        self.assertEqual(dt.scan_reflex_fonts(text, "a.html"), [])


class TestWarningChannelCli(unittest.TestCase):
    def _run(self, content, argv_extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "font.html")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = dt.main([path] + (argv_extra or []))
            return code, buf.getvalue()

    def test_warning_does_not_change_exit_code(self):
        code, out = self._run(DISPLAY_FRAUNCES)
        self.assertEqual(code, 0)          # 告警档不进硬失败通道
        self.assertIn("reflex-font", out)
        self.assertIn("告警档", out)

    def test_json_has_warnings_key(self):
        code, out = self._run(DISPLAY_FRAUNCES, ["--format", "json"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["findings"], [])
        self.assertEqual(len(payload["warnings"]), 1)
        self.assertEqual(payload["warnings"][0]["rule"], "reflex-font")

    def test_hard_finding_still_exits_1_with_warning(self):
        content = DISPLAY_FRAUNCES + '<h1 class="bg-clip-text text-transparent">Hi</h1>'
        code, out = self._run(content)
        self.assertEqual(code, 1)
        self.assertIn("gradient-text", out)
        self.assertIn("reflex-font", out)


if __name__ == "__main__":
    unittest.main()
