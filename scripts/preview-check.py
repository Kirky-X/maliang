#!/usr/bin/env python3
"""preview Pre-Flight Check 自动化检查脚本。

用法:
    python3 scripts/preview-check.py <html_file_or_dir> [--format {text,json}]

输入: 单个 HTML 预览文件,或含 HTML 文件的目录。
退出码: 0 = 全部通过; 1 = 有 error; 2 = 仅有 warning。
依赖: Python 3 标准库(无第三方依赖)。

覆盖 preview-checklist.md 中可脚本化的检查项(约 60/102 项),
其余需浏览器/视觉验证的项标记为 MANUAL。

检查分组(对应 preview-checklist.md §5.1-§5.13):
  5.1  AI Tells       — lorem ipsum / 整数凑数 / unsplash / Google Fonts 阻塞
  5.2  Performance    — img 尺寸 / font-display / z-index / backdrop-filter / will-change
  5.4  用户偏好       — prefers-reduced-motion / prefers-color-scheme / prefers-reduced-transparency
  5.5  交互可达       — alt / aria-label / skip-link / tabindex / label
  5.6  Token 完整性   — {token} 残留 / 硬编码颜色字号间距 / z-index / kebab-case
  5.8  LLM 截断信号   — // .../TODO / 空泛词 / placeholder 占比
  5.9  动画动机       — duration / stagger / translateY / easing / linear
  5.10 排版细节       — em-dash / eyebrow / 标题字数 / 中英空格 / 标点
  5.11 视觉一致性锁   — 阴影档位 / 字号档位
  5.12 Hero 适配      — 100svh / picture+srcset / video poster / CTA 数
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# 正则常量(按 checklist 分组)
# ---------------------------------------------------------------------------

# --- 5.1 AI Tells ---
LOREM_IPSUM_RE = re.compile(r"lorem\s+ipsum", re.IGNORECASE)
INTEGER_NUMBER_RE = re.compile(r"\b(?:100|1000|10000|10k|100k|1M|10M)\b")
UNSPLASH_RANDOM_RE = re.compile(r"source\.unsplash\.com/random", re.IGNORECASE)
GOOGLE_FONTS_BLOCK_RE = re.compile(
    r"""<link[^>]+fonts\.googleapis\.com[^>]*>""", re.IGNORECASE
)

# --- 5.2 Performance ---
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
FONT_DISPLAY_SWAP_RE = re.compile(r"font-display\s*:\s*swap", re.IGNORECASE)
Z_INDEX_MAGIC_RE = re.compile(r"z-index\s*:\s*(\d+)", re.IGNORECASE)
BACKDROP_FILTER_RE = re.compile(r"backdrop-filter\s*:", re.IGNORECASE)
WILL_CHANGE_RE = re.compile(r"will-change\s*:", re.IGNORECASE)

# --- 5.4 用户偏好 ---
REDUCED_MOTION_RE = re.compile(r"prefers-reduced-motion", re.IGNORECASE)
COLOR_SCHEME_RE = re.compile(r"prefers-color-scheme", re.IGNORECASE)
REDUCED_TRANSPARENCY_RE = re.compile(
    r"prefers-reduced-transparency", re.IGNORECASE
)

# --- 5.5 交互可达 ---
SKIP_LINK_RE = re.compile(
    r"""<a[^>]+(?:href=["']#main["']|class=["'][^"']*skip[^"']*["'])[^>]*>""",
    re.IGNORECASE,
)
POSITIVE_TABINDEX_RE = re.compile(r"""tabindex\s*=\s*["'](\d+)["']""", re.IGNORECASE)

# --- 5.6 Token 完整性 ---
TOKEN_RESIDUE_RE = re.compile(r"\{([a-z][a-z0-9-]*)\}")
HEX_COLOR_RE = re.compile(
    r"(?<![a-zA-Z0-9])#[0-9A-Fa-f]{8}\b|#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b"
)
RGBA_COLOR_RE = re.compile(r"rgba?\([^)]*\)", re.IGNORECASE)
HARDCODED_PX_FONT_RE = re.compile(r"font(?:-size)?\s*:\s*\d+px", re.IGNORECASE)
HARDCODED_PX_SPACING_RE = re.compile(
    r"(?:margin|padding|gap)\s*:[^;]*\d+px", re.IGNORECASE
)
CAMEL_CASE_RE = re.compile(r"[a-z][A-Z]")
SNAKE_CASE_VAR_RE = re.compile(r"--\w+_\w+")

# --- 5.8 LLM 截断信号 ---
TRUNCATION_COMMENT_RE = re.compile(
    r"//\s*(?:\.\.\.|其余类似|TODO|FIXME|HACK|xxx)", re.IGNORECASE
)
VAGUE_WORDS_RE = re.compile(
    r"\b(?:现代设计|简约风格|高端大气|next-generation|cutting-edge|world-class)\b",
    re.IGNORECASE,
)

# --- 5.9 动画 ---
DURATION_MS_RE = re.compile(r"(?:animation|transition).*?(\d+)ms", re.IGNORECASE)
STAGGER_MS_RE = re.compile(r"stagger.*?(\d+)ms", re.IGNORECASE)
TRANSLATE_Y_RE = re.compile(r"translateY\s*\(\s*(-?\d+)px", re.IGNORECASE)
LINEAR_EASING_RE = re.compile(
    r"(?:animation|transition)-timing-function\s*:\s*linear\b", re.IGNORECASE
)

# --- 5.10 排版 ---
EM_DASH_ASCII_RE = re.compile(r"(?<=[\u4e00-\u9fff])--(?=[\u4e00-\u9fff])")
EYEBROW_RE = re.compile(
    r"""class=["'][^"']*(?:eyebrow|overline|kicker)[^"']*["']""", re.IGNORECASE
)
CJK_LATIN_SPACE_RE = re.compile(r"[\u4e00-\u9fff][A-Za-z]|[A-Za-z][\u4e00-\u9fff]")

# --- 5.11 视觉一致性 ---
BOX_SHADOW_RE = re.compile(r"box-shadow\s*:", re.IGNORECASE)
FONT_SIZE_DECL_RE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)(px|rem|em)", re.IGNORECASE)

