#!/usr/bin/env python3
"""draw-md 产物文档规范性检查脚本。

退出码: 见 scripts/EXIT-CODES.md(0=看了没问题 / 1=看了有问题 / 2=没能检查;#16)
        —— 0: 检查跑完且无 error(warning 不拦截) / 1: 有 error,含 token.md 产物缺失 /
           2: 目标目录不存在、检查器配置(framework/vocabulary)缺失或目录内 0 个待检 md
           (未测量不得记为通过)。

用法:
    python3 scripts/validate-draw-md.py [target_dir] [--token-file PATH] [--framework-file PATH] [--format {text,json}]

默认 target_dir = examples/ui-markdown/。
默认 token-file  = {target_dir}/token.md
默认 framework-file = references/framework/index.md
默认 format      = text
退出码: 见 scripts/EXIT-CODES.md 三态(0=通过,warning 不拦截 / 1=有 error / 2=没能检查)。
依赖: Python 3 标准库(无第三方依赖)。

输出格式:
  text (默认): 人类可读,含头部信息、逐条 [ERROR]/[WARN] 发现、末尾统计。
  json:        机器可读,stdout 仅输出 JSON 数组,每个元素形如
                {"file","line","severity","rule","message"}
                (前置错误如目录/文件缺失时输出 [] 并将错误写至 stderr)。
                退出码语义不变,调用方可据 exit code 判定通过与否。

检查项(每项对应一个 rule 标识,见 R_* 常量):
  1. 颜色/icon token 悬空引用(error)            rule=token-ref
  2. 颜色硬编码字面量(error)                     rule=color-literal
  3. 组件类型字段缺失或自创 slug(error/warning)  rule=component-slug
  4. frontmatter 必填字段缺失(error)             rule=frontmatter
  5. 章节顺序错误(warning,仅 ui/ 一级页面)       rule=section-order
  6. 二级页面文件位置(error,仅 ui/ 直接子文件)   rule=page-location
  7. 组件参数表缺 action 字段(error)             rule=action-field
  8. 暗色模式 token 引用覆盖(warning)            rule=dark-mode
  9. 交互组件缺 aria-label(error)               rule=aria-label
  10. 触控目标分端判定(原生 <44 error;           rule=touch-target
      Web/未知 <24 error、24-43 warning)
  11. 动效 ≤400ms(error;弹簧路线显式豁免时降      rule=motion-duration
      级 WARN,豁免须同时声明 spring 路线与
      damping/response 参数)
  12. 卡片 radius 违规(error)                    rule=card-radius
  13. z-index 字面量违规(error)                  rule=z-index
  14. 文本容器固定宽度(warn,组件类型含 text)    rule=fixed-width-text
  15. CSS 物理方向属性(warn,行内 ltr-only        rule=physical-property
      标注豁免;frontmatter dir=rtl 时升 ERROR)
  16. px 数值合理性:负值/超 3840px(error)        rule=numeric-sanity
  17. organisms/ 引用存在性(error)               rule=organism-ref
  18. frontmatter components slug 对齐            rule=fm-components
      (自创 error;术语库模式名 warn,应移 pattern 字段)
  19. frontmatter pattern slug 合法性(error,      rule=pattern-slug
      须为 vocabulary 登记模式)
  20. 方向契约块四字段缺失(error,仅 ui/ 页面,     rule=direction-contract
      须在首个 ## 章节前,写法 **thesis**: 等)
  21. 表格值列裸 token 名(warn,icon-/motion- 族    rule=bare-token
      未加 {} 引用形式)

frontmatter 可选契约字段:
  - platform: mobile|web|ios|android|harmony|flutter(端型,触控阈值分端判定)
  - dir: ltr|rtl(书写方向;rtl 时检查 15 升 ERROR)
  - spec_version: 契约版本(当前 1;非 1 时 WARN 提示按 v1 规则可能有漏检)
"""

import argparse
import json
import os
import re
import sys

# 共用模块(同目录下的 maliang_common.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maliang_common import parse_frontmatter as _shared_parse_frontmatter
from maliang_common import (  # noqa: F401 —— TOKEN_REF_RE re-export 供本文件多处使用
    TOKEN_REF_RE,
    is_action_row,
    iter_token_refs,
    parse_token_names,
)


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# frontmatter 必填字段
REQUIRED_FRONTMATTER_FIELDS = [
    "name",
    "description",
    "background",
    "updated",
    "version",
    "components",
]

# 已知二级页面 slug(直接放在 ui/ 根目录算 error,应放子目录如 ui/setting/)
SECONDARY_PAGE_SLUGS = {
    "about",
    "feedback",
    "privacy",
    "terms",
    "login",
    "signup",
    "forgot-password",
    "agreement",
    "about-us",
    "register",
    "reset-password",
}

# token 引用形式 {token-name}(kebab-case)—— 单一实现在 maliang_common,
# 与 ui-graph token-usage 共享,防「什么算 token 引用」两处判定漂移
# (re-export 见文件头 import)

# 颜色字面量:#RRGGBBAA / #RRGGBB / #RGB / rgba(...) / rgb(...)
HEX_COLOR_RE = re.compile(r"#[0-9A-Fa-f]{8}\b|#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")
RGBA_COLOR_RE = re.compile(r"rgba?\([^)]*\)", re.IGNORECASE)

# markdown 表格分隔行(如 | --- | --- |)——共享单源在 maliang_common,本文件只 re-export 供行级扫描使用
from maliang_common import TABLE_SEP_RE  # noqa: E402

# kebab-case 标识符
KEBAB_RE = re.compile(r"[a-z][a-z0-9-]*")

# 暗色 token 引用形式 {xxx-dark}
DARK_TOKEN_REF_RE = re.compile(r"\{[a-z][a-z0-9-]*-dark\}")

# 毫秒时长字面量 \d+ms
MS_DURATION_RE = re.compile(r"(\d+)ms")

# 像素尺寸字面量 \d+px
PX_VALUE_RE = re.compile(r"(\d+)px")

# 交互组件 slug(参数表需含 aria-label)
INTERACTIVE_SLUGS = {"button", "icon", "input", "link"}

# 可点击组件 slug(触控区需 ≥44px)
CLICKABLE_SLUGS = {"button", "icon", "link"}

# 触控目标分端阈值(px,对齐 ux-rules.md §5 分层口径):
# - 原生移动端(iOS/Android/鸿蒙)按平台规范 44pt/48dp/44vp,<44 判 ERROR;
# - Web 按 WCAG 2.2 2.5.8 AA 最低 24×24 CSS px,<24 判 ERROR,24-43 判 WARN
#   (提示 Web 最低 24px 合规,推荐 44px)。
# 平台出处：页面 frontmatter 可选 platform 字段(draw-md 契约未强制声明);
# 未声明按 Web/未知处理,不误杀 24-43px 的合规 Web 目标。
TOUCH_TARGET_MIN = 44
TOUCH_TARGET_MIN_WEB = 24
MOBILE_PLATFORMS = {"ios", "android", "harmony", "harmonyos", "arkts", "flutter"}

