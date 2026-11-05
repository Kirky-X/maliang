# 进度与确认模式命名词汇

> 模式词汇库。用"过程感"替代二次确认弹窗与干瘪进度条的模式命名:进度可视化融进组件本体,确认动作带阈值与回弹,与 [`micro-interactions.md`](micro-interactions.md)、[`popups.md`](popups.md) 互补。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `progress-fill-bg` | 组件背景填充宽度即进度:勾选一项底色前推一段,完成时整卡轻微提亮 | 清单勾选、表单分组完成度、多步任务 |
| `confirm-slide-bar` | 滑动确认条:轨道渐进填充,滑过 80% 阈值触发,成功态滑块/箭头翻成对勾;不足弹回起点不执行 | 删除、支付等破坏性/重要操作(移动端) |
| `confirm-hold-ring` | 按住确认时间环:环形进度沿边缘走满才执行,中途松手环退回 | 删除、清空、退出登录等低频高危操作 |
| `checkin-hold-burst` | 长按打卡环:环从十二点方向按住填满,满格瞬间炸开收成一枚金属圆盘,对勾一笔画出;按住填满即执行、满格即收束(与 `confirm-hold-ring` 互见:彼条松手回退,用于高危确认;本条满格收束为完成庆祝),炸开粒子与 [`buttons.md`](buttons.md) `btn-burst` 同族 | 打卡/签到等完成型长按 |
| `progress-segmented` | 分段进度条:Stories 式分段自动走,按住暂停,点左右半区切上/下一项 | 图集浏览、引导页、快看内容流 |
| `progress-timeline-card` | 进度时间线卡:节点三态(完成/当前/未到),当前节点高亮并展开详情 | 物流跟踪、审批流、订单状态 |
| `route-reveal-progress` | 点「追踪」才展开:路线节点依次点亮绘制,再点收回(渐进披露,不为看一眼常驻整条路线);节点依次亮起属装饰档可跳过;与 `progress-timeline-card` 互见:彼条完整时间线常驻,本条按需展开 | 物流/行程追踪、路线预览 |
| `step-overshoot` | 步骤条超调回弹:完成一步进度先冲过一点再收回,像用力走完 | 多步向导完成反馈(MOTION ≥ 6) |
| `step-dot-checkline` | 步进完成四联动:当前圆点翻成对勾、连接线前段填充到位、下一点亮起、说明文字同步切换;四处同帧启动(联动不齐即像卡住);与 `progress-timeline-card` 互见:彼条节点三态静态呈现,本条完成一步的推进瞬间 | 多步向导、引导流程 |
| `undo-toast-countdown` | 撤销倒计时进度化:撤销剩余时间做成 toast 内嵌进度条,走完即消失 | 删除后撤销、发送后撤回 |
| `progress-save-ring` | 保存按钮变进度环:点击后文字收缩成圆形,边缘一圈环形进度走满,再撑开变回按钮,文字切成「打开」(与 [`sheet-drawer.md`](sheet-drawer.md) `button-submit-morph` 互见:本条环形绑定真实进度,彼条定时长转场+对勾收尾) | 上传/保存类按钮的提交全程反馈 |
| `progress-btn-bar-morph` | 按钮原地变进度条:背景从左向右填充,实时百分比跟着走,走满切成功态,短暂停留自动复位;同容器单值插值驱动宽度与百分比,复位前停留足供读出结果(与 `progress-save-ring` 互见:彼条环形+文字切「打开」,本条条形+自动复位) | 提交/上传等短任务按钮 |
| `upload-cards-converge` | 文件卡片依次向中间收拢汇入上传入口,进度走完显成功标记,随后卡片复原回原位;多文件聚合成一股进度,收拢错峰、复原不抢进度显示(与 `progress-save-ring` 互见:彼条按钮本体变进度,本条外部卡片汇入按钮) | 多文件上传/导入 |
| `focus-timer-ring` | 专注计时环:拖滑块定时长,圆环随倒计时收缩、中心数字联动递减,完成变绿显对勾后自动复位;毛玻璃变体完成瞬间补一圈光晕;滑块/环/数字三处同频联动,倒计时是驻留语义非转场时长(见文末注),完成变绿即状态切换 | 番茄钟、专注/休息计时 |
| `habit-week-ring-checkin` | 七日沿圆周排布的打卡环:当日节点打卡时变色并扩散一圈光圈,中心连续天数同步滚动,圆周路径逐日连续绘制,满周显对勾;打卡反馈属庆祝档可跳过;天数滚动见 [`number-motion.md`](number-motion.md) `num-ticker-partial`;与 `checkin-hold-burst` 互见:彼条单次打卡收束,本条整周推进 | 习惯打卡、连续签到、周目标 |
| `confirm-copy-tick` | 复制成功翻转:复制图标原地翻成对勾,上方冒出「已复制」小提示,约 1s 后一起复原 | 复制链接/代码/口令按钮 |
| `scrubber-waveform` | 波形进度条:整段内容压成一排竖条波形,已过部分高亮;按住拖动实时更新进度,松手从该位置继续播放 | 音频/视频/语音消息的进度控制(波形只动 transform) |

> 环形进度与「约 1s 后复原」为进度/驻留语义,非转场时长,draw-md 勿写 `duration: 1000ms` 类字面量(防检查 11 误报,先例同 [`micro-interactions.md`](micro-interactions.md) `micro-hold-confirm`)。

## 使用规则

- 破坏性操作二选一:`confirm-slide-bar`(移动端)或 `confirm-hold-ring`(沉浸/全屏场景);不再叠加二次确认弹窗(双重确认是负担)
- `confirm-slide-bar` 阈值固定 80%,不足弹回必须带回弹缓动(`ease-spring`,过冲 ≤ 1.2)
- `confirm-hold-ring` 时长 600-1000ms;环走满与执行之间不允许额外等待
- `progress-fill-bg` 的填充必须用 `transform: scaleX` 或 width 单属性过渡,完成提亮 ≤ 150ms(见 [`micro-interactions.md`](micro-interactions.md) 时长预算)
- `undo-toast-countdown` 走完消失前 200ms 不再响应撤销点击(防误触已失效操作)
- 所有确认控件必须可被键盘/读屏替代完成(`confirm-hold-ring` 提供"按 Enter 持续 1s 或直接二次确认"替代路径,见 [`accessibility.md`](../meta/accessibility.md))
- 图表内的进度/目标表达(可拖动目标线、环形入场画线)见 [`charts.md`](charts.md) 的可交互图表条目

### 确定性进度

- **能确定就不转圈**:确定进度帮人决策(等/稍后再来/放弃);一旦耗时变得可估算,立即从转圈切换为进度条
- **进度速率要匀**:前 90% 用 5 秒、后 10% 用 5 分钟让人觉得卡死甚至被骗;进度停走必须给原因与出路(可 Cancel/Pause;取消丢进度须警告)
- **转圈与进度条外形不互转**:尺寸形状跳变扰界;中途升级只允许"转圈→进度条"的单向切换(见上条),禁反向
- **任务描述写具体动作**:正在解析数据集/正在上传 3 个文件,禁 loading/authenticating 空话(与 [`notifications.md`](notifications.md) 生成等待反馈同理);转圈适合后台小任务与窄空间,可免标签
- **最短进度动画 400ms**:任务实际完成时间短于 400ms 时,进度动画仍播满 400ms——闪现的进度条比没有更糟(与转圈→进度条单向切换配套:确定进度一旦展示就保持最短可感知时长)
- **整体进度与实时进度分色**:同时表达总量进度与实时速度(缓冲/下载速率)时,两色必须明显区分;相近色会误导用户对进度的判断

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
