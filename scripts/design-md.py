#!/usr/bin/env python3
"""design-md —— design-md 域工具合并入口(4→1):token-md / extract-tokens / derive-dark / validate。

用法(子命令 + 各自原参数透传):
    python3 scripts/design-md.py token-md <DESIGN.md> [options]        # DESIGN.md → 产物层 token.md
    python3 scripts/design-md.py extract-tokens <文件...> [options]    # 代码/截图 token 提取
    python3 scripts/design-md.py derive-dark <参数>                    # 亮色行 → 暗色行确定性派生
    python3 scripts/design-md.py validate <DESIGN.md> [options]        # token 溯源核对(V1–V5)与绑定表形态

退出码: 各子命令沿用原脚本三态语义,canonical 见 scripts/EXIT-CODES.md。
各节实现为原独立脚本全文并入(节界注释标注来源),顶层名除 main 外零改名;
本入口只做分发。依赖: Python 3 标准库(无第三方依赖)。
"""
import sys

_SUBCOMMANDS = ("token-md", "extract-tokens", "derive-dark", "validate")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("usage: design-md.py {" + "|".join(_SUBCOMMANDS) + "} [args...]")
        return 2
    sub, rest = argv[0], argv[1:]
    dispatch = {
        "token-md": _main_token_md,
        "extract-tokens": _main_extract_tokens,
        "derive-dark": _main_derive_dark,
        "validate": _main_validate,
    }
    if sub not in dispatch:
        print("[ERROR] 未知子命令: " + sub + "(可用: " + ", ".join(_SUBCOMMANDS) + ")")
        return 2
    return dispatch[sub](rest)




# ============================================================
# 来源节: design_md_to_token_md.py (子命令: token-md)

# ---- 原 design_md_to_token_md.py 模块说明 ----
"""DESIGN.md -> 产物层 token.md 自动生成脚本。

用法:
    python3 scripts/design-md.py token-md <input.md> <output.md>

依赖: Python 3 标准库 + PyYAML(可选,不可用时降级正则解析并打印警告)。
契约: 同一输入永远产出同一输出;RGBA 由 hex 计算,禁止硬编码颜色值。
"""
# ---- 模块说明结束 ----
import sys
import os
import re
import datetime


def warn(msg):
    print("[warn] {}".format(msg), file=sys.stderr)


