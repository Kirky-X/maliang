# 新手引导模式命名词汇

> 术语库。新手引导是"让用户尽快完成第一个有价值动作"的一组模式,本表标准化其变体命名,与页面状态词汇(states.md)互补。来源:Nielsen Norman Group(nngroup.com)、Carbon Design System(carbondesignsystem.com)、Atlassian Design(atlassian.design)、Apple HIG(developer.apple.com)、Shopify Dev(shopify.dev)、UI-Patterns.com;抓取日期 2026-09-08 verified。

## 命名表

| 模式名 | 构成要素(内容/动作) | 适用场景 |
| --- | --- | --- |
| `onboard-welcome` | 欢迎屏/启动屏:极简占位 + 品牌标识,传达"秒开即用" | 首次启动(Apple HIG:启动屏唯一职能是强化"快速可用"的感知) |
| `onboard-tour` | 分步高亮 + 逐步文案 + 上一步/下一步 + 跳过 | 首次进入复杂工作台(Atlassian spotlight 的 multi-step tours) |
| `onboard-coach-mark` | 页内锚定气泡(非阻断),指向单个控件,操作即散 | 功能首次可见时的上下文提示(NN/g "pull revelations" 就地揭示) |
| `onboard-checklist` | 任务清单 + 完成勾选 + 进度感,每项直达对应功能 | 多步配置的 SaaS 首启,引导完成第一个有价值动作(Shopify:空屏是引导首个动作的机会) |
| `onboard-sample-data` | 预填示例数据 + "示例"标记 + 一键清空 | 空仪表盘/看板:先试后删(Carbon starter content;NN/g demo data 供"安全探索") |
| `onboard-empty-template` | 预置模板/套件 + 预览 + 使用入口 | 文档、项目类工具起步(Carbon "pre-built templates" 提供生产力起点) |
| `onboard-progressive-disclosure` | 默认只露主路径,高级项按需展开;主功能配内联文档 | 功能多但首启只需少数路径(Carbon in-line documentation) |
| `onboard-lazy-registration` | 先体验后注册,触发保存/分享时才要求账号 | 免注册试用(UI-Patterns.com:注册前即可使用并行动) |
| `onboard-import` | 第三方导入向导 + 字段映射 + 导入进度反馈 | 竞品切换场景,降低重建数据的成本 |
| `onboard-feature-announcement` | 新功能焦点公告,一次性展示、可忽略 | 老用户的功能上新(Atlassian spotlight 亦用于引入新功能) |

> 注:本表是"模式命名",不负责引导浮层的出入场动效;模态阻断式浮层(注册墙、首启弹窗)的链路设计见 [`popups.md`](popups.md)。

## 使用规则

- 引导的目的是让用户尽快完成第一个有价值动作,不是功能说明书:上下文内提示比强制教程更有效(NN/g 实证),Apple HIG 亦要求首启快速直达
- 优先顺序:上下文 coach-mark > 空态内引导(见 [`states.md`](states.md))> 分步 tour > 欢迎屏;能不阻断就不阻断
- tour 与 coach-mark 必须可跳过/可关闭;引导是可选项,须与基础空态并存(Carbon:引导流程要搭配基础空态使用)
- 与 [`popups.md`](popups.md) 分工:模态阻断浮层走 popups.md 的弹窗链路;本表 coach-mark/tour 是页内锚定提示,不进入浮层链路
- 示例数据必须有"示例"标记与清空出口,并保留基础空态兜底(Carbon:starter content 可能被用户删除)
- 同一首启流程引导模式 ≤ 2 种、清单项 ≤ 5;principles 第 14 定律要求四类状态完整,引导不能替代 Loading/Empty/Error 兜底
- 空态插画策略见 [../meta/visual-assets.md](../meta/visual-assets.md);引导文案写法见 [../meta/content-guide.md](../meta/content-guide.md)

## 在 draw-md 中的写法

```markdown
## Onboarding (first-run)
- pattern: onboard-tour
- steps: [highlight-inbox, highlight-compose, highlight-settings]
- dismiss: { skippable: true, persistent: false }

## Onboarding (empty-dashboard)
- pattern: onboard-sample-data
- sample: { marked: true, reset: clear-to-empty }
- fallback: state-empty-first-use

## Onboarding (guest-mode)
- pattern: onboard-lazy-registration
- gate: { trigger: save-or-share, defer: true }
```
