#!/usr/bin/env python3
"""stage-audit —— 段级汇总审计(「必须有结果才能到下一阶段」的机械形态)。

用法:
    python3 scripts/stage-audit.py --list                     # 七段审计表
    python3 scripts/stage-audit.py --stage 3                  # 审计段3(设计)
    python3 scripts/stage-audit.py --stage 3 --root <项目根>   # 默认当前目录
    python3 scripts/stage-audit.py --all                      # 逐段审计(链条顺序)
    python3 scripts/stage-audit.py --stage 1 --skip-gates     # 只查产物面,不跑门禁

每段审计两步:
    1. **产物存在性**——该段必备结果(路径按 workspace-layout.md canonical:design/ 下;
       存量项目旧路径 examples/ 兼容识别)。缺任一必备产物 = 该段没有结果,不得进下一段。
    2. **段门禁**——该段可无头运行的确定性脚本;跑前 receipts init 绑定产物+脚本哈希,
       跑后 attach 登记报告与退出码,末尾 verify 三态(收据编排,对齐 receipts 机制)。

段1(研究)无既有脚本,内置存在性检查:DESIGN.md + YAML frontmatter + `users:` 块
(用户三产出的 schema 落点,spec-schema.md);无用户研究时须有显式降级声明
(「未做用户研究」)。四产出质量与自检问题属人工判据,不在机械层。

无机械审计面的段:段6(交付)判定在 preview-checklist 唯一 canonical 清单 + 编号门禁
(两处都过才算过),本工具显式标注「无机械审计面」并计入 exit 2(没能检查),
--all 汇总时该段不拖垮其余段,单列显示。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
    0 = 产物齐且门禁全过(--skip-gates 时 0 仅覆盖产物面,不满足进段条件)
    1 = 任一必备产物缺失,或任一门禁退出码 1
    2 = 项目根不存在/用法错误/门禁自身没能跑(退出码 2 或异常码)
收据写不出按未记录处理(显性报错,不静默当成功)。
依赖: Python 3 标准库(无第三方依赖)。
"""

import argparse
import glob as _glob
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import receipts  # noqa: E402  同目录收据机制,收据编排的唯一实现

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

DEGRADED_NO_RESEARCH = "未做用户研究"
_RUN_SEQ = 0

# 门禁输出落盘上限:报告由产物内容驱动,巨量 findings 不得无界放大父进程内存/磁盘
_REPORT_OUTPUT_CAP = 1_000_000
# 不可信项目场景:收据/报告路径若被预置为符号链接,拒绝跟随(防写出项目树外)
_LINK_ERR = "路径是符号链接,拒绝跟随(不可信项目防护): %s"


def _symlink_guard(*paths):
    for p in paths:
        if p and os.path.islink(p):
            raise OSError(_LINK_ERR % p)


# ---------------------------------------------------------------------------
# 段表:artifacts 为 (标签, 判定函数) 列表;gates 为 (门禁名, 命令构造器) 列表
# ---------------------------------------------------------------------------

def _spec_dir(root):
    """页面规格目录:canonical design/ui-markdown,存量项目旧路径 examples/ui-markdown。"""
    for rel in ("design/ui-markdown", "examples/ui-markdown"):
        p = os.path.join(root, rel)
        if os.path.isdir(p):
            return p, rel
    return None, None


def _preview_dir(root):
    for rel in ("design/preview", "examples/preview"):
        p = os.path.join(root, rel)
        if os.path.isdir(p):
            return p, rel
    return None, None


def _file_exists(path):
    return os.path.isfile(path)


def _dir_has_preview(root):
    d, _ = _preview_dir(root)
    if not d:
        return False
    return bool(_glob.glob(os.path.join(d, "preview_*.html")))


def _gate_validate_design_md(root):
    design = os.path.join(root, "DESIGN.md")
    return [sys.executable, os.path.join(SCRIPT_DIR, "design-md.py"), "validate", design]


def _gate_validate_draw_md(root):
    spec, _ = _spec_dir(root)
    return [
        sys.executable, os.path.join(SCRIPT_DIR, "validate.py"), "draw-md", spec,
        "--framework-file", os.path.join(SKILL_DIR, "references", "framework", "index.md"),
        "--vocabulary-dir", os.path.join(SKILL_DIR, "references", "vocabulary"),
    ]


def _gate_preview_check(root):
    d, _ = _preview_dir(root)
    return [sys.executable, os.path.join(SCRIPT_DIR, "preview-check.py"), d]


