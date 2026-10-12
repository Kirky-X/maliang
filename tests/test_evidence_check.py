"""evidence-check.py 取证齐套校验测试。

覆盖验收标准(R-ei-002):缺项样例报出缺失清单且退出码非零;齐套样例通过;
另覆盖:找不到 report.json → exit 2、报告非法 → 问题、文件复用 → 假齐套。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

ec = load("evidence-check.py")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestEvidenceCheck(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.shots = self.root / "shots"
        self.shots.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def _complete_report(self, name="report.json"):
        """构建一份齐套报告（2 状态页）+ 全部引用文件。"""
        files = [
            "shots/home-idle.png", "shots/home-idle@2x.png", "shots/home-idle-masked.png",
            "shots/home-done.png", "shots/home-done@2x.png", "shots/home-done-masked.png",
            "shots/sheet-home.png", "probe/home-motion.json", "record/home.mp4",
        ]
        for rel in files:
            _write(self.root / rel, "data:" + rel)
        report = {
            "schema": "maliang-evidence/1",
            "capturedAt": "2026-10-12T10:00:00+08:00",
            "pages": [{
                "page": "preview_home_iphone15.html",
                "viewport": "390x844",
                "sheet": "shots/sheet-home.png",
                "motion": "probe/home-motion.json",
                "recording": "record/home.mp4",
                "states": [
                    {"state": "idle", "shot": "shots/home-idle.png",
                     "shot2x": "shots/home-idle@2x.png", "masked": "shots/home-idle-masked.png"},
                    {"state": "done", "shot": "shots/home-done.png",
                     "shot2x": "shots/home-done@2x.png", "masked": "shots/home-done-masked.png"},
                ],
            }],
        }
        path = self.root / name
        _write(path, json.dumps(report, ensure_ascii=False))
        return path

    def test_complete_report_passes(self):
        # 不应报: 齐套样例通过(exit 0)
        self._complete_report()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = ec.main([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("齐套", out.getvalue())

    def test_missing_items_reported_nonzero(self):
        # 应报: 缺遮字图 + 缺录屏,清单列出且 exit 1
        path = self._complete_report()
        (self.shots / "home-idle-masked.png").unlink()
        report = json.loads(path.read_text(encoding="utf-8"))
        del report["pages"][0]["recording"]
        _write(path, json.dumps(report, ensure_ascii=False))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = ec.main([str(path)])
        self.assertEqual(code, 1)
        text = out.getvalue()
        self.assertIn("遮字图", text)
        self.assertIn("录屏", text)
        self.assertIn("unverified", text)

    def test_empty_file_is_not_evidence(self):
        # 应报: 空文件不算证据
        path = self._complete_report()
        (self.shots / "home-idle@2x.png").write_text("", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = ec.main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("文件为空", out.getvalue())

    def test_same_file_reused_is_problem(self):
        # 应报: 2x 图与状态图同文件 = 假齐套
        path = self._complete_report()
        report = json.loads(path.read_text(encoding="utf-8"))
        report["pages"][0]["states"][0]["shot2x"] = "shots/home-idle.png"
        _write(path, json.dumps(report, ensure_ascii=False))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = ec.main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("复用", out.getvalue())

    def test_no_report_exit_2(self):
        # 验收: 找不到 report.json → 没能检查 exit 2
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = ec.main([str(self.root)])
        self.assertEqual(code, 2)
        self.assertIn("未测量", err.getvalue())

    def test_broken_report_is_problem(self):
        # 应报: 报告不是合法 JSON → 问题(exit 1),不是静默跳过
        path = self.root / "report.json"
        _write(path, "{not json")
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            code = ec.main([str(path)])
        self.assertEqual(code, 1)

    def test_single_state_page_no_sheet_is_note(self):
        # 不应报: 单状态页无并排图可查(记为 n/a,不是缺项)
        for rel in ["shots/one.png", "shots/one@2x.png", "shots/one-masked.png",
                    "probe/one-motion.json", "record/one.mp4"]:
            _write(self.root / rel, "data")
        report = {
            "schema": "maliang-evidence/1",
            "pages": [{
                "page": "preview_one.html",
                "motion": "probe/one-motion.json",
                "recording": "record/one.mp4",
                "states": [{"state": "idle", "shot": "shots/one.png",
                            "shot2x": "shots/one@2x.png", "masked": "shots/one-masked.png"}],
            }],
        }
        path = self.root / "report.json"
        _write(path, json.dumps(report, ensure_ascii=False))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = ec.main([str(path)])
        self.assertEqual(code, 0)
        self.assertIn("n/a", out.getvalue())

    def test_failed_entry_counts_as_missing(self):
        # 应报: 条目自报 failed → 计入缺项并转录原因
        path = self._complete_report()
        report = json.loads(path.read_text(encoding="utf-8"))
        report["pages"][0]["states"][1]["failed"] = True
        report["pages"][0]["states"][1]["error"] = "SCREENSHOT_TIMEOUT"
        _write(path, json.dumps(report, ensure_ascii=False))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = ec.main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("SCREENSHOT_TIMEOUT", out.getvalue())


if __name__ == "__main__":
    unittest.main()
