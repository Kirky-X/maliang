# Surface Modes 访客模式 —— Persuade / Operate / Read / Experience / Delegate / Data / Commerce

> 规范层。七模式"访客模式"回答一个问题：**这个页面为谁的成功服务？** 模式按 surface（页面）选择而非按项目选择——工具的落地页仍是 Persuade，时尚屋的文档仍是 Read。模式级联校准色彩默认、字体口味、动效容忍度与审计侧重。来源：impeccable SKILL Modes 节，2026-09 吸收；Delegate 第五模式 Adapted from finesse-ui（MIT），2026-09 吸收；Data/Commerce 第六、七模式据 frontend-design-practicalswan 思想中文自研，2026-09 吸收。

## 使用时机

`draw-md` 产出页面前、`redesign` 审计开始前，先判当前页面模式并在页面规格头部标注一行：`mode: operate`。模式只影响该页面，不写进 DESIGN.md 全局。

## 七模式定义

| 模式 | 访客的成功是什么 | 典型页面 | 色彩默认 | 字体口味 | 动效容忍 |
| --- | --- | --- | --- | --- | --- |
| **Persuade** 说服 | 被打动并采取行动（注册/购买） | 落地页、营销首页、活动页 | 允许 Committed/Drenched 高承诺色彩 | 展示体可用，标题有个性 | 中高：入场 + 滚动揭示 |
| **Operate** 操作 | 快速完成任务并离开 | 后台、设置、工作台、管理 | Restrained：中性 + 单强调 | UI sans，正文 ≥14px | 低：状态过渡即可，装饰动画禁 |
| **Read** 阅读 | 舒适吸收长内容 | 文档、文章、帮助中心 | Restrained；正文对比度优先 | 衬线/人文 sans 正文，行长 60-75ch | 极低：仅链接/目录反馈 |
| **Experience** 沉浸 | 获得体验与情绪 | 品牌站、展览、作品集 | 自由（四阶梯任一） | 表现力优先 | 高：滚动叙事、视差、转场 |
| **Delegate** 代办 | 监督 AI/代理把活干完，随时可介入 | AI 工作台、agent 控制台、运行队列、审批值守页 | Restrained + 显式 `--warn`/`--down` 色槽 | UI sans + 等宽（载荷/数字） | 低：仅状态转场族（R3） |
| **Data** 数据 | 扫描、比较、发现异常后做出判断 | 仪表盘、监控面板、报表中心、看板 | Restrained：中性底 + 语义色只标状态，数据墨水优先 | UI sans + 等宽数字（tabular-nums），单位随数值 | 极低：数值滚动/状态闪烁即可，禁装饰性图表动画 |
| **Commerce** 交易 | 放心完成购买/预约/服务流程 | 商品列表/详情、购物车、结账流、客服/预约服务页 | Restrained：强调色留给价格与主 CTA，促销色克制 | UI sans，价格/库存大号高对比 | 低：加购/支付反馈过渡即可，交易流程中禁干扰动画 |

> **Delegate 判定**：页面上"不是访客、而是别的东西在持续干活"（agent 多步执行 / 队列 / 流式输出 / 中途可失败），用户是监督者而非执行者。它与 Operate 的区别：Operate 的主操作是**访客自己做**，Delegate 的主操作是**批准、停止、纠偏**。落地层见 [`templates/page/ai-console.md`](../templates/page/ai-console.md)。

> **Data 判定**：页面主交互是**看和比较**（发现异常、对比指标、支撑决策），而非改状态——主交互是改状态的是 Operate。判定问句："这个页面成功一次 = 访客做出了一个正确判断吗？"是则 Data。仪表盘里嵌操作（如"重启服务"按钮）不改变整页模式，按主区块拆分处理。
>
> **Commerce 判定**：页面成功 = **一笔交易/服务被放心完成**（找到 → 比较价格与承诺 → 下单 → 支付/预约成功）。它与 Persuade 的区别：Persuade 说服访客"想要"，Commerce 让访客"买得放心"——商品详情页头部种草区可判 Persuade、购买决策与支付区块判 Commerce，按主区块拆分。

### 新旧模式判定边界（防错用）

