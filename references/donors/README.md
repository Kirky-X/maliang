# 供体层（Donors）—— 可偷值的品牌设计档案

> 供体层是"写码前先偷"的**具体数值库**:每个文件记录一家真实产品站点的可偷值(hex / 字重 / 字距 / 阴影栈 / OpenType / 圆角刻度 / 交互位移等),粒度到具体值,来源可溯。
> 与另两层分工:[`../dimensions/design-systems.md`](../dimensions/design-systems.md) 是**对外锚点**("本设计对齐哪个系统");[`../templates/`](../templates/README.md) 是**可执行配方**(模板墙);供体层是**值仓库**——只借值,不借外观。
> 来源:styleseed 仓的 design-systems 索引 + craft-loop 偷值纪律,2026-10 吸收;值核读自 awesome-design-md 库(qiaomu-design 仓的 design-systems 库收录),措辞自著。

---

## 1. 文件契约（schema）

每个供体一个 `.md`，frontmatter 沿用 [`../templates/README.md`](../templates/README.md) 的前置字段契约（`category: donor` 为供体层取值，已登记进模板墙 README §2 分类表）：

```yaml
---
name: <kebab-case-id>          # 全库唯一,如 linear
title: <站点名>
category: donor                # 供体层取值(模板墙枚举以 templates/README.md 为准)
status: production             # production | style | experimental(语义同模板墙)
source: <站点 URL + 采样库注记> # 必须可溯源;禁止"网上看到的"
era: <采样年份>
verified: <YYYY-MM-DD>         # 最后人工核验日期;超 365 天须复核或降级
variance/motion/density        # 站点实测气质折算的 dial 参考区间(见 §4 注)
platforms: <适用平台>
---
```

## 2. 正文 9 节（顺序固定）

视觉主题与氛围 → 色板与角色 → 排版规则 → 组件样式 → 布局原则 → 深度与海拔 → Do's and Don'ts → 响应式 → Agent Prompt Guide。

- 每节必须给**到具体值**:hex、字号-字重-行高-字距四元组、多层阴影栈、OpenType feature、圆角刻度、hover 位移量——不给"高级感""克制"式形容词结论
- 写不清具体值的节写"本项无稳定值",不编

## 3. 偷值纪律（怎么用）

写码前、方向确定后,从本目录挑 **1-2 个气质最接近站点**作为供体,提取 **3-5 个具体值或动作**写进设计计划,并逐条写明「**从 {site} 偷了什么**」:

- 不是"参考 Linear 的感觉",而是"偷 Linear 的 510 签名字重与 -1.056px@48px 显示字距","偷 Stripe 的蓝调多层阴影栈 `rgba(50,50,93,0.25) 0px 30px 45px -30px, rgba(0,0,0,0.1) 0px 18px 36px -18px`"
- 可偷的东西:阴影体系 / 圆角刻度 / 字阶比例 / 字重与字距策略 / hover 位移与过渡方式 / 边框策略 / 用色分配 / 留白节奏
- **写不出「从谁偷了什么」= 没偷,重来**——这条与 [`../interface-design/craft-discipline.md`](../interface-design/craft-discipline.md)「Steal Values, Not Looks」节互为执行与判据
- **只偷值,不复制品牌外观**:不得整站照搬(与 design-systems.md 的「禁止照搬」同源);品牌识别元素(logo / 吉祥物 / 专属字形 / 标志性插画)不偷——它们不是值,是身份
- 偷来的值进入本项目时仍须回 design-md 走 token 与溯源通道(补决策 id 或 `no-decision`),不绕过设计系统

## 4. 首批供体索引

| 供体 | 气质 | 最适配 | 文件 |
| ---- | ---- | ------ | ---- |
| Linear | 暗色原生精密工程:近黑画布 + 单色强调 + 签名字重 510 | 开发者工具 / 事务追踪 / 数据密集 Operate 界面 | [linear.md](linear.md) |
| Vercel | 工程静默:纯白画廊 + shadow-as-border + 压缩大字 | 开发平台 / 文档站 / 极简 Persuade 首页 | [vercel.md](vercel.md) |
| Stripe | 金融精致:浅字重大标题 + 蓝调染色阴影 + 表格数字 | 支付 / 金融科技 / 数据与图表密集页 | [stripe.md](stripe.md) |
| Raycast | 桌面原生暗色:蓝调近黑 + inset 高光阴影 + 正字距正文 | 启动器 / 效率工具 / 桌面应用站 | [raycast.md](raycast.md) |

> `variance/motion/density` 是**编者按站点实测特征折算的气质参考区间**(非官方参数、非选型约束):用于四步路由做气质初筛,选型仍以项目 dials 为主;供体只提供可偷值,不承担模板墙的 dial 匹配职责。

## 5. 维护规则

- **来源可溯**:无 `source` 的条目不收录;数值必须来自可复核的采样(样式表 / computed styles / 公开 design 文档),禁止凭印象
- **核验时效**:`verified` 超 365 天须复核或降级;站点改版后旧值标 `status: style` 或注明"历史值,以当前站点为准"
- **增强条件**:新增供体须 ① 与首批气质轴不重复(暗 / 亮 / 工具 / 内容至少一轴不同)② 9 节能写到具体值 ③ 与既有供体查重(避免同质)
- 候选池:awesome-design-md 库收录的 58 站均可按上述条件晋升;不做"整库平移",逐家按需收录
