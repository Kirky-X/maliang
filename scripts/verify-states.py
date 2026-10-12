#!/usr/bin/env python3
"""真浏览器「状态态」WCAG 对比度门禁:default / hover / focus 三态实测。

用法:
    python3 scripts/verify-states.py <html_file_or_dir> [--dark]
                                     [--format {text,json}]
                                     [--browser PATH] [--viewport WxH] [--timeout MS]

背景:静态解析只能看到默认态的 color×background 组合;按钮悬停后文字色被
抽掉、次要按钮 hover 继承主色填充这类「静态通过、悬停失败」的问题,只有把
鼠标真的移上去读计算样式才看得见。本脚本用本机 Chrome/Chromium 的 DevTools
协议实测每个交互元素的 default / hover / focus 三态。

阈值:无直接文字的图形控件(icon-only)3:1(WCAG 1.4.11 非文本对比度);
文本按字号/字重 4.5:1 或 3:1(≥24px 或 ≥18.66px 且 ≥700)。豁免:原生
checkbox/radio、role=switch、opacity:0、disabled / aria-disabled(WCAG 1.4.3/1.4.11)。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        没装浏览器 / 目标不存在 / 页面上一个可比对元素都没有 → UNMEASURED + 2,
        绝不静默通过。
依赖: Python 3 标准库 + 本机 Chrome/Chromium(可选依赖,经 DevTools 协议驱动)。
来源:ux-ui-agent-skills scripts/verify_states.mjs(同阈值/同豁免口径)与
     scripts/_targets.mjs(三态退出码、「未测量不算通过」),2026-10 吸收;
     浏览器驱动为本地自研的轻量 CDP 实现(不引入 Playwright)。
"""

import argparse
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_UNMEASURED = 2

VIEWPORT_DEFAULT = "1280x900"
TIMEOUT_DEFAULT_MS = 60000

# 候选交互元素(与 verify_states.mjs 的 handles 一致)
CANDIDATE_SELECTOR = (
    'button, a[href], input, select, textarea, [role="button"], [role="switch"]'
)

# 三态读取:按元素性质返回是否豁免、是否图形控件、前景/背景色(canvas 回读,
# oklch/color-mix 也能拿到 rgba)、字号字重与报告标签。
# 背景沿祖先链回溯,遇渐变/图片背景判为「不可知」(bgUnknown),不猜。
READ_JS = r"""
(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const toRgba = (value) => {
    if (!ctx || !value) return null;
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = 'rgba(0,0,0,0)';
    ctx.fillStyle = value;
    ctx.fillRect(0, 0, 1, 1);
    const d = ctx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  };
  const transparent = (c) => !c || c === 'rgba(0, 0, 0, 0)' || (c.match(/[\d.]+/g) || []).length === 4
    && parseFloat(c.match(/[\d.]+/g)[3]) === 0;
  const cs = getComputedStyle(el);
  const tag = el.tagName;
  const type = (el.getAttribute('type') || '').toLowerCase();
  const role = el.getAttribute('role') || '';
  const isToggle = tag === 'INPUT' && (type === 'checkbox' || type === 'radio');
  const isDisabled = el.disabled === true || el.getAttribute('aria-disabled') === 'true';
  const skip = isToggle || role === 'switch' || parseFloat(cs.opacity) === 0 || isDisabled;

  // 有效背景:自身背景透明则沿祖先链找第一个不透明层;途中遇渐变/图片 → 不可知。
  let bg = null;
  let bgUnknown = false;
  for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
    const s = getComputedStyle(n);
    if (s.backgroundImage && s.backgroundImage !== 'none') { bgUnknown = true; break; }
    const c = s.backgroundColor;
    if (!transparent(c)) {
      bg = toRgba(c);
      const a = bg ? bg[3] : 0;
      if (a >= 0.999) break;
    }
  }
  if (!bg && !bgUnknown) {
    const bodyBg = document.body ? getComputedStyle(document.body).backgroundColor : null;
    bg = transparent(bodyBg) ? [255, 255, 255, 1] : toRgba(bodyBg);
  }
  const fg = toRgba(cs.color);
  const graphical = ![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
  return {
    skip, graphical, bgUnknown, fg, bg,
    label: (el.textContent || el.value || el.getAttribute('aria-label') || '')
      .trim().replace(/\s+/g, ' ').slice(0, 18),
    px: parseFloat(cs.fontSize),
    bold: (parseInt(cs.fontWeight, 10) || 400) >= 700,
    opacity: parseFloat(cs.opacity),
  };
}
"""

