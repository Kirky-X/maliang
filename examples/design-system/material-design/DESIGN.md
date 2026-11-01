---
version: alpha
name: Material Design
description: Google 的跨平台设计语言，建立在材质隐喻、有意义的动效与基于阴影的海拔之上。
colors:
  primary: "#6200EE"
  primary-light: "#7C4DFF"
  tertiary: "#BB86FC"
  secondary: "#03DAC6"
  background: "#FFFFFF"
  surface: "#FFFFFF"
  on-surface: "#212121"
  on-primary: "#FFFFFF"
  on-secondary: "#000000"
  outline: "#BDBDBD"
  error: "#B00020"
typography:
  headline-lg:
    fontFamily: Roboto
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.25
  headline-md:
    fontFamily: Roboto
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.33
  body-md:
    fontFamily: Roboto
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Roboto
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
  label:
    fontFamily: Roboto
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0.1em
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  xxxl: 48px
  huge: 64px
components:
  button-filled:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 10px 24px
  button-filled-hover:
    backgroundColor: "{colors.primary-light}"
  button-outlined:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 9px 23px
  button-text:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    padding: 10px 12px
  fab:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.full}"
    padding: 16px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 16px
  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

Material Design 是 Google 的设计语言，建立在材质隐喻之上——受物理世界启发的表面、边缘与阴影——并结合有意义的动效，跨平台提供一致、直觉、可预测的体验。UI 被视为层层数字纸张，可以响应输入而分裂、合并与抬升，光与影负责指示层级。

目标受众：构建跨平台产品（Android、Web、iOS）的团队、企业后台与管理系统，以及层级清晰、组件可预测与可访问性不可妥协的复杂数据应用。Material Design 尤其适合 Android 应用与必须在各处都显得原生的多平台产品，以及优先考虑可访问性标准的团队。

## Colors

调色板将深紫 `primary` 与鲜亮青绿 `secondary` 搭配，并由中性灰阶打底。

- **primary (#6200EE)：** 深紫——品牌锚点。用于填充按钮、激活态与关键可供性。搭配 `on-primary`（#FFFFFF）作为标签，对比度 7.6:1。
- **primary-light (#7C4DFF)：** 更浅的紫色调伴随色，用于 `primary` 填充上的悬停态（见 `button-filled-hover`）。
- **tertiary (#BB86FC)：** 来自源调色板的淡紫点缀。用于装饰性高亮与选中态，在这些位置 `primary` 会过于沉重。
- **secondary (#03DAC6)：** 鲜亮青绿，作为次级点缀——FAB 填充与开关高亮。使用 `on-secondary`（#000000），因为青绿足够浅，黑色文字在 11.9:1 下通过 AA，而白色文字会失败。
- **background / surface (#FFFFFF)：** 两者都默认为纯白。`background` 是页面画布；`surface` 是卡片/纸张层。前景文字使用 `on-surface`（#212121，近黑），对比度 16:1。
- **outline (#BDBDBD)：** 细线分隔线与描边按钮的描边。仅装饰——绝不用于正文。
- **error (#B00020)：** 专用于错误态与表单校验消息。

## Typography

单一字体——**Roboto**——通过四个字重（Light 300、Regular 400、Medium 500、Bold 700）承载整个层级。

- **headline-lg (32px / 700)：** 屏幕标题与主视觉文字。紧凑而自信。
- **headline-md (24px / 500)：** 区块标题与对话框标题。
- **body-md (16px / 400)：** 主正文，1.5 行高，用于长文可读性。正文绝不低于 16px。
- **body-sm (14px / 400)：** 次级文字、说明文字与辅助文字。
- **label (12px / 500，0.1em 字距)：** 按钮、chip、标签页与导航。宽字距是 Material 的签名——凡是控件内的文字标签都应用它。

## Layout

**12 列网格**构建每个屏幕，基础间距单位为 4px。间距刻度——`xs`（4）、`sm`（8）、`md`（12）、`lg`（16）、`xl`（24）、`xxl`（32）、`xxxl`（48）、`huge`（64）——覆盖触控目标、槽宽与区块节奏。

- 最小触控目标：48×48px（使用 `xxxl` 间距保证余量）。
- 卡片内边距：移动端 `lg`（16px），桌面端 `xl`（24px）。
- 区块分隔：顶层区块之间 `huge`（64px）；区块内 `xxl`（32px）。
- 断点：600px 以下将 12 列网格塌缩为单列；在 lg 断点用 `xl` 扩大槽宽。

## Elevation & Depth

深度通过**阴影海拔**表达，而不是颜色。Material 表面占据五个海拔层级之一（0dp → 24dp 阴影）。海拔越高意味着优先级越高，阴影越柔和、越弥散。

动效强化海拔：表面在按压时抬升（海拔过渡），FAB 展开为纸张，模态框以减速曲线缩放进入。所有动效都应自然且有意义——绝不装饰。按下的卡片以 `lg` 阴影升起；对话框以 `xxxl` 海拔到达。

## Shapes

Material 形状语言使用四种圆角加 `none` 来示意组件类型：

- **none (0)：** 满幅图像与分隔线。
- **sm (4px)：** 文本字段、描边按钮与小卡片——克制且功能化。
- **md (8px)：** 填充按钮、对话框与中型卡片——大多数表面的默认值。
- **lg (16px)：** 底部抽屉、大卡片与 FAB 展开的纸张——更柔和、更显眼。
- **full (9999px)：** FAB、chip 与头像——示意可触性的药丸/圆形。

绝不要在同一组件组内混用 `sm` 与 `full`。

## Components

- **button-filled：** 实心 `primary` 背景配 `on-primary` 标签。默认 CTA。使用 `md` 圆角与 `label` 字型。悬停时背景提升为 `primary-light`（`button-filled-hover`）。
- **button-outlined：** 白色 `background` 填充，`primary` 文字，1px `outline` 描边。用于需要较少视觉重量的次级动作。
- **button-text：** 白色 `background`，`primary` 文字，无描边。三级与流内动作（例如对话框中的"取消"）。
- **fab：** 圆形（`full` 圆角）`secondary` 填充按钮，承载 `on-secondary` 文字/图标。突出单一的主屏幕动作——每屏只有一个 FAB。
- **input：** 白色 `surface` 配 `on-surface` 文字，`sm` 圆角，默认用 `outline` 描边。聚焦时边框提升为 `primary`。辅助文字以 `body-sm` 显示在下方。
- **chip：** `surface` 背景，`on-surface` 标签，`full` 圆角。用于筛选与选中。

图标遵循 Outlined 风格，24dp，以保持系统一致。

## Do's and Don'ts

- **Do** 每屏只保留一个 FAB——它的显眼程度取决于唯一性。
- **Don't** 用 `secondary` 青绿做正文——它在白底上无法通过 AA。
- **Do** 对每个控件内标签应用 `label` 字型（0.1em 字距）。
- **Don't** 在组件组内混用圆角——按钮保持 `md`，chip 保持 `full`。
- **Do** 保持 WCAG AA（≥4.5:1）——每个 `on-*` token 都配对通过。
- **Don't** 用投影做装饰——海拔是有意义的，并与状态绑定。
- **Do** 只把 `error`（#B00020）用于错误；绝不用作品牌色。
- **Don't** 把正文字号缩到 16px 以下（`body-md`）。
