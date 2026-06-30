---
version: alpha
name: Editorial
description: Magazine-grade typographic storytelling with generous white space and a single warm gold accent.
colors:
  primary: "#000000"
  secondary: "#333333"
  tertiary: "#C8A97E"
  neutral: "#FAFAFA"
  surface: "#FFFFFF"
  on-surface: "#000000"
  on-primary: "#FFFFFF"
typography:
  headline-display:
    fontFamily: Playfair Display
    fontSize: 72px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.7
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.14em"
rounded:
  none: 0px
  sm: 2px
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
    textColor: "{colors.on-primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.none}"
    padding: 12px 28px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.none}"
    padding: 11px 27px
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.none}"
    padding: 4px 12px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 10px 14px
  input-focus:
    textColor: "{colors.primary}"
---

## Overview

编辑风格的灵感来自杂志排版与视觉叙事——它的参照不是某张 app 截图，而是《The New Yorker》《Kinfolk》《Monocle》的版面与 Dieter Rams 的"少即更多"。它强调留白、精致排版与内容层级，以优雅的方式呈现信息，让界面回归内容本身。当装饰被剥离，剩下的就是叙事：排版即结构，留白即节奏。

目标场景是内容驱动的平台——博客、杂志、新闻平台、品牌官网、作品集与高端产品展示。目标用户是重视阅读体验与品牌质感的读者。情感调性是优雅、克制、可信——像翻开一本排版精良的杂志，而不是加载一个 app。如 Dieter Rams 所言："Good design is as little design as possible."

## Colors

调色板是高对比中性色 + 单一暖金强调色的组合。中性色承担 99% 的视觉，金色只在关键处出现。