def die(msg):
    print("[error] {}".format(msg), file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# frontmatter 解析
# ---------------------------------------------------------------------------

from maliang_common import extract_frontmatter  # noqa: E402  单一实现,style-ledger 共用


def parse_frontmatter(yaml_str):
    """解析 frontmatter。优先 PyYAML,降级正则。返回 dict。

    「PyYAML 优先+降级」骨架共享实现见 maliang_common.load_yaml_block;
    本包装保留 dmt 专属语义:非映射按空 dict(on_not_map=empty)与
    PyYAML 不可用时降级到本文件的缩进解析器(含注释剥离/转义还原,
    DESIGN.md 的 heritage 结构依赖,语义由 test_design_md_frontmatter 锁定)。
    """
    import importlib.util

    import maliang_common

    if importlib.util.find_spec("yaml") is None:
        warn("PyYAML 不可用,降级使用正则解析 frontmatter(仅支持简单 map 结构)。")
    data, err = maliang_common.load_yaml_block(
        yaml_str, fallback=parse_frontmatter_indent, on_not_map="empty")
    if err is not None:
        # 非法 YAML 响亮失败(与 c9397cf 前语义一致):PyYAML 缺失才降级,YAML 坏了不带病产出
        raise ValueError(f"frontmatter YAML 非法: {err}")
    return data


def _parse_scalar(val):
    """解析 YAML 标量:去引号/转数字,其余保留字符串。"""
    if val == "":
        return ""
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        inner = val[1:-1]
        if val.startswith('"'):
            # 双引号标量还原 YAML 转义,与 PyYAML 语义对齐(`\"` → `"`,
            # `\\` → `\`);占位符两段替换保证 `\\\"` 这类连续转义不误配。
            inner = (
                inner.replace("\\\\", "\x00")
                .replace('\\"', '"')
                .replace("\x00", "\\")
            )
        return inner
    try:
        if re.fullmatch(r"-?\d+", val):
            return int(val)
        if re.fullmatch(r"-?\d+\.\d+", val):
            return float(val)
    except (ValueError, TypeError):
        pass
    return val


def _strip_comment(raw):
    """去掉行尾 YAML 注释(引号外的 ` #`),保住 `"#212121"` 这类带 # 的值。

    token 溯源注释(`primary: "#212121" # D-P1-1`)依赖这一步:不剥离会让
    降级解析器把注释吃进标量,并把 `headline-lg: # D-P2-1` 误判成标量而非子块。
    引号内反斜杠转义整体拷贝(`\"` 不闭合引号),否则 `"a\" # x"` 会在值中间
    误剥注释截断标量,`"a\"b" # 注释` 的行尾注释则剥不掉。
    """
    out = []
    quote = None
    i = 0
    while i < len(raw):
        ch = raw[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < len(raw):
                out.append(raw[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "#" and (i == 0 or raw[i - 1] in " \t"):
            break
        out.append(ch)
        i += 1
    return "".join(out).rstrip()


def parse_frontmatter_indent(yaml_str):
    """基于缩进的降级解析器,支持两层 map + 标量(heritage 结构够用)。"""
    lines = [_strip_comment(ln) for ln in yaml_str.split("\n")]
    n = len(lines)
    state = {"i": 0}

    def parse_block(indent):
        obj = {}
        while state["i"] < n:
            raw = lines[state["i"]]
            if not raw.strip() or raw.strip().startswith("#"):
                state["i"] += 1
                continue
            cur_indent = len(raw) - len(raw.lstrip())
            if cur_indent < indent:
                break
            if cur_indent > indent:
                state["i"] += 1
                continue
            stripped = raw.strip()
            if ":" not in stripped:
                state["i"] += 1
                continue
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            state["i"] += 1
            if val == "":
                # 子块:看下一非空行缩进
                child_indent = None
                j = state["i"]
                while j < n:
                    nxt = lines[j]
                    if not nxt.strip() or nxt.strip().startswith("#"):
                        j += 1
                        continue
                    child_indent = len(nxt) - len(nxt.lstrip())
                    break
                if child_indent is not None and child_indent > cur_indent:
                    obj[key] = parse_block(child_indent)
                else:
                    obj[key] = {}
            else:
                obj[key] = _parse_scalar(val)
        return obj

    # 找首个非空行的缩进作为顶层
    top_indent = 0
    for ln in lines:
        if ln.strip():
            top_indent = len(ln) - len(ln.lstrip())
            break
    return parse_block(top_indent)


# ---------------------------------------------------------------------------
# 颜色 hex -> rgba
# ---------------------------------------------------------------------------

def _fmt_alpha(a_byte):
    a = round(a_byte / 255, 4)
    if a == int(a):
        return str(int(a))
    return "{:.4f}".format(a).rstrip("0").rstrip(".")


def hex_to_rgba(color):
    """#RGB/#RGBA/#RRGGBB/#RRGGBBAA -> rgba(...)。无法解析返回 None。"""
    s = color.strip()
    if not s.startswith("#"):
        return None
    s = s[1:]
    if not re.fullmatch(r"[0-9a-fA-F]+", s):
        return None
    try:
        if len(s) == 3:
            r, g, b = (int(c * 2, 16) for c in s)
            return "rgba({},{},{},1)".format(r, g, b)
        if len(s) == 4:
            r, g, b, a = (int(c * 2, 16) for c in s)
            return "rgba({},{},{},{})".format(r, g, b, _fmt_alpha(a))
        if len(s) == 6:
            r = int(s[0:2], 16)
            g = int(s[2:4], 16)
            b = int(s[4:6], 16)
            return "rgba({},{},{},1)".format(r, g, b)
        if len(s) == 8:
            r = int(s[0:2], 16)
            g = int(s[2:4], 16)
            b = int(s[4:6], 16)
            a = int(s[6:8], 16)
            return "rgba({},{},{},{})".format(r, g, b, _fmt_alpha(a))
    except ValueError:
        return None
    return None


# ---------------------------------------------------------------------------
# components 引用解析(校验用,最大深度 2,循环检测)
# ---------------------------------------------------------------------------

def resolve_ref(ref, data, depth=0, seen=()):
    if depth > 2:
        raise ValueError("引用解析超过最大深度 2: {}".format(ref))
    if ref in seen:
        raise ValueError("循环引用: {}".format(" -> ".join(seen + (ref,))))
    cur = data
    for part in ref.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise ValueError("无法解析引用: {}".format(ref))
        cur = cur[part]
    if isinstance(cur, str) and cur.startswith("{") and cur.endswith("}"):
        return resolve_ref(cur[1:-1], data, depth + 1, seen + (ref,))
    return cur


def validate_components(data):
    components = data.get("components") or {}
    if not isinstance(components, dict):
        return
    for comp_name, props in components.items():
        if not isinstance(props, dict):
            continue
        for prop_name, val in props.items():
            if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
                ref = val[1:-1]
                try:
                    resolve_ref(ref, data)
                except ValueError as e:
                    die("组件 {}.{} 引用解析失败: {}".format(comp_name, prop_name, e))


# ---------------------------------------------------------------------------
# markdown 表格渲染(按显示宽度对齐,中文算 2 宽)
# ---------------------------------------------------------------------------

def _disp_width(s):
    w = 0
    for ch in s:
        w += 2 if "\u4e00" <= ch <= "\u9fff" else 1
    return w


def _pad(s, width):
    s = str(s)
    return s + " " * max(0, width - _disp_width(s))


def md_table(headers, rows):
    cols = len(headers)
    widths = [_disp_width(h) for h in headers]
    for row in rows:
        for i in range(cols):
            widths[i] = max(widths[i], _disp_width(str(row[i])))
    out = []
    out.append("| " + " | ".join(_pad(h, widths[i]) for i, h in enumerate(headers)) + " |")
    out.append("| " + " | ".join("-" * widths[i] for i in range(cols)) + " |")
    for row in rows:
        out.append("| " + " | ".join(_pad(row[i], widths[i]) for i in range(cols)) + " |")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 章节渲染
# ---------------------------------------------------------------------------

def render_colors(data):
    lines = ["## 1. 颜色(colors)", ""]
    colors = data.get("colors") or {}
    if not isinstance(colors, dict) or not colors:
        lines.append("> DESIGN.md 未定义颜色 token。")
        lines.append("")
        return lines
    rows = []
    for name, val in colors.items():
        hex_val = str(val)
        rgba = hex_to_rgba(hex_val)
        if rgba is None:
            warn("颜色 {}={} 无法转换为 RGBA(命名色/函数式),RGBA 列写 n/a。".format(name, hex_val))
            rgba = "n/a"
        rows.append((name, hex_val, rgba, name))
    lines.append(md_table(["token", "HEX", "RGBA", "用途"], rows))
    lines.append("")
    return lines


def render_typography(data):
    lines = ["## 2. 字体(typography)", ""]
    typography = data.get("typography") or {}
    if not isinstance(typography, dict) or not typography:
        lines.append("> DESIGN.md 未定义字体 token。")
        lines.append("")
        return lines
    families = []
    for name, spec in typography.items():
        if isinstance(spec, dict):
            ff = spec.get("fontFamily")
            if ff and ff not in families:
                families.append(ff)
    if families:
        fam_str = ", ".join('"{}"'.format(f) for f in families)
        lines.append('字族:{}。'.format(fam_str))
    else:
        lines.append("字族:未指定。")
    lines.append("")
    rows = []
    for name, spec in typography.items():
        if not isinstance(spec, dict):
            continue
        if "fontSize" in spec:
            rows.append(("font-size-{}".format(name), str(spec["fontSize"]), name))
        if "fontWeight" in spec:
            rows.append(("font-weight-{}".format(name), str(spec["fontWeight"]), name))
        if "lineHeight" in spec:
            rows.append(("line-height-{}".format(name), str(spec["lineHeight"]), name))
        if "letterSpacing" in spec:
            rows.append(("letter-spacing-{}".format(name), str(spec["letterSpacing"]), name))
    lines.append(md_table(["token", "值", "用途"], rows))
    lines.append("")
    return lines


def render_icon():
    return ["## 3. 图标(icon)", "", "> DESIGN.md 不含图标 token,本节为占位。", ""]


def render_spacing(data):
    lines = ["## 4. 间距(spacing)", ""]
    spacing = data.get("spacing") or {}
    if not isinstance(spacing, dict) or not spacing:
        lines.append("> DESIGN.md 未定义间距 token。")
        lines.append("")
        return lines
    rows = []
    for name, val in spacing.items():
        if isinstance(val, bool):
            rows.append(("spacing-{}".format(name), str(val), name))
        elif isinstance(val, (int, float)):
            rows.append(("spacing-{}".format(name), str(val), "{} (无单位)".format(name)))
        else:
            rows.append(("spacing-{}".format(name), str(val), name))
    lines.append(md_table(["token", "值", "用途"], rows))
    lines.append("")
    return lines


def render_radius(data):
    lines = ["## 5. 圆角(radius)", ""]
    rounded = data.get("rounded") or {}
    if not isinstance(rounded, dict) or not rounded:
        lines.append("> DESIGN.md 未定义圆角 token。")
        lines.append("")
        return lines
    rows = []
    for name, val in rounded.items():
        rows.append(("radius-{}".format(name), str(val), name))
    lines.append(md_table(["token", "值", "用途"], rows))
    lines.append("")
    return lines


def render_border(data):
    lines = ["## 6. 分割线 / 边框(border)", ""]
    lines.append("> DESIGN.md 不含分割线 token,使用默认值。")
    lines.append("")
    rows = [("border-hairline", "0.5px", "极细分隔(默认)")]
    lines.append(md_table(["token", "值", "用途"], rows))
    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def render_token_md(data, input_path):
    today = datetime.date.today().isoformat()
    name = data.get("name") or "unnamed"
    input_name = os.path.basename(input_path)
    out = []
    out.append("---")
    out.append("name: {}".format(name))
    out.append("description: 由 design.md 自动生成的产物层 token 表")
    out.append("updated: {}".format(today))
    out.append("version: 1.0.0")
    out.append("---")
    out.append("")
    out.append("# token.md —— 全局硬 token 表(产物层,自动生成)")
    out.append("")
    out.append("> 由 scripts/design-md.py token-md 从 {} 自动生成。".format(input_name))
    out.append("> 手动修改会被下次生成覆盖。")
    out.append("")
    out.extend(render_colors(data))
    out.extend(render_typography(data))
    out.extend(render_icon())
    out.extend(render_spacing(data))
    out.extend(render_radius(data))
    out.extend(render_border(data))
    return "\n".join(out) + "\n"


def _main_token_md(argv):
    if len(argv) != 3:
        die("用法: python3 scripts/design_md_to_token_md.py <input.md> <output.md>")
    input_path, output_path = argv[1], argv[2]
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        die("读取输入文件失败: {}".format(e))
    yaml_str, _body = extract_frontmatter(text)
    data = parse_frontmatter(yaml_str)
    if not isinstance(data, dict):
        die("frontmatter 解析结果非 map。")
    validate_components(data)
    output = render_token_md(data, input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)
    return 0


# ============================================================
# 来源节: extract-tokens.py (子命令: extract-tokens)

# ---- 原 extract-tokens.py 模块说明 ----
"""本地样式源码的 CSS 自定义属性提取器(--var 设计 token 候选,上下文经济)。

用法:
    python3 scripts/extract-tokens.py <css/html/vue 文件或目录...>
    python3 scripts/extract-tokens.py <路径> --output ./css-vars.json   # 指定完整 JSON 落点
    python3 scripts/extract-tokens.py <路径> --budget 3000              # 压缩摘要字符预算
    python3 scripts/extract-tokens.py --grep 'border|radius'             # 检索上次保存的 JSON(不重扫)
    python3 scripts/extract-tokens.py <路径> --json                      # 全量 JSON 打到 stdout

设计纪律:
  * 数字阶梯折叠成一行:`--space-*: 4=4px 8=8px 12=12px ...`;
  * var() 别名递归解析到终值(`--a: var(--b)` → 打印 --b 的值);
  * 同一变量在不同文件被重定义 → 标 `(redefined elsewhere, likely a theme)`;
  * 框架管道(--tw-* / --el-* / radix-* 等)隐藏,摘要只留显式设计 token;
  * 按类别配额输出摘要,超预算的行数**显式披露**,绝不静默截断;
  * 摘要是一次性读物,想查细节用 --grep 就地检索已保存的 JSON,而不是整读大文件。

这些是**显式设计 token**——作者有意命名的值,在 design-md 1A 提取中可按
✅ 高置信度处理(仍须人工复核用途)。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题(--strict 且有告警)
        / 2=没能检查:路径不存在、没有任何可提取文件或一个变量都没找到;#16)。
依赖: Python 3 标准库(无第三方依赖)。
"""
# ---- 模块说明结束 ----
import argparse
import json
import os
import re
import sys

# CSS 变量定义(容忍空白/多行值/!important)
CSS_VAR_RE = re.compile(
    r"(?:(?<=[{;\s])|^)--([A-Za-z0-9_-]+)\s*:\s*([^;}]+?)\s*(?:!important\s*)?(?:;|(?=\}))",
    re.DOTALL,
)
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)

SCAN_EXTENSIONS = (".css", ".scss", ".sass", ".less", ".html", ".htm", ".vue", ".jsx", ".tsx")

# 名称启发式分类(与 anydesign CATEGORY_HINTS 同思路)
CATEGORY_HINTS = (
    ("color", ("color", "bg", "background", "border", "fg", "foreground", "surface",
               "text", "accent", "primary", "secondary", "muted", "success",
               "warning", "error", "danger", "info", "destructive", "ring")),
    ("spacing", ("space", "spacing", "gap", "padding", "margin", "inset", "size")),
    ("typography", ("font", "leading", "tracking", "line-height", "letter-spacing",
                    "weight", "text-", "heading", "title", "display", "body")),
    ("radius", ("radius", "rounded")),
    ("shadow", ("shadow", "elevation")),
    ("z-index", ("z-", "zindex", "z-index", "layer")),
    ("duration", ("duration", "transition", "delay", "ease")),
    ("breakpoint", ("breakpoint", "screen", "viewport")),
)

# 框架管道与噪声前缀:摘要里隐藏(只进 JSON,不进摘要)
NOISE_PREFIXES = (
    "tw-", "shiki", "radix-", "chakra-", "mantine-", "swiper-", "toastify-", "rdp-",
    "sx-", "framer-", "animate-", "webkit-", "moz-", "docsearch-", "cf-", "sb-",
    "intercom-", "el-", "ant-", "van-", "arco-", "naive-",
)
SEMANTIC_HINTS = ("primary", "secondary", "accent", "brand", "background", "bg", "surface",
                  "foreground", "fg", "text", "border", "muted", "success", "warning",
                  "error", "danger", "font", "radius", "shadow", "focus", "ring", "link")

DIGEST_SHARES = (
    ("color", 0.36), ("typography", 0.18), ("spacing", 0.12), ("shadow", 0.10),
    ("radius", 0.06), ("breakpoint", 0.04), ("duration", 0.04), ("z-index", 0.02),
    ("other", 0.08),
)

SCALE_RE = re.compile(r"^(.*?)[-_]?(\d+(?:\.\d+)?|[2-9]?x[sl]|sm|md|lg|xl)$")
VAR_REF_RE = re.compile(r"^var\(\s*--([A-Za-z0-9_-]+)\s*(?:,\s*(.+))?\)$")
COLOR_VALUE_RE = re.compile(
    r"^(#[0-9a-f]{3,8}|(rgba?|hsla?|oklch|oklab|lab|lch|hwb|color-mix|color)\(|"
    r"(white|black|transparent|currentcolor)$)",
    re.IGNORECASE,
)
DIMENSION_RE = re.compile(r"^(0|-?[\d.]+(px|rem|em|%|vw|vh|vi|ch)|(clamp|calc|min|max)\(.*)$")
TIME_RE = re.compile(r"^[\d.]+m?s$|cubic-bezier\(|^(ease|linear)(\s|$|-in|-out)")
CHANNELS_RE = re.compile(r"^[\d.]+%?(\s*,\s*[\d.]+%?){2,3}$")


READ_ERRORS = []  # 读取失败的文件(不静默:进汇总与 --strict 退出码)


def read_source(path):
    """读一个文件,返回 [];HTML/Vue 只取样式面。失败记入 READ_ERRORS。"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        READ_ERRORS.append(path)
        print("   warn: 读取失败 %s: %s" % (path, exc), file=sys.stderr)
        return []
    if os.path.splitext(path)[1].lower() in (".html", ".htm", ".vue"):
        blocks = STYLE_BLOCK_RE.findall(text)
        if not blocks:
            return [(path, text)]
        return [("%s#style-%d" % (path, i), CSS_COMMENT_RE.sub("", b))
                for i, b in enumerate(blocks)]
    return [(path, CSS_COMMENT_RE.sub("", text))]


def extract_vars_from_css(css_text):
    """返回 [(name, value)];值内空白折叠为单空格。"""
    pairs = []
    for name, raw in CSS_VAR_RE.findall(css_text):
        pairs.append((name, " ".join(raw.split())))
    return pairs


def merge_uniq(pairs):
    """去重保序;同名不同值 → 首个为准,其余记入 alternatives。"""
    seen, overrides = {}, {}
    for name, value in pairs:
        if name not in seen:
            seen[name] = value
        elif seen[name] != value:
            overrides.setdefault(name, []).append(value)
    return seen, overrides


def resolve_alias(value, table, depth=0):
    """var() 别名递归解析到终值(深度上限 6,防环)。"""
    m = VAR_REF_RE.match(value.strip())
    if not m or depth > 6:
        return value
    target = table.get(m.group(1))
    if target is None:
        return m.group(2) or value
    return resolve_alias(target, table, depth + 1)


def categorize(name, value):
    """按名字/值启发式归类。"""
    lower = name.lower()
    if "radius" in lower or "rounded" in lower:
        return "radius"
    if ("shadow" in lower or "elevation" in lower) and not COLOR_VALUE_RE.match(value):
        return "shadow"
    if "breakpoint" in lower or "screen-" in lower:
        return "breakpoint"
    if lower.startswith("z-") or "-z-" in lower or "z-index" in lower or "zindex" in lower:
        return "z-index"
    if COLOR_VALUE_RE.match(value):
        return "color"
    if TIME_RE.search(value) or "duration" in lower or "ease" in lower:
        return "duration"
    if any(h in lower for h in ("padding", "margin", "gap", "space", "inset")) and DIMENSION_RE.match(value):
        return "spacing"
    if any(h in lower for h in ("font", "leading", "tracking", "line-height", "letter", "weight",
                                "text-", "heading", "title", "display", "body")):
        return "typography"
    if DIMENSION_RE.match(value):
        return "spacing"
    for category, hints in CATEGORY_HINTS:
        for hint in hints:
            if hint in lower:
                return category
    return "other"


def is_noise(name, value):
    """框架管道 / 噪声值:只进 JSON,不进摘要。"""
    if name.lower().startswith(NOISE_PREFIXES):
        return True
    if CHANNELS_RE.match(value):
        return True
    return len(value) > 90 or "{" in value or value in ("initial", "inherit", "unset", "")


def section_lines(items, overrides, seen):
    """把一组变量折叠成行:≥3 个成员的 <stem>-<步进> 数字阶梯折成一行。"""
    scales, singles = {}, []
    for name, value in items.items():
        m = SCALE_RE.match(name)
        if m and m.group(1):
            scales.setdefault(m.group(1), []).append((m.group(2), name, value))
        else:
            singles.append((name, value))
    for stem, members in list(scales.items()):
        if len(members) < 3:
            singles.extend((n, v) for _, n, v in members)
            del scales[stem]

    lines = []
    ranked = sorted(scales.items(), key=lambda kv: (
        not any(h in kv[0].lower() for h in SEMANTIC_HINTS + ("gray", "grey", "neutral")),
        -len(kv[1]),
    ))
    for stem, members in ranked:
        steps = " ".join("%s=%s" % (step, value) for step, _n, value in members)
        themed = any(n in overrides for _s, n, _v in members)
        lines.append("- --%s-*: %s%s" % (stem, steps,
                                         "  (redefined elsewhere, likely a theme)" if themed else ""))
    singles.sort(key=lambda nv: (not any(h in nv[0].lower() for h in SEMANTIC_HINTS), len(nv[0])))
    for name, value in singles:
        alt = overrides.get(name)
        alt_note = ""
        if alt:
            alt_note = "  | alt: %s (redefined elsewhere, likely a theme)" % resolve_alias(alt[0], seen)
        lines.append("- --%s: %s%s" % (name, value, alt_note))
    return [line if len(line) <= 200 else line[:197] + "..." for line in lines]


def build_digest(seen, overrides, sources, full_path, budget):
    """按类别配额生成摘要;超预算丢弃的行数显式披露。"""
    kept = {n: v for n, v in seen.items() if not is_noise(n, v)}
    by_category = {}
    for name, value in kept.items():
        resolved = resolve_alias(value, seen)
        by_category.setdefault(categorize(name, resolved), {})[name] = resolved

    out = [
        "# CSS 自定义属性提取:%d 个变量 / %d 个来源" % (len(seen), len(sources)),
        "%d 个框架管道或噪声变量已隐藏,var() 别名已解析为终值。完整 JSON 已保存到 %s;"
        "查更多用 --grep 'border|radius'(不再重扫),不要整读该文件。" % (len(seen) - len(kept), full_path),
    ]
    carry, dropped = 0, 0
    for category, share in DIGEST_SHARES:
        items = by_category.get(category)
        allowance = int(budget * share) + carry
        if not items:
            carry = allowance
            continue
        lines = section_lines(items, overrides, seen)
        out.append("\n## %s (%d)" % (category, len(items)))
        used = 0
        for i, line in enumerate(lines):
            if used + len(line) + 1 > allowance:
                dropped += len(lines) - i
                out.append("- (+%d 行因预算省略)" % (len(lines) - i))
                break
            out.append(line)
            used += len(line) + 1
        carry = max(0, allowance - used)
    if dropped:
        out.append("\n因 %d 字符预算省略了 %d 行;调大 --budget 或用 --grep 就地检索。"
                   % (budget, dropped))
    return "\n".join(out), dropped


def grep_saved(json_path, pattern, budget):
    """就地检索上次保存的 JSON(不重扫源文件)。"""
    if not os.path.exists(json_path):
        return "%s 不存在;先带路径跑一次提取。" % json_path
    try:
        with open(json_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return "读取 %s 失败: %s" % (json_path, exc)
    seen, overrides = {}, {}
    for items in data.get("tokens", {}).values():
        for name, info in items.items():
            seen[name] = info["value"]
            if info.get("alternatives"):
                overrides[name] = info["alternatives"]
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as exc:
        return "正则无效: %s" % exc
    matches = [n for n in seen if regex.search(n)]
    lines, used = [], 0
    for i, name in enumerate(matches):
        alt = overrides.get(name)
        line = "--%s: %s" % (name, resolve_alias(seen[name], seen))
        if alt:
            line += "  | alt: %s" % resolve_alias(alt[0], seen)
        line = line if len(line) <= 200 else line[:197] + "..."
        if used + len(line) > budget:
            lines.append("(+%d 个匹配被预算省略;缩小 pattern)" % (len(matches) - i))
            break
        lines.append(line)
        used += len(line) + 1
    return "\n".join(lines) if lines else "没有变量名匹配 /%s/(%s)。" % (pattern, json_path)


def collect_sources(paths):
    """展开输入为文件列表;返回 (files, missing)。"""
    files, missing = [], []
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = sorted(d for d in dirs if d not in ("node_modules", ".git", "dist", "build"))
                for name in sorted(names):
                    if name.lower().endswith(SCAN_EXTENSIONS):
                        files.append(os.path.join(root, name))
        else:
            missing.append(path)
    return files, missing


def _main_extract_tokens(argv=None):
    parser = argparse.ArgumentParser(
        description="本地样式源码的 CSS 自定义属性提取器:数字阶梯折叠 / 别名解析 / "
                    "主题重定义标注 / 框架管道隐藏 / 预算披露(退出码见 scripts/EXIT-CODES.md)"
    )
    parser.add_argument("paths", nargs="*", help="CSS/HTML/Vue 文件或目录(可多个)")
    parser.add_argument("--output", "-o", default="./css-vars.json",
                        help="完整 JSON 落点(默认 ./css-vars.json)")
    parser.add_argument("--budget", type=int, default=6000,
                        help="打印摘要的字符上限(默认 6000,约 1.5-2k tokens)")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="把完整 JSON 打到 stdout(不写文件;大文件慎用)")
    parser.add_argument("--grep", metavar="REGEX", default=None,
                        help="检索上次保存的 JSON(按变量名,别名已解析;无需路径)")
    parser.add_argument("--pretty", action="store_true", help="JSON 文件缩进输出(默认紧凑)")
    parser.add_argument("--strict", action="store_true", help="有告警时也以 1 退出")
    args = parser.parse_args(argv)

    if args.grep:
        print(grep_saved(args.output, args.grep, args.budget))
        return 0

    warnings = []
    if not args.paths:
        print("UNMEASURED: 没有输入路径。提取器需要至少一个 CSS/HTML/Vue 文件或目录。")
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2

    files, missing = collect_sources(args.paths)
    if missing:
        print("UNMEASURED: 路径不存在: " + ", ".join(missing))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2
    if not files:
        print("UNMEASURED: 输入里没有可提取的样式文件(扩展名白名单: %s)。"
              % "/".join(SCAN_EXTENSIONS))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2

    all_pairs, sources = [], []
    for path in files:
        for source_name, css in read_source(path):
            pairs = extract_vars_from_css(css)
            if pairs:
                sources.append(source_name)
                all_pairs.extend(pairs)

    seen, overrides = merge_uniq(all_pairs)
    if not seen:
        print("UNMEASURED: %d 个文件里没有找到任何 --var 定义。" % len(files))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2

    grouped = {}
    for name, value in seen.items():
        category = categorize(name, resolve_alias(value, seen))
        grouped.setdefault(category, {})[name] = {
            "value": value,
            "source": "css-custom-property",
        }
        if name in overrides:
            grouped[category][name]["alternatives"] = overrides[name]
    output = {
        "tokens": grouped,
        "_meta": {
            "sources": sources,
            "source_count": len(sources),
            "total_variables": len(seen),
            "note": "作者有意命名的显式 CSS 自定义属性;design-md 1A 提取中按高置信度候选处理,"
                    "类别为启发式,用途须人工复核。",
        },
    }

    if args.as_json:
        print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
        return 1 if (args.strict and (warnings or READ_ERRORS)) else 0

    out_path = os.path.abspath(args.output)
    try:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
    except OSError as exc:
        print("UNMEASURED: 无法写入完整 JSON(%s): %s" % (out_path, exc))
        print("收据写不出来就当作未记录,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2

    digest, dropped = build_digest(seen, overrides, sources, out_path, args.budget)
    print(digest)
    if dropped:
        warnings.append("摘要因预算省略 %d 行" % dropped)
    print("")
    print("提取结果: %d 个变量 / %d 个来源;%d 行因预算省略。"
          % (len(seen), len(sources), dropped))
    if READ_ERRORS:
        warnings.append("%d 个文件读取失败(未计入提取):%s"
                        % (len(READ_ERRORS), ", ".join(READ_ERRORS[:5])))

    if args.strict and (warnings or READ_ERRORS):
        for w in warnings:
            print("[WARN] " + w)
        return 1
    return 0


# ============================================================
# 来源节: dark-palette-derive.py (子命令: derive-dark)

# ---- 原 dark-palette-derive.py 模块说明 ----
"""暗色调色板确定性派生引擎。

从一套亮色调色板行(color-palettes.md 的 10 色列)确定性派生暗色模式行:
- 品牌色(Primary/Secondary/Accent/Destructive)原样保留,不换色相;
- 表面色(Background/Card/Muted/Border/Foreground)固定 slate 系,不从品牌色派生;
- Ring 按对暗底对比度 >= 3:1 自动选(品牌色组内择优,均不达标则逐步提亮 Primary);
- 已是暗色的行直接命中返回(passthrough),不重派生;
- 输出 _mode_derivation 溯源字段,记录每列的处理方式与 Ring 决策依据。

依赖: Python 3 标准库(无第三方依赖)。
用法(键不区分大小写,值必填):
    python3 dark-palette-derive.py Primary=#2563EB Background=#F8FAFC ...
"""
# ---- 模块说明结束 ----
import json
import sys

# 调色板 10 色列,与 color-palettes.md 表头一致
COLUMNS = (
    "Primary", "Secondary", "Accent", "Background", "Foreground",
    "Card", "Muted", "Border", "Destructive", "Ring",
)

# 品牌色列(派生时原样保留)与表面色列(固定 slate 系)
BRAND_COLUMNS = ("Primary", "Secondary", "Accent", "Destructive")

# 表面色固定 slate 系(与 color-palettes.md 暗色行既有取值一致)
SLATE_SURFACES = {
    "Background": "#020617",  # slate-950
    "Card": "#0F172A",        # slate-900
    "Muted": "#1E293B",       # slate-800
    "Border": "#334155",      # slate-700
    "Foreground": "#F8FAFC",  # slate-50
}

# Ring 对暗底的非文本 UI 组件对比度阈值(WCAG 1.4.11)
RING_MIN_CONTRAST = 3.0

# 已是暗色的判定阈值:Background 相对亮度低于该值视为暗色行
DARK_LUMINANCE_THRESHOLD = 0.2

# Ring 提亮的白混步长(确定性:从 5% 起每步 +5%)
LIGHTEN_STEP = 0.05


# ---------------------------------------------------------------------------
# 基础色度计算(WCAG 相对亮度与对比度)
# ---------------------------------------------------------------------------

def hex_to_rgb(color):
    """'#RRGGBB' -> (r, g, b),非法输入抛 ValueError。"""
    text = color.strip().lstrip("#")
    if len(text) != 6:
        raise ValueError(f"非法 hex 颜色: {color!r}(需要 #RRGGBB)")
    try:
        return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"非法 hex 颜色: {color!r}")


def relative_luminance(color):
    """WCAG 相对亮度(共享实现见 maliang_common,阈值 0.04045)。"""
    import maliang_common
    return maliang_common.relative_luminance(
        tuple(v / 255.0 for v in hex_to_rgb(color)))


def contrast_ratio(color_a, color_b):
    """两色的 WCAG 对比度,恒 >= 1(共享实现见 maliang_common)。"""
    import maliang_common
    return maliang_common.contrast_ratio_hex(color_a, color_b)


def is_dark(color):
    """暗色判定:相对亮度低于 DARK_LUMINANCE_THRESHOLD。"""
    return relative_luminance(color) < DARK_LUMINANCE_THRESHOLD


def _mix_toward_white(color, ratio):
    """把颜色向白色按比例混合(0=原色,1=纯白),返回 hex。"""
    mixed = tuple(round(c + (255 - c) * ratio) for c in hex_to_rgb(color))
    return "#%02X%02X%02X" % mixed


# ---------------------------------------------------------------------------
# 派生引擎
# ---------------------------------------------------------------------------

def validate_row(row):
    """校验行数据:10 列齐全且均为合法 hex,缺失/非法抛 ValueError。"""
    missing = [name for name in COLUMNS if not row.get(name)]
    if missing:
        raise ValueError(f"调色板行缺列: {', '.join(missing)}")
    for name in COLUMNS:
        hex_to_rgb(row[name])


def _pick_ring(row, dark_bg):
    """从品牌色组按优先序选对暗底 >=3:1 的 Ring;均不达标则确定性提亮 Primary。

    返回 (ring_hex, 溯源说明)。
    """
    candidates = [row[name] for name in ("Primary", "Accent", "Secondary", "Destructive")]
    seen = []
    for color in candidates:
        if color in seen:
            continue
        seen.append(color)
        ratio = contrast_ratio(color, dark_bg)
        if ratio >= RING_MIN_CONTRAST:
            return color, f"kept(对比 {ratio:.2f}:1)"
    base = row["Primary"]
    steps = int(round(1.0 / LIGHTEN_STEP))
    for i in range(1, steps + 1):
        candidate = _mix_toward_white(base, i * LIGHTEN_STEP)
        if contrast_ratio(candidate, dark_bg) >= RING_MIN_CONTRAST:
            return candidate, f"elevated:Primary+白混{round(i * LIGHTEN_STEP * 100)}%"
    raise ValueError("Ring 提亮至纯白仍不达标,暗底色值异常")  # 理论不可达,显性失败


def derive_dark_palette(row):
    """从一套调色板行派生暗色模式行,返回含 _mode_derivation 的新 dict。

    已是暗色(Background 相对亮度 < 阈值)的行直接命中返回原值,不重派生。
    """
    validate_row(row)
    result = dict(row)
    bg_lum = relative_luminance(row["Background"])

    if is_dark(row["Background"]):
        result["_mode_derivation"] = {
            "mode": "passthrough",
            "background_luminance": round(bg_lum, 4),
            "note": "已是暗色行,直接命中不重派生",
        }
        return result

    dark_bg = SLATE_SURFACES["Background"]
    ring, ring_note = _pick_ring(row, dark_bg)
    derivation = {
        "mode": "derived",
        "background_luminance": round(bg_lum, 4),
        "columns": {name: "kept(品牌色)" for name in BRAND_COLUMNS},
    }
    for name, hex_value in SLATE_SURFACES.items():
        result[name] = hex_value
        derivation["columns"][name] = f"slate-fixed:{hex_value}"
    result["Ring"] = ring
    derivation["columns"]["Ring"] = ring_note
    result["_mode_derivation"] = derivation
    return result


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def _parse_args(argv):
    row = {}
    for arg in argv:
        if "=" not in arg:
            raise ValueError(f"参数格式应为 列名=hex: {arg!r}")
        key, value = arg.split("=", 1)
        row[key.strip().capitalize()] = value.strip()
    return row


def _main_derive_dark(argv):
    try:
        row = _parse_args(argv)
        print(json.dumps(derive_dark_palette(row), ensure_ascii=False, indent=2))
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    return 0


# ============================================================
# 来源节: validate-design-md.py (子命令: validate)

# ---- 原 validate-design-md.py 模块说明 ----
"""DESIGN.md token 溯源机械化核对(V1–V3 四处交叉 + token.md 派生一致性)。

用法:
    python3 scripts/validate-design-md.py <DESIGN.md> [--token-file PATH]
                                               [--format {text,json}]

四处交叉(全部要求顶层键层,不要求逐字段):
  1. V2 孤儿 token —— colors / typography / rounded / spacing / components 的
     顶层键必须带溯源注释:`# D-P<n>-<m>` 或 `# no-decision: <来源>`;
  2. V1 悬空溯源 —— 注释里的 id 必须能在 `decisions` 账本里查到;
  3. V3 空原则 —— `## Overview` 声明的每条原则(P1/P2/P3 标记,或 decisions
     id 里出现过的原则号)至少要有一个 token 引用它;
  4. no-decision 占比 —— 超过 1/3 的 token 键写 no-decision 时警告:说明这次
     没做定义阶段,应回 Phase 0,而不是把 no-decision 铺满当通过;
  5. data-floor 绑定表形态(机械化子集)—— 文内出现绑定表(header 含
     「字段」+「写入方」)时校验:六列无空格、写入方为四规范值之一、
     integration 行须带 exists_today、day 1/2/7 台词标记在场(缺标记降
     WARN——写法变体不误杀,结构违规是 ERROR)。无绑定表 = 无数据型
     hook 声明,本检查不触发(G29 的产品判型仍归人工)。

派生一致性:token.md 里的每个 token 必须能追回 DESIGN.md 的 frontmatter
(按类别前缀映射 key,或值本身出现在 DESIGN.md 中);跨文件命名漂移在此拦截。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        显式传入的 --token-file 不存在 → 没能检查,退出码 2。
依赖: Python 3 标准库(+ 可选 PyYAML;复用 scripts/design_md_to_token_md.py 的
      frontmatter 提取逻辑)。
      判据文案对齐 references/meta/token-provenance.md §4/§5。
"""
# ---- 模块说明结束 ----
import argparse
import json
import os
import re
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)



TRACE_BLOCKS = ("colors", "typography", "rounded", "spacing", "components")
ID_RE = re.compile(r"\bD-P(\d+)-(\d+)\b")
NO_DECISION_RE = re.compile(r"no-decision\s*:", re.IGNORECASE)
DECISION_ID_RE = re.compile(r"-\s*id\s*:\s*([A-Za-z0-9._-]+)")
TOKEN_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
SECTION_RE = re.compile(r"^##\s+\d+\.\s*(.+)$")

SECTION_CATEGORY = (
    ("颜色", "colors"), ("字体", "typography"), ("间距", "spacing"),
    ("圆角", "radius"), ("分割线", "border"), ("边框", "border"), ("图标", "icon"),
)

PREFIX_TO_CATEGORY = (
    ("font-size-", ("typography", "fontSize")),
    ("font-weight-", ("typography", "fontWeight")),
    ("line-height-", ("typography", "lineHeight")),
    ("letter-spacing-", ("typography", "letterSpacing")),
    ("font-family-", ("typography", "fontFamily")),
    ("radius-", ("rounded", None)),
    ("spacing-", ("spacing", None)),
    ("color-", ("colors", None)),
)

HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
RGB_RE = re.compile(r"rgba?\([^)]*\)", re.IGNORECASE)

# 交叉 5:data-floor 绑定表(data-floor.md §2 六列;写入方四规范值 §3)
BINDING_HEADER_REQUIRED = ("字段", "写入方")
BINDING_WRITERS = ("user", "derived", "system", "integration")
BINDING_WRITER_RE = re.compile(r"\b(user|derived|system|integration)\b", re.IGNORECASE)
BINDING_EXISTS_TODAY_RE = re.compile(r"exists_today|今天已存在", re.IGNORECASE)
BINDING_SEP_RE = re.compile(r"^\|[\s\-:|]+\|?\s*$")
BINDING_CELL_COUNT = 6  # 字段/读什么/写入方/何时写/第一天空/断连日


def _day_marker_re(n):
    """day N 台词标记:day N / dayN / 第 N 天;n=1 另容「第一天」。"""
    variants = [r"day\s*%d\b" % n, r"第\s*%d\s*天" % n]
    if n == 1:
        variants.append("第一天")
    return re.compile("|".join(variants), re.IGNORECASE)


def check_data_floor_binding(text):
    """交叉 5:绑定表形态机械化子集(判型仍归 G29 人工)。

    返回 findings(dict:line/severity/rule/message,severity=ERROR/WARN);
    文内无绑定表时返回 [](不触发)。
    """
    findings = []
    lines = text.split("\n")
    table = None  # (header_line_no, [列名])
    for i, raw in enumerate(lines):
        if "|" not in raw:
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if (all(col in cells for col in BINDING_HEADER_REQUIRED)
                and i + 1 < len(lines) and BINDING_SEP_RE.match(lines[i + 1].strip())):
            table = (i + 1, cells)
            break
    if table is None:
        return findings
    header_line, header_cells = table
    col_of = {name: header_cells.index(name) for name in header_cells if name}
    for i in range(header_line + 1, len(lines)):
        row = lines[i].strip()
        if not row.startswith("|"):
            break
        if BINDING_SEP_RE.match(row):
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if not any(cells):
            continue
        # 六列无空格(header 列数不足六列时按实际列数判空格)
        for idx, cell in enumerate(cells):
            if not cell:
                col_name = header_cells[idx] if idx < len(header_cells) else "第%d列" % (idx + 1)
                findings.append({
                    "line": i + 1, "severity": "ERROR",
                    "rule": "design-md.binding-empty-cell",
                    "message": "绑定表「%s」列为空(data-floor §2:有空格即不批准)" % col_name,
                })
        writer = cells[col_of["写入方"]] if "写入方" in col_of and col_of["写入方"] < len(cells) else ""
        if writer and not BINDING_WRITER_RE.search(writer):
            findings.append({
                "line": i + 1, "severity": "ERROR",
                "rule": "design-md.binding-writer",
                "message": "绑定表写入方须为 user/derived/system/integration 之一(data-floor §3): "
                           + writer,
            })
        if writer and "integration" in writer.lower():
            row_text = "|".join(cells)
            if not BINDING_EXISTS_TODAY_RE.search(row_text):
                findings.append({
                    "line": i + 1, "severity": "ERROR",
                    "rule": "design-md.binding-integration",
                    "message": "integration 行缺 exists_today/今天已存在 声明(data-floor §3:"
                               "字段只有当集成真建了才存在;今天不存在的离场进 depends_on)",
                })
    for n in (1, 2, 7):
        if not _day_marker_re(n).search(text):
            findings.append({
                "line": 0, "severity": "WARN",
                "rule": "design-md.binding-day-missing",
                "message": "未检测到 day %d 台词标记(data-floor §5:day 1/2/7 写全,进 spec;"
                           "允许写法 day 1/第 1 天/第一天;若已写请对齐标记,未写按 G29 人工复核)" % n,
            })
    return findings


# ---------------------------------------------------------------------------
# frontmatter 原始行解析(带注释;与 design_md_to_token_md._strip_comment 同规则)
# ---------------------------------------------------------------------------

def _split_line_comment(raw):
    """把一行 YAML 拆成 (代码, 行尾注释);引号内的 # 不算注释。"""
    out, quote, i = [], None, 0
    while i < len(raw):
        ch = raw[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < len(raw):
                out.append(raw[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "#" and (i == 0 or raw[i - 1] in " \t"):
            return "".join(out).rstrip(), raw[i + 1:].strip()
        out.append(ch)
        i += 1
    return "".join(out).rstrip(), ""


def _indent_of(line):
    return len(line) - len(line.lstrip())


def parse_token_comments(yaml_str):
    """扫描 frontmatter 五个块的顶层键,返回 [(块, 键, 行号, 注释)].

    行号为 frontmatter 内相对行号(调用方补正文偏移)。
    """
    entries = []
    block = None
    child_indent = None
    for i, raw in enumerate(yaml_str.split("\n"), 1):
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = _indent_of(raw)
        code, comment = _split_line_comment(raw)
        stripped = code.strip()
        if indent == 0:
            m = re.match(r"^([A-Za-z_][\w-]*)\s*:(.*)$", stripped)
            block = m.group(1) if m and m.group(1) in TRACE_BLOCKS else None
            child_indent = None
            continue
        if block is None:
            continue
        if child_indent is None:
            child_indent = indent
        if indent != child_indent:
            continue
        m = re.match(r"^([A-Za-z0-9._-]+)\s*:(.*)$", stripped)
        if not m:
            continue
        key = m.group(1)
        # 值里的内联映射不算顶层键(仅当本行就是该键的子块起点)
        entries.append((block, key, i, comment))
    return entries


def parse_decision_ids(yaml_str):
    """从 decisions 块收集 id 列表,返回 [(id, 行号)]。"""
    ids = []
    in_decisions = False
    for i, raw in enumerate(yaml_str.split("\n"), 1):
        if re.match(r"^decisions\s*:", raw):
            in_decisions = True
            continue
        if in_decisions:
            if raw and _indent_of(raw) == 0 and raw.strip():
                in_decisions = False
                continue
            m = DECISION_ID_RE.search(raw)
            if m:
                ids.append((m.group(1), i))
    return ids


# ---------------------------------------------------------------------------
# frontmatter 结构化解析(供 token.md 派生一致性用)
# ---------------------------------------------------------------------------

def _normalize_literal(value):
    v = re.sub(r"\s+", "", str(value).lower())
    if re.fullmatch(r"#[0-9a-f]{3,4}", v):
        v = "#" + "".join(c * 2 for c in v[1:])
    return v


def collect_design_values(data):
    """收集 DESIGN.md frontmatter 里的键集合与字面值集合(归一化)。"""
    keys = {block: set() for block in TRACE_BLOCKS}
    literals = set()
    for block in TRACE_BLOCKS:
        node = data.get(block)
        if isinstance(node, dict):
            keys[block] = set(node.keys())
    raw_text = json.dumps(data, ensure_ascii=False, default=str)
    for m in HEX_RE.finditer(raw_text):
        literals.add(_normalize_literal(m.group(0)))
    for m in RGB_RE.finditer(raw_text):
        literals.add(_normalize_literal(m.group(0)))
    return keys, literals


def _key_matches(name, keys):
    """名字与键的匹配:精确,或 `brand-primary` 这类后缀 nibble 命中 `primary`。"""
    if name in keys:
        return True
    return any(name.endswith("-" + k) for k in keys if k)


CATEGORY_TO_BLOCK = {
    "colors": "colors", "typography": "typography",
    "spacing": "spacing", "radius": "rounded",
}


def check_token_md(token_text, keys, literals):
    """token.md 里的 token 能追回 DESIGN.md 吗?返回 findings。"""
    findings = []
    category = None
    lines = token_text.split("\n")
    table_sep_re = re.compile(r"^\|[\s\-:|]+\|?\s*$")
    for i, raw in enumerate(lines, 1):
        m = SECTION_RE.match(raw.strip())
        if m:
            title = m.group(1)
            category = next((cat for hint, cat in SECTION_CATEGORY if hint in title), None)
            continue
        if category in (None, "border", "icon"):
            continue
        row = TABLE_ROW_RE.match(raw.strip())
        if not row:
            continue
        if i < len(lines) and table_sep_re.match(lines[i].strip()):
            continue  # 表头行(下一行是分隔行)
        cells = [c.strip() for c in row.group(1).split("|")]
        if len(cells) < 2:
            continue
        name = cells[0].strip("`* ")
        if not TOKEN_NAME_RE.match(name):
            continue  # 表头 / 分隔行 / 说明行
        value = cells[1].strip()
        block = CATEGORY_TO_BLOCK.get(category)
        traceable = _key_matches(name, keys.get(block, set())) if block else False
        if not traceable:
            for prefix, (prefixed_block, _field) in PREFIX_TO_CATEGORY:
                if name.startswith(prefix):
                    if _key_matches(name[len(prefix):], keys.get(prefixed_block, set())):
                        traceable = True
                    break
        if not traceable and value:
            for lit in HEX_RE.finditer(value):
                if _normalize_literal(lit.group(0)) in literals:
                    traceable = True
            for lit in RGB_RE.finditer(value):
                if _normalize_literal(lit.group(0)) in literals:
                    traceable = True
        if not traceable:
            findings.append({
                "line": i, "rule": "design-md.token-untraceable",
                "message": "token.md 的 `%s` 追不回 DESIGN.md(类别 %s 里没有对应键,值也不在 DESIGN.md 中)"
                           " —— 跨文件命名漂移,回 design-md 补 token 或改回已登记名" % (name, category),
            })
    return findings


# ---------------------------------------------------------------------------
# 主检查
# ---------------------------------------------------------------------------

def analyze(design_path, token_path=None, token_explicit=False):
    """返回 (findings, warnings, unmeasured_reason)。findings/warnings 为 dict 列表。"""
    findings = []
    warnings = []
    try:
        with open(design_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        return [], [], "读取 DESIGN.md 失败: %s" % exc

    yaml_str, body = extract_frontmatter(text)
    if not yaml_str.strip():
        return [], [], "DESIGN.md 没有 frontmatter(--- 开头/结尾的 YAML 块),无法核对溯源"
    data = parse_frontmatter(yaml_str)
    if not isinstance(data, dict):
        return [], [], "frontmatter 解析结果不是 map"

    body_offset = text.find(yaml_str)  # frontmatter 起始行
    comment_entries = parse_token_comments(yaml_str)
    decisions = parse_decision_ids(yaml_str)
    decision_ids = {d for d, _line in decisions}

    # 交叉 1:顶层键必须有 id 或 no-decision(V2)
    no_decision_count = 0
    referenced_ids = {}
    for block, key, line, comment in comment_entries:
        id_m = ID_RE.search(comment or "")
        if id_m:
            referenced_ids.setdefault(id_m.group(0), (block, key, line))
        elif NO_DECISION_RE.search(comment or ""):
            no_decision_count += 1
        else:
            findings.append({
                "line": line, "rule": "design-md.orphan-token",
                "message": "V2 孤儿 token:%s.%s 既无溯源 id(# D-P<n>-<m>)也无 # no-decision: <来源>"
                           % (block, key),
            })

    # 交叉 2:id 必须能在 decisions 里查到(V1)
    for id_str, (block, key, line) in sorted(referenced_ids.items(), key=lambda kv: kv[1][2]):
        if id_str not in decision_ids:
            findings.append({
                "line": line, "rule": "design-md.dangling-provenance",
                "message": "V1 悬空溯源:%s.%s 指向 %s,但 decisions 账本里查不到该 id"
                           % (block, key, id_str),
            })

    # 交叉 3:每条原则至少被一个 token 引用(V3)
    overview = re.search(r"^##\s+Overview\s*$(.*?)(?=^##\s|\Z)", body, re.DOTALL | re.MULTILINE)
    declared = set()
    if overview:
        declared.update(int(m) for m in re.findall(r"(?<![A-Za-z0-9])P(\d+)(?![0-9])", overview.group(1)))
        declared.update(int(m) for m in re.findall(r"原则\s*(\d+)", overview.group(1)))
    else:
        warnings.append({
            "line": 0, "rule": "design-md.overview-missing",
            "message": "未找到 ## Overview 节,V3 空原则无法机械判定",
        })
    for id_str in decision_ids:
        m = ID_RE.fullmatch(id_str.strip())
        if m:
            declared.add(int(m.group(1)))
    referenced_principles = set()
    for id_str in referenced_ids:
        m = ID_RE.fullmatch(id_str.strip())
        if m:
            referenced_principles.add(int(m.group(1)))
    if declared:
        for principle in sorted(declared):
            if principle not in referenced_principles:
                findings.append({
                    "line": 0, "rule": "design-md.empty-principle",
                    "message": "V3 空原则:P%d 没有任何 token 的溯源注释指向它"
                               " —— 让原则落到至少一个 token 上,或从 Overview 删掉" % principle,
                })
    if referenced_principles - declared:
        for principle in sorted(referenced_principles - declared):
            warnings.append({
                "line": 0, "rule": "design-md.principle-unlisted",
                "message": "token 引用了 P%d,但 Overview 没有声明该原则编号(编号漂移?)" % principle,
            })

    # 交叉 4:no-decision 占比
    total_keys = len(comment_entries)
    if total_keys and no_decision_count / total_keys > 1.0 / 3.0:
        warnings.append({
            "line": 0, "rule": "design-md.no-decision-ratio",
            "message": "no-decision 占比 %d/%d 超过 1/3:这次没做定义阶段,应回 Phase 0,"
                       "而不是把 no-decision 铺满当通过" % (no_decision_count, total_keys),
        })

    # 行号基准(frontmatter 起始前的行数;findings 的行号统一按「相对
    # frontmatter」存储,末尾统一 +base 还原为绝对行号)
    base = text[:body_offset].count("\n")

    # 交叉 5:data-floor 绑定表形态(机械化子集;判型仍归 G29 人工)。
    # 本交叉直接扫全文,行号已是绝对值:ERROR 进 findings 须预扣 base
    # (末尾统一 +base 还原),WARN 进 warnings 不做偏移。
    for item in check_data_floor_binding(text):
        entry = {"line": item["line"], "rule": item["rule"], "message": item["message"]}
        if item["severity"] == "ERROR":
            if entry["line"] > 0:
                entry["line"] -= base
            findings.append(entry)
        else:
            warnings.append(entry)

    # 派生一致性:token.md → DESIGN.md
    if token_path:
        if not os.path.isfile(token_path):
            if token_explicit:
                return findings, warnings, "token 文件不存在: " + token_path
            warnings.append({
                "line": 0, "rule": "design-md.token-missing",
                "message": "同目录未找到 token.md,跳过派生一致性核对(--token-file 可显式指定)",
            })
        else:
            with open(token_path, "r", encoding="utf-8") as fh:
                token_text = fh.read()
            keys, literals = collect_design_values(data)
            for item in check_token_md(token_text, keys, literals):
                findings.append({
                    "line": 0, "rule": item["rule"],
                    "message": "%s:%d %s" % (os.path.basename(token_path), item["line"], item["message"]),
                })

    # 行号还原:frontmatter 相对行号 → 文件绝对行号(yaml_str 前一行的 --- 计 1 行)
    for item in findings:
        if item["line"] > 0:
            item["line"] += base
    return findings, warnings, None


def _main_validate(argv=None):
    parser = argparse.ArgumentParser(
        description="DESIGN.md 溯源核对:V1 悬空 / V2 孤儿 / V3 空原则 / "
                    "no-decision 占比 / data-floor 绑定表形态 + token.md 派生一致性"
                    "(退出码见 scripts/EXIT-CODES.md)"
    )
    parser.add_argument("design_md", help="DESIGN.md 路径")
    parser.add_argument("--token-file", default=None,
                        help="产物层 token.md 路径(默认取 DESIGN.md 同目录的 token.md)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式: text(人类可读,默认) / json")
    args = parser.parse_args(argv)

    design_path = os.path.abspath(args.design_md)
    token_explicit = args.token_file is not None
    token_path = os.path.abspath(
        args.token_file or os.path.join(os.path.dirname(design_path), "token.md"))

    def _cannot_check(message):
        if args.format == "json":
            print(json.dumps({"status": "unmeasured", "reason": message, "findings": []},
                             ensure_ascii=False))
        else:
            print("UNMEASURED: " + message)
            print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2

    if not os.path.isfile(design_path):
        return _cannot_check("DESIGN.md 不存在: " + design_path)

    findings, warnings, unmeasured = analyze(design_path, token_path, token_explicit)
    if unmeasured:
        return _cannot_check(unmeasured)

    if args.format == "json":
        print(json.dumps({
            "file": design_path,
            "findings": [
                {"line": f["line"], "severity": "ERROR", "rule": f["rule"], "message": f["message"]}
                for f in sorted(findings, key=lambda f: (f["line"], f["rule"]))
            ],
            "warnings": [
                {"line": w["line"], "severity": "WARN", "rule": w["rule"], "message": w["message"]}
                for w in warnings
            ],
        }, ensure_ascii=False, indent=2))
    else:
        print("maliang DESIGN.md 溯源核对 —— " + design_path)
        print("=" * 40)
        for f in sorted(findings, key=lambda f: (f["line"], f["rule"])):
            pos = (":%d" % f["line"]) if f["line"] else ""
            print("[ERROR]%s [%s] %s" % (pos, f["rule"], f["message"]))
        for w in warnings:
            pos = (":%d" % w["line"]) if w["line"] else ""
            print("[WARN] %s [%s] %s" % (pos, w["rule"], w["message"]))
        print("")
        print("=" * 40)
        print("检查结果: %d errors, %d warnings" % (len(findings), len(warnings)))
        print("退出码: " + ("1" if findings else "0"))

    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
