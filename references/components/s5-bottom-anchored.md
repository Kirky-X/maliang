# S5 · 底部锚定（Bottom-anchored）

> 标签或标题放在区段内容的**下方**：内容是主角，标签是它的注脚。反转常规层级。

## 名称与形状

先给内容（图、数据块、作品），内容看完才出现编号/标题行（「— 02 完」式）。读者先被内容抓住，再由标签命名它——画廊、作品集的常见注记法。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 锚定物 | 编号 · 编号+标题 · 图注式说明 |
| 对齐 | 左 · 右 · 居中 |
| 字体 | mono 小字 · 正文小字 · 斜体 |

## 何时用与勿混淆

- **何时用**：内容本身足够有引力、标签只是档案信息；画廊、案例册、摄影页。
- **勿混淆**：[S1 左栏编号](s1-left-margin-numbered.md)（标签领先开路）；[S4 行内不断章](s4-inline-no-break.md)（嵌在正文中）。

## DOM+CSS 骨架

```html
<section>
  <div class="content">…</div>
  <p class="num-label">— 02 完</p>
</section>
```

```css
.num-label { font-family: var(--font-mono); font-size: var(--text-sm);
  color: var(--color-ink-2); margin-block-start: var(--space-sm); }
```

折叠要点：<60rem 与 <40rem 结构不变（单列本就适配）；注意锚定行与内容的间距不得塌陷——贴死内容 = 失去「注脚」语义。

## 反模式

- 重要导航信息放进底部标签——它是注脚不是标题，找关键信息的人不该被迫滚过整个区段。
- 一页里 S5 与 [S1](s1-left-margin-numbered.md) 混用不声明——同页区段头原型互不重复（总则 1）；要么全前置要么全后置，混合时必须有节奏理由并在盖章声明。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id S5 · Bottom-anchored）。
