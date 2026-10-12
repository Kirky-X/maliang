#!/usr/bin/env python3
"""轮换与盖章机械化核验(G41/G42 脚本层)。

读项目构建日志 `.maliang/build-log.json`(JSON 数组,新条目在前;契约见
references/templates/variation-engine.md「构建日志」节),做三查:

  1. immediate repeat  当前构建与日志最近一条同轴同值 —— reuse is only OK
                       if you changed a variation knob and said so(换旋钮并声明)。
  2. hot axis          最近 --window 条构建逐轴聚合,当前取值占比 ≥0.6 即为
                       「热轴默认」——除非 brief 明确要求,换掉并说明。
  3. stamp lies        --stamp 给出时,解析页面盖章 `/* maliang · mode=... · A=...`
                       的坐标,与 --current 声明的 stamp 字段逐键对账;键集或值
                       不一致 = 章与声明不符(G41,章说谎比缺章严重)。

七轴键集(theme/background/typography/hero/section/signature/motion)以
variation-engine.md 为唯一词表;本脚本只做机械一致性,轴值优劣不由脚本判断。

来源: tastemaker scripts/check_structure_history.py(#31)immediate repeat +
hot axis 思想,2026-10 吸收;stamp-lies 与 hallmark(#19)同门合并(裁决见
.absorb-external/ui-benchmark-batch2-findings.md #31)。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)。
        build-log 缺失或非法 = UNMEASURED → 2(G42:不得记通过)。
依赖: Python 3 标准库。
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# 七轴键集(variation-engine.md「构建日志」契约;新条目在前)
AXES_FIELDS = ("theme", "background", "typography", "hero", "section", "signature", "motion")

# 轴是「热」的占比阈值(外部原口径 0.6)
HOT_THRESHOLD = 0.6
# 窗口不足此数不做热轴判定(样本太少没有统计意义)
MIN_WINDOW_FOR_HOT_CHECK = 3

# 盖章坐标:`/* maliang · mode=Experience · A=deep-dark · B=tactile-texture ... */
_STAMP_MODE_RE = re.compile(r"maliang\s*·\s*mode=([^\s·*]+)")
_STAMP_AXIS_RE = re.compile(r"\b([A-G])=([^·\n*]+)")


def load_log(path):
    """读构建日志;缺失/非法返回 (None, 原因)——调用方按 UNMEASURED 处理。"""
    if not path.exists():
        return None, "构建日志不存在: %s" % path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, "构建日志不可解析: %s (%s)" % (path, exc)
    if not isinstance(data, list):
        return None, "构建日志必须是 JSON 数组(新条目在前): %s" % path
    return data, None


def check_immediate_repeat(current_axes, previous_axes):
    """当前构建逐轴对比日志最近一条;同轴同值即立即重复。"""
    problems = []
    for field in AXES_FIELDS:
        cur, prev = current_axes.get(field), previous_axes.get(field)
        if cur and prev and cur == prev:
            problems.append(
                "%s 与最近一次构建重复('%s')——reuse is only OK if you changed "
                "a variation knob and said so(换旋钮并声明)" % (field, cur)
            )
    return problems


def check_hot_axis(current_axes, window, window_size):
    """逐轴统计最近窗口的取值分布;当前取值占比 ≥0.6 即热轴告警。

    window 是 build-log 条目(新条目在前),轴值在条目的 axes 子对象里。
    """
    problems = []
    if len(window) < MIN_WINDOW_FOR_HOT_CHECK:
        return problems
    for field in AXES_FIELDS:
        cur = current_axes.get(field)
        if not cur:
            continue
        counts = Counter()
        for e in window:
            if not isinstance(e, dict):
                continue
            axes = e.get("axes")
            if not isinstance(axes, dict):
                continue
            val = axes.get(field)
            if val:
                counts[val] += 1
        total = sum(counts.values())
        if total == 0:
            continue
        share = counts.get(cur, 0) / total
        if share >= HOT_THRESHOLD:
            problems.append(
                "%s '%s' 占最近 %d 条构建的 %d/%d —— it's the hot default right now;"
                "除非 brief 明确要求,换掉并说明" % (field, cur, window_size, counts[cur], total)
            )
    return problems


def parse_stamp(text):
    """提取盖章坐标,返回 (mode, {A:..~G:..});无盖章返回 (None, {})。"""
    mode = None
    m = _STAMP_MODE_RE.search(text)
    if m:
        mode = m.group(1).strip()
    axes = {}
    for m in _STAMP_AXIS_RE.finditer(text):
        axes[m.group(1)] = m.group(2).strip()
    return mode, axes


def check_stamp_lies(stamp_text, current):
    """盖章与当前构建声明逐键对账;不一致即 stamp lies(G41)。"""
    declared = current.get("stamp")
    if not isinstance(declared, dict):
        return [], []
    problems = []
    stamp_mode, stamp_axes = parse_stamp(stamp_text)
    if stamp_mode is None and not stamp_axes:
        problems.append("页面里没有找到 `/* maliang · ... */` 盖章——缺章(major;G41)")
        return problems, []
    declared_mode = declared.get("mode")
    if declared_mode and stamp_mode and stamp_mode != declared_mode:
        problems.append(
            "盖章 mode=%s 与声明 mode=%s 不符——stamp lies(G41;改章或改页面,二者取实)"
            % (stamp_mode, declared_mode)
        )
    for key, want in sorted(declared.items()):
        if key == "mode":
            continue
        got = stamp_axes.get(key)
        if got is None:
            problems.append("盖章缺坐标 %s(声明为 '%s')——章与实物不符(G41)" % (key, want))
        elif got != str(want):
            problems.append(
                "盖章 %s=%s 与声明 '%s' 不符——stamp lies(G41;改章或改页面,二者取实)"
                % (key, got, want)
            )
    return problems, [k for k in stamp_axes if k not in declared]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="轮换与盖章机械化核验(G41/G42):immediate repeat + hot axis(0.6) + stamp lies"
    )
    parser.add_argument(
        "--current", required=True,
        help="本次构建声明 JSON 文件:{page, axes:{七轴}, stamp:{mode, A..G}(可选)}",
    )
    parser.add_argument(
        "--log", default=".maliang/build-log.json",
        help="构建日志路径(默认 .maliang/build-log.json;缺失 = UNMEASURED/exit 2)",
    )
    parser.add_argument(
        "--stamp", default=None,
        help="含 `/* maliang · ... */` 盖章的 HTML/CSS 文件(给出时做 stamp-lies 对账)",
    )
    parser.add_argument("--window", type=int, default=5, help="热轴统计窗口条数(默认 5)")
    args = parser.parse_args(argv)

    current_path = Path(args.current)
    if not current_path.exists():
        print("check-structure-history: --current 文件不存在: %s" % current_path, file=sys.stderr)
        return 2
    try:
        current = json.loads(current_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print("check-structure-history: --current 不可读: %s" % exc, file=sys.stderr)
        return 2
    if not isinstance(current, dict) or not isinstance(current.get("axes"), dict):
        print("check-structure-history: --current 须为 {page, axes:{...}} 形态", file=sys.stderr)
        return 2
    current_axes = current["axes"]

    log, reason = load_log(Path(args.log))
    if log is None:
        print("check-structure-history: UNMEASURED —— %s(G42:日志缺失不得记通过)" % reason,
              file=sys.stderr)
        return 2

    problems = []
    if log:
        first = log[0]
        if isinstance(first, dict) and isinstance(first.get("axes"), dict):
            problems.extend(check_immediate_repeat(current_axes, first["axes"]))
    window = [e for e in log[: max(0, args.window)] if isinstance(e, dict)]
    problems.extend(check_hot_axis(current_axes, window, len(window)))

    stamp_extra = []
    if args.stamp:
        stamp_path = Path(args.stamp)
        if not stamp_path.exists():
            print("check-structure-history: --stamp 文件不存在: %s" % stamp_path, file=sys.stderr)
            return 2
        stamp_text = stamp_path.read_text(encoding="utf-8", errors="replace")
        stamp_problems, stamp_extra = check_stamp_lies(stamp_text, current)
        problems.extend(stamp_problems)

    checked = "历史 %d 条(窗口 %d)" % (len(log), len(window))
    if not problems:
        print("结构核验通过(%s):取值读作轮换%s" % (checked, ";盖章对账一致" if args.stamp else ""))
        if stamp_extra:
            print("  提示: 盖章含声明外的坐标 %s(信息性,不影响退出码)" % stamp_extra)
        return 0

    print("轮换/盖章违例(%s):" % checked)
    for p in problems:
        print("  - %s" % p)
    print("\n这是机械核验不是品味判断——重复可以是 brief 要的正确选择,但必须说明理由并换 knob。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
