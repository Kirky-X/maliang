"""verify.py capture 子命令:URL/路径转换纯函数 + 无浏览器/缺目标三态。"""
import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

vf = load("verify.py")


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return vf.main(list(argv)), buf.getvalue()


class TestToBrowseUrl(unittest.TestCase):
    def test_http_passthrough(self):
        self.assertEqual(vf._to_browse_url("https://x.dev/a"), "https://x.dev/a")

    def test_local_file_becomes_file_uri(self):
        import tempfile
        f = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        f.close()
        self.addCleanup(os.unlink, f.name)
        url = vf._to_browse_url(f.name)
        self.assertTrue(url.startswith("file:///"))

    def test_missing_returns_none(self):
        self.assertIsNone(vf._to_browse_url("no/such/file.html"))


class TestCaptureExitCodes(unittest.TestCase):
    def test_missing_target_exits_2(self):
        code, out = run_main(["capture", "no/such/page.html"])
        self.assertEqual(code, 2)
        self.assertIn("没能截图", out)

    def test_no_browser_unmeasured_exits_2(self):
        import tempfile
        f = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        f.close()
        self.addCleanup(os.unlink, f.name)
        code, out = run_main(["capture", f.name, "--browser", "no-such-browser-exe"])
        self.assertEqual(code, 2)
        self.assertIn("UNMEASURED", out)

    def test_capture_in_dispatch(self):
        # capture 已入分发表:未知子命令仍 2,help 列出 capture
        code, out = run_main([])
        self.assertEqual(code, 2)
        self.assertIn("capture", out)


if __name__ == "__main__":
    unittest.main()
