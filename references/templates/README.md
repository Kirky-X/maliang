# 模板墙（Template Wall）

> 可直接套用的设计语言 / 整页模式模板库。一模板一文件，供 `design-md`(方向选择) 与 `draw-md`(页面规格) 按需取用。与 [`design-systems.md`](../dimensions/design-systems.md) 的分工：design-systems 是"对外锚点"（告诉 AI 对齐哪个既有系统），模板墙是"可执行配方"（token 级参数 + 结构骨架 + 反模式，直接驱动产出）。

## 1. 文件契约（schema）

每个模板一个 `.md`，frontmatter 必填：

```yaml
---
name: <kebab-case-id>          # 全库唯一
title: 中文名
category: design-language      # design-language | page-pattern | landing-pattern | character-direction | donor
status: production             # production(生产级) | style(风格级) | experimental(实验级) | unverified(未验证/待复核)
source: <官方来源/出处项目>      # 必须可溯源；禁止"网上看到的"
era: <年份/版本>
verified: <YYYY-MM-DD>         # 最后人工核验日期；超 365 天须复核或降级
variance: "3-8"                # dials VARIANCE 适配区间
motion: "2-7"                  # dials MOTION 适配区间
density: "2-8"                 # dials DENSITY 适配区间
platforms: <适用平台>
---
```

正文 9 节（顺序固定）：**一句话定位 → 视觉特征（token 级参数）→ 结构骨架 → 签名动作（带配额）→ 适用场景/慎用场景 → AI 常见翻车点（反模式）→ 共享尾件轮换表 + 非色彩杠杆 → CSS 关键实现（≤15 行）→ 来源链接**。风格级模板须在"AI 常见翻车点"节显式列出绝对负面约束（禁用元素/配色/组合）。category 级合集文件（landing-patterns / character-directions 等）不受单模板正文契约约束，遵循其自身章节结构。来源链接中的 `temp/...` 路径（视频研究/参考项目）以**仓库根**为基准指路，不作 markdown 相对链接解析。

两处主题级深化节（#16，源自 hallmark hum.md 机制，2026-10 吸收）：

- **签名动作**：定义该模板 5-7 个「母题动作」（该语言页面必现的可复用单元），逐个给**配额**（每页限用几处）；产出至少满足其中六个，产品主导页可豁免「性格时刻」一项。关键件给出 **canonical CSS 正本**——全库逐字复用、各构建不得即兴重写（防坏实现逐构建扩散）；canonical CSS 是正本库，不占「CSS 关键实现 ≤15 行」的首屏锚点预算。
- **共享尾件轮换表 + 非色彩杠杆**：定价 / 证言 / 页脚等「共享尾件」**逐构建轮换**——同一模板的两个构建，后半页不得同构（三档定价、三卡证言只是选项之一，不是默认），尾件每个槽位给 ≥3 个候选形状并声明「上一构建：X。本构建：Y，因为 Z」。再配一组**与配色无关**的杠杆（hero 原型、强调手法、特性块形状、密度节奏、容器物理、接缝语言、明暗/灰度分布、装饰剂量、动效 register）逐构建换组合——换调子先换结构，色板只是最后一层。原型候选从 [`../components/INDEX.md`](../components/INDEX.md) 挑名；构建级「每构建一个 off-grid 时刻 + 一个 designed exception」硬要求见 [`variation-engine.md`](variation-engine.md)。

## 2. 分类体系

| category | 内容 | 数量 |
| --- | --- | --- |
| `design-language` | 完整设计语言（液态玻璃、Fluent 2、瑞士编辑排版…） | 见 [INDEX.md](INDEX.md) |
| `page-pattern` | 整页级模式（编辑分栏型、纵深长廊型、Dashboard 原型…），源自视频研究与实战案例 | 同上 |
| `landing-pattern` | 落地页章节编排 + CTA 策略（[landing-patterns.md](landing-patterns.md)） | — |
| `character-direction` | 性格方向卡（精密密度 / 温暖亲和…，与 product-reasoning 产品类型正交的第二轴） | — |
| `components` | 区段级编码原型（导航 14 / hero 9 / 区段头 5 / 主体 6 / CTA 4 / 证言 4 / 页脚 8），从索引挑名、只加载选中的那几个（[INDEX.md](../components/INDEX.md)）；原型含变体旋钮，供 [variation-engine.md](variation-engine.md) 盖章扩 knob | 见 components/ |
| `donor` | 品牌供体值库（Linear / Vercel / Stripe / Raycast…「偷值不偷感觉」，见 [donors/README.md](../donors/README.md)） | 见 donors/ |

## 3. 选型路由（四步，进入 design-md 方向阶段时执行）

1. **先判模式**：该页面为谁的成功服务？查 [`surface-modes.md`](../meta/surface-modes.md)（Persuade/Operate/Read/Experience），模式决定候选池。
2. **dial 匹配**：模板 frontmatter 的 variance/motion/density 区间必须覆盖当前项目 dials 值，不覆盖则换模板（禁止"选了再硬掰档位"）。
3. **轴组合查重**：过一遍 [`variation-engine.md`](variation-engine.md)，确保与最近项目不在同一组合；"能从品类猜出你的选型 = 自检失败"。
4. **一项目一主语言**：选定后整页贯彻；互斥模板不得混用（`glassmorphism` 与 `apple-liquid-glass` 语义不同，二选一）。

## 4. 治理规则

- **来源可溯**：无 `source` 的条目不得入库；数值参数必须有出处（官方文档 / 案例实测 / 视频研究转写）。
- **状态语义**：`production` 可直接上生产；`style` 须先匹配品牌气质、勿与系统级语言混搭；`experimental` 上生产前必须过可访问性审查（WCAG AA）；`unverified`（未验证 / 待复核）是**正式状态**——条目可以入库但未达 production，使用时必须在产物中标注该状态，不得静默当 production 用。
- **晋升规则（升 `production` 前必须全部满足）**：① **≥2 个独立参照集**（两个互不相关的来源都指向同一套值，不是同一来源的复述）；② **明确反例**（写清这套值在什么页面 / 什么内容下不适用）；③ **≥2 类页面渲染样本**（至少在两类不同页面类型上渲染验证过，如营销页 + 工作台）；④ **回归检查**（升级后重跑既有检查，确认未把已批准的项目值改回默认）。四条件缺一不得升 production；未达标的一律标 `unverified` 或 `experimental`。
- **证据时效**：「历史证据不得当作新主张」——旧日期的验证记录只证明当时的状态，改过值 / 换过来源 / 超过 365 天的，须重新核验并把 `verified` 更新到新日期，不得沿用旧证据支撑新主张。
- **废弃重定向**：过时条目不删除，frontmatter 加 `replaced-by: <id>`，正文首行标注"已废弃，见 xxx"（防断链、防模型"以防万一"复用旧模板）。
- **新增门禁**：新条目必须字段齐全 + 反模式节非空 + 与既有条目查重（避免同质条目膨胀）；入库时即标真实状态，未验证的不得先标 production 再补证。
- **覆盖关系**：模板值是"默认建议"，项目 DESIGN.md 的 token 可覆盖；冲突时以 DESIGN.md 为准（SOT 唯一）。

## 5. 与 ai-tells 的联动

每个模板的"AI 常见翻车点"节是该模板语境下的专属反模式；通用反 AI 味黑名单仍在 [`ai-tells.md`](../meta/ai-tells.md)。两者冲突时，模板语境内的特化规则优先。
