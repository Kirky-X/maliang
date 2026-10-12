#!/usr/bin/env python3
"""确定性测色脚本(G23):图片 -> k-means -> ΔE 合并 -> 角色分配 -> stdout JSON。

目测取色会向熟悉的调色板默认漂移(漂移可达 ΔE10+),测量的意义是把
「这些颜色是什么」变成可复核的数字。管线(移植自 design-dna
scripts/measure-colors.mjs,#23,2026-10 吸收;PNG 解码为本仓纯标准库实现):

  1. 解码图片为 RGB 像素;
  2. 分层哈希采样 ≤160k 像素(deterministic_stratified:等分象限 + 固定哈希
     取样点,避免固定相位对周期性细节的混叠删除);
  3. k-means(k 个簇,最远点初始化:小而独立的色块也能分到自己的簇);
  4. CIE ΔE 合并近似簇(PNG ΔE≤2.5 / JPEG 压缩噪声更宽 ΔE≤5);
  5. 角色启发式:最大覆盖=background;与背景明度差 ≥0.25 且覆盖 ≥0.5% 中
     明度差最大者=text;accent 按 饱和度×ΔE×√(min(覆盖,2%)/2%) 打分取最高
     (饱和度 ≥0.25、覆盖 ≥0.2%、明度 0.08-0.92 内)。

格式支持与降级(未测量不得记为通过):
  PNG  纯 Python 标准库解码(8-bit,非隔行,灰度/RGB/RGBA/调色板);
  JPEG 需 Pillow;Pillow 缺失时该文件报 UNMEASURED → 退出码 2(--help 同步注明);
  其余格式(WebP/GIF...)或不受支持的 PNG 变体 → UNMEASURED → 2。

用法:
    python3 scripts/measure-colors.py <image.png> [--k 8] [--json|--text]

输出(stdout,默认 JSON):
    {"source": {file, width, height},
     "measurement": {k, sampling:{method, max_pixels, sampled_pixels}},
     "palette": [{hex, coverage, role}...], "measured": true}

退出码: 见 scripts/EXIT-CODES.md(0=测到了 / 1=不使用 / 2=没能检查/UNMEASURED;#16)。
依赖: Python 3 标准库;JPEG 可选 Pillow。
来源: design-dna #23,2026-10 吸收。
"""

import argparse
import json
import math
import os
import struct
import sys
import zlib

MAX_SAMPLED_PIXELS = 160_000
KMEANS_ITERS = 24
DEFAULT_K = 8

# 角色启发式阈值(外部原口径)
TEXT_MIN_L_DIFF = 0.25
TEXT_MIN_COVERAGE = 0.005
ACCENT_MIN_SAT = 0.25
ACCENT_MIN_COVERAGE = 0.002
ACCENT_L_RANGE = (0.08, 0.92)
ACCENT_COVERAGE_CAP = 0.02

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


# ---------------------------------------------------------------------------
# PNG 解码(纯标准库):8-bit,非隔行,色型 0/2/3/6
# ---------------------------------------------------------------------------

