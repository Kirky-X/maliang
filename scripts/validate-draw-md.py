#!/usr/bin/env python3
"""draw-md 产物文档规范性检查脚本。

用法:
    python3 scripts/validate-draw-md.py [target_dir] [--token-file PATH] [--framework-file PATH]

默认 target_dir = examples/ui-markdown/。
默认 token-file  = {target_dir}/token.md
默认 framework-file = references/framework/index.md
退出码: 0 = 全部通过; 1 = 有 error; 2 = 仅有 warning。
依赖: Python 3 标准库(无第三方依赖)。

检查项:
  1. 颜色/icon token 悬空引用(error)
  2. 颜色硬编码字面量(error)
  3. 组件类型字段缺失或自创 slug(error/warning)
  4. frontmatter 必填字段缺失(error)
  5. 章节顺序错误(warning,仅 ui/ 一级页面)
  6. 二级页面文件位置(error,仅 ui/ 直接子文件)
  7. 组件参数表缺 action 字段(error)
  8. 暗色模式 token 引用覆盖(warning)
  9. aria-label 可访问性(warning)
  10. 触控区 ≥44px(error)
  11. 动效 ≤400ms(error)
  12. 卡片 radius 违规(error)
"""
import argparse
import os
import re
import sys


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# frontmatter 必填字段
REQUIRED_FRONTMATTER_FIELDS = [
    "name", "description", "background", "updated", "version", "components",
]

# 已知二级页面 slug(直接放在 ui/ 根目录算 error,应放子目录如 ui/setting/)
SECONDARY_PAGE_SLUGS = {
    "about", "feedback", "privacy", "terms", "login", "signup",
    "forgot-password", "agreement", "about-us", "register", "reset-password",
}

# token 引用形式 {token-name}(kebab-case)
TOKEN_REF_RE = re.compile(r"\{([a-z][a-z0-9-]*)\}")

# 颜色字面量:#RRGGBBAA / #RRGGBB / #RGB / rgba(...) / rgb(...)
HEX_COLOR_RE = re.compile(r"#[0-9A-Fa-f]{8}\b|#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")
RGBA_COLOR_RE = re.compile(r"rgba?\([^)]*\)", re.IGNORECASE)

# markdown 表格分隔行(如 | --- | --- |)
TABLE_SEP_RE = re.compile(r"^\|[\s\-:|]+\|?\s*$")

# kebab-case 标识符
KEBAB_RE = re.compile(r"[a-z][a-z0-9-]*")

# 暗色 token 引用形式 {xxx-dark}
DARK_TOKEN_REF_RE = re.compile(r"\{[a-z][a-z0-9-]*-dark\}")

# 毫秒时长字面量 \d+ms
MS_DURATION_RE = re.compile(r"(\d+)ms")

# 像素尺寸字面量 \d+px
PX_VALUE_RE = re.compile(r"(\d+)px")

# 交互组件 slug(参数表需含 aria-label)
INTERACTIVE_SLUGS = {"button", "icon", "input", "link"}

# 可点击组件 slug(触控区需 ≥44px)
CLICKABLE_SLUGS = {"button", "icon", "link"}

# 触控区最小尺寸(px)
TOUCH_TARGET_MIN = 44


# ---------------------------------------------------------------------------
# 解析函数
# ---------------------------------------------------------------------------

def parse_token_file(path):
    """解析 token.md,提取所有 token 名。

    遍历所有 header 首列为 "token" 的表格,收集 body 行首列的 kebab-case 名。
    覆盖:颜色(color-*)/字号(font-*)/图标(icon-*)/间距(spacing-*)/
          圆角(radius-*)/边框(border-*)以及暗色模式表(同名去重)。
    返回 set of str;文件不存在返回空 set。
    """
    tokens = set()
    if not os.path.isfile(path):
        return tokens
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    in_token_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_token_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        first = cells[0] if cells else ""
        if first == "token":
            in_token_table = True
            continue
        if TABLE_SEP_RE.match(line):
            continue
        if in_token_table and first and KEBAB_RE.fullmatch(first):
            tokens.add(first)
    return tokens


