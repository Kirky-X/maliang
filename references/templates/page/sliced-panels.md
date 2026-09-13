---
name: sliced-panels
title: 竖切分栏型
category: page-pattern
status: style
source: 视频研究 v05「5 种高级质感网页」（MARCHAL 案例转写）
era: 2026
verified: 2026-09-07
variance: "4-7"
motion: "3-6"
density: "2-5"
platforms: Web 桌面端
---
# 竖切分栏型（Sliced Panels）

## 一句话定位
整屏竖切成 5-6 条，同一时间只亮一格——hover 的那条 flex-grow 展开、恢复彩色，其余压暗降饱和；"只亮一格"是整页的戏剧中心。

## 视觉特征（token 级参数）
- 全屏 flex 容器竖切 5-6 条，默认等宽（flex: 1）
- 展开条：`flex-grow` 过渡约 **1.1s**（展开至 2-3 倍宽）
- 聚焦规则：hover 条 `filter: none`（彩色），其余 `grayscale(1) brightness(.55)` 降饱和压暗
- 文案放在展开条内：竖排或旋转 90° 的标题 + 展开后显影的描述
- 案例 MARCHAL：摄影人像条 + 白色大字"一张照片只是一句话。"

## 结构骨架
1. 全屏 flex 行容器（100vh，overflow hidden）
2. 每条：背景图 cover + 顶部小序号 + 底部标题
3. hover：该条 flex-grow 3-4 + 彩色，兄弟条压暗（transition 同步 1.1s）
4. 展开条内浮层：描述文字淡入（延迟 0.2-0.3s）
5. 移动端降级：改为横向 scroll-snap 轮播，一屏一条

## 适用场景 / 慎用场景
- 适用：分类导航页、系列作品集、服务线展示、品类入口
- 慎用：每条内容需要完整阅读的页面；>6 条（压暗区过窄失去意义）

## AI 常见翻车点（反模式）
1. 同时亮多格或全彩——"只亮一格"原则崩塌，变成普通图墙
2. 展开动画用 0.2s 生硬跳变（正确 0.8-1.2s 缓动）
3. 压暗条仍保留高对比文字，视觉噪声
4. 移动端直接堆叠为普通列表，特色全失

## CSS 关键实现（≤15 行）
```css
.panels { display: flex; height: 100vh; }
.panel { flex: 1; transition: flex-grow 1.1s cubic-bezier(.22,1,.36,1), filter .6s; filter: grayscale(1) brightness(.55); }
.panel:hover { flex-grow: 3; filter: none; }
.panel:hover .desc { opacity: 1; transform: none; transition-delay: .25s; }
.desc { opacity: 0; transform: translateY(8px); transition: .4s; }
@media (max-width: 768px) { .panels { flex-direction: column; } }
```

## 来源链接
- temp/video-analysis/v05.md（帧转写）；案例：MARCHAL 摄影集
