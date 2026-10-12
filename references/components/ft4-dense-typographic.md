# Ft4 · 密集版权页页脚（Dense Typographic / Colophon）

> 一大块小号 mono 文本：版本 · 构建 · 引用字体 · 许可 · 地址，两端对齐或右缘参差。书籍版权页（colophon）的能量。

## 名称与形状

一整块密集文字收尾，像技术书籍的 colophon：把「这页用什么做的」如实交代（字体、版本、许可、构建哈希）。mono 小字是它的制服——信息密度即风格。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 字族 | mono · 衬线 · 无衬线 |
| 排布 | 单块 · 多段落 · 日志式 |
| 收录项 | 构建哈希 · 日期 · 署名（至少含其一） |

## 何时用与勿混淆

- **何时用**：品牌偏编辑/技术写作，colophon 式收尾成立；开发者工具、文字工具。
- **勿混淆**：[Ft3 索引列](ft3-index-style-category-list.md)（导航用，本原型不导航）；[Ft2 单行内联](ft2-inline-rule-single-line.md)（一行，非一整块）。terminal 题材的默认页脚。

## DOM+CSS 骨架

```html
<footer class="foot-dense">
  <p>v0.2.0。字体 The Future、Fraunces、IBM Plex Mono。MIT 许可。
     2026 年于沿河路 137 号。</p>
</footer>
```

```css
.foot-dense { padding: var(--space-2xl) var(--page-gutter);
  font-family: var(--font-mono); font-size: var(--text-xs);
  line-height: 1.7; max-width: 72ch; }
```

折叠要点：<60rem 不变（mono 文本自然换行）、padding 收一档；<40rem 字号再降一档。

## 反模式

- 塞进格式化链接按钮或社交图标行——colophon 是纯文本档案；要导航换 [Ft3](ft3-index-style-category-list.md)。
- 版本/构建信息造假或过期——colophon 的唯一职责是真实；假哈希比没有更糟。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」——同类页脚连续两次构建相同即违规（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft4 · Dense Colophon）。
