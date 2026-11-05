# 弹窗浮层模式命名词汇

> 术语库。弹窗是一条链路(进来/停留/退场/成功)而非一个框,本表标准化弹窗与抽屉的交互变体命名,与 [`micro-interactions.md`](micro-interactions.md) 互补。

## 命名表

| 模式名                    | 视觉特征                                       | 关键参数                                                   | 适用场景                   |
| ------------------------- | ---------------------------------------------- | ---------------------------------------------------------- | -------------------------- |
| `popup-sheet`             | 底部抽屉,从手指来的方向长出                    | 出身=屏幕边缘;禁止屏幕中心 scale 放大冒充抽屉              | 移动端表单、快捷操作       |
| `popup-half-snap`         | 半屏停住,底下页面仍可见                        | 吸附点 SNAP=[52%,8%],露出约 48% 底页                       | 列表详情、需保留上下文     |
| `popup-expand`            | 半屏→全屏,同一个面在展开                       | 位移/圆角/抓手三属性连续变化;圆角收掉、抓手淡出            | 详情逐级展开               |
| `popup-circle-reveal`     | 按钮经圆形裁剪扩展成浮层面板:圆从按钮圆心撑开铺成面板,关闭沿圆收缩回按钮 | 圆心=按钮坐标;与 [`sheet-drawer.md`](sheet-drawer.md) `popup-anchor-grow` 分界:彼条整面缩放长出,本条裁剪揭示(内容随圆逐步露出);铺满全屏的极端版见 [`pro-motion.md`](pro-motion.md) `menu-circular-reveal` | 从 FAB/按钮展开的功能面板(地图详情、搜索展开) |
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
| `banner-task-track`       | 常驻任务跟踪条:上传/导出/配送/直播比分等长任务的一瞥式进度条 | 有明确起止;只显示一瞥必需信息;任务即时结束并给完成摘要,驻留一段后自动消失;内容真变化才更新;敏感信息不外显(旁人可见场景) | 进行中任务的持久可视化;通知分级与投放纪律见 [notifications.md](notifications.md) |
| `popup-toast`             | 即时反馈:纯告知小条,不承载任何交互元素(禁放按钮/链接) | 单次显示 ≤3s;禁止连续弹新 toast 覆盖旧 toast;不遮盖弹出框内容 | 操作结果的轻量告知;需要撤销/重试等动作时升级为 `popup-snackbar` |
| `popup-snackbar`          | 即时操作:反馈 + 一个轻操作(撤销/重试/查看) | 定时模式 5~10s 自动消失,滑动屏幕即关;常驻模式(登录/权限等重要提示)必须提供关闭按钮 | 反馈之外还要给出口的场景;与 `popup-toast` 的分界=是否带操作 |

> 注:`popup-spring-in` 的"翘起 0.24s + 落位 0.66s"为**序列两段值**(合计 0.9s),非单段 transition;单段 transition >400ms 会触发 `validate.py draw-md` 硬门(ERROR,见 [`micro-interactions.md`](micro-interactions.md) 时长预算表注),实现时拆 keyframes 分段或压缩至 400ms 内。

## 浮层选型决策

> 先选对形态,再谈链路。

| 场景 | 该用什么 | 不该用什么 |
| --- | --- | --- |
| 用户主动作引发的分支选择(删除前选范围、分享选目标) | action sheet / 底部动作面板 | alert(二者不可互换:alert 是意外,action sheet 是回应) |
| 意外发生的问题与警示(同步失败、权限被拒) | alert | 通知(notifications.md) |
| 少量相关功能的就近轻编辑 | popover/锚定浮层 | 警告不用 popover(会被误关,改 alert) |
| 命令与选项的按需展开 | menu(见 [`menus.md`](menus.md)) | action sheet(menu 是用户主动展开,action sheet 是系统对动作的回应) |
| 纯告知性信息 | 页内横幅/行内提示 | alert(纯告知不用模态) |

- **alert 三不用**:纯告知不用(改行内提示);常见且可撤销的破坏动作不用(删一封邮件不需要确认,可撤销口径走 [`states.md`](states.md) destructive-undo);应用启动时不用(改用占位数据+行内标注)
- **alert 按钮命名**:用具体动词(Erase/Convert/Delete),OK 只允许纯信息告知;取消永远叫 Cancel;默认按钮放行尾,Cancel 不做默认按钮
- **破坏性样式只用于"非本意的破坏"**:清空回收站是用户本意,不用危险色;alert 含破坏项时必配 Cancel 出口
- **alert 标题**:写清发生了什么/何时/为何,禁"Error 329347";正文只在增值时才写
- **action sheet 纪律**:禁滚动(按钮多到要滚=设计错误);Cancel 固定底部;破坏性项置顶加危险色;选项务必一屏看全,除 Cancel 外 ≤3 项
- **popover 纪律**:同时只开一个,禁级联(新 popover 先关旧的);popover 上不得再叠浮层(alert 除外);尺寸只够装内容,箭头指向触发源;非模态 popover 因点外自动关闭前必须保存工作,只有显式 Cancel 才丢弃
- **模态纪律**:同一时间至多一个模态——先关闭再开新模态(alert 例外可压一切,但也至多一个);模态内保持单一通路,避免"应用中再有应用";必须含子层级时只给一条返回路径,且不放易误认成关闭按钮的控件
- **反馈强度总纲**:传达方式的重要度匹配信息的重要度——状态就近被动展示,只有警告才允许打断;成功确认只留给足够重要的任务(常规成功不打扰);只对"非预期且不可逆"的数据丢失警告,预期内的删除不警告
- **命令无法执行时**:显式说明原因并给出路,禁止无声置灰了事(文案口径见 [`../meta/content-guide.md`](../meta/content-guide.md))
- **弹窗按钮 ≥3 个改上下布局**:顺序由左至右改为从下至上(主操作沉底);弹窗宽度可随窗口弹性伸缩,设最大宽度封顶
- **toast/snackbar 不遮弹窗**:即时反馈出现在弹出框之上时,不得遮盖弹出框的输入区与按钮

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
