#!/usr/bin/env python3
"""确定性 AI-tell 代码检测器(纯正则,无 LLM)。

用法:
    python3 scripts/detect-tells.py <file_or_dir...> [--format {text,json}]

扫描用户真实代码文件(preview 自包含 HTML / redesign 改动行所在文件),只收
**可正则表达的机械规则**;品味类 tell(配色气质 / 布局节奏 / 文案腔调)不在此
扫描,留给 ai-tells.md 的人工对照流程——确定性判断用代码,品味判断留给人与
LLM 评审。

检测规则(与 ai-tells.md 对应):
  gradient-text    渐变文字(bg-clip-text / background-clip:text)          → ai-tells §1
  glow-shadow      辉光阴影(0 偏移大模糊的 box/text-shadow、drop-shadow)   → ai-tells §1
  uniform-radius   全场同圆角(单文件 ≥4 处同一非平凡圆角)                 → ai-tells §1
  tracking-abuse   tracking 滥用(单文件 ≥3 行 tracking-tight*,或 ≥4 行负 letter-spacing) → ai-tells §2
  colored-border   彩边框卡片(饱和色边框;Tailwind 只判 300-700 档)         → ai-tells §1

豁免:复用 ai-tells.md 第 0 节机制——三豁免(DESIGN.md 批准 / 世界类型自洽 /
内容真有动机)的语义判断由人完成,脚本只认**显式记录**的 tell-exempt 标注:

    <!-- tell-exempt: gradient-text, DESIGN.md 批准 -->   HTML 注释
    /* tell-exempt: uniform-radius file */                CSS/JS 注释(// 同理)

标注出现在命中行或其紧邻上一行 → 豁免该处命中;规则 id 带空格 + `file` 后缀
(或标记内单独写 `file`)→ 该规则全文件豁免;`all` 代指全部规则。
误报治理走最窄原则:具体行 > 单文件单规则 > 全项目,能不用 file 豁免就不用。

退出码: 0 = 无非豁免命中; 1 = 有非豁免命中; 2 = 用法 / 输入错误。
依赖: Python 3 标准库(无第三方依赖)。
来源: impeccable hooks 两层规则与豁免窄化思想,2026-09 吸收(中文自研实现)。
"""

import argparse
import json
import os
import re
import sys

# 扫描的代码文件扩展名(设计相关文件;参考 impeccable hooks 内建清单)
SCAN_EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro",
}

# 目录递归扫描时跳过
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}

RULE_GRADIENT_TEXT = "gradient-text"
RULE_GLOW_SHADOW = "glow-shadow"
RULE_UNIFORM_RADIUS = "uniform-radius"
RULE_TRACKING_ABUSE = "tracking-abuse"
RULE_COLORED_BORDER = "colored-border"

# 阈值(确定性口径,写死不猜)
GLOW_BOX_BLUR_MIN = 16      # box-shadow / drop-shadow 0 偏移模糊 ≥16px 判辉光
GLOW_TEXT_BLUR_MIN = 8      # text-shadow 0 偏移模糊 ≥8px 判辉光
UNIFORM_RADIUS_MIN = 4      # 单文件 ≥4 处同一圆角判"全场同圆角"
TRACKING_TW_MIN = 3         # ≥3 行 tracking-tight/tighter 判滥用
TRACKING_CSS_MIN = 4        # ≥4 行负 letter-spacing 判滥用
SATURATION_MIN = 60         # RGB 通道 max-min ≥60 判饱和色(彩边框)

# ---------------------------------------------------------------------------
# 豁免解析
# ---------------------------------------------------------------------------

_EXEMPT_RE = re.compile(r"tell-exempt:\s*([^*>\n]+)")