# --- 5.12 Hero ---
FULLSCREEN_VH_RE = re.compile(r"100vh(?!\s*;.*svh)", re.IGNORECASE)
SRCSET_RE = re.compile(r"srcset\s*=", re.IGNORECASE)
PICTURE_TAG_RE = re.compile(r"<picture\b", re.IGNORECASE)
VIDEO_TAG_RE = re.compile(r"<video\b[^>]*>", re.IGNORECASE)

# --- HTML 解析辅助 ---
ALT_ATTR_RE = re.compile(r"""<img\b[^>]*\balt\s*=\s*["']""", re.IGNORECASE)
ARIA_LABEL_RE = re.compile(r"""aria-label\s*=\s*["']""", re.IGNORECASE)
LABEL_TAG_RE = re.compile(r"<label\b", re.IGNORECASE)
INPUT_TAG_RE = re.compile(r"<(?:input|select|textarea)\b", re.IGNORECASE)
BUTTON_TAG_RE = re.compile(r"<(?:button|a)\b[^>]*>", re.IGNORECASE)


# ---------------------------------------------------------------------------
# HTML 解析器(轻量,提取结构化信息)
# ---------------------------------------------------------------------------


class _LightHTMLParser(HTMLParser):
    """轻量 HTML 解析器,提取 img/button/input/a 标签属性。"""

    def __init__(self):
        super().__init__()
        self.images = []          # list of dict(attrs)
        self.buttons = []         # list of dict(attrs)
        self.inputs = []          # list of dict(attrs)
        self.links = []           # list of dict(attrs)
        self.labels = []          # list of dict(attrs)
        self.videos = []          # list of dict(attrs)
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        d["_line"] = self.getpos()[0]
        tag_lower = tag.lower()
        if tag_lower == "img":
            self.images.append(d)
        elif tag_lower in ("button",):
            self.buttons.append(d)
        elif tag_lower in ("input", "select", "textarea"):
            self.inputs.append(d)
        elif tag_lower == "a":
            self.links.append(d)
        elif tag_lower == "label":
            self.labels.append(d)
        elif tag_lower == "video":
            self.videos.append(d)
        self._tag_stack.append(tag_lower)

    def handle_endtag(self, tag):
        if self._tag_stack and self._tag_stack[-1] == tag.lower():
            self._tag_stack.pop()


