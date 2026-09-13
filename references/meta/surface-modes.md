# Surface Modes 访客模式 —— Persuade / Operate / Read / Experience

> 规范层。四轴"访客模式"回答一个问题：**这个页面为谁的成功服务？** 模式按 surface（页面）选择而非按项目选择——工具的落地页仍是 Persuade，时尚屋的文档仍是 Read。模式级联校准色彩默认、字体口味、动效容忍度与审计侧重。来源：impeccable SKILL Modes 节，2026-09 吸收。

## 使用时机

`draw-md` 产出页面前、`redesign` 审计开始前，先判当前页面模式并在页面规格头部标注一行：`mode: operate`。模式只影响该页面，不写进 DESIGN.md 全局。

## 四模式定义

| 模式 | 访客的成功是什么 | 典型页面 | 色彩默认 | 字体口味 | 动效容忍 |
| --- | --- | --- | --- | --- | --- |
| **Persuade** 说服 | 被打动并采取行动（注册/购买） | 落地页、营销首页、活动页 | 允许 Committed/Drenched 高承诺色彩 | 展示体可用，标题有个性 | 中高：入场 + 滚动揭示 |
| **Operate** 操作 | 快速完成任务并离开 | 后台、设置、工作台、管理 | Restrained：中性 + 单强调 | UI sans，正文 ≥14px | 低：状态过渡即可，装饰动画禁 |
| **Read** 阅读 | 舒适吸收长内容 | 文档、文章、帮助中心 | Restrained；正文对比度优先 | 衬线/人文 sans 正文，行长 60-75ch | 极低：仅链接/目录反馈 |
| **Experience** 沉浸 | 获得体验与情绪 | 品牌站、展览、作品集 | 自由（四阶梯任一） | 表现力优先 | 高：滚动叙事、视差、转场 |

## 级联校准表（模式 → 规则侧重）

| 规则域 | Persuade | Operate | Read | Experience |
| --- | --- | --- | --- | --- |
| 首屏焦点 | 价值主张必须赢 | 当前任务必须赢 | 标题 + 目录必须赢 | 情绪构图必须赢 |
| CTA 密度 | 每屏 1 主 CTA | 工具栏常驻 | 少量（下一页/复制） | 可无 CTA |
| 信息密度 dial 建议 | 3-5 | 6-9 | 4-6 | 1-4 |
| ai-tells 豁免 | 营销修辞可用 | 严格禁修辞 | 禁营销修辞 | 修辞即内容 |
| 审计加权 | 品牌/转化/首屏 | 效率/状态/错误恢复 | 可读性/行宽/导航 | 构图/动效/记忆点 |
| 深度策略默认（四选一，详见 [`../dimensions/elevation.md`](../dimensions/elevation.md)） | subtle-shadows | borders-only 或 subtle-shadows | borders-only | 任一，但全站唯一 |
| Nielsen 评审 n/a 项 | 错误预防可降权 | 情绪化项降权 | 转化项 n/a | 效率项降权 |

## 强制规则

1. **模式决定"好"的定义**：Operate 页做出"安静高效"是对的；把 Operate 页的审美术语（不够惊艳）套到它头上是类别错误。
2. **一页一模式**：页面主体模式唯一；混合页（营销 + 文档）按主区块拆分判定。
3. **与 dials 正交**：模式是"页面类型轴"，dials 是"强度轴"；Operate 也可以高密度、Experience 也可以低动效。
4. **与性格方向联动**：见 [`templates/character-directions.md`](../templates/character-directions.md)，模式约束下限，性格决定气质。
