#!/usr/bin/env python3
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
来源:ux-ui-agent-skills scripts/verify_interactive.mjs(三信号与豁免口径),
      2026-10 吸收。
"""

import argparse
import importlib.util
import json
import os
import sys
import time

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)


def _load_verify_states():
    """按文件名加载带连字符的 verify-states.py,复用其 CDP 机制。"""
    path = os.path.join(_DIR, "verify-states.py")
    spec = importlib.util.spec_from_file_location("maliang_verify_states", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vs = _load_verify_states()

EXIT_OK = vs.EXIT_OK
EXIT_FINDINGS = vs.EXIT_FINDINGS
EXIT_UNMEASURED = vs.EXIT_UNMEASURED

STATE_ATTRS = ["aria-pressed", "aria-expanded", "aria-checked", "aria-selected", "aria-sort"]
STATE_ROLES = ["switch", "tab", "menuitemcheckbox", "menuitemradio", "option"]

CLICKABLE = (
    'button,[role="button"],input[type="checkbox"],input[type="radio"],'
    '[role="switch"],[role="tab"],[role="option"],[role="menuitemcheckbox"],'
    '[role="menuitemradio"],summary'
)

# 候选采集:可见、未禁用、无 data-demo-state 豁免、排除表单提交/文件控件。
COLLECT_JS = r"""
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
                timeout_ms=vs.TIMEOUT_DEFAULT_MS, advisory=False):
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
            " document.head && document.head.appendChild(s); return true; })()" % json.dumps(vs.FREEZE_CSS),
            timeout=_remaining())
        session.evaluate_fn(WATCH_JS, timeout=_remaining())
        return True

    if not _fresh_load():
        result["status"] = "unmeasured"
        result["reason"] = "页面加载失败"
        return result

    candidates, err = session.evaluate_fn(
        COLLECT_JS, {"attrs": STATE_ATTRS, "roles": STATE_ROLES, "clickable": CLICKABLE},
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
        except vs.CDPError as exc:
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


def main(argv=None):
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
    parser.add_argument("--viewport", type=vs.parse_viewport, default=(1280, 900),
                        help="视口,形如 1280x900(默认 1280x900)")
    parser.add_argument("--timeout", type=int, default=vs.TIMEOUT_DEFAULT_MS,
                        help="单文件预算毫秒(默认 %d)" % vs.TIMEOUT_DEFAULT_MS)
    args = parser.parse_args(argv)

    target = os.path.abspath(args.target)
    files = vs.collect_html_files(target)

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

    binary = vs.find_browser(args.browser)
    if not binary:
        return _unmeasured(
            "没找到浏览器(尝试过 --browser / MALIANG_BROWSER / PATH 里的 "
            + "/".join(vs.BROWSER_CANDIDATES) + ");交互真实性必须在真浏览器里点击测量")

    proc = profile_dir = session = None
    results = []
    try:
        try:
            proc, profile_dir, port = vs.launch_browser(binary)
        except vs.CDPError as exc:
            return _unmeasured(str(exc))
        try:
            session = vs.connect_session(port)
            session.call("Page.enable", timeout=10.0)
            session.call("Runtime.enable", timeout=10.0)
        except (vs.CDPError, OSError, ValueError) as exc:
            return _unmeasured("DevTools 协议连接失败: %s" % exc)

        for path in files:
            try:
                results.append(verify_file(
                    session, path, dark=args.dark, viewport=args.viewport,
                    timeout_ms=args.timeout, advisory=args.advisory))
            except vs.CDPError as exc:
                results.append({"file": path, "status": "unmeasured", "reason": str(exc),
                                "candidates": 0, "checked": 0, "dead": [], "invisible": [],
                                "inert": [], "skipped": []})
    finally:
        if session:
            session.close()
        vs.stop_browser(proc, profile_dir)

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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