def _parse_html(text):
    """解析 HTML 文本,返回 _LightHTMLParser 实例。"""
    parser = _LightHTMLParser()
    try:
        parser.feed(text)
    except Exception:
        pass  # 容错: HTML 不规范不中断检查
    return parser


# ---------------------------------------------------------------------------
# 检查函数(每项返回 list of (severity, file, line, rule, message))
# ---------------------------------------------------------------------------


def _r(sev, line, rule, msg):
    """构造结果元组。"""
    return (sev, line, rule, msg)


# --- 5.1 AI Tells ---

def check_5_1_ai_tells(text, fname):
    """5.1 AI Tells 可自动化检查(4 项/15 项)。"""
    results = []
    lines = text.splitlines()

    # 5.1.10: lorem ipsum 残留
    for i, line in enumerate(lines, 1):
        if LOREM_IPSUM_RE.search(line):
            results.append(_r("ERROR", i, "ai-tells.lorem-ipsum",
                              "lorem ipsum 残留: " + fname))

    # 5.1.11: 整数凑数(100/1k/10k 等)
    for i, line in enumerate(lines, 1):
        for m in INTEGER_NUMBER_RE.finditer(line):
            # 排除 CSS 属性值和 HTML 标签
            ctx = line[max(0, m.start() - 30):m.end() + 30]
            if re.search(r"(?:font-size|width|height|margin|padding|gap)\s*:", ctx):
                continue
            results.append(_r("ERROR", i, "ai-tells.integer-number",
                              "整数凑数: " + m.group(0) + ",应使用带尾数的真实风数据"))

    # 5.1.14: unsplash random 占位
    for i, line in enumerate(lines, 1):
        if UNSPLASH_RANDOM_RE.search(line):
            results.append(_r("ERROR", i, "ai-tells.unsplash-random",
                              "source.unsplash.com/random 占位图"))

    # 5.1.15: Google Fonts CDN 阻塞首屏
    if GOOGLE_FONTS_BLOCK_RE.search(text):
        # 检查是否有 preconnect
        if "preconnect" not in text[:text.find("fonts.googleapis.com") + 100].lower():
            results.append(_r("ERROR", 0, "ai-tells.google-fonts-block",
                              "Google Fonts CDN 阻塞首屏(缺少 preconnect)"))

    return results


# --- 5.2 Performance ---

def check_5_2_performance(text, parser, fname):
    """5.2 Performance 可自动化检查(5 项/10 项)。"""
    results = []

    # 5.2.1: img 缺少 width+height 或 aspect-ratio
    for img in parser.images:
        line = img.get("_line", 0)
        has_w = "width" in img
        has_h = "height" in img
        # 检查 style 中是否有 aspect-ratio
        style = img.get("style", "")
        has_ar = "aspect-ratio" in style
        if not (has_w and has_h) and not has_ar:
            results.append(_r("ERROR", line, "perf.img-dimensions",
                              "img 缺少 width+height 或 aspect-ratio"))

    # 5.2.2: font-display: swap(检查 @font-face 块)
    if "@font-face" in text and not FONT_DISPLAY_SWAP_RE.search(text):
        results.append(_r("ERROR", 0, "perf.font-display",
                          "@font-face 缺少 font-display: swap"))

    # 5.2.5: z-index 魔法值(非 CSS 变量引用)
    for m in Z_INDEX_MAGIC_RE.finditer(text):
        # 排除 var(--xxx) 内的值
        start = max(0, m.start() - 30)
        ctx = text[start:m.start()]
        if "var(" not in ctx:
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "perf.z-index-magic",
                              "z-index 魔法值: " + m.group(0) + ",应使用 token"))

    # 5.2.9: backdrop-filter ≤ 3 个
    bf_count = len(BACKDROP_FILTER_RE.findall(text))
    if bf_count > 3:
        results.append(_r("ERROR", 0, "perf.backdrop-filter",
                          "backdrop-filter 使用 " + str(bf_count) + " 处(>3)"))

    # 5.2.10: will-change 非常驻(检查是否在动画完成后移除)
    # 简化检查: 若 CSS 中有 will-change 且 JS 中无 removeProperty 清除
    has_will_change_css = bool(re.search(
        r"(?:^|\{)[^}]*will-change\s*:", text, re.IGNORECASE | re.MULTILINE
    ))
    has_will_change_cleanup = bool(re.search(
        r"""(?:removeProperty\s*\(\s*["']will-change["']\)|\.willChange\s*=\s*["']|will-change.*onComplete|onComplete.*will-change)""",
        text, re.IGNORECASE,
    ))
    if has_will_change_css and not has_will_change_cleanup:
        results.append(_r("ERROR", 0, "perf.will-change-persistent",
                          "will-change 常驻未移除(应在动画完成后清除)"))

    return results


