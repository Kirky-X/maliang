"""style-ledger.py:跨项目外观账本(指纹提取 / add / check / list)。

profile.json 先验、项目 feedback 账本三分),指纹从 DESIGN.md 结构化
token 提取(不解析 HTML)。
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

sl = load("style-ledger.py")

DESIGN = """---
version: alpha
name: LedgerSample
description: 指纹提取样例
colors:
  primary: "#5b7cfa"
  surface-base: "#f7f8fa"
  text-primary: "#1A1D21"
typography:
  display: "Fraunces", serif
  body: "PingFang SC", sans-serif
---

## Overview

**P1** 示例。
"""

DESIGN_DARK = DESIGN.replace('#5b7cfa', '#3D5EDB').replace(
    '#f7f8fa', '#141413').replace('Fraunces', 'Space Grotesk').replace(
    '"PingFang SC", sans-serif', '"Noto Sans SC", sans-serif')

DESIGN_NO_FM = "# 只有正文,没有 frontmatter\n"


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = sl.main(argv)
    return code, buf.getvalue()


class TestExtractFingerprint(unittest.TestCase):
    def test_extracts_fields(self):
        fp = sl.extract_fingerprint(DESIGN)
        self.assertIsNotNone(fp)
        self.assertEqual(fp["primary"], "#5b7cfa")
        self.assertEqual(fp["bg"], "#f7f8fa")
        self.assertEqual(fp["bg_class"], "浅底")
        self.assertIn("Fraunces", fp["font_display"])
        self.assertIn("PingFang", fp["font_body"])
        self.assertIn("#5b7cfa", fp["desc"])

    def test_dark_bg_classified(self):
        fp = sl.extract_fingerprint(DESIGN_DARK)
        self.assertEqual(fp["bg_class"], "深底")

    def test_no_frontmatter_returns_none(self):
        self.assertIsNone(sl.extract_fingerprint(DESIGN_NO_FM))


class TestAddListCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-sl-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.home = os.path.join(self.tmp, "home")
        self.design = os.path.join(self.tmp, "DESIGN.md")
        with open(self.design, "w", encoding="utf-8") as fh:
            fh.write(DESIGN)
        self.design2 = os.path.join(self.tmp, "DESIGN2.md")
        with open(self.design2, "w", encoding="utf-8") as fh:
            fh.write(DESIGN_DARK)

    def _argv(self, *rest):
        return ["--home", self.home] + list(rest)

    def test_add_appends_jsonl(self):
        code, out = run_main(
            self._argv("add", "--project", "alpha", self.design))
        self.assertEqual(code, 0, out)
        path = os.path.join(self.home, "style-ledger.jsonl")
        rows = [json.loads(x) for x in
                open(path, encoding="utf-8").read().splitlines() if x.strip()]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["project"], "alpha")
        self.assertEqual(rows[0]["fp"]["primary"], "#5b7cfa")
        self.assertIn("ts", rows[0])

    def test_add_missing_file_exits_2(self):
        code, out = run_main(
            self._argv("add", "--project", "x", os.path.join(self.tmp, "no.md")))
        self.assertEqual(code, 2)
        self.assertIn("没能", out)

    def test_add_no_frontmatter_exits_2(self):
        bad = os.path.join(self.tmp, "bad.md")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write(DESIGN_NO_FM)
        code, out = run_main(self._argv("add", "--project", "x", bad))
        self.assertEqual(code, 2)
        self.assertIn("frontmatter", out)

    def test_check_empty_ledger_not_blocking(self):
        # 不应报: 账本缺失/为空 = 无历史可查,显式提示后退 0(不阻塞,同 huashu)
        code, out = run_main(self._argv("check"))
        self.assertEqual(code, 0)
        self.assertIn("为空", out)

    def test_check_reports_repeats(self):
        # 应报: 两次交付同底色同字体 → 重复项点名,提示主动避开
        run_main(self._argv("add", "--project", "alpha", self.design))
        run_main(self._argv("add", "--project", "beta", self.design))
        code, out = run_main(self._argv("check"))
        self.assertEqual(code, 0)
        self.assertIn("反复出现", out)
        self.assertIn("#f7f8fa", out)

    def test_check_no_repeat_quiet(self):
        run_main(self._argv("add", "--project", "alpha", self.design))
        run_main(self._argv("add", "--project", "beta", self.design2))
        code, out = run_main(self._argv("check"))
        self.assertEqual(code, 0)
        self.assertNotIn("反复出现", out)

    def test_check_last_limits_scope(self):
        # 不应报: --last 1 只看最近一条,单条构不成重复
        run_main(self._argv("add", "--project", "alpha", self.design))
        run_main(self._argv("add", "--project", "beta", self.design))
        code, out = run_main(self._argv("check", "--last", "1"))
        self.assertEqual(code, 0)
        self.assertNotIn("反复出现", out)

    def test_list_shows_projects(self):
        run_main(self._argv("add", "--project", "alpha", self.design))
        code, out = run_main(self._argv("list"))
        self.assertEqual(code, 0)
        self.assertIn("alpha", out)
        self.assertIn("#5b7cfa", out)


class TestReviewFixes(unittest.TestCase):
    """2026-10-31 审查修复回归:键族误配 / 回显消毒 / 递归断路 / 行守卫 / 幂等。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-slf-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.home = os.path.join(self.tmp, "home")

    def _write_design(self, text, name="D.md"):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def test_canonical_palette_no_cross_key_mismatch(self):
        # 架构 H1 回归:canonical 色板形状(bg-primary/text-primary,无裸
        # primary)不得把文字色/背景色记成主色
        design = """---
colors:
  bg-primary: "#FFFFFF"
  bg-base: "#F7F8FA"
  text-primary: "#1A1D21"
  border-base: "#E5E7EB"
typography:
  body: "Inter"
---
"""
        fp = sl.extract_fingerprint(design)
        self.assertIsNotNone(fp)
        # bg-primary 是明暗模式的页面底色,bg 取它正确(审查实测口径);
        # 关键不变量:文字色不得记成主色,主色在无裸 primary 键时留空
        self.assertEqual(fp["bg"], "#ffffff")
        self.assertNotEqual(fp["primary"], "#1a1d21",
                            "text-primary 不得记成主色")

    def test_sanitize_strips_control_chars(self):
        # 安全 M1 回归:frontmatter 值里的 ESC/换行不得原样回显
        self.assertEqual(sl.sanitize("x\x1b[31mred\x1b[0m"), "x[31mred[0m")
        self.assertEqual(sl.sanitize("a\nb"), "ab")

    def test_add_echo_is_sanitized(self):
        design = """---
colors:
  primary: "#5B7CFA"
typography:
  display: "x\x1b[31mpwn\x1b[0m"
---
"""
        path = self._write_design(design)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = sl.main(["--home", self.home, "add", "--project", "p", path])
        self.assertEqual(code, 0)
        self.assertNotIn("\x1b", buf.getvalue())

    def test_recursive_alias_no_crash(self):
        # 安全 L1 回归:YAML 递归别名不得让 add 崩溃出 traceback
        design = "---\ncolors: &c {a: *c}\n---\n"
        path = self._write_design(design)
        buf, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            code = sl.main(["--home", self.home, "add", "--project", "p", path])
        self.assertIn(code, (0, 2))
        self.assertNotIn("Traceback", err.getvalue())

    def test_non_dict_ledger_row_skipped(self):
        # 安全 L3 回归:合法 JSON 但非账本对象的行跳过不崩
        os.makedirs(self.home)
        ledger = os.path.join(self.home, "style-ledger.jsonl")
        with open(ledger, "w", encoding="utf-8") as fh:
            fh.write('["not", "a", "dict"]\n')
            fh.write('{"no": "fp"}\n')
            fh.write(json.dumps({"ts": "t", "project": "p", "path": "x",
                                 "fp": {"desc": "d", "bg": None,
                                        "primary": None, "palette": [],
                                        "font_display": None,
                                        "font_body": None}}) + "\n")
        code, out = run_main(["--home", self.home, "list"])
        self.assertEqual(code, 0)
        self.assertIn("p", out)

    def test_add_idempotent_same_project_path(self):
        # 架构 L4 回归:同 (project, path) 重复 add 不追加重复行
        design = self._write_design(DESIGN)
        run_main(["--home", self.home, "add", "--project", "alpha", design])
        code, out = run_main(["--home", self.home, "add", "--project", "alpha", design])
        self.assertEqual(code, 0)
        self.assertIn("未重复记账", out)
        ledger = os.path.join(self.home, "style-ledger.jsonl")
        self.assertEqual(len([x for x in open(ledger, encoding="utf-8")
                              if x.strip()]), 1)

    def test_empty_frontmatter_yields_none(self):
        # 安全 L2 回归:无 colors/typography 的 frontmatter 不产垃圾指纹
        self.assertIsNone(sl.extract_fingerprint(
            "---\nname: only-name\ndescription: x\n---\n正文"))


if __name__ == "__main__":
    unittest.main()
