---
name: maliang
description: 设计系统技能,含两个子命令。(A) design-md —— 创建、应用、验证、导出 DESIGN.md 设计系统文件(Google Labs agent-first 格式:YAML 前置 token + Markdown 设计理由);(B) ui-md —— 从 DESIGN.md 产出页面级硬 token UI markdown(布局章节 + 组件参数表,颜色/字体/间距全引用 token,RGBA+HEX)。主动触发:(1) 用户提到 DESIGN.md、design token、设计系统、设计规范、品牌/样式/主题色规范;(2) 想从 CSS、Tailwind、组件代码提取设计 token 或统一样式;(3) 提供 UI 截图/设计稿想转化为结构化设计规范;(4) 需要页面级 UI markdown、组件规格表、布局描述、UI 交付物;(5) 正在开发前端组件需要保持样式一致性;(6) 需要将设计系统导出为 Tailwind/CSS 变量或 W3C DTCG 格式,或 lint、diff、验证 DESIGN.md。任何重要前端项目启动时,主动建议先建立 DESIGN.md,再产出页面 UI markdown —— 不要等用户开口。
license: MIT
---

# maliang —— 设计系统技能

两个子命令构成一条流水线:

- **design-md**(上游)— 产出 prose-first 的 **DESIGN.md**(YAML token + Markdown 设计理由)。解决"设计系统**是什么、为什么**"。
- **ui-md**(下游)— 从 DESIGN.md 产出页面级硬 token **UI markdown**(布局章节 + 组件参数表,RGBA + HEX)。解决"每个页面/组件**具体怎么实现**"。

## 子命令路由

| 用户意图                                    | 子命令    | 完整流程                                             |
| ------------------------------------------- | --------- | ---------------------------------------------------- |
| 创建 / 生成 DESIGN.md(从代码/截图/访谈)     | design-md | [`references/design-md.md`](references/design-md.md) |
| 应用 DESIGN.md 到前端代码                   | design-md | [`references/design-md.md`](references/design-md.md) |
| lint / diff / 导出 / 验证 DESIGN.md         | design-md | [`references/design-md.md`](references/design-md.md) |
| 产出页面级 UI markdown(token 表 + 页面规格) | ui-md     | [`references/ui-md.md`](references/ui-md.md)         |
| 跨页面复用组件(导航栏 / dock)规格化         | ui-md     | [`references/ui-md.md`](references/ui-md.md)         |

进入子命令后,按其流程文档执行。检查点、边界情形、交付核对清单均在各子命令文档内 —— **本路由器不含流程主体**。

## 通用

- **不确定用哪个?** 先 `design-md`。没有 DESIGN.md 就无法产出可靠的 `ui-md` 硬 token。
- 维度规范(色 / 字 / 图 / 距 / 角 / 线 / 布局 / 原则)在 [`references/`](references/) 下,两个子命令共享参考,不在本路由器重复。
