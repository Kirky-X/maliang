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


if __name__ == "__main__":
    unittest.main()
