# 表面海拔与深度体系（Elevation Ladder）

> 维度规范。把"层次"从感觉变为可执行配方：编号海拔阶梯 + 表面规则 + rgba 边框阶梯 + 深度策略唯一性。来源：interface-design Craft Foundations/Subtle Layering，2026-09 吸收；第五节阴影物理据 web-design-pascalorg 思想中文自研，2026-09 吸收。与 [`border.md`](border.md)（边框 vs 阴影的选择）、[`radius.md`](radius.md)（同心/嵌套圆角）配套。

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

## 五、阴影物理（多层软阴影配方）

> 本节数值为 web CSS（`box-shadow`）语境；ArkTS/Flutter 换算见节末。暗色界面不用阴影（靠第一节明度阶梯），本节配方用于亮色界面与 `subtle-shadows`/`layered` 策略。来源：web-design-pascalorg 思想中文自研，2026-09 吸收。

1. **统一光源方向**：全站阴影共享同一光源——默认正上方，阴影只向 y 正方向偏移（`offsetX` 恒为 0）；同页出现左飞一个、右飞一个的阴影即光源错乱，审计按 CRITICAL 级不一致处理。
2. **多层几何递增栈（2-5 层）**：单层阴影发平；把 2-5 层按几何倍数递增（offset 与 blur 逐层翻倍）叠出真实悬浮感。层级越高层数越多（卡片 2 层、弹层 4 层）：

   ```css
   /* 卡片：2 层 */
   box-shadow:
     0 1px 2px hsl(var(--shadow-hue) / 0.10),
     0 2px 4px hsl(var(--shadow-hue) / 0.10);
   /* 弹层：4 层 */
   box-shadow:
     0 1px 2px  hsl(var(--shadow-hue) / 0.07),
     0 2px 4px  hsl(var(--shadow-hue) / 0.07),
     0 4px 8px  hsl(var(--shadow-hue) / 0.07),
     0 8px 16px hsl(var(--shadow-hue) / 0.07);
   ```

3. **blur = 2 × offset**：每层 blur 取该层垂直偏移的 2 倍（y4 配 blur8、y8 配 blur16）。blur 远大于 offset 会虚成光晕，小于则成硬边——两条都是审计眼里的"阴影不对劲"。
4. **阴影着色禁纯黑**：纯黑/纯灰阴影发脏。用背景色的 hue 调成带色深色（蓝灰底配 `hsl(220 30% 12%)` 一类，而非 `#000`），透明度每层 0.06-0.12 起。与 [`meta/ai-tells.md`](../meta/ai-tells.md) "暗底堆黑阴影" Tell 同源——暗底上阴影本就不可见，堆了只剩渲染开销。
5. **禁直接动画多层阴影**：transition/animation 作用在 `box-shadow` 上会让每层逐帧重绘。两套阴影（静止/悬浮）分别放宿主元素与 `::after` 伪元素，只动画伪元素 `opacity`——opacity 走合成器，不触重绘。

**跨平台换算**：

- **Flutter**：`BoxShadow` 原生接受多层（`boxShadow: [BoxShadow(...), ...]`），逐层套本节配方（`blurRadius` = 2 × `offset.dy`）即可。
- **ArkTS**：`shadow()` 的 `ShadowOptions` 单次只描述一层；多层用同尺寸容器叠放近似，实际项目通常收敛为栈内等价单层（offset 取最深一层、radius 同步取大、颜色透明度合并调低），视觉误差在软阴影下可接受。

## 与其他规范联动

- [`meta/surface-modes.md`](../meta/surface-modes.md)：级联校准表"深度策略默认"行——Operate 默认 `borders-only` 或 `subtle-shadows`，Read 默认 `borders-only`，Persuade 默认 `subtle-shadows`，Experience 任一但全站唯一。
- [`meta/ai-tells.md`](../meta/ai-tells.md)：暗底上大量黑阴影不可见但仍堆叠 = 常见 AI 残留。
- 模板墙 `dark-oled`：纯黑底时 E1 起 +4% 即可显形（黑底阶梯更敏感）。
