# F1 · Bento 网格（Bento Grid）

> 8-15 块混合跨度（1×1、2×1、1×2、2×2）的非对称瓦片，节奏来自大小对比。

## 名称与形状

CSS Grid 特性区：等宽轨道 + 固定行高，瓦片用不同 span 制造不对称。每块瓦片是同等合法的入口，视觉权重由跨度分配。注意 [hero.md](../vocabulary/hero.md)「网格拼贴」骨架管首屏怎么排，本原型管主体区段怎么建——两者可衔接。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 瓦片数 | 4 · 6 · 7 · 9 |
| 跨度 | 规则 · 不规则 · 马赛克 |
| 边界 | 全发丝线 · 仅 accent 角 · 无边 |

## 何时用与勿混淆

- **何时用**：多个同等合法的入口点；SaaS 特性页、平台能力总览。
- **勿混淆**：[F2 粘性滚动栈](f2-sticky-scroll-stack.md)（纵向配对滚动）；[F6 商品卡网格](f6-product-card-grid.md)（卖商品，卡片**均匀**是有意的）。

## DOM+CSS 骨架

```html
<section class="bento">
  <article class="cell span-2x2">…</article>
  <article class="cell span-1x1">…</article>
  <article class="cell span-2x1">…</article>
</section>
```

```css
.bento { display: grid; grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 12rem; gap: var(--space-md); }
.span-2x2 { grid-column: span 2; grid-row: span 2; }
.span-2x1 { grid-column: span 2; }
.span-1x2 { grid-row: span 2; }
@media (max-width: 60rem) { .bento { grid-template-columns: repeat(2, 1fr); } }
```

折叠要点：<60rem 4 列收 2 列、大瓦片跨 2 小瓦片跨 1；<40rem 收单列，瓦片顺序按信息优先级排——跨度和层级解耦后顺序就是层级。

## 反模式

- 瓦片 >8 还要继续铺——Hum 等圆润系的硬上限是 8；密度失控读作 dashboard（DENSITY dial 越界）。
- 「图标瓦片 + 标题 + 两行灰字」×3 等距——这是被 [ai-tells.md](../meta/ai-tells.md) 点名的三等卡反射单元；有_three 件事就说成别的形状。
- 跨产出照抄同组旋钮值（上一次 `tiles=6, spans=irregular, accent=corner-only`，这次照抄 = 同款）：至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id F1 · Bento Grid）。
