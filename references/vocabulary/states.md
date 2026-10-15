# 页面状态模式命名词汇

> 术语库。页面级 Loading / Empty / Error 状态的模式命名,与 principles 第 14 定律的四类状态对应(Tactile Feedback 见 micro-interactions.md)。来源:Carbon Design System(carbondesignsystem.com)、Nielsen Norman Group(nngroup.com)、Atlassian Design(atlassian.design)、Apple HIG(developer.apple.com)、Shopify Dev(shopify.dev)、ServiceNow Horizon、Material Design(m3.material.io);抓取日期 2026-09-08 verified。

## 命名表

| 模式名 | 构成要素(插画/文案/动作按钮) | 适用场景 |
| --- | --- | --- |
| `state-skeleton` | 骨架占位 + shimmer 微动,结构同真实内容 | 首屏初次加载(Carbon:skeleton 是组件的简化版,靠动效传达"没卡死",只停留数秒) |
| `state-spinner` | 圆形指示器,无进度语义 | 短等待、局部刷新;超过"一瞬间"应改用进度条(Carbon) |
| `state-progress-bar` | 线性进度条,确定/不确定两态,全屏或区块级;页面级变体:顶部 3px 细条冲刺——快冲到约 30% 后越走越慢,最高停 90% 等数据,数据回来冲 100% 再淡出,原页面保留不动 | 较长等待、上传/导入等可量化任务;文章/页面级切换加载 |
| `state-loading-inline` | 行内/按钮内小指示器,不换页不遮罩 | 表格刷新、按钮提交等局部加载(Carbon inline loading) |
| `state-empty-first-use` | 插画 + 正向标题 + 说明 + 主按钮"创建/添加" | 首次使用无数据(Carbon no-data 型:说明将出现什么、如何添加) |
| `state-empty-no-results` | 简化插画 + 无结果说明 + 调整建议 | 搜索无结果(NN/g:如"所选条件下无记录",传达系统状态) |
| `state-empty-clear-filters` | 说明 + "清除筛选"次级按钮 | 筛选/参数导致的空结果(Carbon user-action 型:建议调整筛选) |
| `state-empty-starter` | 示例数据/模板预填 + 重置回基础空态的出口 | 首启空态的进阶替代(Carbon starter content,需保留基础空态兜底,配合 onboard-sample-data) |
| `state-error-crash` | 错误插画 + 平实文案(无错误码) + 重试/返回首页 | 页面崩溃、渲染兜底(Carbon error-management:直述问题并给建设性出路) |
| `state-error-network` | 断网插画 + 重试按钮,保留已加载数据 | 请求失败;文案直述问题,不指责用户 |
| `state-error-permission` | 锁形插画 + 权限说明 + 申请入口/联系管理员 | 无权限访问(Carbon:permissions 类错误需要更高的具体度) |
| `state-offline` | 持久但不打扰的离线指示/横幅,说明仍可用范围 | 断网或离线操作(Material "offline by choice";ServiceNow 连接异常模板) |
| `state-partial-load` | 分批渲染 + 失败区块"重试"入口 | 分批渐进加载部分失败(Carbon progressive loading,可配 Load more) |
| `state-stale-data` | 数据过期标记/横幅("数据截至 XX:XX") + 立即刷新按钮;旧数据保持可读不隐藏 | 后台数据已更新而页面未刷新、实时性非关键的列表/详情(practicalswan:stale 与 retry 并列为必备状态) |
| `state-auth-expired` | 会话过期说明(直述原因) + 重新登录入口;登录成功后返回中断位置并恢复未提交输入 | 会话/令牌过期、权限变更;登录页选型走 [`auth.md`](auth.md),本条只命名页面状态 |
| `state-destructive-undo` | 三段防护:前置确认(直述后果,焦点置安全侧)→ 执行后可撤销 toast(undo + 倒计时)→ 撤销/关闭后焦点恢复到触发元素 | 删除、移除、批量操作等破坏性动作(practicalswan:confirmation/cancellation/undo/recovery) |

> 末 3 行(数据过期/认证失效/破坏性防护)来源:frontend-design-practicalswan,2026-09 吸收。

## 交互态扩展(选中/多选/反色)