def decode_png(data):
    """解码 PNG 为 (width, height, [(r,g,b)...]);不支持返回 (_UNSUPPORTED, 原因)。"""
    if not data.startswith(_PNG_SIGNATURE):
        return None, "不是 PNG 文件"
    pos = 8
    width = height = None
    color_type = bit_depth = interlace = None
    palette = []
    idat = bytearray()
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        pos += 8
        chunk = data[pos:pos + length]
        if len(chunk) != length:
            return None, "PNG chunk 截断(损坏的文件)"
        pos += length + 4  # 跳过 CRC
        if ctype == b"IHDR":
            try:
                width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                    ">IIBBBBB", chunk
                )
            except struct.error:
                return None, "PNG 结构损坏(IHDR)"
        elif ctype == b"PLTE":
            if len(chunk) % 3 != 0:
                return None, "PLTE 长度非 3 的倍数(损坏的文件)"
            palette = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        elif ctype == b"IDAT":
            idat.extend(chunk)
        elif ctype == b"IEND":
            break
    if width is None:
        return None, "PNG 缺 IHDR"
    if bit_depth != 8:
        return None, "bit depth %d 不支持(仅 8-bit)" % bit_depth
    if interlace != 0:
        return None, "隔行 PNG 不支持"
    channels = {0: 1, 2: 3, 3: 1, 6: 4}.get(color_type)
    if channels is None:
        return None, "色型 %d 不支持(仅 0/2/3/6)" % color_type
    if color_type == 3 and not palette:
        return None, "调色板 PNG 缺 PLTE"

    # 解压炸弹防线:像素总量硬上限,解压输出限长(超出即拒,UNMEASURED/exit 2)
    if width * height > 80_000_000:
        return None, "图像尺寸超限(width*height > 80M 像素)"

    stride = width * channels
    expected = (stride + 1) * height
    try:
        d = zlib.decompressobj()
        raw = d.decompress(bytes(idat), expected + 1_048_576)
    except zlib.error as exc:
        return None, "IDAT 解压失败: %s" % exc
    if len(raw) < expected:
        return None, "像素数据不足(损坏的 PNG)"
    if d.unconsumed_tail:
        return None, "解压输出超过预期上限(疑似解压炸弹)"

    # 逐行 unfilter(五种滤波,见 PNG 规范)
    bpp = channels
    out = bytearray()
    prev = bytearray(stride)
    ptr = 0
    for _ in range(height):
        ftype = raw[ptr]
        ptr += 1
        line = bytearray(raw[ptr:ptr + stride])
        ptr += stride
        if ftype == 1:  # Sub
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ftype == 2:  # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:  # Average
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:  # Paeth
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        elif ftype != 0:
            return None, "未知滤波类型 %d" % ftype
        out.extend(line)
        prev = line

    # 折叠到 RGB
    pixels = []
    if color_type == 2:
        for i in range(0, len(out), 3):
            pixels.append((out[i], out[i + 1], out[i + 2]))
    elif color_type == 6:
        for i in range(0, len(out), 4):
            # alpha 合成到白底(外部 sharp flatten 同口径)
            a = out[i + 3] / 255
            pixels.append(tuple(
                round(out[i + k] * a + 255 * (1 - a)) for k in range(3)
            ))
    elif color_type == 0:
        for v in out:
            pixels.append((v, v, v))
    else:  # 调色板
        for idx in out:
            if idx >= len(palette):
                return None, "调色板索引越界"
            pixels.append(palette[idx])
    return (width, height, pixels), None


def decode_jpeg(data):
    """JPEG 走 Pillow;缺失时返回 UNMEASURED(调用方退出 2)。"""
    try:
        import io
        from PIL import Image  # type: ignore
    except ImportError:
        return None, "JPEG 需要 Pillow(未安装);PNG 全程标准库。UNMEASURED"
    try:
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGB")
    except Exception as exc:
        return None, "JPEG 解码失败: %s" % exc
    return (img.width, img.height, list(img.getdata())), None


def load_image(path):
    """按扩展名解码;返回 (width, height, pixels, is_jpeg) 或抛 UnmeasurableError。"""
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        raise UnmeasurableError("读取失败: %s" % exc)
    is_jpeg = ext in (".jpg", ".jpeg")
    if is_jpeg:
        size, err = decode_jpeg(data)
    elif ext == ".png":
        size, err = decode_png(data)
    else:
        size, err = None, "不支持的格式 %s(仅 PNG;JPEG 需 Pillow)" % ext
    if err:
        raise UnmeasurableError(err)
    return size[0], size[1], size[2], is_jpeg


class UnmeasurableError(Exception):
    """没能检查(UNMEASURED):格式不支持/解码失败/依赖缺失。"""


# ---------------------------------------------------------------------------
# 采样 / k-means / ΔE 合并 / 角色分配(移植自外部 measure-colors.mjs)
# ---------------------------------------------------------------------------

def _mix32(value):
    x = (value + 0x9E3779B9) & 0xFFFFFFFF
    x = ((x ^ (x >> 16)) * 0x21F0AAAD) & 0xFFFFFFFF
    x = ((x ^ (x >> 15)) * 0x735A2D97) & 0xFFFFFFFF
    return (x ^ (x >> 15)) & 0xFFFFFFFF


def stratified_sample(pixels, sample_count):
    """分层哈希采样:等分象限 + 固定哈希取样点,破除固定相位混叠。"""
    total = len(pixels)
    if total <= sample_count:
        return list(pixels)
    out = []
    for s in range(sample_count):
        start = (s * total) // sample_count
        end = ((s + 1) * total) // sample_count
        idx = start + (_mix32(s) % max(1, end - start))
        out.append(pixels[idx])
    return out


