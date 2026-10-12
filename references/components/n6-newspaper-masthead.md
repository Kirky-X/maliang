# N6 · 报纸报头导航（Newspaper Masthead）

> 通栏报头：上排居中大字标、细体期号/日期行（衬线小型大写）、可选链接行，最下双线压阵。NYT / FT / Vogue 的宽版气质。

## 名称与形状

居中对称的报头栈：期号行 → 大字标 → 链接行 → 双细线。整行居中、字距考究——页面被装帧成「一期」而非「一个产品」。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 期号行 | 字标上方 · 字标下方 · 无 |
| 字标字号 | 3xl · 2xl · xl |
| 底线 | 双线 · 单线 · 无 |

## 何时用与勿混淆

- **何时用**：编辑型、杂志形态、或明确装帧为「期/版」的页面；与 [Ft1 报头式页脚](ft1-mast-headed.md) 同族。
- **勿混淆**：[N1 字标双链](n1-wordmark-2-links.md)（不对称的小顶栏）；[N7 粗野厚板](n7-brutal-slab.md)（左对齐、重边、全大写——同是「重」，气质相反）。

## DOM+CSS 骨架

```html
<header class="nav-mast">
  <p class="mast-line muted">第 22 期 · 2026 春 · 工作室</p>
  <h1 class="mast-name">STUDIO</h1>
  <nav class="mast-nav" aria-label="主导航">
    <ul><li><a>目录</a></li><li><a>声音</a></li><li><a>来信</a></li></ul>
  </nav>
  <hr class="mast-rule" aria-hidden="true">
</header>
```

```css
.nav-mast { display: grid; gap: var(--space-2xs); text-align: center;
  padding: var(--space-md) var(--page-gutter) 0; }
.mast-name { font-size: clamp(2.25rem, 5vw, 3.75rem); line-height: 0.95; }
.mast-rule { border: 0; border-top: 1px solid var(--color-rule);
  border-bottom: 1px solid var(--color-rule); height: 4px;
  margin: var(--space-sm) 0 0; }
```

折叠要点：<60rem 期号行堆到字标上方、链接折成第二行；<40rem 字标字号降一档、链接行收进「目录」披露钮（≥44px 命中区）。

## 反模式

- SaaS 仪表盘或开发者工具页用报头——报头词汇属于长文/编辑语境，B2B 产品上读作戏服。
- 字标字体与正文字体无差别——报头靠字标的 display 字面成立；无 display 字面就换原型。
- 写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」——同类导航连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N6 · Newspaper Masthead）。
