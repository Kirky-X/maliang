# H3 · 引言主导（Quote-Led）

> 带署名的拉引言做首屏主角。标题的位置让给借来的可信度。

## 名称与形状

首屏只放一段 display 级引言与一行署名。它赌的是：一句真用户的原话比任何自夸文案都硬。整节无图、无按钮，排印即设计。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 引言字重 | 斜体 display · 正体 display · 正体大号正文 |
| 署名位置 | 引言下方 · 边栏对齐 · 右齐 |
| 长度 | ≤80 字符 · 80-160 字符 |

## 何时用与勿混淆

- **何时用**：手里有一条真证言，硬到足以撑起首页；引言必须是真实可溯的（无真引言不得伪造，见 [data-floor.md](../meta/data-floor.md)）。
- **勿混淆**：[T3 独占巨引](t3-single-huge-quote.md)（住页面中段，不住首屏槽位）；[H5 书信开场](h5-letter-hero.md)（第一人称自述，非他人评价）。

## DOM+CSS 骨架

```html
<section class="hero-quote">
  <blockquote class="display-italic">"…"</blockquote>
  <p class="attribution">— 姓名，职务，公司</p>
</section>
```

```css
.hero-quote { min-height: 70dvh; display: grid; align-content: center;
  gap: var(--space-lg); padding: 0 var(--page-gutter); }
.display-italic { font-size: clamp(1.75rem, 4.5vw, 3.5rem); line-height: 1.15; }
```

折叠要点：<60rem 引言保持全宽、署名折到独立一行；<40rem 引言与署名字号各降一档。

## 反模式

- 中文页面滥用斜体引言——中文没有真斜体，强调优先换字重或引号排版（[font.md](../dimensions/font.md) 口径）；「斜体 display」旋钮值对中文产出等价于换字重档。
- 编造署名或头衔充门面——证言造假比没有证言更伤。
- 跨产出照抄同组旋钮值 = 同款；复用必须至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H3 · Quote-Led）。