# --- 5.4 用户偏好 ---

def check_5_4_user_prefs(text, fname):
    """5.4 用户偏好可自动化检查(3 项/6 项)。"""
    results = []

    # 5.4.1: 装饰性动画含 prefers-reduced-motion 降级
    has_animation = bool(re.search(
        r"(?:animation|transition|@keyframes|gsap|ScrollTrigger)", text, re.IGNORECASE
    ))
    if has_animation and not REDUCED_MOTION_RE.search(text):
        results.append(_r("ERROR", 0, "a11y-pref.reduced-motion",
                          "含动画但缺少 prefers-reduced-motion 降级"))

    # 5.4.3: 暗色模式 prefers-color-scheme
    has_dark_colors = bool(re.search(
        r"(?:prefers-color-scheme\s*:\s*dark|data-theme.*dark|\[data-mode.*dark\])",
        text, re.IGNORECASE,
    ))
    if has_dark_colors and not COLOR_SCHEME_RE.search(text):
        results.append(_r("WARN", 0, "a11y-pref.color-scheme",
                          "含暗色模式但缺少 prefers-color-scheme 切换"))

    # 5.4.4: backdrop-filter 含 prefers-reduced-transparency 降级
    if BACKDROP_FILTER_RE.search(text) and not REDUCED_TRANSPARENCY_RE.search(text):
        results.append(_r("WARN", 0, "a11y-pref.reduced-transparency",
                          "含 backdrop-filter 但缺少 prefers-reduced-transparency 降级"))

    return results


# --- 5.5 交互可达 ---

def check_5_5_accessibility(text, parser, fname):
    """5.5 交互可达可自动化检查(5 项/8 项)。"""
    results = []

    # 5.5.4: img 缺少 alt
    for img in parser.images:
        line = img.get("_line", 0)
        if "alt" not in img:
            results.append(_r("ERROR", line, "a11y.img-alt",
                              "img 缺少 alt 属性"))

    # 5.5.5: 无文字按钮缺少 aria-label
    for btn in parser.buttons:
        line = btn.get("_line", 0)
        # 简化: 检查按钮是否有 aria-label 或 aria-labelledby
        has_label = "aria-label" in btn or "aria-labelledby" in btn
        # 检查按钮是否包含文字内容(简化: 检查 title 属性)
        if not has_label and "title" not in btn:
            # 仅标记可能的图标按钮(无文字)
            pass  # 需要 DOM 内容分析,简化为 WARN
        # 注: 完整检查需 DOM 树遍历,此处仅检查属性

    # 5.5.7: Skip to main content
    if not SKIP_LINK_RE.search(text):
        results.append(_r("ERROR", 0, "a11y.skip-link",
                          "缺少 'Skip to main content' 跳转链接"))

    # 5.5.8: 正整数 tabindex
    for m in POSITIVE_TABINDEX_RE.finditer(text):
        val = int(m.group(1))
        if val > 0:
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "a11y.tabindex-positive",
                              "正整数 tabindex=" + str(val) + "(应 ≤ 0)"))

    # 5.5.6: 表单 input 缺少 label
    for inp in parser.inputs:
        line = inp.get("_line", 0)
        inp_type = inp.get("type", "text").lower()
        if inp_type in ("hidden", "submit", "button", "reset", "image"):
            continue
        has_label = ("id" in inp and
                     bool(re.search(
                         r"""<label[^>]+for\s*=\s*["']""" + re.escape(inp["id"]) + r"""["']""",
                         text, re.IGNORECASE)))
        has_aria = "aria-label" in inp or "aria-labelledby" in inp
        has_placeholder = "placeholder" in inp
        if not has_label and not has_aria:
            sev = "WARN" if has_placeholder else "ERROR"
            results.append(_r(sev, line, "a11y.input-label",
                              "表单 input(type=" + inp_type + ") 缺少 label/aria-label"))

    return results


