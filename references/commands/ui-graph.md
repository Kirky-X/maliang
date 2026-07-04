# ui-graph 子命令 —— UI 关系管理与变更追踪

> 本文件是 `ui-graph` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 输入 = [`draw-md`](./draw-md.md) 产出的 `examples/ui-markdown/` 目录(token.md + organisms/ + ui/*.md)。
> 输出 = 三个 JSON 文件,落在 `examples/ui-markdown/` 下:
>   - `ui-relationships.json` — 页面层级 + 跳转关系图
>   - `ui-hash-state.json` — 每个 markdown 文件的 sha256 哈希快照
>   - `ui-implementation-map.json` — 逻辑 UI ↔ preview HTML ↔ 框架代码三向映射
> 这是 [`draw-md`](./draw-md.md) 的**下游**:draw-md 产出页面 markdown,ui-graph 在其上做关系分析、变更检测与实现覆盖度审计,不修改 draw-md 产出本身。
> 配套脚本 [`scripts/ui-graph.py`](../../scripts/ui-graph.py) 是纯 Python 标准库实现,无第三方依赖。

---

## 产物层目录结构

所有 ui-graph 产出落在 `examples/ui-markdown/`(与 draw-md 产物同目录):

```
examples/ui-markdown/
├── token.md                    # draw-md 产物(本子命令只读,不修改)
├── organisms/                  # draw-md 产物(只读)
├── ui/                         # draw-md 产物(只读)
├── ui-relationships.json       # ui-graph generate 产出
├── ui-hash-state.json          # ui-graph compute-hash 产出
└── ui-implementation-map.json  # ui-graph build-impl-map 产出
```

- `ui-relationships.json` — 描述 pages[](路径/名称/父级/层级/组件)与 navigations[](from/to/event/source_component),是 list-missing / check-nav / list-unimplemented 的输入。
- `ui-hash-state.json` — 记录每个 markdown 文件的 sha256 + size,供 diff-hash 检测增量变更。
- `ui-implementation-map.json` — 记录每个逻辑 UI 是否有 preview HTML 与框架代码实现,供 list-unimplemented 审计覆盖度。

---

## JSON Schema

### ui-relationships.json

```json
{
  "generated_at": "2026-07-05T10:00:00+08:00",
  "target_dir": "examples/ui-markdown",
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

- `pages[].path` — 相对 `examples/ui-markdown/` 的路径(如 `ui/setting/about.md`)。
- `pages[].parent` — 父级目录名(`ui/` 直接子文件为 null;`ui/setting/about.md` 为 `"setting"`)。
- `pages[].depth` — 层级深度(`ui/home.md` = 1;`ui/setting/about.md` = 2)。
- `pages[].components` — 从 frontmatter `components` 字段解析的组件 slug 列表。
- `navigations[].from` / `to` — 均为相对 `examples/ui-markdown/` 的路径。
- `navigations[].event` — 触发事件(当前仅 `tap`;`submit`/`focus` 等不产生跳转,不在此列)。
- `navigations[].source_component` — 触发跳转的组件类型(v1 暂为 null,后续可增强为参数表的"组件类型"字段值)。

### ui-hash-state.json

```json
{
  "computed_at": "2026-07-05T10:00:00+08:00",
  "target_dir": "examples/ui-markdown",
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

解析 `examples/ui-markdown/` 目录,聚合页面层级与跳转关系。

```bash
python3 scripts/ui-graph.py generate [--target PATH]
# 默认 --target examples/ui-markdown/
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

### 4. compute-hash — 计算 markdown 文件哈希

用 `hashlib.sha256` 计算每个 markdown 文件哈希,写 `ui-hash-state.json`。

```bash
python3 scripts/ui-graph.py compute-hash [--target PATH]
# 产出 {target}/ui-hash-state.json
```

### 5. diff-hash — 对比哈希快照

对比当前文件哈希与 `ui-hash-state.json`,输出 added/modified/deleted 三类变更。

```bash
python3 scripts/ui-graph.py diff-hash [--target PATH]
# 输出示例:
#   [added]    ui/setting/notifications.md
#   [modified] ui/home.md
#   [deleted]  ui/old-page.md
```

### 6. build-impl-map — 构建实现映射

扫描 `preview/**/*.html`(从文件名提取 slug,如 `preview_home.html` → `home`)+ 框架代码路径模式(`**/pages/<Slug>.ets` / `**/pages/<slug>.dart` / `**/views/<slug>.vue`),与 `ui-relationships.json` 的 pages 匹配,写 `ui-implementation-map.json`。

```bash
python3 scripts/ui-graph.py build-impl-map [--target PATH] [--preview-root PATH] [--code-root PATH]
# 默认 --preview-root = {target}/../preview  (即 examples/preview/)
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

---

## 流程

0. **前置检查** —— 确认 `examples/ui-markdown/` 存在且含 `ui/` 子目录;若不存在,提示用户先跑 [`draw-md`](./draw-md.md) 产出页面 markdown。

   **🔴 CHECKPOINT · 输入就绪**:确认 `examples/ui-markdown/ui/` 至少有 1 个 .md 文件,再进入下一步。

1. **生成关系图** —— 运行 `generate` 产出 `ui-relationships.json`。

   **🔴 CHECKPOINT · 关系图就绪**:确认 `ui-relationships.json` 的 `pages[]` 非空,`navigations[]` 已提取(可能为空,若无跳转)。

2. **审计跳转完整性** —— 运行 `list-missing` + `check-nav`,识别未生成页面与异常关系。

   **🔴 CHECKPOINT · 跳转完整**:自指/循环/死链均需用户确认是 bug 还是预期(如未实现的占位跳转)。

3. **构建实现映射** —— 运行 `build-impl-map` 产出 `ui-implementation-map.json`,运行 `list-unimplemented` 输出未实现清单。

4. **变更检测(按需)** —— 当 draw-md 产出更新后,运行 `compute-hash` 刷新快照,再运行 `diff-hash` 输出变更页面清单,供前端/预览更新决策。

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
- [ ] `build-impl-map` 的 status MUST 三值枚举:`implemented` / `partial` / `missing`
- [ ] 所有 JSON 产出 MUST 含 ISO8601 时间戳字段(`generated_at` / `computed_at` / `built_at`)
- [ ] 失败 MUST 显性化:目录不存在/JSON 缺失/解析失败时返回非零退出码并打印 ERROR,禁止吞错

---

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| `examples/ui-markdown/` 不存在 | 提示用户先跑 draw-md 产出页面 markdown | 退出码 1,不产出空 JSON |
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
- **禁止 `compute-hash` 把 JSON 产出文件计入哈希**:`ui-relationships.json` / `ui-hash-state.json` / `ui-implementation-map.json` 是本子命令产出,非 draw-md 产出,计入会导致 diff-hash 自我污染。
- **禁止 `build-impl-map` 模糊匹配 slug**:harmony 用 TitleCase(`Home.ets`),flutter/element 用 lowercase(`home.dart` / `home.vue`),不可统一用一种 case 匹配,否则会漏匹配或误匹配。
