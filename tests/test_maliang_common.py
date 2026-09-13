"""maliang_common.parse_frontmatter 单元测试(双列 fixture)。"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

mc = load("maliang_common.py")

import unittest  # noqa: E402


class TestParseFrontmatter(unittest.TestCase):
    def test_no_frontmatter_returns_empty(self):
        # 不应报: 无 frontmatter 的普通 markdown
        self.assertEqual(mc.parse_frontmatter("# 标题\n正文"), {})

    def test_simple_kv(self):
        fm = mc.parse_frontmatter("---\nname: home\ndescription: 首页\n---\n正文")
        self.assertEqual(fm["name"], "home")
        self.assertEqual(fm["description"], "首页")

    def test_inline_components_list(self):
        # 应解析为 list
        fm = mc.parse_frontmatter("---\ncomponents: [button, input, icon]\n---\n")
        self.assertEqual(fm["components"], ["button", "input", "icon"])

    def test_empty_components_list(self):
        fm = mc.parse_frontmatter("---\ncomponents: []\n---\n")
        self.assertEqual(fm["components"], [])

    def test_quoted_value_stripped(self):
        fm = mc.parse_frontmatter('---\nbackground: "{surface-base}"\n---\n')
        self.assertEqual(fm["background"], "{surface-base}")

    def test_multiline_string(self):
        text = "---\ndescription: >\n  第一行\n  第二行\n---\n"
        fm = mc.parse_frontmatter(text)
        self.assertEqual(fm["description"], "第一行\n第二行")


if __name__ == "__main__":
    unittest.main()