def parse_exemptions(lines):
    """解析 tell-exempt 标注。

    返回 (file_scope, line_scope):
    - file_scope: set,全文件豁免的规则 id(可含 "*" 代全部)
    - line_scope: dict rule_id -> set(行号),豁免该行与紧邻下一行(可含 "*")
    """
    file_scope = set()
    line_scope = {}

    for i, line in enumerate(lines, 1):
        for m in _EXEMPT_RE.finditer(line):
            tokens = [t.strip() for t in m.group(1).split(",") if t.strip()]
            rules = []
            for token in tokens:
                if token == "file":
                    # 单独的 `file` 前置规则全部升级为文件级豁免
                    file_scope.update(rules)
                    rules = []
                elif token.endswith(" file"):
                    file_scope.add(token[: -len(" file")].strip())
                elif token in ("all", "*"):
                    rules.append("*")
                else:
                    rules.append(token)
            for rule in rules:
                line_scope.setdefault(rule, set()).update({i, i + 1})

    return file_scope, line_scope


def is_exempt(rule, lineno, file_scope, line_scope):
    """判定某行某规则命中是否被显式豁免。"""
    if rule in file_scope or "*" in file_scope:
        return True
    return lineno in line_scope.get(rule, ()) or lineno in line_scope.get("*", ())


# ---------------------------------------------------------------------------
# 颜色解析(确定性,供彩边框饱和度判断)
# ---------------------------------------------------------------------------

_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_RGB_FUNC_RE = re.compile(r"^rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")


def parse_color(token):
    """解析 #rgb/#rrggbb/rgb()/rgba() 颜色,返回 (r, g, b);失败返回 None。"""
    token = token.strip()
    if _HEX_RE.match(token):
        hex_body = token[1:]
        if len(hex_body) == 3:
            hex_body = "".join(ch * 2 for ch in hex_body)
        return tuple(int(hex_body[i : i + 2], 16) for i in (0, 2, 4))
    m = _RGB_FUNC_RE.match(token)
    if m:
        return tuple(int(m.group(i)) for i in (1, 2, 3))
    return None


def is_saturated(token):
    """饱和色判定:通道极差 ≥ SATURATION_MIN 且非近黑(排除黑/白/灰描边)。"""
    rgb = parse_color(token)
    if rgb is None:
        return False
    return max(rgb) - min(rgb) >= SATURATION_MIN and max(rgb) >= SATURATION_MIN


# ---------------------------------------------------------------------------
# 五条检测规则(每条返回 finding dict 列表)
# ---------------------------------------------------------------------------

_GRADIENT_TEXT_RE = re.compile(r"bg-clip-text|background-clip\s*:\s*text", re.IGNORECASE)

_SHADOW_GLOW_RE = re.compile(
    r"(?:box|text)-shadow\s*:[^;}\n]{0,160}?[,\s]0(?:px)?\s+0(?:px)?\s+(\d{1,4})px",
    re.IGNORECASE,
)
_DROP_SHADOW_GLOW_RE = re.compile(
    r"drop-shadow\(\s*0(?:px)?\s+0(?:px)?\s+(\d{1,4})px", re.IGNORECASE
)

_BORDER_RADIUS_CSS_RE = re.compile(r"border-radius\s*:\s*([^;}\n]+)")
_BORDER_RADIUS_TW_RE = re.compile(r"\brounded(?:-(none|sm|md|lg|xl|2xl|3xl|full))?\b")
_RADIUS_TRIVIAL = {"0", "0px", "none", "50%", "9999px", "full", "circle"}

_TRACKING_TW_RE = re.compile(r"\btracking-(?:tight|tighter)\b")
_TRACKING_CSS_RE = re.compile(r"letter-spacing\s*:\s*-(?:\d*\.)?\d+(?:em|px|rem)")

_BORDER_TW_RE = re.compile(
    r"\bborder-(?:red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|"
    r"indigo|violet|purple|fuchsia|pink|rose)-(\d{2,3})\b"
)
_BORDER_CSS_RE = re.compile(
    r"(?:^|[;\s{])border(?:-(?:top|right|bottom|left))?\s*:\s*([^;}\n]+)", re.MULTILINE
)
_COLOR_TOKEN_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)")


def check_gradient_text(rel_path, lines, file_scope, line_scope):
    """规则 1:渐变文字(bg-clip-text / background-clip:text)。"""
    findings = []
    for i, line in enumerate(lines, 1):
        if _GRADIENT_TEXT_RE.search(line):
            if is_exempt(RULE_GRADIENT_TEXT, i, file_scope, line_scope):
                continue
            findings.append({
                "file": rel_path, "line": i, "rule": RULE_GRADIENT_TEXT,
                "message": "渐变文字签名(bg-clip-text / background-clip:text),见 ai-tells.md §1",
            })
    return findings