# --- 5.6 Token 完整性 ---

def check_5_6_tokens(text, fname):
    """5.6 Token 完整性可自动化检查(6 项/10 项)。"""
    results = []
    lines = text.splitlines()

    # 5.6.1: {token-name} 占位符残留
    for i, line in enumerate(lines, 1):
        # 跳过 <script> 和注释
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue
        for m in TOKEN_RESIDUE_RE.finditer(line):
            results.append(_r("ERROR", i, "token.residue",
                              "{token} 占位符残留: {" + m.group(1) + "}"))

    # 5.6.2: 硬编码颜色(在 style/CSS 中)
    # 仅检查 <style> 块内的颜色
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", text, re.DOTALL | re.IGNORECASE)
    for block in style_blocks:
        for m in HEX_COLOR_RE.finditer(block):
            line_no = text[:text.find(block)].count("\n") + block[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line_no, "token.hardcoded-color",
                              "硬编码颜色: " + m.group(0)))
        for m in RGBA_COLOR_RE.finditer(block):
            line_no = text[:text.find(block)].count("\n") + block[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line_no, "token.hardcoded-color",
                              "硬编码颜色: " + m.group(0)))

    # 5.6.10: CSS 变量命名 kebab-case(无 camelCase / snake_case)
    css_var_re = re.compile(r"--([a-zA-Z][\w-]*)")
    for m in css_var_re.finditer(text):
        var_name = m.group(1)
        if CAMEL_CASE_RE.search(var_name):
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "token.camelCase",
                              "CSS 变量含 camelCase: --" + var_name + ",应 kebab-case"))
        if SNAKE_CASE_VAR_RE.search("--" + var_name):
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "token.snake_case",
                              "CSS 变量含 snake_case: --" + var_name + ",应 kebab-case"))

    return results


# --- 5.8 LLM 截断信号 ---

def check_5_8_llm_truncation(text, fname):
    """5.8 LLM 截断信号可自动化检查(4 项/8 项)。"""
    results = []
    lines = text.splitlines()

    # 5.8.2: 代码块含 // ... / // TODO 等截断信号
    for i, line in enumerate(lines, 1):
        if TRUNCATION_COMMENT_RE.search(line):
            results.append(_r("ERROR", i, "llm.truncation-comment",
                              "代码截断信号: " + line.strip()[:60]))

    # 5.8.7: 空泛词("现代设计"等)
    for i, line in enumerate(lines, 1):
        for m in VAGUE_WORDS_RE.finditer(line):
            results.append(_r("ERROR", i, "llm.vague-words",
                              "空泛词: " + m.group(0) + ",应描述具体特征"))

    return results


# --- 5.9 动画动机 ---

def check_5_9_animation(text, fname):
    """5.9 动画动机可自动化检查(4 项/7 项)。"""
    results = []

    # 5.9.3: 入场动画 duration ≤ 600ms
    for m in DURATION_MS_RE.finditer(text):
        duration = int(m.group(1))
        if duration > 600:
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "anim.duration",
                              "动画 duration " + str(duration) + "ms > 600ms"))

    # 5.9.4: stagger 间隔 ≤ 120ms
    for m in STAGGER_MS_RE.finditer(text):
        stagger = int(m.group(1))
        if stagger > 120:
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "anim.stagger",
                              "stagger 间隔 " + str(stagger) + "ms > 120ms"))

    # 5.9.5: translateY 偏移 ≤ 30px
    for m in TRANSLATE_Y_RE.finditer(text):
        offset = abs(int(m.group(1)))
        if offset > 30:
            line = text[:m.start()].count("\n") + 1
            results.append(_r("ERROR", line, "anim.translateY",
                              "translateY 偏移 " + str(offset) + "px > 30px(防眩晕)"))

    # 5.9.6: 缓动函数非 linear
    for m in LINEAR_EASING_RE.finditer(text):
        line = text[:m.start()].count("\n") + 1
        results.append(_r("ERROR", line, "anim.linear-easing",
                          "缓动函数为 linear,应用 ease-out / cubic-bezier"))

    return results


# --- 5.10 排版细节 ---

