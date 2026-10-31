---
version: alpha
name: Cyberpunk
description: 深色霓虹界面：发光青、紫与洋红在深蓝黑表面上让数据获得视觉形态。
verified: 2026-10-24
license: 自著
colors:
  primary: "#00F0FF"
  secondary: "#1D7AFE"
  tertiary: "#7A5CFF"
  accent: "#E040FF"
  danger: "#FF2D55"
  warning: "#FF9500"
  neutral: "#01012A"
  surface: "#13132C"
  elevated: "#1A2A4A"
  border: "#20354B"
  on-surface: "#00F0FF"
typography:
  headline-lg:
    fontFamily: Orbitron
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: Orbitron
    fontSize: 32px
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
  label-sm:
    fontFamily: Orbitron
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 2px
  md: 4px
  lg: 8px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  gutter: 24px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.secondary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 11px 23px
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    padding: 4px 8px
  chip:
    backgroundColor: "{colors.elevated}"
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
    backgroundColor: "{colors.surface}"
    textColor: "{colors.accent}"
  switch:
    backgroundColor: "{colors.border}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  badge-danger:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.danger}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 4px 8px
  badge-warning:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.warning}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.sm}"
    padding: 4px 8px
---

## Overview

赛博朋克是未来科技的美学——由霓虹与黑暗构筑的机械结构、数据可视化与系统秩序。在这个界面里，数据获得视觉形态：发光的青色、紫色与洋红沿着深蓝黑表面勾勒出信息的轮廓。最终呈现的是一个数据与未来的边界消融的世界——让未来可见。

目标受众：科技产品、数据可视化平台、企业系统后台与创意作品集。用户是能在系统中看见美的工程师、分析师与创作者——仪表盘、数据流、系统健康指标——他们期待界面把数据当作视觉媒介，而不是电子表格。情感调性是电性、精确、面向未来——像读取一台尚未被建造出来的机器的遥测数据。

## Colors

调色板是双系统：用于表面的深近黑蓝光谱，以及用于交互与数据的鲜明霓虹光谱。每种霓虹色都在发光；每种深色都在后退。

