"""build-explorer.py manifest→对比页生成器测试。

覆盖验收标准(R-ei-004 中 build-explorer 部分):--help、最小样例、一次报全错、
--force 保护、baseline 排首位、CSP 口径、自包含内嵌与离线成功一行 JSON。
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

be = load("build-explorer.py")

CANDIDATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="style.css">
</head><body><h1>{title}</h1><img src="pic.png" alt=""><script src="app.js"></script></body></html>
"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestBuildExplorer(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _write(self.root / "style.css", "h1 { color: #123456; } .bg { background: url(pic.png); }\n")
        _write(self.root / "pic.png", "\x89PNG\r\n\x1a\nfake")
        _write(self.root / "app.js", "console.log('hi');\n")
        _write(self.root / "a.html", CANDIDATE.format(title="甲"))
        _write(self.root / "b.html", CANDIDATE.format(title="乙"))

    def tearDown(self):
        self._tmp.cleanup()

    def _manifest(self, **overrides):
        data = {
            "schemaVersion": 1, "project": "样例项目", "brief": "两方向共同任务",
            "round": "02",
            "candidates": [
                {"id": "a", "name": "甲方向", "concept": "概念甲", "typography": "大字距",
                 "palette": ["#112233", "#f5f5f5"], "traits": ["疏"], "source": "a.html"},
                {"id": "b", "name": "乙方向", "concept": "概念乙", "typography": "紧密",
                 "palette": ["#101820"], "traits": ["密"], "source": "b.html", "baseline": True},
            ],
        }
        data.update(overrides)
        path = self.root / "manifest.json"
        _write(path, json.dumps(data, ensure_ascii=False))
        return path

    def test_minimal_build_one_line_json(self):
        # 不应报: 最小样例成功,stdout 一行 JSON(output/candidates/fingerprint/bytes)
        path = self._manifest()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = be.main([str(path)])
        self.assertEqual(code, 0)
        result = json.loads(buf.getvalue().strip().splitlines()[-1])
        self.assertEqual(result["candidates"], 2)
        self.assertEqual(result["bytes"], os.path.getsize(result["output"]))
        self.assertEqual(len(result["fingerprint"]), 24)
        page = Path(result["output"]).read_text(encoding="utf-8")
        # 自包含: 候选 CSS/图片/脚本全部内嵌,不引用网络资源
        self.assertIn("data:image/png;base64,", page)
        self.assertIn("color: #123456", page)
        self.assertIn("connect-src 'none'", page)
        # 静态候选剥离脚本(non-interactive)
        self.assertNotIn("console.log", page)

    def test_baseline_sorted_first(self):
        # 现状候选排第一位(编号 01 标「现状」)
        result = be.build(str(self._manifest()), None, False)
        page = Path(result["output"]).read_text(encoding="utf-8")
        self.assertLess(page.index("乙方向"), page.index("甲方向"))

    def test_manifest_errors_reported_in_one_pass(self):
        # 应报: 多处问题一次报全(不挤牙膏)
        data = json.loads(self._manifest().read_text(encoding="utf-8"))
        data["candidates"][0]["palette"] = ["not-hex"]
        data["candidates"][0]["source"] = "missing.html"
        data["candidates"][1]["id"] = "BAD ID"
        _write(self.root / "manifest.json", json.dumps(data, ensure_ascii=False))
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            code = be.main([str(self.root / "manifest.json")])
        self.assertEqual(code, 1)
        text = buf.getvalue()
        self.assertIn("3 处要改", text)
        self.assertIn("palette", text)
        self.assertIn("找不到 source", text)

    def test_output_exists_needs_force(self):
        # 应报: 输出已存在且无 --force;--force 后覆盖成功
        path = self._manifest()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(be.main([str(path)]), 0)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(be.main([str(path)]), 1)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(be.main([str(path), "--force"]), 0)

    def test_url_candidate_local_only_and_csp(self):
        # 应报: 非本机 url 拒绝;本机 url 放开 connect-src 到该 origin
        data = json.loads(self._manifest().read_text(encoding="utf-8"))
        data["candidates"] = [{"id": "a", "name": "甲", "concept": "c", "typography": "t",
                               "palette": ["#112233"], "traits": ["x"],
                               "kind": "url", "url": "http://example.com/x"}]
        _write(self.root / "manifest.json", json.dumps(data, ensure_ascii=False))
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(be.main([str(self.root / "manifest.json")]), 1)
        self.assertIn("本机开发服务器", err.getvalue())

        data["candidates"][0]["url"] = "http://localhost:5173/orders"
        _write(self.root / "manifest.json", json.dumps(data, ensure_ascii=False))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(be.main([str(self.root / "manifest.json")]), 0)
        page = (self.root / "style-explorer.html").read_text(encoding="utf-8")
        self.assertIn("connect-src http://localhost:5173", page)
        self.assertIn("frame-src 'self' about: data: http://localhost:5173", page)

    def test_foreign_resource_rejected(self):
        # 应报: 候选含未内嵌的外部资源
        _write(self.root / "a.html",
               '<!DOCTYPE html><html><head><title>a</title></head>'
               '<body><script src="https://cdn.example.com/x.js"></script></body></html>')
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(be.main([str(self._manifest())]), 1)
        self.assertIn("未内嵌资源", err.getvalue())

    def test_interactive_keeps_inline_script(self):
        # 不应报: interactive 候选内联脚本(放开 script-src),沙箱运行
        data = json.loads(self._manifest().read_text(encoding="utf-8"))
        data["candidates"] = [{"id": "a", "name": "甲", "concept": "c", "typography": "t",
                               "palette": ["#112233"], "traits": ["x"],
                               "source": "a.html", "interactive": True}]
        _write(self.root / "manifest.json", json.dumps(data, ensure_ascii=False))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(be.main([str(self.root / "manifest.json")]), 0)
        page = (self.root / "style-explorer.html").read_text(encoding="utf-8")
        self.assertIn("console.log", page)
        self.assertIn("script-src 'unsafe-inline'", page)
        self.assertNotIn("unsafe-eval", page, "interactive 候选不需要 eval，CSP 不得放行")

    def test_native_viewport_message(self):
        # 应报: nativeViewport 非法值
        data = json.loads(self._manifest().read_text(encoding="utf-8"))
        data["candidates"][0]["nativeViewport"] = "abc"
        _write(self.root / "manifest.json", json.dumps(data, ensure_ascii=False))
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(be.main([str(self.root / "manifest.json")]), 1)
        self.assertIn("nativeViewport", err.getvalue())

    def test_fingerprint_stable_and_sensitive(self):
        # 指纹: 相同 manifest 两次一致;改一个词即变化
        data = json.loads(self._manifest().read_text(encoding="utf-8"))
        first, _ = be.load_manifest(str(self.root / "manifest.json"))
        second, _ = be.load_manifest(str(self.root / "manifest.json"))
        self.assertEqual(first["fingerprint"], second["fingerprint"])
        data["candidates"][0]["typography"] = "改了"
        _write(self.root / "manifest.json", json.dumps(data, ensure_ascii=False))
        third, _ = be.load_manifest(str(self.root / "manifest.json"))
        self.assertNotEqual(first["fingerprint"], third["fingerprint"])

    def test_no_thumbnail_mockup_layer(self):
        # 不吸收: 缩尺样机层/缩略图九宫格——外壳不含批量缩略图样式
        result = be.build(str(self._manifest()), None, False)
        page = Path(result["output"]).read_text(encoding="utf-8")
        for banned in ("thumbnail", "thumb-grid", "mockup-scale"):
            self.assertNotIn(banned, page)


if __name__ == "__main__":
    unittest.main()
