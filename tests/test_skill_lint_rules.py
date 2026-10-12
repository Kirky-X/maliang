"""skill_lint.py 的 forbid-pattern / count-matches 两类新规则测试。

maliang 仓的 lint-checks.json 用这两类规则把公开计数对账钉在 INDEX 上
（check-claims.py 共享同一 schema）；本测试守护 vendored 副本的规则语义。
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load  # noqa: E402

sl = load("skill_lint.py")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestLintChecksRules(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        _write(self.repo / "INDEX.md",
               "# INDEX\n\n## 设计语言\n\n| id |\n| --- |\n| [a](a.md) |\n| [b](b.md) |\n\n## 其他\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _rules(self, checks):
        _write(self.repo / "lint-checks.json", json.dumps({"checks": checks}, ensure_ascii=False))
        return sl.check_repo_rules(self.repo)

    def test_count_matches_ok(self):
        # 不应报: 声明数 = 唯源表行数
        _write(self.repo / "SKILL.md", "共 2 种设计语言\n")
        fails, warns = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "INDEX.md",
            "section": "## 设计语言", "row_pattern": "^\\|\\s*\\[",
            "claim_files": ["SKILL.md"], "claim_patterns": ["(\\d+)\\s*种设计语言"],
        }])
        self.assertEqual(fails, [])
        self.assertEqual(warns, [])

    def test_count_matches_drift_fail(self):
        # 应报: 漂移按 severity=FAIL 进 fails(带行号)
        _write(self.repo / "SKILL.md", "共 3 种设计语言\n")
        fails, warns = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "INDEX.md",
            "section": "## 设计语言", "claim_files": ["SKILL.md"],
            "claim_patterns": ["(\\d+)\\s*种设计语言"],
        }])
        self.assertTrue(any("计数漂移" in f and "SKILL.md:1" in f for f in fails))
        self.assertEqual(warns, [])

    def test_count_matches_severity_warn(self):
        # 应报: severity=WARN 时漂移进 warns,不阻断
        _write(self.repo / "SKILL.md", "共 3 种设计语言\n")
        fails, warns = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "INDEX.md",
            "section": "## 设计语言", "claim_files": ["SKILL.md"],
            "claim_patterns": ["(\\d+)\\s*种设计语言"], "severity": "WARN",
        }])
        self.assertEqual(fails, [])
        self.assertTrue(any("计数漂移" in w for w in warns))

    def test_count_matches_vacuous(self):
        # 应报: 抓不到任何声明 = 规则形同虚设
        _write(self.repo / "SKILL.md", "模板墙见 INDEX\n")
        fails, _ = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "INDEX.md",
            "claim_files": ["SKILL.md"], "claim_patterns": ["(\\d+)\\s*种设计语言"],
        }])
        self.assertTrue(any("形同虚设" in f for f in fails))

    def test_count_matches_config_errors(self):
        # 应报: 配置错误必须显性化(缺唯源 / 正则无捕获组 / section 未命中)
        _write(self.repo / "SKILL.md", "共 2 种设计语言\n")
        fails, _ = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "GONE.md",
            "claim_files": ["SKILL.md"], "claim_patterns": ["(\\d+)"],
        }])
        self.assertTrue(any("目标文件不存在" in f for f in fails))
        _write(self.repo / "SKILL.md", "共 2 种设计语言\n")
        fails, _ = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "INDEX.md",
            "claim_files": ["SKILL.md"], "claim_patterns": ["\\d+"],
        }])
        self.assertTrue(any("捕获组" in f for f in fails))
        fails, _ = self._rules([{
            "name": "计数对账", "type": "count-matches", "source": "INDEX.md",
            "section": "## 不存在", "claim_files": ["SKILL.md"],
            "claim_patterns": ["(\\d+)"],
        }])
        self.assertTrue(any("section 未命中" in f for f in fails))

    def test_forbid_pattern_hits(self):
        # 应报: 命中禁用语(带行号);ignore 行豁免
        _write(self.repo / "SKILL.md", "禁止清单: 完美\n这是完美的方案\n")
        fails, _ = self._rules([{
            "name": "禁用语表", "type": "forbid-pattern", "files": ["SKILL.md"],
            "pattern": "完美", "ignore": "禁止清单",
        }])
        self.assertTrue(any("SKILL.md:2" in f for f in fails))
        self.assertFalse(any("SKILL.md:1" in f for f in fails))

    def test_forbid_pattern_clean(self):
        # 不应报: 无命中
        _write(self.repo / "SKILL.md", "干净文案\n")
        fails, warns = self._rules([{
            "name": "禁用语表", "type": "forbid-pattern", "files": ["SKILL.md"],
            "pattern": "完美|革命性",
        }])
        self.assertEqual((fails, warns), ([], []))

    def test_unknown_type_still_fails(self):
        # 应报: 未知 type 仍是配置 FAIL(新类型不放开未知键)
        _write(self.repo / "SKILL.md", "x\n")
        fails, _ = self._rules([{"name": "x", "type": "no-such-type"}])
        self.assertTrue(any("未知 type" in f for f in fails))

    def test_section_slice_helper(self):
        text = "# A\n\na\n\n## B\n\nb\n\n## C\n\nc\n"
        self.assertIn("b", sl.section_slice(text, "## B"))
        self.assertNotIn("c", sl.section_slice(text, "## B"))


if __name__ == "__main__":
    unittest.main()