- **Primary (#00F0FF)：** 青色——标志性信号色。用于深色表面上的主文字、主按钮填充、数据折线轨迹与所有"实时"指示。它在深色基底上的电光亮度是这种风格的决定性视觉姿态。在所有深色表面上都有高对比度（12:1+）。
- **Secondary (#1D7AFE)：** 电蓝——次级交互色。用于次级按钮文字与链接，在这些位置青色会过于抢眼。比 `primary` 更冷、更深；提供第二层交互强调。
- **Tertiary (#7A5CFF)：** 紫色——用于数据可视化点缀、三级高亮与渐变端点。常与 `primary` 组成霓虹渐变（青 → 紫），构成赛博朋克的视觉签名。
- **Accent (#E040FF)：** 洋红粉——调色板中最锐利的霓虹色。少量用于焦点态、特殊高亮与关键数据节点。它的色度强度会强行吸引注意力；过度使用会导致视觉疲劳。聚焦时，输入文字切换为 `accent`，以示意当前处于活跃交互。
- **Danger (#FF2D55)：** 红色——警报、错误与关键系统状态。用于徽章组件中的系统警告。绝不要与 `accent`（洋红）混淆，因为它承载明确的语义、非交互含义。
- **Warning (#FF9500)：** 橙色——警示状态与非关键警报。与 `danger` 一起用于徽章组件，构成完整的系统状态词汇。暖色在冷色板中让警告立即可读。
- **Neutral (#01012A)：** 最深的蓝黑——"虚空"。作为页面背景与徽章基底。不是纯黑；轻微的蓝色调赋予它深度，并避免 `#000000` 的"扁平虚空"。所有霓虹色在这个表面上都能达到最大对比度。
- **Surface (#13132C)：** 深蓝黑，用于面板、输入框与卡片。比 `neutral` 亮一阶，在深色光谱内形成色调分层。交互元素的主要容器色。
- **Elevated (#1A2A4A)：** 更亮的深蓝，用于抬升卡片与 chip。形成第三层深度——`neutral` → `surface` → `elevated`——让信息层级通过深色基底内的色调渐变来实现。
- **Border (#20354B)：** 柔和的蓝灰色，用于边框、分隔线与开关的"关闭"态。定义结构边缘，又不与霓虹内容竞争。它的中性特质使其成为开关静息态的理想选择。
- **On-surface (#00F0FF)：** 表面之上的文字色。与 `primary` 同值，但语义独立——描述的是"静息在深色面板上的文字"，而不是"品牌霓虹"。

## Typography

策略是将 **Orbitron**——几何化、未来感的展示字体——用于标题与标签，将 **Exo 2**——高度易读、带有微妙技术气质的无衬线体——用于正文。这种双字族方式把"系统之声"（Orbitron，全大写、宽字距）与"人类可读内容"（Exo 2，自然大小写、舒适行高）区分开来。

- **headline-lg (48px / Bold)：** Orbitron Bold 搭配 `-0.02em` 字距，呈现 HUD 显示屏或终端标题的几何密度。字形本身就看起来像被工程化过——每个字符都像机加工而成，而非书写而成。用于页面级标题与仪表盘页头。768px 以下降到 `headline-md`。
- **headline-md (32px / Semibold)：** Orbitron Semibold 用于区块标题与面板页头。较轻的字重保持工程感，又不会压过周围内容。
- **body-md (16px / Regular)：** Exo 2 Regular，16px，1.6 行高，用于正文与数据描述。Exo 2 微妙的技术气质（略微方折的字形）让它在不牺牲可读性的前提下保持主题一致。绝不低于 16px——数据必须清晰可读。
- **body-sm (14px / Regular)：** Exo 2，用于辅助文字、表格单元格与元数据。不用于主段落。
- **label-sm (12px / Medium)：** Orbitron Medium，用于按钮、标签、系统标签与所有元数据。搭配 `0.1em` 字距与 `text-transform: uppercase`——这种宽字距全大写处理是机器之声，在视觉上把系统标签与人类可读的散文区分开。它是所有风格中最宽的字距；让每个标签都像被终端盖了章。

## Layout

布局遵循 **12 列网格**，24px 槽宽（`gutter`），针对数据密集型仪表盘与多面板界面优化。间距刻度——4 / 8 / 16 / 24 / 32 / 48——提供足够的层级来分隔数据面板，又不浪费屏幕空间。

容器最大宽度 1440px 并居中——比大多数风格更宽，因为赛博朋克界面偏爱多列仪表盘而非单列阅读。面板与卡片使用 16px 内边距（`md`），在保持分隔的同时最大化数据密度。区块之间用 `2xl`（48px）留白分隔，但同一区块内的面板可以近到 `lg`（24px）——霓虹边框与发光边缘提供了视觉分隔，减少了对留白的依赖。

移动端塌缩为单列堆叠，最小内边距保持 16px（`md`）。数据可视化应优雅降级——放不下的图表应塌缩为摘要统计，而不是缩小到无法辨认。

## Elevation & Depth

赛博朋克中的深度通过**霓虹辉光与深色光谱内的色调渐变**传达，而不是传统投影。层级是：

1. Neutral 背景（`#01012A`）——虚空，最深层
2. Surface 面板（`#13132C`）——深蓝黑容器，亮一阶
3. Elevated 卡片（`#1A2A4A`）——抬升面板，第三层深度

**霓虹辉光取代阴影。** 扁平设计用边框、极简主义用色调分隔，而赛博朋克用带霓虹色模糊辉光的 `box-shadow` 来指示活跃或可交互元素。主按钮发青光（`0 0 12px rgba(0, 240, 255, 0.4)`）；聚焦的输入框发洋红光（`0 0 8px rgba(224, 64, 255, 0.3)`）。这种辉光就是赛博朋克语境下的海拔——它示意"这个元素是活的"。

非活跃元素依靠色调渐变（`neutral` → `surface` → `elevated`）与 1px `border`（`#20354B`）描边来分隔。不要给非活跃元素加辉光——辉光只保留给活跃、聚焦或关键状态。滥用辉光会压平层级并造成视觉疲劳。

## Shapes

形状语言由**机械精度与锐利角度**定义。赛博朋克界面唤起被工程化、机加工过的表面——而不是有机曲线。

- `sm`（2px）：按钮、输入框与交互元素的默认值——几乎不圆，保留锐利、工程化的美学。这种近直角是赛博朋克的签名。
- `md`（4px）：用于较大面板与卡片，稍柔和的转角避免界面显得敌意。仍比大多数设计系统锐利得多。
- `lg`（8px）：保留给大容器与模态框，更多圆角提升亲和力，又不放弃机械性格。
- `full`（9999px）：专用于 chip、标签与开关——药丸形元素，与其他棱角分明的界面形成鲜明对比。药丸形示意"状态"或"切换"，区别于矩形的"动作"元素。

绝不要在按钮或面板上使用大圆角——锐利是承重结构。赛博朋克按钮上的 16px 圆角会让它看起来像消费级 app，而不是系统界面。

## Components

**Buttons：** 主按钮使用 `primary`（青）填充配 `neutral`（深蓝黑）文字——发光的青色按钮配深色文字，唤起被点亮的开关或活跃的终端命令。青色填充应带微妙的辉光。次级按钮透明，配 `secondary`（蓝）文字与 1px `border` 描边——"待机"状态。幽灵按钮透明，配 `primary` 文字且无边框——用于三级动作与内联命令。全部使用 `label-sm` 字型（Orbitron，全大写，宽字距）——这是系统之声，不是用户之声。

**Chips：** `elevated` 背景配 `primary` 文字与 `full` 圆角。用于状态标签、数据标签与筛选态。药丸形与棱角面板形成清晰的视觉区分——chip 是元数据，不是动作。

**Inputs：** `surface` 背景配 `primary` 文字与 `sm` 圆角。占位符使用变暗的霓虹色。聚焦时，文字色切换为 `accent`（洋红），输入框获得洋红辉光（`box-shadow: 0 0 8px rgba(224, 64, 255, 0.3)`）——这是终端接受输入的隐喻。错误态使用 `danger` 文字配红色辉光，绝不用 `accent`。

**Switches：** 切换轨道在静息态使用 `border`（柔和蓝灰）配 `primary` 文字。激活时，轨道可切换到 `elevated`，旋钮带青色辉光。`full` 圆角以及静息态与激活态之间的色调切换，让开关不单靠颜色也能被辨认。

**Badges：** `neutral` 背景配语义文字色——`danger`（红）用于错误与关键警报，`warning`（橙）用于警示。用于系统状态指示（例如"78% SYSTEM HEALTH"）。`sm` 圆角让它们保持棱角与技术感。绝不要用 `accent`（洋红）做徽章——它保留给交互焦点态。

## Do's and Don'ts

- **Do** 用霓虹辉光（带模糊霓虹色的 `box-shadow`）指示活跃、聚焦或可交互元素——辉光是赛博朋克语境下的海拔。
- **Don't** 给非活跃或静息元素加辉光——滥用会压平层级并造成视觉疲劳。
- **Do** 把深色光谱（`neutral` → `surface` → `elevated`）作为基础；霓虹色是点缀，不是背景。
- **Don't** 用霓虹色做大面积背景——它们会造成眼睛疲劳，并破坏让这种风格成立的深色基底对比。
- **Do** 用 Orbitron（全大写、宽字距）配标签，用 Exo 2（自然大小写）配正文——系统之声必须与人类可读之声区分开。
- **Don't** 在按钮或面板上使用大圆角——锐利是承重结构；2px 表示"工程化"，16px 表示"消费级"。
- **Do** 保持 WCAG AA 对比度（最低 4.5:1）——`primary` 在 `surface` 上约 13:1，`primary` 在 `elevated` 上约 10:1，`accent` 在 `surface` 上约 5.5:1，`danger` 在 `neutral` 上约 5.5:1。
- **Don't** 把 `accent`（洋红，交互）与 `danger`（红，语义）混淆——它们用途不同，不可互换。
- **Do** 把数据可视化当作一等元素——图表、图形与系统指标不是装饰，它们就是内容。
