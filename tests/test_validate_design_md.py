"""validate-design-md.py:V1 悬空 / V2 孤儿 / V3 空原则 + no-decision 占比 +
token.md 派生一致性。用临时目录搭最小 DESIGN.md(+token.md) 双件套。
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

vd = load("validate-design-md.py")

GOOD_DESIGN = """---
version: alpha
name: Sample
description: 测试用设计系统
decisions:
  - id: D-P1-1
    decision: 深度策略用 borders-only
    rationale: 后台工具要密度
    date: 2026-01-15
  - id: D-P2-1
    decision: 正文优先
    rationale: 阅读场景
    date: 2026-01-15
  - id: D-P3-1
    decision: 圆角克制
    rationale: 与密度一致
    date: 2026-01-15
colors:
  primary: "#1A1C1E" # D-P1-1
  secondary: "#6C7278" # no-decision: 继承品牌规范
typography:
  body-md: # D-P2-1
    fontFamily: Public Sans
    fontSize: 16px
rounded:
  sm: 4px # D-P3-1
spacing:
  md: 16px # D-P3-1
components:
  button-primary: # D-P1-1
    backgroundColor: "{colors.primary}"
---

## Overview

**P1** 用边界而非投影。
**P2** 排版以正文为先。
**P3** 圆角克制。
"""

GOOD_TOKEN = """# token.md

## 1. 颜色(colors)

| token     | HEX     | 用途 |
| --------- | ------- | ---- |
| primary   | #1A1C1E | 主色 |
| secondary | #6C7278 | 次色 |

## 2. 字体(typography)

| token              | 值   | 用途 |
| ------------------ | ---- | ---- |
| font-size-body-md  | 16px | 正文 |

## 5. 圆角(radius)

| token      | 值   | 用途   |
| ---------- | ---- | ------ |
| radius-sm  | 4px  | 小圆角 |
"""


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = vd.main(argv)
    return code, buf.getvalue()


class TestValidateDesignMd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-vd-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.design = os.path.join(self.tmp, "DESIGN.md")
        with open(os.path.join(self.tmp, "token.md"), "w", encoding="utf-8") as fh:
            fh.write(GOOD_TOKEN)

    def _write_design(self, content):
        with open(self.design, "w", encoding="utf-8") as fh:
            fh.write(content)

    def _run(self, fmt="json"):
        return run_main([self.design, "--format", fmt])

    def _rules(self, out):
        payload = json.loads(out)
        return [f["rule"] for f in payload["findings"]]

    def test_clean_design_md_passes(self):
        self._write_design(GOOD_DESIGN)
        code, out = self._run()
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(out)["findings"], [])

    def test_dangling_provenance_reports_v1(self):
        self._write_design(GOOD_DESIGN.replace("# D-P1-1", "# D-P1-9", 1))
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertIn("design-md.dangling-provenance", self._rules(out))

    def test_orphan_token_reports_v2(self):
        self._write_design(GOOD_DESIGN.replace(
            '  secondary: "#6C7278" # no-decision: 继承品牌规范',
            '  secondary: "#6C7278"'))
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertIn("design-md.orphan-token", self._rules(out))

    def test_empty_principle_reports_v3(self):
        # P3 没有任何 token 指向它(rounded/spacing 改指 P1)
        broken = (GOOD_DESIGN
                  .replace("  sm: 4px # D-P3-1", "  sm: 4px # D-P1-1")
                  .replace("  md: 16px # D-P3-1", "  md: 16px # D-P1-1"))
        self._write_design(broken)
        code, out = self._run()
        self.assertEqual(code, 1)
        payload = json.loads(out)
        self.assertTrue(any(f["rule"] == "design-md.empty-principle" and "P3" in f["message"]
                            for f in payload["findings"]))

    def test_token_md_drift_reports(self):
        with open(os.path.join(self.tmp, "token.md"), "a", encoding="utf-8") as fh:
            fh.write("\n| brand-novel | #FF00AA | 漂移色 |\n")
        self._write_design(GOOD_DESIGN)
        code, out = self._run()
        self.assertEqual(code, 1)
        self.assertIn("design-md.token-untraceable", self._rules(out))

    def test_no_decision_ratio_warns(self):
        # 两个 token 键里 1 个 no-decision → 50% > 1/3;同时 V2 应为 0
        text = GOOD_DESIGN.replace(
            '  primary: "#1A1C1E" # D-P1-1',
            '  primary: "#1A1C1E" # no-decision: 继承').replace(
            '  button-primary: # D-P1-1', '  button-primary: # no-decision: 按组件库')
        self._write_design(text)
        code, out = self._run()
        payload = json.loads(out)
        self.assertTrue(any(w["rule"] == "design-md.no-decision-ratio" for w in payload["warnings"]))
        # 告警不改变退出码(canonical:0=看了没问题,允许 warning)
        self.assertEqual(code, 1 if payload["findings"] else 0)

    def test_explicit_missing_token_file_exits_2(self):
        self._write_design(GOOD_DESIGN)
        code, out = run_main([self.design, "--token-file", os.path.join(self.tmp, "nope.md")])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)

    def test_missing_design_md_exits_2(self):
        code, out = run_main([os.path.join(self.tmp, "nope.md")])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)

    def test_no_frontmatter_is_unmeasured(self):
        self._write_design("# 没有 frontmatter 的 DESIGN\n")
        code, out = self._run()
        self.assertEqual(code, 2)
        self.assertIn("unmeasured", out)  # json 模式下用 status 字段表达


class TestDataFloorBinding(unittest.TestCase):
    """交叉 5:data-floor 绑定表机械化子集。

    无绑定表 = 不触发(判型归 G29 人工);有绑定表时结构违规 ERROR
    (空格/非法写入方/integration 缺 exists_today),day 台词标记缺失 WARN
    (写法变体不误杀)。
    """

    GOOD_DESIGN = """---
