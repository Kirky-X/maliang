# F7 · KPI 指标卡阵列（Stat Card Grid）

> 2-6 张同构统计卡并排：图标·数值·限定语·delta，共基线等高。数据区不是营销区——均匀是纪律，不是凑数。

## 名称与形状

App/后台首屏的「今日概览」区：一排（窄屏两排）同构指标卡，每卡内部固定行槽——图标（定框）→ 数值（tabular）→ 限定语，可选 delta。卡与卡**等宽等高、对应行跨卡对齐**（判据见 [alignment.md](../dimensions/alignment.md)，门禁 G44）；这与 [T4 编号数据条](t4-numbered-stat-strip.md)的分野：T4 是无容器的轻条，本原型是带容器的卡片阵列，且必须过等高/行槽纪律。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 卡数 | 2 · 4 · 6 |
| 图标位 | 顶部独立行 · 数值左侧内联 · 无图标 |
| delta | 有（涨跌色按业务语义） · 无 |
| 容器 | 卡片底 · 仅分隔线 · 纯间距 |

## 何时用与勿混淆

- **何时用**：App / 后台首屏概览，指标 ≥2 且各有真实数据源（逐指标过 [data-floor.md](../meta/data-floor.md) 绑定表；数字必须经得起追问）。
- **勿混淆**：[T4 编号数据条](t4-numbered-stat-strip.md)（无容器的横排轻条，营销页证明区）；[F1 Bento](f1-bento-grid.md)（非对称瓦片，卖特性——数据阵列**禁止**借 Bento 的不对称，均匀是本原型的语义）；[F6 商品卡网格](f6-product-card-grid.md)（卖商品）。

## DOM+CSS 骨架

```html
<section class="stat-grid">
  <article class="kpi">
    <span class="glyph" aria-hidden="true"></span>
    <b class="tnum">128</b>
    <span class="label">今日订单</span>
  </article>
  <!-- ×N,同构重复 -->
</section>
```

```css
.stat-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-md); }
.kpi { display: grid; row-gap: var(--space-xs); padding: var(--space-md);
  border-radius: var(--radius-lg); }
.kpi .glyph { width: 2.5rem; height: 2.5rem; } /* 图标定框:禁内容天然高度决定行位 */
.kpi b { font-size: var(--text-2xl); font-variant-numeric: tabular-nums;
  line-height: var(--line-height-tight); }
```

折叠要点：<40rem 4 卡收 2×2、6 卡收 2×3；数值字号降一档；行槽关系不变（收拢后仍须等高共基线）。触控目标 ≥44px（总则 5）。

## 反模式

- **图标不定框**（`width: auto` / 直接放 SVG）——图标天然高度决定行位，第 2 行起全部错位，这是统计卡错位的第一根因（G44 / alignment.md 行槽）。
- 同排卡高不等（某卡 `align-self` 逃逸或内容溢出）——同构阵列必须等高（G44）。
- 凑数卡：没有真实数据源的指标硬凑满一排——过 data-floor，`—` + 待确认，不虚构（G29）。
- 卡数 >6 还硬挤一行——超过 6 转两排或换 [F3 规格表](f3-tabular-spec-sheet.md) 逐行讲。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

maliang 自研，2026-10（用户实测反馈「四宫格统计卡各列错位」驱动补建，配 alignment.md 关系型判据与 preview-lint `siblingRowMisalign` / `siblingUnequalSize` 探针）。
