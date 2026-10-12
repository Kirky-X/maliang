# N1b · SaaS 三段标准栏（Canonical SaaS Three-Section）

> 字标贴左 · 中簇 4-6 条链接（可带 hover 下拉）· 登录 + 实心 CTA 贴右。2024-26 的主导营销导航（Stripe / Linear / Vercel / Figma / Notion 谱系）。N1 是极简双链变体；本原型是密集均衡版。

## 名称与形状

三段 grid（`1fr auto 1fr`）：品牌左、中簇居中、动作右；滚动过约 24px 后磨砂化（blur 背景 + 发丝线 + 软影）并收紧高度。滚动处理器必须 rAF 节流。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 中簇链接数 | 3 · 4 · 5-6 |
| 下拉数 | 无 · 1 · 2 |
| 滚动态 | 滚动磨砂（默认）· 恒实底 · 透明固定 |
| CTA 组 | 登录+实心 · 仅实心 |

## 何时用与勿混淆

- **何时用**：SaaS / 产品 / 开发工具页，目的地多且有清晰主行动。modern-minimal 与活泼系产品页的默认第一顺位。
- **勿混淆**：[N1](n1-wordmark-2-links.md)（无中簇）；[N5 浮动药丸](n5-floating-pill.md)（脱离页缘）；[N11 巨型菜单](n11-mega-menu.md)（全宽面板，非小下拉）。

## DOM+CSS 骨架

```html
<header class="nav"><div class="nav__inner">
  <a class="nav__brand"> conduit </a>
  <nav class="nav__center">
    <a class="nav__link">文档</a><a class="nav__link">定价</a>
  </nav>
  <div class="nav__right"><a class="btn--text">登录</a><a class="btn">开始</a></div>
</div></header>
```

```css
.nav { position: fixed; inset: 0 0 auto; z-index: 500; transition: background 240ms, border-color 240ms; }
.nav.is-scrolled { background: color-mix(in oklch, var(--color-paper) 72%, transparent);
  backdrop-filter: blur(18px) saturate(160%);
  border-bottom-color: var(--color-rule); }
.nav__inner { max-width: var(--page-max); margin: 0 auto; height: 64px;
  padding-inline: var(--page-gutter);
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; }
```

折叠要点：<900px 隐藏 `.nav__center`——品牌 + CTA（或汉堡）留守；汉堡与 CTA 命中区 ≥44px（总则 5）。

## 反模式

- 中簇与品牌/CTA 挤撞——放不下就减到 3 条或退 [N1](n1-wordmark-2-links.md)。
- 下拉只认点击、无 hover/focus 通道——键盘与指针用户全灭；下拉必须 `:focus-within` 同开。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；题材默认款不能连用。跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N1b · Canonical SaaS Three-section）。
