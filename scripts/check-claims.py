#!/usr/bin/env python3
"""check-claims —— 公开声明 × 仓库事实对账。

文档里手写的数字会漂移：模板墙加了两个设计语言，SKILL.md 与 README 里的
「12 种」不会自己改。本脚本按 lint-checks.json 的规则把公开声明对账到**唯一
来源**（如 templates/INDEX.md 的表行数），并检查必现短语与禁用语表。

规则类型（lint-checks.json `checks[]`，与 skill_lint.py 共享同一 schema）:

    {"name": "设计语言计数对账", "type": "count-matches",
     "source": "references/templates/INDEX.md",    # 唯一来源（计数的出处）
     "section": "## 设计语言",                      # 可选:只数该标题节内的行
     "row_pattern": "^\\|\\s*\\[",                  # 可选:一"条"匹配一行（默认表行）
     "claim_files": ["SKILL.md", "README.md"],      # 声明出现的位置
     "claim_patterns": ["(\\d+)\\s*种设计语言", "(\\d+)\\s+design languages"],
     "min_claims": 1,                               # 可选:一条声明都抓不到 = 规则形同虚设
     "severity": "WARN"}                            # FAIL / WARN（缺省 FAIL）

    {"name": "禁用夸张语", "type": "forbid-pattern",
     "files": ["README.md", "SKILL.md", "README_EN.md"],
     "pattern": "完美|革命性|颠覆性|行业第一|首屈一指|保证通过",
     "ignore": "禁用夸张语表",                        # 可选:匹配该正则的行豁免
     "severity": "FAIL"}

    {"name": "必现短语", "type": "require-pattern",   # 既有类型,本脚本同样执行
     "file": "README.md", "pattern": "纯 Python 标准库", "min_count": 1}

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
    0 = 看了没问题（warning 级发现不改变退出码）
    1 = 存在 error 级发现（FAIL 级规则命中；--strict 下所有发现都升级为 error）
    2 = 没能检查（没有 lint-checks.json / 没有可执行的声明规则 / 用法错误）
依赖: Python 3 标准库(无第三方依赖)。
来源: styleseed/scripts/test-public-claims.mjs(countedClaims/requiredPhrases/
denylist)与 .github/workflows/validate-engine.yml, 2026-10 吸收, 中文自研实现。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HANDLED_TYPES = ("count-matches", "forbid-pattern", "require-pattern")


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("lint-checks.json 顶层必须是对象")
    return data


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return []


def _section_text(text: str, section: str | None) -> str:
    """截取 `section` 标题到下一个同级（或更高级）标题之间的文本。"""
    if not section:
        return text
    m = re.match(r"^(#+)\s", section)
    level = len(m.group(1)) if m else 6
    stop_re = re.compile(r"^#{1,%d}\s" % level)
    lines = text.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.startswith(section):
            start = i
            continue
        if start is not None and stop_re.match(line):
            return "".join(lines[start:i])
    if start is None:
        raise ValueError(f"section 未命中: {section!r}")
    return "".join(lines[start:])


def count_source(repo: str, rule: dict) -> tuple[int, str]:
    """数唯一来源的条目数（section 限制 + row_pattern 逐行匹配）。"""
    source = rule.get("source")
    if not source:
        raise ValueError("count-matches 需要 source（唯一来源文件）")
    path = os.path.join(repo, source)
    if not os.path.isfile(path):
        raise ValueError(f"source 不存在: {source}")
    text = _section_text(_read(path), rule.get("section"))
    row_re = re.compile(rule.get("row_pattern", r"^\|\s*\["), re.MULTILINE)
    count = len(row_re.findall(text))
    detail = f"{source}" + (f" [{rule['section']}]" if rule.get("section") else "")
    return count, detail


def check_count_matches(repo: str, rule: dict) -> list[dict]:
    findings: list[dict] = []
    severity = rule.get("severity", "FAIL")
    expected, detail = count_source(repo, rule)
    patterns = _as_list(rule.get("claim_pattern")) + _as_list(rule.get("claim_patterns"))
    if not patterns:
        raise ValueError("count-matches 需要 claim_pattern 或 claim_patterns（抓声明的正则，须含一个捕获组）")
    min_claims = rule.get("min_claims", 1)
    if not isinstance(min_claims, int) or min_claims < 0:
        raise ValueError("min_claims 必须是 ≥0 的整数")
    seen = 0
    for rel in _as_list(rule.get("claim_files")):
        path = os.path.join(repo, rel)
        if not os.path.isfile(path):
            raise ValueError(f"claim_files 里的文件不存在: {rel}")
        text = _read(path)
        for pattern in patterns:
            try:
                regex = re.compile(pattern)
            except re.error as exc:
                raise ValueError(f"claim_pattern 非法正则 {pattern!r}: {exc}") from None
            if regex.groups != 1:
                raise ValueError(f"claim_pattern 必须恰好一个捕获组: {pattern!r}")
            for m in regex.finditer(text):
                seen += 1
                number = int(m.group(1))
                if number != expected:
                    findings.append({
                        "rule": rule.get("name", "count-matches"),
                        "severity": severity,
                        "file": rel,
                        "line": _line_of(text, m.start()),
                        "message": (
                            f"{rel}:{_line_of(text, m.start())} 声称 {number}（{' '.join(m.group(0).split())}）;"
                            f" 唯一来源 {detail} 是 {expected}"
                        ),
                    })
    if seen < min_claims:
        findings.append({
            "rule": rule.get("name", "count-matches"),
            "severity": severity,
            "file": ",".join(_as_list(rule.get("claim_files"))) or "(未配置)",
            "line": 0,
            "message": (
                f"一条声明都没抓到时规则形同虚设（min_claims={min_claims}）;"
                f"确认 claim_files/claim_patterns 仍对准公开声明（唯一来源 {detail} = {expected}）"
            ),
        })
    return findings


def check_forbid_pattern(repo: str, rule: dict) -> list[dict]:
    findings: list[dict] = []
    severity = rule.get("severity", "FAIL")
    pattern = rule.get("pattern")
    if not pattern:
        raise ValueError("forbid-pattern 需要 pattern")
    regex = re.compile(pattern)
    ignore = re.compile(rule["ignore"]) if rule.get("ignore") else None
    for rel in _as_list(rule.get("files")) or _as_list(rule.get("file")):
        path = os.path.join(repo, rel)
        if not os.path.isfile(path):
            raise ValueError(f"forbid-pattern 目标文件不存在: {rel}")
        text = _read(path)
        for line_no, line in enumerate(text.splitlines(), 1):
            if ignore and ignore.search(line):
                continue
            m = regex.search(line)
            if m:
                findings.append({
                    "rule": rule.get("name", "forbid-pattern"),
                    "severity": severity,
                    "file": rel,
                    "line": line_no,
                    "message": f"{rel}:{line_no} 命中禁用表述 {m.group(0)!r}",
                })
    return findings


def check_require_pattern(repo: str, rule: dict) -> list[dict]:
    findings: list[dict] = []
    severity = rule.get("severity", "FAIL")
    rel = rule.get("file")
    pattern = rule.get("pattern")
    if not rel or not pattern:
        raise ValueError("require-pattern 需要 file 与 pattern")
    path = os.path.join(repo, rel)
    if not os.path.isfile(path):
        raise ValueError(f"require-pattern 目标文件不存在: {rel}")
    min_count = rule.get("min_count", 1)
    found = len(re.findall(pattern, _read(path)))
    if found < min_count:
        findings.append({
            "rule": rule.get("name", "require-pattern"),
            "severity": severity,
            "file": rel,
            "line": 0,
            "message": f"{rel} 必现短语未满足（命中 {found}/{min_count}）: {pattern!r}",
        })
    return findings


def run(repo: str, config_path: str | None, fmt: str, strict: bool) -> int:
    repo = os.path.abspath(repo)
    cfg_path = config_path or os.path.join(repo, "lint-checks.json")
    if not os.path.isfile(cfg_path):
        print(f"check-claims: 没能检查——找不到 {cfg_path}（未测量，不得记为通过）。", file=sys.stderr)
        return 2
    try:
        cfg = _load_json(cfg_path)
        rules = [r for r in cfg.get("checks", []) if isinstance(r, dict) and r.get("type", "require-pattern") in HANDLED_TYPES]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"check-claims: 配置不可用：{exc}", file=sys.stderr)
        return 2
    if not rules:
        print(
            "check-claims: 没能检查——lint-checks.json 没有 count-matches / forbid-pattern / "
            "require-pattern 规则可执行（未测量，不得记为通过）。",
            file=sys.stderr,
        )
        return 2

    findings: list[dict] = []
    errors: list[str] = []
    for i, rule in enumerate(rules, 1):
        rtype = rule.get("type", "require-pattern")
        try:
            if rtype == "count-matches":
                findings.extend(check_count_matches(repo, rule))
            elif rtype == "forbid-pattern":
                findings.extend(check_forbid_pattern(repo, rule))
            else:
                findings.extend(check_require_pattern(repo, rule))
        except (OSError, ValueError) as exc:
            errors.append(f"checks[{i}]（{rule.get('name', rtype)}）配置/目标不可用：{exc}")

    if strict:
        for f in findings:
            f["severity"] = "FAIL"
    hard = [f for f in findings if f["severity"] == "FAIL"]
    soft = [f for f in findings if f["severity"] != "FAIL"]

    if fmt == "json":
        print(json.dumps(
            {"repo": repo, "config": cfg_path, "findings": findings, "errors": errors,
             "summary": {"fail": len(hard), "warn": len(soft)}},
            ensure_ascii=False, indent=2))
    else:
        for err in errors:
            print(f"  ✗ {err}")
        for f in hard:
            print(f"  ✗ [{f['rule']}] {f['message']}")
        for f in soft:
            print(f"  ~ [{f['rule']}] {f['message']}")
        print("")
        print("=" * 40)
        if errors:
            print(f"对账结果: {len(errors)} 条规则无法执行（按未测量处理）")
        if hard or soft:
            print(f"对账结果: {len(hard)} error, {len(soft)} warning")
        if not errors and not findings:
            print("对账结果: 声明与仓库事实一致（计数唯一来源 + 必现短语 + 禁用语表）")
    if hard:
        return 1
    return 2 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check-claims.py",
        description="公开声明 × 仓库事实对账：计数对账（唯源 INDEX）+ 必现短语 + 禁用语表。",
        epilog="规则 schema 见脚本头注；退出码三态见 scripts/EXIT-CODES.md。示例:\n"
        "  python3 scripts/check-claims.py .\n"
        "  python3 scripts/check-claims.py . --format json --strict",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("repo", nargs="?", default=".", help="仓库根（默认当前目录）")
    parser.add_argument("--lint-checks", default=None, help="lint-checks.json 路径（默认 <repo>/lint-checks.json）")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式（默认 text）")
    parser.add_argument("--strict", action="store_true", help="把全部发现升级为 error 级")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return run(args.repo, args.lint_checks, args.format, args.strict)


if __name__ == "__main__":
    sys.exit(main())
