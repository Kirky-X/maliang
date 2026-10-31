#!/usr/bin/env python3
"""audit —— 内容与证据审计域合并入口(6→1)。

用法(子命令 + 各自原参数透传):
    python3 scripts/audit.py tells <文件...> [options]        # AI 味三批规则扫描
    python3 scripts/audit.py copy <文件...> [options]         # 句型级反模板
    python3 scripts/audit.py claims <repo> [options]          # 公开声明对账(lint-checks.json)
    python3 scripts/audit.py structure-history [options]      # 轮换重复/热轴/盖章真伪(G41/G42)
    python3 scripts/audit.py fingerprint [options]            # 重审计源码指纹
    python3 scripts/audit.py evidence <目录> [options]        # 取证齐套校验

退出码: 各子命令沿用原脚本三态语义,canonical 见 scripts/EXIT-CODES.md。
各节实现为原独立脚本全文并入;同名冲突按节改名(SCAN_EXTENSIONS·SKIP_DIRS·
collect_files 的 _TELLS/_COPY 双份、evidence 的 run→run_evidence)。
依赖: Python 3 标准库(无第三方依赖)。
"""

import sys

_SUBCOMMANDS = ("tells", "copy", "claims", "structure-history",
                "fingerprint", "evidence")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("usage: audit.py {" + "|".join(_SUBCOMMANDS) + "} [args...]")
        return 2
    dispatch = {
        "tells": _main_tells,
        "copy": _main_copy,
        "claims": _main_claims,
        "structure-history": _main_structure_history,
        "fingerprint": _main_fingerprint,
        "evidence": _main_evidence,
    }
    if argv[0] not in dispatch:
        print("[ERROR] 未知子命令: " + argv[0] + "(可用: " + ", ".join(_SUBCOMMANDS) + ")")
        return 2
    return dispatch[argv[0]](argv[1:])


# ============================================================
# 来源节: detect-tells.py (子命令: tells)

# ---- 原 detect-tells.py 模块说明 ----
"""确定性 AI-tell 代码检测器(纯正则,无 LLM)。

用法:
    python3 scripts/detect-tells.py <file_or_dir...> [--format {text,json}]

扫描用户真实代码文件(preview 自包含 HTML / redesign 改动行所在文件),只收
**可正则表达的机械规则**;品味类 tell(配色气质 / 布局节奏 / 文案腔调)不在此
扫描,留给 ai-tells.md 的人工对照流程——确定性判断用代码,品味判断留给人与
LLM 评审。

检测规则按**四档严重级**对齐:
critical 与 major 进「硬命中」通道 → 退出码 1;minor 与 warn 进告警档,只报不拦。

硬命中通道(退出码 1):
  gradient-text         渐变文字(bg-clip-text / background-clip:text)        → ai-tells §1 [critical]
  glow-shadow           辉光阴影(0 偏移大模糊的 box/text-shadow、drop-shadow) → ai-tells §1 [major]
  uniform-radius        全场同圆角(单文件 ≥4 处同一非平凡圆角)               → ai-tells §1 [major]
  tracking-abuse        tracking 滥用(单文件 ≥3 行 tracking-tight*,或 ≥4 行负 letter-spacing) → ai-tells §2 [major]
  colored-border        彩边框卡片(饱和色边框;Tailwind 只判 300-700 档)      → ai-tells §1 [major]
  purple-cyan-gradient  紫蓝粉渐变背景:同一渐变内紫系(255°-350°)与蓝青系(170°-255°)
                        同现,或 Tailwind class 紫系(purple/violet/fuchsia/indigo)
                        搭配蓝青系(cyan/sky/blue/teal)或粉系(pink/rose)——按值判定
                        补齐「只认 Tailwind class」的逃逸通道(裸 CSS 渐变同样命中)  → ai-tells §1 [critical]
  transition-all        transition: all / transition-all(动画不列具体属性)    → numbered-gates G17 [critical]
  uppercase-heading     ALL CAPS 标题(h1-h4 + uppercase;≤13px 且加字距的小标签例外) → ai-tells §10 [critical]
  celebration-motion    庆祝性动效(class/animation 命中 animate-bounce/confetti/
                        celebrat*/firework*)                                  → G18 + component.md [major]
  emoji-icon            emoji 当功能图标(元素内容全 emoji,或 emoji 前缀标题)  → ai-tells 人工通道 [major]
  placeholder-copy      Lorem ipsum 占位文案残留                              → ai-tells §4 [major]
  lilac-purple          柔紫强调色(#a78bfa / #c4b5fd / #8b5cf6)               → ai-tells §7 [major]
  gradient-button       渐变 CTA/按钮(同行 btn/button/cta × 渐变标记)        → ai-tells §1 [major]
  aurora-blob           aurora 光斑背景(blur ≥40px / blur-2xl·3xl 色斑;
                        <img> 打码行与 backdrop-filter 行除外)               → ai-tells §1 [major]
  library-primary       库默认主色(#6366f1 / #4f46e5 / #409eff / #5e6ad2)    → ai-tells §7 [major]
  uniform-shadow        全场同款阴影(≥4 处同一 shadow,无海拔分档)           → ai-tells §1 [major]

告警档(advisory,只报不拦,不影响退出码;同样支持 tell-exempt 豁免):
  numbered-eyebrow [minor]  零填充编号 eyebrow(「01 · About」装饰性编号)      → ai-tells §10
  glass-backdrop-blur [minor] 玻璃拟态默认(backdrop-blur;命中不自动违规,
                            液态玻璃模板墙与 §0 豁免放行)                     → ai-tells §1
  undeclared-font [minor]   字体声明未加载(font-family 引用的字族在本文件内
                            无 @font-face/字体链接;外部加载须人工核)          → ai-tells §2
  reflex-font [warn]        display 首位字族命中 ai-tells §11 反射字体清单。命中不自动
                            违规(仍走 §0 豁免总则),故进告警档而非硬失败通道;命中后
                            要么换字族,要么写出「没有其他字体能满足」的理由并标豁免。

豁免:复用 ai-tells.md 第 0 节机制——三豁免(DESIGN.md 批准 / 世界类型自洽 /
内容真有动机)的语义判断由人完成,脚本只认**显式记录**的 tell-exempt 标注:

    <!-- tell-exempt: gradient-text, DESIGN.md 批准 -->   HTML 注释
    /* tell-exempt: uniform-radius file */                CSS/JS 注释(// 同理)

标注出现在命中行或其紧邻上一行 → 豁免该处命中;规则 id 带空格 + `file` 后缀
(或标记内单独写 `file`)→ 该规则全文件豁免;`all` 代指全部规则。
误报治理走最窄原则:具体行 > 单文件单规则 > 全项目,能不用 file 豁免就不用。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        告警档(minor/warn)命中不改变退出码。
依赖: Python 3 标准库(无第三方依赖)。
      四档对齐与机械规则扩充: 规则库 scripts/detect/rules.mjs(#21)
      第三批(gradient-button/aurora-blob/library-primary/uniform-shadow/
      glass-backdrop-blur/undeclared-font): 社区 AI-slop 清单扩充
      (developersdigest.dev 16 patterns / funboy322 avoid-ai-design),2026-10-25。
"""
# ---- 模块说明结束 ----
import argparse
import json
import os
import re
import sys
from urllib.parse import unquote

# 扫描的代码文件扩展名(设计相关文件;参考 设计工艺库 hooks 内建清单)
SCAN_EXTENSIONS_TELLS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro",
}

# 目录递归扫描时跳过
SKIP_DIRS_TELLS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}

# 四档严重级(与 maliang 审查三档 + 告警档对齐;出处：规则库 #21 四档)
SEV_CRITICAL = "critical"   # 硬失败
SEV_MAJOR = "major"         # 硬失败
SEV_MINOR = "minor"         # 告警档(不拦截)
SEV_WARN = "warn"           # 告警档(不拦截)
HARD_SEVERITIES = (SEV_CRITICAL, SEV_MAJOR)

RULE_GRADIENT_TEXT = "gradient-text"
RULE_GLOW_SHADOW = "glow-shadow"
RULE_UNIFORM_RADIUS = "uniform-radius"
RULE_TRACKING_ABUSE = "tracking-abuse"
RULE_COLORED_BORDER = "colored-border"
RULE_REFLEX_FONT = "reflex-font"
RULE_PURPLE_GRADIENT = "purple-cyan-gradient"
RULE_TRANSITION_ALL = "transition-all"
RULE_UPPERCASE_HEADING = "uppercase-heading"
RULE_CELEBRATION_MOTION = "celebration-motion"
RULE_EMOJI_ICON = "emoji-icon"
RULE_PLACEHOLDER_COPY = "placeholder-copy"
RULE_LILAC_PURPLE = "lilac-purple"
RULE_NUMBERED_EYEBROW = "numbered-eyebrow"
RULE_GRADIENT_BUTTON = "gradient-button"
RULE_AURORA_BLOB = "aurora-blob"
RULE_LIBRARY_PRIMARY = "library-primary"
RULE_UNIFORM_SHADOW = "uniform-shadow"
RULE_GLASS_BACKDROP = "glass-backdrop-blur"
RULE_UNDECLARED_FONT = "undeclared-font"

# 阈值(确定性口径,写死不猜)
GLOW_BOX_BLUR_MIN = 16      # box-shadow / drop-shadow 0 偏移模糊 ≥16px 判辉光
GLOW_TEXT_BLUR_MIN = 8      # text-shadow 0 偏移模糊 ≥8px 判辉光
UNIFORM_RADIUS_MIN = 4      # 单文件 ≥4 处同一圆角判"全场同圆角"
UNIFORM_SHADOW_MIN = 4      # 单文件 ≥4 处同一阴影判"全场同款重阴影"
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
                "severity": SEV_CRITICAL,
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
                "severity": SEV_MAJOR,
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
                "severity": SEV_MAJOR,
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
                "severity": SEV_MAJOR,
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
                "severity": SEV_MAJOR,
                "message": "tracking 滥用(%d 行统一 tracking-tight*,display 与 UI 字体未分档),见 ai-tells.md §2"
                           % len(tw_lines),
            }]
    if len(css_lines) >= TRACKING_CSS_MIN:
        first = css_lines[0]
        if not is_exempt(RULE_TRACKING_ABUSE, first, file_scope, line_scope):
            return [{
                "file": rel_path, "line": first, "rule": RULE_TRACKING_ABUSE,
                "severity": SEV_MAJOR,
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
                "severity": SEV_MAJOR,
            "message": "彩边框(饱和色 %s;确认语义色或按 ai-tells.md §0 豁免)" % hit,
        })
    return findings


# ---------------------------------------------------------------------------
# 第二批扩充规则(#21):紫蓝粉渐变按值判定 + ALL CAPS 标题 + emoji 图标
# ---------------------------------------------------------------------------

# Tailwind 渐变方向 class 与 stop 色阶 from/via/to
_TW_GRADIENT_DIR_RE = re.compile(r"\bbg-gradient-to-(?:r|l|t|b|tr|tl|br|bl)\b")
_TW_STOP_RE = re.compile(r"\b(?:from|via|to)-([a-z]+)-\d{2,3}\b")
_TW_PURPLE_SET = {"purple", "violet", "fuchsia", "indigo"}
_TW_PINK_SET = {"pink", "rose"}
_TW_COOL_SET = {"cyan", "sky", "blue", "teal"}

# CSS 渐变函数与颜色字面量(按值判定,补齐「只认 Tailwind class」逃逸通道)
_GRADIENT_FN_RE = re.compile(
    r"(?:linear|radial|conic)-gradient\(([^()]*(?:\([^()]*\)[^()]*)*)\)", re.IGNORECASE
)
_GRADIENT_STOP_RE = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)|oklch\([^)]*\)"
)

# 暖紫带/冷蓝青带(规则库 原口径 255-330;上限放宽到 350 覆盖 ai-tells §1
# 「紫蓝粉」的 pink 系 330°-345°——自研口径,标注)
_WARM_HUE_LO, _WARM_HUE_HI = 255.0, 350.0
_COOL_HUE_LO, _COOL_HUE_HI = 170.0, 255.0


def css_hue(token):
    """CSS 颜色字面量的色相(度),读不出返回 None(近灰无有效色相亦 None)。

    改写自 规则库 scripts/detect/rules.mjs cssHue(#21)
    """
    v = token.strip().lower()
    m = re.match(r"^hsla?\(\s*([\d.]+)(?:deg)?", v)
    if m:
        return float(m.group(1)) % 360
    m = re.match(r"^oklch\(\s*[\d.%]+\s+[\d.]+\s+([\d.]+)", v)
    if m:
        return float(m.group(1)) % 360
    rgb = parse_color(v)
    if rgb is None:
        return None
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 0.12:  # 近灰无有效色相,当一色会产出噪声
        return None
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return (h * 60) % 360


