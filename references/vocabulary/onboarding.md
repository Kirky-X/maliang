# 新手引导模式命名词汇

> 术语库。新手引导是"让用户尽快完成第一个有价值动作"的一组模式,本表标准化其变体命名,与页面状态词汇(states.md)互补。

## 命名表

| 模式名 | 构成要素(内容/动作) | 适用场景 |
| --- | --- | --- |
| `onboard-welcome` | 欢迎屏/启动屏:极简占位 + 品牌标识,传达"秒开即用" | 首次启动 |
| `onboard-tour` | 分步高亮 + 逐步文案 + 上一步/下一步 + 跳过 | 首次进入复杂工作台 |
| `onboard-coach-mark` | 页内锚定气泡(非阻断),指向单个控件,操作即散 | 功能首次可见时的上下文提示 |
| `onboard-checklist` | 任务清单 + 完成勾选 + 进度感,每项直达对应功能 | 多步配置的 SaaS 首启,引导完成第一个有价值动作 |
| `onboard-sample-data` | 预填示例数据 + "示例"标记 + 一键清空 | 空仪表盘/看板:先试后删 |
| `onboard-empty-template` | 预置模板/套件 + 预览 + 使用入口 | 文档、项目类工具起步 |
| `onboard-progressive-disclosure` | 默认只露主路径,高级项按需展开;主功能配内联文档 | 功能多但首启只需少数路径 |
| `onboard-lazy-registration` | 先体验后注册,触发保存/分享时才要求账号 | 免注册试用 |
| `onboard-import` | 第三方导入向导 + 字段映射 + 导入进度反馈 | 竞品切换场景,降低重建数据的成本 |
| `onboard-feature-announcement` | 新功能焦点公告,一次性展示、可忽略 | 老用户的功能上新 |

> 注:本表是"模式命名",不负责引导浮层的出入场动效;模态阻断式浮层(注册墙、首启弹窗)的链路设计见 [`popups.md`](popups.md)。

## 使用规则

- 引导的目的是让用户尽快完成第一个有价值动作,不是功能说明书:上下文内提示比强制教程更有效(实证),首启要求快速直达
- 优先顺序:上下文 coach-mark > 空态内引导(见 [`states.md`](states.md))> 分步 tour > 欢迎屏;能不阻断就不阻断
- tour 与 coach-mark 必须可跳过/可关闭;引导是可选项,须与基础空态并存
- 与 [`popups.md`](popups.md) 分工:模态阻断浮层走 popups.md 的弹窗链路;本表 coach-mark/tour 是页内锚定提示,不进入浮层链路
- 示例数据必须有"示例"标记与清空出口,并保留基础空态兜底
- 同一首启流程引导模式 ≤ 2 种、清单项 ≤ 5;principles 第 14 定律要求四类状态完整,引导不能替代 Loading/Empty/Error 兜底
- 空态插画策略见 [../meta/visual-assets.md](../meta/visual-assets.md);引导文案写法见 [../meta/content-guide.md](../meta/content-guide.md)

### 请求时机(权限/评分/tip)

- **权限请求先给理由**:请求通知/定位/摄像头等授权前,要么并入引导流程说明"为何需要+给什么好处",要么推迟到用户首次使用该功能的那一刻;禁止启动即索权——场景化请求让用户在理解价值后做决定
- **评分请求看参与度**:只在用户展示出参与度后(完成关键任务/达成里程碑)请求评分;首次启动与引导期间禁止;找自然停顿点,不打断进行中任务;频控:两次请求间隔 ≥1-2 周
- **tip 有资格与频控**:按参数/事件判定展示资格(用过该功能的人不再展示),节奏如每 24 小时一次;功能超过 3 步就不适合 tip(改走 tour/文档);tip 1-2 句、动词开头、禁推广内容
- **教程跳过但不消失**:用户跳过的教程不再自动弹出,但在帮助/设置区保持可达
- **splash 只放引导开头**:需要 splash 屏时放在 onboarding 流程开头(无 onboarding 才在启动后首屏);启动屏禁文字、须与首屏几乎一致防闪变
- **授权被拒后的处置三禁令**:禁止拒绝授权后闪退/强制退出;禁止重复弹框纠缠;用户再次触发该功能时给"前往设置"的开启引导;单个流程内连续授权弹框不超过 2 个
- **引导文案字符预算**:标题 ≤10 字符,辅助文本 22 字符以内为佳、44 字符上限——引导文案是扫读不是阅读
- **tour 步数 3-7 步**:超 7 步的引导该拆页或改 coach-mark;回访用户永不再见首启引导(seen-state 尊重 dismiss)

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
