"""check-structure-history.py(G41/G42)的单元测试 + fixture 冒烟。

七轴键集与 build-log 契约见 references/templates/variation-engine.md;
测试同时锁:immediate repeat / hot axis(0.6) / stamp lies / 日志缺失 UNMEASURED。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

csh = load("check-structure-history.py")

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "build-log")

AXES_A = {
    "theme": "Deep Dark Mode", "background": "tactile textured surface feel",
    "typography": "editorial serif + sans", "hero": "massive image-first hero",
    "section": "gallery-led cadence", "signature": "pristine gapless bento grid",
    "motion": "pinned narrative section",
}
AXES_B = {
    "theme": "Pristine Light Mode", "background": "subtle technical grid",
    "typography": "clean grotesk", "hero": "asymmetric split hero",
    "section": "Swiss grid discipline", "signature": "off-grid editorial layout",
    "motion": "staggered float-up",
}


def _entry(page, axes):
    return {"date": "2026-10-01", "page": page, "mode": "Experience",
            "axes": axes, "dials": {}, "brief": ""}


class TestImmediateRepeat(unittest.TestCase):
    def test_same_axis_value_reports(self):
        problems = csh.check_immediate_repeat(AXES_A, dict(AXES_A))
        self.assertEqual(len(problems), 7)
        self.assertIn("reuse is only OK", problems[0])

    def test_rotated_axes_pass(self):
        self.assertEqual(csh.check_immediate_repeat(AXES_B, AXES_A), [])


class TestHotAxis(unittest.TestCase):
    def test_hot_axis_reports_at_threshold(self):
        window = [_entry("p%d" % i, AXES_A) for i in range(3)]
        problems = csh.check_hot_axis(AXES_A, window, len(window))
        self.assertEqual(len(problems), 7)
        self.assertIn("hot default", problems[0])

    def test_small_window_skips(self):
        window = [_entry("p0", AXES_A), _entry("p1", AXES_A)]
        self.assertEqual(csh.check_hot_axis(AXES_A, window, 2), [])

    def test_diverse_window_passes(self):
        axes_c = {
            "theme": "Bold Studio Solid", "background": "full-bleed cinematic imagery",
            "typography": "Swiss rational hierarchy", "hero": "cinematic centered minimalist",
            "section": "modular bento rhythm", "signature": "turning polaroid arc",
            "motion": "cinematic fade-through",
        }
        window = [_entry("p0", AXES_A), _entry("p1", AXES_B), _entry("p2", axes_c)]
        self.assertEqual(csh.check_hot_axis(AXES_A, window, 3), [])


class TestStampLies(unittest.TestCase):
    def test_consistent_stamp_passes(self):
        current = {"axes": AXES_A,
                   "stamp": {"mode": "experience", "A": "deep-dark", "B": "tactile-texture"}}
        problems, extra = csh.check_stamp_lies(
            "/* maliang · mode=experience · A=deep-dark · B=tactile-texture */", current)
        self.assertEqual(problems, [])

    def test_mismatched_mode_reports(self):
        current = {"axes": AXES_A, "stamp": {"mode": "craft"}}
        problems, _ = csh.check_stamp_lies(
            "/* maliang · mode=experience · A=deep-dark */", current)
        self.assertTrue(any("mode" in p and "stamp lies" in p for p in problems))

    def test_missing_coordinate_reports(self):
        current = {"axes": AXES_A, "stamp": {"mode": "experience", "C": "editorial-serif"}}
        problems, _ = csh.check_stamp_lies(
            "/* maliang · mode=experience · A=deep-dark */", current)
        self.assertTrue(any("盖章缺坐标 C" in p for p in problems))

    def test_no_stamp_reports_missing(self):
        problems, _ = csh.check_stamp_lies("body { color: red; }", {"axes": AXES_A, "stamp": {"mode": "x"}})
        self.assertTrue(any("缺章" in p for p in problems))

    def test_no_declaration_is_noop(self):
        problems, _ = csh.check_stamp_lies("anything", {"axes": AXES_A})
        self.assertEqual(problems, [])


class TestCli(unittest.TestCase):
    def _write(self, directory, name, payload):
        path = os.path.join(directory, name)
        with open(path, "w", encoding="utf-8") as fh:
            if isinstance(payload, str):
                fh.write(payload)
            else:
                json.dump(payload, fh, ensure_ascii=False)
        return path

    def _current(self, directory, axes=AXES_B, **extra):
        payload = {"page": "p-new", "mode": "Experience", "axes": axes}
        payload.update(extra)
        return self._write(directory, "current.json", payload)

    def test_fixture_smoke_passes(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = csh.main([
                "--current", os.path.join(FIXTURES, "current.json"),
                "--log", os.path.join(FIXTURES, "log.json"),
                "--stamp", os.path.join(FIXTURES, "stamp.css"),
            ])
        self.assertEqual(code, 0, buf.getvalue())
        self.assertIn("结构核验通过", buf.getvalue())

    def test_repeat_and_hot_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = [_entry("prev", AXES_A), _entry("old1", AXES_A), _entry("old2", AXES_A)]
            log_path = self._write(tmp, "log.json", log)
            cur = self._current(tmp, axes=dict(AXES_A))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = csh.main(["--current", cur, "--log", log_path])
            self.assertEqual(code, 1)
            out = buf.getvalue()
            self.assertIn("重复", out)
            self.assertIn("hot default", out)

    def test_missing_log_is_unmeasured_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            cur = self._current(tmp)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = csh.main(["--current", cur, "--log",
                                 os.path.join(tmp, "no-such-log.json")])
            self.assertEqual(code, 2)
            self.assertIn("UNMEASURED", err.getvalue())

    def test_missing_current_exits_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = csh.main(["--current", "/nonexistent/current.json"])
        self.assertEqual(code, 2)

    def test_stamp_lie_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = self._write(tmp, "log.json", [_entry("prev", AXES_A)])
            cur = self._current(tmp, **{"stamp": {"mode": "craft", "A": "pristine-light"}})
            stamp = self._write(tmp, "stamp.css",
                                "/* maliang · mode=experience · A=deep-dark */")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = csh.main(["--current", cur, "--log", log_path, "--stamp", stamp])
            self.assertEqual(code, 1)
            self.assertIn("stamp lies", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
