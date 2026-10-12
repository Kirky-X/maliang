#!/usr/bin/env python3
"""生成码机械校验:框架产物(dist draw-element 等的产出)是否守住 token 与组件契约。

用法:
    python3 scripts/validate-generated.py [target_dir] [--token-file PATH]
                                          [--framework-index PATH]
                                          [--format {text,json}]

默认 target_dir = examples/element-plus/(draw-element 的产出目录)。
默认 token-file = examples/ui-markdown/token.md
默认 framework-index = references/framework/index.md(组件白名单从同目录
framework/element/ 的文档里抽取 el-* 标签与 El* 服务名)。

检查项:
  1. gen.token-residue       — `{token-name}` 占位符零残留(error)
  2. gen.color-literal       — 颜色字面量必须回溯得到 token.md(error;
                               按字面值聚合计数,G04「硬编码视觉值」)
  3. gen.component-whitelist — 模板里的 `el-*` 标签与 element-plus 导入的
                               `El*` 名必须在 framework 文档白名单里(error)
  4. gen.sfc-structure       — Vue SFC 三段式(<template> + <script setup> +
                               <style>)与文件头来源注释完整(error)
  5. gen.class-undefined     — 模板里每个 class 必须在同文件 <style> 里有定义,
                               或属于框架基础类(el-*,运行时渲染)(error)

诚实范围:本脚本只做静态/机械校验,证明的是「组件产出」,不证明点击行为 ——
交互真实性由 scripts/verify-interactive.py 在真浏览器里验证。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        目标目录/token.md/framework 目录缺失 → 没能检查,退出码 2。
依赖: Python 3 标准库(无第三方依赖)。
来源:ux-ui-agent-skills scripts/render_framework_source.mjs(«每个 class 都必须
     在链接的样式表里有定义»、服务端渲染的诚实范围声明),2026-10 吸收。
"""

import argparse
import json
import os
import re
import sys

SCAN_EXTENSIONS = (".vue", ".ts", ".tsx", ".js", ".jsx")

