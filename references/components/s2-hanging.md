# S2 · 悬置标题（Hanging）

> 标题浮在区段上方的负空间里：无边、无分割线。安静、有呼吸感的内容配它。

## 名称与形状

最省的区段头：一个标题 + 一大段上下 padding，靠空白把标题「悬」在节前。没有任何线条与框，分隔感全部来自留白——与 [principles.md](../meta/principles.md) 接近性原则同源：间距够时不需要分隔物。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 悬置量 | `3xl` 上距 · `2xl` 上距（密度节奏留一枚给 [F4](f4-step-sequence.md) 等密区） |
| 标题对齐 | 左 · 居中 |
| 前缀 | 无 · 类目小字 · 编号 |

## 何时用与勿混淆

- **何时用**：内容有安静、留得住呼吸的编辑气质；区段间需要大节奏对比时。
- **勿混淆**：[S4 行内不断章](s4-inline-no-break.md)（嵌进正文流，无空间断章）；[S3 粘性钉住](s3-sticky-pinned.md)（随滚动钉住，本原型完全静止）。

## DOM+CSS 骨架

```html
<header class="head-hang">
  <h2>…</h2>
</header>
```

```css
.head-hang { padding-block: var(--space-3xl) var(--space-xl); }
```

折叠要点：<40rem 悬置量按比例收（`3xl`→`xl` 档）——手机屏留白是奢侈品，但不得收为零：留白归零即失去原型身份。

## 反模式

- 手痒补一条分割线或底色——负空间就是本原型的全部；要线就用 [S1 左栏编号](s1-left-margin-numbered.md) 的体系。
- 悬置量全页恒定、节与节无密度对比——与「交替疏密」的节奏纪律相抵（[variation-engine.md](../templates/variation-engine.md) 密度轴）。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id S2 · Hanging）。
