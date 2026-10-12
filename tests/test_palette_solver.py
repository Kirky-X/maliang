"""palette-solver.py(#33,无 MOODS)的单元测试:三档求解 + 矩阵契约。"""

import contextlib
import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

ps = load("palette-solver.py")


class TestSolve(unittest.TestCase):
    def test_three_roles_meet_floors(self):
        roles, missing = ps.solve_palette("0b0d12", hue=150, chroma=0.12)
        self.assertEqual(missing, [])
        self.assertGreaterEqual(ps.contrast_ratio(roles["text"], roles["bg"]), 4.5)
        self.assertGreaterEqual(ps.contrast_ratio(roles["ui"], roles["bg"]), 3.0)
        self.assertLess(ps.contrast_ratio(roles["decorative"], roles["bg"]), 3.0)
        # 三档互不撞色(近底微差色 ≠ UI 档)
        self.assertNotEqual(roles["decorative"], roles["ui"])
        self.assertNotEqual(roles["ui"], roles["text"])

    def test_light_bg_solves_dark_foreground(self):
        roles, missing = ps.solve_palette("fbfbfe", hue=220, chroma=0.10)
        self.assertEqual(missing, [])
        self.assertGreaterEqual(ps.contrast_ratio(roles["text"], roles["bg"]), 4.5)

    def test_unreachable_floor_returns_none(self):
        # 显性无解:floor 15 不可达 → None(不得静默给不达标色)
        self.assertIsNone(ps.solve_foreground("808080", hue=30, chroma=0.15,
                                              floor=15.0, mode="at-least"))

    def test_matrix_covers_all_pairs(self):
        roles, missing = ps.solve_palette("0b0d12", hue=150, chroma=0.12)
        pairs = ps.pairing_matrix(roles)
        self.assertEqual(len(pairs), 6)  # 4 色 C(4,2)
        for a, b, ratio, cls in pairs:
            self.assertGreater(ratio, 1.0)
            self.assertIn(cls, ("text-safe (>=4.5)", "UI-safe (>=3.0)", "decorative (<3.0)"))

    def test_no_moods_table(self):
        # 裁决 6:砍 MOODS——模块不得再有关键词查表
        self.assertFalse(any(k.lower() == "moods" for k in dir(ps)))


class TestCli(unittest.TestCase):
    def test_text_report_has_legal_pairings(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ps.main(["--bg", "0b0d12", "--hue", "150", "--chroma", "0.12"])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("Contrast matrix", out)
        self.assertIn("Legal pairings (record these in the style lock)", out)
        self.assertIn("Text-safe", out)

    def test_json_shape(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ps.main(["--bg", "0b0d12", "--hue", "150", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(set(payload["roles"]) - {"bg"}, {"text", "ui", "decorative"})
        self.assertEqual(len(payload["matrix"]), 6)
        self.assertIn("text", payload["legal_pairings"])

    def test_bad_bg_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = ps.main(["--bg", "xyz", "--hue", "150"])
        self.assertEqual(code, 2)

    def test_bad_hue_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = ps.main(["--bg", "0b0d12", "--hue", "999"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
