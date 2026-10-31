"""version-check.py:skill 版本检查的确定性逻辑(节流判定/版本比较/记录)。

SKILL.md「版本检查」节的流程主体落点——agent 只跑命令与 git ls-remote,
日期节流与 semver 比较进脚本(规则7:确定性逻辑不交给模型)。
"""

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

vc = load("version-check.py")


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = vc.main(argv)
    return code, buf.getvalue()


class TestDue(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-vc-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.state = os.path.join(self.tmp, "version-check")

    def _write_state(self, text):
        with open(self.state, "w", encoding="utf-8") as fh:
            fh.write(text)

    def test_no_state_is_due(self):
        code, out = run_main(["--state", self.state, "due"])
        self.assertEqual(code, 0)
        self.assertIn("due", out)

    def test_state_off_skips(self):
        self._write_state("off\n")
        code, out = run_main(["--state", self.state, "due"])
        self.assertEqual(code, 0)
        self.assertIn("skip:off", out)

    def test_recent_ok_skips(self):
        self._write_state(datetime.now().strftime("%Y-%m-%d") + " ok\n")
        code, out = run_main(["--state", self.state, "due"])
        self.assertEqual(code, 0)
        self.assertIn("skip:fresh", out)

    def test_old_ok_is_due(self):
        self._write_state(
            (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d") + " ok\n")
        code, out = run_main(["--state", self.state, "due"])
        self.assertIn("due", out)

    def test_recent_failed_skips(self):
        self._write_state(datetime.now().strftime("%Y-%m-%d") + " failed\n")
        code, out = run_main(["--state", self.state, "due"])
        self.assertIn("skip:fresh-failed", out)

    def test_old_failed_is_due(self):
        self._write_state(
            (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d") + " failed\n")
        code, out = run_main(["--state", self.state, "due"])
        self.assertIn("due", out)

    def test_date_only_legacy_format_counts_as_ok(self):
        self._write_state(datetime.now().strftime("%Y-%m-%d") + "\n")
        code, out = run_main(["--state", self.state, "due"])
        self.assertIn("skip:fresh", out)


class TestCompare(unittest.TestCase):
    def test_newer_remote(self):
        code, out = run_main(["compare", "v0.4.0", "--current", "0.3.8"])
        self.assertEqual(code, 0)
        self.assertIn("newer", out)

    def test_same_version(self):
        code, out = run_main(["compare", "v0.3.8", "--current", "0.3.8"])
        self.assertEqual(code, 0)
        self.assertIn("same", out)

    def test_remote_older_treated_same(self):
        code, out = run_main(["compare", "v0.3.7", "--current", "0.3.8"])
        self.assertEqual(code, 0)
        self.assertIn("same", out)

    def test_malformed_tag_is_ignored(self):
        # 安全审查 L4:tag 不符合 vX.Y.Z 形状按没有标签处理(不回显)
        code, out = run_main(["compare", "not-a-version", "--current", "0.3.8"])
        self.assertEqual(code, 0)
        self.assertIn("same", out)


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="maliang-vc-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.state = os.path.join(self.tmp, "version-check")

    def test_record_ok_writes_today(self):
        code, out = run_main(["--state", self.state, "record", "ok"])
        self.assertEqual(code, 0)
        with open(self.state, encoding="utf-8") as fh:
            content = fh.read()
        self.assertTrue(content.startswith(datetime.now().strftime("%Y-%m-%d")))
        self.assertIn("ok", content)

    def test_record_failed(self):
        code, out = run_main(["--state", self.state, "record", "failed"])
        self.assertEqual(code, 0)
        with open(self.state, encoding="utf-8") as fh:
            self.assertIn("failed", fh.read())

    def test_record_off(self):
        code, out = run_main(["--state", self.state, "record", "off"])
        self.assertEqual(code, 0)
        with open(self.state, encoding="utf-8") as fh:
            self.assertEqual(fh.read().strip(), "off")

    def test_record_bad_value_exits_2(self):
        code, out = run_main(["--state", self.state, "record", "sometimes"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
