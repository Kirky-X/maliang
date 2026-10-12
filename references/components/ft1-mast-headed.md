# Ft1 · 报头式页脚（Mast-headed）

> 字标 + 标语锚定一条横带，旁边两三条小链接，地址或许可放下面。内容重的页面，页脚就该安静而单一。

## 名称与形状

一条横带式页脚：字标（+ 一句标语）在左，两三个小链接在侧，地址/许可收在底部一行。单层结构，无分栏矩阵。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 字标字号 | display 3xl · display 2xl · xl |
| 标语 | 斜体衬线（西文限定）· 正体正文 · 无 |
| 链接行 | 单行内联 · 两行堆叠 |

## 何时用与勿混淆

- **何时用**：页面内容重、页脚应当退后；编辑型、工作室站。
- **勿混淆**：[Ft2 单行内联](ft2-inline-rule-single-line.md)（更彻底的减法）；[Ft5 宣言句](ft5-statement.md)（主角是一句话，非字标）。

## DOM+CSS 骨架

```html
<footer class="foot-mast">
  <p class="wordmark">工作室名</p>
  <p class="tagline muted">设计得不像生成的。</p>
  <p class="links muted">版权 · 隐私 · 联系</p>
</footer>
```

```css
.foot-mast { padding: var(--space-2xl) var(--page-gutter);
  display: grid; gap: var(--space-2xs); }
.foot-mast .wordmark { font-size: var(--text-2xl); font-weight: 600; }
.foot-mast .muted { color: var(--color-ink-2); font-size: var(--text-sm); }
```

折叠要点：<60rem 链接折成两行、标语落到字标下方；<40rem 字标字号降一档。

## 反模式

- 偷偷长出四列链接矩阵——那是 [Ft3](ft3-index-style-category-list.md) 的形状；两原型不得互串。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」——同类页脚连续两次构建相同即违规（总则 2）。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft1 · Mast-headed）。
