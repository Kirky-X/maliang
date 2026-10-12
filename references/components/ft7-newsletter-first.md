# Ft7 · 订阅优先页脚（Newsletter-first）

> 订阅表单（label + 输入 + 提交）是页脚的**主角**；字标、链接、版权全部收成 12px 弱化小字垫底。

## 名称与形状

页脚反转：表单占主位（`max-width: 56ch` 窄栏），其余元信息退化为一行小字。Stratechery、Substack 形态的独立出版物页脚。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 布局 | 堆叠 · 行内 · 分栏（表单左·元信息右） |
| 提交样式 | 实心 · 描边 · 箭头链接 |
| 隐私行 | 有 · 无 |

## 何时用与勿混淆

- **何时用**：品牌真的持续出版，且**首屏以上已经出现过订阅邀约**——页脚是最后一次邀请，不是伏击。
- **勿混淆**：[C2 行内表单 CTA](c2-inline-form-as-cta.md)（表单住在页面行动位）；[Ft1](ft1-mast-headed.md)（不索取任何东西的页脚）。同页 C2 与 Ft7 不得都是订阅表单。

## DOM+CSS 骨架

```html
<footer class="foot-news">
  <form action="/subscribe" method="post">
    <label for="foot-email">工作室来信 · 每月一封</label>
    <div class="row">
      <input id="foot-email" name="email" type="email" required placeholder="you@domain">
      <button type="submit">订阅</button>
    </div>
  </form>
  <p class="meta muted">工作室 · © 2026 · <a href="/imprint">版权页</a></p>
</footer>
```

```css
.foot-news { padding: var(--space-2xl) var(--page-gutter);
  display: grid; gap: var(--space-lg); max-width: 56ch; }
.foot-news .row { display: flex; gap: var(--space-2xs); }
.foot-news input { flex: 1; min-height: 44px; padding-inline: var(--space-sm);
  border: 1px solid var(--color-rule); border-radius: var(--radius-input); }
.foot-news .meta { font-size: var(--text-xs); }
```

折叠要点：<60rem 输入与按钮纵向堆叠、各自全宽；<40rem label 移到输入上方、按钮全宽落底（44px 命中区，横切规则 5）。

## 反模式

- 首屏从未提订阅、页脚突然弹表单——伏击式索取；没邀约过就退到 [Ft2](ft2-inline-rule-single-line.md)。
- 表单之外的链接偷偷长大成四列矩阵——元信息必须保持小字身份；长出矩阵就换 [Ft3](ft3-index-style-category-list.md)。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft7 · Newsletter-first）。
