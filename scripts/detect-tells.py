#!/usr/bin/env python3
"""确定性 AI-tell 代码检测器(纯正则,无 LLM)。

用法:
    python3 scripts/detect-tells.py <file_or_dir...> [--format {text,json}]

扫描用户真实代码文件(preview 自包含 HTML / redesign 改动行所在文件),只收
**可正则表达的机械规则**;品味类 tell(配色气质 / 布局节奏 / 文案腔调)不在此
扫描,留给 ai-tells.md 的人工对照流程——确定性判断用代码,品味判断留给人与
LLM 评审。

检测规则按**四档严重级**对齐(critical / major / minor / warn;来源:ui-craft
detect/rules.mjs 四档实测 critical 14/major 25/minor 2/warn 2,2026-10 吸收):
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

告警档(advisory,只报不拦,不影响退出码;同样支持 tell-exempt 豁免):
  numbered-eyebrow [minor]  零填充编号 eyebrow(「01 · About」装饰性编号)      → ai-tells §10
  reflex-font [warn]        display 首位字族命中 ai-tells §11 反射字体清单。命中不自动
                            违规(仍走 §0 豁免总则),故进告警档而非硬失败通道;命中后
                            要么换字族,要么写出「没有其他字体能满足」的理由并标豁免。
                            来源:hue scripts/validate.mjs checkFonts(BANNED_DISPLAY_FONTS),2026-10 吸收。

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
来源: impeccable hooks 两层规则与豁免窄化思想,2026-09 吸收(中文自研实现);
      四档对齐与机械规则扩充: ui-craft scripts/detect/rules.mjs(#21),2026-10 吸收。
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

# 四档严重级(与 maliang 审查三档 + 告警档对齐;来源:ui-craft #21 四档)
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

# 暖紫带/冷蓝青带(ui-craft 原口径 255-330;上限放宽到 350 覆盖 ai-tells §1
# 「紫蓝粉」的 pink 系 330°-345°——自研口径,标注)
_WARM_HUE_LO, _WARM_HUE_HI = 255.0, 350.0
_COOL_HUE_LO, _COOL_HUE_HI = 170.0, 255.0


def css_hue(token):
    """CSS 颜色字面量的色相(度),读不出返回 None(近灰无有效色相亦 None)。

    移植自 ui-craft scripts/detect/rules.mjs cssHue(#21),2026-10 吸收。
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

    例外(ui-craft 同款):≤13px 且加宽字距的小标签是文档化例外,不算喊叫。
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

    句中 emoji 不算;来源 ui-craft emoji-feature-icon(#21),2026-10 吸收。
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


_CHECKS = (
    check_gradient_text,
    check_glow_shadow,
    check_uniform_radius,
    check_tracking_abuse,
    check_colored_border,
    check_purple_cyan_gradient,
    check_uppercase_heading,
    check_emoji_icon,
)


# ---------------------------------------------------------------------------
# 告警档:reflex-font(display 首位字族命中 ai-tells §11 反射字体清单)
#
# 不进硬失败通道的理由:ai-tells.md §11 明说「命中不自动违规(仍走第 0 节豁免
# 总则)」,而 preview.md「命中非豁免 tell = 硬性失败」只约束硬通道;两条并存时
# 反射字体只能进告警档(来源:hue scripts/validate.mjs checkFonts 的 WARN 口径)。
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
    (RULE_NUMBERED_EYEBROW, SEV_MINOR,
     re.compile(r">\s*0\d{1,2}\s+[·/—–-]\s+[A-Za-z]"),
     "零填充编号 eyebrow(「01 · About」装饰性编号),见 ai-tells.md §10;人工裁量"),
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

    # 豁免计数:同一套匹配在不带豁免的口径下重跑一次,差值即被豁免掉的命中数
    total_hits = 0
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
            print("%s:%d: [%s] %s" % (
                finding["file"], finding["line"], finding["rule"], finding["message"],
            ))
        for warning in warnings:
            print("%s:%d: [%s·告警档] %s" % (
                warning["file"], warning["line"], warning["rule"], warning["message"],
            ))
        print("扫描 %d 个文件,命中 %d 处 tell(豁免 %d 处,读取失败 %d 个);告警档 %d 处(不拦截)"
              % (len(files) - unreadable, len(findings), exempted, unreadable, len(warnings)))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
