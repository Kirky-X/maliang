# H9 · 手绘插画主角（Custom Illustration Centerpiece）

> 一件自建 SVG（或纯 CSS 形状）做首屏唯一主视觉：面包店的面包、工作室吉祥物、流程图。插画是「画」出来的，不是素材库里捡的。

## 名称与形状

文案 + 一件手建插画的 hero。插画本体按 [visual-assets.md](../meta/visual-assets.md) 富化层级自建：简单形状用纯 CSS，复杂造型手写 SVG——禁 Storyset / Humaaans / unDraw / Lottie 现成品。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 构建法 | 纯 CSS（简单形状）· 手写 SVG · 生成 · 图库（后两档须过资产门） |
| 动画 | 无 · 循环 · 滚动联动（40rem 以下禁，横切规则 7） |
| 体量 | 小点缀 · 主角 |

## 何时用与勿混淆

- **何时用**：品牌有一件「值得画出来的东西」——一门手艺、一个角色、一道工序。
- **勿混淆**：[H6 摄影满版](h6-photographic-fold.md)（真摄影）；[H8 模型分栏](h8-mockup-split-browser-framed.md)（产品截图，非画作）。

## DOM+CSS 骨架

```html
<section class="hero-art">
  <div>
    <p class="eyebrow">枫树街面包房 · 创立于 2026</p>
    <h1>每天早晨的酸面包。</h1>
  </div>
  <svg viewBox="0 0 200 100" class="loaf" aria-label="一只面包">
    <path class="loaf__body" d="M 20 70 Q 100 10 180 70 L 180 90 L 20 90 Z" />
    <path class="loaf__score" d="M 60 50 L 90 30 M 100 45 L 130 25 M 140 50 L 165 35" />
  </svg>
</section>
```

```css
.hero-art { display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--space-2xl); align-items: center; }
.loaf__body { fill: oklch(72% 0.14 50); }
.loaf__score { stroke: oklch(38% 0.10 35); stroke-width: 2;
  fill: none; stroke-linecap: round; }
```

折叠要点：<60rem 塌单栏、插画移到文案下方（或上方——按气质定）；<40rem 插画缩到视口宽 ≤40%，永不喧宾夺主。

## 反模式

- 从素材库拖一张「通用插画」冒充手绘——AI 味重灾区（见 [ai-tells.md](../meta/ai-tells.md)）；画不出来就换纯文字构图。
- 插画 + 倾斜 + 阴影 + 视差全上——一件主角只需要体量，不需要特效叠加。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H9 · Custom Illustration Centerpiece）。
