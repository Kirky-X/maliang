# N7 · 粗野厚板导航（Brutal Slab）

> 重型通栏导航：2px 实线下边、全大写字标与加字距大写链接行、密节奏。无阴影、无圆角。Pentagram 项目页、Liquid Death、粗野主义倾向代理的气质。

## 名称与形状

一行重排版：粗字标 + 大写链接行 + 块状 CTA，下边一条 2px 墨线封底。全部语言是「板」——平、重、直角；与圆角/模糊/软影词汇互斥。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 边重 | 2px · 3px · 4px |
| 字距 | 加字距大写 · 常规 |
| CTA | 实心厚板块 · 描边块 · 纯文字 |

## 何时用与勿混淆

- **何时用**：playful 系里的粗野/宣言/运动调性，或品牌声音本身沉重、宣告式。
- **勿混淆**：[N1 字标双链](n1-wordmark-2-links.md)（小而安静）；[N6 报纸报头](n6-newspaper-masthead.md)（居中对称的编辑重，非左对齐的粗野重）。

## DOM+CSS 骨架

```html
<header class="nav-slab">
  <a class="slab-mark">STUDIO</a>
  <nav class="slab-nav" aria-label="主导航">
    <ul><li><a>目录</a></li><li><a>声音</a></li><li><a>作品</a></li></ul>
  </nav>
  <a class="cta-slab">获取</a>
</header>
```

```css
.nav-slab { display: flex; align-items: center; gap: var(--space-md);
  padding: var(--space-sm) var(--page-gutter);
  border-bottom: 2px solid var(--color-ink); background: var(--color-paper); }
.slab-mark { font-weight: 800; letter-spacing: 0.04em; }
.slab-nav ul { display: flex; gap: var(--space-md); list-style: none; margin-left: auto; }
.slab-nav a { text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
```

折叠要点：<60rem 链接折到第二行、CTA 保持右对齐；<40rem 链接收进汉堡——只留字标 + 汉堡（≥44px 命中区）。

## 反模式

- N7 配圆角、软影或 backdrop-blur——词汇对冲；要 blur 退 [N5](n5-floating-pill.md)，要圆角退 [N1](n1-wordmark-2-links.md)。
- 加字距大写用在中文链接——中文无大写，等价物是加字距 + 字重（[font.md](../dimensions/font.md)），硬写 `text-transform` 无效。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N7 · Brutal Slab）。
