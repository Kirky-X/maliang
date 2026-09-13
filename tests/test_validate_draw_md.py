"""validate-draw-md.py 全部 13 项检查的 fixture 单元测试。

双列 fixture 约定(对齐 impeccable TDD 流程):每项检查至少 1 个"应报"用例
+ 1 个"不应报"用例;规则实现为纯函数,直接以合成行列表调用。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

vdm = load("validate-draw-md.py")

import unittest  # noqa: E402

VALID_TOKENS = {
    "surface-base", "surface-card", "text-primary", "text-secondary",
    "color-primary", "font-size-md", "radius-md", "radius-lg",
    "spacing-md", "z-index-overlay", "surface-dark", "icon-home",
}
VALID_SLUGS = {"button", "icon", "input", "link", "card", "navigation", "list", "text"}

PARAM_TABLE_HEADER = ["| 参数        | 值 | 说明 |", "| --- | --- | --- |"]


def _rows_to_lines(rows):
    return PARAM_TABLE_HEADER + rows


def _sev(results):
    """把检查结果归并为 {(severity, rule-ish message 前缀)} 计数。"""
    return [(r[0], r[3]) for r in results]


class TestTokenReferences(unittest.TestCase):
    def test_dangling_token_reports_error(self):
        # 应报: 引用未定义 token
        lines = ["| 背景颜色 | {surface-ghost} | 说明 |"]
        results = vdm.check_token_references("ui/home.md", lines, VALID_TOKENS)
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_defined_token_passes(self):
        # 不应报: token 已定义
        lines = ["| 背景颜色 | {surface-card} | 说明 |"]
        results = vdm.check_token_references("ui/home.md", lines, VALID_TOKENS)
        self.assertEqual(results, [])

    def test_action_line_placeholders_skipped(self):
        # 不应报: action 行的 {input-value} 是 URL 模板参数,非 token
        lines = ["| action | tap=→ui/search.md?q={input-value}; db=无 | 说明 |"]
        results = vdm.check_token_references("ui/home.md", lines, VALID_TOKENS)
        self.assertEqual(results, [])


class TestColorLiterals(unittest.TestCase):
    def test_hex_literal_reports_error(self):
        for bad in ["| 背景颜色 | #FFFFFF |", "| 字体颜色 | rgba(0,0,0,0.8) |"]:
            results = vdm.check_color_literals("ui/home.md", [bad])
            self.assertTrue(any(r[0] == "ERROR" for r in results), bad)

    def test_token_ref_passes(self):
        # 不应报: token 引用
        results = vdm.check_color_literals("ui/home.md", ["| 背景颜色 | {surface-card} |"])
        self.assertEqual(results, [])

    def test_separator_row_skipped(self):
        # 不应报: 表格分隔行
        results = vdm.check_color_literals("ui/home.md", ["| --- | --- | --- |"])
        self.assertEqual(results, [])


class TestComponentSlugs(unittest.TestCase):
    def test_missing_type_row_warns(self):
        lines = _rows_to_lines(["| 宽度 width | 375px | |"])
        results = vdm.check_component_slugs("ui/home.md", lines, VALID_SLUGS)
        self.assertTrue(any(r[0] == "WARN" for r in results))

    def test_blockquote_type_accepted_for_dual_table(self):
        # 不应报: 双列对比表用表前引用块标注(draw-md.md 规范)
        lines = [
            "> **组件类型**:`button` + `icon` + `text`(组合)",
            "",
        ] + _rows_to_lines([
            "| 图标风格 | 填充(filled) | 线性(stroke) |",
            "| 字体颜色 | `{color-brand-primary}` | `{color-text-secondary}` |",
        ])
        results = vdm.check_component_slugs("organisms/dock.md", lines, VALID_SLUGS)
        self.assertEqual(results, [])

    def test_blockquote_invented_slug_reports_error(self):
        # 应报: 引用块内的自创 slug 同样受检
        lines = [
            "> **组件类型**:`search-bar`(自创)",
            "",
        ] + _rows_to_lines(["| 图标风格 | 填充 | 线性 |"])
        results = vdm.check_component_slugs("organisms/dock.md", lines, VALID_SLUGS)
        self.assertTrue(any(r[0] == "ERROR" and "search-bar" in r[3] for r in results))

    def test_invented_slug_reports_error(self):
        # 应报: 自创 slug search-bar(未传 vocab_slugs,保持契约禁止语义)
        lines = _rows_to_lines(["| 组件类型 | `search-bar` | 自创 |"])
        results = vdm.check_component_slugs("ui/home.md", lines, VALID_SLUGS)
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_vocabulary_slug_allowed(self):
        # 不应报: vocabulary 登记的模式 slug(chart-line)在传入 vocab_slugs 时放行
        # (审计 P0-3: framework 45 类无图表类,术语库区块模式需合法表达)
        lines = _rows_to_lines(["| 组件类型 | `chart-line` | 图表 |"])
        results = vdm.check_component_slugs(
            "ui/dashboard.md", lines, VALID_SLUGS, {"chart-line", "chart-bar"})
        self.assertEqual(results, [])

    def test_invented_slug_still_reports_with_vocab(self):
        # 应报: 传入 vocab_slugs 后,术语库未登记的自创 slug 仍报 error
        lines = _rows_to_lines(["| 组件类型 | `mega-widget` | 自创 |"])
        results = vdm.check_component_slugs(
            "ui/home.md", lines, VALID_SLUGS, {"chart-line"})
        self.assertTrue(any(r[0] == "ERROR" and "mega-widget" in r[3] for r in results))

    def test_valid_combo_passes(self):
        # 不应报: 合法 slug 组合
        lines = _rows_to_lines(["| 组件类型 | `input` + `icon` | 搜索框 |"])
        results = vdm.check_component_slugs("ui/home.md", lines, VALID_SLUGS)
        self.assertEqual(results, [])


class TestFrontmatter(unittest.TestCase):
    GOOD_FM = (
        "---\nname: home\ndescription: 首页\nbackground: \"{surface-base}\"\n"
        "updated: 2026-06-30\nversion: 1.0.0\ncomponents: [button]\n---\n正文"
    )

    def test_complete_frontmatter_passes(self):
        # 不应报: 全字段 + token 背景
        results = vdm.check_frontmatter("ui/home.md", self.GOOD_FM)
        self.assertEqual(results, [])

    def test_missing_field_reports_error(self):
        text = self.GOOD_FM.replace("version: 1.0.0\n", "")
        results = vdm.check_frontmatter("ui/home.md", text)
        self.assertTrue(any("version" in r[3] for r in results))

    def test_literal_background_reports_error(self):
        # 应报: background 硬编码色值
        text = self.GOOD_FM.replace('"{surface-base}"', "#FFFFFF")
        results = vdm.check_frontmatter("ui/home.md", text)
        self.assertTrue(any("background" in r[3] for r in results))


class TestActionField(unittest.TestCase):
    def test_missing_action_reports_error(self):
        lines = _rows_to_lines(["| 组件类型 | `button` | |"])
        results = vdm.check_action_field("ui/home.md", lines)
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_action_present_passes(self):
        # 不应报: 含 action 行
        lines = _rows_to_lines([
            "| 组件类型 | `button` | |",
            "| action | tap=→ui/mine.md; state=按下高亮; db=无; api=无; long-press=无 | |",
        ])
        results = vdm.check_action_field("ui/home.md", lines)
        self.assertEqual(results, [])


class TestSectionOrder(unittest.TestCase):
    def test_wrong_order_warns(self):
        # 应报(warning): 首章非导航、末章非 dock
        lines = ["## 主体区块", "内容", "## 其他"]
        results = vdm.check_section_order("ui/home.md", lines)
        self.assertEqual(len([r for r in results if r[0] == "WARN"]), 2)

    def test_nav_then_dock_passes(self):
        # 不应报: 导航开头 + dock 结尾
        lines = ["## 顶部导航", "内容", "## 底部 dock"]
        results = vdm.check_section_order("ui/home.md", lines)
        self.assertEqual(results, [])


class TestSecondaryPages(unittest.TestCase):
    def test_flat_secondary_page_reports_error(self):
        # 应报: about.md 直接放 ui/ 根目录
        results = vdm.check_secondary_pages("ui/about.md")
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_nested_page_passes(self):
        # 不应报: 子目录嵌套 + 一级页面白名单
        self.assertEqual(vdm.check_secondary_pages("ui/setting/about.md"), [])
        self.assertEqual(vdm.check_secondary_pages("ui/home.md"), [])


class TestDarkModeCoverage(unittest.TestCase):
    def test_no_dark_coverage_warns(self):
        lines = ["| 背景颜色 | {surface-base} | |"]
        results = vdm.check_dark_mode_coverage("ui/home.md", lines)
        self.assertTrue(any(r[0] == "WARN" for r in results))

    def test_dark_token_passes(self):
        # 不应报: 引用 dark token
        lines = ["| 暗色背景 | {surface-dark} | |"]
        results = vdm.check_dark_mode_coverage("ui/home.md", lines)
        self.assertEqual(results, [])

    def test_dark_section_passes(self):
        # 不应报: 含暗色模式章节
        lines = ["## 暗色模式", "说明"]
        results = vdm.check_dark_mode_coverage("ui/home.md", lines)
        self.assertEqual(results, [])


def _interactive_table():
    return _rows_to_lines([
        "| 组件类型 | `button` | |",
        "| 宽度 width | 88px | |",
        "| 高度 height | 44px | |",
    ])


class TestAriaLabels(unittest.TestCase):
    def test_interactive_without_aria_reports(self):
        results = vdm.check_aria_labels("ui/home.md", _interactive_table())
        self.assertTrue(any("aria-label" in r[3] for r in results))

    def test_interactive_with_aria_passes(self):
        # 不应报: 含 aria-label 行
        lines = _interactive_table() + ["| aria-label | 提交订单 | |"]
        results = vdm.check_aria_labels("ui/home.md", lines)
        self.assertEqual(results, [])

    def test_container_component_skipped(self):
        # 不应报: 容器组件(navigation)不检查
        lines = _rows_to_lines(["| 组件类型 | `navigation` | |"])
        results = vdm.check_aria_labels("ui/home.md", lines)
        self.assertEqual(results, [])


class TestTouchTarget(unittest.TestCase):
    """触控目标分端判定:原生 <44 ERROR;Web/未知 <24 ERROR、24-43 WARN。

    期望同步说明(修复 P0 触控口径分裂):原先不分端一律 <44 判 ERROR,会误杀
    24-43px 的合规 Web 目标(WCAG 2.2 2.5.8 AA);现按 frontmatter platform
    分端,平台未声明按 Web/未知处理。
    """

    def test_small_clickable_native_reports_error(self):
        # 应报: 声明移动端平台(platform=harmony)时 32px < 44 触控区不足
        lines = _rows_to_lines([
            "| 组件类型 | `button` | |",
            "| 宽度 width | 32px | |",
            "| 高度 height | 32px | |",
        ])
        results = vdm.check_touch_target("ui/home.md", lines, platform="harmony")
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_web_24_to_43px_warns_not_error(self):
        # 应报(warning): Web/平台未知时 24-43px 判 WARN(Web 最低 24px 合规,推荐 44px)
        lines = _rows_to_lines([
            "| 组件类型 | `button` | |",
            "| 宽度 width | 32px | |",
            "| 高度 height | 32px | |",
        ])
        results = vdm.check_touch_target("ui/home.md", lines)
        self.assertTrue(any(r[0] == "WARN" for r in results))
        self.assertFalse(any(r[0] == "ERROR" for r in results))

    def test_web_below_24_reports_error(self):
        # 应报: Web 侧 20px 低于 WCAG 2.2 2.5.8 AA 下限
        lines = _rows_to_lines([
            "| 组件类型 | `icon` | |",
            "| 宽度 width | 20px | |",
            "| 高度 height | 20px | |",
        ])
        results = vdm.check_touch_target("ui/home.md", lines)
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_run_checks_reads_platform_frontmatter(self):
        # 应报: run_checks 从 frontmatter platform 字段取端型,native 32px 判 ERROR
        text = (
            "---\nname: x\ndescription: d\nbackground: \"{surface-base}\"\n"
            "updated: 2026-01-01\nversion: 1.0.0\ncomponents: [button]\n"
            "platform: harmony\n---\n"
        )
        lines = _rows_to_lines([
            "| 组件类型 | `button` | |",
            "| 宽度 width | 32px | |",
        ])
        results = vdm.run_checks("ui/home.md", text, lines, VALID_TOKENS,
                                 VALID_SLUGS, False)
        self.assertTrue(
            any(r[0] == "ERROR" and r[3] == "touch-target" for r in results))

    def test_44px_passes(self):
        # 不应报: 44px 达标(原生与 Web 两侧均合规)
        results = vdm.check_touch_target("ui/home.md", _interactive_table())
        self.assertEqual(results, [])

    def test_match_parent_passes(self):
        # 不应报: match-parent 非定值
        lines = _rows_to_lines([
            "| 组件类型 | `button` | |",
            "| 宽度 width | match-parent | |",
        ])
        results = vdm.check_touch_target("ui/home.md", lines)
        self.assertEqual(results, [])


class TestMotionDuration(unittest.TestCase):
    def test_over_400ms_reports_error(self):
        results = vdm.check_motion_duration("ui/home.md", ["duration: 500ms"])
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_400ms_boundary_passes(self):
        # 不应报: 400ms 恰好达标
        results = vdm.check_motion_duration("ui/home.md", ["duration: 400ms"])
        self.assertEqual(results, [])


class TestCardRadius(unittest.TestCase):
    def test_card_with_md_radius_reports_error(self):
        lines = _rows_to_lines([
            "| 组件类型 | `card` | |",
            "| 圆角 radius | {radius-md} | |",
        ])
        results = vdm.check_card_radius("ui/home.md", lines)
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_card_with_lg_radius_passes(self):
        # 不应报: 卡片用 radius-lg
        lines = _rows_to_lines([
            "| 组件类型 | `card` | |",
            "| 圆角 radius | {radius-lg} | |",
        ])
        results = vdm.check_card_radius("ui/home.md", lines)
        self.assertEqual(results, [])


class TestZIndex(unittest.TestCase):
    def test_literal_zindex_reports_error(self):
        results = vdm.check_z_index_literals("ui/home.md", ["z-index: 999"])
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_token_zindex_passes(self):
        # 不应报: z-index token 引用
        results = vdm.check_z_index_literals("ui/home.md", ["z-index: {z-index-overlay}"])
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
