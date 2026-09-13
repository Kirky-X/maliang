# 卡片模式命名词汇

> 模式词汇库。卡片是 UI 中最通用的容器组件,本表标准化其变体命名。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `card-basic`          | 标题 + 描述,无图                                 | 功能介绍、简单列表                    |
| `card-media-top`      | 顶部图 + 下方文案                                 | 博客文章、商品卡、案例展示            |
| `card-media-left`     | 左图 + 右文(水平)                              | 列表项、搜索结果、商品列表            |
| `card-media-bg`       | 背景图 + 浮层文字                                 | 类目入口、IP 展示、活动卡             |
| `card-action`         | 含 CTA 按钮                                       | 商品卡(加购)、服务卡(预约)         |
| `card-collapsible`    | 可折叠(点击展开)                                | FAQ、设置项、详情展开                 |
| `card-glass`          | 玻璃质感(见 [`glass-effect.md`](../dimensions/glass-effect.md)) | 浮动 dock、模态浮层 |
| `card-shadowed`       | 强阴影悬浮                                        | Tooltip 卡、下拉菜单                  |
| `card-bordered`       | 仅 border 无阴影                                  | 列表项、表格行替代                    |
| `card-tinted`         | 浅色背景 tint(非白)                             | 高亮项、选中态、分组                  |
| `card-skeleton`       | 加载占位骨架                                      | Loading 状态(见 [`principles.md`](../meta/principles.md) 第 14 定律) |
| `card-empty`          | 空状态卡(插画 + 文案 + CTA)                     | 空列表(见 [`principles.md`](../meta/principles.md) 第 14 定律) |
| `card-double-bezel`   | 双层嵌套容器:外壳 `bg-*/5` + ring 发丝边 + `p-1.5` + 大圆角,内核独立底色 + 内高光 + 同心圆角 `calc(外圆角 - 0.375rem)` | 高级感工艺卡、设置组、统计卡(来源:taste-skill soft-skill) |
| `card-tilt-depth`     | 卡片层深 tilt:0.4 / 1.0 / 1.6 三档层深,hover 视差(层移/旋转参数详见 [buttons.md](buttons.md)) | 精品内容卡、作品集、封面卡(来源:视频研究 v07) |
| `card-stat`           | 数值卡:大数值 + 标签 + delta 涨跌,数字用等宽数字(tabular-nums) | KPI 概览、仪表盘指标卡(样式基准见 [data-dense-dashboard](../templates/data-dense-dashboard.md) 模板) |

> 来源注:`card-stat` 为**审计补全**(2026-09-08 组件覆盖审计):对照 Ant Design Statistic 组件清单(IBM Carbon / Material 3 无独立对应,由卡片组合);键值对详情展示归 [tables.md](tables.md) `table-descriptions`。

## 使用规则

- 同一页面卡片变体 ≤ 3 种(避免混乱)
- 卡片间距统一(用 spacing-md 或 spacing-lg,不混用)
- 卡片圆角按 [`radius.md`](../dimensions/radius.md) 分档,容器 > 控件
- 触发 [`ai-tells.md`](../meta/ai-tells.md) "全场 rounded-2xl" 时,差异化圆角
- 等高三列卡片网格禁用(见 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节),改 bento 或非对称

## 在 draw-md 中的写法

```markdown
## Card (product-card)
- pattern: card-media-top
- media: { image: product.jpg, ratio: 4:3 }
- title: { typography: font-size-title-md, max_lines: 2 }
- meta: { typography: font-size-label-sm, color: color-text-secondary }
- price: { typography: font-size-display-md, color: color-brand }
- action: { type: button-primary, label: "加入购物车" }
- states: [default, hover-lift, pressed-scale]
```