def check_purple_cyan_gradient(rel_path, lines, file_scope, line_scope):
    """规则 6:紫蓝粉渐变背景(裸 CSS 渐变按值判定 + Tailwind class 词表)。

    判定:同一渐变内 紫系(暖带 ≥1 stop)与 蓝青系(冷带 ≥1 stop)同现;
    Tailwind 形式按色名词表(紫系 × [蓝青系 ∪ 粉系])。归属 ai-tells §1。
    """
    findings = []
    for i, line in enumerate(lines, 1):
        hit = None
        m = _GRADIENT_FN_RE.search(line)
        if m:
            hues = [css_hue(s) for s in _GRADIENT_STOP_RE.findall(m.group(0))]
            hues = [h for h in hues if h is not None]
            warm = any(_WARM_HUE_LO <= h < _WARM_HUE_HI for h in hues)
            cool = any(_COOL_HUE_LO <= h < _COOL_HUE_HI for h in hues)
            if warm and cool:
                hit = m.group(0)[:90]
        if hit is None and _TW_GRADIENT_DIR_RE.search(line):
            stops = {c.lower() for c in _TW_STOP_RE.findall(line)}
            has_purple = bool(stops & _TW_PURPLE_SET)
            has_cool = bool(stops & _TW_COOL_SET)
            has_pink = bool(stops & _TW_PINK_SET)
            if has_purple and (has_cool or has_pink):
                hit = line.strip()[:90]
        if hit is None:
            continue
        if is_exempt(RULE_PURPLE_GRADIENT, i, file_scope, line_scope):
            continue
        findings.append({
            "file": rel_path, "line": i, "rule": RULE_PURPLE_GRADIENT,
            "severity": SEV_CRITICAL,
            "message": "紫蓝粉渐变背景(%s),见 ai-tells.md §1;背景改中性梯度,品牌色仅 10%% 强调" % hit,
        })
    return findings


_UPPERCASE_TW_RE = re.compile(
    r"<h[1-4]\b[^>]*\bclass\s*=\s*[\"'][^\"']*\buppercase\b[^\"']*[\"']", re.IGNORECASE
)
_UPPERCASE_TW_SMALL_RE = re.compile(
    r"\btext-(?:xs|\[1?[0-3]px\])\b.*\btracking-(?:wide|wider|widest|\[)"
    r"|\btracking-(?:wide|wider|widest|\[).*\btext-(?:xs|\[1?[0-3]px\])\b"
)
_UPPERCASE_CSS_RE = re.compile(r"h[1-4][^{;]*\{[^}]*text-transform\s*:\s*uppercase", re.IGNORECASE)
_FONT_SIZE_PX_RE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", re.IGNORECASE)
_LETTER_SPACING_RE = re.compile(r"letter-spacing\s*:", re.IGNORECASE)


def check_uppercase_heading(rel_path, lines, file_scope, line_scope):
    """规则 7:ALL CAPS 标题(h1-h4 + uppercase)。

    例外(规则库 同款):≤13px 且加宽字距的小标签是文档化例外,不算喊叫。
    归属 ai-tells §10(生产测试 tells)。
    """
    findings = []
    for i, line in enumerate(lines, 1):
        hit = None
        m = _UPPERCASE_TW_RE.search(line)
        if m:
            if not _UPPERCASE_TW_SMALL_RE.search(m.group(0)):
                hit = m.group(0)[:80]
        else:
            m = _UPPERCASE_CSS_RE.search(line)
            if m:
                size = _FONT_SIZE_PX_RE.search(line)
                if size and float(size.group(1)) <= 13 and _LETTER_SPACING_RE.search(line):
                    continue
                hit = "text-transform: uppercase"
        if hit is None:
            continue
        if is_exempt(RULE_UPPERCASE_HEADING, i, file_scope, line_scope):
            continue
        findings.append({
            "file": rel_path, "line": i, "rule": RULE_UPPERCASE_HEADING,
            "severity": SEV_CRITICAL,
            "message": "ALL CAPS 标题(%s),见 ai-tells.md §10;改 sentence case,大写只留给 ≤13px 加字距小标签" % hit,
        })
    return findings


# emoji 当图标:默认 emoji 表现码点(对勾/箭头等排版字形不算,外部同款边界)
_EMOJI_CP = "\U0001F300-\U0001FAFF\u2728\u26A1\u2705\u274C\u2B50\u2757\u2764"
_EMOJI_ICON_ONLY_RE = re.compile(
    r"<(\w+)[^>]*>\s*[%s]{1,3}\s*</\1>" % _EMOJI_CP
)
_EMOJI_ICON_EMBED_RE = re.compile(
    r"[%s]\s*<(?:h[234]|p\b[^>]*font-semibold)" % _EMOJI_CP
)


def check_emoji_icon(rel_path, lines, file_scope, line_scope):
    """规则 8:emoji 当功能图标(元素内容全 emoji,或 emoji 前缀标题)。

    句中 emoji 不算;来源 规则库 emoji-feature-icon(#21)
    """
    findings = []
    for i, line in enumerate(lines, 1):
        m = _EMOJI_ICON_ONLY_RE.search(line) or _EMOJI_ICON_EMBED_RE.search(line)
        if m and not is_exempt(RULE_EMOJI_ICON, i, file_scope, line_scope):
            findings.append({
                "file": rel_path, "line": i, "rule": RULE_EMOJI_ICON,
                "severity": SEV_MAJOR,
                "message": "emoji 当功能图标(%s);换真图标集(Lucide/Phosphor)——emoji 跨平台渲染不一" % m.group(0)[:60],
            })
    return findings


# ---------------------------------------------------------------------------
# 第三批扩充规则(2026-10-25):社区 AI-slop 清单扩充(developersdigest 16
# patterns / funboy322 avoid-ai-design)——CTA 渐变 / aurora 色斑 / 全场同款
# 重阴影进硬通道;玻璃拟态与未加载字体的告警档在文件尾部
# ---------------------------------------------------------------------------

_GRADIENT_MARKER_RE = re.compile(r"\bbg-gradient-to-[a-z]+\b|(?:linear|radial)-gradient\(", re.IGNORECASE)
_CTA_TOKEN_RE = re.compile(r"\b(?:btn|button|cta)\b", re.IGNORECASE)
_BLUR_BLOB_CSS_RE = re.compile(r"blur\(\s*(?:[4-9]\d|\d{3,})px", re.IGNORECASE)
_BLUR_BLOB_TW_RE = re.compile(r"\bblur-(?:2xl|3xl)\b")
_SHADOW_TW_RE = re.compile(r"\bshadow-(?:sm|md|lg|xl|2xl)\b")
_SHADOW_CSS_RE = re.compile(r"box-shadow\s*:\s*([^;}\n]+)", re.IGNORECASE)


def check_gradient_button(rel_path, lines, file_scope, line_scope):
    """规则:渐变 CTA/按钮(同一行内 btn/button/cta 词元与渐变标记同现)。"""
    findings = []
    for i, line in enumerate(lines, 1):
        if not (_CTA_TOKEN_RE.search(line) and _GRADIENT_MARKER_RE.search(line)):
            continue
        if is_exempt(RULE_GRADIENT_BUTTON, i, file_scope, line_scope):
            continue
        findings.append({
            "file": rel_path, "line": i, "rule": RULE_GRADIENT_BUTTON,
            "severity": SEV_MAJOR,
            "message": "渐变 CTA/按钮(主操作用实色高对比),见 ai-tells.md §1;渐变只在品牌色相内有理由时用于背景层",
        })
    return findings


def check_aurora_blob(rel_path, lines, file_scope, line_scope):
    """规则:aurora 光斑背景(blur ≥40px / blur-2xl·3xl 的装饰色斑)。

    例外:<img> 行(图片打码)与 backdrop-filter 行(玻璃拟态归告警档)不判 aurora。
    """
    findings = []
    for i, line in enumerate(lines, 1):
        m = _BLUR_BLOB_CSS_RE.search(line)
        tw = None if m else _BLUR_BLOB_TW_RE.search(line)
        if not m and not tw:
            continue
        low = line.lower()
        if "<img" in low or "backdrop" in low:
            continue
        hit = m.group(0) if m else tw.group(0)
        if is_exempt(RULE_AURORA_BLOB, i, file_scope, line_scope):
            continue
        findings.append({
            "file": rel_path, "line": i, "rule": RULE_AURORA_BLOB,
            "severity": SEV_MAJOR,
            "message": "aurora 光斑背景(%s;大面积彩色渲染默认形态),见 ai-tells.md §1;背景走中性梯度,品牌色 10%% 强调" % hit,
        })
    return findings


def check_uniform_shadow(rel_path, lines, file_scope, line_scope):
    """规则:全场同款阴影(≥UNIFORM_SHADOW_MIN 处同一 shadow,无海拔分档)。

    聚合型:整文件至多报 1 处,定位于首个 shadow 声明行。var() 引用与 none 不算平凡值。
    """
    values = []
    for i, line in enumerate(lines, 1):
        for m in _SHADOW_TW_RE.finditer(line):
            values.append((i, m.group(0).lower()))
        for m in _SHADOW_CSS_RE.finditer(line):
            v = m.group(1).strip().rstrip(",;")
            if not v or v.startswith(("var(", "{", "none")):
                continue
            values.append((i, v))
    if len(values) < UNIFORM_SHADOW_MIN:
        return []
    unique = {v for _, v in values}
    if len(unique) != 1:
        return []
    if is_exempt(RULE_UNIFORM_SHADOW, values[0][0], file_scope, line_scope):
        return []
    return [{
        "file": rel_path, "line": values[0][0], "rule": RULE_UNIFORM_SHADOW,
        "severity": SEV_MAJOR,
        "message": "全场同款阴影(%d 处均为 %s,无海拔分档),见 ai-tells.md §1;阴影按 elevation 分档,浮层才拿重阴影"
                   % (len(values), values[0][1]),
    }]


_CHECKS = (
    check_gradient_text,
    check_glow_shadow,
    check_uniform_radius,
    check_tracking_abuse,
    check_colored_border,
    check_purple_cyan_gradient,
    check_uppercase_heading,
    check_emoji_icon,
    check_gradient_button,
    check_aurora_blob,
    check_uniform_shadow,
)


# ---------------------------------------------------------------------------
# 告警档:reflex-font(display 首位字族命中 ai-tells §11 反射字体清单)
#
# 不进硬失败通道的理由:ai-tells.md §11 明说「命中不自动违规(仍走第 0 节豁免
# 总则)」,而 preview.md「命中非豁免 tell = 硬性失败」只约束硬通道;两条并存时
# 反射字体只能进告警档。
# ---------------------------------------------------------------------------

_STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
_CSS_COMMENT_STRIP_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
_CSS_PROP_DEF_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;}]+)")
_VAR_REF_START_RE = re.compile(r"var\(\s*(--[\w-]+)")
_FONT_FAMILY_DECL_RE = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.IGNORECASE)
_DISPLAY_SELECTOR_RE = re.compile(
    r"(?:\bh[1-3]\b|display|hero|heading|headline|\btitle\b)", re.IGNORECASE
)
_DISPLAY_VAR_NAME_RE = re.compile(
    r"--[\w-]*(?:display|heading|hero|headline|title)[\w-]*", re.IGNORECASE
)

# ai-tells.md §11 反射字体清单(逐字;小写). 前缀匹配允许 "Crimson Pro" /
# "IBM Plex Sans" / "DM Serif Display" / "Inter Tight" 这类变体
REFLEX_FONTS = (
    "fraunces", "playfair display", "cormorant", "lora", "crimson", "newsreader",
    "syne", "space grotesk", "space mono", "ibm plex", "inter", "dm sans",
    "dm serif", "outfit", "plus jakarta sans", "instrument sans",
    "instrument serif", "geist",
)


def _first_font_family(value, defs):
    """取 font-family 值的首位字族(解析一层 var(--x) 间接),小写、去引号。"""
    v = value.strip()
    m = _VAR_REF_START_RE.match(v)
    if m and m.group(1) in defs:
        v = defs[m.group(1)].strip()
    v = v.split(",")[0].strip().strip("\"'").strip()
    return v.lower()


def _is_reflex_family(family):
    """首位字族是否命中反射字体清单(整名或 `名字 + 变体后缀`)。"""
    return any(family == name or family.startswith(name + " ") for name in REFLEX_FONTS)


def scan_reflex_fonts(text, rel_path):
    """扫描 reflex-font 告警档,返回 warning dict 列表(不影响退出码)。

    判定面(display 上下文两条):
      a) 选择器含 h1-h3 / display / hero / heading / headline / title 的规则里
         声明 font-family;
      b) 名字含 display/heading/hero/headline/title 的自定义属性定义值
         (如 --font-display: "Fraunces", serif)。
    非 display 上下文(正文/UI 字族)不在本扫描范围;命中不自动违规,豁免沿用
    tell-exempt 标注(行级/file/all,与硬命中同一套解析)。
    """
    lines = text.splitlines()
    file_scope, line_scope = parse_exemptions(lines)

    defs = {}
    for m in _CSS_PROP_DEF_RE.finditer(text):
        defs.setdefault(m.group(1), m.group(2).strip())

    targets = [
        (m.start(1), m.group(1)) for m in _STYLE_BLOCK_RE.finditer(text)
    ]
    if not targets:
        targets = [(0, text)]  # .css / .js 文件:无 <style> 时整文件即样式面

    warnings = []
    seen = set()

    def _emit(line_no, family, where):
        if (line_no, family) in seen:
            return
        if is_exempt(RULE_REFLEX_FONT, line_no, file_scope, line_scope):
            return
        seen.add((line_no, family))
        warnings.append({
            "file": rel_path, "line": line_no, "rule": RULE_REFLEX_FONT,
            "message": "display 首位字族 %s 命中反射字体清单(%s),见 ai-tells.md §11"
                       "——换字族,或写出「没有其他字体能满足」的理由并标 tell-exempt"
                       % (family, where),
        })

    for offset, block in targets:
        css = _CSS_COMMENT_STRIP_RE.sub("", block)
        # 无花括号的内容(如纯类名 HTML)对 CSS 规则正则是 O(n²) 回退面,直接跳过
        if "{" not in css:
            continue

        for m in _CSS_PROP_DEF_RE.finditer(css):
            if not _DISPLAY_VAR_NAME_RE.match(m.group(1)):
                continue
            family = _first_font_family(m.group(2), defs)
            if not family or not _is_reflex_family(family):
                continue
            line_no = text[:offset].count("\n") + css[:m.start()].count("\n") + 1
            _emit(line_no, family, "自定义属性 " + m.group(1))

        for m in _CSS_RULE_RE.finditer(css):
            selector = m.group(1).strip()
            if not selector or selector.startswith("@"):
                continue
            if not _DISPLAY_SELECTOR_RE.search(selector):
                continue
            body = m.group(2)
            for fm in _FONT_FAMILY_DECL_RE.finditer(body):
                family = _first_font_family(fm.group(1), defs)
                if not family or not _is_reflex_family(family):
                    continue
                line_no = (text[:offset].count("\n")
                           + css[:m.start(2)].count("\n")
                           + body[:fm.start()].count("\n") + 1)
                _emit(line_no, family, "选择器 " + selector[:36])

    warnings.sort(key=lambda w: (w["file"], w["line"], w["rule"]))
    return warnings


