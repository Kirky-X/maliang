"""文档-脚本计数一致性断言:防 preview-checklist 扩分区后脚本头注/输出计数再漂移。

背景:整合轮发现 check 节头注停留 49/113 而清单已扩至 135 项,
清单(600ms)与脚本(400ms)双门槛漂移同源——纯文案改动,无逻辑,故用纯文本断言守护。
51 为实测可脚本化覆盖数(脚本检查分组 §5.1-§5.13),由 check 节演进时同步维护。
"""

import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECKLIST = os.path.join(BASE, "references", "commands", "preview-checklist.md")
PREVIEW_MD = os.path.join(BASE, "references", "commands", "preview.md")
PC_SCRIPT = os.path.join(BASE, "scripts", "preview.py")  # check 节(原 preview-check.py)
ADAPTER_CONTRACT = os.path.join(BASE, "references", "framework", "adapter-contract.md")
FRAMEWORK_INDEX = os.path.join(BASE, "references", "framework", "INDEX.md")
COMPONENT_ROUTING = os.path.join(BASE, "references", "framework", "component-routing.md")
GLASS_EFFECT = os.path.join(BASE, "references", "dimensions", "glass-effect.md")
DRAW_REACT = os.path.join(BASE, "references", "commands", "draw-react.md")
SKILL_MD = os.path.join(BASE, "SKILL.md")
README_MD = os.path.join(BASE, "README.md")

SCRIPTED = 51


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class TestCoverageCounts(unittest.TestCase):
    def test_script_and_preview_md_match_checklist_total(self):
        checklist = _read(CHECKLIST)
        m = re.search(r"= \*\*(\d+) 项\*\*", checklist)
        self.assertIsNotNone(m, "preview-checklist.md 统计行缺失或格式变更")
        total = int(m.group(1))
        runtime = total - SCRIPTED

        script = _read(PC_SCRIPT)
        self.assertIn("51/%d 项" % total, script,
                      "check 节头注覆盖计数与清单总数漂移")
        self.assertIn("覆盖: 51/%d 项" % total, script,
                      "check 节输出行覆盖计数与清单总数漂移")
        self.assertIn("其余 %d 项" % runtime, script,
                      "check 节输出行运行时计数与清单总数漂移")
        self.assertNotIn("(MANUAL,见 5.13)", script,
                         "运行时项指针漂移:5.13 仅为 CWV 分区,运行时项分布见输出行新指针")

        preview = _read(PREVIEW_MD)
        # 2026-10 起 preview.md 只保留分组速览表与路由,执行规则与 51/3/89 账本
        # 以 preview-checklist.md 为唯一 canonical——preview.md 不再复述账本,
        # 但必须显式指向该 canonical(防读者在 preview.md 侧找不到口径)。
        self.assertIn("唯一 canonical 在 [`preview-checklist.md`](./preview-checklist.md)", preview,
                      "preview.md 缺少指向 checklist 账本 canonical 的路由")
        self.assertNotIn("51 项由", preview,
                         "preview.md 复述了脚本覆盖账本(canonical 已收敛到 checklist)")
        gate_covered = 3  # verify-color-fidelity / verify-assets / check-copy
        runtime_after_gate = total - SCRIPTED - gate_covered
        self.assertIn("其余 %d 项" % runtime_after_gate, checklist,
                      "checklist 运行时计数与清单总数漂移")

    def test_checklist_uses_script_threshold_400ms(self):
        checklist = _read(CHECKLIST)
        self.assertNotIn("duration ≤ 600ms", checklist,
                         "入场时长口径须与脚本 400ms 硬门一致(分层长动效见 micro-interactions)")