def parse_framework_file(path):
    """解析 framework/index.md,提取所有组件 slug(共 45 类)。

    遍历所有 header 首列为 "组件类型" 的表格(现有 3 + P0 4 + P1 21 + P2 17),
    收集 body 行首列的 kebab-case slug。
    返回 set of str;文件不存在返回空 set。
    """
    slugs = set()
    if not os.path.isfile(path):
        return slugs
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    in_slug_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_slug_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        first = cells[0] if cells else ""
        if first == "组件类型":
            in_slug_table = True
            continue
        if TABLE_SEP_RE.match(line):
            continue
        if in_slug_table and first and KEBAB_RE.fullmatch(first):
            slugs.add(first)
    return slugs


def parse_frontmatter(text):
    """从 markdown 文本提取 YAML frontmatter(简单 flat 解析,无第三方依赖)。

    仅支持顶层 `key: value` 行;不处理嵌套/多行字符串。
    返回 dict: 字段名 -> 原始值字符串(去首尾空白,保留引号)。
    无 frontmatter 返回空 dict。
    """
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*", text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


def _strip_quotes(v):
    """去掉值两端的引号(单引号或双引号)。"""
    if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
        return v[1:-1]
    return v


def _extract_param_tables(lines):
    """提取所有"参数表"(header 含"参数"的 markdown 表)。

    返回 list of (header_line_no, rows),rows = list of (line_no, cells)。
    表的识别:某行以 | 开头,且下一行是分隔行;其 header 单元格含"参数"。
    """
    tables = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if "参数" in header_cells:
                rows = []
                j = i + 2
                while j < n and lines[j].strip().startswith("|"):
                    if TABLE_SEP_RE.match(lines[j]):
                        j += 1
                        continue
                    cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    rows.append((j + 1, cells))
                    j += 1
                tables.append((i + 1, rows))
                i = j
                continue
        i += 1
    return tables


def _extract_slugs_from_value(value):
    """从"组件类型"值单元格提取 slug 列表(反引号包裹的部分)。

    例: "`input` + `icon`(P0 + P1,组合:...)" -> ["input", "icon"]
        "`navigation`(P1,导航容器)"            -> ["navigation"]
    """
    return re.findall(r"`([^`]+)`", value)


# ---------------------------------------------------------------------------
# 检查函数(每个返回 list of (severity, file, line, message))
# ---------------------------------------------------------------------------

def check_token_references(rel_path, lines, valid_tokens):
    """检查 1:颜色/icon token 悬空引用(error)。

    扫描所有 {token-name} 形式引用,若 token 未在 token.md 定义则报 error。
    跳过 action 字段行(| action |...),因为其中的 {xxx} 通常是 URL 查询参数
    或 JS 模板占位符(如 {input-value}),不是设计 token。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        # 跳过 action 字段行(action 描述交互行为,{xxx} 是 URL/JS 占位符)
        stripped = line.lstrip()
        if stripped.startswith("| action") or stripped.startswith("|action"):
            continue
        for m in TOKEN_REF_RE.finditer(line):
            name = m.group(1)
            if name not in valid_tokens:
                results.append(("ERROR", rel_path, i,
                                "悬空 token 引用: {" + name + "}"))
    return results


def check_color_literals(rel_path, lines):
    """检查 2:颜色硬编码字面量(error)。

    扫描 #RRGGBB / #RGB / #RRGGBBAA / rgba() / rgb(),报 error。
    跳过表格分隔行。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        for m in HEX_COLOR_RE.finditer(line):
            results.append(("ERROR", rel_path, i,
                            "颜色硬编码字面量: " + m.group(0) + ",应引用 token"))
        for m in RGBA_COLOR_RE.finditer(line):
            results.append(("ERROR", rel_path, i,
                            "颜色硬编码字面量: " + m.group(0) + ",应引用 token"))
    return results


