#!/usr/bin/env python3
"""receipts —— 测量收据机制（证据可重算运行记录）。

"绝不说出一个你没量过的数字" 需要一个可重算的载体：模型可以随手打出一个对比度
比值，下游无法分辨它是量出来的还是想出来的。本脚本把每次测量绑定到被测产物的
sha256 上——哈希在**跑之前**取（那才是这些数字所描述的状态），产物一旦被编辑，
收据即 EXPIRED，记住了的数字就变成了谎言。

机制（#17 测量收据 + #19 证据从自述升级为可重算运行记录，合并为同一实现；
来源: ux-ui-agent-skills/scripts/gate.mjs 与 styleseed evidence-gate.mjs,
2026-10 吸收,中文自研实现）:

    init    绑定产物 + 脚本的 sha256（跑门禁**之前**执行）
    attach  登记门禁报告（report.json 等）的 sha256 + 退出码 + 关键数字
    verify  重算全部绑定哈希，输出三态 OK / EXPIRED / UNMEASURED

会话隔离：收据按会话分文件（`<root>/.maliang/receipts/<session>.jsonl`），
上一会话的收据永不复用——UNMEASURED 就是本次会话还没有量过，不是失败也不是通过。
会话 id 取 `--session` > 环境变量 `MALIANG_SESSION_ID` > 本地兜底 `local`。

查询：

    python3 scripts/receipts.py --check <产物路径>   # 该产物在本次会话有没有活收据
    python3 scripts/receipts.py --list               # 本次会话全部收据

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
    0 = OK（verify 全绿 / --check 有活收据）
    1 = EXPIRED（量过之后被改）或 UNMEASURED（没有收据 = 未记录）
    2 = 没能检查（路径不存在 / 用法错误 / 收据文件不可读）
写不出收据时按未记录处理（显式报错，禁止静默当成功）。

依赖: Python 3 标准库(无第三方依赖)；只读/追加写，不修改被测产物。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

STATE_OK = "OK"
STATE_EXPIRED = "EXPIRED"
STATE_UNMEASURED = "UNMEASURED"

SESSION_ENV = "MALIANG_SESSION_ID"
DEFAULT_ROOT = ".maliang/receipts"
# 会话 id 只保留可作文件名的字符（与 gate.mjs 同款净化）
SESSION_SANITIZE_RE = re.compile(r"[^\w-]")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_file(path: str) -> str:
    """产物 sha256；文件不存在时抛 FileNotFoundError（显性失败）。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _sanitize_session(value: str) -> str:
    clean = SESSION_SANITIZE_RE.sub("", value or "")
    return clean or "local"


def session_id(explicit: str | None) -> str:
    if explicit:
        return _sanitize_session(explicit)
    return _sanitize_session(os.environ.get(SESSION_ENV, "") or "local")


def receipts_dir(root: str, session: str) -> str:
    return os.path.join(os.path.abspath(root), DEFAULT_ROOT)


def receipts_file(root: str, session: str) -> str:
    return os.path.join(receipts_dir(root, session), session + ".jsonl")


def read_receipts(root: str, session: str) -> list[dict]:
    """读取本次会话收据（append-only JSONL）。

    损坏行不静默跳过，抛 ValueError 显性上报——收据文件不可信时不能假装无收据。
    """
    path = receipts_file(root, session)
    if not os.path.isfile(path):
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"收据文件损坏 {path}:{lineno}: {exc}") from exc
    return records


def append_receipt(root: str, session: str, record: dict) -> bool:
    """追加一条收据；写不出返回 False（调用方按未记录处理）。"""
    path = receipts_file(root, session)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except OSError as exc:
        print(
            f"receipts: 收据写入失败（{exc}）。这次测量按**未记录**处理（Treat as unrecorded）。",
            file=sys.stderr,
        )
        return False


def _file_entry(path: str) -> dict:
    """绑定条目：绝对路径 + 跑前快照（sha256/bytes）。"""
    abs_path = os.path.abspath(path)
    return {
        "path": abs_path,
        "sha256": _sha256_file(abs_path),
        "bytes": os.path.getsize(abs_path),
    }


def init_run(
    root: str,
    session: str,
    run: str,
    artifacts: list[str],
    scripts: list[str],
    note: str | None,
) -> dict:
    """init：绑定产物 + 脚本哈希（必须在跑门禁之前执行）。"""
    existing = [r for r in read_receipts(root, session) if r.get("run") == run and r.get("type") == "init"]
    if existing:
        raise ValueError(
            f"run={run} 已有 init 收据（收据不可覆盖）；换一个 run id，或换会话。"
        )
    if not artifacts and not scripts:
        raise ValueError("init 至少需要一个 --artifact 或 --script（没有绑定对象的收据不成立）")
    record = {
        "type": "init",
        "run": run,
        "at": _now(),
        "session": session,
        "artifacts": [_file_entry(p) for p in artifacts],
        "scripts": [_file_entry(p) for p in scripts],
    }
    if note:
        record["note"] = note
    if not append_receipt(root, session, record):
        raise OSError("收据写入失败")
    return record


