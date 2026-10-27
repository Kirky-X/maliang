#!/usr/bin/env python3
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

import argparse
import json
import os
import re
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import design_md_to_token_md as dmt  # noqa: E402  (复用 extract/parse_frontmatter)

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

    yaml_str, body = dmt.extract_frontmatter(text)
    if not yaml_str.strip():
        return [], [], "DESIGN.md 没有 frontmatter(--- 开头/结尾的 YAML 块),无法核对溯源"
    data = dmt.parse_frontmatter(yaml_str)
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


def main(argv=None):
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
    sys.exit(main(sys.argv[1:]))
