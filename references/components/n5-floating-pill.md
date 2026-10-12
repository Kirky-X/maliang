# N5 · 浮动药丸导航（Floating Pill）

> 圆角药丸形导航，明显脱离页缘，悬在顶部约 `var(--space-md)` 处：模糊底衬 + 软影。当代 modern-minimal 的招牌（Vercel / Linear / Framer / Raycast 谱系）。

## 名称与形状

`position: fixed` 居中悬置的内容尺寸药丸：`border-radius: 999px`、`backdrop-filter: blur` 底衬、软阴影。关键在「明显脱离」——药丸不接页缘，悬浮感靠四周留白成立。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 宽 | 内容尺寸 · 上限 ~720px · 上限 ~560px |
| 底衬 | blur+saturate · 实底 · 轻渐变 |
| 锚点 | 顶居中 · 顶右 · 顶左 |

## 何时用与勿混淆

- **何时用**：modern-minimal / 氛围型页面，且药丸下方有可透过模糊看见的 distinct 表面或图像——blur 没东西可糊就失去意义。
- **勿混淆**：[N1 字标双链](n1-wordmark-2-links.md)（通栏）；[N2 浮动角标](n2-floating-chip.md)（角落锚定、单动作）；[N10 滚动形变浮窗](n10-floating-on-scroll-morph.md)（N5 + 落地栏态，含滚动行为）。

## DOM+CSS 骨架

```html
<nav class="nav-pill" aria-label="主导航">
  <a class="wordmark">工作室</a>
  <ul class="links"><li><a>目录</a></li><li><a>声音</a></li></ul>
  <a class="cta-fill">获取 →</a>
</nav>
```

```css
.nav-pill { position: fixed; inset: var(--space-md) auto auto 50%;
  transform: translateX(-50%); display: inline-flex; align-items: center;
  gap: var(--space-md); padding: 0.5rem 0.875rem;
  background: color-mix(in oklch, var(--color-paper) 78%, transparent);
  backdrop-filter: blur(14px) saturate(120%);
  border: 1px solid var(--color-rule); border-radius: 999px;
  box-shadow: 0 8px 24px -12px oklch(0% 0 0 / 0.18); z-index: 20; }
```

折叠要点：<60rem 药丸撤掉链接列表，只留字标 + CTA，保持脱离；<40rem 变成顶角 chip——字标左、汉堡右（汉堡 ≥44px 命中区，总则 5）。

## 反模式

- 宽到约 95% 视口的「药丸」——那是圆了角的通栏导航，不是药丸；链接把药丸撑过 ~720px 就删一条链接或换 [N1b](n1b-saas-three-section.md)。
- 药丸下面是纯色平地——blur 无物可糊，改实底或换原型。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N5 · Floating Pill）。
