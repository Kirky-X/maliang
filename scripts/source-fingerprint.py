#!/usr/bin/env python3
"""redesign 重审计源码指纹基线(G30 脚本层):廉价新鲜度检查,不读内容进上下文。

重跑 redesign 时先判断「用户的仓库变没变」:逐文件 SHA-256 指纹基线,
对比得出 changed/added/removed——全程只算哈希,**不把文件内容读进模型
上下文**(外部原口径:Hashing is a cheap freshness check)。

信任边界(移植自 superdesign-skill RESUME.md「Trust boundary」,#30,
2026-10 吸收;基线文件按不可信缓存对待):
  - 仅仓库内路径:resolve 后必须落在仓库根内,拒绝绝对路径与 ../ 逃逸;
  - 拒涉密文件: .env* / .git/ / credentials* / 私钥证书(*.pem、id_rsa*、
    *.key)/ 任何疑似 secret store;
  - 键集精确相等:check 模式要求基线 files 键集与重算键集可逐键对账,
    基线含仓外/涉密/重复路径 → 按不可信缓存拒绝(退出 2),不静默清选;
  - 原子写:临时文件 + os.replace,中断不留半截基线。

diff 归约入口:diff 子命令对**单个变更路径**运行 `git diff HEAD -- <path>`
(参数列表传递,路径加引号限定,绝不裸跑全仓 diff);git 不可得时明说并退 2。
归约成「有意义 UI delta」是模型/人的活——本脚本只输出统计,并且明确:
**不得以变更行数或整文件哈希推断重要性**;指纹不匹配单独不强制冷路由。

用法:
    python3 scripts/source-fingerprint.py create <repo> [--output PATH]
    python3 scripts/source-fingerprint.py check  <repo> --baseline PATH
    python3 scripts/source-fingerprint.py diff   <repo> --baseline PATH --path <rel>

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题(有变更) / 2=没能检查;#16)。
依赖: Python 3 标准库(git 仅 diff 子命令需要)。
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

SCHEMA_VERSION = 1

# 目录排除(依赖/构建产物/版本库自身)
EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".next", "__pycache__",
                ".venv", "venv", ".maliang", "specmark"}

# 涉密文件签名(信任边界;命中即拒绝入基线/拒绝信任基线)
SECRET_FILE_RE = re.compile(
    r"(^|/)(\.env[^/]*|credentials[^/]*|id_rsa[^/]*|id_ed25519[^/]*|id_ecdsa[^/]*"
    r"|id_dsa[^/]*|\.git-credentials|\.netrc|\.npmrc|\.pypirc|.*\.pem|.*\.key"
    r"|.*\.p12|.*\.pfx|secrets?\.[a-z]+)$",
    re.IGNORECASE,
)


def is_safe_rel_path(repo_root, rel):
    """仓库内相对路径信任校验:仓内、非涉密、非目录穿越。"""
    if os.path.isabs(rel) or ".." in rel.split(os.sep) or rel.startswith("~"):
        return False, "路径逃逸/绝对路径: %s" % rel
    if ".git" in rel.replace(os.sep, "/").split("/"):
        return False, "版本库内部路径(.git): %s" % rel
    if SECRET_FILE_RE.search(rel.replace(os.sep, "/")):
        return False, "疑似涉密文件(信任边界拒绝): %s" % rel
    full = os.path.normpath(os.path.join(repo_root, rel))
    if not (full == repo_root or full.startswith(repo_root + os.sep)):
        return False, "解析后落在仓库外: %s" % rel
    return True, ""


def walk_repo(repo_root):
    """遍历仓库文件,返回相对路径列表(排除目录与涉密文件)。"""
    out = []
    for root, dirs, names in os.walk(repo_root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("."))
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(root, name), repo_root)
            safe, _ = is_safe_rel_path(repo_root, rel)
            if safe:
                out.append(rel)
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def build_fingerprints(repo_root):
    """逐文件哈希;单个文件读不了 = 显性报错(不算基线)。"""
    files = {}
    for rel in walk_repo(repo_root):
        full = os.path.join(repo_root, rel)
        if not os.path.isfile(full) or os.path.islink(full):
            continue
        try:
            files[rel.replace(os.sep, "/")] = sha256_file(full)
        except OSError as exc:
            raise RuntimeError("无法读取 %s: %s" % (rel, exc))
    return files


def atomic_write_json(path, payload):
    """临时文件 + os.replace 原子写(中断不留半截基线)。"""
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def load_baseline(path, repo_root):
    """读基线并做信任校验;不可信 → 抛 UntrustedBaseline(退出 2)。"""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise UntrustedBaseline("基线不可读: %s" % exc)
    if not isinstance(data, dict) or data.get("schemaVersion") != SCHEMA_VERSION:
        raise UntrustedBaseline("基线 schemaVersion 缺失或不符(按不可信缓存拒绝)")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise UntrustedBaseline("基线缺 files 映射(按不可信缓存拒绝)")
    for rel in files:
        safe, why = is_safe_rel_path(repo_root, rel)
        if not safe:
            raise UntrustedBaseline("基线内路径不可信: %s" % why)
        if not isinstance(files[rel], str) or len(files[rel]) != 64:
            raise UntrustedBaseline("基线内指纹非法: %s" % rel)
    return data, files


class UntrustedBaseline(Exception):
    """基线按不可信缓存拒绝(退出 2,不静默清选)。"""


def cmd_create(args):
    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(repo_root):
        print("source-fingerprint: 仓库目录不存在: %s" % repo_root, file=sys.stderr)
        return 2
    try:
        files = build_fingerprints(repo_root)
    except RuntimeError as exc:
        print("source-fingerprint: %s" % exc, file=sys.stderr)
        return 2
    payload = {
        "schemaVersion": SCHEMA_VERSION,
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "repo": os.path.basename(repo_root),
        "files": files,
    }
    output = args.output or os.path.join(repo_root, ".maliang", "source-fingerprints.json")
    atomic_write_json(output, payload)
    print("基线已写入 %s(%d 个文件;哈希只做新鲜度,不读内容进上下文)" % (output, len(files)))
    return 0


def cmd_check(args):
    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(repo_root):
        print("source-fingerprint: 仓库目录不存在: %s" % repo_root, file=sys.stderr)
        return 2
    try:
        _meta, baseline_files = load_baseline(args.baseline, repo_root)
    except UntrustedBaseline as exc:
        print("source-fingerprint: UNTRUSTED —— %s(重建基线后再跑)" % exc, file=sys.stderr)
        return 2
    try:
        current = build_fingerprints(repo_root)
    except RuntimeError as exc:
        print("source-fingerprint: %s" % exc, file=sys.stderr)
        return 2

    changed = sorted(f for f in current if f in baseline_files and current[f] != baseline_files[f])
    added = sorted(f for f in current if f not in baseline_files)
    removed = sorted(f for f in baseline_files if f not in current)
    for f in changed:
        print("changed: %s" % f)
    for f in added:
        print("added:   %s" % f)
    for f in removed:
        print("removed: %s" % f)
    if not (changed or added or removed):
        print("指纹一致(%d 个文件):自基线以来仓库未变。" % len(current))
        return 0
    print("指纹差异:%d changed / %d added / %d removed(哈希只证变化,不证重要性;"
          "不得以变更行数或整文件哈希推断重要性)" % (len(changed), len(added), len(removed)))
    return 1


def cmd_diff(args):
    repo_root = os.path.abspath(args.repo)
    rel = args.path.replace("/", os.sep)
    safe, why = is_safe_rel_path(repo_root, args.path)
    if not safe:
        print("source-fingerprint: %s" % why, file=sys.stderr)
        return 2
    if not os.path.isfile(os.path.join(repo_root, rel)):
        print("source-fingerprint: 文件不存在: %s" % args.path, file=sys.stderr)
        return 2
    try:
        _meta, baseline_files = load_baseline(args.baseline, repo_root)
    except UntrustedBaseline as exc:
        print("source-fingerprint: UNTRUSTED —— %s" % exc, file=sys.stderr)
        return 2
    full_path = os.path.join(repo_root, rel)
    if os.path.islink(full_path):
        print("source-fingerprint: UNMEASURED —— 符号链接不入基线(与 create 口径一致)", file=sys.stderr)
        return 2
    unchanged = baseline_files.get(args.path.replace(os.sep, "/")) == sha256_file(os.path.join(repo_root, rel))
    if unchanged:
        print("%s 与基线一致:无需 diff(基线即 HEAD 之外的独立新鲜度凭证)。" % args.path)
        return 0
    try:
        proc = subprocess.run(
            ["git", "-C", repo_root, "diff", "HEAD", "--", args.path],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("source-fingerprint: git 不可得(%s)——文件已变,但精确 delta 不可得;"
              "按哈希刷新处理,不要编造变更摘要。" % exc, file=sys.stderr)
        return 2
    if proc.returncode != 0:
        print("source-fingerprint: git diff 失败: %s——文件已变,但精确 delta 不可得,"
              "按哈希刷新处理。" % proc.stderr.strip(), file=sys.stderr)
        return 2
    sys.stdout.write(proc.stdout)
    if not proc.stdout.strip():
        print("(git diff 为空:文件相对 HEAD 无未提交改动;指纹差异来自已提交的历史)"
              "——delta 不可得时明说,不得以行数推断重要性。")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="源码 SHA-256 指纹基线(create/check/diff;信任边界+原子写;不读内容进上下文)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="建立指纹基线")
    p_create.add_argument("repo")
    p_create.add_argument("--output", default=None, help="基线输出路径(默认 <repo>/.maliang/source-fingerprints.json)")

    p_check = sub.add_parser("check", help="对比基线,输出 changed/added/removed")
    p_check.add_argument("repo")
    p_check.add_argument("--baseline", required=True)

    p_diff = sub.add_parser("diff", help="对单个变更路径跑 git diff HEAD -- <path>(引号限定)")
    p_diff.add_argument("repo")
    p_diff.add_argument("--baseline", required=True)
    p_diff.add_argument("--path", required=True, help="仓库内相对路径")

    args = parser.parse_args(argv)
    return {"create": cmd_create, "check": cmd_check, "diff": cmd_diff}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
