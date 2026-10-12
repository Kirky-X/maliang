"""source-fingerprint.py(#30)的单元测试:指纹基线 / 信任边界 / 原子写 / diff 归约入口。"""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

sf = load("source-fingerprint.py")

HAS_GIT = shutil.which("git") is not None


def _repo(tmp):
    root = os.path.join(tmp, "proj")
    os.makedirs(os.path.join(root, "src"))
    with open(os.path.join(root, "src", "a.ts"), "w") as fh:
        fh.write("export const a = 1;\n")
    with open(os.path.join(root, "src", "b.css"), "w") as fh:
        fh.write(".a { color: red; }\n")
    return root


class TestCreate(unittest.TestCase):
    def test_baseline_written_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            out = os.path.join(tmp, "baseline.json")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sf.main(["create", root, "--output", out])
            self.assertEqual(code, 0)
            data = json.load(open(out, encoding="utf-8"))
            self.assertEqual(data["schemaVersion"], 1)
            self.assertEqual(sorted(data["files"]), ["src/a.ts", "src/b.css"])
            # 原子写:不留 .tmp 残片
            self.assertEqual([f for f in os.listdir(tmp) if f.endswith(".tmp")], [])

    def test_secret_files_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            for name in (".env", ".env.local", "id_rsa", "server.pem"):
                open(os.path.join(root, name), "w").write("secret")
            out = os.path.join(tmp, "baseline.json")
            with contextlib.redirect_stdout(io.StringIO()):
                sf.main(["create", root, "--output", out])
            data = json.load(open(out, encoding="utf-8"))
            self.assertNotIn(".env", data["files"])
            self.assertNotIn("id_rsa", data["files"])
            self.assertNotIn("server.pem", data["files"])

    def test_missing_repo_exit_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = sf.main(["create", os.path.join("no", "such")])
        self.assertEqual(code, 2)


class TestCheck(unittest.TestCase):
    def _baseline(self, tmp, root):
        out = os.path.join(tmp, "baseline.json")
        with contextlib.redirect_stdout(io.StringIO()):
            sf.main(["create", root, "--output", out])
        return out

    def test_unchanged_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = self._baseline(tmp, root)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sf.main(["check", root, "--baseline", baseline])
            self.assertEqual(code, 0)
            self.assertIn("指纹一致", buf.getvalue())

    def test_changed_exit_1_lists_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = self._baseline(tmp, root)
            with open(os.path.join(root, "src", "a.ts"), "a") as fh:
                fh.write("export const b = 2;\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sf.main(["check", root, "--baseline", baseline])
            self.assertEqual(code, 1)
            self.assertIn("changed: src/a.ts", buf.getvalue())
            self.assertIn("不得以变更行数或整文件哈希推断重要性", buf.getvalue())

    def test_added_and_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = self._baseline(tmp, root)
            os.remove(os.path.join(root, "src", "b.css"))
            with open(os.path.join(root, "src", "c.md"), "w") as fh:
                fh.write("x\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sf.main(["check", root, "--baseline", baseline])
            self.assertEqual(code, 1)
            self.assertIn("added:   src/c.md", buf.getvalue())
            self.assertIn("removed: src/b.css", buf.getvalue())

    def test_untrusted_baseline_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = self._baseline(tmp, root)
            data = json.load(open(baseline, encoding="utf-8"))
            data["files"]["../outside.ts"] = "0" * 64
            json.dump(data, open(baseline, "w", encoding="utf-8"))
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = sf.main(["check", root, "--baseline", baseline])
            self.assertEqual(code, 2)
            self.assertIn("UNTRUSTED", err.getvalue())

    def test_secret_in_baseline_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = self._baseline(tmp, root)
            data = json.load(open(baseline, encoding="utf-8"))
            data["files"][".env"] = "0" * 64
            json.dump(data, open(baseline, "w", encoding="utf-8"))
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = sf.main(["check", root, "--baseline", baseline])
            self.assertEqual(code, 2)
            self.assertIn("涉密", err.getvalue())

    def test_bad_fingerprint_format_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = self._baseline(tmp, root)
            data = json.load(open(baseline, encoding="utf-8"))
            data["files"]["src/a.ts"] = "tooshort"
            json.dump(data, open(baseline, "w", encoding="utf-8"))
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = sf.main(["check", root, "--baseline", baseline])
            self.assertEqual(code, 2)


class TestDiff(unittest.TestCase):
    def test_unsafe_path_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = os.path.join(tmp, "b.json")
            with contextlib.redirect_stdout(io.StringIO()):
                sf.main(["create", root, "--output", baseline])
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = sf.main(["diff", root, "--baseline", baseline, "--path", "../x.ts"])
            self.assertEqual(code, 2)

    def test_unchanged_file_short_circuits_without_git(self):
        # 与基线一致 → 直接说明,不跑 git
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = os.path.join(tmp, "b.json")
            with contextlib.redirect_stdout(io.StringIO()):
                sf.main(["create", root, "--output", baseline])
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sf.main(["diff", root, "--baseline", baseline, "--path", "src/a.ts"])
            self.assertEqual(code, 0)
            self.assertIn("与基线一致", buf.getvalue())

    @unittest.skipUnless(HAS_GIT, "需要 git 验证引号限定 diff")
    def test_changed_file_runs_scoped_git_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "-C", root, "add", "."], check=True)
            subprocess.run(["git", "-C", root, "-c", "user.email=t@t", "-c", "user.name=t",
                            "commit", "-qm", "init"], check=True)
            baseline = os.path.join(tmp, "b.json")
            with contextlib.redirect_stdout(io.StringIO()):
                sf.main(["create", root, "--output", baseline])
            with open(os.path.join(root, "src", "a.ts"), "a") as fh:
                fh.write("export const b = 2;\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = sf.main(["diff", root, "--baseline", baseline, "--path", "src/a.ts"])
            self.assertEqual(code, 0)
            self.assertIn("diff --git", buf.getvalue())
            self.assertIn("export const b = 2;", buf.getvalue())

    def test_changed_file_without_git_says_delta_unavailable(self):
        # git 不可得(非 git 仓)→ 明说 delta 不可得,退出 2
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            baseline = os.path.join(tmp, "b.json")
            with contextlib.redirect_stdout(io.StringIO()):
                sf.main(["create", root, "--output", baseline])
            with open(os.path.join(root, "src", "a.ts"), "a") as fh:
                fh.write("export const b = 2;\n")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = sf.main(["diff", root, "--baseline", baseline, "--path", "src/a.ts"])
            self.assertEqual(code, 2)
            self.assertIn("delta 不可得", err.getvalue())


if __name__ == "__main__":
    unittest.main()