STAGES = {
    1: {
        "name": "研究",
        "target": "DESIGN.md + users: 块(或显式降级声明);四产出质量属人工判据",
        "artifacts": None,  # 内置 stage1 检查(见 check_stage1)
        "gates": [],
    },
    2: {
        "name": "定义",
        "target": "DESIGN.md(决策账本/token 溯源)",
        "artifacts": [("DESIGN.md", lambda root: _file_exists(os.path.join(root, "DESIGN.md")))],
        "gates": [("validate-design-md", _gate_validate_design_md)],
    },
    3: {
        "name": "设计",
        "target": "design/ui-markdown/ 页面规格(token.md 必备)",
        "artifacts": [("token.md(页面规格层)", lambda root: _file_exists(
            os.path.join(_spec_dir(root)[0] or root, "token.md")) if _spec_dir(root)[0] else False)],
        "gates": [("validate-draw-md", _gate_validate_draw_md)],
    },
    4: {
        "name": "实现",
        "target": "ui-implementation-map.json(实现映射);完整性判定走 ui-graph list-unimplemented",
        "artifacts": [("ui-implementation-map.json", lambda root: _file_exists(
            os.path.join(_spec_dir(root)[0] or root, "ui-implementation-map.json")) if _spec_dir(root)[0] else False)],
        "gates": [],
    },
    5: {
        "name": "验证",
        "target": "design/preview/ 下 preview_*.html",
        "artifacts": [("preview_*.html(预览产物)", _dir_has_preview)],
        "gates": [("preview-check", _gate_preview_check)],
    },
    6: {
        "name": "交付",
        "target": "无机械审计面:preview-checklist(唯一 canonical)+ 编号门禁,两处都过",
        "artifacts": None,
        "gates": [],
        "no_machine_face": True,
    },
    7: {
        "name": "迭代",
        "target": "ui-hash-state.json(哈希基线,decisions 回写属 DESIGN.md 人工层)",
        "artifacts": [("ui-hash-state.json(哈希基线)", lambda root: _file_exists(
            os.path.join(_spec_dir(root)[0] or root, "ui-hash-state.json")) if _spec_dir(root)[0] else False)],
        "gates": [],
    },
}


# ---------------------------------------------------------------------------
# 段1 内置存在性检查
# ---------------------------------------------------------------------------

_FM_OPEN_RE = re.compile(r"^---\s*$")


def check_stage1(root):
    """段1(研究)产物检查,返回缺失/问题清单(空 = 过)。"""
    problems = []
    path = os.path.join(root, "DESIGN.md")
    if not os.path.isfile(path):
        return ["DESIGN.md 不存在(段1·2 无结果,全链路 CHECKPOINT 禁止跳段)"]
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return ["DESIGN.md 读取失败: %s" % exc]
    lines = text.splitlines()
    if not lines or not _FM_OPEN_RE.match(lines[0]):
        problems.append("DESIGN.md 缺 YAML frontmatter(首行须为 ---)")
        return problems
    fm_end = None
    for i in range(1, min(len(lines), 200)):
        if _FM_OPEN_RE.match(lines[i]):
            fm_end = i
            break
    if fm_end is None:
        problems.append("DESIGN.md frontmatter 未闭合(200 行内无结束 ---)")
        return problems
    frontmatter = "\n".join(lines[1:fm_end])
    if not re.search(r"^users\s*:", frontmatter, re.MULTILINE) and DEGRADED_NO_RESEARCH not in text:
        problems.append(
            "用户三产出缺失:frontmatter 无 users: 块,全文亦未见「%s」降级声明"
            "(design-md 0a 用户三产出/spec-schema users 块)" % DEGRADED_NO_RESEARCH)
    return problems


# ---------------------------------------------------------------------------
# 收据编排:init(跑门禁前)→ 跑门禁 → attach → verify
# ---------------------------------------------------------------------------

def _receipts_for_stage(root, stage_no, artifact_paths, gate_script_paths):
    """返回 (session, run_id) 或 (None, None);init 失败显性提示并按未记录处理。"""
    bind_artifacts = [p for p in artifact_paths if os.path.isfile(p)]
    bind_scripts = [p for p in gate_script_paths if os.path.isfile(p)]
    if not bind_artifacts and not bind_scripts:
        return None, None
    session = receipts.session_id(None)
    # 收据 init 不可覆盖:同毫秒内重复审计须换 run id,追加全局序号
    global _RUN_SEQ
    _RUN_SEQ += 1
    run_id = "stage%d-%d-%d" % (stage_no, int(time.time() * 1000), _RUN_SEQ)
    try:
        receipts.init_run(root, session, run_id, bind_artifacts, bind_scripts,
                          note="stage-audit 段%d(%s)" % (stage_no, STAGES[stage_no]["name"]))
    except (ValueError, OSError) as exc:
        print("stage-audit: 收据 init 未记录(%s);本次审计按无收据继续" % exc, file=sys.stderr)
        return None, None
    return session, run_id


