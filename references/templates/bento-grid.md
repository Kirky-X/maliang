---
name: bento-grid
title: 便当盒网格
source: Apple 2022 Keynote 版式普及（社区范式，无单一官方规范）
era: 2022 至今（Apple Keynote / Linear / Vercel 式官网）
category: design-language
status: production        # production | style | experimental
variance: 5-8          # dials VARIANCE 适配区间
motion: 2-6          # dials MOTION 适配区间
density: 3-7          # dials DENSITY 适配区间
platforms: 全平台（Web 官网为主）
verified: 2026-09-07
---
# 便当盒网格（Bento Grid）

## 一句话定位
不等尺寸矩形瓷砖拼贴的信息版式：一格一主题、大格叙事、小格点缀，源自 Apple Keynote，现被 SaaS 官网与个人主页全面采用。

## 视觉特征（token 级参数）
- **栅格**：桌面 12 列 / 平板 6 列 / 手机 2 列；典型跨度 = 6×2 主格、3×1 中格、2×1 点缀格；行高统一 96~140px 或以 aspect-ratio 锁定
- **间距**：gap 16~24px（Apple Keynote 紧凑风 8~12px）；页面外边距 24~48px
- **圆角**：18~28px，同一面墙内必须一致（Apple 风 18~24px）
- **瓷砖底**：交替 3 类——实色 #F5F5F7、黑媒体格 #000000、渐变/图片格；全墙强调色 ≤2 种
- **边框/阴影**：可选 1px rgba(0,0,0,.06)；阴影最多 1 层 `0 2px 8px rgba(0,0,0,.04)`，禁止投影堆叠
- **字阶**：主格标题 28~40px semibold + 副题 16~18px；小格标题 16~18px、说明 13~14px；数据格数字 48~64px
- **动效**：入场 stagger 60~80ms/格（位移 12~24px + fade，400~500ms，`cubic-bezier(0.22,1,0.36,1)`）；悬停整格 scale 1.02

## 结构骨架
1. 顶部：1 个主格（6×2）承载核心卖点或大字
2. 中部：2~4 个中格（各 3~4 列宽）分主题展开
3. 底部/边角：2×1 小格做数据、logo 墙、CTA 点缀
4. 视觉动线左上→右下，重要性随面积递减
5. 全墙对齐同一行高基线，禁止孤立空缝

## 适用场景 / 慎用场景
- 适用：产品官网 hero、作品集首页、发布页 changelog、功能矩阵总览
- 慎用：长文阅读页；层级复杂的后台表单流；单墙超过 10 格（信息过载）

## AI 常见翻车点（反模式）
1. 每格面积与信息重量相同——Bento 的灵魂是大小对比（至少 2:1 面积差）
2. 圆角/间距不统一、出现参差缝隙——必须同一 gap、同一 radius
3. 每格都上渐变和动效——瓷砖风靠安静，强调格 ≤ 全墙 1/3
4. 移动端不降级硬挤——必须塌缩为单列/双列

## CSS 关键实现（≤15 行核心代码）
```css
.bento { display:grid; gap:16px; grid-template-columns:repeat(12,1fr); grid-auto-rows:120px; }
.bento > * { border-radius:24px; transition: transform .4s cubic-bezier(.22,1,.36,1); }
.bento-hero { grid-column: span 6; grid-row: span 2; }
.bento-med  { grid-column: span 3; background:#F5F5F7; }
.bento-dot  { grid-column: span 2; }
.bento > *:hover { transform: scale(1.02); }
@media (max-width:768px) {
  .bento { grid-template-columns: repeat(2,1fr); grid-auto-rows:100px; }
  .bento-hero, .bento-med, .bento-dot { grid-column: span 2; }
}
```

## 来源链接
- Apple Keynote 版式源头（2022-09 发布会幻灯片）：https://www.apple.com/apple-events/
- 组件级范例汇总：https://bentogrids.com/
- CSS Grid 规范基础：https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
