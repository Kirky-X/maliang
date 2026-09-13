# 模板墙（Template Wall）

> 可直接套用的设计语言 / 整页模式模板库。一模板一文件，供 `design-md`(方向选择) 与 `draw-md`(页面规格) 按需取用。与 [`design-systems.md`](../dimensions/design-systems.md) 的分工：design-systems 是"对外锚点"（告诉 AI 对齐哪个既有系统），模板墙是"可执行配方"（token 级参数 + 结构骨架 + 反模式，直接驱动产出）。

## 1. 文件契约（schema）

每个模板一个 `.md`，frontmatter 必填：

```yaml
---
name: <kebab-case-id>          # 全库唯一
title: 中文名
category: design-language      # design-language | page-pattern | landing-pattern | character-direction
status: production             # production(生产级) | style(风格级) | experimental(实验级)
source: <官方来源/出处项目>      # 必须可溯源；禁止"网上看到的"
era: <年份/版本>
verified: <YYYY-MM-DD>         # 最后人工核验日期；超 365 天须复核或降级
variance: "3-8"                # dials VARIANCE 适配区间
motion: "2-7"                  # dials MOTION 适配区间
density: "2-8"                 # dials DENSITY 适配区间
platforms: <适用平台>
---
```

正文 7 节（顺序固定）：**一句话定位 → 视觉特征（token 级参数）→ 结构骨架 → 适用场景/慎用场景 → AI 常见翻车点（反模式）→ CSS 关键实现（≤15 行）→ 来源链接**。风格级模板须在"AI 常见翻车点"节显式列出绝对负面约束（禁用元素/配色/组合）。category 级合集文件（landing-patterns / character-directions 等）不受单模板正文契约约束，遵循其自身章节结构。来源链接中的 `temp/...` 路径（视频研究/参考项目）以**仓库根**为基准指路，不作 markdown 相对链接解析。

## 2. 分类体系

| category | 内容 | 数量 |
| --- | --- | --- |
| `design-language` | 完整设计语言（液态玻璃、Fluent 2、瑞士编辑排版…） | 见 [INDEX.md](INDEX.md) |
| `page-pattern` | 整页级模式（编辑分栏型、纵深长廊型、Dashboard 原型…），源自视频研究与实战案例 | 同上 |
| `landing-pattern` | 落地页章节编排 + CTA 策略（[landing-patterns.md](landing-patterns.md)） | — |
| `character-direction` | 性格方向卡（精密密度 / 温暖亲和…，与 product-reasoning 产品类型正交的第二轴） | — |

## 3. 选型路由（四步，进入 design-md 方向阶段时执行）

1. **先判模式**：该页面为谁的成功服务？查 [`surface-modes.md`](../meta/surface-modes.md)（Persuade/Operate/Read/Experience），模式决定候选池。
2. **dial 匹配**：模板 frontmatter 的 variance/motion/density 区间必须覆盖当前项目 dials 值，不覆盖则换模板（禁止"选了再硬掰档位"）。
3. **轴组合查重**：过一遍 [`variation-engine.md`](variation-engine.md)，确保与最近项目不在同一组合；"能从品类猜出你的选型 = 自检失败"。
4. **一项目一主语言**：选定后整页贯彻；互斥模板不得混用（`glassmorphism` 与 `apple-liquid-glass` 语义不同，二选一）。

## 4. 治理规则

- **来源可溯**：无 `source` 的条目不得入库；数值参数必须有出处（官方文档 / 案例实测 / 视频研究转写）。
- **状态语义**：`production` 可直接上生产；`style` 须先匹配品牌气质、勿与系统级语言混搭；`experimental` 上生产前必须过可访问性审查（WCAG AA）。
- **废弃重定向**：过时条目不删除，frontmatter 加 `replaced-by: <id>`，正文首行标注"已废弃，见 xxx"（防断链、防模型"以防万一"复用旧模板）。
- **新增门禁**：新条目必须字段齐全 + 反模式节非空 + 与既有条目查重（避免同质条目膨胀）。
- **覆盖关系**：模板值是"默认建议"，项目 DESIGN.md 的 token 可覆盖；冲突时以 DESIGN.md 为准（SOT 唯一）。

## 5. 与 ai-tells 的联动

每个模板的"AI 常见翻车点"节是该模板语境下的专属反模式；通用反 AI 味黑名单仍在 [`ai-tells.md`](../meta/ai-tells.md)。两者冲突时，模板语境内的特化规则优先。
