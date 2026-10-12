"""测试共用:纯标准库 PNG 编码器(供测色/保真测试在内存构造图像)。

用法:
    from _png import png_bytes, write_png
    data = png_bytes(100, 100, lambda x, y: (255, 255, 255))
"""

import os
import struct
import zlib


def png_bytes(width, height, pixel_at, color_type=2):
    """生成 PNG 字节流。pixel_at(x, y) -> (r, g, b) 或 (r, g, b, a)(color_type=6)。"""
    channels = 3 if color_type == 2 else 4
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # 滤波类型 0(None)
        for x in range(width):
            raw.extend(pixel_at(x, y)[:channels])

    def chunk(ctype, data):
        return (struct.pack(">I", len(data)) + ctype + data
                + struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw))) + chunk(b"IEND", b""))


def write_png(path, width, height, pixel_at, color_type=2):
    with open(path, "wb") as fh:
        fh.write(png_bytes(width, height, pixel_at, color_type))
    return path


FIXTURE_DIR = os.path.dirname(os.path.abspath(__file__))
