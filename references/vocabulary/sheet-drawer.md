# 抽屉与浮层链路模式命名词汇

> 模式词汇库。底部抽屉(sheet)的完整手势生命周期,以及浮层"从哪里来回哪里去"的链路语义。来源:UI 交互教学视频转录提取(2026-09,西瓜同学/叨叨AI);与 [`popups.md`](popups.md)(弹窗类型选型)、[`micro-interactions.md`](micro-interactions.md)(时长预算)互补。

## 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `sheet-directional-entry` | 从触发方向出现:从手指按下的一侧/底部滑入,不从屏幕中央凭空出现 | 移动端所有 sheet 的默认入场 |
| `sheet-velocity-dismiss` | 速度判关:下拉距离过半**或**松手甩动速度超阈值即关闭,双条件或 | 所有可下拉关闭的 sheet |
| `sheet-notch-snap` | 档位吸附:半屏/全屏多档,松手吸附最近档位,拖动跟手无跳变 | 地图详情、评论面板、快捷设置 |
| `sheet-nested-back` | 嵌套后退:第二层 sheet 压上时第一层缩小变暗后退,表示层级加深 | 多级详情(列表→详情→子详情) |
| `sheet-backdrop-triplet` | 背景退后三件套:底页变暗 + 模糊 + 轻微缩小,才算"退到后面" | 全部模态场景(三件套缺一即"贴纸感") |
| `sheet-grow-into-page` | 抽屉长成页面:卡片直接长大成下一页,不先关抽屉再开新页 | 详情链路转场(与 [`../motion-skeletons/shared-element.md`](../motion-skeletons/shared-element.md) 联动) |
| `popup-anchor-grow` | 弹窗锚点生长:弹窗从被按按钮那一点放大长出,关闭原路收回同一点 | 从按钮/图标触发的 popover、菜单 |
| `button-submit-morph` | 按钮提交态形变:宽按钮收成圆→圆环转两圈→撑开→对勾画出,全程位置不挪 | 表单提交、支付按钮 |
| `toast-queue-handoff` | toast 队列让位:多条依次让位进出,位移+透明度进场,停够时长平滑退走 | 连续操作反馈(批量删除、连发消息) |
| `badge-lifecycle` | 红点生命周期:点红点从其位置展开提示面板;处理完红点沿原位缩回散掉 | 消息红点与提示面板的来去一致 |
| `preview-longpress-peek` | 长按浮起预览:背景压暗虚化,该项放大浮起,下方弹操作排,不进详情页 | 相册/列表的快捷预览(iOS context menu) |
| `banner-push-down` | 顶部横幅推下内容:横幅从状态栏降下,页面内容跟着下让一段 | 离线提示、系统通知栏内嵌横幅 |
| `panel-grow-from-plus` | 新建面板从加号长出:面板从按下的 FAB 长出,新条目落进列表"有来路" | 新建/发布流程的起点反馈 |

## 使用规则

- 浮层链路铁律:**从哪里来,回哪里去**。`popup-anchor-grow`/`badge-lifecycle`/`panel-grow-from-plus` 的退场必须复现入场轨迹(锚点丢失时降级为缩放淡出)
- `sheet-velocity-dismiss` 双阈值:距离 > 50% **或**速度 > 0.5 px/ms;距离不足但速度够也关(见 [`../motion-skeletons/gesture-arbitration.md`](../motion-skeletons/gesture-arbitration.md))
- `sheet-notch-snap` 档位 ≤ 3 个;拖动全程跟手,只在松手后吸附
- `sheet-backdrop-triplet` 三件套参数:变暗 40% + 模糊 8px + 缩小 0.98;缺缩小最易产生"贴纸感"
- `button-submit-morph` 全程 ≤ 400ms 且位置钉死;失败态对勾变叉,同一容器内切换
- `toast-queue-handoff` 同屏 ≤ 2 条,第 3 条起排队;单条停留 2-3s,进出场各 ≤ 250ms
- `preview-longpress-peek` 长按 400ms 触发;三路手势:松手落回 / 拖到操作项执行 / 拖出范围取消
- 所有 sheet 关闭必须响应系统返回键/Esc,且与下拉关闭走同一动画(见 [`accessibility.md`](../meta/accessibility.md) 焦点管理)
- 入退场时长 ≤ 400ms(浮层档,见 [`micro-interactions.md`](micro-interactions.md) 分层口径);`prefers-reduced-motion` 降级为淡入淡出

## 在 draw-md 中的写法

```markdown
## Sheet (comment-panel)
- pattern: sheet-directional-entry + sheet-notch-snap
- notches: [50vh, 90vh], dismiss: velocity+distance, backdrop: sheet-backdrop-triplet
- reduced_motion_fallback: fade

## Submit (pay-button)
- pattern: button-submit-morph
- stages: [shrink-to-circle, ring-spin-2, expand, check-draw], anchor-locked: true
```
