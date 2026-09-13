# 页面状态模式命名词汇

> 术语库。页面级 Loading / Empty / Error 状态的模式命名,与 principles 第 14 定律的四类状态对应(Tactile Feedback 见 micro-interactions.md)。来源:Carbon Design System(carbondesignsystem.com)、Nielsen Norman Group(nngroup.com)、Atlassian Design(atlassian.design)、Apple HIG(developer.apple.com)、Shopify Dev(shopify.dev)、ServiceNow Horizon、Material Design(m3.material.io);抓取日期 2026-09-08 verified。

## 命名表

| 模式名 | 构成要素(插画/文案/动作按钮) | 适用场景 |
| --- | --- | --- |
| `state-skeleton` | 骨架占位 + shimmer 微动,结构同真实内容 | 首屏初次加载(Carbon:skeleton 是组件的简化版,靠动效传达"没卡死",只停留数秒) |
| `state-spinner` | 圆形指示器,无进度语义 | 短等待、局部刷新;超过"一瞬间"应改用进度条(Carbon) |
| `state-progress-bar` | 线性进度条,确定/不确定两态,全屏或区块级 | 较长等待、上传/导入等可量化任务 |
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

## 使用规则

- principles 第 14 定律:Loading / Empty / Error / Tactile 四类状态必须齐备,缺任一类即半成品;本表命名前三类,Tactile Feedback 见 [`micro-interactions.md`](micro-interactions.md)
- 空态三要素:是什么(状态)、为什么(可省)、下一步(主按钮或文案内链接),不把用户引进死胡同(Carbon)
- 加载中禁止提前显示"无记录"空文案(NN/g:状态失实损害信任,用户会提前离开);skeleton 只停留数秒,超时转入错误态并给重试
- 错误文案用平实语言、不带错误码,直述问题并建议修复(呼应 NN/g 启发式:帮助用户识别、诊断并从错误中恢复)
- 同屏多个空态降级为文本 + 次级按钮,避免堆叠多个主按钮(Carbon);一个空态只保留一个主行动
- 与 cards.md / popups.md 分工:页面级状态归本表;卡片局部骨架/空态复用 [`cards.md`](cards.md) 的 `card-skeleton` / `card-empty`;弹窗内的成功反馈走 [`popups.md`](popups.md) 的 `popup-modal-to-success`
- 空态插画策略见 [../meta/visual-assets.md](../meta/visual-assets.md);状态文案写法见 [../meta/content-guide.md](../meta/content-guide.md)
- 无障碍:状态切换须对屏幕阅读器可感知(loading/busy/失败均需通知,Carbon)

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
