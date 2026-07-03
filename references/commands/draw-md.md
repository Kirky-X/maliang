# draw-md 子命令 —— 产出页面级硬 token UI markdown

> 本文件是 `draw-md` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 产出物 = **页面级 UI markdown**,落在 `examples/ui-markdown/` 下:每页一份 markdown,用 YAML frontmatter + 表格描述布局与组件参数,**颜色/字体/间距等全部引用硬 token**(RGBA + HEX 双格式)。
> 这是 [`design-md`](./design-md.md) 的**下游**:design-md 产出 prose-first 的 DESIGN.md(规范理由),draw-md 产出硬值 token + 页面规格(可实现)。
> draw-md 产出的逻辑 UI markdown 是下游 `draw-harmony` / `draw-flutter` / `draw-element` 三个框架适配子命令的输入。

---

## 关键区分:两个 token.md(不可混用)

本项目存在两份同名但职责隔离的 `token.md`(规范层仅定义命名规则与层级体系,不含色值;产物层承载具体硬值 RGBA + HEX;职责隔离以避免下游 draw-* 解析失败):

| 文件                                | 层级   | 职责                                                                                  | 是否含色值 |
| ----------------------------------- | ------ | ------------------------------------------------------------------------------------- | ---------- |
| [`token.md`](../meta/token.md)(本目录)    | 规范层 | token **命名规则**(kebab-case、层级、语义),受 [`philosophy.md`](../meta/philosophy.md) 约束 | **否**     |
| `examples/ui-markdown/token.md`(产物层) | 产物层 | token **硬值**(RGBA + HEX)                                                            | **是**     |

**draw-md 产出物的 frontmatter 与参数表 MUST 引用产物层 `examples/ui-markdown/token.md`,禁止引用规范层 `references/meta/token.md`**(后者不含色值,引用它会导致下游无法解析)。规范层 token.md 仅在"如何命名一个新 token"时参考。

---

## 产物层目录结构

所有 draw-md 产出落在 `examples/ui-markdown/`:

```
examples/ui-markdown/
├── token.md          # 全局硬 token 表(颜色/字体/图标/间距/圆角/分割线,RGBA+HEX)
├── organisms/        # 跨页面复用组件(导航栏、dock 栏……)
│   └── *.md
└── ui/               # 页面 markdown(可按层级嵌套子目录)
    ├── home.md       # 首页(一级页面)
    ├── main.md       # 主页(可选,与 home 二选一或并存)
    └── setting/      # 二级页面按功能分目录
        ├── about.md
        └── *.md
```

- `token.md` — 单一硬值来源,所有页面引用它。
- `organisms/` — **重复性/跨页面**组件(出现在多页的导航栏、dock 栏等),单独成文,页面通过名称引用,不重复定义。
- `ui/` — **页面** markdown,一页一文件;二级页面用子目录表达嵌套(如 `setting/about.md`)。

---

## 页面 markdown 契约

### YAML frontmatter(每页 MUST 含)

```yaml
---
name: home # 页面名称(kebab-case 或简明英文/中文)
description: 首页 — 商品瀑布流 + 金刚区入口 # 一句话页面用途
background: "{surface-base}" # 页面背景,MUST 引用 token.md 的 token(非硬编码色值)
updated: 2026-06-30 # 更新时间(ISO 日期)
version: 1.0.0 # 页面版本号
---
```

- `background` 等任何颜色字段 **MUST 是 token 引用**(如 `{surface-base}`),**禁止硬编码字面量**(如 `#FFFFFF` / `rgba(0,0,0,0.8)`)。这是 draw-md 的硬约束(见验证点 5.2)。
- `updated` 用 ISO 日期(`YYYY-MM-DD`)。
- `version` 语义化版本。

### 正文:按视觉顺序的布局章节

正文按**从上到下、从左到右**的视觉顺序组织章节:

1. **第一章 = 顶部导航**(引用 `organisms/` 里的导航栏组件)
2. 中间章节 = 页面主体各区块(每区块一章)
3. **最后一章 = 底部 dock**(引用 `organisms/` 里的 dock 栏组件)

每个章节内,子组件**从左到右**描述;内部组件用嵌套子章节展开。

> 布局类型选用与嵌套规则见 [`layout.md`](../dimensions/layout.md)。

### 组件参数表(每个组件 MUST 含)

每个组件用一张表描述可实现参数:

