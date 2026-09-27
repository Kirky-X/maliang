---
name: landing-patterns
title: 落地页编排模式
category: landing-pattern
status: production
source: ui-ux-pro-max-skill data/landing.csv（34 模式精选 18 条中文化）
era: 2026
verified: 2026-09-07
variance: "2-8"
motion: "1-7"
density: "2-8"
platforms: Web
---
# 落地页编排模式（Landing Patterns）

> 整页"章节序列 + 主 CTA 位置 + 转化优化"速查表。`draw-md` 排营销/落地页时先查此表定骨架，再由设计语言模板定皮肤。字段：章节顺序｜主 CTA 位置｜转化要点。

## 精选 18 模式

| # | 模式 | 章节顺序 | 主 CTA 位置 | 转化要点 |
| --- | --- | --- | --- | --- |
| L01 | Hero+特性+CTA | Hero > 特性 > 定价 > CTA > Footer | Hero 与定价后各一 | 万金油；特性 ≤3 组，每组一图 |
| L02 | Hero+证言+CTA | Hero > 证言 > 特性 > CTA | 证言墙后 | 证言带真实头像/公司；禁 20 行文字墙 |
| L03 | 产品演示先行 | Demo > 特性 > 定价 > CTA | Demo 内嵌 | 首屏即"看到产品"；截图必须真实 UI |
| L04 | 极简单列 | Hero > 3 段价值 > CTA | 每段末 | 适合单功能工具；全页 <5 屏 |
| L05 | 三步漏斗 | Hero > 步骤 1-2-3 > CTA | 步骤后 | 步骤编号即视觉锚；每步一动词 |
| L06 | 对比表+CTA | Hero > 对比表 > FAQ > CTA | 表格后 | "我们 vs 他们"列 ≤5 行才有可读性 |
| L07 | 领奖诱饵+表单 | Hero > 诱饵展示 > 表单 | 表单按钮 | 表单字段 ≤3；说明兑换物价值 |
| L08 | 定价页 | Hero(一句话) > 价格卡 ×3 > FAQ > CTA | 中间档卡内 | 中间档高亮"最受欢迎" |
| L09 | 视频首屏 | Video Hero > 特性 > CTA | 播放器旁 | 封面帧即高潮；提供静音字幕 |
| L10 | 滚动叙事 | 固定视觉 + 滚动推进章节 | 每章节末 | 一屏一观点；进度指示器 |
| L12 | 候补/即将上线 | Hero > 价值预告 > 邮箱表单 | 邮箱按钮 | 展示已注册人数/倒计时 |
| L15 | 应用商店式 | 手机样机 > 功能滑动 > 评分 > 下载 | 粘性底栏 | 样机随章节切换屏幕 |
| L18 | 活动/大会 | Hero(日期地点) > 议程 > 讲者 > 票务 | 票价卡 | 议程可折叠；讲者真实照片 |
| L21 | Before-After | Hero > 前后对比 > 数据 > CTA | 对比后 | 滑块对比组件；数字用等宽字 |
| L25 | 企业门户 | Hero(价值宣言) > 方案分区 > 案例 > 联系 | 预约演示 | 分区按角色/行业二选一 |
| L28 | Bento 展示 | Hero > Bento 网格特性 > CTA | 网格后 | 大格一主题小格一点缀（见 bento-grid 模板） |
| L33 | 信任与权威 | Hero > Logo 墙/奖项 > 案例 > CTA | 案例后 | Logo 墙用真实 SVG（见 [visual-assets.md](../meta/visual-assets.md)） |
| L34 | 实时运营 | 状态墙 > 实时数据 > 异常入口 | — | 数字自动刷新；降级显示最后快照时间 |

## 营销页转化要素构成表

> 供 `draw-md` 生成营销页作必备元素依据、供 `critique` 查漏（来源：landing-page-guide-v2，2026-09 吸收）。编排选上面的 L 编号，本表管每个要素内部"必须有什么"。

