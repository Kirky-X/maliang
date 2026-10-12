# 转化文案策略 —— Persuade surface 的设计输入

> 规范层。**定位：设计输入，不是独立产物**——仅在 surface=Persuade（见 [`surface-modes.md`](surface-modes.md)：落地页/营销首页/活动页）的设计与审计中作为输入生效，不触发独立的文案生成任务；Operate/Read/Experience 等 surface 不适用。来源：landing-page-design Copy Strategy 思想吸收（中文自研，非文本翻译），2026-09 吸收。分工：[`../templates/landing-patterns.md`](../templates/landing-patterns.md) 模式表管页面「**必须有什么**」（章节序列与 CTA 位置），[`content-guide.md`](content-guide.md) 管「**怎么写合格**」（语气/长度/格式），本文管「**说什么、按什么策略说**」（转化逻辑）。

## 总纲方程

```
Purchase Rate = Desire − (Labor + Confusion)
```

转化率 = 想要的程度 −（操作负担 + 困惑）。所有文案决策都落在这三个杠杆上：

| 杠杆 | 方向 | 手段 |
| --- | --- | --- |
| **Desire 想要** | 拉高 | 具体、可验证的价值陈述（说清「得到什么」而非「我们多努力」） |
| **Labor 负担** | 压低 | 短句、可扫读结构、显而易见的下一步 |
| **Confusion 困惑** | 压低 | 说清「这是什么」；按钮一眼可辨是按钮且可预判结果 |

卡在任何一句文案上时，裁决问句只有一个：**这句话是在拉高想要，还是在降低负担/困惑？** 三者都不沾，删掉。

## 七步文案线

### ① 异议发现

写任何标题前，先回答两个问题（有真实用户就问用户，没有就按产品推理（[`product-reasoning.md`](product-reasoning.md)）自答）：

- 「用户下单前，什么差点让他关掉页面？」
- 「还没买的人在等什么？」

常见异议五类：**不会用/没时间学**、**不适合我的具体情况**、**贵，不值这个价**、**还不信任你**、**没看懂它到底干嘛**。

写下 **Top 3 异议**，并逐一指派消解位——每个异议必须有着落，否则它会留在页面某处拦截转化：

| 异议 | 消解位 |
| --- | --- |
| 异议 1（最致命） | headline 的 hook 直面（见 ②） |
| 异议 2 | 对应 feature 段落内消解（见 ③） |
| 异议 3 | CTA 旁或按钮文案本身（见 ④） |

### ② Headline = 价值主张 + 钩子

**价值主张必须通过 litmus test：访客只看到 headline 这一行、其余全遮住，能否准确说出你卖的是什么？**

| 判定 | 例 |
| --- | --- |
| ❌ 不过关 | 「提升你的工作效率」（什么工作？怎么提升？空话） |
| ❌ 不过关 | 「效率的未来」（什么都没说） |
| ✅ 过关 | 「生鲜 1 小时送达，迟到免单」（卖什么+具体承诺） |
| ✅ 过关 | 「拖拽搭页面，零代码上线」（干什么+回应最大异议） |

**钩子两型，用 ① 的头号异议选型**：

- **A 型 · 大胆具体断言**（用数字造好奇）：如「3000 家门店的补货周期，从 7 天压到 1 天」——数字必须是用户提供的真实数；未供的量化声明按下方「数字阶梯」处置，不编造
- **B 型 · 直面头号异议**（拆掉第一道购买门槛）：信任异议→「免费试用，无需绑卡」；切换成本异议→「现有工具一键迁移」；怕麻烦异议→「5 分钟完成设置」

**副标题补位，只做两件事之一**：headline 讲了利益 → 副标题说清「这是什么」；headline 抛了断言 → 副标题解释「怎么做到的」。上限 1-2 句——需要第三句，说明 headline 没干完自己的活，回去改 headline。

### ③ Feature 三件套，每个回扣 hero

每个特性点恰好三件套，缺一不可：

| 件 | 规则 |
| --- | --- |
| **价值句 header** | 短、直白，只说这条特性给用户的价值。❌「为团队赋能」→ ✅「实时协同编辑」 |
| **一段描述** | 简短说明 + **只带一个异议消解**；细节给链接，不堆文字墙 |
| **行动中的产品图** | 软件产品：动图 > 截图 > 抽象插画；实物：使用场景 + 细节特写。图必须是「正在被用」，不是「摆着好看」 |

**回扣 hero 是硬规则**：特性不是随机罗列的功能清单，而是 hero 承诺的**证据链**——每个三件套都要能回答「这如何支撑 headline 说的那句话」；支撑不了 hero 主张的特性，再亮眼也砍掉或换位。

### ④ CTA：叙事的下一句，禁万能词

按钮文案必须**延续 headline 的叙事**——读完 headline，CTA 读起来就是顺理成章的下一句：

