---
name: character-directions
title: 六种性格方向
category: character-direction
status: production
source: interface-design README「Design Directions」+ system 示例转写
era: 2026
verified: 2026-09-07
variance: "2-9"
motion: "1-7"
density: "2-9"
platforms: 全平台
---
# 性格方向卡（Character Directions）

> 与 `product-reasoning.md` 的产品类型轴**正交**的第二选型轴：产品类型回答"这是哪类产品"，性格方向回答"它给人的感觉"。选型公式：`产品类型 × 性格方向 → 模板墙与 dials 取值`。两份完整对照样例见 interface-design `reference/examples/system-precision.md`（精密）与 `system-warmth.md`（温暖）。

## 六方向

| 方向 | 感觉 | 适用品类 | dials 建议 (V/M/D) | 字族策略 |
| --- | --- | --- | --- | --- |
| **Precision & Density** 精密密度 | 紧凑、技术感、近单色 | 开发者工具、管理后台 | 3-5 / 1-3 / 7-9 | 等宽字体做数据；UI sans 小号 |
| **Warmth & Approachability** 温暖亲和 | 宽松间距、软阴影、圆角 | 协作工具、消费应用 | 5-7 / 3-5 / 3-5 | 人文无衬线（圆润端点）；标题可微衬线 |
| **Sophistication & Trust** 成熟可信 | 冷色调、层次深度、克制 | 金融、企业 B2B | 3-5 / 1-4 / 4-7 | 传统衬线标题 + 中性 sans 正文 |
| **Boldness & Clarity** 大胆清晰 | 高对比、戏剧性留白 | 现代看板、数据重产品 | 6-9 / 3-6 / 4-7 | 超粗展示体标题 + 干净 sans 正文 |
| **Utility & Function** 效用功能 | 低饱和、功能密度优先 | GitHub 式工具、文档站 | 2-4 / 1-2 / 6-9 | 系统 UI 字体栈；图标线性统一 |
| **Data & Analysis** 数据分析 | 图表优化、数字先行 | 分析、BI 工具 | 2-5 / 1-3 / 7-10 | tabular-nums 等宽；图表字体独立 token |

## 与既有机制的关系

1. **双轴选型**：product-reasoning 查"类型档案"后，用性格方向校准感觉偏差（同为工具型，Precision 与 Utility 产出不同）。
2. **dials 映射**：每方向的 V/M/D 建议区间是 [`dials.md`](../meta/dials.md) 拨轮的"性格预设"，Design Read 时可与信号推断交叉验证。
3. **模板墙联动**：性格方向决定 design-language 短名单（如 Warmth → claymorphism/soft 系；Sophistication → editorial-swiss/fluent-2；Boldness → neo-brutalism/bento）。
4. **对照样例的启示**（precision vs warmth 同构不同值）：按钮高 32px vs 40px、圆角 4/6/8 锐角 vs 8/12/16 软角、数据用 mono vs 正文统一——**同一种 schema，性格体现在取值**。

## 使用规则

- 一个项目一个主方向，整页贯彻；落地页与后台可共用主方向但允许 D（密度）拨轮相差 ±2。
- 性格方向不是品牌色板；色彩仍由 DESIGN.md 的 color token 与色彩策略阶梯（dimensions/color.md）决定。
