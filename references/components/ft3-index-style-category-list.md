# Ft3 · 索引式分类列页脚（Index-style Category List）

> 3-4 短列：小型大写类目头，各挂 4-6 条链接。真枢纽或文档根的页脚。

## 名称与形状

分栏链接矩阵：每列一个大写/小型大写类目头（产品 · 公司 · 资源），列内 4-6 条链接。它是**站点地图的页脚化**——列结构必须映射真实的站点信息架构。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 列数 | 3 · 4 · 5 |
| 类目头风格 | 小型大写 · 斜体 · mono |
| 列内符号 | 发丝线分隔 · 无 |

## 何时用与勿混淆

- **何时用**：页面是枢纽或文档根，确有一张站点地图要放。
- **勿混淆**：其余一切场景——**默认远离 Ft3**：「产品·公司·资源·法律 + 社交行 + 小版权」四件套是最被滥用的 AI 指纹页脚；非枢纽页脚默认 [Ft1](ft1-mast-headed.md)/[Ft2](ft2-inline-rule-single-line.md)/[Ft4](ft4-dense-typographic.md)-[Ft8](ft8-marquee-scroll.md)。

## DOM+CSS 骨架

```html
<footer class="foot-index">
  <div><p class="caps">产品</p><ul><li>…</li></ul></div>
  <div><p class="caps">公司</p><ul><li>…</li></ul></div>
  <div><p class="caps">资源</p><ul><li>…</li></ul></div>
</footer>
```

```css
.foot-index { display: grid; grid-template-columns: repeat(3, 1fr);
  gap: var(--space-xl); padding: var(--space-2xl) var(--page-gutter); }
.foot-index .caps { font-variant-caps: all-small-caps;
  letter-spacing: 0.06em; margin-block-end: var(--space-sm); }
.foot-index ul { list-style: none; display: grid; gap: var(--space-2xs); }
```

折叠要点：<60rem 4 列 → 2 列；<40rem → 1 列，类目头保留（塌成手风琴亦可，头必须在）。

## 反模式

- 无真站点地图也铺四列——列是承诺：每条链接必须真实可达，死链接 = 伪造结构。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」——同类页脚连续两次构建相同即违规（总则 2）。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft3 · Index-style Category List）。
