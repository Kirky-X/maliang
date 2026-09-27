"""文档-脚本计数一致性断言:防 preview-checklist 扩分区后脚本头注/输出计数再漂移。

背景:2026-09 吸收整合轮发现 preview-check.py 头注停留 49/113 而清单已扩至 135 项,
清单(600ms)与脚本(400ms)双门槛漂移同源——纯文案改动,无逻辑,故用纯文本断言守护。
49 为实测可脚本化覆盖数(脚本检查分组 §5.1-§5.13),由 preview-check.py 演进时同步维护。
"""

import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECKLIST = os.path.join(BASE, "references", "commands", "preview-checklist.md")
PREVIEW_MD = os.path.join(BASE, "references", "commands", "preview.md")
PC_SCRIPT = os.path.join(BASE, "scripts", "preview-check.py")

SCRIPTED = 49


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
        self.assertIn("49/%d 项" % total, script,
                      "preview-check.py 头注覆盖计数与清单总数漂移")
        self.assertIn("其余 %d 项" % runtime, script,
                      "preview-check.py 输出行运行时计数与清单总数漂移")
        self.assertNotIn("(MANUAL,见 5.13)", script,
                         "运行时项指针漂移:5.13 仅为 CWV 分区,运行时项分布见输出行新指针")

        preview = _read(PREVIEW_MD)
        self.assertIn("49 项由", preview, "preview.md 脚本化计数表述漂移")
        self.assertIn("其余 %d 项" % runtime, preview,
                      "preview.md 运行时计数与清单总数漂移")

    def test_checklist_uses_script_threshold_400ms(self):
        checklist = _read(CHECKLIST)
        self.assertNotIn("duration ≤ 600ms", checklist,
                         "入场时长口径须与脚本 400ms 硬门一致(分层长动效见 micro-interactions)")


if __name__ == "__main__":
    unittest.main()
