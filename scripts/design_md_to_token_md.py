#!/usr/bin/env python3
"""DESIGN.md -> 产物层 token.md 自动生成脚本。

用法:
    python3 scripts/design_md_to_token_md.py <input.md> <output.md>

依赖: Python 3 标准库 + PyYAML(可选,不可用时降级正则解析并打印警告)。
契约: 同一输入永远产出同一输出;RGBA 由 hex 计算,禁止硬编码颜色值。
"""
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

def extract_frontmatter(text):
    """从 markdown 提取 YAML frontmatter 与正文。返回 (yaml_str, body)。"""
    if not text.startswith("---"):
        return "", text
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)$", text, re.DOTALL)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def parse_frontmatter(yaml_str):
    """解析 frontmatter。优先 PyYAML,降级正则。返回 dict。"""
    if not yaml_str.strip():
        return {}
    try:
        import yaml
        data = yaml.safe_load(yaml_str)
        return data if isinstance(data, dict) else {}
    except ImportError:
        warn("PyYAML 不可用,降级使用正则解析 frontmatter(仅支持简单 map 结构)。")
        return parse_frontmatter_indent(yaml_str)


def _parse_scalar(val):
    """解析 YAML 标量:去引号/转数字,其余保留字符串。"""
    if val == "":
        return ""
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    try:
        if re.fullmatch(r"-?\d+", val):
            return int(val)
        if re.fullmatch(r"-?\d+\.\d+", val):
            return float(val)
    except (ValueError, TypeError):
        pass
    return val


def parse_frontmatter_indent(yaml_str):
    """基于缩进的降级解析器,支持两层 map + 标量(heritage 结构够用)。"""
    lines = yaml_str.split("\n")
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
    out.append("> 由 scripts/design_md_to_token_md.py 从 {} 自动生成。".format(input_name))
    out.append("> 手动修改会被下次生成覆盖。")
    out.append("")
    out.extend(render_colors(data))
    out.extend(render_typography(data))
    out.extend(render_icon())
    out.extend(render_spacing(data))
    out.extend(render_radius(data))
    out.extend(render_border(data))
    return "\n".join(out) + "\n"


def main(argv):
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