- **Primary (#000000)**：纯黑，所有标题与正文的主色，也是主按钮的填充色。提供最大可读性与"永久感"。编辑风格不用深灰妥协——黑就是黑。
- **Secondary (#333333)**：深灰，承担辅助文字、元数据、caption。对比度约 13:1（on neutral），安全用于次要正文。绝不用 #999999 作正文——在白底上对比仅约 2.8:1。
- **Tertiary (#C8A97E)**：暖金，唯一的强调色，专属用于品牌高亮、引文标记、关键链接的视觉锚点。每屏至多一处——稀缺即品质感。
- **Neutral (#FAFAFA)**：页面底色。比纯白柔和，给产品一层"纸张"般的触感。不用作卡片背景——卡片必须用 surface 纯白，才能与底色形成层次分离。
- **Surface (#FFFFFF)**：纯白，用于卡片、模态、输入框等"抬升"容器。
- **On-surface (#000000)**：surface 之上的文字色，与 primary 同值但语义独立——前者描述"文字落在哪个面"，后者描述"主品牌色"。
- **On-primary (#FFFFFF)**：primary 之上的文字色。纯白在纯黑上对比 21:1，主按钮文字极致清晰。

源调色板另含 #D4734F（橙红）、#E74C3C（红）、#3498DB（蓝）、#2C3E50（深蓝）等编辑性 accent——它们用于插图、引文色块与数据可视化，不进入核心 UI token 体系，按需在 CSS 层引用。

## Typography

策略是**双字族对位**：Playfair Display 承担标题的衬线优雅，Inter 承担正文的无衬线可读性。这是杂志排版的经典配方——衬线标题建立文学气质，无衬线正文保证屏幕阅读。

- **Headlines (Playfair Display / Bold)**：`headline-display` (72px) 用于文章主标题与英雄字。负字距 `-0.03em` 模拟印刷标题的紧凑密度，让 Playfair 的高对比衬线在大幅面上形成戏剧张力。768px 以下必须降到 `headline-lg`。
- **headline-lg (48px) / headline-md (32px)**：区块标题与卡片标题。Playfair 的衬线在 32px 仍保持可读，是编辑风格的层级底线——低于此尺寸改用 Inter。
- **Body (Inter / Regular)**：`body-md` (16px) 行高 1.7——比极简风格更宽松，模拟杂志正文行距。**不得低于 16px**。长文阅读体验是编辑风格的核心度量。
- **body-sm (14px)**：辅助文字、caption、表格单元格。不用于主体段落。
- **label-caps (Inter / Medium, 12px)**：按钮、标签、元数据专用。必须配合 `text-transform: uppercase` 与 `0.14em` 字距——宽字距是编辑风格的标签语言，把"功能性文字"与"阅读性文字"在视觉上彻底分离。不用于段落正文。

字重选择遵循"少即是多"：Regular / Medium / Bold 三档足够建立完整层级，一屏内不超过两种字重。

## Layout

布局基于 **12 列网格**，8px 基准单位。编辑风格接受更宽松的间距节奏——留白是这种风格的性格，不是"空"。

容器最大宽度 1200px 居中，避免宽屏下阅读行宽失控。卡片内边距统一 24px（`gutter`）。章节之间用 `xl`（64px）留白建立呼吸感——留白在这里就是层级，信息密度的高低不靠卡片堆叠传达，靠间距节奏传达。不对称布局（Asymmetry）是编辑风格的签名——允许主列与侧栏采用 7:5 或 8:4 的非对称比例，模拟杂志版面的视觉叙事。

禁止超过两层容器嵌套。编辑风格依靠留白建立层级，而不是靠层层包裹的盒子。移动端塌缩为单列流式网格，最小内边距保持 16px（`md`）——任何屏幕尺寸下，间距都不应低于这个底线。

## Elevation & Depth

层次通过**色调分层**传达，不通过阴影。三层结构清晰固定：

1. Neutral 底色（`#FAFAFA`）——基础层，最柔
2. Surface 白卡（`#FFFFFF`）——内容卡片与面板
3. Primary 墨色（`#000000`）——文字与交互覆盖层

**不用 `box-shadow` 做 elevation**。阴影会让平面变得"浮夸"，背离编辑风格的印刷质感。需要分隔时，使用 1px `secondary`（`#333333`）边框或 1px `neutral` 色阶线——这是 CSS 层的实现细节，不在 token schema 内定义。这个约束让整个视觉语言保持扁平、克制、像一份排版文档。

## Shapes

圆角哲学是**锐利**。所有交互元素与容器默认使用 `none`（0px）——编辑风格的参照是印刷品，纸张没有圆角。直角本身就是杂志气质的宣言。

`sm`（2px）虽已定义，但仅用于极少数需要脱离像素级锯齿的场合，且必须全屏一致使用。**绝不混用 `none` 与 `sm`**——圆角的不一致比没有圆角更糟糕。编辑风格没有 `full` 圆角：药丸形 chip 不属于这种风格，状态标签用直角矩形承载，像一枚印刷标签。

## Components

**Buttons**：Primary 用纯黑填充 + 白字（对比 21:1），是系统中最强的视觉锚点。Secondary 用 surface 白底 + 黑字 + 1px 黑色边框（CSS 层），构成"线框"效果。Text Link 用 `tertiary` 暖金或 `primary` 黑，配合下划线。两者都用 `label-caps` 字型（全大写 + 宽字距）强化编辑感，圆角一律 `none`。按钮宽度不超过 200px，除非横跨整列。

**Chips**：`neutral` 底 + `secondary` 字 + `none` 圆角。用于筛选标签与分类态。直角矩形把它与圆角药丸彻底区分——编辑风格的 chip 是"印刷标签"，不是"胶囊"。

**Inputs**：极简——`surface` 白底 + `none` 圆角。占位符用小写（如 `Type something...`），呼应编辑风格的克制语气。默认 1px `secondary` 边框（CSS 层）。focus 时边框提升为 `primary` 黑，文字色保持 `primary`。错误态用 CSS 红，不复用 `tertiary`，避免表单错误与品牌高亮混淆。

## Do's and Don'ts

- **Do** 用 `tertiary` 暖金作为品牌高亮——它的品质感来自稀缺，每屏至多一处。
- **Don't** 用 `box-shadow` 做层次；用色调分离（neutral → surface → primary）与 1px 边框。
- **Do** 所有 `label-caps` 文字通过 `text-transform: uppercase` 渲染为大写——这是编辑风格的标签语言。
- **Don't** 在窄于 768px 的屏幕使用 `headline-display`（72px）；缩到 `headline-lg`（48px）。
- **Do** 保证所有正文达到 WCAG AA 对比度（最低 4.5:1）；`primary` (#000000) on `surface` (#FFFFFF) 约 21:1，`secondary` (#333333) on `neutral` (#FAFAFA) 约 13:1。
- **Don't** 用 #999999 作正文主体色——在白底上对比仅约 2.8:1，只允许出现在 caption 与元数据。
- **Do** 用 `neutral` (#FAFAFA) 作页面底色，不用纯白——纯白底会让卡片失去层次依托。
- **Don't** 在单一组件组内混用 `none` 与 `sm` 圆角——保持全屏圆角语言一致。
- **Do** 用 `xl`（64px）留白分隔章节，留白是编辑风格的层级工具。
