---
version: alpha
name: Brutalism
description: High-contrast, raw-material functionalism with forceful typography for data-dense and industrial interfaces.
colors:
  primary: "#00F5C3"
  secondary: "#007BFF"
  tertiary: "#6C00FF"
  neutral: "#111111"
  surface: "#2A2A2A"
  on-surface: "#FFFFFF"
  on-primary: "#111111"
  error: "#FF2D55"
  outline: "#555555"
typography:
  headline-display:
    fontFamily: Chakra Petch
    fontSize: 64px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  headline-lg:
    fontFamily: Chakra Petch
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  headline-md:
    fontFamily: Chakra Petch
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.2
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
    fontFamily: Chakra Petch
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.12em"
  mono:
    fontFamily: Chakra Petch
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.04em"
rounded:
  none: 0px
  sm: 2px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
  gutter: 16px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.none}"
    padding: 12px 24px
  button-secondary:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.none}"
    padding: 11px 23px
  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.none}"
    padding: 4px 12px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

野蛮主义强调功能与结构，去除一切冗余装饰。它以高对比度、粗陋材质和强烈的排版，创造直接而有力的视觉体验——参照不是某张漂亮的 app 截图，而是工业控制台、终端界面与 90 年代的早期网络美学。当装饰被剥离，剩下的就是信息本身：数据即层级，对比即指引。

目标场景是数据仪表盘、监控系统、企业后台、开发者工具与工业/未来主义产品。目标用户是追求效率的专业人士——运维、工程师、数据分析师。他们不需要被取悦，需要被尊重。情感调性是直接、硬朗、不妥协——像打开一台正在运行的工业设备面板，而不是加载一个消费品 app。

## Colors

调色板由高饱和的电气色与深暗中性色构成。亮色负责指引，暗色负责承载。

