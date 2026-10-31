#!/usr/bin/env python3
"""verify —— 浏览器/像素实测域合并入口(6→1)。

用法(子命令 + 各自原参数透传):
    python3 scripts/verify.py states <preview.html> [options]            # 三态对比度/焦点实测
    python3 scripts/verify.py interactive <preview.html> [options]       # 交互真实性三信号
    python3 scripts/verify.py color-fidelity <impl> --reference <ref>    # 逐色保真 ΔE(G39)
    python3 scripts/verify.py assets <preview.html> [options]            # 资产位在场验证(G40)
    python3 scripts/verify.py measure-colors <图片> [options]            # 图片确定性测色
    python3 scripts/verify.py palette-solver <参数>                      # OKLCH 亮度求解 + 配对矩阵

退出码: 各子命令沿用原脚本三态语义,canonical 见 scripts/EXIT-CODES.md。
各节实现为原独立脚本全文并入;interactive 节原经 importlib 动态加载
verify-states,合并后同文件直接引用;同名冲突按节改名(COLLECT_JS_INTERACTIVE /
contrast_ratio_hex_pair)。依赖: Python 3 标准库;states/interactive 需浏览器,
无浏览器自报 UNMEASURED(退出码 2)。
"""
import sys

_SUBCOMMANDS = ("states", "interactive", "color-fidelity", "assets",
                "measure-colors", "palette-solver")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("usage: verify.py {" + "|".join(_SUBCOMMANDS) + "} [args...]")
        return 2
    dispatch = {
        "states": _main_states,
        "interactive": _main_interactive,
        "color-fidelity": _main_color_fidelity,
        "assets": _main_assets,
        "measure-colors": _main_measure_colors,
        "palette-solver": _main_palette_solver,
    }
    if argv[0] not in dispatch:
        print("[ERROR] 未知子命令: " + argv[0] + "(可用: " + ", ".join(_SUBCOMMANDS) + ")")
        return 2
    return dispatch[argv[0]](argv[1:])


# ============================================================
# 来源节: verify-states.py (子命令: states)

# ---- 原 verify-states.py 模块说明 ----
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
     scripts/_targets.mjs(三态退出码、「未测量不算通过」)
     浏览器驱动为本地自研的轻量 CDP 实现(不引入 Playwright)。
"""
# ---- 模块说明结束 ----
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
    import maliang_common
    l1 = maliang_common.relative_luminance(maliang_common.blend_alpha(fg, bg))
    l2 = maliang_common.relative_luminance(tuple(v / 255.0 for v in bg[:3]))
    return maliang_common.contrast_ratio(l1, l2)


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
            _close_streams(proc)
            shutil.rmtree(profile_dir, ignore_errors=True)
            raise CDPError("浏览器提前退出: " + err.strip()[-300:])
        if os.path.exists(port_file):
            with open(port_file, "r", encoding="utf-8") as fh:
                first = fh.read().splitlines()
            if first:
                return proc, profile_dir, int(first[0])
        time.sleep(0.05)
    proc.terminate()
    _close_streams(proc)
    shutil.rmtree(profile_dir, ignore_errors=True)
    raise CDPError("浏览器启动超时(DevToolsActivePort 未出现)")


def _close_streams(proc):
    """关掉 Popen 开的管道,否则未读的 stderr 管道在 GC 时抛 ResourceWarning。"""
    for stream in (proc.stdin, proc.stdout, proc.stderr):
        if stream is not None:
            try:
                stream.close()
            except OSError:
                pass


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
        if proc is not None:
            _close_streams(proc)
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


def _main_states(argv=None):
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


# ============================================================
# 来源节: verify-interactive.py (子命令: interactive)

# ---- 原 verify-interactive.py 模块说明 ----
"""交互真实性门禁:声明了状态契约的控件,点击后必须真的兑现。

用法:
    python3 scripts/verify-interactive.py <html_file_or_dir> [--dark]
                                          [--format {text,json}] [--advisory]
                                          [--browser PATH] [--viewport WxH] [--timeout MS]

三个信号:
  [A] dead —— 控件声明了 aria-pressed / aria-expanded / aria-checked /
      aria-selected / aria-sort 或 state-bearing role(switch/tab/menuitemcheckbox/
      menuitemradio/option),真实点击后整页毫无变化(属性、DOM、焦点都没动)。
      控件承诺了状态却不兑现 → 失败。
  [B] inert —— 普通按钮点击无任何可观察效果。demo 页面合法地会摆静态按钮,
      只作 advisory 提示,不失败。
  [C] invisible —— 状态属性翻转了,但控件自身及内部的计算样式、文本、几何
      完全一致:屏幕阅读器听得见、肉眼看不见 → 失败。
豁免:`data-demo-state` 属性 = 作者显式声明「这是状态渲染展示,不是活控件」,
      由作者手写,门禁不推断。
每次点击都在全新加载的页面上进行,一个控件的残留状态不会掩盖另一个。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        没装浏览器 / 目标不存在 / 一个控件都没点到 → UNMEASURED + 2。
依赖: Python 3 标准库 + 本机 Chrome/Chromium(共享 scripts/verify-states.py 的
      CDP 轻实现)。
