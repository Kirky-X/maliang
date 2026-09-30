"""design_md_to_token_md.py 的 frontmatter 解析测试(两条路径须一致)。

背景:2026-09 吸收 token 溯源(design-md Phase 0d 决策表 + token 行尾 `# D-P<n>-<m>` 注释)后,
PyYAML 路径会正确丢弃注释,但 PyYAML 缺席时的缩进降级路径会把注释吃进标量
(`primary` 变成 `"#212121" # D-P1-1`),并把 `headline-lg: # D-P2-1` 误判成标量而非子块,
导致无 PyYAML 环境下导出的 token.md 全线失真。故用等价性断言守住降级路径。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

d2t = load("design_md_to_token_md.py")

import unittest  # noqa: E402

FRONTMATTER = """version: alpha
name: Trace
colors:
  primary: "#212121" # D-P1-1
  tertiary: "#2563EB" # D-P1-1 全屏至多一处
  neutral: "#F5F5F5" # no-decision: 继承品牌规范
typography:
  headline-lg: # D-P2-1
    fontFamily: Inter
    fontSize: 48px
spacing:
  md: 16px # D-P3-1
components:
  button-primary: # D-P1-3
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.md}"
"""


class TestTokenProvenanceComments(unittest.TestCase):
    def test_strip_comment_keeps_hash_inside_quotes(self):
        self.assertEqual(d2t._strip_comment('  primary: "#212121" # D-P1-1'),
                         '  primary: "#212121"')
        self.assertEqual(d2t._strip_comment('  primary: "#212121"'), '  primary: "#212121"')

    def test_strip_comment_handles_escaped_quote_before_trailing_comment(self):
        # `\"` 是转义引号:不闭合字符串,行尾注释要正确剥离。
        self.assertEqual(d2t._strip_comment('  label: "say \\"hi\\"" # D-P1-1'),
                         '  label: "say \\"hi\\""')
        # 值内的 ` #`(转义引号之后)不得被当成注释而截断标量。
        self.assertEqual(d2t._strip_comment('  label: "a\\" # b"'),
                         '  label: "a\\" # b"')
        # `\\` 转义单元整体消费后,后随的 `"` 正常闭合引号,行尾注释照剥
        # (原断言把闭合引号误写作 `\"`,构成未闭合字符串——任何一致的
        # 扫描器都无法在保住上一条 `\"` 语义的同时满足它,故修正字面量)。
        self.assertEqual(d2t._strip_comment('  path: "C:\\\\tmp" # 注释'),
                         '  path: "C:\\\\tmp"')

    def test_fallback_parses_escaped_quote_scalar_with_provenance(self):
        parsed = d2t.parse_frontmatter_indent(
            'components:\n  label: "say \\"hi\\"" # D-P1-1\n'
        )
        self.assertEqual(parsed["components"]["label"], 'say "hi"')

    def test_fallback_matches_pyyaml_on_provenance_comments(self):
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML 不可用,无对照路径")
        self.assertEqual(d2t.parse_frontmatter(FRONTMATTER),
                         d2t.parse_frontmatter_indent(FRONTMATTER))

    def test_fallback_keeps_nested_map_key_as_map(self):
        parsed = d2t.parse_frontmatter_indent(FRONTMATTER)
        self.assertEqual(parsed["typography"]["headline-lg"]["fontSize"], "48px")
        self.assertEqual(parsed["components"]["button-primary"]["backgroundColor"],
                         "{colors.primary}")

    def test_fallback_drops_comment_from_scalar_values(self):
        parsed = d2t.parse_frontmatter_indent(FRONTMATTER)
        self.assertEqual(parsed["colors"]["primary"], "#212121")
        self.assertEqual(parsed["spacing"]["md"], "16px")

    def test_provenance_annotated_frontmatter_is_parseable_by_both_paths(self):
        """带溯源注释的 DESIGN.md 两条路径都不得抛错,且都拿到完整结构。"""
        for parse in (d2t.parse_frontmatter, d2t.parse_frontmatter_indent):
            data = parse(FRONTMATTER)
            self.assertEqual(set(data), {"version", "name", "colors", "typography",
                                         "spacing", "components"})
            self.assertEqual(data["colors"]["tertiary"], "#2563EB")


if __name__ == "__main__":
    unittest.main()