# 收集候选:可见 + nth-child 路径定位 + 视口中心坐标(供真实鼠标悬停)
COLLECT_JS = r"""
() => {
  const path = (el) => {
    const parts = [];
    for (let n = el; n && n.nodeType === 1 && n !== document.documentElement; n = n.parentElement) {
      const i = [...n.parentElement.children].indexOf(n) + 1;
      parts.unshift(n.tagName.toLowerCase() + ':nth-child(' + i + ')');
    }
    return parts.join(' > ');
  };
  const visible = (el) => {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    return cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) !== 0
      && r.width > 0 && r.height > 0 && !el.closest('[hidden]');
  };
  const out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll(%s)) {
    if (!visible(el)) continue;
    el.scrollIntoView({ block: 'center', inline: 'center' });
    const sel = path(el);
    if (seen.has(sel)) continue;
    seen.add(sel);
    const r = el.getBoundingClientRect();
    out.push({ sel, tag: el.tagName.toLowerCase(), x: r.left + r.width / 2, y: r.top + r.height / 2 });
    if (out.length >= 300) break;
  }
  return out;
}
""" % json.dumps(CANDIDATE_SELECTOR)

# 悬停/聚焦是瞬时的,过渡与动画会拖慢读数 —— 注入后强制关闭(只影响本次临时测量)
FREEZE_CSS = "*,*::before,*::after{transition:none!important;animation:none!important}"


# ---------------------------------------------------------------------------
# 颜色与阈值(纯函数,便于单测;不含浏览器)
# ---------------------------------------------------------------------------

def contrast_ratio(fg, bg):
    """WCAG 对比度;fg 含 alpha 时先合成到 bg 上。fg/bg = [r,g,b,a]。"""
    a = fg[3] if len(fg) > 3 else 1.0
    if a < 1.0:
        fg = [fg[i] * a + bg[i] * (1 - a) for i in range(3)] + [1.0]

    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    l1 = 0.2126 * lin(fg[0]) + 0.7152 * lin(fg[1]) + 0.0722 * lin(fg[2])
    l2 = 0.2126 * lin(bg[0]) + 0.7152 * lin(bg[1]) + 0.0722 * lin(bg[2])
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def needed_ratio(px, bold, graphical):
    """按元素性质取阈值:图形控件 3.0;大文本 3.0;其余正文 4.5。"""
    if graphical:
        return 3.0
    if px >= 24 or (px >= 18.66 and bold):
        return 3.0
    return 4.5


# ---------------------------------------------------------------------------
# 浏览器发现与 DevTools 协议(轻量 CDP,标准库实现)
# ---------------------------------------------------------------------------

BROWSER_CANDIDATES = (
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "chrome", "msedge", "microsoft-edge",
)


class BrowserUnavailable(RuntimeError):
    """没有可用的浏览器 —— 调用方按 UNMEASURED/exit 2 处理。"""


class CDPError(RuntimeError):
    pass


def find_browser(explicit=None):
    """按 显式参数 > MALIANG_BROWSER > PATH 候选 的顺序找浏览器;找不到返回 None。"""
    if explicit:
        return explicit if os.path.exists(explicit) else None
    env = os.environ.get("MALIANG_BROWSER")
    if env:
        return env if os.path.exists(env) else None
    for name in BROWSER_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    return None


def _launch_once(binary, headless_flag, timeout_s):
    """启动一次浏览器,等 DevToolsActivePort 出现;失败抛 CDPError。"""
    profile_dir = tempfile.mkdtemp(prefix="maliang-verify-")
    args = [
        binary, headless_flag, "--remote-debugging-port=0",
        "--user-data-dir=" + profile_dir, "--no-first-run",
        "--no-default-browser-check", "--disable-gpu", "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--disable-extensions", "--mute-audio", "about:blank",
    ]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        args.append("--no-sandbox")  # 容器内以 root 运行时 Chrome 需要
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    port_file = os.path.join(profile_dir, "DevToolsActivePort")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if proc.poll() is not None:
            err = (proc.stderr.read() or b"").decode("utf-8", "replace")
            shutil.rmtree(profile_dir, ignore_errors=True)
            raise CDPError("浏览器提前退出: " + err.strip()[-300:])
        if os.path.exists(port_file):
            with open(port_file, "r", encoding="utf-8") as fh:
                first = fh.read().splitlines()
            if first:
                return proc, profile_dir, int(first[0])
        time.sleep(0.05)
    proc.terminate()
    shutil.rmtree(profile_dir, ignore_errors=True)
    raise CDPError("浏览器启动超时(DevToolsActivePort 未出现)")


