#!/usr/bin/env python3
"""ledger —— 反馈→规则状态机账本（项目级 `.maliang/feedback/`，append-only JSONL）。

把真实反馈、可复现缺陷与验证结果，转成下一次任务能执行、能检查、能回滚的规则。
账本放在**项目级** `<root>/.maliang/feedback/`（与 variation-engine 的 build-log
同域），不动 skill 安装目录；目录布局与已发布规则的五字段格式以
[`references/meta/feedback-ledger.md`](../references/meta/feedback-ledger.md) §2/§5 为准:
`events.jsonl` / `candidates.jsonl` / `decisions.jsonl` + `rules.md`
（级别 / 何时适用 / 原话摘录 / 收录日期｜状态）。

状态机（来源: styleseed evolution 协议与 qiaomu-design evolution-protocol,
2026-10 吸收; 边界: 本账本管「反馈→给 Skill 的长期规则」,与 design-md 的
`decisions[]`（项目级设计决策）职责不同,互不替代）:

    observed → proposed → accepted → published → retired
                  ↓           ↓          ↓
                rejected    (拒绝)    rolled-back

铁律:
  - 追加写,不原地改历史;每条记录有唯一 id/timestamp/type/source;
  - `record` 只记事实不改行为;`propose` 必须声明 level/scope/rationale/eventIds;
  - 自发现问题（source=self）强制附 --evidence 路径（截图/日志/测试输出,
    路径须真实存在;「看起来不对」不算）;
  - 一次性需求不入长期账本（`--once` 标记的事件禁止 propose）;
  - `publish` 必须 --confirm;与同 scope 的既有规则冲突时先生成冲突报告
    （`conflicts/` 目录）,旧规则改「已废止（日期，原因）」，**不删除**；
  - 发布后重跑门禁失败 → `transition --status rolled-back` 留痕。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
    0 = 完成且无冲突;1 = 有冲突/verify 有错;2 = 没能检查或用法/输入错误。
依赖: Python 3 标准库(无第三方依赖)。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time

LEVELS = ("硬禁令", "强偏好", "情境规则")
EVENT_TYPES = ("correction", "preference", "approval", "defect", "validation")
DECISION_STATES = ("accepted", "rejected", "published", "retired", "rolled-back")
RULE_ID_RE = re.compile(r"P-[A-Za-z0-9-]+\Z")
LEDGER_MD_HEADER = (
    "# 反馈账本（项目级）\n\n"
    "> 由 `scripts/ledger.py publish` 维护；规则五字段：级别 / 何时适用 / 原话摘录 / "
    "收录日期｜状态（格式 canonical 见 references/meta/feedback-ledger.md §5）。\n"
    "> 废止不删除：旧规则保留原文，状态行改为「已废止（日期，原因）」。\n"
)


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _today() -> str:
    return time.strftime("%Y-%m-%d")


def _new_id(prefix: str, payload: str) -> str:
    digest = hashlib.sha256(f"{time.time_ns()}\n{payload}".encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{digest}"


def ledger_dir(root: str) -> str:
    return os.path.join(os.path.abspath(root), ".maliang", "feedback")


def ledger_file(root: str, name: str) -> str:
    return os.path.join(ledger_dir(root), name)


def markdown_path(root: str) -> str:
    return os.path.join(os.path.abspath(root), ".maliang", "feedback", "rules.md")


def ensure_store(root: str) -> None:
    os.makedirs(ledger_dir(root), exist_ok=True)
    for name in ("events.jsonl", "candidates.jsonl", "decisions.jsonl"):
        path = ledger_file(root, name)
        if not os.path.exists(path):
            with open(path, "a", encoding="utf-8"):
                pass


def append(root: str, name: str, record: dict) -> None:
    ensure_store(root)
    with open(ledger_file(root, name), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(root: str, name: str) -> list[dict]:
    path = ledger_file(root, name)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"账本不存在：{path}；先跑 ledger.py init")
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{name}:{lineno} 不是有效 JSON：{exc}") from exc
    return records


def state_of(decisions: list[dict], candidate_id: str) -> str:
    latest = None
    for decision in decisions:
        if decision.get("candidateId") == candidate_id:
            latest = decision.get("status")
    return latest or "proposed"


def active_rules(decisions: list[dict], candidates: list[dict]) -> list[dict]:
    """当前生效（published 且未 retired/rolled-back）的候选规则。"""
    out = []
    for candidate in candidates:
        state = state_of(decisions, candidate["id"])
        if state == "published":
            out.append(candidate)
    return out


def _normalize_scope(scope: str) -> str:
    return re.sub(r"\s+", "", scope or "")


def find_conflicts(root: str, candidate: dict) -> list[dict]:
    """同 scope 的其它生效规则视为冲突候选（先生成报告,不靠后写覆盖前写）。"""
    decisions = read_jsonl(root, "decisions.jsonl")
    candidates = read_jsonl(root, "candidates.jsonl")
    scope = _normalize_scope(candidate.get("scope", ""))
    return [c for c in active_rules(decisions, candidates)
            if c.get("id") and c.get("id") != candidate.get("id")
            and _normalize_scope(c.get("scope", "")) == scope]


def write_conflict_report(root: str, candidate: dict, conflicts: list[dict]) -> str:
    directory = os.path.join(ledger_dir(root), "conflicts")
    os.makedirs(directory, exist_ok=True)
    safe_id = re.sub(r"[^A-Za-z0-9._-]", "_", str(candidate.get("id") or "unknown"))
    path = os.path.join(directory, f"{time.strftime('%Y%m%d-%H%M%S')}-{safe_id}.md")
    decisions = read_jsonl(root, "decisions.jsonl")
    published_by_candidate = {d.get("candidateId"): d.get("ruleId") for d in decisions
                              if d.get("status") == "published" and d.get("ruleId")}
    lines = [
        "# 规则冲突报告", "",
        f"- 生成时间：{_now()}",
        f"- 新候选：`{candidate['id']}`（{candidate.get('level')}，scope: {candidate.get('scope')}）",
        f"- 规则：{candidate.get('rule')}", "",
        "## 与现有生效规则冲突", "",
    ]
    for old in conflicts:
        rule_no = published_by_candidate.get(old["id"])
        label = f"`{rule_no}`（候选 `{old['id']}`）" if rule_no else f"候选 `{old['id']}`"
        lines.append(f"- {label}（scope: {old.get('scope')}）：{old.get('rule')}")
    lines += [
        "", "## 处置（二选一，不得两不选）", "",
        "1. 收敛新规则 scope，避免与旧规则重叠：重新 propose（旧规则不动）；",
        "2. 明确替代旧规则：publish 时加 `--supersedes <旧规则编号>` 与 `--reason`，",
        "   旧规则在 feedback-ledger.md 中改「已废止（日期，原因）」并保留原文。", "",
        "本报告只记录冲突事实,不改动任何规则。",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


# ---------------------------------------------------------------------------
# 子命令实现
# ---------------------------------------------------------------------------

def cmd_init(root: str) -> int:
    ensure_store(root)
    print(f"已初始化账本：{ledger_dir(root)}")
    print("提示：把 .maliang/ 加进项目 .gitignore（与 variation-engine build-log 同域同待遇）。")
    return 0


def cmd_record(root: str, args) -> int:
    event_type = args.type
    if event_type not in EVENT_TYPES:
        print(f"ledger: --type 只能是 {'/'.join(EVENT_TYPES)}", file=sys.stderr)
        return 2
    if not args.quote:
        print("ledger: record 需要 --quote（原话摘录；不许转述）", file=sys.stderr)
        return 2
    evidence = list(args.evidence or [])
    if args.source == "self" and not evidence:
        print("ledger: source=self 必须附 --evidence（截图/日志/测试输出路径）；「看起来不对」不算",
              file=sys.stderr)
        return 2
    missing = [p for p in evidence if not os.path.exists(p)]
    if missing:
        print(f"ledger: --evidence 路径不存在：{missing}（证据必须真实存在）", file=sys.stderr)
        return 2
    record = {
        "id": _new_id("evt", args.quote),
        "timestamp": _now(),
        "type": event_type,
        "source": args.source,
        "quote": args.quote,
        "scope": args.scope or "待提炼",
        "taskId": args.task_id,
        "evidence": evidence,
        "longTerm": not args.once,
        "status": "observed",
    }
    append(root, "events.jsonl", record)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    if args.once:
        print("（已标记一次性需求：不会被 propose 收进长期账本）")
    return 0


def cmd_propose(root: str, args) -> int:
    try:
        events = read_jsonl(root, "events.jsonl")
    except FileNotFoundError as exc:
        print(f"ledger: 没能检查——{exc}", file=sys.stderr)
        return 2
    event = next((e for e in events if e.get("id") == args.event), None)
    if not event:
        print(f"ledger: 找不到事件 {args.event}", file=sys.stderr)
        return 2
    if event.get("longTerm") is False:
        print("ledger: 该事件标记为一次性需求，不入长期账本；确需长期请重新 record（不带 --once）",
              file=sys.stderr)
        return 2
    if event.get("source") == "self" and not event.get("evidence"):
        print("ledger: 自发现事件缺少证据路径，候选不受理（先 record --evidence）", file=sys.stderr)
        return 2
    if args.level not in LEVELS:
        print(f"ledger: --level 只能是 {'/'.join(LEVELS)}", file=sys.stderr)
        return 2
    for required in ("scope", "reason"):
        if not getattr(args, required):
            print(f"ledger: propose 需要 --{required}", file=sys.stderr)
            return 2
    record = {
        "id": _new_id("cand", f"{args.event}\n{args.rule}"),
        "timestamp": _now(),
        "type": "candidate",
        "source": "cli",
        "eventIds": [args.event],
        "rule": args.rule,
        "level": args.level,
        "scope": args.scope,
        "rationale": args.reason,
        "preflight": args.preflight,
        "status": "proposed",
    }
    append(root, "candidates.jsonl", record)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def cmd_approve(root: str, args) -> int:
    try:
        candidates = read_jsonl(root, "candidates.jsonl")
        decisions = read_jsonl(root, "decisions.jsonl")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ledger: 没能检查——{exc}", file=sys.stderr)
        return 2
    candidate = next((c for c in candidates if c.get("id") == args.candidate), None)
    if not candidate:
        print(f"ledger: 找不到候选规则 {args.candidate}", file=sys.stderr)
        return 2
    if args.status not in ("accepted", "rejected"):
        print("ledger: --status 只能是 accepted 或 rejected", file=sys.stderr)
        return 2
    if args.status == "accepted" and not args.confirm:
        print("ledger: 批准候选会让规则进入 accepted，必须显式加 --confirm", file=sys.stderr)
        return 2
    current = state_of(decisions, args.candidate)
    if current in ("accepted", "rejected", "published", "retired", "rolled-back"):
        print(f"ledger: 候选当前状态是 {current}，不能重复审核", file=sys.stderr)
        return 2
    decision = {
        "id": _new_id("dec", f"{args.candidate}\n{args.status}"),
        "timestamp": _now(),
        "type": "decision",
        "candidateId": args.candidate,
        "status": args.status,
        "reason": args.reason or ("显式批准候选规则" if args.status == "accepted" else "拒绝候选规则"),
    }
    append(root, "decisions.jsonl", decision)
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0


def _update_rule_status(root: str, rule_id: str, status_text: str, note: str) -> None:
    """把已发布规则的状态行改为 status_text（保留原文，不删除）。"""
    path = markdown_path(root)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    pattern = re.compile(r"(### %s · .*?\n(?:- .*\n)*)" % re.escape(rule_id))
    m = pattern.search(text)
    if not m:
        raise ValueError(f"feedback-ledger.md 里找不到规则 {rule_id}（发布链路不完整）")
    section = m.group(1)
    updated = re.sub(r"（?状态：生效）?", f"状态：{status_text}", section)
    if updated == section:
        if f"状态：{status_text}" not in section:
            raise ValueError(f"规则 {rule_id} 的状态行无法更新（当前不是「生效」）")
    updated += f"- 变更记录：{_today()}｜{note}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text[:m.start(1)] + updated + text[m.end(1):])


def cmd_publish(root: str, args) -> int:
    if not args.confirm:
        print("ledger: 发布会改变 rules.md，必须显式加 --confirm", file=sys.stderr)
        return 2
    if args.rule_id is not None and not RULE_ID_RE.match(args.rule_id):
        print("ledger: --rule-id 必须是可读的规则编号（如 P-01）", file=sys.stderr)
        return 2
    try:
        events = read_jsonl(root, "events.jsonl")
        candidates = read_jsonl(root, "candidates.jsonl")
        decisions = read_jsonl(root, "decisions.jsonl")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ledger: 没能检查——{exc}", file=sys.stderr)
        return 2
    candidate = next((c for c in candidates if c.get("id") == args.candidate), None)
    if not candidate:
        print(f"ledger: 找不到候选规则 {args.candidate}", file=sys.stderr)
        return 2
    if state_of(decisions, args.candidate) != "accepted":
        print("ledger: 只能发布已经 accepted 的候选规则（先 approve --confirm）", file=sys.stderr)
        return 2
    if any(d.get("status") == "published" and d.get("candidateId") == args.candidate
           for d in decisions):
        print("ledger: 该候选已经发布过，禁止重复发布", file=sys.stderr)
        return 2

    path = markdown_path(root)
    existing = ""
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = f.read()
    rule_id = args.rule_id
    if rule_id is None:
        # 缺省接当前最大号递增;编号不复用(已废止规则的编号也占位)
        used_numbers = [int(m) for m in re.findall(r"### P-(\d+) ·", existing)]
        for decision in decisions:
            match = re.fullmatch(r"P-(\d+)", str(decision.get("ruleId") or ""))
            if match:
                used_numbers.append(int(match.group(1)))
        rule_id = f"P-{(max(used_numbers) + 1) if used_numbers else 1:02d}"
    if re.search(r"### %s ·" % re.escape(rule_id), existing):
        print(f"ledger: 规则编号已存在：{rule_id}（编号不复用）", file=sys.stderr)
        return 2

    conflicts = find_conflicts(root, candidate)
    if conflicts and not args.supersedes:
        report = write_conflict_report(root, candidate, conflicts)
        print(f"ledger: 与 {len(conflicts)} 条生效规则冲突（同 scope）；未发布。", file=sys.stderr)
        print(f"冲突报告：{report}", file=sys.stderr)
        print("处置：收敛 scope 后重新 propose，或 publish 时加 --supersedes <规则编号> --reason <原因>",
              file=sys.stderr)
        return 1
    superseded_candidate_id = None
    if args.supersedes:
        if not args.reason:
            print("ledger: --supersedes 必须同时给 --reason（废止旧规则的原因）", file=sys.stderr)
            return 2
        if not _rule_exists(existing, args.supersedes):
            print(f"ledger: feedback-ledger.md 里找不到要废止的规则 {args.supersedes}", file=sys.stderr)
            return 2
        published_by_rule = {d.get("ruleId"): d.get("candidateId") for d in decisions
                             if d.get("status") == "published" and d.get("ruleId")}
        superseded_candidate_id = published_by_rule.get(args.supersedes)
        if not superseded_candidate_id:
            print(f"ledger: 规则 {args.supersedes} 没有对应的已发布候选记录", file=sys.stderr)
            return 2
        if state_of(decisions, superseded_candidate_id) != "published":
            print(f"ledger: 规则 {args.supersedes} 当前不是生效状态，不能再次废止", file=sys.stderr)
            return 2

    event = next((e for e in events if e["id"] in candidate.get("eventIds", [])), None)
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(LEDGER_MD_HEADER)
    quote = event.get("quote", "见事件记录") if event else "见事件记录"
    section = (
        f"\n### {rule_id} · {candidate['rule']}\n"
        f"- 级别：{candidate['level']}\n"
        f"- 何时适用：{candidate['scope']}\n"
        f"- 原话摘录：\"{quote}\"\n"
        f"- 收录：{_today()}｜状态：生效\n"
    )
    if args.supersedes:
        section += f"- 替代：{args.supersedes}（废止原因见其变更记录）\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(section)
    if args.supersedes:
        _update_rule_status(root, args.supersedes, f"已废止（{_today()}，{args.reason}）",
                            f"由 {rule_id} 替代：{args.reason}")
        append(root, "decisions.jsonl", {
            "id": _new_id("dec", f"{superseded_candidate_id}\nretired"), "timestamp": _now(),
            "type": "decision", "candidateId": superseded_candidate_id, "status": "retired",
            "ruleId": args.supersedes, "reason": args.reason,
        })
    append(root, "decisions.jsonl", {
        "id": _new_id("dec", f"{args.candidate}\npublished"), "timestamp": _now(),
        "type": "decision", "candidateId": args.candidate, "status": "published",
        "ruleId": rule_id, "target": os.path.relpath(path, os.path.abspath(root)),
    })
    print(f"已发布 {args.candidate} → {path}（规则号 {rule_id}）")
    if args.supersedes:
        print(f"旧规则 {args.supersedes} 已标「已废止（{_today()}，{args.reason}）」，原文保留。")
    print("发布后请重跑受影响门禁；失败则 `transition --status rolled-back --reason ...` 留痕。")
    return 0


def _rule_exists(markdown: str, rule_id: str) -> bool:
    return bool(re.search(r"### %s ·" % re.escape(rule_id), markdown))


def cmd_transition(root: str, args) -> int:
    if not args.confirm:
        print("ledger: 状态迁移必须显式加 --confirm", file=sys.stderr)
        return 2
    if args.status not in ("retired", "rolled-back"):
        print("ledger: --status 只能是 retired 或 rolled-back", file=sys.stderr)
        return 2
    try:
        candidates = read_jsonl(root, "candidates.jsonl")
        decisions = read_jsonl(root, "decisions.jsonl")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ledger: 没能检查——{exc}", file=sys.stderr)
        return 2
    if not any(c.get("id") == args.candidate for c in candidates):
        print(f"ledger: 找不到候选规则 {args.candidate}", file=sys.stderr)
        return 2
    current = state_of(decisions, args.candidate)
    if current not in ("accepted", "published"):
        print(f"ledger: 当前状态 {current} 不能迁移为 {args.status}", file=sys.stderr)
        return 2
    if not args.reason:
        print("ledger: transition 需要 --reason", file=sys.stderr)
        return 2
    rule_id = None
    for decision in decisions:
        if decision.get("candidateId") == args.candidate and decision.get("status") == "published":
            rule_id = decision.get("ruleId")
    if rule_id and os.path.isfile(markdown_path(root)):
        label = "已废止" if args.status == "retired" else "已回滚"
        _update_rule_status(root, rule_id, f"{label}（{_today()}，{args.reason}）",
                            f"{args.status}：{args.reason}")
    append(root, "decisions.jsonl", {
        "id": _new_id("dec", f"{args.candidate}\n{args.status}"), "timestamp": _now(),
        "type": "decision", "candidateId": args.candidate, "status": args.status,
        "ruleId": rule_id, "reason": args.reason,
    })
    print(f"已记录 {args.candidate} → {args.status}（{args.reason}）")
    return 0


def verify_ledger(root: str) -> tuple[list[str], dict]:
    events = read_jsonl(root, "events.jsonl")
    candidates = read_jsonl(root, "candidates.jsonl")
    decisions = read_jsonl(root, "decisions.jsonl")
    errors: list[str] = []
    ids: set[str] = set()
    for record in events + candidates + decisions:
        rid = record.get("id")
        if not rid or rid in ids:
            errors.append(f"重复或缺少 id：{rid or '(空)'}")
        ids.add(rid)
    for event in events:
        if event.get("type") not in EVENT_TYPES:
            errors.append(f"{event.get('id')}: 未知事件类型 {event.get('type')}")
        if event.get("source") == "self" and not event.get("evidence"):
            errors.append(f"{event.get('id')}: 自发现事件缺少证据")
    for candidate in candidates:
        if candidate.get("level") not in LEVELS:
            errors.append(f"{candidate.get('id')}: 未知规则级别 {candidate.get('level')}")
        for event_id in candidate.get("eventIds", []):
            event = next((e for e in events if e.get("id") == event_id), None)
            if not event:
                errors.append(f"{candidate.get('id')}: 缺少事件 {event_id}")
            elif event.get("longTerm") is False:
                errors.append(f"{candidate.get('id')}: 引用了一次性需求事件 {event_id}（不应入长期账本）")
    markdown = ""
    if os.path.isfile(markdown_path(root)):
        with open(markdown_path(root), "r", encoding="utf-8") as f:
            markdown = f.read()
    for decision in decisions:
        if decision.get("status") not in DECISION_STATES:
            errors.append(f"{decision.get('id')}: 未知决策状态 {decision.get('status')}")
        if not any(c.get("id") == decision.get("candidateId") for c in candidates):
            errors.append(f"{decision.get('id')}: 缺少候选规则 {decision.get('candidateId')}")
        if decision.get("status") == "published":
            rule_id = decision.get("ruleId")
            if not rule_id or not _rule_exists(markdown, rule_id):
                errors.append(f"{decision.get('id')}: 已发布规则 {rule_id} 在 rules.md 中缺失（不删除历史）")
    if markdown:
        numbers = re.findall(r"### (P-[A-Za-z0-9-]+) ·", markdown)
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        if duplicates:
            errors.append(f"rules.md 规则编号重复：{duplicates}（编号必须唯一,不复用）")
    summary = {
        "events": len(events),
        "candidates": len(candidates),
        "decisions": len(decisions),
        "states": {},
        "oneOffEvents": sum(1 for e in events if e.get("longTerm") is False),
    }
    for candidate in candidates:
        cid = candidate.get("id")
        if not cid:
            errors.append("candidates.jsonl 存在缺 id 的记录(畸形条目,未统计)")
            continue
        state = state_of(decisions, cid)
        summary["states"][state] = summary["states"].get(state, 0) + 1
    return errors, summary


def cmd_verify(root: str, _args) -> int:
    try:
        errors, summary = verify_ledger(root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ledger: 没能检查——{exc}", file=sys.stderr)
        return 2
    if errors:
        print(f"账本校验失败（{len(errors)} 项）：")
        for error in errors:
            print(f"  ✗ {error}")
        return 1
    print(f"账本校验通过：{summary['events']} 事件 / {summary['candidates']} 候选 / "
          f"{summary['decisions']} 决策")
    return 0


def cmd_report(root: str, _args) -> int:
    try:
        errors, summary = verify_ledger(root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ledger: 没能检查——{exc}", file=sys.stderr)
        return 2
    decisions = read_jsonl(root, "decisions.jsonl")
    candidates = read_jsonl(root, "candidates.jsonl")
    conflicts = [c for c in candidates if state_of(decisions, c["id"]) == "published"
                 and find_conflicts(root, c)]
    report = {"root": ledger_dir(root), **summary, "errors": errors,
              "activeWithSameScope": len(conflicts)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ledger.py",
        description="反馈→规则状态机账本：events/candidates/decisions 追加写 + --confirm 发布 + 冲突报告。",
        epilog="账本落点 <root>/.maliang/feedback/（events/candidates/decisions.jsonl + rules.md），\n"
               "布局与五字段格式 canonical 见 references/meta/feedback-ledger.md。\n"
               "一次性需求用 `record --once` 标记，不会进长期账本；自发现问题必须附真实证据路径。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", default=".", help="项目根（账本在 <root>/.maliang/，默认当前目录）")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="创建账本目录与追加日志").set_defaults(func=lambda root, a: cmd_init(root))

    record = sub.add_parser("record", help="记录反馈/自发现缺陷（不改行为）")
    record.add_argument("--type", required=True, help="/".join(EVENT_TYPES))
    record.add_argument("--source", required=True, choices=["user", "self"])
    record.add_argument("--quote", required=True, help="原话摘录")
    record.add_argument("--scope", default=None)
    record.add_argument("--task-id", default=None)
    record.add_argument("--evidence", action="append", default=[], help="证据路径（source=self 必填）")
    record.add_argument("--once", action="store_true", help="一次性需求（不入长期账本）")
    record.set_defaults(func=cmd_record)

    propose = sub.add_parser("propose", help="从事件抽象候选规则（不改行为）")
    propose.add_argument("--event", required=True)
    propose.add_argument("--rule", required=True)
    propose.add_argument("--level", required=True, help="/".join(LEVELS))
    propose.add_argument("--scope", required=True)
    propose.add_argument("--reason", required=True, help="rationale：为什么抽象成规则")
    propose.add_argument("--preflight", default=None)
    propose.set_defaults(func=cmd_propose)

    approve = sub.add_parser("approve", help="接受/拒绝候选（accepted 必须 --confirm）")
    approve.add_argument("--candidate", required=True)
    approve.add_argument("--status", default="accepted", help="accepted / rejected")
    approve.add_argument("--reason", default=None)
    approve.add_argument("--confirm", action="store_true")
    approve.set_defaults(func=cmd_approve)

    publish = sub.add_parser("publish", help="发布已接受候选到 feedback-ledger.md（必须 --confirm）")
    publish.add_argument("--candidate", required=True)
    publish.add_argument("--rule-id", default=None,
                         help="规则编号（如 P-01;缺省接当前最大号递增,编号不复用）")
    publish.add_argument("--supersedes", default=None, help="废止的旧规则编号（冲突处置）")
    publish.add_argument("--reason", default=None)
    publish.add_argument("--confirm", action="store_true")
    publish.set_defaults(func=cmd_publish)

    transition = sub.add_parser("transition", help="retired / rolled-back 留痕（必须 --confirm）")
    transition.add_argument("--candidate", required=True)
    transition.add_argument("--status", required=True, help="retired / rolled-back")
    transition.add_argument("--reason", required=True)
    transition.add_argument("--confirm", action="store_true")
    transition.set_defaults(func=cmd_transition)

    sub.add_parser("verify", help="校验 JSONL、引用与发布链路").set_defaults(func=cmd_verify)
    sub.add_parser("report", help="输出事件/候选/规则状态摘要").set_defaults(func=cmd_report)

    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    root = os.path.abspath(args.root)
    try:
        return args.func(root, args)
    except (ValueError, OSError) as exc:
        print(f"ledger: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