version: alpha
name: Ledger
description: 数据型样例
decisions:
  - id: D-P1-1
    decision: 状态句式
    rationale: 台账域
    date: 2026-01-15
colors:
  primary: "#1A1C1E" # D-P1-1
---

## Overview

**P1** 数据说话。

## 绑定表

| 字段 | 读什么 | 写入方 | 何时写 | 第一天空数据时 | 断连/跳过日 |
| --- | --- | --- | --- | --- | --- |
| streak | 连续天数 | system(存记录时写) | 保存跟进记录时 | day 1 只索要一条记录 | 显示「上次记录 · N 天前」 |
| today_total | 今日合计 | derived(自记录求和) | 读时计算 | day 2 回显首条规律 | 禁把昨天的数当今日 |

### 冷启动台词

- day 1:记下第一笔,解锁连续天数。
- day 2:这是你第一条规律。
- day 7:本周节奏已经出来了。
"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-vd5-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.design = os.path.join(self.tmp, "DESIGN.md")

    def _write_design(self, text):
        with open(self.design, "w", encoding="utf-8") as fh:
            fh.write(text)

    def _run_json(self):
        code, out = run_main([self.design, "--format", "json"])
        return code, json.loads(out) if code != 2 else {"warnings": []}

    def test_clean_binding_passes(self):
        self._write_design(self.GOOD_DESIGN)
        code, data = self._run_json()
        self.assertEqual(code, 0, data)
        rules = [w["rule"] for w in data["warnings"]]
        self.assertNotIn("design-md.binding-day-missing", rules)

    def test_no_binding_table_noop(self):
        # 不应报: 无绑定表 = 无数据型 hook 声明,交叉 5 不触发
        self._write_design(GOOD_DESIGN)
        code, data = self._run_json()
        self.assertEqual(code, 0)
        rules = [f["rule"] for f in data["findings"]]
        self.assertFalse(any(r.startswith("design-md.binding") for r in rules))

    def test_empty_cell_reports_error(self):
        self._write_design(self.GOOD_DESIGN.replace(
            "| today_total | 今日合计 | derived(自记录求和) | 读时计算 | day 2 回显首条规律 | 禁把昨天的数当今日 |",
            "| today_total | 今日合计 | derived(自记录求和) |  | day 2 回显首条规律 | 禁把昨天的数当今日 |"))
        code, data = self._run_json()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "design-md.binding-empty-cell"
                            for f in data["findings"]))

    def test_bad_writer_reports_error(self):
        self._write_design(self.GOOD_DESIGN.replace(
            "system(存记录时写)", "自动化流程"))
        code, data = self._run_json()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "design-md.binding-writer"
                            for f in data["findings"]))

    def test_integration_without_exists_today_reports(self):
        self._write_design(self.GOOD_DESIGN.replace(
            "| streak | 连续天数 | system(存记录时写) | 保存跟进记录时 | day 1 只索要一条记录 | 显示「上次记录 · N 天前」 |",
            "| quota | API 用量 | integration(计量服务) | 回调时 | day 1 只索要一条记录 | 显示「上次记录 · N 天前」 |"))
        code, data = self._run_json()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["rule"] == "design-md.binding-integration"
                            for f in data["findings"]))

    def test_integration_with_exists_today_passes(self):
        self._write_design(self.GOOD_DESIGN.replace(
            "| quota | API 用量 | integration(计量服务) | 回调时 | day 1 只索要一条记录 | 显示「上次记录 · N 天前」 |",
            "| quota | API 用量 | integration(计量服务,exists_today=true) | 回调时 | day 1 只索要一条记录 | 显示「上次记录 · N 天前」 |"))
        code, data = self._run_json()
        self.assertEqual(code, 0, data)

    def test_missing_day_marker_warns(self):
        # day 7 台词缺失 → WARN(不拦),提示对齐标记写法
        self._write_design(self.GOOD_DESIGN.replace(
            "- day 7:本周节奏已经出来了。\n", ""))
        code, data = self._run_json()
        self.assertEqual(code, 0)
        self.assertTrue(any(w["rule"] == "design-md.binding-day-missing"
                            and "day 7" in w["message"]
                            for w in data["warnings"]))


if __name__ == "__main__":
    unittest.main()
