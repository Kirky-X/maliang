---
version: alpha
name: Y2K
description: Millennial futurism with neon gradients, metallic glassmorphism, and high-saturation chrome.
colors:
  primary: "#7A00FF"
  secondary: "#00F0FF"
  tertiary: "#FF00CC"
  neutral: "#EEEEEE"
  surface: "#FFFFFF"
  on-surface: "#0A0A1A"
  on-primary: "#FFFFFF"
  on-tertiary: "#0A0A1A"
typography:
  headline-display:
    fontFamily: Orbitron
    fontSize: 64px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  headline-lg:
    fontFamily: Orbitron
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  headline-md:
    fontFamily: Exo 2
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: Exo 2
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Exo 2
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Orbitron
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.15em"
rounded:
  none: 0px
  sm: 8px
  md: 16px
  lg: 24px
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
    textColor: "{colors.on-primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 12px 28px
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 11px 27px
  button-ghost:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 11px 27px
  chip:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

Y2K 风格源于 2000 年代的互联网美学，融合未来科技幻想、金属质感、霓虹渐变与玻璃态设计，营造出充满活力与个性的数字体验——它的参照不是某张现代 app 截图，而是早期 Flash 网站、iMac G3 的透明外壳、摩托罗拉 V70 的金属环与《黑客帝国》的数字雨。当装饰回归，剩下的就是视觉冲击：渐变即情绪，高光即科技感。

目标场景是面向未来的科技产品、创新型平台/工具、Z 世代用户群体、娱乐/游戏/元宇宙与概念设计/实验性项目。目标用户是追求个性表达与沉浸感的数字原住民。情感调性是活力、未来、怀旧——像打开一台充满霓虹高光的千禧设备，而不是加载一个克制的工具 app。

## Colors

调色板由高饱和电气色与中性底色构成。亮色负责情绪，渐变负责氛围。**frontmatter 中的颜色是固态锚点；渐变在 prose 中说明，由 CSS `linear-gradient` / `radial-gradient` 在运行时合成。**