def attach_report(
    root: str,
    session: str,
    run: str,
    report: str,
    gate: str | None,
    exit_code: int | None,
    values: list[str],
) -> dict:
    """attach：登记门禁报告的 sha256、退出码与关键数字。"""
    inits = [r for r in read_receipts(root, session) if r.get("run") == run and r.get("type") == "init"]
    if not inits:
        raise ValueError(f"run={run} 还没有 init 收据；先 init 绑定产物，再跑门禁，最后 attach")
    entry = _file_entry(report)
    record = {
        "type": "attach",
        "run": run,
        "at": _now(),
        "session": session,
        "gate": gate or "unknown",
        "exit": exit_code,
        "report": entry,
        "values": list(values),
    }
    if not append_receipt(root, session, record):
        raise OSError("收据写入失败")
    return record


def _recompute(entry: dict) -> tuple[bool, str | None]:
    """重算绑定条目的哈希；返回 (是否仍然一致, 说明)。"""
    path = entry.get("path", "")
    if not os.path.isfile(path):
        return False, f"文件已不存在: {path}"
    try:
        now = _sha256_file(path)
    except OSError as exc:
        return False, f"无法读取 {path}: {exc}"
    if now != entry.get("sha256"):
        return False, f"内容已改变: {path}"
    return True, None


def verify_run(root: str, session: str, run: str) -> dict:
    """verify：重算 run 的全部绑定哈希，输出三态。"""
    records = [r for r in read_receipts(root, session) if r.get("run") == run]
    inits = [r for r in records if r.get("type") == "init"]
    if not inits:
        return {
            "run": run,
            "state": STATE_UNMEASURED,
            "session": session,
            "message": "UNMEASURED: 本次会话没有 run=" + run + " 的收据。没有量过，不是通过。",
            "stale": [],
            "attachments": [],
        }
    init = inits[0]
    stale: list[str] = []
    for group in ("artifacts", "scripts", "inputs"):
        for entry in init.get(group, []) or []:
            ok, why = _recompute(entry)
            if not ok:
                stale.append(f"[{group}] {why}")
    attachments = []
    for rec in records:
        if rec.get("type") != "attach":
            continue
        report = rec.get("report") or {}
        ok, why = _recompute(report)
        if not ok:
            stale.append(f"[report] {why}")
        attachments.append(
            {
                "gate": rec.get("gate"),
                "exit": rec.get("exit"),
                "path": report.get("path"),
                "live": ok,
                "values": rec.get("values", []),
                "at": rec.get("at"),
            }
        )
    if stale:
        return {
            "run": run,
            "state": STATE_EXPIRED,
            "session": session,
            "message": "EXPIRED: run=" + run + " 量过之后被改。旧的数字不再描述它。",
            "stale": stale,
            "attachments": attachments,
            "init_at": init.get("at"),
            "note": init.get("note"),
        }
    return {
        "run": run,
        "state": STATE_OK,
        "session": session,
        "message": f"OK: run={run} 的全部绑定哈希与测量时一致。",
        "stale": [],
        "attachments": attachments,
        "init_at": init.get("at"),
        "note": init.get("note"),
    }


def check_path(root: str, session: str, path: str) -> dict:
    """--check：某产物在本次会话是否有活收据（三态）。

    口径：收据描述的是整个绑定集合；集合内任一文件变化，该收据即 EXPIRED
    （「源变即 stale」），而非只失效被改的那一个。跨会话收据不参与判定。
    """
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        return {
            "path": abs_path,
            "state": None,
            "message": f"没能检查：路径不存在 {abs_path}（未测量，不得记为通过）。",
        }
    measured: list[dict] = []
    for rec in read_receipts(root, session):
        if rec.get("type") != "init":
            continue
        targets = (rec.get("artifacts") or []) + (rec.get("scripts") or [])
        if any(os.path.abspath(t.get("path", "")) == abs_path for t in targets):
            measured.append(rec)
    if not measured:
        return {
            "path": abs_path,
            "state": STATE_UNMEASURED,
            "message": f"UNMEASURED: 本次会话没有任何门禁量过 {abs_path}。",
        }
    verdicts = [verify_run(root, session, rec.get("run", "")) for rec in measured]
    live = [v for v in verdicts if v["state"] == STATE_OK]
    if live:
        return {
            "path": abs_path,
            "state": STATE_OK,
            "message": f"OK: {abs_path} 有 {len(live)} 条活收据。",
            "receipts": live,
        }
    return {
        "path": abs_path,
        "state": STATE_EXPIRED,
        "message": f"EXPIRED: {abs_path} 量过之后被改（或其同批产物被改）。旧的数字不再描述它。",
        "receipts": verdicts,
    }


def list_receipts(root: str, session: str) -> list[dict]:
    out = []
    for rec in read_receipts(root, session):
        if rec.get("type") == "init":
            verdict = verify_run(root, session, rec.get("run", ""))
            out.append(
                {
                    "run": rec.get("run"),
                    "at": rec.get("at"),
                    "state": verdict["state"],
                    "artifacts": [t.get("path") for t in rec.get("artifacts", [])],
                    "scripts": [t.get("path") for t in rec.get("scripts", [])],
                    "stale": verdict["stale"],
                }
            )
    return out


