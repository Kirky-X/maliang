---
version: alpha
name: Glassmorphism
description: 磨砂玻璃界面风格：以半透明、背景模糊与微妙高光，让内容悬浮在鲜艳背景之上。
colors:
  primary: "#7EA8FF"
  secondary: "#A78BFA"
  accent-pink: "#F9A8D4"
  accent-yellow: "#FCD34D"
  accent-green: "#6EE7B7"
  glass-bg: "#FFFFFF26"
  glass-border: "#FFFFFF40"
  glass-shadow: "#1F2687"
  on-glass: "#0F172A"
  on-color: "#0F172A"
  text-muted: "#64748B"
  white: "#FFFFFF"
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
    backgroundColor: "{colors.glass-bg}"
    textColor: "{colors.on-glass}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.on-glass}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 11px 23px
  input:
    backgroundColor: "{colors.glass-bg}"
    textColor: "{colors.on-glass}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  chip:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-color}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

Glassmorphism 将内容浮在半透明磨砂玻璃表面上，这些表面会模糊并染色其背后的任何东西。通过组合 `backdrop-filter: blur`、半透明填充以及微妙的白色边框与高光，这种风格以氛围式分层而非不透明卡片来营造深度。结果轻盈、现代且沉浸——界面属于它所处的环境，而不是压在环境之上。

目标受众：高端产品与品牌站点、系统与工具类应用、数据可视化仪表盘、移动界面，以及氛围与未来感打磨比信息密度更重要的创意或艺术项目。最适合用在鲜艳或渐变背景之上，这样模糊效果才可见。

## Colors

调色板分为**鲜艳玻璃色**（用于背景与点缀）与**半透明白色**（用于玻璃表面本身）。