| 参数        | 值                          | 说明       |
| ----------- | --------------------------- | ---------- |
| 组件类型    | `button` + `icon`(组合)     | 引用 [framework/index.md](../framework/index.md) 的 45 类组件 slug,组合用 ` + ` 连接 |
| 宽度 width  | 375px(或 `match-parent`)    | 组件宽度   |
| 高度 height | 64px                        | 组件高度   |
| 字体大小    | `{font-size-md}`            | 引用 token |
| 圆角 radius | `{radius-md}`               | 引用 token |
| 背景颜色    | `{surface-card}`            | 引用 token |
| 字体颜色    | `{text-primary}`            | 引用 token |
| padding     | `{spacing-md} {spacing-lg}` | 引用 token |

- 颜色、字号、间距、圆角 **MUST 引用 `token.md` 的 token**,不在表里写裸值。
- 尺寸(宽高)可写具体像素(实现层需要)。
- 响应式:如有多断点,在表后补"响应式"说明(375 / 768 / 1024 各自差异)。
- **组件类型**字段 MUST 引用 [`framework/index.md`](../framework/index.md) 的 45 类组件 slug(如 `button`/`input`/`list`/`navigation`),组合组件用 ` + ` 连接(如 `input + icon`)。单列参数表将该字段作为首行;双列对比表(如 dock 选中/未选中态对比)在表前用 `> **组件类型**:...` 引用块标注。

### 组件类型标注规范

每个组件参数表 MUST 声明"组件类型"字段,引用 [`framework/index.md`](../framework/index.md) 的 45 类组件 slug,实现 draw-md 产出与 framework 组件索引的端到端对齐:

- **单组件**:直接写 slug,如 `button`、`input`、`text`、`navigation`
- **组合组件**:用 ` + ` 连接,如 `input + icon`(搜索框)、`grid + button + icon`(金刚区)、`list + card`(内容流)
- **标注位置**:
  - 单列参数表(参数 | 值 | 说明):"组件类型"作为首行字段
  - 双列对比表(参数 | 选中态 | 未选中态):在表前用 `> **组件类型**:...` 引用块标注
- **跨页面复用**:引用 `organisms/` 的章节,在引用行括号内注明组件类型,如"引用 organisms/nav-bar.md(组件类型:`navigation`)"
- **frontmatter components 字段**:数组形式,按页面出现顺序列出所有组件 slug(去重,含 organisms 引用的),供下游 draw-* 子命令快速识别本页组件清单

**与 framework/index.md 的映射约束**:组件类型字段值 SHALL 与 framework/index.md 的 45 类组件 slug 完全对齐,不得自创 slug。若需新组件类型,先按 framework/index.md「新增组件流程」补充,再在本字段引用。

---

## 流程

0. **读取 DESIGN.md 提取 token** —— 读取项目根目录的 DESIGN.md,提取 YAML frontmatter 中的所有 token(colors/typography/spacing/radius 等),写入 `examples/ui-markdown/token.md` 作为本子命令的 token 锚点。这是从 [`design-md`](./design-md.md) 衔接进入 draw-md 的状态过渡步骤:DESIGN.md 是 design-md 的产出物,draw-md 必须基于它产出硬值 token,不可凭空生成。

   **🔴 CHECKPOINT · token 提取**:确认 token.md 已生成且包含 DESIGN.md 中的全部 token,再进入下一步。若 DESIGN.md 缺失关键 token,走「失败模式与 fallback」表中的对应策略。

1. **先定 token.md** —— 若 `examples/ui-markdown/token.md` 不存在或需补充,先产出/更新它(6 章节:颜色/字体/图标/间距/圆角/分割线,RGBA + HEX 双格式)。token 命名遵循规范层 [`token.md`](../meta/token.md) 的规则。
2. **抽取 organisms** —— 识别跨页面复用组件(导航栏、dock 栏),写入 `organisms/`,每份含 frontmatter + 参数表。

   **🔴 CHECKPOINT · 逐页产出前**:确认 token.md + organisms 已定义,展示待产出页面清单供用户确认,再进入逐页产出。

### 步骤 2.5(可选):页面清单确认

> **仅新项目触发**。存量项目(`examples/ui-markdown/ui/` 已有页面)跳过此步骤,直接进入步骤 3。

**触发条件**(二选一即触发):
1. `examples/ui-markdown/ui/` 目录为空或不存在(判定为新项目首次产出)。
2. 用户明确要求"全量产出"/"补齐默认页面"。

**步骤行为**:
1. 读取 [`references/default-pages/index.md`](../default-pages/index.md),根据端型展示默认页面清单:
   - App 端项目 → 引用 [`app.md`](../default-pages/app.md)(15 页:home/discover/messages/mine/login/signup/forgot-password/settings/about/privacy/terms/feedback/empty-state/network-error/not-found)
   - Web 端项目 → 引用 [`web.md`](../default-pages/web.md)(15 页:home/about/contact/login/signup/forgot-password/verify-email/dashboard/settings/profile/not-found/server-error/forbidden/privacy/terms)
   - 跨端项目 → 两端清单各自适用,共享 design token 保证视觉一致
