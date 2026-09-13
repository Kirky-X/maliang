---
name: scroll-band-gallery
title: 滚动图带六式
category: page-pattern
status: style
source: 视频研究 v06「6 种 Web 交互设计动效」（Quorum/Chorus/Splay/Parade/Continuum/Vector 参数转写）
era: 2026
verified: 2026-09-07
variance: "5-8"
motion: "5-9"
density: "1-4"
platforms: Web 桌面端
---
# 滚动图带六式（Scroll Band Gallery）

## 一句话定位
作品集图墙的六种"收拢成形状"动效骨架（带/扇/筒/环/扭/隧道）——分水岭在普通网页停下的 FLAT WALL 之后：把平面图墙收拢成一个几何体，页面才真正与用户互动。

## 视觉特征（token 级参数）
- 共同前提：同一批图片节点，先排平面墙再收拢成几何形态；驱动统一为 scroll/drag 增量，perspective 给容器、3D 变换给子项

### 式一：反向图带（Reverse Rails）— Quorum
- 两行 translateX 反号；速度差 0.3×/1.0×；hover 时 rotate ±8°
- 适用：图墙入场、制造纵深速度感

### 式二：扇形牌阵（A Hand of Cards）— Chorus
- 第 i 张 rotate i×4.5°；rotateY 180° 翻背面；FAN↔WALL 两态连动（同一批节点两种排布）
- 适用：图片集暗示"还有更多"——排成网格一眼到底，扇形才让人知道后面还有很多张

### 式三：圆柱卡带（Cylinder Reel）— Splay
- rotateY + translateZ 卷成筒；perspective 给容器；一个 velocity（DRAG VELOCITY 0.09）喂两处：卷筒转动 + 标题 letter-spacing 2px 联动
- 适用：沉浸式横向浏览、拖拽交互

### 式四：环形画廊（On the Turn）— Parade
- 相机放在环外面；点选补角度差到正前；环和墙共用一批节点
- 适用：开场从深处飞入、滚动收尾

### 式五：扭环带（One Side）— Continuum
- 带子中间扭 180°（twist: 180°）；过扭转点走 backface；一套动效管正反两面
- 适用：能摊成看板、再收回成带子

### 式六：纵深隧道（Head-On）— Vector
- 每张卡一个 z 值；scroll 增量平移全体 z；scale = d / (d - z)
- 适用：图片朝观者飞来，反向即倒退

## 结构骨架
1. 平面墙起手（FLAT WALL）→ 收拢成一个形状（分水岭步骤：RAIL/FAN/CYLINDER/RING/TWIST/TUNNEL 六选一）
2. 一个 velocity 喂两处以上：形态 + 版式（字距/位移）联动，整个页面才"活"
3. 形态可逆：FAN↔WALL、环↔墙、带↔板，两态共用同一批节点不做第二份 DOM；每张卡 z 值/角度序号显式赋值（--i / --z）

## 适用场景 / 慎用场景
- 适用：作品集、画廊、品牌页等图片主导的展示页
- 慎用：转化页/内容型页面（动效抢焦点）；移动端低性能设备（3D 变换链长，降级回静态图墙）

## AI 常见翻车点（反模式）
1. 只做到平面图墙就结束——缺"收拢成一个形状"，页面显得死
2. 同一批图排成网格一眼到底，失去"还有更多"的暗示
3. 动效只驱动一处（形态自己动、版面不动）——没把 velocity 喂第二处
4. 六式混用（一页只选一式）；3D 变换忘给容器 perspective，透视全失真

## CSS 关键实现（≤15 行）
```css
.stage { perspective: 1200px; } /* 透视给容器 */
.rail { transform: translateX(calc(var(--s) * 1px)); }
.rail.rev { transform: translateX(calc(var(--s) * -0.3px)); } /* 反号 + 0.3× 速度差 */
.fan li { transform: rotate(calc(var(--i) * 4.5deg)); }
.reel li { transform: rotateY(calc(var(--i) * 18deg)) translateZ(280px); } /* 圆柱卡带 */
.ring li { transform: rotateY(var(--a)) translateZ(var(--r)); } /* 相机在环外 */
.tunnel li { transform: translateZ(var(--z)) scale(calc(var(--d) / (var(--d) - var(--z)))); }
.twist li:nth-child(even) { transform: rotateX(180deg); backface-visibility: visible; }
.title { letter-spacing: calc(var(--v) * 2px); } /* 同一个 velocity 喂第二处 */
```

## 来源链接
- temp/video-analysis/v06.md（六模式参数全量转写）；案例：Quorum / Chorus / Splay / Parade / Continuum / Vector
