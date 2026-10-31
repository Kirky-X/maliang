---
version: alpha
name: Neomorphism
description: 一种柔和的挤出式 UI 风格，在单色画布上使用双向光影，带来可触的未来感。
verified: 2026-10-24
license: 自著
colors:
  primary: "#6B7280"
  accent: "#7A87BA"
  accent-cyan: "#7DC9FC"
  accent-purple: "#AC84E4"
  background: "#E0E5EC"
  surface: "#E0E5EC"
  on-surface: "#4B5563"
  on-primary: "#FFFFFF"
  muted: "#9CA3AF"
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.25
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.33
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
  label:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0.05em
rounded:
  sm: 8px
  md: 12px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-raised:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

Neomorphism（Soft UI）创造仿佛从单一单色表面挤出而成的界面。通过对与背景同色的元素施加柔和的双向阴影，它产生可触的、未来感的美学——就像控件被压入或抬出某种柔软材质。结果是平静、低对比、安静现代，长时间使用也舒适。

目标受众：系统与工具类应用、数据与信息仪表盘、协作与效率平台，以及重视安宁、低疲劳界面而非高对比紧迫感的轻量消费级应用。

**关于对比度的说明（公开而非隐藏）：** 源调色板有意低饱和、偏浅。它最深的中性色 `primary`（#6B7280）在标志性 `background`（#E0E5EC）画布上仅达到 3.8:1——低于 WCAG AA。为了在尊重风格的同时保持文字可读，正文使用 `on-surface`（#4B5563），这是来自同一中性色族的更深伴随灰，在 6:1 下通过 AA。`primary`（#6B7280）保留给按钮填充，在那里与 `on-primary` 白色文字搭配为 4.8:1。这一取舍遵循来源自身的告诫：在低对比语境中，确保可读性与明显的交互反馈。

## Colors

调色板建立在一个基础画布色与一小组柔和点缀色之上。

