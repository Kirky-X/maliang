# Ft5 · 宣言句页脚（Statement）

> 一句 display 大字统治页脚——是收束的结语，不是站点地图。字标、少量链接、版权压在下面的小字里。

## 名称与形状

页脚的主角是一句话（与页面论证呼应的 closing line），`clamp(1.75rem, 5vw, 3.25rem)`、`max-width: 28ch`；下方一条发丝线，字标与版权分列两端。Stripe（旧版）、Mailchimp（改版前）、代理公司作品集的收尾法。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 句宽 | 28ch · 38ch · 50ch |
| 字标位置 | 句下方 · 右上 · 无 |
| 元信息上缘线 | 发丝线 · 双线 · 无 |

## 何时用与勿混淆

- **何时用**：页面需要一句「结语」——编辑型、宣言型、氛围型。句子必须与该页的论证呼应，不是口号转储。
- **勿混淆**：[Ft1 报头式](ft1-mast-headed.md)（字标先行，非句子）；[Ft3 索引列](ft3-index-style-category-list.md)（导航用）。氛围题材的默认页脚。

## DOM+CSS 骨架

```html
<footer class="foot-stmt">
  <p class="foot-stmt__line">做一件被人记住的东西。</p>
  <div class="foot-stmt__meta">
    <span class="wordmark">工作室</span>
    <span class="muted">© 2026 · MIT</span>
  </div>
</footer>
```

```css
.foot-stmt { padding: var(--space-2xl) var(--page-gutter) var(--space-xl);
  display: grid; gap: var(--space-lg); }
.foot-stmt__line { font-size: clamp(1.75rem, 5vw, 3.25rem);
  line-height: 1.0; letter-spacing: -0.02em; max-width: 28ch; }
.foot-stmt__meta { display: flex; justify-content: space-between;
  align-items: baseline; padding-block-start: var(--space-sm);
  border-top: 1px solid var(--color-rule); }
```

折叠要点：<60rem 句子保持全宽、元信息行堆叠；<40rem 句子 clamp 下限抬高一档（再缩一档）、元信息换行。

## 反模式

- 文档根/枢纽页用宣言句——在那儿读作营销噪音，默认 [Ft3](ft3-index-style-category-list.md)。
- 巨大字标 + `auto 1fr 1fr 1fr` 元信息网格贴下——「同一副巨尾件」是最伤的共享尾件（见 [templates/README.md](../templates/README.md) 共享尾件轮换表）；写页脚前声明「上一构建页脚：X。本构建：Y，因为 Z」。
- 跨产出照抄同组旋钮值（同句宽 + 同字标位）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft5 · Statement）。