def kmeans(pixels, k, iters=KMEANS_ITERS):
    """最远点初始化的 k-means;返回 [{center, share}](按覆盖降序)。"""
    # 最远点初始化:从最暗像素起步,反复加入离现有中心最远的像素
    centers = [list(min(pixels, key=lambda p: p[0] * 3 + p[1] * 6 + p[2]))]
    nearest = [float("inf")] * len(pixels)
    while len(centers) < k:
        last = centers[-1]
        far, fd = 0, -1.0
        for i, p in enumerate(pixels):
            d = (p[0] - last[0]) ** 2 + (p[1] - last[1]) ** 2 + (p[2] - last[2]) ** 2
            if d < nearest[i]:
                nearest[i] = d
            if nearest[i] > fd:
                fd, far = nearest[i], i
        if fd <= 0:
            break  # 不同色少于 k
        centers.append(list(pixels[far]))
    k = len(centers)
    assign = [0] * len(pixels)
    for _ in range(iters):
        moved = False
        for i, p in enumerate(pixels):
            best, bd = 0, float("inf")
            for c in range(k):
                ctr = centers[c]
                d = (p[0] - ctr[0]) ** 2 + (p[1] - ctr[1]) ** 2 + (p[2] - ctr[2]) ** 2
                if d < bd:
                    bd, best = d, c
            if assign[i] != best:
                assign[i] = best
                moved = True
        sums = [[0, 0, 0, 0] for _ in range(k)]
        for i, a in enumerate(assign):
            s = sums[a]
            s[0] += pixels[i][0]
            s[1] += pixels[i][1]
            s[2] += pixels[i][2]
            s[3] += 1
        for c in range(k):
            if sums[c][3] > 0:
                centers[c] = [sums[c][j] / sums[c][3] for j in range(3)]
        if not moved:
            break
    counts = [0] * k
    for a in assign:
        counts[a] += 1
    clusters = [
        {"center": centers[c], "share": counts[c] / len(pixels)}
        for c in range(k) if counts[c] > 0
    ]
    clusters.sort(key=lambda c: -c["share"])
    return clusters


def srgb_to_lab(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = f(rgb[0]), f(rgb[1]), f(rgb[2])
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

    def t(v):
        return v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116

    x, y, z = t(x), t(y), t(z)
    return [116 * y - 16, 500 * (x - y), 200 * (y - z)]


def delta_e(a, b):
    """CIE76 ΔE(外部 color-math.mjs 同口径)。"""
    la, lb = srgb_to_lab(a), srgb_to_lab(b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(la, lb)))


def merge_similar(clusters, max_de):
    """合并感知等价的簇(抗锯齿/JPEG 噪声);按覆盖降序。"""
    merged = []
    for c in clusters:
        near = None
        for m in merged:
            if delta_e(m["center"], c["center"]) <= max_de:
                near = m
                break
        if near is not None:
            total = near["share"] + c["share"]
            near["center"] = [
                (near["center"][i] * near["share"] + c["center"][i] * c["share"]) / total
                for i in range(3)
            ]
            near["share"] = total
        else:
            merged.append({"center": list(c["center"]), "share": c["share"]})
    merged.sort(key=lambda c: -c["share"])
    return merged


def hsv(rgb):
    """(色相°, HSV 饱和度, HSL 明度)。accent 判定用 HSV 饱和度(近白不爆表)。"""
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    s = 0 if mx == 0 else d / mx
    l = (mx + mn) / 2
    h = 0.0
    if d != 0:
        if mx == r:
            h = 60 * (((g - b) / d) % 6)
        elif mx == g:
            h = 60 * ((b - r) / d + 2)
        else:
            h = 60 * ((r - g) / d + 4)
    return (h + 360) % 360, s, l


