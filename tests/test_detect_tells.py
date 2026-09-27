"""detect-tells.py 五条规则 + 豁免机制 + CLI 的 fixture 单元测试。

双列 fixture 约定(对齐既有测试):每条规则至少 1 个"应报"用例
+ 1 个"不应报"用例;规则实现为纯函数,直接以合成文本调用。
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

dt = load("detect-tells.py")


def findings_rules(findings):
    """把 finding 列表归并为 [(rule, line)] 便于断言。"""
    return [(f["rule"], f["line"]) for f in findings]


class TestGradientText(unittest.TestCase):
    def test_bg_clip_text_reports(self):
        text = '<h1 class="bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">Hi</h1>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertIn(("gradient-text", 1), findings_rules(findings))

    def test_background_clip_text_reports(self):
        text = ".hero { background-clip: text; color: transparent; }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertTrue(any(f["rule"] == "gradient-text" for f in findings))

    def test_plain_gradient_without_clip_passes(self):
        text = '<div class="bg-gradient-to-r from-purple-600 to-pink-500"></div>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])


class TestGlowShadow(unittest.TestCase):
    def test_box_shadow_glow_reports(self):
        text = ".card { box-shadow: 0 0 24px #7C3AED; }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertIn(("glow-shadow", 1), findings_rules(findings))

    def test_text_shadow_glow_reports(self):
        text = "h1 { text-shadow: 0 0 12px rgba(124, 58, 237, 0.6); }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertTrue(any(f["rule"] == "glow-shadow" for f in findings))

    def test_drop_shadow_glow_reports(self):
        text = ".logo { filter: drop-shadow(0 0 20px #22d3ee); }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertTrue(any(f["rule"] == "glow-shadow" for f in findings))

    def test_offset_shadow_passes(self):
        # 不应报: 有偏移的正常投影(0 4px 6px),非 0 偏移辉光
        text = ".card { box-shadow: 0 4px 6px rgba(0,0,0,0.1); }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])

    def test_small_blur_passes(self):
        text = ".btn { box-shadow: 0 0 4px rgba(0,0,0,0.2); }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])


class TestUniformRadius(unittest.TestCase):
    def test_four_same_radius_reports(self):
        text = "\n".join(["border-radius: 16px;"] * 4)
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], "uniform-radius")

    def test_three_same_radius_passes(self):
        text = "\n".join(["border-radius: 16px;"] * 3)
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])

    def test_mixed_radius_passes(self):
        # 不应报: 有层级分档(容器 16 / 控件 8 / 头像 full)
        text = ".card { border-radius: 16px; }\n.btn { border-radius: 8px; }\n.avatar { border-radius: 9999px; }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])

    def test_tailwind_uniform_reports(self):
        text = "\n".join(['<div class="rounded-2xl %d"></div>' % i for i in range(4)])
        findings, _ = dt.scan_text(text, "a.html")
        self.assertTrue(any(f["rule"] == "uniform-radius" for f in findings))

    def test_tailwind_full_passes(self):
        # 不应报: rounded-full 属平凡值(头像等),不在检测范围
        text = "\n".join(['<div class="rounded-full %d"></div>' % i for i in range(4)])
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])


class TestTrackingAbuse(unittest.TestCase):
    def test_three_tracking_tight_lines_report(self):
        text = "\n".join(['<h%d class="tracking-tight">T</h%d>' % (i + 1, i + 1) for i in range(3)])
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], "tracking-abuse")

    def test_two_lines_pass(self):
        text = '<h1 class="tracking-tight">A</h1>\n<h2 class="tracking-tight">B</h2>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])

    def test_css_negative_letter_spacing_reports(self):
        text = "\n".join(["letter-spacing: -0.02em;"] * 4)
        findings, _ = dt.scan_text(text, "a.css")
        self.assertTrue(any(f["rule"] == "tracking-abuse" for f in findings))

    def test_positive_letter_spacing_passes(self):
        text = "\n".join(["letter-spacing: 0.05em;"] * 5)
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])


class TestColoredBorder(unittest.TestCase):
    def test_saturated_hex_border_reports(self):
        text = ".card { border: 1px solid #E8452C; border-radius: 12px; }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertIn(("colored-border", 1), findings_rules(findings))

    def test_tailwind_colored_border_reports(self):
        text = '<div class="rounded-xl border-indigo-500">x</div>'
        findings, _ = dt.scan_text(text, "a.html")
        self.assertTrue(any(f["rule"] == "colored-border" for f in findings))

    def test_neutral_border_passes(self):
        # 不应报: 灰系描边(低饱和)与 Tailwind 中性色不在检测范围
        text = (".card { border: 1px solid #E5E7EB; }\n"
                '<div class="border-slate-300 rounded-lg">x</div>')
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])

    def test_black_border_passes(self):
        text = ".card { border: 2px solid #000000; }"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])


class TestExemptions(unittest.TestCase):
    def test_line_marker_above_exempts(self):
        text = ("<!-- tell-exempt: gradient-text, DESIGN.md 批准 -->\n"
                '<h1 class="bg-clip-text text-transparent">Hi</h1>')
        findings, exempted = dt.scan_text(text, "a.html")
        self.assertEqual(findings, [])
        self.assertEqual(exempted, 1)

    def test_trailing_marker_on_same_line_exempts(self):
        text = ".hero { background-clip: text; } /* tell-exempt: gradient-text */"
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])

    def test_file_scope_marker_exempts(self):
        text = ("/* tell-exempt: uniform-radius file */\n" + "border-radius: 16px;\n" * 4)
        findings, exempted = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])
        self.assertEqual(exempted, 1)

    def test_marker_for_other_rule_does_not_exempt(self):
        text = ("<!-- tell-exempt: glow-shadow -->\n"
                '<h1 class="bg-clip-text text-transparent">Hi</h1>')
        findings, _ = dt.scan_text(text, "a.html")
        self.assertEqual(len(findings), 1)

    def test_all_keyword_exempts_line(self):
        text = ("// tell-exempt: all, 品牌既有规范\n"
                ".card { border: 1px solid #E8452C; }")
        findings, _ = dt.scan_text(text, "a.css")
        self.assertEqual(findings, [])

    def test_parse_file_scope_suffix(self):
        file_scope, line_scope = dt.parse_exemptions(
            ["/* tell-exempt: colored-border file, gradient-text */"])
        self.assertIn("colored-border", file_scope)
        self.assertIn("gradient-text", line_scope)


class TestCli(unittest.TestCase):
    def _write(self, directory, name, content):
        path = os.path.join(directory, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return path

    def test_hit_file_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "bad.html", '<h1 class="bg-clip-text text-transparent">Hi</h1>')
            exit_code = dt.main([path])
            self.assertEqual(exit_code, 1)

    def test_clean_file_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "good.html", "<p>干净内容,无 tell。</p>")
            exit_code = dt.main([path])
            self.assertEqual(exit_code, 0)

    def test_json_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "bad.css", ".card { box-shadow: 0 0 30px #7C3AED; }")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exit_code = dt.main([path, "--format", "json"])
            self.assertEqual(exit_code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["files_scanned"], 1)
            self.assertEqual(len(payload["findings"]), 1)
            self.assertEqual(payload["findings"][0]["rule"], "glow-shadow")

    def test_directory_scan_and_skip_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = os.path.join(tmp, "src")
            node = os.path.join(tmp, "node_modules")
            os.makedirs(sub)
            os.makedirs(node)
            self._write(sub, "page.html", '<h1 class="bg-clip-text text-transparent">Hi</h1>')
            self._write(node, "vendor.js", ".x { border-radius: 8px; }")
            self._write(tmp, "notes.txt", "非代码文件不扫 bg-clip-text")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exit_code = dt.main([tmp])
            self.assertEqual(exit_code, 1)
            self.assertIn("page.html", buf.getvalue())
            self.assertNotIn("notes.txt", buf.getvalue())

    def test_missing_path_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "no-such-file.html")
            import contextlib
            import io
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                exit_code = dt.main([missing])
            self.assertEqual(exit_code, 2)
            self.assertIn("路径不存在", err.getvalue())


if __name__ == "__main__":
    unittest.main()
