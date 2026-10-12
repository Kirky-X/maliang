#!/usr/bin/env python3
"""preview-server —— 本地预览→用户选择回传桥（仅绑定 127.0.0.1）。

把风格对比页/预览页挂在本地 127.0.0.1 上打开，用户点「选择」→ 页面内确认弹层
**确认后**才写入 selection.json，同时把一句哨兵打到 stdout：
`MALIANG_DESIGN_SELECTION::{...}`。没有确认就不写盘；没有倒计时、没有超时默认、
没有推荐态自动写入——选择永远由用户的确认动作产生。

    python3 scripts/preview-server.py serve --file style-explorer.html [--exit-on-select]
    python3 scripts/preview-server.py <预览目录>            # 简写 = serve(目录内找对比页/索引页)
    python3 scripts/preview-server.py watch --selection selection.json [--stdin]
    python3 scripts/preview-server.py fallback-note

回传契约（explore.md / preview.md 的「回传协议」节引用本脚本）:
  - 认定「用户已选」= 三选一证据（已观察到 selection.json / 已见 stdout 哨兵 /
    对话中明确选择）；显式禁止把推荐态或页面默认高亮当作选择。
  - watcher 口径「事件优先、轮询并发兜底」: stdin 哨兵行是零延迟事件通道，
    文件轮询（--interval，默认 75ms）与事件通道**并发**运行而不是只在最后兜底。
  - 服务不可用时的降级：用 file:// 直接打开 + 剪贴板复制选择句，并明说
    「当前不会自动回传」（`fallback-note` 打印这句）；降级不等于静默降级。

stdout 哨兵（供 Agent/脚本解析）:
  MALIANG_PREVIEW_URL::{url}                      serve 就绪
  MALIANG_PREVIEW_SELECTION_FILE::{path}          selection 落盘位置
  MALIANG_DESIGN_SELECTION::{json}                serve 收到确认选择
  MALIANG_DESIGN_SELECTION_OBSERVED::{json}       watch 观察到选择
  MALIANG_DESIGN_SELECTION_TIMEOUT::{path}        watch 超时（未选择）

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
  0 = 正常结束（serve 关停 / watch 观察到选择）
  1 = 运行中出错（端口绑定失败、selection 目录不可写等）
  2 = 没能检查或用法错误（--file 不存在 / watch 超时 / 参数错误）
依赖: Python 3 标准库(无第三方依赖)。来源: qiaomu-design preview-server 与
watch-selection(2026-10 吸收; 修正口径: 轮询为并发兜底非「仅兜底」), 中文自研实现。
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import tempfile
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

BRIDGE_MARKER = "<!-- MALIANG_PREVIEW_BRIDGE -->"
SENTINEL_SELECTION = "MALIANG_DESIGN_SELECTION::"
SENTINEL_OBSERVED = "MALIANG_DESIGN_SELECTION_OBSERVED::"
SENTINEL_TIMEOUT = "MALIANG_DESIGN_SELECTION_TIMEOUT::"
FALLBACK_NOTE = (
    "当前服务不可用，已降级为 file:// 直接打开 + 复制选择句；"
    "这种方式不会自动回传，请把选择句粘贴给我。"
)
MIME = {
    ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif",
}


BRIDGE = BRIDGE_MARKER + r"""
<script>
/* 选择回传桥（幂等注入）：确认弹层确认后才 POST /api/select；无倒计时、无推荐态自动写入。 */
(function () {
  if (window.__maliangBridgeInstalled) return;
  window.__maliangBridgeInstalled = true;
  var optionSelector = '[data-design-option],[data-option],[data-choice],[data-direction],.card[data-name],article.option,.option';
  var pending = null;

  var style = document.createElement('style');
  style.textContent = [
    '.ml-bar{position:fixed;left:0;right:0;top:0;z-index:2147483000;height:52px;display:flex;align-items:center;gap:14px;',
    'padding:0 18px;background:rgba(251,251,250,.96);border-bottom:1px solid #d8dbe1;color:#191b21;',
    'font:500 13px/1.3 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;backdrop-filter:blur(12px)}',
    'body.ml-active{padding-top:52px!important}',
    '.ml-bar b{font-size:14px}',
    '.ml-bar .ml-hint{color:#5b6472}',
    '.ml-pick{display:inline-flex;align-items:center;justify-content:center;min-height:40px;margin-top:12px;padding:0 16px;',
    'border:1px solid #191b21;border-radius:8px;background:#191b21;color:#fff;font:600 13px/1.2 inherit;cursor:pointer}',
    '.ml-picked{outline:3px solid rgba(25,27,33,.78)!important;outline-offset:3px!important}',
    '.ml-picked .ml-pick{background:#168a5f;border-color:#168a5f}',
    '.ml-overlay{position:fixed;inset:0;z-index:2147483100;display:none;align-items:center;justify-content:center;background:rgba(15,23,42,.45)}',
    '.ml-overlay.open{display:flex}',
    '.ml-dialog{width:min(420px,92vw);background:#fff;border-radius:14px;padding:20px;color:#191b21;',
    'font:14px/1.5 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;box-shadow:0 24px 60px rgba(15,23,42,.3)}',
    '.ml-dialog p{margin:6px 0 14px;color:#5b6472}',
    '.ml-dialog .ml-actions{display:flex;gap:10px;justify-content:flex-end}',
    '.ml-dialog button{font:inherit;padding:8px 16px;border-radius:8px;border:1px solid #d8dbe1;background:#fff;cursor:pointer}',
    '.ml-dialog button.ml-confirm{background:#191b21;color:#fff;border-color:#191b21}',
    '.ml-error{color:#b42318}'
  ].join('');
  document.head.appendChild(style);

  function ensureBar() {
    if (document.querySelector('.ml-bar')) return;
    var bar = document.createElement('div');
    bar.className = 'ml-bar';
    bar.innerHTML = '<b>预览回传桥</b><span class="ml-hint">点「选择此方向」→ 确认后写入 selection.json 并回传；取消不写任何文件。</span>';
    document.body.appendChild(bar);
    document.body.classList.add('ml-active');
  }

  function cardName(el, index) {
    return el.getAttribute('data-name') || el.getAttribute('data-design-option') ||
      (el.querySelector('h1,h2,h3') || {}).textContent || ('方向 ' + (index + 1));
  }

  function ensurePickButtons() {
    var cards = Array.prototype.slice.call(document.querySelectorAll(optionSelector));
    cards.forEach(function (el, index) {
      if (el.querySelector('.ml-pick')) return;
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'ml-pick';
      button.textContent = '选择此方向';
      button.addEventListener('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        openConfirm(el, index);
      });
      el.appendChild(button);
    });
  }

  function openConfirm(el, index) {
    pending = {id: el.getAttribute('data-id') || String(index + 1), name: cardName(el, index), element: el};
    var overlay = document.querySelector('.ml-overlay');
    overlay.querySelector('.ml-name').textContent = pending.name;
    overlay.classList.add('open');
    overlay.querySelector('.ml-confirm').focus();
  }

  function closeConfirm() {
    pending = null;
    document.querySelector('.ml-overlay').classList.remove('open');
  }

  function sendSelection() {
    if (!pending) return;
    var payload = {id: pending.id, name: pending.name, source: 'preview-confirm'};
    fetch('/api/select', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-Maliang-Token': '__MALIANG_BRIDGE_TOKEN__'},
      body: JSON.stringify(payload)}).then(function (resp) {
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      return resp.json();
    }).then(function () {
      document.querySelectorAll('.ml-picked').forEach(function (x) { x.classList.remove('ml-picked'); });
      if (pending.element) pending.element.classList.add('ml-picked');
      var dialog = document.querySelector('.ml-dialog');
      dialog.querySelector('p').textContent = '已回传：' + pending.name;
      dialog.querySelector('.ml-actions').innerHTML =
        '<button type="button" class="ml-ok">好</button>';
      dialog.querySelector('.ml-ok').addEventListener('click', closeConfirm);
      document.querySelector('.ml-confirm').style.display = 'none';
      document.querySelector('.ml-cancel').textContent = '关闭';
      pending = null;
    }).catch(function (error) {
      var dialog = document.querySelector('.ml-dialog');
      var err = dialog.querySelector('.ml-error');
      err.textContent = '回传失败（' + error.message + '）。请用页面里的「复制选择句」或直接说出选择——不会自动回传。';
      err.style.display = 'block';
    });
  }

  function ensureOverlay() {
    if (document.querySelector('.ml-overlay')) return;
    var overlay = document.createElement('div');
    overlay.className = 'ml-overlay';
    overlay.innerHTML = [
      '<div class="ml-dialog" role="dialog" aria-modal="true" aria-label="确认选择">',
      '<h2 style="margin:0;font-size:16px">确认选择「<span class="ml-name"></span>」？</h2>',
      '<p>确认后才写入 selection.json 并回传；取消不写任何文件。没有倒计时、不会自动替你选。</p>',
      '<div class="ml-error" style="display:none"></div>',
      '<div class="ml-actions"><button type="button" class="ml-cancel">取消</button>',
      '<button type="button" class="ml-confirm">确认选择</button></div></div>'
    ].join('');
    document.body.appendChild(overlay);
    overlay.addEventListener('click', function (event) {
      if (event.target === overlay) closeConfirm();
    });
    overlay.querySelector('.ml-cancel').addEventListener('click', closeConfirm);
    overlay.querySelector('.ml-confirm').addEventListener('click', sendSelection);
  }

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && document.querySelector('.ml-overlay.open')) { closeConfirm(); return; }
    if (event.target.closest('input,textarea,select,[contenteditable="true"]')) return;
    if (document.querySelector('.ml-overlay.open')) return;
    var index = ['1', '2', '3', '4', '5', '6', '7', '8', '9'].indexOf(event.key);
    if (index < 0) return;
    var cards = document.querySelectorAll(optionSelector);
    if (!cards[index]) return;
    event.preventDefault();
    openConfirm(cards[index], index);
  }, true);

  function boot() { ensureBar(); ensurePickButtons(); ensureOverlay(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, {once: true});
  } else {
    boot();
  }
})();
</script>
"""


def inject_bridge(html: str, token: str = "") -> str:
    """幂等注入选择壳（已有 marker 不重复注入）。token 为本次会话回传令牌（跨源页面读不到）。"""
    bridge = BRIDGE.replace("__MALIANG_BRIDGE_TOKEN__", token)
    if BRIDGE_MARKER in html:
        return html
    if "</body>" in html:
        return html.replace("</body>", bridge + "\n</body>", 1)
    return html + "\n" + bridge


def _read_json_body(handler) -> dict:
    length = int(handler.headers.get("Content-Length") or 0)
    if length <= 0 or length > 1024 * 1024:
        raise ValueError("请求体缺失或超过 1MB")
    raw = handler.rfile.read(length).decode("utf-8")
    data = json.loads(raw or "{}")
    if not isinstance(data, dict):
        raise ValueError("请求体必须是 JSON 对象")
    return data


def write_selection(path: str, record: dict) -> None:
    """用户确认后的唯一写盘点（append 语义：整文件原子替换，由确认动作触发）。"""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".selection-", suffix=".tmp",
                                dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        os.replace(temp, path)
    except BaseException:
        if os.path.exists(temp):
            os.unlink(temp)
        raise


def create_server(page: str, selection_path: str, quiet: bool = False):
    """构建绑定 127.0.0.1 的预览服务；返回 (server, url)。

    server.exit_on_select 置 True 时：收到确认选择、响应写完后自动关停。
    """
    page = os.path.realpath(page)
    root = os.path.dirname(page)
    selection_path = os.path.realpath(selection_path)
    token = secrets.token_urlsafe(24)  # 会话回传令牌：跨源页面读不到注入内容，拿不到 token

    class Handler(BaseHTTPRequestHandler):
        server_version = "maliang-preview/1.0"

        def log_message(self, fmt, *args):  # 默认日志太吵：只留错误
            if not quiet and str(args[1] if len(args) > 1 else "").startswith(("4", "5")):
                sys.stderr.write("preview-server: %s\n" % (fmt % args))

        def _send_json(self, status: int, payload: dict):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/api/health":
                return self._send_json(200, {"ok": True, "file": os.path.basename(page), "selectionFile": selection_path})
            if path == "/api/selection":
                try:
                    with open(selection_path, "r", encoding="utf-8") as f:
                        return self._send_json(200, {"ok": True, "selection": json.load(f)})
                except (OSError, ValueError):
                    return self._send_json(200, {"ok": True, "selection": None})
            try:
                target = page if path in ("/", "") else os.path.realpath(
                    os.path.join(root, "." + unquote(path)))
            except (ValueError, OSError):
                return self._send_json(400, {"ok": False, "error": "Bad request path"})
            if not (target == root or target.startswith(root + os.sep)) or not os.path.isfile(target):
                return self._send_json(404, {"ok": False, "error": "Not found"})
            try:
                with open(target, "rb") as f:
                    body = f.read()
                ext = os.path.splitext(target)[1].lower()
                if ext == ".html":
                    body = inject_bridge(body.decode("utf-8"), token).encode("utf-8")
            except UnicodeDecodeError:
                return self._send_json(400, {"ok": False, "error": "HTML 非 UTF-8，无法注入回传桥"})
            except OSError:
                return self._send_json(500, {"ok": False, "error": "读取失败"})
            self.send_response(200)
            self.send_header("Content-Type", MIME.get(ext, "application/octet-stream"))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if urlsplit(self.path).path != "/api/select":
                return self._send_json(404, {"ok": False, "error": "Not found"})
            origin = self.headers.get("Origin")
            expected_origin = "http://127.0.0.1:%d" % self.server.server_address[1]
            if origin and origin != expected_origin:
                return self._send_json(403, {"ok": False, "error": "跨源请求被拒绝"})
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if ctype != "application/json":
                return self._send_json(415, {"ok": False, "error": "Content-Type 必须为 application/json"})
            if self.headers.get("X-Maliang-Token") != token:
                return self._send_json(403, {"ok": False, "error": "缺少或错误的回传令牌"})
            try:
                data = _read_json_body(self)
            except (ValueError, json.JSONDecodeError) as exc:
                return self._send_json(400, {"ok": False, "error": str(exc)})
            record = {
                "id": str(data.get("id") or ""),
                "name": str(data.get("name") or ""),
                "notes": str(data.get("notes") or ""),
                "source": str(data.get("source") or "preview-confirm"),
                "receivedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }
            if not record["id"] and not record["name"]:
                return self._send_json(400, {"ok": False, "error": "id 与 name 至少一个非空"})
            try:
                write_selection(selection_path, record)
            except OSError as exc:
                return self._send_json(500, {"ok": False, "error": f"写盘失败: {exc}"})
            print(SENTINEL_SELECTION + json.dumps(record, ensure_ascii=False), flush=True)
            self._send_json(200, {"ok": True, "selection": record})
            if getattr(self.server, "exit_on_select", False) and not getattr(self.server, "exiting", False):
                self.server.exiting = True
                # 让响应先写完，再关停
                threading.Thread(target=self.server.shutdown, daemon=True).start()

    class Server(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    server = Server(("127.0.0.1", 0), Handler)
    server.exit_on_select = False
    server.exiting = False
    server.bridge_token = token  # 测试与集成方读取（生产不暴露）
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    return server, url


def resolve_page(target: str, explicit: str | None) -> str:
    """把 <预览目录或 HTML> 解析为具体页面（explore/preview 文档的简写调用）。

    目录:优先 style-explorer.html → index.html → 目录内唯一 HTML;
    文件:按原样使用。两处都给(--file 与位置参数)视为歧义,显性报错。
    """
    if explicit and target:
        raise ValueError("位置参数与 --file 不能同时给（要打开哪个页面有歧义）")
    given = explicit or target
    if not given:
        raise ValueError("缺少要打开的页面:给 <预览目录或 HTML> 或 --file")
    if os.path.isdir(given):
        for name in ("style-explorer.html", "index.html"):
            candidate = os.path.join(given, name)
            if os.path.isfile(candidate):
                return candidate
        htmls = sorted(fn for fn in os.listdir(given) if fn.lower().endswith(".html"))
        if len(htmls) == 1:
            return os.path.join(given, htmls[0])
        raise ValueError(f"目录里没有 style-explorer.html / index.html,HTML 也不唯一: {given}")
    return given


def cmd_serve(args) -> int:
    try:
        page = resolve_page(args.target, args.file)
    except ValueError as exc:
        print(f"preview-server: {exc}", file=sys.stderr)
        return 2
    if not os.path.isfile(page):
        print(f"preview-server: 没能检查——页面不存在 {page}", file=sys.stderr)
        return 2
    selection = args.selection or os.path.join(os.path.dirname(os.path.abspath(page)), "selection.json")
    server, url = create_server(page, selection)
    server.exit_on_select = args.exit_on_select
    print(f"MALIANG_PREVIEW_URL::{url}", flush=True)
    print(f"MALIANG_PREVIEW_SELECTION_FILE::{os.path.realpath(selection)}", flush=True)
    print("确认弹层确认后才写 selection.json；取消不写任何文件（无倒计时、无默认选择）。", flush=True)
    if not args.no_open:
        try:
            opened = webbrowser.open(url)
            if not opened:
                print("提示：自动打开浏览器失败，请手动访问上面的 URL。", file=sys.stderr)
        except Exception as exc:
            print(f"提示：自动打开浏览器失败（{exc}），请手动访问上面的 URL。", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def cmd_watch(args) -> int:
    """事件优先、轮询并发兜底：stdin 哨兵行零延迟结算；文件轮询并发运行。"""
    selection = os.path.realpath(args.selection)
    done = threading.Event()
    result = {"record": None, "channel": None}

    def observe(record, channel):
        if record and not done.is_set():
            result["record"] = record
            result["channel"] = channel
            done.set()

    def read_file():
        try:
            with open(selection, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and (data.get("id") or data.get("name")):
                return data
        except (OSError, ValueError):
            return None
        return None

    observe(read_file(), "file-seed")  # 启动先查一次（文件已存在算已观察到）

    threads = []
    if args.stdin:
        def stdin_reader():
            for line in sys.stdin:
                marker = line.rfind(SENTINEL_SELECTION)
                if marker < 0:
                    continue
                try:
                    observe(json.loads(line[marker + len(SENTINEL_SELECTION):].strip()), "stdin-event")
                    return
                except ValueError:
                    continue
        thread = threading.Thread(target=stdin_reader, daemon=True)
        thread.start()
        threads.append(thread)

    def poller():
        # 轮询与事件通道并发运行（不是「仅兜底」）：兜住 stdio 不接管的进程形态
        while not done.is_set():
            observe(read_file(), "file-poll")
            done.wait(args.interval / 1000.0)
    thread = threading.Thread(target=poller, daemon=True)
    thread.start()
    threads.append(thread)

    if args.timeout > 0:
        done.wait(args.timeout / 1000.0)
    else:
        while not done.is_set():
            done.wait(0.2)
    if result["record"]:
        print(SENTINEL_OBSERVED + json.dumps(result["record"], ensure_ascii=False), flush=True)
        return 0
    if args.timeout > 0:
        print(f"{SENTINEL_TIMEOUT}{selection}", file=sys.stderr, flush=True)
        return 2
    print("preview-server: watch 被中断（未观察到选择）", file=sys.stderr)
    return 2


def cmd_fallback_note(_args) -> int:
    print(FALLBACK_NOTE)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="preview-server.py",
        description="本地预览→用户选择回传桥（仅绑定 127.0.0.1；确认弹层确认后才写 selection.json）。",
        epilog="降级口径：服务不可用时用 file:// 直接打开 + 剪贴板复制选择句，并明说不会自动回传\n"
               "（`fallback-note` 打印这句；禁止把推荐态/默认高亮当作已选择）。\n"
               "watcher 口径：stdin 哨兵行是零延迟事件通道，文件轮询（默认 75ms）与其并发兜底。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="挂起预览页并接收确认选择")
    serve.add_argument("target", nargs="?", default="", help="预览目录或 HTML（目录按 style-explorer.html → index.html → 唯一 HTML 解析）")
    serve.add_argument("--file", default=None, help="要打开的 HTML（也可用位置参数;两者互斥）")
    serve.add_argument("--selection", default=None, help="selection.json 路径（默认页面同目录）")
    serve.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    serve.add_argument("--exit-on-select", action="store_true", help="收到确认选择后自动关闭服务")
    serve.set_defaults(func=cmd_serve)

    watch = sub.add_parser("watch", help="观察 selection.json（事件优先、轮询并发兜底）")
    watch.add_argument("--selection", required=True, help="selection.json 路径")
    watch.add_argument("--stdin", action="store_true", help="同时监听 stdin 里的 MALIANG_DESIGN_SELECTION:: 哨兵行")
    watch.add_argument("--interval", type=int, default=75, help="轮询间隔毫秒（默认 75；与事件通道并发）")
    watch.add_argument("--timeout", type=int, default=0, help="毫秒；0=不限时（默认；不做倒计时默认选择）")
    watch.set_defaults(func=cmd_watch)

    fallback = sub.add_parser("fallback-note", help="打印服务不可用时的降级说明句")
    fallback.set_defaults(func=cmd_fallback_note)

    raw = list(sys.argv[1:] if argv is None else argv)
    # 兼容文档简写:首个参数是路径(而非子命令/旗标)时按 serve 处理
    if raw and not raw[0].startswith("-") and raw[0] not in ("serve", "watch", "fallback-note"):
        raw = ["serve"] + raw
    args = parser.parse_args(raw)
    try:
        return args.func(args)
    except OSError as exc:
        print(f"preview-server: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
