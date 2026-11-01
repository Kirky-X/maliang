---
version: alpha
name: Skeuomorphism
description: 一种可触的界面，借用现实世界材质——皮革、纸张、木材、玻璃——让数字可供性显得熟悉而可信。
colors:
  primary: "#2E1E15"
  secondary: "#8B6B4D"
  tertiary: "#D4A574"
  neutral: "#F5F0E6"
  surface: "#E8D5B7"
  on-surface: "#2E1E15"
  leather: "#5A3E2B"
  wood: "#C9B99C"
  glass: "#A7C7E7"
typography:
  headline-lg:
    fontFamily: Georgia
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: Georgia
    fontSize: 32px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: Helvetica
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Helvetica
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: Helvetica
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.04em
rounded:
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  gutter: 20px
components:
  button-primary:
    backgroundColor: "{colors.leather}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
  button-secondary:
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 11px 23px
  chip:
    backgroundColor: "{colors.wood}"
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
    textColor: "{colors.tertiary}"
  switch:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
---

## Overview

拟物化是一种向物理世界借形的设计哲学。通过模拟真实材质——皮革、木材、纸张、玻璃——及其纹理、光照与物理交互，界面让用户通过熟悉的视觉隐喻理解功能。这降低了学习曲线，以可触的真实感建立信任，并创造产生情感共鸣的沉浸体验。

目标受众：从现实世界隐喻中受益的广泛用户群体，包括物理可供性让复杂操作变得直觉的汽车与工业场景、沉浸感至上的游戏与娱乐应用，以及必须通过材质品质传达工艺与传承的文化或奢侈品牌。情感调性是温暖、厚实、精心制作——像握着一件做工精良的实物。

## Colors

调色板是从自然材质中提取的温暖大地色光谱。每种颜色都映射到一种物理物质，赋予界面可触、精工制作的品质。