"""
# ---- 模块说明结束 ----
import argparse
import importlib.util
import json
import os
import sys
import time

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)






STATE_ATTRS = ["aria-pressed", "aria-expanded", "aria-checked", "aria-selected", "aria-sort"]
STATE_ROLES = ["switch", "tab", "menuitemcheckbox", "menuitemradio", "option"]

CLICKABLE = (
    'button,[role="button"],input[type="checkbox"],input[type="radio"],'
    '[role="switch"],[role="tab"],[role="option"],[role="menuitemcheckbox"],'
    '[role="menuitemradio"],summary'
)

# 候选采集:可见、未禁用、无 data-demo-state 豁免、排除表单提交/文件控件。
COLLECT_JS_INTERACTIVE = r"""
({ attrs, roles, clickable }) => {
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
    return cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity) !== 0
      && r.width > 0 && r.height > 0 && !el.closest('[hidden]');
  };
  const out = [];
  for (const el of document.querySelectorAll(clickable)) {
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    if (el.hasAttribute('data-demo-state')) continue;   // 状态渲染展示,作者已声明
    if (el.type === 'file') continue;
    if (el.form && (el.type === 'submit' || el.type === 'reset')) continue;
    if (!visible(el)) continue;
    const owner = el.closest('th,[role="columnheader"],[role="tab"],[role="option"]') || el;
    const declared = attrs.filter((a) => el.hasAttribute(a) || owner.hasAttribute(a));
    const role = el.getAttribute('role') || '';
    out.push({
      sel: path(el),
      label: el.tagName.toLowerCase()
        + (typeof el.className === 'string' && el.className.trim()
          ? '.' + el.className.trim().split(/\s+/)[0] : '')
        + (el.textContent ? ' 「' + el.textContent.replace(/\s+/g, ' ').trim().slice(0, 22) + '」' : ''),
      declares: [...declared, ...(roles.includes(role) ? ['role=' + role] : [])],
      native: el.tagName === 'INPUT',
    });
  }
  return out;
}
"""

# 点击前后要观察的「变化」:整页 mutation 计数 + 焦点是否移走。
WATCH_JS = r"""
() => {
  window.__maliangMut = 0;
  window.__maliangFocus = document.activeElement;
  const observer = new MutationObserver((records) => { window.__maliangMut += records.length; });
  observer.observe(document.documentElement,
    { attributes: true, childList: true, subtree: true, characterData: true });
  return true;
}
"""

# 点完读回:自己获得焦点不算变化(浏览器行为),焦点落到别处才算。
CHANGED_JS = r"""
(sel) => {
  const me = document.querySelector(sel);
  const now = document.activeElement;
  return { mut: window.__maliangMut, focusMoved: window.__maliangFocus !== now && now !== me };
}
"""

# 控件「看起来什么样」的指纹:自身与内部所有元素的计算样式 + 几何 + 文本。
FINGERPRINT_JS = r"""
(sel) => {
  const root = document.querySelector(sel);
  if (!root) return null;
  const props = ['backgroundColor', 'color', 'borderColor', 'borderWidth', 'boxShadow',
    'transform', 'opacity', 'outlineColor', 'backgroundImage', 'textDecorationLine', 'fontWeight'];
  const one = (el) => {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    return props.map((p) => cs[p]).join('|') + '|' + Math.round(r.width) + 'x' + Math.round(r.height)
      + '|' + (el.getAttribute('href') || '');
  };
  const parts = [one(root), (root.textContent || '').replace(/\s+/g, ' ').trim()];
  for (const el of root.querySelectorAll('*')) parts.push(one(el));
  return parts.join('~');
}
"""

STATE_OF_JS = r"""
({ sel, attrs }) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const owner = el.closest('th,[role="columnheader"],[role="tab"],[role="option"]') || el;
  return attrs.map((a) => a + '=' + (el.getAttribute(a) ?? owner.getAttribute(a) ?? '')).join(',');
}
"""

CLICK_POINT_JS = r"""
(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  el.scrollIntoView({ block: 'center', inline: 'center' });
  const r = el.getBoundingClientRect();
  return [r.left + r.width / 2, r.top + r.height / 2];
}
"""


def verify_file(session, path, dark=False, viewport=(1280, 900),
                timeout_ms=TIMEOUT_DEFAULT_MS, advisory=False):
    """点击一个文件里的每个候选控件,返回结果 dict(不抛业务异常)。"""
    deadline = time.time() + timeout_ms / 1000.0
    result = {"file": path, "status": "measured", "reason": "",
              "candidates": 0, "checked": 0, "dead": [], "invisible": [], "inert": [], "skipped": []}

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
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            raw_html = fh.read()
    except OSError:
        raw_html = ""

    def _fresh_load():
        """每次点击前重新加载,候选之间互不污染。"""
        if not session.navigate(url, timeout=_remaining(20.0)):
            return False
        if dark:
            session.call("Emulation.setEmulatedMedia", {"features": [
                {"name": "prefers-color-scheme", "value": "dark"},
            ]}, timeout=_remaining())
            if "[data-theme" in raw_html:
                session.evaluate(
                    "document.documentElement.setAttribute('data-theme','dark')", timeout=_remaining())
        session.evaluate(
            "(() => { const s=document.createElement('style'); s.textContent=%s;"
            " document.head && document.head.appendChild(s); return true; })()" % json.dumps(FREEZE_CSS),
            timeout=_remaining())
        session.evaluate_fn(WATCH_JS, timeout=_remaining())
        return True

    if not _fresh_load():
        result["status"] = "unmeasured"
        result["reason"] = "页面加载失败"
        return result

    candidates, err = session.evaluate_fn(
        COLLECT_JS_INTERACTIVE, {"attrs": STATE_ATTRS, "roles": STATE_ROLES, "clickable": CLICKABLE},
        timeout=_remaining())
    if candidates is None:
        result["status"] = "unmeasured"
        result["reason"] = "候选控件收集失败: %s" % err
        return result
    result["candidates"] = len(candidates)

    for cand in candidates:
        if time.time() > deadline:
            result["skipped"].append("测量预算耗尽,剩余控件未点击")
            break
        sel = cand["sel"]
        # 原生 checkbox/radio 由浏览器自己翻转,不构成「控件兑现契约」的证据
        if cand.get("native") and not cand.get("declares"):
            result["skipped"].append(cand["label"] + " 原生勾选控件(浏览器自身行为)")
            continue
        if not _fresh_load():
            result["skipped"].append(cand["label"] + " 重新加载失败,跳过点击")
            continue
        point, err = session.evaluate_fn(CLICK_POINT_JS, sel, timeout=_remaining())
        if point is None:
            result["skipped"].append(cand["label"] + " 重新加载后找不到该控件(动态渲染)")
            continue

        declared_attrs = [d for d in cand["declares"] if not d.startswith("role=")]
        before = None
        state_before = None
        if cand["declares"]:
            before, _err = session.evaluate_fn(FINGERPRINT_JS, sel, timeout=_remaining())
            if declared_attrs:
                state_before, _err = session.evaluate_fn(
                    STATE_OF_JS, {"sel": sel, "attrs": declared_attrs}, timeout=_remaining())

        x, y = point
        click_error = None
        try:
            session.call("Input.dispatchMouseEvent", {
                "type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1,
            }, timeout=_remaining())
            session.call("Input.dispatchMouseEvent", {
                "type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1,
            }, timeout=_remaining())
            time.sleep(0.08)
        except CDPError as exc:
            click_error = str(exc)

        if click_error:
            # 点不到不是证据(ux-ui 同口径:could not click: not evidence)
            result["skipped"].append(cand["label"] + " 无法点击: " + click_error)
            continue

        changed, err = session.evaluate_fn(CHANGED_JS, sel, timeout=_remaining())
        if changed is None:
            result["skipped"].append(cand["label"] + " 点击后状态读取失败")
            continue
        state_after = None
        after = None
        if cand["declares"]:
            time.sleep(0.26)  # 等一次过渡走完再比指纹
            after, _err = session.evaluate_fn(FINGERPRINT_JS, sel, timeout=_remaining())
            if declared_attrs:
                state_after, _err = session.evaluate_fn(
                    STATE_OF_JS, {"sel": sel, "attrs": declared_attrs}, timeout=_remaining())

        result["checked"] += 1
        where = os.path.basename(path) + "  " + cand["label"]
        moved = changed.get("mut", 0) > 0 or changed.get("focusMoved")
        if moved:
            state_moved = (state_before is not None and state_after is not None
                           and state_before != state_after)
            if state_moved and before and after and before == after:
                result["invisible"].append(
                    where + " —— " + ", ".join(cand["declares"]) + " 翻转了,但控件外观完全没变")
            continue
        if cand["declares"]:
            result["dead"].append(
                where + " —— 声明了 " + ", ".join(cand["declares"]) + ",但点击后整页毫无变化")
        else:
            result["inert"].append(where + " —— 点击没有任何可观察效果")

    if result["checked"] == 0:
        result["status"] = "unmeasured"
        result["reason"] = "0 个控件被真实点到(候选 %d 个全部跳过),未测量不得记为通过" % result["candidates"]
    return result


def _main_interactive(argv=None):
    parser = argparse.ArgumentParser(
        description="交互真实性门禁:A 死状态契约 / B 惰性控件(advisory)/ C 隐形状态;"
                    "退出码见 scripts/EXIT-CODES.md"
    )
    parser.add_argument("target", help="HTML 文件或目录")
    parser.add_argument("--dark", action="store_true", help="按暗色模式点击测量")
    parser.add_argument("--advisory", action="store_true",
                        help="只报告不失败(A/C 信号也仅提示,退出码保持 0)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式: text(默认) / json")
    parser.add_argument("--browser", default=None,
                        help="浏览器可执行文件路径(默认取 MALIANG_BROWSER 或 PATH 里的 Chrome/Chromium)")
    parser.add_argument("--viewport", type=parse_viewport, default=(1280, 900),
                        help="视口,形如 1280x900(默认 1280x900)")
    parser.add_argument("--timeout", type=int, default=TIMEOUT_DEFAULT_MS,
                        help="单文件预算毫秒(默认 %d)" % TIMEOUT_DEFAULT_MS)
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
            + "/".join(BROWSER_CANDIDATES) + ");交互真实性必须在真浏览器里点击测量")

    proc = profile_dir = session = None
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
                results.append(verify_file(
                    session, path, dark=args.dark, viewport=args.viewport,
                    timeout_ms=args.timeout, advisory=args.advisory))
            except CDPError as exc:
                results.append({"file": path, "status": "unmeasured", "reason": str(exc),
                                "candidates": 0, "checked": 0, "dead": [], "invisible": [],
                                "inert": [], "skipped": []})
    finally:
        if session:
            session.close()
        stop_browser(proc, profile_dir)

    unmeasured = [r for r in results if r["status"] != "measured"]
    checked = sum(r["checked"] for r in results)
    dead = [d for r in results for d in r["dead"]]
    invisible = [i for r in results for i in r["invisible"]]
    inert = [i for r in results for i in r["inert"]]
    hard = dead + invisible

    if args.format == "json":
        print(json.dumps({
            "status": "unmeasured" if unmeasured else ("fail" if (hard and not args.advisory) else "ok"),
            "checked": checked, "advisory": args.advisory,
            "dead": dead, "invisible": invisible, "inert": inert,
            "results": [
                {"file": r["file"], "status": r["status"], "reason": r["reason"],
                 "candidates": r["candidates"], "checked": r["checked"],
                 "skipped": r["skipped"][:20]}
                for r in results
            ],
        }, ensure_ascii=False, indent=2))
    else:
        print("maliang verify-interactive —— 交互真实性(A 死状态契约 / B 惰性 / C 隐形状态)")
        print("浏览器: %s | 视口: %dx%d%s" % (binary, args.viewport[0], args.viewport[1],
                                             " | dark" if args.dark else ""))
        for r in results:
            rel = (os.path.relpath(r["file"], os.path.dirname(target))
                   if os.path.isdir(target) else os.path.basename(r["file"]))
            if r["status"] != "measured":
                print("UNMEASURED %s —— %s" % (rel, r["reason"]))
                continue
            print("%s: 点击 %d 个控件(候选 %d)" % (rel, r["checked"], r["candidates"]))
            for item in r["skipped"][:8]:
                print("   - 跳过: " + item)
        if dead:
            print("")
            print("FAIL%s —— 控件承诺了状态却不兑现:" % ("(advisory)" if args.advisory else ""))
            for item in dead:
                print("   x [A dead] " + item)
            print("   修法:接上处理器让状态属性真的变化,或停止声明该状态(连同它的外观暗示一起删)。")
        if invisible:
            print("")
            print("FAIL%s —— 状态变化没人看得见:" % ("(advisory)" if args.advisory else ""))
            for item in invisible:
                print("   x [C invisible] " + item)
            print("   修法:让控件自身有视觉状态——轨道填充、图标切换、文案变化;"
                  "只翻转 aria 属性只服务屏幕阅读器。")
        if inert:
            print("")
            print("(advisory) %d 个控件点击无效果(demo 静态按钮合法,只提示):" % len(inert))
            for item in inert[:8]:
                print("   - [B inert] " + item)
            if len(inert) > 8:
                print("   ... 其余 %d 个" % (len(inert) - 8))
        print("")
        print("合计: %d 个控件已被真实点击,%d 处 A/C 失败,%d 处 B 提示" % (checked, len(hard), len(inert)))

    if unmeasured:
        if args.format == "text":
            print("判定: UNMEASURED —— 部分目标没能检查,不得记为通过(退出码 2)")
        return EXIT_UNMEASURED
    if hard and not args.advisory:
        return EXIT_FINDINGS
    return EXIT_OK


# ============================================================
# 来源节: verify-color-fidelity.py (子命令: color-fidelity)

# ---- 原 verify-color-fidelity.py 模块说明 ----
"""生成端 ΔE 验收回路(G39 脚本层):重建截图 vs 参考图逐色保真打分。

