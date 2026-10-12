"""measure-colors.py(#23)的单元测试:PNG 解码 / k-means / 角色分配 / UNMEASURED。"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402
from _png import write_png

mc = load("measure-colors.py")

try:
    import PIL  # type: ignore
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class TestPngDecode(unittest.TestCase):
    def test_rgb_solid(self):
        from _png import png_bytes
        size, err = mc.decode_png(png_bytes(4, 4, lambda x, y: (10, 20, 30)))
        self.assertIsNone(err)
        self.assertEqual(size[0], 4)
        self.assertEqual(size[2], [(10, 20, 30)] * 16)

    def test_alpha_composited_on_white(self):
        from _png import png_bytes
        size, err = mc.decode_png(png_bytes(2, 1, lambda x, y: (0, 0, 0, 0), color_type=6))
        self.assertIsNone(err)
        self.assertEqual(set(size[2]), {(255, 255, 255)})

    def test_grayscale(self):
        from _png import png_bytes
        raw = bytearray()
        for _ in range(3):
            raw.append(0)
            raw.extend(bytes([128] * 3))
        import struct, zlib
        def chunk(ctype, payload):
            return (struct.pack(">I", len(payload)) + ctype + payload
                    + struct.pack(">I", zlib.crc32(ctype + payload) & 0xFFFFFFFF))
        data = (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", 3, 3, 8, 0, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(bytes(raw))) + chunk(b"IEND", b""))
        size, err = mc.decode_png(data)
        self.assertIsNone(err)
        self.assertEqual(set(size[2]), {(128, 128, 128)})

    def test_unsupported_bit_depth(self):
        import struct, zlib
        def chunk(ctype, payload):
            return (struct.pack(">I", len(payload)) + ctype + payload
                    + struct.pack(">I", zlib.crc32(ctype + payload) & 0xFFFFFFFF))
        data = (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 2, 16, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(b"\x00" * 16)) + chunk(b"IEND", b""))
        size, err = mc.decode_png(data)
        self.assertIsNone(size)
        self.assertIn("bit depth", err)


class TestMeasure(unittest.TestCase):
    def _measure(self, tmp, name, pixel_at, **kw):
        path = write_png(os.path.join(tmp, name), *kw.pop("size", (40, 40)), pixel_at=pixel_at)
        return mc.measure_image(path, **kw)

    def test_solid_color_role_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._measure(tmp, "solid.png", lambda x, y: (59, 130, 246))
        self.assertTrue(result["measured"])
        self.assertEqual(len(result["palette"]), 1)
        entry = result["palette"][0]
        self.assertEqual(entry["hex"], "#3b82f6")
        self.assertEqual(entry["coverage"], 1.0)
        self.assertEqual(entry["role"], "background")
        self.assertLessEqual(result["measurement"]["sampling"]["sampled_pixels"], 160_000)

    def test_two_color_stripes_both_kept(self):
        # 分层采样防周期混叠:红蓝 1px 交替条纹两色都必须在簇里
        def stripes(x, y):
            return (255, 0, 0) if x % 2 == 0 else (0, 0, 255)
        with tempfile.TemporaryDirectory() as tmp:
            result = self._measure(tmp, "stripes.png", stripes, size=(200, 100))
        by_hex = {p["hex"]: p["coverage"] for p in result["palette"]}
        self.assertIn("#ff0000", by_hex)
        self.assertIn("#0000ff", by_hex)
        self.assertGreater(by_hex["#ff0000"], 0.45)
        self.assertLess(by_hex["#ff0000"], 0.55)

    def test_accent_favors_separation_over_area(self):
        # 深底 + 小亮青块:accent 必须是亮青,不是大面积深表面(外部对照实验同款)
        def pixel(x, y):
            i = y * 100 + x
            if i < 250:
                return (243, 246, 254)
            if i < 500:
                return (110, 231, 255)
            if i < 1300:
                return (27, 37, 63)
            return (15, 21, 38)
        with tempfile.TemporaryDirectory() as tmp:
            result = self._measure(tmp, "dash.png", pixel, size=(100, 100))
        roles = {p["role"]: p["hex"] for p in result["palette"] if p["role"] != "unassigned"}
        self.assertEqual(roles.get("text"), "#f3f6fe")
        self.assertEqual(roles.get("accent"), "#6ee7ff")

    def test_k_clamped(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._measure(tmp, "solid.png", lambda x, y: (1, 2, 3), k=99)
        self.assertEqual(result["measurement"]["k"], 16)


class TestUnmeasured(unittest.TestCase):
    def test_unsupported_format_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "pic.webp")
            open(path, "wb").write(b"RIFFxxxxWEBP")
            buf, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
                code = mc.main([path])
            self.assertEqual(code, 2)
            payload = json.loads(buf.getvalue())
            self.assertFalse(payload["measured"])
            self.assertIn("UNMEASURED", err.getvalue())

    def test_missing_file_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = mc.main([os.path.join("no", "such.png")])
        self.assertEqual(code, 2)

    @unittest.skipIf(HAS_PIL, "Pillow 在场:JPEG 可测,UNMEASURED 降级路径不触发")
    def test_jpeg_without_pillow_is_unmeasured(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "pic.jpg")
            open(path, "wb").write(b"\xff\xd8\xff\xe0fake")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = mc.main([path])
            self.assertEqual(code, 2)
            self.assertIn("Pillow", err.getvalue())

    @unittest.skipUnless(HAS_PIL, "需要 Pillow 才能验证 JPEG 正通道")
    def test_jpeg_with_pillow_measures(self):
        import io as _io
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "pic.jpg")
            Image.new("RGB", (20, 20), (200, 60, 60)).save(path)
            result = mc.measure_image(path)
        self.assertTrue(result["measured"])


if __name__ == "__main__":
    unittest.main()
