#!/usr/bin/env python3
"""framework 组件文档规范性检查脚本。

用法:
    python3 scripts/validate-framework.py [--framework-dir PATH] [--format {text,json}]

默认 framework-dir = references/framework/。
退出码: 0 = 全部通过; 1 = 有 error; 2 = 仅有 warning。
依赖: Python 3 标准库(无第三方依赖)。

检查项:
  1. 框架目录完整性: 3 框架(harmony/flutter/element)都存在(error)
  2. 组件目录对称性: 3 框架的组件目录集合一致(warning)
  3. 必需文件存在性: 每个组件目录含 2 个文件(error)
  4. 代码块语言标签: 示例代码含语言标签(warning)
  5. 参考链接章节: 文件含 ## 参考链接(warning)
  6. N/A 文件内容: N/A 占位文件含缺失原因/替代方案(warning)
  7. slug 命名一致性: 目录名为 kebab-case(error)
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

FRAMEWORKS = ["harmony", "flutter", "element"]

# 每个框架的文件命名惯例
EXPECTED_FILES = {
    "harmony": ["component.md", "usage.md"],
    "flutter": ["widget.md", "properties.md"],
    "element": ["component.md", "api.md"],
}

KEBAB_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


# ---------------------------------------------------------------------------
# 检查函数
# ---------------------------------------------------------------------------


def check_framework_dirs(framework_dir):
    """检查 1: 3 框架目录都存在。"""
    results = []
    for fw in FRAMEWORKS:
        fw_dir = os.path.join(framework_dir, fw)
        if not os.path.isdir(fw_dir):
            results.append(("ERROR", fw, 0, "框架目录不存在: " + fw_dir))
    return results


def _get_component_dirs(framework_dir, fw):
    """获取某框架下的组件目录列表(排序)。"""
    fw_dir = os.path.join(framework_dir, fw)
    if not os.path.isdir(fw_dir):
        return []
    return sorted([
        d for d in os.listdir(fw_dir)
        if os.path.isdir(os.path.join(fw_dir, d))
    ])


def check_slug_naming(framework_dir):
    """检查 7: 目录名为 kebab-case。"""
    results = []
    for fw in FRAMEWORKS:
        for comp in _get_component_dirs(framework_dir, fw):
            if not KEBAB_CASE_RE.match(comp):
                results.append((
                    "ERROR", fw + "/" + comp, 0,
                    "组件目录名非 kebab-case: " + comp,
                ))
    return results


def check_symmetry(framework_dir):
    """检查 2: 3 框架的组件目录集合一致。"""
    results = []
    slug_sets = {}
    for fw in FRAMEWORKS:
        slug_sets[fw] = set(_get_component_dirs(framework_dir, fw))

    # 以 element 为基准(45 类)
    base = slug_sets.get("element", set())
    for fw in FRAMEWORKS:
        missing = base - slug_sets[fw]
        extra = slug_sets[fw] - base
        for s in sorted(missing):
            results.append((
                "WARN", fw, 0,
                "组件目录缺失(相对 element 基准): " + s,
            ))
        for s in sorted(extra):
            results.append((
                "WARN", fw, 0,
                "组件目录多余(相对 element 基准): " + s,
            ))
    return results


def check_required_files(framework_dir):
    """检查 3: 每个组件目录含 2 个必需文件。"""
    results = []
    for fw in FRAMEWORKS:
        expected = EXPECTED_FILES.get(fw, [])
        for comp in _get_component_dirs(framework_dir, fw):
            comp_dir = os.path.join(framework_dir, fw, comp)
            for fname in expected:
                fpath = os.path.join(comp_dir, fname)
                if not os.path.isfile(fpath):
                    results.append((
                        "ERROR", fw + "/" + comp, 0,
                        "必需文件缺失: " + fname,
                    ))
    return results


def check_code_language_tags(framework_dir):
    """检查 4: 示例代码含语言标签。"""
    results = []
    lang_tags = {"arkts", "dart", "vue", "typescript", "javascript"}
    for fw in FRAMEWORKS:
        for comp in _get_component_dirs(framework_dir, fw):
            comp_dir = os.path.join(framework_dir, fw, comp)
            for fname in os.listdir(comp_dir):
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(comp_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                # 查找代码块
                code_blocks = re.findall(r"```(\w*)\n", content)
                if code_blocks:
                    has_lang = any(tag in lang_tags for tag in code_blocks if tag)
                    if not has_lang and any(tag == "" for tag in code_blocks):
                        results.append((
                            "WARN", fw + "/" + comp + "/" + fname, 0,
                            "代码块缺少语言标签(应为 " +
                            {"harmony": "arkts", "flutter": "dart", "element": "vue"}.get(fw, "") +
                            ")",
                        ))
    return results


def check_reference_links(framework_dir):
    """检查 5: 文件含 ## 参考链接 章节。"""
    results = []
    for fw in FRAMEWORKS:
        for comp in _get_component_dirs(framework_dir, fw):
            comp_dir = os.path.join(framework_dir, fw, comp)
            for fname in os.listdir(comp_dir):
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(comp_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                # N/A 文件不检查参考链接
                if "N/A" in content[:200] or "无原生" in content[:200]:
                    continue
                if "## 参考链接" not in content and "## Reference" not in content:
                    results.append((
                        "WARN", fw + "/" + comp + "/" + fname, 0,
                        "缺少 '## 参考链接' 章节",
                    ))
    return results


def check_na_files(framework_dir):
    """检查 6: N/A 占位文件含必需内容(缺失原因/替代方案)。"""
    results = []
    na_keywords = ["N/A", "无原生", "无对应", "不支援"]
    required_sections = ["缺失原因", "替代方案"]
    for fw in FRAMEWORKS:
        for comp in _get_component_dirs(framework_dir, fw):
            comp_dir = os.path.join(framework_dir, fw, comp)
            for fname in os.listdir(comp_dir):
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(comp_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                # 判断是否为 N/A 文件
                is_na = any(kw in content[:300] for kw in na_keywords)
                if not is_na:
                    continue
                # 检查必需内容
                for section in required_sections:
                    if section not in content:
                        results.append((
                            "WARN", fw + "/" + comp + "/" + fname, 0,
                            "N/A 文件缺少 '" + section + "' 说明",
                        ))
    return results


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main(argv):
    parser = argparse.ArgumentParser(
        description="maliang framework 组件文档规范性检查")
    parser.add_argument(
        "--framework-dir", default=None,
        help="framework 目录(默认 references/framework/)")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式: text(默认) / json")
    args = parser.parse_args(argv[1:])
    fmt = args.format

    framework_dir = os.path.abspath(
        args.framework_dir or os.path.join(os.getcwd(), "references", "framework"))

    if fmt == "text":
        print("maliang framework 组件文档规范性检查")
        print("=" * 40)
        print("Framework 目录: " + framework_dir)
        print("")

    if not os.path.isdir(framework_dir):
        msg = "framework 目录不存在: " + framework_dir
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 1

    all_results = []
    all_results.extend(check_framework_dirs(framework_dir))
    all_results.extend(check_slug_naming(framework_dir))
    all_results.extend(check_symmetry(framework_dir))
    all_results.extend(check_required_files(framework_dir))
    all_results.extend(check_code_language_tags(framework_dir))
    all_results.extend(check_reference_links(framework_dir))
    all_results.extend(check_na_files(framework_dir))

    # 排序
    severity_rank = {"ERROR": 0, "WARN": 1}
    all_results.sort(key=lambda r: (severity_rank.get(r[0], 9), r[1], r[2]))

    error_count = sum(1 for r in all_results if r[0] == "ERROR")
    warn_count = sum(1 for r in all_results if r[0] == "WARN")

    if fmt == "json":
        findings = [
            {"file": f, "line": ln, "severity": sev, "message": msg}
            for (sev, f, ln, msg) in all_results
        ]
        print(json.dumps(findings, ensure_ascii=False))
    else:
        for sev, f, ln, msg in all_results:
            label = "[ERROR]" if sev == "ERROR" else "[WARN] "
            if ln > 0:
                print("{} {}:{} {}".format(label, f, ln, msg))
            else:
                print("{} {} {}".format(label, f, msg))
        print("")
        print("=" * 40)
        print("检查结果: {} errors, {} warnings".format(error_count, warn_count))

    if error_count > 0:
        if fmt == "text":
            print("退出码: 1")
        return 1
    if warn_count > 0:
        if fmt == "text":
            print("退出码: 2")
        return 2
    if fmt == "text":
        print("退出码: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