def launch_browser(binary, timeout_s=25):
    """启动无头浏览器,返回 (proc, profile_dir, port)。新版失败回退旧版 --headless。"""
    last_error = None
    for flag in ("--headless=new", "--headless"):
        try:
            return _launch_once(binary, flag, timeout_s)
        except CDPError as exc:
            last_error = exc
    raise CDPError("无法启动浏览器: %s" % last_error)


def stop_browser(proc, profile_dir):
    """收尾:终止进程并清理临时 profile。"""
    try:
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
    finally:
        if profile_dir:
            shutil.rmtree(profile_dir, ignore_errors=True)


class _WebSocket:
    """最小 WebSocket 客户端(仅满足 CDP 需要的文本帧与 ping/pong)。"""

    def __init__(self, url, timeout=10.0):
        parsed = urllib.parse.urlsplit(url)
        host, port = parsed.hostname, parsed.port or 80
        self._sock = socket.create_connection((host, port), timeout=timeout)
        self._pending = b""
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        path = parsed.path or "/"
        request = (
            "GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\n"
            "Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n" % (path, host, port, key)
        )
        self._sock.sendall(request.encode("ascii"))
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise CDPError("WebSocket 握手失败:连接被关闭")
            buf += chunk
        header, _, self._pending = buf.partition(b"\r\n\r\n")
        status = header.split(b"\r\n")[0]
        if b" 101 " not in status:
            raise CDPError("WebSocket 握手失败: " + status.decode("utf-8", "replace"))

    def settimeout(self, value):
        self._sock.settimeout(value)

    def _recv_exact(self, count):
        while len(self._pending) < count:
            chunk = self._sock.recv(65536)
            if not chunk:
                raise CDPError("WebSocket 连接被关闭")
            self._pending += chunk
        out, self._pending = self._pending[:count], self._pending[count:]
        return out

    def _recv_frame(self):
        b1, b2 = self._recv_exact(2)
        fin = bool(b1 & 0x80)
        opcode = b1 & 0x0F
        masked = b2 & 0x80
        length = b2 & 0x7F
        if length == 126:
            length = struct.unpack(">H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._recv_exact(8))[0]
        mask = self._recv_exact(4) if masked else None
        data = self._recv_exact(length)
        if mask:
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        return fin, opcode, data

    def send_text(self, text):
        payload = text.encode("utf-8")
        header = bytearray([0x81])
        if len(payload) < 126:
            header.append(0x80 | len(payload))
        elif len(payload) <= 0xFFFF:
            header.append(0x80 | 126)
            header += struct.pack(">H", len(payload))
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", len(payload))
        mask = os.urandom(4)
        header += mask
        self._sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def recv_text(self):
        """读一条完整文本消息(支持分片);ping 自动回 pong,close 抛错。"""
        chunks = []
        while True:
            fin, opcode, data = self._recv_frame()
            if opcode in (0x1, 0x0):
                chunks.append(data)
                if fin:
                    break
            elif opcode == 0x9:  # ping
                self._send_control(0xA, data)
            elif opcode == 0x8:
                raise CDPError("WebSocket 连接被服务端关闭")
        return b"".join(chunks).decode("utf-8", "replace")

    def _send_control(self, opcode, data):
        header = bytearray([0x80 | opcode])
        if len(data) < 126:
            header.append(0x80 | len(data))
        else:
            header.append(0x80 | 126)
            header += struct.pack(">H", len(data))
        mask = os.urandom(4)
        header += mask
        self._sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def close(self):
        try:
            self._send_control(0x8, b"")
        except OSError:
            pass
        try:
            self._sock.close()
        except OSError:
            pass


class CDPSession:
    """CDP 会话:同步请求/响应,忽略事件通知。"""

    def __init__(self, ws_url, timeout=10.0):
        self._ws = _WebSocket(ws_url, timeout=timeout)
        self._id = 0
        self._default_timeout = timeout

    def call(self, method, params=None, timeout=None):
        self._id += 1
        mid = self._id
        self._ws.send_text(json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + (timeout or self._default_timeout)
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise CDPError("CDP 调用超时: " + method)
            self._ws.settimeout(max(0.2, min(remaining, 10.0)))
            try:
                message = json.loads(self._ws.recv_text())
            except socket.timeout:
                continue
            if message.get("id") == mid:
                if "error" in message:
                    raise CDPError("CDP %s 失败: %s" % (method, message["error"]))
                return message.get("result", {})
            # 事件通知:测量不需要,直接丢弃

    def evaluate(self, expression, timeout=None):
        """执行 JS 表达式并返回其值(returnByValue)。异常返回 (None, 错误文本)。"""
        result = self.call("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        }, timeout=timeout)
        if "exceptionDetails" in result:
            return None, str(result["exceptionDetails"].get("text") or "JS 异常")
        return result.get("result", {}).get("value"), None

    def evaluate_fn(self, function_source, arg=None, timeout=None):
        """执行 JS 函数(源码形如 `(x) => ...`),以 JSON 传入单个参数。"""
        return self.evaluate("(%s)(%s)" % (function_source, json.dumps(arg)), timeout=timeout)

    def navigate(self, url, timeout=None):
        """跳转并等待 readyState=complete(CDN 加载不上时按剩余预算放弃等待)。"""
        self.call("Page.navigate", {"url": url}, timeout=timeout)
        deadline = time.time() + (timeout or self._default_timeout)
        while time.time() < deadline:
            ready, _err = self.evaluate("document.readyState", timeout=min(5.0, max(0.5, deadline - time.time())))
            if ready == "complete":
                return True
            time.sleep(0.05)
        return False

    def close(self):
        self._ws.close()


def connect_session(port, timeout=10.0):
    """连上浏览器里已存在的 page target,返回 CDPSession。"""
    with urllib.request.urlopen("http://127.0.0.1:%d/json/list" % port, timeout=timeout) as resp:
        targets = json.loads(resp.read().decode("utf-8"))
    pages = [t for t in targets if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
    if not pages:
        raise CDPError("浏览器里没有可用的 page target")
    return CDPSession(pages[0]["webSocketDebuggerUrl"], timeout=timeout)


# ---------------------------------------------------------------------------
# 单文件测量
# ---------------------------------------------------------------------------

def parse_viewport(value):
    m = re.fullmatch(r"(\d{2,5})[xX](\d{2,5})", value.strip())
    if not m:
        raise argparse.ArgumentTypeError("viewport 需形如 1280x900")
    return int(m.group(1)), int(m.group(2))


def measure_file(session, path, dark=False, viewport=(1280, 900), timeout_ms=TIMEOUT_DEFAULT_MS):
    """测一个文件的 default/hover/focus 三态,返回结果 dict(不抛业务异常)。"""
    deadline = time.time() + timeout_ms / 1000.0
    result = {
        "file": path, "status": "measured", "reason": "",
        "candidates": 0, "checked": 0, "skipped": [], "fails": [],
    }

    def _remaining(default=10.0):
        return max(0.5, min(default, deadline - time.time()))

    session.call("Emulation.setDeviceMetricsOverride", {
        "width": viewport[0], "height": viewport[1], "deviceScaleFactor": 1, "mobile": False,
    }, timeout=_remaining())
    if dark:
        session.call("Emulation.setEmulatedMedia", {
            "features": [{"name": "prefers-color-scheme", "value": "dark"}],
        }, timeout=_remaining())

    url = "file://" + os.path.abspath(path)
    try:
        session.navigate(url, timeout=_remaining(20.0))
    except CDPError as exc:
        result["status"] = "unmeasured"
        result["reason"] = "页面加载失败: %s" % exc
        return result

    if dark:
        # 页面用 [data-theme] 约定时同步属性(纯 media 方案已由 Emulation 覆盖)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
        except OSError:
            raw = ""
        if "[data-theme" in raw:
            session.evaluate(
                "document.documentElement.setAttribute('data-theme','dark')", timeout=_remaining())

    session.evaluate(
        "(() => { const s=document.createElement('style'); s.textContent=%s;"
        " document.head && document.head.appendChild(s); return true; })()" % json.dumps(FREEZE_CSS),
        timeout=_remaining())
    session.evaluate("document.fonts && document.fonts.ready.then(() => true)", timeout=_remaining())

    candidates, err = session.evaluate_fn(COLLECT_JS, timeout=_remaining())
    if candidates is None:
        result["status"] = "unmeasured"
        result["reason"] = "候选元素收集失败: %s" % err
        return result
    result["candidates"] = len(candidates)
    if not candidates:
        result["status"] = "unmeasured"
        result["reason"] = "页面没有可见的交互元素,无可测量目标"
        return result

    for cand in candidates:
        if time.time() > deadline:
            result["skipped"].append("测量预算耗尽,剩余候选未测")
            break
        sel = cand["sel"]
        default_read, err = session.evaluate_fn(READ_JS, sel, timeout=_remaining())
        if default_read is None:
            result["skipped"].append("%s 读取失败(元素可能在交互后消失)" % sel)
            continue
        if default_read.get("skip"):
            result["skipped"].append("%s 豁免(disabled/toggle/opacity:0)" % (default_read.get("label") or sel))
            continue

        for state in ("default", "hover", "focus"):
            if state == "hover":
                session.call("Input.dispatchMouseEvent", {
                    "type": "mouseMoved", "x": cand["x"], "y": cand["y"], "button": "none",
                }, timeout=_remaining())
                time.sleep(0.06)
            elif state == "focus":
                session.call("Input.dispatchMouseEvent", {
                    "type": "mouseMoved", "x": 0, "y": 0, "button": "none",
                }, timeout=_remaining())
                session.evaluate_fn(
                    "(sel) => { const el = document.querySelector(sel); if (el && el.focus) el.focus(); return true; }",
                    sel, timeout=_remaining())

            if state == "default":
                read, read_err = default_read, None
            else:
                read, read_err = session.evaluate_fn(READ_JS, sel, timeout=_remaining())
            if read is None:
                result["skipped"].append(
                    "%s(%s) 读取失败: %s" % (default_read.get("label") or sel, state, read_err))
                break
            if read.get("skip"):
                result["skipped"].append("%s 豁免(disabled/toggle/opacity:0)" % (read.get("label") or sel))
                break
            if read.get("bgUnknown") or not read.get("fg") or not read.get("bg"):
                result["skipped"].append(
                    "%s(%s) 背景含渐变/图像或颜色不可解析,未测量" % (read.get("label") or sel, state))
                continue

            need = needed_ratio(read.get("px") or 16.0, bool(read.get("bold")), bool(read.get("graphical")))
            ratio = contrast_ratio(read["fg"], read["bg"])
            result["checked"] += 1
            if ratio < need:
                result["fails"].append({
                    "selector": sel, "state": state,
                    "label": read.get("label") or sel,
                    "ratio": round(ratio, 2), "need": need,
                    "fg": read["fg"][:3], "bg": read["bg"][:3],
                })

        # 每轮状态测完把焦点与悬停还原,避免污染下一个元素
        session.evaluate_fn(
            "(sel) => { const el = document.querySelector(sel); if (el && el.blur) el.blur(); return true; }",
            sel, timeout=_remaining())

    if result["checked"] == 0 and result["fails"] == []:
        result["status"] = "unmeasured"
        result["reason"] = "0 个元素态可比对(候选全部豁免或背景不可知),未测量不得记为通过"
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def collect_html_files(target):
    if os.path.isfile(target):
        return [os.path.abspath(target)]
    if os.path.isdir(target):
        found = []
        for dp, dns, fns in os.walk(target):
            dns[:] = [d for d in dns if d not in ("node_modules", ".git", "dist", "build")]
            for fn in sorted(fns):
                if fn.endswith(".html"):
                    found.append(os.path.abspath(os.path.join(dp, fn)))
        return found
    return []


def _fmt_rgb(rgb):
    return "rgb(%d,%d,%d)" % (rgb[0], rgb[1], rgb[2])


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="真浏览器状态态 WCAG 对比度门禁(default/hover/focus 三态实测;"
                    "退出码见 scripts/EXIT-CODES.md)"
    )
    parser.add_argument("target", help="HTML 文件或目录")
    parser.add_argument("--dark", action="store_true", help="按暗色模式测量(prefers-color-scheme: dark)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式: text(默认) / json")
    parser.add_argument("--browser", default=None,
                        help="浏览器可执行文件路径(默认取 MALIANG_BROWSER 或 PATH 里的 Chrome/Chromium)")
    parser.add_argument("--viewport", type=parse_viewport, default=(1280, 900),
                        help="视口,形如 1280x900(默认 1280x900)")
    parser.add_argument("--timeout", type=int, default=TIMEOUT_DEFAULT_MS,
                        help="单文件测量预算毫秒(默认 %d)" % TIMEOUT_DEFAULT_MS)
    args = parser.parse_args(argv)

    target = os.path.abspath(args.target)
    files = collect_html_files(target)

    def _unmeasured(message):
        if args.format == "json":
            print(json.dumps({"status": "unmeasured", "reason": message, "files": []},
                             ensure_ascii=False))
        else:
            print("UNMEASURED: " + message)
            print("Nothing was measured. This is not a pass(见 scripts/EXIT-CODES.md)。")
        return EXIT_UNMEASURED

    if not files:
        return _unmeasured("目标不存在或没有 HTML 文件: " + target)

    binary = find_browser(args.browser)
    if not binary:
        return _unmeasured(
            "没找到浏览器(尝试过 --browser / MALIANG_BROWSER / PATH 里的 "
            + "/".join(BROWSER_CANDIDATES) + ");三态对比度必须在真浏览器里测量")

    proc = profile_dir = session = None
    started = time.time()
    results = []
    try:
        try:
            proc, profile_dir, port = launch_browser(binary)
        except CDPError as exc:
            return _unmeasured(str(exc))
        try:
            session = connect_session(port)
            session.call("Page.enable", timeout=10.0)
            session.call("Runtime.enable", timeout=10.0)
        except (CDPError, OSError, ValueError) as exc:
            return _unmeasured("DevTools 协议连接失败: %s" % exc)

        for path in files:
            try:
                results.append(measure_file(
                    session, path, dark=args.dark, viewport=args.viewport,
                    timeout_ms=args.timeout))
            except CDPError as exc:
                results.append({"file": path, "status": "unmeasured", "reason": str(exc),
                                "candidates": 0, "checked": 0, "skipped": [], "fails": []})
    finally:
        if session:
            session.close()
        stop_browser(proc, profile_dir)

    unmeasured = [r for r in results if r["status"] != "measured"]
    checked = sum(r["checked"] for r in results)
    fails = [f for r in results for f in r["fails"]]

    if args.format == "json":
        print(json.dumps({
            "status": "unmeasured" if unmeasured else ("fail" if fails else "ok"),
            "checked": checked,
            "results": [
                {
                    "file": os.path.relpath(r["file"], os.path.dirname(target)) if os.path.isdir(target) else os.path.basename(r["file"]),
                    "status": r["status"], "reason": r["reason"],
                    "candidates": r["candidates"], "checked": r["checked"],
                    "skipped": r["skipped"][:20], "fails": r["fails"],
                }
                for r in results
            ],
        }, ensure_ascii=False, indent=2))
    else:
        print("maliang verify-states —— 真浏览器 default/hover/focus 三态对比度")
        print("浏览器: %s | 视口: %dx%d%s" % (binary, args.viewport[0], args.viewport[1], " | dark" if args.dark else ""))
        for r in results:
            rel = os.path.relpath(r["file"], os.path.dirname(target)) if os.path.isdir(target) else os.path.basename(r["file"])
            if r["status"] != "measured":
                print("UNMEASURED %s —— %s" % (rel, r["reason"]))
                continue
            print("%s: %d 个可比对元素态(候选 %d)" % (rel, r["checked"], r["candidates"]))
            for skip in r["skipped"][:8]:
                print("   - 跳过: " + skip)
            for f in r["fails"]:
                print("   [ERROR] %-7s \"%s\" %.2f:1 < %.1f:1  [%s on %s]  %s"
                      % (f["state"], f["label"], f["ratio"], f["need"],
                         _fmt_rgb(f["fg"]), _fmt_rgb(f["bg"]), f["selector"]))
        print("")
        print("合计: %d 个元素态已测量,%d 处低于 WCAG AA,%.1fs"
              % (checked, len(fails), time.time() - started))

    if unmeasured:
        if args.format == "text":
            print("判定: UNMEASURED —— 部分目标没能检查,不得记为通过(退出码 2)")
        return EXIT_UNMEASURED
    if fails:
        return EXIT_FINDINGS
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
