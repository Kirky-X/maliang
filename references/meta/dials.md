# Three Dials 系统 —— DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY

> 规范层。三档可调标度,用于在 design-md 阶段表达"视觉强度档位",并驱动后续 draw-md / preview / draw-* 的取舍。来源:taste-skill。

每个 dial 取整数 1-10,1-3 / 4-7 / 8-10 分为三档行为定义。三档独立调节,不强制同步——例如可以做"高密度 + 低动效 + 中变化"的组合。档位写入 DESIGN.md 的 frontmatter 顶层 `dials:` 块,供下游子命令读取。

## 三个 Dial 的语义

| Dial              | 维度           | 低档(1-3)              | 中档(4-7)            | 高档(8-10)            |
| ----------------- | -------------- | ----------------------- | --------------------- | --------------------- |
| DESIGN_VARIANCE   | 视觉变化丰富度 | 严格网格,极少量变体    | 中等节奏,关键页变体  | 强对比,大量变体       |
| MOTION_INTENSITY  | 动效强度       | 仅状态过渡,无装饰动画  | 入场+滚动揭示         | 全动效(视差/物理曲线) |
| VISUAL_DENSITY    | 信息密度       | 大量留白,单焦点         | 平衡密度              | 紧凑信息,Dashboard 风 |

## DESIGN_VARIANCE(视觉变化丰富度)

### Level 1-3 · 极简一致

- 严格 8 列网格,跨页不变形
- 组件库仅 1 套按钮 / 卡片 / 列表变体
- 颜色仅 60-30-10 三色,无第三色相
- 圆角 / 字重 / 字号档位 ≤ 3 个
- **适用**:工具型 SaaS、企业后台、文档站、合规类金融页

### Level 4-7 · 中等节奏

- 关键页(首页/详情)允许 1-2 个变体
- 卡片支持 2 种圆角(如 md + lg)以区分层级
- 强调色 2 个(primary + tertiary)
- **适用**:大多数 C 端 App、营销站、电商详情页

### Level 8-10 · 强对比叙事

- 每个章节可有独立视觉处理
- 大量异形切割 / 重叠 / 非对称布局
- 多色相 + 渐变 + 纹理叠加
- **适用**:品牌站、艺术展类、潮流文化、IP 落地页

## MOTION_INTENSITY(动效强度)

### Level 1-3 · 仅状态过渡

- 只允许 hover / pressed / focus 的颜色与边框过渡(duration ≤ 150ms)
- 禁止入场动画 / 滚动揭示 / 视差
- **适用**:效率型工具、表单密集型后台、无障碍优先场景

### Level 4-7 · 入场 + 滚动揭示

- 入场 fade + 微 translate(≤ 12px,duration ≤ 400ms)
- 滚动触发的 stagger 揭示(间隔 ≤ 80ms)
- 列表项过渡用 ease-out,禁用 spring / bounce
- **适用**:主流消费 App、营销落地页、内容社区

### Level 8-10 · 全动效

- 视差滚动、pin sticky、横向平移
- 物理曲线(spring / elastic),配 GSAP / Lenis
- 数字 / 图表入场动画
- **强制**:`prefers-reduced-motion` 降级到 Level 1-3(见 [`accessibility.md`](./accessibility.md))
- **适用**:品牌站、作品集、产品发布页、3D 交互场景

## VISUAL_DENSITY(信息密度)

### Level 1-3 · 大量留白

- 单屏焦点 ≤ 2 个,行高 ≥ 1.7
- 卡片内 padding ≥ spacing-lg
- 字号档位 ≤ 3,大字主导
- **适用**:品牌首页、奢侈品、冥想 / 健康类、引导页

### Level 4-7 · 平衡密度

- 单屏 3-5 个信息块
- 行高 1.4-1.6
- 卡片 padding = spacing-md
- **适用**:大多数 C 端 App 默认值

### Level 8-10 · 紧凑信息

- Dashboard 风,行高 1.2-1.3
- 表格 / 列表密度优先,卡片 padding = spacing-sm
- 多列布局(3-4 列)可接受
- **适用**:数据后台、监控大屏、交易终端、B 端表单密集页

## 在 DESIGN.md 中的写法

```yaml
---
dials:
  design_variance: 5
  motion_intensity: 4
  visual_density: 6
---
```

下游 draw-md / preview 读取后,按档位自动调整:Level 4-7 的 MOTION 默认加入入场动画;Level 8-10 的 DENSITY 默认 3 列网格等。档位冲突时(如 Level 8 MOTION + 无障碍要求),按 [`rules-priority.md`](./rules-priority.md) 中 Accessibility > Animation 解决。

## 与其他规则的关系

- **三档非默认值**:不写 `dials:` 块时,默认全部取 4(中等档),由 draw-md 根据产品类型从 [`product-reasoning.md`](./product-reasoning.md) 推理覆盖
- **档位漂移**:跨页档位差异 > 3 档时(如首页 Level 8 + 详情页 Level 2),必须显式说明意图,否则视为不一致
- **降级触发**:`prefers-reduced-motion` 触发时,MOTION_INTENSITY 强制 ≤ 3;`prefers-contrast: more` 触发时,DESIGN_VARIANCE 强制 ≤ 4
