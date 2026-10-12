# F6 · 商品卡网格（Product Card Grid）

> 每卡一个商品：图 · 名 · 价 · 一个微动作。读作店面的货架，不是营销页。

## 名称与形状

等尺寸商品卡网格——**均匀是有意的**：节奏来自商品本身的图与名，不来自版式花样。卡内结构固定：媒体区（固定比例）+ 名称 + 价格（tabular 数字）+ 一个微动作。卖的是「物」，不是「特性」。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 卡比例 | 3/4 竖 · 1/1 方 · 4/3 横 |
| 密度 | 3 列 · 4 列 · 5 列 |
| 价格处理 | 名称下方 · 压图上 · hover 显现 |
| 微动作 | 加入 · 收藏 · 查看 → · 无 |

## 何时用与勿混淆

- **何时用**：电商、目录、lookbook、市集——一切「页面在卖东西」的场合。
- **勿混淆**：[F1 Bento](f1-bento-grid.md)（卖特性、瓦片跨度不均）。商品卡借 Bento 的不规则跨度 = 破坏货架语义。

## DOM+CSS 骨架

```html
<section class="product-grid">
  <article class="product">
    <a class="product__media" href=""><img src="" alt="" loading="lazy" /></a>
    <div class="product__meta">
      <h3 class="product__name">靛蓝亚麻围裙</h3>
      <p class="product__price tnum">¥ 148</p>
    </div>
  </article>
</section>
```

```css
.product-grid { display: grid; grid-template-columns: repeat(3, 1fr);
  gap: var(--space-xl) var(--space-lg); }
.product__media { display: block; aspect-ratio: 3 / 4; overflow: hidden;
  background: var(--color-paper-2); }
.product__media img { width: 100%; height: 100%; object-fit: cover;
  transition: transform var(--dur-long) var(--ease-out); }
.product__media:hover img { transform: scale(1.02); }
@media (max-width: 60rem) { .product-grid { grid-template-columns: repeat(2, 1fr); } }
```

折叠要点：<60rem 3 列 → 2 列；<40rem 2 列 → 1 列、卡高改弹性。hover 显现的微动作在触屏（`pointer: coarse`）必须恒显，否则功能不可达；可点目标满足总则 5（44px）。

## 反模式

- 借 Bento 不规则跨度——商品要均匀节奏。
- 商品名下挂两行特性描述——价格就是描述；描述膨胀读作营销页。
- 空闲时图片自走缩放动画——只在 hover 动，且 ≤1.02×。
- 容器信号叠满（阴影+圆角+描边+缎带全上）——按容器从轻序只取一种(仅间距 → 单分隔线 → 描边 → 卡片;canonical 见 meta/principles.md「分隔线根因与容器从轻序」)。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id F6 · Product Card Grid）。
