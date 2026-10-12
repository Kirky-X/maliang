#!/usr/bin/env python3
"""句型级反模板文案扫描(G32/preview-checklist §5.1 脚本层)。

词表禁令挡不住换同义词——真正的 tell 是**句子模板**本身:"The [adj] way to
[verb]" 换哪个词都读作生成。本脚本收 10 式模板句正则(移植自 tastemaker
check_copy_diversity.py 的 TEMPLATE_PATTERNS,#32,2026-10 吸收),另收
em-dash 滥用:英文 em-dash(—)插入语判 critical(外部 HIGH 口径);
中文全角破折号「——」是规范用法,豁免(与 ai-tells §6 口径一致)。

扫描面:markup 文件的**可见文本节点**(>text< 形态);<style>/<script>/注释
不扫。也支持 --headline/--cta/--subhead 直接检查给定字符串(CI 与手工用)。

三角度候选淘汰(mechanism/outcome/tension)是写作流程,不进脚本——脚本只拦
已写出的模板句,候选发散由人与 LLM 评审承担。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
依赖: Python 3 标准库。
来源: tastemaker references/copy-voice.md 模板银行 + anti_slop_scan.py em-dash
      HIGH 口径(#32),2026-10 吸收;中文破折号例外为本仓 ai-tells §6 既有口径。
"""

import argparse
import os
import re
import sys

# 扫描的 markup 文件扩展名(可见文案存在的文件)
SCAN_EXTENSIONS = {
    ".html", ".htm", ".vue", ".svelte", ".astro", ".jsx", ".tsx",
}

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}

# 可见文本节点:>text<;不含标签内属性。跨行文本节点由 DOTALL 覆盖。
_TEXT_NODE_RE = re.compile(r">([^<>]+)<", re.DOTALL)
_STYLE_SCRIPT_RE = re.compile(r"<(style|script)\b.*?</\1>", re.DOTALL | re.IGNORECASE)
_COMMENT_RE = re.compile(r"<!--.*?-->|/\*.*?\*/", re.DOTALL)

# 英文 em-dash(单 — 夹在 ASCII 词间);「——」(中文破折号)先剥除再判
_CN_DASH_RE = re.compile(r"——")
_EN_EM_DASH_RE = re.compile(r"[A-Za-z0-9]\s*—\s*[A-Za-z0-9]")

# 10 式模板句(移植自 tastemaker TEMPLATE_PATTERNS,#32;正则 → 规则名 → 释义)
TEMPLATE_PATTERNS = (
    (r"\bthe\s+\w+\s+way\s+to\s+\w+", "the-adj-way-to", "「The [adjective] way to [verb]」"),
    (r"\bbuilt\s+for\s+\w+(?:\s+\w+)?\s+who\s+\w+", "built-for-who", "「Built for [audience] who [verb]」作全部主张"),
    (r"^\s*\w+\s+your\s+\w+\s+in\s+(?:seconds|minutes|hours|no\s+time)", "verb-your-noun-in-time", "「[Verb] your [noun] in [time]」"),
    (r"\bwhere\s+\w+\s+meets\s+\w+", "where-x-meets-y", "「Where [noun] meets [noun]」"),
    (r"^\s*\w+(?:,\s*\w+)+\s+\w+\s*[.!]?\s*$", "adj-adj-noun", "「[Adjective], [adjective] [noun]」当标题"),
    (r"\beverything\s+you\s+need\s+to\s+\w+", "everything-you-need", "「Everything you need to [verb]」"),
    (r"^\s*\w+\s+made\s+\w+\s*[.!]?\s*$", "noun-made-adj", "「[Noun] made [adjective]」"),
    (r"\bsay\s+goodbye\s+to\b", "say-goodbye-to", "「Say goodbye to [problem]」"),
    (r"\byour\s+\w+,?\s+(?:reimagined|reinvented)\b", "noun-reimagined", "「Your [noun], reimagined/reinvented」"),
    (r"\bone\s+platform\s+for\s+all\s+your\b", "one-platform-for-all", "「One platform for all your [noun]」"),
)
_TEMPLATE_RES = [(re.compile(p, re.IGNORECASE | re.MULTILINE), name, desc) for p, name, desc in TEMPLATE_PATTERNS]


def findings_for_text(text, label):
    """对一段文案跑模板句 + em-dash 检查,返回 finding dict 列表。"""
    out = []
    for regex, name, desc in _TEMPLATE_RES:
        m = regex.search(text)
        if m:
            out.append({
                "where": label, "rule": "copy-template/%s" % name,
                "message": "命中模板句 %s —— 换同义词没用,句型本身读作生成;按"
                           " mechanism/outcome/tension 三角度重写(文案原文: %.80s)"
                           % (desc, m.group(0)),
            })
    # 中文破折号「——」豁免后残留的英文 em-dash 插入语
    stripped = _CN_DASH_RE.sub("", text)
    for m in _EN_EM_DASH_RE.finditer(stripped):
        out.append({
            "where": label, "rule": "em-dash",
            "message": "英文 em-dash 插入语(「%.40s」)——改句号/冒号/括号断句;"
                       "中文破折号「——」不受此限(ai-tells §6)" % m.group(0),
        })
    return out


def scan_markup(text, rel_path):
    """扫描 markup 文件的可见文本节点。"""
    cleaned = _STYLE_SCRIPT_RE.sub(" ", text)
    cleaned = _COMMENT_RE.sub(" ", cleaned)
    findings = []
    for m in _TEXT_NODE_RE.finditer(cleaned):
        node = m.group(1).strip()
        if not node:
            continue
        line = cleaned.count("\n", 0, m.start()) + 1
        for f in findings_for_text(node, "%s:%d" % (rel_path, line)):
            findings.append(f)
    return findings


def collect_files(paths):
    files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                for name in sorted(names):
                    if os.path.splitext(name)[1].lower() in SCAN_EXTENSIONS:
                        files.append(os.path.join(root, name))
        elif os.path.isfile(path):
            files.append(path)
        else:
            print("check-copy: 路径不存在: %s" % path, file=sys.stderr)
            return None
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="句型级反模板文案扫描(10 式模板句 + em-dash critical,中文——豁免)"
    )
    parser.add_argument("paths", nargs="*", help="待扫描的 markup 文件或目录")
    parser.add_argument("--headline", default=None, help="直接检查 hero 标题字符串")
    parser.add_argument("--cta", default=None, help="直接检查 CTA 文案字符串")
    parser.add_argument("--subhead", default=None, help="直接检查副标题字符串")
    args = parser.parse_args(argv)

    findings = []
    scanned = 0
    if args.paths:
        files = collect_files(args.paths)
        if files is None:
            return 2
        for path in files:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError as exc:
                print("check-copy: 读取失败(跳过): %s (%s)" % (path, exc), file=sys.stderr)
                continue
            findings.extend(scan_markup(text, path))
            scanned += 1
    for label, value in (("--headline", args.headline), ("--cta", args.cta), ("--subhead", args.subhead)):
        if value is not None:
            findings.extend(findings_for_text(value, label))
            scanned += 1

    if scanned == 0:
        print("check-copy: 没有可检查目标(无文件且未给 --headline/--cta/--subhead)——没能检查",
              file=sys.stderr)
        return 2

    for f in findings:
        print("%s: [%s] %s" % (f["where"], f["rule"], f["message"]))
    if not findings:
        print("扫描 %d 个目标:未命中模板句与 em-dash 滥用(句型读作具体)。" % scanned)
        return 0
    print("扫描 %d 个目标,命中 %d 处(改写后再扫;三角度候选淘汰见 copy-strategy 文档)" % (scanned, len(findings)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