class TestFrameworkAdapterDocs(unittest.TestCase):
    """framework-adapter-live-query 变更产物在场守护:删除文档或关键节即失败。"""

    def test_adapter_contract_exists_with_key_enums(self):
        text = _read(ADAPTER_CONTRACT)
        for token in ("registry-json", "docs-site", "bundled-snapshot",
                      "npm-package", "copy-paste", "用户强制指定门",
                      "查询契约", "不建持久缓存"):
            self.assertIn(token, text, "adapter-contract.md 缺少关键字段: %s" % token)

    def test_framework_index_has_two_level_selection_and_onboarding(self):
        text = _read(FRAMEWORK_INDEX)
        for token in ("运行时 × 组件源两级选型表", "新增框架接入流程",
                      "shadcn/ui", "Motif", "Astryx", "混用规则",
                      "adapter-contract.md"):
            self.assertIn(token, text, "framework/INDEX.md 缺少新选型层: %s" % token)
        self.assertNotIn("## 框架选型指南", text,
                         "旧单级「框架选型指南」节应已被两级选型表取代")

    def test_routing_has_recipe_section(self):
        text = _read(COMPONENT_ROUTING)
        for token in ("复合组件配方", "search-box", "配方 schema"):
            self.assertIn(token, text, "component-routing.md 缺少配方层: %s" % token)

    def test_glass_effect_has_degradation_section(self):
        text = _read(GLASS_EFFECT)
        self.assertIn("效果 → 组件参数退化", text, "glass-effect.md 缺少退化节")
        self.assertIn("adapter-contract.md", text, "退化节未链接适配器契约")

    def test_preview_md_documents_react_channel(self):
        text = _read(PREVIEW_MD)
        self.assertIn("React 通道", text, "preview.md 缺少 React 通道说明")
        self.assertIn("cdn.tailwindcss.com", text, "preview.md React 骨架缺 Tailwind CDN")


class TestE2eFrictionFixes(unittest.TestCase):
    """e2e-friction-fixes 变更守护:模板 colors 键前缀 + 账本 id 制式统一。"""

    TEMPLATE = os.path.join(BASE, "template", "DESIGN.md")
    ADAPTER = os.path.join(BASE, "references", "framework", "adapter-contract.md")
    DRAW_REACT = os.path.join(BASE, "references", "commands", "draw-react.md")

    def test_template_colors_leaf_keys_carry_category_prefix(self):
        text = _read(self.TEMPLATE)
        colors_block = text.split("colors:", 1)[1].split("typography:", 1)[0]
        for line in colors_block.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or ":" not in stripped:
                continue
            key = stripped.split(":", 1)[0].strip()
            self.assertTrue(
                key.startswith("color-"),
                "template colors 组 leaf 键应带 color- 前缀(token 名直出): {}".format(key),
            )

    def test_ledger_id_scheme_unified_to_provenance(self):
        for path in (self.ADAPTER, self.DRAW_REACT):
            text = _read(path)
            self.assertNotIn("D-<阶段>", text, "{} 残留自创账本 id 制式".format(path))
            self.assertIn("D-P<原则序号>-<决策序号>", text, "{} 缺 token-provenance 制式引用".format(path))


class TestP2DeferredBatch(unittest.TestCase):
    """p2-deferred-batch 变更守护:design-md.md 字号档指引在场。"""

    def test_design_md_has_minimal_font_ladder_guidance(self):
        text = _read(os.path.join(BASE, "references", "commands", "design-md.md"))
        self.assertIn(
            "≥18.66px", text,
            "design-md.md 缺 typography 最小档位指引(大文本 AA 3:1 合规空间)",
        )


class TestReactGenerationEntry(unittest.TestCase):
    """react-generation-entry 变更产物在场守护:删除 draw-react.md 或关键节即失败。"""

    def test_draw_react_exists_with_key_sections(self):
        text = _read(DRAW_REACT)
        for token in ("组件词典", "用户强制指定", "三级查询通道", "UNMEASURED",
                      "禁止事项", "复制粘贴型", "Astryx", "决策账本"):
            self.assertIn(token, text, "draw-react.md 缺少关键节: %s" % token)

    def test_skill_md_routes_draw_react_and_counts_14(self):
        text = _read(SKILL_MD)
        self.assertIn("draw-react.md", text, "SKILL.md 路由表缺 draw-react 行")
        self.assertNotIn("十三个子命令", text, "SKILL.md 仍有旧计数「十三个子命令」")
        self.assertIn("十四个子命令", text, "SKILL.md 缺「十四个子命令」计数")

    def test_readme_counts_14_subcommands(self):
        text = _read(README_MD)
        self.assertIn("14 个子命令", text, "README.md 缺「14 个子命令」计数")
        self.assertNotIn("13 个子命令", text, "README.md 仍有旧计数「13 个子命令」")
        self.assertIn("draw-react", text, "README.md 缺 draw-react 功能行")


if __name__ == "__main__":
    unittest.main()
