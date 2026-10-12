# F2 · 粘性滚动栈（Sticky Scroll Stack）

> 左栏钉住，右栏滚动逐张换出关联截图。一条特性配一串子状态的讲法。

## 名称与形状

两栏特性区：左栏 `position: sticky` 钉住特性标题与配文，右栏纵向滚过多张截图/代码块，滚动与左栏文案形成「讲到哪、图到哪」的同步感。粘性层纪律与 [S3](s3-sticky-pinned.md) 配对规则相同。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 钉住侧 | 左 · 右 |
| 右栏内容 | 代码 · 截图 · 图示 |
| 配对数 | 3 · 4 · 5 |

## 何时用与勿混淆

- **何时用**：特性有多个子状态值得按序展示；功能演示、编辑器/工具类产品。
- **勿混淆**：[F4 步骤序列](f4-step-sequence.md)（线性编号、无滚动同步）；[F5 标注截图](f5-annotated-screenshot.md)（单张截图上打标注）。

## DOM+CSS 骨架

```html
<section class="sticky-stack">
  <div class="pane-sticky"><h3>…</h3><p>…</p></div>
  <div class="pane-scroll">
    <figure>1</figure><figure>2</figure><figure>3</figure>
  </div>
</section>
```

```css
.sticky-stack { display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--space-2xl); }
.pane-sticky { position: sticky;
  top: calc(var(--banner-height, 0px) + var(--space-xl));
  align-self: start; z-index: var(--z-sticky); }
```

折叠要点：<60rem 粘性解除（横切规则：粘性栏 unstick），内容退化为「配文块 + 图」交替的线性序列；<40rem 图统一收为 16/9 行内尺寸，全页无粘性行为。

## 反模式

- 钉住栏高度超过视口——钉住内容必须短于一屏，否则底部永远看不见。
- 与粘性导航叠用未声明 `--banner-height`——`calc()` 缺项导致钉住栏钻到导航底下。
- 跨产出照抄同组旋钮值（同钉侧 + 同配对数）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id F2 · Sticky-scroll Stack）。