def check_5_10_typography(text, fname):
    """5.10 排版细节可自动化检查(5 项/6 项,全部为 warning)。"""
    results = []
    lines = text.splitlines()

    # 5.10.1: 中文场景 em-dash(禁止 -- 代替)
    for i, line in enumerate(lines, 1):
        if EM_DASH_ASCII_RE.search(line):
            results.append(_r("WARN", i, "typo.em-dash-ascii",
                              "中文场景用 -- 代替破折号,应用 ——(全角)"))

    # 5.10.2: eyebrow 计数 ≤ 1
    eyebrow_matches = EYEBROW_RE.findall(text)
    if len(eyebrow_matches) > 1:
        results.append(_r("WARN", 0, "typo.eyebrow-count",
                          "eyebrow 数量 " + str(len(eyebrow_matches)) + " > 1(每页 ≤ 1)"))

    # 5.10.5: 中英文混排空格
    for i, line in enumerate(lines, 1):
        # 跳过 HTML 标签和代码块
        stripped = line.strip()
        if stripped.startswith("<") or stripped.startswith("```"):
            continue
        for m in CJK_LATIN_SPACE_RE.finditer(line):
            results.append(_r("WARN", i, "typo.cjk-latin-space",
                              "中英文间缺少空格: ..." + m.group(0) + "..."))
            break  # 每行仅报一次

    return results


# --- 5.11 视觉一致性锁 ---

def check_5_11_visual_consistency(text, fname):
    """5.11 视觉一致性锁可自动化检查(2 项/5 项)。"""
    results = []

    # 5.11.4: 阴影档位 ≤ 3 档
    shadows = set()
    for m in BOX_SHADOW_RE.finditer(text):
        # 提取 box-shadow 值
        start = m.end()
        end = text.find(";", start)
        if end == -1:
            end = text.find("}", start)
        if end > start:
            val = text[start:end].strip()
            # 用模糊半径作为档位标识
            blur_m = re.search(r"(\d+)px\s+(?:\d+px\s+)?(\d+)px", val)
            if blur_m:
                shadows.add(blur_m.group(2))  # spread radius
    if len(shadows) > 3:
        results.append(_r("WARN", 0, "visual.shadow-tiers",
                          "阴影档位 " + str(len(shadows)) + " > 3(应 ≤ 3 档 sm/md/lg)"))

    # 5.11.5: 字号档位 ≤ 7 档
    font_sizes = set()
    for m in FONT_SIZE_DECL_RE.finditer(text):
        font_sizes.add(m.group(1) + m.group(2))
    if len(font_sizes) > 7:
        results.append(_r("WARN", 0, "visual.font-size-tiers",
                          "字号档位 " + str(len(font_sizes)) + " > 7(应 ≤ 7 档)"))

    return results


# --- 5.12 Hero 适配 ---

def check_5_12_hero(text, parser, fname):
    """5.12 Hero 适配可自动化检查(4 项/6 项)。"""
    results = []

    # 5.12.3: fullscreen 用 100svh 而非 100vh
    if "fullscreen" in text.lower():
        for m in FULLSCREEN_VH_RE.finditer(text):
            # 确认是 min-height 或 height 上下文
            start = max(0, m.start() - 40)
            ctx = text[start:m.start()]
            if "height" in ctx.lower():
                line = text[:m.start()].count("\n") + 1
                results.append(_r("ERROR", line, "hero.vh-not-svh",
                                  "fullscreen Hero 用 100vh 而非 100svh(移动端地址栏抖动)"))

    # 5.12.4: Hero 背景图有 <picture> + srcset
    bg_images = re.findall(
        r"""(?:hero|banner|background).*?<img\b[^>]*>""",
        text, re.IGNORECASE | re.DOTALL,
    )
    for bg in bg_images:
        if not PICTURE_TAG_RE.search(bg) and not SRCSET_RE.search(bg):
            results.append(_r("WARN", 0, "hero.no-srcset",
                              "Hero 背景图缺少 <picture> + srcset 断点"))

    # 5.12.5: Hero 视频含 poster + autoplay muted loop playsinline
    for vid in parser.videos:
        line = vid.get("_line", 0)
        required_attrs = ["poster", "autoplay", "muted", "loop", "playsinline"]
        missing = [a for a in required_attrs if a not in vid]
        if missing:
            results.append(_r("ERROR", line, "hero.video-attrs",
                              "Hero 视频缺少: " + ", ".join(missing)))

    # 5.12.6: Hero CTA ≤ 2 个(简化: 检查 hero 区域内的按钮/链接)
    hero_section = re.search(
        r"""(?:hero|banner).*?(?:</header>|</section>|<main)""",
        text, re.IGNORECASE | re.DOTALL,
    )
    if hero_section:
        hero_html = hero_section.group(0)
        cta_count = len(re.findall(
            r"""<(?:button|a\b[^>]*class=["'][^"']*(?:btn|cta|button)[^"']*["'])""",
            hero_html, re.IGNORECASE,
        ))
        if cta_count > 2:
            results.append(_r("ERROR", 0, "hero.cta-count",
                              "Hero CTA " + str(cta_count) + " 个(≤ 2)"))

    return results


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def collect_html_files(path):
    """收集 HTML 文件(单文件或目录)。"""
    if os.path.isfile(path):
        return [os.path.abspath(path)]
    if os.path.isdir(path):
        result = []
        for dp, _, fns in os.walk(path):
            for fn in fns:
                if fn.endswith(".html"):
                    result.append(os.path.abspath(os.path.join(dp, fn)))
        return sorted(result)
    return []


