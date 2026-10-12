"""ledger.py 反馈→规则状态机账本测试。

覆盖验收标准(R-ei-004 中 ledger 部分):追加写 JSONL + --confirm 发布 + 冲突报告 +
旧规则标「已废止」不删除;另覆盖一次性需求不入长期账本、自发现须附证据、
rollback 留痕与 verify 引用完整性。
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

lg = load("ledger.py")


class TestLedger(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.evidence = Path(self.root) / "shot.png"
        self.evidence.write_text("png", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, argv, expect=None):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = lg.main(["--root", self.root] + argv)
        if expect is not None:
            self.assertEqual(code, expect, f"argv={argv}\nstdout={out.getvalue()}\nstderr={err.getvalue()}")
        return code, out.getvalue(), err.getvalue()

    def _record(self, quote="页面太挤", source="user", extra=None):
        argv = ["record", "--type", "correction", "--source", source, "--quote", quote,
                "--scope", "中文界面", "--evidence", str(self.evidence)]
        if extra:
            argv += extra
        _, out, _ = self._run(argv, expect=0)
        return json.JSONDecoder().raw_decode(out[out.index("{"):])[0]["id"]

    def _propose_accept(self, event_id, rule="正文行高不低于 1.5", level="强偏好"):
        _, out, _ = self._run(["propose", "--event", event_id, "--rule", rule,
                               "--level", level, "--scope", "中文界面",
                               "--reason", "反复出现"], expect=0)
        cand = json.loads(out)["id"]
        self._run(["approve", "--candidate", cand, "--confirm"], expect=0)
        return cand

    def _publish(self, cand, rule_id=None, extra=None, expect=None):
        argv = ["publish", "--candidate", cand, "--confirm"]
        if rule_id:
            argv += ["--rule-id", rule_id]
        if extra:
            argv += extra
        return self._run(argv, expect=expect)

    def test_publish_requires_confirm(self):
        # 应报: publish 无 --confirm 拒绝(不改 feedback-ledger.md)
        event = self._record()
        cand = self._propose_accept(event)
        code, _, err = self._run(["publish", "--candidate", cand, "--rule-id", "P-01"], expect=2)
        self.assertIn("--confirm", err)
        self.assertFalse((Path(self.root) / ".maliang" / "feedback" / "rules.md").exists())

    def test_full_flow_publish_and_verify(self):
        # 不应报: record→propose→approve→publish 全链路,账本 verify 通过,五字段落盘
        event = self._record()
        cand = self._propose_accept(event)
        _, out, _ = self._publish(cand, expect=0)
        self.assertIn("P-01", out)
        md = (Path(self.root) / ".maliang" / "feedback" / "rules.md").read_text(encoding="utf-8")
        for field in ("级别：", "何时适用：", "原话摘录：", "收录："):
            self.assertIn(field, md)
        self.assertIn("状态：生效", md)
        _, out, _ = self._run(["verify"], expect=0)
        self.assertIn("账本校验通过", out)

    def test_one_off_event_not_longterm(self):
        # 应报: 一次性需求(--once)禁止 propose 进长期账本
        event = self._record(quote="这次先这样", extra=["--once"])
        _, _, err = self._run(["propose", "--event", event, "--rule", "x", "--level", "情境规则",
                               "--scope", "中文界面", "--reason", "r"], expect=2)
        self.assertIn("一次性", err)

    def test_self_discovery_requires_existing_evidence(self):
        # 应报: source=self 无证据 / 证据路径不存在
        _, _, err = self._run(["record", "--type", "defect", "--source", "self",
                               "--quote", "看起来不对", "--scope", "中文界面"], expect=2)
        self.assertIn("--evidence", err)
        _, _, err = self._run(["record", "--type", "defect", "--source", "self",
                               "--quote", "x", "--evidence", str(Path(self.root) / "ghost.png")],
                              expect=2)
        self.assertIn("不存在", err)

    def test_conflict_report_then_supersede(self):
        # 应报: 同 scope 冲突 → 生成报告且不发布;--supersedes 后旧规则标已废止且原文保留
        event1 = self._record("旧反馈")
        cand1 = self._propose_accept(event1, rule="正文用 16px", level="强偏好")
        code, _, _ = self._publish(cand1, rule_id="P-01")
        self.assertEqual(code, 0)
        event2 = self._record("新反馈")
        cand2 = self._propose_accept(event2, rule="正文用 15px")
        code, _, err = self._publish(cand2, rule_id="P-02")
        self.assertEqual(code, 1)
        self.assertIn("冲突报告", err)
        conflicts_dir = Path(self.root) / ".maliang" / "feedback" / "conflicts"
        reports = list(conflicts_dir.glob("*.md"))
        self.assertEqual(len(reports), 1)
        self.assertIn("P-01", reports[0].read_text(encoding="utf-8"))
        # 冲突未决时不得发布新规则
        md = (Path(self.root) / ".maliang" / "feedback" / "rules.md").read_text(encoding="utf-8")
        self.assertNotIn("P-02", md)
        # 明确替代: 旧规则标已废止(不删除),新规则发布
        code, out, _ = self._publish(
            cand2, rule_id="P-02",
            extra=["--supersedes", "P-01", "--reason", "新基线更准"])
        self.assertEqual(code, 0)
        md = (Path(self.root) / ".maliang" / "feedback" / "rules.md").read_text(encoding="utf-8")
        self.assertIn("P-01", md, "旧规则原文必须保留")
        self.assertIn("状态：已废止（", md)
        self.assertIn("正文用 16px", md, "旧规则正文不删除")
        self.assertIn("P-02", md)
        _, out, _ = self._run(["verify"], expect=0)
        self.assertIn("通过", out)

    def test_rollback_flow(self):
        # 应报: 发布后重跑门禁失败 → rolled-back 留痕(规则状态改已回滚)
        event = self._record()
        cand = self._propose_accept(event)
        self._publish(cand, "P-01", expect=0)
        self._run(["transition", "--candidate", cand, "--status", "rolled-back",
                   "--reason", "重跑 preview-check 失败", "--confirm"], expect=0)
        md = (Path(self.root) / ".maliang" / "feedback" / "rules.md").read_text(encoding="utf-8")
        self.assertIn("已回滚", md)
        self._run(["verify"], expect=0)

    def test_duplicate_rule_id_refused(self):
        # 应报: 规则编号不复用
        event = self._record()
        cand = self._propose_accept(event)
        code, _, _ = self._publish(cand, "P-01")
        self.assertEqual(code, 0)
        event2 = self._record("另一个")
        cand2 = self._propose_accept(event2, level="情境规则")
        _, _, err = self._publish(cand2, "P-01")
        self.assertIn("编号已存在", err)

    def test_verify_detects_dangling_reference(self):
        # 应报: 引用不存在的事件 → verify exit 1
        event = self._record()
        self._propose_accept(event)
        broken = Path(self.root) / ".maliang" / "feedback" / "candidates.jsonl"
        with open(broken, "a", encoding="utf-8") as f:
            f.write(json.dumps({"id": "cand-broken", "type": "candidate", "eventIds": ["evt-ghost"],
                                "rule": "x", "level": "强偏好", "scope": "s", "rationale": "r"},
                               ensure_ascii=False) + "\n")
        _, out, _ = self._run(["verify"], expect=1)
        self.assertIn("缺少事件 evt-ghost", out)

    def test_auto_rule_id_increments_without_reuse(self):
        # 应报: 缺省 --rule-id 接最大号递增;已废止编号不复用
        event = self._record()
        cand = self._propose_accept(event)
        code, out, _ = self._publish(cand)  # 不传 rule_id → 自动 P-01
        self.assertEqual(code, 0)
        self.assertIn("P-01", out)
        event2 = self._record("第二个")
        cand2 = self._propose_accept(event2, level="情境规则")
        code, out, _ = self._publish(cand2, extra=["--supersedes", "P-01", "--reason", "替代"])
        self.assertEqual(code, 0)
        self.assertIn("P-02", out)

    def test_report_summary(self):
        # report: 摘要含事件/候选/决策计数与状态分布
        event = self._record()
        self._propose_accept(event)
        _, out, _ = self._run(["report"], expect=0)
        data = json.loads(out)
        self.assertEqual(data["events"], 1)
        self.assertEqual(data["candidates"], 1)
        self.assertEqual(data["states"].get("accepted"), 1)

    def test_verify_without_ledger_exit_2(self):
        # 没能检查: 账本不存在
        _, _, err = self._run(["verify"], expect=2)
        self.assertIn("没能检查", err)


if __name__ == "__main__":
    unittest.main()
