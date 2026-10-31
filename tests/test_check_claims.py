"""check-claims.py 公开声明对账测试。

覆盖验收标准(R-ei-003):「12 种设计语言」式计数漂移能报出(含行号),
修复后通过;并覆盖禁用语表、必现短语、min_claims 防白检与退出码三态。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _load import load, write  # noqa: E402

cc = load("audit.py")




INDEX = """# INDEX

## 设计语言（design-language）

| id | 中文名 |
| --- | --- |
| [a](a.md) | 甲 |
| [b](b.md) | 乙 |

## 整页模式
"""


class TestCheckClaims(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        write(self.root / "references" / "templates" / "INDEX.md", INDEX)
        self.config = {
            "checks": [{
                "name": "设计语言计数对账",
                "type": "count-matches",
                "source": "references/templates/INDEX.md",
                "section": "## 设计语言",
                "row_pattern": "^\\|\\s*\\[",
                "claim_files": ["SKILL.md"],
                "claim_patterns": ["(\\d+)\\s*种设计语言"],
                "severity": "WARN",
            }],
        }
        write(self.root / "SKILL.md", "共 2 种设计语言。\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _write_config(self, extra_checks=None):
        cfg = {"checks": list(self.config["checks"]) + list(extra_checks or [])}
        write(self.root / "lint-checks.json", json.dumps(cfg, ensure_ascii=False))

    def test_matching_count_passes(self):
        # 不应报: 声明数与 INDEX 表行数一致
        self._write_config()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("一致", out.getvalue())

    def test_drift_reported_with_line(self):
        # 应报: 声称 12 vs 唯源 14;WARN 级不改变退出码
        write(self.root / "SKILL.md", "共 12 种设计语言。\n")
        self._write_config()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertIn("SKILL.md:1", text)
        self.assertIn("声称 12", text)
        self.assertIn("是 2", text)

    def test_drift_strict_upgrades_to_error(self):
        # --strict: 全部发现升级 error → exit 1
        write(self.root / "SKILL.md", "共 12 种设计语言。\n")
        self._write_config()
        with contextlib.redirect_stdout(io.StringIO()):
            code = cc._main_claims([str(self.root), "--strict"])
        self.assertEqual(code, 1)

    def test_min_claims_vacuity_reported(self):
        # 应报: 声明全被删掉后规则形同虚设(防"改掉措辞就静默失效")
        write(self.root / "SKILL.md", "模板墙见 INDEX。\n")
        self._write_config()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("形同虚设", out.getvalue())

    def test_forbid_pattern_hit_is_error(self):
        # 应报: 禁用语命中 → FAIL 级 → exit 1
        self._write_config([{
            "name": "禁用语表", "type": "forbid-pattern",
            "files": ["SKILL.md"], "pattern": "完美|革命性",
        }])
        write(self.root / "SKILL.md", "这是一个完美的方案。\n")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("禁用表述", out.getvalue())

    def test_forbid_pattern_ignore_line(self):
        # 不应报: ignore 正则豁免的行(counted-claim 表里列举禁用词本身)
        write(self.root / "lint-checks.json", json.dumps({"checks": [{
            "name": "禁用语表", "type": "forbid-pattern",
            "files": ["SKILL.md"], "pattern": "完美", "ignore": "禁止清单",
        }]}, ensure_ascii=False))
        write(self.root / "SKILL.md", "禁止清单: 完美/革命性\n")
        with contextlib.redirect_stdout(io.StringIO()):
            code = cc._main_claims([str(self.root), "--strict"])
        self.assertEqual(code, 0)

    def test_require_pattern_phrase(self):
        # 应报: 必现短语缺失 → exit 1
        self._write_config([{
            "name": "依赖声明", "type": "require-pattern",
            "file": "SKILL.md", "pattern": "纯 Python 标准库",
        }])
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("必现短语未满足", out.getvalue())

    def test_missing_config_exit_2(self):
        # 没能检查: 没有 lint-checks.json
        with contextlib.redirect_stderr(io.StringIO()):
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 2)

    def test_missing_source_exit_2(self):
        # 没能检查: 规则指向的唯源文件不存在(不得静默算过)
        self.config["checks"][0]["source"] = "references/templates/GONE.md"
        self._write_config()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 2)

    def test_no_handled_rules_exit_2(self):
        # 没能检查: 配置里没有可执行的声明规则
        write(self.root / "lint-checks.json", json.dumps({"checks": [
            {"name": "x", "type": "file-header", "dirs": ["references"], "fields": ["来源"]}]}))
        with contextlib.redirect_stderr(io.StringIO()):
            code = cc._main_claims([str(self.root)])
        self.assertEqual(code, 2)

    def test_json_output_shape(self):
        write(self.root / "SKILL.md", "共 12 种设计语言。\n")
        self._write_config()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cc._main_claims([str(self.root), "--format", "json"])
        self.assertEqual(code, 0)
        data = json.loads(out.getvalue())
        self.assertEqual(data["summary"]["warn"], 1)
        self.assertEqual(data["findings"][0]["file"], "SKILL.md")


if __name__ == "__main__":
    unittest._main_claims()
