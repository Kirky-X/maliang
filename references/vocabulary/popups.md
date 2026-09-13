# 弹窗浮层模式命名词汇

> 术语库。弹窗是一条链路(进来/停留/退场/成功)而非一个框,本表标准化弹窗与抽屉的交互变体命名,与 [`micro-interactions.md`](micro-interactions.md) 互补。来源:视频研究 v01(10 SHEETS)。

## 命名表

| 模式名                    | 视觉特征                                       | 关键参数                                                   | 适用场景                   |
| ------------------------- | ---------------------------------------------- | ---------------------------------------------------------- | -------------------------- |
| `popup-sheet`             | 底部抽屉,从手指来的方向长出                    | 出身=屏幕边缘;禁止屏幕中心 scale 放大冒充抽屉              | 移动端表单、快捷操作       |
| `popup-half-snap`         | 半屏停住,底下页面仍可见                        | 吸附点 SNAP=[52%,8%],露出约 48% 底页                       | 列表详情、需保留上下文     |
| `popup-expand`            | 半屏→全屏,同一个面在展开                       | 位移/圆角/抓手三属性连续变化;圆角收掉、抓手淡出            | 详情逐级展开               |
| `popup-blur-backdrop`     | 背景退后,弹窗压暗底层                          | 底层模糊 18px + 缩放 0.96                                  | 弹窗出现时的背景处理       |
| `popup-spring-in`         | 弹性出现,两段到位有抽出手感                    | 翘起 0.24s + 落位 0.66s(一段到位只像普通弹窗)            | 抽屉入场                   |
| `popup-drag-close`        | 下滑关闭,位移+速度双条件                       | 例:40px/速度 0.72 关,31px/速度 0.11 不关                  | 抽屉手势退场               |
| `popup-drag-snap`         | 三档拖拽 FULL/HALF/PEEK                        | 松手必吸附某一档,档间是过路不是车位                        | 地图、可分级面板           |
| `popup-nested`            | 嵌套抽屉,新层压上前层退回                      | 前层后退约 6% + 缩小 + 变暗                                | 多级抽屉(如双层评论)     |
| `popup-sheet-to-page`     | 抽屉卡直接长成整页                             | 禁止先关抽屉再开页(两件事,中间会断)                      | 详情直达                   |
| `popup-modal-to-success`  | 原地变成功态,不是关闭                          | 按钮缩成圆 → 勾一笔画出 → 收成一条回执                     | 提交/完成反馈              |
| `popup-confirm`           | 二次确认浮层:轻量小卡,取消为主操作,危险操作文字红字 | 就近触发出现在操作点旁(气泡/轻弹窗),不遮蔽全屏            | 破坏性操作前的轻量确认(删除/注销/退款) |
| `popup-error`             | 错误浮层/错误条:错误图标 + 重试动作 + 可关闭    | 重试为唯一主操作;常驻直到用户关闭或问题解决               | 登录失败、请求失败等操作失败反馈;表单错误汇总另见 [forms.md](forms.md) 的 `error-summary` |
| `banner-notification`     | 常驻通知横幅:页面级持久消息,可多行排版,带操作位与关闭 | 驻留至用户关闭或问题解除;与 toast(短暂、单条、无操作位)按驻留性/可操作性区分;离线提示衔接 [states.md](states.md) `state-offline` | 系统公告、离线/同步提醒、需操作的应用内通知(framework `notification` 类) |

> 来源注:`popup-confirm` / `popup-error` 两行为**审计补全**(auth.md/states.md 引用需求),非"视频研究 v01 10 SHEETS"来源;其余 10 模式均为实测动链。
> 来源注:`banner-notification` 为**审计补全**(2026-09-08 组件覆盖审计):对照 Ant Design Notification、IBM Carbon Notification(inline)、Material 3 Banner 组件清单,非"视频研究 v01 10 SHEETS"实测来源。
> 注:`popup-spring-in` 的"翘起 0.24s + 落位 0.66s"为**序列两段值**(合计 0.9s),非单段 transition;单段 transition >400ms 会触发 `validate-draw-md.py` 硬门(ERROR,见 [`micro-interactions.md`](micro-interactions.md) 时长预算表注),实现时拆 keyframes 分段或压缩至 400ms 内。

## 使用规则

- 弹窗是链路:出现 → 停留 → 回应 → 成功 → 退场各环节连续,弹出后每一步都要接得住用户的手;"只出现一个框"是反模式
- 新一层压上时,前一层要退回(压暗 + 缩小);层级感是退出来的,不是叠出来的
- 半屏弹窗的价值在"露出来的那一截":底下页面看得见,人才知道自己没走远
- 结束也该是一段动画:完成动作不是关闭,而是弹窗原地变成成功状态
- 抽屉的出身是边缘长出;从屏幕中间放大的那是弹窗不是抽屉(出身错误 = AI 翻车点)
- 拖拽关闭位移与速度都要看:快速小幅下滑也应关闭,慢速长滑未过阈值则不关
- `popup-expand` 与 `popup-sheet-to-page` 靠"同一个面连续变化"成立:中途禁止断帧,更不许先关抽屉再开页
- 三档拖拽里档与档之间只是过路:松手必须落在 FULL/HALF/PEEK 之一,不许停在半档
- 多级场景组合 `popup-nested` + `popup-blur-backdrop`;成功反馈固定走 `popup-modal-to-success`

## 在 draw-md 中的写法

```markdown
## Popup (comment-sheet)
- pattern: popup-sheet
- enter: { origin: edge-bottom, stages: [lift-0.24s, settle-0.66s] }
- backdrop: { blur: 18px, scale: 0.96 }
- snap: [52%, 8%]
- drag: { close: { offset: 40px, velocity: 0.72 }, levels: [FULL, HALF, PEEK] }
- nested: { parent: { dim: true, scale: 0.94, offset: -6% } }
- expand: { props: [offset, radius, grabber], continuous: true }
- success: { morph: button-to-circle, draw: check, collapse: receipt }
- chain: [enter, stay, respond, success, exit]
```