| ❌ 万能词（无上下文，哪都能贴） | ✅ 叙事延续（页面专属） |
| --- | --- |
| 「立即开始」「了解更多」 | 外卖页「找找附近的晚餐」；搭站工具「开始搭我的首页」；理财页「算算我能省多少」 |

万能词的判定：把这句 CTA 贴到任何行业任何产品上都成立，它就是万能词——推倒重写。与 [`content-guide.md`](content-guide.md) §2 分工：**全页唯一性归 content-guide §2**（同一意图全页只准一个标签），**页面专属具体性归本文**——Persuade 页两者同时满足；格式规范（动词开头、长度）同样以 content-guide §2 为准。

### ⑤ Social proof：冷启动分支，禁造假

- **有背书**（知名客户/媒体报道）：logo 墙放显著位 + 硬指标（服务客户数/处理流水/好评率），数字必须真实可溯。
- **冷启动没有背书**：给 3-5 家可识别的公司免费使用换授权展示；用 beta 用户做**具名真实**证言（真名+真实头像+具体场景）；聚合小数字（「500+ 团队在使用」）好过空 logo 墙；有任何媒体/播客/Newsletter 提及就上「媒体报道」位。

**红线：禁造假。** 假 logo、编造的证言、无法溯源的数字一票否决（critique/审计按虚假宣传处理）。**空的 social proof 区不如不设**——删掉该章节比放占位符诚实。非社证区的量化声明（proof strip 指标 / 对比行 / 功能区效率数字）按下方「数字阶梯」处置。

### ⑥ Multi-audience routing

产品服务多类差异明显的人群（个人 vs 团队、开发者 vs 设计师）时，页面顶部加「自选路径」入口，不把所有人塞进同一条漏斗：

- 切换 tab：「我是开发者 / 我是设计师」
- 分叉 hero：「我是[角色 A]」/「我是[角色 B]」
- hero 下方双入口卡，分别链向分段落地页

单一人群产品禁用此节——硬加的角色切换只会增加 Labor（见总纲方程）。

### ⑦ 收口：异议指派复核

七步走完，回到 ① 的 Top 3 做闭环复核（审计/ critique 同样用此表）：

```
TOP 3 异议：
1. [异议] → 消解于 [headline / feature 段 / CTA] → 是否有着落？[是/否]
2. [异议] → 消解于 [位置] → [是/否]
3. [异议] → 消解于 [位置] → [是/否]

HEADLINE：价值主张[具体卖什么] / 钩子型[A 断言 / B 异议] / litmus test [过/不过]
副标题：[1-2 句，补什么位]
CTA：[headline 的下一句] / 万能词判定 [非万能]
受众：[单一 / 多人群]（多人群：路由方式）
```

任一「否/不过」，回到对应步骤修，不带病交付。

## 真实声音样本库与禁用开场白

> 落地页文案有一个分布默认：不给他国非默认声音时，模型会滑向「Built for the modern team / Unleash your X / Where A meets B」。样本库是**真实站点的真实开场白**——给它非默认的模仿对象。判定原则：**模仿的是具体性的种类，不是措辞**——具名地点、具名日期、具名数字、拒绝隐喻、拒绝营销动词。开场白按品牌声音挑最接近的一型作基准；与 [`content-guide.md`](content-guide.md) §1 三级语气模型的分工：三级管 UI 文案的礼貌度，本节七型管 Persuade 页开场白的品牌气质。句型级机械扫描另按 `scripts/check-copy.py`（10 式模板句正则）。来源：hallmark copy.md「Voice samples per tone / Banned opening lines」，2026-10 吸收（样本为真实站点开场白，引文保留原文；标注「自建样例」的为外部 skill 检具，非真实站点）。

### 七型真实开场白

| 型 | 声音模式 | 真实开场白与具体性来源 |
| --- | --- | --- |
| 编辑 Editorial | 日期锚定 / 拒绝动词 / 列举 | "Creative direction, design and type for culture since 2003."（apracticeforeverydaylife.com，日期 + 具名领域）· "A thing well made."（klim.co.nz，拒绝动词，把设计当材料）· "Writer + Photographer."（craigmod.com，三个词两个身份，零废字） |
| 粗野 Brutalist | 平铺宣言 / 拒绝隐喻 / 直述后果 | "The product development system for teams and agents."（linear.app，平铺直叙，无 "powered by AI"）· "We design products that last twelve years. We do not design products that need replacing every two."（具体年数 + 成对宣言）· "We will not put our work behind a chatbot. We will answer the email ourselves."（宣言式拒绝，两句短句） |
| 柔和 Soft | 诗意克制 / 列举见热忱 / 脆弱带实证 | "It's about time."（cron.com，双关不眨眼）· "Time is our most precious resource."（Notion Calendar，先哲学前提后具体）· "I craft UI demos that explore the power of the web and help others sharpen their skills."（jhey.dev，点名动词 craft、点名受众 others） |
| 技术 Technical | 规格嵌散文 / 克制措辞 / 数据开场 | "The 14-inch MacBook Pro with M5 brings serious speed and advanced on-device AI to the work you do every day."（apple.com，规格嵌进散文）· "434 total posts. New CSS you feel like you could use today."（nerdy.dev，数据先行）· "Open the trace, find the span, fix the regression. No glossary required."（三个具体动词 + 一个拒绝） |
| 奢雅 Luxury | 具名的传承 / 以拒绝当高级 / 具名规模 | "The world's most acclaimed creative collective, where 23 partners work independently…"（pentagram.com，具名规模：23 位合伙人）· "By appointment."（以拒绝当门槛）· "A study in the senses."（自建样例，单一名词短语） |
| 俏皮 Playful | 流行文化类比 / 感官隐喻 / 预期读者反应 | "Playlists, but for ideas."（are.na，有用的类比）· "Devouring details. Nourishing novelty. Deploying excellence."（rauno.me，食物 + 技术隐喻）· "The kind that make you say, 'Wait, how did you do that?'"（jhey.dev，写出读者反应） |
| 极简 Austere | 极端缩写 / 原则开场 / 拒绝营销语言 | "Things Become Other Things."（craigmod.com，三个词，品牌当文章标题）· "This is a page that doesn't try."（自建样例，公开点名立场）· "One HTML file."（自建样例，数量即自夸） |