**Testimonial 证言** —— 每条 5 字段：真人头像｜全名｜公司与职位｜一句可验证的结论（带具体数字）｜使用场景（用什么功能解决了什么问题）。4 条筛选标准，不满足不上墙：①结论可验证（有数字 / 结果，非"很棒"式空评）；②身份可溯（头像与公司可查，占位头像即 ai-tells，见 [visual-assets.md](../meta/visual-assets.md)）；③与本页卖点对应（每条消解一个具体顾虑）；④长度 ≤ 2 行（长文折叠进案例页）。冷启动无真实证言时禁造假——留位待补或以产品演示替代（见 [copy-strategy.md](../meta/copy-strategy.md) 社会证明分支）。

**FAQ** —— 5 类必覆盖：①价格与计费（怎么收 / 能否退）；②技术对接（集成 / 迁移 / 数据安全）；③产品边界（不做什么 / 适合谁）；④对比疑虑（vs 竞品 / vs 自建）；⑤售后支持（服务 / SLA / 联系入口）。每问答 ≤ 3 行，答不完链到详情页；FAQ 放最终 CTA 之前——先拆顾虑再要行动。

**Social proof** —— 5 类素材按可信度递增，取 2-3 类即可：客户 Logo 墙（真实 SVG，见 commerce `social-proof-logos`）｜用量数字（真实可溯）｜证言（按上表）｜权威背书（奖项 / 媒体 / 认证——无可验证证据禁写"获奖"，见 [ai-tells.md](../meta/ai-tells.md)）｜可点入的完整案例。

**Final CTA 风险消除** —— 按钮周围放消除下单风险的要素：免费试用 / 随时取消｜无需绑卡｜退款政策一句话｜隐私承诺。CTA 文案延续页内叙事（按钮文案是标题的下一句，策略见 [copy-strategy.md](../meta/copy-strategy.md)）；紧迫感使用受 [commerce.md](../vocabulary/commerce.md) 约束——每页至多一种紧迫信号且必须真实，本表不重复定义。

**Footer 法规** —— 按受众与司法域取必需项：ICP 备案号（中国大陆上线必挂，链工信部备案系统）｜服务条款｜隐私政策｜Cookie 声明（GDPR 受众）｜版权行｜联系方式。条款与政策页必须真实存在可点开，死链 / 占位链接即 ai-tells。

**URL** —— 正例：`/pricing`、`/free-trial`、`/features/analytics`（短、小写连字符、语义可读）；反例：`/page?id=8829`（参数串）、`/final-v3-new`（版本残渣）、`/Index2`（大小写混乱）。URL 是投放落地参数的基底，改版禁改 slug（见 [redesign.md](../commands/redesign.md) 第 6 节永不静默改动清单）。

## 使用规则

1. 先按产品目标选模式（转化 / 注册 / 下载 / 品牌再选 L 编号），再套设计语言模板定视觉。
2. 章节序列是"默认序"，可根据 brief 增删但不得打乱"价值 → 证据 → 行动"三段逻辑。
3. 主 CTA 全页唯一主色；次级 CTA 降级为描边样式。
4. 每个模式配 `ai-tells` 自检：章节编号眉标、装饰性状态点、"Scroll to explore" 提示均为禁项（见 ai-tells.md 第 10 节）。
5. **双轴验收**：每个转化要素同时过「功能有效（推进转化）+ 设计卓越（值得记住）」两关，只过一关即不合格——要素构成表管"必须有什么"，验收管"必须两关都过"；此为页面级验收，与 `draw-md` intent 字段的组件级定位区分。
6. **文案层挂接**：Persuade 场景下 headline / feature / CTA 的写法策略见 [`../meta/copy-strategy.md`](../meta/copy-strategy.md)（要素构成表管"必须有什么"，文案策略管"怎么说"；来源：landing-page-design，2026-09 吸收）。