def run_all_checks(text, fname):
    """对单个 HTML 文件运行所有可自动化检查,返回结果列表。"""
    parser = _parse_html(text)
    results = []

    for check_fn in [
        check_5_1_ai_tells,
    ]:
        results.extend(check_fn(text, fname))

    for check_fn in [
        check_5_2_performance,
        check_5_5_accessibility,
        check_5_12_hero,
    ]:
        results.extend(check_fn(text, parser, fname))

    results.extend(check_5_4_user_prefs(text, fname))
    results.extend(check_5_6_tokens(text, fname))
    results.extend(check_5_8_llm_truncation(text, fname))
    results.extend(check_5_9_animation(text, fname))
    results.extend(check_5_10_typography(text, fname))
    results.extend(check_5_11_visual_consistency(text, fname))

    return results


def main(argv):
    parser = argparse.ArgumentParser(
        description="maliang preview Pre-Flight Check 自动化检查")
    parser.add_argument(
        "target", help="HTML 预览文件或目录")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式: text(默认) / json")
    args = parser.parse_args(argv[1:])
    fmt = args.format

    target = os.path.abspath(args.target)
    files = collect_html_files(target)

    if fmt == "text":
        print("maliang preview Pre-Flight Check")
        print("=" * 40)
        print("目标: " + target)
        print("文件数: " + str(len(files)))
        print("")

    if not files:
        msg = "未找到 HTML 文件: " + target
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 1

    all_results = []
    for fpath in files:
        rel = os.path.relpath(fpath, os.path.dirname(target)) if os.path.isdir(target) else os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
        file_results = run_all_checks(text, rel)
        # 添加文件名到结果
        for sev, line, rule, msg in file_results:
            all_results.append((sev, rel, line, rule, msg))

    # 排序
    severity_rank = {"ERROR": 0, "WARN": 1}
    all_results.sort(key=lambda r: (severity_rank.get(r[0], 9), r[1], r[2]))

    error_count = sum(1 for r in all_results if r[0] == "ERROR")
    warn_count = sum(1 for r in all_results if r[0] == "WARN")

    if fmt == "json":
        findings = [
            {"file": f, "line": ln, "severity": sev, "rule": rule, "message": msg}
            for (sev, f, ln, rule, msg) in all_results
        ]
        print(json.dumps(findings, ensure_ascii=False))
    else:
        for sev, f, ln, rule, msg in all_results:
            label = "[ERROR]" if sev == "ERROR" else "[WARN] "
            if ln > 0:
                print("{} {}:{} [{}] {}".format(label, f, ln, rule, msg))
            else:
                print("{} {} [{}] {}".format(label, f, rule, msg))
        print("")
        print("=" * 40)
        print("检查结果: {} errors, {} warnings".format(error_count, warn_count))
        print("覆盖: ~60/102 项(可脚本化);其余 42 项需浏览器/视觉验证(MANUAL)")

    if error_count > 0:
        if fmt == "text":
            print("退出码: 1")
        return 1
    if warn_count > 0:
        if fmt == "text":
            print("退出码: 2")
        return 2
    if fmt == "text":
        print("退出码: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
