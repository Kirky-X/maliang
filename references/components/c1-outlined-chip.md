# C1 · 描边 chip（Outlined Chip）

> 透明底、描边、排版动词（「保存更改」）的按钮。页面有一个主行动、想让它可见但不吵时用。

## 名称与形状

`inline-flex` 描边按钮：1px 墨线边框、无填充、动词文案。存在感来自边框与留白，不来自色块——与实心主按钮（[buttons.md](../vocabulary/buttons.md)）的分工：一页唯一实心位留给真正的主 CTA，本原型承担次级行动。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 形状 | 矩形 · 药丸（仅限tactile/俏皮调性）· 厚板块 |
| 密度 | 宽松 · 紧凑 |
| 装饰符 | 箭头 → · 加号 + · 无 |

## 何时用与勿混淆

- **何时用**：页面已有唯一实心主 CTA，本按钮做次级；或整页调性安静、CTA 不该喧哗。
- **勿混淆**：[C3 排版链接](c3-typographic-link.md)（无边无框纯文字）；实心 CTA（不同词汇，勿同位混用）。

## DOM+CSS 骨架

```html
<a class="cta-outline">打开你的工作室 →</a>
```

```css
.cta-outline { display: inline-flex; align-items: center; gap: 0.4em;
  padding: 0.7rem 1.2rem; border: 1px solid var(--color-ink);
  min-height: 44px; }
.cta-outline:hover { background: var(--color-ink); color: var(--color-paper); }
```

折叠要点：<60rem 不变（多枚 chips 自然换行）；<40rem 变全宽单枚、`min-height: 44px` 命中区不可退让（横切规则 5）。

## 反模式

- 页面出现第二、第三枚同等重量按钮——层级稀释；次级以下用 [C3](c3-typographic-link.md)。
- 药丸形状用在严肃/精密调性——药丸是俏皮调性专属旋钮值，错配读作廉价（[ai-tells.md](../meta/ai-tells.md)）。
- 跨产出照抄同组旋钮值（同形状 + 同装饰符）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id C1 · Outlined Chip）。
