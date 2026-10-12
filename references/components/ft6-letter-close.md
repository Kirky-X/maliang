# Ft6 · 书信落款页脚（Letter Close）

> 像信一样收尾：「此致，工作室。2026。」下方可带一行附言。把整页当一篇文字来收。

## 名称与形状

落款结构：斜体「此致，」+ 正体署名，可选一行 P.S.（附言，常放联系邮箱）。`max-width: 60ch` 的窄栏，与 [H5 书信开场](h5-letter-hero.md) 首尾成对时最有力量。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 落款样式 | 斜体 · 正体 · 缩写花押 |
| 附言 | 有 · 无 |
| 栏宽 | 40ch · 60ch · 80ch |

## 何时用与勿混淆

- **何时用**：页面声音温暖、手写感、编辑安静——个人站、工作室、与 H5 配对。
- **勿混淆**：[Ft1 报头式](ft1-mast-headed.md)（字标锚点，非落款）；数据主导/B2B 页面禁用——落款腔在那些页读作「装」。

## DOM+CSS 骨架

```html
<footer class="foot-letter">
  <p class="close">此致，<br><span class="sign">— 工作室</span></p>
  <p class="ps muted">P.S. — 回信欢迎：<a href="mailto:hi@studio">hi@studio</a>。</p>
</footer>
```

```css
.foot-letter { padding: var(--space-2xl) var(--page-gutter); max-width: 60ch; }
.foot-letter .close { font-style: italic; font-size: var(--text-lg);
  line-height: 1.4; }
.foot-letter .sign { font-style: normal; font-weight: 600; }
.foot-letter .ps { font-size: var(--text-sm); margin-top: var(--space-md); }
```

折叠要点：<60rem 单列不变、附言自然换行；<40rem 落款字号降一档、附言未斜体的保持不斜（中文语境一律不依赖斜体，见 [font.md](../dimensions/font.md)）。

## 反模式

- 数据主导/统计型页面用书信落款——声音错位读作 twee；跨产出照抄同组旋钮值 = 同款。
- 与 [H5](h5-letter-hero.md) 配对时署名不一致（开场自称 A、落款签 B）——首尾必须同人同称。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」——同类页脚连续两次构建相同即违规（总则 2）。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft6 · Letter Close）。