**brief 给不出具体性时**：停下问用户——问一个能引出具体名词、动词或地点的问题。用户知道自己的产品；**模型不许发明具体性**（与数字阶梯同一原则）。

### 禁用开场白

命中即换——用上表对应型的声音模式重写，不做同义替换（换词不换型照样命中）：

| 开场白 | 为什么禁 |
| --- | --- |
| "Built for the modern team" | 空泛；零具体性；营销腔时间词 |
| "Unleash your [X]" | 夸张；软件释放不了任何东西 |
| "Where X meets Y" | 假综合；创作上的偷懒 |
| "Empower your..." | 传教语言；回避具体收益 |
| "Reimagine the way you..." | 没讲需求先暗示不满 |
| "Supercharge your workflow" | 能量隐喻，无机制 |
| "Innovative solutions" | 无意义；每个产品都自称创新 |
| "Seamless integration" | 「无缝」没有反义词；不具体的信号 |
| "In today's digital landscape" | 时间性空话；假设读者需要被定向 |
| "Next-generation" | 暗示前代不行；给不出差异 |

## 数字阶梯（未供量化声明的三种处置）

**适用面（窄口，先划界）**：首屏 / hook 的数据条款与 persuade 信任数字归 [`data-floor.md`](data-floor.md) 门禁（绑定表 / 写入方 / 禁编造）；社证区数字归上方 ⑤ 禁造假；**本阶梯管剩下的说服位**——proof strip 的指标、对比行、功能区的效率数字、CTA 旁的承诺数字。来源：hallmark slop-test gate 46，2026-10 吸收（适用面经复核收窄：data-floor §0 已覆盖 persuade 首屏信任数字，本阶梯只补非首屏非社证区的空当）。

**触发**：页面出现用户未供、无来源、为填版面而写的量化声明——「10× faster」「每周省 5 小时」「50,000+ 团队」「99.9% uptime」「+47% 转化」——判失败。

**三种处置（任选其一；没有第四种「编个数」）**：

1. 数字位写 `—`，配一块标注「待确认指标」的灰块，交付说明列出待确认清单；
2. 停下问用户要真实数（用户知道自己的产品）；
3. 重写该章节，去掉证明位——空证明位好过编造的证明位。

**stat 永不做 hero 唯一标题**：大数字只在有文字标题伴随时主导 hero——一行说明它含义的字必须同场；裸数字当主标题是 tell。stat 主导的宏观结构（stat-led）在数字沦为装饰的那一刻就是 slop。

## 与其他文档的关系

- **Persuade 限定**：本策略只在 [`surface-modes.md`](surface-modes.md) 的 Persuade 模式生效；同页若混有 Operate 区块（如登录入口），登录区文案回归 `content-guide.md` 中性语气
- 页面骨架（章节顺序/CTA 位置）查 [`../templates/landing-patterns.md`](../templates/landing-patterns.md)；落地页视觉词汇查 [`../vocabulary/hero.md`](../vocabulary/hero.md)
- 文案格式硬规范（语气/长度/中英混排）见 [`content-guide.md`](content-guide.md)；AI 腔反例见 [`ai-tells.md`](ai-tells.md) §4——该节数据口径已与本文件「数字阶梯」统一：真实数据用真实精度，未供的不虚构尾数
- 数字分工三层：首屏 / hook 数据条款 → [`data-floor.md`](data-floor.md) 门禁；社证区 → 本文 ⑤ 禁造假；其余说服位 → 本文「数字阶梯」
- 「为什么 CTA 要可见可辨、异议要被消解」的心理学依据见 [`ux-laws.md`](ux-laws.md)（Von Restorff / 蔡格尼克 / 目标梯度）
