"""verify-states.py:纯函数 + 真浏览器状态态门禁测试。

无浏览器时浏览器用例自动跳过(UNMEASURED 路径用例不跳过);有浏览器时
hover-fail fixture 必须被拒绝、all-pass fixture 必须通过。
"""

import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

vs = load("verify-states.py")

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "verify_states")
BROWSER = vs.find_browser()
NO_BROWSER_REASON = "本机没有 Chrome/Chromium,浏览器用例跳过(UNMEASURED 路径仍受测)"


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = vs.main(argv)
    return code, buf.getvalue()


class TestPureFunctions(unittest.TestCase):
    def test_contrast_black_on_white_is_21(self):
        self.assertAlmostEqual(
            vs.contrast_ratio([0, 0, 0, 1], [255, 255, 255, 1]), 21.0, places=1)

    def test_contrast_alpha_composited(self):
        # rgba(0,0,0,0.5) on white ≈ #808080 → 3.99
        self.assertAlmostEqual(
            vs.contrast_ratio([0, 0, 0, 0.5], [255, 255, 255, 1]), 3.99, places=1)

    def test_needed_ratio_text(self):
        self.assertEqual(vs.needed_ratio(16.0, False, False), 4.5)
        self.assertEqual(vs.needed_ratio(14.0, True, False), 4.5)

    def test_needed_ratio_large_text(self):
        self.assertEqual(vs.needed_ratio(24.0, False, False), 3.0)
        self.assertEqual(vs.needed_ratio(18.66, True, False), 3.0)
        self.assertEqual(vs.needed_ratio(18.66, False, False), 4.5)

    def test_needed_ratio_graphical(self):
        # 图形控件(无直接文字节点)按 WCAG 1.4.11 走 3:1
        self.assertEqual(vs.needed_ratio(14.0, False, True), 3.0)

    def test_parse_viewport(self):
        self.assertEqual(vs.parse_viewport("390x844"), (390, 844))
        with self.assertRaises(Exception):
            vs.parse_viewport("wat")


class TestUnmeasuredPaths(unittest.TestCase):
    """「没能检查」必须 exit 2,不得静默通过(EXIT-CODES canonical)。"""

    def test_missing_target_exits_2(self):
        code, out = run_main([os.path.join(FIXTURES, "no-such-file.html")])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)
        self.assertIn("not a pass", out)

    def test_missing_browser_exits_2(self):
        # 显式给一个不存在的浏览器 → UNMEASURED,而不是 0
        code, out = run_main([
            os.path.join(FIXTURES, "all_states_pass.html"),
            "--browser", "/nonexistent/chrome-binary",
        ])
        self.assertEqual(code, 2)
        self.assertIn("没找到浏览器", out)
        self.assertIn("UNMEASURED", out)


@unittest.skipUnless(BROWSER, NO_BROWSER_REASON)
class TestBrowserGates(unittest.TestCase):
    def test_hover_fail_fixture_rejected(self):
        # 核心坏 fixture:default 通过、hover 掉到 1.43:1 → 必须 exit 1
        code, out = run_main([
            os.path.join(FIXTURES, "static_pass_hover_fail.html")])
        self.assertEqual(code, 1, out)
        self.assertIn("hover", out)
        self.assertIn("1.43", out)

    def test_all_states_pass_fixture_ok(self):
        code, out = run_main([os.path.join(FIXTURES, "all_states_pass.html")])
        self.assertEqual(code, 0, out)
        self.assertIn("3 个可比对元素态", out)

    def test_graphical_icon_uses_3to1(self):
        # #8B8B8B on #FFFFFF = 3.41:1:图形控件(3:1)通过;若是正文(4.5)会失败
        code, out = run_main([
            os.path.join(FIXTURES, "graphical_icon_3to1_pass.html")])
        self.assertEqual(code, 0, out)

    def test_no_interactive_targets_is_unmeasured(self):
        # 页面没有任何交互元素 = 无目标 → UNMEASURED exit 2
        code, out = run_main([
            os.path.join(FIXTURES, "no_interactive_targets.html")])
        self.assertEqual(code, 2, out)
        self.assertIn("无可测量目标", out)

    def test_json_format_shape(self):
        code, out = run_main([
            os.path.join(FIXTURES, "static_pass_hover_fail.html"), "--format", "json"])
        self.assertEqual(code, 1, out)
        payload = __import__("json").loads(out)
        self.assertEqual(payload["status"], "fail")
        self.assertGreaterEqual(payload["checked"], 3)
        self.assertTrue(any(f["state"] == "hover" for r in payload["results"] for f in r["fails"]))


if __name__ == "__main__":
    unittest.main()
