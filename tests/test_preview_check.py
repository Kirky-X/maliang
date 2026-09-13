"""preview-check.py 检查的 fixture 单元测试。

双列 fixture:每项至少 1 个"应报" + 1 个"不应报"用例。
对比度数值用 WCAG 相对亮度公式手工验算的已知值断言。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

pc = load("preview-check.py")

import unittest  # noqa: E402


def _rules(results):
    return {r[2] for r in results}


def _run(text):
    parser = pc._parse_html(text)
    return pc.run_all_checks(text, "fixture.html")


GOOD_HTML = """<!DOCTYPE html>
<html><head><style>
:root {
  --color-text: #1A1B1E;
  --color-text-muted: #6B7280;
  --surface-base: #FFFFFF;
  --focus-ring: rgba(59,130,246,0.5);
}
body { background: var(--surface-base); color: var(--color-text); }
.btn { background: var(--surface-base); color: var(--color-text); }
.btn:hover { opacity: 0.9; }
.btn:active { transform: scale(0.97); }
.btn:focus-visible { box-shadow: 0 0 0 2px var(--focus-ring); }
.btn:disabled { color: var(--color-text-muted); }
input::placeholder { color: var(--color-text-muted); }
</style></head>
<body><main id="main"><button class="btn">提交订单</button>
<p>今日成交 2,847 单</p></main>
<a class="skip" href="#main">Skip to main content</a>
</body></html>
"""


class TestContrastMath(unittest.TestCase):
    """对比度公式本身:用可手工验算的已知值。"""

    def test_black_on_white_is_21(self):
        ratio = pc._contrast_ratio((0, 0, 0, 1), (255, 255, 255, 1))
        self.assertAlmostEqual(ratio, 21.0, places=1)

    def test_b0b0b0_on_white(self):
        # #B0B0B0 亮度 ≈ 0.4342 → (1.05)/(0.4842) ≈ 2.17
        ratio = pc._contrast_ratio((176, 176, 176, 1), (255, 255, 255, 1))
        self.assertAlmostEqual(ratio, 2.17, places=1)

    def test_alpha_composited_over_bg(self):
        # 半透明前景先合成再计算:rgba(0,0,0,0.5) on white ≈ #808080 → 3.99
        ratio = pc._contrast_ratio((0, 0, 0, 0.5), (255, 255, 255, 1))
        self.assertAlmostEqual(ratio, 3.99, places=1)

    def test_color_parsing(self):
        self.assertEqual(pc._color_to_rgba("#f00"), (255, 0, 0, 1))
        self.assertEqual(pc._color_to_rgba("#FF000080"), (255, 0, 0, 128 / 255.0))
        self.assertEqual(pc._color_to_rgba("rgba(0, 128, 0, 1)"), (0, 128, 0, 1.0))
        self.assertEqual(pc._color_to_rgba("white"), (255, 255, 255, 1))
        self.assertIsNone(pc._color_to_rgba("linear-gradient(to right, #fff, #000)"))


class TestContrastCheck(unittest.TestCase):
    def test_low_body_text_reports_error(self):
        # 应报: #b0b0b0 on #ffffff = 2.17 < 4.5
        html = "<style>body { background: #ffffff; color: #b0b0b0; }</style>"
        results = pc.check_5_3_contrast(html, pc._parse_html(html), "x.html")
        self.assertIn("contrast.low", _rules(results))

    def test_large_text_threshold_3_to_1(self):
        # #8b8b8b on white = 3.41:1 → 26px 大文本达标不报;
        # 同色若为正文(< 4.5)则应报 — 阈值区分生效
        html_large = ("<style>.title { font-size: 26px; color: #8b8b8b; "
                      "background: #ffffff; }</style>")
        results = pc.check_5_3_contrast(html_large, pc._parse_html(html_large), "x.html")
        self.assertNotIn("contrast.low", _rules(results))
        html_body = ("<style>.title { color: #8b8b8b; "
                     "background: #ffffff; }</style>")
        results_body = pc.check_5_3_contrast(html_body, pc._parse_html(html_body), "x.html")
        self.assertIn("contrast.low", _rules(results_body))

    def test_disabled_threshold_3_to_1(self):
        # 不应报: disabled 3.5:1 ≥ 3.0
        html = ("<style>button:disabled { color: #6b7280; "
                "background: #ffffff; }</style>")
        results = pc.check_5_3_contrast(html, pc._parse_html(html), "x.html")
        self.assertNotIn("contrast.low", _rules(results))

    def test_placeholder_low_reports(self):
        # 应报: placeholder 1.61:1
        html = ("<style>input::placeholder { color: #cccccc; "
                "background: #ffffff; }</style>")
        results = pc.check_5_3_contrast(html, pc._parse_html(html), "x.html")
        self.assertIn("contrast.low", _rules(results))

    def test_var_resolution_and_dark_media(self):
        # 不应报: var 链解析 + @media dark 内重声明均达标
        html = ("<style>:root { --fg: #1a1b1e; --bg: #ffffff; }"
                "body { color: var(--fg); background: var(--bg); }"
                "@media (prefers-color-scheme: dark) {"
                ":root { --fg: #f3f4f6; --bg: #1a1b1e; }"
                "body { color: var(--fg); background: var(--bg); }"
                "}</style>")
        results = pc.check_5_3_contrast(html, pc._parse_html(html), "x.html")
        self.assertNotIn("contrast.low", _rules(results))

    def test_unresolvable_skipped_not_reported(self):
        # 不应报: 渐变背景无法静态解析,跳过不猜测
        html = ("<style>.hero { color: #b0b0b0; background: "
                "linear-gradient(to right, #fff, #000); }</style>")
        results = pc.check_5_3_contrast(html, pc._parse_html(html), "x.html")
        self.assertNotIn("contrast.low", _rules(results))

    def test_pure_red_warns(self):
        html = "<style>.status { color: #ff0000; background: #ffffff; }</style>"
        results = pc.check_5_3_contrast(html, pc._parse_html(html), "x.html")
        self.assertIn("contrast.pure-red-green", _rules(results))


class TestStatesCheck(unittest.TestCase):
    def test_outline_none_without_alt_reports_error(self):
        # 应报: outline none 且无 :focus 替代
        html = "<style>.x { outline: none; }</style><button>按钮</button>"
        results = pc.check_5_7_states(html, pc._parse_html(html), "x.html")
        self.assertIn("state.focus-ring-removed", _rules(results))

    def test_focus_box_shadow_alt_passes(self):
        # 不应报: :focus-visible box-shadow 替代
        html = ("<style>.b { outline: none; }"
                ".b:focus-visible { box-shadow: 0 0 0 2px blue; }</style>"
                "<button>按钮</button>")
        results = pc.check_5_7_states(html, pc._parse_html(html), "x.html")
        self.assertNotIn("state.focus-ring-removed", _rules(results))

    def test_interactive_without_states_warns(self):
        html = "<style>.b { color: red; }</style><button>按钮</button>"
        results = pc.check_5_7_states(html, pc._parse_html(html), "x.html")
        rules = _rules(results)
        self.assertIn("state.no-hover", rules)
        self.assertIn("state.no-active", rules)

    def test_full_states_pass(self):
        # 不应报: hover/active/focus/disabled/tactile 齐全
        html = ("<style>.b:hover { opacity: .9; }"
                ".b:active { transform: scale(0.97); }"
                ".b:focus-visible { box-shadow: 0 0 0 2px blue; }"
                ".b:disabled { opacity: .5; }</style><button class=b>按钮</button>")
        results = pc.check_5_7_states(html, pc._parse_html(html), "x.html")
        self.assertEqual([r for r in results if r[0] == "ERROR"], [])
        self.assertNotIn("state.no-tactile", _rules(results))


class TestAiTells(unittest.TestCase):
    def test_lorem_reports(self):
        results = pc.check_5_1_ai_tells("<p>lorem ipsum dolor</p>", "x.html")
        self.assertTrue(any(r[2] == "ai-tells.lorem-ipsum" for r in results))

    def test_integer_fabrication_reports(self):
        # 应报: 营销文案整数凑数
        results = pc.check_5_1_ai_tells("<p>100+ Users 信任我们</p>", "x.html")
        self.assertTrue(any(r[2] == "ai-tells.integer-number" for r in results))

    def test_css_numeric_values_not_flagged(self):
        # 不应报: CSS 数值型属性与自定义属性合法使用整数
        html = ("<style>:root { --motion-duration-instant: 100ms; }"
                ".x { z-index: 100; width: 100px; transition-duration: 200ms; }</style>")
        results = pc.check_5_1_ai_tells(html, "x.html")
        self.assertEqual([r for r in results if r[2] == "ai-tells.integer-number"], [])

    def test_unsplash_random_reports(self):
        results = pc.check_5_1_ai_tells(
            '<img src="https://source.unsplash.com/random/800x600" alt="x">',
            "x.html")
        self.assertTrue(any(r[2] == "ai-tells.unsplash-random" for r in results))

    def test_real_data_passes(self):
        # 不应报: 带尾数的真实风数据
        results = pc.check_5_1_ai_tells("<p>2,847 位用户 · 99.97% 可用性</p>", "x.html")
        self.assertEqual(results, [])


class TestAriaLabelCheck(unittest.TestCase):
    """5.5.5 无文字按钮可访问名(ux-rules aria-labels)静态实现。"""

    def test_icon_button_without_name_reports(self):
        # 应报: 纯图标按钮无任何可访问名
        html = ("<body><button class=\"icon\">"
                "<svg viewBox=\"0 0 24 24\"><path d=\"M4 7h16\"/></svg>"
                "</button></body>")
        results = pc.check_5_5_accessibility(html, pc._parse_html(html), "x.html")
        self.assertIn("a11y.aria-label", _rules(results))

    def test_aria_label_attr_passes(self):
        # 不应报: aria-label 属性
        html = "<button aria-label=\"菜单\"><svg/></button>"
        results = pc.check_5_5_accessibility(html, pc._parse_html(html), "x.html")
        self.assertNotIn("a11y.aria-label", _rules(results))

    def test_bound_aria_label_passes(self):
        # 不应报: Vue 绑定 :aria-label(框架模板常见写法)
        html = "<button :aria-label=\"t.label\"><svg/></button>"
        results = pc.check_5_5_accessibility(html, pc._parse_html(html), "x.html")
        self.assertNotIn("a11y.aria-label", _rules(results))

    def test_visible_text_passes(self):
        # 不应报: 按钮有可见文本
        html = "<button>提交订单</button>"
        results = pc.check_5_5_accessibility(html, pc._parse_html(html), "x.html")
        self.assertNotIn("a11y.aria-label", _rules(results))

    def test_template_interpolation_passes(self):
        # 不应报: 模板插值文本(渲染后有内容)
        html = "<button><span>{{ e.label }}</span></button>"
        results = pc.check_5_5_accessibility(html, pc._parse_html(html), "x.html")
        self.assertNotIn("a11y.aria-label", _rules(results))

    def test_inner_img_alt_passes(self):
        # 不应报: 内嵌 img 提供非空 alt
        html = "<button><img src=\"x.png\" alt=\"下载\"></button>"
        results = pc.check_5_5_accessibility(html, pc._parse_html(html), "x.html")
        self.assertNotIn("a11y.aria-label", _rules(results))


class TestTokenIntegrity(unittest.TestCase):
    def test_token_residue_reports(self):
        results = pc.check_5_6_tokens("<p>color: {surface-card}</p>", "x.html")
        self.assertTrue(any(r[2] == "token.residue" for r in results))

    def test_root_var_defs_exempt(self):
        # 不应报: :root 内自定义属性定义是 token 解析合法落点
        html = "<style>:root { --color-primary: #409EFF; --font-size-md: 16px; }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertEqual([r for r in results if r[2] == "token.hardcoded-color"], [])

    def test_hardcoded_color_in_rule_reports(self):
        # 应报: 选择器内硬编码色值
        html = "<style>.btn { color: #FF0000; }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertTrue(any(r[2] == "token.hardcoded-color" for r in results))

    def test_root_non_var_decl_still_checked(self):
        # 应报: :root 内非自定义属性声明的硬编码色仍受检
        html = "<style>:root { color: #FF0000; }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertTrue(any(r[2] == "token.hardcoded-color" for r in results))

    def test_comment_color_exempt(self):
        # 不应报: CSS 注释中的色值是文档说明,非生效样式
        html = "<style>/* 主色取自 token.md 的 #5B7CFA */\n.btn { color: var(--color-brand-primary); }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertEqual([r for r in results if r[2] == "token.hardcoded-color"], [])

    def test_camelcase_var_reports(self):
        html = "<style>:root { --colorPrimary: #fff; }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertTrue(any(r[2] == "token.camelCase" for r in results))

    def test_hardcoded_font_size_reports(self):
        # 应报: 选择器内硬编码字号(5.6.3 接线)
        html = "<style>.x { font-size: 14px; }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertTrue(any(r[2] == "token.hardcoded-font-size" for r in results))

    def test_font_size_var_passes(self):
        # 不应报: :root token 定义与 var() 引用(5.6.3 的 :root 豁免)
        html = ("<style>:root { --font-size-md: 16px; } "
                ".x { font-size: var(--font-size-md); }</style>")
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertEqual(
            [r for r in results if r[2] == "token.hardcoded-font-size"], [])

    def test_hardcoded_spacing_warns(self):
        # 应报(warning): 硬编码间距(5.6.4 接线,静态代理降级 WARN)
        html = "<style>.x { padding: 13px; }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertTrue(any(
            r[0] == "WARN" and r[2] == "token.hardcoded-spacing" for r in results))

    def test_spacing_var_passes(self):
        # 不应报: 间距引用 token
        html = "<style>.x { padding: var(--spacing-md); }</style>"
        results = pc.check_5_6_tokens(html, "x.html")
        self.assertEqual(
            [r for r in results if r[2] == "token.hardcoded-spacing"], [])


class TestAnimation(unittest.TestCase):
    def test_long_duration_reports(self):
        results = pc.check_5_9_animation("<style>.x { transition: all 800ms; }</style>", "x.html")
        self.assertTrue(any(r[2] == "anim.duration" for r in results))

    def test_linear_easing_reports(self):
        results = pc.check_5_9_animation(
            "<style>.x { transition-timing-function: linear; }</style>", "x.html")
        self.assertTrue(any(r[2] == "anim.linear-easing" for r in results))

    def test_reasonable_animation_passes(self):
        # 不应报: 240ms + ease-out
        results = pc.check_5_9_animation(
            "<style>.x { transition: opacity 240ms ease-out; }</style>", "x.html")
        self.assertEqual(results, [])


class TestEndToEnd(unittest.TestCase):
    def test_good_html_zero_errors(self):
        # 不应报: 合规预览页全绿
        results = _run(GOOD_HTML)
        errors = [r for r in results if r[0] == "ERROR"]
        self.assertEqual(errors, [])

    def test_bad_html_flags_expected_rules(self):
        # 应报: 多项违规同时命中
        bad = """<html><head><style>
        body { background: #ffffff; color: #b0b0b0; }
        .x { outline: none; }
        </style></head><body><button>按钮</button></body></html>"""
        rules = _run(bad)
        found = {r[2] for r in rules}
        self.assertIn("contrast.low", found)
        self.assertIn("state.focus-ring-removed", found)


if __name__ == "__main__":
    unittest.main()
