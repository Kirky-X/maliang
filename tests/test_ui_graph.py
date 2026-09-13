"""ui-graph.py 核心流程的 fixture 集成测试。

在临时目录构建最小 ui-markdown 结构(2 个有关联跳转的页面),
验证 generate / check-nav / list-missing 的应报与不应报。
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

ug = load("ui-graph.py")

PAGE_FM = (
    "---\n"
    "name: {name}\n"
    "description: {desc}\n"
    "background: \"{{surface-base}}\"\n"
    "updated: 2026-09-05\n"
    "version: 1.0.0\n"
    "components: [button]\n"
    "---\n\n"
    "## 顶部导航\n\n"
    "| 参数 | 值 | 说明 |\n| --- | --- | --- |\n"
    "| 组件类型 | `navigation` | |\n"
    "| action | tap=无; state=无; db=无; api=无; long-press=无 | |\n\n"
    "{body}\n"
)


def _make_tree(root, home_action):
    """构建 home(一级) → setting/about(二级) 两页结构。

    root 限定为系统临时目录下的既有目录(realpath 校验),防路径逃逸。
    """
    base = Path(os.path.realpath(root))
    if base.parent != Path(tempfile.gettempdir()):
        raise ValueError("fixture root 必须位于系统临时目录内: " + str(base))
    ui = base / "ui"
    setting = ui / "setting"
    setting.mkdir(parents=True)
    (base / "token.md").write_text(
        "# token\n\n| Token | 值 |\n| --- | --- |\n| surface-base | #FFFFFF |\n",
        encoding="utf-8")
    (ui / "home.md").write_text(PAGE_FM.format(
        name="home", desc="首页",
        body="| action | " + home_action + " | |\n",
    ), encoding="utf-8")
    (setting / "about.md").write_text(PAGE_FM.format(
        name="about", desc="关于", body="正文\n",
    ), encoding="utf-8")
    return str(base)


class TestUiGraph(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/setting/about.md; state=无; db=无; api=无")

    def tearDown(self):
        self._tmp.cleanup()

    def test_generate_and_clean_nav(self):
        # 不应报: home → setting/about 跳转目标存在
        result = ug.generate(self.root)
        self.assertEqual(len(result["pages"]), 2)
        self.assertEqual(len(result["navigations"]), 1)
        self.assertTrue(os.path.isfile(
            str(Path(self.root) / "ui-relationships.json")))
        missing = ug.list_missing(self.root)
        self.assertEqual(missing, [])
        nav_issues = ug.check_nav(self.root)
        dangling = [i for i in nav_issues if "目标不存在" in str(i)]
        self.assertEqual(dangling, [])

    def test_dangling_nav_reported(self):
        # 应报: 跳转目标页面不存在
        ug.generate(self.root)
        home = Path(self.root) / "ui" / "home.md"
        patched = home.read_text(encoding="utf-8").replace(
            "tap=→ui/setting/about.md", "tap=→ui/ghost-page.md")
        home.write_text(patched, encoding="utf-8")
        ug.generate(self.root)
        missing = ug.list_missing(self.root)
        self.assertTrue(any("ghost-page" in str(m) for m in missing))
        rel_json = json.loads(
            (Path(self.root) / "ui-relationships.json").read_text(encoding="utf-8"))
        self.assertTrue(any(
            nav["to"].endswith("ghost-page.md") for nav in rel_json["navigations"]))

    def test_nav_target_normalization(self):
        # 不应报: 无 .md 后缀、无 ui/ 前缀的写法归一化到同一目标
        navs = ug.extract_navigations("tap=→setting/about; state=无")
        self.assertEqual(navs, [{"to": "ui/setting/about.md", "event": "tap"}])

    def test_non_nav_events_skipped(self):
        # 不应报: 无/back 非页面跳转
        navs = ug.extract_navigations("tap=无; long-press=back; api=无")
        self.assertEqual(navs, [])

    def test_parent_depth_derivation(self):
        self.assertEqual(ug._derive_parent_and_depth("ui/home.md"), (None, 1))
        self.assertEqual(ug._derive_parent_and_depth("ui/setting/about.md"), ("setting", 2))
        self.assertEqual(ug._derive_parent_and_depth("organisms/nav-bar.md"), (None, 0))

    def test_missing_dir_raises(self):
        # 显性失败: 目录不存在抛 FileNotFoundError,不假装成功
        with self.assertRaises(FileNotFoundError):
            ug.parse_directory(str(Path(self.root) / "no-such-dir"))


class TestBuildImplMap(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/setting/about.md; state=无; db=无; api=无")
        ug.generate(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_device_suffix_and_views_convention(self):
        # 不应报: preview_<page>_<device>.html(preview.md 命名约定)与
        # **/views/<slug>.vue(element 代码约定)均应匹配到 ui/home.md
        preview_root = Path(self.root) / "preview"
        preview_root.mkdir()
        (preview_root / "preview_home_iphone15.html").write_text(
            "<html><body>home preview</body></html>", encoding="utf-8")
        code_root = Path(self.root) / "element"
        (code_root / "views").mkdir(parents=True)
        (code_root / "views" / "Home.vue").write_text(
            "<template><div /></template>\n", encoding="utf-8")
        ug.build_impl_map(self.root, str(preview_root), str(code_root))
        data = json.loads(
            (Path(self.root) / "ui-implementation-map.json").read_text(encoding="utf-8"))
        by_path = {m["logical_ui"]: m for m in data["mappings"]}
        home = by_path["ui/home.md"]
        self.assertEqual(home["status"], "implemented")
        self.assertTrue(home["preview_html"].endswith("preview_home_iphone15.html"))
        self.assertTrue(home["framework_code"]["element"].endswith("views/Home.vue"))
        about = by_path["ui/setting/about.md"]
        self.assertEqual(about["status"], "missing")


if __name__ == "__main__":
    unittest.main()