# ---------------------------------------------------------------------------
# 告警档:undeclared-font(font-family 引用的字族在本文件内无加载声明)
#
# 「写了字体名单但没人负责加载」是社区清单点名的确定性签名(渲染静默回落);
# 告警档而非硬失败:多文件项目里字体可在别的文件加载,命中后人工核外部加载,
# preview 自包含 HTML 内命中即应修(自包含产物没有"别的文件")。
# ---------------------------------------------------------------------------

_FONTFACE_FAMILY_RE = re.compile(
    r"@font-face[^{}]{0,2000}\{[^{}]{0,2000}?font-family\s*:\s*[\"']?([^;\"'}\n]{0,200})",
    re.IGNORECASE | re.DOTALL,
)
_WEBFONT_LINK_RE = re.compile(
    r"fonts\.(?:googleapis|gstatic)\.com[^\"'\n]{0,2000}?family=([^&\"'\n]{0,200})", re.IGNORECASE
)
_FONT_FAMILY_USE_RE = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.IGNORECASE)

# 泛型/系统栈字族不算"声明未加载"(本机必有或由栈回落兜底)
_GENERIC_OR_SYSTEM_FONTS = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded",
    "inherit", "initial", "unset",
    "arial", "helvetica", "helvetica neue", "georgia", "times", "times new roman",
    "courier new", "verdana", "tahoma", "trebuchet ms", "impact",
    "-apple-system", "blinkmacsystemfont", "segoe ui", "roboto",
    "sf pro display", "sf pro text", "noto sans", "noto serif",
    "microsoft yahei", "pingfang sc", "hiragino sans gb", "source han sans",
}


def scan_undeclared_fonts(text, rel_path):
    """扫描 undeclared-font 告警档:font-family 引用 vs @font-face/字体链接。

    判定:逐处 font-family 声明取首位字族(解析一层 var() 间接),不在泛型/系统
    栈白名单、也不在本文件 @font-face 或 Google Fonts 链接的已声明集合内 → 告警。
    同一字族至多报一次(定位于首个引用行);豁免沿用 tell-exempt。
    """
    lines = text.splitlines()
    file_scope, line_scope = parse_exemptions(lines)

    defs = {}
    for m in _CSS_PROP_DEF_RE.finditer(text):
        defs.setdefault(m.group(1), m.group(2).strip())

    declared = set()
    for m in _FONTFACE_FAMILY_RE.finditer(text):
        for part in m.group(1).split(","):
            declared.add(part.strip().strip("\"'").lower())
    for m in _WEBFONT_LINK_RE.finditer(text):
        for fam in m.group(1).split("|"):
            name = unquote(fam.replace("+", " ")).split(":")[0].strip().strip("\"'").lower()
            if name:
                declared.add(name)

    warnings = []
    seen = set()
    for i, line in enumerate(lines, 1):
        for m in _FONT_FAMILY_USE_RE.finditer(line):
            family = _first_font_family(m.group(1), defs)
            if not family or family in _GENERIC_OR_SYSTEM_FONTS or family in declared:
                continue
            if family in seen:
                continue
            if is_exempt(RULE_UNDECLARED_FONT, i, file_scope, line_scope):
                continue
            seen.add(family)
            warnings.append({
                "file": rel_path, "line": i, "rule": RULE_UNDECLARED_FONT,
                "severity": SEV_MINOR,
                "message": "字体声明未加载(%s 本文件内无 @font-face/字体链接;多文件项目核外部加载,"
                           "preview 自包含产物内即应修),见 ai-tells.md §2" % family,
            })
    return warnings

# ---------------------------------------------------------------------------
# 行级数据驱动规则表(#21):单正则即判定的规则,归属按 maliang 实际文件
# ---------------------------------------------------------------------------

_LINE_RULES = (
    (RULE_TRANSITION_ALL, SEV_CRITICAL,
     re.compile(r"(?<![\w-])transition\s*:\s*[\"']?all\b|(?<![\w-])transition-all\b"),
     "transition: all(动画不列具体属性),见 numbered-gates.md G17;改列 transform/opacity/background-color"),
    (RULE_CELEBRATION_MOTION, SEV_MAJOR,
     re.compile(r"\bclass\s*=\s*[\"'][^\"']*\b(?:animate-bounce|confetti|celebrat\w+|fireworks?)\b"
                r"|\banimation\s*:[^;}\n]*\b(?:bounce|confetti|fireworks?)\b", re.IGNORECASE),
     "庆祝性动效(结果已在屏上就别庆祝),见 numbered-gates.md G18 与 commands/component.md success 状态"),
    (RULE_PLACEHOLDER_COPY, SEV_MAJOR,
     re.compile(r"\bLorem ipsum\b|\bLorem\b[^.\n]{0,60}\bdolor\b", re.IGNORECASE),
     "Lorem ipsum 占位文案残留,见 ai-tells.md §4;换真实或「显然为假但合理」的域内容"),
    (RULE_LILAC_PURPLE, SEV_MAJOR,
     re.compile(r"#a78bfa|#c4b5fd|#8b5cf6", re.IGNORECASE),
     "柔紫/莫兰迪紫强调色,见 ai-tells.md §7;换具体品牌色相,必须紫时用深紫 #4c1d95"),
    (RULE_LIBRARY_PRIMARY, SEV_MAJOR,
     re.compile(r"#6366f1|#4f46e5|#409eff|#5e6ad2", re.IGNORECASE),
     "库默认主色未调(shadcn indigo / Element Plus 蓝 / Linear 紫),见 ai-tells.md §7;主色从 DESIGN.md 品牌色相派生。"
     "通用 Tailwind blue 不在本表(clean 夹具 #2563eb 为合法 accent 先例),留给人工对照"),
    (RULE_NUMBERED_EYEBROW, SEV_MINOR,
     re.compile(r">\s*0\d{1,2}\s+[·/—–-]\s+[A-Za-z]"),
     "零填充编号 eyebrow(「01 · About」装饰性编号),见 ai-tells.md §10;人工裁量"),
    (RULE_GLASS_BACKDROP, SEV_MINOR,
     re.compile(r"\bbackdrop-blur\b|backdrop-filter\s*:\s*[^;}\n]*blur", re.IGNORECASE),
     "玻璃拟态默认(backdrop-blur;命中不自动违规),见 ai-tells.md §1;液态玻璃走模板墙选型并标 tell-exempt"),
)


def _scan_line_rules(rel_path, lines, file_scope, line_scope, hard_only):
    """跑行级规则表;hard_only=True 返回硬命中,否则返回告警档。"""
    out = []
    for i, line in enumerate(lines, 1):
        for rule_id, severity, regex, message in _LINE_RULES:
            if hard_only != (severity in HARD_SEVERITIES):
                continue
            if regex.search(line) and not is_exempt(rule_id, i, file_scope, line_scope):
                out.append({
                    "file": rel_path, "line": i, "rule": rule_id,
                    "severity": severity, "message": message,
                })
    return out


def scan_text(text, rel_path):
    """扫描单文件文本,返回 (findings, exempted_count)——仅硬命中通道。"""
    lines = text.splitlines()
    file_scope, line_scope = parse_exemptions(lines)

    findings = []
    for check in _CHECKS:
        findings.extend(check(rel_path, lines, file_scope, line_scope))
    findings.extend(_scan_line_rules(rel_path, lines, file_scope, line_scope, hard_only=True))

    # 豁免计数:仅当文件含 tell-exempt 标注时,把同一套匹配在不带豁免的口径下重跑一遍
    # (差值即被豁免掉的命中数;无标注文件的豁免数恒为 0,免除整遍全量重扫)
    total_hits = 0
    if any("tell-exempt" in line for line in lines):
        for check in _CHECKS:
            total_hits += len(check(rel_path, lines, set(), {}))
        total_hits += len(_scan_line_rules(rel_path, lines, set(), {}, hard_only=True))

    findings.sort(key=lambda f: (f["file"], f["line"], f["rule"]))
    return findings, total_hits - len(findings)


def scan_advisory_tells(text, rel_path):
    """扫描告警档行级规则(minor/warn,不拦截),返回 warnings 列表。

    与 reflex-font 同一出口语义:命中不改变退出码,豁免沿用同一套 tell-exempt。
    """
    lines = text.splitlines()
    file_scope, line_scope = parse_exemptions(lines)
    return _scan_line_rules(rel_path, lines, file_scope, line_scope, hard_only=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def collect_files_tells(paths):
    """展开输入路径(文件 / 目录)为待扫描文件列表;路径不存在返回 None。"""
    files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS_TELLS)
                for name in sorted(names):
                    if os.path.splitext(name)[1].lower() in SCAN_EXTENSIONS_TELLS:
                        files.append(os.path.join(root, name))
        elif os.path.isfile(path):
            files.append(path)
        else:
            print("detect-tells: 路径不存在: %s" % path, file=sys.stderr)
            return None
    return files


