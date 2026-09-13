---
name: editorial-split
title: 编辑分栏型
category: page-pattern
status: production
source: 视频研究 v05「5 种高级质感网页」（SALON 案例转写）
era: 2026
verified: 2026-09-07
variance: "4-7"
motion: "1-4"
density: "2-5"
platforms: Web 桌面端
---
# 编辑分栏型（Editorial Split）

## 一句话定位
左栏文字 + 大中缝留白 + 右栏图墙的杂志式左右分栏——用"中缝的空"制造高级感，替代 AI 默认的"标题上图下"堆叠。

## 视觉特征（token 级参数）
- 三段水平结构：左栏（文字）600px · 中缝留白 452px · 右栏（图墙）460px
- 图墙图比 4:5；栏间分隔线 1px（低对比）
- 左栏：超大标题（衬线或粗无衬线均可）+ 短导语 + 眉标；中缝完全留空，不放任何元素
- 参考案例 SALON：奶油底近白 + 近黑文字 + 单一红点缀（"一句话"标色）

## 结构骨架
1. 顶栏：品牌名左置 + 极简导航右置（1 行）
2. 主区 grid：`600px | 452px(gap) | 460px` 三列；左列标题块垂直居中偏上，右列图墙贴齐顶栏下缘
3. 图墙：2×3 或不等高拼贴，gap 统一（8-12px）
4. 底部：一行说明条（WALL I — DENSE HANG 式编号命名）

## 适用场景 / 慎用场景
- 适用：作品集、画廊、杂志专题、品牌故事、高端服务介绍
- 慎用：移动端（降级为标题上图下的堆叠，中缝保留为段间距）；强 CTA 转化页（焦点被图墙分走）

## AI 常见翻车点（反模式）
1. 标题和图上下堆一列（正确：左右分栏，中缝留白 ≥400px）
2. 中缝塞装饰元素或次级文案——中缝必须是空的
3. 三列等宽（正确：600/460 不等宽，比例才有杂志感）
4. 图墙图片比例不一且无对齐基线

## CSS 关键实现（≤15 行）
```css
.hero { display: grid; grid-template-columns: 600px 1fr 460px; min-height: 88vh; }
.gap { /* 中缝：空列，不放内容 */ }
.title { font-size: clamp(48px, 6vw, 88px); line-height: 1.05; }
.wall { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.wall img { aspect-ratio: 4 / 5; object-fit: cover; width: 100%; }
@media (max-width: 1024px) { .hero { grid-template-columns: 1fr; } .gap { display: none; } }
```

## 来源链接
- temp/video-analysis/v05.md（帧转写）；案例：SALON 生成式策展画廊
