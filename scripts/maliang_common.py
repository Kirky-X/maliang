#!/usr/bin/env python3
"""maliang 脚本共享层(validate-draw-md / ui-graph / check-claims / 各验证脚本共用)。

职责面:①frontmatter 解析(含一层嵌套);②markdown 表格解析;③WCAG 对比度数学
(全库唯一实现);④lint-checks.json 规则引擎(check-claims canonical;skill_lint 为
vendored 自包含孪生副本,parity 测试守护);⑤「PyYAML 优先+降级」骨架。
依赖: Python 3 标准库(无第三方依赖)。
"""

import os
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


def strip_quotes(v):
    """去掉值两端的引号(单引号或双引号)。公开名;_strip_quotes 为兼容别名。"""
    return _strip_quotes(v)


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


# ---------------------------------------------------------------------------
# token.md 解析(产物层 token 名收集)
# ---------------------------------------------------------------------------

def parse_token_names(path):
    """从产物层 token.md 收集全部 token 名。

    遍历首列为 "token"(大小写不敏感)的表格 body 行,取首列 kebab-case 名
    (兼容 `{token-name}` 与 token-name 两种写法,剥反引号与花括号)。覆盖
    颜色/字号/图标/间距/圆角/边框及暗色模式表(同名去重)。单一实现:
    validate-draw-md(token 悬空检查)与 ui-graph(token-usage 反向索引)
    共用,防两处解析漂移。文件不存在返回空 set。
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
        if first.lower() == "token":
            in_token_table = True
            continue
        if TABLE_SEP_RE.match(line):
            continue
        if in_token_table and first:
            name = first.strip("`").strip("{}").strip()
            if name and re.fullmatch(r"[a-z][a-z0-9-]*", name):
                tokens.add(name)
    return tokens


# ---------------------------------------------------------------------------
# {token} 引用提取(单一实现:validate-draw-md 检查 1/21 与 ui-graph
# token-usage 共用,防「什么算 token 引用」三处判定漂移)
# ---------------------------------------------------------------------------

# {token-name} 引用形式(kebab-case)
TOKEN_REF_RE = re.compile(r"\{([a-z][a-z0-9-]*)\}")


def is_action_row(stripped_line):
    """判定(已 lstrip 的)行是否为参数表 action 行。

    action 行内的 {xxx} 是 URL/JS 模板参数(如 {input-value}),不是设计
    token——检查 1(悬空引用)、检查 21(裸名)与 ui-graph token-usage
    统一按本谓词跳过。
    """
    return stripped_line.startswith("| action") or stripped_line.startswith("|action")


def iter_token_refs(lines):
    """逐行产出 (line_no, [token 名]);action 行跳过(is_action_row)。

    lines 为 1-based 行号对应的可枚举文本(enumerate(lines, 1) 形态由调用方
    自选;本函数接受 (line_no, line) 对的迭代器,调用方保留行号控制权)。
    """
    for line_no, line in lines:
        stripped = line.lstrip()
        if is_action_row(stripped):
            continue
        yield line_no, TOKEN_REF_RE.findall(line)


# ---------------------------------------------------------------------------
# WCAG 对比度数学(全库唯一实现)
# ---------------------------------------------------------------------------

# 线性化阈值:WCAG 2.1 / sRGB 标准值 0.04045。对全部 8-bit 量化通道值,
# 与 WCAG 2.0 旧值 0.03928 结果全等(见 tests/test_maliang_common.py 回归断言);
# 仅在不取整的浮点 alpha 合成路径上两者有差——全库统一采用标准值。
WCAG_LINEAR_THRESHOLD = 0.04045


def srgb_to_linear(c):
    """单通道 sRGB → 线性光。c 为 0-1 浮点;阈值见 WCAG_LINEAR_THRESHOLD。"""
    return c / 12.92 if c <= WCAG_LINEAR_THRESHOLD else ((c + 0.055) / 1.055) ** 2.4


def hex_to_rgb255(hex_color):
    """'#RRGGBB'(可省 #)→ (r, g, b) 0-255 整数三元组;非法输入抛 ValueError。"""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        raise ValueError("expected 6-digit hex, got %r" % hex_color)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def blend_alpha(fg, bg):
    """前景按 alpha 合成到背景上,返回 (r, g, b) 0-1 浮点(不取整,保留精度)。

    fg/bg 为 0-255 分量序列;fg 可含第 4 位 alpha(0-1 浮点),缺省视为 1.0。
    """
    a = fg[3] if len(fg) > 3 else 1.0
    if a >= 1.0:
        return tuple(fg[i] / 255.0 for i in range(3))
    return tuple((fg[i] * a + bg[i] * (1 - a)) / 255.0 for i in range(3))


def relative_luminance(rgb01):
    """WCAG 相对亮度:L = 0.2126R + 0.7152G + 0.0722B(线性光分量,0-1 浮点)。"""
    return 0.2126 * srgb_to_linear(rgb01[0]) + 0.7152 * srgb_to_linear(rgb01[1]) + 0.0722 * srgb_to_linear(rgb01[2])


def contrast_ratio(l1, l2):
    """两亮度的 WCAG 对比度,恒 >= 1。"""
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def contrast_ratio_hex(hex1, hex2):
    """六位 hex 颜色对的 WCAG 对比度便捷入口。"""
    l1 = relative_luminance(tuple(v / 255.0 for v in hex_to_rgb255(hex1)))
    l2 = relative_luminance(tuple(v / 255.0 for v in hex_to_rgb255(hex2)))
    return contrast_ratio(l1, l2)


# ---------------------------------------------------------------------------
# lint-checks.json 规则引擎(check-claims.py 的唯一实现)
#
# skill_lint.py 内联同语义实现,但它按 docstring 契约「自包含单文件、可 vendored
# 进兄弟仓 CI」,不依赖本模块——改引擎语义时两处联动;孪生一致性由
# tests/test_maliang_common.py 的 parity 测试守护(同一 fixture 两侧同判)。
# ---------------------------------------------------------------------------

# 引擎返回 findings 为 dict:{rule, severity, file, line, message};
# 配置/目标错误抛 ValueError(调用方各自决定 FAIL 还是退出码 2)。
# 消息词表同时覆盖两端的既有断言(计数漂移/声称/形同虚设/命中禁用表述/必现短语未满足)。
#
# 威胁模型:lint-checks.json 在 pull_request CI 中可被 PR 作者改写,因此
# pattern 视为不受信输入——_safe_compile 拒绝灾难回溯形状与超长正则(防 ReDoS),
# _engine_read 拒绝越出仓库的路径(防配置指路读仓外文件回显进日志)。

ENGINE_RULE_TYPES = ("count-matches", "forbid-pattern", "require-pattern", "consistency")

_MAX_PATTERN_LEN = 500
# 嵌套量词启发式:量词化的组内再含量词化组(如 (a+)+ / (\d+*) )*——灾难回溯的典型形状。
_NESTED_QUANT_RE = re.compile(r"\([^()]*[+*{][^()]*\)[+*{]")


def _safe_compile(pattern, flags=0):
    """受信边界内的 re.compile:配置正则视为不受信输入。

    拒绝:超长 pattern、嵌套量词启发式命中、非法正则(re.error 归一为
    ValueError,兑现引擎"配置错误抛 ValueError"的契约)。
    """
    if not isinstance(pattern, str) or len(pattern) > _MAX_PATTERN_LEN:
        raise ValueError(f"pattern 非法或超长(>{_MAX_PATTERN_LEN}): {pattern!r:.80}")
    if _NESTED_QUANT_RE.search(pattern):
        raise ValueError(f"pattern 含嵌套量词(灾难回溯风险),拒绝编译: {pattern!r}")
    try:
        return re.compile(pattern, flags)
    except re.error as exc:
        raise ValueError(f"非法正则 {pattern!r}: {exc}") from None


def _engine_read(repo, rel):
    """读仓库内目标文件;拒绝绝对路径与 .. 穿越(防配置指路读仓外文件)。"""
    if os.path.isabs(rel):
        raise ValueError(f"目标路径必须是仓库相对路径: {rel!r}")
    repo_real = os.path.realpath(repo)
    path = os.path.realpath(os.path.join(repo_real, rel))
    if path != repo_real and not path.startswith(repo_real + os.sep):
        raise ValueError(f"目标文件越出仓库: {rel!r}")
    if not os.path.isfile(path):
        raise ValueError(f"目标文件不存在: {rel}")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def section_slice(text, section):
    """截取 `section` 标题到下一个同级(或更高级)标题之间的文本。

    section 为 None 时原样返回;未命中抛 ValueError("section 未命中")。
    """
    if not section:
        return text
    m = re.match(r"^(#+)\s", section)
    level = len(m.group(1)) if m else 6
    stop_re = re.compile(r"^#{1,%d}\s" % level)
    lines = text.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if start is None and line.startswith(section):
            start = i
            continue
        if start is not None and stop_re.match(line):
            return "".join(lines[start:i])
    if start is None:
        raise ValueError(f"section 未命中: {section!r}")
    return "".join(lines[start:])


def _engine_read(repo, rel):
    path = os.path.join(repo, rel)
    if not os.path.isfile(path):
        raise ValueError(f"目标文件不存在: {rel}")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _engine_as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return []


def engine_count_matches(repo, rule):
    """count-matches:唯一来源行数 × 各声明文件里抓到的数字对账。"""
    findings = []
    severity = rule.get("severity", "FAIL")
    name = rule.get("name", "count-matches")
    source = rule.get("source")
    if not source:
        raise ValueError("count-matches 需要 source(唯一来源文件)")
    text = section_slice(_engine_read(repo, source), rule.get("section"))
    row_re = _safe_compile(rule.get("row_pattern", r"^\|\s*\["), re.MULTILINE)
    expected = len(row_re.findall(text))
    detail = source + (f" [{rule['section']}]" if rule.get("section") else "")
    patterns = _engine_as_list(rule.get("claim_pattern")) + _engine_as_list(rule.get("claim_patterns"))
    if not patterns:
        raise ValueError("count-matches 需要 claim_pattern 或 claim_patterns(抓声明的正则,须含一个捕获组)")
    min_claims = rule.get("min_claims", 1)
    if not isinstance(min_claims, int) or min_claims < 0:
        raise ValueError("min_claims 必须是 ≥0 的整数")
    seen = 0
    for rel in _engine_as_list(rule.get("claim_files")):
        body = _engine_read(repo, rel)
        for pattern in patterns:
            regex = _safe_compile(pattern)
            if regex.groups != 1:
                raise ValueError(f"claim_pattern 必须恰好一个捕获组: {pattern!r}")
            for m in regex.finditer(body):
                seen += 1
                number = int(m.group(1))
                if number != expected:
                    line_no = body.count("\n", 0, m.start()) + 1
                    findings.append({
                        "rule": name, "severity": severity, "file": rel, "line": line_no,
                        "message": (
                            f"{rel}:{line_no} 计数漂移:声称 {number}"
                            f"({' '.join(m.group(0).split())});唯一来源 {detail} 是 {expected}"
                        ),
                    })
    if seen < min_claims:
        findings.append({
            "rule": name, "severity": severity,
            "file": ",".join(_engine_as_list(rule.get("claim_files"))) or "(未配置)", "line": 0,
            "message": (
                f"一条声明都没抓到,规则形同虚设(min_claims={min_claims});"
                f"确认 claim_files/claim_patterns 仍对准公开声明(唯一来源 {detail} = {expected})"
            ),
        })
    return findings


def engine_forbid_pattern(repo, rule):
    """forbid-pattern:逐行匹配,命中即发现(ignore 正则豁免行)。"""
    findings = []
    severity = rule.get("severity", "FAIL")
    name = rule.get("name", "forbid-pattern")
    pattern = rule.get("pattern")
    if not pattern:
        raise ValueError("forbid-pattern 需要 pattern")
    regex = _safe_compile(pattern)
    ignore = _safe_compile(rule["ignore"]) if rule.get("ignore") else None
    for rel in _engine_as_list(rule.get("files")) or _engine_as_list(rule.get("file")):
        body = _engine_read(repo, rel)
        for line_no, line in enumerate(body.splitlines(), 1):
            if ignore and ignore.search(line):
                continue
            m = regex.search(line)
            if m:
                findings.append({
                    "rule": name, "severity": severity, "file": rel, "line": line_no,
                    "message": f"{rel}:{line_no} 命中禁用表述 {m.group(0)!r}",
                })
    return findings


def engine_require_pattern(repo, rule):
    """require-pattern:文件内必现短语计数对账。"""
    findings = []
    severity = rule.get("severity", "FAIL")
    name = rule.get("name", "require-pattern")
    rel = rule.get("file")
    pattern = rule.get("pattern")
    if not rel or not pattern:
        raise ValueError("require-pattern 需要 file 与 pattern")
    min_count = rule.get("min_count", 1)
    if not isinstance(min_count, int) or min_count < 1:
        raise ValueError("require-pattern 的 min_count 必须为 ≥1 整数(0/负数 = 形同虚设配置)")
    found = len(re.findall(pattern, _engine_read(repo, rel)))
    if found < min_count:
        findings.append({
            "rule": name, "severity": severity, "file": rel, "line": 0,
            "message": f"{rel} 必现短语未满足(命中 {found}/{min_count}): {pattern!r}",
        })
    return findings


def engine_consistency(repo, rule):
    """consistency:同一规范句跨文件逐字节一致(防手工联动漂移)。

    {"name": "draw fallback 行一致性", "type": "consistency",
     "files": ["a.md", "b.md"],        # 全部文件都必须命中 pattern
     "pattern": "^\\\\|.*缺失关键.*\\\\|$"}   # 每文件恰好一行命中(多行取首行)
    任一文件未命中 → FAIL;各行不完全一致 → FAIL(附各行内容)。
    """
    findings = []
    severity = rule.get("severity", "FAIL")
    name = rule.get("name", "consistency")
    files = _engine_as_list(rule.get("files"))
    pattern = rule.get("pattern")
    if len(files) < 2 or not pattern:
        raise ValueError("consistency 需要 files(≥2)与 pattern")
    regex = _safe_compile(pattern, re.MULTILINE)
    hits = {}
    for rel in files:
        body = _engine_read(repo, rel)
        ms = regex.findall(body)
        if not ms:
            findings.append({
                "rule": name, "severity": severity, "file": rel, "line": 0,
                "message": f"{rel} 未命中一致性 pattern(该文件缺规范句或 pattern 漂移): {pattern!r}",
            })
        else:
            hits[rel] = ms[0]
    if len({*hits.values()}) > 1:
        detail = "; ".join(f"{rel}={v!r}" for rel, v in sorted(hits.items()))
        findings.append({
            "rule": name, "severity": severity, "file": ",".join(files), "line": 0,
            "message": f"跨文件一致性漂移:同名规范句在各文件不一致——{detail}",
        })
    return findings


def engine_run_rule(repo, rule):
    """按 type 分发到共享引擎;未知 type 抛 ValueError。"""
    rtype = rule.get("type", "require-pattern")
    if rtype == "count-matches":
        return engine_count_matches(repo, rule)
    if rtype == "forbid-pattern":
        return engine_forbid_pattern(repo, rule)
    if rtype == "require-pattern":
        return engine_require_pattern(repo, rule)
    if rtype == "consistency":
        return engine_consistency(repo, rule)
    raise ValueError(f"未知 type: {rtype!r}")


# ---------------------------------------------------------------------------
# YAML frontmatter:「PyYAML 优先 + 降级」骨架(仓内 canonical;
# skill_lint 按 vendored 自包含契约保留同源副本)
# ---------------------------------------------------------------------------

def _parse_frontmatter_lines(block):
    """无 PyYAML 时的逐行降级解析:一层嵌套 map + 标量 + 续行拼接。

    一层嵌套子键(如 metadata.version)必须成 dict,否则 string→string
    校验会在无 PyYAML 环境误报(源自 skill_lint 的降级语义)。
    """
    data = {}
    key = None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m2 = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m2:
            key = m2.group(1)
            data[key] = m2.group(2).strip().strip("\"'")
        elif key and re.match(r"^\s+\S", line):
            m3 = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
            if m3:
                if not isinstance(data.get(key), dict):
                    data[key] = {}
                data[key][m3.group(1)] = m3.group(2).strip().strip("\"'")
            else:
                data[key] = (
                    f"{data[key]} {line.strip()}" if data.get(key) else line.strip()
                )
    return data


def load_yaml_block(block, fallback=None, on_not_map="error"):
    """「PyYAML 优先,缺失时降级」的唯一骨架。返回 (dict, error)。

    block 为 frontmatter 正文(不含 --- 围栏);fallback(block) 为无 PyYAML
    时的降级解析器,缺省用 _parse_frontmatter_lines。on_not_map:
    "error"(YAML 合法但非映射时报错,skill_lint 语义)或
    "empty"(静默按空 dict,design_md_to_token_md 语义)。
    """
    if not block.strip():
        return {}, None
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block)
        if not isinstance(data, dict):
            if on_not_map == "empty":
                return {}, None
            return None, "frontmatter 不是键值映射"
        return data, None
    except ImportError:
        if fallback is not None:
            return fallback(block), None
        return _parse_frontmatter_lines(block), None
    except Exception as exc:
        return None, f"frontmatter YAML 非法: {exc}"


def parse_frontmatter_lenient(block):
    """宽容解析 frontmatter 正文:PyYAML,报错或缺失时降级逐行解析。

    供消费「设计产物 frontmatter」的读取方使用(style-ledger 指纹提取等)
    ——真实产物常含 `"Fraunces", serif` 这类 PyYAML 严格语法拒收的值,
    逐行降级解析器可容忍。与 load_yaml_block 的差别:后者把 PyYAML 报错
    当失败返回(校验器语义),本函数把报错当「换宽容解析器」的信号。
    """
    data, err = load_yaml_block(block)
    if err:
        return _parse_frontmatter_lines(block)
    return data
