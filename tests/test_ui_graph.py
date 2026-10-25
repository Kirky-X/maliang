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

    def test_tap_arrow_without_equals_is_matched(self):
        # 2026-10 补:home.md:17 的 `左=tap→抽屉菜单` 变体(无等号)此前零命中,
        # 14 处导航声明对 check-nav 结构性不可见——现在必须能取到
        navs = ug.extract_navigations("nav-bar action:左=tap→ui/drawer.md; 中=无; 右=tap→ui/message.md")
        tos = sorted(n["to"] for n in navs)
        self.assertEqual(tos, ["ui/drawer.md", "ui/message.md"])

    def test_table_target_column_is_extracted(self):
        # 2026-10 补:金刚区/dock/about 的表格 target 列(`tap=跳转至 item.target 声明页面`)
        # 是第三种导航声明形态,此前 check-nav 看不见
        table = (
            "### 3.2 金刚区\n\n"
            "| 字段 | 类型 | 说明 |\n| --- | --- | --- |\n"
            "| `label` | string | 名称 |\n"
            "| `target` | string | tap 跳转目标 |\n\n"
            "| id | label | target |\n| --- | --- | --- |\n"
            "| feed | 信息流 | ui/feed.md |\n"
            "| rank | 排行榜 | ui/rank.md |\n"
        )
        navs = ug.extract_navigations(table)
        tos = sorted(n["to"] for n in navs)
        self.assertEqual(tos, ["ui/feed.md", "ui/rank.md"])

    def test_table_rows_without_target_column_ignored(self):
        # 不应报: 无 target 列的普通参数表
        table = "| 参数 | 值 |\n| --- | --- |\n| 组件类型 | `navigation` |\n"
        self.assertEqual(ug.extract_navigations(table), [])

    def test_table_non_page_targets_ignored(self):
        # 不应报: history.back 尾注、action: 动作标识、外链 URL——都不是页面目标
        table = (
            "| 项目 | target |\n| --- | --- |\n"
            "| 返回 | history.back(返回上一级) |\n"
            "| 检查更新 | action:check-update(检查新版本) |\n"
            "| 官网 | https://maliang.example.com |\n"
        )
        self.assertEqual(ug.extract_navigations(table), [])

    def test_parent_depth_derivation(self):
        self.assertEqual(ug._derive_parent_and_depth("ui/home.md"), (None, 1))
        self.assertEqual(ug._derive_parent_and_depth("ui/setting/about.md"), ("setting", 2))
        self.assertEqual(ug._derive_parent_and_depth("organisms/nav-bar.md"), (None, 0))

    def test_missing_dir_raises(self):
        # 显性失败: 目录不存在抛 FileNotFoundError,不假装成功
        with self.assertRaises(FileNotFoundError):
            ug.parse_directory(str(Path(self.root) / "no-such-dir"))