# 输出卫生:产物派生字符串(文件名/命中片段)进终端前剥离控制字符,防 ANSI 转义注入
_CTL_CLEAN_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def _main_tells(argv=None):
    parser = argparse.ArgumentParser(
        description="确定性 AI-tell 代码检测器(纯正则,无 LLM;豁免口径见 references/meta/ai-tells.md 第 0 节)"
    )
    parser.add_argument("paths", nargs="+", help="待扫描的文件或目录")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式: text(默认) / json",
    )
    args = parser.parse_args(argv)

    files = collect_files_tells(args.paths)
    if files is None:
        return 2

    findings = []
    warnings = []
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
        file_warnings = scan_reflex_fonts(text, path)
        for w in file_warnings:
            w["severity"] = SEV_WARN
        warnings.extend(file_warnings)
        warnings.extend(scan_advisory_tells(text, path))
        warnings.extend(scan_undeclared_fonts(text, path))
        exempted += file_exempted

    warnings.sort(key=lambda w: (w["file"], w["line"], w["rule"]))

    if args.format == "json":
        print(json.dumps({
            "files_scanned": len(files) - unreadable,
            "unreadable": unreadable,
            "exempted": exempted,
            "findings": findings,
            "warnings": warnings,
        }, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print(_CTL_CLEAN_RE.sub("", "%s:%d: [%s] %s" % (
                finding["file"], finding["line"], finding["rule"], finding["message"],
            )))
        for warning in warnings:
            print(_CTL_CLEAN_RE.sub("", "%s:%d: [%s·告警档] %s" % (
                warning["file"], warning["line"], warning["rule"], warning["message"],
            )))
        print("扫描 %d 个文件,命中 %d 处 tell(豁免 %d 处,读取失败 %d 个);告警档 %d 处(不拦截)"
              % (len(files) - unreadable, len(findings), exempted, unreadable, len(warnings)))

    return 1 if findings else 0


# ============================================================
# 来源节: check-copy.py (子命令: copy)

# ---- 原 check-copy.py 模块说明 ----
"""句型级反模板文案扫描(G32/preview-checklist §5.1 脚本层)。

词表禁令挡不住换同义词——真正的 tell 是**句子模板**本身:"The [adj] way to
[verb]" 换哪个词都读作生成。本脚本收 10 式模板句正则,另收
em-dash 滥用:英文 em-dash(—)插入语判 critical(外部 HIGH 口径);
中文全角破折号「——」是规范用法,豁免(与 ai-tells §6 口径一致)。

扫描面:markup 文件的**可见文本节点**(>text< 形态);<style>/<script>/注释
不扫。也支持 --headline/--cta/--subhead 直接检查给定字符串(CI 与手工用)。

三角度候选淘汰(mechanism/outcome/tension)是写作流程,不进脚本——脚本只拦
已写出的模板句,候选发散由人与 LLM 评审承担。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
依赖: Python 3 标准库。
      HIGH 口径(#32)中文破折号例外为本仓 ai-tells §6 既有口径。
"""
# ---- 模块说明结束 ----
import argparse
import os
import re
import sys

# 扫描的 markup 文件扩展名(可见文案存在的文件)
SCAN_EXTENSIONS_COPY = {
    ".html", ".htm", ".vue", ".svelte", ".astro", ".jsx", ".tsx",
}

SKIP_DIRS_COPY = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}

# 可见文本节点:>text<;不含标签内属性。跨行文本节点由 DOTALL 覆盖。
_TEXT_NODE_RE = re.compile(r">([^<>]+)<", re.DOTALL)
_STYLE_SCRIPT_RE = re.compile(r"<(style|script)\b.*?</\1>", re.DOTALL | re.IGNORECASE)
_COMMENT_RE = re.compile(r"<!--.*?-->|/\*.*?\*/", re.DOTALL)

# 英文 em-dash(单 — 夹在 ASCII 词间);「——」(中文破折号)先剥除再判
_CN_DASH_RE = re.compile(r"——")
_EN_EM_DASH_RE = re.compile(r"[A-Za-z0-9]\s*—\s*[A-Za-z0-9]")

# 10 式模板句(改写自 检测工具 TEMPLATE_PATTERNS,#32;正则 → 规则名 → 释义)
TEMPLATE_PATTERNS = (
    (r"\bthe\s+\w+\s+way\s+to\s+\w+", "the-adj-way-to", "「The [adjective] way to [verb]」"),
    (r"\bbuilt\s+for\s+\w+(?:\s+\w+)?\s+who\s+\w+", "built-for-who", "「Built for [audience] who [verb]」作全部主张"),
    (r"^\s*\w+\s+your\s+\w+\s+in\s+(?:seconds|minutes|hours|no\s+time)", "verb-your-noun-in-time", "「[Verb] your [noun] in [time]」"),
    (r"\bwhere\s+\w+\s+meets\s+\w+", "where-x-meets-y", "「Where [noun] meets [noun]」"),
    (r"^\s*\w+(?:,\s*\w+)+\s+\w+\s*[.!]?\s*$", "adj-adj-noun", "「[Adjective], [adjective] [noun]」当标题"),
    (r"\beverything\s+you\s+need\s+to\s+\w+", "everything-you-need", "「Everything you need to [verb]」"),
    (r"^\s*\w+\s+made\s+\w+\s*[.!]?\s*$", "noun-made-adj", "「[Noun] made [adjective]」"),
    (r"\bsay\s+goodbye\s+to\b", "say-goodbye-to", "「Say goodbye to [problem]」"),
    (r"\byour\s+\w+,?\s+(?:reimagined|reinvented)\b", "noun-reimagined", "「Your [noun], reimagined/reinvented」"),
    (r"\bone\s+platform\s+for\s+all\s+your\b", "one-platform-for-all", "「One platform for all your [noun]」"),
)
_TEMPLATE_RES = [(re.compile(p, re.IGNORECASE | re.MULTILINE), name, desc) for p, name, desc in TEMPLATE_PATTERNS]


def findings_for_text(text, label):
    """对一段文案跑模板句 + em-dash 检查,返回 finding dict 列表。"""
    out = []
    for regex, name, desc in _TEMPLATE_RES:
        m = regex.search(text)
        if m:
            out.append({
                "where": label, "rule": "copy-template/%s" % name,
                "message": "命中模板句 %s —— 换同义词没用,句型本身读作生成;按"
                           " mechanism/outcome/tension 三角度重写(文案原文: %.80s)"
                           % (desc, m.group(0)),
            })
    # 中文破折号「——」豁免后残留的英文 em-dash 插入语
    stripped = _CN_DASH_RE.sub("", text)
    for m in _EN_EM_DASH_RE.finditer(stripped):
        out.append({
            "where": label, "rule": "em-dash",
            "message": "英文 em-dash 插入语(「%.40s」)——改句号/冒号/括号断句;"
                       "中文破折号「——」不受此限(ai-tells §6)" % m.group(0),
        })
    return out


def scan_markup(text, rel_path):
    """扫描 markup 文件的可见文本节点。"""
    cleaned = _STYLE_SCRIPT_RE.sub(" ", text)
    cleaned = _COMMENT_RE.sub(" ", cleaned)
    findings = []
    for m in _TEXT_NODE_RE.finditer(cleaned):
        node = m.group(1).strip()
        if not node:
            continue
        line = cleaned.count("\n", 0, m.start()) + 1
        for f in findings_for_text(node, "%s:%d" % (rel_path, line)):
            findings.append(f)
    return findings


def collect_files_copy(paths):
    files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS_COPY)
                for name in sorted(names):
                    if os.path.splitext(name)[1].lower() in SCAN_EXTENSIONS_COPY:
                        files.append(os.path.join(root, name))
        elif os.path.isfile(path):
            files.append(path)
        else:
            print("check-copy: 路径不存在: %s" % path, file=sys.stderr)
            return None
    return files


def _main_copy(argv=None):
    parser = argparse.ArgumentParser(
        description="句型级反模板文案扫描(10 式模板句 + em-dash critical,中文——豁免)"
    )
    parser.add_argument("paths", nargs="*", help="待扫描的 markup 文件或目录")
    parser.add_argument("--headline", default=None, help="直接检查 hero 标题字符串")
    parser.add_argument("--cta", default=None, help="直接检查 CTA 文案字符串")
    parser.add_argument("--subhead", default=None, help="直接检查副标题字符串")
    args = parser.parse_args(argv)

    findings = []
    scanned = 0
    if args.paths:
        files = collect_files_copy(args.paths)
        if files is None:
            return 2
        for path in files:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError as exc:
                print("check-copy: 读取失败(跳过): %s (%s)" % (path, exc), file=sys.stderr)
                continue
            findings.extend(scan_markup(text, path))
            scanned += 1
    for label, value in (("--headline", args.headline), ("--cta", args.cta), ("--subhead", args.subhead)):
        if value is not None:
            findings.extend(findings_for_text(value, label))
            scanned += 1

    if scanned == 0:
        print("check-copy: 没有可检查目标(无文件且未给 --headline/--cta/--subhead)——没能检查",
              file=sys.stderr)
        return 2

    for f in findings:
        print("%s: [%s] %s" % (f["where"], f["rule"], f["message"]))
    if not findings:
        print("扫描 %d 个目标:未命中模板句与 em-dash 滥用(句型读作具体)。" % scanned)
        return 0
    print("扫描 %d 个目标,命中 %d 处(改写后再扫;三角度候选淘汰见 copy-strategy 文档)" % (scanned, len(findings)))
    return 1


# ============================================================
# 来源节: check-claims.py (子命令: claims)

# ---- 原 check-claims.py 模块说明 ----
"""check-claims —— 公开声明 × 仓库事实对账。

文档里手写的数字会漂移：模板墙加了两个设计语言，SKILL.md 与 README 里的
「12 种」不会自己改。本脚本按 lint-checks.json 的规则把公开声明对账到**唯一

规则类型（lint-checks.json `checks[]`，与 skill_lint.py 共享同一 schema）:

    {"name": "设计语言计数对账", "type": "count-matches",
     "source": "references/templates/INDEX.md",    # 唯一来源（计数的出处）
     "section": "## 设计语言",                      # 可选:只数该标题节内的行
     "row_pattern": "^\\|\\s*\\[",                  # 可选:一"条"匹配一行（默认表行）
     "claim_files": ["SKILL.md", "README.md"],      # 声明出现的位置
     "claim_patterns": ["(\\d+)\\s*种设计语言", "(\\d+)\\s+design languages"],
     "min_claims": 1,                               # 可选:一条声明都抓不到 = 规则形同虚设
     "severity": "WARN"}                            # FAIL / WARN（缺省 FAIL）

    {"name": "禁用夸张语", "type": "forbid-pattern",
     "files": ["README.md", "SKILL.md", "README_EN.md"],
     "pattern": "完美|革命性|颠覆性|行业第一|首屈一指|保证通过",
     "ignore": "禁用夸张语表",                        # 可选:匹配该正则的行豁免
     "severity": "FAIL"}

    {"name": "必现短语", "type": "require-pattern",   # 既有类型,本脚本同样执行
     "file": "README.md", "pattern": "纯 Python 标准库", "min_count": 1}

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
    0 = 看了没问题（warning 级发现不改变退出码）
    1 = 存在 error 级发现（FAIL 级规则命中；--strict 下所有发现都升级为 error）
    2 = 没能检查（没有 lint-checks.json / 没有可执行的声明规则 / 用法错误）
依赖: Python 3 标准库(无第三方依赖)。
denylist)与 .github/workflows/validate-engine.yml, 中文自研实现。
"""
# ---- 模块说明结束 ----

import argparse
import json
import os
import re
import sys

# 规则引擎唯一实现见 maliang_common(仓内 canonical);skill_lint.py 为可 vendored 的
# 自包含孪生副本(兄弟仓 CI 用,不依赖本仓模块)——改引擎语义时两处联动,
# tests/test_maliang_common.py 的孪生一致性测试守护两侧同判。
from maliang_common import (  # noqa: E402
    ENGINE_RULE_TYPES as HANDLED_TYPES,
    engine_run_rule as _engine_run_rule,
)


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("lint-checks.json 顶层必须是对象")
    return data


