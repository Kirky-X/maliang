# S1 · 左栏编号（Left-margin Numbered）

> 窄左栏放「01 — 标签.」，宽右栏放标题与内容。编辑排印的经典编号骨架。

## 名称与形状

区段头两栏结构：左列固定约 10rem 放编号标签（`01 — Foundations` 式），右列放区段标题与正文。编号建立页面的章节感，基线对齐。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 编号制式 | `01` · `1.0` · `一/二/三`（中文语境优先） |
| 标签内容 | 纯编号 · 编号+类目词 · 类目词大写 |
| 左栏宽 | 8rem · 10rem · 12rem |

## 何时用与勿混淆

- **何时用**：编辑型/样册型页面；章节多、需要导航感的 long document。
- **勿混淆**：[S5 底部锚定](s5-bottom-anchored.md)（标签在区段下面）；[S3 粘性钉住](s3-sticky-pinned.md)（标题随滚动钉住）。

## DOM+CSS 骨架

```html
<header class="head-margin">
  <p class="num-label">01 — 基础</p>
  <h2>…</h2>
</header>
```

```css
.head-margin { display: grid; grid-template-columns: 10rem 1fr;
  gap: var(--space-xl); align-items: baseline; }
.num-label { font-family: var(--font-mono); font-size: var(--text-sm);
  color: var(--color-ink-2); }
```

折叠要点：<60rem 左栏并入正文流——编号标签移到标题上方成行内（横切规则：边栏标签转行内）；右栏全宽。

## 反模式

- 每个区段都编号 + 每段都用本原型——同页区段头原型必须互不重复（总则 1），编号全页一套制式。
- 编号是装饰但章节关系是假的（跳号、重号）——编号必须反映真实结构。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id S1 · Left-margin Numbered）。
