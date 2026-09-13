---
name: depth-corridor
title: 纵深长廊型
category: page-pattern
status: style
source: 视频研究 v05「5 种高级质感网页」（STRATUM GALLERY 案例转写）
era: 2026
verified: 2026-09-07
variance: "5-8"
motion: "5-8"
density: "1-4"
platforms: Web 桌面端
---
# 纵深长廊型（Depth Corridor）

## 一句话定位
作品不摆成网格，摆成一条路：透视 1500px + 滚动给冲量，滚得越快两侧退得越远、越远越暗——滚动是"走路"，不是"读列表"。

## 视觉特征（token 级参数）
- 容器透视：`perspective: 1500px`
- 作品沿一条路排布（中景大、两侧小、间距递减），禁等距网格
- 滚动冲量系数约 **0.42**（滚动速度映射为位移增益/景深变化）
- 深度衰减：越远越小且越暗（`brightness`/`opacity` 随 z 递减）
- 案例 STRATUM GALLERY：近黑长廊 + 中景竖幅作品 + 左上 "STRATUM GALLERY" 字标

## 结构骨架
1. 全屏暗色容器，perspective 打在作品轨道上
2. 作品沿 z/对角线序列摆放，首屏保证一件中景作品清晰可见
3. 滚动监听：速度 → 冲量插值 → 轨道位移 + 两侧作品后退/变暗
4. 停止滚动：惯性衰减归位，最近作品自动聚光
5. 移动端降级：退化为垂直视差列表（保留"远暗近亮"）

## 适用场景 / 慎用场景
- 适用：作品集、展览馆、品牌里程碑、叙事型落地页
- 慎用：需要 SEO 抓取全部内容的主内容页（懒渲染须留无障碍替代）；性能敏感页面（大量 layer 合成）

## AI 常见翻车点（反模式）
1. 摆成等距网格再撒透视——正确：沿路排布、不等距
2. 透视值过小（<800px）变形剧烈，或过大（>3000px）无纵深感
3. 无惯性插值，滚动生硬（正确：冲量 + lerp 衰减）
4. 远处作品不压暗，长廊变"平面拼贴"

## CSS 关键实现（≤15 行）
```css
.corridor { perspective: 1500px; height: 100vh; overflow: hidden; background: #0a0a0c; }
.track { transform-style: preserve-3d; will-change: transform; }
.piece { position: absolute; transform: translate3d(var(--x), var(--y), var(--z));
  filter: brightness(calc(1 - var(--z-n) * .45)); }
/* JS: wheel 速度 → 冲量 0.42 → rAF lerp 更新 --z；离屏作品降级为静态 */
@media (prefers-reduced-motion: reduce) { .track { transform: none !important; } }
```

## 来源链接
- temp/video-analysis/v05.md（帧转写）；案例：STRATUM GALLERY 作品集