def run(repo: str, config_path: str | None, fmt: str, strict: bool) -> int:
    repo = os.path.abspath(repo)
    cfg_path = config_path or os.path.join(repo, "lint-checks.json")
    if not os.path.isfile(cfg_path):
        print(f"check-claims: 没能检查——找不到 {cfg_path}（未测量，不得记为通过）。", file=sys.stderr)
        return 2
    try:
        cfg = _load_json(cfg_path)
        rules = [r for r in cfg.get("checks", []) if isinstance(r, dict)]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"check-claims: 配置不可用：{exc}", file=sys.stderr)
        return 2
    if not any(r.get("type", "require-pattern") in HANDLED_TYPES for r in rules):
        print(
            "check-claims: 没能检查——lint-checks.json 没有本脚本可执行的规则类型"
            "（未测量，不得记为通过）。",
            file=sys.stderr,
        )
        return 2

    findings: list[dict] = []
    errors: list[str] = []
    skipped: list[str] = []
    for i, rule in enumerate(rules, 1):
        rtype = rule.get("type", "require-pattern")
        if rtype not in HANDLED_TYPES:
            # 显性跳过(不再静默过滤):该类型由 skill_lint 的 check_repo_rules 执行
            skipped.append(f"checks[{i}]（{rule.get('name', rtype)}）type={rtype}")
            continue
        try:
            findings.extend(_engine_run_rule(repo, rule))
        except (OSError, ValueError) as exc:
            errors.append(f"checks[{i}]（{rule.get('name', rtype)}）配置/目标不可用：{exc}")

    if strict:
        for f in findings:
            f["severity"] = "FAIL"
    hard = [f for f in findings if f["severity"] == "FAIL"]
    soft = [f for f in findings if f["severity"] != "FAIL"]

    if fmt == "json":
        print(json.dumps(
            {"repo": repo, "config": cfg_path, "findings": findings, "errors": errors,
             "summary": {"fail": len(hard), "warn": len(soft)}},
            ensure_ascii=False, indent=2))
    else:
        for err in errors:
            print(f"  ✗ {err}")
        for s in skipped:
            print(f"  ~ 跳过(由 skill_lint 执行): {s}")
        for f in hard:
            print(f"  ✗ [{f['rule']}] {f['message']}")
        for f in soft:
            print(f"  ~ [{f['rule']}] {f['message']}")
        print("")
        print("=" * 40)
        if errors:
            print(f"对账结果: {len(errors)} 条规则无法执行（按未测量处理）")
        if hard or soft:
            print(f"对账结果: {len(hard)} error, {len(soft)} warning")
        if not errors and not findings:
            print("对账结果: 声明与仓库事实一致（计数唯一来源 + 必现短语 + 禁用语表）")
    if hard:
        return 1
    return 2 if errors else 0



    parser = argparse.ArgumentParser(
        prog="check-claims.py",
        description="公开声明 × 仓库事实对账：计数对账（唯源 INDEX）+ 必现短语 + 禁用语表。",
        epilog="规则 schema 见脚本头注；退出码三态见 scripts/EXIT-CODES.md。示例:\n"
        "  python3 scripts/check-claims.py .\n"
        "  python3 scripts/check-claims.py . --format json --strict",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("repo", nargs="?", default=".", help="仓库根（默认当前目录）")
    parser.add_argument("--lint-checks", default=None, help="lint-checks.json 路径（默认 <repo>/lint-checks.json）")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式（默认 text）")
    parser.add_argument("--strict", action="store_true", help="把全部发现升级为 error 级")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return run(args.repo, args.lint_checks, args.format, args.strict)


# ============================================================
# 来源节: check-structure-history.py (子命令: structure-history)

# ---- 原 check-structure-history.py 模块说明 ----
"""轮换与盖章机械化核验(G41/G42 脚本层)。

读项目构建日志 `.maliang/build-log.json`(JSON 数组,新条目在前;契约见
references/templates/variation-engine.md「构建日志」节),做三查:

  1. immediate repeat  当前构建与日志最近一条同轴同值 —— reuse is only OK
                       if you changed a variation knob and said so(换旋钮并声明)。
  2. hot axis          最近 --window 条构建逐轴聚合,当前取值占比 ≥0.6 即为
                       「热轴默认」——除非 brief 明确要求,换掉并说明。
  3. stamp lies        --stamp 给出时,解析页面盖章 `/* maliang · mode=... · A=...`
                       的坐标,与 --current 声明的 stamp 字段逐键对账;键集或值
                       不一致 = 章与声明不符(G41,章说谎比缺章严重)。

七轴键集(theme/background/typography/hero/section/signature/motion)以
variation-engine.md 为唯一词表;本脚本只做机械一致性,轴值优劣不由脚本判断。

hot axis 思想stamp-lies 与 设计基准库(#19)同门合并(裁决见
.absorb-external/ui-benchmark-batch2-findings.md #31)。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        build-log 缺失或非法 = UNMEASURED → 2(G42:不得记通过)。
依赖: Python 3 标准库。
"""
# ---- 模块说明结束 ----
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# 七轴键集(variation-engine.md「构建日志」契约;新条目在前)
AXES_FIELDS = ("theme", "background", "typography", "hero", "section", "signature", "motion")

# 轴是「热」的占比阈值(外部原口径 0.6)
HOT_THRESHOLD = 0.6
# 窗口不足此数不做热轴判定(样本太少没有统计意义)
MIN_WINDOW_FOR_HOT_CHECK = 3

# 盖章坐标:`/* maliang · mode=Experience · A=deep-dark · B=tactile-texture ... */
_STAMP_MODE_RE = re.compile(r"maliang\s*·\s*mode=([^\s·*]+)")
_STAMP_AXIS_RE = re.compile(r"\b([A-G])=([^·\n*]+)")


def load_log(path):
    """读构建日志;缺失/非法返回 (None, 原因)——调用方按 UNMEASURED 处理。"""
    if not path.exists():
        return None, "构建日志不存在: %s" % path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, "构建日志不可解析: %s (%s)" % (path, exc)
    if not isinstance(data, list):
        return None, "构建日志必须是 JSON 数组(新条目在前): %s" % path
    return data, None


def check_immediate_repeat(current_axes, previous_axes):
    """当前构建逐轴对比日志最近一条;同轴同值即立即重复。"""
    problems = []
    for field in AXES_FIELDS:
        cur, prev = current_axes.get(field), previous_axes.get(field)
        if cur and prev and cur == prev:
            problems.append(
                "%s 与最近一次构建重复('%s')——reuse is only OK if you changed "
                "a variation knob and said so(换旋钮并声明)" % (field, cur)
            )
    return problems


def check_hot_axis(current_axes, window, window_size):
    """逐轴统计最近窗口的取值分布;当前取值占比 ≥0.6 即热轴告警。

    window 是 build-log 条目(新条目在前),轴值在条目的 axes 子对象里。
    """
    problems = []
    if len(window) < MIN_WINDOW_FOR_HOT_CHECK:
        return problems
    for field in AXES_FIELDS:
        cur = current_axes.get(field)
        if not cur:
            continue
        counts = Counter()
        for e in window:
            if not isinstance(e, dict):
                continue
            axes = e.get("axes")
            if not isinstance(axes, dict):
                continue
            val = axes.get(field)
            if val:
                counts[val] += 1
        total = sum(counts.values())
        if total == 0:
            continue
        share = counts.get(cur, 0) / total
        if share >= HOT_THRESHOLD:
            problems.append(
                "%s '%s' 占最近 %d 条构建的 %d/%d —— it's the hot default right now;"
                "除非 brief 明确要求,换掉并说明" % (field, cur, window_size, counts[cur], total)
            )
    return problems


def parse_stamp(text):
    """提取盖章坐标,返回 (mode, {A:..~G:..});无盖章返回 (None, {})。"""
    mode = None
    m = _STAMP_MODE_RE.search(text)
    if m:
        mode = m.group(1).strip()
    axes = {}
    for m in _STAMP_AXIS_RE.finditer(text):
        axes[m.group(1)] = m.group(2).strip()
    return mode, axes


def check_stamp_lies(stamp_text, current):
    """盖章与当前构建声明逐键对账;不一致即 stamp lies(G41)。"""
    declared = current.get("stamp")
    if not isinstance(declared, dict):
        return [], []
    problems = []
    stamp_mode, stamp_axes = parse_stamp(stamp_text)
    if stamp_mode is None and not stamp_axes:
        problems.append("页面里没有找到 `/* maliang · ... */` 盖章——缺章(major;G41)")
        return problems, []
    declared_mode = declared.get("mode")
    if declared_mode and stamp_mode and stamp_mode != declared_mode:
        problems.append(
            "盖章 mode=%s 与声明 mode=%s 不符——stamp lies(G41;改章或改页面,二者取实)"
            % (stamp_mode, declared_mode)
        )
    for key, want in sorted(declared.items()):
        if key == "mode":
            continue
        got = stamp_axes.get(key)
        if got is None:
            problems.append("盖章缺坐标 %s(声明为 '%s')——章与实物不符(G41)" % (key, want))
        elif got != str(want):
            problems.append(
                "盖章 %s=%s 与声明 '%s' 不符——stamp lies(G41;改章或改页面,二者取实)"
                % (key, got, want)
            )
    return problems, [k for k in stamp_axes if k not in declared]


def _main_structure_history(argv=None):
    parser = argparse.ArgumentParser(
        description="轮换与盖章机械化核验(G41/G42):immediate repeat + hot axis(0.6) + stamp lies"
    )
    parser.add_argument(
        "--current", required=True,
        help="本次构建声明 JSON 文件:{page, axes:{七轴}, stamp:{mode, A..G}(可选)}",
    )
    parser.add_argument(
        "--log", default=".maliang/build-log.json",
        help="构建日志路径(默认 .maliang/build-log.json;缺失 = UNMEASURED/exit 2)",
    )
    parser.add_argument(
        "--stamp", default=None,
        help="含 `/* maliang · ... */` 盖章的 HTML/CSS 文件(给出时做 stamp-lies 对账)",
    )
    parser.add_argument("--window", type=int, default=5, help="热轴统计窗口条数(默认 5)")
    args = parser.parse_args(argv)

    current_path = Path(args.current)
    if not current_path.exists():
        print("check-structure-history: --current 文件不存在: %s" % current_path, file=sys.stderr)
        return 2
    try:
        current = json.loads(current_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print("check-structure-history: --current 不可读: %s" % exc, file=sys.stderr)
        return 2
    if not isinstance(current, dict) or not isinstance(current.get("axes"), dict):
        print("check-structure-history: --current 须为 {page, axes:{...}} 形态", file=sys.stderr)
        return 2
    current_axes = current["axes"]

    log, reason = load_log(Path(args.log))
    if log is None:
        print("check-structure-history: UNMEASURED —— %s(G42:日志缺失不得记通过)" % reason,
              file=sys.stderr)
        return 2

    problems = []
    if log:
        first = log[0]
        if isinstance(first, dict) and isinstance(first.get("axes"), dict):
            problems.extend(check_immediate_repeat(current_axes, first["axes"]))
    window = [e for e in log[: max(0, args.window)] if isinstance(e, dict)]
    problems.extend(check_hot_axis(current_axes, window, len(window)))

    stamp_extra = []
    if args.stamp:
        stamp_path = Path(args.stamp)
        if not stamp_path.exists():
            print("check-structure-history: --stamp 文件不存在: %s" % stamp_path, file=sys.stderr)
            return 2
        stamp_text = stamp_path.read_text(encoding="utf-8", errors="replace")
        stamp_problems, stamp_extra = check_stamp_lies(stamp_text, current)
        problems.extend(stamp_problems)

    checked = "历史 %d 条(窗口 %d)" % (len(log), len(window))
    if not problems:
        print("结构核验通过(%s):取值读作轮换%s" % (checked, ";盖章对账一致" if args.stamp else ""))
        if stamp_extra:
            print("  提示: 盖章含声明外的坐标 %s(信息性,不影响退出码)" % stamp_extra)
        return 0

    print("轮换/盖章违例(%s):" % checked)
    for p in problems:
        print("  - %s" % p)
    print("\n这是机械核验不是品味判断——重复可以是 brief 要的正确选择,但必须说明理由并换 knob。")
    return 1


# ============================================================
# 来源节: source-fingerprint.py (子命令: fingerprint)

# ---- 原 source-fingerprint.py 模块说明 ----
"""redesign 重审计源码指纹基线(G30 脚本层):廉价新鲜度检查,不读内容进上下文。

重跑 redesign 时先判断「用户的仓库变没变」:逐文件 SHA-256 指纹基线,
对比得出 changed/added/removed——全程只算哈希,**不把文件内容读进模型
上下文**(外部原口径:Hashing is a cheap freshness check)。

信任边界(改写自 方法库 RESUME.md「Trust boundary」,#30,
- 仅仓库内路径:resolve 后必须落在仓库根内,拒绝绝对路径与 ../ 逃逸;
  - 拒涉密文件: .env* / .git/ / credentials* / 私钥证书(*.pem、id_rsa*、
    *.key)/ 任何疑似 secret store;
  - 键集精确相等:check 模式要求基线 files 键集与重算键集可逐键对账,
    基线含仓外/涉密/重复路径 → 按不可信缓存拒绝(退出 2),不静默清选;
  - 原子写:临时文件 + os.replace,中断不留半截基线。

diff 归约入口:diff 子命令对**单个变更路径**运行 `git diff HEAD -- <path>`
(参数列表传递,路径加引号限定,绝不裸跑全仓 diff);git 不可得时明说并退 2。
归约成「有意义 UI delta」是模型/人的活——本脚本只输出统计,并且明确:
**不得以变更行数或整文件哈希推断重要性**;指纹不匹配单独不强制冷路由。

用法:
    python3 scripts/source-fingerprint.py create <repo> [--output PATH]
    python3 scripts/source-fingerprint.py check  <repo> --baseline PATH
    python3 scripts/source-fingerprint.py diff   <repo> --baseline PATH --path <rel>

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题(有变更) / 2=没能检查;#16)。
依赖: Python 3 标准库(git 仅 diff 子命令需要)。
"""
# ---- 模块说明结束 ----
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

SCHEMA_VERSION = 1

# 目录排除(依赖/构建产物/版本库自身)
EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".next", "__pycache__",
                ".venv", "venv", ".maliang", "specmark"}

# 涉密文件签名(信任边界;命中即拒绝入基线/拒绝信任基线)
SECRET_FILE_RE = re.compile(
    r"(^|/)(\.env[^/]*|credentials[^/]*|id_rsa[^/]*|id_ed25519[^/]*|id_ecdsa[^/]*"
    r"|id_dsa[^/]*|\.git-credentials|\.netrc|\.npmrc|\.pypirc|.*\.pem|.*\.key"
    r"|.*\.p12|.*\.pfx|secrets?\.[a-z]+)$",
    re.IGNORECASE,
)


def is_safe_rel_path(repo_root, rel):
    """仓库内相对路径信任校验:仓内、非涉密、非目录穿越。"""
    if os.path.isabs(rel) or ".." in rel.split(os.sep) or rel.startswith("~"):
        return False, "路径逃逸/绝对路径: %s" % rel
    if ".git" in rel.replace(os.sep, "/").split("/"):
        return False, "版本库内部路径(.git): %s" % rel
    if SECRET_FILE_RE.search(rel.replace(os.sep, "/")):
        return False, "疑似涉密文件(信任边界拒绝): %s" % rel
    full = os.path.normpath(os.path.join(repo_root, rel))
    if not (full == repo_root or full.startswith(repo_root + os.sep)):
        return False, "解析后落在仓库外: %s" % rel
    return True, ""


def walk_repo(repo_root):
    """遍历仓库文件,返回相对路径列表(排除目录与涉密文件)。"""
    out = []
    for root, dirs, names in os.walk(repo_root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("."))
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(root, name), repo_root)
            safe, _ = is_safe_rel_path(repo_root, rel)
            if safe:
                out.append(rel)
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def build_fingerprints(repo_root):
    """逐文件哈希;单个文件读不了 = 显性报错(不算基线)。"""
    files = {}
    for rel in walk_repo(repo_root):
        full = os.path.join(repo_root, rel)
        if not os.path.isfile(full) or os.path.islink(full):
            continue
        try:
            files[rel.replace(os.sep, "/")] = sha256_file(full)
        except OSError as exc:
            raise RuntimeError("无法读取 %s: %s" % (rel, exc))
    return files


def atomic_write_json(path, payload):
    """临时文件 + os.replace 原子写(中断不留半截基线)。"""
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def load_baseline(path, repo_root):
    """读基线并做信任校验;不可信 → 抛 UntrustedBaseline(退出 2)。"""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise UntrustedBaseline("基线不可读: %s" % exc)
    if not isinstance(data, dict) or data.get("schemaVersion") != SCHEMA_VERSION:
        raise UntrustedBaseline("基线 schemaVersion 缺失或不符(按不可信缓存拒绝)")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise UntrustedBaseline("基线缺 files 映射(按不可信缓存拒绝)")
    for rel in files:
        safe, why = is_safe_rel_path(repo_root, rel)
        if not safe:
            raise UntrustedBaseline("基线内路径不可信: %s" % why)
        if not isinstance(files[rel], str) or len(files[rel]) != 64:
            raise UntrustedBaseline("基线内指纹非法: %s" % rel)
    return data, files


class UntrustedBaseline(Exception):
    """基线按不可信缓存拒绝(退出 2,不静默清选)。"""


def cmd_create(args):
    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(repo_root):
        print("source-fingerprint: 仓库目录不存在: %s" % repo_root, file=sys.stderr)
        return 2
    try:
        files = build_fingerprints(repo_root)
    except RuntimeError as exc:
        print("source-fingerprint: %s" % exc, file=sys.stderr)
        return 2
    payload = {
        "schemaVersion": SCHEMA_VERSION,
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "repo": os.path.basename(repo_root),
        "files": files,
    }
    output = args.output or os.path.join(repo_root, ".maliang", "source-fingerprints.json")
    atomic_write_json(output, payload)
    print("基线已写入 %s(%d 个文件;哈希只做新鲜度,不读内容进上下文)" % (output, len(files)))
    return 0


