"""receipts.py 测量收据机制测试：init→attach→verify 三态与 --check 查询。

覆盖验收标准(R-ei-001):全绿 / 改动产物后 EXPIRED / 无收据 UNMEASURED /
不存在的路径 exit 2;并覆盖会话隔离(上一会话收据不复用)与收据不可覆盖。
"""

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

rc = load("receipts.py")


class TestReceipts(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.session = "s1"
        self.artifact = Path(self.root) / "home.html"
        self.artifact.write_text("<html>v1</html>\n", encoding="utf-8")
        self.script = Path(self.root) / "gate.py"
        self.script.write_text("# gate v1\n", encoding="utf-8")
        self.report = Path(self.root) / "report.json"
        self.report.write_text('{"ok": true}\n', encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _init(self, run="r1"):
        return rc.init_run(self.root, self.session, run,
                           [str(self.artifact)], [str(self.script)], "样例测量")

    def _attach(self, run="r1"):
        return rc.attach_report(self.root, self.session, run, str(self.report),
                                "preview-check", 0, ["contrast=4.6:1"])

    def test_full_green_then_expired(self):
        # 不应报: init→attach→verify 全绿;改动产物 → EXPIRED
        self._init()
        self._attach()
        result = rc.verify_run(self.root, self.session, "r1")
        self.assertEqual(result["state"], rc.STATE_OK)
        self.assertEqual(result["stale"], [])
        self.assertEqual(result["attachments"][0]["values"], ["contrast=4.6:1"])

        self.artifact.write_text("<html>v2</html>\n", encoding="utf-8")
        result = rc.verify_run(self.root, self.session, "r1")
        self.assertEqual(result["state"], rc.STATE_EXPIRED)
        self.assertTrue(any("内容已改变" in s for s in result["stale"]))

    def test_expired_when_report_edited(self):
        # 应报: 报告(证据本身)在 attach 后被改 → EXPIRED
        self._init()
        self._attach()
        self.report.write_text('{"ok": false}\n', encoding="utf-8")
        result = rc.verify_run(self.root, self.session, "r1")
        self.assertEqual(result["state"], rc.STATE_EXPIRED)
        self.assertTrue(any("[report]" in s for s in result["stale"]))

    def test_unmeasured_without_receipt(self):
        # 应报: 没有任何收据的产物 --check → UNMEASURED
        result = rc.check_path(self.root, self.session, str(self.artifact))
        self.assertEqual(result["state"], rc.STATE_UNMEASURED)

    def test_check_ok_then_expired_after_edit(self):
        # --check: 有活收据 OK;同批产物被改后 → EXPIRED(源变即 stale)
        self._init()
        ok = rc.check_path(self.root, self.session, str(self.artifact))
        self.assertEqual(ok["state"], rc.STATE_OK)
        self.script.write_text("# gate v2\n", encoding="utf-8")
        expired = rc.check_path(self.root, self.session, str(self.artifact))
        self.assertEqual(expired["state"], rc.STATE_EXPIRED)

    def test_check_missing_path_exit_2(self):
        # 验收: 不存在的路径 exit 2(没能检查),不得记为通过
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = rc.main(["--check", str(Path(self.root) / "ghost.html"),
                            "--root", self.root, "--session", self.session])
        self.assertEqual(code, 2)

    def test_check_main_exit_codes(self):
        # 主入口三态退出码: OK=0 / EXPIRED=1 / UNMEASURED=1
        self._init()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(
                rc.main(["--check", str(self.artifact), "--root", self.root,
                         "--session", self.session]), 0)
        self.artifact.write_text("<html>v3</html>\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(
                rc.main(["--check", str(self.artifact), "--root", self.root,
                         "--session", self.session]), 1)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(
                rc.main(["--check", str(self.script), "--root", self.root,
                         "--session", "other"]), 1)

    def test_session_isolation(self):
        # 不应复用: 上一会话的收据对新会话不生效(按会话分文件)
        self._init()
        result = rc.verify_run(self.root, "s2", "r1")
        self.assertEqual(result["state"], rc.STATE_UNMEASURED)
        self.assertNotEqual(rc.receipts_file(self.root, "s1"),
                            rc.receipts_file(self.root, "s2"))

    def test_init_duplicate_run_rejected(self):
        # 应报: 同一 run 重复 init(收据不可覆盖)
        self._init()
        with self.assertRaises(ValueError):
            self._init()

    def test_init_missing_artifact_raises(self):
        # 应报: 绑定不存在的产物 → 显性失败(FileNotFoundError)
        with self.assertRaises(FileNotFoundError):
            rc.init_run(self.root, self.session, "r9",
                        [str(Path(self.root) / "nope.html")], [], None)

    def test_attach_requires_init(self):
        # 应报: 没有 init 就 attach
        with self.assertRaises(ValueError):
            self._attach(run="r-nope")

    def test_list_and_dir(self):
        self._init()
        items = rc.list_receipts(self.root, self.session)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["state"], rc.STATE_OK)
        self.assertTrue(rc.receipts_file(self.root, self.session).endswith("s1.jsonl"))

    def test_verify_unmeasured_exit_1(self):
        # verify 无收据 → UNMEASURED,exit 1(未测量不是通过)
        with contextlib.redirect_stdout(io.StringIO()):
            code = rc.main(["verify", "--run", "ghost", "--root", self.root,
                            "--session", self.session])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
