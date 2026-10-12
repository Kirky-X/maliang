# C4 · 粘性底栏（Sticky Bottom Bar）

> 钉在视口底部的横条：一枚 CTA + 一句安心话。长页面上行动永远够得着。

## 名称与形状

`position: fixed` 底部通栏：左侧一句 reassurance（「免费试 14 天，无需绑卡」），右侧一枚 CTA。上缘一条发丝线与内容分隔。它是**常驻元素**，不是 hero CTA——勿与首屏行动混淆。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 显现时机 | 始终 · 上滚时 · 过首屏后 |
| 锚定 | 视口底 · 视口顶 · 行内落底 |
| 阴影 | 发丝线 · 无 · 轻阴影 |

## 何时用与勿混淆

- **何时用**：页面长、CTA 需要随时可达；移动端长落地页。
- **勿混淆**：[C1 描边 chip](c1-outlined-chip.md)（文档流内的次级按钮）；[N2 浮动角标](n2-floating-chip.md)（角落小块，非全宽通栏）。

## DOM+CSS 骨架

```html
<aside class="cta-sticky">
  <span>免费试 14 天。</span>
  <a class="cta-outline">开始 →</a>
</aside>
```

```css
.cta-sticky { position: fixed; left: 0; right: 0; bottom: 0;
  padding: var(--space-sm) var(--space-md); background: var(--color-paper);
  border-top: 1px solid var(--color-rule);
  display: flex; justify-content: space-between; align-items: center;
  min-height: 44px; }
```

折叠要点：<60rem 已为窄屏设计，无需处理；<40rem 文案可截断、CTA 保持右对齐、整条 ≥44px 命中区（横切规则 5）。页面底部留出等高 padding，防遮住页脚最后一行。

## 反模式

- 过首屏就弹出、遮住正在读的内容——显现时机是旋钮，「立即弹」是最差值；移动端弹出物纪律见 [mobile-floor.md](../meta/mobile-floor.md)。
- 底栏塞两个以上动作——一栏一主行动；安心话不算动作。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id C4 · Sticky Bottom Bar）。
