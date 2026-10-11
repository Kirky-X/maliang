---
name: warm-minimal
title: 暖极简编辑风
source: 社区范式 minimalist-ui（外部 skill，license 未考——思想内化，本文措辞为本仓库自著）
era: 2020s workspace 平台审美（Notion / Linear 谱系的暖色分支）
category: design-language
status: style        # production | style | experimental
variance: 2-5          # dials VARIANCE 适配区间
motion: 1-4          # dials MOTION 适配区间
density: 2-5          # dials DENSITY 适配区间
platforms: Web（文档型产品 / 工作台 / 内容站）
verified: 2026-10-11
---
# 暖极简编辑风（Warm Utilitarian Minimalism）

> [`editorial-swiss.md`](editorial-swiss.md) 的暖色变体：同一套「排版即设计 + 1px 分割 + 零装饰」骨架（栅格、字阶、留白纪律全部沿用 editorial-swiss），把冷白纸换成**暖骨白画布**，并引入**退饱和淡彩**做唯一的色彩点缀。适用于文档型产品、工作台、知识库等「像一间安静工作室」的题材。

## 一句话定位

纸是暖的、色彩是配给的、组件是平的——一个用灰阶与四种淡彩运作的文档世界。

## 视觉特征（token 级参数）

| 角色 | 值 | 说明 |
| --- | --- | --- |
| 画布 | `#F7F6F3` / `#FBFBFA` | 暖骨白/暖纯白，全站底色（区别于 editorial-swiss 的冷纸白） |
| 卡片面 | `#FFFFFF` / `#F9F9F8` | 暖白卡片 |
| 正文 | `#111111` / `#2F3437` | 禁纯黑 `#000`；行高 ≥1.6 |
| 次级文本 | `#787774` | 静灰，元数据/说明文字 |
| 分割线 | `#EAEAEA` / `rgba(0,0,0,0.06)` | 全站统一 `1px solid`，唯一线条语言 |
| 淡彩 tag × 4 | 底 `#FDEBEC`/`#E1F3FE`/`#EDF3EC`/`#FBF3DB`，字 `#9F2F2D`/`#1F6C9F`/`#346538`/`#956400` | 红/蓝/绿/黄四组，**只**用于 tag、行内代码底、图标底 |

主 CTA：`#111111` 实底白字，圆角 4-6px，无投影，hover 微移 `#333` 或 `scale(0.98)`。大容器/卡片禁 pill 形（`rounded-full` 仅限小 tag 徽章）。

## 结构骨架

macro-whitespace 先行（节间距 `py-24` 档，正文宽度 `max-w-4xl` 档）→ 非对称 bento 承载特性（`border: 1px solid #EAEAEA`、圆角 ≤12px、内边距 24-40px）→ FAQ/列表剥容器只留底线 → 微组件两件：`<kbd>` 键帽（1px `#EAEAEA` 边、4px 圆角、`#F7F6F3` 底、mono 字）与伪 OS 窗口（白顶栏 + 三枚浅灰圆点，mockup 软件时用）。

图标与图像同语言：图标走中粗描边系统（Phosphor Bold / Radix 档）全站统一字重；插图用白底单色连续线稿 + 一块淡彩几何偏移填充；照片降饱和偏暖并叠 `0.04` 暖噪点融入灰阶（占位图按 [`../meta/visual-assets.md`](../meta/visual-assets.md) 口径，禁 `?random`）。

## 适用场景 / 慎用场景

- **适用**：文档/知识库产品、团队工作台、写作与笔记工具、安静的内容站。
- **慎用**：需要强烈情绪唤起的品牌页（淡彩压不住）、数据密集监控（→ [`data-dense-dashboard.md`](data-dense-dashboard.md)）、暗色场景（→ [`dark-oled.md`](dark-oled.md)）。

## AI 常见翻车点

- 淡彩扩散为大面积底色——四组淡彩只做「点」,铺开即失焦;大色块背景一律禁(见 [`../meta/ai-tells.md`](../meta/ai-tells.md) §8)。
- 暖白画布配冷灰分割线后仍用纯黑文字——`#000` 一出现,纸感即破。
- 阴影反弹:`shadow-md/lg` 是本语言的对立面,层级全靠 1px 线与留白;仅卡片 hover 允许 `0 2px 8px rgba(0,0,0,0.04)` 一档。
- 与 editorial-swiss 混搭:同一页冷纸白与暖骨白并用、两套分割线灰度并存 = 都不是。
- 字体走默认:Inter/system 直接开跑,丢掉衬线标题 × 几何无衬线正文的对比(标题字距 `-0.02 ~ -0.04em`、行高 1.1)。

## CSS 关键实现（≤15 行核心代码）

```css
:root {
  --canvas: #F7F6F3; --surface: #FFFFFF;
  --ink: #111111; --ink-muted: #787774; --line: #EAEAEA;
}
body { background: var(--canvas); color: var(--ink); line-height: 1.6; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; }
.tag--blue  { background: #E1F3FE; color: #1F6C9F; border-radius: 9999px; }
kbd { border: 1px solid var(--line); border-radius: 4px;
      background: var(--canvas); font-family: var(--font-mono); }
.card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
```

## 来源链接

- 上游:外部 skill minimalist-ui(部署目录,license 未考,思想内化后本仓自著;吸收完成前原件留部署目录)
- 主干纪律:[`editorial-swiss.md`](editorial-swiss.md);淡彩配给制与 [`../dimensions/color-palettes.md`](../dimensions/color-palettes.md) 呼应