def check_component_slugs(rel_path, lines, valid_slugs):
    """检查 3:组件类型字段缺失或自创 slug(error/warning)。

    参数表(header 含"参数")无"组件类型"行 -> warning;
    组件类型值含不在 45 类中的 slug -> error。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            results.append(("WARN", rel_path, header_line,
                            "组件参数表缺'组件类型'字段"))
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        for slug in _extract_slugs_from_value(value):
            if slug not in valid_slugs:
                results.append(("ERROR", rel_path, line_no,
                                "自创组件 slug: " + slug +
                                ",应引用 framework/index.md 的 45 类"))
    return results


def check_frontmatter(rel_path, text):
    """检查 4:frontmatter 必填字段缺失(error);background 必须引用 token。"""
    results = []
    fm = parse_frontmatter(text)
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm or not fm[field]:
            results.append(("ERROR", rel_path, 0,
                            "frontmatter 缺失字段: " + field))
    bg = _strip_quotes(fm.get("background", ""))
    if bg and not TOKEN_REF_RE.search(bg):
        results.append(("ERROR", rel_path, 0,
                        "frontmatter background 未引用 token: " + bg))
    return results


def check_action_field(rel_path, lines):
    """检查 7:组件参数表缺 action 字段(error)。

    每个组件参数表(header 含"参数")MUST 含"action"行,描述组件交互行为
    五元组(tap/state/db/api/long-press;输入类可扩展 submit/focus/blur/input)。
    双列对比表(如 dock 选中/未选中态)的 action 在表内,首列应为 "action"。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        has_action = False
        for line_no, cells in rows:
            if cells and cells[0] == "action":
                has_action = True
                break
        if not has_action:
            results.append(("ERROR", rel_path, header_line,
                            "组件参数表缺 'action' 字段(交互行为五元组 tap/state/db/api/long-press)"))
    return results


