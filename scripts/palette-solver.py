#!/usr/bin/env python3
"""OKLCH 亮度域配色求解器 + 全配对矩阵契约(G33 脚本层;按裁决 6 不含 MOODS)。

给定背景色与色相/彩度,在 OKLCH 亮度域求解三档可用前景色:
  text       对比度 ≥4.5(正文/链接/按钮标签)
  ui         对比度 ≥3.0(大字号/图标/传达状态的描边,WCAG 1.4.11)
  decorative 对比度 <3.0(纯装饰:发丝线/底纹;不得是传达状态的唯一手段)

  求解即安全:对每个目标档在 L=0.02..0.99 扫描,text/ui 取「达标且最接近
偏好亮度」的候选,decorative 取「恰低于 3.0 且亮度最贴近背景」的近底微差色
(发丝线/底纹的真实用法);chroma 不可达时按 0.85 逐步降(Adobe Leonardo 同
思路:亮度对比度目标求解)。外部原文的 MOODS 关键词查表**砍掉不吸收**——它
与 ai-tells §8 正面相抵,且查表本身就是新的同质化源(裁决 6)。

输出:三档角色色 + 全配对矩阵(每一对按其清的档分类)+「Legal pairings
(record these in the style lock)」清单。design-md Phase 0d 的颜色契约:
模型只能组合矩阵内配对;调色板扩充必须重跑矩阵。

来源: tastemaker scripts/generate_palette.py(:91-140 求解)+ check_contrast.py
(:83-111 矩阵分类)(#33),2026-10 吸收;MOODS 按裁决 6 砍除。

退出码: 见 scripts/EXIT-CODES.md(0=求解成功 / 1=有档位无解 / 2=没能检查;#16)。
依赖: Python 3 标准库。
"""

import argparse
import json
import math
import sys

AA_NORMAL = 4.5        # 正文文本档
AA_LARGE_OR_UI = 3.0   # UI 组件/大字号档

SOLVE_L_STEP = 0.01    # 亮度扫描步长(0.02..0.99)
CHROMA_DECAY = 0.85    # chroma 降档系数(外部原口径)
CHROMA_MAX_TRIES = 8
GAMUT_MAX_TRIES = 40


# ---------- sRGB <-> OKLab <-> OKLCH(移植自外部 generate_palette.py) ----------

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def _linear_rgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_ = l ** (1 / 3) if l > 0 else 0.0
    m_ = m ** (1 / 3) if m > 0 else 0.0
    s_ = s ** (1 / 3) if s > 0 else 0.0
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _oklab_to_linear_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_hex(L, C, H):
    """OKLCH -> hex;gamut 外按 0.92 降 chroma 至可显示(外部原口径)。"""
    hr = math.radians(H)
    c = C
    lr, lg, lb = 0.0, 0.0, 0.0
    for _ in range(GAMUT_MAX_TRIES):
        a, b = c * math.cos(hr), c * math.sin(hr)
        lr, lg, lb = _oklab_to_linear_rgb(L, a, b)
        if all(-1e-4 <= v <= 1 + 1e-4 for v in (lr, lg, lb)):
            break
        c *= 0.92
    lr, lg, lb = (min(1.0, max(0.0, v)) for v in (lr, lg, lb))
    r, g, b = (round(_linear_to_srgb(v) * 255) for v in (lr, lg, lb))
    return "%02x%02x%02x" % (r, g, b)


# ---------- WCAG 对比度(移植自外部 check_contrast.py) ----------

