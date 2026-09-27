"""dark-palette-derive.py 单元测试(暗色调色板确定性派生引擎)。"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

dpd = load("dark-palette-derive.py")

import unittest  # noqa: E402

# color-palettes.md No.1 SaaS (General):典型亮色行
LIGHT_ROW = {
    "Primary": "#2563EB",
    "Secondary": "#3B82F6",
    "Accent": "#EA580C",
    "Background": "#F8FAFC",
    "Foreground": "#1E293B",
    "Card": "#FFFFFF",
    "Muted": "#E9EFF8",
    "Border": "#E2E8F0",
    "Destructive": "#DC2626",
    "Ring": "#2563EB",
}

# color-palettes.md No.6 Financial Dashboard:已是暗色行
DARK_ROW = {
    "Primary": "#0F172A",
    "Secondary": "#1E293B",
    "Accent": "#22C55E",
    "Background": "#020617",
    "Foreground": "#F8FAFC",
    "Card": "#0E1223",
    "Muted": "#1A1E2F",
    "Border": "#334155",
    "Destructive": "#EF4444",
    "Ring": "#0F172A",
}


class TestColorMath(unittest.TestCase):
    def test_white_vs_black_contrast_21(self):
        self.assertAlmostEqual(dpd.contrast_ratio("#FFFFFF", "#000000"), 21.0, places=1)

    def test_same_color_contrast_1(self):
        self.assertAlmostEqual(dpd.contrast_ratio("#2563EB", "#2563EB"), 1.0)

    def test_hex_to_rgb_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            dpd.hex_to_rgb("#12345")
        with self.assertRaises(ValueError):
            dpd.hex_to_rgb("nothex")


class TestDeriveDarkPalette(unittest.TestCase):
    def test_dark_row_passthrough_untouched(self):
        out = dpd.derive_dark_palette(DARK_ROW)
        self.assertEqual(out["_mode_derivation"]["mode"], "passthrough")
        for name in dpd.COLUMNS:
            self.assertEqual(out[name], DARK_ROW[name])

    def test_light_row_marks_derived(self):
        out = dpd.derive_dark_palette(LIGHT_ROW)
        self.assertEqual(out["_mode_derivation"]["mode"], "derived")

    def test_brand_colors_kept(self):
        out = dpd.derive_dark_palette(LIGHT_ROW)
        for name in dpd.BRAND_COLUMNS:
            self.assertEqual(out[name], LIGHT_ROW[name], f"{name} 应保留品牌色")

    def test_surfaces_fixed_slate(self):
        out = dpd.derive_dark_palette(LIGHT_ROW)
        for name, hex_value in dpd.SLATE_SURFACES.items():
            self.assertEqual(out[name], hex_value, f"{name} 应固定 slate 值")

    def test_ring_meets_contrast_on_dark_bg(self):
        out = dpd.derive_dark_palette(LIGHT_ROW)
        ratio = dpd.contrast_ratio(out["Ring"], dpd.SLATE_SURFACES["Background"])
        self.assertGreaterEqual(ratio, dpd.RING_MIN_CONTRAST)

    def test_ring_prefers_brand_color_when_qualifying(self):
        # Primary #2563EB 对 slate-950 对比度达标时,Ring 应直接取 Primary
        out = dpd.derive_dark_palette(LIGHT_ROW)
        if dpd.contrast_ratio(LIGHT_ROW["Primary"], dpd.SLATE_SURFACES["Background"]) >= dpd.RING_MIN_CONTRAST:
            self.assertEqual(out["Ring"], LIGHT_ROW["Primary"])
            note = out["_mode_derivation"]["columns"]["Ring"]
            self.assertTrue(note.startswith("kept"))

    def test_ring_elevated_when_primary_too_dark(self):
        # 品牌色全组为暗色系(对暗底均 <3:1)时,Ring 必须提亮且仍 >=3:1
        row = dict(LIGHT_ROW,
                   Primary="#1C1917", Secondary="#292524",
                   Accent="#44403C", Destructive="#7F1D1D", Ring="#1C1917")
        out = dpd.derive_dark_palette(row)
        self.assertNotEqual(out["Ring"], "#1C1917")
        ratio = dpd.contrast_ratio(out["Ring"], dpd.SLATE_SURFACES["Background"])
        self.assertGreaterEqual(ratio, dpd.RING_MIN_CONTRAST)
        self.assertTrue(out["_mode_derivation"]["columns"]["Ring"].startswith("elevated"))

    def test_derivation_trail_records_columns(self):
        out = dpd.derive_dark_palette(LIGHT_ROW)
        columns = out["_mode_derivation"]["columns"]
        self.assertIn("Background", columns)
        self.assertIn("Ring", columns)
        self.assertEqual(columns["Primary"], "kept(品牌色)")

    def test_missing_column_raises(self):
        row = dict(LIGHT_ROW)
        del row["Border"]
        with self.assertRaises(ValueError):
            dpd.derive_dark_palette(row)

    def test_foreground_passes_aa_on_derived_bg(self):
        # 派生行自身也必须过对比度:正文白对 slate-950 远超 4.5:1
        out = dpd.derive_dark_palette(LIGHT_ROW)
        ratio = dpd.contrast_ratio(out["Foreground"], out["Background"])
        self.assertGreaterEqual(ratio, 4.5)


class TestCli(unittest.TestCase):
    def test_parse_args_case_insensitive_keys(self):
        row = dpd._parse_args(["primary=#2563EB", "BACKGROUND=#F8FAFC"])
        self.assertEqual(row["Primary"], "#2563EB")
        self.assertEqual(row["Background"], "#F8FAFC")

    def test_main_rejects_bad_arg_format(self):
        self.assertEqual(dpd.main(["not-a-kv"]), 1)

    def test_main_emits_json_with_trail(self):
        import contextlib
        import io
        import json
        argv = [f"{k}={v}" for k, v in LIGHT_ROW.items()]
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = dpd.main(argv)
        self.assertEqual(code, 0)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["_mode_derivation"]["mode"], "derived")


if __name__ == "__main__":
    unittest.main()