class TestDiffHash(unittest.TestCase):
    """diff-hash 基线对比:无快照容错(视为 added)/无变更/修改与删除检出。

    无 ui-hash-state.json 时不作硬失败,视为空基线(对齐 ui-graph.md
    失败模式表:输出"无历史快照,所有文件视为 added",提示先跑 compute-hash);
    此语义同时是 critique backlog 指纹失效判定的基础。
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/setting/about.md; state=无; db=无; api=无")

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_baseline_treated_as_added(self):
        # 不应阻断: 无快照视为空基线,全部页面计入 added(token.md 仍排除)
        result = ug.diff_hash(self.root)
        self.assertTrue(result["baseline_missing"])
        self.assertEqual(result["added"],
                         ["ui/home.md", "ui/setting/about.md"])
        self.assertNotIn("token.md", result["added"])
        self.assertEqual(result["modified"], [])
        self.assertEqual(result["deleted"], [])

    def test_unchanged_reports_no_diff(self):
        # 不应报: 建基线后无任何改动,三列表全空且 baseline_missing=False
        ug.compute_hash(self.root)
        result = ug.diff_hash(self.root)
        self.assertFalse(result["baseline_missing"])
        self.assertEqual(
            (result["added"], result["modified"], result["deleted"]),
            ([], [], []))

    def test_modified_and_deleted_detected(self):
        # 应报: 逐字节比对——home.md 改一个字节即 modified,删除即 deleted
        ug.compute_hash(self.root)
        home = Path(self.root) / "ui" / "home.md"
        patched = home.read_text(encoding="utf-8") + "\n<!-- touched -->\n"
        home.write_text(patched, encoding="utf-8")
        (Path(self.root) / "ui" / "setting" / "about.md").unlink()
        result = ug.diff_hash(self.root)
        self.assertEqual(result["modified"], ["ui/home.md"])
        self.assertEqual(result["deleted"], ["ui/setting/about.md"])
        self.assertEqual(result["added"], [])


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


class TestPreviewHash(unittest.TestCase):
    """--kind preview 哈希扩展(#17 落点):预览 HTML/截图清单指纹。

    与 critique 的 draw-md 产物指纹区分:基线文件为 preview-hash-state.json,
    只收 HTML/截图/取证清单,不收 selection.json(交互记录不是产物)。
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(os.path.realpath(self._tmp.name))
        self.root = str(base / "preview")
        (base / "preview" / "shots").mkdir(parents=True)
        (base / "preview" / "preview_home.html").write_text(
            "<html><body>v1</body></html>", encoding="utf-8")
        (base / "preview" / "shots" / "home-idle.png").write_text("png1", encoding="utf-8")
        (base / "preview" / "shots" / "report.json").write_text(
            '{"schema": "maliang-evidence/1"}', encoding="utf-8")
        (base / "preview" / "selection.json").write_text('{"id": "1"}', encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_preview_hash_scope_and_state_file(self):
        # 不应报: 收 HTML/截图/清单;排除 selection.json;基线文件独立命名
        result = ug.compute_hash(self.root, kind="preview")
        paths = [f["path"] for f in result["files"]]
        self.assertIn("preview_home.html", paths)
        self.assertIn("shots/home-idle.png", paths)
        self.assertIn("shots/report.json", paths)
        self.assertNotIn("selection.json", paths)
        self.assertEqual(result["kind"], "preview")
        state = Path(self.root) / "preview-hash-state.json"
        self.assertTrue(state.is_file())
        self.assertFalse((Path(self.root) / "ui-hash-state.json").exists(),
                         "preview 指纹不得混用 draw-md 基线文件")

    def test_preview_diff_detects_screenshot_change(self):
        # 应报: 截图或 report.json 改一个字节 → modified(逐字节比对)
        ug.compute_hash(self.root, kind="preview")
        shot = Path(self.root) / "shots" / "home-idle.png"
        shot.write_text("png2", encoding="utf-8")
        result = ug.diff_hash(self.root, kind="preview")
        self.assertIn("shots/home-idle.png", result["modified"])
        report = Path(self.root) / "shots" / "report.json"
        report.write_text('{"schema": "maliang-evidence/1", "changed": true}', encoding="utf-8")
        result = ug.diff_hash(self.root, kind="preview")
        self.assertIn("shots/report.json", result["modified"])

    def test_draw_md_kind_unchanged(self):
        # 不应报: draw-md 默认口径与既有行为一致(仍排除 token.md、写 ui-hash-state.json)
        base = str(Path(self.root).parent / "mds")
        Path(base, "ui").mkdir(parents=True)
        (Path(base) / "token.md").write_text("# token", encoding="utf-8")
        (Path(base) / "ui" / "home.md").write_text("# home", encoding="utf-8")
        result = ug.compute_hash(base)
        self.assertEqual([f["path"] for f in result["files"]], ["ui/home.md"])
        self.assertTrue((Path(base) / "ui-hash-state.json").is_file())

    def test_unknown_kind_rejected(self):
        # 应报: 未知 kind 显性失败
        with self.assertRaises(ValueError):
            ug.compute_hash(self.root, kind="no-such-kind")


class TestTokenUsage(unittest.TestCase):
    """token-usage 反向索引:token → 波及页面 + 孤儿 token(DESIGN.md 变更波及分析)。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/setting/about.md; state=无; db=无; api=无")

    def tearDown(self):
        self._tmp.cleanup()

    def test_usage_index_and_orphan(self):
        # 应报: surface-base 被两页引用;token.md 新增未被引用的 spacing-xl 是孤儿
        token_path = Path(self.root) / "token.md"
        token_path.write_text(
            token_path.read_text(encoding="utf-8") + "| spacing-xl | 32px |\n",
            encoding="utf-8")
        result = ug.token_usage(self.root)
        self.assertEqual(result["tokens"].get("surface-base"),
                         ["ui/home.md", "ui/setting/about.md"])
        self.assertEqual(result["unreferenced"], ["spacing-xl"])
        self.assertTrue((Path(self.root) / "token-usage.json").is_file())

    def test_action_line_placeholder_not_token(self):
        # 不应报: action 行的 {input-value} 是 URL 模板参数,不算 token 引用
        home = Path(self.root) / "ui" / "home.md"
        patched = home.read_text(encoding="utf-8").replace(
            "tap=→ui/setting/about.md", "tap=→ui/search.md?q={input-value}")
        home.write_text(patched, encoding="utf-8")
        result = ug.token_usage(self.root)
        self.assertNotIn("input-value", result["tokens"])


class TestCodeHashAndCheckSync(unittest.TestCase):
    """--kind code 实现指纹 + check-sync 四态分类(规格先行/代码漂移/双侧分叉/同步)。

    基线语义 = 「上次全部对齐时的快照」:build-impl-map 后连跑两个
    compute-hash 建基线;之后任一侧单独变即对应失同步态。
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/setting/about.md; state=无; db=无; api=无")
        ug.generate(self.root)
        self.preview_root = Path(self.root) / "preview"
        self.preview_root.mkdir()
        (self.preview_root / "preview_home_iphone15.html").write_text(
            "<html><body>home v1</body></html>", encoding="utf-8")
        self.code_root = Path(self.root) / "element"
        (self.code_root / "views").mkdir(parents=True)
        self.vue = self.code_root / "views" / "Home.vue"
        self.vue.write_text("<template><div>home v1</div></template>\n",
                            encoding="utf-8")
        ug.build_impl_map(self.root, str(self.preview_root), str(self.code_root))
        ug.compute_hash(self.root)
        ug.compute_hash(self.root, kind="code")

    def tearDown(self):
        self._tmp.cleanup()

    def test_compute_hash_code_covers_impl_files(self):
        # 不应报: code 基线收 impl-map 映射的实现文件(preview HTML + vue)
        state = json.loads(
            (Path(self.root) / "code-hash-state.json").read_text(encoding="utf-8"))
        paths = [f["path"] for f in state["files"]]
        self.assertTrue(any(p.endswith("Home.vue") for p in paths), paths)
        self.assertTrue(any(p.endswith("preview_home_iphone15.html") for p in paths))
        self.assertTrue(all(len(f["sha256"]) == 64
                            for f in state["files"] if not f.get("missing")))

    def test_diff_hash_code_detects_code_change(self):
        self.vue.write_text("<template><div>home v2</div></template>\n",
                            encoding="utf-8")
        result = ug.diff_hash(self.root, kind="code")
        self.assertTrue(any("Home.vue" in p for p in result["modified"]))

    def test_in_sync_when_nothing_changed(self):
        result = ug.check_sync(self.root)
        by_page = {s["logical_ui"]: s["status"] for s in result["statuses"]}
        self.assertEqual(by_page.get("ui/home.md"), "in-sync")
        self.assertNotIn("ui/setting/about.md", by_page)  # missing 页不参与判定

    def test_spec_ahead_when_md_changed_only(self):
        home = Path(self.root) / "ui" / "home.md"
        home.write_text(
            home.read_text(encoding="utf-8") + "\n<!-- spec touch -->\n",
            encoding="utf-8")
        result = ug.check_sync(self.root)
        by_page = {s["logical_ui"]: s["status"] for s in result["statuses"]}
        self.assertEqual(by_page.get("ui/home.md"), "spec-ahead")

    def test_code_drifted_when_code_changed_only(self):
        self.vue.write_text("<template><div>hand edited</div></template>\n",
                            encoding="utf-8")
        result = ug.check_sync(self.root)
        by_page = {s["logical_ui"]: s["status"] for s in result["statuses"]}
        self.assertEqual(by_page.get("ui/home.md"), "code-drifted")

    def test_diverged_when_both_changed(self):
        home = Path(self.root) / "ui" / "home.md"
        home.write_text(
            home.read_text(encoding="utf-8") + "\n<!-- spec touch -->\n",
            encoding="utf-8")
        self.vue.write_text("<template><div>hand edited</div></template>\n",
                            encoding="utf-8")
        result = ug.check_sync(self.root)
        by_page = {s["logical_ui"]: s["status"] for s in result["statuses"]}
        self.assertEqual(by_page.get("ui/home.md"), "diverged")

    def test_deleted_code_counts_as_drift(self):
        self.vue.unlink()
        result = ug.check_sync(self.root)
        entry = [s for s in result["statuses"] if s["logical_ui"] == "ui/home.md"][0]
        self.assertEqual(entry["status"], "code-drifted")
        self.assertTrue(any("Home.vue" in p for p in entry["missing_files"]))

    def test_missing_baseline_raises(self):
        (Path(self.root) / "ui-hash-state.json").unlink()
        with self.assertRaises(FileNotFoundError):
            ug.check_sync(self.root)

    def test_compute_hash_code_requires_impl_map(self):
        (Path(self.root) / "ui-implementation-map.json").unlink()
        with self.assertRaises(FileNotFoundError):
            ug.compute_hash(self.root, kind="code")

    def test_anchor_decouples_consumer_cwd(self):
        # 审查 H1:基线锚定在 impl-map 的 base_dir,消费方换 cwd 不产生假漂移/假同步
        impl_path = Path(self.root) / "ui-implementation-map.json"
        impl = json.loads(impl_path.read_text(encoding="utf-8"))
        self.assertIn("base_dir", impl)
        old_cwd = os.getcwd()
        try:
            os.chdir(tempfile.gettempdir())
            result = ug.check_sync(self.root)
            by_page = {s["logical_ui"]: s["status"] for s in result["statuses"]}
            self.assertEqual(by_page.get("ui/home.md"), "in-sync")
        finally:
            os.chdir(old_cwd)

    def test_compute_hash_code_refuses_missing_impl_file(self):
        # 审查 H1/M1:实现文件缺失时拒绝建立基线(防 None==None 伪造全同步)
        self.vue.unlink()
        with self.assertRaises(FileNotFoundError):
            ug.compute_hash(self.root, kind="code")
        # setUp 建立的合法基线仍在,且未被含缺失的空测量覆盖
        self.assertFalse(self._code_state_has_missing())
        state = json.loads(
            (Path(self.root) / "code-hash-state.json").read_text(encoding="utf-8"))
        self.assertTrue(all(f["sha256"] for f in state["files"]))

    def _code_state_has_missing(self):
        p = Path(self.root) / "code-hash-state.json"
        if not p.is_file():
            return False
        state = json.loads(p.read_text(encoding="utf-8"))
        return any(f.get("missing") for f in state["files"])

    def test_impl_map_absolute_path_rejected(self):
        # 审查 M-1:impl-map 记录绝对路径/.. 穿越时拒绝消费(防越界读取)
        impl_path = Path(self.root) / "ui-implementation-map.json"
        impl = json.loads(impl_path.read_text(encoding="utf-8"))
        for m in impl["mappings"]:
            if m.get("preview_html"):
                m["preview_html"] = "C:/Windows/win.ini"
                break
        impl_path.write_text(json.dumps(impl, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValueError):
            ug.compute_hash(self.root, kind="code")
        impl["mappings"][0]["preview_html"] = "../../etc/passwd"
        impl_path.write_text(json.dumps(impl, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValueError):
            ug.check_sync(self.root)

    def test_cli_check_sync_corrupt_baseline_exits_2(self):
        # 审查 L-1:基线 JSON 损坏 → 退出码 2(没能检查),不是崩溃退出码 1
        import contextlib
        import io
        (Path(self.root) / "code-hash-state.json").write_text(
            "{broken json", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ug.main(["ui-graph.py", "check-sync", "--target", self.root])
        self.assertEqual(code, 2)


class TestCheckNavStrict(unittest.TestCase):
    """check-nav 退出码:--strict 按三态拦(异常=1),缺省 informational 退 0。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/ghost-page.md; state=无; db=无; api=无")
        ug.generate(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *extra):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            return ug.main(["ui-graph.py", "check-nav", "--target", self.root]
                           + list(extra))

    def test_default_informational_exit_zero(self):
        # 缺省:发现死链仍退 0(EXIT-CODES.md 迁移登记的 informational 语义)
        self.assertEqual(self._run(), 0)

    def test_strict_exit_one_on_anomaly(self):
        # --strict:同树同发现,退出码 1(无人值守按三态判定)
        self.assertEqual(self._run("--strict"), 1)

    def test_strict_exit_zero_when_clean(self):
        home = Path(self.root) / "ui" / "home.md"
        patched = home.read_text(encoding="utf-8").replace(
            "tap=→ui/ghost-page.md", "tap=→ui/setting/about.md")
        home.write_text(patched, encoding="utf-8")
        ug.generate(self.root)
        self.assertEqual(self._run("--strict"), 0)


class TestCyclesAndUnimplemented(unittest.TestCase):
    """既有盲区补测:长度 2 的循环检出、list-unimplemented 的 missing 报告。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = _make_tree(
            self._tmp.name, "tap=→ui/setting/about.md; state=无; db=无; api=无")
        ug.generate(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_cycle_pair_detected(self):
        # 应报: home→about 已有,补 about→home 构成 A↔B 长度 2 的环
        about = Path(self.root) / "ui" / "setting" / "about.md"
        about.write_text(
            about.read_text(encoding="utf-8") + "\n返回=tap→ui/home.md\n",
            encoding="utf-8")
        ug.generate(self.root)
        result = ug.check_nav(self.root)
        self.assertTrue(any(
            {c["a"], c["b"]} == {"ui/home.md", "ui/setting/about.md"}
            for c in result["cycles"]))

    def test_list_unimplemented_reports_missing_pages(self):
        # 应报: 只有 home 有实现(仅 preview),about 无 preview 无代码 → missing
        preview_root = Path(self.root) / "preview"
        preview_root.mkdir()
        (preview_root / "preview_home_iphone15.html").write_text(
            "<html><body>home</body></html>", encoding="utf-8")
        empty_code = Path(self.root) / "element"
        empty_code.mkdir()
        ug.build_impl_map(self.root, str(preview_root), str(empty_code))
        missing = ug.list_unimplemented(self.root)
        self.assertEqual([m["logical_ui"] for m in missing],
                         ["ui/setting/about.md"])

    def test_list_unimplemented_empty_when_all_implemented(self):
        # 不应报: 每页至少 preview 或代码一项 → status 非 missing,清单为空
        preview_root = Path(self.root) / "preview"
        preview_root.mkdir()
        (preview_root / "preview_home_iphone15.html").write_text("h", encoding="utf-8")
        (preview_root / "preview_about_iphone15.html").write_text("a", encoding="utf-8")
        empty_code = Path(self.root) / "element"
        empty_code.mkdir()
        ug.build_impl_map(self.root, str(preview_root), str(empty_code))
        self.assertEqual(ug.list_unimplemented(self.root), [])


if __name__ == "__main__":
    unittest.main()