def _attach_gate(root, session, run_id, gate_name, exit_code, report_path):
    if session is None:
        return
    try:
        receipts.attach_report(root, session, run_id, report_path, gate_name, exit_code, [])
    except (ValueError, OSError) as exc:
        print("stage-audit: 收据 attach 未记录(%s)" % exc, file=sys.stderr)


def _verify_receipt(root, session, run_id):
    if session is None:
        return None
    try:
        return receipts.verify_run(root, session, run_id)
    except (ValueError, OSError) as exc:
        print("stage-audit: 收据 verify 失败(%s)" % exc, file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# 段审计主体
# ---------------------------------------------------------------------------

def audit_stage(stage_no, root, run_gates=True, gates_override=None):
    """审计单段,返回 (exit_code, result_dict)。exit 三态见模块 docstring。"""
    stage = STAGES.get(stage_no)
    if stage is None:
        return 2, {"error": "未知段号 %r(1-7)" % stage_no}

    result = {"stage": stage_no, "name": stage["name"], "target": stage["target"],
              "missing": [], "gates": [], "receipt": None, "notes": []}

    if stage.get("no_machine_face"):
        result["notes"].append(
            "无机械审计面:判定在 preview-checklist(唯一 canonical 清单)+ 编号门禁,"
            "两处都过才算过(numbered-gates §0);本段计入没能检查(2),不构成通过")
        return 2, result

    # 1) 产物存在性(artifact_paths = 本段实际判定依据的产物,供收据绑定)
    artifact_paths = []
    if stage_no == 1:
        result["missing"].extend(check_stage1(root))
        artifact_paths = [os.path.join(root, "DESIGN.md")]
    else:
        for label, predicate in stage["artifacts"]:
            if not predicate(root):
                result["missing"].append(label)
        spec, rel = _spec_dir(root)
        if spec:
            result["notes"].append("规格目录:%s(%s)" % (
                rel, "canonical" if rel.startswith("design/") else "存量旧路径,建议迁移见 workspace-layout.md"))
            binding = {3: "token.md", 4: "ui-implementation-map.json",
                       7: "ui-hash-state.json"}.get(stage_no)
            if binding:
                artifact_paths.append(os.path.join(spec, binding))
        if stage_no == 5:
            d, rel = _preview_dir(root)
            if d:
                result["notes"].append("预览目录:%s(%s)" % (
                    rel, "canonical" if rel.startswith("design/") else "存量旧路径,建议迁移见 workspace-layout.md"))
                artifact_paths.extend(_glob.glob(os.path.join(d, "preview_*.html")))
        if stage_no == 2:
            artifact_paths = [os.path.join(root, "DESIGN.md")]

    if result["missing"]:
        return 1, result

    # 2) 段门禁(收据编排:init 于跑门禁之前)
    gates = gates_override if gates_override is not None else stage["gates"]
    if not run_gates or not gates:
        if gates and not run_gates:
            result["notes"].append("--skip-gates:仅产物面,门禁未跑(不代表通过)")
        session, run_id = _receipts_for_stage(root, stage_no, artifact_paths, [])
        receipt = _verify_receipt(root, session, run_id)
        if receipt:
            result["receipt"] = {"run": run_id, "state": receipt["state"]}
        return 0, result

    gate_cmds = [(name, builder(root)) for name, builder in gates]
    session, run_id = _receipts_for_stage(
        root, stage_no, artifact_paths, [cmd[1] for _name, cmd in gate_cmds])
    if session is None and (artifact_paths or gate_cmds):
        result["notes"].append("收据未记录(无可绑定对象或写入失败,详见 stderr);审计结果无收据背书")

    reports_dir = os.path.join(root, ".maliang", "receipts", "reports")
    worst = 0
    for name, cmd in gate_cmds:
        try:
            os.makedirs(reports_dir, exist_ok=True)
            _symlink_guard(
                os.path.join(root, ".maliang"),
                os.path.join(root, ".maliang", "receipts"),
                reports_dir,
            )
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            code = proc.returncode
            output = (proc.stdout or "") + (proc.stderr or "")
            if len(output) > _REPORT_OUTPUT_CAP:
                output = output[:_REPORT_OUTPUT_CAP] + "\n...[输出超 %d 字符,已截断]" % _REPORT_OUTPUT_CAP
        except (OSError, subprocess.TimeoutExpired) as exc:
            result["gates"].append({"gate": name, "exit": None, "note": "没能跑:%s" % exc})
            worst = 2
            continue
        report_path = os.path.join(reports_dir, "%s-%s.txt" % (run_id or "stage%d" % stage_no, name))
        try:
            _symlink_guard(report_path)
            with open(report_path, "w", encoding="utf-8") as fh:
                fh.write(output)
        except OSError as exc:
            print("stage-audit: 门禁报告写不出(%s);attach 按未记录处理" % exc, file=sys.stderr)
            report_path = None
        if report_path:
            _attach_gate(root, session, run_id, name, code, report_path)
        result["gates"].append({"gate": name, "exit": code})
        if code == 1:
            worst = 1
        elif code != 0 and worst != 1:
            worst = 2

    receipt = _verify_receipt(root, session, run_id)
    if receipt:
        result["receipt"] = {"run": run_id, "state": receipt["state"],
                             "stale": receipt.get("stale", [])}
    return worst, result


def audit_all(root, run_gates=True):
    """逐段审计;exit = 有机械面各段的最差值(1 > 2 > 0;段6 单列,不计入)。"""
    worst = 0
    results = []
    for n in sorted(STAGES):
        code, res = audit_stage(n, root, run_gates=run_gates)
        results.append(res)
        if STAGES[n].get("no_machine_face"):
            continue
        if code == 1:
            worst = 1
        elif code == 2 and worst != 1:
            worst = 2
    return worst, results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_result(res):
    print("段%d %s —— %s" % (res["stage"], res["name"], res["target"]))
    for m in res.get("missing", []):
        print("  ✗ 缺产物:%s" % m)
    for g in res.get("gates", []):
        if g.get("exit") is None:
            print("  ✗ 门禁 %s:%s" % (g["gate"], g.get("note", "")))
        else:
            mark = "✓" if g["exit"] == 0 else "✗"
            print("  %s 门禁 %s 退出码 %d" % (mark, g["gate"], g["exit"]))
    r = res.get("receipt")
    if r:
        print("  · 收据 run=%s state=%s" % (r.get("run"), r.get("state")))
        for why in r.get("stale", []):
            print("    %s" % why)
    for note in res.get("notes", []):
        print("  · %s" % note)
    if res.get("error"):
        print("  ✗ %s" % res["error"])


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="stage-audit.py",
        description="段级汇总审计:产物存在性 + 段门禁 + 测量收据(init→attach→verify),三态退出")
    parser.add_argument("--stage", type=int, default=None, help="审计单段(1-7)")
    parser.add_argument("--all", action="store_true", help="逐段审计(链条顺序)")
    parser.add_argument("--list", action="store_true", help="打印七段审计表")
    parser.add_argument("--root", default=".", help="项目根(默认当前目录)")
    parser.add_argument("--skip-gates", action="store_true", help="只查产物面,不跑门禁(不代表通过)")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args(argv)

    if args.list:
        for n in sorted(STAGES):
            s = STAGES[n]
            face = "无机械审计面" if s.get("no_machine_face") else (
                "内置检查" if n == 1 else "%d 产物 + %d 门禁" % (len(s["artifacts"]), len(s["gates"])))
            print("段%d %-4s | %s | %s" % (n, s["name"], face, s["target"]))
        return 0

    if not args.stage and not args.all:
        parser.error("需要 --stage N 或 --all(或 --list 查看段表)")
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("stage-audit: 项目根不存在: %s" % root, file=sys.stderr)
        return 2

    if args.all:
        code, results = audit_all(root, run_gates=not args.skip_gates)
        if args.json:
            print(json.dumps({"exit": code, "stages": results}, ensure_ascii=False, indent=2))
        else:
            for res in results:
                _print_result(res)
                print("")
        print("汇总退出码: %d(%s)" % (code, {0: "机械面全过(段6 无机械面,单列)", 1: "有问题", 2: "没能检查"}.get(code, str(code))))
        return code

    code, res = audit_stage(args.stage, root, run_gates=not args.skip_gates)
    if args.json:
        print(json.dumps({"exit": code, "stage": res}, ensure_ascii=False, indent=2))
    else:
        _print_result(res)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
