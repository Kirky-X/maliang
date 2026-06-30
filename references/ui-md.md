# ui-md 子命令 —— 产出页面级硬 token UI markdown

> 本文件是 `ui-md` 子命令的完整流程,由顶层 [`SKILL.md`](../SKILL.md) 路由进入。
> 产出物 = **页面级 UI markdown**,落在 `examples/ui-markdown/` 下:每页一份 markdown,用 YAML frontmatter + 表格描述布局与组件参数,**颜色/字体/间距等全部引用硬 token**(RGBA + HEX 双格式)。
> 这是 [`design-md`](./design-md.md) 的**下游**:design-md 产出 prose-first 的 DESIGN.md(规范理由),ui-md 产出硬值 token + 页面规格(可实现)。

---

## 关键区分:两个 token.md(不可混用)

本项目存在两份同名但职责隔离的 `token.md`(见 `design.md` Decision 4):

| 文件                                | 层级   | 职责                                                                                  | 是否含色值 |
| ----------------------------------- | ------ | ------------------------------------------------------------------------------------- | ---------- |
| [`token.md`](./token.md)(本目录)    | 规范层 | token **命名规则**(kebab-case、层级、语义),受 [`philosophy.md`](./philosophy.md) 约束 | **否**     |
| `examples/ui-markdown/token.md`(产物层) | 产物层 | token **硬值**(RGBA + HEX)                                                            | **是**     |

**ui-md 产出物的 frontmatter 与参数表 MUST 引用产物层 `examples/ui-markdown/token.md`,禁止引用规范层 `references/token.md`**(后者不含色值,引用它会导致下游无法解析)。规范层 token.md 仅在"如何命名一个新 token"时参考。

---

## 产物层目录结构

所有 ui-md 产出落在 `examples/ui-markdown/`:

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

- `background` 等任何颜色字段 **MUST 是 token 引用**(如 `{surface-base}`),**禁止硬编码字面量**(如 `#FFFFFF` / `rgba(0,0,0,0.8)`)。这是 ui-md 的硬约束(见验证点 5.2)。
- `updated` 用 ISO 日期(`YYYY-MM-DD`)。
- `version` 语义化版本。

### 正文:按视觉顺序的布局章节

正文按**从上到下、从左到右**的视觉顺序组织章节:

1. **第一章 = 顶部导航**(引用 `organisms/` 里的导航栏组件)
2. 中间章节 = 页面主体各区块(每区块一章)
3. **最后一章 = 底部 dock**(引用 `organisms/` 里的 dock 栏组件)

每个章节内,子组件**从左到右**描述;内部组件用嵌套子章节展开。

### 组件参数表(每个组件 MUST 含)

每个组件用一张表描述可实现参数:

| 参数        | 值                          | 说明       |
| ----------- | --------------------------- | ---------- |
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

---

## 流程

1. **先定 token.md** —— 若 `examples/ui-markdown/token.md` 不存在或需补充,先产出/更新它(6 章节:颜色/字体/图标/间距/圆角/分割线,RGBA + HEX 双格式)。token 命名遵循规范层 [`token.md`](./token.md) 的规则。
2. **抽取 organisms** —— 识别跨页面复用组件(导航栏、dock 栏),写入 `organisms/`,每份含 frontmatter + 参数表。
3. **逐页产出** —— 每个页面一份 markdown:frontmatter(背景引用 token)+ 顶部导航章 → 主体章 → 底部 dock 章,每组件一张参数表(值引用 token)。
4. **自检** —— grep 确认所有颜色字段是 token 引用而非字面量(对应验证点 5.2)。

---

## 约束汇总(硬性)

- [ ] frontmatter 含 name/description/background/updated/version,background 引用 token
- [ ] 正文第一章 = 顶部导航,最后一章 = 底部 dock
- [ ] 每个组件有参数表(宽/高/字号/圆角/背景/字色/padding)
- [ ] 所有颜色值引用产物层 `examples/ui-markdown/token.md`,**无硬编码色值字面量**
- [ ] 二级页面用子目录嵌套(如 `setting/about.md`)
- [ ] 跨页面复用组件放 `organisms/`,页面引用而非重复定义
