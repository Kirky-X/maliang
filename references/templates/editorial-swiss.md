---
name: editorial-swiss
title: 瑞士编辑排版风
source: 瑞士国际主义平面设计（Josef Müller-Brockmann 栅格系统）；IxD 基金会风格综述
era: 1950s 起源 / 2018 至今 Web 复兴
category: design-language
status: production        # production | style | experimental
variance: 3-6          # dials VARIANCE 适配区间
motion: 1-4          # dials MOTION 适配区间
density: 2-5          # dials DENSITY 适配区间
platforms: Web（内容/品牌站）
verified: 2026-09-07
---
# 瑞士编辑排版风（Editorial / Swiss International Style）

## 一句话定位
排版本身即设计：严格栅格、无衬线大字、大量留白、1px hairline 分割，几乎零装饰，层级全靠字号、字重与对齐。

## 视觉特征（token 级参数）
- **颜色**：纸白 #FAFAF8 或 #FFFFFF、墨黑 #111111、单一强调色三选一——瑞士红 #E30613 / 国际橙 #FF4F00 / 克莱因蓝 #002FA7；图片不加滤镜
- **字体**：Neue Haas Grotesk / Helvetica Neue / Inter / Söhne；最多 2 个字族
- **字阶**（1.25 模数）：caption 12 → body 16 → h4 20 → h3 25 → h2 31 → h1 39 → display 56~96（允许断尺）；行高正文 1.5、标题 1.02~1.15；标题 letter-spacing -0.01~-0.02em；大写小标签 +0.08em
- **栅格**：12 列、gutter 24px、版心 1200~1440px；正文栏宽 60~75 字符
- **分割**：1px #111 横线分区；radius 0、无阴影、无渐变、无玻璃
- **间距**：段间 24~32px、节间 96~128px、页边距 clamp(24px, 5vw, 80px)
- **对齐**：一切左对齐（flush left / ragged right），标题可悬挂出血
- **动效**：极克制——hover 下划线 1px 从左扫入 200ms linear；reveal 可选 300ms ease-out；禁用视差与弹跳

## 结构骨架
1. Masthead：上下细黑线夹报头（刊名 + 期号/日期，两端对齐）
2. Hero：display 大标题占 8~10 列，右侧 2~4 列留白或放导语
3. 正文：单栏 65ch 或 8/4 双栏错位（文字列 + 图片列）
4. 分节：1px 横线 + 大写节号（01 / 02 / 03）
5. 页脚：hairline 上边线 + 多栏 12px 小字

## 适用场景 / 慎用场景
- 适用：杂志/媒体/博客、作品集、建筑与时尚品牌官网、年报长文
- 慎用：游戏化/儿童产品；重插画重色彩的品牌；功能密集工具界面

## AI 常见翻车点（反模式）
1. 忍不住加卡片阴影/圆角——本风格层级只靠字号、留白与 1px 线
2. 字阶只差 2px——必须 1.5~2 倍跳跃（display 96 vs body 16）
3. 强调色到处用——每屏最多 1 处（一个词、一条线或一个数字）
4. 居中对齐滥用——瑞士风几乎一切左对齐

## CSS 关键实现（≤15 行核心代码）
```css
.swiss { max-width:1280px; margin:0 auto; padding:0 clamp(24px,5vw,80px);
  color:#111; background:#FAFAF8;
  font: 400 16px/1.5 "Neue Haas Grotesk","Helvetica Neue",Inter,sans-serif; }
.swiss h1 { font-size:clamp(56px,9vw,96px); line-height:1.02;
  letter-spacing:-.02em; font-weight:500; }
.swiss .rule { border:0; border-top:1px solid #111; margin:96px 0 32px; }
.swiss .kicker { font-size:12px; letter-spacing:.08em; text-transform:uppercase; }
.swiss .accent { color:#E30613; }
.swiss a { color:inherit; text-decoration:none;
  border-bottom:1px solid #111; }
```

## 来源链接
- 风格综述（Interaction Design Foundation）：https://www.interaction-design.org/literature/topics/swiss-design
- 经典书目：Müller-Brockmann《Grid Systems in Graphic Design》（1981）
- Web 复兴范例：https://www.vitsoe.com/about/good-design（瑞士系品牌排版实践）
