"""extract-tokens.py:阶梯折叠 / 别名解析 / 主题重定义标注 / 框架管道隐藏 /
预算披露 / --grep 就地检索 / 退出码三态。
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

et = load("extract-tokens.py")

SITE_CSS = """:root {
  --color-brand-primary: #5B7CFA;
  --color-brand-secondary: var(--color-brand-primary);
  --surface-base: #F7F8FA;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --font-size-body: 14px;
  --tw-ring-offset-shadow: 0 0 #0000;
  --el-color-primary: #409EFF;
}
@media (prefers-color-scheme: dark) {
  :root { --surface-base: #141413; }
}
"""


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = et.main(argv)
    return code, buf.getvalue()


class TestPureFunctions(unittest.TestCase):
    def test_merge_uniq_records_overrides(self):
        seen, overrides = et.merge_uniq([
            ("a", "1px"), ("b", "2px"), ("a", "#fff"), ("a", "#000"),
        ])
        self.assertEqual(seen, {"a": "1px", "b": "2px"})
        self.assertEqual(overrides["a"], ["#fff", "#000"])

    def test_resolve_alias_chain(self):
        table = {"a": "var(--b)", "b": "var(--c)", "c": "16px"}
        self.assertEqual(et.resolve_alias("var(--a)", table), "16px")

    def test_resolve_alias_fallback_and_cycle(self):
        self.assertEqual(et.resolve_alias("var(--nope, 8px)", {}), "8px")
        self.assertEqual(et.resolve_alias("var(--a)", {"a": "var(--a)"}), "var(--a)")

    def test_is_noise_hides_framework_pipes(self):
        self.assertTrue(et.is_noise("tw-ring-offset-shadow", "0 0 #0000"))
        self.assertTrue(et.is_noise("el-color-primary", "#409EFF"))
        self.assertFalse(et.is_noise("color-brand-primary", "#5B7CFA"))


class TestDigest(unittest.TestCase):
    def _digest(self, budget=6000):
        pairs = et.extract_vars_from_css(SITE_CSS)
        seen, overrides = et.merge_uniq(pairs)
        return et.build_digest(seen, overrides, ["site.css"], "/tmp/x.json", budget)

    def test_numeric_scale_collapsed_to_one_line(self):
        digest, _dropped = self._digest()
        self.assertIn("--space-*: 1=4px 2=8px 3=12px", digest)

    def test_alias_resolved_to_terminal_value(self):
        digest, _ = self._digest()
        self.assertIn("--color-brand-secondary: #5B7CFA", digest)

    def test_theme_redefinition_marked(self):
        digest, _ = self._digest()
        self.assertIn("(redefined elsewhere, likely a theme)", digest)

    def test_framework_noise_hidden_with_count(self):
        digest, _ = self._digest()
        self.assertNotIn("--tw-ring-offset-shadow", digest)
        self.assertNotIn("--el-color-primary:", digest)
        self.assertIn("2 个框架管道或噪声变量已隐藏", digest)

    def test_budget_drops_are_disclosed(self):
        digest, dropped = self._digest(budget=120)
        self.assertGreater(dropped, 0)
        self.assertIn("预算", digest)
        self.assertIn("省略", digest)


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-et-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.css = os.path.join(self.tmp, "site.css")
        with open(self.css, "w", encoding="utf-8") as fh:
            fh.write(SITE_CSS)
        self.out = os.path.join(self.tmp, "vars.json")

    def test_extract_ok_writes_json_and_exit_0(self):
        code, out = run_main([self.css, "--output", self.out])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(self.out))
        with open(self.out, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        self.assertIn("--color-brand-primary", json.dumps(payload))

    def test_strict_escalates_budget_warning_to_1(self):
        code, _ = run_main([self.css, "--output", self.out, "--budget", "120", "--strict"])
        self.assertEqual(code, 1)

    def test_grep_reads_saved_json_without_rescan(self):
        run_main([self.css, "--output", self.out])
        code, out = run_main(["--grep", "space", "--output", self.out])
        self.assertEqual(code, 0)
        self.assertIn("--space-3: 12px", out)

    def test_missing_path_exits_2(self):
        code, out = run_main([os.path.join(self.tmp, "nope.css")])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)

    def test_no_variables_exits_2(self):
        plain = os.path.join(self.tmp, "plain.css")
        with open(plain, "w", encoding="utf-8") as fh:
            fh.write("body { color: red; }\n")
        code, out = run_main([plain])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)

    def test_no_paths_exits_2(self):
        code, out = run_main([])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)


if __name__ == "__main__":
    unittest.main()
