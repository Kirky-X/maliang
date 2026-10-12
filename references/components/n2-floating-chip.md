# N2 · 浮动角标导航（Floating Chip）

> 钉在角落的小 chip：字标 + 单一动作（「试试」）。不占文档流。首屏很满、传统导航会跟内容打架时用它。

## 名称与形状

`position: fixed` 的小块贴角：无边框顾虑的小 chip，字标与一枚动作并排。页面顶部完全让给内容——导航缩成一件随身物件。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 锚点 | 顶部 · 底部 · 右上 · 左下 |
| 内容 | 主题切换 · 搜索 · 导航 |
| 底衬 | 模糊 · 实底 · 无 |

## 何时用与勿混淆

- **何时用**：满版/沉浸式首屏（[H6](h6-photographic-fold.md) 满版图、[H7](h7-demo-video-clipped-by-viewport-edge.md) 视频裁边）压顶时，导航退居角落。
- **勿混淆**：[C4 粘性底栏](c4-sticky-bottom-bar.md)（全宽通栏）；[N5 浮动药丸](n5-floating-pill.md)（内容尺寸药丸含链接簇）。

## DOM+CSS 骨架

```html
<aside class="nav-chip">
  <a class="wordmark">工作室</a>
  <a class="cta-outline">试试 →</a>
</aside>
```

```css
.nav-chip { position: fixed; top: var(--space-md); right: var(--space-md);
  display: inline-flex; gap: var(--space-md);
  padding: 0.5rem 0.75rem; background: var(--color-paper);
  border: 1px solid var(--color-rule); }
```

折叠要点：<60rem chip 仍浮动、padding 收一档；<40rem 加宽到支持 44px 命中区（总则 5）、宽度不得低于 280px。

## 反模式

- 把整套导航塞进 chip——它只带一个动作；目的地多就换 [N1b](n1b-saas-three-section.md)。
- chip 悬在内容上却无底衬——文字与下层内容混叠不可读；模糊或实底至少取一。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N2 · Floating Chip）。
