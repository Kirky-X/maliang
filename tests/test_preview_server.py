"""preview-server.py 选择回传桥测试。

覆盖验收标准(R-ei-004 中 preview-server 部分):无确认不写 selection.json;
确认(POST /api/select)才写盘;并覆盖 127.0.0.1 绑定、路径逃逸防护、幂等注入、
watch 事件优先/轮询并发与降级说明句。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

ps = load("preview-server.py")

PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>explorer</title></head>
<body>
<article class="card" data-name="甲方向"><h2>甲</h2></article>
<article class="card" data-name="乙方向"><h2>乙</h2></article>
</body></html>
"""


class TestPreviewServer(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.page = self.root / "style-explorer.html"
        self.page.write_text(PAGE, encoding="utf-8")
        self.selection = self.root / "selection.json"
        self.server, self.url = ps.create_server(str(self.page), str(self.selection), quiet=True)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        self._tmp.cleanup()

    def _get(self, path, raw=False):
        with urllib.request.urlopen(self.url.rstrip("/") + path) as resp:
            data = resp.read()
        return data if raw else data.decode("utf-8")

    def _post(self, path, payload):
        req = urllib.request.Request(
            self.url.rstrip("/") + path, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "X-Maliang-Token": self.server.bridge_token}, method="POST")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def test_binds_loopback_only(self):
        # 仅绑 127.0.0.1:对外地址不在监听
        host = self.server.server_address[0]
        self.assertEqual(host, "127.0.0.1")

    def test_no_confirm_no_write(self):
        # 验收: 无确认不写 selection.json——GET 页面/查询/健康检查都不落盘
        page = self._get("/")
        health = json.loads(self._get("/api/health"))
        current = json.loads(self._get("/api/selection"))
        self.assertIn(ps.BRIDGE_MARKER, page)
        self.assertTrue(health["ok"])
        self.assertIsNone(current["selection"])
        self.assertFalse(self.selection.exists(), "无确认动作时不得写入 selection.json")

    def test_confirm_writes_and_sentinel(self):
        # 确认动作(POST)才写盘 + 打印哨兵
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = self._post("/api/select", {"id": "2", "name": "乙方向", "source": "preview-confirm"})
        self.assertTrue(result["ok"])
        saved = json.loads(self.selection.read_text(encoding="utf-8"))
        self.assertEqual(saved["name"], "乙方向")
        self.assertIn("MALIANG_DESIGN_SELECTION::", buf.getvalue())
        live = json.loads(self._get("/api/selection"))
        self.assertEqual(live["selection"]["id"], "2")

    def test_bridge_gates_write_behind_confirm_without_timers(self):
        # 确认闸门: 选择动作先开确认弹层,唯一写盘调用在确认按钮回调里;无倒计时/定时器
        html = self._get("/")
        script = html.split(ps.BRIDGE_MARKER, 1)[1]
        self.assertIn("确认后才写入 selection.json", script)
        self.assertIn("openConfirm", script)
        self.assertIn("'/api/select'", script)
        self.assertIn(".ml-confirm", script)
        self.assertNotIn("setInterval", script)
        self.assertNotIn("countdown", script.lower())
        # 唯一 fetch 调用点位于 sendSelection(由确认按钮触发)
        self.assertEqual(script.count("fetch('/api/select'"), 1)

    def test_bridge_injection_idempotent(self):
        # 幂等注入: 二次注入不重复
        html = self._get("/")
        self.assertEqual(ps.inject_bridge(html).count(ps.BRIDGE_MARKER), html.count(ps.BRIDGE_MARKER))

    def test_path_traversal_blocked(self):
        # 路径逃逸: 目录外文件不可读
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self._get("/../outside.txt")
        self.assertEqual(ctx.exception.code, 404)

    def test_positional_dir_shorthand(self):
        # 文档简写: 位置参数给目录 → 自动找 style-explorer.html(B 的调用形态)
        self.page.write_text(PAGE, encoding="utf-8")
        self.assertEqual(ps.resolve_page(str(self.root), None), str(self.page))
        self.assertEqual(ps.resolve_page("", str(self.page)), str(self.page))
        with self.assertRaises(ValueError):
            ps.resolve_page(str(self.root), str(self.page))  # 两处都给 = 歧义

    def test_positional_dir_unique_html(self):
        # 目录里没有对比页/索引页但有唯一 HTML 时也能解析
        (self.root / "style-explorer.html").unlink()
        only = self.root / "only.html"
        only.write_text(PAGE, encoding="utf-8")
        self.assertEqual(ps.resolve_page(str(self.root), None), str(only))

    def test_empty_select_rejected(self):
        # 应报: id 与 name 都空 → 400,不写盘
        req = urllib.request.Request(
            self.url.rstrip("/") + "/api/select", data=b"{}",
            headers={"Content-Type": "application/json",
                     "X-Maliang-Token": self.server.bridge_token}, method="POST")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)
        self.assertFalse(self.selection.exists())


class TestWatchAndFallback(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.selection = self.root / "selection.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_watch_sees_existing_selection(self):
        # 不应报: 启动时 selection.json 已在 = 已观察到(事件优先的第一查)
        self.selection.write_text(json.dumps({"id": "1", "name": "甲"}), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ps.main(["watch", "--selection", str(self.selection), "--timeout", "2000"])
        self.assertEqual(code, 0)
        self.assertIn("MALIANG_DESIGN_SELECTION_OBSERVED::", buf.getvalue())

    def test_watch_timeout_exit_2(self):
        # 超时未选 → exit 2 + TIMEOUT 哨兵(未测量不是通过)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = ps.main(["watch", "--selection", str(self.selection), "--timeout", "120"])
        self.assertEqual(code, 2)
        self.assertIn("MALIANG_DESIGN_SELECTION_TIMEOUT::", err.getvalue())

    def test_watch_poll_concurrent(self):
        # 轮询通道与事件通道并发: 无 stdin 时写入文件也能被观察到
        result = {}

        def run():
            with contextlib.redirect_stdout(io.StringIO()):
                result["code"] = ps.main(
                    ["watch", "--selection", str(self.selection), "--timeout", "3000",
                     "--interval", "30"])

        thread = threading.Thread(target=run)
        thread.start()
        time.sleep(0.15)
        self.selection.write_text(json.dumps({"id": "9", "name": "轮询看到"}), encoding="utf-8")
        thread.join(timeout=5)
        self.assertEqual(result.get("code"), 0)

    def test_fallback_note_states_no_auto_return(self):
        # 降级说明句必须明说「不会自动回传」
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ps.main(["fallback-note"])
        self.assertEqual(code, 0)
        self.assertIn("不会自动回传", buf.getvalue())

    def test_serve_missing_file_exit_2(self):
        # 没能检查: --file 不存在
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = ps.main(["serve", "--file", str(self.root / "ghost.html"), "--no-open"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