2. 标注优先级:
   - **P0(必备,不可删)**:App 4 页(home/mine/login/settings);Web 4 页(home/login/dashboard/settings)
   - **P1(按业务选)**:根据产品形态选配(如电商 App 选 discover/messages;SaaS Web 选 verify-email/profile)
   - **P2(可选)**:错误页/协议页等,按合规与容错需求选配,建议至少保留 not-found
3. 询问用户:确认 P0 全部产出 + 从 P1/P2 勾选所需页面,或自定义增补。
4. 用户确认后形成本项目的"页面产出清单",作为步骤 3 逐页产出的输入。

**产物约束**:产出的页面文件名 SHALL 与 `default-pages` 清单 slug 对齐(如 `home.md`/`forgot-password.md`),与「产物层目录结构」的 `ui/home.md`、`ui/setting/about.md` 嵌套约定一致。

3. **逐页产出** —— 每个页面一份 markdown:frontmatter(背景引用 token)+ 顶部导航章 → 主体章 → 底部 dock 章,每组件一张参数表(值引用 token)。
4. **自检** —— grep 确认所有颜色字段是 token 引用而非字面量(对应验证点 5.2)。

   **🔴 CHECKPOINT · 自检通过**:自检全部通过后,产出物方可交付给下游(preview / draw-harmony / draw-flutter / draw-element)使用。

---

## 约束汇总(硬性)

- [ ] frontmatter 含 name/description/background/updated/version,background 引用 token
- [ ] frontmatter 含 components 字段(数组),列出本页所有章节用到的组件 slug(含 organisms 引用的,去重)
- [ ] 正文第一章 = 顶部导航,最后一章 = 底部 dock
- [ ] 每个组件有参数表(宽/高/字号/圆角/背景/字色/padding)
- [ ] 每个组件参数表首行声明"组件类型"字段,引用 framework/index.md 的 45 类组件 slug,组合组件用 ` + ` 连接
- [ ] 所有颜色值引用产物层 `examples/ui-markdown/token.md`,**无硬编码色值字面量**
- [ ] 二级页面用子目录嵌套(如 `setting/about.md`)
- [ ] 跨页面复用组件放 `organisms/`,页面引用而非重复定义

---

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| DESIGN.md 缺失关键 token(如无 color.text) | 列出缺失 token 清单,询问用户补全 | 用 `{color-text-primary}` 等标准命名占位,标注"假设值,需 DESIGN.md 确认" |
| organisms 重复定义(导航栏/dock 多页面重复) | 引用已有 organisms/*.md 而非重写 | 在 token.md 顶部声明 organisms 引用清单 |
| 用户提供的 UI 不符合 draw-md 规格(缺布局章节) | 提示具体偏差(缺 token / 缺布局章节) | 引导用户重跑 draw-md,不要硬解析不规范输入 |
| 页面组件无对应 framework 文档 | 在 index.md 索引表查最接近类型 | 用基础组件(button/text/list/layout)组合实现,标注"组合方案" |

---

## 禁止事项(反例)

- **禁止在组件参数表写裸色值**(如 `#FFFFFF`、`rgba(0,0,0,0.8)`):色值脱离 token 体系会导致多端不一致与主题切换失效。MUST 引用 `examples/ui-markdown/token.md` 的 token(如 `{surface-card}`)。
- **禁止引用规范层 `references/meta/token.md`**:它只定义命名规则、不含色值,引用它会让下游 draw-* 无法解析出具体值。MUST 引用产物层 `examples/ui-markdown/token.md`(RGBA + HEX 硬值)。
- **禁止组件类型字段自创 slug**(如 `search-bar`、`tab-item`):脱离 framework 索引会导致下游 draw-* 映射失败。MUST 引用 [`framework/index.md`](../framework/index.md) 的 45 类组件 slug,组合组件用 ` + ` 连接(如 `input + icon`)。
- **禁止跨页面复用组件在多页重复定义**:重复定义会造成维护漂移与 token 不一致。MUST 放入 `organisms/` 单独成文,各页面通过名称引用。
- **禁止二级页面文件直接放 `ui/` 根目录**(如 `ui/about.md`):扁平放置会让页面层级丢失、无法表达导航嵌套。MUST 用子目录(如 `ui/setting/about.md`)。
