---
version: alpha
name: Swiss Style
description: 网格驱动、排版理性的系统，以单一信号红承担交互。
verified: 2026-10-24
license: 自著
colors:
  primary: "#E30613"
  ink: "#000000"
  ink-muted: "#666666"
  surface: "#FFFFFF"
  neutral: "#F2F2F2"
typography:
  headline-display:
    fontFamily: Helvetica Neue
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Helvetica Neue
    fontSize: 40px
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Helvetica Neue
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.25
  body-md:
    fontFamily: Helvetica Neue
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: Helvetica Neue
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Helvetica Neue
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
rounded:
  sm: 2px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  gutter: 24px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 12px 28px
  button-primary-hover:
    backgroundColor: "{colors.ink}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 11px 27px
  button-text:
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

瑞士风格（国际主义排版风格）是一种建立在网格系统、理性排版与客观信息层级之上的设计语言。界面传达清晰与工程精度：每个元素都通过功能而非装饰赢得自己的位置。单一信号红（`#E30613`）驱动所有交互；其余一切都是灰度逻辑。

目标受众：信息产品、数据分析平台、专业工具与 B2B 服务，在这些领域，信任来自清晰而非装饰。产品应像一件精密工程的仪器，而不是一个被造型过的表面。

## Colors

调色板是高对比灰度，由单一信号红锚定。

- **Primary (#E30613)：** 标志性的瑞士红。保留给主 CTA、激活态与关键数据强调。少量使用——它的力量来自稀缺。在白底上达到约 4.9:1 对比度；绝不要把红色文字放在 `neutral`（#F2F2F2）背景上（降到约 4.4:1，低于 AA）。
- **Ink (#000000)：** 纯黑，用于标题、主文字与次级按钮文字。提供最大对比度（白底 21:1）与恒久感。
- **Ink-muted (#666666)：** 石板灰，用于说明文字、元数据与 chip 文字。白底 5.7:1，`neutral` 上 5.2:1——正文通过 AA。
- **Surface (#FFFFFF)：** 纯白，用于卡片、输入框与抬升容器。保持与 neutral 页面背景的色调分隔。
- **Neutral (#F2F2F2)：** 浅灰基础，用于页面背景。比白色更柔和；无需装饰就能在色调上分隔内容区。
- **Divider (#CCCCCC)：** 用于 1px 边框与分隔线。仅装饰——绝不用于文字（白底 1.6:1）。

## Typography

Helvetica Neue 承载整个系统——它的中性就是重点。层级来自字号与字重，而不是字体变化。

- **Headlines：** 大字号下的紧凑负字距模仿瑞士印刷的密度。展示字号使用 Bold（700）；区块标题降到 Medium（500）。绝不要在 768px 以下不降到 `headline-lg` 就缩放 `headline-display`。
- **Body：** Regular（400），16px，1.55 行高，用于持续阅读。正文不要低于 16px。
- **Labels：** Medium（500），12px，宽字距（0.08em），全大写渲染——保留给元数据、标签与 UI 控件。散文与元数据之间的视觉分隔是瑞士身份的核心；不要把 `label-caps` 用于段落文字。

## Layout

布局遵循严格的 **12 列网格**（max-width 1280px，居中），8px 基准间距单位。

网格对齐不可妥协：每个元素都吸附到列边界与 8px 节奏。区块分隔使用 `xl`（64px）创造呼吸空间；组件内边距使用 `md`（16px）。`gutter` token（24px）控制列间间隙。

移动端断点：塌缩为 4 列网格。在所有屏幕尺寸下保持 `md`（16px）作为最小内边距。网格就是结构——绝不要为装饰效果破坏对齐。

## Elevation & Depth

深度通过**色调分层与 1px 分隔线**传达，绝不用投影。

1. Neutral 背景（`#F2F2F2`）——基础层
2. 白色表面（`#FFFFFF`）——内容卡片与输入框
3. Ink（`#000000`）——文字与交互覆盖层

如果组件需要分隔，使用 1px `#CCCCCC` 边框。禁止 `box-shadow`——视觉语言必须保持扁平、印刷般、客观。

## Shapes

形状语言由**工程化锐利**定义。圆角最小：交互元素与容器使用 `sm`（2px）——刚好避免像素渲染的粗糙感，仅此而已。

`full`（9999px）圆角专用于 chip 与标签——小的药丸形元素，圆边示意可选中性。绝不要把 `full` 用于按钮或卡片；圆润会软化工程化美学并破坏瑞士性格。

## Components

**Buttons：** 主按钮使用信号红（`#E30613`）配白色文字——系统中唯一的红色填充。悬停时，填充切换为 `ink`（`#000000`）。次级按钮使用白色 `surface` 填充，配 1px `#CCCCCC` 边框（通过 CSS）与 `ink` 文字。文字链接使用 `primary` 红。所有按钮使用 `label-caps` 字型，强化功能主义、标签般的性格。

**Chips：** `neutral`（#F2F2F2）背景配 `ink-muted`（#666666）文字与 `full` 圆角。用于筛选与元数据标签。药丸形让它们区别于锐边按钮。

**Input fields：** 白色 `surface`，2px 圆角，默认 1px `#CCCCCC` 边框。聚焦时，边框提升为 `primary`（红）——输入处于活跃状态的唯一信号。占位符使用 `ink-muted`。

## Do's and Don'ts

- **Do** 每个屏幕视图只保留一个使用红色的主 CTA（`#E30613`）——稀缺就是它的力量。
- **Don't** 使用投影；所有深度都由色调层与 1px `#CCCCCC` 边框承载。
- **Do** 让每个元素吸附到 8px 网格与 12 列结构。
- **Don't** 把红色文字放在 `neutral`（#F2F2F2）背景上——对比度降到 4.5:1 以下。
- **Do** 通过 `text-transform: uppercase` 把 `label-caps` 渲染为全大写。
- **Don't** 把 `full` 圆角用于按钮或卡片——只用于 chip 与标签。
- **Do** 保证所有背景上的所有正文达到 WCAG AA 对比度（≥ 4.5:1）。
- **Don't** 引入装饰性字体——Helvetica Neue 就是整个系统。