「好不好看」判断不了,「颜色对不对」可以变成数字。本脚本把实现图与参考
测量做逐色对账:

  阈值:mean ΔE ≤5(实现侧覆盖加权均值)/ max ΔE ≤20(双侧显著簇)/
       coverage drift ≤0.35(逐参考色 |参考覆盖-实现覆盖| 之和)。
  显著线:覆盖 <0.5% 的簇/残渣不计入 max ΔE,也不算「保留了该色」。

反聚合盲区设计(对应 tests/test_verify_color_fidelity.py 五组攻击用例):
  - 实现侧显著错误色块逐簇单独计分,不得被覆盖率加权平均掉;
  - 大错误区域配稀有参考色(参考侧覆盖 <0.5%)仍走实现侧逐簇 max 暴露;
  - 显著参考色在实现侧缺失 → 参考侧 max ΔE 反向暴露;
  - 0.1% 残渣不算保留(显著参考色的最近匹配只在显著实现簇里找);
  - coverage drift 保留 4 位小数,0.3502 > 0.35 的边界失败可解释。

用法:
    python3 scripts/verify-color-fidelity.py <impl.png> --reference <ref.png|spec.json>

参考输入二选一形态:
  - 参考图(PNG):脚本先用 measure-colors 同管线测出 palette(k 可由 --k 覆盖);
  - 测量 spec(JSON):measure-colors 的输出,或嵌套
    {"design_system":{"color":{"measured_palette":[...],"measurement":{"k":...}}}}。
    复测必须与测量同 k(否则不可比)——spec 带 k 时以 spec 为准。

输出(stdout JSON):逐色报告(每个参考色的最近实现色/ΔE/覆盖、每个实现簇
的最近参考色/ΔE/覆盖)+ 汇总与 PASS/FAIL。

