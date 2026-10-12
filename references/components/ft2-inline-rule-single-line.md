# Ft2 · 单行内联页脚（Inline Rule Single Line）

> 一行版权 · 地址 · 许可，上压一条发丝线。没有分栏。页脚是「事后想起」的编辑型页面用它。

## 名称与形状

最省的页脚：一条 hairline + 一行小字。全部元信息（版权、地址、许可）排在一行内，用中点分隔。没有字标阵、没有链接列——页面的结束就是一个句号。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 顺序 | 字标/链接/许可 · 许可/字标/链接 |
| 分隔符 | 中点 · 竖线 · 长破折 · 细竖线 |
| 密度 | 紧凑 · 疏朗 |

## 何时用与勿混淆

- **何时用**：编辑型页面、页脚本就是事后之事；单页站、文章页。
- **勿混淆**：[Ft4 密集版权页](ft4-dense-typographic.md)（一大块多信息 mono 文本）；[Ft1 报头式](ft1-mast-headed.md)（有字标横带）。

## DOM+CSS 骨架

```html
<footer class="foot-line">
  <p>© 2026 · 沿河路 137 号 · MIT 许可</p>
</footer>
```

```css
.foot-line { border-top: 1px solid var(--color-rule);
  padding: var(--space-md) var(--page-gutter); }
.foot-line p { font-size: var(--text-sm); color: var(--color-ink-2); }
```

折叠要点：<60rem 内容多时折成多行、分隔符换成软回车（行尾分隔符去掉）；<40rem 退化为纵向列表。

## 反模式

- 一行塞进全部站点链接——装不下就换 [Ft3](ft3-index-style-category-list.md)（真枢纽才配它）或 [Ft1](ft1-mast-headed.md)。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」——同类页脚连续两次构建相同即违规（总则 2）。
- 跨产出照抄同组旋钮值（同顺序 + 同分隔符）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft2 · Inline Rule Single Line）。
