---
name: cursor-reveal
title: 叠影显影型
category: page-pattern
status: style
source: 视频研究 v05「5 种高级质感网页」（FORMA 空间案例转写）
era: 2026
verified: 2026-09-07
variance: "5-8"
motion: "4-7"
density: "1-4"
platforms: Web 桌面端
---
# 叠影显影型（Cursor Reveal）

## 一句话定位
同一位置叠放两张照片，底层压暗，鼠标划过处出现 300px 光环、环内"显影"出另一张照片——光标即手电筒，双叙事并行。

## 视觉特征（token 级参数）
- 两张图同尺寸同位置绝对定位叠放
- 底层图压暗到 **28% 不透明度**（`opacity: .28` 或叠黑色遮罩）
- 跟随鼠标的光环直径 **300px**（`border-radius: 50%`，环内 `overflow: hidden` 显示上层图）
- 光环边缘 1px 细白描边（低透明度），环内图像 100% 不透明
- 案例基调：近黑背景 + 灰调室内摄影 + 极细字重标题（FORMA 空间）

## 结构骨架
1. 全屏 Hero：底层照片铺满 + 压暗
2. 上层照片同位叠放，通过光环遮罩裁切显示
3. 光环 div 跟随 mousemove（rAF 节流）
4. 页面角落：极简标题 + 一行说明；导航融入暗背景
5. 移动端降级：替换为"点击切换"或上下两图淡入淡出

## 适用场景 / 慎用场景
- 适用：摄影集、建筑事务所、改造前后对比、双叙事品牌（暗/亮、旧/新）
- 慎用：信息密度高的页面；触屏设备不做降级直接照搬

## AI 常见翻车点（反模式）
1. 底层只压到 70-80%——显影对比不足，光环存在感消失
2. 光环跟随无节流，帧率掉到不可用
3. 忘记移动端降级（触屏无 mousemove）
4. 两张图内容无叙事关联，变成纯炫技

## CSS 关键实现（≤15 行）
```css
.stack { position: relative; }
.stack .base { opacity: .28; }
.stack .top { position: absolute; inset: 0;
  clip-path: circle(150px at var(--mx) var(--my)); /* 300px 光环 */
}
.page { cursor: none; } /* 隐藏原生光标，光环即光标 */
/* JS: rAF 内 lerp 跟随 mousemove 更新 --mx/--my，惯性插值 0.08-0.12 */
@media (pointer: coarse) { .stack .top { clip-path: none; opacity: 0; } }
```

## 来源链接
- temp/video-analysis/v05.md（帧转写）；案例：FORMA 空间建筑事务所
