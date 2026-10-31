#!/usr/bin/env python3
"""version-check —— skill 版本检查的确定性逻辑(SKILL.md「版本检查」节落点)。

用法:
    python3 scripts/version-check.py due [--state PATH]      该不该查(节流判定)
    python3 scripts/version-check.py compare <tag> [--current X.Y.Z]
    python3 scripts/version-check.py record ok|failed|off [--state PATH]

三步与 SKILL.md「版本检查」节对应(架构审查 M4:日期节流与版本比较是
确定性逻辑,进脚本;agent 只跑本脚本 + git ls-remote):
  1. `due` —— 读状态文件,输出 `due`(该查)或 `skip:<原因>`(off/30 天内
     ok/7 天内 failed)。无状态文件 = due。
  2. agent 跑 `git -C {SKILL_DIR} ls-remote --tags --refs --sort=-v:refname origin 'v*'`,
     取第一行 tag 传给 `compare`——`newer`(远程更高,报话术)/ `same`
     (含远程更旧与 tag 不符合 vX.Y.Z 形状:按没有标签处理,不回显)。
  3. `record ok|failed` 把 `<今天> <结果>` 写进状态文件;`record off` 是
     用户关掉检查的唯一写法。

状态文件默认 `~/.maliang/version-check`(架构审查 L3:状态统一落用户
主目录,不写 SKILL_DIR——插件缓存等只读安装下不退化)。
退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;
record 参数非法退 2;due/compare 是判定型,恒 0)。
依赖: Python 3 标准库(无第三方依赖)。
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta

DEFAULT_STATE = os.path.join(os.path.expanduser("~"), ".maliang", "version-check")
DEFAULT_VERSION = "0.0.0"
OK_FRESH_DAYS = 30
FAILED_FRESH_DAYS = 7
TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
VER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def _read_state(path):
    """读状态文件 → (日期, 结果);无文件/空文件 → (None, None)。

    两种合法形态:`YYYY-MM-DD ok|failed`(标准)与 `off`(关闭)。
    单 token 旧格式按「只有日期的 ok」算,但 `off` 单词本身是关闭指令,
    不按日期解析。"""
    if not os.path.isfile(path):
        return None, None
    with open(path, "r", encoding="utf-8") as fh:
        first = fh.readline().strip()
    if not first:
        return None, None
    parts = first.split()
    if len(parts) == 1:
        if parts[0] == "off":
            return "", "off"
        return parts[0], "ok"      # 只有日期的旧格式按 ok 算(SKILL.md 约定)
    return parts[0], parts[1]


def _parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return None


def cmd_due(state):
    last_date, last_result = _read_state(state)
    if last_result == "off":
        print("skip:off")
        return 0
    today = datetime.now()
    if last_date:
        d = _parse_date(last_date)
        if d:
            age = (today - d).days
            if last_result == "failed":
                if age < FAILED_FRESH_DAYS:
                    print("skip:fresh-failed(" + str(age) + "d)")
                    return 0
            elif age < OK_FRESH_DAYS:
                print("skip:fresh(" + str(age) + "d)")
                return 0
    print("due")
    return 0


def _semver_tuple(text, regex):
    m = regex.match(text.strip())
    if not m:
        return None
    return tuple(int(g) for g in m.groups())


def cmd_compare(tag, current):
    remote = _semver_tuple(tag, TAG_RE)
    if remote is None:
        # tag 不符合 vX.Y.Z 形状按没有标签处理(安全审查 L4:不回显来源侧文本)
        print("same(无有效版本标签)")
        return 0
    cur = _semver_tuple(current, VER_RE) or _semver_tuple(DEFAULT_VERSION, VER_RE)
    if remote > cur:
        print("newer " + tag.strip())
    else:
        print("same")
    return 0


def cmd_record(value, state):
    if value == "off":
        os.makedirs(os.path.dirname(state) or ".", exist_ok=True)
        with open(state, "w", encoding="utf-8") as fh:
            fh.write("off\n")
        print("已关闭版本检查(" + state + ")")
        return 0
    if value not in ("ok", "failed"):
        print("[ERROR] record 取值须为 ok|failed|off: " + value)
        return 2
    os.makedirs(os.path.dirname(state) or ".", exist_ok=True)
    with open(state, "w", encoding="utf-8") as fh:
        fh.write(datetime.now().strftime("%Y-%m-%d") + " " + value + "\n")
    print("已记录: " + value + " → " + state)
    return 0


def main(argv):
    parser = argparse.ArgumentParser(
        description="skill 版本检查的确定性逻辑:due / compare / record"
                    "(退出码见 scripts/EXIT-CODES.md)")
    parser.add_argument("--state", default=DEFAULT_STATE,
                        help="状态文件路径(默认 ~/.maliang/version-check)")
    sub = parser.add_subparsers(dest="subcommand")
    sub.add_parser("due", help="该不该查(节流判定)")
    p_cmp = sub.add_parser("compare", help="远程 tag 与当前版本比较")
    p_cmp.add_argument("tag", help="git ls-remote 第一行的 tag(如 v0.4.0)")
    p_cmp.add_argument("--current", default=None,
                       help="当前版本(默认读本仓 SKILL.md frontmatter)")
    p_rec = sub.add_parser("record", help="记录检查结果 ok|failed|off")
    p_rec.add_argument("value", help="ok|failed|off(非法取值退 2)")
    args, extra = parser.parse_known_args(argv)

    if args.subcommand == "due":
        return cmd_due(args.state)
    if args.subcommand == "compare":
        current = args.current or _read_current_version()
        return cmd_compare(args.tag, current)
    if args.subcommand == "record":
        return cmd_record(args.value, args.state)
    parser.print_help()
    return 2


def _read_current_version():
    """从本仓 SKILL.md frontmatter 读 metadata.version;读不到退 0.0.0。"""
    skill_md = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "SKILL.md")
    try:
        with open(skill_md, "r", encoding="utf-8") as fh:
            for line in fh:
                m = re.search(r'version:\s*"(\d+\.\d+\.\d+)"', line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return DEFAULT_VERSION


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
