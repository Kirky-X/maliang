---
version: alpha
name: Illustrative
description: 温暖、故事驱动的系统，将手绘插画与鲜艳、圆润的几何形结合。
verified: 2026-10-24
license: 自著
colors:
  primary: "#5C5CE7"
  secondary: "#FF8A56"
  accent-green: "#7ED56F"
  accent-cyan: "#4ECDC4"
  accent-yellow: "#FFD166"
  ink: "#2D3436"
  ink-muted: "#636E72"
  surface: "#FFFFFF"
  neutral: "#F7F9FA"
  surface-muted: "#DFE6E9"
typography:
  headline-display:
    fontFamily: Round Friendly
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Round Friendly
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Round Friendly
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.25
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
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
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
  xl: 48px
  gutter: 20px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.md}"
    padding: 12px 28px
  button-primary-hover:
    backgroundColor: "{colors.ink}"
  button-secondary:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.ink}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.md}"
    padding: 11px 27px
  button-text:
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
  chip:
    backgroundColor: "{colors.accent-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  chip-success:
    backgroundColor: "{colors.accent-green}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  chip-info:
    backgroundColor: "{colors.accent-cyan}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  chip-secondary:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.full}"
    padding: 4px 12px
    typography: "{typography.label-caps}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

Illustrative 是一种建立在温暖、角色与故事之上的设计语言。手绘插画、鲜艳而有纪律的色彩，以及圆润的几何形共同作用，让产品显得亲和、有人情味。界面不只是呈现信息——它邀请用户进入。让设计温暖，让体验难忘（MAKE DESIGN WARM, MAKE EXPERIENCE MEMORABLE）。

目标受众：需要情感连接的面向消费者产品——学习、效率、社区与生活方式类应用。产品应像一位友好的伙伴，而不是一件工具。

**插画风格：** 扁平风格的角色插画，描绘多样生活场景（工作、学习、运动、休闲），以鲜艳色彩渲染。插画调色板与 UI 调色板一致——`primary` 紫、`secondary` 橙、`accent-green`、`accent-cyan` 与 `accent-yellow`——因此图画与界面读起来像一个系统。插画出现在空状态、新手引导与主视觉时刻；它们绝不围绕关键数据做装饰。

## Colors

调色板将一个果断的主色与一组插画点缀色搭配，并由温暖的灰色打底。

