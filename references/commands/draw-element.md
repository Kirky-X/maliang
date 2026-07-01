# draw-element 子命令 —— 将逻辑 UI 转换为 Element Plus(Vue 3)实现

> 本文件是 `draw-element` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 输入 = `draw-md` 产出的页面级 UI markdown(`examples/ui-markdown/` 下),输出 = Element Plus + Vue 3 SFC 实现代码。
> 组件映射参考 [`framework/element/`](../framework/element/) 下的组件文档。

---

## 流程概览(三段式)

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  1. 输入解析      │ -> │  2. 组件映射      │ -> │  3. 产出校验      │
│  读取 draw-md 产出 │    │  查 framework 文档 │    │  Element API + token │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 1. 输入解析

读取 `draw-md` 产出的页面 markdown(位于 `examples/ui-markdown/ui/` 下):

1. **解析 frontmatter** — 提取 `name`、`description`、`background`、`updated`、`version`
2. **解析 token.md** — 读取 `examples/ui-markdown/token.md`,建立 token 名→硬值映射表(颜色/字体/间距/圆角)
3. **解析布局章节** — 按"顶部导航 → 主体区块 → 底部 dock"顺序,逐章提取组件类型(按钮/文本/列表/...)与参数表

**🔴 CHECKPOINT · 输入解析确认**:确认 UI markdown + token.md 已读取,展示组件映射表(逻辑组件 → Element Plus 组件)供用户确认,再进入代码生成。

---

## 2. 组件映射

逐组件查 [`framework/element/`](../framework/element/) 文档,将逻辑组件映射为 Element Plus 组件:

### 组件映射表

| 逻辑组件(draw-md) | Element Plus 组件 | 框架文档 |
| ------------------- | ----------------- | -------- |
| button | `<el-button>` | [component.md](../framework/element/button/component.md) + [api.md](../framework/element/button/api.md) |
| text | `<el-text>` / Typography | [component.md](../framework/element/text/component.md) + [api.md](../framework/element/text/api.md) |
| list | `<el-table>` + `<el-table-column>` | [component.md](../framework/element/list/component.md) + [api.md](../framework/element/list/api.md) |
| image | `<el-image>` | [component.md](../framework/element/image/component.md) + [api.md](../framework/element/image/api.md) |
| input | `<el-input>` | [component.md](../framework/element/input/component.md) + [api.md](../framework/element/input/api.md) |
| navigation bar | `<el-menu>` / `<el-header>` | [component.md](../framework/element/navigation/component.md) + [api.md](../framework/element/navigation/api.md) |
| layout | `<el-row>` + `<el-col>` / `<el-container>` + `<el-aside>` | [component.md](../framework/element/layout/component.md) + [api.md](../framework/element/layout/api.md) |
| tabs | `<el-tabs>` + `<el-tab-pane>` | [component.md](../framework/element/tabs/component.md) + [api.md](../framework/element/tabs/api.md) |
| form | `<el-form>` + `<el-form-item>` | [component.md](../framework/element/form/component.md) + [api.md](../framework/element/form/api.md) |
| dialog | `<el-dialog>` | [component.md](../framework/element/dialog/component.md) + [api.md](../framework/element/dialog/api.md) |
| grid | `<el-row>` + `<el-col>`(栅格) | [component.md](../framework/element/grid/component.md) + [api.md](../framework/element/grid/api.md) |
| progress | `<el-progress>` | [component.md](../framework/element/progress/component.md) + [api.md](../framework/element/progress/api.md) |
| icon | `<el-icon>` | [component.md](../framework/element/icon/component.md) + [api.md](../framework/element/icon/api.md) |
| shape | `<el-divider>` / 自定义 SVG | [component.md](../framework/element/shape/component.md) + [api.md](../framework/element/shape/api.md) |
| theme | `<el-config-provider>` + CSS 变量(浅/暗) | [component.md](../framework/element/theme/component.md) + [api.md](../framework/element/theme/api.md) |
| animation | `<transition>` / `<TransitionGroup>` + CSS animation | [component.md](../framework/element/animation/component.md) + [api.md](../framework/element/animation/api.md) |
| gesture | N/A(Element 无手势组件,用 Vue `@click`/`v-touch` 指令) | [N/A](../framework/element/gesture/component.md) |
| i18n | `<el-config-provider>` + `vue-i18n` | [component.md](../framework/element/i18n/component.md) + [api.md](../framework/element/i18n/api.md) |
| a11y | N/A(Element 无 a11y 章节,遵循 Vue a11y 规范) | [N/A](../framework/element/a11y/component.md) |
| video | N/A(Element 无视频组件,用原生 `<video>` 封装) | [N/A](../framework/element/video/component.md) |
| menu | `<el-menu>` / `<el-dropdown>` | [component.md](../framework/element/menu/component.md) + [api.md](../framework/element/menu/api.md) |
| scroll | `<el-scrollbar>` | [component.md](../framework/element/scroll/component.md) + [api.md](../framework/element/scroll/api.md) |
| carousel | `<el-carousel>` + `<el-carousel-item>` | [component.md](../framework/element/carousel/component.md) + [api.md](../framework/element/carousel/api.md) |
| radio | `<el-radio>` + `<el-radio-group>` | [component.md](../framework/element/radio/component.md) + [api.md](../framework/element/radio/api.md) |
| switch | `<el-switch>` | [component.md](../framework/element/switch/component.md) + [api.md](../framework/element/switch/api.md) |
| popover | `<el-popover>` / `<el-tooltip>` / `<el-popconfirm>` | [component.md](../framework/element/popover/component.md) + [api.md](../framework/element/popover/api.md) |
| message | `ElMessage` | [component.md](../framework/element/message/component.md) + [api.md](../framework/element/message/api.md) |
| drawer | `<el-drawer>` | [component.md](../framework/element/drawer/component.md) + [api.md](../framework/element/drawer/api.md) |

