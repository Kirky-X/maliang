"""validate-draw-md.py 全部 23 项检查的 fixture 单元测试。

双列 fixture 约定(对齐 设计工艺库 TDD 流程):每项检查至少 1 个"应报"用例
+ 1 个"不应报"用例;规则实现为纯函数,直接以合成行列表调用。
16-21 为 2026-10 契约完备性补批(数值合理性/organisms 引用/frontmatter
components 与 pattern 校验/方向契约块/裸 token 名)+ dir=rtl 升级与
spec_version 取值。
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

    def test_vocabulary_slug_now_reports_with_pattern_hint(self):
        # 应报(2026-10 归一裁决):vocabulary 模式 slug 不再放行进组件类型——
        # pattern 字段 + 检查 19 已成为合法通道,原 P0-3 放行理由失效;
        # 消息须指路 pattern 字段
        lines = _rows_to_lines(["| 组件类型 | `chart-line` | 图表 |"])
        results = vdm.check_component_slugs(
            "ui/dashboard.md", lines, VALID_SLUGS, {"chart-line", "chart-bar"})
        self.assertTrue(any(
            r[0] == "ERROR" and "chart-line" in r[3] and "pattern" in r[3]
            for r in results))

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

    def test_spring_route_with_params_downgrades_to_warn(self):
        # 弹簧豁免: 显式 spring 路线 + damping/response 参数 → WARN 留痕
        line = ("| transition | motion-model: spring(response=0.4, damping=1.0), "
                "settle-cap 500ms | 弹簧无固定时长 |")
        results = vdm.check_motion_duration("ui/home.md", [line])
        self.assertTrue(any(r[0] == "WARN" for r in results))
        self.assertFalse(any(r[0] == "ERROR" for r in results))

    def test_spring_route_without_params_still_error(self):
        # 豁免条件不成立: 只写 spring 路线未给参数 → 仍 ERROR,提示补参数
        line = "| transition | motion-model: spring, 500ms | 缺参数 |"
        results = vdm.check_motion_duration("ui/home.md", [line])
        self.assertTrue(any(r[0] == "ERROR" for r in results))
        self.assertFalse(any(r[0] == "WARN" for r in results))

    def test_ease_spring_bezier_not_exempt(self):
        # ease-spring 是 cubic-bezier 近似(固定时长),不含 spring 调用形式,
        # 不得匹配豁免 → 500ms 仍 ERROR
        line = "| transition | 500ms ease-spring | 近似弹簧 |"
        results = vdm.check_motion_duration("ui/home.md", [line])
        self.assertTrue(any(r[0] == "ERROR" for r in results))
        self.assertFalse(any(r[0] == "WARN" for r in results))


class TestFixedWidthText(unittest.TestCase):
    def test_text_fixed_width_warns(self):
        # 应报(warn,ux-rules slug fixed-width-text §6): text 组件定宽,超长文本不鲁棒
        lines = _rows_to_lines([
            "| 组件类型 | `text` | |",
            "| 宽度 width | 200px | |",
        ])
        results = vdm.check_fixed_width_text("ui/home.md", lines)
        self.assertTrue(any(r[0] == "WARN" for r in results))
        self.assertFalse(any(r[0] == "ERROR" for r in results))

    def test_text_min_width_passes(self):
        # 不应报: min-/max- 是加固定边界,非定宽
        lines = _rows_to_lines([
            "| 组件类型 | `text` | |",
            "| 宽度 width | min-width: 120px | |",
        ])
        results = vdm.check_fixed_width_text("ui/home.md", lines)
        self.assertEqual(results, [])

    def test_text_match_parent_passes(self):
        # 不应报: match-parent 非定值
        lines = _rows_to_lines([
            "| 组件类型 | `text` | |",
            "| 宽度 width | match-parent | |",
        ])
        results = vdm.check_fixed_width_text("ui/home.md", lines)
        self.assertEqual(results, [])

    def test_non_text_component_skipped(self):
        # 不应报: 非 text 组件定宽不属本检查(button 定宽另行由触控检查管)
        lines = _rows_to_lines([
            "| 组件类型 | `button` | |",
            "| 宽度 width | 200px | |",
        ])
        results = vdm.check_fixed_width_text("ui/home.md", lines)
        self.assertEqual(results, [])


class TestPhysicalProperty(unittest.TestCase):
    def test_margin_left_warns(self):
        # 应报(warn,ux-rules slug physical-property §12): 物理方向属性应改逻辑属性
        for bad in ["| 外边距 | margin-left: 8px | |",
                    "| 内边距 | padding-right: 12px | |",
                    "| 边框 | border-left: 1px solid | |"]:
            results = vdm.check_physical_property("ui/home.md", [bad])
            self.assertTrue(any(r[0] == "WARN" for r in results), bad)
            self.assertFalse(any(r[0] == "ERROR" for r in results), bad)

    def test_text_align_left_warns(self):
        results = vdm.check_physical_property(
            "ui/home.md", ["| 对齐 | text-align: left | |"])
        self.assertTrue(any(r[0] == "WARN" for r in results))
        self.assertFalse(any(r[0] == "ERROR" for r in results))

    def test_logical_properties_pass(self):
        # 不应报: 逻辑属性
        for good in ["| 外边距 | margin-inline-start: 8px | |",
                     "| 对齐 | text-align: start | |"]:
            results = vdm.check_physical_property("ui/home.md", [good])
            self.assertEqual(results, [])

    def test_ltr_only_annotation_exempt(self):
        # 不应报: 行内 ltr-only 显式标注豁免
        results = vdm.check_physical_property(
            "ui/home.md", ["| 外边距 | margin-left: 8px (ltr-only) | 方向无关 |"])
        self.assertEqual(results, [])

    def test_run_checks_covers_new_rules(self):
        # run_checks 聚合层含 fixed-width-text / physical-property 两个新 rule
        text = (
            "---\nname: x\ndescription: d\nbackground: \"{surface-base}\"\n"
            "updated: 2026-01-01\nversion: 1.0.0\ncomponents: [text]\n---\n"
        )
        lines = _rows_to_lines([
            "| 组件类型 | `text` | |",
            "| 宽度 width | 200px | |",
            "| 外边距 | margin-left: 8px | |",
        ])
        results = vdm.run_checks("ui/home.md", text, lines, VALID_TOKENS,
                                 VALID_SLUGS, False)
        rules = {r[3] for r in results}
        self.assertIn("fixed-width-text", rules)
        self.assertIn("physical-property", rules)


class TestCardRadius(unittest.TestCase):
    def test_card_with_control_tier_radius_reports_error(self):
        # 卡片必须用卡片档 rounded/lg/xl;控件档 subtle、直角档 sharp、
        # 胶囊档 full 与已废弃旧词 radius-md 都不是卡片圆角
        for token in ("{radius-md}", "{radius-subtle}", "{radius-sharp}",
                      "{radius-full}"):
            lines = _rows_to_lines([
                "| 组件类型 | `card` | |",
                "| 圆角 radius | %s | |" % token,
            ])
            results = vdm.check_card_radius("ui/home.md", lines)
            self.assertTrue(any(r[0] == "ERROR" for r in results), token)

    def test_card_with_card_tier_radius_passes(self):
        # 不应报: 卡片档 rounded(主流)/lg(大卡)/xl(模态)
        for token in ("{radius-rounded}", "{radius-lg}", "{radius-xl}"):
            lines = _rows_to_lines([
                "| 组件类型 | `card` | |",
                "| 圆角 radius | %s | |" % token,
            ])
            results = vdm.check_card_radius("ui/home.md", lines)
            self.assertEqual(results, [], token)

    def test_non_card_component_radius_not_checked(self):
        # 非卡片组件(如 input)不受卡片档约束
        lines = _rows_to_lines([
            "| 组件类型 | `input` | |",
            "| 圆角 radius | {radius-subtle} | |",
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


class TestNumericSanity(unittest.TestCase):
    def test_negative_px_reports_error(self):
        # 应报: 负宽高/负间距不是物理合理值,此前逃过所有检查
        results = vdm.check_numeric_sanity("ui/home.md", ["| 宽度 | -100px |"])
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_oversize_px_reports_error(self):
        # 应报: 超出 4K 画布上限,疑为数量级笔误
        results = vdm.check_numeric_sanity("ui/home.md", ["| 间距 | 30000px |"])
        self.assertTrue(any(r[0] == "ERROR" for r in results))

    def test_normal_px_passes(self):
        # 不应报: 375px 常规 / 3840px 恰在上限 / 0.5px 细分割线
        for good in ["| 宽度 | 375px |", "| 画布 | 3840px |", "| 分割 | 0.5px |"]:
            self.assertEqual(
                vdm.check_numeric_sanity("ui/home.md", [good]), [], good)


class TestOrganismRefs(unittest.TestCase):
    def test_missing_organism_reports_error(self):
        # 应报: 引用的 organisms 组件文件不存在(此前写错文件名全绿通过)
        lines = ["引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)"]
        results = vdm.check_organism_refs(
            "ui/home.md", lines, {"organisms/dock.md"})
        self.assertTrue(any(
            r[0] == "ERROR" and "nav-bar" in r[3] for r in results))

    def test_existing_organism_passes(self):
        # 不应报: 引用目标在 organisms/ 集合内
        lines = ["引用 [`../organisms/nav-bar.md`](../organisms/nav-bar.md)"]
        self.assertEqual(
            vdm.check_organism_refs(
                "ui/home.md", lines, {"organisms/nav-bar.md"}),
            [])

    def test_none_set_skips(self):
        # 不应报: organisms/ 目录不存在时跳过(main 传 None)
        self.assertEqual(
            vdm.check_organism_refs(
                "ui/home.md", ["引用 organisms/x.md"], None),
            [])


class TestFmComponentsAndPattern(unittest.TestCase):
    def _fm(self, **repl):
        text = TestFrontmatter.GOOD_FM
        for old, new in repl.items():
            text = text.replace(old, new)
        return text

    def test_invented_fm_slug_reports_error(self):
        # 应报: frontmatter components 自创 slug(此前只查字段存在)
        text = self._fm(**{"components: [button]": "components: [button, mega-chip]"})
        results = vdm.check_fm_components(
            "ui/home.md", text, VALID_SLUGS)
        self.assertTrue(any(r[0] == "ERROR" and "mega-chip" in r[3]
                            for r in results))

    def test_vocab_slug_in_components_reports_error(self):
        # 应报(2026-10 归一): 术语库模式名进 components 与检查 3 同口径报 error
        text = self._fm(**{"components: [button]": "components: [button, chart-line]"})
        results = vdm.check_fm_components(
            "ui/home.md", text, VALID_SLUGS, {"chart-line"})
        self.assertTrue(any(r[0] == "ERROR" and "chart-line" in r[3]
                            for r in results))
        self.assertFalse(any(r[0] == "WARN" for r in results))

    def test_valid_fm_components_pass(self):
        results = vdm.check_fm_components(
            "ui/home.md", self._fm(), VALID_SLUGS)
        self.assertEqual(results, [])

    def test_pattern_invented_reports_error(self):
        # 应报: pattern 自创模式名(此前 pattern 字段零校验)
        text = self._fm(**{"components: [button]\n---": "components: [button]\npattern: [chart-line, mega-chart]\n---"})
        results = vdm.check_fm_pattern(
            "ui/home.md", text, {"chart-line"})
        self.assertTrue(any(r[0] == "ERROR" and "mega-chart" in r[3]
                            for r in results))

    def test_pattern_registered_passes(self):
        text = self._fm(**{"components: [button]\n---": "components: [button]\npattern: [chart-line]\n---"})
        self.assertEqual(
            vdm.check_fm_pattern("ui/home.md", text, {"chart-line"}), [])


class TestDirectionContract(unittest.TestCase):
    CONTRACT = [
        "**thesis**: 三秒内能出发",
        "**own-world**: 灰白底上的一张张白卡",
        "**first-viewport**: 搜索框 + 金刚区入口",
        "**signature-interaction**: 长按卡片弹分享菜单",
    ]

    def test_missing_fields_report_error(self):
        # 应报: 页面无方向契约块(draw-md MUST 项,示例页曾自身缺失)
        results = vdm.check_direction_contract(
            "ui/home.md", ["# 首页", "", "## 1. 顶部导航"])
        self.assertTrue(any(r[0] == "ERROR" and "thesis" in r[3]
                            for r in results))

    def test_full_contract_before_first_section_passes(self):
        # 不应报: 四字段在首个 ## 章节前以加粗字段名行呈现
        lines = ["# 首页(home)", ""] + self.CONTRACT + ["", "## 1. 顶部导航"]
        self.assertEqual(
            vdm.check_direction_contract("ui/home.md", lines), [])

    def test_contract_after_first_section_not_counted(self):
        # 应报: 契约写在首个 ## 之后不算——区域界定是检查的一部分
        lines = ["## 1. 顶部导航"] + self.CONTRACT
        results = vdm.check_direction_contract("ui/home.md", lines)
        self.assertTrue(any(r[0] == "ERROR" for r in results))


class TestBareTokenNames(unittest.TestCase):
    def test_bare_icon_in_value_cell_warns(self):
        # 应报(warn): 值列裸 icon 名逃逸悬空检查(示例金刚区曾现 3 个未定义图标)
        results = vdm.check_bare_token_names(
            "ui/home.md", ["| 图标 | icon-feed | 说明 |"])
        self.assertTrue(any(r[0] == "WARN" and "icon-feed" in r[3]
                            for r in results))

    def test_braced_reference_passes(self):
        self.assertEqual(
            vdm.check_bare_token_names(
                "ui/home.md", ["| 图标 | {icon-feed} | x |"]),
            [])

    def test_field_name_column_not_flagged(self):
        # 不应报: 只扫值列,字段名列 icon-right 不误报
        self.assertEqual(
            vdm.check_bare_token_names(
                "ui/home.md", ["| icon-right | {icon-search-filled} | |"]),
            [])

    def test_action_line_skipped(self):
        self.assertEqual(
            vdm.check_bare_token_names(
                "ui/home.md", ["| action | tap=icon-feed-page; db=无 | |"]),
            [])

    def test_backticked_bare_name_still_warns(self):
        # 应报: 反引号不豁免——`icon-feed` 同样是逃逸校验的裸名
        results = vdm.check_bare_token_names(
            "ui/home.md", ["| 图标 | `icon-feed` | 说明 |"])
        self.assertTrue(any(r[0] == "WARN" for r in results))

    def test_header_column_name_not_flagged(self):
        # 不应报: 表头列名(如 icon-left/icon-filled)是字段命名不是取值
        lines = [
            "| 顺序 | id | icon-left | target |",
            "| --- | --- | --- | --- |",
            "| 1 | settings | icon-settings | ui/x.md |",
        ]
        results = vdm.check_bare_token_names("ui/mine.md", lines)
        # 数据行的裸值应报,表头行不报——同名只报一次会失真,故按行独立
        self.assertTrue(any(r[0] == "WARN" and "icon-settings" in r[3]
                            for r in results))
        header_only = [
            "| 顺序 | id | icon-left | target |",
            "| --- | --- | --- | --- |",
            "| 1 | settings | {icon-settings} | ui/x.md |",
        ]
        self.assertEqual(
            vdm.check_bare_token_names("ui/mine.md", header_only), [])


class TestDirAndSpecVersion(unittest.TestCase):
    def test_rtl_escalates_physical_property_to_error(self):
        # 应报: 声明 dir=rtl 后物理属性从 WARN 升 ERROR(声明即承担硬门)
        results = vdm.check_physical_property(
            "ui/home.md", ["| 外边距 | margin-left: 8px | |"], rtl=True)
        self.assertTrue(any(r[0] == "ERROR" for r in results))
        self.assertFalse(any(r[0] == "WARN" for r in results))

    def test_invalid_dir_value_reports_error(self):
        text = TestFrontmatter.GOOD_FM.replace(
            "components: [button]\n", "components: [button]\ndir: vertical\n")
        results = vdm.check_frontmatter("ui/home.md", text)
        self.assertTrue(any(r[0] == "ERROR" and "dir" in r[3] for r in results))

    def test_valid_dir_passes(self):
        text = TestFrontmatter.GOOD_FM.replace(
            "components: [button]\n", "components: [button]\ndir: rtl\n")
        self.assertEqual(vdm.check_frontmatter("ui/home.md", text), [])

    def test_future_spec_version_warns(self):
        text = TestFrontmatter.GOOD_FM.replace(
            "components: [button]\n",
            "components: [button]\nspec_version: 2\n")
        results = vdm.check_frontmatter("ui/home.md", text)
        self.assertTrue(any(r[0] == "WARN" and "spec_version" in r[3]
                            for r in results))

    def test_current_spec_version_passes(self):
        text = TestFrontmatter.GOOD_FM.replace(
            "components: [button]\n",
            "components: [button]\nspec_version: 1\n")
        self.assertEqual(vdm.check_frontmatter("ui/home.md", text), [])


class TestMainExitCodes(unittest.TestCase):
    """main() 退出码三态断言(补批:此前仅一处 WARN 计数断言,退出码无守护)。"""

    def setUp(self):
        import shutil
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="maliang-vdm-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

        token_file = os.path.join(self.tmp, "token.md")
        with open(token_file, "w", encoding="utf-8") as fh:
            fh.write("| token | 值 |\n| --- | --- |\n| surface-base | #FFFFFF |\n")
        self.token_file = token_file

        fw = os.path.join(self.tmp, "framework.md")
        with open(fw, "w", encoding="utf-8") as fh:
            fh.write("# index\n\n| 组件类型 | 说明 |\n| --- | --- |\n| button | 按钮 |\n")
        self.framework_file = fw

        vocab = os.path.join(self.tmp, "vocabulary")
        os.makedirs(vocab)
        with open(os.path.join(vocab, "charts.md"), "w", encoding="utf-8") as fh:
            fh.write("# charts\n\n| 模式 | 说明 |\n| --- | --- |\n| `chart-line` | 折线 |\n")
        self.vocab_dir = vocab

        self.target = os.path.join(self.tmp, "ui-markdown")
        os.makedirs(os.path.join(self.target, "ui"))

    def _write_page(self, body_color):
        page = (
            "---\nname: home\ndescription: 首页\nbackground: \"{surface-base}\"\n"
            "updated: 2026-10-26\nversion: 1.0.0\ncomponents: [button]\n"
            "spec_version: 1\n---\n"
            "**thesis**: t\n**own-world**: w\n**first-viewport**: f\n"
            "**signature-interaction**: s\n\n"
            "## 1. 顶部导航\n\n"
            "| 参数 | 值 |\n| --- | --- |\n"
            "| 组件类型 | `button` |\n"
            "| 背景颜色 | " + body_color + " |\n"
            "| aria-label | 提交 |\n"
            "| action | tap=无; state=无; db=无; api=无; long-press=无 |\n"
        )
        with open(os.path.join(self.target, "ui", "home.md"),
                  "w", encoding="utf-8") as fh:
            fh.write(page)

    def _run(self, target=None):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            # main(argv) 按 argv[1:] 解析,首位是程序名——target 不可放 [0]
            return vdm.main([
                "validate-draw-md.py",
                target or self.target,
                "--token-file", self.token_file,
                "--framework-file", self.framework_file,
                "--vocabulary-dir", self.vocab_dir,
            ])

    def test_error_fixture_exits_1(self):
        # 应报: 悬空 token 引用 → 退出码 1(看了,有问题)
        self._write_page("{surface-ghost}")
        self.assertEqual(self._run(), 1)

    def test_clean_fixture_exits_0(self):
        self._write_page("{surface-base}")
        self.assertEqual(self._run(), 0)

    def test_missing_target_exits_2(self):
        # 应报: 目标目录不存在 → 退出码 2(没能检查,不得记为通过)
        self._write_page("{surface-base}")
        self.assertEqual(self._run(os.path.join(self.tmp, "nowhere")), 2)


class TestBreakpointsAndActionTargets(unittest.TestCase):
    """检查 22(breakpoints 形态)与检查 23(api=/db= 目标形态)。"""

    def _fm_with(self, extra):
        return TestFrontmatter.GOOD_FM.replace(
            "components: [button]\n", "components: [button]\n" + extra + "\n")

    def test_breakpoints_valid_passes(self):
        text = self._fm_with("breakpoints: [375, 768, 1024]")
        self.assertEqual(vdm.check_breakpoints("ui/home.md", text), [])

    def test_breakpoints_unsorted_reports(self):
        text = self._fm_with("breakpoints: [768, 375]")
        results = vdm.check_breakpoints("ui/home.md", text)
        self.assertTrue(any("升序" in r[3] for r in results))

    def test_breakpoints_out_of_range_reports(self):
        text = self._fm_with("breakpoints: [100, 768]")
        results = vdm.check_breakpoints("ui/home.md", text)
        self.assertTrue(any("越界" in r[3] for r in results))

    def test_breakpoints_duplicate_or_single_reports(self):
        text = self._fm_with("breakpoints: [768, 768]")
        self.assertTrue(any("重复" in r[3] for r in
                            vdm.check_breakpoints("ui/home.md", text)))
        text2 = self._fm_with("breakpoints: [768]")
        self.assertTrue(any("≥2" in r[3] for r in
                            vdm.check_breakpoints("ui/home.md", text2)))

    def test_breakpoints_absent_passes(self):
        self.assertEqual(
            vdm.check_breakpoints("ui/home.md", TestFrontmatter.GOOD_FM), [])

    def _action_table(self, action_value):
        return _rows_to_lines([
            "| 组件类型 | `list` | |",
            "| action | " + action_value + " | |",
        ])

    def test_api_shape_valid_passes(self):
        lines = self._action_table(
            "tap=→ui/feed.md; db=无; api=GET /api/feed?cursor=?; long-press=无")
        self.assertEqual(vdm.check_action_targets("ui/home.md", lines), [])

    def test_api_without_method_reports(self):
        # 应报: api= 自由散文(「调接口拿数据」)无映射锚
        lines = self._action_table(
            "tap=无; db=无; api=调接口拿数据; long-press=无")
        results = vdm.check_action_targets("ui/home.md", lines)
        self.assertTrue(any("METHOD /path" in r[3] for r in results))

    def test_db_without_identifier_reports(self):
        lines = self._action_table(
            "tap=无; db=保存用户设置; api=无; long-press=无")
        results = vdm.check_action_targets("ui/home.md", lines)
        self.assertTrue(any("表名标识符" in r[3] for r in results))

    def test_db_with_table_passes(self):
        lines = self._action_table(
            "tap=无; db=UPDATE user_settings SET last_tab=?; api=无")
        self.assertEqual(vdm.check_action_targets("ui/home.md", lines), [])

    def test_exempt_values_pass(self):
        # 不应报: 无 / 视功能 / 按页面声明 等豁免词(nav-bar 右侧按钮旧写法)
        for value in ("tap=无; db=视功能; api=视功能; long-press=无",
                      "tap=无; db=无; api=无",
                      "tap=按页面声明; db=无; api=无"):
            self.assertEqual(
                vdm.check_action_targets("ui/home.md", self._action_table(value)),
                [], value)


if __name__ == "__main__":
    unittest.main()
