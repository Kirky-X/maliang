#!/usr/bin/env python3
"""maliang 脚本共用工具模块。

提供 parse_frontmatter() 等共享函数,供 validate-draw-md.py 和 ui-graph.py 共用。
依赖: Python 3 标准库(无第三方依赖)。
"""

import re


# ---------------------------------------------------------------------------
# Frontmatter 解析
# ---------------------------------------------------------------------------

# frontmatter 边界匹配(--- 开头和结尾)
_FRONTMATTER_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*", re.DOTALL)

# 键值对匹配(key: value)
_KV_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")

# 多行字符串续行(以 2+ 空格开头的行)
_CONTINUATION_RE = re.compile(r"^  \s+(.*)$")


def parse_frontmatter(text):
    """从 markdown 文本提取 YAML frontmatter(增强版,支持多行字符串)。

    支持格式:
    - 简单 key: value(顶层)
    - 多行字符串(value 以 > 或 | 开头,后续缩进行为续行)
    - inline 数组 [a, b, c](解析为 list)
    - 引号包裹的字符串(自动去引号)

    返回 dict: 字段名 -> 原始值(components 为 list,其他为 str)。
    无 frontmatter 返回空 dict。
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}

    result = {}
    current_key = None
    current_value_lines = []
    in_multiline = False

    for line in m.group(1).split("\n"):
        # 检查是否是新键值对
        kv_match = _KV_RE.match(line)
        if kv_match and not line.startswith("  "):
            # 先保存前一个多行值
            if in_multiline and current_key:
                result[current_key] = "\n".join(current_value_lines).strip()
                in_multiline = False
                current_key = None
                current_value_lines = []

            key = kv_match.group(1).strip()
            value = kv_match.group(2).strip()

            # 检查是否多行开始(> 或 |)
            if value in (">", "|", ">-", "|-", ">+", "|+"):
                current_key = key
                current_value_lines = []
                in_multiline = True
                continue

            current_key = key
            # 解析值
            if key == "components":
                result[key] = _parse_inline_list(value)
            else:
                result[key] = _strip_quotes(value)
        elif in_multiline:
            # 多行续行
            stripped = line.strip()
            if stripped:
                current_value_lines.append(stripped)
        elif line.strip() == "" and current_key:
            # 空行结束多行
            if in_multiline:
                result[current_key] = "\n".join(current_value_lines).strip()
                in_multiline = False
                current_key = None
                current_value_lines = []

    # 处理最后一个多行值
    if in_multiline and current_key:
        result[current_key] = "\n".join(current_value_lines).strip()

    return result


def _parse_inline_list(value):
    """解析 inline YAML 数组 `[a, b, c]` 为 list。

    支持格式:[a, b, c] / [a,b,c] / [ a , b ] / []。
    非 `[...]` 格式时当作单元素 list(或空 list)。
    """
    v = value.strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]
    return [v] if v else []


def _strip_quotes(v):
    """去掉值两端的引号(单引号或双引号)。"""
    if len(v) >= 2 and (
        (v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")
    ):
        return v[1:-1]
    return v


# ---------------------------------------------------------------------------
# 表格解析共用
# ---------------------------------------------------------------------------

# markdown 表格分隔行(如 | --- | --- |)
TABLE_SEP_RE = re.compile(r"^\|[\s\-:|]+\|?\s*$")


def parse_table_rows(lines, header_predicate):
    """从 markdown 行列表中提取匹配 header_predicate 的表格行。

    header_predicate: 接收 header cells 列表,返回 bool。
    返回 list of (header_line_no, rows), rows = list of (line_no, cells)。
    """
    tables = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if (
            line.strip().startswith("|")
            and i + 1 < n
            and TABLE_SEP_RE.match(lines[i + 1])
        ):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header_predicate(header_cells):
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
