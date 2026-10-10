# 抽屉与浮层链路模式命名词汇

> 模式词汇库。底部抽屉(sheet)的完整手势生命周期,以及浮层"从哪里来回哪里去"的链路语义。来源:UI 交互教学视频转录提取(2026-09,西瓜同学/叨叨AI);与 [`popups.md`](popups.md)(弹窗类型选型)、[`micro-interactions.md`](micro-interactions.md)(时长预算)互补。专业面板 6 组件见文末「专业面板组件」节(2026-10 视频截图提取)。

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

## 专业面板组件

> 6 个专业级面板入场与展开组件(X Sheet 系列 + 原地翻面)。与上文链路模式分工:上文命名手势生命周期,本节命名入场编排与内部动效。来源:专业面板组件视频截图提取(2026-10,与前篇同系列)。`sheet-ring-count` 为已有模式的面板化组合(命名收编),其余 5 组新增;速度投射锚点见 [`pro-motion.md`](pro-motion.md) `sheet-velocity-anchor`。

### 命名表

| 模式名 | 视频组件 | 视觉特征 | 适用场景 |
| --- | --- | --- | --- |
| `sheet-glass-frost` | 玻璃面板浮起 Frosted Glass Sheet | 打开时背景页模糊 0→26px,面板底色 rgba(255,255,255,.42) 从 0.94 放大到 1 浮起;内部进度格按已用比例从底部填充,每格错开 4 帧 | 会员 / 通行证 / 余量浮层(glass 配方见 [`../dimensions/glass-effect.md`](../dimensions/glass-effect.md)) |
| `sheet-ring-count` | 圆环计数弹出 Ring Count Sheet | 底部面板升入 + scrim 40%;落定后圆环 stroke-dashoffset 画到剩余比例,中心数字从 0 同步滚到目标值 | 配额 / 余量 / 有效期面板(chart-ring-draw + `num-ticker-onview` 的面板化组合) |
| `sheet-tick-ruler` | 刻度尺扫到今天 Tick Ruler Sheet | 面板滑入后刻度从左到右逐根变深(每根错 1 帧),今天格换强调色停住;敏感编号原地逐字展开,行高不变 | 进度 / 日程手账;敏感信息揭示 |
| `sheet-photo-drawer` | 照片抽屉贴合 Photo Drawer Sheet | 照片 1.08 缩回 1 铺满,暗角托白字;抽屉负 margin 压住照片底边从下推入,进度条随后 0→比例 | 封面主导的详情抽屉(食谱 / 商品) |
| `panel-flip-reveal` | 点击翻面凭证 Flip to Reveal | 面板 perspective 1200px 绕 Y 翻转 180°,90° 时切换正反面;背面承载完整信息,再点沿原路翻回 | 凭证 / 票据正反面切换 |
| `sheet-pull-reveal` | 下拉展开面板 Pull Down Reveal | 面板弹入落定,下沿留把手与虚线;下拖时下半张沿虚线分离跟手,带 2° 摆动,超 40% 松手展开,不足弹回 | 编号 / 敏感区藏在下半张的面板 |

### AI 描述词对照

> 视频提示词原文;落 draw-md 时按模式名与使用规则参数化,不整段照抄。

| # | 组件 | AI 描述词 |
| --- | --- | --- |
| 01 | 玻璃面板浮起 | 毛玻璃浮层(Frosted Glass Sheet):打开时背景页 backdrop-filter 模糊从 0 过渡到 26px,面板底色 rgba(255,255,255,.42),从 0.94 放大到 1 浮起;12 月份格按已用比例从底部填充,每格错开 4 帧,用 cubic-bezier(.2,.7,.2,1) 在 1 秒内完成。 |
| 02 | 圆环计数弹出 | 圆环计数弹出(Ring Count Sheet):底部面板用 cubic-bezier(.2,.7,.2,1) 在 0.5 秒内从屏幕外升到位,背景压暗到 40%;落定后圆环 stroke-dashoffset 用同一条曲线 1.2 秒画到剩余比例,中心数字从 0 同步滚到目标值。 |
| 03 | 刻度尺扫到今天 | 刻度尺进度弹出(Tick Ruler Sheet):面板从下方滑入后,53 根周刻度从左到右逐根变深,每根错开 1 帧,到今天这一格换成强调色并停住;点击显示按钮,被遮住的编号原地逐字展开,行高不变。 |
| 04 | 照片抽屉贴合 | 照片抽屉弹出(Photo Drawer Sheet):上半部照片按原比例从 1.08 缩回 1 铺满,暗角托住白色大字;抽屉用 margin-top:-22px 压住照片底边,从下方推入,进度条随后从 0 涨到剩余比例。 |
| 05 | 点击翻面凭证 | 原地翻面面板(Flip to Reveal):点击后面板以 perspective 1200px 绕 Y 轴翻转 180 度,用 cubic-bezier(.3,.7,.2,1) 在 0.8 秒内完成,翻到 90 度时切换正反面内容;背面显示出未用的编号和完整信息,再点一次沿原路翻回。 |
| 06 | 下拉展开面板 | 下拉展开面板(Pull Down Reveal):面板从底部弹入落定,下沿留一截把手和一条虚线;向下拖动把手时下半张沿虚线分离,跟手下移并带 2 度摆动,超过 40% 松手就展开露出完整信息,不到就弹回。 |

