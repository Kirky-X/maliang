"""verify-color-fidelity.py(#24/G39)的单元测试:五组攻击聚合盲区 + 三态退出码。

对应 G39 反聚合设计:显著错误色块不得被均值掩盖 / 大错误区域配稀有参考色
仍 FAIL / 缺失显著参考色反向 max / 0.1% 残渣不算保留 / 0.3502>0.35 边界。
B 工作流勘误:FAIL 是退出码 1 不是 2。
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
from _png import png_bytes, write_png

mc = load("measure-colors.py")
vcf = load("verify-color-fidelity.py")


def _build(tmp, name, pixel_at, size=(100, 100)):
    return write_png(os.path.join(tmp, name), size[0], size[1], pixel_at)


def _verify_pair(tmp, ref_at, impl_at, ref_size=(100, 100), impl_size=(100, 100)):
    ref = _build(tmp, "ref.png", ref_at, ref_size)
    impl = _build(tmp, "impl.png", impl_at, impl_size)
    ref_palette, ref_k = vcf.load_reference(ref, None)
    impl_result = mc.measure_image(impl, ref_k)
    return vcf.verify(impl_result, ref_palette, ref_k)


class TestAttackBlindSpots(unittest.TestCase):
    """五组攻击聚合盲区用例(B 工作流验收硬性要求)。"""

    def test_significant_wrong_cluster_not_averaged_away(self):
        # ① 白底 4% 黑块:ΔE>100 的错误色块不得被覆盖率加权平均掉
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(tmp, lambda x, y: (255, 255, 255),
                                  lambda x, y: (0, 0, 0) if x < 4 else (255, 255, 255))
        black = next(c for c in report["implementationClusters"] if c["imageHex"] == "#000000")
        self.assertAlmostEqual(black["imageCoverage"], 0.04, places=3)
        self.assertGreater(black["deltaE"], 90)
        self.assertGreater(report["maxDeltaE"], 90)
        self.assertFalse(report["pass"])

    def test_large_wrong_region_with_rare_reference_still_fails(self):
        # ② 参考 0.4% 黑(亚显著),实现 17.5% 灰:走实现侧逐簇 max 暴露
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(
                tmp,
                lambda x, y: (0, 0, 0) if y * 100 + x < 40 else (255, 255, 255),
                lambda x, y: (85, 85, 85) if y * 100 + x < 1750 else (255, 255, 255))
        gray = next(c for c in report["implementationClusters"] if c["imageHex"] == "#555555")
        self.assertAlmostEqual(gray["imageCoverage"], 0.175, places=3)
        self.assertGreater(gray["deltaE"], 20)
        self.assertLess(report["coverageDrift"], report["thresholds"]["coverageDrift"])
        self.assertFalse(report["pass"])

    def test_missing_significant_reference_exposed_in_reverse(self):
        # ③ 参考 10% 黑,实现全白:参考侧 max ΔE 反向暴露缺失
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(
                tmp,
                lambda x, y: (0, 0, 0) if x < 10 else (255, 255, 255),
                lambda x, y: (255, 255, 255))
        missing = next(e for e in report["entries"] if e["specHex"] == "#000000")
        self.assertEqual(missing["nearestImageHex"], "#ffffff")
        self.assertGreater(missing["deltaE"], 90)
        self.assertFalse(report["pass"])

    def test_trace_remnant_does_not_count_as_preserved(self):
        # ④ 参考 10% 黑,实现 0.1% 黑:残渣不算保留,最近匹配只在显著簇里找
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(
                tmp,
                lambda x, y: (0, 0, 0) if y * 100 + x < 1000 else (255, 255, 255),
                lambda x, y: (0, 0, 0) if y * 100 + x < 10 else (255, 255, 255))
        missing = next(e for e in report["entries"] if e["specHex"] == "#000000")
        self.assertAlmostEqual(missing["imageCoverage"], 0.001, places=4)
        self.assertEqual(missing["nearestImageHex"], "#ffffff")
        self.assertGreater(missing["deltaE"], 90)
        self.assertLess(report["coverageDrift"], report["thresholds"]["coverageDrift"])
        self.assertFalse(report["pass"])

    def test_coverage_drift_boundary_03502(self):
        # ⑤ drift 0.3502 > 0.35 边界失败必须可解释(4 位小数)
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(
                tmp,
                lambda x, y: (0, 0, 0) if y * 100 + x < 10 else (255, 255, 255),
                lambda x, y: (0, 0, 0) if y * 100 + x < 1761 else (255, 255, 255))
        self.assertEqual(report["coverageDrift"], 0.3502)
        self.assertEqual(report["thresholds"]["coverageDrift"], 0.35)
        self.assertEqual(report["meanDeltaE"], 0.0)  # 只有漂移越线
        self.assertFalse(report["pass"])


class TestNormalPaths(unittest.TestCase):
    def test_same_image_passes_with_zero_de(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(tmp, lambda x, y: (59, 130, 246),
                                  lambda x, y: (59, 130, 246), ref_size=(40, 40), impl_size=(40, 40))
        self.assertTrue(report["pass"])
        self.assertEqual(report["meanDeltaE"], 0.0)
        self.assertEqual(report["maxDeltaE"], 0.0)
        self.assertEqual(report["coverageDrift"], 0.0)

    def test_entry_deltae_describes_nearest_image_hex(self):
        # 条目 ΔE 永远描述其 nearestImageHex(逐条目可复算)
        with tempfile.TemporaryDirectory() as tmp:
            report = _verify_pair(
                tmp,
                lambda x, y: (0, 0, 0) if x < 50 else (255, 255, 255),
                lambda x, y: (20, 20, 20) if x < 25 else ((80, 80, 80) if x < 50 else (245, 245, 245)))
        for e in report["entries"]:
            expected = round(mc.delta_e(vcf.parse_hex(e["specHex"]),
                                        vcf.parse_hex(e["nearestImageHex"])), 2)
            self.assertEqual(e["deltaE"], expected)

    def test_spec_json_reference_with_persisted_k(self):
        # 测量 spec(含 k)作参考:复测同 k,同图 PASS
        with tempfile.TemporaryDirectory() as tmp:
            img = _build(tmp, "g.png", lambda x, y: (59, 130, 246), size=(40, 40))
            measured = mc.measure_image(img, 3)
            spec_path = os.path.join(tmp, "spec.json")
            json.dump(measured, open(spec_path, "w", encoding="utf-8"))
            palette, k = vcf.load_reference(spec_path, None)
            self.assertEqual(k, 3)
            impl_result = mc.measure_image(img, k)
            self.assertTrue(vcf.verify(impl_result, palette, k)["pass"])

    def test_embedded_design_system_spec(self):
        measured = {"design_system": {"color": {
            "measured_palette": [{"hex": "#3b82f6", "coverage": 1.0, "role": "background"}],
            "measurement": {"k": 4}}}}
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = os.path.join(tmp, "spec.json")
            json.dump(measured, open(spec_path, "w", encoding="utf-8"))
            palette, k = vcf.load_reference(spec_path, None)
        self.assertEqual(k, 4)
        self.assertEqual(palette[0]["hex"], "#3b82f6")


class TestCli(unittest.TestCase):
    def _fixture_pair(self, tmp, impl_at=None):
        ref = write_png(os.path.join(tmp, "ref.png"), 40, 40, lambda x, y: (59, 130, 246))
        impl = write_png(os.path.join(tmp, "impl.png"), 40, 40,
                         impl_at or (lambda x, y: (59, 130, 246)))
        return impl, ref

    def test_same_image_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            impl, ref = self._fixture_pair(tmp)
            err, out = io.StringIO(), io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
                code = vcf.main([impl, "--reference", ref])
            self.assertEqual(code, 0)
            self.assertIn("PASS", err.getvalue())
            payload = json.loads(out.getvalue())
            self.assertTrue(payload["pass"])

    def test_shifted_image_exit_1_not_2(self):
        # B 工作流勘误:FAIL 是 1 不是 2
        with tempfile.TemporaryDirectory() as tmp:
            impl, ref = self._fixture_pair(tmp, lambda x, y: (180, 40, 40))
            err, out = io.StringIO(), io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
                code = vcf.main([impl, "--reference", ref])
            self.assertEqual(code, 1)
            self.assertIn("FAIL", err.getvalue())

    def test_missing_reference_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            impl, ref = self._fixture_pair(tmp)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = vcf.main([impl, "--reference", os.path.join(tmp, "gone.png")])
            self.assertEqual(code, 2)
            self.assertIn("UNMEASURED", err.getvalue())


if __name__ == "__main__":
    unittest.main()
