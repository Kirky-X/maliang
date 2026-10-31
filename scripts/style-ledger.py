#!/usr/bin/env python3
"""style-ledger —— 跨项目外观账本:每次交付记一条外观指纹,开工前查重复。

用法:
    python3 scripts/style-ledger.py add --project <名> <DESIGN.md 路径>
    python3 scripts/style-ledger.py check [--last N]
    python3 scripts/style-ledger.py list
    公共参数: [--home PATH](默认 ~/.maliang;测试与多环境用)

账本: {home}/style-ledger.jsonl,JSON Lines 只追加,只在本机,不随 skill 分发。
指纹从 DESIGN.md frontmatter 的结构化 token 提取(不解析 HTML):底色 /
主色 / 色板 / display·body 字族 / 一句话 desc。

为产出史,与 profile.json 偏好先验、项目 .maliang/feedback/ 协作规则账本、
项目内 build-log 构图轮换四账分工,互不写入——登记表见 feedback-ledger.md §8):
  - explore / draw-md 开工前:`check` —— 最近 N 个交付反复出现的底色/字体/
    主色,这次主动避开(报告,不阻塞;项目 brief 与 DESIGN.md 契约永远优先)
  - design-md 交付后:`add` —— 用户认可的外观看齐产物落一条
  - 任意时点:`list` —— 全部历史
退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查)。
check 是报告型:空账本与有重复都退 0(重复是提示不是拦截);add 的目标
文件缺失或无 frontmatter 退 2(没能提取,不得记为已记录)。
依赖: Python 3 标准库(无第三方依赖;PyYAML 可选,同 maliang_common 骨架)。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import maliang_common
import design_md_to_token_md as dmt

HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
LEDGER_FILE = "style-ledger.jsonl"
DEFAULT_HOME = os.path.join(os.path.expanduser("~"), ".maliang")
BG_PRIMARY_KEYS = ("surface-base", "background", "surface", "base", "bg")
PRIMARY_KEYS = ("primary", "brand-primary", "accent", "brand")
DISPLAY_KEYS = ("font-family-display", "display", "font-display", "title")
BODY_KEYS = ("font-family-ui", "body", "font-body", "text")
# 键族排除前缀(架构审查 H1:包含匹配会把 text-primary/bg-primary 记成
# 主色、background-muted 记成底色——canonical 色板只有 bg-primary/
# text-primary 形状,无裸 primary 键)
_BG_EXCLUDE = ("text-", "border-", "divider-", "shadow-")
_PRIMARY_EXCLUDE = ("text-", "border-", "bg-", "surface-", "divider-", "shadow-")
CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")
_FLATTEN_MAX_DEPTH = 8


def _norm_hex(raw):
    """'#ABC'→'#AABBCC' 与 validate-generated 同口径;非法返回 None。"""
    v = raw.lower()
    if re.fullmatch(r"#[0-9a-f]{3,4}", v):
        v = "#" + "".join(c * 2 for c in v[1:])
    return v if re.fullmatch(r"#[0-9a-f]{6}([0-9a-f]{2})?", v) else None


def sanitize(text):
    """剥离控制字符(\x00-\x1f\x7f)后回显——frontmatter 值是半不可信输入
    (安全审查 M1:终端转义序列注入与输出行伪造面),落盘侧 json.dumps
    已转义,只有 stdout 回显需要消毒。"""
    return CONTROL_CHARS_RE.sub("", str(text))


def _flatten_value(value, depth=0):
    """token 值展平为字符串:dict 取 fontFamily/family/size 等叶子,
    list 取首项;其余 str()。深度超限返回 ""(递归别名/超深嵌套断路)。"""
    if depth > _FLATTEN_MAX_DEPTH:
        return ""
    if isinstance(value, dict):
        for leaf_key in ("fontFamily", "family", "size", "value", "fontWeight"):
            if leaf_key in value:
                return _flatten_value(value[leaf_key], depth + 1)
        for v in value.values():
            return _flatten_value(v, depth + 1)
        return ""
    if isinstance(value, list):
        return _flatten_value(value[0], depth + 1) if value else ""
    return str(value)


def _hex_of(value):
    """取值串里第一个可归一 hex;无则 None。"""
    for m in HEX_RE.finditer(_flatten_value(value)):
        norm = _norm_hex(m.group(0))
        if norm:
            return norm
    return None


def _first_font(value):
    """字族值取第一个族名(去引号);无则 None。"""
    s = _flatten_value(value).strip().strip("\"'")
    first = s.split(",")[0].strip().strip("\"'")
    return first or None


def _bg_class(bg_hex):
    """底色分类:WCAG 亮度三档(深底/中底/浅底)。解析失败归「未知底」。"""
    if not bg_hex or len(bg_hex) < 7:
        return "未知底"
    try:
        rgb = maliang_common.hex_to_rgb255(bg_hex[:7])
        lum = maliang_common.relative_luminance(tuple(v / 255.0 for v in rgb))
    except (ValueError, TypeError):
        return "未知底"
    if lum < 0.2:
        return "深底"
    if lum > 0.75:
        return "浅底"
    return "中底"


def _pick(colors, keys, exclude_prefixes):
    """colors 块里按键名优先级找值:精确名优先,再前缀匹配
    (name == key 或 name.startswith(key + "-")),命中排除前缀的键族跳过
    (架构审查 H1:防 text-primary/bg-primary 被记成主色)。"""
    for key in keys:
        for name, value in colors.items():
            name_l = str(name).lower()
            if name_l != key and not name_l.startswith(key + "-"):
                continue
            if any(name_l.startswith(p) for p in exclude_prefixes):
                continue
            return value
    return None


def extract_fingerprint(design_text):
    """从 DESIGN.md 文本提取外观指纹;无 frontmatter/非映射返回 None。

    bg 取底色系键,primary 取主色系键,palette 收 colors 块全部 hex(≤8),
    字族取 typography 的 display/body 键。解析不到的项为 None,desc 如实
    写「?」——不编造(既定口径:指纹只量事实)。
    """
    yaml_str, _body = dmt.extract_frontmatter(design_text)
    if not yaml_str.strip():
        return None
    # canonical 优先(dmt.parse_frontmatter,与 validate-design-md 同路径,
    # PyYAML 报错即 raise);宽容兜底:真实产物的字族值(如 "Fraunces",
    # serif)PyYAML 严格语法会拒收,报错时降级逐行解析。两路都拿不到
    # 映射 → 无指纹返回 None(不记垃圾行,安全审查 L2)。
    try:
        data = dmt.parse_frontmatter(yaml_str)
    except Exception:
        data = maliang_common.parse_frontmatter_lenient(yaml_str)
    if not isinstance(data, dict) or not data:
        return None
    colors = data.get("colors") if isinstance(data.get("colors"), dict) else {}
    typo = data.get("typography") if isinstance(data.get("typography"), dict) else {}
    if not colors and not typo:
        return None
    bg = _hex_of(_pick(colors, BG_PRIMARY_KEYS, _BG_EXCLUDE) or "")
    primary = _hex_of(_pick(colors, PRIMARY_KEYS, _PRIMARY_EXCLUDE) or "")
    palette = []
    for value in colors.values():
        h = _hex_of(value)
        if h and h not in palette:
            palette.append(h)
        if len(palette) >= 8:
            break
    font_display = _first_font(_pick(typo, DISPLAY_KEYS, ()) or "")
    font_body = _first_font(_pick(typo, BODY_KEYS, ()) or "")
    desc = "%s %s,主色 %s,display %s / body %s" % (
        _bg_class(bg), bg or "?", primary or "?",
        font_display or "?", font_body or "?")
    return {
        "bg": bg,
        "bg_class": _bg_class(bg),
        "primary": primary,
        "palette": palette,
        "font_display": font_display,
        "font_body": font_body,
        "desc": desc,
    }


def _ledger_path(home):
    return os.path.join(home, LEDGER_FILE)


def _append(home, row):
    os.makedirs(home, exist_ok=True)
    with open(_ledger_path(home), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_rows(home):
    path = os.path.join(home, LEDGER_FILE)
    if not os.path.isfile(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                print("[WARN] 跳过损坏行: " + sanitize(line[:60]), file=sys.stderr)
                continue
            # 类型守卫(安全审查 L3):合法 JSON 但非对象/缺 fp 的行按损坏处理
            if not isinstance(row, dict) or not isinstance(row.get("fp"), dict):
                print("[WARN] 跳过非账本行: " + sanitize(line[:60]), file=sys.stderr)
                continue
            rows.append(row)
    return rows


def _already_recorded(rows, project, design_path):
    """同一 (project, path) 已记过 → True(架构审查 L4:append-only 账本
    的幂等守卫,重复 add 会虚增 check 的重复信号)。"""
    return any(r.get("project") == project and r.get("path") == design_path
               for r in rows)


def cmd_add(home, project, design_path):
    """add:提取指纹并追加一条;目标缺失/无指纹退 2(没能提取)。"""
    if not os.path.isfile(design_path):
        print("[ERROR] 目标文件不存在: " + design_path)
        print("没能提取,不得记为已记录(见 scripts/EXIT-CODES.md)。")
        return 2
    with open(design_path, "r", encoding="utf-8") as fh:
        fp = extract_fingerprint(fh.read())
    if fp is None:
        print("[ERROR] " + design_path + " 无 frontmatter(或不是映射),"
              "提取不到外观指纹")
        print("没能提取,不得记为已记录(见 scripts/EXIT-CODES.md)。")
        return 2
    if _already_recorded(_load_rows(home), project, design_path):
        print("已存在同 (project, path) 记录,未重复记账: "
              + sanitize(project) + " — " + design_path)
        return 0
    _append(home, {
        "ts": datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "project": project,
        "path": design_path,
        "fp": fp,
    })
    print("已记账: " + sanitize(project) + " — " + sanitize(fp["desc"]))
    print("  账本: " + _ledger_path(home))
    return 0


def cmd_check(home, last):
    """check:最近 N 条里反复出现的底色/主色/字族点名提示(报告,不阻塞)。

    账本为空 → 显式提示「无历史可查」退 0;有重复也退 0——它是开工前的
    避让提示,不是门禁;项目 brief 与 DESIGN.md 契约永远优先。
    """
    rows = _load_rows(home)[-last:]
    if not rows:
        print("外观账本为空或缺失(" + _ledger_path(home) + "),无历史可查。")
        return 0
    print("最近 " + str(len(rows)) + " 个交付的外观:")
    for row in rows:
        print("  " + sanitize(row.get("project", "?")) + " — "
              + sanitize(row.get("fp", {}).get("desc", "?")))
    repeats = []
    for field, label in (("bg", "底色"), ("primary", "主色"),
                         ("font_display", "display 字族"),
                         ("font_body", "body 字族")):
        counts = {}
        for row in rows:
            value = row.get("fp", {}).get(field)
            if value:
                counts.setdefault(value, []).append(row.get("project", "?"))
        for value, projects in sorted(counts.items(), key=lambda kv: -len(kv[1])):
            if len(projects) >= 2:
                repeats.append(label + " " + value + "("
                               + ", ".join(projects) + ")")
    if repeats:
        print("")
        print("反复出现(本次主动避开,除非 brief 要求):")
        for item in repeats:
            print("  - " + item)
    else:
        print("")
        print("无重复项。")
    return 0


def cmd_list(home):
    """list:全部条目逐行列出。"""
    rows = _load_rows(home)
    if not rows:
        print("外观账本为空(" + _ledger_path(home) + ")。")
        return 0
    for row in rows:
        print(sanitize(row.get("ts", "?")) + "  "
              + sanitize(row.get("project", "?")) + "  "
              + sanitize(row.get("fp", {}).get("desc", "?")))
    return 0


def main(argv):
    parser = argparse.ArgumentParser(
        description="跨项目外观账本:指纹提取 / add / check / list"
                    "(退出码见 scripts/EXIT-CODES.md)")
    parser.add_argument("--home", default=DEFAULT_HOME,
                        help="账本目录(默认 ~/.maliang)")
    sub = parser.add_subparsers(dest="subcommand")
    p_add = sub.add_parser("add", help="记一条外观指纹")
    p_add.add_argument("--project", required=True, help="项目名")
    p_add.add_argument("design_md", help="DESIGN.md 路径")
    p_check = sub.add_parser("check", help="最近 N 条的重复项报告")
    p_check.add_argument("--last", type=int, default=8,
                         help="回看条数(默认 8)")
    sub.add_parser("list", help="列出全部条目")
    args = parser.parse_args(argv)

    if args.subcommand == "add":
        return cmd_add(args.home, args.project, args.design_md)
    if args.subcommand == "check":
        return cmd_check(args.home, max(1, args.last))
    if args.subcommand == "list":
        return cmd_list(args.home)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