def cmd_check(args):
    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(repo_root):
        print("source-fingerprint: 仓库目录不存在: %s" % repo_root, file=sys.stderr)
        return 2
    try:
        _meta, baseline_files = load_baseline(args.baseline, repo_root)
    except UntrustedBaseline as exc:
        print("source-fingerprint: UNTRUSTED —— %s(重建基线后再跑)" % exc, file=sys.stderr)
        return 2
    try:
        current = build_fingerprints(repo_root)
    except RuntimeError as exc:
        print("source-fingerprint: %s" % exc, file=sys.stderr)
        return 2

    changed = sorted(f for f in current if f in baseline_files and current[f] != baseline_files[f])
    added = sorted(f for f in current if f not in baseline_files)
    removed = sorted(f for f in baseline_files if f not in current)
    for f in changed:
        print("changed: %s" % f)
    for f in added:
        print("added:   %s" % f)
    for f in removed:
        print("removed: %s" % f)
    if not (changed or added or removed):
        print("指纹一致(%d 个文件):自基线以来仓库未变。" % len(current))
        return 0
    print("指纹差异:%d changed / %d added / %d removed(哈希只证变化,不证重要性;"
          "不得以变更行数或整文件哈希推断重要性)" % (len(changed), len(added), len(removed)))
    return 1


