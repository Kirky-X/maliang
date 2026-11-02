#!/usr/bin/env python3
"""ui-graph —— UI 关系管理与变更追踪脚本。

用法:
    python3 scripts/ui-graph.py <subcommand> [--target PATH] [options]

子命令:
    generate           生成 ui-relationships.json(页面层级 + 跳转关系)
    list-missing       列出跳转目标未生成对应 markdown 的清单
    check-nav          检测异常跳转(自指/循环/死链);--strict 时发现异常退 1,
                       默认 informational(EXIT-CODES.md 迁移登记,退 0)
    compute-hash       计算目标文件 sha256,写哈希基线(file 指纹)
    diff-hash          对比当前哈希与基线,输出 added/modified/deleted
    build-impl-map     构建 logical_ui ↔ preview_html ↔ framework_code 映射
    list-unimplemented  列出 status=missing 的未实现逻辑页面
    token-usage        生成 token-usage.json:token → 引用页面反向索引 + 孤儿
                       token 清单(供 DESIGN.md token 变更的波及分析;--token X
                       只看单个 token 的波及页面)
    check-sync         对比 draw-md 基线与实现基线,逐页输出同步状态
                       (in-sync / spec-ahead / code-drifted / diverged);
                       任一页失同步退 1,基线缺失退 2(先建基线)

哈希范围(--kind,compute-hash / diff-hash 共用):
    draw-md(默认)  构建产物的 .md 页面(.maliang/ui-markdown/,排除 token.md),
                    基线文件 ui-hash-state.json —— 供 critique backlog 指纹判定
                    (critique.md「指纹失效判定」,只管 draw-md 产物)使用;
    preview        预览产品物 + 取证清单(**.html + 截图 png/jpg/jpeg/webp/svg
                    + report.json 等 JSON 清单,排除 selection.json 与基线自身),
                    基线文件 preview-hash-state.json —— 供测量收据/证据链
                    (receipts.py)记录「被实测的预览状态」;与 draw-md 指纹分开,
                    两者不得混用同一基线文件。

默认 --target = .maliang/ui-markdown/。
所有 JSON 产出的相对路径均以 target_dir 为根目录。
依赖: Python 3 标准库(无第三方依赖)。
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime

# 共用模块(同目录下的 maliang_common.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maliang_common import parse_frontmatter as _shared_parse_frontmatter
from maliang_common import (  # noqa: F401 —— TOKEN_REF_RE 同时 re-export 供测试引用
    TOKEN_REF_RE,
    is_action_row,
    iter_token_refs,
    parse_token_names,
)


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# draw-md 的 token 锚点文件,非页面,parse_directory / compute-hash 均排除
TOKEN_FILE_NAME = "token.md"

# 本子命令产出的 JSON 文件,compute-hash 排除(避免自我污染)
UI_GRAPH_OUTPUT_FILES = {
    "ui-relationships.json",
    "ui-hash-state.json",
    "ui-implementation-map.json",
    "preview-hash-state.json",       # preview 指纹基线(--kind preview)
    "code-hash-state.json",          # 实现指纹基线(--kind code)
    "token-usage.json",              # token 引用反向索引(token-usage)
}

# preview 指纹范围:预览 HTML + 截图 + 取证清单;选择结果(selection.json)是交互记录不是产物
# code 指纹范围:ui-implementation-map.json 映射到的实现文件(preview HTML + 三框架代码),
# 路径相对 impl-map 的 anchors 锚根(preview_root/code_root)记录,消费侧按锚根
# 解析(不受运行时 cwd 影响),基线文件 code-hash-state.json —— 供 check-sync
# 判「规格改了代码没跟 / 代码手改了规格没动」;实现文件缺失时拒绝建基线
HASH_KINDS = ("draw-md", "preview", "code")
PREVIEW_HASH_STATE = "preview-hash-state.json"
CODE_HASH_STATE = "code-hash-state.json"
TOKEN_USAGE_FILE = "token-usage.json"
PREVIEW_SUFFIXES = (".html", ".htm", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".json")
PREVIEW_EXCLUDE_FILES = {"selection.json"}

# 默认 target 目录(相对脚本调用的工作目录)
DEFAULT_TARGET = ".maliang/ui-markdown"


# ---------------------------------------------------------------------------
# 解析函数
# ---------------------------------------------------------------------------

def parse_directory(target_dir):
    """扫描 target_dir 下所有 .md 文件,排除 token.md,返回相对路径列表(排序)。

    用 os.walk 递归遍历,返回相对 target_dir 的 POSIX 路径
    (如 'ui/setting/about.md'),跨平台统一用 '/' 分隔符。
    排除 token.md(draw-md 的 token 锚点,非页面)。
    target_dir 不存在时抛 FileNotFoundError(显性失败,不返回空列表假装成功)。
    """
    if not os.path.isdir(target_dir):
        raise FileNotFoundError("target_dir 不存在: " + target_dir)
    result = []
    for dirpath, _, filenames in os.walk(target_dir):
        for fn in filenames:
            if fn.endswith(".md") and fn != TOKEN_FILE_NAME:
                abs_path = os.path.join(dirpath, fn)
                rel = os.path.relpath(abs_path, target_dir)
                rel_posix = rel.replace(os.sep, "/")
                result.append(rel_posix)
    return sorted(result)


def parse_frontmatter(text):
    """从 markdown 文本提取 YAML frontmatter(委托共用模块,支持多行字符串)。

    仅支持顶层 `key: value` 行; components 字段(inline `[a, b, c]`)解析为 list;
    其他字段保留为字符串(保留引号)。
    返回 dict: 字段名 -> 值(components 为 list,其他为 str)。
    无 frontmatter 返回空 dict。
    """
    return _shared_parse_frontmatter(text)


# 提取 tap 跳转目标:tap=→<target> 或 tap→<target>(2026-10 补无等号变体,home.md 导航行实写)
# 支持:小写英文/驼峰/中文/连字符/斜杠/点号(遇空格/分号/竖线停止)
TAP_NAV_RE = re.compile(r"\btap=?→([^\s|;]+)")


def _normalize_target(raw):
    """归一化跳转目标为 ui/<to>.md;非页面目标(无/back/动作标识/URL)返回 None。"""
    raw = raw.strip().strip("`")
    raw = raw.rstrip("。；;，,")
    # 去掉尾注(如 "history.back(返回上一级)" 的括号说明)
    raw = re.sub(r"[（(][^）)]*[）)]$", "", raw).strip()
    if raw in ("", "无", "back", "history.back", "-"):
        return None
    if raw.startswith("history.back("):
        return None
    if raw.startswith(("action:", "http://", "https://")):
        return None
    if raw.startswith("ui/"):
        return raw if raw.endswith(".md") else raw + ".md"
    return "ui/" + raw + ".md"


def _extract_table_targets(text):
    """提取 markdown 表格中 target 列的跳转目标(金刚区/dock/about 的第三种声明形态)。

    仅当表头存在名为 target 的列时,逐数据行取该列归一化;
    字段定义表(表头为 字段/类型/…)无 target 列,天然不命中。
    """
    targets = []
    lines = text.splitlines()
    i = 0
    from maliang_common import TABLE_SEP_RE as _SEP
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and i + 1 < len(lines) and _SEP.match(lines[i + 1].strip()):
            header = [c.strip().strip("`").lower() for c in line.strip("|").split("|")]
            if "target" in header:
                col = header.index("target")
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    cells = lines[j].strip().strip("|").split("|")
                    if col < len(cells):
                        t = _normalize_target(cells[col])
                        if t:
                            targets.append(t)
                    j += 1
                i = j
                continue
            i += 2
            continue
        i += 1
    return targets


def extract_navigations(text, from_path=None):
    """提取文本中所有 tap 跳转关系,返回 [{'to':..., 'event':'tap'}]。

    两种声明形态:
    - 行内 action:`tap=→<target>` / `tap→<target>`
    - 表格 target 列(`tap=跳转至 item.target 声明页面` 的数据表)

    - 跳过 `无`/`back`(history.back,非具体页面)
    - 归一化为 ui/<to>.md 路径:
      * 原始值以 ui/ 开头且以 .md 结尾 → 保持原样
      * 原始值以 ui/ 开头但不以 .md 结尾 → 补 .md
      * 原始值不以 ui/ 开头 → ui/<raw>.md

    from_path 当前未使用(generate 聚合时添加 from 字段),保留参数以匹配
    T007 签名 extract_navigations(text, from_path)。
    """
    results = []
    seen = set()

    def _add(raw):
        to_path = _normalize_target(raw)
        if to_path and to_path not in seen:
            seen.add(to_path)
            results.append({"to": to_path, "event": "tap"})

    for m in TAP_NAV_RE.finditer(text):
        _add(m.group(1))
    for raw in _extract_table_targets(text):
        _add(raw)
    return results


def _derive_parent_and_depth(rel_path):
    """从相对路径推导 parent 与 depth。

    ui/home.md           → (None, 1)       # ui/ 直接子文件
    ui/setting/about.md  → ('setting', 2)  # ui/<dir>/ 子文件
    organisms/nav-bar.md → (None, 0)       # 非 ui/ 路径
    """
    parts = rel_path.split("/")
    if parts[0] != "ui":
        return (None, 0)
    depth = len(parts) - 1
    if depth >= 2:
        parent = parts[-2]
    else:
        parent = None
    return (parent, depth)


def _derive_name(rel_path, frontmatter):
    """从 frontmatter 提取 name,缺失时用文件名(去 .md)兜底。"""
    name = frontmatter.get("name")
    if name:
        return name
    return os.path.basename(rel_path).replace(".md", "")


def _now_iso():
    """当前时间的 ISO8601 字符串(含本地时区,微秒归零)。"""
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def generate(target_dir):
    """生成 ui-relationships.json:聚合 pages[] + navigations[]。

    流程:
    1. parse_directory(target_dir) → 所有 .md 相对路径
    2. 对每个文件:parse_frontmatter 提取 name/components,
       extract_navigations 提取跳转,_derive_parent_and_depth 推导层级
    3. 聚合为 {'generated_at', 'target_dir', 'pages[]', 'navigations[]'}
    4. 写入 {target_dir}/ui-relationships.json

    navigations[].source_component v1 暂为 None(后续可增强为参数表的
    "组件类型"字段值)。
    返回聚合 dict。
    """
    rel_paths = parse_directory(target_dir)
    pages = []
    navigations = []
    for rel_path in rel_paths:
        abs_path = os.path.join(target_dir, rel_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        parent, depth = _derive_parent_and_depth(rel_path)
        components = fm.get("components", [])
        if not isinstance(components, list):
            components = []
        pages.append({
            "path": rel_path,
            "name": _derive_name(rel_path, fm),
            "parent": parent,
            "depth": depth,
            "components": components,
        })
        for nav in extract_navigations(text, from_path=rel_path):
            navigations.append({
                "from": rel_path,
                "to": nav["to"],
                "event": nav["event"],
                "source_component": None,
            })
    result = {
        "generated_at": _now_iso(),
        "target_dir": target_dir,
        "pages": pages,
        "navigations": navigations,
    }
    out_path = os.path.join(target_dir, "ui-relationships.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


# ---------------------------------------------------------------------------
# token 引用提取(token-usage 反向索引;实现与 action 行跳过规则在
# maliang_common,与 validate-draw-md 检查 1/21 共享单一实现)
# ---------------------------------------------------------------------------


def extract_token_refs(text):
    """提取文本中全部 {token} 引用名(排除 action 行,规则见 maliang_common)。"""
    refs = []
    for _line_no, names in iter_token_refs(enumerate(text.splitlines(), 1)):
        refs.extend(names)
    return refs


def token_usage(target_dir, token_file=None, write=True):
    """生成 token-usage.json:token → 引用页面反向索引 + 孤儿 token 清单。

    数据源:parse_directory 的全部 .md(ui/ 页面 + organisms/,排除 token.md)
    + token.md 的 token 名(maliang_common.parse_token_names,单一实现)。
    用途:①DESIGN.md 改一个 token 后,机械回答「哪些页要重生成」;
    ②unreferenced 列表给 G02(孤儿 token)提供产物层信号。
    write=False 供 --token 只读查询使用(查询不产生写副作用)。
    返回 {'computed_at', 'target_dir', 'tokens', 'unreferenced'}。
    """
    rel_paths = parse_directory(target_dir)
    if token_file is None:
        token_file = os.path.join(target_dir, TOKEN_FILE_NAME)
    usage = {}
    for rel_path in rel_paths:
        with open(os.path.join(target_dir, rel_path), "r", encoding="utf-8") as f:
            refs = extract_token_refs(f.read())
        for name in sorted(set(refs)):
            usage.setdefault(name, []).append(rel_path)
    known = parse_token_names(token_file)
    unreferenced = sorted(known - set(usage))
    result = {
        "computed_at": _now_iso(),
        "target_dir": target_dir,
        "tokens": {k: sorted(v) for k, v in sorted(usage.items())},
        "unreferenced": unreferenced,
    }
    if write:
        out_path = os.path.join(target_dir, TOKEN_USAGE_FILE)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    return result


# ---------------------------------------------------------------------------
# JSON 加载辅助
# ---------------------------------------------------------------------------

def _load_relationships(target_dir):
    """加载 ui-relationships.json。缺失抛 FileNotFoundError(显性失败)。"""
    path = os.path.join(target_dir, "ui-relationships.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            "ui-relationships.json 不存在: " + path + ",请先运行 generate")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_impl_map(target_dir):
    """加载 ui-implementation-map.json。缺失抛 FileNotFoundError。"""
    path = os.path.join(target_dir, "ui-implementation-map.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            "ui-implementation-map.json 不存在: " + path + ",请先运行 build-impl-map")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# T009: list-missing
# ---------------------------------------------------------------------------

def list_missing(target_dir):
    """列出跳转目标未生成对应 markdown 的清单。

    对比 navigations[].to 与 pages[].path,返回 [{'from', 'to'}] 列表
    (to 不在 pages 路径集合中即为缺失)。
    """
    rel = _load_relationships(target_dir)
    page_paths = {p["path"] for p in rel.get("pages", [])}
    missing = []
    for nav in rel.get("navigations", []):
        if nav["to"] not in page_paths:
            missing.append({"from": nav["from"], "to": nav["to"]})
    return missing


# ---------------------------------------------------------------------------
# T010: check-nav
# ---------------------------------------------------------------------------

def check_nav(target_dir):
    """检测异常跳转,返回 {'self_refs', 'cycles', 'dead_links'}。

    - 自指:self_refs(from == to)
    - 循环:cycles(长度 2 的环 A→B 且 B→A,去重)
    - 死链:dead_links(to 不在 pages 路径集合中,且非自指)
    """
    rel = _load_relationships(target_dir)
    page_paths = {p["path"] for p in rel.get("pages", [])}
    navigations = rel.get("navigations", [])

    self_refs = []
    dead_links = []
    for nav in navigations:
        if nav["from"] == nav["to"]:
            self_refs.append(nav)
        elif nav["to"] not in page_paths:
            dead_links.append(nav)

    # 长度 2 的循环:A→B 且 B→A(去重,不重复报 B→A)
    nav_pairs = {(n["from"], n["to"]) for n in navigations if n["from"] != n["to"]}
    cycles = []
    seen = set()
    for (a, b) in nav_pairs:
        if (b, a) in nav_pairs:
            key = tuple(sorted([a, b]))
            if key not in seen:
                cycles.append({"a": a, "b": b})
                seen.add(key)

    return {"self_refs": self_refs, "cycles": cycles, "dead_links": dead_links}


# ---------------------------------------------------------------------------
# T011: compute-hash / diff-hash
# ---------------------------------------------------------------------------

def _parse_preview_directory(target_dir):
    """扫描 preview 指纹范围:HTML/截图/取证清单(排除选择记录与状态文件)。

    返回相对路径列表(排序,跨平台统一 '/' 分隔)。
    """
    if not os.path.isdir(target_dir):
        raise FileNotFoundError("target_dir 不存在: " + target_dir)
    result = []
    for dirpath, _, filenames in os.walk(target_dir):
        for fn in filenames:
            if not fn.lower().endswith(PREVIEW_SUFFIXES):
                continue
            if fn in PREVIEW_EXCLUDE_FILES or fn in UI_GRAPH_OUTPUT_FILES:
                continue
            abs_path = os.path.join(dirpath, fn)
            rel = os.path.relpath(abs_path, target_dir)
            result.append(rel.replace(os.sep, "/"))
    return sorted(result)


def _resolve_impl_path(impl, root_key, raw_path):
    """把 impl-map 记录的实现路径解析为绝对路径(锚定 + 边界校验)。

    锚定:优先用 impl.anchors[root_key](preview_root / code_root,路径记录
    基准);旧版 impl-map 无 anchors 时退回 base_dir/当前 cwd(legacy)。
    边界:拒绝绝对路径与含 .. 段的相对路径,且解析结果必须落在锚根之内
    ——impl-map 是仓库内可篡改文件,路径消费前必须校验,防存在性探测/
    越界读取(安全审查 M-1)。失败抛 ValueError(调用方按三态退 2)。
    """
    raw_norm = raw_path.replace("\\", "/")
    if os.path.isabs(raw_norm) or (
            len(raw_norm) >= 2 and raw_norm[0].isalpha() and raw_norm[1] == ":"):
        raise ValueError(
            "impl-map 记录了绝对路径(拒绝执行,防越界): " + raw_path)
    parts = raw_norm.split("/")
    if ".." in parts:
        raise ValueError(
            "impl-map 路径含 .. 穿越(拒绝执行,防越界): " + raw_path)
    anchors = impl.get("anchors") or {}
    root = anchors.get(root_key) or impl.get("base_dir") or os.getcwd()
    resolved = os.path.normpath(os.path.join(root, *parts))
    root_abs = os.path.abspath(root)
    if os.path.commonpath([resolved, root_abs]) != root_abs:
        raise ValueError(
            "impl-map 路径解析越出锚根 " + root_key + "(" + root_abs + "): "
            + raw_path)
    return resolved


def _impl_map_code_files(target_dir):
    """从 ui-implementation-map.json 收集被映射的实现文件(原始路径, 绝对路径)对。

    含 preview_html 与三框架 framework_code 的非空值,去重排序;绝对路径经
    _resolve_impl_path 锚定解析(base_dir)+ 边界校验。原始路径串作为基线
    JSON 的键(不落机器相关绝对路径,基线文件可入库);绝对路径仅用于读取。
    impl-map 缺失时 _load_impl_map 抛 FileNotFoundError(显性失败)。
    """
    impl = _load_impl_map(target_dir)
    pairs = set()
    for m in impl.get("mappings", []):
        if m.get("preview_html"):
            pairs.add((m["preview_html"],
                       _resolve_impl_path(impl, "preview_root", m["preview_html"])))
        for v in (m.get("framework_code") or {}).values():
            if v:
                pairs.add((v, _resolve_impl_path(impl, "code_root", v)))
    return sorted(pairs)


def _hash_paths(pairs, strict_missing=False):
    """对 (原始路径, 绝对路径) 对列表计算 sha256,条目键为原始路径。

    文件缺失:strict_missing=False 记 sha256=None + missing=True(不静默跳过);
    strict_missing=True(建基线)抛 FileNotFoundError——拒绝把含缺失的测量
    写成基线(架构审查 H1 失败链②:None==None 会伪造「全部 in-sync」)。
    """
    files = []
    for raw, abs_path in pairs:
        if os.path.isfile(abs_path):
            with open(abs_path, "rb") as f:
                content = f.read()
            files.append({
                "path": raw,
                "sha256": hashlib.sha256(content).hexdigest(),
                "size": len(content),
            })
        elif strict_missing:
            raise FileNotFoundError(
                "impl-map 映射的实现文件不存在: " + raw
                + "(拒绝建立含缺失的基线;先在正确目录重跑 build-impl-map,"
                  "或补齐实现文件)")
        else:
            files.append({"path": raw, "sha256": None, "missing": True})
    return files


def _hash_files(target_dir, kind):
    """按 --kind 收集并哈希目标文件,返回 (files, state_name)。"""
    if kind == "preview":
        rel_paths = _parse_preview_directory(target_dir)
        state_name = PREVIEW_HASH_STATE
    elif kind == "code":
        files = _hash_paths(_impl_map_code_files(target_dir), strict_missing=True)
        return files, CODE_HASH_STATE
    else:
        rel_paths = parse_directory(target_dir)
        state_name = "ui-hash-state.json"
    files = []
    for rel_path in rel_paths:
        abs_path = os.path.join(target_dir, rel_path)
        with open(abs_path, "rb") as f:
            content = f.read()
        files.append({
            "path": rel_path,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size": len(content),
        })
    return files, state_name


def _hash_scope_note(kind):
    if kind == "preview":
        return ("指纹范围: 预览 HTML + 截图 + 取证清单(preview-hash-state.json;"
                "与 critique 的 draw-md 产物指纹 ui-hash-state.json 区分)")
    if kind == "code":
        return ("指纹范围: impl-map 映射的实现文件(preview HTML + 三框架代码,"
                "code-hash-state.json;check-sync 的实现侧基线)")
    return "指纹范围: draw-md 产物 .md 页面(ui-hash-state.json;critique backlog 指纹判定用)"


def compute_hash(target_dir, kind="draw-md"):
    """按 --kind 计算目标文件 sha256,写对应基线状态文件。

    draw-md: parse_directory(排除 token.md);preview: HTML/截图/取证清单。
    返回 {'computed_at', 'target_dir', 'kind', 'files[]'}。
    """
    if kind not in HASH_KINDS:
        raise ValueError("未知 --kind: " + str(kind))
    files, state_name = _hash_files(target_dir, kind)
    result = {
        "computed_at": _now_iso(),
        "target_dir": target_dir,
        "kind": kind,
        "scope_note": _hash_scope_note(kind),
        "files": files,
    }
    out_path = os.path.join(target_dir, state_name)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


def diff_hash(target_dir, kind="draw-md"):
    """对比当前哈希与基线状态文件,返回 {'baseline_missing', 'added', 'modified', 'deleted'}。

    - baseline_missing: 历史快照不存在(True 时视为空基线,不作硬失败)
    - added: 当前存在但历史快照中没有
    - modified: 两边都有但 sha256 不同
    - deleted: 历史快照中有但当前不存在
    取值范围与 compute-hash 同 --kind 一致(draw-md / preview 各自独立基线)。
    无历史快照时视为空基线:全部当前文件计入 added,由调用方打印提示
    引导先跑 compute-hash(ui-graph.md 失败模式表约定,禁止静默吞掉)。
    """
    if kind not in HASH_KINDS:
        raise ValueError("未知 --kind: " + str(kind))
    files, state_name = _hash_files(target_dir, kind)
    current_files = {f["path"]: f["sha256"] for f in files}
    state_path = os.path.join(target_dir, state_name)
    baseline_missing = not os.path.isfile(state_path)
    old_files = {}
    if not baseline_missing:
        with open(state_path, "r", encoding="utf-8") as f:
            old_state = json.load(f)
        old_files = {f["path"]: f["sha256"] for f in old_state.get("files", [])}

    added = sorted([p for p in current_files if p not in old_files])
    modified = sorted([p for p in current_files
                       if p in old_files and old_files[p] != current_files[p]])
    deleted = sorted([p for p in old_files if p not in current_files])
    return {"baseline_missing": baseline_missing,
            "added": added, "modified": modified, "deleted": deleted}


# ---------------------------------------------------------------------------
# T012: build-impl-map
# ---------------------------------------------------------------------------

def _extract_slug(filename):
    """从文件名提取 slug(lowercase,去扩展名,去 preview_ 前缀)。

    preview_home.html → 'home'
    Home.ets          → 'home'
    home.dart         → 'home'
    home.vue          → 'home'
    """
    name, _ = os.path.splitext(filename)
    if name.startswith("preview_"):
        name = name[len("preview_"):]
    return name.lower()


def _logical_ui_slug(rel_path):
    """从逻辑 UI 路径提取 slug(basename 去 .md,lowercase)。

    ui/home.md           → 'home'
    ui/setting/about.md  → 'about'
    """
    return os.path.splitext(os.path.basename(rel_path))[0].lower()


def _scan_preview_html(preview_root):
    """扫描 preview_root 下所有 .html,返回 {slug: 相对 preview_root 路径}。"""
    result = {}
    if not preview_root or not os.path.isdir(preview_root):
        return result
    for dirpath, _, filenames in os.walk(preview_root):
        for fn in filenames:
            if fn.endswith(".html"):
                slug = _extract_slug(fn)
                abs_path = os.path.join(dirpath, fn)
                rel = os.path.relpath(abs_path, preview_root)
                result[slug] = rel.replace(os.sep, "/")
    return result


def _scan_framework_code(code_root):
    """扫描框架代码,返回 {'harmony': {}, 'flutter': {}, 'element': {}}。

    harmony: **/pages/<Slug>.ets
    flutter: **/pages/<slug>.dart
    element: **/views/<slug>.vue
    路径记录为相对 code_root(跨盘符 cwd 下 relpath 会抛错,相对各自根
    记录才稳定——锚点见 build_impl_map 的 anchors 字段)。
    """
    result = {"harmony": {}, "flutter": {}, "element": {}}
    if not code_root or not os.path.isdir(code_root):
        return result
    for dirpath, _, filenames in os.walk(code_root):
        # 路径转 POSIX 风格用于模式匹配
        dir_posix = (dirpath + "/").replace(os.sep, "/")
        for fn in filenames:
            slug = _extract_slug(fn)
            rel_path = os.path.relpath(os.path.join(dirpath, fn), code_root)
            rel_path = rel_path.replace(os.sep, "/")
            if fn.endswith(".ets") and "/pages/" in dir_posix:
                result["harmony"][slug] = rel_path
            elif fn.endswith(".dart") and "/pages/" in dir_posix:
                result["flutter"][slug] = rel_path
            elif fn.endswith(".vue") and "/views/" in dir_posix:
                result["element"][slug] = rel_path
    return result


def build_impl_map(target_dir, preview_root, code_root):
    """构建 ui-implementation-map.json。

    扫描 preview HTML + 框架代码(harmony/flutter/element),与
    ui-relationships.json 的 pages 匹配,写 ui-implementation-map.json。
    status: implemented(preview+framework 都有) / partial(只有一项) / missing(都无)。
    记录两个锚点字段,消费侧(check-sync / compute-hash --kind code)据此
    解析路径,不受消费时 cwd 影响(防跨目录运行的「假漂移/假同步」链):
    - base_dir:构建时工作目录的绝对路径(legacy 语义,兼容旧 impl-map)
    - anchors.preview_root / anchors.code_root:实现路径各自的记录基准根;
      preview_html 相对 preview_root,framework_code 相对 code_root
    """
    rel = _load_relationships(target_dir)
    pages = rel.get("pages", [])

    preview_map = _scan_preview_html(preview_root)
    fw_map = _scan_framework_code(code_root)

    mappings = []
    for page in pages:
        slug = _logical_ui_slug(page["path"])
        # preview 命名约定为 preview_<page-name>_<device>.html(preview.md 产出物),
        # 故 slug 精确相等或以 <slug>_ 设备后缀均视为匹配
        preview_html = None
        for pslug, ppath in preview_map.items():
            if pslug == slug or pslug.startswith(slug + "_"):
                preview_html = ppath
                break
        framework_code = {
            "harmony": fw_map["harmony"].get(slug),
            "flutter": fw_map["flutter"].get(slug),
            "element": fw_map["element"].get(slug),
        }
        has_preview = preview_html is not None
        has_framework = any(v is not None for v in framework_code.values())
        if has_preview and has_framework:
            status = "implemented"
        elif has_preview or has_framework:
            status = "partial"
        else:
            status = "missing"
        mappings.append({
            "logical_ui": page["path"],
            "preview_html": preview_html,
            "framework_code": framework_code,
            "status": status,
        })

    result = {
        "built_at": _now_iso(),
        "base_dir": os.getcwd(),
        "anchors": {
            "preview_root": os.path.abspath(preview_root) if preview_root else None,
            "code_root": os.path.abspath(code_root) if code_root else None,
        },
        "mappings": mappings,
    }
    out_path = os.path.join(target_dir, "ui-implementation-map.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


# ---------------------------------------------------------------------------
# T013: list-unimplemented
# ---------------------------------------------------------------------------

def list_unimplemented(target_dir):
    """列出 status=missing 的未实现逻辑页面。

    返回 [{'logical_ui', 'reason'}],reason = '无 preview_html 且无 framework_code'。
    """
    rel = _load_relationships(target_dir)
    impl = _load_impl_map(target_dir)
    page_paths = {p["path"] for p in rel.get("pages", [])}
    missing = []
    for m in impl.get("mappings", []):
        if m.get("status") == "missing" and m["logical_ui"] in page_paths:
            missing.append({
                "logical_ui": m["logical_ui"],
                "reason": "无 preview_html 且无 framework_code",
            })
    return missing


# ---------------------------------------------------------------------------
# T014: check-sync(规格 ↔ 实现同步状态)
# ---------------------------------------------------------------------------

def _sha256_file(path):
    """单文件 sha256;文件不存在返回 None(删除也是一种变更)。"""
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_sync(target_dir):
    """对比 draw-md 基线与实现基线,逐页输出同步状态。

    两个基线(缺任一即抛 FileNotFoundError,没能检查不假装通过):
    - ui-hash-state.json  规格侧基线(compute-hash 默认)
    - code-hash-state.json 实现侧基线(compute-hash --kind code;基线键为
      impl-map 原始路径,读取按 impl 的 base_dir 锚定解析——跨 cwd 运行
      不再产生假漂移/假同步)

    建基线节奏:每次全量产出/重生成后,先 build-impl-map,再连跑两个
    compute-hash——基线语义 = 「上次全部对齐时的快照」;基线建立时
    实现文件缺失即拒绝(compute-hash --kind code 抛 FileNotFoundError)。

    逐映射分类(仅 status != 'missing' 的页面):
    - in-sync       规格与实现均与基线一致
    - spec-ahead    规格已改、实现未跟 → 重跑 draw-*/preview 再建基线
    - code-drifted  实现已改(手改/外部变更/删除)、规格未动 → 回写规格或说明
    - diverged      两侧都变 → 先人工对齐再交付
    返回 {'checked_at', 'target_dir', 'statuses', 'summary'}。
    impl-map 记录绝对路径或 .. 穿越路径时抛 ValueError(边界校验,防越界)。
    """
    md_state_path = os.path.join(target_dir, "ui-hash-state.json")
    code_state_path = os.path.join(target_dir, CODE_HASH_STATE)
    for p, hint in (
        (md_state_path, "compute-hash"),
        (code_state_path, "compute-hash --kind code"),
    ):
        if not os.path.isfile(p):
            raise FileNotFoundError(
                "基线缺失: " + p + "(先运行 " + hint + " 建基线)")
    try:
        with open(md_state_path, "r", encoding="utf-8") as f:
            md_base = {x["path"]: x["sha256"]
                       for x in json.load(f).get("files", [])}
        with open(code_state_path, "r", encoding="utf-8") as f:
            code_base = {x["path"]: x["sha256"]
                         for x in json.load(f).get("files", [])}
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError("基线文件损坏,无法解析(" + str(exc) + ");"
                         "按三态属「没能检查」,重跑 compute-hash 重建基线")

    impl = _load_impl_map(target_dir)
    statuses = []
    for m in impl.get("mappings", []):
        if m.get("status") == "missing":
            continue
        logical = m["logical_ui"]
        cur_md = _sha256_file(os.path.join(target_dir, logical))
        base_md = md_base.get(logical)
        md_changed = cur_md != base_md
        raws = [(m.get("preview_html"), "preview_root")]
        raws.extend((v, "code_root")
                    for v in (m.get("framework_code") or {}).values())
        code_changed = False
        code_missing = []
        for raw, root_key in raws:
            if not raw:
                continue
            abs_path = _resolve_impl_path(impl, root_key, raw)
            cur = _sha256_file(abs_path)
            if cur is None:
                code_missing.append(raw)
            if cur != code_base.get(raw):
                code_changed = True
        if md_changed and code_changed:
            status = "diverged"
        elif md_changed:
            status = "spec-ahead"
        elif code_changed:
            status = "code-drifted"
        else:
            status = "in-sync"
        statuses.append({
            "logical_ui": logical,
            "status": status,
            "missing_files": code_missing,
        })
    summary = {}
    for s in statuses:
        summary[s["status"]] = summary.get(s["status"], 0) + 1
    return {
        "checked_at": _now_iso(),
        "target_dir": target_dir,
        "statuses": statuses,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(
        description="maliang UI 关系管理与变更追踪")
    parser.add_argument("subcommand",
                        choices=["generate", "list-missing", "check-nav",
                                 "compute-hash", "diff-hash",
                                 "build-impl-map", "list-unimplemented",
                                 "token-usage", "check-sync"],
                        help="子命令")
    parser.add_argument("--target", default=DEFAULT_TARGET,
                        help="目标目录(默认 " + DEFAULT_TARGET + ")")
    parser.add_argument("--preview-root", default=None,
                        help="preview HTML 根目录(build-impl-map 用,默认 {target}/../preview)")
    parser.add_argument("--code-root", default=None,
                        help="框架代码根目录(build-impl-map 用,默认当前工作目录)")
    parser.add_argument("--kind", choices=list(HASH_KINDS), default="draw-md",
                        help="哈希范围(compute-hash/diff-hash 用):"
                             "draw-md=draw-md 产物 .md(默认);preview=预览 HTML/截图清单;"
                             "code=impl-map 映射的实现文件")
    parser.add_argument("--strict", action="store_true", default=False,
                        help="check-nav 专用:发现异常跳转时退出码 1(三态「看了有问题」);"
                             "缺省保持 informational 退 0(EXIT-CODES.md 迁移登记)")
    parser.add_argument("--token", default=None,
                        help="token-usage 专用:只看该 token 的波及页面清单")
    args, _ = parser.parse_known_args(argv[1:])

    target = os.path.abspath(args.target)

    if args.subcommand == "generate":
        return _cmd_generate(target)
    if args.subcommand == "list-missing":
        return _cmd_list_missing(target)
    if args.subcommand == "check-nav":
        return _cmd_check_nav(target, strict=args.strict)
    if args.subcommand == "compute-hash":
        return _cmd_compute_hash(target, args.kind)
    if args.subcommand == "diff-hash":
        return _cmd_diff_hash(target, args.kind)
    if args.subcommand == "build-impl-map":
        preview_root = args.preview_root or os.path.join(os.path.dirname(target), "preview")
        code_root = args.code_root or os.getcwd()
        return _cmd_build_impl_map(target, preview_root, code_root)
    if args.subcommand == "list-unimplemented":
        return _cmd_list_unimplemented(target)
    if args.subcommand == "token-usage":
        return _cmd_token_usage(target, args.token)
    if args.subcommand == "check-sync":
        return _cmd_check_sync(target)
    print("[ERROR] 未知子命令: " + args.subcommand)
    return 1


def _cmd_generate(target):
    """generate:生成 ui-relationships.json。"""
    if not os.path.isdir(target):
        print("[ERROR] target 目录不存在: " + target)
        return 1
    result = generate(target)
    print("已生成 " + os.path.join(target, "ui-relationships.json"))
    print("  pages: " + str(len(result["pages"])))
    print("  navigations: " + str(len(result["navigations"])))
    return 0


def _cmd_list_missing(target):
    """list-missing:列出跳转目标未生成的清单。"""
    try:
        missing = list_missing(target)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        return 1
    if not missing:
        print("全部跳转目标已生成")
        return 0
    print("缺失跳转目标 " + str(len(missing)) + " 项:")
    for m in missing:
        print("  " + m["from"] + " → " + m["to"] + " (缺失)")
    return 0


def _cmd_check_nav(target, strict=False):
    """check-nav:检测异常跳转(自指/循环/死链)。

    退出码:无异常 0;有异常时 --strict 退 1(三态「看了有问题」),默认
    informational 退 0(EXIT-CODES.md 迁移登记——样例仓存在已知的未生成
    跳转目标,严打前须先补齐或显式豁免);基线文件缺失退 1。
    """
    try:
        result = check_nav(target)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        return 1
    total = (len(result["self_refs"]) + len(result["cycles"])
             + len(result["dead_links"]))
    if total == 0:
        print("无异常跳转")
        return 0
    if result["self_refs"]:
        print("自指 (" + str(len(result["self_refs"])) + " 项):")
        for nav in result["self_refs"]:
            print("  " + nav["from"] + " → " + nav["to"])
    if result["cycles"]:
        print("循环 (" + str(len(result["cycles"])) + " 项):")
        for c in result["cycles"]:
            print("  " + c["a"] + " ↔ " + c["b"])
    if result["dead_links"]:
        print("死链 (" + str(len(result["dead_links"])) + " 项):")
        for nav in result["dead_links"]:
            print("  " + nav["from"] + " → " + nav["to"] + " (目标不存在)")
    if strict:
        print("共 " + str(total) + " 项异常(--strict:按三态拦截)")
        return 1
    print("共 " + str(total) + " 项异常(informational,退 0;无人值守判定用 --strict)")
    return 0


def _state_name_for(kind):
    """kind → 基线文件名单一映射(命令层打印与 _hash_files 同源,防漂移)。"""
    return {kind: name for kind, name in [
        ("draw-md", "ui-hash-state.json"),
        ("preview", PREVIEW_HASH_STATE),
        ("code", CODE_HASH_STATE),
    ]}.get(kind, "ui-hash-state.json")


def _cmd_compute_hash(target, kind="draw-md"):
    """compute-hash:计算文件哈希,写对应基线状态文件(按 --kind)。"""
    if not os.path.isdir(target):
        print("[ERROR] target 目录不存在: " + target)
        return 1
    try:
        result = compute_hash(target, kind)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2
    print("已生成 " + os.path.join(target, _state_name_for(kind)))
    print("  " + _hash_scope_note(kind))
    print("  files: " + str(len(result["files"])))
    return 0


def _cmd_diff_hash(target, kind="draw-md"):
    """diff-hash:对比哈希快照,输出 added/modified/deleted(按 --kind)。"""
    try:
        result = diff_hash(target, kind)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2
    if result.get("baseline_missing"):
        print("无历史快照(" + _state_name_for(kind) + "),所有文件视为 added"
              "(提示:先运行 compute-hash --kind " + kind + " 建基线)")
    total = len(result["added"]) + len(result["modified"]) + len(result["deleted"])
    if total == 0:
        print("无变更")
        return 0
    for p in result["added"]:
        print("[added]    " + p)
    for p in result["modified"]:
        print("[modified] " + p)
    for p in result["deleted"]:
        print("[deleted]  " + p)
    return 0


def _cmd_build_impl_map(target, preview_root, code_root):
    """build-impl-map:构建 ui-implementation-map.json。"""
    try:
        result = build_impl_map(target, preview_root, code_root)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        return 1
    print("已生成 " + os.path.join(target, "ui-implementation-map.json"))
    counts = {"implemented": 0, "partial": 0, "missing": 0}
    for m in result["mappings"]:
        counts[m["status"]] = counts.get(m["status"], 0) + 1
    print("  implemented: " + str(counts["implemented"]))
    print("  partial:     " + str(counts["partial"]))
    print("  missing:     " + str(counts["missing"]))
    return 0


def _cmd_list_unimplemented(target):
    """list-unimplemented:列出 status=missing 的未实现页面。"""
    try:
        missing = list_unimplemented(target)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        return 1
    if not missing:
        print("全部逻辑页面已实现")
        return 0
    print("未实现逻辑页面 " + str(len(missing)) + " 项:")
    for m in missing:
        print("  " + m["logical_ui"] + " (" + m["reason"] + ")")
    return 0


def _cmd_token_usage(target, token_filter=None):
    """token-usage:token → 引用页面反向索引 + 孤儿 token(--token 只看单个)。"""
    if not os.path.isdir(target):
        print("[ERROR] target 目录不存在: " + target)
        return 1
    result = token_usage(target, write=token_filter is None)
    if token_filter:
        pages = result["tokens"].get(token_filter)
        print("token {" + token_filter + "} 波及页面:")
        if pages:
            for p in pages:
                print("  " + p)
        else:
            print("  (无页面引用;token.md 也未登记的话即悬空/孤儿)")
        return 0
    print("已生成 " + os.path.join(target, TOKEN_USAGE_FILE))
    print("  tokens(被引用): " + str(len(result["tokens"])))
    print("  unreferenced(孤儿): " + str(len(result["unreferenced"])))
    for name in result["unreferenced"]:
        print("    {" + name + "}")
    print("  波及分析用法: ui-graph.py token-usage --target <dir> --token <name>")
    return 0


def _cmd_check_sync(target):
    """check-sync:规格(draw-md)↔ 实现(preview/框架码)同步状态。

    退出码:全部 in-sync → 0;任一页 spec-ahead/code-drifted/diverged → 1;
    基线缺失/impl-map 缺失/基线损坏/路径越界 → 2(没能检查,先建基线)。
    """
    try:
        result = check_sync(target)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2
    except ValueError as e:
        print("[ERROR] " + str(e))
        print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2
    summary = result["summary"]
    print("同步状态: in-sync=" + str(summary.get("in-sync", 0))
          + " spec-ahead=" + str(summary.get("spec-ahead", 0))
          + " code-drifted=" + str(summary.get("code-drifted", 0))
          + " diverged=" + str(summary.get("diverged", 0)))
    for s in result["statuses"]:
        if s["status"] == "in-sync":
            continue
        line = "  [" + s["status"] + "] " + s["logical_ui"]
        if s["missing_files"]:
            line += " (实现文件缺失: " + ", ".join(s["missing_files"]) + ")"
        print(line)
    if summary.get("spec-ahead", 0):
        print("修复: spec-ahead → 重跑 preview/draw-* 后重建两份基线")
    if summary.get("code-drifted", 0) or summary.get("diverged", 0):
        print("修复: 实现侧变更须回写 ui-markdown 或在 decisions 账本登记原因")
    out_of_sync = sum(1 for s in result["statuses"] if s["status"] != "in-sync")
    if out_of_sync:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
