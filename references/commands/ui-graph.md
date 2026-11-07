# ui-graph 子命令 —— UI 关系管理与变更追踪

> 本文件是 `ui-graph` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 输入 = [`draw-md`](./draw-md.md) 产出的 `.maliang/ui-markdown/` 目录(token.md + organisms/ + ui/*.md)。
> 输出 = 六个 JSON 文件,落在 `.maliang/ui-markdown/` 下:
>   - `ui-relationships.json` — 页面层级 + 跳转关系图
>   - `ui-hash-state.json` — 每个 markdown 文件的 sha256 哈希快照（draw-md 指纹）
>   - `preview-hash-state.json` — 预览 HTML/截图清单的 sha256 快照（`--kind preview`,落在预览目录）
>   - `ui-implementation-map.json` — 逻辑 UI ↔ preview HTML ↔ 框架代码三向映射
>   - `code-hash-state.json` — 实现文件(preview HTML + 三框架代码)指纹基线（`--kind code`）
>   - `token-usage.json` — token → 引用页面反向索引 + 孤儿 token 清单
> 这是 [`draw-md`](./draw-md.md) 的**下游**:draw-md 产出页面 markdown,ui-graph 在其上做关系分析、变更检测与实现覆盖度审计,不修改 draw-md 产出本身。
> 配套脚本 [`scripts/ui-graph.py`](../../scripts/ui-graph.py) 是纯 Python 标准库实现,无第三方依赖。

---

> **CHECKPOINT 与无人值守**:无人值守时按 [`SKILL.md`](../../SKILL.md)「无人值守与 CHECKPOINT 降级」节的默认取值表执行,不逐点阻塞;自选决定与理由写入交付说明。

## 产物层目录结构

所有 ui-graph 产出落在 `.maliang/ui-markdown/`(与 draw-md 产物同目录):

```
.maliang/ui-markdown/
├── token.md                    # draw-md 产物(本子命令只读,不修改)
├── organisms/                  # draw-md 产物(只读)
├── ui/                         # draw-md 产物(只读)
├── ui-relationships.json       # ui-graph generate 产出
├── ui-hash-state.json          # ui-graph compute-hash 产出(draw-md 基线)
├── ui-implementation-map.json  # ui-graph build-impl-map 产出
├── code-hash-state.json        # ui-graph compute-hash --kind code 产出(实现基线)
└── token-usage.json            # ui-graph token-usage 产出
```

- `ui-relationships.json` — 描述 pages[](路径/名称/父级/层级/组件)与 navigations[](from/to/event/source_component),是 list-missing / check-nav / list-unimplemented 的输入。
- `ui-hash-state.json` — 记录每个 markdown 文件的 sha256 + size,供 diff-hash 检测增量变更。
- `ui-implementation-map.json` — 记录每个逻辑 UI 是否有 preview HTML 与框架代码实现,供 list-unimplemented 审计覆盖度。
- `code-hash-state.json` — impl-map 映射到的实现文件指纹,供 check-sync 判同步方向。
- `token-usage.json` — token → 页面反向索引 + 孤儿 token,供 DESIGN.md token 变更波及分析。

---

## JSON Schema

### ui-relationships.json

```json
{
  "generated_at": "2026-07-05T10:00:00+08:00",
  "target_dir": ".maliang/ui-markdown",
  "pages": [
    {
      "path": "ui/home.md",
      "name": "home",
      "parent": null,
      "depth": 1,
      "components": ["navigation", "input", "icon", "grid", "button", "list", "card"]
    },
    {
      "path": "ui/setting/about.md",
      "name": "about",
      "parent": "setting",
      "depth": 2,
      "components": ["navigation", "image", "text", "list", "button", "icon"]
    }
  ],
  "navigations": [
    {
      "from": "ui/home.md",
      "to": "ui/setting/notifications.md",
      "event": "tap",
      "source_component": null
    }
  ]
}
```

- `pages[].path` — 相对 `.maliang/ui-markdown/` 的路径(如 `ui/setting/about.md`)。
- `pages[].parent` — 父级目录名(`ui/` 直接子文件为 null;`ui/setting/about.md` 为 `"setting"`)。
- `pages[].depth` — 层级深度(`ui/home.md` = 1;`ui/setting/about.md` = 2)。
- `pages[].components` — 从 frontmatter `components` 字段解析的组件 slug 列表。
- `navigations[].from` / `to` — 均为相对 `.maliang/ui-markdown/` 的路径。
- `navigations[].event` — 触发事件(当前仅 `tap`;`submit`/`focus` 等不产生跳转,不在此列)。
- `navigations[].source_component` — 触发跳转的组件类型(v1 暂为 null,后续可增强为参数表的"组件类型"字段值)。

### ui-hash-state.json

```json
{
  "computed_at": "2026-07-05T10:00:00+08:00",
  "target_dir": ".maliang/ui-markdown",
  "files": [
    { "path": "ui/home.md", "sha256": "abc123...", "size": 2048 },
    { "path": "organisms/nav-bar.md", "sha256": "def456...", "size": 1024 }
  ]
}
```

### ui-implementation-map.json

```json
{
  "built_at": "2026-07-05T10:00:00+08:00",
  "mappings": [
    {
      "logical_ui": "ui/home.md",
      "preview_html": "preview/home/preview_home.html",
      "framework_code": {
        "harmony": "entry/src/main/ets/pages/Home.ets",
        "flutter": "lib/pages/home.dart",
        "element": "src/views/home.vue"
      },
      "status": "implemented"
    }
  ]
}
```

- `status` — `implemented`(preview + 至少一个框架都有)/ `partial`(只有一项)/ `missing`(都无)。
- `framework_code` 三键对应 [`draw-harmony`](./draw-harmony.md) / [`draw-flutter`](./draw-flutter.md) / [`draw-element`](./draw-element.md) 三个子命令的产出路径模式:
  - harmony: `**/pages/<Slug>.ets`(Slug 为 TitleCase,如 `Home`)
  - flutter: `**/pages/<slug>.dart`(slug 为 lowercase,如 `home`)
  - element: `**/views/<slug>.vue`(slug 为 lowercase,如 `home`)

---

## 子命令

### 1. generate — 生成 ui-relationships.json

解析 `.maliang/ui-markdown/` 目录,聚合页面层级与跳转关系。

```bash
python3 scripts/ui-graph.py generate [--target PATH]
# 默认 --target .maliang/ui-markdown/
# 产出 {target}/ui-relationships.json
```

流程:
1. `parse_directory(target)` — 扫描所有 .md 文件(排除 token.md),返回相对路径列表。
2. 对每个文件:`parse_frontmatter(text)` 提取 name/components,`extract_navigations(text, path)` 提取跳转。
3. 从路径推导 parent/depth(`ui/setting/about.md` → parent=`setting`, depth=2)。
4. 聚合为 `pages[]` + `navigations[]`,写 JSON。

### 2. list-missing — 列出跳转目标未生成的页面

加载 `ui-relationships.json`,对比 `navigations[].to` 与 `pages[].path`,输出未生成对应 markdown 的清单。

```bash
python3 scripts/ui-graph.py list-missing [--target PATH]
# 输出示例:
#   ui/home.md → ui/setting/notifications.md (缺失)
# 无缺失输出: 全部跳转目标已生成
```

### 3. check-nav — 检测异常跳转

加载 `ui-relationships.json`,分类输出异常:
- **自指**:`from == to`
- **循环**:A→B→A(长度 2 的环)
- **死链**:`to` 不在 `pages[].path` 中

```bash
python3 scripts/ui-graph.py check-nav [--target PATH]
```

### 4. compute-hash — 计算哈希基线（三种范围）

用 `hashlib.sha256` 计算目标文件哈希,写对应基线文件。`--kind` 决定范围（基线文件分开,不得混用）:

| --kind | 范围 | 基线文件 | 用途 |
| --- | --- | --- | --- |
| `draw-md`（默认） | draw-md 产物 `.md` 页面（排除 `token.md`） | `ui-hash-state.json` | critique backlog 指纹失效判定（只管 draw-md 产物） |
| `preview` | 预览 HTML + 截图（png/jpg/jpeg/webp/svg）+ 取证清单（`report.json` 等 JSON；排除 `selection.json` 与基线自身） | `preview-hash-state.json` | 测量收据/证据链（`receipts.py`）记录「被实测的预览状态」；预览 HTML 恰是被实测对象,证据须带产物哈希、哈希变了证据作废 |
| `code` | `ui-implementation-map.json` 映射到的实现文件（preview HTML + 三框架代码;路径相对 impl-map 的 `anchors` 锚根记录,消费侧按锚根解析,**不受运行时 cwd 影响**） | `code-hash-state.json` | `check-sync` 的实现侧基线——判「规格改了代码没跟 / 代码手改了规格没动」;实现文件缺失时**拒绝建基线**(防空测量伪造全同步) |

```bash
python3 scripts/ui-graph.py compute-hash [--target PATH] [--kind draw-md|preview|code]
# 产出 {target}/ui-hash-state.json（draw-md）、preview-hash-state.json（preview）或 code-hash-state.json（code）
# preview 示例（目标为预览产物目录）:
python3 scripts/ui-graph.py compute-hash --target .maliang/preview --kind preview
```

### 5. diff-hash — 对比哈希快照

对比当前文件哈希与对应基线文件（`--kind` 同 compute-hash,含 code）,输出 added/modified/deleted 三类变更。

```bash
python3 scripts/ui-graph.py diff-hash [--target PATH] [--kind draw-md|preview|code]
# 输出示例:
#   [added]    ui/setting/notifications.md
#   [modified] ui/home.md
#   [deleted]  ui/old-page.md
```

### 6. build-impl-map — 构建实现映射

扫描 `preview/**/*.html`(从文件名提取 slug,如 `preview_home.html` → `home`)+ 框架代码路径模式(`**/pages/<Slug>.ets` / `**/pages/<slug>.dart` / `**/views/<slug>.vue`),与 `ui-relationships.json` 的 pages 匹配,写 `ui-implementation-map.json`。

```bash
python3 scripts/ui-graph.py build-impl-map [--target PATH] [--preview-root PATH] [--code-root PATH]
# 默认 --preview-root = {target}/../preview  (即 .maliang/preview/)
# 默认 --code-root = 当前工作目录
# 产出 {target}/ui-implementation-map.json
```

### 7. list-unimplemented — 列出未实现的逻辑页面

加载 `ui-relationships.json` 与 `ui-implementation-map.json`,对比输出 `status=missing` 的页面清单。

```bash
python3 scripts/ui-graph.py list-unimplemented [--target PATH]
# 输出示例:
#   ui/setting/notifications.md (缺失原因: 无 preview_html 且无 framework_code)
```

### 8. token-usage — token 引用反向索引 + 孤儿 token

解析全部页面/organisms 的 `{token}` 引用(action 行除外——其 `{xxx}` 是 URL/JS 模板参数),产出 `token-usage.json`;token.md 里从未被引用的 token 列为孤儿(给 G02 孤儿 token 提供产物层信号)。**用途:DESIGN.md 改一个 token 后,机械回答「哪些页要重生成」。**

```bash
python3 scripts/ui-graph.py token-usage [--target PATH] [--token NAME]
# --token 只看单个 token 的波及页面:
#   token {color-brand-primary} 波及页面:
#     ui/home.md
#     ui/mine.md
```

### 9. check-sync — 规格 ↔ 实现同步状态

对比 draw-md 基线(`ui-hash-state.json`)与实现基线(`code-hash-state.json`),逐页分类(仅 status != missing 的页面):

| 状态 | 含义 | 修复 |
| --- | --- | --- |
| `in-sync` | 规格与实现均与基线一致 | — |
| `spec-ahead` | 规格已改、实现未跟 | 重跑 preview / draw-* 后重建两份基线 |
| `code-drifted` | 实现已改(手改/外部变更/删除)、规格未动 | 手改回写 ui-markdown,或在 decisions 账本登记「为什么代码是对的」 |
| `diverged` | 两侧都变 | 先人工对齐再交付 |

```bash
python3 scripts/ui-graph.py check-sync [--target PATH]
# 退出码:全部 in-sync 0 / 任一失同步 1 / 基线或 impl-map 缺失 2(没能检查,先建基线)
```

**基线节奏**(基线语义 = 「上次全部对齐时的快照」):每次全量产出/重生成后,`build-impl-map` → `compute-hash` → `compute-hash --kind code` 连跑建双基线;此后任何时点 `check-sync` 都能机械判定漂移方向。路径锚定:impl-map 记录 `anchors.preview_root` / `anchors.code_root`(以及 legacy 的 `base_dir`),实现路径相对各自锚根解析——**任何 cwd 运行 check-sync 均可**;impl-map 出现绝对路径或 `..` 穿越路径时拒绝消费(退出码 2,防越界读取)。增量重生成纪律见 [`llm-behavior.md`](../meta/llm-behavior.md) §6.2。

> **哈希盲区**:check-sync 判「变没变」,判不出「没变但错」——功能缺失 / 写死值 / 架构偏离等语义层漂移走下方「[语义漂移审计](#语义漂移审计语义层agent-执行形态吸收自-egm-drift-report)」。

---

## 语义漂移审计(语义层,agent 执行;形态吸收自 EGM Drift Report)

> check-sync 是逐字节哈希对照:只判「文件变没变」,判不出「文件没变但实现错了」。本节是它的**语义层**,由 agent 读码对照——纯脚本做不了,也不做成 `ui-graph.py` 子命令(避免伪机械检查;脚本子命令仍是 9 个)。

**时机**:交付前对 P0 页例行抽审;check-sync 判 `in-sync` 但抽查怀疑「对不上」时对目标页加审。全量逐页读码成本高,默认只审 P0 页 + check-sync 的 `code-drifted` / `diverged` 页;全量仅在用户显式要求时跑。

**流程**:

1. **取审计范围**:`ui-implementation-map.json` 的 mappings 按默认范围过滤;impl-map 缺失先跑 `build-impl-map`;
2. **逐页对照** `ui/<page>.md` 与映射到的实现文件(preview HTML / 三框架代码),只查四类漂移:

   | 类 | 判据 | 例 |
   | --- | --- | --- |
   | 功能缺失 | 规格写了、代码没有 | 参数表里的禁用态 / 空态未实现 |
   | 结构缺字段 | 数据结构比规格少字段 | 列表项规格 5 字段,代码只渲染 3 个 |
   | 写死替代动态 | 规格要求动态逻辑,代码写死 | token 引用被换字面量 / 条件分支写死 |
   | 架构偏离 | 实现用了规格外的模式/库 | 规格说复用 organisms/dock,代码自造一份 |

3. **只报差异**:有漂移的页逐条列;全匹配的页一行「无漂移」,禁止复述一致项(防报告膨胀);
4. **定级与去向**:每条漂移按 P0-P3 定级 + 给修法(注明走 redesign / draw-md / draw-* 哪条路),报告落 `.maliang/critique/drift_<date>.md`——**禁止落 `ui-markdown/`**(根级 .md 会被 `compute-hash --kind draw-md` 当页面计入基线,污染指纹);
5. **链接回填提示**:某条规格在代码里找不到对应物、且 impl-map 未记录该实现路径时,提示用户把实现路径补进对应页锚点——链接齐了,下次 `build-impl-map` 与本审计都更便宜。

**边界**:本审计只读不改——发现漂移一律移交对应子命令处置,禁止顺手改码;修复后按「基线节奏」重建基线再复审,复评同样适用 [`critique.md`](./critique.md) 的「重审上限」语义。

---

---

## 流程

0. **前置检查** —— 确认 `.maliang/ui-markdown/` 存在且含 `ui/` 子目录;若不存在,提示用户先跑 [`draw-md`](./draw-md.md) 产出页面 markdown。

   **🔴 CHECKPOINT · 输入就绪**:确认 `.maliang/ui-markdown/ui/` 至少有 1 个 .md 文件,再进入下一步。

1. **生成关系图** —— 运行 `generate` 产出 `ui-relationships.json`。

   **🔴 CHECKPOINT · 关系图就绪**:确认 `ui-relationships.json` 的 `pages[]` 非空,`navigations[]` 已提取(可能为空,若无跳转)。

2. **审计跳转完整性** —— 运行 `list-missing` + `check-nav`,识别未生成页面与异常关系。

   **🔴 CHECKPOINT · 跳转完整**:自指/循环/死链均需用户确认是 bug 还是预期(如未实现的占位跳转)。

3. **构建实现映射** —— 运行 `build-impl-map` 产出 `ui-implementation-map.json`,运行 `list-unimplemented` 输出未实现清单。

4. **变更检测(按需)** —— 当 draw-md 产出更新后,运行 `compute-hash` 刷新快照,再运行 `diff-hash` 输出变更页面清单,供前端/预览更新决策。

5. **同步判定(按需)** —— 重生成/手改后运行 `check-sync` 判定规格与实现的漂移方向;基线缺失时先按「基线节奏」补建。token 变更后运行 `token-usage --token <name>` 列波及页面。P0 页交付前按需加跑一轮「语义漂移审计」(语义层,哈希照不到「没变但错」)。

---

## 约束汇总(硬性)

- [ ] `ui-graph.py` 仅用 Python 标准库(os/sys/re/json/hashlib/argparse/datetime/pathlib),**无第三方依赖**
- [ ] `parse_directory` MUST 排除 `token.md`(它是 draw-md 的 token 锚点,非页面)
- [ ] `parse_frontmatter` MUST 处理 `components: [a, b, c]` 内联数组格式(逐行 key: value,无嵌套)
- [ ] `extract_navigations` MUST 跳过 `tap=无` 与 `tap=back`(非跳转目标)
- [ ] `extract_navigations` 的正则 `tap=→([a-z][a-z0-9/-]*)` 提取相对目标,归一化为 `ui/<to>.md`(若原始值已含 `ui/` 前缀,直接补 `.md`,避免双重前缀)
- [ ] `pages[].parent` 从路径推导:`ui/<dir>/<file>.md` → parent=`<dir>`;`ui/<file>.md` → parent=null
- [ ] `pages[].depth` 从路径推导:`ui/` 直接子文件 depth=1;`ui/<dir>/` 子文件 depth=2
- [ ] `check-nav` 的三类异常(自指/循环/死链)MUST 分类输出,不可合并
- [ ] `compute-hash` MUST 计算每个 .md 文件(含 organisms/,排除 token.md 与本子命令产出的 .json)
- [ ] `--kind code` MUST 依赖 ui-implementation-map.json(缺失时显性失败,提示先跑 build-impl-map);哈希目标为 impl-map 映射到的实现文件
- [ ] `check-sync` 的状态 MUST 四值枚举:`in-sync` / `spec-ahead` / `code-drifted` / `diverged`;基线缺失 MUST 退出码 2(没能检查),不得按 in-sync 处理
- [ ] 语义漂移审计(agent 执行)MUST 只报差异(全匹配页一行「无漂移」);报告落 `.maliang/critique/drift_<date>.md`,禁止落 `ui-markdown/`(根级 .md 会污染 compute-hash 基线)
- [ ] `token-usage` MUST 排除 action 行的 `{xxx}`(URL/JS 模板参数,非 token 引用,与 validate-draw-md 检查 1 同规则)
- [ ] `build-impl-map` 的 status MUST 三值枚举:`implemented` / `partial` / `missing`
- [ ] 所有 JSON 产出 MUST 含 ISO8601 时间戳字段(`generated_at` / `computed_at` / `built_at`)
- [ ] 失败 MUST 显性化:目录不存在/JSON 缺失/解析失败时返回非零退出码并打印 ERROR,禁止吞错

---

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| `.maliang/ui-markdown/` 不存在 | 提示用户先跑 draw-md 产出页面 markdown | 退出码 1,不产出空 JSON |
| 页面 markdown 缺 frontmatter | `parse_frontmatter` 返回空 dict,`name` 用文件名(去 .md)兜底 | 在 `pages[]` 标注 `name=null`,继续处理其他页面 |
| frontmatter `components` 字段格式异常(非 `[a,b,c]`) | 当作字符串处理,split(',') 兜底 | 设为空 list,不阻塞 generate |
| action 字段含 `tap=→` 但目标为中文/含空格(如 `tap=→对应目标页`) | 正则 `[a-z][a-z0-9/-]*` 不匹配,自动跳过 | 记入 `navigations[]` 的 `to=null`(可选增强) |
| `ui-hash-state.json` 不存在(diff-hash 时) | 输出 "无历史快照,所有文件视为 added" | 提示用户先跑 compute-hash |
| `preview/` 或框架代码目录不存在(build-impl-map 时) | 当作空集合,status 全为 missing | 在输出顶部标注 "未找到 preview/ 或框架代码根" |
| `ui-implementation-map.json` 不存在(list-unimplemented 时) | 提示用户先跑 build-impl-map | 退出码 1 |

---

## 禁止事项(反例)

- **禁止修改 draw-md 产出**:ui-graph 是只读分析工具,`parse_directory` / `compute-hash` 只读 markdown,不修改 `ui/*.md` / `organisms/*.md` / `token.md`。修改 draw-md 产出会破坏 draw-md 的 token 引用一致性。
- **禁止在 `ui-relationships.json` 中内联 markdown 内容**:JSON 只存结构化字段(path/name/parent/depth/components/from/to/event),不存原文。内联会导致 JSON 膨胀且与源文件漂移。
- **禁止 `extract_navigations` 把 `tap=无` / `tap=back` 当作跳转**:`无` 是无操作,`back` 是 history.back(非具体页面),均不产生页面级跳转关系。
- **禁止 `check-nav` 把"未生成页面"当作"死链"**:未生成(detect by list-missing)与死链(to 不在 pages 中)语义不同——未生成是"还没写",死链是"目标路径不存在于当前 pages 集合"。check-nav 报死链,list-missing 报未生成,职责分离。
- **禁止 `compute-hash` 把 JSON 产出文件计入哈希**:`ui-relationships.json` / `ui-hash-state.json` / `ui-implementation-map.json` / `preview-hash-state.json` / `code-hash-state.json` / `token-usage.json` 是本子命令产出,非被测产物,计入会导致 diff-hash 自我污染;`--kind preview` 另排除 `selection.json`（用户选择记录,不是产物）。
- **禁止 `build-impl-map` 模糊匹配 slug**:harmony 用 TitleCase(`Home.ets`),flutter/element 用 lowercase(`home.dart` / `home.vue`),不可统一用一种 case 匹配,否则会漏匹配或误匹配。
