#!/usr/bin/env python3
"""生成端 ΔE 验收回路(G39 脚本层):重建截图 vs 参考图逐色保真打分。

「好不好看」判断不了,「颜色对不对」可以变成数字。本脚本把实现图与参考
测量做逐色对账(移植自 design-dna scripts/verify.mjs,#24,2026-10 吸收;
退出码按本仓三态,B 工作流勘误:FAIL 是 1 不是 2):

  阈值:mean ΔE ≤5(实现侧覆盖加权均值)/ max ΔE ≤20(双侧显著簇)/
       coverage drift ≤0.35(逐参考色 |参考覆盖-实现覆盖| 之和)。
  显著线:覆盖 <0.5% 的簇/残渣不计入 max ΔE,也不算「保留了该色」。

反聚合盲区设计(对应 tests/test_verify_color_fidelity.py 五组攻击用例):
  - 实现侧显著错误色块逐簇单独计分,不得被覆盖率加权平均掉;
  - 大错误区域配稀有参考色(参考侧覆盖 <0.5%)仍走实现侧逐簇 max 暴露;
  - 显著参考色在实现侧缺失 → 参考侧 max ΔE 反向暴露;
  - 0.1% 残渣不算保留(显著参考色的最近匹配只在显著实现簇里找);
  - coverage drift 保留 4 位小数,0.3502 > 0.35 的边界失败可解释。

用法:
    python3 scripts/verify-color-fidelity.py <impl.png> --reference <ref.png|spec.json>

参考输入二选一形态:
  - 参考图(PNG):脚本先用 measure-colors 同管线测出 palette(k 可由 --k 覆盖);
  - 测量 spec(JSON):measure-colors 的输出,或嵌套
    {"design_system":{"color":{"measured_palette":[...],"measurement":{"k":...}}}}。
    复测必须与测量同 k(否则不可比)——spec 带 k 时以 spec 为准。

输出(stdout JSON):逐色报告(每个参考色的最近实现色/ΔE/覆盖、每个实现簇
的最近参考色/ΔE/覆盖)+ 汇总与 PASS/FAIL。

退出码: 见 scripts/EXIT-CODES.md(0=PASS / 1=FAIL(任一阈值不过) / 2=没能检查;#16)。
依赖: Python 3 标准库;JPEG 需 Pillow(缺失 → UNMEASURED/2,同 measure-colors)。
来源: design-dna #24,2026-10 吸收。
"""

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

THRESHOLD_MEAN_DE = 5.0
THRESHOLD_MAX_DE = 20.0
THRESHOLD_DRIFT = 0.35
SIGNIFICANT_COVERAGE = 0.005


