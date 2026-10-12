"""verify-assets.py(#29/G40)的单元测试 + fixture 冒烟。"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

va = load("verify-assets.py")

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "assets")


def _manifest(tmp, payload, name="manifest.json"):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    return path


LOGO_URL = "https://cdn.example.com/acme-logo.svg"
MANIFEST = [{"slot": "logo", "assetKey": "acme-logo", "url": LOGO_URL}]


class TestVerify(unittest.TestCase):
    def test_declared_asset_present_passes(self):
        html = '<img id="logo" src="%s" alt="Acme">' % LOGO_URL
        findings, warnings, summary = va.verify_assets(html, MANIFEST, "a.html")
        self.assertEqual(findings, [])
        self.assertEqual(summary["manifest_slots"], 1)
        self.assertEqual(summary["enum_slots"], 1)

    def test_declared_asset_missing_fails_with_fix_hint(self):
        html = '<img src="https://cdn.example.com/other.png" alt="x">'
        findings, _, _ = va.verify_assets(html, MANIFEST, "a.html")
        self.assertTrue(any("未在场" in f["message"] and "最小修复" in f["message"]
                            for f in findings))

    def test_placeholder_class_rejected(self):
        html = '<div class="logo placeholder"></div><img class="skeleton" src="tbd.png">'
        findings, _, _ = va.verify_assets(html, MANIFEST, "a.html")
        # 声明缺席 + 占位签名
        self.assertTrue(any("占位签名" in f["message"] for f in findings))
        self.assertTrue(any("未在场" in f["message"] for f in findings))

    def test_data_uri_shill_rejected(self):
        html = ('<img src="%s" alt="logo">'
                '<img src="data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=" alt="x">') % LOGO_URL
        findings, _, _ = va.verify_assets(html, MANIFEST, "a.html")
        self.assertTrue(any("data-URI 空壳" in f["message"] for f in findings))

    def test_emoji_alt_rejected(self):
        html = ('<img src="%s" alt="logo">'
                '<span class="logo">\U0001F680</span>') % LOGO_URL
        findings, _, _ = va.verify_assets(html, MANIFEST, "a.html")
        # emoji 不在 alt 里不误报(在文本节点,归 detect-tells 管道);alt 里 emoji 才拒
        html2 = '<img src="%s" alt="\U0001F680">' % LOGO_URL
        findings2, _, _ = va.verify_assets(html2, MANIFEST, "a.html")
        self.assertTrue(any("alt 里是 emoji" in f["message"] for f in findings2))
        self.assertFalse(any("alt 里是 emoji" in f["message"] for f in findings))

    def test_text_only_svg_logo_rejected(self):
        html = ('<img src="%s" alt="logo">'
                '<svg class="brand-logo"><text x="0" y="10">A</text></svg>') % LOGO_URL
        findings, _, _ = va.verify_assets(html, MANIFEST, "a.html")
        self.assertTrue(any("自造内联 SVG" in f["message"] for f in findings))

    def test_declared_more_than_slots_warns(self):
        html = "<p>没有图槽</p>"
        findings, warnings, _ = va.verify_assets(html, MANIFEST, "a.html")
        self.assertTrue(any("有声明无槽位" in w for w in warnings))
        self.assertTrue(findings)  # 声明资产当然也不在场

    def test_assetkey_match_counts_as_present(self):
        # URL/logoAssetKey 匹配即算在场(外部原口径:URL 或 logoAssetKey)
        html = '<img data-asset-key="acme-logo" src="./assets/acme-logo.svg" alt="Acme">'
        manifest = [{"slot": "logo", "assetKey": "acme-logo", "url": "https://cdn.example.com/x.svg"}]
        findings, _, _ = va.verify_assets(html, manifest, "a.html")
        self.assertFalse(any("未在场" in f["message"] for f in findings))


class TestCli(unittest.TestCase):
    def test_fixture_passes_exit_0(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = va.main([os.path.join(FIXTURES, "pass.html"),
                            "--manifest", os.path.join(FIXTURES, "manifest.json")])
        self.assertEqual(code, 0, buf.getvalue())

    def test_missing_manifest_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = os.path.join(tmp, "page.html")
            open(html, "w", encoding="utf-8").write("<p>x</p>")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = va.main([html])
            self.assertEqual(code, 2)
            self.assertIn("manifest", err.getvalue())

    def test_bad_manifest_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = os.path.join(tmp, "page.html")
            open(html, "w", encoding="utf-8").write("<p>x</p>")
            bad = _manifest(tmp, {"not": "a list"})
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = va.main([html, "--manifest", bad])
            self.assertEqual(code, 2)

    def test_missing_html_exit_2(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = va.main([os.path.join("no", "such.html")])
        self.assertEqual(code, 2)

    def test_failure_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = os.path.join(tmp, "page.html")
            open(html, "w", encoding="utf-8").write('<img class="placeholder" src="tbd">')
            manifest = _manifest(tmp, MANIFEST)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = va.main([html, "--manifest", manifest])
            self.assertEqual(code, 1)
            self.assertIn("不许宣称完成", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
