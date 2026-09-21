# 数字动效模式命名词汇

> 模式词汇库。数字变化的动态表达命名:数字是界面中最敏感的元素,变化的"方式"传达变化的"来源"。来源:UI 交互教学视频转录提取(2026-09,叨叨AI/西瓜同学);与 [`micro-interactions.md`](micro-interactions.md) `scroll-driven-anim`、[`charts.md`](charts.md) 联动。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `num-ticker-partial` | 局部滚动计数:只让变化的位滚动翻过,未变的位原地不动;缓停不急刹 | 价格变化、统计刷新、配置联动 |
| `num-ticker-onview` | 进入视口从 0 滚到当前值:与图表画线同步,缓出收尾 | 首屏 KPI 卡、年度报告(与 [`charts.md`](charts.md) `chart-ring-draw` 联动) |
| `num-badge-flip` | 角标数字位移翻动:9→10 带位移翻过去,不直接替换文字 | 未读数、购物车数量、库存变化 |
| `badge-chain-decrement` | 红点三级连锁减数:处理一条,分组角标与顶部汇总一起减 | 邮件/消息中心的多层级未读 |
| `stat-pill-expand` | 摘要胶囊下拉展开统计面板:收起为一行关键数胶囊,下拉跟手撑开成完整面板;下方内容下移压暗 | 列表页顶部统计(跑步汇总、账单汇总) |
| `num-slot-reveal` | 位数槽显隐:数值位数变化时空位淡入淡出,不跳动占位 | 金额从 99→128 等位数增减 |

## 使用规则

- `num-ticker-partial` 只动变化的位是铁律:整串重滚会掩盖"哪里变了"(与筛选联动时尤其关键)
- 滚动时长 ≤ 400ms,缓出收尾(`ease-out-soft`),禁止急刹与回绕(9→10 禁止倒滚一圈)
- `num-badge-flip` 用位移+透明度翻转(99+ 封顶,超出不再动画)
- `badge-chain-decrement` 三级(条目→分组→汇总)必须在同一帧内联动更新,延迟 > 100ms 即失去"连锁"语义
- `stat-pill-expand` 展开跟手(进度绑手势),松手按速度/过半判定;下方内容压暗 40% 让焦点给面板
- 货币/大数场景先确定小数位与千分位格式再动画,禁止动画中途变格式
- 无障碍:数值变化必须 `aria-live="polite"` 播报最终值,动画只是视觉层(见 [`accessibility.md`](../meta/accessibility.md))
- 数字滚动动画属反馈类 ≤ 400ms;`num-ticker-onview` 属入场装饰 ≤ 600ms 且可跳过(见 [`micro-interactions.md`](micro-interactions.md) 分层口径)

## 在 draw-md 中的写法

```markdown
## Stat (cart-count)
- pattern: num-badge-flip
- cap: "99+", duration: 200ms, chain: [folder-badge, topbar-badge]

## KPI (daily-revenue)
- pattern: num-ticker-partial
- changed_digits_only: true, duration: 350ms, easing: ease-out-soft
- aria_live: polite
```
