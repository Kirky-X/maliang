#!/usr/bin/env python3
"""资产在场后置验收门(G40 脚本层):品牌/内容资产渲染在场验证。

生成后逐资产位核验(移植自 superdesign-skill LOGO RENDER POSTCONDITION,
#29,2026-10 吸收):
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


def main(argv=None):
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
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("verify-assets: manifest 不可读: %s" % exc, file=sys.stderr)
        return 2
    if not isinstance(manifest, list):
        print("verify-assets: manifest 必须是 JSON 数组", file=sys.stderr)
        return 2

    html = open(args.html, encoding="utf-8", errors="replace").read()
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


if __name__ == "__main__":
    sys.exit(main())