> 页面级状态之外的"整页切态"与自适应状态命名。来源:UI 交互教学视频转录提取(2026-09)。

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `state-selection-mode` | 长按进入多选:长按一张卡整页切态——卡片缩一档让出勾选圈,标题变已选数,底部升起操作条 | 相册/文件/邮件批量操作 |
| `state-focus-spotlight` | 选中聚焦其余后退:选中项放大提亮,同层未选中降饱和+缩小+轻微模糊 | 媒体选择、方案对比(MOTION ≥ 6) |
| `state-adaptive-invert` | 悬浮元素亮度自适应反色:悬浮按钮/文字按背后区域明暗自动反色,滚动中连续过渡 | 悬浮 FAB/播放按钮压在内容图上 |
| `state-skeleton-equal` | 骨架屏等高落位:占位块与真实内容同尺寸,骨架高度=内容高度,防止到达时跳动 | 首屏列表/卡片加载(`state-skeleton` 的强制细则) |
| `state-image-blur-up` | 图片模糊到清晰:未加载先用主色调+高斯模糊小图占位,原图到达后模糊渐清晰并 1.04→1 轻缩(约 500ms,装饰档 ≤600ms 须可跳过/reduced-motion 直显终态),像相机对焦;图框尺寸提前固定,加载前后版面不跳;距进入视口约 300px 即预加载 | 图片墙、瀑布流、商品图 |
| `state-upload-reveal` | 上传蒙层刷亮:缩略图先盖半透明深色蒙层,上传时蒙层自下而上退去,退到哪亮到哪;中心细圆环随进度,完成变对勾弹一下淡出;多张错峰开始各走各速;进度长在被上传的内容本身上,非外挂 spinner | 多图上传、发帖页(上传期间主任务不阻断) |
| `state-map-matching` | 水波匹配等待:定位点向外扩波纹(每圈约 1.6s,越扩越淡,3 圈错开),周边候选图标缓慢驶近;底部状态卡显示进度文案与已等待秒数走动;匹配成功波纹收拢成点、结果卡上翻出详情 | 打车/匹配/调度类地图等待(等待要"有东西看") |

> 来源注:`state-upload-reveal` / `state-map-matching` 2 行为**转录补全**(2026-10,UI 交互教学视频转录提取)。

- `state-selection-mode` 进入/退出必须动画过渡(卡片位移+勾选圈淡入),底部操作条入场 ≤ 300ms;系统返回键先退多选态再退页面
- `state-focus-spotlight` 未选中项降饱和 60% + 模糊 2px + 缩小 0.96 为上限,过强会像禁用态(与 [`states.md`](#) 禁用语义区分)
- `state-adaptive-invert` 以元素背后采样区域亮度切换 `color: white/black`,过渡 200ms 连续插值,禁止硬切
- 骨架屏高度必须用与真实内容相同的布局结构渲染(同一组件两态),禁止固定假高度
- 加载动效配自然隐喻(骨架浮现如退潮、`state-image-blur-up` 如相机对焦、列表接续如传送带、流式回复如真人打字),实现与提示词都把隐喻目标写进去;骨架数据到达后按头像/标题/图块自上而下错峰浮现(单档 ≤ 80ms,口径同 [`micro-interactions.md`](micro-interactions.md));等待尽量前置消化:`scroll-infinite` 距底约一屏预载、图片距进入视口约 300px 预载(**转录补全**,2026-10)

## 使用规则

- principles 第 14 定律:Loading / Empty / Error / Tactile 四类状态必须齐备,缺任一类即半成品;本表命名前三类,Tactile Feedback 见 [`micro-interactions.md`](micro-interactions.md)
- 空态三要素:是什么(状态)、为什么(可省)、下一步(主按钮或文案内链接),不把用户引进死胡同(Carbon)
- 加载中禁止提前显示"无记录"空文案(NN/g:状态失实损害信任,用户会提前离开);skeleton 只停留数秒,超时转入错误态并给重试
- 错误文案用平实语言、不带错误码,直述问题并建议修复(呼应 NN/g 启发式:帮助用户识别、诊断并从错误中恢复)
- 同屏多个空态降级为文本 + 次级按钮,避免堆叠多个主按钮(Carbon);一个空态只保留一个主行动
- 与 cards.md / popups.md 分工:页面级状态归本表;卡片局部骨架/空态复用 [`cards.md`](cards.md) 的 `card-skeleton` / `card-empty`;弹窗内的成功反馈走 [`popups.md`](popups.md) 的 `popup-modal-to-success`
- 空态插画策略见 [../meta/visual-assets.md](../meta/visual-assets.md);状态文案写法见 [../meta/content-guide.md](../meta/content-guide.md)
- 无障碍:状态切换须对屏幕阅读器可感知(loading/busy/失败均需通知,Carbon)
- **操作成功前不得显示成功**:乐观更新必须能对账失败并回滚,失败立即转错误态——"假成功"比加载慢更伤信任(practicalswan:never show success before the operation succeeds)
- **保留可恢复输入**:任何失败、过期、中断都不得清空用户已填内容(表单值、草稿、筛选条件);重新登录或重试后原样恢复(practicalswan:retain recoverable user input)
- **状态转换可理解**:异步状态变化必须可感知(视觉过渡 + 屏幕阅读器通知),用户能说出"刚才发生了什么、现在处于什么状态"(practicalswan:keep state transitions understandable;三条行为规则来源:frontend-design-practicalswan,2026-09 吸收)

## 在 draw-md 中的写法

```markdown
## State (list-loading)
- pattern: state-skeleton
- shimmer: true, duration: under-4s, timeout: error-retry

## State (search-empty)
- pattern: state-empty-no-results
- composition: { illustration, headline, hint, action: "清除筛选" }

## State (request-failed)
- pattern: state-error-network
- action: [retry, keep-loaded-data]
```
