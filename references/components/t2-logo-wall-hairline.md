# T2 · 发丝线 logo 墙（Logo Wall, Hairline）

> 一排单色客户 logo，发丝线分格。没有卡片盒，没有阴影——安静地列出「谁在用」。

## 名称与形状

`auto-fit` 网格铺开 logo，每格 `place-items: center`，格间右边框发丝线分隔；logo 统一 `grayscale(1)` + 70% 透明度压平。与 AI 默认的「6-logo 卡片盒网格」相反：本原型拒绝容器。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 布局 | 单行 · 两行 · 3×N 网格 |
| logo 处理 | 单色墨 · 品牌原色 · 幽灵淡显 |
| 分隔 | 发丝线分格 · 无 |

## 何时用与勿混淆

- **何时用**：有可识别的真实客户，且想安静地陈列。logo 必须取官方 SVG 资产——具名品牌资产协议见 [visual-assets.md](../meta/visual-assets.md)（拿不到官方 logo = 停下补齐，不画剪影顶替）。
- **勿混淆**：AI 默认的卡片盒 logo 墙（带盒带影——恰是本原型反对的形状）；[T4 数据条](t4-numbered-stat-strip.md)（数字，非标识）。

## DOM+CSS 骨架

```html
<section class="logo-wall">
  <ul>
    <li><img src="" alt="客户 A" /></li>
    <li><img src="" alt="客户 B" /></li>
  </ul>
</section>
```

```css
.logo-wall ul { display: grid;
  grid-template-columns: repeat(auto-fit, minmax(8rem, 1fr)); }
.logo-wall li { padding: var(--space-md);
  border-right: 1px solid var(--color-rule);
  display: grid; place-items: center; }
.logo-wall img { filter: grayscale(1); opacity: 0.7; }
```

折叠要点：<60rem 6 列 → 3 列；<40rem 3 列 → 2 列、logo 高度降档（32px → 24px）。

## 反模式

- logo 放进带阴影圆角的卡片里——盒化即背叛本原型；需要卡片感说明选错了原型。
- 无真实客户就放虚构 logo 墙——伪造社会证明比空白更伤（[data-floor.md](../meta/data-floor.md)）；没有就换 [T4](t4-numbered-stat-strip.md) 或留白。
- 跨产出照抄同组旋钮值（同布局 + 同处理）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id T2 · Logo Wall Hairline）。
