"""validate-generated.py:token 零残留 / 颜色回溯 token.md / 组件白名单 /
SFC 结构与类名解析。用临时目录搭最小「生成码 + token.md + framework 文档」三件套。
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

vg = load("validate.py")

TOKEN_MD = """---
name: token
---

# token.md

## 1. 颜色(colors)

| token   | HEX     | 用途   |
| ------- | ------- | ------ |
| primary | #5B7CFA | 品牌主 |

## 2. 字体(typography)

| token               | 值   | 用途 |
| ------------------- | ---- | ---- |
| font-size-h3        | 16px | 小标题 |
"""

GOOD_VUE = """<!--
  由 draw-element 从 examples/ui-markdown/ui/home.md 生成
-->
<template>
  <div class="page">
    <el-button class="cta" type="primary">提交</el-button>
  </div>
</template>

<script setup>
import { ElMessage } from "element-plus";
const notify = () => ElMessage("ok");
</script>

<style>
:root { --color-brand-primary: #5B7CFA; }
.page { padding: 16px; color: var(--color-brand-primary); }
.cta { margin: 8px; }
</style>
"""


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = vg._main_generated(argv)
    return code, buf.getvalue()


class TestValidateGenerated(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-vg-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

        # framework 白名单:index.md + element/ 下的组件文档
        fw = os.path.join(self.tmp, "framework")
        os.makedirs(os.path.join(fw, "element", "button"))
        os.makedirs(os.path.join(fw, "element", "message"))
        with open(os.path.join(fw, "index.md"), "w", encoding="utf-8") as fh:
            fh.write("# 框架资源总览\n")
        with open(os.path.join(fw, "element", "button", "component.md"), "w", encoding="utf-8") as fh:
            fh.write("# Button\n\n```html\n<el-button type=\"primary\">\n```\n")
        with open(os.path.join(fw, "element", "message", "component.md"), "w", encoding="utf-8") as fh:
            fh.write("# Message\n\n`ElMessage('ok')`\n")
        self.fw_index = os.path.join(fw, "index.md")

        self.token_file = os.path.join(self.tmp, "token.md")
        with open(self.token_file, "w", encoding="utf-8") as fh:
            fh.write(TOKEN_MD)

        self.target = os.path.join(self.tmp, "views")
        os.makedirs(self.target)

    def _write(self, name, content):
        path = os.path.join(self.target, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return path

    def _run(self, fmt="json"):
        argv = [self.target, "--token-file", self.token_file,
                "--framework-index", self.fw_index, "--format", fmt]
        return run_main(argv)

    def test_clean_generated_code_passes(self):
        self._write("Home.vue", GOOD_VUE)
        code, out = self._run()
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(out), [])

    def test_color_literal_not_in_token_md_reports(self):
        # 应报: #FF00AA 不在 token.md 里(G04 硬编码视觉值)
        self._write("Bad.vue", GOOD_VUE.replace("#5B7CFA", "#FF00AA"))
        code, out = self._run()
        self.assertEqual(code, 1)
        findings = json.loads(out)
        self.assertTrue(any(f["rule"] == "gen.color-literal" for f in findings))

    def test_token_residue_reports(self):
        self._write("Residue.vue", GOOD_VUE.replace(">提交<", ">{color-primary}<"))
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "gen.token-residue" for f in json.loads(out)))

    def test_unknown_component_tag_reports(self):
        self._write("Weird.vue", GOOD_VUE.replace("<el-button", "<el-widget"))
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "gen.component-whitelist" for f in json.loads(out)))

    def test_unknown_el_import_reports(self):
        self._write("Weird.vue", GOOD_VUE.replace("ElMessage", "ElMadeUp"))
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "gen.component-whitelist" for f in json.loads(out)))

    def test_missing_style_section_reports(self):
        broken = GOOD_VUE.split("<style>")[0]
        self._write("NoStyle.vue", broken)
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "gen.sfc-structure" for f in json.loads(out)))

    def test_missing_provenance_comment_reports(self):
        self._write("NoComment.vue", GOOD_VUE.replace("<!--\n  由 draw-element 从 examples/ui-markdown/ui/home.md 生成\n-->\n", ""))
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "gen.sfc-structure" for f in json.loads(out)))

    def test_undefined_class_reports(self):
        self._write("Orphan.vue", GOOD_VUE.replace('class="page"', 'class="page ghost"'))
        code, out = self._run()
        self.assertEqual(code, 1)
        findings = json.loads(out)
        self.assertTrue(any(f["rule"] == "gen.class-undefined" and "ghost" in f["message"]
                            for f in findings))

    def test_missing_target_exits_2(self):
        code, out = run_main([os.path.join(self.tmp, "nowhere"),
                              "--token-file", self.token_file,
                              "--framework-index", self.fw_index])
        self.assertEqual(code, 2)
        self.assertIn("没能检查", out)

    def test_missing_token_file_exits_2(self):
        self._write("Home.vue", GOOD_VUE)
        code, out = run_main([self.target, "--token-file", os.path.join(self.tmp, "nope.md"),
                              "--framework-index", self.fw_index])
        self.assertEqual(code, 2)
        self.assertIn("token.md 不存在", out)


class TestDangerousApi(unittest.TestCase):
    """检查 6 注入面(G46):执行面 API 无条件 error;HTML 绑定面 warn。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-vg6-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        fw = os.path.join(self.tmp, "framework")
        os.makedirs(os.path.join(fw, "element", "button"))
        os.makedirs(os.path.join(fw, "element", "message"))
        with open(os.path.join(fw, "index.md"), "w", encoding="utf-8") as fh:
            fh.write("# 框架资源总览\n")
        with open(os.path.join(fw, "element", "button", "component.md"), "w", encoding="utf-8") as fh:
            fh.write("# Button\n\n```html\n<el-button type=\"primary\">\n```\n")
        with open(os.path.join(fw, "element", "message", "component.md"), "w", encoding="utf-8") as fh:
            fh.write("# Message\n\n`ElMessage('ok')`\n")
        self.fw_index = os.path.join(fw, "index.md")
        self.token_file = os.path.join(self.tmp, "token.md")
        with open(self.token_file, "w", encoding="utf-8") as fh:
            fh.write(TOKEN_MD)
        self.target = os.path.join(self.tmp, "views")
        os.makedirs(self.target)

    def _write_and_run(self, content):
        with open(os.path.join(self.target, "Home.vue"), "w", encoding="utf-8") as fh:
            fh.write(content)
        return run_main([self.target, "--token-file", self.token_file,
                         "--framework-index", self.fw_index, "--format", "json"])

    def test_eval_reports_error(self):
        # 应报: eval() 是执行面,与数据来源无关,一律 error
        code, out = self._write_and_run(
            GOOD_VUE.replace("const notify = () => ElMessage(\"ok\");",
                             "const notify = () => eval(\"ElMessage('ok')\");"))
        self.assertEqual(code, 1)
        findings = json.loads(out)
        self.assertTrue(any(f["rule"] == "gen.dangerous-api" and f["severity"] == "ERROR"
                            for f in findings))

    def test_javascript_url_reports_error(self):
        code, out = self._write_and_run(
            GOOD_VUE.replace("<el-button", "<el-button data-x=\"javascript:alert(1)\""))
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "gen.dangerous-api"
                            for f in json.loads(out)))

    def test_v_html_binding_warns_not_errors(self):
        # 应报(warn): v-html 绑定是 HTML 注入面;本地常量绑定可过但须留痕,
        # 来源判定在 G46 门禁层——脚本层不无条件拦截(示例产物合法使用此形态)
        code, out = self._write_and_run(
            GOOD_VUE.replace('<el-button class="cta" type="primary">提交</el-button>',
                             '<el-button class="cta" type="primary" v-html="iconSvg">提交</el-button>'))
        self.assertEqual(code, 0)
        findings = json.loads(out)
        self.assertTrue(any(f["rule"] == "gen.dangerous-api" and f["severity"] == "WARN"
                            for f in findings))

    def test_commented_api_not_flagged(self):
        # 不应报: 注释里的说明文字不是实现
        code, out = self._write_and_run(
            GOOD_VUE.replace("</script>",
                             "// 禁止 eval( 与 v-html= 的说明注释\n</script>"))
        self.assertEqual(code, 0)
        self.assertFalse(any(f["rule"] == "gen.dangerous-api"
                             for f in json.loads(out)))


if __name__ == "__main__":
    unittest._main_generated()
