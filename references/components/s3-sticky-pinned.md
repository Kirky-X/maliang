# S3 · 粘性钉住（Sticky Pinned）

> 标题钉在视口内，内容从底下滚过。方向辅助器：密区里用户随时知道自己在哪。

## 名称与形状

区段头 `position: sticky`，滚动时钉在视口顶部（或粘性导航之下），右/下方内容继续滚动。适合长而密的章节。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 钉住内容 | 标题 · 编号+标题 · 进度指示 |
| 底边 | 实线 1px · 发丝线 · 无 |
| 背景 | 纸色实底 · 半透明模糊 |

## 何时用与勿混淆

- **何时用**：区段内容长而密，用户受益于始终可见的方位感；规格页、长文档。
- **勿混淆**：[S1 左栏编号](s1-left-margin-numbered.md)（不动）；[F2 粘性滚动栈](f2-sticky-scroll-stack.md)（钉的是配文栏，非区段头）。

## DOM+CSS 骨架

```html
<header class="head-sticky">
  <p class="num-label">02</p>
  <h2>…</h2>
</header>
```

```css
.head-sticky { position: sticky; top: var(--banner-height, 0px);
  background: var(--color-paper); padding-block: var(--space-sm);
  border-bottom: 1px solid var(--color-ink); z-index: var(--z-sticky); }
```

**粘性配对规则**：页面存在粘性 `<header>`/`<nav>`/横幅（任何 `position: sticky; top: 0` 元素）时，必须在 token 里声明 `--banner-height`（导航实测 px 高）与 `--z-sticky-nav`（高于 `--z-sticky` 一级），本原型同时消费两者——缺了它们，区段头滚动时会盖住导航（[numbered-gates.md](../meta/numbered-gates.md) 粘性层门）。

折叠要点：<60rem 粘性通常解除（多栏塌单栏时钉住失去意义），标题回归普通流；<40rem 一律解除粘性。

## 反模式

- 与粘性导航叠用却不声明 `--banner-height`——遮挡是硬伤，不是风格。
- 同时钉多个区段头——同页只允许一个钉住元素在视口内；多个粘性头互相推挤读作 bug。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id S3 · Sticky Pinned）。