def check_glow_shadow(rel_path, lines, file_scope, line_scope):
    """规则 2:辉光阴影(0 偏移大模糊的 shadow 声明)。"""
    findings = []
    for i, line in enumerate(lines, 1):
        for m in _SHADOW_GLOW_RE.finditer(line):
            blur = int(m.group(1))
            is_text = m.group(0).lower().startswith("text-shadow")
            threshold = GLOW_TEXT_BLUR_MIN if is_text else GLOW_BOX_BLUR_MIN
            if blur < threshold:
                continue
            if is_exempt(RULE_GLOW_SHADOW, i, file_scope, line_scope):
                continue
            findings.append({
                "file": rel_path, "line": i, "rule": RULE_GLOW_SHADOW,
                "message": "辉光阴影(0 偏移 %dpx 模糊 ≥%dpx),见 ai-tells.md §1" % (blur, threshold),
            })
        for m in _DROP_SHADOW_GLOW_RE.finditer(line):
            blur = int(m.group(1))
            if blur < GLOW_BOX_BLUR_MIN:
                continue
            if is_exempt(RULE_GLOW_SHADOW, i, file_scope, line_scope):
                continue
            findings.append({
                "file": rel_path, "line": i, "rule": RULE_GLOW_SHADOW,
                "message": "辉光阴影(drop-shadow 0 偏移 %dpx 模糊 ≥%dpx),见 ai-tells.md §1" % (blur, GLOW_BOX_BLUR_MIN),
            })
    return findings


def _radius_values(lines):
    """收集单文件全部圆角声明,返回 [(行号, 归一化值)](仅非平凡值)。"""
    values = []
    for i, line in enumerate(lines, 1):
        for m in _BORDER_RADIUS_CSS_RE.finditer(line):
            first = m.group(1).strip().split()[0] if m.group(1).strip() else ""
            first = first.rstrip(",;")
            if first.startswith(("var(", "{")) or first in _RADIUS_TRIVIAL:
                continue
            values.append((i, first))
        for m in _BORDER_RADIUS_TW_RE.finditer(line):
            token = m.group(1) if m.group(1) else "rounded"
            if token in ("none", "full"):
                continue
            values.append((i, token))
    return values


def check_uniform_radius(rel_path, lines, file_scope, line_scope):
    """规则 3:全场同圆角(≥UNIFORM_RADIUS_MIN 处同一非平凡圆角)。

    聚合型规则:整文件至多报 1 处,定位于首个圆角声明行。
    """
    values = _radius_values(lines)
    if len(values) < UNIFORM_RADIUS_MIN:
        return []
    unique = {v for _, v in values}
    if len(unique) != 1:
        return []
    if is_exempt(RULE_UNIFORM_RADIUS, values[0][0], file_scope, line_scope):
        return []
    return [{
        "file": rel_path, "line": values[0][0], "rule": RULE_UNIFORM_RADIUS,
        "message": "全场同圆角(%d 处均为 %s,无层级分档),见 ai-tells.md §1"
                   % (len(values), values[0][1]),
    }]


def check_tracking_abuse(rel_path, lines, file_scope, line_scope):
    """规则 4:tracking 滥用(多行统一负字距,无分档)。聚合型,至多报 1 处。"""
    tw_lines = [i for i, line in enumerate(lines, 1) if _TRACKING_TW_RE.search(line)]
    css_lines = [i for i, line in enumerate(lines, 1) if _TRACKING_CSS_RE.search(line)]

    if len(tw_lines) >= TRACKING_TW_MIN:
        first = tw_lines[0]
        if not is_exempt(RULE_TRACKING_ABUSE, first, file_scope, line_scope):
            return [{
                "file": rel_path, "line": first, "rule": RULE_TRACKING_ABUSE,
                "message": "tracking 滥用(%d 行统一 tracking-tight*,display 与 UI 字体未分档),见 ai-tells.md §2"
                           % len(tw_lines),
            }]
    if len(css_lines) >= TRACKING_CSS_MIN:
        first = css_lines[0]
        if not is_exempt(RULE_TRACKING_ABUSE, first, file_scope, line_scope):
            return [{
                "file": rel_path, "line": first, "rule": RULE_TRACKING_ABUSE,
                "message": "tracking 滥用(%d 行负 letter-spacing,字距未随字号分档),见 ai-tells.md §2 与 font.md 字距节"
                           % len(css_lines),
            }]
    return []


