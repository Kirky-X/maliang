# 进度与确认模式命名词汇

> 模式词汇库。用"过程感"替代二次确认弹窗与干瘪进度条的模式命名:进度可视化融进组件本体,确认动作带阈值与回弹。来源:UI 交互教学视频转录提取(2026-09,叨叨AI/西瓜同学),与 [`micro-interactions.md`](micro-interactions.md)、[`popups.md`](popups.md) 互补。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `progress-fill-bg` | 组件背景填充宽度即进度:勾选一项底色前推一段,完成时整卡轻微提亮 | 清单勾选、表单分组完成度、多步任务 |
| `confirm-slide-bar` | 滑动确认条:滑过 80% 阈值触发,不足弹回起点 | 删除、支付等破坏性/重要操作(移动端) |
| `confirm-hold-ring` | 按住确认时间环:环形进度沿边缘走满才执行,中途松手环退回 | 删除、清空、退出登录等低频高危操作 |
| `progress-segmented` | 分段进度条:Stories 式分段自动走,按住暂停,点左右半区切上/下一项 | 图集浏览、引导页、快看内容流 |
| `progress-timeline-card` | 进度时间线卡:节点三态(完成/当前/未到),当前节点高亮并展开详情 | 物流跟踪、审批流、订单状态 |
| `step-overshoot` | 步骤条超调回弹:完成一步进度先冲过一点再收回,像用力走完 | 多步向导完成反馈(MOTION ≥ 6) |
| `undo-toast-countdown` | 撤销倒计时进度化:撤销剩余时间做成 toast 内嵌进度条,走完即消失 | 删除后撤销、发送后撤回 |

## 使用规则

- 破坏性操作二选一:`confirm-slide-bar`(移动端)或 `confirm-hold-ring`(沉浸/全屏场景);不再叠加二次确认弹窗(双重确认是负担)
- `confirm-slide-bar` 阈值固定 80%,不足弹回必须带回弹缓动(`ease-spring`,过冲 ≤ 1.2)
- `confirm-hold-ring` 时长 600-1000ms;环走满与执行之间不允许额外等待
- `progress-fill-bg` 的填充必须用 `transform: scaleX` 或 width 单属性过渡,完成提亮 ≤ 150ms(见 [`micro-interactions.md`](micro-interactions.md) 时长预算)
- `undo-toast-countdown` 走完消失前 200ms 不再响应撤销点击(防误触已失效操作)
- 所有确认控件必须可被键盘/读屏替代完成(`confirm-hold-ring` 提供"按 Enter 持续 1s 或直接二次确认"替代路径,见 [`accessibility.md`](../meta/accessibility.md))
- 图表内的进度/目标表达(可拖动目标线、环形入场画线)见 [`charts.md`](charts.md) 的可交互图表条目

## 在 draw-md 中的写法

```markdown
## Confirm (delete-account)
- pattern: confirm-hold-ring
- duration: 800ms, ring: edge-trace, cancel: release-retract
- a11y_alt: press-enter-1s | double-confirm

## Checklist (setup-tasks)
- pattern: progress-fill-bg
- fill: scaleX-transition, complete-glint: 150ms
```
