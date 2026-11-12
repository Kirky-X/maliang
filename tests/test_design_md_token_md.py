"""design-md.py token-md 子命令回归:参数错位 bug 与字族派生缺口。

来源:e2e-friction-fixes 变更(friction ①④)。Red→Green 纪律:
T001/T003 用例先失败(_main_token_md len!=3 die / 缺 font-family 派生),T002/T004 修复转绿。
"""

import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

dm = load("design-md.py")

# 最小 DESIGN.md 夹具:colors 组 leaf 已用最终 token 名(color-*,T009 后的形态);
# typography 含带引号字族串(触发引号套引号缺陷形态);rounded/spacing 保持语义名。
FIXTURE = """---
name: e2e-fix-fixture
description: token-md 回归夹具
version: 1.0.0
colors:
  color-primary: "#1A1A2E" # D-P1-1
  color-neutral: "#F5F5F5" # D-P1-2
typography:
  display:
    fontFamily: '"Fraunces", "Noto Sans SC", sans-serif'
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
rounded:
  md: 8px # D-P3-1
spacing:
  md: 16px # D-P3-1
---

## Overview
- 高对比深色底承载品牌性格,强调色只出现在交互点 (# D-P1-1)
"""


def _write_fixture(td):
    src = os.path.join(td, "DESIGN.md")
    with open(src, "w", encoding="utf-8") as f:
        f.write(FIXTURE)
    return src


class TestTokenMdArgv(unittest.TestCase):
    """friction ①:dispatch 传 2 参数,_main_token_md 却要求 3(standalone 残留)。"""

    def test_two_args_succeeds(self):
        with tempfile.TemporaryDirectory() as td:
            src = _write_fixture(td)
            dst = os.path.join(td, "token.md")
            rc = dm.main(["token-md", src, dst])
            self.assertEqual(rc, 0)
            with open(dst, encoding="utf-8") as f:
                out = f.read()
            self.assertIn("color-primary", out, "colors 组 leaf 键应作为 token 名输出")

    def test_usage_message_has_current_script_name(self):
        err = StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stderr(err):
                dm.main(["token-md", "only-one-arg"])
        msg = err.getvalue()
        self.assertIn("design-md.py token-md", msg, "用法文案应指向合并入口")
        self.assertNotIn(
            "design_md_to_token_md.py", msg, "用法文案不应残留合并前老脚本名"
        )


class TestFontFamilyDerivation(unittest.TestCase):
    """friction ④:render_typography 缺 font-family token + 字族行引号套引号。"""

    def test_font_family_token_emitted(self):
        with tempfile.TemporaryDirectory() as td:
            src = _write_fixture(td)
            dst = os.path.join(td, "token.md")
            dm.main(["token-md", src, dst])
            with open(dst, encoding="utf-8") as f:
                out = f.read()
            self.assertIn(
                "font-family-display", out, "typography.display.fontFamily 应派生 font-family token"
            )

    def test_no_doubled_quote_in_family_line(self):
        with tempfile.TemporaryDirectory() as td:
            src = _write_fixture(td)
            dst = os.path.join(td, "token.md")
            dm.main(["token-md", src, dst])
            with open(dst, encoding="utf-8") as f:
                out = f.read()
            self.assertNotIn('""Fraunces', out, "字族行不应出现引号套引号")


class TestTokenMdArgparse(unittest.TestCase):
    """friction ⑨:token-md 裸 argv 无 --help(--help 被当文件名 die)。Red→Green:T003 先失败,T004 转绿。"""

    def test_help_exits_zero_with_usage(self):
        out = StringIO()
        with self.assertRaises(SystemExit) as cm:
            with redirect_stdout(out):
                dm.main(["token-md", "--help"])
        self.assertEqual(cm.exception.code, 0, "--help 应以 0 退出")
        self.assertIn("usage", out.getvalue().lower(), "--help 应输出用法")

    def test_extra_args_exit_two(self):
        err = StringIO()
        with self.assertRaises(SystemExit) as cm:
            with redirect_stderr(err):
                dm.main(["token-md", "a", "b", "c"])
        self.assertEqual(cm.exception.code, 2, "多余参数应走 argparse 标准 exit 2")


class TestDeriveDarkArgparse(unittest.TestCase):
    """friction ⑨:derive-dark mini parser 无 --help(--help 被当键值对走 ValueError)。Red→Green:T005 先失败,T006 转绿。"""

    def test_help_exits_zero_with_usage(self):
        out = StringIO()
        with self.assertRaises(SystemExit) as cm:
            with redirect_stdout(out):
                dm.main(["derive-dark", "--help"])
        self.assertEqual(cm.exception.code, 0, "--help 应以 0 退出")
        self.assertIn("usage", out.getvalue().lower(), "--help 应输出用法")

    def test_pairs_output_json(self):
        out = StringIO()
        with redirect_stdout(out):
            code = dm.main(["derive-dark",
                "Primary=#1A1C1E", "Secondary=#6C7278", "Accent=#C2551B",
                "Background=#FAF4E8", "Foreground=#16544A", "Card=#FFFFFF",
                "Muted=#E8E2D5", "Border=#D8D2C4", "Destructive=#B3261E",
                "Ring=#16544A"])
        self.assertEqual(code, 0, "正常 10 列行应派生成功")
        self.assertIn('"_mode_derivation"', out.getvalue(), "应输出 JSON 暗色板(含派生模式)")


if __name__ == "__main__":
    unittest.main()