def check_colored_border(rel_path, lines, file_scope, line_scope):
    """规则 5:彩边框卡片(饱和色边框;Tailwind 只判 300-700 档)。"""
    findings = []
    for i, line in enumerate(lines, 1):
        hit = None
        for m in _BORDER_TW_RE.finditer(line):
            if 300 <= int(m.group(1)) <= 700:
                hit = "border-%s" % m.group(0).split("-")[1]
                break
        if hit is None:
            for m in _BORDER_CSS_RE.finditer(line):
                for color_m in _COLOR_TOKEN_RE.finditer(m.group(1)):
                    if is_saturated(color_m.group(0)):
                        hit = color_m.group(0)
                        break
                if hit:
                    break
        if hit is None:
            continue
        if is_exempt(RULE_COLORED_BORDER, i, file_scope, line_scope):
            continue
        findings.append({
            "file": rel_path, "line": i, "rule": RULE_COLORED_BORDER,
            "message": "彩边框(饱和色 %s;确认语义色或按 ai-tells.md §0 豁免)" % hit,
        })
    return findings


_CHECKS = (
    check_gradient_text,
    check_glow_shadow,
    check_uniform_radius,
    check_tracking_abuse,
    check_colored_border,
)


def scan_text(text, rel_path):
    """扫描单文件文本,返回 (findings, exempted_count)。"""
    lines = text.splitlines()
    file_scope, line_scope = parse_exemptions(lines)

    findings = []
    for check in _CHECKS:
        findings.extend(check(rel_path, lines, file_scope, line_scope))

    # 豁免计数:同一套匹配在不带豁免的口径下重跑一次,差值即被豁免掉的命中数
    total_hits = 0
    for check in _CHECKS:
        total_hits += len(check(rel_path, lines, set(), {}))

    findings.sort(key=lambda f: (f["file"], f["line"], f["rule"]))
    return findings, total_hits - len(findings)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def collect_files(paths):
    """展开输入路径(文件 / 目录)为待扫描文件列表;路径不存在返回 None。"""
    files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                for name in sorted(names):
                    if os.path.splitext(name)[1].lower() in SCAN_EXTENSIONS:
                        files.append(os.path.join(root, name))
        elif os.path.isfile(path):
            files.append(path)
        else:
            print("detect-tells: 路径不存在: %s" % path, file=sys.stderr)
            return None
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="确定性 AI-tell 代码检测器(纯正则,无 LLM;豁免口径见 references/meta/ai-tells.md 第 0 节)"
    )
    parser.add_argument("paths", nargs="+", help="待扫描的文件或目录")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式: text(默认) / json",
    )
    args = parser.parse_args(argv)

    files = collect_files(args.paths)
    if files is None:
        return 2

    findings = []
    exempted = 0
    unreadable = 0
    for path in files:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            print("detect-tells: 读取失败(跳过): %s (%s)" % (path, exc), file=sys.stderr)
            unreadable += 1
            continue
        file_findings, file_exempted = scan_text(text, path)
        findings.extend(file_findings)
        exempted += file_exempted

    if args.format == "json":
        print(json.dumps({
            "files_scanned": len(files) - unreadable,
            "unreadable": unreadable,
            "exempted": exempted,
            "findings": findings,
        }, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print("%s:%d: [%s] %s" % (
                finding["file"], finding["line"], finding["rule"], finding["message"],
            ))
        print("扫描 %d 个文件,命中 %d 处 tell(豁免 %d 处,读取失败 %d 个)"
              % (len(files) - unreadable, len(findings), exempted, unreadable))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