- **background (#E0E5EC)：** 标志性的浅灰蓝画布。每个表面都共享这个颜色，因此定义边缘的是阴影——而不是填充。
- **surface (#E0E5EC)：** 按设计就与 `background` 完全相同。新拟态元素从不靠填充区分；只靠光与影。
- **primary (#6B7280)：** 源调色板中最深的中性色。用作主按钮填充，也用作边框/分隔线。搭配 `on-primary`（#FFFFFF）作为按钮标签，对比度 4.8:1。
- **on-surface (#4B5563)：** 正文与标题文字。比 #6B7280 更深的伴随色，选择它是为了让文字在浅色画布上通过 WCAG AA（6:1）。所有文字——标题、正文、标签——都使用这个 token。
- **accent (#7A87BA)：** 柔和的蓝紫色，用于激活态、选中 chip 与焦点环。仅装饰/交互——不用于正文（画布上 2.8:1）。
- **accent-cyan (#7DC9FC) / accent-purple (#AC84E4)：** 渐变端点与图标色调。少量用于愉悦感（按来源为蓝→青、青→紫、紫→粉的渐变）。
- **muted (#9CA3AF)：** 占位符文字与禁用态。仅限大字号或非关键用途。
- **on-primary (#FFFFFF)：** `primary` 填充上的白色标签文字。

## Typography

**Inter**（或 SF Pro Display）承载整个系统，覆盖五个字重（Light 300、Regular 400、Medium 500、Semibold 600、Bold 700）。

- **headline-lg (32px / 600)：** 页面标题。以 `on-surface` 渲染。
- **headline-md (24px / 500)：** 区块标题与卡片标题。
- **body-md (16px / 400)：** 主正文，1.5 行高。绝不低于 16px。
- **body-sm (14px / 400)：** 说明文字、辅助文字与元数据。
- **label (12px / 500，0.05em 字距)：** 按钮、chip 与开关。字距略宽于正文，以分隔控件标签与散文。

保持字重克制——每屏两个字重最理想。沉重的粗体使用会削弱平静的美学。

## Layout

简单的流式网格，4px 基准单位。间距刻度——`xs`（4）、`sm`（8）、`md`（16）、`lg`（24）、`xl`（32）——刻意紧凑，因为新拟态依赖宽裕的画布呼吸空间，而不是密集堆叠。

- 卡片内边距：标准 `md`（16px），主面板 `lg`（24px）。
- 区块间隙：`xl`（32px）。避免更大的间隙——柔和美学受益于邻近感。
- 触控目标：最小 44×44px（用 `md` 间距保证余量）。
- 断点：768px 以下单列；在所有尺寸下保持 `md`（16px）作为最小内边距。

## Elevation & Depth

深度是新拟态的决定性特征。元素不使用投影，而是使用**双向阴影**——左上浅阴影与右下深阴影——看起来像从共享的 `surface`/`background` 画布上挤出（或被压入）。

- **Raised（默认）：** `box-shadow: -9px -9px 16px #FFFFFF, 9px 9px 16px rgba(163,177,198,.6);` ——元素看起来从表面升起。（标准配方：[`references/templates/neumorphism.md`](../../../references/templates/neumorphism.md) ——偏移 8-10px，模糊 ≈ 2×偏移，浅色左上 / 深色右下，135°。）
- **Pressed/inset：** `box-shadow: inset -9px -9px 16px #FFFFFF, inset 9px 9px 16px rgba(163,177,198,.6);` ——元素看起来被压入。用于激活开关、按下的按钮与选中的输入框。
- **Flat：** 无阴影——用于禁用或信息性表面。

假设光源在左上方，并始终一致。绝不要在同一屏幕内反转。阴影必须保持柔和——锐利阴影会破坏材质错觉。避免堆叠超过两个海拔层级；美学依赖单一、平静的平面。

## Shapes

新拟态偏爱**柔和、宽大的圆角**——锐角与柔和阴影美学冲突。

- **sm (8px)：** 输入框与小控件——柔和度的下限。
- **md (12px)：** 按钮与中型卡片——大多数组件的默认圆角。
- **lg (16px)：** 大面板与容器——更柔和、更显眼。
- **full (9999px)：** chip、头像与圆形开关。

绝不使用 0px 圆角——它会破坏柔和美学。在组件组内保持圆角一致。

## Components

- **button-primary：** `primary`（#6B7280）填充配 `on-primary` 白色标签。主 CTA。`md` 圆角，`label` 字型。按下时过渡为内嵌阴影。
- **button-raised：** `surface` 背景（与画布相同）配 `on-surface` 文字，通过双向阴影抬升。最典型的新拟态按钮——用于次级动作。
- **input：** `surface` 背景，`on-surface` 文字，`sm` 圆角，内嵌阴影显得凹陷。占位符使用 `muted`。聚焦时内嵌阴影略微加深，并出现 `accent` 焦点环。
- **chip：** `surface` 背景，`on-surface` 标签，`full` 圆角。选中态使用 `accent` 填充。

图标简单而柔和——描边字重、圆头线帽、没有锐利细节。

## Do's and Don'ts

- **Do** 每个抬升元素都使用双向阴影（左上浅、右下深）。
- **Don't** 用填充区分元素——只用阴影与内嵌。
- **Do** 所有文字使用 `on-surface`（#4B5563），以在浅色画布上通过 WCAG AA。
- **Don't** 用 `accent`（#7A87BA）做正文——无法通过 AA（2.8:1）。
- **Do** 在整个屏幕内保持光源一致（左上）。
- **Don't** 堆叠超过两个海拔层级——美学需要单一平静的平面。
- **Do** 按下与激活态使用内嵌阴影。
- **Don't** 使用 0px 圆角——它们会破坏柔和美学。
- **Do** 当仅靠阴影不足以在低视力语境中保证可读性时，退回到微妙的 `primary` 边框。