- **primary (#7EA8FF)：** 柔和蓝——品牌点缀色与默认 chip/激活色调。搭配 `on-color`（#0F172A，近黑）作为标签，对比度 7.6:1。
- **secondary (#A78BFA)：** 柔和紫——次级点缀色与渐变端点。
- **accent-pink (#F9A8D4) / accent-yellow (#FCD34D) / accent-green (#6EE7B7)：** 鲜艳色调，用于数据可视化、标签与装饰性渐变。作为背景时搭配 `on-color` 深色文字。
- **glass-bg (#FFFFFF26)：** 核心玻璃填充——15% 不透明度的白色。每个玻璃表面（卡片、输入框、按钮）都使用它。配合 `backdrop-filter: blur(20px)` 产生磨砂效果。
- **glass-border (#FFFFFF40)：** 25% 不透明度的 1px 白色边框。定义玻璃边缘并捕捉光线。
- **glass-shadow (#1F2687)：** 标准投影 `0 8px 32px rgba(31,38,135,0.37)` 背后的彩色阴影色调。赋予玻璃悬浮于画布之上的感觉。
- **on-glass (#0F172A)：** 玻璃表面上的深石板色文字。在浅色磨砂填充上满足 AA（在白色上约 18:1）。
- **on-color (#0F172A)：** 同样的深石板色，用于白色文字会失败的鲜艳色调（例如 `primary` + 白色 = 2.4:1 ✗；`primary` + `on-color` = 7.6:1 ✓）。
- **text-muted (#64748B)：** 次级文字与说明文字。仅用于浅色背景之上的玻璃。
- **white (#FFFFFF)：** 高光与内嵌顶边光（`inset 0 1px 0 rgba(255,255,255,0.4)`）。

## Typography

**Inter**（或 SF Pro Display），覆盖五个字重（Light 300、Regular 400、Medium 500、Semibold 600、Bold 700）。

- **headline-lg (32px / 600)：** 玻璃上的主视觉与页面标题。以 `on-glass` 渲染。
- **headline-md (24px / 500)：** 卡片标题与区块页头。
- **body-md (16px / 400)：** 主正文，1.5 行高。保持 16px 或以上。
- **body-sm (14px / 400)：** 说明文字与辅助文字，使用 `text-muted`。
- **label (12px / 500，0.05em 字距)：** 按钮、chip 与标签页标签。

字体应显得轻盈——优先使用 Regular 与 Medium 而非 Bold。重字重会挤占通透的美学。

## Layout

流式网格，4px 基准。间距刻度——`xs`（4）、`sm`（8）、`md`（16）、`lg`（24）、`xl`（32）——保持宽松，让玻璃面板有悬浮的空间。

- 玻璃卡片内边距：桌面端 `lg`（24px），移动端 `md`（16px）。
- 玻璃面板之间的间隙：最少 `md`（16px）——面板不能相接，否则模糊会重叠得很难看。
- 区块节奏：`xl`（32px）。
- 断点：768px 以下单列；移动端降低模糊半径以保证性能。

## Elevation & Depth

深度来自**分层半透明**，而不是不透明阴影。玻璃表面之所以悬浮，是因为它模糊并染色其背后的鲜艳背景，并由细线 `glass-border` 与使用 `glass-shadow` 色调的柔和彩色阴影框住。

标准玻璃配方（依据来源）：

- 背景：`rgba(255,255,255,0.15)` → `glass-bg` (#FFFFFF26)
- 模糊：`backdrop-filter: blur(20px)`
- 边框：`1px solid rgba(255,255,255,0.25)` → `glass-border` (#FFFFFF40)
- 阴影：`0 8px 32px rgba(31,38,135,0.37)` → 由 `glass-shadow` 着色
- 高光：`inset 0 1px 0 rgba(255,255,255,0.4)` → 使用 `white`

层级顺序：鲜艳/渐变页面背景 → 玻璃面板 → 文字/控件。绝不要堆叠超过两层玻璃——嵌套模糊会破坏可读性与性能。

## Shapes

玻璃表面偏爱**柔和、宽大的圆角**，以呼应磨砂美学。

- **sm (8px)：** 输入框与小控件。
- **md (12px)：** 按钮与中型卡片——默认值。
- **lg (16px)：** 大玻璃面板、模态框与主视觉卡片。
- **full (9999px)：** chip、头像与药丸形开关。

锐角（0px）与柔和、液态的感觉冲突——避免使用。

## Components

- **button-primary：** `glass-bg` 填充配 `on-glass` 深色标签，`md` 圆角，`label` 字型。带 `glass-border` 与标准阴影。默认 CTA——它悬浮在画布之上。
- **button-secondary：** 不透明 `white` 填充配 `on-glass` 文字——用于玻璃按钮会在繁杂背景中消失的场合。
- **input：** `glass-bg` 填充，`on-glass` 文字，`sm` 圆角，内嵌高光。占位符使用 `text-muted`。聚焦时 `glass-border` 变亮。
- **chip：** `primary` 色调填充配 `on-color` 深色文字，`full` 圆角。选中态切换为 `secondary`。

图标采用 Outline 风格——细线条，匹配通透、轻盈的美学。

## Do's and Don'ts

- **Do** 把玻璃放在鲜艳或渐变背景之上——模糊需要有东西可模糊。
- **Don't** 堆叠超过两层玻璃——嵌套模糊会毁掉可读性与性能。
- **Do** 在玻璃上使用 `on-glass`（#0F172A）深色文字；白色文字在浅色磨砂填充上无法通过 AA。
- **Don't** 在 `primary`/`secondary` 色调上使用白色文字——无法通过 AA（2.4:1）。改用 `on-color`。
- **Do** 包含 `backdrop-filter: blur(20px)`——没有它，表面只是一个半透明盒子，不是玻璃。
- **Don't** 在性能关键的列表或低端移动设备上使用模糊——退回到不透明的 `white` 表面。
- **Do** 加上内嵌顶部高光（`white`，0.4）——它赋予玻璃"被上方照亮"的感觉。
- **Don't** 使用 0px 圆角——锐角与柔和美学冲突。