- **Primary (#00F5C3)**：青绿，主 CTA 填充色与焦点指示。在深色背景上提供最高辨识度。不用于正文文字（在浅底上对比不足），只作为填充或焦点环。
- **Secondary (#007BFF)**：电蓝，次级交互与链接。仅用于交互态，不用于装饰。
- **Tertiary (#6C00FF)**：紫，强调与高亮态。每屏至多一处，稀缺即力度。
- **Neutral (#111111)**：近黑，页面底色。野蛮主义的视觉重量来自深暗背景——它让亮色 CTA 像信号灯一样跳出。
- **Surface (#2A2A2A)**：抬升容器色——卡片、输入框、面板。与 neutral 形成 1 个明度阶的层次分离。
- **On-surface (#FFFFFF)**：surface 之上的文字色。纯白在 #2A2A2A 上对比约 14:1，保证数据密集场景的可读性。
- **On-primary (#111111)**：primary 之上的文字色。深墨在青绿上对比约 13:1，确保主按钮文字清晰。
- **Error (#FF2D55)**：错误与危险态。不用于交互 CTA，避免与 primary 混淆。
- **Outline (#555555)**：1px 边框与分隔线。CSS 层实现，token schema 不定义 border 属性。

源调色板另含 #00B8A9（青）、#FFCC00（黄）、#00FF59（绿）、#808080、#AAAAAA 等状态色——它们用于数据可视化与状态指示，不进入核心 UI token 体系，按需在 CSS 层引用。

## Typography

策略是**双字族对位**：Chakra Petch 承担标题与标签的工业气质，Inter 承担正文的可读性。Chakra Petch 的几何方折感与野蛮主义同源——它本身就是"工程化"的视觉宣言。

- **Headlines (Chakra Petch / Bold)**：`headline-display` (64px) 用于数据仪表盘的主标题与单页英雄字。负字距 `-0.02em` 模拟印刷标题的紧凑密度。768px 以下必须降到 `headline-lg`，否则压迫感过强。
- **headline-lg (40px) / headline-md (24px)**：区块标题与卡片标题。轻负字距保持紧凑。
- **Body (Inter / Regular)**：`body-md` (16px) 行高 1.6，承担数据描述与说明文字。**不得低于 16px**——野蛮主义不等于把字变小，而是让每个字号都有存在的理由。
- **label-caps (Chakra Petch / Medium, 12px)**：按钮、标签、表头、状态指示专用。必须配合 `text-transform: uppercase` 与 `0.12em` 字距——全大写 + 宽字距是野蛮主义的身份印记，把"功能性文字"与"阅读性文字"在视觉上彻底分离。不用于段落正文。
- **mono (Chakra Petch / Regular, 13px)**：数据流、代码、技术数值专用（如 `DATA IN 12.4 TB/s`）。轻字距 `0.04em` 保持等宽感。

字重选择遵循"少即是多"：一屏内不超过两种字重。Display / Bold / Regular / Mono 四档足够建立完整层级。

## Layout

布局基于 **12 列网格**，4px 基准单位。野蛮主义接受更紧凑的间距节奏——信息密度本身就是这种风格的性格。

容器最大宽度 1280px 居中，适配数据密集型仪表盘的横向布局。卡片内边距统一 16px（`gutter`），比编辑风格更紧——野蛮主义不靠留白呼吸，靠对比指引。章节之间用 `lg`（24px）留白分隔，不滥用 `xl`。

禁止超过两层容器嵌套。野蛮主义依靠明度对比建立层级，而不是靠层层包裹的盒子。移动端塌缩为单列流式网格，最小内边距保持 16px（`md`）。

## Elevation & Depth

层次通过**明度阶分层**传达，不通过柔和阴影。三层结构清晰固定：

1. Neutral 底色（`#111111`）——基础层，最深
2. Surface 容器（`#2A2A2A`）——卡片与面板，抬升一阶
3. On-surface 文字（`#FFFFFF`）——文字与交互覆盖层，最亮

**不用 `box-shadow` 做 elevation**。野蛮主义的层次是硬切的明度阶，不是渐变浮起的阴影。需要分隔时，使用 1px `outline`（`#555555`）硬边框——这是 CSS 层的实现细节，不在 token schema 内定义。这个约束让整个视觉语言保持扁平、硬朗、像一份工程图纸。

## Shapes

圆角哲学是**零圆角**。所有交互元素与容器默认使用 `none`（0px）——野蛮主义拒绝任何"软化"处理，锐利的直角本身就是工程气质的宣言。

`sm`（2px）虽已定义，但仅用于极少数需要脱离像素级锯齿的场合，且必须全屏一致使用。**绝不混用 `none` 与 `sm`**——圆角的不一致比没有圆角更糟糕。野蛮主义没有 `full` 圆角：药丸形 chip 不属于这种风格，状态标签用直角矩形承载。

## Components

**Buttons**：Primary 用青绿填充 + 深墨文字（对比约 13:1），是系统中最强的视觉信号。Secondary 反相——深墨底 + 青绿字，构成"阴刻"效果。两者都用 `label-caps` 字型（全大写 + 宽字距）强化工具感，圆角一律 `none`。按钮宽度不超过 200px，除非横跨整列。Tertiary 状态（源材料未单独 token 化）通过 hover 切换到 `tertiary` 紫实现。

**Chips**：`surface` 深灰底 + `on-surface` 白字 + `none` 圆角。用于状态标签与筛选态。直角矩形把它与圆角药丸彻底区分——野蛮主义的 chip 是"印章"，不是"胶囊"。

**Inputs**：`surface` 底 + `none` 圆角。占位符用全大写（如 `TYPE SOMETHING...`、`NAME@EXAMPLE.COM`）——这是野蛮主义的输入语言。默认 1px `outline` 边框（CSS 层）。focus 时文字色提升为 `primary` 青绿，边框同步切换。错误态用 `error` 红，不复用 `primary`。

## Do's and Don'ts

- **Do** 用 `primary` 青绿作为最强 CTA 填充——在深暗背景上它的辨识度最高。
- **Don't** 用 `box-shadow` 做层次；用明度阶分离（neutral → surface → on-surface）与 1px `outline` 硬边框。
- **Do** 所有 `label-caps` 文字通过 `text-transform: uppercase` 渲染为大写——这是野蛮主义的身份印记。
- **Don't** 在窄于 768px 的屏幕使用 `headline-display`（64px）；缩到 `headline-lg`（40px）。
- **Do** 保证所有正文达到 WCAG AA 对比度（最低 4.5:1）；`on-surface` (#FFFFFF) on `surface` (#2A2A2A) 约 14:1，`on-primary` (#111111) on `primary` (#00F5C3) 约 13:1。
- **Don't** 把 `primary` 青绿用作浅底上的正文文字色——在白底上对比不足 2:1。
- **Do** 用 `neutral` (#111111) 作页面底色，深暗背景是野蛮主义视觉重量的来源。
- **Don't** 在单一组件组内混用 `none` 与 `sm` 圆角——保持全屏圆角语言一致。
- **Do** 数据流与技术数值用 `mono` 字型呈现（如 `DATA IN 12.4 TB/s`），强化工程感。
