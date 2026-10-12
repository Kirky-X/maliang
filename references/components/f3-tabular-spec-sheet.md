# F3 · 规格表（Tabular Spec Sheet）

> 每行一个特性：名称、值、脚注三列，发丝线分行，数字一律 tabular。特性可以定量比较时的讲法。

## 名称与形状

真表格语义（`<table>` 或 dl 列表）：行是特性，列是字段，行间发丝线。数值用 `tabular-nums` 保证纵向可对位。最诚实的特性区——没有卡片、没有图标，只有数据。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 列数 | 2（名/值）· 3（名/值/单位）· 4（加脚注） |
| 分线密度 | 每行 · 每 3 行分组 · 只留表头线 |
| 数字 | tabular · 比例字宽 |

## 何时用与勿混淆

- **何时用**：特性之间可以量化比较；技术规格、定价参数、性能数据。数值必须真实可溯（[data-floor.md](../meta/data-floor.md)）。
- **勿混淆**：[F1 Bento](f1-bento-grid.md)（非表格、视觉节奏主导）；[T4 编号数据条](t4-numbered-stat-strip.md)（3-5 个指标横排，非逐行清单）。

## DOM+CSS 骨架

```html
<table class="spec-sheet tnum">
  <tr><th>延迟</th><td>p99 &lt; 50 ms</td><td class="muted">外部实测</td></tr>
  <tr><th>可用性</th><td>99.97%</td><td class="muted">过去 12 个月</td></tr>
</table>
```

```css
.spec-sheet { width: 100%; border-collapse: collapse; }
.spec-sheet td, .spec-sheet th { padding-block: var(--space-sm);
  border-bottom: 1px solid var(--color-rule); text-align: left; }
.spec-sheet .tnum, .tnum td { font-variant-numeric: tabular-nums; }
```

折叠要点：<60rem 列数收敛：4 列 → 2 列（名 + 值），单位与脚注并入值列括注；<40rem 转纵向定义列表，每行 `dt` 在上 `dd` 在下。

## 反模式

- 拿装饰性表格格式硬凑（隔行变色 + 斑马纹 + 竖线全套）——本原型的语言是发丝线 + 留白，装饰叠加读作后台导出（[visual-symptoms.md](../meta/visual-symptoms.md)「数据库导出」病灶）。
- 数据列用比例字宽导致小数点不对位——数值列必须 tabular。
- 跨产出照抄同组旋钮值 = 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id F3 · Tabular Spec Sheet）。
