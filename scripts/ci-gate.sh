#!/usr/bin/env bash
# maliang CI 验证门 —— 文档/产物规范 + 脚本回归一键检查
#
# 用法: bash scripts/ci-gate.sh   (在仓库根目录执行;CI 与本地同一入口)
#
# 判定表(对齐 scripts/EXIT-CODES.md 三态;「warning 放行」与「未测量拦截」拆分):
#   退出码 0                  → 放行(看过了,没问题;warning 提示不改变退出码)
#   退出码 1                  → 拦截(看过了,有 error 级发现)
#   退出码 2(三态)           → 拦截(没能检查:路径不存在/无目标/没装浏览器)
#                               —— Nothing was measured. This is not a pass。
#   退出码 2(迁移中脚本)     → warning 放行,且输出须自证 0 errors;
#                               仅限 EXIT-CODES.md「与旧口径的对照」表登记的
#                               未迁移脚本(validate-draw-md.py / validate-framework.py),
#                               迁移切换后本门必须改回 strict。
#   退出码 1(advisory 门)    → 报告放行(不拦截):仅限下方「advisory 登记」列出的
#                               目标——其发现是本批门禁上线前既存的历史债,清账后
#                               改回 strict;退出码 2 在 advisory 档仍拦截。
#   其他退出码                → 拦截(异常退出)
#
# advisory 登记(2026-10-12,本批接线时实测既存发现):
#   - validate-design-md.py @ examples/design-system/DESIGN.md — 29 处 V2 孤儿 token
#     (示例 DESIGN.md 早于 token 溯源契约);清账方式:补 # no-decision:/决策 id。
#   - validate-generated.py @ examples/element-plus/ — Home.vue 8 处颜色字面量(G04);
#     清账方式:回 design-md 补 token 或改用已登记值。
#   两处清账后把本文件的 gate_if_script 调用改回 strict(去掉 --advisory)。
#
# 分层接线原则(design.md Decision 4):ci-gate 只接**无浏览器可跑**的脚本;
# 浏览器依赖门(verify-states.py / verify-interactive.py)不进 CI 默认路径,
# 本地单独运行,无浏览器时它们自报 UNMEASURED / 退出码 2,不得记为通过。
#
# 覆盖:
#   1. tests/ fixture 单元测试
#   2. validate-draw-md.py  — draw-md 产物 15 项检查(目标: examples/ui-markdown/)
#   3. validate-framework.py — framework 组件文档检查(目标: references/framework/)
#   4. ui-graph.py check-nav — 导航关系图冒烟(缺页为 informational,不拦截)
#   5. preview-check.py     — 若 examples/preview/ 存在则跑 Pre-Flight 自动化检查
#   6. check-claims.py      — 公开声明对账(计数唯一来源 / 必现短语 / 禁用语表)
#   7. evidence-check.py    — 若 examples/ 下有取证 report.json 则跑齐套校验
#   8. validate-design-md.py / validate-generated.py — 交付后自动接入(存在即跑)
#   9. ledger.py verify     — 项目反馈账本存在时校验
#  10. 浏览器依赖门清单      — 不运行,只打印手动入口与「未测量不得记为通过」口径

set -u
cd "$(dirname "$0")/.." || exit 1

FAIL=0
GATE_LOG_DIR="$(mktemp -d)"
trap 'rm -rf "${GATE_LOG_DIR}"' EXIT