def cmd_diff(args):
    repo_root = os.path.abspath(args.repo)
    rel = args.path.replace("/", os.sep)
    safe, why = is_safe_rel_path(repo_root, args.path)
    if not safe:
        print("source-fingerprint: %s" % why, file=sys.stderr)
        return 2
    if not os.path.isfile(os.path.join(repo_root, rel)):
        print("source-fingerprint: 文件不存在: %s" % args.path, file=sys.stderr)
        return 2
    try:
        _meta, baseline_files = load_baseline(args.baseline, repo_root)
    except UntrustedBaseline as exc:
        print("source-fingerprint: UNTRUSTED —— %s" % exc, file=sys.stderr)
        return 2
    full_path = os.path.join(repo_root, rel)
    if os.path.islink(full_path):
        print("source-fingerprint: UNMEASURED —— 符号链接不入基线(与 create 口径一致)", file=sys.stderr)
        return 2
    unchanged = baseline_files.get(args.path.replace(os.sep, "/")) == sha256_file(os.path.join(repo_root, rel))
    if unchanged:
        print("%s 与基线一致:无需 diff(基线即 HEAD 之外的独立新鲜度凭证)。" % args.path)
        return 0
    try:
        proc = subprocess.run(
            ["git", "-C", repo_root, "diff", "HEAD", "--", args.path],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("source-fingerprint: git 不可得(%s)——文件已变,但精确 delta 不可得;"
              "按哈希刷新处理,不要编造变更摘要。" % exc, file=sys.stderr)
        return 2
    if proc.returncode != 0:
        print("source-fingerprint: git diff 失败: %s——文件已变,但精确 delta 不可得,"
              "按哈希刷新处理。" % proc.stderr.strip(), file=sys.stderr)
        return 2
    sys.stdout.write(proc.stdout)
    if not proc.stdout.strip():
        print("(git diff 为空:文件相对 HEAD 无未提交改动;指纹差异来自已提交的历史)"
              "——delta 不可得时明说,不得以行数推断重要性。")
    return 0


def _main_fingerprint(argv=None):
    parser = argparse.ArgumentParser(
        description="源码 SHA-256 指纹基线(create/check/diff;信任边界+原子写;不读内容进上下文)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="建立指纹基线")
    p_create.add_argument("repo")
    p_create.add_argument("--output", default=None, help="基线输出路径(默认 <repo>/.maliang/source-fingerprints.json)")

    p_check = sub.add_parser("check", help="对比基线,输出 changed/added/removed")
    p_check.add_argument("repo")
    p_check.add_argument("--baseline", required=True)

    p_diff = sub.add_parser("diff", help="对单个变更路径跑 git diff HEAD -- <path>(引号限定)")
    p_diff.add_argument("repo")
    p_diff.add_argument("--baseline", required=True)
    p_diff.add_argument("--path", required=True, help="仓库内相对路径")

    args = parser.parse_args(argv)
    return {"create": cmd_create, "check": cmd_check, "diff": cmd_diff}[args.cmd](args)


# ============================================================
# 来源节: evidence-check.py (子命令: evidence)

# ---- 原 evidence-check.py 模块说明 ----
"""evidence-check —— 取证契约校验（截图证据齐套性检查）。

"看一眼"与"取证"是两种用途：看一眼只截当前屏；取证一次取齐，只在送评审前与
交付前做。本脚本校验一次取证产出的 `report.json` 是否齐套——缺项不是"跳过"，
是把结论推到 `unverified`（未验证不得记为通过、disposition 不得为 deliver）。

report.json 契约（maliang-evidence/1，纯 JSON，路径相对 report.json 所在目录）:

    {
      "schema": "maliang-evidence/1",
      "capturedAt": "2026-10-12T10:00:00+08:00",
      "pages": [
        {
          "page": "preview_home_iphone15.html",
          "viewport": "390x844",
          "sheet": "shots/sheet-home.png",          # 并排图（≥2 个状态时必填）
          "motion": "probe/home-motion.json",       # 动效探测（必填）
          "recording": "record/home.mp4",           # 录屏（必填）
          "states": [
            {
              "state": "idle",
              "shot": "shots/home-idle.png",        # 状态图（必填）
              "shot2x": "shots/home-idle@2x.png",   # 2x 图（必填）
              "masked": "shots/home-idle-masked.png"# 遮字图（必填）
            }
          ]
        }
      ]
    }

规则:
  - 每页每状态必齐 状态图 / 2x 图 / 遮字图；每页必齐 动效探测 / 录屏；
    多状态页必齐 并排图（单状态页无并排图可言，记为 n/a 而非缺项）；
  - 任一被引用文件不存在或为空 → 该槽位计缺项（空文件不是证据）；
  - 同一文件被多个槽位复用 → 计问题（2x 图与状态图同文件、并排图与状态图同
    文件都是假齐套）；
  - 条目带 `failed: true` / `skipped: true` → 计缺项并在清单里转录原因；
  - 空 WebGL 截图不当证据（内容级别判断超出静态校验能力，见 preview.md 取证契约节）。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
  0 = 齐套；1 = 有缺项/问题；2 = 没能检查（找不到 report.json / 用法错误）。
依赖: Python 3 标准库(无第三方依赖)。
"""
# ---- 模块说明结束 ----

import argparse
import json
import os
import sys

SCHEMA_NAME = "maliang-evidence/1"
REQUIRED_REPORT_FILES = ("report.json",)
STATE_SLOTS = (("shot", "状态图"), ("shot2x", "2x 图"), ("masked", "遮字图"))
PAGE_SLOTS = (("motion", "动效探测"), ("recording", "录屏"))


def _slot_path(value) -> str | None:
    """槽位取值：字符串路径，或 {"file": path} 形态；其余视为未提供。"""
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("file", "path"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return None


def _find_reports(target: str) -> list[str]:
    """目标为 report.json 文件，或含 report.json 的目录（递归）。"""
    if os.path.isfile(target):
        return [os.path.abspath(target)]
    if os.path.isdir(target):
        found = []
        for dirpath, _, filenames in os.walk(target):
            for fn in filenames:
                if fn in REQUIRED_REPORT_FILES:
                    found.append(os.path.abspath(os.path.join(dirpath, fn)))
        return sorted(found)
    return []


def check_report(report_path: str) -> dict:
    """校验单个 report.json；返回 {problems, missing, notes, pages}。"""
    problems: list[str] = []
    missing: list[str] = []
    notes: list[str] = []
    base = os.path.dirname(os.path.abspath(report_path))
    with open(report_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError(
            "report.json 顶层必须是对象（含 schema 与 pages[]）；"
            "扁平条目数组不是本契约的形态"
        )
    schema = raw.get("schema")
    if schema != SCHEMA_NAME:
        problems.append(f"schema={schema!r} 不是 {SCHEMA_NAME!r}（契约版本不符）")
    pages = raw.get("pages")
    if not isinstance(pages, list) or not pages:
        problems.append("pages[] 缺省或为空（没有任何页面的取证不成立）")
        return {"problems": problems, "missing": missing, "notes": notes, "pages": 0}
    seen_paths: dict[str, str] = {}

    def require_file(rel: str, slot_label: str, where: str) -> None:
        abs_path = os.path.normpath(os.path.join(base, rel))
        if not os.path.isfile(abs_path):
            missing.append(f"{where} 缺 {slot_label}: {rel}（文件不存在）")
            return
        if os.path.getsize(abs_path) == 0:
            missing.append(f"{where} 缺 {slot_label}: {rel}（文件为空，空文件不是证据）")
            return
        owner = seen_paths.get(abs_path)
        if owner:
            problems.append(
                f"{where} 的 {slot_label} 与 {owner} 复用同一文件 {rel}（假齐套）"
            )
        else:
            seen_paths[abs_path] = f"{where} {slot_label}"

    for index, page in enumerate(pages, 1):
        if not isinstance(page, dict):
            problems.append(f"第 {index} 页不是对象")
            continue
        page_name = page.get("page") or page.get("id") or f"pages[{index}]"
        where_page = str(page_name)
        states = page.get("states")
        if not isinstance(states, list) or not states:
            problems.append(f"{where_page}: states[] 缺省或为空")
            states = []
        for slot, label in PAGE_SLOTS:
            rel = _slot_path(page.get(slot))
            if rel:
                require_file(rel, label, where_page)
            else:
                missing.append(f"{where_page} 缺 {label}（{slot}）")
        if len(states) >= 2:
            rel = _slot_path(page.get("sheet"))
            if rel:
                require_file(rel, "并排图", where_page)
            else:
                missing.append(f"{where_page} 缺 并排图（sheet）")
        elif "sheet" not in page:
            notes.append(f"{where_page}: 单状态页无并排图可查（n/a）")
        for sindex, state in enumerate(states, 1):
            if not isinstance(state, dict):
                problems.append(f"{where_page}: 第 {sindex} 个状态不是对象")
                continue
            state_name = state.get("state") or state.get("name") or f"states[{sindex}]"
            where = f"{where_page} · {state_name}"
            if state.get("failed") is True or state.get("skipped") is True:
                reason = state.get("reason") or state.get("error") or "条目自报失败/跳过"
                missing.append(f"{where}: 条目未完成（{reason}）")
                continue
            for slot, label in STATE_SLOTS:
                rel = _slot_path(state.get(slot))
                if rel:
                    require_file(rel, label, where)
                else:
                    missing.append(f"{where} 缺 {label}（{slot}）")
    return {"problems": problems, "missing": missing, "notes": notes, "pages": len(pages)}


def run_evidence(target: str, fmt: str) -> int:
    reports = _find_reports(target)
    if not reports:
        print(
            f"evidence-check: 没能检查——{target} 下找不到 report.json（未测量，不得记为通过）。",
            file=sys.stderr,
        )
        return 2
    total_missing = 0
    total_problems = 0
    results = []
    for report in reports:
        try:
            result = check_report(report)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"[FAIL] {report}: 报告不可解析或非法：{exc}", file=sys.stderr)
            total_problems += 1
            results.append({"report": report, "problems": [str(exc)], "missing": []})
            continue
        total_missing += len(result["missing"])
        total_problems += len(result["problems"])
        results.append({"report": report, **result})
        if fmt == "text":
            status = "FAIL" if (result["missing"] or result["problems"]) else "PASS"
            print(f"[{status}] {report}  ({result['pages']} 页)")
            for item in result["problems"]:
                print(f"  ✗ {item}")
            for item in result["missing"]:
                print(f"  ✗ {item}")
            for item in result["notes"]:
                print(f"  · {item}")
    if fmt == "json":
        print(json.dumps(
            {"reports": results, "missing": total_missing, "problems": total_problems},
            ensure_ascii=False, indent=2))
    else:
        print("")
        print("=" * 40)
        if total_missing or total_problems:
            print(
                f"取证结果: {total_missing} 项缺件, {total_problems} 项问题——"
                "缺项按 unverified 处理（未验证不得记为通过，disposition 不得为 deliver）；"
                "重取后重跑。"
            )
        else:
            print("取证结果: 齐套（状态图/2x/遮字/并排/动效探测/录屏）")
    return 1 if (total_missing or total_problems) else 0


def _main_claims(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="check-claims.py",
        description="公开声明 × 仓库事实对账：计数对账（唯源 INDEX）+ 必现短语 + 禁用语表。",
        epilog="规则 schema 见脚本头注；退出码三态见 scripts/EXIT-CODES.md。示例:\n"
        "  python3 scripts/check-claims.py .\n"
        "  python3 scripts/check-claims.py . --format json --strict",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("repo", nargs="?", default=".", help="仓库根（默认当前目录）")
    parser.add_argument("--lint-checks", default=None, help="lint-checks.json 路径（默认 <repo>/lint-checks.json）")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式（默认 text）")
    parser.add_argument("--strict", action="store_true", help="把全部发现升级为 error 级")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return run(args.repo, args.lint_checks, args.format, args.strict)


# ============================================================
# 来源节: check-structure-history.py (子命令: structure-history)

# ---- 原 check-structure-history.py 模块说明 ----
"""轮换与盖章机械化核验(G41/G42 脚本层)。

读项目构建日志 `.maliang/build-log.json`(JSON 数组,新条目在前;契约见
references/templates/variation-engine.md「构建日志」节),做三查:

  1. immediate repeat  当前构建与日志最近一条同轴同值 —— reuse is only OK
                       if you changed a variation knob and said so(换旋钮并声明)。
  2. hot axis          最近 --window 条构建逐轴聚合,当前取值占比 ≥0.6 即为
                       「热轴默认」——除非 brief 明确要求,换掉并说明。
  3. stamp lies        --stamp 给出时,解析页面盖章 `/* maliang · mode=... · A=...`
                       的坐标,与 --current 声明的 stamp 字段逐键对账;键集或值
                       不一致 = 章与声明不符(G41,章说谎比缺章严重)。

七轴键集(theme/background/typography/hero/section/signature/motion)以
variation-engine.md 为唯一词表;本脚本只做机械一致性,轴值优劣不由脚本判断。

hot axis 思想stamp-lies 与 设计基准库(#19)同门合并(裁决见
.absorb-external/ui-benchmark-batch2-findings.md #31)。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        build-log 缺失或非法 = UNMEASURED → 2(G42:不得记通过)。
依赖: Python 3 标准库。
"""
# ---- 模块说明结束 ----
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# 七轴键集(variation-engine.md「构建日志」契约;新条目在前)
AXES_FIELDS = ("theme", "background", "typography", "hero", "section", "signature", "motion")

# 轴是「热」的占比阈值(外部原口径 0.6)
HOT_THRESHOLD = 0.6
# 窗口不足此数不做热轴判定(样本太少没有统计意义)
MIN_WINDOW_FOR_HOT_CHECK = 3

# 盖章坐标:`/* maliang · mode=Experience · A=deep-dark · B=tactile-texture ... */
_STAMP_MODE_RE = re.compile(r"maliang\s*·\s*mode=([^\s·*]+)")
_STAMP_AXIS_RE = re.compile(r"\b([A-G])=([^·\n*]+)")


def load_log(path):
    """读构建日志;缺失/非法返回 (None, 原因)——调用方按 UNMEASURED 处理。"""
    if not path.exists():
        return None, "构建日志不存在: %s" % path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, "构建日志不可解析: %s (%s)" % (path, exc)
    if not isinstance(data, list):
        return None, "构建日志必须是 JSON 数组(新条目在前): %s" % path
    return data, None


def check_immediate_repeat(current_axes, previous_axes):
    """当前构建逐轴对比日志最近一条;同轴同值即立即重复。"""
    problems = []
    for field in AXES_FIELDS:
        cur, prev = current_axes.get(field), previous_axes.get(field)
        if cur and prev and cur == prev:
            problems.append(
                "%s 与最近一次构建重复('%s')——reuse is only OK if you changed "
                "a variation knob and said so(换旋钮并声明)" % (field, cur)
            )
    return problems


def check_hot_axis(current_axes, window, window_size):
    """逐轴统计最近窗口的取值分布;当前取值占比 ≥0.6 即热轴告警。

    window 是 build-log 条目(新条目在前),轴值在条目的 axes 子对象里。
    """
    problems = []
    if len(window) < MIN_WINDOW_FOR_HOT_CHECK:
        return problems
    for field in AXES_FIELDS:
        cur = current_axes.get(field)
        if not cur:
            continue
        counts = Counter()
        for e in window:
            if not isinstance(e, dict):
                continue
            axes = e.get("axes")
            if not isinstance(axes, dict):
                continue
            val = axes.get(field)
            if val:
                counts[val] += 1
        total = sum(counts.values())
        if total == 0:
            continue
        share = counts.get(cur, 0) / total
        if share >= HOT_THRESHOLD:
            problems.append(
                "%s '%s' 占最近 %d 条构建的 %d/%d —— it's the hot default right now;"
                "除非 brief 明确要求,换掉并说明" % (field, cur, window_size, counts[cur], total)
            )
    return problems


def parse_stamp(text):
    """提取盖章坐标,返回 (mode, {A:..~G:..});无盖章返回 (None, {})。"""
    mode = None
    m = _STAMP_MODE_RE.search(text)
    if m:
        mode = m.group(1).strip()
    axes = {}
    for m in _STAMP_AXIS_RE.finditer(text):
        axes[m.group(1)] = m.group(2).strip()
    return mode, axes


def check_stamp_lies(stamp_text, current):
    """盖章与当前构建声明逐键对账;不一致即 stamp lies(G41)。"""
    declared = current.get("stamp")
    if not isinstance(declared, dict):
        return [], []
    problems = []
    stamp_mode, stamp_axes = parse_stamp(stamp_text)
    if stamp_mode is None and not stamp_axes:
        problems.append("页面里没有找到 `/* maliang · ... */` 盖章——缺章(major;G41)")
        return problems, []
    declared_mode = declared.get("mode")
    if declared_mode and stamp_mode and stamp_mode != declared_mode:
        problems.append(
            "盖章 mode=%s 与声明 mode=%s 不符——stamp lies(G41;改章或改页面,二者取实)"
            % (stamp_mode, declared_mode)
        )
    for key, want in sorted(declared.items()):
        if key == "mode":
            continue
        got = stamp_axes.get(key)
        if got is None:
            problems.append("盖章缺坐标 %s(声明为 '%s')——章与实物不符(G41)" % (key, want))
        elif got != str(want):
            problems.append(
                "盖章 %s=%s 与声明 '%s' 不符——stamp lies(G41;改章或改页面,二者取实)"
                % (key, got, want)
            )
    return problems, [k for k in stamp_axes if k not in declared]


def _main_structure_history(argv=None):
    parser = argparse.ArgumentParser(
        description="轮换与盖章机械化核验(G41/G42):immediate repeat + hot axis(0.6) + stamp lies"
    )
    parser.add_argument(
        "--current", required=True,
        help="本次构建声明 JSON 文件:{page, axes:{七轴}, stamp:{mode, A..G}(可选)}",
    )
    parser.add_argument(
        "--log", default=".maliang/build-log.json",
        help="构建日志路径(默认 .maliang/build-log.json;缺失 = UNMEASURED/exit 2)",
    )
    parser.add_argument(
        "--stamp", default=None,
        help="含 `/* maliang · ... */` 盖章的 HTML/CSS 文件(给出时做 stamp-lies 对账)",
    )
    parser.add_argument("--window", type=int, default=5, help="热轴统计窗口条数(默认 5)")
    args = parser.parse_args(argv)

    current_path = Path(args.current)
    if not current_path.exists():
        print("check-structure-history: --current 文件不存在: %s" % current_path, file=sys.stderr)
        return 2
    try:
        current = json.loads(current_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print("check-structure-history: --current 不可读: %s" % exc, file=sys.stderr)
        return 2
    if not isinstance(current, dict) or not isinstance(current.get("axes"), dict):
        print("check-structure-history: --current 须为 {page, axes:{...}} 形态", file=sys.stderr)
        return 2
    current_axes = current["axes"]

    log, reason = load_log(Path(args.log))
    if log is None:
        print("check-structure-history: UNMEASURED —— %s(G42:日志缺失不得记通过)" % reason,
              file=sys.stderr)
        return 2

    problems = []
    if log:
        first = log[0]
        if isinstance(first, dict) and isinstance(first.get("axes"), dict):
            problems.extend(check_immediate_repeat(current_axes, first["axes"]))
    window = [e for e in log[: max(0, args.window)] if isinstance(e, dict)]
    problems.extend(check_hot_axis(current_axes, window, len(window)))

    stamp_extra = []
    if args.stamp:
        stamp_path = Path(args.stamp)
        if not stamp_path.exists():
            print("check-structure-history: --stamp 文件不存在: %s" % stamp_path, file=sys.stderr)
            return 2
        stamp_text = stamp_path.read_text(encoding="utf-8", errors="replace")
        stamp_problems, stamp_extra = check_stamp_lies(stamp_text, current)
        problems.extend(stamp_problems)

    checked = "历史 %d 条(窗口 %d)" % (len(log), len(window))
    if not problems:
        print("结构核验通过(%s):取值读作轮换%s" % (checked, ";盖章对账一致" if args.stamp else ""))
        if stamp_extra:
            print("  提示: 盖章含声明外的坐标 %s(信息性,不影响退出码)" % stamp_extra)
        return 0

    print("轮换/盖章违例(%s):" % checked)
    for p in problems:
        print("  - %s" % p)
    print("\n这是机械核验不是品味判断——重复可以是 brief 要的正确选择,但必须说明理由并换 knob。")
    return 1


# ============================================================
# 来源节: source-fingerprint.py (子命令: fingerprint)

# ---- 原 source-fingerprint.py 模块说明 ----
"""redesign 重审计源码指纹基线(G30 脚本层):廉价新鲜度检查,不读内容进上下文。

重跑 redesign 时先判断「用户的仓库变没变」:逐文件 SHA-256 指纹基线,
对比得出 changed/added/removed——全程只算哈希,**不把文件内容读进模型
上下文**(外部原口径:Hashing is a cheap freshness check)。

信任边界(改写自 方法库 RESUME.md「Trust boundary」,#30,
- 仅仓库内路径:resolve 后必须落在仓库根内,拒绝绝对路径与 ../ 逃逸;
  - 拒涉密文件: .env* / .git/ / credentials* / 私钥证书(*.pem、id_rsa*、
    *.key)/ 任何疑似 secret store;
  - 键集精确相等:check 模式要求基线 files 键集与重算键集可逐键对账,
    基线含仓外/涉密/重复路径 → 按不可信缓存拒绝(退出 2),不静默清选;
  - 原子写:临时文件 + os.replace,中断不留半截基线。

diff 归约入口:diff 子命令对**单个变更路径**运行 `git diff HEAD -- <path>`
(参数列表传递,路径加引号限定,绝不裸跑全仓 diff);git 不可得时明说并退 2。
归约成「有意义 UI delta」是模型/人的活——本脚本只输出统计,并且明确:
**不得以变更行数或整文件哈希推断重要性**;指纹不匹配单独不强制冷路由。

用法:
    python3 scripts/source-fingerprint.py create <repo> [--output PATH]
    python3 scripts/source-fingerprint.py check  <repo> --baseline PATH
    python3 scripts/source-fingerprint.py diff   <repo> --baseline PATH --path <rel>

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题(有变更) / 2=没能检查;#16)。
依赖: Python 3 标准库(git 仅 diff 子命令需要)。
"""
# ---- 模块说明结束 ----
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

SCHEMA_VERSION = 1

# 目录排除(依赖/构建产物/版本库自身)
EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".next", "__pycache__",
                ".venv", "venv", ".maliang", "specmark"}

# 涉密文件签名(信任边界;命中即拒绝入基线/拒绝信任基线)
SECRET_FILE_RE = re.compile(
    r"(^|/)(\.env[^/]*|credentials[^/]*|id_rsa[^/]*|id_ed25519[^/]*|id_ecdsa[^/]*"
    r"|id_dsa[^/]*|\.git-credentials|\.netrc|\.npmrc|\.pypirc|.*\.pem|.*\.key"
    r"|.*\.p12|.*\.pfx|secrets?\.[a-z]+)$",
    re.IGNORECASE,
)


def is_safe_rel_path(repo_root, rel):
    """仓库内相对路径信任校验:仓内、非涉密、非目录穿越。"""
    if os.path.isabs(rel) or ".." in rel.split(os.sep) or rel.startswith("~"):
        return False, "路径逃逸/绝对路径: %s" % rel
    if ".git" in rel.replace(os.sep, "/").split("/"):
        return False, "版本库内部路径(.git): %s" % rel
    if SECRET_FILE_RE.search(rel.replace(os.sep, "/")):
        return False, "疑似涉密文件(信任边界拒绝): %s" % rel
    full = os.path.normpath(os.path.join(repo_root, rel))
    if not (full == repo_root or full.startswith(repo_root + os.sep)):
        return False, "解析后落在仓库外: %s" % rel
    return True, ""


def walk_repo(repo_root):
    """遍历仓库文件,返回相对路径列表(排除目录与涉密文件)。"""
    out = []
    for root, dirs, names in os.walk(repo_root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("."))
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(root, name), repo_root)
            safe, _ = is_safe_rel_path(repo_root, rel)
            if safe:
                out.append(rel)
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def build_fingerprints(repo_root):
    """逐文件哈希;单个文件读不了 = 显性报错(不算基线)。"""
    files = {}
    for rel in walk_repo(repo_root):
        full = os.path.join(repo_root, rel)
        if not os.path.isfile(full) or os.path.islink(full):
            continue
        try:
            files[rel.replace(os.sep, "/")] = sha256_file(full)
        except OSError as exc:
            raise RuntimeError("无法读取 %s: %s" % (rel, exc))
    return files


def atomic_write_json(path, payload):
    """临时文件 + os.replace 原子写(中断不留半截基线)。"""
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def load_baseline(path, repo_root):
    """读基线并做信任校验;不可信 → 抛 UntrustedBaseline(退出 2)。"""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise UntrustedBaseline("基线不可读: %s" % exc)
    if not isinstance(data, dict) or data.get("schemaVersion") != SCHEMA_VERSION:
        raise UntrustedBaseline("基线 schemaVersion 缺失或不符(按不可信缓存拒绝)")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise UntrustedBaseline("基线缺 files 映射(按不可信缓存拒绝)")
    for rel in files:
        safe, why = is_safe_rel_path(repo_root, rel)
        if not safe:
            raise UntrustedBaseline("基线内路径不可信: %s" % why)
        if not isinstance(files[rel], str) or len(files[rel]) != 64:
            raise UntrustedBaseline("基线内指纹非法: %s" % rel)
    return data, files


class UntrustedBaseline(Exception):
    """基线按不可信缓存拒绝(退出 2,不静默清选)。"""


def cmd_create(args):
    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(repo_root):
        print("source-fingerprint: 仓库目录不存在: %s" % repo_root, file=sys.stderr)
        return 2
    try:
        files = build_fingerprints(repo_root)
    except RuntimeError as exc:
        print("source-fingerprint: %s" % exc, file=sys.stderr)
        return 2
    payload = {
        "schemaVersion": SCHEMA_VERSION,
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "repo": os.path.basename(repo_root),
        "files": files,
    }
    output = args.output or os.path.join(repo_root, ".maliang", "source-fingerprints.json")
    atomic_write_json(output, payload)
    print("基线已写入 %s(%d 个文件;哈希只做新鲜度,不读内容进上下文)" % (output, len(files)))
    return 0


def cmd_check(args):
    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(repo_root):
        print("source-fingerprint: 仓库目录不存在: %s" % repo_root, file=sys.stderr)
        return 2
    try:
        _meta, baseline_files = load_baseline(args.baseline, repo_root)
    except UntrustedBaseline as exc:
        print("source-fingerprint: UNTRUSTED —— %s(重建基线后再跑)" % exc, file=sys.stderr)
        return 2
    try:
        current = build_fingerprints(repo_root)
    except RuntimeError as exc:
        print("source-fingerprint: %s" % exc, file=sys.stderr)
        return 2

    changed = sorted(f for f in current if f in baseline_files and current[f] != baseline_files[f])
    added = sorted(f for f in current if f not in baseline_files)
    removed = sorted(f for f in baseline_files if f not in current)
    for f in changed:
        print("changed: %s" % f)
    for f in added:
        print("added:   %s" % f)
    for f in removed:
        print("removed: %s" % f)
    if not (changed or added or removed):
        print("指纹一致(%d 个文件):自基线以来仓库未变。" % len(current))
        return 0
    print("指纹差异:%d changed / %d added / %d removed(哈希只证变化,不证重要性;"
          "不得以变更行数或整文件哈希推断重要性)" % (len(changed), len(added), len(removed)))
    return 1


def cmd_diff(args):
    repo_root = os.path.abspath(args.repo)
    rel = args.path.replace("/", os.sep)
    safe, why = is_safe_rel_path(repo_root, args.path)
    if not safe:
        print("source-fingerprint: %s" % why, file=sys.stderr)
        return 2
    if not os.path.isfile(os.path.join(repo_root, rel)):
        print("source-fingerprint: 文件不存在: %s" % args.path, file=sys.stderr)
        return 2
    try:
        _meta, baseline_files = load_baseline(args.baseline, repo_root)
    except UntrustedBaseline as exc:
        print("source-fingerprint: UNTRUSTED —— %s" % exc, file=sys.stderr)
        return 2
    full_path = os.path.join(repo_root, rel)
    if os.path.islink(full_path):
        print("source-fingerprint: UNMEASURED —— 符号链接不入基线(与 create 口径一致)", file=sys.stderr)
        return 2
    unchanged = baseline_files.get(args.path.replace(os.sep, "/")) == sha256_file(os.path.join(repo_root, rel))
    if unchanged:
        print("%s 与基线一致:无需 diff(基线即 HEAD 之外的独立新鲜度凭证)。" % args.path)
        return 0
    try:
        proc = subprocess.run(
            ["git", "-C", repo_root, "diff", "HEAD", "--", args.path],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("source-fingerprint: git 不可得(%s)——文件已变,但精确 delta 不可得;"
              "按哈希刷新处理,不要编造变更摘要。" % exc, file=sys.stderr)
        return 2
    if proc.returncode != 0:
        print("source-fingerprint: git diff 失败: %s——文件已变,但精确 delta 不可得,"
              "按哈希刷新处理。" % proc.stderr.strip(), file=sys.stderr)
        return 2
    sys.stdout.write(proc.stdout)
    if not proc.stdout.strip():
        print("(git diff 为空:文件相对 HEAD 无未提交改动;指纹差异来自已提交的历史)"
              "——delta 不可得时明说,不得以行数推断重要性。")
    return 0


def _main_fingerprint(argv=None):
    parser = argparse.ArgumentParser(
        description="源码 SHA-256 指纹基线(create/check/diff;信任边界+原子写;不读内容进上下文)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="建立指纹基线")
    p_create.add_argument("repo")
    p_create.add_argument("--output", default=None, help="基线输出路径(默认 <repo>/.maliang/source-fingerprints.json)")

    p_check = sub.add_parser("check", help="对比基线,输出 changed/added/removed")
    p_check.add_argument("repo")
    p_check.add_argument("--baseline", required=True)

    p_diff = sub.add_parser("diff", help="对单个变更路径跑 git diff HEAD -- <path>(引号限定)")
    p_diff.add_argument("repo")
    p_diff.add_argument("--baseline", required=True)
    p_diff.add_argument("--path", required=True, help="仓库内相对路径")

    args = parser.parse_args(argv)
    return {"create": cmd_create, "check": cmd_check, "diff": cmd_diff}[args.cmd](args)


# ============================================================
# 来源节: evidence-check.py (子命令: evidence)

# ---- 原 evidence-check.py 模块说明 ----
"""evidence-check —— 取证契约校验（截图证据齐套性检查）。

"看一眼"与"取证"是两种用途：看一眼只截当前屏；取证一次取齐，只在送评审前与
交付前做。本脚本校验一次取证产出的 `report.json` 是否齐套——缺项不是"跳过"，
是把结论推到 `unverified`（未验证不得记为通过、disposition 不得为 deliver）。

report.json 契约（maliang-evidence/1，纯 JSON，路径相对 report.json 所在目录）:

    {
      "schema": "maliang-evidence/1",
      "capturedAt": "2026-10-12T10:00:00+08:00",
      "pages": [
        {
          "page": "preview_home_iphone15.html",
          "viewport": "390x844",
          "sheet": "shots/sheet-home.png",          # 并排图（≥2 个状态时必填）
          "motion": "probe/home-motion.json",       # 动效探测（必填）
          "recording": "record/home.mp4",           # 录屏（必填）
          "states": [
            {
              "state": "idle",
              "shot": "shots/home-idle.png",        # 状态图（必填）
              "shot2x": "shots/home-idle@2x.png",   # 2x 图（必填）
              "masked": "shots/home-idle-masked.png"# 遮字图（必填）
            }
          ]
        }
      ]
    }

规则:
  - 每页每状态必齐 状态图 / 2x 图 / 遮字图；每页必齐 动效探测 / 录屏；
    多状态页必齐 并排图（单状态页无并排图可言，记为 n/a 而非缺项）；
  - 任一被引用文件不存在或为空 → 该槽位计缺项（空文件不是证据）；
  - 同一文件被多个槽位复用 → 计问题（2x 图与状态图同文件、并排图与状态图同
    文件都是假齐套）；
  - 条目带 `failed: true` / `skipped: true` → 计缺项并在清单里转录原因；
  - 空 WebGL 截图不当证据（内容级别判断超出静态校验能力，见 preview.md 取证契约节）。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
  0 = 齐套；1 = 有缺项/问题；2 = 没能检查（找不到 report.json / 用法错误）。
依赖: Python 3 标准库(无第三方依赖)。
"""
# ---- 模块说明结束 ----

import argparse
import json
import os
import sys

SCHEMA_NAME = "maliang-evidence/1"
REQUIRED_REPORT_FILES = ("report.json",)
STATE_SLOTS = (("shot", "状态图"), ("shot2x", "2x 图"), ("masked", "遮字图"))
PAGE_SLOTS = (("motion", "动效探测"), ("recording", "录屏"))


def _slot_path(value) -> str | None:
    """槽位取值：字符串路径，或 {"file": path} 形态；其余视为未提供。"""
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("file", "path"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return None


def _find_reports(target: str) -> list[str]:
    """目标为 report.json 文件，或含 report.json 的目录（递归）。"""
    if os.path.isfile(target):
        return [os.path.abspath(target)]
    if os.path.isdir(target):
        found = []
        for dirpath, _, filenames in os.walk(target):
            for fn in filenames:
                if fn in REQUIRED_REPORT_FILES:
                    found.append(os.path.abspath(os.path.join(dirpath, fn)))
        return sorted(found)
    return []


def check_report(report_path: str) -> dict:
    """校验单个 report.json；返回 {problems, missing, notes, pages}。"""
    problems: list[str] = []
    missing: list[str] = []
    notes: list[str] = []
    base = os.path.dirname(os.path.abspath(report_path))
    with open(report_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError(
            "report.json 顶层必须是对象（含 schema 与 pages[]）；"
            "扁平条目数组不是本契约的形态"
        )
    schema = raw.get("schema")
    if schema != SCHEMA_NAME:
        problems.append(f"schema={schema!r} 不是 {SCHEMA_NAME!r}（契约版本不符）")
    pages = raw.get("pages")
    if not isinstance(pages, list) or not pages:
        problems.append("pages[] 缺省或为空（没有任何页面的取证不成立）")
        return {"problems": problems, "missing": missing, "notes": notes, "pages": 0}
    seen_paths: dict[str, str] = {}

    def require_file(rel: str, slot_label: str, where: str) -> None:
        abs_path = os.path.normpath(os.path.join(base, rel))
        if not os.path.isfile(abs_path):
            missing.append(f"{where} 缺 {slot_label}: {rel}（文件不存在）")
            return
        if os.path.getsize(abs_path) == 0:
            missing.append(f"{where} 缺 {slot_label}: {rel}（文件为空，空文件不是证据）")
            return
        owner = seen_paths.get(abs_path)
        if owner:
            problems.append(
                f"{where} 的 {slot_label} 与 {owner} 复用同一文件 {rel}（假齐套）"
            )
        else:
            seen_paths[abs_path] = f"{where} {slot_label}"

    for index, page in enumerate(pages, 1):
        if not isinstance(page, dict):
            problems.append(f"第 {index} 页不是对象")
            continue
        page_name = page.get("page") or page.get("id") or f"pages[{index}]"
        where_page = str(page_name)
        states = page.get("states")
        if not isinstance(states, list) or not states:
            problems.append(f"{where_page}: states[] 缺省或为空")
            states = []
        for slot, label in PAGE_SLOTS:
            rel = _slot_path(page.get(slot))
            if rel:
                require_file(rel, label, where_page)
            else:
                missing.append(f"{where_page} 缺 {label}（{slot}）")
        if len(states) >= 2:
            rel = _slot_path(page.get("sheet"))
            if rel:
                require_file(rel, "并排图", where_page)
            else:
                missing.append(f"{where_page} 缺 并排图（sheet）")
        elif "sheet" not in page:
            notes.append(f"{where_page}: 单状态页无并排图可查（n/a）")
        for sindex, state in enumerate(states, 1):
            if not isinstance(state, dict):
                problems.append(f"{where_page}: 第 {sindex} 个状态不是对象")
                continue
            state_name = state.get("state") or state.get("name") or f"states[{sindex}]"
            where = f"{where_page} · {state_name}"
            if state.get("failed") is True or state.get("skipped") is True:
                reason = state.get("reason") or state.get("error") or "条目自报失败/跳过"
                missing.append(f"{where}: 条目未完成（{reason}）")
                continue
            for slot, label in STATE_SLOTS:
                rel = _slot_path(state.get(slot))
                if rel:
                    require_file(rel, label, where)
                else:
                    missing.append(f"{where} 缺 {label}（{slot}）")
    return {"problems": problems, "missing": missing, "notes": notes, "pages": len(pages)}


def run_evidence(target: str, fmt: str) -> int:
    reports = _find_reports(target)
    if not reports:
        print(
            f"evidence-check: 没能检查——{target} 下找不到 report.json（未测量，不得记为通过）。",
            file=sys.stderr,
        )
        return 2
    total_missing = 0
    total_problems = 0
    results = []
    for report in reports:
        try:
            result = check_report(report)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"[FAIL] {report}: 报告不可解析或非法：{exc}", file=sys.stderr)
            total_problems += 1
            results.append({"report": report, "problems": [str(exc)], "missing": []})
            continue
        total_missing += len(result["missing"])
        total_problems += len(result["problems"])
        results.append({"report": report, **result})
        if fmt == "text":
            status = "FAIL" if (result["missing"] or result["problems"]) else "PASS"
            print(f"[{status}] {report}  ({result['pages']} 页)")
            for item in result["problems"]:
                print(f"  ✗ {item}")
            for item in result["missing"]:
                print(f"  ✗ {item}")
            for item in result["notes"]:
                print(f"  · {item}")
    if fmt == "json":
        print(json.dumps(
            {"reports": results, "missing": total_missing, "problems": total_problems},
            ensure_ascii=False, indent=2))
    else:
        print("")
        print("=" * 40)
        if total_missing or total_problems:
            print(
                f"取证结果: {total_missing} 项缺件, {total_problems} 项问题——"
                "缺项按 unverified 处理（未验证不得记为通过，disposition 不得为 deliver）；"
                "重取后重跑。"
            )
        else:
            print("取证结果: 齐套（状态图/2x/遮字/并排/动效探测/录屏）")
    return 1 if (total_missing or total_problems) else 0


def _main_evidence(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="evidence-check.py",
        description="取证契约校验：report.json 的截图证据齐套性（状态图/2x/并排/遮字/动效探测/录屏）。",
        epilog="report.json 契约见脚本头注；缺项推 unverified。示例:\n"
        "  python3 scripts/evidence-check.py shots/report.json\n"
        "  python3 scripts/evidence-check.py examples/preview/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", help="report.json 路径，或含 report.json 的目录")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式（默认 text）")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return run_evidence(args.target, args.format)


if __name__ == "__main__":
    sys.exit(main())
