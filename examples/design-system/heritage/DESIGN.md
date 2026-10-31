---
version: alpha
name: Heritage
description: 以建筑式极简与新闻般的庄重感打造的编辑型产品。
verified: 2026-10-24
license: 自著
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
typography:
  headline-display:
    fontFamily: Public Sans
    fontSize: 64px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 4px
  md: 8px
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
    textColor: "{colors.neutral}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 12px 28px
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 11px 27px
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.secondary}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
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

建筑式极简主义遇上新闻般的庄重感。界面唤起高级哑光质感——一份高端大报或当代画廊图录。每个布局决策都优先考虑阅读清晰度而非装饰。交互元素保持克制：单一的土红色点缀承担所有行动号召的重量。

目标受众：将视觉克制与可信度联系在一起的高素养读者与专业人士。产品应让人感觉像翻开一本设计精良的杂志，而不是加载一个 app。

## Colors

调色板扎根于高对比中性色，并由单一而富有感染力的点缀色锚定。

- **Primary (#1A1C1E)：** 深墨色，用于标题与核心文字。提供最大可读性与恒久感。用于所有主文字、主按钮与轮廓。
- **Secondary (#6C7278)：** 精致的石板灰，用于功能性元素——边框、说明文字、占位符文字与元数据。绝不用作背景填充；它只存在于辅助角色中。
- **Tertiary (#B8422E)：** 土砖红，作为交互的唯一驱动。专用于主 CTA、悬停态与关键高亮。每屏不要对超过一个元素使用 tertiary——它的力量来自稀缺。
- **Neutral (#F7F5F2)：** 温暖的石灰岩色，作为所有页面的基础。比纯白更柔和；赋予产品可触的、纸张般的感觉。
- **Surface (#FFFFFF)：** 纯白，用于卡片、模态框与抬升容器，以保持与 neutral 背景的色调分隔。

## Typography

策略利用两种性格分明的字体：**Public Sans** 承载编辑之声；**Space Grotesk** 处理所有技术与元数据角色。

- **Display & Headlines：** Public Sans 以不同字重建立视觉层级。大字号使用紧凑的负字距（`-0.03em`），达到印刷标题的密度。绝不要在小屏宽度上不缩小就使用 `headline-display`。
- **Body：** Public Sans Regular，16px，宽松行高（1.6），确保长文可读性。正文不要低于 16px。
- **Labels：** Space Grotesk 专用于时间戳、标签、元数据与 UI 标签。始终以全大写渲染，并配宽字距（`0.1em`）。散文与元数据之间的这种视觉分隔是核心身份元素——不要把 `label-caps` 用于段落文字。

## Layout

布局遵循**固定最大宽度网格**（max-width: 1200px，居中），配严格的 8px 间距刻度。

卡片使用 24px 内边距（`gutter`）。区块分隔使用 `xl` 间距（64px），在内容块之间创造呼吸空间。避免嵌套超过两层容器——这种设计语言依靠留白建立层级，而不是分层。

移动端断点：塌缩为单列流式网格。在所有屏幕尺寸下保持 16px 基准间距单位（`md`）作为最小内边距。

## Elevation & Depth

深度通过**色调分层**传达，而不是投影。层级是：

1. Neutral 背景（`#F7F5F2`）——基础层
2. 白色表面（`#FFFFFF`）——内容卡片与面板
3. Primary 墨色（`#1A1C1E`）——文字与交互覆盖层

不要用 `box-shadow` 做海拔。如果组件中必须传达深度，使用 secondary 色（`#6C7278`）的 1px `border`，而不是阴影。这让视觉语言保持扁平、印刷般的质感。

## Shapes

形状语言由**建筑式锐利**定义。所有交互元素与容器默认使用 `sm` 圆角（4px）。这提供了恰到好处的柔和感，显得现代，同时保持刚性、工程化的美学。

`full` 圆角（9999px）专用于 chip 与标签——小的药丸形元素，圆边示意可选中性。绝不要把 `full` 用于按钮或卡片。

## Components

**Buttons：** 主按钮使用深墨背景配 neutral 文字。悬停时，背景切换为 tertiary（土红）——唯一被认可的悬停色。次级按钮为无填充描边。两者都使用 `label-caps` 字型，以强化功能主义性格。按钮宽度不应超过 200px，除非横跨整列。

**Chips：** Neutral 背景配 secondary 文字与边框。用于筛选标签与选中态。药丸形（full 圆角）在视觉上与按钮区分开。

**Input fields：** 极简——白色背景，微妙的 `sm` 圆角。边框是 CSS 层细节（token schema 不定义 border 属性），默认实现为 1px secondary 描边。聚焦时，边框提升为 primary 色。错误态使用 CSS 红色；表单错误中不使用 `tertiary`，以免与交互 CTA 混淆。

## Do's and Don'ts

- **Do** 每个屏幕视图只对一个 CTA 使用 `tertiary`——它的冲击力取决于稀缺。
- **Don't** 添加投影；改用色调分隔与 1px 边框。
- **Do** 通过 `text-transform: uppercase` 把所有 `label-caps` 文字渲染为全大写。
- **Don't** 在窄于 768px 的屏幕上使用 `headline-display`（64px）——缩到 `headline-lg`。
- **Do** 保证所有背景上的所有正文达到 WCAG AA 对比度（最低 4.5:1）。
- **Don't** 在单一组件组内混用 `sm` 与 `full` 圆角。
- **Do** 用 `neutral`（#F7F5F2）作页面背景，而不是纯白。
- **Don't** 在单一屏幕上使用超过两种字重。