# gate [--warn-pass|--advisory] <名称> <命令...>
#   --warn-pass: EXIT-CODES.md 登记的迁移中脚本专用(2=仅 warning 时放行,
#                但必须输出自证 0 errors;其余非 0 一律拦截)
#   --advisory:  历史债登记门(1=报告放行,不拦截;2=未能检查仍拦截)
gate() {
  local mode="strict"
  if [ "${1:-}" = "--warn-pass" ]; then
    mode="warn-pass"
    shift
  elif [ "${1:-}" = "--advisory" ]; then
    mode="advisory"
    shift
  fi
  local name="$1"
  shift
  echo ""
  echo "==> ${name}"
  local log="${GATE_LOG_DIR}/$(echo "${name}" | tr -c '[:alnum:]' '_').log"
  "$@" 2>&1 | tee "${log}"
  local rc=${PIPESTATUS[0]}
  if [ "${mode}" = "advisory" ]; then
    if [ "${rc}" -eq 0 ]; then
      echo "[GATE] ✓ ${name}"
    elif [ "${rc}" -eq 1 ]; then
      local advisory_n advisory_max
      advisory_n="$(sed -n 's/.*检查结果: \([0-9][0-9]*\) errors.*/\1/p' "${log}" | tail -1)"
      advisory_max="${ADVISORY_MAX:-}"
      if [ -n "${advisory_max}" ] && [ -n "${advisory_n}" ] && [ "${advisory_n}" -gt "${advisory_max}" ]; then
        echo "[GATE] ✗ ${name} — advisory 发现数 ${advisory_n} 超过登记基线 ${advisory_max}(疑似新回归,拦截;清账后改回 strict)"; FAIL=1
      else
        echo "[GATE] △ ${name} — 报告放行(advisory:发现数 ${advisory_n:-?} 未超登记基线 ${advisory_max:-?},均为门禁上线前既存历史债;清账后改回 strict)"
      fi
    elif [ "${rc}" -eq 2 ]; then
      echo "[GATE] ✗ ${name} — 没能检查(退出码 2/UNMEASURED);未测量不得记为通过"
      FAIL=1
    else
      echo "[GATE] ✗ ${name} — 异常退出码 ${rc}"
      FAIL=1
    fi
    return 0
  fi
  if [ "${mode}" = "warn-pass" ]; then
    if [ "${rc}" -eq 1 ]; then
      echo "[GATE] ✗ ${name} — 存在 error 级发现(退出码 1)"
      FAIL=1
    elif [ "${rc}" -eq 2 ] && grep -qE "([^0-9]|^)0 errors" "${log}"; then
      echo "[GATE] △ ${name} — warning 放行(迁移中:2=仅 warning 且 0 errors;不代表通过)"
    elif [ "${rc}" -ne 0 ]; then
      echo "[GATE] ✗ ${name} — 退出码 ${rc},且未能自证仅 warning → 按没能检查拦截"
      FAIL=1
    else
      echo "[GATE] ✓ ${name}"
    fi
    return 0
  fi
  if [ "${rc}" -eq 0 ]; then
    echo "[GATE] ✓ ${name}"
  elif [ "${rc}" -eq 1 ]; then
    echo "[GATE] ✗ ${name} — 存在 error 级发现(退出码 1)"
    FAIL=1
  elif [ "${rc}" -eq 2 ]; then
    echo "[GATE] ✗ ${name} — 没能检查(退出码 2/UNMEASURED);未测量不得记为通过"
    FAIL=1
  else
    echo "[GATE] ✗ ${name} — 异常退出码 ${rc}"
    FAIL=1
  fi
  return 0
}

# 脚本未交付时的显式登记(不静默跳过)
skip_note() {
  echo ""
  echo "==> $1"
  echo "[GATE] － 跳过:$2"
}

