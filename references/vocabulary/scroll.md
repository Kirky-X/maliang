# 滚动模式命名词汇

> 模式词汇库。滚动是页面交互的基础,本表标准化滚动相关动效与行为命名。来源:taste-skill。

## 命名表

| 模式名                  | 视觉特征                                        | 适用场景                              |
| ----------------------- | ----------------------------------------------- | ------------------------------------- |
| `scroll-native`         | 原生滚动,无干预                                | 默认,大多数页面                      |
| `scroll-smooth`         | `scroll-behavior: smooth`                       | 锚点跳转、回到顶部                    |
| `scroll-infinite`       | 滚动到底自动加载                                | Feed 流、列表、社交社区               |
| `scroll-pull-refresh`   | 下拉刷新                                        | 移动 App、Feed                        |
| `scroll-snap`           | 滚动吸附(横向 / 纵向)                         | 轮播、Tab 切换、全屏叙事              |
| `scroll-parallax`       | 多层视差(背景 / 中景 / 前景速率不同)          | 品牌叙事、产品发布                    |
| `scroll-pinned`         | 元素 pin 在视口(配合 sticky-stack 骨架)        | 章节堆叠、产品功能展示                |
| `scroll-horizontal`     | 垂直滚动驱动横向位移(配合 horizontal-pan 骨架) | 品牌站、作品集、时间线                |
| `scroll-reveal`         | 进入视口揭示(配合 scroll-reveal-stagger 骨架) | 默认推荐,主流消费 App                |
| `scroll-progress`       | 顶部 / 侧边进度条                               | 长文章、教程、流程页                  |
| `scroll-driven-anim`    | 滚动驱动动画(数字 / 图表)                     | 数据展示、产品发布                    |
| `scroll-virtualized`    | 长列表虚拟滚动                                  | 表格 > 100 行、IM 消息列表            |

## 使用规则

- MOTION_INTENSITY ≥ 7 才能用 `scroll-parallax` / `scroll-pinned` / `scroll-horizontal`(见 [`dials.md`](../meta/dials.md))
- 所有非原生滚动必须实现 `prefers-reduced-motion` 降级到 `scroll-native`(见 [`accessibility.md`](../meta/accessibility.md))
- `scroll-infinite` 必须有 loading skeleton 与"已加载全部"终止态
- `scroll-virtualized` 用于列表 > 100 项,见 [`performance.md`](../meta/performance.md) DOM Cost
- 单页滚动模式 ≤ 2 种组合(如 `scroll-reveal` + `scroll-progress`)

## 在 draw-md 中的写法

```markdown
## Scroll Behavior
- mode: scroll-reveal
- reveal: { pattern: scroll-reveal-stagger, direction: up, stagger: 80ms }
- progress: scroll-progress (top, 4px height, color: color-brand)
- reduced_motion_fallback: scroll-native
```