def check_section_order(rel_path, lines):
    """检查 5:章节顺序错误(warning,仅 ui/ 一级页面)。

    第一章(首个 ## 标题)应含"导航"/"nav-bar";最后一章应含"dock"/"底部"。
    """
    results = []
    h2 = []
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^(#{2,3})\s+(.*)$", line)
        if m and m.group(1) == "##":
            h2.append((i, m.group(2).lower()))
    if not h2:
        return results
    first_title = h2[0][1]
    last_title = h2[-1][1]
    if not ("导航" in first_title or "nav-bar" in first_title or "nav" in first_title):
        results.append(("WARN", rel_path, h2[0][0],
                        "章节顺序: 第一章非导航"))
    if not ("dock" in last_title or "底部" in last_title):
        results.append(("WARN", rel_path, h2[-1][0],
                        "章节顺序: 最后一章非 dock"))
    return results


def check_secondary_pages(rel_path):
    """检查 6:二级页面文件位置(error,仅 ui/ 直接子文件)。

    若 ui/ 根目录下存在 about/feedback/privacy 等已知二级页面 slug 文件,
    报 error,建议放入子目录(如 ui/setting/<slug>.md)。
    """
    results = []
    m = re.match(r"^ui/([a-z0-9-]+)\.md$", rel_path)
    if not m:
        return results
    slug = m.group(1)
    if slug in SECONDARY_PAGE_SLUGS:
        suggested = "ui/setting/" + slug + ".md"
        results.append(("ERROR", rel_path, 0,
                        "二级页面应放在子目录: " + suggested))
    return results


def check_dark_mode_coverage(rel_path, lines, valid_tokens=None):
    """检查 8:暗色模式 token 引用覆盖(warning)。

    扫描含 -dark 后缀的 token 引用(正则 \\{xxx-dark\\}),
    0 引用则报 warning,提示暗色模式覆盖缺失(AUDIT-REPORT G01)。
    valid_tokens 参数为兼容现有 check_* 签名,本检查不依赖它。
    """
    results = []
    has_dark = False
    for line in lines:
        if DARK_TOKEN_REF_RE.search(line):
            has_dark = True
            break
    if not has_dark:
        results.append(("WARN", rel_path, 0,
                        "页面未引用任何 dark token,暗色模式覆盖缺失"))
    return results


def check_aria_labels(rel_path, lines):
    """检查 9:交互组件 aria-label 可访问性(warning)。

    识别交互组件参数表(组件类型含 button/icon/input/link 之一),
    检查参数表是否含 aria-label 字段,缺失返回 warning(AUDIT-REPORT G02)。
    容器组件(navigation 等)不检查。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        interactive = [s for s in slugs if s in INTERACTIVE_SLUGS]
        if not interactive:
            continue
        has_aria = False
        for _, row_cells in rows:
            if row_cells and "aria-label" in row_cells[0].lower():
                has_aria = True
                break
        if not has_aria:
            results.append(("WARN", rel_path, line_no,
                            "交互组件 " + "+".join(interactive) +
                            " 缺少 aria-label 字段"))
    return results


def check_touch_target(rel_path, lines):
    """检查 10:可点击组件触控区 ≥44px(error)。

    识别可点击组件(组件类型含 button/icon/link 之一),
    解析 width/height 字段(正则 \\d+px),<44px 返回 error(AUDIT-REPORT G03)。
    match-parent 跳过(非定值,继承父级)。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        if not any(s in CLICKABLE_SLUGS for s in slugs):
            continue
        for row_line_no, row_cells in rows:
            if not row_cells:
                continue
            field = row_cells[0].lower()
            if ("width" not in field and "height" not in field
                    and "宽度" not in field and "高度" not in field):
                continue
            row_value = row_cells[1] if len(row_cells) > 1 else ""
            if "match-parent" in row_value.lower():
                continue
            m = PX_VALUE_RE.search(row_value)
            if m:
                size = int(m.group(1))
                if size < TOUCH_TARGET_MIN:
                    results.append(("ERROR", rel_path, row_line_no,
                                    "可点击组件 " + str(size) +
                                    "px <44px,触控区不足"))
    return results


def check_motion_duration(rel_path, lines):
    """检查 11:动效 duration ≤400ms(error)。

    扫描 \\d+ms 模式,>400 返回 error(AUDIT-REPORT G06)。
    引用 token(如 {duration-slower})不含 \\d+ms,自然跳过。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        for m in MS_DURATION_RE.finditer(line):
            duration = int(m.group(1))
            if duration > 400:
                results.append(("ERROR", rel_path, i,
                                "动效 " + str(duration) +
                                "ms >400ms 硬约束违规"))
    return results


def check_card_radius(rel_path, lines):
    """检查 12:卡片组件 radius 违规(error)。

    扫描组件类型含 card 的参数表,检查 radius 字段,
    为 {radius-md} 返回 error,应用 {radius-lg}(AUDIT-REPORT G07)。
    {radius-full}/{radius-sm} 不报错。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        if not any("card" in s for s in slugs):
            continue
        for row_line_no, row_cells in rows:
            if not row_cells:
                continue
            field = row_cells[0].lower()
            if "radius" not in field and "圆角" not in field:
                continue
            row_value = row_cells[1] if len(row_cells) > 1 else ""
            if "{radius-md}" in row_value:
                results.append(("ERROR", rel_path, row_line_no,
                                "卡片组件使用 radius-md 违规,应用 radius-lg"))
    return results


# ---------------------------------------------------------------------------
# 文件收集与主流程
# ---------------------------------------------------------------------------

def collect_md_files(root):
    """递归收集 root 下所有 .md 文件(绝对路径),按路径排序。"""
    result = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".md"):
                result.append(os.path.join(dirpath, fn))
    return sorted(result)