### Token 映射规则

| draw-md token 引用 | Element Plus 实现 |
| ------------------- | ----------------- |
| `{color-primary}` | CSS 变量 `var(--el-color-primary)` 或 `var(--color-primary)` |
| `{font-size-md}` | CSS 变量 `var(--el-font-size-base)` 或 `var(--font-size-md)` |
| `{spacing-md}` | CSS 变量 `var(--spacing-md)` 或 `16px` |
| `{radius-md}` | CSS 变量 `var(--el-border-radius-base)` 或 `8px` |

> 优先使用 CSS 变量(便于主题切换),通过 `<style>` 块的 `:root` 或组件 scoped 样式注入。

### 映射步骤

1. 识别组件类型 — 从参数表的组件名推断(如"按钮"→`<el-button>`)
2. 查框架文档 — 读 `framework/element/<component>/component.md` 获取用法,读 `api.md` 获取属性/事件/方法表
3. 填充属性 — 将 draw-md 参数表的值(token 引用)映射为 Element Plus 组件 props 与 CSS 变量
4. 生成代码 — 产出 Vue 3 SFC(`<template>` + `<script setup>` + `<style scoped>`)

**🔴 CHECKPOINT · 代码生成确认**:展示生成的 Vue 3 SFC 代码片段,确认 token 引用正确(无硬编码颜色/字号/间距),再进入产出校验。

---

## 3. 产出校验

生成 Element Plus Vue 3 SFC 代码后,执行自检:

- [ ] 所有组件使用正确的 Element Plus 标签(`<el-button>` / `<el-text>` / `<el-table>` 等)
- [ ] 颜色值已从 token 映射为 CSS 变量或硬值,无 `{token-name}` 占位符残留
- [ ] 布局结构符合 draw-md 章节顺序(顶部导航 → 主体 → 底部 dock)
- [ ] 组件 props 与 `framework/element/` 文档一致(无杜撰 API)
- [ ] 产出文件含注释标注来源(`<!-- 由 draw-element 从 <page>.md 生成 -->`)
- [ ] SFC 三段式结构完整(`<template>` + `<script setup>` + `<style scoped>`)
- [ ] `<script setup>` 中正确 import 使用的 Element Plus 组件(如需)

**🔴 CHECKPOINT · 校验通过**:校验全部通过后,Vue 3 SFC 代码方可交付使用。

---

## 产出物

- 一个页面 → 一个 Vue 3 SFC 文件(`<PageName>.vue`)
- 跨页面复用组件 → 单独 SFC 文件(被各页面 import)
- 文件命名:`<PageName>.vue`(如 `Home.vue`、`SettingAbout.vue`)

---

## 约束汇总(硬性)

- [ ] 输入必须是 draw-md 产出(含 frontmatter + 参数表 + token 引用),MUST NOT 直接从 DESIGN.md 跳过 draw-md
- [ ] 组件映射 MUST 查 `framework/element/` 文档,MUST NOT 凭记忆杜撰 Element Plus 组件 API
- [ ] Token 引用 MUST 解析为具体值(CSS 变量或硬值),MUST NOT 在产出代码中残留 `{token-name}` 占位符
- [ ] 产出代码 MUST 为合法 Vue 3 SFC(语法正确、标签闭合、script setup 有效)

---

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| DESIGN.md 缺失关键 token(如无 color.text) | 列出缺失 token 清单,询问用户补全 | 用 `{color-text-primary}` 等标准命名占位,标注"假设值,需 DESIGN.md 确认" |
| UI markdown 出现裸值(如 `#FF0000` / `14px`) | 提示用户回退 draw-md 重新产出 | 拒绝硬编码,显式标注"需回 draw-md 修复" |
| `framework/element/` 无对应组件类型 | 在 index.md 索引表查最接近类型 | 用基础组件(button/text/list/layout)组合实现,标注"无原生对应,本方案为组合" |
| Vue 3 SFC 编译报错(如 token 占位符未替换) | 检查 `{token-name}` 是否全部解析 | 标注未解析 token 清单,引导用户回 design-md 确认 |

---

## 禁止事项(反例)

- **禁止用 `inline style` 写颜色**(如 `style="color: #5B7CFA"`):内联硬值脱离 CSS 变量体系,主题切换失效且无法统一改值。MUST 用 CSS 变量(`var(--color-primary)`)或 SCSS 变量引用 design token。
- **禁止用 `v-if` 切换大量列表项**:`v-if` 会销毁/重建 DOM,频繁切换大量节点性能差。MUST 用 `v-show`(`display` 切换)或组件复用。
- **禁止直接操作 DOM**(如 `document.querySelector`):绕过 Vue 响应式系统会导致状态与视图脱节、难以维护。MUST 用 Vue 的 `ref` 和 `reactive` 访问元素与状态。
- **禁止表单不用 `el-form` + `rules` 校验、自己写校验逻辑**:自写校验重复造轮子、缺统一错误提示与异步校验。MUST 用 `<el-form :rules>` + `<el-form-item prop>` 声明式校验。
- **禁止用 `scoped CSS` 写颜色硬值**:scoped 中硬编码颜色无法被主题变量覆盖,暗色模式失效。MUST 用 CSS 变量(`var(--xxx)`),scoped 仅用于作用域隔离。
