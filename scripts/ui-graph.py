#!/usr/bin/env python3
"""ui-graph —— UI 关系管理与变更追踪脚本。

用法:
    python3 scripts/ui-graph.py <subcommand> [--target PATH] [options]

子命令:
    generate           生成 ui-relationships.json(页面层级 + 跳转关系)
    list-missing       列出跳转目标未生成对应 markdown 的清单
    check-nav          检测异常跳转(自指/循环/死链)
    compute-hash       计算每个 markdown 文件 sha256,写 ui-hash-state.json
    diff-hash          对比当前哈希与 ui-hash-state.json,输出 added/modified/deleted
    build-impl-map     构建 logical_ui ↔ preview_html ↔ framework_code 映射
    list-unimplemented  列出 status=missing 的未实现逻辑页面

默认 --target = examples/ui-markdown/。
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
}

# 默认 target 目录(相对脚本调用的工作目录)
DEFAULT_TARGET = "examples/ui-markdown"


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
    """从 markdown 文本提取 YAML frontmatter(简单 flat 解析,无第三方依赖)。

    仅支持顶层 `key: value` 行;不处理嵌套/多行字符串。
    components 字段(inline `[a, b, c]`)解析为 list;其他字段保留为字符串
    (保留引号,与 validate-draw-md.py 的 parse_frontmatter 行为一致)。
    返回 dict: 字段名 -> 值(components 为 list,其他为 str)。
    无 frontmatter 返回空 dict。
    """
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*", text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if not k:
            continue
        if k == "components":
            result[k] = _parse_inline_list(v)
        else:
            result[k] = v
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
        return [item.strip() for item in inner.split(",") if item.strip()]
    return [v] if v else []


# 提取 tap 跳转目标:tap=→<target>,target 为 [a-z][a-z0-9/-]* (遇 . / 空格 / 中文停止)
TAP_NAV_RE = re.compile(r"tap=→([a-z][a-z0-9/-]*)")


def extract_navigations(text, from_path=None):
    """提取文本中所有 tap 跳转关系,返回 [{'to':..., 'event':'tap'}]。

    用正则 tap=→([a-z][a-z0-9/-]*) 提取跳转目标:
    - 跳过 `无`(正则不匹配,中文非 [a-z])/ `back`(history.back,非具体页面)
    - 跳过中文/含空格目标(正则不匹配)
    - 归一化为 ui/<to>.md 路径:
      * 原始值不以 ui/ 开头(如 setting/notifications)→ ui/<raw>.md
      * 原始值已以 ui/ 开头(如 ui/message,正则遇 . 停止)→ <raw>.md(避免双重前缀)

    from_path 当前未使用(generate 聚合时添加 from 字段),保留参数以匹配
    T007 签名 extract_navigations(text, from_path)。
    """
    results = []
    for m in TAP_NAV_RE.finditer(text):
        raw = m.group(1)
        if raw in ("无", "back"):
            continue
        if raw.startswith("ui/"):
            to_path = raw + ".md"
        else:
            to_path = "ui/" + raw + ".md"
        results.append({"to": to_path, "event": "tap"})
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

def compute_hash(target_dir):
    """计算每个 markdown 文件 sha256,写 ui-hash-state.json。

    parse_directory 已排除 token.md;.json 产出文件非 .md,自动排除。
    返回 {'computed_at', 'target_dir', 'files[]'}(files[] 含 path/sha256/size)。
    """
    rel_paths = parse_directory(target_dir)
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
    result = {
        "computed_at": _now_iso(),
        "target_dir": target_dir,
        "files": files,
    }
    out_path = os.path.join(target_dir, "ui-hash-state.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


def diff_hash(target_dir):
    """对比当前哈希与 ui-hash-state.json,返回 {'added', 'modified', 'deleted'}。

    - added: 当前存在但历史快照中没有
    - modified: 两边都有但 sha256 不同
    - deleted: 历史快照中有但当前不存在
    """
    state_path = os.path.join(target_dir, "ui-hash-state.json")
    if not os.path.isfile(state_path):
        raise FileNotFoundError(
            "ui-hash-state.json 不存在: " + state_path + ",请先运行 compute-hash")
    with open(state_path, "r", encoding="utf-8") as f:
        old_state = json.load(f)
    old_files = {f["path"]: f["sha256"] for f in old_state.get("files", [])}

    rel_paths = parse_directory(target_dir)
    current_files = {}
    for rel_path in rel_paths:
        abs_path = os.path.join(target_dir, rel_path)
        with open(abs_path, "rb") as f:
            content = f.read()
        current_files[rel_path] = hashlib.sha256(content).hexdigest()

    added = sorted([p for p in current_files if p not in old_files])
    modified = sorted([p for p in current_files
                       if p in old_files and old_files[p] != current_files[p]])
    deleted = sorted([p for p in old_files if p not in current_files])
    return {"added": added, "modified": modified, "deleted": deleted}


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
    """扫描 preview_root 下所有 .html,返回 {slug: rel_path}。"""
    result = {}
    if not preview_root or not os.path.isdir(preview_root):
        return result
    for dirpath, _, filenames in os.walk(preview_root):
        for fn in filenames:
            if fn.endswith(".html"):
                slug = _extract_slug(fn)
                abs_path = os.path.join(dirpath, fn)
                result[slug] = os.path.relpath(abs_path, os.getcwd())
    return result


def _scan_framework_code(code_root):
    """扫描框架代码,返回 {'harmony': {}, 'flutter': {}, 'element': {}}。

    harmony: **/pages/<Slug>.ets
    flutter: **/pages/<slug>.dart
    element: **/views/<slug>.vue
    """
    result = {"harmony": {}, "flutter": {}, "element": {}}
    if not code_root or not os.path.isdir(code_root):
        return result
    for dirpath, _, filenames in os.walk(code_root):
        # 路径转 POSIX 风格用于模式匹配
        dir_posix = (dirpath + "/").replace(os.sep, "/")
        for fn in filenames:
            abs_path = os.path.join(dirpath, fn)
            rel_path = os.path.relpath(abs_path, os.getcwd())
            slug = _extract_slug(fn)
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
    """
    rel = _load_relationships(target_dir)
    pages = rel.get("pages", [])

    preview_map = _scan_preview_html(preview_root)
    fw_map = _scan_framework_code(code_root)

    mappings = []
    for page in pages:
        slug = _logical_ui_slug(page["path"])
        preview_html = preview_map.get(slug)
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

    result = {"built_at": _now_iso(), "mappings": mappings}
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
# 主流程
# ---------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(
        description="maliang UI 关系管理与变更追踪")
    parser.add_argument("subcommand",
                        choices=["generate", "list-missing", "check-nav",
                                 "compute-hash", "diff-hash",
                                 "build-impl-map", "list-unimplemented"],
                        help="子命令")
    parser.add_argument("--target", default=DEFAULT_TARGET,
                        help="目标目录(默认 " + DEFAULT_TARGET + ")")
    parser.add_argument("--preview-root", default=None,
                        help="preview HTML 根目录(build-impl-map 用,默认 {target}/../preview)")
    parser.add_argument("--code-root", default=None,
                        help="框架代码根目录(build-impl-map 用,默认当前工作目录)")
    args, _ = parser.parse_known_args(argv[1:])

    target = os.path.abspath(args.target)

    if args.subcommand == "generate":
        return _cmd_generate(target)
    if args.subcommand == "list-missing":
        return _cmd_list_missing(target)
    if args.subcommand == "check-nav":
        return _cmd_check_nav(target)
    if args.subcommand == "compute-hash":
        return _cmd_compute_hash(target)
    if args.subcommand == "diff-hash":
        return _cmd_diff_hash(target)
    if args.subcommand == "build-impl-map":
        preview_root = args.preview_root or os.path.join(os.path.dirname(target), "preview")
        code_root = args.code_root or os.getcwd()
        return _cmd_build_impl_map(target, preview_root, code_root)
    if args.subcommand == "list-unimplemented":
        return _cmd_list_unimplemented(target)
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


def _cmd_check_nav(target):
    """check-nav:检测异常跳转(自指/循环/死链)。"""
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
    return 0


def _cmd_compute_hash(target):
    """compute-hash:计算 markdown 文件哈希,写 ui-hash-state.json。"""
    if not os.path.isdir(target):
        print("[ERROR] target 目录不存在: " + target)
        return 1
    result = compute_hash(target)
    print("已生成 " + os.path.join(target, "ui-hash-state.json"))
    print("  files: " + str(len(result["files"])))
    return 0


def _cmd_diff_hash(target):
    """diff-hash:对比哈希快照,输出 added/modified/deleted。"""
    try:
        result = diff_hash(target)
    except FileNotFoundError as e:
        print("[ERROR] " + str(e))
        return 1
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