def assign_roles(clusters):
    """角色启发式:background / text / accent,其余 unassigned。"""
    entries = []
    for c in clusters:
        h, s, l = hsv(c["center"])
        entries.append({"center": c["center"], "share": c["share"],
                        "h": h, "s": s, "l": l, "role": "unassigned"})
    if not entries:
        return entries
    taken = set()
    # 背景 = 最大覆盖
    entries[0]["role"] = "background"
    taken.add(0)
    bg_l = entries[0]["l"]
    # 文本 = 与背景明度差最大且覆盖达标者
    text_i, best_c = -1, 0.0
    for i, e in enumerate(entries):
        if i in taken:
            continue
        c = abs(e["l"] - bg_l)
        if e["share"] >= TEXT_MIN_COVERAGE and c > best_c:
            best_c, text_i = c, i
    if text_i >= 0 and best_c > TEXT_MIN_L_DIFF:
        entries[text_i]["role"] = "text"
        taken.add(text_i)
    # accent = 饱和度 × ΔE(对背景) × 覆盖折扣打分;覆盖到 2% 后不再加分——
    # 大面积浅色表面不得压过小而亮的 CTA
    accents = []
    for i, e in enumerate(entries):
        if i in taken:
            continue
        if not (e["s"] >= ACCENT_MIN_SAT and e["share"] >= ACCENT_MIN_COVERAGE
                and ACCENT_L_RANGE[0] <= e["l"] <= ACCENT_L_RANGE[1]):
            continue
        score = (e["s"] * delta_e(e["center"], entries[0]["center"])
                 * math.sqrt(min(e["share"], ACCENT_COVERAGE_CAP) / ACCENT_COVERAGE_CAP))
        accents.append((score, i))
    if accents:
        accents.sort(key=lambda p: -p[0])
        entries[accents[0][1]]["role"] = "accent"
        taken.add(accents[0][1])
    return entries


def measure_image(path, k=DEFAULT_K):
    """测量单图,返回输出 JSON dict。UNMEASURED 抛 UnmeasurableError。"""
    width, height, pixels, is_jpeg = load_image(path)
    if width <= 0 or height <= 0 or not pixels:
        raise UnmeasurableError("图像为空")
    k = max(2, min(16, int(k)))
    sampled = stratified_sample(pixels, MAX_SAMPLED_PIXELS)
    # JPEG 压缩把平坦色摊成更宽的噪声带,合并阈值放档(外部同口径)
    clusters = merge_similar(kmeans(sampled, k), 5.0 if is_jpeg else 2.5)
    palette = [
        {"hex": "#%02x%02x%02x" % tuple(round(v) for v in e["center"]),
         "coverage": round(e["share"], 4), "role": e["role"]}
        for e in assign_roles(clusters)
    ]
    return {
        "source": {"file": os.path.basename(path), "width": width, "height": height},
        "measurement": {
            "k": k,
            "sampling": {
                "method": "deterministic_stratified",
                "max_pixels": MAX_SAMPLED_PIXELS,
                "sampled_pixels": len(sampled),
            },
        },
        "palette": palette,
        "measured": True,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="确定性测色(PNG 纯标准库;JPEG 需 Pillow,缺失报 UNMEASURED/exit 2)"
    )
    parser.add_argument("image", help="待测图片(.png;.jpg/.jpeg 需 Pillow)")
    parser.add_argument("--k", type=int, default=DEFAULT_K, help="簇数 2-16(默认 8;verify 复测必须同 k)")
    parser.add_argument("--json", action="store_true", default=True,
                        help="输出 JSON(默认即为 JSON;保留开关与外部 CLI 兼容)")
    parser.add_argument("--text", dest="json", action="store_false", help="输出人类可读汇总")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.image):
        print("measure-colors: 文件不存在: %s" % args.image, file=sys.stderr)
        return 2
    try:
        result = measure_image(args.image, args.k)
    except UnmeasurableError as exc:
        print(json.dumps({"source": {"file": os.path.basename(args.image)},
                          "measured": False, "unmeasured_reason": str(exc)},
                         ensure_ascii=False))
        print("measure-colors: UNMEASURED —— %s" % exc, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("%s (%dx%d, k=%d, 采样 %d 像素)" % (
            result["source"]["file"], result["source"]["width"],
            result["source"]["height"], result["measurement"]["k"],
            result["measurement"]["sampling"]["sampled_pixels"]))
        for p in result["palette"]:
            print("  %-11s #%s  覆盖 %5.1f%%  角色 %s" % (
                p["hex"], p["hex"], p["coverage"] * 100, p["role"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
