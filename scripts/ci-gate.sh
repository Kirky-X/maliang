#!/usr/bin/env bash
# maliang CI 验证门 —— 文档/产物规范 + 脚本回归一键检查
#
# 用法: bash scripts/ci-gate.sh   (在仓库根目录执行;CI 与本地同一入口)
#
# 门禁语义(对齐各验证脚本退出码约定):
#   - 退出码 0(全过)与 2(仅 warning)放行;
#   - 退出码 1(有 error)拦截;
#   - 单元测试必须全绿(非 0 即拦截)。
# 覆盖:
#   1. tests/ fixture 单元测试(validate-draw-md / preview-check / ui-graph / 共用模块)
#   2. validate-draw-md.py  — draw-md 产物 13 项检查(目标: examples/ui-markdown/)
#   3. validate-framework.py — framework 组件文档检查(目标: references/framework/)
#   4. ui-graph.py check-nav — 导航关系图冒烟(缺页为 informational,不拦截)
#   5. preview-check.py     — 若 examples/preview/ 存在则跑 Pre-Flight 自动化检查

set -u
cd "$(dirname "$0")/.." || exit 1

FAIL=0

gate() {
  local name="$1"; shift
  echo ""
  echo "==> ${name}"
  "$@"
  local rc=$?
  if [ "${rc}" -eq 1 ]; then
    echo "[GATE] ✗ ${name} — 存在 error 级发现(退出码 1)"
    FAIL=1
  elif [ "${rc}" -ne 0 ]; then
    echo "[GATE] △ ${name} — 通过(仅 warning,退出码 ${rc})"
  else
    echo "[GATE] ✓ ${name}"
  fi
  return 0
}

echo "maliang CI 验证门"
echo "================="

# 1. 单元测试(必须全绿)
echo ""
echo "==> 单元测试(tests/)"
python3 -m unittest discover -s tests
if [ $? -ne 0 ]; then
  echo "[GATE] ✗ 单元测试失败"
  FAIL=1
else
  echo "[GATE] ✓ 单元测试"
fi

# 2-4. 文档与产物验证(error 拦截,warning 放行)
gate "validate-draw-md(draw-md 产物检查)" \
  python3 scripts/validate-draw-md.py examples/ui-markdown/
gate "validate-framework(framework 组件文档检查)" \
  python3 scripts/validate-framework.py
gate "ui-graph check-nav(导航关系冒烟)" \
  python3 scripts/ui-graph.py check-nav

# 5. preview Pre-Flight(目录存在时)
if [ -d examples/preview ]; then
  gate "preview-check(Pre-Flight 自动化检查)" \
    python3 scripts/preview-check.py examples/preview/
else
  echo ""
  echo "==> preview-check(跳过: examples/preview/ 不存在)"
fi

echo ""
echo "================="
if [ "${FAIL}" -ne 0 ]; then
  echo "结果: FAIL(存在 error 级发现,见上方 [GATE] ✗ 条目)"
  exit 1
fi
echo "结果: PASS"
exit 0
