"""detect-tells.py 的 cjk-font-chain 告警档测试。

锁定 dimensions/font.md「CJK 排印补丁」的 fallback 链序反模式:中文字体在链首
且后随西文命名族 = 西文字体永远轮不到出场(逐字符匹配语义)。告警档只报不拦,
豁免沿用 tell-exempt 同一套解析。
"""

import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

dt = load("audit.py")

BAD_CHAIN = ('<style>body { font-family: "PingFang SC", "SF Pro Text", '
             '-apple-system, sans-serif; }</style>')
GOOD_CHAIN = ('<style>body { font-family: "SF Pro Text", "PingFang SC", '
              '"Noto Sans SC", "Microsoft YaHei", -apple-system, sans-serif; }</style>')
CJK_ONLY = '<style>body { font-family: "PingFang SC", sans-serif; }</style>'
SYSTEM_HOOK_AFTER = ('<style>body { font-family: "Microsoft YaHei", -apple-system, '
                     'BlinkMacSystemFont, sans-serif; }</style>')
CJK_AFTER_LATIN = ('<style>body { font-family: "Inter", "Noto Sans SC", '
                   '"PingFang SC", sans-serif; }</style>')
DISPLAY_REFLEX = ('<style>@font-face { font-family: "Fraunces"; src: local("Fraunces"); }\n'
                  'h1 { font-family: "Fraunces", serif; }</style>')


class TestCjkFontChainWarning(unittest.TestCase):
    def test_cjk_first_with_latin_after_reports(self):
        warnings = dt.scan_advisory_tells(BAD_CHAIN, "a.html")
        self.assertEqual([w["rule"] for w in warnings], ["cjk-font-chain"])
        self.assertEqual(warnings[0]["severity"], "minor")

    def test_correct_chain_passes(self):
        self.assertEqual(dt.scan_advisory_tells(GOOD_CHAIN, "a.html"), [])

    def test_cjk_first_without_latin_passes(self):
        # 中文链首但后面只有泛型兜底,不构成「西文被吃掉」签名
        self.assertEqual(dt.scan_advisory_tells(CJK_ONLY, "a.html"), [])

    def test_system_hook_after_cjk_not_latin(self):
        # -apple-system / BlinkMacSystemFont 是系统钩子,不算西文命名族
        self.assertEqual(dt.scan_advisory_tells(SYSTEM_HOOK_AFTER, "a.html"), [])

    def test_latin_first_cjk_after_passes(self):
        self.assertEqual(dt.scan_advisory_tells(CJK_AFTER_LATIN, "a.html"), [])

    def test_hard_finding_still_exits_1_with_warning(self):
        # 硬命中通道与告警档互不吞并:gradient-text 硬失败时告警同屏
        code, out = self._cli(BAD_CHAIN + '<h1 class="bg-clip-text">Hi</h1>')
        self.assertEqual(code, 1)
        self.assertIn("cjk-font-chain", out)
        self.assertIn("gradient-text", out)

    def _cli(self, content):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "font.html")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = dt._main_tells([path])
            return code, buf.getvalue()


if __name__ == "__main__":
    unittest.main()
