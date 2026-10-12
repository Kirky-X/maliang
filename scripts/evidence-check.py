#!/usr/bin/env python3
"""evidence-check —— 取证契约校验（截图证据齐套性检查）。

"看一眼"与"取证"是两种用途：看一眼只截当前屏；取证一次取齐，只在送评审前与
交付前做。本脚本校验一次取证产出的 `report.json` 是否齐套——缺项不是"跳过"，
是把结论推到 `unverified`（未验证不得记为通过、disposition 不得为 deliver）。

report.json 契约（maliang-evidence/1，纯 JSON，路径相对 report.json 所在目录）:

    {
      "schema": "maliang-evidence/1",
      "capturedAt": "2026-10-12T10:00:00+08:00",
      "pages": [
        {
          "page": "preview_home_iphone15.html",
          "viewport": "390x844",
          "sheet": "shots/sheet-home.png",          # 并排图（≥2 个状态时必填）
          "motion": "probe/home-motion.json",       # 动效探测（必填）
          "recording": "record/home.mp4",           # 录屏（必填）
          "states": [
            {
              "state": "idle",
              "shot": "shots/home-idle.png",        # 状态图（必填）
              "shot2x": "shots/home-idle@2x.png",   # 2x 图（必填）
              "masked": "shots/home-idle-masked.png"# 遮字图（必填）
            }
          ]
        }
      ]
    }

规则（来源: oil-ui/references/tools.md「什么时候截，截多少/看结果」与
scripts/shoot.mjs 的 report 结构, 2026-10 吸收, 中文自研实现）:
  - 每页每状态必齐 状态图 / 2x 图 / 遮字图；每页必齐 动效探测 / 录屏；
    多状态页必齐 并排图（单状态页无并排图可言，记为 n/a 而非缺项）；
  - 任一被引用文件不存在或为空 → 该槽位计缺项（空文件不是证据）；
  - 同一文件被多个槽位复用 → 计问题（2x 图与状态图同文件、并排图与状态图同
    文件都是假齐套）；
  - 条目带 `failed: true` / `skipped: true` → 计缺项并在清单里转录原因；
  - 空 WebGL 截图不当证据（内容级别判断超出静态校验能力，见 preview.md 取证契约节）。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
  0 = 齐套；1 = 有缺项/问题；2 = 没能检查（找不到 report.json / 用法错误）。
依赖: Python 3 标准库(无第三方依赖)。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SCHEMA_NAME = "maliang-evidence/1"
REQUIRED_REPORT_FILES = ("report.json",)
STATE_SLOTS = (("shot", "状态图"), ("shot2x", "2x 图"), ("masked", "遮字图"))
PAGE_SLOTS = (("motion", "动效探测"), ("recording", "录屏"))


def _slot_path(value) -> str | None:
    """槽位取值：字符串路径，或 {"file": path} 形态；其余视为未提供。"""
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("file", "path"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return None


def _find_reports(target: str) -> list[str]:
    """目标为 report.json 文件，或含 report.json 的目录（递归）。"""
    if os.path.isfile(target):
        return [os.path.abspath(target)]
    if os.path.isdir(target):
        found = []
        for dirpath, _, filenames in os.walk(target):
            for fn in filenames:
                if fn in REQUIRED_REPORT_FILES:
                    found.append(os.path.abspath(os.path.join(dirpath, fn)))
        return sorted(found)
    return []


def check_report(report_path: str) -> dict:
    """校验单个 report.json；返回 {problems, missing, notes, pages}。"""
    problems: list[str] = []
    missing: list[str] = []
    notes: list[str] = []
    base = os.path.dirname(os.path.abspath(report_path))
    with open(report_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError(
            "report.json 顶层必须是对象（含 schema 与 pages[]）；"
            "扁平条目数组不是本契约的形态"
        )
    schema = raw.get("schema")
    if schema != SCHEMA_NAME:
        problems.append(f"schema={schema!r} 不是 {SCHEMA_NAME!r}（契约版本不符）")
    pages = raw.get("pages")
    if not isinstance(pages, list) or not pages:
        problems.append("pages[] 缺省或为空（没有任何页面的取证不成立）")
        return {"problems": problems, "missing": missing, "notes": notes, "pages": 0}
    seen_paths: dict[str, str] = {}

    def require_file(rel: str, slot_label: str, where: str) -> None:
        abs_path = os.path.normpath(os.path.join(base, rel))
        if not os.path.isfile(abs_path):
            missing.append(f"{where} 缺 {slot_label}: {rel}（文件不存在）")
            return
        if os.path.getsize(abs_path) == 0:
            missing.append(f"{where} 缺 {slot_label}: {rel}（文件为空，空文件不是证据）")
            return
        owner = seen_paths.get(abs_path)
        if owner:
            problems.append(
                f"{where} 的 {slot_label} 与 {owner} 复用同一文件 {rel}（假齐套）"
            )
        else:
            seen_paths[abs_path] = f"{where} {slot_label}"

    for index, page in enumerate(pages, 1):
        if not isinstance(page, dict):
            problems.append(f"第 {index} 页不是对象")
            continue
        page_name = page.get("page") or page.get("id") or f"pages[{index}]"
        where_page = str(page_name)
        states = page.get("states")
        if not isinstance(states, list) or not states:
            problems.append(f"{where_page}: states[] 缺省或为空")
            states = []
        for slot, label in PAGE_SLOTS:
            rel = _slot_path(page.get(slot))
            if rel:
                require_file(rel, label, where_page)
            else:
                missing.append(f"{where_page} 缺 {label}（{slot}）")
        if len(states) >= 2:
            rel = _slot_path(page.get("sheet"))
            if rel:
                require_file(rel, "并排图", where_page)
            else:
                missing.append(f"{where_page} 缺 并排图（sheet）")
        elif "sheet" not in page:
            notes.append(f"{where_page}: 单状态页无并排图可查（n/a）")
        for sindex, state in enumerate(states, 1):
            if not isinstance(state, dict):
                problems.append(f"{where_page}: 第 {sindex} 个状态不是对象")
                continue
            state_name = state.get("state") or state.get("name") or f"states[{sindex}]"
            where = f"{where_page} · {state_name}"
            if state.get("failed") is True or state.get("skipped") is True:
                reason = state.get("reason") or state.get("error") or "条目自报失败/跳过"
                missing.append(f"{where}: 条目未完成（{reason}）")
                continue
            for slot, label in STATE_SLOTS:
                rel = _slot_path(state.get(slot))
                if rel:
                    require_file(rel, label, where)
                else:
                    missing.append(f"{where} 缺 {label}（{slot}）")
    return {"problems": problems, "missing": missing, "notes": notes, "pages": len(pages)}


def run(target: str, fmt: str) -> int:
    reports = _find_reports(target)
    if not reports:
        print(
            f"evidence-check: 没能检查——{target} 下找不到 report.json（未测量，不得记为通过）。",
            file=sys.stderr,
        )
        return 2
    total_missing = 0
    total_problems = 0
    results = []
    for report in reports:
        try:
            result = check_report(report)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"[FAIL] {report}: 报告不可解析或非法：{exc}", file=sys.stderr)
            total_problems += 1
            results.append({"report": report, "problems": [str(exc)], "missing": []})
            continue
        total_missing += len(result["missing"])
        total_problems += len(result["problems"])
        results.append({"report": report, **result})
        if fmt == "text":
            status = "FAIL" if (result["missing"] or result["problems"]) else "PASS"
            print(f"[{status}] {report}  ({result['pages']} 页)")
            for item in result["problems"]:
                print(f"  ✗ {item}")
            for item in result["missing"]:
                print(f"  ✗ {item}")
            for item in result["notes"]:
                print(f"  · {item}")
    if fmt == "json":
        print(json.dumps(
            {"reports": results, "missing": total_missing, "problems": total_problems},
            ensure_ascii=False, indent=2))
    else:
        print("")
        print("=" * 40)
        if total_missing or total_problems:
            print(
                f"取证结果: {total_missing} 项缺件, {total_problems} 项问题——"
                "缺项按 unverified 处理（未验证不得记为通过，disposition 不得为 deliver）；"
                "重取后重跑。"
            )
        else:
            print("取证结果: 齐套（状态图/2x/遮字/并排/动效探测/录屏）")
    return 1 if (total_missing or total_problems) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="evidence-check.py",
        description="取证契约校验：report.json 的截图证据齐套性（状态图/2x/并排/遮字/动效探测/录屏）。",
        epilog="report.json 契约见脚本头注；缺项推 unverified。示例:\n"
        "  python3 scripts/evidence-check.py shots/report.json\n"
        "  python3 scripts/evidence-check.py examples/preview/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", help="report.json 路径，或含 report.json 的目录")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式（默认 text）")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return run(args.target, args.format)


if __name__ == "__main__":
    sys.exit(main())
