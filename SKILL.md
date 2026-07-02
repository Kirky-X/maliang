---
name: maliang
description: "设计系统技能。触发:DESIGN.md/design token/设计系统;CSS/Tailwind 提取 token;页面级 UI markdown/组件规格;导出 Tailwind/CSS/W3C DTCG/lint;UI markdown 转 HarmonyOS/Flutter/Element Plus。English: design system, design tokens, UI markdown, ArkTS, Flutter, Element Plus."
license: MIT
---

# maliang (马良) —— 设计系统技能

六个子命令构成一条完整流水线:design-md(创建 DESIGN.md)→ draw-md(页面级 UI markdown)→ preview(预览验证)→ draw-harmony/draw-flutter/draw-element(框架代码)。

- **design-md**(上游)— 产出 prose-first 的 **DESIGN.md**(YAML token + Markdown 设计理由,Google Labs agent-first 格式)。支持"创建、应用、验证、导出"四个动作。解决"设计系统**是什么、为什么**"。
- **redesign**(上游旁路)— 改版现有 UI,8 维度审计 + 保留规则 + 现代化杠杆 + 决策树。支持 Refresh / Restructure / Rebuild 三模式。解决"**现有设计如何变好**"。
- **draw-md**(中游)— 从 DESIGN.md 产出页面级硬 token **UI markdown**(布局章节 + 组件参数表,颜色/字体/间距全引用 token,RGBA + HEX)。解决"每个页面/组件**具体怎么实现**"。
- **preview**(验证)— 使用 Element Plus 框架对 draw-md 产出进行实时预览验证,支持 iOS/Android 设备外壳。解决"**效果对不对**"。
- **draw-harmony**(下游)— 将 draw-md 逻辑 UI 转换为 HarmonyOS(ArkTS)框架实现。解决"HarmonyOS **代码怎么写**"。
- **draw-flutter**(下游)— 将 draw-md 逻辑 UI 转换为 Flutter 框架实现。解决"Flutter **代码怎么写**"。
- **draw-element**(下游)— 将 draw-md 逻辑 UI 转换为 Element Plus 框架实现。解决"Element Plus **代码怎么写**"。

## 子命令路由

> 🔴 **CHECKPOINT**:无 DESIGN.md 时,严禁直接进入 draw-md / draw-* 下游子命令 —— 必须先走 design-md 建立设计系统,否则产出的 UI markdown 与框架代码无 token 可引用。

| 用户意图                                    | 子命令        | 完整流程                                                          |
| ------------------------------------------- | ------------- | ----------------------------------------------------------------- |
| 创建 / 生成 DESIGN.md(从代码/截图/访谈)     | design-md     | [`references/commands/design-md.md`](references/commands/design-md.md) |
| 应用 DESIGN.md 到前端代码                   | design-md     | [`references/commands/design-md.md`](references/commands/design-md.md) |
| lint / diff / 导出 / 验证 DESIGN.md         | design-md     | [`references/commands/design-md.md`](references/commands/design-md.md) |
| 🔷 改版 / 重设计现有 UI(Refresh/Restructure/Rebuild) | redesign | [`references/commands/redesign.md`](references/commands/redesign.md) |
| 产出页面级 UI markdown(token 表 + 页面规格) | draw-md       | [`references/commands/draw-md.md`](references/commands/draw-md.md)     |
| 跨页面复用组件(导航栏 / dock)规格化         | draw-md       | [`references/commands/draw-md.md`](references/commands/draw-md.md)     |
| 🔴 预览 UI markdown 效果(设备外壳 + Element)| preview       | [`references/commands/preview.md`](references/commands/preview.md)     |
| 🔴 将 UI markdown 转换为 HarmonyOS(ArkTS)代码  | draw-harmony  | [`references/commands/draw-harmony.md`](references/commands/draw-harmony.md) |
| 🔴 将 UI markdown 转换为 Flutter(Dart)代码    | draw-flutter  | [`references/commands/draw-flutter.md`](references/commands/draw-flutter.md) |
| 🔴 将 UI markdown 转换为 Element Plus(Vue 3)代码 | draw-element | [`references/commands/draw-element.md`](references/commands/draw-element.md) |

> 🔴 标记的行需先确认 draw-md 产出存在;preview/draw-* 无 UI markdown 输入时应在子命令流程内 fallback 引导用户回退到 draw-md。

进入子命令后,按其流程文档执行。检查点、边界情形、交付核对清单均在各子命令文档内 —— **本路由器不含流程主体**。

## 通用

- **不确定用哪个?** 先 `design-md`。没有 DESIGN.md 就无法产出可靠的 `draw-md` 硬 token,更无法进行框架适配。
- **完整流程链路**(每步产出 = 下步输入): `design-md`(→DESIGN.md) → `draw-md`(→examples/ui-markdown/*.md) → `preview`(→preview_*.html) → `draw-harmony`/`draw-flutter`/`draw-element`(→框架代码)
- 维度规范(色 / 字 / 图 / 距 / 角 / 线 / 布局)在 [`references/dimensions/`](references/dimensions/) 下;设计原则在 [`references/meta/principles.md`](references/meta/principles.md),六个子命令共享参考,不在本路由器重复。
- 默认页面清单(App 15 页 + Web 15 页,含 P0/P1/P2 选用规则)在 [`references/default-pages/index.md`](references/default-pages/index.md) 下,供 `draw-md` 子命令在新项目触发"页面清单确认"步骤时引用。
- 框架组件文档(按钮/文本/列表 × 三框架)在 [`references/framework/`](references/framework/index.md) 下,三个 draw-* 子命令共享。

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
| -------- | -------- | ---------- |
| 无 DESIGN.md 直接要 UI markdown | 引导用户先走 design-md | 若用户坚持,产出"无 token 锚点"的临时规格并显式标注"待 DESIGN.md 建立后回填" |
| DESIGN.md 缺失关键 token(如无 color.text) | 在子命令流程内列出缺失 token 清单,询问用户补全 | 用 `{color-text-primary}` 等标准命名占位,标注"假设值,需 DESIGN.md 确认" |
| draw-* 找不到组件文档(framework/ 无对应类型) | 在 index.md 索引表查最接近的组件类型 | 用基础组件(button/text/list/layout)组合实现,标注"无原生对应,本方案为组合" |
| 用户提供的 UI markdown 不符合 draw-md 规格(见禁止事项 #3) | 提示具体偏差(缺 token / 缺布局章节) | 引导用户重跑 draw-md,不要硬解析不规范输入;preview 设备尺寸不在 scripts/ 时用最接近尺寸替代 |

## 禁止事项(反例黑名单)
1. **禁止跳过 design-md** — 无 DESIGN.md 直接产出 UI markdown 或框架代码,会导致 token 引用悬空、视觉不一致。
2. **禁止硬编码颜色/字号/间距** — 所有视觉值必须用 `{token-name}` 占位符引用,严禁 `#FF0000`、`14px`、`16px` 等具体值出现在示例代码中(文档说明中的 token 映射对照除外)。
3. **禁止跨子命令直连 / 禁止混合 token 命名** — design-md 产出不经 draw-md 直接转 draw-* 会丢失上下文,必须按链路执行;token 命名遵循 references/meta/token.md,不得混用 `{color-primary}` 和 `{primary-color}` 两种风格。
4. **禁止忽略 N/A 占位 / 禁止在 router 内写流程主体** — 跨框架转换时 N/A 组件不得强行冒充(回退组合方案);本文件是路由器,流程细节必须放在 references/commands/*.md。