def main(argv):
    parser = argparse.ArgumentParser(
        description="maliang draw-md 文档规范性检查")
    parser.add_argument("target_dir", nargs="?", default="examples/ui-markdown",
                        help="目标目录(默认 examples/ui-markdown)")
    parser.add_argument("--token-file", default=None,
                        help="token.md 路径(默认 {target_dir}/token.md)")
    parser.add_argument("--framework-file", default=None,
                        help="framework/index.md 路径(默认 references/framework/index.md)")
    args = parser.parse_args(argv[1:])

    target_dir = os.path.abspath(args.target_dir)
    token_file = os.path.abspath(args.token_file or os.path.join(target_dir, "token.md"))
    framework_file = os.path.abspath(
        args.framework_file or os.path.join(os.getcwd(), "references", "framework", "index.md"))

    # 头部输出
    print("maliang draw-md 文档规范性检查")
    print("=" * 32)
    print("目标目录: " + target_dir)
    print("Token 文件: " + token_file)
    print("Framework 文件: " + framework_file)
    print("")

    # 目录/文件存在性(缺失即终止,显性失败)
    if not os.path.isdir(target_dir):
        print("[ERROR] 目标目录不存在: " + target_dir)
        return 1
    if not os.path.isfile(token_file):
        print("[ERROR] token 文件不存在: " + token_file)
        return 1
    if not os.path.isfile(framework_file):
        print("[ERROR] framework 文件不存在: " + framework_file)
        return 1

    valid_tokens = parse_token_file(token_file)
    valid_slugs = parse_framework_file(framework_file)

    # 收集待检查文件
    ui_dir = os.path.join(target_dir, "ui")
    organisms_dir = os.path.join(target_dir, "organisms")
    ui_files = collect_md_files(ui_dir) if os.path.isdir(ui_dir) else []
    org_files = collect_md_files(organisms_dir) if os.path.isdir(organisms_dir) else []

    all_results = []

    def rel(path):
        return os.path.relpath(path, target_dir)

    # ui 文件:检查 1-4 + 7-12 全做;检查 5/6 仅直接子文件
    for abs_path in ui_files:
        rp = rel(abs_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.splitlines()
        all_results.extend(check_token_references(rp, lines, valid_tokens))
        all_results.extend(check_color_literals(rp, lines))
        all_results.extend(check_component_slugs(rp, lines, valid_slugs))
        all_results.extend(check_frontmatter(rp, text))
        all_results.extend(check_action_field(rp, lines))
        all_results.extend(check_dark_mode_coverage(rp, lines, valid_tokens))
        all_results.extend(check_aria_labels(rp, lines))
        all_results.extend(check_touch_target(rp, lines))
        all_results.extend(check_motion_duration(rp, lines))
        all_results.extend(check_card_radius(rp, lines))
        if os.path.dirname(rp) == "ui":
            all_results.extend(check_section_order(rp, lines))
            all_results.extend(check_secondary_pages(rp))

    # organisms 文件:检查 1-4 + 7-12
    for abs_path in org_files:
        rp = rel(abs_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.splitlines()
        all_results.extend(check_token_references(rp, lines, valid_tokens))
        all_results.extend(check_color_literals(rp, lines))
        all_results.extend(check_component_slugs(rp, lines, valid_slugs))
        all_results.extend(check_frontmatter(rp, text))
        all_results.extend(check_action_field(rp, lines))
        all_results.extend(check_dark_mode_coverage(rp, lines, valid_tokens))
        all_results.extend(check_aria_labels(rp, lines))
        all_results.extend(check_touch_target(rp, lines))
        all_results.extend(check_motion_duration(rp, lines))
        all_results.extend(check_card_radius(rp, lines))

    # 排序:error 先于 warn,再按 file、line
    severity_rank = {"ERROR": 0, "WARN": 1}
    all_results.sort(key=lambda r: (severity_rank.get(r[0], 9), r[1], r[2]))

    # 输出
    error_count = 0
    warn_count = 0
    for severity, file, line, msg in all_results:
        label = "[ERROR]" if severity == "ERROR" else "[WARN] "
        if line > 0:
            print("{} {}:{} {}".format(label, file, line, msg))
        else:
            print("{} {} {}".format(label, file, msg))
        if severity == "ERROR":
            error_count += 1
        else:
            warn_count += 1

    print("")
    print("=" * 32)
    print("检查结果: {} errors, {} warnings".format(error_count, warn_count))
    if error_count > 0:
        print("退出码: 1")
        return 1
    if warn_count > 0:
        print("退出码: 2")
        return 2
    print("退出码: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
