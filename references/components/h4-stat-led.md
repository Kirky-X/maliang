# H4 · 数字主导（Stat-Led）

> 一个巨型数字做首屏主角，底下一行小限定语。数字必须经得起追问。

## 名称与形状

首屏放一个 display 级数字（tabular 数字、行高压到 0.85）加一行限定语；可选配两枚次级数据。整节靠数字的体量压场，无图无按钮组。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 数字风格 | tabular display · 斜体 display · 等宽 mono |
| 限定语位置 | 数字下方 · 行内右置 · 上方堆叠 |
| 次级数据 | 无 · 下方两枚 · 一行四枚 |

## 何时用与勿混淆

- **何时用**：手里有一个站得住、可外部验证的数字（实测延迟、真实用户量）。数字必须真实——用户未供的量化声明按 [data-floor.md](../meta/data-floor.md) 与 [copy-strategy.md](../meta/copy-strategy.md) 阶梯处理（`—` + 待确认，不虚构）。
- **勿混淆**：[T4 编号数据条](t4-numbered-stat-strip.md)（多个指标横排，非单一焦点）；[H1 跑马灯宣言](h1-marquee.md)（主角是句子）。

## DOM+CSS 骨架

```html
<section class="hero-stat">
  <p class="figure tnum">99.97<span class="unit">%</span></p>
  <p class="qualifier">外部实测，过去 12 个月</p>
</section>
```

```css
.hero-stat { min-height: 70dvh; display: grid; align-content: center;
  padding: 0 var(--page-gutter); }
.figure { font-size: clamp(6rem, 18vw, 16rem);
  font-variant-numeric: tabular-nums; line-height: 0.85; }
```

折叠要点：<60rem 数字保持全宽、文字在下方堆叠、次级数据收成两列；<40rem 数字 clamp 下限抬高一档（视觉再缩）、限定语换行。

## 反模式

- 用「大数字 + 小标签 + 渐变 accent」品类默认套路而不声明拒绝——见 [design-md.md](../commands/design-md.md) Defaults 机制。
- 数字编尾数充门面：stat 永不做 hero 唯一标题的借口；没有真实数字就换 [H1](h1-marquee.md) 或 [H3](h3-quote-led.md)。
- 跨产出照抄同组旋钮值 = 同款；复用必须至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H4 · Stat-Led）。
