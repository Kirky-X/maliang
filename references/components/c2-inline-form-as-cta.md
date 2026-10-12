# C2 · 行内表单即 CTA（Inline Form-as-CTA）

> CTA 本身就是表单：一个邮箱输入 + 旁边「提交 →」。不用单独落地页收邮箱。

## 名称与形状

`grid: 1fr auto` 的输入行：无边框输入框压在一条底线上，提交按钮贴右。行动与表单合一，减少一跳。label 以视觉隐藏方式保留可访问性。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 字段数 | 1 · 2 · 3 |
| 提交位 | 行尾 · 独立行 · 内嵌按钮 |
| 辅助文案 | 上方 · 下方 · 无 |

## 何时用与勿混淆

- **何时用**：动作就是收一个邮箱（订阅、候补名单）；别让用户再跳一页。
- **勿混淆**：[C1 描边 chip](c1-outlined-chip.md)（导航型动作，非提交型）；[Ft7 订阅优先页脚](ft7-newsletter-first.md)（同一表单住页脚主角位——同页两处不得都用订阅表单当主角）。

## DOM+CSS 骨架

```html
<form class="cta-form">
  <label for="email" class="visually-hidden">邮箱</label>
  <input id="email" type="email" placeholder="you@example.com" />
  <button type="submit">发送 →</button>
</form>
```

```css
.cta-form { display: grid; grid-template-columns: 1fr auto;
  border-bottom: 1px solid var(--color-ink); }
.cta-form input { background: none; border: 0; padding: 0.7rem 0;
  min-height: 44px; }
```

折叠要点：<60rem 输入与按钮纵向堆叠、各自全宽；<40rem label 移到输入上方显式可见、按钮全宽落底——堆叠后仍保 44px 命中区（横切规则 5）。

## 反模式

- 砍掉 label 只留 placeholder——placeholder 在输入后消失且对比度常不达标（[accessibility.md](../meta/accessibility.md)）；视觉可省，语义 label 不可省。
- 提交按钮 `<div>` 顶替——表单语义完整性（Enter 提交、校验反馈）随语义元素一起消失。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id C2 · Inline Form-as-CTA）。
