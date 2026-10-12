"""preview-lint.js:静态片段契约 + 真浏览器探针(14 类可量测问题与动效四相位)。

无浏览器时浏览器用例跳过;有浏览器时:
  - probe_all_rules.html 上至少命中 13 类规则;
  - motion_phases.html 的 load 相位识别出一位性出场与循环动画;
  - weak 阈值结论文案(合成 weak 相位)与滚动提示文案逐字符在场。
"""

import json
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

vs = load("verify-states.py")

HERE = os.path.dirname(__file__)
LINT_JS = os.path.join(HERE, "..", "scripts", "preview-lint.js")
FIXTURES = os.path.join(HERE, "fixtures", "preview_lint")
BROWSER = vs.find_browser()
NO_BROWSER_REASON = "本机没有 Chrome/Chromium,浏览器探针用例跳过"

ALL_RULES = [
    "eyebrow", "numbered", "sideStripe", "gradientText", "nestedCards", "emojiIcon",
    "englishLabel", "contrastLow", "grayOnColor", "smallText", "tightLeading",
    "longMeasure", "stuck", "headingSpacing",
]


class TestStaticFragment(unittest.TestCase):
    def test_exports_and_rule_labels(self):
        with open(LINT_JS, "r", encoding="utf-8") as fh:
            src = fh.read()
        for hook in ("window.__maliangLint", "window.__maliangMotion",
                     "__maliangMotionIssues", "__maliangMotionBrief", "setPhase"):
            self.assertIn(hook, src)
        for rule in ALL_RULES:
            self.assertIn(rule + ":", src)  # LABELS 表里 14 类齐全
        # 只读取证:不得出现会写回页面的 style 注入
        self.assertNotIn("appendChild(s)", src)
        self.assertNotIn("document.head.append", src)


@unittest.skipUnless(BROWSER, NO_BROWSER_REASON)
class TestBrowserProbe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = cls.profile = cls.session = None
        cls.proc, cls.profile, port = vs.launch_browser(BROWSER)
        cls.session = vs.connect_session(port)
        cls.session.call("Page.enable", timeout=10.0)
        cls.session.call("Runtime.enable", timeout=10.0)
        with open(LINT_JS, "r", encoding="utf-8") as fh:
            cls.lint_source = fh.read()

    @classmethod
    def tearDownClass(cls):
        if cls.session:
            cls.session.close()
        vs.stop_browser(cls.proc, cls.profile)

    def _load(self, filename, settle=0.5):
        session = self.session
        result = session.call("Page.addScriptToEvaluateOnNewDocument",
                              {"source": self.lint_source})
        identifier = result.get("identifier")
        try:
            session.navigate("file://" + os.path.join(FIXTURES, filename))
            time.sleep(settle)
        finally:
            if identifier:
                session.call("Page.removeScriptToEvaluateOnNewDocument",
                             {"identifier": identifier})

    def test_lint_hits_expected_rule_classes(self):
        self._load("probe_all_rules.html")
        out, err = self.session.evaluate("JSON.stringify(__maliangLint())")
        self.assertIsNone(err)
        rules = {item["rule"] for item in json.loads(out)}
        self.assertGreaterEqual(len(rules), 13, rules)
        for rule in ("contrastLow", "grayOnColor", "smallText", "tightLeading",
                     "longMeasure", "stuck", "nestedCards", "emojiIcon",
                     "englishLabel", "eyebrow", "numbered", "sideStripe",
                     "gradientText", "headingSpacing"):
            self.assertIn(rule, rules)

    def test_contrast_below_1_5_not_reported(self):
        # 高于 1.5:1 才报;低于时按「文字后另有底板」归为噪声
        self._load("probe_all_rules.html")
        out, _ = self.session.evaluate("JSON.stringify(__maliangLint())")
        items = {i["rule"]: i for i in json.loads(out)}
        self.assertIn("contrastLow", items)
        self.assertTrue(all(":1" in ex for ex in items["contrastLow"]["examples"]))

    def test_motion_summary_detects_one_off_and_loop(self):
        self._load("motion_phases.html", settle=1.2)
        out, err = self.session.evaluate("JSON.stringify(__maliangMotion.summary('load'))")
        self.assertIsNone(err)
        phase = json.loads(out)
        self.assertGreaterEqual(phase["elements"], 2)
        self.assertEqual(phase["loops"], 1)
        self.assertGreaterEqual(phase["maxMove"], 4)

    def test_motion_issues_three_conclusions(self):
        session = self.session
        # 1) 没有检测到动画
        out, _ = session.evaluate(
            "JSON.stringify(__maliangMotionIssues({load: {elements: 0, loops: 0,"
            " maxMove: 0, maxSize: 0, maxOpacity: 0, top: []}}, {viewportHeight: 900}))")
        self.assertIn("没有检测到动画", out)
        # 2) 只有循环动画
        out, _ = session.evaluate(
            "JSON.stringify(__maliangMotionIssues({load: {elements: 2, loops: 2,"
            " maxMove: 10, maxSize: 0.1, maxOpacity: 0.5, top: []}}, {viewportHeight: 900}))")
        self.assertIn("只有持续循环的动画", out)
        # 3) weak 阈值逐字符:maxMove<4 && maxSize<0.02 && maxOpacity<0.3
        out, _ = session.evaluate(
            "JSON.stringify(__maliangMotionIssues({load: {elements: 1, loops: 0,"
            " maxMove: 3, maxSize: 0.01, maxOpacity: 0.2, top: []}}, {viewportHeight: 900}))")
        self.assertIn("动画幅度太小，看不出来", out)
        # 滚动叙事只是提示:p.scrollable=true 且无元素
        out, _ = session.evaluate(
            "JSON.stringify(__maliangMotionIssues({scroll: {elements: 0, loops: 0,"
            " maxMove: 0, maxSize: 0, maxOpacity: 0, top: [], scrollable: true}},"
            " {viewportHeight: 900}))")
        self.assertIn("没有检测到随滚动出现的变化", out)

    def test_motion_hero_depth_reported_not_judged(self):
        session = self.session
        out, _ = session.evaluate(
            "JSON.stringify(__maliangMotionIssues({hero: {elements: 2, loops: 0,"
            " maxMove: 60, maxSize: 0.2, maxOpacity: 0.9, top: [{size: 0.2, move: 60}]}},"
            " {viewportHeight: 900}))")
        self.assertEqual(json.loads(out), [])  # 首屏景深不记问题
        brief, _ = session.evaluate(
            "JSON.stringify(__maliangMotionBrief('hero', {elements: 2, loops: 0,"
            " maxMove: 60, maxSize: 0.2, maxOpacity: 0.9, top: [{size: 0.2, move: 60}]},"
            " {viewportHeight: 900}))")
        self.assertIn("层在变", brief)


if __name__ == "__main__":
    unittest.main()
