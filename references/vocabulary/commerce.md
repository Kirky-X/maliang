# 商业转化与定价模式命名词汇

> 术语库。定价与转化的组件级模式命名:价格卡、计费切换、对比矩阵、社会证明、紧迫感、结账信任。来源:Smashing Magazine《Designing A Better Pricing Page》、Nielsen Norman Group《Comparison Tables》、Baymard Institute(结账 UX 指南与支付安全感研究)、CXL《Creating Urgency》。verified:2026-09-08。

## 命名表

| 模式名 | 视觉特征 | 适用场景 | 关键要点 |
| --- | --- | --- | --- |
| `pricing-tier-cards` | 方案并排成列,左→右由低价到高价,主力档居中 | SaaS 定价页、订阅方案 | 档位过多时换行或分组,禁横向滚动 |
| `pricing-toggle-billing` | 月付/年付分段切换,置于价格表顶部 | 按月/年计费的订阅制 | 默认年付并标注"省 2 个月"类激励 |
| `pricing-feature-matrix` | 方案为列、功能为行,短词 + 勾叉,行间分隔 | 多档细节对照 | 属性须逐档填全,缺失即不如不放 |
| `pricing-highlight-popular` | 主力档底色/描边区分 + 主色 CTA | 三档引导用户选中档 | 位置(居中)与色彩双通道同时高亮 |
| `pricing-enterprise-cta` | 最右独立档,CTA 为"联系销售"非自助购买 | B2B 大客户、定制报价 | 不放价格数字,改放价值描述 |
| `pricing-per-seat` | 单价 × 席位步进器,实时算总价 | 团队版、按人头计费 | 总价早显,并附一条计价规则说明 |
| `pricing-freemium-banner` | 当前档标识 + 差异卖点 + 升级 CTA 横幅 | 免费用户向付费转化 | 一次只推一个升级理由,不堆卖点 |
| `plan-compare-drawer` | 卡内"查看全部功能"展开抽屉/手风琴 | 价格卡信息放不下时 | 用点按展开替代 hover tooltip |
| `social-proof-logos` | 客户 Logo 灰度单行墙,等高排列 | 定价区上下建立信任 | 用真实 SVG Logo,禁灰色占位块 |
| `social-proof-testimonial` | 证言卡:真人头像 + 姓名 + 公司 + 一句结论 | 消除付费顾虑 | 头像与身份必须真实可溯 |
| `urgency-countdown` | 限时倒计时,固定位置贴近 CTA | 闪购、活动票务 | 归零必须真失效,假倒计时毁信任 |
| `scarcity-stock-counter` | "仅剩 X 份 / X of Y"实时递减计数 | 电商库存、限量名额 | 数字须真实,递减本身即社会证明 |
| `checkout-progress` | 步骤条,已完成步可点击回退 | 多步结账、多步开通流程 | 步骤与流程 1:1 映射,禁合并隐藏 |
| `trust-badges` | 支付区独立视觉封装 + 1-2 枚安全标 | 支付表单、结账页 | 安全标放进卡号封装区内,不散放 |
| `sticky-plan-tabs` | 移动端底部粘性档位切换 tab | 移动端定价页 | 底部放置防手指遮挡,代替横滚表 |
| `rating-display` | 星型评分 + 数值 + 评分人数,支持半星精度 | 商品详情、评论列表、商家评分头部 | 星与数值并显;只显星不显数值 = 藏精度 |
| `rating-input` | 评分输入:点击/拖动设星,支持半星,配标签提示(差/一般/好) | 评价提交、服务打分 | 已选值即时回显,提交前可改;无预期不默认预选 |
| `rating-no-score` | 无分控评:不显均分,仅展示评分人数或好评比例 | 评分样本过少、防刷分层场景 | 均分须配最低样本数阈值;异常评分先降级为比例展示 |

> 来源注:`rating-display` / `rating-input` / `rating-no-score` 3 行为**审计补全**(2026-09-08 组件覆盖审计):Ant Design Rate 为一等组件,IBM Carbon 与 Material 3 无原生(生态方案);framework `rate` 类提供控件层支撑。

## 使用规则

- 分工:landing-patterns.md 管整页章节编排(先选 L 编号定骨架),本表管骨架内的组件级定价/转化模式命名
- 价格卡容器样式沿用 [cards.md](cards.md) 的 card-* 变体,本表只命名定价语义,不重复定义容器
- 倒计时与库存计数的数字动效见 [micro-interactions.md](micro-interactions.md)
- 证言头像与客户 Logo 必须用真实资源(见 [../meta/visual-assets.md](../meta/visual-assets.md)),占位头像即 ai-tells
- urgency 类模式(`urgency-countdown`、`scarcity-stock-counter`)滥用即 ai-tells:每页至多一种紧迫信号,且必须真实
- 移动端禁横向滚动价格表,改堆叠卡或 `sticky-plan-tabs`;功能矩阵移动端降级为双档对照
- 结账页剥离主导航只留 logo 逃逸口;按钮文案用目的地词("继续到付款")替代泛化"继续"

## 在 draw-md 中的写法

- 定价区先写容器 pattern 名再逐档展开,档位命名与命名表一致
- 结算/开通流程用 `checkout-progress` 声明步骤序列,每步一个动词
- 涉及动效或真实资源的模式,在字段内注明引用文件

```markdown
## Pricing (pricing-tier-cards)
- toggle: { pattern: pricing-toggle-billing, default: annual, note: "年付省 2 个月" }
- tiers: [free, pro, enterprise]
- tier-pro:
  - highlight: pricing-highlight-popular
  - price: { amount: 79, period: month, billed: annual }
  - cta: { type: button-primary, label: "开始 14 天试用" }
  - details: { pattern: plan-compare-drawer }
```