def _load_measure_module():
    """复用 measure-colors 的解码与测色管线(同目录模块,importlib 加载)。"""
    import importlib.util
    path = os.path.join(_HERE, "measure-colors.py")
    spec = importlib.util.spec_from_file_location("_maliang_measure_colors", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_hex(s):
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError("bad hex: %r" % s)
    return [int(s[i:i + 2], 16) for i in (0, 2, 4)]


def load_reference(reference_path, k_override):
    """读参考:PNG 测量或 spec JSON;返回 (palette, k)。UNMEASURED 抛异常。"""
    mc = _load_measure_module()
    ext = os.path.splitext(reference_path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg"):
        result = mc.measure_image(reference_path, k_override or mc.DEFAULT_K)
        return result["palette"], result["measurement"]["k"]
    try:
        with open(reference_path, "r", encoding="utf-8") as fh:
            spec = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise mc.UnmeasurableError("参考 spec 不可读: %s" % exc)
    palette = spec.get("palette")
    if palette is None:
        palette = (spec.get("design_system") or {}).get("color", {}).get("measured_palette")
    if not isinstance(palette, list) or not palette:
        raise mc.UnmeasurableError(
            "参考 spec 须含 palette 数组(measure-colors 输出)或"
            " design_system.color.measured_palette"
        )
    for entry in palette:
        if not isinstance(entry, dict) or not isinstance(entry.get("coverage"), (int, float)) \
                or not isinstance(entry.get("hex"), str):
            raise mc.UnmeasurableError("参考 palette 条目形态非法(须为 {hex, coverage} 对象)")
        try:
            parse_hex(entry["hex"])
        except ValueError as exc:
            raise mc.UnmeasurableError("参考 palette hex 非法: %s" % exc)
    cfg_k = k_override
    if cfg_k is None:
        cfg_k = (spec.get("measurement") or {}).get("k")
        if cfg_k is None:
            cfg_k = ((spec.get("design_system") or {}).get("color", {}).get("measurement") or {}).get("k")
    k = max(2, min(16, int(cfg_k))) if cfg_k else mc.DEFAULT_K
    return palette, k


def verify(impl_result, ref_palette, ref_k):
    """核心对账:返回报告 dict(pass 字段 + 逐色条目)。impl_result 是 measure 输出。"""
    mc = _load_measure_module()
    d_e = mc.delta_e

    # 重新测量实现图时必须用与参考相同的 k(复测同参数否则不可比)
    impl_k = impl_result["measurement"]["k"]

    # 实现簇按最近参考色分组;参考色的组合覆盖 = 组内簇覆盖之和
    assigned = [[] for _ in ref_palette]
    for c in impl_result["palette"]:
        best, bd = 0, float("inf")
        for i, s in enumerate(ref_palette):
            d = d_e(parse_hex(s["hex"]), parse_hex(c["hex"]))
            if d < bd:
                bd, best = d, i
        entry = dict(c)
        entry["deltaE"] = bd
        assigned[best].append(entry)

    significant_impl = [c for c in impl_result["palette"] if c["coverage"] >= SIGNIFICANT_COVERAGE]

    entries = []
    for i, s in enumerate(ref_palette):
        group = assigned[i]
        cov = sum(g["coverage"] for g in group)
        # 显著参考色的「最近实现色」只在显著实现簇里找:亚百分比残渣不算保留
        candidates = significant_impl if (s.get("coverage", 0) >= SIGNIFICANT_COVERAGE
                                          and significant_impl) else impl_result["palette"]
        nearest, nd = None, float("inf")
        for c in candidates:
            d = d_e(parse_hex(s["hex"]), parse_hex(c["hex"]))
            if d < nd:
                nd, nearest = d, c["hex"]
        entries.append({
            "specHex": s["hex"], "role": s.get("role", "unassigned"),
            "nearestImageHex": nearest, "deltaE": round(nd, 2),
            "specCoverage": s.get("coverage", 0.0), "imageCoverage": round(cov, 4),
        })

    # 实现簇逐簇计分:显著错误色块不得被加权平均掩盖
    impl_clusters = []
    for c in impl_result["palette"]:
        best, bd, role = None, float("inf"), None
        for s in ref_palette:
            d = d_e(parse_hex(c["hex"]), parse_hex(s["hex"]))
            if d < bd:
                bd, best, role = d, s["hex"], s.get("role")
        impl_clusters.append({
            "imageHex": c["hex"], "imageCoverage": c["coverage"],
            "nearestSpecHex": best, "nearestSpecRole": role, "deltaE": round(bd, 2),
        })

    # mean ΔE 按实现侧实际覆盖加权;遗漏色由 drift 与参考侧 max 暴露
    weighted = sum(c["deltaE"] * c["imageCoverage"] for c in impl_clusters)
    weight = sum(c["imageCoverage"] for c in impl_clusters)
    mean_de = weighted / weight if weight > 0 else 0.0
    drift = sum(abs(e["specCoverage"] - e["imageCoverage"]) for e in entries)

    sig_impl_de = [c["deltaE"] for c in impl_clusters if c["imageCoverage"] >= SIGNIFICANT_COVERAGE]
    sig_ref_de = [e["deltaE"] for e in entries if e["specCoverage"] >= SIGNIFICANT_COVERAGE]
    max_de = max([0.0] + sig_impl_de + sig_ref_de)

    passed = (mean_de <= THRESHOLD_MEAN_DE and max_de <= THRESHOLD_MAX_DE
              and drift <= THRESHOLD_DRIFT)
    return {
        "entries": entries,
        "implementationClusters": impl_clusters,
        "meanDeltaE": round(mean_de, 2),
        "maxDeltaE": round(max_de, 2),
        # 保留足够精度解释边界失败(如 0.3502 > 0.35)
        "coverageDrift": round(drift, 4),
        "measurement": {"k": impl_k, "reference_k": ref_k},
        "thresholds": {
            "meanDeltaE": THRESHOLD_MEAN_DE,
            "maxDeltaE": THRESHOLD_MAX_DE,
            "coverageDrift": THRESHOLD_DRIFT,
            "significantCoverage": SIGNIFICANT_COVERAGE,
        },
        "pass": passed,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="ΔE 保真验证(G39):mean ΔE≤5 / max ΔE≤20 / coverage drift≤0.35,逐色报告"
    )
    parser.add_argument("image", help="实现图(.png;JPEG 需 Pillow)")
    parser.add_argument("--reference", required=True,
                        help="参考:参考图(.png)或测量 spec JSON(measure-colors 输出)")
    parser.add_argument("--k", type=int, default=None,
                        help="测量簇数(参考为图时生效;spec 自带 k 时以 spec 为准)")
    args = parser.parse_args(argv)

    mc = _load_measure_module()
    for p in (args.image, args.reference):
        if not os.path.isfile(p):
            print("verify-color-fidelity: UNMEASURED —— 文件不存在: %s" % p, file=sys.stderr)
            return 2
    try:
        ref_palette, ref_k = load_reference(args.reference, args.k)
        impl_result = mc.measure_image(args.image, ref_k)
    except mc.UnmeasurableError as exc:
        print(json.dumps({"measured": False, "unmeasured_reason": str(exc)}, ensure_ascii=False))
        print("verify-color-fidelity: UNMEASURED —— %s" % exc, file=sys.stderr)
        return 2

    report = verify(impl_result, ref_palette, ref_k)
    report["implementation"] = os.path.basename(args.image)
    report["reference"] = os.path.basename(args.reference)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    verdict = "PASS" if report["pass"] else "FAIL"
    print("%s — mean ΔE %.2f, max ΔE %.2f, coverage drift %.4f" % (
        verdict, report["meanDeltaE"], report["maxDeltaE"], report["coverageDrift"]),
        file=sys.stderr)
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
