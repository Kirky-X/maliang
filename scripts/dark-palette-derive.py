#!/usr/bin/env python3
"""暗色调色板确定性派生引擎。

从一套亮色调色板行(color-palettes.md 的 10 色列)确定性派生暗色模式行:
- 品牌色(Primary/Secondary/Accent/Destructive)原样保留,不换色相;
- 表面色(Background/Card/Muted/Border/Foreground)固定 slate 系,不从品牌色派生;
- Ring 按对暗底对比度 >= 3:1 自动选(品牌色组内择优,均不达标则逐步提亮 Primary);
- 已是暗色的行直接命中返回(passthrough),不重派生;
- 输出 _mode_derivation 溯源字段,记录每列的处理方式与 Ring 决策依据。

依赖: Python 3 标准库(无第三方依赖)。
来源: ui-ux-pro-max 思想中文自研, 2026-09 吸收。
用法(键不区分大小写,值必填):
    python3 dark-palette-derive.py Primary=#2563EB Background=#F8FAFC ...
"""

import json
import sys

# 调色板 10 色列,与 color-palettes.md 表头一致
COLUMNS = (
    "Primary", "Secondary", "Accent", "Background", "Foreground",
    "Card", "Muted", "Border", "Destructive", "Ring",
)

# 品牌色列(派生时原样保留)与表面色列(固定 slate 系)
BRAND_COLUMNS = ("Primary", "Secondary", "Accent", "Destructive")

# 表面色固定 slate 系(与 color-palettes.md 暗色行既有取值一致)
SLATE_SURFACES = {
    "Background": "#020617",  # slate-950
    "Card": "#0F172A",        # slate-900
    "Muted": "#1E293B",       # slate-800
    "Border": "#334155",      # slate-700
    "Foreground": "#F8FAFC",  # slate-50
}

# Ring 对暗底的非文本 UI 组件对比度阈值(WCAG 1.4.11)
RING_MIN_CONTRAST = 3.0

# 已是暗色的判定阈值:Background 相对亮度低于该值视为暗色行
DARK_LUMINANCE_THRESHOLD = 0.2

# Ring 提亮的白混步长(确定性:从 5% 起每步 +5%)
LIGHTEN_STEP = 0.05


# ---------------------------------------------------------------------------
# 基础色度计算(WCAG 相对亮度与对比度)
# ---------------------------------------------------------------------------

def hex_to_rgb(color):
    """'#RRGGBB' -> (r, g, b),非法输入抛 ValueError。"""
    text = color.strip().lstrip("#")
    if len(text) != 6:
        raise ValueError(f"非法 hex 颜色: {color!r}(需要 #RRGGBB)")
    try:
        return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"非法 hex 颜色: {color!r}")


def relative_luminance(color):
    """WCAG 相对亮度: L = 0.2126R + 0.7152G + 0.0722B(gamma 校正后)。"""
    ratios = []
    for value in hex_to_rgb(color):
        c = value / 255.0
        c = c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        ratios.append(c)
    return 0.2126 * ratios[0] + 0.7152 * ratios[1] + 0.0722 * ratios[2]


def contrast_ratio(color_a, color_b):
    """两色的 WCAG 对比度,恒 >= 1。"""
    la, lb = relative_luminance(color_a), relative_luminance(color_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def is_dark(color):
    """暗色判定:相对亮度低于 DARK_LUMINANCE_THRESHOLD。"""
    return relative_luminance(color) < DARK_LUMINANCE_THRESHOLD


def _mix_toward_white(color, ratio):
    """把颜色向白色按比例混合(0=原色,1=纯白),返回 hex。"""
    mixed = tuple(round(c + (255 - c) * ratio) for c in hex_to_rgb(color))
    return "#%02X%02X%02X" % mixed


# ---------------------------------------------------------------------------
# 派生引擎
# ---------------------------------------------------------------------------

def validate_row(row):
    """校验行数据:10 列齐全且均为合法 hex,缺失/非法抛 ValueError。"""
    missing = [name for name in COLUMNS if not row.get(name)]
    if missing:
        raise ValueError(f"调色板行缺列: {', '.join(missing)}")
    for name in COLUMNS:
        hex_to_rgb(row[name])


def _pick_ring(row, dark_bg):
    """从品牌色组按优先序选对暗底 >=3:1 的 Ring;均不达标则确定性提亮 Primary。

    返回 (ring_hex, 溯源说明)。
    """
    candidates = [row[name] for name in ("Primary", "Accent", "Secondary", "Destructive")]
    seen = []
    for color in candidates:
        if color in seen:
            continue
        seen.append(color)
        ratio = contrast_ratio(color, dark_bg)
        if ratio >= RING_MIN_CONTRAST:
            return color, f"kept(对比 {ratio:.2f}:1)"
    base = row["Primary"]
    steps = int(round(1.0 / LIGHTEN_STEP))
    for i in range(1, steps + 1):
        candidate = _mix_toward_white(base, i * LIGHTEN_STEP)
        if contrast_ratio(candidate, dark_bg) >= RING_MIN_CONTRAST:
            return candidate, f"elevated:Primary+白混{round(i * LIGHTEN_STEP * 100)}%"
    raise ValueError("Ring 提亮至纯白仍不达标,暗底色值异常")  # 理论不可达,显性失败


def derive_dark_palette(row):
    """从一套调色板行派生暗色模式行,返回含 _mode_derivation 的新 dict。

    已是暗色(Background 相对亮度 < 阈值)的行直接命中返回原值,不重派生。
    """
    validate_row(row)
    result = dict(row)
    bg_lum = relative_luminance(row["Background"])

    if is_dark(row["Background"]):
        result["_mode_derivation"] = {
            "mode": "passthrough",
            "background_luminance": round(bg_lum, 4),
            "note": "已是暗色行,直接命中不重派生",
        }
        return result

    dark_bg = SLATE_SURFACES["Background"]
    ring, ring_note = _pick_ring(row, dark_bg)
    derivation = {
        "mode": "derived",
        "background_luminance": round(bg_lum, 4),
        "columns": {name: "kept(品牌色)" for name in BRAND_COLUMNS},
    }
    for name, hex_value in SLATE_SURFACES.items():
        result[name] = hex_value
        derivation["columns"][name] = f"slate-fixed:{hex_value}"
    result["Ring"] = ring
    derivation["columns"]["Ring"] = ring_note
    result["_mode_derivation"] = derivation
    return result


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def _parse_args(argv):
    row = {}
    for arg in argv:
        if "=" not in arg:
            raise ValueError(f"参数格式应为 列名=hex: {arg!r}")
        key, value = arg.split("=", 1)
        row[key.strip().capitalize()] = value.strip()
    return row


def main(argv):
    try:
        row = _parse_args(argv)
        print(json.dumps(derive_dark_palette(row), ensure_ascii=False, indent=2))
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