# {token-name} 占位符(与 preview-check.py 的 token.residue 同 regex)
TOKEN_RESIDUE_RE = re.compile(r"\{([a-z][a-z0-9-]*)\}")
# 颜色字面量(hex / rgb / rgba / hsl / oklch 只做可回溯判定的子集:hex + rgb(a))
COLOR_LITERAL_RE = re.compile(
    r"#[0-9A-Fa-f]{3,8}\b|rgba?\([^)]*\)", re.IGNORECASE
)
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
TEMPLATE_RE = re.compile(r"<template>(.*?)</template>", re.DOTALL | re.IGNORECASE)
SCRIPT_RE = re.compile(r"<script[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
CLASS_ATTR_RE = re.compile(r'class\s*=\s*"([^"]*)"')
BOUND_CLASS_RE = re.compile(r':class\s*=\s*"([^"]*)"')
QUOTED_RE = re.compile(r"'([^']*)'|\"([^\"]*)\"")
CLASS_SELECTOR_RE = re.compile(r"\.([A-Za-z][\w-]*)")
EL_TAG_RE = re.compile(r"<(el-[a-z0-9-]+)\b")
EL_IMPORT_RE = re.compile(r"""import\s*\{([^}]*)\}\s*from\s*["']element-plus["']""")
EL_NAME_RE = re.compile(r"^El[A-Z][A-Za-z0-9]*$")


def _line_of(text, index):
    return text[:index].count("\n") + 1


def _norm_color(value):
    """颜色字面量归一化:小写去空白,3/4 位 hex 展开为 6/8 位。"""
    v = re.sub(r"\s+", "", value.lower())
    if re.fullmatch(r"#[0-9a-f]{3,4}", v):
        v = "#" + "".join(c * 2 for c in v[1:])
    return v


def parse_token_values(token_text):
    """从 token.md 收集全部颜色值(归一化),作为「可回溯」的判定集。"""
    values = set()
    stripped = CSS_COMMENT_RE.sub("", token_text)
    for m in COLOR_LITERAL_RE.finditer(stripped):
        values.add(_norm_color(m.group(0)))
    return values


def parse_framework_whitelist(framework_docs_dir):
    """从 framework/<name>/ 的文档里抽取组件白名单(el-* 标签 + El* 服务名)。"""
    tags, names = set(), set()
    for root, _dirs, files in os.walk(framework_docs_dir):
        for name in files:
            if not name.endswith(".md"):
                continue
            try:
                with open(os.path.join(root, name), "r", encoding="utf-8") as fh:
                    content = fh.read()
            except OSError as exc:
                print("   warn: framework 文档读取失败(白名单可能不完整): %s: %s"
                      % (name, exc), file=sys.stderr)
                continue
            tags.update(EL_TAG_RE.findall(content))
            names.update(re.findall(r"\bEl[A-Z][A-Za-z0-9]*\b", content))
    return tags, names


def check_token_residue(text, rel_path):
    """检查 1:{token} 占位符残留。"""
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(("//", "/*", "*")):
            continue
        for m in TOKEN_RESIDUE_RE.finditer(line):
            # 跳过 {{ 插值 与 ${ 模板串表达式(不是 token 占位符)
            if m.start() > 0 and line[m.start() - 1] in "{$":
                continue
            findings.append({
                "file": rel_path, "line": i, "severity": "ERROR",
                "rule": "gen.token-residue",
                "message": "{token} 占位符残留: " + m.group(0) + ",生成码必须已解析为具体值",
            })
    return findings


def check_color_literals(text, rel_path, token_values):
    """检查 2:颜色字面量必须能回溯到 token.md(按字面值聚合)。"""
    findings = []
    # 只看样式面(<style> 块 + 行内 style/填充属性);CSS 注释是文档说明,不算
    sources = []
    for m in STYLE_BLOCK_RE.finditer(text):
        sources.append((m.start(1), CSS_COMMENT_RE.sub("", m.group(1))))
    for m in re.finditer(r'style="([^"]*)"', text):
        sources.append((m.start(1), m.group(1)))
    for m in re.finditer(r'(?:fill|stroke|color)\s*=\s*"([^"]*)"', text):
        sources.append((m.start(1), m.group(1)))
    if not sources:
        # 没有任何样式面时退化为整文件扫描:JS/模板里的硬编码色同样要回溯
        sources = [(0, text)]

    seen = {}
    for offset, chunk in sources:
        for m in COLOR_LITERAL_RE.finditer(chunk):
            raw = m.group(0)
            if not token_values or _norm_color(raw) not in token_values:
                key = _norm_color(raw)
                if key in seen:
                    seen[key]["count"] += 1
                else:
                    seen[key] = {
                        "raw": raw,
                        "count": 1,
                        "line": _line_of(text, offset + m.start()),
                    }
    for key, info in sorted(seen.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
        findings.append({
            "file": rel_path, "line": info["line"], "severity": "ERROR",
            "rule": "gen.color-literal",
            "message": "颜色字面量 %s 不在 token.md 中(%d 处;G04——回 design-md 补 token 或改用已登记值)"
                       % (info["raw"], info["count"]),
        })
    return findings


def check_component_whitelist(text, rel_path, tag_whitelist, name_whitelist):
    """检查 3:组件标签/服务名在 framework 白名单内。"""
    findings = []
    template = TEMPLATE_RE.search(text)
    if template:
        for m in EL_TAG_RE.finditer(template.group(1)):
            tag = m.group(1)
            if tag not in tag_whitelist:
                findings.append({
                    "file": rel_path, "line": _line_of(text, template.start(1) + m.start()),
                    "severity": "ERROR", "rule": "gen.component-whitelist",
                    "message": "组件 <" + tag + "> 不在 framework/element/ 白名单中(可能杜撰 API)",
                })
    for m in EL_IMPORT_RE.finditer(text):
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[0].strip()
            if not name:
                continue
            if name not in name_whitelist:
                findings.append({
                    "file": rel_path, "line": _line_of(text, m.start()),
                    "severity": "ERROR", "rule": "gen.component-whitelist",
                    "message": "从 element-plus 导入的 " + name + " 不在 framework/element/ 白名单中",
                })
    return findings


def check_sfc_structure(text, rel_path):
    """检查 4:Vue SFC 三段式 + 文件头来源注释(其余扩展名仅查来源注释)。"""
    findings = []
    is_vue = rel_path.lower().endswith(".vue")
    if is_vue:
        for part, label in (("<template>", "template"), ("<script", "script"),
                            ("<style", "style")):
            if part not in text:
                findings.append({
                    "file": rel_path, "line": 1, "severity": "ERROR",
                    "rule": "gen.sfc-structure",
                    "message": "SFC 三段式缺 " + label + " 段(应为 <template> + <script setup> + <style>)",
                })
        if "<script" in text and not re.search(r"<script[^>]*setup", text):
            findings.append({
                "file": rel_path, "line": 1, "severity": "ERROR",
                "rule": "gen.sfc-structure",
                "message": "script 段缺少 setup(draw-element 产出应为 <script setup>)",
            })
    head = text[:900]
    comment = re.search(r"<!--(.*?)-->", head, re.DOTALL)
    if not comment or not re.search(r"draw-|由\s*\S+\s*生成|生成自", comment.group(1)):
        findings.append({
            "file": rel_path, "line": 1, "severity": "ERROR",
            "rule": "gen.sfc-structure",
            "message": "文件头缺少来源注释(应标注由哪个 draw-* 从哪份页面 markdown 生成)",
        })
    return findings


def check_class_resolution(text, rel_path, class_prefix_ok=("el-",)):
    """检查 5:模板里每个 class 必须在同文件 style 有定义或属框架基础类。"""
    template = TEMPLATE_RE.search(text)
    if not template:
        return []
    used = {}
    for m in CLASS_ATTR_RE.finditer(template.group(1)):
        for cls in m.group(1).split():
            used.setdefault(cls, template.start(1) + m.start())
    for m in BOUND_CLASS_RE.finditer(template.group(1)):
        for lit in QUOTED_RE.finditer(m.group(1)):
            for cls in (lit.group(1) or lit.group(2) or "").split():
                if re.fullmatch(r"[A-Za-z][\w-]*", cls):
                    used.setdefault(cls, template.start(1) + m.start())

    defined = set()
    for m in STYLE_BLOCK_RE.finditer(text):
        css = CSS_COMMENT_RE.sub("", m.group(1))
        css = re.sub(r"\[[^\]]*\]", "", css)            # 属性选择器不贡献类名
        defined.update(CLASS_SELECTOR_RE.findall(css))

    findings = []
    for cls, index in sorted(used.items(), key=lambda kv: kv[1]):
        if cls in defined or any(cls.startswith(p) for p in class_prefix_ok):
            continue
        findings.append({
            "file": rel_path, "line": _line_of(text, index), "severity": "ERROR",
            "rule": "gen.class-undefined",
            "message": "类 .%s 在模板里用了,但同文件 <style> 没有定义(渲染成裸元素,"
                       "对比度与 axe 都看不见)" % cls,
        })
    return findings


def collect_files(target_dir):
    found = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = sorted(d for d in dirs if d not in ("node_modules", ".git", "dist", "build"))
        for name in sorted(files):
            if name.lower().endswith(SCAN_EXTENSIONS):
                found.append(os.path.join(root, name))
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="生成码机械校验:token 零残留 / 颜色回溯 token.md / 组件白名单 / "
                    "SFC 结构与类名解析(退出码见 scripts/EXIT-CODES.md)"
    )
    parser.add_argument("target_dir", nargs="?", default="examples/element-plus",
                        help="生成码目录(默认 examples/element-plus)")
    parser.add_argument("--token-file", default=None,
                        help="token.md 路径(默认 examples/ui-markdown/token.md)")
    parser.add_argument("--framework-index", default=None,
                        help="framework/index.md 路径(默认 references/framework/index.md)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式: text(人类可读,默认) / json(stdout 仅 JSON 数组)")
    args = parser.parse_args(argv)

    target_dir = os.path.abspath(args.target_dir)
    token_file = os.path.abspath(args.token_file or os.path.join(
        os.getcwd(), "examples", "ui-markdown", "token.md"))
    framework_index = os.path.abspath(args.framework_index or os.path.join(
        os.getcwd(), "references", "framework", "index.md"))
    framework_dir = os.path.join(os.path.dirname(framework_index), "element")

    def _cannot_check(message):
        if args.format == "json":
            print("[]")
            print("[ERROR] " + message, file=sys.stderr)
        else:
            print("[ERROR] " + message)
            print("没能检查,不得记为通过(见 scripts/EXIT-CODES.md)。")
        return 2

    if not os.path.isdir(target_dir):
        return _cannot_check("目标目录不存在: " + target_dir)
    if not os.path.isfile(token_file):
        return _cannot_check("token.md 不存在: " + token_file)
    if not os.path.isdir(framework_dir):
        return _cannot_check("framework 组件文档目录不存在: " + framework_dir)

    files = collect_files(target_dir)
    if not files:
        return _cannot_check("目标目录里没有可校验的生成码文件: " + target_dir)

    with open(token_file, "r", encoding="utf-8") as fh:
        token_values = parse_token_values(fh.read())
    tag_whitelist, name_whitelist = parse_framework_whitelist(framework_dir)

    if args.format == "text":
        print("maliang 生成码机械校验")
        print("=" * 32)
        print("目标目录: " + target_dir)
        print("Token 文件: " + token_file)
        print("组件白名单: " + framework_dir + "(%d 个标签 / %d 个服务名)"
              % (len(tag_whitelist), len(name_whitelist)))
        print("")

    all_results = []
    for path in files:
        rel = os.path.relpath(path, target_dir)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            all_results.append({
                "file": rel, "line": 0, "severity": "ERROR", "rule": "gen.read",
                "message": "读取失败: %s" % exc,
            })
            continue
        all_results.extend(check_token_residue(text, rel))
        all_results.extend(check_color_literals(text, rel, token_values))
        all_results.extend(check_component_whitelist(text, rel, tag_whitelist, name_whitelist))
        all_results.extend(check_sfc_structure(text, rel))
        all_results.extend(check_class_resolution(text, rel))

    severity_rank = {"ERROR": 0, "WARN": 1}
    all_results.sort(key=lambda r: (severity_rank.get(r["severity"], 9), r["file"], r["line"]))

    if args.format == "json":
        print(json.dumps([
            {"file": r["file"], "line": r["line"], "severity": r["severity"],
             "rule": r["rule"], "message": r["message"]}
            for r in all_results
        ], ensure_ascii=False))
    else:
        for r in all_results:
            label = "[ERROR]" if r["severity"] == "ERROR" else "[WARN] "
            print("{} {}:{} [{}] {}".format(label, r["file"], r["line"], r["rule"], r["message"]))
        print("")
        print("=" * 32)
        print("检查结果: %d errors" % len(all_results))
        print("诚实范围:静态校验只证明组件产出,不证明点击行为(交给 verify-interactive.py)。")
        print("退出码: " + ("1" if all_results else "0"))

    return 1 if all_results else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
