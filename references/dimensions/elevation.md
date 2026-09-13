# 表面海拔与深度体系（Elevation Ladder）

> 维度规范。把"层次"从感觉变为可执行配方：编号海拔阶梯 + 表面规则 + rgba 边框阶梯 + 深度策略唯一性。来源：interface-design Craft Foundations/Subtle Layering，2026-09 吸收。与 [`border.md`](border.md)（边框 vs 阴影的选择）、`radius.md`（同心圆角）配套。

## 一、海拔阶梯（暗色表面）

暗色界面不靠阴影靠**明度阶梯**——每级只比上一级亮几个百分点，叠起来才显形：

| 级 | 表面 | 明度规则 | 示例 |
| --- | --- | --- | --- |
| E0 | 页面画布 base | 基准（如 #0a0a0c） | 页面背景 |
| E1 | 卡片 / 面板 | base 亮度 **+7%** | 列表卡、图表容器 |
| E2 | 浮出面板（dropdown/popover 父级） | **+9%** | 筛选面板 |
| E3 | 弹层（modal / popover / toast） | **+12%** | 模态、菜单 |
| — | 输入框 | 比周围表面**更深**（inset 隐喻"在此输入"） | 输入/文本域 |

亮色界面用同构的"白阶"（base → +4% 白 → +8% 白）或 1px 边框 + 软阴影（见 border.md）。

## 二、表面规则

1. **侧栏与画布同底色**：用细边框（1px rgba）分隔，禁止"侧栏一个世界、内容一个世界"的割裂感；例外：强分区需求（如导航 rail）用 E1。
2. **输入框比周围深**：`background` 比所在面板低一档明度（暗色）或加 `inset` 阴影（亮色）；"输入 = 凹陷"是物理隐喻，放之四海皆准。
3. **popover 恒为父表面上一层**：popover 永远比触发它的表面高一级；两级弹层叠加时逐级递增，禁止同级。
4. **弹层投影**（亮色）：三层配方——1px ring（中性 8%）+ 近距软影（y2 blur8 8%）+ 远距软影（y16 blur32 12%）；暗色塌缩为单 ring（暗底上深度阴影不可见）。

## 三、rgba 边框阶梯（替代实色 hex 边框）

| 用途 | 暗色 | 亮色 |
| --- | --- | --- |
| 同色表面分隔 | `rgba(255,255,255,.06)` | `rgba(0,0,0,.06)` |
| 卡片边界 | `rgba(255,255,255,.10)` | `rgba(0,0,0,.10)` |
| 强调边界（hover/focus） | `rgba(255,255,255,.12~.16)` | `rgba(0,0,0,.12~.16)` |

实色 hex 边框（`#333`、`#e5e5e5`）在底色变化时无法自适应，优先改 rgba 阶梯。与 [`border.md`](border.md) 的分工：border.md 管"边框 vs 阴影怎么选"，本文管"所选策略内怎么取值"；`borders-only` 策略下卡片以边框为界、不叠装饰阴影（此时边框取值按本表 rgba 阶梯）。

## 四、深度策略四选一（全站唯一）

| 策略 | 手法 | 适用 |
| --- | --- | --- |
| `borders-only` | 只用边框，零阴影 | 密集后台、表格、Read 模式 |
| `subtle-shadows` | 软阴影 + 微边框 | 大多数 SaaS / 消费页 |
| `layered` | 明度阶梯为主 + 阴影为辅 | 暗色产品、仪表盘 |
| `tint-shift` | 色彩深浅代替明暗 | 品牌感强、彩色底产品 |

**同一项目 DESIGN.md 只声明一种深度策略**（脚本暂未覆盖，列为 preview 人工复核项）。

## 与其他规范联动

- [`meta/surface-modes.md`](../meta/surface-modes.md)：级联校准表"深度策略默认"行——Operate 默认 `borders-only` 或 `subtle-shadows`，Read 默认 `borders-only`，Persuade 默认 `subtle-shadows`，Experience 任一但全站唯一。
- [`meta/ai-tells.md`](../meta/ai-tells.md)：暗底上大量黑阴影不可见但仍堆叠 = 常见 AI 残留。
- 模板墙 `dark-oled`：纯黑底时 E1 起 +4% 即可显形（黑底阶梯更敏感）。
