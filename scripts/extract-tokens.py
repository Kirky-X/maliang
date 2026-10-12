#!/usr/bin/env python3
"""本地样式源码的 CSS 自定义属性提取器(--var 设计 token 候选,上下文经济)。

用法:
    python3 scripts/extract-tokens.py <css/html/vue 文件或目录...>
    python3 scripts/extract-tokens.py <路径> --output ./css-vars.json   # 指定完整 JSON 落点
    python3 scripts/extract-tokens.py <路径> --budget 3000              # 压缩摘要字符预算
    python3 scripts/extract-tokens.py --grep 'border|radius'             # 检索上次保存的 JSON(不重扫)
    python3 scripts/extract-tokens.py <路径> --json                      # 全量 JSON 打到 stdout

设计纪律(来源:anydesign scripts/extract_css_vars.py,2026-10 吸收):
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
    """读一个文件,返回 [(来源名, CSS 文本)];HTML/Vue 只取样式面。失败记入 READ_ERRORS。"""
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


def main(argv=None):
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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
