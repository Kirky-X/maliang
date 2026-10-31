#!/usr/bin/env python3
"""check-claims —— 公开声明 × 仓库事实对账。

文档里手写的数字会漂移：模板墙加了两个设计语言，SKILL.md 与 README 里的
「12 种」不会自己改。本脚本按 lint-checks.json 的规则把公开声明对账到**唯一

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
denylist)与 .github/workflows/validate-engine.yml, 中文自研实现。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# 规则引擎唯一实现见 maliang_common(仓内 canonical);skill_lint.py 为可 vendored 的
# 自包含孪生副本(兄弟仓 CI 用,不依赖本仓模块)——改引擎语义时两处联动,
# tests/test_maliang_common.py 的孪生一致性测试守护两侧同判。
from maliang_common import (  # noqa: E402
    ENGINE_RULE_TYPES as HANDLED_TYPES,
    engine_run_rule as _engine_run_rule,
)


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("lint-checks.json 顶层必须是对象")
    return data


def run(repo: str, config_path: str | None, fmt: str, strict: bool) -> int:
    repo = os.path.abspath(repo)
    cfg_path = config_path or os.path.join(repo, "lint-checks.json")
    if not os.path.isfile(cfg_path):
        print(f"check-claims: 没能检查——找不到 {cfg_path}（未测量，不得记为通过）。", file=sys.stderr)
        return 2
    try:
        cfg = _load_json(cfg_path)
        rules = [r for r in cfg.get("checks", []) if isinstance(r, dict)]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"check-claims: 配置不可用：{exc}", file=sys.stderr)
        return 2
    if not any(r.get("type", "require-pattern") in HANDLED_TYPES for r in rules):
        print(
            "check-claims: 没能检查——lint-checks.json 没有本脚本可执行的规则类型"
            "（未测量，不得记为通过）。",
            file=sys.stderr,
        )
        return 2

    findings: list[dict] = []
    errors: list[str] = []
    skipped: list[str] = []
    for i, rule in enumerate(rules, 1):
        rtype = rule.get("type", "require-pattern")
        if rtype not in HANDLED_TYPES:
            # 显性跳过(不再静默过滤):该类型由 skill_lint 的 check_repo_rules 执行
            skipped.append(f"checks[{i}]（{rule.get('name', rtype)}）type={rtype}")
            continue
        try:
            findings.extend(_engine_run_rule(repo, rule))
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
        for s in skipped:
            print(f"  ~ 跳过(由 skill_lint 执行): {s}")
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