- **Primary (#5C5CE7)：** 友好的紫色。驱动主 CTA、链接与焦点环。紫底白字达到 5.0:1——按钮文字安全。
- **Secondary (#FF8A56)：** 温暖橙色，用于插画点缀、次级表面与俏皮高亮。不用于白底正文（2.3:1，未通过 AA）；在橙色填充上使用 `ink`（#2D3436）文字（5.2:1，通过）。
- **Accent-green (#7ED56F)：** 成功态与插画植物。仅装饰——绝不用于文字。
- **Accent-cyan (#4ECDC4)：** 信息态与插画中的水/天空。装饰性；青色上的 `ink` 文字通过（6.3:1）。
- **Accent-yellow (#FFD166)：** chip 与徽章背景，插画的暖意。黄色上的 `ink` 文字通过（8.5:1）。
- **Ink (#2D3436)：** 深暖灰，用于所有主文字（白底 12.2:1）。
- **Ink-muted (#636E72)：** 说明文字与元数据（白底 5.2:1，`neutral` 上 5.0:1）。
- **Surface (#FFFFFF)：** 纯白，用于卡片与输入框。
- **Neutral (#F7F9FA)：** 近白页面背景——比纯白更柔和，赋予产品纸张般的温暖。
- **Surface-muted (#DFE6E9)：** 浅灰，用于次级容器与 `button-secondary` 填充（配 `ink` 文字 9.6:1）。

## Typography

两种友好的字体：**Round Friendly** 用于展示标题（圆润的字端强化亲和力），**Inter** 用于正文与 UI 标签（开放的字怀保持可读性）。

- **Headlines：** Round Friendly Bold/Semibold，大字号。展示字号下的紧凑负字距让标题足够密集，显得有意为之。Round Friendly 只是展示字体——绝不要用于正文。
- **Body：** Inter Regular，16px，宽松的 1.6 行高。开放感匹配友好语调——正文行高绝不压缩到 1.5 以下，正文也绝不低于 16px。
- **Labels：** Inter Medium，12px，0.08em 字距。用于标签、元数据与按钮标签。全大写是可选的——Illustrative 不像编辑型系统那样僵硬；为温暖感可以接受句子式大小写。

## Layout

布局使用 **12 列流式网格**（max-width 1200px），8px 基准间距单位，但允许有意的非对称，以显得不那么工程化。

卡片使用 16px–24px 内边距（`md`–`lg`）。区块分隔使用 `xl`（48px）创造呼吸空间。`gutter` token（20px）控制列间间隙。插画可以在主视觉时刻打破网格——它们是唯一被认可的对列结构的偏离，用于注入个性而不牺牲可读性。

移动端断点：塌缩为单列，插画缩放到全宽。在所有屏幕尺寸下保持 `md`（16px）作为最小内边距。

## Elevation & Depth

深度通过**柔和色调分层与轻柔阴影**传达——与扁平系统不同，Illustrative 允许卡片上使用单一柔和阴影，让卡片从 `neutral` 背景上浮起。

1. Neutral 背景（`#F7F9FA`）——基础层
2. Surface（`#FFFFFF`）——卡片与输入框，可选柔和阴影
3. Surface-muted（`#DFE6E9`）——内嵌或次级容器

阴影：`0 4px 12px rgba(45, 52, 54, 0.08)`——低不透明度、短扩散、温暖。绝不要使用锐利或深色阴影；它们会破坏友好的性格。每个组件只用一个阴影——不要堆叠。

## Shapes

形状语言由**圆润的友好感**定义。卡片、输入框与按钮的默认圆角是 `md`（12px）。`sm`（8px）用于小的内联元素；`lg`（16px）用于显眼的卡片。

`full`（9999px）圆角保留给 chip、徽章与头像形元素。圆润几何是身份核心——绝不要在主容器上使用锐利的 0px 直角。

## Components

**Buttons：** 主按钮使用 `primary` 紫（#5C5CE7）配白色文字——品牌之声。悬停时，填充切换为 `ink`（#2D3436），形成落地的按压态。次级按钮使用 `surface-muted`（#DFE6E9）配 `ink` 文字。文字按钮使用 `primary` 紫。所有按钮使用 `md`（12px）圆角与 `label-caps` 字型。

**Chips：** 药丸形（`full` 圆角）标签，用于状态与选中。默认 chip 使用 `accent-yellow`（#FFD166）配 `ink` 文字。变体把调色板映射到语义：`chip-success`（`accent-green`）、`chip-info`（`accent-cyan`）与 `chip-secondary`（`neutral` 背景配 `ink-muted` 文字，用于弱化标签）。全部使用 `label-caps` 字型。药丸形与温暖填充让它们区别于圆角按钮。

**Input fields：** 白色 `surface`，`md`（12px）圆角，默认 1px `surface-muted` 边框。聚焦时，边框提升为 `primary`（紫）——温暖的注意力信号。占位符使用 `ink-muted`。

## Do's and Don'ts

- **Do** 在空状态、新手引导与主视觉时刻使用插画——它们是系统的心脏。
- **Don't** 在白底上放 `secondary` 橙色文字——对比度不足（2.3:1）；改用 `ink`。
- **Do** 让每种点缀色搭配 `ink`（#2D3436）文字，或在对比度允许处搭配白色文字。
- **Don't** 在主容器上使用锐利的 0px 直角——圆润几何就是身份。
- **Do** 让插画与 UI 调色板保持一致；脱离调色板的图画会破坏系统。
- **Don't** 使用沉重或深色阴影——只允许那一层柔和的暖阴影。
- **Do** 保证所有背景上的所有正文达到 WCAG AA 对比度（≥ 4.5:1）。
- **Don't** 把 Round Friendly 用于正文——它只是展示字体。
