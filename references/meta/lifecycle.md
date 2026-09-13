# UIUX 全生命周期地图（Lifecycle Map）

> 规范层。maliang 负责 UIUX 全生命周期的总图：七段（研究 → 定义 → 设计 → 实现 → 验证 → 交付 → 迭代），每段给出目标、载体（子命令 × 参考文件 × 产物）与出口检查点。跨段裁决仍以 [`rules-priority.md`](rules-priority.md) 与 [`philosophy.md`](philosophy.md) 为准。2026-09 建立轮廓：研究/定义段吸收自 impeccable（PRODUCT 层 + 领域探索）、interface-design（Signature/提案块），验证段吸收自 impeccable（critique 协议）与 ui-ux-pro-max（动态审计/交付清单），迭代段吸收自 interface-design（决策账本）与 taste-skill（SEO/埋点基线）。

## 七段总览

| 段 | 目标（回答什么） | 主要载体 | 关键产物 | 出口检查点 |
| --- | --- | --- | --- | --- |
| 1 研究 Research | 产品世界是什么？谁在用？ | `design-md` Phase 0a 领域探索（Domain/Color world/Signature/Defaults 四产出 + 用户三产出/竞品拆解/信息架构前置草案）+ [`product-reasoning.md`](product-reasoning.md) 类型校准 | 领域四产出、安静约束声明（无障碍/强监管/儿童等覆盖审美） | "把产品名删掉还能认出它是做什么的？" |
| 2 定义 Define | 设计立场与约束是什么？ | `design-md` Phase 0c Suggest+Ask 提案块 + [surface-modes.md](surface-modes.md) 页面模式 + [dials.md](dials.md) + [templates/variation-engine.md](../templates/variation-engine.md) 七轴组合 | DESIGN.md（含 decisions 账本、schema 戳）+ 组合声明 + 性格方向（[character-directions](../templates/character-directions.md)） | 提案块经用户确认；"读起来像情绪 = 方向还没定" |
| 3 设计 Design | 每页具体怎么搭？ | `draw-md`（方向契约块 + 组件意图头）+ [templates/](../templates/INDEX.md) 模板墙选型 + [landing-patterns](../templates/landing-patterns.md) + 术语库 | ui-markdown 页面规格（token 硬引用） | 契约四字段非空；dial 区间与模板匹配 |
| 4 实现 Implement | 代码怎么落地？ | `draw-harmony` / `draw-flutter` / `draw-element` + [framework/](../framework/index.md)（复用阶梯：原生 → headless → 手搓须带行为契约） | 三框架代码 | 无结构性 hack；完整交互状态（第 14 定律） |
| 5 验证 Validate | 效果对不对？好不好用？ | `preview`（13 项脚本检查 + 113 项 Pre-Flight 清单（约 49/113 可脚本化）+ 推定阻断项 + squint test + 捕获有效性）+ `critique`（Nielsen 评分 + persona 走查 + 任务脚本走查 + 认知负荷 + 五秒测试 + A11y 实测记录模板）+ [ai-tells.md](ai-tells.md)（含第 10 节生产测试 Tells） | 预览验证报告、critique 评分快照、A11y 实测记录 | 无推定阻断项命中；MOTION>4 有真实动画（档位兑现） |
| 6 交付 Deliver | 怎么交出去？ | [preview-checklist.md](../commands/preview-checklist.md)（唯一 canonical 清单：Process 动态实测区 + 完备性 6 项）+ 报告文风（[content-guide.md](content-guide.md) 文案自检） | 交付包 + 已勾选清单 | Process 区实测全过；清单为全流水线唯一 |
| 7 迭代 Iterate | 怎么持续变好不漂移？ | `redesign`（9 维审计 / Refresh·Restructure·Rebuild·Deslop / 折中禁令 / 根因四分类 / SEO·追踪维度）+ 埋点基线比对（[analytics-events.md](analytics-events.md)）+ `ui-graph`（哈希基线/实现映射）+ decisions 账本回写 | 改版方案、更新后的 DESIGN.md/ui-markdown、ui-relationships.json | 新决策已提议写入 decisions；SEO/埋点基线未破坏 |

## 段间交接物（下游输入 = 上游产物）

```
研究(领域四产出) → 定义(DESIGN.md + dials + 组合声明) → 设计(ui-markdown)
  → 实现(框架代码) → 验证(验证报告 + critique 快照) → 交付(清单)
  → 迭代(改动回流 DESIGN.md decisions + ui-graph 哈希基线) ↺ 回到设计/定义
```

- 无 DESIGN.md 时严禁跳到 3/4 段（SKILL.md 路由 🔴 CHECKPOINT）。
- 迭代段的新决策一律走 decisions 账本——"哈希记忆回答变了什么，Decisions 记忆回答为什么是这样"。

## 覆盖对照（子命令 × 阶段）

| 子命令 | 段 |
| --- | --- |
| design-md（创建/应用/验证/导出 + Phase 0a/0c + decisions） | 1 · 2 · 7 |
| redesign（审计 + 三模式 + Deslop + SEO 维度） | 7 · 1（重设计时补研究） |
| draw-md（方向契约 + 组件意图 + 模板墙选型） | 3 |
| preview（静态检查 + 推定阻断 + 捕获有效性） | 5 · 6 |
| critique（Nielsen 评分 + persona 走查） | 5 |
| draw-harmony / draw-flutter / draw-element | 4 |
| ui-graph（关系 + 哈希 + 实现映射） | 7 |
| ip / ip-handbook（IP 形象与视觉手册） | 2 · 3（品牌资产） |

## 资产治理（全生命周期共用）

术语库 / 模板墙 / 设计规范三大资产的治理规则见 [`templates/README.md`](../templates/README.md) §4：来源可溯、verified 日期、状态语义（production/style/experimental）、废弃重定向不删除、新增门禁。条目超 365 天未复核须降级或重验。