# 规则标识(用于 --format json 输出的 rule 字段;每项检查一个稳定标识)。
# ux-rules 回链:能对上 references/meta/ux-rules.md slug 的在行内标注 slug,
# 对不上的注明"无 ux-rules 对应"(结构/token 契约项),与 ux-rules.md 文末声明一致。
RULE_TOKEN_REF = "token-ref"              # 无 ux-rules 对应(token.md 契约项)
RULE_COLOR_LITERAL = "color-literal"      # 无 ux-rules 对应(token.md 契约项)
RULE_COMPONENT_SLUG = "component-slug"    # 无 ux-rules 对应(framework 契约项)
RULE_FRONTMATTER = "frontmatter"          # 无 ux-rules 对应(结构合规项)
RULE_ACTION_FIELD = "action-field"        # 无 ux-rules 对应(draw-md 契约项)
RULE_SECTION_ORDER = "section-order"      # 无 ux-rules 对应(结构合规项)
RULE_PAGE_LOCATION = "page-location"      # 无 ux-rules 对应(结构合规项)
RULE_DARK_MODE = "dark-mode"              # 无 ux-rules 对应(color.md 第 5 节)
RULE_ARIA_LABEL = "aria-label"            # ux-rules slug: aria-labels
RULE_TOUCH_TARGET = "touch-target"        # ux-rules slug: touch-target-44 + web-target-size-24
RULE_MOTION_DURATION = "motion-duration"  # 无 ux-rules 对应(micro-interactions.md 时长预算)
RULE_CARD_RADIUS = "card-radius"          # 无 ux-rules 对应(radius.md 阶梯)
RULE_Z_INDEX = "z-index"                  # 无 ux-rules 对应(token.md z-index 档)
RULE_FIXED_WIDTH_TEXT = "fixed-width-text"        # ux-rules slug: fixed-width-text(§6, WARN)
RULE_PHYSICAL_PROPERTY = "physical-property"      # ux-rules slug: physical-property(§12, WARN)
RULE_NUMERIC_SANITY = "numeric-sanity"            # 无 ux-rules 对应(参数表数值契约项)
RULE_ORGANISM_REF = "organism-ref"                # 无 ux-rules 对应(organisms 复用契约项)
RULE_FM_COMPONENTS = "fm-components"              # 无 ux-rules 对应(framework 契约项)
RULE_PATTERN_SLUG = "pattern-slug"                # 无 ux-rules 对应(vocabulary 契约项)
RULE_DIRECTION_CONTRACT = "direction-contract"    # 无 ux-rules 对应(draw-md 方向契约 MUST)
RULE_BARE_TOKEN = "bare-token"                    # 无 ux-rules 对应(token 引用形式契约)

# 当前 ui-markdown 契约版本(与 draw-md.md「页面 markdown 契约」同步演进;
# frontmatter spec_version 声明未来版本时校验器按本版本规则检查并 WARN)
SPEC_VERSION_CURRENT = "1"

# 方向契约块四字段(加粗标注形式 **thesis**: …,位于 frontmatter 后、
# 首个 ## 章节之前;draw-md.md「方向契约块」MUST 项)
DIRECTION_CONTRACT_FIELDS = (
    "thesis",
    "own-world",
    "first-viewport",
    "signature-interaction",
)

# px 数值(带符号、可选小数与科学计数法):负值/超上限即非物理合理值
# (1e3px 类写法同样要进数值比较,防绕过上限检查)
PX_SIGNED_RE = re.compile(r"(-?\d+(?:\.\d+)?(?:e-?\d+)?)px", re.IGNORECASE)
PX_VALUE_MAX = 3840  # 常见设计画布上限(4K 宽),超出疑为笔误

# organisms 引用(organisms/<name>.md 子串,兼容 ../organisms/ 相对链接;
# 大小写不敏感——Windows/macOS 文件系统不区分大小写,Linux CI 区分,
# 非规范大小写引用在 CI 上必断链,按 error 报出而不是静默放过)
ORGANISM_REF_RE = re.compile(
    r"organisms/([a-z0-9][a-z0-9-/]*\.md)", re.IGNORECASE)

# 表格值列裸 token 名:icon-/motion- 族未加 {} 引用形式(lookbehind 排除
# {icon-x} 引用;反引号不豁免——`icon-x` 同样是逃逸校验的裸名;只扫值列,
# 字段名列如 icon-right 不误报)
BARE_TOKEN_NAME_RE = re.compile(r"(?<!\{)\b(?:icon|motion)-[a-z][a-z0-9-]*(?![\w}])")

# z-index 字面量(匹配 z-index: <数字> 形式,排除 token 引用 {z-index-*})
Z_INDEX_LITERAL_RE = re.compile(
    r"z-index\s*[:=]\s*\d+", re.IGNORECASE
)

# 弹簧路线显式标记(检查 11 豁免条件之一):motion-model: spring /
# timing: spring / spring-route 注记 / spring(...) 调用形式。
# ease-spring 是 cubic-bezier 近似(有固定时长,仍受 400ms 硬门),不含
# spring( 调用形式与独立 spring 词,不会误匹配。
SPRING_ROUTE_RE = re.compile(
    r"motion-model\s*[:=]\s*spring|timing\s*[:=]\s*spring\b|\bspring-route\b"
    r"|spring\s*\(",
    re.IGNORECASE,
)

# 弹簧参数声明(检查 11 豁免条件之二):damping / dampingFraction /
# bounce / response / stiffness 之一带数值。豁免必须同时声明参数,
# 防止只写 spring 二字即绕过硬门(显式条件,非放宽阈值)。
SPRING_PARAMS_RE = re.compile(
    r"(?:damping(?:fraction)?|bounce|response|stiffness)\s*[:=]\s*-?\d+(?:\.\d+)?",
    re.IGNORECASE,
)

# CSS 物理方向属性(harden 可正则子集):margin/padding/border 的
# left/right 物理变体,RTL 语境应改逻辑属性 -inline-start/-inline-end。
# top/bottom 不随书写方向翻转,不收;`(?<![\w-])` 防 "sub-margin-left" 类误配。
PHYSICAL_MARGIN_PADDING_RE = re.compile(
    r"(?<![\w-])(?:margin|padding|border)-(?:left|right)\s*[:=]",
    re.IGNORECASE,
)
TEXT_ALIGN_PHYSICAL_RE = re.compile(
    r"text-align\s*[:=]\s*(left|right)\b", re.IGNORECASE
)


# ---------------------------------------------------------------------------
# 解析函数
# ---------------------------------------------------------------------------


