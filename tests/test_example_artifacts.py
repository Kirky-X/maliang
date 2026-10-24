"""示例产物一致性守护(F12 补遗):Home.vue 与 preview HTML 是 home.md 的两条平行下游。

双份手抄维护已发生过 ≥7 处漂移(含死交互);本测试锁定两条纪律:
1. 两份产物中逐字共享的数据块(ICONS / entries / feed / tabs)必须保持一致——
   改任一份的数据必须同步另一份,否则此处 FAIL;
2. home.md 内容指纹钉在本文件——源页一改,两份产物就必须重新核对/再生成,
   并把指纹更新为新值(把「改了源忘了产物」从静默漂移变成显性失败)。

CSS 层两份产物存在**有意差异**(preview 设备壳的 padding-bottom、:root 超集变量),
已在两文件内注释声明,不做机械比对。
"""

import hashlib
import os
import re
import sys
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOME_MD = os.path.join(BASE, "examples", "ui-markdown", "ui", "home.md")
VUE = os.path.join(BASE, "examples", "element-plus", "views", "Home.vue")
PREVIEW = os.path.join(BASE, "examples", "preview", "preview_home_iphone15.html")

# home.md 的 SHA-256(2026-10-24 与两份产物核对一致后钉定)
HOME_MD_SHA256 = "ef63dc531f4e0f67a9973de977a6d1c6ea7d9ea7aaf0511a67a4a13d4f5e8f0f"


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _extract_block(text, name):
    """提取数据字面量块。两种声明形态:
    - `const NAME = {` / `const NAME = [`(Home.vue 顶层)
    - `NAME: {` / `NAME: [`(preview 的 data() 对象属性)
    花括号/方括号配平取整块。"""
    m = (re.search(r"const %s = (?:ref\()?([{\[])" % name, text)
         or re.search(r"(?m)^\s*%s: ([{\[])" % name, text))
    if not m:
        return None
    open_ch, close_ch = m.group(1), {"{": "}", "[": "]"}[m.group(1)]
    depth = 0
    for i in range(m.end() - 1, len(text)):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                return text[m.start():i + 1]
    return None


class TestArtifactDataSync(unittest.TestCase):
    def test_shared_data_blocks_identical(self):
        vue, prev = _read(VUE), _read(PREVIEW)
        for name in ("ICONS", "entries", "feed", "tabs"):
            bv, bp = _extract_block(vue, name), _extract_block(prev, name)
            self.assertIsNotNone(bv, f"Home.vue 缺 {name} 数据块")
            self.assertIsNotNone(bp, f"preview 缺 {name} 数据块")
            # 数据行逐字一致(剥掉声明行与行首缩进;两文件声明形态与缩进体系不同)
            norm = lambda b: [ln.strip() for ln in b.splitlines()[1:] if ln.strip()]
            self.assertEqual(norm(bv), norm(bp),
                             f"{name} 数据块在两份产物间漂移——改数据必须两份同步"
                             "(或消除双份,见 F12)")

    def test_home_md_fingerprint_fresh(self):
        current = hashlib.sha256(_read(HOME_MD).encode("utf-8")).hexdigest()
        self.assertEqual(
            current, HOME_MD_SHA256,
            "examples/ui-markdown/ui/home.md 已改动——Home.vue 与 preview_home_iphone15.html "
            "是它的两条下游产物,请核对/重新生成后把 tests/test_example_artifacts.py 的 "
            "HOME_MD_SHA256 更新为新指纹")


if __name__ == "__main__":
    unittest.main()