退出码: 见 scripts/EXIT-CODES.md(0=PASS / 1=FAIL(任一阈值不过) / 2=没能检查;#16)。
依赖: Python 3 标准库;JPEG 需 Pillow(缺失 → UNMEASURED/2,同 measure-colors)。
"""
# ---- 模块说明结束 ----
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

THRESHOLD_MEAN_DE = 5.0
THRESHOLD_MAX_DE = 20.0
THRESHOLD_DRIFT = 0.35
SIGNIFICANT_COVERAGE = 0.005




def parse_hex(s):
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError("bad hex: %r" % s)
    return [int(s[i:i + 2], 16) for i in (0, 2, 4)]


def load_reference(reference_path, k_override):
    """读参考:PNG 测量或 spec JSON;返回 (palette, k)。UNMEASURED 抛异常。"""
    ext = os.path.splitext(reference_path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg"):
        result = measure_image(reference_path, k_override or DEFAULT_K)
        return result["palette"], result["measurement"]["k"]
    try:
        with open(reference_path, "r", encoding="utf-8") as fh:
            spec = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise UnmeasurableError("参考 spec 不可读: %s" % exc)
    palette = spec.get("palette")
    if palette is None:
        palette = (spec.get("design_system") or {}).get("color", {}).get("measured_palette")
    if not isinstance(palette, list) or not palette:
        raise UnmeasurableError(
            "参考 spec 须含 palette 数组(measure-colors 输出)或"
            " design_system.color.measured_palette"
        )
    for entry in palette:
        if not isinstance(entry, dict) or not isinstance(entry.get("coverage"), (int, float)) \
                or not isinstance(entry.get("hex"), str):
            raise UnmeasurableError("参考 palette 条目形态非法(须为 {hex, coverage} 对象)")
        try:
            parse_hex(entry["hex"])
        except ValueError as exc:
            raise UnmeasurableError("参考 palette hex 非法: %s" % exc)
    cfg_k = k_override
    if cfg_k is None:
        cfg_k = (spec.get("measurement") or {}).get("k")
        if cfg_k is None:
            cfg_k = ((spec.get("design_system") or {}).get("color", {}).get("measurement") or {}).get("k")
    k = max(2, min(16, int(cfg_k))) if cfg_k else DEFAULT_K
    return palette, k


def verify(impl_result, ref_palette, ref_k):
    """核心对账:返回报告 dict(pass 字段 + 逐色条目)。impl_result 是 measure 输出。"""
    d_e = delta_e

    # 重新测量实现图时必须用与参考相同的 k(复测同参数否则不可比)
    impl_k = impl_result["measurement"]["k"]

    # 实现簇按最近参考色分组;参考色的组合覆盖 = 组内簇覆盖之和
    assigned = [[] for _ in ref_palette]
    for c in impl_result["palette"]:
        best, bd = 0, float("inf")
        for i, s in enumerate(ref_palette):
            d = d_e(parse_hex(s["hex"]), parse_hex(c["hex"]))
            if d < bd:
                bd, best = d, i
        entry = dict(c)
        entry["deltaE"] = bd
        assigned[best].append(entry)

    significant_impl = [c for c in impl_result["palette"] if c["coverage"] >= SIGNIFICANT_COVERAGE]

    entries = []
    for i, s in enumerate(ref_palette):
        group = assigned[i]
        cov = sum(g["coverage"] for g in group)
        # 显著参考色的「最近实现色」只在显著实现簇里找:亚百分比残渣不算保留
        candidates = significant_impl if (s.get("coverage", 0) >= SIGNIFICANT_COVERAGE
                                          and significant_impl) else impl_result["palette"]
        nearest, nd = None, float("inf")
        for c in candidates:
            d = d_e(parse_hex(s["hex"]), parse_hex(c["hex"]))
            if d < nd:
                nd, nearest = d, c["hex"]
        entries.append({
            "specHex": s["hex"], "role": s.get("role", "unassigned"),
            "nearestImageHex": nearest, "deltaE": round(nd, 2),
            "specCoverage": s.get("coverage", 0.0), "imageCoverage": round(cov, 4),
        })

    # 实现簇逐簇计分:显著错误色块不得被加权平均掩盖
    impl_clusters = []
    for c in impl_result["palette"]:
        best, bd, role = None, float("inf"), None
        for s in ref_palette:
            d = d_e(parse_hex(c["hex"]), parse_hex(s["hex"]))
            if d < bd:
                bd, best, role = d, s["hex"], s.get("role")
        impl_clusters.append({
            "imageHex": c["hex"], "imageCoverage": c["coverage"],
            "nearestSpecHex": best, "nearestSpecRole": role, "deltaE": round(bd, 2),
        })

    # mean ΔE 按实现侧实际覆盖加权;遗漏色由 drift 与参考侧 max 暴露
    weighted = sum(c["deltaE"] * c["imageCoverage"] for c in impl_clusters)
    weight = sum(c["imageCoverage"] for c in impl_clusters)
    mean_de = weighted / weight if weight > 0 else 0.0
    drift = sum(abs(e["specCoverage"] - e["imageCoverage"]) for e in entries)

    sig_impl_de = [c["deltaE"] for c in impl_clusters if c["imageCoverage"] >= SIGNIFICANT_COVERAGE]
    sig_ref_de = [e["deltaE"] for e in entries if e["specCoverage"] >= SIGNIFICANT_COVERAGE]
    max_de = max([0.0] + sig_impl_de + sig_ref_de)

    passed = (mean_de <= THRESHOLD_MEAN_DE and max_de <= THRESHOLD_MAX_DE
              and drift <= THRESHOLD_DRIFT)
    return {
        "entries": entries,
        "implementationClusters": impl_clusters,
        "meanDeltaE": round(mean_de, 2),
        "maxDeltaE": round(max_de, 2),
        # 保留足够精度解释边界失败(如 0.3502 > 0.35)
        "coverageDrift": round(drift, 4),
        "measurement": {"k": impl_k, "reference_k": ref_k},
        "thresholds": {
            "meanDeltaE": THRESHOLD_MEAN_DE,
            "maxDeltaE": THRESHOLD_MAX_DE,
            "coverageDrift": THRESHOLD_DRIFT,
            "significantCoverage": SIGNIFICANT_COVERAGE,
        },
        "pass": passed,
    }


def _main_color_fidelity(argv=None):
    parser = argparse.ArgumentParser(
        description="ΔE 保真验证(G39):mean ΔE≤5 / max ΔE≤20 / coverage drift≤0.35,逐色报告"
    )
    parser.add_argument("image", help="实现图(.png;JPEG 需 Pillow)")
    parser.add_argument("--reference", required=True,
                        help="参考:参考图(.png)或测量 spec JSON(measure-colors 输出)")
    parser.add_argument("--k", type=int, default=None,
                        help="测量簇数(参考为图时生效;spec 自带 k 时以 spec 为准)")
    args = parser.parse_args(argv)

    for p in (args.image, args.reference):
        if not os.path.isfile(p):
            print("verify-color-fidelity: UNMEASURED —— 文件不存在: %s" % p, file=sys.stderr)
            return 2
    try:
        ref_palette, ref_k = load_reference(args.reference, args.k)
        impl_result = measure_image(args.image, ref_k)
    except UnmeasurableError as exc:
        print(json.dumps({"measured": False, "unmeasured_reason": str(exc)}, ensure_ascii=False))
        print("verify-color-fidelity: UNMEASURED —— %s" % exc, file=sys.stderr)
        return 2

    report = verify(impl_result, ref_palette, ref_k)
    report["implementation"] = os.path.basename(args.image)
    report["reference"] = os.path.basename(args.reference)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    verdict = "PASS" if report["pass"] else "FAIL"
    print("%s — mean ΔE %.2f, max ΔE %.2f, coverage drift %.4f" % (
        verdict, report["meanDeltaE"], report["maxDeltaE"], report["coverageDrift"]),
        file=sys.stderr)
    return 0 if report["pass"] else 1


# ============================================================
# 来源节: verify-assets.py (子命令: assets)

# ---- 原 verify-assets.py 模块说明 ----
"""资产在场后置验收门(G40 脚本层):品牌/内容资产渲染在场验证。

生成后逐资产位核验:
  1. 逐资产位枚举:数出页面里应有的图槽(<img>/<svg>/<picture> 与 CSS
     background-image)与 logo 位;
  2. 逐一验证渲染的是**声明的真实资产**:manifest 里声明的 URL / assetKey
     必须真的出现在对应资产位——「把资产传给了生成器」不是在场证明;
  3. 显式拒绝五类顶替物:灰 div 占位 / emoji / 首字母 / 纯文字 SVG /
     data-URI 空壳;
  4. 每个发现附最小确定性修复指令(把哪个槽换成声明的 URL);
  5. 复查仍失败 → 如实上报退出码 1,禁止宣称完成。

诚实范围声明:本脚本是**结构化 HTML 验证,不冒充视觉 QA**——视觉还原
仍按 preview 截图走查执行。

manifest 形态(JSON 数组,缺省 assets.json 随产物放 .maliang/):
    [{"slot": "logo", "assetKey": "acme-logo",
      "url": "https://cdn.example.com/acme-logo.svg",
      "selector": "#logo"}]        # selector 可选:限定核验的容器
url 也可为本仓相对路径(file 资产,存在性当场核验)。

退出码: 见 scripts/EXIT-CODES.md(0=在场验证通过 / 1=有发现 / 2=没能检查;#16)。
依赖: Python 3 标准库。
"""
# ---- 模块说明结束 ----
import argparse
import json
import os
import re
import sys

# 顶替物签名
_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2728\u26A1\u2705\u274C\u2B50\u2757\u2764]")
_SINGLE_INITIAL_RE = re.compile(r"^\s*([A-Za-z])\s*$")
_PLACEHOLDER_TOKEN_RE = re.compile(
    r"\b(?:placeholder|skeleton|lorem|dummy|sample-logo|logo-here|tbd)\b", re.IGNORECASE
)
_DATA_URI_RE = re.compile(r"data:image/[a-z+]+;base64,", re.IGNORECASE)
# 自造 SVG:内联 <svg> 且仅含 <text>(没有引用外部资产)
_TEXT_ONLY_SVG_RE = re.compile(
    r"<svg\b[^>]*>(?:(?!</svg>).)*?<text(?:(?!</svg>).)*?</svg>", re.DOTALL | re.IGNORECASE
)
_ASSET_SLOTS_RE = re.compile(r"<(?:img|picture|svg)\b", re.IGNORECASE)
_BG_IMAGE_RE = re.compile(r"background-image\s*:\s*url\((['\"]?)([^'\")]+)\1\)", re.IGNORECASE)
_LOGO_HINT_RE = re.compile(r"logo|brand|mark", re.IGNORECASE)
_IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_ATTR_SRC_RE = re.compile(r"\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
_ATTR_ALT_RE = re.compile(r"\balt\s*=\s*[\"']([^\"']*)[\"']", re.IGNORECASE)
_ATTR_CLASS_RE = re.compile(r"\bclass\s*=\s*[\"']([^\"']*)[\"']", re.IGNORECASE)


def extract_asset_slots(html):
    """枚举资产位:img 标签、内联 svg、CSS background-image。返回描述列表。"""
    slots = []
    for m in _IMG_TAG_RE.finditer(html):
        tag = m.group(0)
        line = html.count("\n", 0, m.start()) + 1
        src = _ATTR_SRC_RE.search(tag)
        alt = _ATTR_ALT_RE.search(tag)
        cls = _ATTR_CLASS_RE.search(tag)
        slots.append({
            "kind": "img", "line": line,
            "src": src.group(1) if src else "",
            "alt": alt.group(1) if alt else "",
            "cls": cls.group(1) if cls else "",
        })
    for m in _TEXT_ONLY_SVG_RE.finditer(html):
        line = html.count("\n", 0, m.start()) + 1
        cls = _ATTR_CLASS_RE.search(m.group(0))
        slots.append({"kind": "inline-svg", "line": line, "src": "",
                      "alt": "", "cls": cls.group(1) if cls else ""})
    for m in _BG_IMAGE_RE.finditer(html):
        line = html.count("\n", 0, m.start()) + 1
        slots.append({"kind": "bg-image", "line": line, "src": m.group(2), "alt": "", "cls": ""})
    return slots


_ASSET_EXT_RE = re.compile(r"\.(?:svg|png|jpe?g|webp|gif|avif)$", re.IGNORECASE)


def _is_asset_ref(src):
    """src 是否形似资产引用(http(s)/绝对/相对路径/数据 URI/图片扩展名)。"""
    if src.startswith(("http://", "https://", "/", "data:", "./", "../")):
        return True
    return bool(_ASSET_EXT_RE.search(src.split("?", 1)[0]))


def substitute_findings(slot, declared_urls, declared_keys):
    """对一个资产位跑五类顶替物签名;返回发现消息列表(空 = 干净)。"""
    msgs = []
    src = (slot.get("src") or "").strip()
    is_declared = src in declared_urls or any(k in src for k in declared_keys if k)
    if slot["kind"] == "img":
        if not src:
            msgs.append("img 无 src(空壳图槽)")
        elif not _is_asset_ref(src):
            msgs.append("img src 不是资产引用: %s" % src[:60])
        elif _DATA_URI_RE.match(src) and len(src) < 512:
            msgs.append("data-URI 空壳图(<512B): %s…" % src[:60])
        if _PLACEHOLDER_TOKEN_RE.search(src) or _PLACEHOLDER_TOKEN_RE.search(slot.get("cls", "")):
            msgs.append("占位签名(placeholder/skeleton/tbd)未替换: %s" % (src or slot.get("cls", ""))[:60])
    if slot["kind"] == "inline-svg" and _LOGO_HINT_RE.search(slot.get("cls", "")):
        msgs.append("logo 位渲染自造内联 SVG(纯文字/手绘 path),未见声明资产引用")
    if slot["kind"] == "bg-image" and _PLACEHOLDER_TOKEN_RE.search(slot["src"]):
        msgs.append("背景图占位未替换: %s" % slot["src"][:60])
    # emoji 顶替:alt 或 bg 段内 emoji
    if _EMOJI_RE.search(slot.get("alt", "")):
        msgs.append("alt 里是 emoji,不是声明资产: %s" % slot["alt"][:40])
    return msgs, is_declared


def verify_assets(html, manifest, html_path):
    """主核验:返回 (findings, warnings, summary)。"""
    findings = []
    warnings = []
    slots = extract_asset_slots(html)
    declared_urls = {str(a.get("url", "")).strip() for a in manifest if a.get("url")}
    declared_keys = {str(a.get("assetKey", "")).strip() for a in manifest if a.get("assetKey")}
    basename = os.path.basename(html_path)

    # ① 声明资产必须在场
    blob = html
    for asset in manifest:
        slot_name = asset.get("slot") or asset.get("assetKey") or "未命名"
        url = str(asset.get("url", "")).strip()
        key = str(asset.get("assetKey", "")).strip()
        hit = False
        if url:
            hit = url in blob or (not url.startswith("http") and os.path.basename(url) in blob)
        if not hit and key:
            hit = bool(re.search(r"[\w-]*%s" % re.escape(key), blob))
        if not hit:
            findings.append({
                "file": basename, "slot": slot_name,
                "message": "声明资产未在场(slot=%s):url/assetKey 均未出现在产物中"
                           "——「传给生成器」不是在场证明;最小修复:把对应图槽 src 换成 %s"
                           % (slot_name, url or key),
            })

    # ② 逐槽顶替物扫描
    for slot in slots:
        msgs, _ = substitute_findings(slot, declared_urls, declared_keys)
        for msg in msgs:
            findings.append({"file": basename, "slot": "line %d" % slot["line"], "message": msg})

    # ③ 数量对账:声明的槽位 vs 页面实际资产位(枚举数出应有图槽)
    if len(manifest) > len(slots):
        warnings.append(
            "manifest 声明 %d 个资产位,页面只枚举出 %d 个资产位——有声明无槽位,核对选择器"
            % (len(manifest), len(slots))
        )
    return findings, warnings, {"manifest_slots": len(manifest), "enum_slots": len(slots)}


def _main_assets(argv=None):
    parser = argparse.ArgumentParser(
        description="资产在场验证(G40):枚举资产位→验证声明资产渲染在场→拒绝五类顶替物"
                    "(结构化 HTML 验证,不冒充视觉 QA)"
    )
    parser.add_argument("html", help="产物 HTML 文件")
    parser.add_argument("--manifest", default=None,
                        help="资产声明 JSON 数组(默认:<html 同目录>/.maliang/assets.json 或 assets.json)")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.html):
        print("verify-assets: 文件不存在: %s" % args.html, file=sys.stderr)
        return 2
    manifest_path = args.manifest
    if manifest_path is None:
        for cand in (os.path.join(os.path.dirname(args.html), ".maliang", "assets.json"),
                     os.path.join(os.path.dirname(args.html), "assets.json")):
            if os.path.isfile(cand):
                manifest_path = cand
                break
    if manifest_path is None or not os.path.isfile(manifest_path):
        print("verify-assets: 找不到资产 manifest(--manifest 或 <html 同目录>/assets.json)——"
              "没有声明就没有对照物,UNMEASURED", file=sys.stderr)
        return 2
    try:
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print("verify-assets: manifest 不可读: %s" % exc, file=sys.stderr)
        return 2
    if not isinstance(manifest, list):
        print("verify-assets: manifest 必须是 JSON 数组", file=sys.stderr)
        return 2

    with open(args.html, encoding="utf-8", errors="replace") as fh:
        html = fh.read()
    findings, warnings, summary = verify_assets(html, manifest, args.html)

    for f in findings:
        print("%s [%s] %s" % (f["file"], f["slot"], f["message"]))
    for w in warnings:
        print("%s [数量对账·告警档] %s" % (os.path.basename(args.html), w))
    print("资产位枚举 %d,声明 %d;发现 %d 处(顶替物/缺席)%s" % (
        summary["enum_slots"], summary["manifest_slots"], len(findings),
        ";告警 %d 处" % len(warnings) if warnings else ""))
    if findings:
        print("诚实声明:结构验证失败 ≠ 视觉 QA 通过;修复后复查,仍失败如实上报,不许宣称完成。")
        return 1
    return 0


# ============================================================
# 来源节: measure-colors.py (子命令: measure-colors)

# ---- 原 measure-colors.py 模块说明 ----
"""确定性测色脚本(G23):图片 -> k-means -> ΔE 合并 -> 角色分配 -> stdout JSON。

目测取色会向熟悉的调色板默认漂移(漂移可达 ΔE10+),测量的意义是把
「这些颜色是什么」变成可复核的数字。管线:

  1. 解码图片为 RGB 像素;
  2. 分层哈希采样 ≤160k 像素(deterministic_stratified:等分象限 + 固定哈希
     取样点,避免固定相位对周期性细节的混叠删除);
  3. k-means(k 个簇,最远点初始化:小而独立的色块也能分到自己的簇);
  4. CIE ΔE 合并近似簇(PNG ΔE≤2.5 / JPEG 压缩噪声更宽 ΔE≤5);
  5. 角色启发式:最大覆盖=background;与背景明度差 ≥0.25 且覆盖 ≥0.5% 中
     明度差最大者=text;accent 按 饱和度×ΔE×√(min(覆盖,2%)/2%) 打分取最高
     (饱和度 ≥0.25、覆盖 ≥0.2%、明度 0.08-0.92 内)。

格式支持与降级(未测量不得记为通过):
  PNG  纯 Python 标准库解码(8-bit,非隔行,灰度/RGB/RGBA/调色板);
  JPEG 需 Pillow;Pillow 缺失时该文件报 UNMEASURED → 退出码 2(--help 同步注明);
  其余格式(WebP/GIF...)或不受支持的 PNG 变体 → UNMEASURED → 2。

用法:
    python3 scripts/measure-colors.py <image.png> [--k 8] [--json|--text]

输出(stdout,默认 JSON):
    {"source": {file, width, height},
     "measurement": {k, sampling:{method, max_pixels, sampled_pixels}},
     "palette": [{hex, coverage, role}...], "measured": true}

退出码: 见 scripts/EXIT-CODES.md(0=测到了 / 1=不使用 / 2=没能检查/UNMEASURED;#16)。
依赖: Python 3 标准库;JPEG 可选 Pillow。
"""
# ---- 模块说明结束 ----
import argparse
import json
import math
import os
import struct
import sys
import zlib

MAX_SAMPLED_PIXELS = 160_000
KMEANS_ITERS = 24
DEFAULT_K = 8

# 角色启发式阈值(外部原口径)
TEXT_MIN_L_DIFF = 0.25
TEXT_MIN_COVERAGE = 0.005
ACCENT_MIN_SAT = 0.25
ACCENT_MIN_COVERAGE = 0.002
ACCENT_L_RANGE = (0.08, 0.92)
ACCENT_COVERAGE_CAP = 0.02

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


# ---------------------------------------------------------------------------
# PNG 解码(纯标准库):8-bit,非隔行,色型 0/2/3/6
# ---------------------------------------------------------------------------

def decode_png(data):
    """解码 PNG 为 (width, height, [(r,g,b)...]);不支持返回 (_UNSUPPORTED, 原因)。"""
    if not data.startswith(_PNG_SIGNATURE):
        return None, "不是 PNG 文件"
    pos = 8
    width = height = None
    color_type = bit_depth = interlace = None
    palette = []
    idat = bytearray()
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        pos += 8
        chunk = data[pos:pos + length]
        if len(chunk) != length:
            return None, "PNG chunk 截断(损坏的文件)"
        pos += length + 4  # 跳过 CRC
        if ctype == b"IHDR":
            try:
                width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                    ">IIBBBBB", chunk
                )
            except struct.error:
                return None, "PNG 结构损坏(IHDR)"
        elif ctype == b"PLTE":
            if len(chunk) % 3 != 0:
                return None, "PLTE 长度非 3 的倍数(损坏的文件)"
            palette = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        elif ctype == b"IDAT":
            idat.extend(chunk)
        elif ctype == b"IEND":
            break
    if width is None:
        return None, "PNG 缺 IHDR"
    if bit_depth != 8:
        return None, "bit depth %d 不支持(仅 8-bit)" % bit_depth
    if interlace != 0:
        return None, "隔行 PNG 不支持"
    channels = {0: 1, 2: 3, 3: 1, 6: 4}.get(color_type)
    if channels is None:
        return None, "色型 %d 不支持(仅 0/2/3/6)" % color_type
    if color_type == 3 and not palette:
        return None, "调色板 PNG 缺 PLTE"

    # 解压炸弹防线:像素总量硬上限,解压输出限长(超出即拒,UNMEASURED/exit 2)
    if width * height > 80_000_000:
        return None, "图像尺寸超限(width*height > 80M 像素)"

    stride = width * channels
    expected = (stride + 1) * height
    try:
        d = zlib.decompressobj()
        raw = d.decompress(bytes(idat), expected + 1_048_576)
    except zlib.error as exc:
        return None, "IDAT 解压失败: %s" % exc
    if len(raw) < expected:
        return None, "像素数据不足(损坏的 PNG)"
    if d.unconsumed_tail:
        return None, "解压输出超过预期上限(疑似解压炸弹)"

    # 逐行 unfilter(五种滤波,见 PNG 规范)
    bpp = channels
    out = bytearray()
    prev = bytearray(stride)
    ptr = 0
    for _ in range(height):
        ftype = raw[ptr]
        ptr += 1
        line = bytearray(raw[ptr:ptr + stride])
        ptr += stride
        if ftype == 1:  # Sub
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ftype == 2:  # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:  # Average
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:  # Paeth
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        elif ftype != 0:
            return None, "未知滤波类型 %d" % ftype
        out.extend(line)
        prev = line

    # 折叠到 RGB
    pixels = []
    if color_type == 2:
        for i in range(0, len(out), 3):
            pixels.append((out[i], out[i + 1], out[i + 2]))
    elif color_type == 6:
        for i in range(0, len(out), 4):
            # alpha 合成到白底(外部 sharp flatten 同口径)
            a = out[i + 3] / 255
            pixels.append(tuple(
                round(out[i + k] * a + 255 * (1 - a)) for k in range(3)
            ))
    elif color_type == 0:
        for v in out:
            pixels.append((v, v, v))
    else:  # 调色板
        for idx in out:
            if idx >= len(palette):
                return None, "调色板索引越界"
            pixels.append(palette[idx])
    return (width, height, pixels), None


def decode_jpeg(data):
    """JPEG 走 Pillow;缺失时返回 UNMEASURED(调用方退出 2)。"""
    try:
        import io
        from PIL import Image  # type: ignore
    except ImportError:
        return None, "JPEG 需要 Pillow(未安装);PNG 全程标准库。UNMEASURED"
    try:
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGB")
    except Exception as exc:
        return None, "JPEG 解码失败: %s" % exc
    # tobytes() 取原始 RGB 字节(每像素 3 字节,行优先);不用 getdata()——
    # 它在 Pillow 14 将被移除,老版本又没有替代 API,跨版本只此一路稳。
    raw = img.tobytes()
    pixels = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
    return (img.width, img.height, pixels), None


def load_image(path):
    """按扩展名解码;返回 (width, height, pixels, is_jpeg) 或抛 UnmeasurableError。"""
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        raise UnmeasurableError("读取失败: %s" % exc)
    is_jpeg = ext in (".jpg", ".jpeg")
    if is_jpeg:
        size, err = decode_jpeg(data)
    elif ext == ".png":
        size, err = decode_png(data)
    else:
        size, err = None, "不支持的格式 %s(仅 PNG;JPEG 需 Pillow)" % ext
    if err:
        raise UnmeasurableError(err)
    return size[0], size[1], size[2], is_jpeg


class UnmeasurableError(Exception):
    """没能检查(UNMEASURED):格式不支持/解码失败/依赖缺失。"""


# ---------------------------------------------------------------------------
# 采样 / k-means / ΔE 合并 / 角色分配(改写自外部 measure-colors.mjs)
# ---------------------------------------------------------------------------

def _mix32(value):
    x = (value + 0x9E3779B9) & 0xFFFFFFFF
    x = ((x ^ (x >> 16)) * 0x21F0AAAD) & 0xFFFFFFFF
    x = ((x ^ (x >> 15)) * 0x735A2D97) & 0xFFFFFFFF
    return (x ^ (x >> 15)) & 0xFFFFFFFF


def stratified_sample(pixels, sample_count):
    """分层哈希采样:等分象限 + 固定哈希取样点,破除固定相位混叠。"""
    total = len(pixels)
    if total <= sample_count:
        return list(pixels)
    out = []
    for s in range(sample_count):
        start = (s * total) // sample_count
        end = ((s + 1) * total) // sample_count
        idx = start + (_mix32(s) % max(1, end - start))
        out.append(pixels[idx])
    return out


def kmeans(pixels, k, iters=KMEANS_ITERS):
    """最远点初始化的 k-means;返回 [{center, share}](按覆盖降序)。"""
    # 最远点初始化:从最暗像素起步,反复加入离现有中心最远的像素
    centers = [list(min(pixels, key=lambda p: p[0] * 3 + p[1] * 6 + p[2]))]
    nearest = [float("inf")] * len(pixels)
    while len(centers) < k:
        last = centers[-1]
        far, fd = 0, -1.0
        for i, p in enumerate(pixels):
            d = (p[0] - last[0]) ** 2 + (p[1] - last[1]) ** 2 + (p[2] - last[2]) ** 2
            if d < nearest[i]:
                nearest[i] = d
            if nearest[i] > fd:
                fd, far = nearest[i], i
        if fd <= 0:
            break  # 不同色少于 k
        centers.append(list(pixels[far]))
    k = len(centers)
    assign = [0] * len(pixels)
    for _ in range(iters):
        moved = False
        for i, p in enumerate(pixels):
            best, bd = 0, float("inf")
            for c in range(k):
                ctr = centers[c]
                d = (p[0] - ctr[0]) ** 2 + (p[1] - ctr[1]) ** 2 + (p[2] - ctr[2]) ** 2
                if d < bd:
                    bd, best = d, c
            if assign[i] != best:
                assign[i] = best
                moved = True
        sums = [[0, 0, 0, 0] for _ in range(k)]
        for i, a in enumerate(assign):
            s = sums[a]
            s[0] += pixels[i][0]
            s[1] += pixels[i][1]
            s[2] += pixels[i][2]
            s[3] += 1
        for c in range(k):
            if sums[c][3] > 0:
                centers[c] = [sums[c][j] / sums[c][3] for j in range(3)]
        if not moved:
            break
    counts = [0] * k
    for a in assign:
        counts[a] += 1
    clusters = [
        {"center": centers[c], "share": counts[c] / len(pixels)}
        for c in range(k) if counts[c] > 0
    ]
    clusters.sort(key=lambda c: -c["share"])
    return clusters


def srgb_to_lab(rgb):
    import maliang_common

    def f(v):
        return maliang_common.srgb_to_linear(v / 255)
    r, g, b = f(rgb[0]), f(rgb[1]), f(rgb[2])
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

    def t(v):
        return v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116

    x, y, z = t(x), t(y), t(z)
    return [116 * y - 16, 500 * (x - y), 200 * (y - z)]


def delta_e(a, b):
    """CIE76 ΔE(外部 color-math.mjs 同口径)。"""
    la, lb = srgb_to_lab(a), srgb_to_lab(b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(la, lb)))


def merge_similar(clusters, max_de):
    """合并感知等价的簇(抗锯齿/JPEG 噪声);按覆盖降序。"""
    merged = []
    for c in clusters:
        near = None
        for m in merged:
            if delta_e(m["center"], c["center"]) <= max_de:
                near = m
                break
        if near is not None:
            total = near["share"] + c["share"]
            near["center"] = [
                (near["center"][i] * near["share"] + c["center"][i] * c["share"]) / total
                for i in range(3)
            ]
            near["share"] = total
        else:
            merged.append({"center": list(c["center"]), "share": c["share"]})
    merged.sort(key=lambda c: -c["share"])
    return merged


def hsv(rgb):
    """(色相°, HSV 饱和度, HSL 明度)。accent 判定用 HSV 饱和度(近白不爆表)。"""
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    s = 0 if mx == 0 else d / mx
    l = (mx + mn) / 2
    h = 0.0
    if d != 0:
        if mx == r:
            h = 60 * (((g - b) / d) % 6)
        elif mx == g:
            h = 60 * ((b - r) / d + 2)
        else:
            h = 60 * ((r - g) / d + 4)
    return (h + 360) % 360, s, l


def assign_roles(clusters):
    """角色启发式:background / text / accent,其余 unassigned。"""
    entries = []
    for c in clusters:
        h, s, l = hsv(c["center"])
        entries.append({"center": c["center"], "share": c["share"],
                        "h": h, "s": s, "l": l, "role": "unassigned"})
    if not entries:
        return entries
    taken = set()
    # 背景 = 最大覆盖
    entries[0]["role"] = "background"
    taken.add(0)
    bg_l = entries[0]["l"]
    # 文本 = 与背景明度差最大且覆盖达标者
    text_i, best_c = -1, 0.0
    for i, e in enumerate(entries):
        if i in taken:
            continue
        c = abs(e["l"] - bg_l)
        if e["share"] >= TEXT_MIN_COVERAGE and c > best_c:
            best_c, text_i = c, i
    if text_i >= 0 and best_c > TEXT_MIN_L_DIFF:
        entries[text_i]["role"] = "text"
        taken.add(text_i)
    # accent = 饱和度 × ΔE(对背景) × 覆盖折扣打分;覆盖到 2% 后不再加分——
    # 大面积浅色表面不得压过小而亮的 CTA
    accents = []
    for i, e in enumerate(entries):
        if i in taken:
            continue
        if not (e["s"] >= ACCENT_MIN_SAT and e["share"] >= ACCENT_MIN_COVERAGE
                and ACCENT_L_RANGE[0] <= e["l"] <= ACCENT_L_RANGE[1]):
            continue
        score = (e["s"] * delta_e(e["center"], entries[0]["center"])
                 * math.sqrt(min(e["share"], ACCENT_COVERAGE_CAP) / ACCENT_COVERAGE_CAP))
        accents.append((score, i))
    if accents:
        accents.sort(key=lambda p: -p[0])
        entries[accents[0][1]]["role"] = "accent"
        taken.add(accents[0][1])
    return entries


def measure_image(path, k=DEFAULT_K):
    """测量单图,返回输出 JSON dict。UNMEASURED 抛 UnmeasurableError。"""
    width, height, pixels, is_jpeg = load_image(path)
    if width <= 0 or height <= 0 or not pixels:
        raise UnmeasurableError("图像为空")
    k = max(2, min(16, int(k)))
    sampled = stratified_sample(pixels, MAX_SAMPLED_PIXELS)
    # JPEG 压缩把平坦色摊成更宽的噪声带,合并阈值放档(外部同口径)
    clusters = merge_similar(kmeans(sampled, k), 5.0 if is_jpeg else 2.5)
    palette = [
        {"hex": "#%02x%02x%02x" % tuple(round(v) for v in e["center"]),
         "coverage": round(e["share"], 4), "role": e["role"]}
        for e in assign_roles(clusters)
    ]
    return {
        "source": {"file": os.path.basename(path), "width": width, "height": height},
        "measurement": {
            "k": k,
            "sampling": {
                "method": "deterministic_stratified",
                "max_pixels": MAX_SAMPLED_PIXELS,
                "sampled_pixels": len(sampled),
            },
        },
        "palette": palette,
        "measured": True,
    }


def _main_measure_colors(argv=None):
    parser = argparse.ArgumentParser(
        description="确定性测色(PNG 纯标准库;JPEG 需 Pillow,缺失报 UNMEASURED/exit 2)"
    )
    parser.add_argument("image", help="待测图片(.png;.jpg/.jpeg 需 Pillow)")
    parser.add_argument("--k", type=int, default=DEFAULT_K, help="簇数 2-16(默认 8;verify 复测必须同 k)")
    parser.add_argument("--json", action="store_true", default=True,
                        help="输出 JSON(默认即为 JSON;保留开关与外部 CLI 兼容)")
    parser.add_argument("--text", dest="json", action="store_false", help="输出人类可读汇总")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.image):
        print("measure-colors: 文件不存在: %s" % args.image, file=sys.stderr)
        return 2
    try:
        result = measure_image(args.image, args.k)
    except UnmeasurableError as exc:
        print(json.dumps({"source": {"file": os.path.basename(args.image)},
                          "measured": False, "unmeasured_reason": str(exc)},
                         ensure_ascii=False))
        print("measure-colors: UNMEASURED —— %s" % exc, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("%s (%dx%d, k=%d, 采样 %d 像素)" % (
            result["source"]["file"], result["source"]["width"],
            result["source"]["height"], result["measurement"]["k"],
            result["measurement"]["sampling"]["sampled_pixels"]))
        for p in result["palette"]:
            print("  %-11s #%s  覆盖 %5.1f%%  角色 %s" % (
                p["hex"], p["hex"], p["coverage"] * 100, p["role"]))
    return 0


# ============================================================
# 来源节: palette-solver.py (子命令: palette-solver)

# ---- 原 palette-solver.py 模块说明 ----
"""OKLCH 亮度域配色求解器 + 全配对矩阵契约(G33 脚本层;按裁决 6 不含 MOODS)。

给定背景色与色相/彩度,在 OKLCH 亮度域求解三档可用前景色:
  text       对比度 ≥4.5(正文/链接/按钮标签)
  ui         对比度 ≥3.0(大字号/图标/传达状态的描边,WCAG 1.4.11)
  decorative 对比度 <3.0(纯装饰:发丝线/底纹;不得是传达状态的唯一手段)

  求解即安全:对每个目标档在 L=0.02..0.99 扫描,text/ui 取「达标且最接近
偏好亮度」的候选,decorative 取「恰低于 3.0 且亮度最贴近背景」的近底微差色
(发丝线/底纹的真实用法);chroma 不可达时按 0.85 逐步降(Adobe Leonardo 同
思路:亮度对比度目标求解)。外部原文的 MOODS 关键词查表**砍掉不扩充**——它
与 ai-tells §8 正面相抵,且查表本身就是新的同质化源(裁决 6)。

输出:三档角色色 + 全配对矩阵(每一对按其清的档分类)+「Legal pairings
(record these in the style lock)」清单。design-md Phase 0d 的颜色契约:
模型只能组合矩阵内配对;调色板扩充必须重跑矩阵。

(:83-111 矩阵分类)(#33)MOODS 按裁决 6 砍除。

退出码: 见 scripts/EXIT-CODES.md(0=求解成功 / 1=有档位无解 / 2=没能检查;#16)。
依赖: Python 3 标准库。
"""
# ---- 模块说明结束 ----
import argparse
import json
import math
import sys

AA_NORMAL = 4.5        # 正文文本档
AA_LARGE_OR_UI = 3.0   # UI 组件/大字号档

SOLVE_L_STEP = 0.01    # 亮度扫描步长(0.02..0.99)
CHROMA_DECAY = 0.85    # chroma 降档系数(外部原口径)
CHROMA_MAX_TRIES = 8
GAMUT_MAX_TRIES = 40


# ---------- sRGB <-> OKLab <-> OKLCH(改写自外部 generate_palette.py) ----------

from maliang_common import srgb_to_linear as _srgb_to_linear  # 全库唯一 WCAG/线性化实现


def _linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def _linear_rgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_ = l ** (1 / 3) if l > 0 else 0.0
    m_ = m ** (1 / 3) if m > 0 else 0.0
    s_ = s ** (1 / 3) if s > 0 else 0.0
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _oklab_to_linear_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_hex(L, C, H):
    """OKLCH -> hex;gamut 外按 0.92 降 chroma 至可显示(外部原口径)。"""
    hr = math.radians(H)
    c = C
    lr, lg, lb = 0.0, 0.0, 0.0
    for _ in range(GAMUT_MAX_TRIES):
        a, b = c * math.cos(hr), c * math.sin(hr)
        lr, lg, lb = _oklab_to_linear_rgb(L, a, b)
        if all(-1e-4 <= v <= 1 + 1e-4 for v in (lr, lg, lb)):
            break
        c *= 0.92
    lr, lg, lb = (min(1.0, max(0.0, v)) for v in (lr, lg, lb))
    r, g, b = (round(_linear_to_srgb(v) * 255) for v in (lr, lg, lb))
    return "%02x%02x%02x" % (r, g, b)


# ---------- WCAG 对比度(改写自外部 check_contrast.py) ----------

def _linearize(c):
    return _srgb_to_linear(c / 255)


def luminance(hex_color):
    import maliang_common
    return maliang_common.relative_luminance(
        tuple(v / 255.0 for v in maliang_common.hex_to_rgb255(hex_color)))


def contrast_ratio_hex_pair(hex1, hex2):
    import maliang_common
    return maliang_common.contrast_ratio_hex(hex1, hex2)


def classify(ratio):
    if ratio >= AA_NORMAL:
        return "text-safe (>=4.5)"
    if ratio >= AA_LARGE_OR_UI:
        return "UI-safe (>=3.0)"
    return "decorative (<3.0)"


# ---------- 亮度域求解 ----------

def oklch_L_of_hex(hex_color):
    """反查一个 hex 的 OKLCH 亮度(决定偏好方向:暗底求亮前景,反之求暗)。"""
    h = hex_color.lstrip("#")
    r, g, b = (_srgb_to_linear(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    return _linear_rgb_to_oklab(r, g, b)[0]


def solve_foreground(bg_hex, hue, chroma, floor, mode, prefer_l=None, objective="prefer"):
    """求对比度 ≥floor 的前景色;chroma 不可达按 0.85 逐步降。

    objective="prefer":对比度达标者里亮度最贴近 prefer_l(正文档,text)。
    objective="floor":达标者里对比度最贴近地板(UI 档,ui——贴着 3.0 的
    临界色,与 text 天然分离)。
    mode="at-most" 求装饰档:对比度 <3.0 且亮度最贴近背景(近底微差色,
    发丝线/底纹的真实用法;同时避免与 UI 档在同一边界撞色)。
    """
    bg_l = oklch_L_of_hex(bg_hex)
    if prefer_l is None:
        prefer_l = 0.85 if bg_l < 0.5 else 0.25

    def better(candidate, incumbent):
        if mode == "at-most":
            return abs(candidate[0] - bg_l) < abs(incumbent[0] - bg_l)
        if objective == "floor":
            return abs(candidate[2] - floor) < abs(incumbent[2] - floor)
        return abs(candidate[0] - prefer_l) < abs(incumbent[0] - prefer_l)

    c = chroma
    for _ in range(CHROMA_MAX_TRIES):
        best = None
        L = 0.02
        while L <= 0.99:
            hx = oklch_to_hex(L, c, hue)
            ratio = contrast_ratio_hex_pair(hx, bg_hex)
            ok = ratio < AA_LARGE_OR_UI if mode == "at-most" else ratio >= floor
            if ok and (best is None or better((L, hx, ratio), best)):
                best = (L, hx, ratio)
            L += SOLVE_L_STEP
        if best:
            return best
        c *= CHROMA_DECAY
    return None


def solve_palette(bg_hex, hue, chroma):
    """三档求解;无解的档位记入 missing(显性化,不静默降级)。"""
    roles = {"bg": bg_hex.lstrip("#").lower()}
    missing = []
    for role, floor, mode, objective in (
        ("text", AA_NORMAL, "at-least", "prefer"),
        ("ui", AA_LARGE_OR_UI, "at-least", "floor"),
        ("decorative", None, "at-most", None),
    ):
        got = solve_foreground(roles["bg"], hue, chroma, floor, mode, objective=objective)
        if got is None:
            missing.append(role)
        else:
            roles[role] = got[1]
    return roles, missing


def pairing_matrix(roles):
    """全配对矩阵:每对给对比度与档位分类,按对比度降序。"""
    names = [n for n in roles if roles[n]]
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = contrast_ratio_hex_pair(roles[a], roles[b])
            pairs.append((a, b, r, classify(r)))
    pairs.sort(key=lambda p: -p[2])
    return pairs


def format_report(roles, pairs, missing, hue, chroma):
    lines = []
    lines.append("# 求解配色 — bg=%s hue=%.1f chroma=%.3f" % (roles["bg"], hue, chroma))
    if missing:
        lines.append("!! 无解档位: %s(色相/彩度组合在该档无解;换 hue 或降 chroma)" % ", ".join(missing))
    for role in ("text", "ui", "decorative"):
        if roles.get(role):
            lines.append("  %-11s #%s" % (role, roles[role]))
    lines.append("")
    lines.append("== Contrast matrix (%d pairs) ==" % len(pairs))
    for a, b, r, cls in pairs:
        lines.append("  %-11s x %-11s %6.2f  %s" % (a, b, r, cls))
    lines.append("")
    lines.append("== Legal pairings (record these in the style lock) ==")
    text_safe = ", ".join("%s/%s" % (a, b) for a, b, r, c in pairs if r >= AA_NORMAL) or "none"
    ui_safe = ", ".join("%s/%s" % (a, b) for a, b, r, c in pairs if AA_LARGE_OR_UI <= r < AA_NORMAL) or "none"
    deco = ", ".join("%s/%s" % (a, b) for a, b, r, c in pairs if r < AA_LARGE_OR_UI) or "none"
    lines.append("  Text-safe   (>=4.5): %s" % text_safe)
    lines.append("  UI-safe     (>=3.0 and <4.5): %s" % ui_safe)
    lines.append("  Decorative  (<3.0;不得是传达状态的唯一手段): %s" % deco)
    return "\n".join(lines)


def _main_palette_solver(argv=None):
    parser = argparse.ArgumentParser(
        description="OKLCH 亮度域配色求解 + 全配对矩阵(text≥4.5/UI≥3.0/decorative<3.0;无 MOODS)"
    )
    parser.add_argument("--bg", required=True, help="背景色 6 位 hex,如 0b0d12")
    parser.add_argument("--hue", type=float, required=True, help="前景色相(度,0-360)")
    parser.add_argument("--chroma", type=float, default=0.12, help="起始彩度(默认 0.12;无解时自动 0.85 降档)")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON(默认人类可读报告)")
    args = parser.parse_args(argv)

    bg = args.bg.lstrip("#").lower()
    if len(bg) != 6:
        print("palette-solver: --bg 必须是 6 位 hex,得到 %r" % args.bg, file=sys.stderr)
        return 2
    if not (0.0 <= args.hue <= 360.0) or not (0.0 <= args.chroma <= 0.4):
        print("palette-solver: --hue 须在 [0,360]、--chroma 须在 [0,0.4]", file=sys.stderr)
        return 2

    roles, missing = solve_palette(bg, args.hue, args.chroma)
    pairs = pairing_matrix(roles)

    if args.json:
        print(json.dumps({
            "bg": roles["bg"], "hue": args.hue, "chroma": args.chroma,
            "roles": {k: v for k, v in roles.items() if v},
            "missing_roles": missing,
            "matrix": [{"a": a, "b": b, "ratio": round(r, 2), "class": c} for a, b, r, c in pairs],
            "legal_pairings": {
                "text": ["%s/%s" % (a, b) for a, b, r, _ in pairs if r >= AA_NORMAL],
                "ui": ["%s/%s" % (a, b) for a, b, r, _ in pairs if AA_LARGE_OR_UI <= r < AA_NORMAL],
                "decorative": ["%s/%s" % (a, b) for a, b, r, _ in pairs if r < AA_LARGE_OR_UI],
            },
        }, ensure_ascii=False, indent=2))
    else:
        print(format_report(roles, pairs, missing, args.hue, args.chroma))

    # 有档位无解 = 看了有问题(显性化,不静默给一半结果)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
