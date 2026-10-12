# T4 · 编号数据条（Numbered Stat Strip）

> 3-5 个互补指标（数字 + 限定语）横排一条，tabular 数字。多个指标互相成全时的证明区。

## 名称与形状

单行水平条：3-5 组「大数字 + 小限定语」并排，数字 tabular 对位。与 hero 的单数字不同：这里每个数字是证人之一，合起来构成群体证据。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 布局 | 3 列 · 4 列 · 5 列 · 6 列 |
| 数字字重 | display · 大号正文 |
| 限定语位置 | 数字下方 · 行内 · 上方 |

## 何时用与勿混淆

- **何时用**：手里有多个互补的真实指标（用户数 · 可用性 · 覆盖地域）。数字必须真实——未供的量化声明按 [data-floor.md](../meta/data-floor.md) 阶梯置 `—` 待确认，不虚构。
- **勿混淆**：[H4 数字主导](h4-stat-led.md)（hero 槽位的单一焦点数字）；[F3 规格表](f3-tabular-spec-sheet.md)（逐行特性清单）。

## DOM+CSS 骨架

```html
<section class="stat-strip tnum">
  <div><b>240 万</b><span>用户</span></div>
  <div><b>99.97%</b><span>可用性</span></div>
  <div><b>14</b><span>地域</span></div>
</section>
```

```css
.stat-strip { display: grid; grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg); }
.stat-strip b { font-size: var(--text-2xl);
  font-variant-numeric: tabular-nums; display: block; }
.stat-strip span { font-size: var(--text-sm); color: var(--color-ink-2); }
```

折叠要点：<60rem 4 列 → 2 列；<40rem 转纵向——一指标一行（竖排后限定语保持跟随其数字，勿拆散配对）。

## 反模式

- 指标膨胀到 6 个以上还硬挤一行——超过 6 列转 [F3 规格表](f3-tabular-spec-sheet.md) 逐行讲。
- 数字对不上限定语（单位缺失、口径不明）——每个限定语必须能回答「这数字怎么测的」。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id T4 · Numbered Stat Strip）。