def parse_token_file(path):
    """解析 token.md,提取所有 token 名。

    实现委托 maliang_common.parse_token_names(单一实现,与 ui-graph
    token-usage 共用,防两处解析漂移)。覆盖:颜色(color-*)/字号
    (font-*)/图标(icon-*)/间距(spacing-*)/圆角(radius-*)/边框
    (border-*)以及暗色模式表(同名去重)。
    返回 set of str;文件不存在返回空 set。
    """
    return parse_token_names(path)


def parse_framework_file(path):
    """解析 framework/index.md,提取所有组件 slug(现 56 类,以文件实测为准)。

    遍历所有 header 首列为 "组件类型" 的表格,收集 body 行首列的
    kebab-case slug。返回 set of str;文件不存在返回空 set。
    """
    slugs = set()
    if not os.path.isfile(path):
        return slugs
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    in_slug_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_slug_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        first = cells[0] if cells else ""
        if first == "组件类型":
            in_slug_table = True
            continue
        if TABLE_SEP_RE.match(line):
            continue
        if in_slug_table and first and KEBAB_RE.fullmatch(first):
            slugs.add(first)
    return slugs


def parse_vocabulary_slugs(vocab_dir):
    """解析 references/vocabulary/*.md,收集术语库登记的模式 slug。

    审计 P0 配套:framework 45 类是组件抽象,charts/search 等术语库模式是
    区块抽象,组件类型字段引用术语库模式名(如 chart-line)需在契约下合法
    表达,不应按自创 slug 报 error。取各表首列反引号包裹的 kebab-case slug
    (与 parse_framework_file 同风格,非表格/非纯 slug 单元格自然跳过)。
    返回 set of str;目录不存在返回空 set。
    """
    slugs = set()
    if not os.path.isdir(vocab_dir):
        return slugs
    cell_re = re.compile(r"`([a-z][a-z0-9-]*)`")
    for fn in sorted(os.listdir(vocab_dir)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(vocab_dir, fn)
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                stripped = line.strip()
                if not stripped.startswith("|"):
                    continue
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                first = cells[0] if cells else ""
                m = cell_re.fullmatch(first)
                if m:
                    slugs.add(m.group(1))
    return slugs


def parse_frontmatter(text):
    """从 markdown 文本提取 YAML frontmatter(委托共用模块,支持多行字符串)。

    返回 dict: 字段名 -> 原始值字符串(去首尾空白,保留引号)。
    无 frontmatter 返回空 dict。
    """
    return _shared_parse_frontmatter(text)


def _strip_quotes(v):
    """去掉值两端的引号(单引号或双引号)。委托共用模块。"""
    from maliang_common import strip_quotes as _sq
    return _sq(v)


def _extract_param_tables(lines):
    """提取所有"参数表"(header 含"参数"的 markdown 表)。

    返回 list of (header_line_no, rows),rows = list of (line_no, cells)。
    共享实现见 maliang_common.parse_table_rows,本函数只固化"参数"这一 header 约定。
    """
    import maliang_common

    return maliang_common.parse_table_rows(lines, lambda cells: "参数" in cells)


def _extract_slugs_from_value(value):
    """从"组件类型"值单元格提取 slug 列表(反引号包裹的部分)。

    例: "`input` + `icon`(P0 + P1,组合:...)" -> ["input", "icon"]
        "`navigation`(P1,导航容器)"            -> ["navigation"]
    """
    return re.findall(r"`([^`]+)`", value)


def _find_blockquote_type(lines, header_line):
    """在参数表(header 行)上方最多 3 行内查找 `> **组件类型**:` 引用块。

    draw-md.md 规定:双列对比表(如 dock 选中/未选中态)的组件类型标注在
    表前引用块中。找到返回 (line_no, slugs),否则返回 None。
    """
    blockquote_re = re.compile(r"^>\s*\*\*组件类型\*\*[:：]?(.*)$")
    for offset in range(1, 4):
        idx = header_line - 1 - offset
        if idx < 0:
            break
        m = blockquote_re.match(lines[idx].strip())
        if m:
            return (idx + 1, _extract_slugs_from_value(m.group(1)))
        if lines[idx].strip().startswith("|"):
            break  # 遇到另一张表即停
    return None


# ---------------------------------------------------------------------------
# 检查函数(每个返回 list of (severity, file, line, message))
# ---------------------------------------------------------------------------


def check_token_references(rel_path, lines, valid_tokens):
    """检查 1:颜色/icon token 悬空引用(error)。

    扫描所有 {token-name} 形式引用,若 token 未在 token.md 定义则报 error。
    跳过 action 字段行(| action |...),因为其中的 {xxx} 通常是 URL 查询参数
    或 JS 模板占位符(如 {input-value}),不是设计 token——跳过谓词
    is_action_row 与引用正则均在 maliang_common 单一实现(ui-graph 共用)。
    """
    results = []
    for i, names in iter_token_refs(enumerate(lines, 1)):
        for name in names:
            if name not in valid_tokens:
                results.append(
                    ("ERROR", rel_path, i, "悬空 token 引用: {" + name + "}")
                )
    return results


def check_color_literals(rel_path, lines):
    """检查 2:颜色硬编码字面量(error)。

    扫描 #RRGGBB / #RGB / #RRGGBBAA / rgba() / rgb(),报 error。
    跳过表格分隔行。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        for m in HEX_COLOR_RE.finditer(line):
            results.append(
                (
                    "ERROR",
                    rel_path,
                    i,
                    "颜色硬编码字面量: " + m.group(0) + ",应引用 token",
                )
            )
        for m in RGBA_COLOR_RE.finditer(line):
            results.append(
                (
                    "ERROR",
                    rel_path,
                    i,
                    "颜色硬编码字面量: " + m.group(0) + ",应引用 token",
                )
            )
    return results


def check_component_slugs(rel_path, lines, valid_slugs, vocab_slugs=None):
    """检查 3:组件类型字段缺失或自创 slug(error/warning)。

    参数表(header 含"参数")无"组件类型"行 -> warning;
    组件类型值含不在 framework 组件类且不在术语库的 slug -> error。
    references/vocabulary/*.md 登记的模式 slug(如 chart-line / filter-chip)
    放行:framework 组件类是组件抽象,charts/search 等术语库模式是区块抽象,
    需在组件类型字段合法表达(审计 P0-3);由 main() 解析 vocabulary 目录传入。
    注意:draw-md.md「模式引用」节另规定 vocabulary 模式名应走 pattern 字段、
    不得混入组件类型——两条裁决并存,最终归一待契约侧决策(见
    tests/test_validate_draw_md.py TestComponentSlugs 用例注释)。
    双列对比表允许用表前 `> **组件类型**:` 引用块标注(draw-md.md 规范),
    引用块与表格行二选一即可,两者皆无才报 warning。
    """

    def _invented(slug):
        return slug not in valid_slugs and not (vocab_slugs and slug in vocab_slugs)

    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            blockquote = _find_blockquote_type(lines, header_line)
            if blockquote is not None:
                bq_line_no, bq_slugs = blockquote
                for slug in bq_slugs:
                    if _invented(slug):
                        results.append(
                            (
                                "ERROR",
                                rel_path,
                                bq_line_no,
                                "自创组件 slug: "
                                + slug
                                + ",应引用 framework/index.md 组件类"
                                + "或 references/vocabulary/ 已登记 slug",
                            )
                        )
                continue
            results.append(
                ("WARN", rel_path, header_line, "组件参数表缺'组件类型'字段")
            )
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        for slug in _extract_slugs_from_value(value):
            if _invented(slug):
                results.append(
                    (
                        "ERROR",
                        rel_path,
                        line_no,
                        "自创组件 slug: "
                        + slug
                        + ",应引用 framework/index.md 组件类"
                        + "或 references/vocabulary/ 已登记 slug",
                    )
                )
    return results


def check_frontmatter(rel_path, text):
    """检查 4:frontmatter 必填字段缺失(error);background 必须引用 token;
    可选契约字段取值校验(dir 须 ltr|rtl;spec_version 非 1 时 WARN)。"""
    results = []
    fm = parse_frontmatter(text)
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm or not fm[field]:
            results.append(("ERROR", rel_path, 0, "frontmatter 缺失字段: " + field))
    bg = _strip_quotes(fm.get("background", ""))
    if bg and not TOKEN_REF_RE.search(bg):
        results.append(
            ("ERROR", rel_path, 0, "frontmatter background 未引用 token: " + bg)
        )
    dir_v = _strip_quotes(fm.get("dir", ""))
    if dir_v and dir_v not in ("ltr", "rtl"):
        results.append(
            ("ERROR", rel_path, 0,
             "frontmatter dir 取值非法: " + dir_v + "(须 ltr|rtl)")
        )
    sv = _strip_quotes(fm.get("spec_version", ""))
    if sv and sv != SPEC_VERSION_CURRENT:
        results.append(
            ("WARN", rel_path, 0,
             "spec_version=" + sv + " 非当前契约版本(" + SPEC_VERSION_CURRENT
             + "),按 v" + SPEC_VERSION_CURRENT + " 规则检查可能有漏检")
        )
    return results


def check_action_field(rel_path, lines):
    """检查 7:组件参数表缺 action 字段(error)。

    每个组件参数表(header 含"参数")MUST 含"action"行,描述组件交互行为
    五元组(tap/state/db/api/long-press;输入类可扩展 submit/focus/blur/input)。
    双列对比表(如 dock 选中/未选中态)的 action 在表内,首列应为 "action"。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        has_action = False
        for line_no, cells in rows:
            if cells and cells[0] == "action":
                has_action = True
                break
        if not has_action:
            results.append(
                (
                    "ERROR",
                    rel_path,
                    header_line,
                    "组件参数表缺 'action' 字段(交互行为五元组 tap/state/db/api/long-press)",
                )
            )
    return results


def check_section_order(rel_path, lines):
    """检查 5:章节顺序错误(warning,仅 ui/ 一级页面)。

    第一章(首个 ## 标题)应含"导航"/"nav-bar";最后一章应含"dock"/"底部"。
    """
    results = []
    h2 = []
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^(#{2,3})\s+(.*)$", line)
        if m and m.group(1) == "##":
            h2.append((i, m.group(2).lower()))
    if not h2:
        return results
    first_title = h2[0][1]
    last_title = h2[-1][1]
    if not ("导航" in first_title or "nav-bar" in first_title or "nav" in first_title):
        results.append(("WARN", rel_path, h2[0][0], "章节顺序: 第一章非导航"))
    if not ("dock" in last_title or "底部" in last_title):
        results.append(("WARN", rel_path, h2[-1][0], "章节顺序: 最后一章非 dock"))
    return results


def check_secondary_pages(rel_path):
    """检查 6:二级页面文件位置(error,仅 ui/ 直接子文件)。

    若 ui/ 根目录下存在 about/feedback/privacy 等已知二级页面 slug 文件,
    报 error,建议放入子目录(如 ui/setting/<slug>.md)。
    """
    results = []
    m = re.match(r"^ui/([a-z0-9-]+)\.md$", rel_path)
    if not m:
        return results
    slug = m.group(1)
    if slug in SECONDARY_PAGE_SLUGS:
        suggested = "ui/setting/" + slug + ".md"
        results.append(("ERROR", rel_path, 0, "二级页面应放在子目录: " + suggested))
    return results


def check_dark_mode_coverage(rel_path, lines, valid_tokens=None):
    """检查 8:暗色模式 token 引用覆盖(warning)。

    合规判定(满足任一即合规,对齐 R-validation-007 约束 1):
    - 含 -dark 后缀的 token 引用(正则 \\{xxx-dark\\}),OR
    - 含 `## 暗色模式` 章节(含编号变体,如 `## 6. 暗色模式`)
    两者均无则报 warning,提示暗色模式覆盖缺失(AUDIT-REPORT G01)。
    valid_tokens 参数为兼容现有 check_* 签名,本检查不依赖它。
    """
    results = []
    has_dark_token = False
    has_dark_section = False
    for line in lines:
        if DARK_TOKEN_REF_RE.search(line):
            has_dark_token = True
            break
    if not has_dark_token:
        for line in lines:
            stripped = line.lstrip("#").strip().lstrip()
            # 兼容 "## 暗色模式" / "## 6. 暗色模式" / "### 暗色模式" 等
            if "暗色模式" in stripped and not stripped.startswith("|"):
                has_dark_section = True
                break
    if not has_dark_token and not has_dark_section:
        results.append(
            (
                "WARN",
                rel_path,
                0,
                "页面未引用任何 dark token 且无'## 暗色模式'章节,暗色模式覆盖缺失",
            )
        )
    return results


def check_aria_labels(rel_path, lines):
    """检查 9:交互组件 aria-label 可访问性(error)。

    识别交互组件参数表(组件类型含 button/icon/input/link 之一),
    检查参数表是否含 aria-label 字段,缺失返回 error(AUDIT-REPORT G02)。
    容器组件(navigation 等)不检查。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        interactive = [s for s in slugs if s in INTERACTIVE_SLUGS]
        if not interactive:
            continue
        has_aria = False
        for _, row_cells in rows:
            if row_cells and "aria-label" in row_cells[0].lower():
                has_aria = True
                break
        if not has_aria:
            results.append(
                (
                    "ERROR",
                    rel_path,
                    line_no,
                    "交互组件 " + "+".join(interactive) + " 缺少 aria-label 字段",
                )
            )
    return results


def check_touch_target(rel_path, lines, platform=""):
    """检查 10:可点击组件触控目标分端判定。

    识别可点击组件(组件类型含 button/icon/link 之一),解析 width/height
    字段(正则 \\d+px),按端分阈值(AUDIT-REPORT G03 + P0 触控口径分裂修复):
    - platform ∈ MOBILE_PLATFORMS(原生移动端): <44px 判 ERROR
      (44pt/48dp/44vp 平台规范档);
    - Web 或平台未声明: <24px 判 ERROR(WCAG 2.2 2.5.8 AA 下限),24-43px
      判 WARN(提示 Web 最低 24×24 合规,推荐 44px)。
    match-parent 跳过(非定值,继承父级)。
    """
    results = []
    native = platform in MOBILE_PLATFORMS
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        if not any(s in CLICKABLE_SLUGS for s in slugs):
            continue
        for row_line_no, row_cells in rows:
            if not row_cells:
                continue
            field = row_cells[0].lower()
            if (
                "width" not in field
                and "height" not in field
                and "宽度" not in field
                and "高度" not in field
            ):
                continue
            row_value = row_cells[1] if len(row_cells) > 1 else ""
            if "match-parent" in row_value.lower():
                continue
            m = PX_VALUE_RE.search(row_value)
            if m:
                size = int(m.group(1))
                if native:
                    if size < TOUCH_TARGET_MIN:
                        results.append(
                            (
                                "ERROR",
                                rel_path,
                                row_line_no,
                                "可点击组件 "
                                + str(size)
                                + "px <44px(原生移动端 44pt/48dp/44vp),触控区不足",
                            )
                        )
                elif size < TOUCH_TARGET_MIN_WEB:
                    results.append(
                        (
                            "ERROR",
                            rel_path,
                            row_line_no,
                            "可点击组件 "
                            + str(size)
                            + "px <24px,低于 Web WCAG 2.2 2.5.8 AA 下限",
                        )
                    )
                elif size < TOUCH_TARGET_MIN:
                    results.append(
                        (
                            "WARN",
                            rel_path,
                            row_line_no,
                            "可点击组件 "
                            + str(size)
                            + "px:Web 最低 24px 合规,推荐 44px;"
                            "移动端产物应在 frontmatter 声明 platform",
                        )
                    )
    return results


def check_motion_duration(rel_path, lines):
    """检查 11:动效 duration ≤400ms(error),弹簧路线显式豁免。

    扫描 \\d+ms 模式,>400 返回 error(AUDIT-REPORT G06)。
    引用 token(如 {duration-slower})不含 \\d+ms,自然跳过。
    spring 豁免(显式条件,非放宽阈值):同一行同时声明
    弹簧路线(SPRING_ROUTE_RE:motion-model: spring / spring(...) /
    spring-route)与弹簧参数(SPRING_PARAMS_RE:damping/response 等
    带数值)时,该行 ms 值解释为落定保险丝,降级 WARN 留痕——弹簧无
    固定时长,400 上限只是兜底断路器。只写 spring 路线不写参数,豁免
    不成立,仍报 error 并提示补参数;完全无 spring 标记照旧 error。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        has_route = SPRING_ROUTE_RE.search(line) is not None
        has_params = SPRING_PARAMS_RE.search(line) is not None
        for m in MS_DURATION_RE.finditer(line):
            duration = int(m.group(1))
            if duration <= 400:
                continue
            if has_route and has_params:
                results.append(
                    (
                        "WARN",
                        rel_path,
                        i,
                        "动效 "
                        + str(duration)
                        + "ms >400ms:弹簧路线豁免(spring 路线与 damping/response"
                        " 参数均已声明),ms 值按落定保险丝留痕",
                    )
                )
            elif has_route:
                results.append(
                    (
                        "ERROR",
                        rel_path,
                        i,
                        "动效 "
                        + str(duration)
                        + "ms >400ms 硬约束违规:声明了弹簧路线但未给 damping/"
                        "response 等参数,豁免条件不成立",
                    )
                )
            else:
                results.append(
                    (
                        "ERROR",
                        rel_path,
                        i,
                        "动效 " + str(duration) + "ms >400ms 硬约束违规",
                    )
                )
    return results


CARD_RADIUS_BANNED = (
    "{radius-md}",      # 已废弃旧词(token 词表已无此档)
    "{radius-sharp}",   # 直角档:图片 / 严谨数据表
    "{radius-subtle}",  # 控件档:标签 / chip / 输入
    "{radius-full}",    # 胶囊档:按钮 / 头像 / 开关
)


def check_card_radius(rel_path, lines):
    """检查 12:卡片组件 radius 违规(error)。

    扫描组件类型含 card 的参数表,检查 radius 字段:卡片必须用卡片档
    {radius-rounded}/{radius-lg}/{radius-xl};控件档/直角档/胶囊档与旧词
    radius-md 报 error(AUDIT-REPORT G07;档位语义见 token.md §5 圆角)。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        if not any("card" in s for s in slugs):
            continue
        for row_line_no, row_cells in rows:
            if not row_cells:
                continue
            field = row_cells[0].lower()
            if "radius" not in field and "圆角" not in field:
                continue
            row_value = row_cells[1] if len(row_cells) > 1 else ""
            for banned in CARD_RADIUS_BANNED:
                if banned in row_value:
                    results.append(
                        (
                            "ERROR",
                            rel_path,
                            row_line_no,
                            "卡片圆角必须用卡片档 {radius-rounded}/{radius-lg}/"
                            "{radius-xl},%s 不是卡片档" % banned,
                        )
                    )
                    break
    return results


def check_z_index_literals(rel_path, lines):
    """检查 13:z-index 字面量(error)。

    扫描 z-index: <数字> 形式(如 z-index: 999),报 error。
    token 引用 {z-index-modal} 不含数字字面量,自然跳过。
    跳过表格分隔行。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        for m in Z_INDEX_LITERAL_RE.finditer(line):
            results.append(
                (
                    "ERROR",
                    rel_path,
                    i,
                    "z-index 字面量: " + m.group(0) + ",应引用 {z-index-*} token",
                )
            )
    return results


def check_fixed_width_text(rel_path, lines):
    """检查 14:文本容器固定宽度(warn)。

    ux-rules slug: fixed-width-text(§6 文本韧性,WARN 级)。
    harden 可正则子集:组件类型含 text 的参数表,width/宽度 字段
    为 \\d+px 定值即报 warn——文本容器定宽对超长输入(超长词/未断行
    长串/emoji/RTL)不鲁棒,应改 min-width / max-width / match-parent /
    flex 弹性。min-/max- 前缀是加固定边界而非定宽,放行。
    """
    results = []
    for header_line, rows in _extract_param_tables(lines):
        type_row = None
        for line_no, cells in rows:
            if cells and cells[0] == "组件类型":
                type_row = (line_no, cells)
                break
        if type_row is None:
            continue
        line_no, cells = type_row
        value = cells[1] if len(cells) > 1 else ""
        slugs = _extract_slugs_from_value(value)
        if not any("text" in s for s in slugs):
            continue
        for row_line_no, row_cells in rows:
            if not row_cells:
                continue
            field = row_cells[0].lower()
            if ("width" not in field and "宽度" not in field) or "height" in field:
                continue
            if field.strip().startswith(("min-", "max-")) or "min-" in field or "max-" in field:
                continue
            row_value = row_cells[1] if len(row_cells) > 1 else ""
            if "match-parent" in row_value.lower():
                continue
            if PX_VALUE_RE.fullmatch(row_value.strip().strip("`")):
                results.append(
                    (
                        "WARN",
                        rel_path,
                        row_line_no,
                        "文本容器固定宽度 "
                        + row_value
                        + ",超长文本不鲁棒(溢出/截断);改 min-width/max-width/"
                        "match-parent/flex(ux-rules: fixed-width-text)",
                    )
                )
    return results


def check_physical_property(rel_path, lines, rtl=False):
    """检查 15:CSS 物理方向属性(warn;dir=rtl 时升 error),行内 ltr-only 豁免。

    ux-rules slug: physical-property(§12 国际化与方向)。
    harden 可正则子集:margin/padding/border-left|right 与
    text-align: left|right 在 RTL 语境需镜像,应改逻辑属性
    -inline-start/-inline-end 与 text-align: start|end。
    确与方向无关的写法可在行内标注 ltr-only 豁免(显式声明优于静默)。
    页面 frontmatter 声明 dir: rtl 时,本检查从 WARN 升为 ERROR——
    声明了 RTL 即承担逻辑属性硬门(隐性 RTL 页保持 WARN 提示)。
    """
    severity = "ERROR" if rtl else "WARN"
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        if "ltr-only" in line.lower():
            continue
        for m in PHYSICAL_MARGIN_PADDING_RE.finditer(line):
            results.append(
                (
                    severity,
                    rel_path,
                    i,
                    "物理方向属性 "
                    + m.group(0).rstrip(":=").strip()
                    + ",RTL 语境应改逻辑属性 -inline-start/-inline-end"
                    "(确与方向无关可加 ltr-only 标注;ux-rules: physical-property"
                    + (";dir=rtl 已声明,升 ERROR" if rtl else "") + ")",
                )
            )
        for m in TEXT_ALIGN_PHYSICAL_RE.finditer(line):
            results.append(
                (
                    severity,
                    rel_path,
                    i,
                    "text-align: "
                    + m.group(1)
                    + ",应改 start/end 逻辑值(RTL 自动镜像;"
                    "确与方向无关可加 ltr-only 标注;ux-rules: physical-property"
                    + (";dir=rtl 已声明,升 ERROR" if rtl else "") + ")",
                )
            )
    return results


# ---------------------------------------------------------------------------
# 检查 16-21(2026-10 契约完备性补批)
# ---------------------------------------------------------------------------


def check_numeric_sanity(rel_path, lines):
    """检查 16:px 数值合理性(error)。

    负值尺寸/间距不是物理合理值;>3840px(4K 画布上限)超出任何常见设计
    画布,疑为笔误(如把间距写成字号数量级)。两类都逃过旧检查:PX_VALUE_RE
    只匹配无符号正整数,触控检查只看下限不看上限。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        for m in PX_SIGNED_RE.finditer(line):
            value = float(m.group(1))
            if value < 0:
                results.append(
                    ("ERROR", rel_path, i,
                     "px 数值为负: " + m.group(0) + ",尺寸/间距不可为负")
                )
            elif value > PX_VALUE_MAX:
                results.append(
                    ("ERROR", rel_path, i,
                     "px 数值超上限: " + m.group(0)
                     + "(>" + str(PX_VALUE_MAX) + "px 超出常见设计画布,疑为笔误)")
                )
    return results


def check_organism_refs(rel_path, lines, existing_organisms):
    """检查 17:organisms/ 引用存在性(error)。

    页面以 markdown 链接引用 organisms/*.md(如 ../organisms/nav-bar.md);
    引用不存在的组件文件报 error。此前引用目标完全逃逸校验——写错文件名
    全绿通过,下游 draw-* 找不到复用组件。existing_organisms 为
    target_dir 下 organisms/ 的相对路径集合(None 时跳过,目录不存在)。
    """
    results = []
    if existing_organisms is None:
        return results
    existing_lower = {p.lower() for p in existing_organisms}
    for i, line in enumerate(lines, start=1):
        for m in ORGANISM_REF_RE.finditer(line):
            ref = "organisms/" + m.group(1)
            if ref.lower() not in existing_lower:
                results.append(
                    ("ERROR", rel_path, i,
                     "引用的 organisms 组件不存在: " + ref
                     + "(检查文件名,或先在 organisms/ 下产出该组件)")
                )
    return results


def _as_slug_list(value):
    """frontmatter 字段值归一为 slug 列表。

    共享 parse_frontmatter 只把 components 解析为 list,其余字段(pattern 等)
    保留字符串——inline 数组字符串 "[a, b]" 在此拆为列表,防整串被当
    单个 slug 误报。
    """
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    v = str(value or "").strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")
                if item.strip()]
    return [v] if v else []


def check_fm_components(rel_path, text, valid_slugs, vocab_slugs=None):
    """检查 18:frontmatter components 数组 slug 对齐(error/warn)。

    components 应为 framework/index.md 组件类 slug 清单(draw-md.md
    「组件类型标注规范」);此前 frontmatter 只查字段存在,自创 slug 不报。
    术语库模式 slug(如 chart-line)出现在 components → WARN,提示移至
    pattern 字段(契约:两套命名各司其职,不得混写)。
    """
    results = []
    fm = parse_frontmatter(text)
    for slug in _as_slug_list(fm.get("components", [])):
        if not slug or slug in valid_slugs:
            continue
        if vocab_slugs and slug in vocab_slugs:
            results.append(
                ("WARN", rel_path, 0,
                 "frontmatter components 含术语库模式 slug: " + slug
                 + ",区块模式应移至 pattern 字段(组件类与模式名各司其职)")
            )
        else:
            results.append(
                ("ERROR", rel_path, 0,
                 "frontmatter components 自创 slug: " + slug
                 + ",应引用 framework/index.md 组件类")
            )
    return results


def check_fm_pattern(rel_path, text, vocab_slugs):
    """检查 19:frontmatter pattern 数组 slug 合法性(error)。

    pattern 字段只能引用 references/vocabulary/ 各篇命名表登记的模式 slug;
    自创模式名报 error(此前 pattern 字段零校验)。
    """
    results = []
    if not vocab_slugs:
        return results
    fm = parse_frontmatter(text)
    for slug in _as_slug_list(fm.get("pattern", [])):
        if slug and slug not in vocab_slugs:
            results.append(
                ("ERROR", rel_path, 0,
                 "pattern 自创 slug: " + slug
                 + ",须引用 references/vocabulary/ 已登记模式(draw-md.md 禁令)")
            )
    return results


def check_direction_contract(rel_path, lines):
    """检查 20:方向契约块四字段缺失(error,仅 ui/ 页面)。

    draw-md.md「方向契约块」为每页 MUST(thesis / own-world / first-viewport /
    signature-interaction),此前零校验且示例页自身缺失。机器可查的字面
    形态:四字段在 frontmatter 之后、首个 ## 章节之前,以加粗字段名行书写
    (**thesis**: …);语义兑现仍由 preview 的 Brand Fit 人工复核。
    organisms/ 是组件文档非页面,不检查。
    """
    results = []
    region_end = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("## "):
            region_end = i
            break
    region = "\n".join(lines[:region_end])
    missing = [f for f in DIRECTION_CONTRACT_FIELDS
               if not re.search(r"\*\*" + re.escape(f) + r"\*\*", region)]
    if missing:
        results.append(
            ("ERROR", rel_path, 0,
             "方向契约块缺字段: " + ", ".join(missing)
             + "(frontmatter 后、首个 ## 章节前,写法 **字段**: …;draw-md MUST)")
        )
    return results


def check_bare_token_names(rel_path, lines):
    """检查 21:表格值列裸 token 名(warn)。

    icon-/motion- 族取值必须以 {icon-x} 引用;裸写(icon-feed)既脱离
    token 解析,也无法被悬空检查看见——示例页曾因此出现 3 个未定义图标
    全绿通过。只扫表格行的值列(cells[1:]),字段名列(如 icon-right)
    不误报;反引号不豁免(`icon-x` 同样是裸名)。
    """
    results = []
    for i, line in enumerate(lines, start=1):
        if TABLE_SEP_RE.match(line):
            continue
        stripped = line.lstrip()
        if not stripped.startswith("|"):
            continue
        if is_action_row(stripped):
            continue
        # 表头行跳过(其后紧跟分隔行):列名如 icon-filled/icon-left 是
        # 字段命名,不是取值,不该按裸 token 名报
        if i < len(lines) and TABLE_SEP_RE.match(lines[i]):
            continue
        cells = stripped.rstrip().strip("|").split("|")
        seen = set()
        for cell in cells[1:]:
            for m in BARE_TOKEN_NAME_RE.finditer(cell):
                name = m.group(0)
                if name in seen:
                    continue
                seen.add(name)
                results.append(
                    ("WARN", rel_path, i,
                     "裸 token 名: " + name + ",应写 {" + name
                     + "} 引用形式(裸名逃逸悬空检查)")
                )
    return results


# ---------------------------------------------------------------------------
# 文件收集与主流程
# ---------------------------------------------------------------------------


def collect_md_files(root):
    """递归收集 root 下所有 .md 文件(绝对路径),按路径排序。"""
    result = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".md"):
                result.append(os.path.join(dirpath, fn))
    return sorted(result)


def _tag(rule, check_results):
    """为 4-tuple 检查结果附加 rule 字段,转为 5-tuple。

    输入: check_* 返回的 (severity, file, line, message) 列表
    输出: (severity, file, line, rule, message) 列表
    """
    return [(sev, f, ln, rule, msg) for (sev, f, ln, msg) in check_results]


def run_checks(rel_path, text, lines, valid_tokens, valid_slugs, is_ui_top_level,
               vocab_slugs=None, existing_organisms=None):
    """对单个文件运行检查 1-21,返回 5-tuple 列表 (severity, file, line, rule, message)。

    检查 5 (section-order) / 检查 6 (page-location) 仅对 ui/ 直接子文件运行
    (is_ui_top_level=True);检查 20 (direction-contract) 仅对 ui/ 页面运行
    (由 rel_path.startswith("ui/") 推导,organisms 是组件文档非页面);
    检查 17 需要 existing_organisms(organisms/ 相对路径集合,目录不存在时
    None 跳过)。
    触控分端判定(检查 10)读取 frontmatter 可选 platform 字段;检查 15 的
    RTL 升级读取 frontmatter 可选 dir 字段。
    """
    results = []
    fm = parse_frontmatter(text)
    platform = _strip_quotes(fm.get("platform", "")).lower()
    rtl = _strip_quotes(fm.get("dir", "")).lower() == "rtl"
    is_page = rel_path.startswith("ui/")
    results.extend(
        _tag(RULE_TOKEN_REF, check_token_references(rel_path, lines, valid_tokens))
    )
    results.extend(_tag(RULE_COLOR_LITERAL, check_color_literals(rel_path, lines)))
    results.extend(
        _tag(
            RULE_COMPONENT_SLUG,
            check_component_slugs(rel_path, lines, valid_slugs, vocab_slugs),
        )
    )
    results.extend(_tag(RULE_FRONTMATTER, check_frontmatter(rel_path, text)))
    results.extend(
        _tag(RULE_ACTION_FIELD, check_action_field(rel_path, lines))
    )
    results.extend(
        _tag(RULE_DARK_MODE, check_dark_mode_coverage(rel_path, lines, valid_tokens))
    )
    results.extend(_tag(RULE_ARIA_LABEL, check_aria_labels(rel_path, lines)))
    results.extend(
        _tag(RULE_TOUCH_TARGET, check_touch_target(rel_path, lines, platform))
    )
    results.extend(_tag(RULE_MOTION_DURATION, check_motion_duration(rel_path, lines)))
    results.extend(_tag(RULE_CARD_RADIUS, check_card_radius(rel_path, lines)))
    results.extend(_tag(RULE_Z_INDEX, check_z_index_literals(rel_path, lines)))
    results.extend(
        _tag(RULE_FIXED_WIDTH_TEXT, check_fixed_width_text(rel_path, lines))
    )
    results.extend(
        _tag(RULE_PHYSICAL_PROPERTY,
             check_physical_property(rel_path, lines, rtl=rtl))
    )
    results.extend(
        _tag(RULE_NUMERIC_SANITY, check_numeric_sanity(rel_path, lines))
    )
    results.extend(
        _tag(RULE_ORGANISM_REF,
             check_organism_refs(rel_path, lines, existing_organisms))
    )
    results.extend(
        _tag(RULE_FM_COMPONENTS,
             check_fm_components(rel_path, text, valid_slugs, vocab_slugs))
    )
    results.extend(
        _tag(RULE_PATTERN_SLUG, check_fm_pattern(rel_path, text, vocab_slugs))
    )
    if is_page:
        results.extend(
            _tag(RULE_DIRECTION_CONTRACT,
                 check_direction_contract(rel_path, lines))
        )
    results.extend(
        _tag(RULE_BARE_TOKEN, check_bare_token_names(rel_path, lines))
    )
    if is_ui_top_level:
        results.extend(_tag(RULE_SECTION_ORDER, check_section_order(rel_path, lines)))
        results.extend(_tag(RULE_PAGE_LOCATION, check_secondary_pages(rel_path)))
    return results


def main(argv):
    parser = argparse.ArgumentParser(description="maliang draw-md 文档规范性检查")
    parser.add_argument(
        "target_dir",
        nargs="?",
        default="examples/ui-markdown",
        help="目标目录(默认 examples/ui-markdown)",
    )
    parser.add_argument(
        "--token-file", default=None, help="token.md 路径(默认 {target_dir}/token.md)"
    )
    parser.add_argument(
        "--framework-file",
        default=None,
        help="framework/index.md 路径(默认 references/framework/index.md)",
    )
    parser.add_argument(
        "--vocabulary-dir",
        default=None,
        help="references/vocabulary 目录路径(默认 references/vocabulary);"
        "其登记的模式 slug(如 chart-line)在组件类型校验中放行",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式: text(人类可读,默认) / json(机器可读,stdout 仅 JSON 数组)",
    )
    args = parser.parse_args(argv[1:])
    fmt = args.format

    target_dir = os.path.abspath(args.target_dir)
    token_file = os.path.abspath(
        args.token_file or os.path.join(target_dir, "token.md")
    )
    framework_file = os.path.abspath(
        args.framework_file
        or os.path.join(os.getcwd(), "references", "framework", "index.md")
    )
    vocabulary_dir = os.path.abspath(
        args.vocabulary_dir
        or os.path.join(os.getcwd(), "references", "vocabulary")
    )

    # 头部输出(json 模式保持 stdout 纯净,仅末尾输出 JSON 数组)
    if fmt == "text":
        print("maliang draw-md 文档规范性检查")
        print("=" * 32)
        print("目标目录: " + target_dir)
        print("Token 文件: " + token_file)
        print("Framework 文件: " + framework_file)
        print("Vocabulary 目录: " + vocabulary_dir)
        print("")

    # 目录/文件存在性(缺失即终止,显性失败)
    # 三态:#16 —— target 缺失 = 无目标(2);token.md 是 draw-md 产物,缺失 = 有问题(1);
    # framework/vocabulary 是检查器配置,缺失 = 没能检查(2)。json 模式:stdout 输出空数组 [],
    # 错误信息写 stderr
    if not os.path.isdir(target_dir):
        msg = "目标目录不存在: " + target_dir
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 2
    if not os.path.isfile(token_file):
        msg = "token 文件不存在: " + token_file
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 1
    if not os.path.isfile(framework_file):
        msg = "framework 文件不存在: " + framework_file
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 2
    if not os.path.isdir(vocabulary_dir):
        msg = "vocabulary 目录不存在: " + vocabulary_dir
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 2

    valid_tokens = parse_token_file(token_file)
    valid_slugs = parse_framework_file(framework_file)
    vocab_slugs = parse_vocabulary_slugs(vocabulary_dir)

    # 收集待检查文件
    ui_dir = os.path.join(target_dir, "ui")
    organisms_dir = os.path.join(target_dir, "organisms")
    ui_files = collect_md_files(ui_dir) if os.path.isdir(ui_dir) else []
    org_files = collect_md_files(organisms_dir) if os.path.isdir(organisms_dir) else []

    # organisms/ 相对路径集合(检查 17 引用存在性);目录不存在为 None(跳过)
    existing_organisms = None
    if os.path.isdir(organisms_dir):
        existing_organisms = set()
        for dirpath, _, filenames in os.walk(organisms_dir):
            for fn in filenames:
                if fn.endswith(".md"):
                    rel_org = os.path.relpath(
                        os.path.join(dirpath, fn), target_dir)
                    existing_organisms.add(rel_org.replace(os.sep, "/"))

    # 无目标不得记为通过(#16):目录存在但 0 个待检 md = 没能检查
    if not ui_files and not org_files:
        msg = ("无待检文件: {} 下 ui/ 与 organisms/ 均无 md"
               "(未测量不得记为通过)").format(target_dir)
        if fmt == "json":
            print("[]")
            print("[ERROR] " + msg, file=sys.stderr)
        else:
            print("[ERROR] " + msg)
        return 2

    all_results = []

    def rel(path):
        return os.path.relpath(path, target_dir)

    # ui 文件:检查 1-21 全做(检查 5/6 仅直接子文件;检查 20 由路径推导)
    for abs_path in ui_files:
        rp = rel(abs_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.splitlines()
        all_results.extend(
            run_checks(
                rp, text, lines, valid_tokens, valid_slugs,
                os.path.dirname(rp) == "ui", vocab_slugs=vocab_slugs,
                existing_organisms=existing_organisms,
            )
        )

    # organisms 文件:检查 1-19 + 21(无 5/6/20——组件文档非页面,
    # 无章节顺序约束、无方向契约块要求;检查 20 按路径前缀自动跳过)
    for abs_path in org_files:
        rp = rel(abs_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.splitlines()
        all_results.extend(
            run_checks(
                rp, text, lines, valid_tokens, valid_slugs, False,
                vocab_slugs=vocab_slugs,
                existing_organisms=existing_organisms,
            )
        )

    # 排序:error 先于 warn,再按 file、line
    severity_rank = {"ERROR": 0, "WARN": 1}
    all_results.sort(key=lambda r: (severity_rank.get(r[0], 9), r[1], r[2]))

    # 统计
    error_count = sum(1 for r in all_results if r[0] == "ERROR")
    warn_count = sum(1 for r in all_results if r[0] == "WARN")

    # 输出
    if fmt == "json":
        # 机器可读:stdout 仅输出 JSON 数组,每元素 {file,line,severity,rule,message}
        findings = [
            {
                "file": f,
                "line": ln,
                "severity": sev,
                "rule": rule,
                "message": msg,
            }
            for (sev, f, ln, rule, msg) in all_results
        ]
        print(json.dumps(findings, ensure_ascii=False))
    else:
        for sev, f, ln, _rule, msg in all_results:
            label = "[ERROR]" if sev == "ERROR" else "[WARN] "
            if ln > 0:
                print("{} {}:{} {}".format(label, f, ln, msg))
            else:
                print("{} {} {}".format(label, f, msg))
        print("")
        print("=" * 32)
        print("检查结果: {} errors, {} warnings".format(error_count, warn_count))

    # 退出码三态(#16):0=通过(warning 不拦截),1=有 error;2 只在上方"没能检查"路径返回
    if error_count > 0:
        if fmt == "text":
            print("退出码: 1")
        return 1
    if fmt == "text":
        if warn_count > 0:
            print("退出码: 0({} warnings 不拦截,见 EXIT-CODES.md 三态)".format(warn_count))
        else:
            print("退出码: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
