"""verify-interactive.py:三信号(死状态契约 / 惰性 / 隐形状态)+ 豁免 + UNMEASURED。

无浏览器时浏览器用例自动跳过;有浏览器时四个 fixture 各验一个信号。
"""

import contextlib
import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

vi = load("verify-interactive.py")
vs = vi.vs

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "verify_interactive")
BROWSER = vs.find_browser()
NO_BROWSER_REASON = "本机没有 Chrome/Chromium,浏览器用例跳过(UNMEASURED 路径仍受测)"


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = vi.main(argv)
    return code, buf.getvalue()


class TestUnmeasuredPaths(unittest.TestCase):
    def test_missing_target_exits_2(self):
        code, out = run_main([os.path.join(FIXTURES, "no-such.html")])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)

    def test_missing_browser_exits_2(self):
        code, out = run_main([
            os.path.join(FIXTURES, "dead_contract_fail.html"),
            "--browser", "/nonexistent/chrome-binary",
        ])
        self.assertEqual(code, 2)
        self.assertIn("没找到浏览器", out)


@unittest.skipUnless(BROWSER, NO_BROWSER_REASON)
class TestBrowserSignals(unittest.TestCase):
    def test_dead_state_contract_fails(self):
        # 信号 A:aria-pressed 声明了却没兑现 → exit 1
        code, out = run_main([os.path.join(FIXTURES, "dead_contract_fail.html")])
        self.assertEqual(code, 1, out)
        self.assertIn("[A dead]", out)

    def test_live_contract_passes(self):
        code, out = run_main([os.path.join(FIXTURES, "live_contract_pass.html")])
        self.assertEqual(code, 0, out)
        self.assertNotIn("[A dead]", out)

    def test_invisible_state_fails(self):
        # 信号 C:aria-checked 翻转但外观没变 → exit 1
        code, out = run_main([os.path.join(FIXTURES, "invisible_state_fail.html")])
        self.assertEqual(code, 1, out)
        self.assertIn("[C invisible]", out)

    def test_inert_is_advisory_and_demo_state_exempt(self):
        # 信号 B:普通静态按钮只 advisory;data-demo-state 的控件完全跳过
        code, out = run_main([
            os.path.join(FIXTURES, "inert_advisory_and_demo_state.html")])
        self.assertEqual(code, 0, out)
        self.assertIn("[B inert]", out)
        self.assertNotIn("[A dead]", out)
        self.assertIn("点击 1 个控件", out)  # 2 个候选里豁免掉 1 个

    def test_advisory_flag_downgrades_a_and_c(self):
        code, out = run_main([
            os.path.join(FIXTURES, "dead_contract_fail.html"), "--advisory"])
        self.assertEqual(code, 0, out)
        self.assertIn("ADVISORY", out.upper())
        self.assertIn("[A dead]", out)

    def test_json_format_shape(self):
        code, out = run_main([
            os.path.join(FIXTURES, "dead_contract_fail.html"), "--format", "json"])
        self.assertEqual(code, 1, out)
        payload = json.loads(out)
        self.assertEqual(payload["status"], "fail")
        self.assertTrue(payload["dead"])


if __name__ == "__main__":
    unittest.main()