def _linearize(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) != 6:
        raise ValueError("expected 6-digit hex, got %r" % hex_color)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def contrast_ratio(hex1, hex2):
    l1, l2 = luminance(hex1), luminance(hex2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def classify(ratio):
    if ratio >= AA_NORMAL:
        return "text-safe (>=4.5)"
    if ratio >= AA_LARGE_OR_UI:
        return "UI-safe (>=3.0)"
    return "decorative (<3.0)"


# ---------- 亮度域求解 ----------

def oklch_L_of_hex(hex_color):
    """反查一个 hex 的 OKLCH 亮度(决定偏好方向:暗底求亮前景,反之求暗)。"""
    h = hex_color.lstrip("#")
    r, g, b = (_srgb_to_linear(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    return _linear_rgb_to_oklab(r, g, b)[0]


def solve_foreground(bg_hex, hue, chroma, floor, mode, prefer_l=None, objective="prefer"):
    """求对比度 ≥floor 的前景色;chroma 不可达按 0.85 逐步降。

    objective="prefer":对比度达标者里亮度最贴近 prefer_l(正文档,text)。
    objective="floor":达标者里对比度最贴近地板(UI 档,ui——贴着 3.0 的
    临界色,与 text 天然分离)。
    mode="at-most" 求装饰档:对比度 <3.0 且亮度最贴近背景(近底微差色,
    发丝线/底纹的真实用法;同时避免与 UI 档在同一边界撞色)。
    """
    bg_l = oklch_L_of_hex(bg_hex)
    if prefer_l is None:
        prefer_l = 0.85 if bg_l < 0.5 else 0.25

    def better(candidate, incumbent):
        if mode == "at-most":
            return abs(candidate[0] - bg_l) < abs(incumbent[0] - bg_l)
        if objective == "floor":
            return abs(candidate[2] - floor) < abs(incumbent[2] - floor)
        return abs(candidate[0] - prefer_l) < abs(incumbent[0] - prefer_l)

    c = chroma
    for _ in range(CHROMA_MAX_TRIES):
        best = None
        L = 0.02
        while L <= 0.99:
            hx = oklch_to_hex(L, c, hue)
            ratio = contrast_ratio(hx, bg_hex)
            ok = ratio < AA_LARGE_OR_UI if mode == "at-most" else ratio >= floor
            if ok and (best is None or better((L, hx, ratio), best)):
                best = (L, hx, ratio)
            L += SOLVE_L_STEP
        if best:
            return best
        c *= CHROMA_DECAY
    return None


def solve_palette(bg_hex, hue, chroma):
    """三档求解;无解的档位记入 missing(显性化,不静默降级)。"""
    roles = {"bg": bg_hex.lstrip("#").lower()}
    missing = []
    for role, floor, mode, objective in (
        ("text", AA_NORMAL, "at-least", "prefer"),
        ("ui", AA_LARGE_OR_UI, "at-least", "floor"),
        ("decorative", None, "at-most", None),
    ):
        got = solve_foreground(roles["bg"], hue, chroma, floor, mode, objective=objective)
        if got is None:
            missing.append(role)
        else:
            roles[role] = got[1]
    return roles, missing


def pairing_matrix(roles):
    """全配对矩阵:每对给对比度与档位分类,按对比度降序。"""
    names = [n for n in roles if roles[n]]
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = contrast_ratio(roles[a], roles[b])
            pairs.append((a, b, r, classify(r)))
    pairs.sort(key=lambda p: -p[2])
    return pairs


def format_report(roles, pairs, missing, hue, chroma):
    lines = []
    lines.append("# 求解配色 — bg=%s hue=%.1f chroma=%.3f" % (roles["bg"], hue, chroma))
    if missing:
        lines.append("!! 无解档位: %s(色相/彩度组合在该档无解;换 hue 或降 chroma)" % ", ".join(missing))
    for role in ("text", "ui", "decorative"):
        if roles.get(role):
            lines.append("  %-11s #%s" % (role, roles[role]))
    lines.append("")
    lines.append("== Contrast matrix (%d pairs) ==" % len(pairs))
    for a, b, r, cls in pairs:
        lines.append("  %-11s x %-11s %6.2f  %s" % (a, b, r, cls))
    lines.append("")
    lines.append("== Legal pairings (record these in the style lock) ==")
    text_safe = ", ".join("%s/%s" % (a, b) for a, b, r, c in pairs if r >= AA_NORMAL) or "none"
    ui_safe = ", ".join("%s/%s" % (a, b) for a, b, r, c in pairs if AA_LARGE_OR_UI <= r < AA_NORMAL) or "none"
    deco = ", ".join("%s/%s" % (a, b) for a, b, r, c in pairs if r < AA_LARGE_OR_UI) or "none"
    lines.append("  Text-safe   (>=4.5): %s" % text_safe)
    lines.append("  UI-safe     (>=3.0 and <4.5): %s" % ui_safe)
    lines.append("  Decorative  (<3.0;不得是传达状态的唯一手段): %s" % deco)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="OKLCH 亮度域配色求解 + 全配对矩阵(text≥4.5/UI≥3.0/decorative<3.0;无 MOODS)"
    )
    parser.add_argument("--bg", required=True, help="背景色 6 位 hex,如 0b0d12")
    parser.add_argument("--hue", type=float, required=True, help="前景色相(度,0-360)")
    parser.add_argument("--chroma", type=float, default=0.12, help="起始彩度(默认 0.12;无解时自动 0.85 降档)")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON(默认人类可读报告)")
    args = parser.parse_args(argv)

    bg = args.bg.lstrip("#").lower()
    if len(bg) != 6:
        print("palette-solver: --bg 必须是 6 位 hex,得到 %r" % args.bg, file=sys.stderr)
        return 2
    if not (0.0 <= args.hue <= 360.0) or not (0.0 <= args.chroma <= 0.4):
        print("palette-solver: --hue 须在 [0,360]、--chroma 须在 [0,0.4]", file=sys.stderr)
        return 2

    roles, missing = solve_palette(bg, args.hue, args.chroma)
    pairs = pairing_matrix(roles)

    if args.json:
        print(json.dumps({
            "bg": roles["bg"], "hue": args.hue, "chroma": args.chroma,
            "roles": {k: v for k, v in roles.items() if v},
            "missing_roles": missing,
            "matrix": [{"a": a, "b": b, "ratio": round(r, 2), "class": c} for a, b, r, c in pairs],
            "legal_pairings": {
                "text": ["%s/%s" % (a, b) for a, b, r, _ in pairs if r >= AA_NORMAL],
                "ui": ["%s/%s" % (a, b) for a, b, r, _ in pairs if AA_LARGE_OR_UI <= r < AA_NORMAL],
                "decorative": ["%s/%s" % (a, b) for a, b, r, _ in pairs if r < AA_LARGE_OR_UI],
            },
        }, ensure_ascii=False, indent=2))
    else:
        print(format_report(roles, pairs, missing, args.hue, args.chroma))

    # 有档位无解 = 看了有问题(显性化,不静默给一半结果)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
