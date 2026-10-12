#!/usr/bin/env python3
"""build-explorer —— 风格对比页生成器（manifest → 离线自包含 HTML）。

把 manifest 里列出的候选页面组装成一张可以离线打开的对比页：候选并排或单张
查看、按实际尺寸（100%）判读、选定后复制一句选择回传。对比页**不写回任何
文件**、不自动选择、不显示推荐态——选择永远由用户做出。

manifest.json（与候选文件同目录；最少字段见 --help）:
    {"schemaVersion": 1, "project": "...", "brief": "...", "round": "01",
     "candidates": [{"id": "a", "name": "...", "concept": "...",
       "typography": "...", "palette": ["#112233"], "traits": ["..."],
       "source": "a.html"}]}

情形表（来源: oil-ui references/style-explorer.md + scripts/build_explorer.py,
2026-10 吸收; 缩尺样机层明确不吸收——与 explore.md 禁缩略图九宫格矛盾）:
  - nativeViewport  固定画布：顶层或候选里写 "1920x1080" / {"width":..,"height":..}，
                    对比页按原生视口渲染，候选不用自己写缩放；
  - interactive     自己写的可操作小样（单个 HTML、脚本内联、无网络）；
  - kind="url"      项目里要运行起来才能看的页面：只认 localhost/127.0.0.1/::1
                    的本机开发服务器，顶层 serve 写启动方式；
  - kind="image"    只有截图（PNG/JPEG/WebP）；
  - baseline=true   现状候选，排第一位并标「现状」，每轮最多一个。

安全边界：候选在 sandbox iframe 内渲染，注入候选的 CSP 默认 `script-src 'none'`
（interactive 才放开 inline script），图片/字体/视频以 data: 内嵌，不引用网络资源；
对比页自身的 CSP `connect-src 'none'`（有本机地址候选时才放开到那些 origin）。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
  0 = 已生成（stdout 一行 JSON: output/candidates/fingerprint/bytes）
  1 = 未生成（manifest 全部问题一次列出 / 输出已存在且无 --force）
  2 = 用法错误
依赖: Python 3 标准库(无第三方依赖)；需要 Python 3.9+。
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import urlsplit

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VIEWPORTS = {"desktop": [1280, 900], "mobile": [390, 844]}
DATA_MARKER = "/*__MALIANG_EXPLORER_DATA__*/ null"
CONNECT_MARKER = "connect-src 'none'"
HEX_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\Z")
ID_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")
LOOPBACK = {"localhost", "127.0.0.1", "::1"}

CANDIDATE_CSP = (
    "default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src data:; "
    "media-src data:; script-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'"
)
EMBEDDABLE = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
    ".gif": "image/gif", ".avif": "image/avif", ".svg": "image/svg+xml",
    ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf",
    ".mp4": "video/mp4", ".webm": "video/webm",
}


class ManifestError(ValueError):
    """把发现的问题一次报全，便于一轮改完。"""

    def __init__(self, problems: list[str]):
        self.problems = problems
        if len(problems) == 1:
            super().__init__(problems[0])
        else:
            joined = "\n".join(f"  {i}. {p}" for i, p in enumerate(problems, 1))
            super().__init__(f"manifest 有 {len(problems)} 处要改：\n{joined}")


# ---------------------------------------------------------------------------
# 候选预处理（内嵌 / CSP / 结构检查）
# ---------------------------------------------------------------------------

ATTR_REF_RE = re.compile(
    r"""(?P<lead>\b(?:src|poster|xlink:href|href)\s*=\s*)(?P<q>["'])(?P<ref>[^"'#][^"']*)(?P=q)""")
CSS_URL_RE = re.compile(r"""url\(\s*(?P<q>["']?)(?P<ref>[^"')\s][^"')]*)(?P=q)\s*\)""", re.I)
LINK_TAG_RE = re.compile(r"<link\b[^>]*>", re.I)
SCRIPT_SRC_RE = re.compile(
    r"""<script\b(?P<attrs>[^>]*?)\bsrc\s*=\s*(?P<q>["'])(?P<ref>[^"']+)(?P=q)(?P<rest>[^>]*)>\s*</script>""",
    re.I)
SCRIPT_BLOCK_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
LINK_ATTR_RE = re.compile(r"""\b(?P<name>rel|href)\s*=\s*(?P<q>["'])(?P<value>[^"']*)(?P=q)""", re.I)

STORAGE_SHIM = (
    "<script>(function(){var mem=function(){var m={};return{get length(){return Object.keys(m).length},"
    "key:function(i){return Object.keys(m)[i]||null},getItem:function(k){return k in m?m[k]:null},"
    "setItem:function(k,v){m[String(k)]=String(v)},removeItem:function(k){delete m[String(k)]},"
    "clear:function(){m={}}}};['localStorage','sessionStorage'].forEach(function(n){try{window[n].length}catch(e){"
    "try{Object.defineProperty(window,n,{value:mem(),configurable:true})}catch(e2){}}})})();</script>"
)


class CandidateCheck(HTMLParser):
    """候选 HTML 结构检查：禁嵌套文档/自动跳转/base，禁止未内嵌资源。"""

    def __init__(self, label: str):
        super().__init__()
        self.label = label
        self.styles: list[str] = []
        self.in_style = False
        self.head_end: int | None = None
        self.problems: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs = dict(attrs)
        if tag == "head" and self.head_end is None:
            self.head_end = self.getpos()[1] + len(self.get_starttag_text())
        if tag in ("iframe", "frame", "object", "embed"):
            self.problems.append(f"{self.label}: 候选不支持嵌套文档（{tag}）；请改用静态内容或截图")
        if tag == "base":
            self.problems.append(f"{self.label}: 候选不应包含 base；资源需要内嵌")
        if tag == "meta" and (attrs.get("http-equiv") or "").lower() == "refresh":
            self.problems.append(f"{self.label}: 候选不应自动跳转（meta refresh）")
        if attrs.get("srcset"):
            self.problems.append(f"{self.label}: 候选请用内嵌 src 代替 srcset")
        if tag == "style":
            self.in_style = True
        if attrs.get("style"):
            self.styles.append(attrs["style"])
        for key in ("src", "poster", "data", "xlink:href", "href"):
            value = attrs.get(key) or ""
            if not value or value.startswith(("#", "data:")):
                continue
            self.problems.append(f"{self.label}: 候选含未内嵌资源 {tag}.{key}: {value}（用相对路径引用并放进 manifest 目录）")

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.styles.append(data)


def local_file(ref: str, base: str, root: str) -> str | None:
    """把相对引用解析为 manifest 目录内的真实文件；网络/绝对引用返回 None。"""
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("//"):
        return None
    target = os.path.realpath(os.path.join(base, ref.split("?")[0].split("#")[0]))
    root_real = os.path.realpath(root)
    if not (target == root_real or target.startswith(root_real + os.sep)):
        raise ValueError(
            f"引用了 manifest 目录以外的文件 {ref}；把文件复制进 manifest 目录或子目录，再更新相对路径")
    return target if os.path.isfile(target) else None


def _data_url(ref: str, base: str, root: str, used: set[str]) -> str | None:
    target = local_file(ref, base, root)
    if target is None:
        return None
    mime = EMBEDDABLE.get(os.path.splitext(target)[1].lower())
    if not mime:
        return None
    used.add(target)
    with open(target, "rb") as f:
        payload = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def embed_local_files(content: str, base: str, root: str, used: set[str]) -> str:
    """内嵌候选引用的本地图片/字体/视频（含 CSS url()）。"""
    def attr(m):
        url = _data_url(m["ref"], base, root, used)
        return m.group(0) if url is None else f'{m["lead"]}{m["q"]}{url}{m["q"]}'

    def css(m):
        url = _data_url(m["ref"], base, root, used)
        return m.group(0) if url is None else f'url("{url}")'

    return CSS_URL_RE.sub(css, ATTR_REF_RE.sub(attr, content))


def inline_local_code(content: str, base: str, root: str, used: set[str], interactive: bool) -> str:
    """内联本地样式表；interactive 候选同时内联本地脚本（脚本与样式都不外链）。"""
    deferred: list[str] = []

    def link(m):
        attrs = {x["name"].lower(): x["value"] for x in LINK_ATTR_RE.finditer(m.group(0))}
        if "stylesheet" not in (attrs.get("rel") or "").lower():
            return m.group(0)
        target = local_file(attrs.get("href", ""), base, root)
        if target is None:
            return m.group(0)
        used.add(target)
        with open(target, "r", encoding="utf-8") as f:
            css = f.read()
        css = embed_local_files(css, os.path.dirname(target), root, used)
        return "<style>" + re.sub(r"(?i)</(style)", lambda m: "<\\/" + m.group(1).lower(), css) + "</style>"

    def script(m):
        target = local_file(m["ref"], base, root)
        if target is None:
            return m.group(0)  # 外部/网络脚本：留给结构检查报「未内嵌资源」
        used.add(target)
        if not interactive:
            return ""  # 静态候选不执行脚本：本地脚本直接移除
        with open(target, "r", encoding="utf-8") as f:
            code = re.sub(r"(?i)</(script)", lambda m: "<\\/" + m.group(1).lower(), f.read())
        attrs = f'{m["attrs"]} {m["rest"]}'
        is_module = re.search(r"""type\s*=\s*["']module["']""", attrs, re.I)
        tag = ('<script type="module">' if is_module else "<script>") + code + "</script>"
        # 内联脚本忽略 defer：把 defer 文件移到 body 末尾以保持原有执行时机
        if re.search(r"\bdefer\b", attrs, re.I) and not is_module:
            deferred.append(tag)
            return ""
        return tag

    content = SCRIPT_SRC_RE.sub(script, LINK_TAG_RE.sub(link, content))
    if deferred:
        close = content.lower().rfind("</body>")
        content = content + "".join(deferred) if close < 0 else content[:close] + "".join(deferred) + content[close:]
    return content


def prepare_html(path: str, root: str, interactive: bool, used: set[str]) -> str:
    """候选 HTML → 自包含内容（内嵌资源 + 注入 CSP；non-interactive 去掉脚本）。"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    label = os.path.basename(path)
    content = inline_local_code(content, os.path.dirname(path), root, used, interactive)
    content = embed_local_files(content, os.path.dirname(path), root, used)
    checker = CandidateCheck(label)
    try:
        checker.feed(content)
    except Exception as exc:  # 解析失败按结构问题处理
        raise ValueError(f"{label}: HTML 解析失败: {exc}")
    if checker.head_end is None:
        raise ValueError(f"{label}: 候选 HTML 需要完整的 head 元素")
    css_problems = check_css(checker.styles, label)
    if checker.problems or css_problems:
        raise ValueError("\n".join(checker.problems + css_problems))
    if not interactive:
        # 静态候选：结构检查过后剥掉全部脚本（CSP script-src 'none' + 不执行）
        content = SCRIPT_BLOCK_RE.sub("", content)
    csp = (CANDIDATE_CSP.replace("script-src 'none'", "script-src 'unsafe-inline'")
           if interactive else CANDIDATE_CSP)
    meta = f'<meta http-equiv="Content-Security-Policy" content="{csp}">'
    head_open = content.find(">", content.lower().find("<head"))
    if head_open < 0:
        raise ValueError(f"{label}: 候选 HTML 需要完整的 head 元素")
    shim = STORAGE_SHIM if interactive else ""
    return content[:head_open + 1] + meta + shim + content[head_open + 1:]


def check_css(snippets: list[str], label: str) -> list[str]:
    """CSS 资源纪律：@import 拒绝；url() 只能是 data:/#（本地文件应已内嵌）。"""
    problems: list[str] = []
    for css in snippets:
        if re.search(r"@import\b", css, re.I):
            problems.append(f"{label}: CSS 含 @import；请内嵌样式，不引用外部样式表")
        for m in CSS_URL_RE.finditer(css):
            ref = m.group("ref").strip()
            if not ref or ref.startswith(("#", "data:")):
                continue
            problems.append(f"{label}: CSS 含未内嵌资源 url({ref})；把文件放进 manifest 目录用相对路径引用")
    return problems


def prepare_image(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        mime = "image/png"
    elif data.startswith(b"\xff\xd8\xff"):
        mime = "image/jpeg"
    elif data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        raise ValueError(f"{os.path.basename(path)}: 图片候选只支持 PNG、JPEG 和 WebP")
    return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")


def local_url(value: str, label: str) -> str:
    """url 候选只指向本机开发服务器（localhost/127.0.0.1/::1）。"""
    try:
        parts = urlsplit(value)
        parts.port  # 提前拒绝非法端口
    except ValueError:
        raise ValueError(f"{label}必须是有效的本机 http(s) 地址，收到的是 {value}") from None
    if (parts.scheme not in ("http", "https") or (parts.hostname or "").lower() not in LOOPBACK
            or parts.username or parts.password):
        raise ValueError(f"{label}只能是本机开发服务器地址（如 http://localhost:5173/orders），收到的是 {value}")
    return value


def native_viewport(value, where: str) -> dict:
    dims = None
    if isinstance(value, str):
        m = re.fullmatch(r"\s*(\d+)\s*[xX×]\s*(\d+)\s*", value)
        if m:
            dims = [int(x) for x in m.groups()]
    elif isinstance(value, dict):
        dims = [value.get("width"), value.get("height")]
    if dims and all(isinstance(n, (int, float)) and not isinstance(n, bool) and n > 0 and n == int(n)
                    for n in dims):
        return {"width": int(dims[0]), "height": int(dims[1])}
    raise ValueError(
        f'{where}nativeViewport 必须是正整数宽高，如 "1920x1080"、"1920×1080" 或 '
        f'{{"width":1920,"height":1080}}；收到的是 {json.dumps(value, ensure_ascii=False)}')


# ---------------------------------------------------------------------------
# manifest 读取（问题一次报全）
# ---------------------------------------------------------------------------

def load_manifest(path: str):
    """返回 (data, inputs)。任何问题都收进 ManifestError.problems，一轮报全。"""
    problems: list[str] = []

    def attempt(fn):
        try:
            return fn()
        except ValueError as exc:
            problems.append(str(exc))
            return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as exc:
        raise ManifestError([f"manifest 不是合法 JSON：第 {exc.lineno} 行第 {exc.colno} 列，{exc.msg}"]) from None
    except OSError as exc:
        raise ManifestError([f"找不到 manifest：{path}（{exc}）。先写好 manifest.json，字段见 --help"]) from None
    if not isinstance(raw, dict):
        raise ManifestError(["manifest 最外层必须是对象（schemaVersion/project/brief/candidates）"])

    if raw.get("schemaVersion") != 1:
        problems.append("schemaVersion 必须为 1")
    data: dict = {"schemaVersion": 1}

    def text_field(obj, name, where, default=None):
        value = obj.get(name, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{where}{name} 必须是非空字符串")
        return value.strip()

    def text_list(obj, name, where):
        values = obj.get(name)
        if not isinstance(values, list) or not values:
            raise ValueError(f"{where}{name} 必须是非空字符串数组")
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(f"{where}{name} 的每项必须是非空字符串")
        return [v.strip() for v in values]

    data["project"] = attempt(lambda: text_field(raw, "project", "manifest."))
    data["brief"] = attempt(lambda: text_field(raw, "brief", "manifest."))
    data["round"] = attempt(lambda: text_field(raw, "round", "manifest.", default="01"))
    manifest_dir = os.path.dirname(os.path.abspath(path))
    inputs = {os.path.abspath(path)}
    root = manifest_dir

    if "serve" in raw:
        serve = raw["serve"]
        if not isinstance(serve, dict):
            problems.append('serve 必须是对象，如 {"command": "pnpm dev", "cwd": "/项目的绝对路径", "url": "http://localhost:3000"}')
        else:
            if not isinstance(serve.get("command"), str) or not serve["command"].strip():
                problems.append("serve.command 必须是非空字符串")
            if "cwd" in serve and not os.path.isabs(str(serve["cwd"])):
                problems.append("serve.cwd 必须是绝对路径")
            if "url" in serve:
                attempt(lambda: local_url(str(serve["url"]), "serve.url "))
            data["serve"] = serve

    viewport = None
    if "nativeViewport" in raw:
        viewport = attempt(lambda: native_viewport(raw["nativeViewport"], "manifest："))

    candidates = raw.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        problems.append("candidates 至少需要一个候选")
        candidates = []
    seen_ids: set[str] = set()
    output: list[dict] = []
    for index, candidate in enumerate(candidates, 1):
        if not isinstance(candidate, dict):
            problems.append(f"第 {index} 个候选必须是对象")
            continue
        before = len(problems)
        ident = candidate.get("id")
        if not isinstance(ident, str) or not ID_RE.match(ident.strip() or ""):
            problems.append(f'第 {index} 个候选 id 无效：只用小写字母、数字、连字符和下划线，如 "a"/"dir-2"')
            ident = None
        else:
            ident = ident.strip()
            if ident in seen_ids:
                problems.append(f'候选 id "{ident}" 重复了，每个候选要用不同的 id')
            seen_ids.add(ident)
        where = f"候选 {ident}：" if ident else f"第 {index} 个候选："
        kind = candidate.get("kind", "html")
        if kind not in ("html", "image", "url"):
            problems.append(f'{where}kind 只能是 "html"、"image" 或 "url"，收到的是 {json.dumps(kind, ensure_ascii=False)}')
            kind = None
        baseline = candidate.get("baseline", False)
        interactive = candidate.get("interactive", False)
        if not isinstance(baseline, bool) or not isinstance(interactive, bool):
            problems.append(f"{where}baseline 和 interactive 必须是 true 或 false")
        elif interactive and kind not in ("html", None):
            problems.append(f"{where}interactive 只用于 html 候选")
        cand_viewport = (attempt(lambda: native_viewport(candidate["nativeViewport"], where))
                         if "nativeViewport" in candidate else viewport)
        source = url = None
        if kind == "url":
            url = attempt(lambda: local_url(text_field(candidate, "url", where), f"{where}url "))
        elif kind:
            name = attempt(lambda: text_field(candidate, "source", where))
            if name:
                source = os.path.realpath(os.path.join(manifest_dir, name))
                if not (source == os.path.realpath(manifest_dir)
                        or source.startswith(os.path.realpath(manifest_dir) + os.sep)):
                    problems.append(f"{where}source 必须在 manifest 所在目录里（收到 {name}）")
                    source = None
                elif not os.path.isfile(source):
                    problems.append(f"{where}找不到 source 文件 {name}（按 manifest 所在目录找）")
                    source = None
                else:
                    inputs.add(source)
        colors = attempt(lambda: text_list(candidate, "palette", where))
        if colors:
            bad = [c for c in colors if not HEX_COLOR_RE.match(c)]
            if bad:
                problems.append(f'{where}palette 要写十六进制颜色（如 "#1a2b3c"）；这几项不是：{"、".join(bad)}')
        texts = {name: attempt(lambda: text_field(candidate, name, where))
                 for name in ("name", "concept", "typography")}
        traits = attempt(lambda: text_list(candidate, "traits", where))
        if len(problems) > before:
            continue
        try:
            if kind == "url":
                content = url
            elif kind == "html":
                content = prepare_html(source, root, interactive, inputs)
            else:
                content = prepare_image(source)
        except ValueError as exc:
            message = str(exc)
            if source and message.startswith(os.path.basename(source) + ": "):
                message = message[len(os.path.basename(source)) + 2:]
            problems.append(f"{where}{os.path.basename(source)} {message}" if source else f"{where}{message}")
            continue
        entry = {
            "id": ident, **texts, "palette": colors, "traits": traits, "kind": kind,
            "content": content, "baseline": baseline, "interactive": interactive,
            "sourceLabel": url if kind == "url" else os.path.basename(source or ""),
        }
        if cand_viewport:
            entry["nativeViewport"] = cand_viewport
        output.append(entry)
    if sum(1 for c in output if c["baseline"]) > 1:
        problems.append("最多只能有一个基线候选（baseline: true，标「现状」）")
    if problems:
        raise ManifestError(problems)
    # 现状候选排第一位：每个方向都对着它读
    output.sort(key=lambda c: not c["baseline"])
    data["candidates"] = output
    canonical = json.dumps(
        {k: v for k, v in data.items() if k in ("project", "brief", "round", "candidates", "serve")},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    data["fingerprint"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]
    return data, inputs


# ---------------------------------------------------------------------------
# 对比页外壳（自包含；不缩放默认视图，「实际尺寸 100%」为判读口径）
# ---------------------------------------------------------------------------

EXPLORER_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; font-src data:; media-src data:; frame-src 'self' about: data:__FRAME_ORIGINS__; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'">
<title>风格对比页 · __PROJECT__</title>
<style>
:root { --ink:#191b21; --muted:#5b6472; --line:#d8dbe1; --bg:#f6f7f9; --card:#fff; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:14px/1.5 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif; }
header { position:sticky; top:0; z-index:10; background:rgba(246,247,249,.96);
  border-bottom:1px solid var(--line); padding:14px 20px; display:flex; gap:18px; flex-wrap:wrap; align-items:center; }
h1 { font-size:16px; margin:0; }
.brief { color:var(--muted); max-width:56ch; }
.toolbar { margin-left:auto; display:flex; gap:8px; flex-wrap:wrap; }
button { font:inherit; padding:6px 12px; border:1px solid var(--line); border-radius:8px;
  background:#fff; color:var(--ink); cursor:pointer; }
button[aria-pressed="true"], button.primary { background:var(--ink); color:#fff; border-color:var(--ink); }
main { padding:20px; display:grid; gap:20px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.card > header { position:static; background:none; border:0; padding:14px 16px; display:block; }
.card h2 { font-size:15px; margin:0 0 6px; }
.badge { display:inline-block; font-size:12px; border:1px solid var(--line); border-radius:999px;
  padding:1px 8px; margin-left:6px; vertical-align:2px; }
.concept { margin:4px 0; }
.meta { color:var(--muted); font-size:13px; }
.swatches { display:inline-flex; gap:4px; margin-left:6px; vertical-align:-2px; }
.swatch { width:14px; height:14px; border-radius:4px; border:1px solid rgba(0,0,0,.12); }
.stage-wrap { border-top:1px solid var(--line); background:#eceef1; overflow:auto; max-height:78vh; }
.stage { transform-origin:0 0; }
.frame { border:0; background:#fff; display:block; margin:0 auto; }
.zoom-note { color:var(--muted); font-size:12px; padding:6px 16px; border-top:1px solid var(--line); }
.serve-note { margin:0 20px; padding:10px 14px; border:1px dashed var(--line); border-radius:10px;
  background:#fff; color:var(--muted); font-size:13px; }
.file-note { font-size:12px; color:var(--muted); }
footer { padding:8px 20px 28px; color:var(--muted); font-size:12px; }
.single .card { display:none; }
.single .card.active { display:block; }
</style>
</head>
<body>
<header>
  <h1>风格对比页 <span class="file-note">__ROUND_LABEL__</span></h1>
  <div class="brief">__BRIEF__</div>
  <div class="toolbar">
    <button id="mode-parallel" aria-pressed="true">并排</button>
    <button id="mode-single" aria-pressed="false">单张</button>
    <button id="vp-desktop" class="primary">桌面 1280×900</button>
    <button id="vp-mobile">手机 390×844</button>
    <button id="prev" hidden>‹ 上一个</button>
    <button id="next" hidden>下一个 ›</button>
    <button id="zoom-toggle">实际尺寸 100%</button>
  </div>
</header>
<div id="serve-note" hidden></div>
<main id="cards"></main>
<footer>
  对比页不写回任何文件、不自动选择、不显示推荐态。选定后点「复制选择」，
  会复制一句「__ROUND_PREFIX__：选 NN 方向名」——粘贴给 Agent 或在对话里直接说出即可。
  判读口径：单张查看的「实际尺寸 100%」；适应窗口的缩小视图只能看块面，不能作为可读性通过。
</footer>
<script>
const DATA = /*__MALIANG_EXPLORER_DATA__*/ null;
const cards = document.getElementById('cards');
let mode = 'parallel';
let singleIndex = 0;
let fit = false;
let preset = 'desktop';

function el(tag, attrs, children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === undefined || v === null) continue;
    if (k === 'text') node.textContent = v; else node.setAttribute(k, v);
  }
  for (const child of children || []) node.appendChild(child);
  return node;
}

function pad2(n) { return String(n).padStart(2, '0'); }

function viewportOf(c) {
  if (c.nativeViewport) return [c.nativeViewport.width, c.nativeViewport.height];
  return DATA.viewports[preset];
}

function render() {
  cards.className = mode === 'single' ? 'single' : '';
  for (const [i, c] of DATA.candidates.entries()) {
    const existing = document.getElementById('card-' + c.id);
    const [w, h] = viewportOf(c);
    if (!existing) {
      const swatches = el('span', {class: 'swatches'}, c.palette.map((hex) =>
        el('span', {class: 'swatch', style: 'background:' + hex, title: hex})));
      const head = el('header', {}, [
        el('h2', {text: pad2(i + 1) + ' ' + c.name + '　'}),
        ...(c.baseline ? [el('span', {class: 'badge', text: '现状'})] : []),
        el('p', {class: 'concept', text: c.concept}),
        el('p', {class: 'meta', text: 'typography: ' + c.typography}),
        el('p', {class: 'meta'}, [
          el('span', {text: 'palette: '}), swatches,
          el('span', {text: '　traits: ' + c.traits.join(' · ') + '　来源: ' + c.sourceLabel +
            (c.interactive ? '　interactive' : '')})]),
        el('p', {}, [el('button', {class: 'primary pick', 'data-id': c.id, text: '复制选择'})]),
      ]);
      const frame = el('iframe', {
        class: 'frame', title: c.name, width: w, height: h,
        sandbox: c.kind === 'url' ? 'allow-scripts allow-same-origin allow-forms'
               : (c.interactive ? 'allow-scripts allow-forms' : ''),
      });
      if (c.kind === 'url') frame.src = c.content; else frame.srcdoc = c.content;
      const stage = el('div', {class: 'stage'}, [frame]);
      const wrap = el('div', {class: 'stage-wrap'}, [stage]);
      const note = el('div', {class: 'zoom-note',
        text: '视口 ' + w + '×' + h + '（' + (c.nativeViewport ? 'nativeViewport' : '对比页预设') +
              '）；判读用「实际尺寸 100%」，缩小视图只能看块面。'});
      cards.appendChild(el('article', {class: 'card', id: 'card-' + c.id}, [head, wrap, note]));
    }
    const card = document.getElementById('card-' + c.id);
    card.classList.toggle('active', i === singleIndex);
    const frame = card.querySelector('.frame');
    if (frame && !c.nativeViewport) { frame.setAttribute('width', w); frame.setAttribute('height', h); }
    const note = card.querySelector('.zoom-note');
    if (note) note.textContent = '视口 ' + w + '×' + h + '（' + (c.nativeViewport ? 'nativeViewport' : '对比页预设') +
      '）；判读用「实际尺寸 100%」，缩小视图只能看块面。';
  }
  document.getElementById('prev').hidden = mode !== 'single';
  document.getElementById('next').hidden = mode !== 'single';
  document.getElementById('zoom-toggle').textContent = fit ? '实际尺寸 100%' : '适应窗口';
  document.getElementById('vp-desktop').className = preset === 'desktop' ? 'primary' : '';
  document.getElementById('vp-mobile').className = preset === 'mobile' ? 'primary' : '';
  document.getElementById('mode-parallel').setAttribute('aria-pressed', String(mode === 'parallel'));
  document.getElementById('mode-single').setAttribute('aria-pressed', String(mode === 'single'));
  applyFit();
}

function applyFit() {
  const wrapWidth = cards.clientWidth || 1200;
  for (const c of DATA.candidates) {
    const stage = document.querySelector('#card-' + c.id + ' .stage');
    const frame = document.querySelector('#card-' + c.id + ' .frame');
    if (!stage || !frame) continue;
    const w = viewportOf(c)[0], h = viewportOf(c)[1];
    const scale = fit && mode === 'single' ? Math.min(1, (wrapWidth - 48) / w) : 1;
    stage.style.width = w + 'px';
    stage.style.transform = scale < 1 ? 'scale(' + scale + ')' : '';
    stage.style.height = scale < 1 ? Math.round(h * scale) + 'px' : '';
  }
}

async function copyText(text) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch (e) { /* file:// 或无权限时走兜底 */ }
  const area = document.createElement('textarea');
  area.value = text; document.body.appendChild(area); area.select();
  let ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  area.remove();
  return ok;
}

document.addEventListener('click', async (event) => {
  const pick = event.target.closest('.pick');
  if (pick) {
    const idx = DATA.candidates.findIndex((c) => c.id === pick.dataset.id);
    const c = DATA.candidates[idx];
    const text = DATA.round + '：选 ' + pad2(idx + 1) + ' ' + c.name;
    const ok = await copyText(text);
    pick.textContent = ok ? '已复制：' + text : '复制失败，请手动复制';
    if (!ok) window.prompt('复制这句回传：', text);
    return;
  }
  if (event.target.id === 'mode-parallel') { mode = 'parallel'; render(); return; }
  if (event.target.id === 'mode-single') { mode = 'single'; render(); return; }
  if (event.target.id === 'vp-desktop') { preset = 'desktop'; render(); return; }
  if (event.target.id === 'vp-mobile') { preset = 'mobile'; render(); return; }
  if (event.target.id === 'zoom-toggle') { fit = !fit; render(); return; }
  if (event.target.id === 'prev') { singleIndex = (singleIndex - 1 + DATA.candidates.length) % DATA.candidates.length; render(); return; }
  if (event.target.id === 'next') { singleIndex = (singleIndex + 1) % DATA.candidates.length; render(); return; }
});

if (DATA.serve) {
  const note = document.getElementById('serve-note');
  note.hidden = false;
  note.className = 'serve-note';
  note.textContent = '本机地址候选需要开发服务器：' + DATA.serve.command +
    (DATA.serve.cwd ? '（cwd: ' + DATA.serve.cwd + '）' : '') +
    (DATA.serve.url ? '，地址 ' + DATA.serve.url : '') + '；开着服务器再重新打开本页。';
}
render();
</script>
</body>
</html>
"""


def _html_escape(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build(manifest_path: str, output_path: str | None, force: bool) -> dict:
    manifest_path = os.path.abspath(manifest_path)
    data, inputs = load_manifest(manifest_path)
    output = os.path.realpath(output_path) if output_path else os.path.join(
        os.path.dirname(manifest_path), "style-explorer.html")
    if output in inputs:
        raise ValueError("输出不能覆盖 manifest 或候选文件")
    if os.path.commonpath([output, os.path.realpath(SKILL_ROOT)]) == os.path.realpath(SKILL_ROOT):
        raise ValueError("输出不能写进 Skill 安装目录；把对比页生成在任务目录里")
    if os.path.exists(output) and not force:
        raise FileExistsError(f"输出已存在：{output}。要更新它就加 --force，要保留它就用 --output 换一个路径")
    data["viewports"] = DEFAULT_VIEWPORTS
    origins = set()
    for candidate in data["candidates"]:
        if candidate["kind"] == "url":
            parts = urlsplit(candidate["content"])
            host = "localhost" if parts.hostname == "::1" else (parts.hostname or "").lower()
            port = f":{parts.port}" if parts.port is not None else ""
            origins.add(f"{parts.scheme}://{host}{port}")
    connect_csp = "connect-src " + (" ".join(sorted(origins)) if origins else "'none'")
    frame_origins = (" " + " ".join(sorted(origins))) if origins else ""
    # 候选内容里出现 "</script>" 或行分隔符不能逃出数据槽
    payload = (json.dumps(data, ensure_ascii=False)
               .replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    page = EXPLORER_TEMPLATE
    for marker, value in ((CONNECT_MARKER, connect_csp), (DATA_MARKER, payload),
                          ("__FRAME_ORIGINS__", frame_origins)):
        if page.count(marker) != 1:
            raise ValueError(f"模板数据入口缺失或重复: {marker}")
        page = page.replace(marker, value)
    round_label = f"第 {data['round']} 轮 · {len(data['candidates'])} 个候选"
    round_prefix = f"第{data['round']}轮" if data["round"] != "01" else "第01轮"
    page = (page.replace("__PROJECT__", _html_escape(str(data["project"])))
                .replace("__BRIEF__", _html_escape(str(data["brief"])))
                .replace("__ROUND_LABEL__", _html_escape(str(round_label)))
                .replace("__ROUND_PREFIX__", _html_escape(str(round_prefix))))
    os.makedirs(os.path.dirname(output), exist_ok=True)
    if force:
        temp = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=os.path.dirname(output),
                                             delete=False) as handle:
                temp = handle.name
                handle.write(page)
            os.replace(temp, output)
        finally:
            if temp and os.path.exists(temp):
                os.unlink(temp)
    else:
        with open(output, "x", encoding="utf-8") as handle:
            handle.write(page)
    if origins and "serve" not in data:
        print("提醒：本轮包含 url 候选，建议在 manifest 顶层补上 serve 启动方式，方便重新打开对比页。", file=sys.stderr)
    return {"output": os.path.relpath(output, os.getcwd()), "candidates": len(data["candidates"]),
            "fingerprint": data["fingerprint"], "bytes": os.path.getsize(output)}


HELP_EPILOG = """\
用法示例：
  python3 scripts/build-explorer.py <manifest 所在目录>/manifest.json
      生成 <manifest 所在目录>/style-explorer.html；已有同名文件时加 --force 覆盖，
      或用 --output 换一个路径。

manifest.json 最少要有：
  {"schemaVersion": 1, "project": "<项目名>", "brief": "<所有候选共同的内容与任务>",
   "candidates": [{"id": "a", "name": "<方向名>", "concept": "<一句体验意图>",
     "typography": "<实际使用的字体关系>", "palette": ["#112233", "#f5f5f5"],
     "traits": ["<看得见的特征>"], "source": "a.html"}]}

可选字段：
  round             顶层。轮次，如 "01"，会出现在用户复制的选择句里。
  nativeViewport    固定画布的原生视口。写顶层对所有候选生效，写候选里只对它生效。
                    认 "1920x1080"、"1920×1080" 和 {"width":1920,"height":1080}。
                    省略时用对比页预设：桌面 1280×900、手机 390×844。
  kind              候选。"html"（默认）、"image"（source 指 PNG/JPEG/WebP），
                    或 "url"（用 url 字段代替 source，只认 localhost/127.0.0.1/::1）。
  serve             顶层。有 url 候选时写启动方式：
                    {"command": "<启动命令>", "cwd": "<项目绝对路径>", "url": "<服务地址>"}
  interactive       候选。true = 可操作小样：单个 HTML、脚本内联、无网络。
  baseline          候选。true = 现状，排第一位并标「现状」，每轮最多一个。

候选文件要求：候选与它引用的图片/字体/视频都放在 manifest 目录或子目录里，
生成器会把它们内嵌（不引用网络资源）；HTML 候选要带 head，不认 iframe/object/
embed/base/srcset。问题会一次列全；成功时 stdout 一行 JSON（output/candidates/
fingerprint/bytes）。对比页不写回任何文件，选择由用户复制回传。
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="build-explorer.py",
        description="把 manifest 里列出的候选页面组装成一张可离线打开的风格对比页。",
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("manifest", help="manifest.json 路径（候选文件与它同目录）")
    parser.add_argument("--output", default=None, help="输出 HTML 路径（默认 manifest 旁边的 style-explorer.html）")
    parser.add_argument("--force", action="store_true", help="输出已存在时覆盖")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        print(json.dumps(build(args.manifest, args.output, args.force), ensure_ascii=False))
        return 0
    except ManifestError as exc:
        print(f"未生成对比页：{exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(f"未生成对比页：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