def _print_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        prog="receipts.py",
        description="测量收据：init 绑定产物/脚本哈希（跑前取）→ attach 登记报告 sha256 → verify 重算三态。",
        epilog="示例：\n"
        "  python3 scripts/receipts.py init --run r1 --artifact preview/home.html --script scripts/preview-check.py\n"
        "  python3 scripts/receipts.py attach --run r1 --report shots/report.json --gate preview-check --exit-code 0 \\\n"
        "      --value 'contrast=4.6:1'\n"
        "  python3 scripts/receipts.py verify --run r1\n"
        "  python3 scripts/receipts.py --check preview/home.html\n"
        "  python3 scripts/receipts.py --list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", nargs="?", choices=["init", "attach", "verify"], help="子命令")
    parser.add_argument("--root", default=".", help="项目根（收据落在 <root>/.maliang/receipts/，默认当前目录）")
    parser.add_argument("--session", default=None, help=f"会话 id（缺省取 ${SESSION_ENV}，再缺省 local）")
    parser.add_argument("--run", default=None, help="本次测量运行 id（init/attach/verify 共用）")
    parser.add_argument("--artifact", action="append", default=[], help="init：被测产物路径（可重复）")
    parser.add_argument("--script", action="append", default=[], help="init：本次使用的门禁脚本路径（可重复）")
    parser.add_argument("--note", default=None, help="init：备注（如测量目标）")
    parser.add_argument("--report", default=None, help="attach：门禁报告路径（report.json）")
    parser.add_argument("--gate", default=None, help="attach：门禁名（如 preview-check）")
    parser.add_argument("--exit-code", type=int, default=None, help="attach：门禁退出码")
    parser.add_argument("--value", action="append", default=[], help="attach：关键数字（可重复，如 'contrast=4.6:1'）")
    parser.add_argument("--check", default=None, metavar="PATH", help="查询某产物在本次会话的收据三态")
    parser.add_argument("--list", action="store_true", help="列出本次会话全部收据")
    parser.add_argument("--dir", action="store_true", help="打印本次会话收据目录")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args(argv)

    session = session_id(args.session)
    root = os.path.abspath(args.root)

    try:
        if args.dir:
            print(receipts_file(root, session))
            return 0
        if args.list:
            items = list_receipts(root, session)
            if args.json:
                _print_json(items)
                return 0
            if not items:
                print("本次会话没有收据。什么都还没量过（Nothing has been measured yet）。")
                return 0
            for item in items:
                mark = "" if item["state"] == STATE_OK else f"  [{item['state']}]"
                paths = " ".join(item["artifacts"] + item["scripts"])
                print(f"{item['at']}  {item['state']:<10} run={item['run']}  {paths}{mark}")
                for why in item["stale"]:
                    print(f"           {why}")
            return 0
        if args.check:
            result = check_path(root, session, args.check)
            if result.get("state") is None:
                if args.json:
                    _print_json(result)
                print(result["message"], file=sys.stderr)
                return 2
            if args.json:
                _print_json(result)
            else:
                print(result["message"])
                for rec in result.get("receipts", []):
                    for why in rec.get("stale", []):
                        print(f"  {why}")
            return 0 if result["state"] == STATE_OK else 1

        if not args.run:
            parser.error("init/attach/verify 需要 --run")
        if args.command == "init":
            record = init_run(root, session, args.run, args.artifact, args.script, args.note)
            print(f"已记录收据 init run={args.run}（产物 {len(record['artifacts'])} / 脚本 {len(record['scripts'])}）")
            print(f"  收据文件: {receipts_file(root, session)}")
            print("  提示：把 .maliang/ 加进项目 .gitignore（会话收据是本地状态，不入仓）。")
            return 0
        if args.command == "attach":
            if not args.report:
                parser.error("attach 需要 --report")
            record = attach_report(root, session, args.run, args.report, args.gate, args.exit_code, args.value)
            print(f"已登记报告 attach run={args.run} → {record['report']['path']}")
            print(f"  sha256: {record['report']['sha256']}")
            return 0
        if args.command == "verify":
            result = verify_run(root, session, args.run)
            if args.json:
                _print_json(result)
            else:
                print(result["message"])
                for why in result["stale"]:
                    print(f"  ✗ {why}")
                for att in result["attachments"]:
                    values = ", ".join(att["values"]) if att["values"] else "无记录数字"
                    live = "live" if att["live"] else "STALE"
                    print(f"  [{live}] {att['gate']} exit={att['exit']}  {values}")
                if result["state"] == STATE_UNMEASURED:
                    print("  提示：先 init（跑前取哈希）→ 跑门禁 → attach，然后再 verify。")
            return 0 if result["state"] == STATE_OK else 1
        parser.print_help()
        return 2
    except FileNotFoundError as exc:
        print(f"receipts: 没能检查（文件不存在）：{exc}", file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"receipts: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