# 交付即接入:脚本存在就跑,不存在打印待接入登记
# 用法: gate_if_script <脚本路径> <gate 模式旗标...> <名称> <命令...>
gate_if_script() {
  local script="$1"
  shift
  local mode=""
  if [ "${1:-}" = "--advisory" ] || [ "${1:-}" = "--warn-pass" ]; then
    mode="$1"
    shift
  fi
  if [ -f "${script}" ]; then
    if [ -n "${mode}" ]; then
      gate "${mode}" "$@"
    else
      gate "$@"
    fi
  else
    skip_note "$1" "${script} 未交付(登记为待接入,交付后自动生效)"
  fi
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

# 2-3. 文档与产物验证(迁移中脚本:EXIT-CODES.md 对照表登记的 2=仅 warning)
# 前置:目标 0 文件时不得记为通过(未测量不通过;占位在墙角,不是绿)
if find examples/ui-markdown -name '*.md' -print -quit 2>/dev/null | grep -q .; then
  gate --warn-pass "validate-draw-md(draw-md 产物检查;迁移中)" \
    python3 scripts/validate-draw-md.py examples/ui-markdown/
else
  echo "[GATE] ✗ validate-draw-md — 目标目录 0 个 .md 文件(未测量不得记为通过)"; FAIL=1
fi
if find references/framework -name '*.md' -print -quit 2>/dev/null | grep -q .; then
  gate --warn-pass "validate-framework(framework 组件文档检查;迁移中)" \
    python3 scripts/validate-framework.py
else
  echo "[GATE] ✗ validate-framework — references/framework 下 0 个 .md(未测量不得记为通过)"; FAIL=1
fi

# 4. 导航冒烟(ui-graph 缺目标为 1;三态下按 strict 处理)
gate "ui-graph check-nav(导航关系冒烟)" \
  python3 scripts/ui-graph.py check-nav

# 5. preview Pre-Flight(目录存在时;已迁移三态:2=无目标 → 拦截)
if [ -d examples/preview ]; then
  gate "preview-check(Pre-Flight 自动化检查)" \
    python3 scripts/preview-check.py examples/preview/
else
  skip_note "preview-check" "examples/preview/ 不存在"
fi

# 6. 公开声明对账(无浏览器;计数唯一来源 + 必现短语 + 禁用语表)
gate "check-claims(公开声明对账)" \
  python3 scripts/check-claims.py .

# 7. 取证齐套(本轮真的取过证时才跑;无 report.json = 本轮无取证,不是通过也不是失败)
if find examples -name report.json -print -quit 2>/dev/null | grep -q .; then
  gate "evidence-check(取证齐套)" \
    python3 scripts/evidence-check.py examples/
else
  skip_note "evidence-check" "examples/ 下没有 report.json(本轮未取证)"
fi

# 8. A1 侧无浏览器脚本:交付即接入(目标以各自 --help 为准)
#    advisory 原因与清账方式见头部「advisory 登记」;清账后改回 strict。
ADVISORY_MAX=29 gate_if_script scripts/validate-design-md.py --advisory "validate-design-md(DESIGN.md 溯源交叉检查;advisory:历史债登记,基线 29)" \
  python3 scripts/validate-design-md.py examples/design-system/DESIGN.md
ADVISORY_MAX=8 gate_if_script scripts/validate-generated.py --advisory "validate-generated(生成码机械校验;advisory:历史债登记,基线 8)" \
  python3 scripts/validate-generated.py examples/element-plus/

# 9. 项目反馈账本(存在才校验;账本是项目级 .maliang/feedback/ 状态,不存在即未启用)
if [ -f .maliang/feedback/decisions.jsonl ]; then
  gate "ledger verify(反馈账本校验)" python3 scripts/ledger.py verify
else
  skip_note "ledger verify" "本项目未启用 .maliang/feedback/(账本为空,未测量)"
fi

# 10. 浏览器依赖门(design 口径:不进 CI 默认路径;无浏览器时不得记为通过)
echo ""
echo "==> 浏览器依赖门(不在 CI 内运行)"
echo "    python3 scripts/verify-states.py examples/preview/        # 三态对比度实测"
echo "    python3 scripts/verify-interactive.py examples/preview/   # 交互真实性实测"
echo "    无浏览器时两脚本自报 UNMEASURED / 退出码 2 —— 未测量不得记为通过。"

echo ""
echo "================="
if [ "${FAIL}" -ne 0 ]; then
  echo "结果: FAIL(见上方 [GATE] ✗ 条目;警告放行条目以 △ 标注)"
  exit 1
fi
echo "结果: PASS"
exit 0
