---
version: alpha
name: Minimalism
description: 瑞士国际主义平面设计的数字延续——网格先行、留白即层级、单一蓝色强调色驱动所有交互。
colors:
  primary: "#212121"
  secondary: "#9D9D9D"
  tertiary: "#2563EB"
  neutral: "#F5F5F5"
  surface: "#FFFFFF"
  on-surface: "#212121"
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  gutter: 24px
  grid-columns: 12
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 11px 23px
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

Maliang Minimalism 是瑞士国际主义平面设计（International Typographic Style）在数字界面的延续——它的参照不是某张 app 截图，而是 Josef Müller-Brockmann 的网格系统与 Linear、Vercel、Notion 这类现代 SaaS 工具的克制美学。当一切装饰被剥离，剩下的就是信息本身：网格先行、留白即层级、单一蓝色强调色驱动所有交互。

目标用户是追求效率的工具型产品使用者——开发者、运营、数据分析师。他们不需要被取悦，需要被尊重。每屏至多一处蓝色 CTA，是因为克制本身就是这种风格的性格，而不是节省成本；少即是多，是因为"多"会稀释焦点。情感调性是冷静、专业、可信——像打开一份排版精良的技术文档，而不是加载一个 app。

## Colors

调色板是高对比中性色 + 单一强调色的组合。中性色承担 99% 的视觉，蓝色只在关键交互处出现。

