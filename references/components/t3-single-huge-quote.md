# T3 · 独占巨引（Single Huge Quote）

> 一句引言放大到占据整节：居中、无支撑文本、署名收成一行小型大写。一句好到配得上整个房间的引言。

## 名称与形状

整节只放一条 display 级引言 + 一行小署名。没有卡片、没有头像、没有 supporting 文本——排印的体量就是全部说服力。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 引言字面 | 衬线斜体（西文限定）· 正体 display · 斜体 mono |
| 宽度 | 满版 · 60ch · 40ch |
| 署名位置 | 同行末 · 独立条带 |

## 何时用与勿混淆

- **何时用**：一条真引言强到值得独占一节（融资公告引用、关键客户背书）。引言真实性归 [data-floor.md](../meta/data-floor.md)。
- **勿混淆**：[T1 边注拉引言](t1-pull-quote-with-marginalia.md)（旁注 mate，非房间主角）；[H3 引言主导](h3-quote-led.md)（同一形状住 hero 槽位——同页两者只取其一）。

## DOM+CSS 骨架

```html
<section class="proof-room">
  <blockquote class="display">"…"</blockquote>
  <p class="attribution"><span class="caps">— 姓名，公司</span></p>
</section>
```

```css
.proof-room { min-height: 60dvh; display: grid; align-content: center;
  justify-items: center; gap: var(--space-lg);
  padding: 0 var(--page-gutter); }
.proof-room blockquote { font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.15; max-width: 30ch; text-align: center; }
```

折叠要点：<60rem 引言保持全宽、署名折到下方；<40rem 引言字号按 1.4× 系数降档。

## 反模式

- 没有好引言硬凑一条——本原型没有「退而求其次」档：引言不够强就用 [T4 数据条](t4-numbered-stat-strip.md)。
- 中文页强用衬线斜体旋钮值——中文无斜体，等价值是换字重/引语体（[font.md](../dimensions/font.md)）。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id T3 · Single Huge Quote）。