- **Primary (#2E1E15)：** 最深的棕色——带暖意的近黑。用于所有正文与标题，比纯黑边缘更柔和，保持可读性。也是主按钮的悬停态，把皮革加深到最浓郁的色调。
- **Secondary (#8B6B4D)：** 中等马鞍棕，用于辅助角色——边框、说明文字、元数据与占位符文字。它的暖意让功能元素不显得冰冷或临床。绝不用于正文；对比度不足以支撑长时间阅读。
- **Tertiary (#D4A574)：** 温暖金色点缀——陈年黄铜的包浆。少量用于高光、焦点态与交互强调。它的材质暖意让它区别于数字 UI 的扁平蓝；它示意"这是手工制作的，不是计算出来的"。
- **Neutral (#F5F0E6)：** 最浅的暖色调——陈年纸张。作为页面背景，赋予产品羊皮纸般的基础。比白色更柔和温暖；绝不用于卡片，卡片需要 surface 色调与基底分开。
- **Surface (#E8D5B7)：** 浅暖色调——陈年羊皮纸或浅色木材。用于卡片、输入框与抬升容器。它与 `neutral` 的色调差异无需阴影就能创造深度，唤起层层堆叠的纸张。
- **On-surface (#2E1E15)：** 表面之上的文字色。与 `primary` 同值但语义独立——描述的是"静息在材质表面上的文字"，而不是"品牌墨色"。
- **Leather (#5A3E2B)：** 深沉浓郁的棕色——上油皮革的颜色。专用于主按钮填充，在那里材质隐喻最强。悬停时加深为 `primary`，形成"按压皮革"的效果。
- **Wood (#C9B99C)：** 中间调的暖灰棕——浅色木材或陈年黄铜。用于 chip 与标签，它的材质暖意让它们区别于扁平的数字化药丸。也适合分隔线与次级边框。
- **Glass (#A7C7E7)：** 冷调半透明蓝——磨砂玻璃。用于开关的"开启"态，唤起玻璃旋钮滑入位置。冷色调在原本温暖的调色板中提供唯一的色度对比，把视线引向激活的开关状态。

## Typography

策略将 **Georgia**（衬线体）用于标题，将 **Helvetica**（无衬线体）用于正文与 UI 文字。这种双字族方式呼应编辑传统——衬线体承载庄重，无衬线体处理功能——这一惯例强化了拟物化材质、精工的性格。

- **headline-lg (48px / Bold)：** Georgia 粗体搭配 `-0.02em` 字距，呈现皮革装订书名的密度与权威感。用于页面级标题。衬线字形增添了无衬线体无法提供的质感——每个字端与括弧都贡献了精工感。
- **headline-md (32px / Medium)：** Georgia 中等字重用于区块标题。较轻的字距 `-0.01em` 保持紧凑，同时让衬线有呼吸空间。
- **body-md (16px / Regular)：** Helvetica Regular，16px，1.6 行高，用于正文。Helvetica 的中性让内容发声，由周围的材质承载个性。绝不低于 16px——可读性不可妥协。
- **body-sm (14px / Regular)：** Helvetica，用于辅助文字、表格单元格与卡片副文本。不用于主段落。
- **label-sm (12px / Medium)：** Helvetica Medium，用于按钮、标签与元数据。搭配 `0.04em` 字距与 `text-transform: uppercase`，营造"刻印标签"效果——令人想起皮革制品上的压印文字。

## Layout

布局遵循 **12 列网格**，20px 槽宽（`gutter`），唤起印刷图录的比例。间距刻度——4 / 8 / 16 / 24 / 32 / 48——提供足够的层级来叠放材质而不拥挤。

容器最大宽度 1200px 并居中。卡片使用 24px 内边距（`lg`），让内容在材质框架内有呼吸空间。区块之间用 `2xl`（48px）留白分隔——比扁平设计更宽裕，因为拟物元素承载视觉重量，需要周围空间以避免显得杂乱。

避免嵌套超过两层容器。每一层材质都应在视觉上分明（皮革 → 纸张 → 木材），而不是任意堆叠。移动端塌缩为单列，最小内边距保持 16px（`md`）。

## Elevation & Depth

拟物化中的深度通过**材质分层与微妙内阴影**传达，而不是扁平的色调切换。层级唤起静置在表面上的实物：

1. Neutral 背景（`#F5F0E6`）——桌面或桌台表面
2. Surface 卡片（`#E8D5B7`）——铺在桌面上的纸张或羊皮纸
3. 皮革与木质元素——静置在纸张上的实物

与扁平设计不同，拟物化*确实*使用 `box-shadow`，但克制且有意图：卡片下方柔和的低偏移阴影暗示它们物理上静置在表面；按钮顶边的内嵌高光暗示凸起的可触表面。这些阴影应微妙（低不透明度、小模糊）——目标是暗示，不是写实。沉重的投影是业余拟物化的标志，应避免。

对于开关与切换器，"开启"态使用 `glass` 色配微妙内嵌阴影，暗示凹陷的轨道，而旋钮本身显得凸起。这种物理隐喻让开关状态立即可读。

## Shapes

形状语言由**与材质相称的圆角**定义。与极简主义的建筑式锐利不同，拟物元素拥有实物般更柔和的边缘。

- `sm`（4px）：用于输入框与文本字段——冲压或裁切纸张边缘的轻微圆角。
- `md`（8px）：用于按钮——皮革按钮或木块的圆角，足够厚实以显得可触，又不失结构。
- `lg`（16px）：保留给较大的容器与卡片，更明显的圆角唤起实物的曲率。
- `full`（9999px）：专用于 chip、标签与开关——药丸形元素，模仿开关与标签徽章等物理组件。

绝不要在同一组件组内混用 `sm` 与 `lg`——不一致会破坏材质错觉。

## Components

**Buttons：** 主按钮使用 `leather` 填充配 `neutral` 文字——深色皮革按钮配浅色压印文字的隐喻。悬停时，填充加深为 `primary`（最浓郁的皮革色调）。次级按钮透明，配 `primary` 文字与 1px `secondary` 边框，唤起刻印轮廓。两者都使用 `label-sm` 全大写字型，模拟压印或刻印标签。`md` 圆角赋予按钮可触、略圆的边缘。

**Chips：** `wood` 背景配 `primary` 文字与 `full` 圆角。温暖的木色让它们区别于按钮，药丸形示意可选中性。用于筛选标签与选中态。

**Inputs：** `surface` 背景（羊皮纸）配 `primary` 文字与 `sm` 圆角。默认边框是 1px `secondary` 描边，暗示内嵌面板的凹陷边缘。聚焦时，文字色切换为 `tertiary`（暖金），边框可获得微妙内发光——光线捕捉黄铜框架的隐喻。错误态使用柔和红色，绝不用 `tertiary`。

**Switches：** 切换轨道在"开启"态使用 `glass`（磨砂蓝），配 `primary` 文字。`full` 圆角与冷蓝调在暖色板中形成清晰的"激活"信号——像玻璃指示灯亮起。在"关闭"态，轨道恢复为 `neutral` 或 `wood`，旋钮停在凹陷位置。

## Do's and Don'ts

- **Do** 让每种颜色都映射到一种物理材质——如果一种颜色唤不起皮革、木材、纸张或玻璃，它就不属于这个调色板。
- **Don't** 过度拟物——过多的纹理与装饰会造成视觉噪音与认知负荷。目标是暗示，不是照片级写实。
- **Do** 使用微妙阴影（低不透明度、小模糊）暗示物理分层——卡片静置在表面、按钮凸起。
- **Don't** 使用沉重投影或过多渐变——业余拟物化依赖它们；精工拟物化通过材质与色调暗示深度。
- **Do** 用 Georgia（衬线）配标题，用 Helvetica（无衬线）配正文——这种编辑式搭配强化精工、材质的性格。
- **Don't** 在同一组件组内混用 `sm` 与 `lg` 圆角——不一致的圆角会破坏材质错觉。
- **Do** 保持 WCAG AA 对比度（最低 4.5:1）——`primary` 在 `neutral` 上约 12:1，`primary` 在 `surface` 上约 11:1，`neutral` 在 `leather` 上约 8.5:1。
- **Don't** 把拟物化用于数据密集型仪表盘或性能敏感语境——材质丰富度会与信息清晰度竞争，并可能影响低端设备的渲染性能。
- **Do** 确保跨设备的一致可用性——拟物纹理与阴影在无法忠实渲染的屏幕上必须优雅降级。
