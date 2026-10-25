"""stage-audit.py 的单元测试(段级汇总审计)。

锁定:段1 内置存在性检查(DESIGN.md / frontmatter / users 块 / 降级声明)、
产物缺失三态、旧路径兼容、收据编排(init→attach→verify)、门禁退出码映射
(0/1/2/异常码)、段6 无机械审计面语义。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

sa = load("stage-audit.py")


def _write(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def _stub(root, name, code):
    """写一个以指定退出码退出的桩门禁脚本,返回路径。"""
    return _write(os.path.join(root, "_stubs", name + ".py"),
                  "import sys\nsys.exit(%d)\n" % code)


DESIGN_WITH_USERS = "---\ncolors:\n  primary: \"#123456\"\nusers:\n  personas: []\n---\n# Demo\n"
DESIGN_PLAIN = "---\ncolors:\n  primary: \"#123456\"\n---\n# Demo\n"
DESIGN_DEGRADED = DESIGN_PLAIN + "\n未做用户研究,按 surface-modes 模式假设。\n"


class TestStage1(unittest.TestCase):
    def _root(self, design=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        if design is not None:
            _write(os.path.join(tmp.name, "DESIGN.md"), design)
        return tmp.name

    def test_pass_with_users_block(self):
        root = self._root(DESIGN_WITH_USERS)
        code, res = sa.audit_stage(1, root, run_gates=False)
        self.assertEqual(code, 0)
        self.assertEqual(res["missing"], [])
        self.assertEqual(res["receipt"]["state"], "OK")

    def test_pass_with_degraded_declaration(self):
        code, _ = sa.audit_stage(1, self._root(DESIGN_DEGRADED), run_gates=False)
        self.assertEqual(code, 0)

    def test_missing_design_md(self):
        code, res = sa.audit_stage(1, self._root(), run_gates=False)
        self.assertEqual(code, 1)
        self.assertTrue(any("DESIGN.md 不存在" in m for m in res["missing"]))

    def test_no_frontmatter(self):
        root = self._root("# 只有正文没有 frontmatter\n")
        code, res = sa.audit_stage(1, root, run_gates=False)
        self.assertEqual(code, 1)
        self.assertTrue(any("frontmatter" in m for m in res["missing"]))

    def test_missing_users_without_degraded(self):
        code, res = sa.audit_stage(1, self._root(DESIGN_PLAIN), run_gates=False)
        self.assertEqual(code, 1)
        self.assertTrue(any("用户三产出缺失" in m for m in res["missing"]))


class TestArtifacts(unittest.TestCase):
    def _root(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return tmp.name

    def test_stage3_missing_spec_dir(self):
        code, res = sa.audit_stage(3, self._root(), run_gates=False)
        self.assertEqual(code, 1)
        self.assertTrue(res["missing"])

    def test_stage3_canonical_path(self):
        root = self._root()
        _write(os.path.join(root, "design", "ui-markdown", "token.md"), "token")
        code, res = sa.audit_stage(3, root, run_gates=False)
        self.assertEqual(code, 0)
        self.assertTrue(any("canonical" in n for n in res["notes"]))

    def test_stage3_legacy_examples_fallback(self):
        root = self._root()
        _write(os.path.join(root, "examples", "ui-markdown", "token.md"), "token")
        code, res = sa.audit_stage(3, root, run_gates=False)
        self.assertEqual(code, 0)
        self.assertTrue(any("存量旧路径" in n for n in res["notes"]))

    def test_stage5_needs_preview_html(self):
        root = self._root()
        _write(os.path.join(root, "design", "preview", "keep.txt"), "x")
        code, _ = sa.audit_stage(5, root, run_gates=False)
        self.assertEqual(code, 1)
        _write(os.path.join(root, "design", "preview", "preview_home_iphone15.html"), "<html></html>")
        code, _ = sa.audit_stage(5, root, run_gates=False)
        self.assertEqual(code, 0)

    def test_stage4_implementation_map(self):
        root = self._root()
        _write(os.path.join(root, "design", "ui-markdown", "ui-implementation-map.json"), "{}")
        code, _ = sa.audit_stage(4, root, run_gates=False)
        self.assertEqual(code, 0)

    def test_stage6_no_machine_face_is_two(self):
        code, res = sa.audit_stage(6, self._root(), run_gates=False)
        self.assertEqual(code, 2)
        self.assertTrue(any("无机械审计面" in n for n in res["notes"]))


class TestGateOrchestration(unittest.TestCase):
    def _spec_root(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = tmp.name
        _write(os.path.join(root, "design", "ui-markdown", "token.md"), "token")
        return root

    def _audit_with_stub(self, root, code):
        stub = _stub(root, "stub%d" % code, code)
        gates = [("stub", lambda r: [sys.executable, stub])]
        return sa.audit_stage(3, root, run_gates=True, gates_override=gates)

    def test_gate_pass_attaches_receipt(self):
        root = self._spec_root()
        code, res = self._audit_with_stub(root, 0)
        self.assertEqual(code, 0)
        self.assertEqual(res["gates"][0]["exit"], 0)
        self.assertEqual(res["receipt"]["state"], "OK")
        reports = os.listdir(os.path.join(root, ".maliang", "receipts", "reports"))
        self.assertEqual(len(reports), 1)

    def test_gate_exit1_fails_stage(self):
        code, _ = self._audit_with_stub(self._spec_root(), 1)
        self.assertEqual(code, 1)

    def test_gate_exit2_is_could_not_check(self):
        code, _ = self._audit_with_stub(self._spec_root(), 2)
        self.assertEqual(code, 2)

    def test_gate_abnormal_exit_is_could_not_check(self):
        code, _ = self._audit_with_stub(self._spec_root(), 3)
        self.assertEqual(code, 2)

    def test_gate_script_missing_is_could_not_check(self):
        # 解释器存在而脚本缺失:python 以退出码 2 报 can't open file → 三态传导为没能检查
        root = self._spec_root()
        gates = [("ghost", lambda r: [sys.executable, os.path.join(root, "ghost.py")])]
        code, res = sa.audit_stage(3, root, run_gates=True, gates_override=gates)
        self.assertEqual(code, 2)
        self.assertEqual(res["gates"][0]["exit"], 2)


class TestCli(unittest.TestCase):
    def test_list_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(sa.main(["--list"]), 0)
        self.assertIn("段3", buf.getvalue())

    def test_stage1_cli_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write(os.path.join(tmp, "DESIGN.md"), DESIGN_WITH_USERS)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(sa.main(["--stage", "1", "--root", tmp, "--skip-gates"]), 0)

    def test_bad_root_is_two(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(sa.main(["--stage", "1", "--root", os.path.join("Z:", "no", "such")]), 2)

    def test_json_output_parses(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write(os.path.join(tmp, "DESIGN.md"), DESIGN_PLAIN)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sa.main(["--stage", "1", "--root", tmp, "--skip-gates", "--json"])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["exit"], 1)
            self.assertTrue(payload["stage"]["missing"])


if __name__ == "__main__":
    unittest.main()