- **Primary (#212121)**：近黑墨色，所有标题与正文文字的主色，也是主按钮的填充色。提供最大可读性与"永久感"。不用作大面积背景——深色背景会压垮留白，破坏极简的呼吸感。
- **Secondary (#9D9D9D)**：中灰，承担所有辅助角色——次要文字、占位符、分隔线、边框、元数据。绝不用于正文主体（对比度不足 4.5:1），它的存在就是"退到幕后"。
- **Tertiary (#2563EB)**：唯一的强调色，专属用于 CTA、文本链接、焦点环。每屏至多一处——稀缺即力度，蓝色一旦泛滥就失去指引能力。不用作背景填充（除 hover 态），不用于错误状态（避免与交互 CTA 混淆）。
- **Neutral (#F5F5F5)**：页面底色。比纯白柔和，给产品一层"纸张"般的触感。不用作卡片背景——卡片必须用 surface 白，才能与底色形成层次分离。
- **Surface (#FFFFFF)**：纯白，用于卡片、模态、输入框等"抬升"容器。维持与 neutral 底色的色调对比。
- **On-surface (#212121)**：surface 之上的文字色，与 primary 同值但语义独立——前者描述"文字落在哪个面"，后者描述"主品牌色"。语义分层让未来暗色模式可独立替换。

## Typography

策略是**单一字族 Inter**，SF Pro Display 作为 macOS 系统等价物自动回落。极简主义的核心是减法——两个字族会引入不必要的视觉噪音，而 Inter 的 5 档字重（Light/Regular/Medium/Semibold/Bold）足够建立完整层级。字重选择遵循"少即是多"：一屏内不超过两种字重。

- **headline-lg (48px / Semibold)**：负字距 `-0.02em` 模拟印刷标题的紧凑密度。用于页面主标题。768px 以下屏幕必须降到 `headline-md`，否则压迫感过强。
- **headline-md (32px / Semibold)**：次级标题与区块标题。轻负字距 `-0.01em` 保持紧凑但不过分。
- **body-md (16px / Regular)**：正文，行高 1.6 保证长文可读性。**不得低于 16px**——极简不等于把字变小，而是让每个字号都有存在的理由。
- **body-sm (14px / Regular)**：辅助文字、表格单元格、卡片副文本。不用于主体段落。
- **label-sm (12px / Medium)**：按钮、标签、元数据专用。必须配合 `text-transform: uppercase` 与 `0.04em` 字距使用——这套全大写 + 宽字距是极简主义的身份印记，把"功能性文字"与"阅读性文字"在视觉上彻底分离。不用于段落正文。

## Layout

布局基于 **12 列网格**，8px 基准单位。间距阶梯 4/8/12/16/24/32/48/64 全部是 4 的倍数，保证任何组合都能对齐到同一套节拍。

容器最大宽度 1200px 居中，避免宽屏下阅读行宽失控。卡片内边距统一 24px（`gutter`）。章节之间用 `xl`（64px）留白建立呼吸感——留白在这里就是层级，不是"空"；信息密度的高低不靠卡片堆叠传达，靠间距节奏传达。

禁止超过两层容器嵌套。极简主义依靠留白建立层级，而不是靠层层包裹的盒子。移动端塌缩为单列流式网格，最小内边距保持 16px（`md`）——任何屏幕尺寸下，间距都不应低于这个底线。

## Elevation & Depth

层次通过**色调分层**传达，不通过阴影。三层结构清晰固定：

1. Neutral 底色（`#F5F5F5`）——基础层
2. Surface 白卡（`#FFFFFF`）——内容卡片与面板
3. Primary 墨色（`#212121`）——文字与交互覆盖层

**不用 `box-shadow` 做 elevation**。阴影会让平面变得"浮夸"，背离极简的印刷质感。需要分隔时，使用 1px `secondary` 色（`#9D9D9D`）边框——这是 CSS 层的实现细节，不在 token schema 内定义。这个约束让整个视觉语言保持扁平、克制、像一份排版文档。

## Shapes

圆角哲学是**克制**。交互元素与容器默认使用 `sm`（4px）——刚好脱离锐利，又保留工程化的硬朗气质。

`full`（9999px）仅用于 chip / tag 这类小尺寸药丸元素，圆角在这里信号化"可选中"。`lg`（16px）虽已定义，但不用于按钮或卡片——过大圆角会软化极简主义的工程气质，让它滑向"亲和"而非"专业"。圆角的选择本身就是性格宣言：4px 说"我是工具"，16px 说"我是消费品"——Maliang 是前者。

## Components

**Buttons**：Primary 用深墨色填充 + 白字，hover 切到 `tertiary` 蓝（整个系统唯一允许的 hover 色）。Secondary 透明描边、无填充，靠 1px `secondary` 边框界定边界。两者都用 `label-sm` 字型（全大写 + 宽字距）强化工具感。按钮宽度不超过 200px，除非横跨整列。

**Chips**：`neutral` 底 + `primary` 字 + `full` 圆角。用于筛选标签与选中态。药丸形状把它与按钮在视觉上彻底区分——按钮是动作，chip 是状态。

**Inputs**：极简——`surface` 白底 + `sm` 圆角。默认 1px `secondary` 边框（CSS 层实现，token schema 不定义 border）。focus 时边框提升为 `tertiary` 蓝，文字色保持 `primary`。错误态用 CSS 红，**不复用 `tertiary`**，避免表单错误与 CTA 混淆。

## Do's and Don'ts

- **Do** 每屏至多保留一处 `tertiary` CTA——它的指引力来自稀缺，泛滥即失效。
- **Don't** 用 `box-shadow` 做层次；用色调分离（neutral → surface → primary）与 1px `secondary` 边框。
- **Do** 所有 `label-sm` 文字通过 `text-transform: uppercase` 渲染为大写——这是极简主义的身份印记。
- **Don't** 在窄于 768px 的屏幕使用 `headline-lg`（48px）；缩到 `headline-md`（32px）。
- **Do** 保证所有正文达到 WCAG AA 对比度（最低 4.5:1）；`primary` on `surface` 约 16:1，`primary` on `neutral` 约 14:1。
- **Don't** 把 `secondary`（#9D9D9D）用作正文主体色——对比度仅约 2.6:1，只允许出现在辅助文字与边框。
- **Do** 用 `neutral`（#F5F5F5）作页面底色，不用纯白——纯白底会让卡片失去层次依托。
- **Don't** 在单一屏幕内混用超过两种字重——字重是层级工具，不是装饰。