### 使用规则

- 时长口径:面板升入属转场档 ≤ 400ms(视频 0.5s / 0.8s 弃用,先例同 ROUTING §5 时长从属声明);圆环画线、进度格填充属装饰档 ≤ 600ms 且必须可跳过,draw-md 规格用 `{duration-*}` token 表达(见 [`micro-interactions.md`](micro-interactions.md) 分层口径)
- 缓动:视频曲线 cubic-bezier(.2,.7,.2,1) / (.3,.7,.2,1) 属 ease-out 家族一次性过渡(系统驱动走 easing,合法);内部错峰在面板落定后启动,禁与转场重叠抢帧
- `sheet-glass-frost`:玻璃配方(模糊 + 饱和 + 边缘高光)照抄 [`glass-effect.md`](../dimensions/glass-effect.md);背景页模糊禁 backdrop-filter 插值(逐帧重绘),用预模糊层 opacity 0→1 交叉淡入;面板自身 backdrop-filter 静态写死,移动端按 glass-effect 降级口径给实底 fallback
- `sheet-ring-count`:圆环走 SVG stroke-dashoffset;圆环与数字同曲线同步启动,数字滚动用 [`number-motion.md`](number-motion.md) `num-ticker-onview`;scrim 40% 与 `sheet-backdrop-triplet` 变暗档一致
- `sheet-tick-ruler`:刻度总数 ≤ 60,每根错 1 帧;今天格强调色是状态语义,禁做成纯装饰高亮;编号逐字展开行高不变(占位稳定,禁 reflow 跳动);reduced-motion 刻度直接全深、编号直接显示
- `sheet-photo-drawer`:照片 1.08→1 只动 `transform: scale`;压边负 margin 是静态布局值,入场推入走 transform,禁动 margin;暗角渐变保白字对比度(见 [`accessibility.md`](../meta/accessibility.md))
- `panel-flip-reveal`:双面板 `backface-visibility: hidden`,90° 中点切换内容;翻转是揭示不是装饰——背面必须承载完整信息;触发用点击,禁 hover(触屏一致);reduced-motion 直接切换正反面
- `sheet-pull-reveal`:40% 距离阈值 + 速度双判据(挂 `sheet-velocity-dismiss`);2° 为跟手摆动上限(微扰,非回弹);把手热区 ≥ 44px;展开后完整信息可读,收起时下半张禁露字
- 共同:整段编排(转场 + 内部内容)≤ 600ms;全部给 `prefers-reduced-motion` 静止终态;关闭链路沿用上文模式(`sheet-pull-reveal` 收起 / 关闭仍走 `sheet-velocity-dismiss`,响应系统返回键)

### 在 draw-md 中的写法

```markdown
## Sheet (pass-detail)
- pattern: sheet-glass-frost
- blur: 26px, fill: rgba(255,255,255,.42), scale: 0.94→1
- cells: bottom-fill, stagger: 4f, duration: {duration-decorate}

## Sheet (quota-panel)
- pattern: sheet-ring-count
- entry: 400ms, scrim: 40%, ring: dashoffset, sync: num-ticker-onview

## Panel (pass-card)
- pattern: panel-flip-reveal
- perspective: 1200px, swap: 90deg, back: full-info
```
