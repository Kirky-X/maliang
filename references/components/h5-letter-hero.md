# H5 · 书信开场（Letter Hero）

> 第一人称开场：「致读者，」。首屏无按钮，读起来像私人信件而非营销页。

## 名称与形状

首屏是一封信的称呼 + 开头一两段正文。没有 display 大字轰炸，靠字号适中的正文排版与称呼建立「人对人」的语气。署名在页尾由 [Ft6 书信落款](ft6-letter-close.md) 接住，首尾成对。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 称呼 | 问候语 · 「致 X，」 · 时间戳 |
| 正文长度 | 1 段 · 2 段 · 3 段 |
| 落款样式 | 键入姓名 · 手绘签名 SVG · 缩写 |

## 何时用与勿混淆

- **何时用**：创始人/作者的声音就是品牌；个人站、工作室、独立产品 changelog。
- **勿混淆**：[H1 跑马灯宣言](h1-marquee.md)（非人称的宣言）；[H3 引言主导](h3-quote-led.md)（他人评价，非自述）。

## DOM+CSS 骨架

```html
<section class="hero-letter">
  <p class="salutation"><em>致读者，</em></p>
  <p class="lede">…</p>
</section>
```

```css
.hero-letter { min-height: 70dvh; display: grid; align-content: center;
  gap: var(--space-md); max-width: 60ch; padding: 0 var(--page-gutter); }
.salutation { font-style: italic; font-size: var(--text-lg); }
```

折叠要点：<60rem 保持单列；如有侧栏移到正文下方、分隔改为顶边框；<40rem 称呼字号降一档、落款收紧。

## 反模式

- 首屏塞 CTA——书信语气里按钮一出现就穿帮；行动留给后续区段或 [C3 排版链接](c3-typographic-link.md)。
- 中文页面用 `<em>` 斜体当强调——中文无真斜体，称呼的语气改用字重或引号处理（[font.md](../dimensions/font.md)）。
- 书信腔配 B2B 产品页——气质错位读作「装」；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H5 · Letter Hero）。