- **Commerce「防错与恢复」 ≠ Operate「错误恢复」**：Operate 管访客自己操作出错的回退（表单校验、undo）；Commerce 管不可逆交易动作前的确认与中断后的恢复（支付失败可重试不丢单、订单状态可回溯、库存/价格变化明示）。
- **Commerce「防错与恢复」 ≠ Delegate「监督纠偏」**：Delegate 的防错对象是**机器在干活**（停止是一级控件、审批有证据）；Commerce 的防错对象是**访客在花钱**（承诺显式、误触可拦、失败可退）。AI 工作台内嵌交易/数据面板的混合页，一律按强制规则 2「一页一模式 + 主区块拆分」处理，不给整页贴第二模式。
- **模板墙联动**：Data 页选型优先 [`templates/data-dense-dashboard.md`](../templates/data-dense-dashboard.md) 与 [`templates/page/dashboard-styles.md`](../templates/page/dashboard-styles.md)；Commerce 暂无交易专属模板，营销侧编排见 [`templates/landing-patterns.md`](../templates/landing-patterns.md)，交易区块按本模式规则执行。

## 级联校准表（模式 → 规则侧重）

| 规则域 | Persuade | Operate | Read | Experience | **Delegate** | Data | Commerce |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 首屏焦点 | 价值主张必须赢 | 当前任务必须赢 | 标题 + 目录必须赢 | 情绪构图必须赢 | **正在运行的麻烦必须赢**（三时态同屏） | 关键指标与异常必须赢 | 商品与信任要素必须赢 |
| CTA 密度 | 每屏 1 主 CTA | 工具栏常驻 | 少量（下一页/复制） | 可无 CTA | **停止是一级控件，常驻** | 工具栏化（筛选/钻取），无推销 CTA | 关键流程每步 1 主 CTA，单一路径 |
| 信息密度 dial 建议 | 3-5 | 6-9 | 4-6 | 1-4 | 6-9 | 7-10 | 4-7 |
| ai-tells 豁免 | 营销修辞可用 | 严格禁修辞 | 禁营销修辞 | 修辞即内容 | 严格禁修辞;证据必须逐字 | 严格禁修辞；装饰性卡片马赛克即 Tell | 促销修辞仅限营销区块，交易区块禁 |
| 审计加权 | 品牌/转化/首屏 | 效率/状态/错误恢复 | 可读性/行宽/导航 | 构图/动效/记忆点 | 可信度/可中断性/成本可见 | 可扫描性/新鲜度/单位与空错态 | 信任/防错恢复/流程完成率 |
| 深度策略默认（四选一，详见 [`../dimensions/elevation.md`](../dimensions/elevation.md)） | subtle-shadows | borders-only 或 subtle-shadows | borders-only | 任一，但全站唯一 | borders-only | borders-only 或 layered | subtle-shadows |
| Nielsen 评审 n/a 项 | 错误预防可降权 | 情绪化项降权 | 转化项 n/a | 效率项降权 | 情绪化项 n/a | 情绪化项 n/a；美学 flexibility 降权 | 创意/情绪项降权；错误预防与防错**永不降权** |
| 失败形态 | 不可信的承诺 | 低效 | 不可读 | 无记忆点 | **不可信**（审批无证据/失败被藏/停不下来） | **误读**（新鲜度/单位不明、异常被装饰淹没） | **不敢买/买错/中断流失**（信任缺失、支付中断无法恢复） |

## 强制规则

1. **模式决定"好"的定义**：Operate 页做出"安静高效"是对的；把 Operate 页的审美术语（不够惊艳）套到它头上是类别错误。
2. **一页一模式**：页面主体模式唯一；混合页（营销 + 文档）按主区块拆分判定。
3. **与 dials 正交**：模式是"页面类型轴"，dials 是"强度轴"；Operate 也可以高密度、Experience 也可以低动效。
4. **与性格方向联动**：见 [`templates/character-directions.md`](../templates/character-directions.md)，模式约束下限，性格决定气质。
5. **Delegate 叠加而非替代**：AI 工作台 = Operate 的壳 + Delegate 层（运行流/九状态/审批卡/成本回执），见 [`templates/page/ai-console.md`](../templates/page/ai-console.md)；页面标注 `mode: delegate`。
6. **Data 页三要素 + 禁马赛克**：数据必须自带**新鲜度**（最后更新时间/时间范围）、**单位**（数值不离单位）、**范围**（统计口径/时间窗），且空态与错误态同真实数据同等设计（空图 ≠ 空白格子）；严禁为"看起来丰富"拼贴装饰性仪表盘卡片马赛克——每张卡必须回答一个决策问题，答不出的卡删掉。
7. **Commerce 信任结构 + 关键流程最小干扰**：品类结构用访客熟悉的形态（列表/详情/购物车/结账，不自创导航隐喻），价格、运费、退换承诺、库存状态显式呈现；不可逆动作（支付/提交订单）前必须确认、失败后必须可恢复不丢单；结账流程中不插广告、不弹促销、不改布局——干扰即流失。