- **Primary (#7A00FF)**：电紫，主 CTA 填充色与品牌主色。在浅底上提供最强辨识度，与白字对比约 6.4:1。是 Electric Blue→Purple 渐变的终点色。
- **Secondary (#00F0FF)**：电青，次级交互与高亮。是 Electric Blue→Purple 渐变的起点色，也是 Silver→Blue 渐变的终点。不用于浅底正文（对比不足 1.5:1），只作为填充或焦点环。
- **Tertiary (#FF00CC)**：热粉，强调与状态高亮。是 Hot Pink→Violet 渐变的起点色。与深字对比约 5.7:1，用于 chip 与标签填充。
- **Neutral (#EEEEEE)**：浅灰，页面底色。比纯白柔和，给玻璃态与渐变留出层次依托。
- **Surface (#FFFFFF)**：纯白，用于玻璃态卡片的实体底色（叠加 `backdrop-filter: blur()` 形成玻璃质感）。
- **On-surface (#0A0A1A)**：近黑深蓝，surface 与 neutral 之上的文字色。带蓝色调的深色与 Y2K 调性同源——纯黑会显得生硬，#0A0A1A 在白底对比约 19.6:1。
- **On-primary (#FFFFFF)**：primary 之上的文字色。纯白在电紫上对比约 6.4:1。
- **On-tertiary (#0A0A1A)**：tertiary 之上的文字色。深墨蓝在热粉上对比约 5.7:1。

**渐变定义（CSS 层实现，不在 token schema 内）：**
- Electric Blue→Purple：`linear-gradient(135deg, #00F0FF 0%, #7A00FF 100%)`
- Hot Pink→Violet：`linear-gradient(135deg, #FF00CC 0%, #7A00FF 100%)`
- Silver→Blue：`linear-gradient(135deg, #EEEEEE 0%, #00F0FF 100%)`

源调色板另含 #FFFFFF（白）作为高光反射色——已用作 surface 与 on-primary，不单独 token 化。

## Typography

策略是**双字族对位**：Orbitron 承担标题与标签的未来感，Exo 2 承担正文的可读性。Orbitron 的几何方折与宽字距本身就是"科技幻想"的视觉宣言——它像一台正在启动的设备显示屏。

- **Headlines (Orbitron / Bold)**：`headline-display` (64px) 用于英雄字与产品名。负字距 `-0.02em` 让 Orbitron 的宽字距字形在大幅面上形成未来张力。768px 以下必须降到 `headline-lg`。
- **headline-lg (40px) / headline-md (24px)**：区块标题与卡片标题。`headline-md` 改用 Exo 2——Orbitron 在小尺寸会因宽字距损失可读性，32px 以下是 Exo 2 的领域。
- **Body (Exo 2 / Regular)**：`body-md` (16px) 行高 1.6，承担说明文字与数据描述。**不得低于 16px**——Y2K 的可读性底线不因装饰而妥协。
- **body-sm (14px)**：辅助文字、表格单元格、卡片副文本。不用于主体段落。
- **label-caps (Orbitron / Semibold, 12px)**：按钮、标签、状态指示专用。必须配合 `text-transform: uppercase` 与 `0.15em` 字距——Orbitron 在全大写 + 极宽字距下才显出科技感，这是 Y2K 的身份印记。不用于段落正文。

字重选择遵循 Bold / Semibold / Regular 三档，一屏内不超过两种字重。

## Layout

布局基于 **12 列网格**，4px 基准单位。Y2K 接受紧凑但有节奏的间距——玻璃态卡片需要呼吸，但不依赖大留白建立层级。

容器最大宽度 1280px 居中。卡片内边距统一 20px（`gutter`），比编辑风格更紧——Y2K 的层次靠渐变与高光传达，不靠间距。章节之间用 `lg`（24px）留白分隔。允许不对称与斜切布局——Y2K 拒绝严格的网格对齐，倾斜元素与错位卡片是个性表达的工具，但斜切角度必须全站统一（建议 -4° 或 4°）。

禁止超过两层容器嵌套。Y2K 依靠渐变与玻璃态建立层级，而不是靠层层包裹的盒子。移动端塌缩为单列流式网格，最小内边距保持 16px（`md`）。

## Elevation & Depth

层次通过**玻璃态分层**与**渐变高光**传达，不通过扁平阴影。三层结构清晰固定：

1. Neutral 底色（`#EEEEEE`）——基础层
2. Surface 白卡（`#FFFFFF`）+ `backdrop-filter: blur(12px)`——玻璃态卡片与面板
3. 渐变覆盖层（CSS `linear-gradient`）——交互态与高光反射

**不用扁平 `box-shadow` 做 elevation**。Y2K 的深度来自材质，不是投影。需要抬升感时，使用 `box-shadow` 的彩色辉光变体（如 `0 8px 32px rgba(122, 0, 255, 0.3)`）——这是 CSS 层的实现细节，不在 token schema 内定义。玻璃态边框用 1px `rgba(255, 255, 255, 0.4)` 模拟高光反射。这个约束让整个视觉语言保持未来感、有材质、像一台正在运行的千禧设备。

## Shapes

圆角哲学是**圆润胶囊**。交互元素默认使用 `full`（9999px）——Y2K 拒绝锐利直角，胶囊形本身就是未来科技感的宣言，像一颗颗发光的按钮。

- `full`（9999px）：按钮、chip、状态标签——所有可交互元素。
- `lg`（24px）：卡片与大容器——保持圆润但不至于完全药丸。
- `md`（16px）：次级容器与面板。
- `sm`（8px）：输入框——比按钮更克制，因为输入框需要承载文字。
- `none`（0px）：仅用于装饰性斜切元素与硬边高光条。

**绝不混用 `full` 与 `none`**——圆角语言的不一致比任何单一选择都更糟糕。`full` 是 Y2K 的默认，`none` 是例外且必须全屏一致。

## Components

**Buttons**：Primary 用电紫填充 + 白字（对比约 6.4:1）+ `full` 圆角，是系统中的视觉锚点。Secondary 用电青填充 + 深字（对比约 13.9:1）+ `full` 圆角。Ghost 用 `neutral` 浅灰底 + 深字，承担低优先级操作。三者都用 `label-caps` 字型（Orbitron 全大写 + 极宽字距）强化未来感。按钮可叠加彩色辉光阴影（CSS 层）增强沉浸感。

**Chips**：`tertiary` 热粉底 + `on-tertiary` 深字 + `full` 圆角。用于状态标签与筛选态。胶囊形把它与直角标签彻底区分——Y2K 的 chip 是"发光胶囊"，不是"印章"。

**Inputs**：`surface` 白底 + `sm`（8px）圆角——比按钮更克制，因为输入框需要承载文字。占位符用小写（如 `Type something...`）。默认 1px 玻璃态边框（CSS 层）。focus 时文字色提升为 `primary` 电紫，边框叠加彩色辉光。滑块（Slider）用渐变轨道（CSS `linear-gradient`），是 Y2K 的标志性控件。

## Do's and Don'ts

- **Do** 用渐变（Electric Blue→Purple 等）作为氛围层——渐变是 Y2K 的情绪载体。
- **Don't** 用扁平 `box-shadow` 做层次；用玻璃态（`backdrop-filter: blur`）与彩色辉光阴影。
- **Do** 所有 `label-caps` 文字通过 `text-transform: uppercase` 渲染为大写——Orbitron 在全大写 + 极宽字距下才显出科技感。
- **Don't** 在窄于 768px 的屏幕使用 `headline-display`（64px）；缩到 `headline-lg`（40px）。
- **Do** 保证所有正文达到 WCAG AA 对比度（最低 4.5:1）；`on-surface` (#0A0A1A) on `surface` (#FFFFFF) 约 19.6:1，`on-primary` (#FFFFFF) on `primary` (#7A00FF) 约 6.4:1，`on-tertiary` (#0A0A1A) on `tertiary` (#FF00CC) 约 5.7:1。
- **Don't** 用 `secondary` (#00F0FF) 电青作浅底正文文字色——在白底上对比不足 1.5:1，只允许作为填充或焦点环。
- **Do** 用 `neutral` (#EEEEEE) 作页面底色，给玻璃态与渐变留出层次依托。
- **Don't** 在单一组件组内混用 `full` 与 `none` 圆角——`full` 是默认，`none` 是例外且必须全屏一致。
- **Do** 玻璃态卡片叠加 1px `rgba(255, 255, 255, 0.4)` 高光边框，模拟金属反射。
