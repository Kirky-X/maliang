# 编号门禁 —— 交付前的二元否决清单

> 规范层。清单式 reference 满仓都是(ai-tells 的 Tell、ux-rules 的 slug、preview-checklist 的 135 项),但它们多数回答「这样好不好」,不回答「不这样能不能交」。本文只收**二元门禁**:每条要么 PASS 要么 FAIL,无灰区,任一命中即不许交付,修复后重跑全部。
>
> 每条门禁三段写死:**违反什么**(可被指认的字面形态)/ **怎么判定**(证据从哪来)/ **怎么修**(指回可执行的文档)。软提示式表述(「注意质量」「保持一致」「尽量避免」)一律不构成门禁。机制来源:oh-my-design 的 numbered slop gates(编号 + 二元 + 机器可判项必须留 grep 证据,MIT,2026-09 吸收,条目与判据中文自研)。

---

## 0. 执行纪律(先读这节,否则下面的门形同虚设)

1. **全量过,不摘要**。把门禁清单压缩成「主要几条」= 丢门。门禁的价值在于覆盖了没被想到的形态,摘要恰好删掉没被想到的那些。
2. **有据才判**。「源码里没看到违反」这种结论**必须附判定记录**,否则视为未判定。机械可判项至少留命中行号清单(命中 / 无害判理由),非机械项留检查点结论。
3. **不豁免、不降级**。唯一合法出路是修复。确有正当理由(如 DESIGN.md 显式批准某个 AI Tells 值)时,走 [`ai-tells.md`](ai-tells.md) §0 豁免总则的**显式记录**要求,静默豁免 = FAIL。
4. **CRITICAL 一票否决**。任一 CRITICAL 门 FAIL,不得被任何评分补偿——沿用 [`rules-priority.md`](rules-priority.md) 冲突裁决规则 1 与「加权评分从属声明」。
5. **修复后重跑全部**,不可只跑失败项(与 [`../commands/preview-checklist.md`](../commands/preview-checklist.md) 执行规则一致)。

**严重级**:CRITICAL(可访问性 / 功能损坏,一票否决)· HIGH(AI 味 / 系统一致性,阻断交付)· MEDIUM(打磨项,不阻断但须在报告列为 known issue)。

**与 135 项清单的关系**:本文**不替代** [`preview-checklist.md`](../commands/preview-checklist.md),也不重复其条目。135 项是「全量机械检查」,本文是「否决门」——门禁条目均可映射到 135 项的分区或 ai-tells / ux-rules 的既有条目,映射关系写在各条的「怎么判定」里。**两处都过才算过**:清单过了不豁免门禁,门禁过了不豁免清单。本节是这条规则的**唯一 canonical 表述**——其余文档(SKILL.md / lifecycle.md / preview.md / preview-checklist.md)提及此规则时只留一句提示并链接到本节,不各自复述全文;修订规则语义只改本节。

---

## A 组 · 溯源与 token(设计系统自洽)

> 「悬空溯源 / 孤儿 token / 空原则」三类违规名的 canonical 定义在 [`token-provenance.md`](token-provenance.md) §4(V1/V2/V3);本组 G01–G03 只收交付门禁判定,判据以彼处为准。

### G01 · 悬空溯源
- **违反什么**:token 注释里的决策 id 在 `decisions[]` 中查不到,或 `D-P<n>` 指向的 `## Overview` 原则不存在。
- **怎么判定**:人工判定,逐个 id 对账(design-md 交付 / 改过 token 的 redesign 交付时)。溯源核对三行记录缺任一行即 FAIL。机制与修法见 [`token-provenance.md`](token-provenance.md) §4 V1。
- **怎么修**:补写缺失决策(决策 / 理由 / 日期 / 范围),或把注释改指正确 id。**禁止**删注释了事——无来源的 token 是 V2 不是豁免。

### G02 · 孤儿 token
- **违反什么**:`colors` / `typography` / `rounded` / `spacing` / `components` 顶层键既无 id 也无 `no-decision:`;或下游产物(ui-markdown / 框架代码 / 预览 HTML)出现 DESIGN.md 里不存在的视觉值。
- **怎么判定**:人工判定顶层键覆盖 + 人工/脚本混合判定下游值(下游值另见 `validate-draw-md.py` 的 `color-literal` 检查)。判据见 [`token-provenance.md`](token-provenance.md) §4 V2 与 §6。
- **怎么修**:归到一条决策下,或回 design-md 补决策再把值写进系统;无依据的写 `# no-decision: <原因>` 显式声明。

### G03 · 空原则
- **违反什么**:`## Overview` 声明了 2–3 条原则,其中某条不改变任何 token 值——只写在散文里,是装饰不是立场。
- **怎么判定**:人工判定,只数 token 注释里的 id 引用,不看散文(见 [`token-provenance.md`](token-provenance.md) §4 V3)。
- **怎么修**:让原则落到至少一个 token 上(改值或加注释引用),或把该原则从 Overview 删掉。

### G04 · 硬编码视觉值
- **违反什么**:产物中出现 token 体系外的字面值——`#FF0000` / `14px` / `16px` 等直接写在样式或示例代码里。跨框架转换中的 N/A 组件、文档说明里的 token 映射对照不算命中。
- **怎么判定**:`python3 scripts/validate-draw-md.py` 的 `color-literal` 等检查 + [`../commands/draw-md.md`](../commands/draw-md.md) 约束汇总逐条过。CRITICAL 侧的对应项是 SKILL.md 禁止事项 #2。
- **怎么修**:换成 `{token-name}` 引用;确需 token 外的值时先回 design-md 补 token,再引用。

### G05 · token 跨层直连 / 混用命名
- **违反什么**:component 层 token 直接引用 primitive(`color-button-primary-bg: color-red-500` 绕过语义层),或同一系统内 `{color-primary}` 与 `{primary-color}` 两种风格并存。
- **怎么判定**:人工判定,对照 [`token.md`](token.md) 三层层级与四大原则;命名抽查对照 SKILL.md 禁止事项 #3。
- **怎么修**:补语义层中转,统一到 [`token.md`](token.md) 的 `[namespace]-[category]-[property]-[tier]-[state]-[mode]` 结构。

### G06 · 暗色未走 mode 引用
- **违反什么**:暗色模式用 `filter: invert()` / 运行时 HSL 计算反色,或暗色区块里沿用亮色文字 token 而未取 `mode` 后缀的暗色值。
- **怎么判定**:`validate-draw-md.py` 的 dark-mode 覆盖检查 + 人工看语义 token 是否随主题指向不同值(反演 ≠ 重映射)。
- **怎么修**:按 [`../dimensions/color.md`](../dimensions/color.md) 的暗色重映射写法重建语义指向。

---

## B 组 · 可访问性与触控(CRITICAL,一票否决)

### G07 · 焦点不可见 / 焦点只在鼠标下出现
- **违反什么**:`outline: none` 未补替代焦点样式;或焦点环用 `:focus` 写,导致鼠标点击也弹出焦点环(应为 `:focus-visible`);或路由切换把焦点移到容器元素后视觉焦点环仍画在容器上。
- **怎么判定**:Tab 实测 + `validate-draw-md.py` 的 `aria-label` / 焦点相关检查。对应 ux-rules slug `focus-states`(ERROR)。
- **怎么修**:2–4px 可见焦点环,`:focus-visible` 限定;程序性聚焦的容器抑制视觉环但保留焦点(`#page-title:focus { outline: none }`)。见 [`accessibility.md`](accessibility.md)。

### G08 · 触控目标缩水
- **违反什么**:指针目标小于平台下限(原生 ≥44pt/48dp/44vp,Web ≥24×24 CSS px,推荐 44px),或相邻目标间距 <8px。
- **怎么判定**:`validate-draw-md.py` 的 `touch-target` 检查 + 设备预览实测。对应 ux-rules slug `touch-target-44` / `web-target-size-24` / `touch-spacing`。
- **怎么修**:视觉尺寸不变、热区扩展到达标,或加大相邻间距。

### G09 · 正文对比度不足
- **违反什么**:正文 <4.5:1、大字 / 图标 / 焦点环 <3:1;或暗色区块未把文字与边框切到反色 token(页脚也算)。
- **怎么判定**:`npx @google/design.md lint` 的 `contrast-ratio` + 预览实测。对应 ux-rules slug `color-contrast`(ERROR)。
- **怎么修**:加深/提亮到达标,或换更高对比的 token 组合。**不得**用 CRITICAL 之外的偏好覆盖(冲突裁决规则 4)。

### G10 · 状态不只靠颜色传达
- **违反什么**:错误 / 成功 / 警告仅靠红绿区分,无图标或文字辅助。
- **怎么判定**:人工判定,对应 ux-rules slug `color-not-only`(ERROR)。
- **怎么修**:附图标或文案;颜色只作强化,不单独承载语义。

---

## C 组 · 视觉签名(AI 味硬命中)

> 本组每条都对应 [`ai-tells.md`](ai-tells.md) 的某个 Tell,只列**在交付层最容易复发且判据可指认**的形态;命中时按该 Tell 的替代做法修,不重复其理由。

### G11 · 模板化版式三件套
- **违反什么**:三列等高卡片(icon + 标题 + 描述)凑数;卡片套卡片;某侧一条粗彩色边条(含左侧 border 强调)当装饰。
- **怎么判定**:人工判定 + Squint test(见 [`../commands/preview.md`](../commands/preview.md) 决定性自检)。对应 ai-tells §1 / §3。
- **怎么修**:换成不对称 bento / 纵向叙事 + 单个对比块;层级用留白与排版建立,不靠嵌套盒与色条。

### G12 · 渐变文字 / 紫蓝粉大面积渐变
- **违反什么**:`background-clip: text` 渐变标题;紫→蓝 / 青→洋红渐变大面积铺底。
- **怎么判定**:`python3 scripts/detect-tells.py <文件...>` 扫描 + 人工复核豁免语义。对应 ai-tells §1。
- **怎么修**:单色高字重 + 一个强调色块;必须用渐变时限制在同一品牌色相内两阶梯度。

### G13 · 纯黑纯白基色
- **违反什么**:基底直接用 `#000` / `#fff`,或中性色阶完全无色相(纯灰 RGB 相等)。
- **怎么判定**:人工判定,对照 [`../dimensions/color.md`](../dimensions/color.md) 的中性色阶要求。对应 ai-tells §1 与 G09。
- **怎么修**:按参照物给中性色阶一点色温,基底与 surface 拉开一档。

### G14 · 圆角无层级
- **违反什么**:全场同一圆角档(全 `rounded-2xl` 或全 `border-radius: 8px`),容器 / 控件 / 头像不分档。
- **怎么判定**:人工判定,对照 [`../dimensions/radius.md`](../dimensions/radius.md) 的 sm/md/lg/full 分档。对应 ai-tells §1。
- **怎么修**:容器 > 控件 > 头像差异化;嵌套时内圆角 = 外圆角 − 间距。

---

## D 组 · 交互与状态

### G15 · 焦点 / 按下 / 禁用态缺环
- **违反什么**:可交互元素缺 `:focus-visible` / `:active` / `:disabled` 三态之一;禁用态与可用态外观无差别。
- **怎么判定**:人工判定 + [`../commands/preview-checklist.md`](../commands/preview-checklist.md) §5.7 完整交互状态。对应 ux-rules slug `focus-states` / `disabled-states`。
- **怎么修**:三态补齐,禁用态给独立语义(`disabled` 属性 + 视觉降级),不留可点状态。

### G16 · 状态间改几何
- **违反什么**:状态切换时改 `border-width`(输入框 1px→2px 抖动)、用 border 冒充焦点、或 input 高度与相邻按钮高度不等。
- **怎么判定**:人工判定(逐组件比对 default / hover / focus / disabled 的 box metrics);`validate-draw-md.py` 的固定宽度文本等几何检查为辅。
- **怎么修**:用阴影 / 背景 / ring 表达焦点,几何尺寸跨状态恒定;input 与 button 高度取同一档。

### G17 · 动效不遵守硬约束
- **违反什么**:`transition: all`;动画 layout 属性(width / height / top / margin);入场时长 >400ms;`prefers-reduced-motion: reduce` 下不回落到静态。
- **怎么判定**:`validate-draw-md.py` 的 `motion-duration`(400ms 口径)与 `physical-property` 检查 + 人工 grep `transition: all` + 减少动效实测。
- **怎么修**:改 `transition: transform, opacity` 等具体属性;时长回 400ms 内;补 `@media (prefers-reduced-motion: reduce)` 回落。分层长动效见 [`../vocabulary/micro-interactions.md`](../vocabulary/micro-interactions.md)。

### G18 · 庆祝性反馈用于无操作结果
- **违反什么**:结果已经摆在屏幕上了,还弹庆祝 toast / 撒花;或自动轮播内容无暂停。
- **怎么判定**:人工判定。对应 [`principles.md`](principles.md) 第 13 定律(动画动机)。
- **怎么修**:只给需要告知的结果做反馈;轮播加暂停控件或移出自动播放。

---

## E 组 · 布局与响应

### G19 · 横向滚动
- **违反什么**:320px–1920px 任一宽度出现横向滚动条,或横向溢出靠 `overflow-x: hidden` 遮掉根因。
- **怎么判定**:设备预览逐档实测 + `overflow-x: clip` 复查。对应 preview-checklist §5.0 的 375px 窄屏实测。
- **怎么修**:定位超宽元素(长 token、图表 canvas、固定宽容器)改为流式 / 换行 / 容器查询。

### G20 · 网格轨道缺 minmax
- **违反什么**:`grid-template-columns` 轨道末位裸 `1fr`(应 `minmax(0,1fr)`),长内容把轨道撑破。
- **怎么判定**:人工判定 + 窄屏实测。
- **怎么修**:末位改 `minmax(0,1fr)`;超长文本槽位补 `min-width: 0`。

### G21 · display 标题溢出
- **违反什么**:display 字号标题未设 `overflow-wrap` / `min-width`,长词或 CJK 长串破版。
- **怎么判定**:用超长无空格 token、emoji 多码位序列实测(见 [`hardening.md`](hardening.md) §1 极端输入)。
- **怎么修**:标题槽位补 `overflow-wrap: anywhere` + `min-width: 0`,并给 CJK 单独的行高。

### G22 · 全屏 hero 顶满
- **违反什么**:`min-height: 100vh` 的整屏居中堆叠 hero,首屏塞不下任何真实内容。
- **怎么判定**:1280×800 实测首屏可见内容。对应 ai-tells §1。
- **怎么修**:hero 高度按内容定,或首屏至少给一个真实动作;移动端改 `100dvh` 并让出安全区。

---

## F 组 · 交付与可核验性

### G23 · 溯源 / 决策未留痕
- **违反什么**:改过 token 或视觉值后交付,报告里没有溯源核对三行记录(见 [`token-provenance.md`](token-provenance.md) §5);或本轮新决策未按 [`../commands/design-md.md`](../commands/design-md.md) 的「决策回写」提议进账本。
- **怎么判定**:读交付报告,三行记录与决策提议是否在场。
- **怎么修**:补齐记录后重跑 G01–G03;决策表未获用户确认的不静默写入账本。

### G24 · 静态声明代替实测
- **违反什么**:「看起来没问题」「整体达标」作为验证结论,没有判定记录 / 实测截图 / grep 命中清单;或 135 项清单的运行时项用静态扫描结论顶替。
- **怎么判定**:报告首行 disposition 与证据四分类(见 [`../commands/preview.md`](../commands/preview.md) 证据四分类)是否填全。
- **怎么修**:按 preview.md 的证据四分类补齐;无法实测的项如实标 `unresolved`,不许默认通过。

### G25 · 评审未与生成隔离
- **违反什么**:自评自签,无独立评审者且未标 `⚠️ DEGRADED: self-review`。
- **怎么判定**:看报告首行是否有 disposition 与降级标注(见 [`../commands/preview.md`](../commands/preview.md) 评审隔离)。
- **怎么修**:派生独立 subagent 评审;不能派生时显式降级并从紧。

### G26 · 规模性空转
- **违反什么**:选了某种版式语法(轮播 / bento / 图集)但内容条数不够它成立——bento 少于 5 块、图集少于 4 张、轮播少于 4 项。
- **怎么判定**:人工判定,数内容条数而非看效果。
- **怎么修**:换更小的语法,或先补内容/资产再排版——**内容不足时先补内容,不靠缩排版掩盖**。

### G27 · 层级靠细读成立
- **违反什么**:眯眼 / 缩小后焦点不最先被看到、层级只剩细线与弱对比撑起(无焦点 / 扁平层级)。
- **怎么判定**:Squint test(见 [`../commands/preview.md`](../commands/preview.md) 决定性自检)。命中时 Brand Fit ≤ 2 分。
- **怎么修**:先重建层级(尺度差 / 重量差 / 留白差),再谈细节;判为组合性缺陷时回 draw-md 重走。

### G28 · 状态语义在页面泄漏
- **违反什么**:开发用状态切换器 / 调试面板出现在产品 UI 里;或页面文案里出现文件名、字段名、框架术语。
- **怎么判定**:人工判定 + 预览产物巡检。
- **怎么修**:状态切换器移出产物(只留在 preview 调试页),文案换成用户语言。

---

## G 组 · 定义层成立性(数据与存活)

> 本组判的不是页面长得对不对,而是**定义层成立不成立**:首屏的数据有没有底座、定义扛不扛得住第二周。判据 canonical 在 [`data-floor.md`](data-floor.md) 与 [`day-two-blacklist.md`](day-two-blacklist.md),本组只收交付判定。

### G29 · 首屏数据无底座
- **违反什么**:首屏 / hook 区出现数值、进度、结论条、指标卡,而该数据分句没有绑定表一行(无字段 / 无写入方 / 无冷启动台词);或呈现 `--` / 空表 / 编造演示数;或断连 / 跳过日无专属台词;或 `integration` 字段未声明 exists_today。
- **怎么判定**:人工判定,逐个首屏数据分句对 [`data-floor.md`](data-floor.md) §2 绑定表;design-md 交付时检查 `constraints:` 块是否含绑定表与 day 1/2/7 三行台词(数据型产品)。CRITICAL 级,一票否决。
- **怎么修**:给字段挂写入方(优先 `system` 副作用写入,见 data-floor §4 Move 0);今天不存在的集成数字离场进 depends_on;补冷启动台词;首屏禁假演示数(与 [`../vocabulary/states.md`](../vocabulary/states.md) 的 state-empty-starter 边界按 data-floor §7 裁决)。

### G30 · 定义级死法命中
- **违反什么**:spec / 提案 / 构思命中 [`day-two-blacklist.md`](day-two-blacklist.md) 任一 D/S 条目(如幸运签 hook、演示数据谎、百科轨超 1/3、列表页地狱)。
- **怎么判定**:人工判定,按黑名单清单跑两域各自全量(含 D0/D0′ 两条前置);定义级输入(spec / proposal / 构思)即可触发,不要求先有建成页面。CRITICAL 级(D1/D6/S1/S3/S6 等上线日即死项),一票否决。
- **怎么修**:按黑名单该条的 Fix 修;无法在定义层修复的(如集成今天不存在)按 G29 同规则离场处理。

---

## 与既有文档的关系

| 主题                     | canonical 在哪                                        | 本文角色                                   |
| ------------------------ | ----------------------------------------------------- | ------------------------------------------ |
| 全量机械检查             | [`../commands/preview-checklist.md`](../commands/preview-checklist.md) | 门禁不替代它,只在其之上加否决             |
| 规则库 / slug / 严重级   | [`ux-rules.md`](ux-rules.md)                         | 门禁条目映射到 slug,不重写规则             |
| AI 味黑名单 / 豁免总则   | [`ai-tells.md`](ai-tells.md)                         | C 组只列复发形态,豁免走其 §0               |
| 定义层死法黑名单         | [`day-two-blacklist.md`](day-two-blacklist.md)       | G30 判定其 D/S 条目的命中                   |
| 数据底座判据             | [`data-floor.md`](data-floor.md)                     | G29 引用其绑定表与冷启动协议                 |
| 产品结构分类             | [`workbench-structures.md`](workbench-structures.md) | 定义期输入(结构判定),不替代任何视觉层规范 |
| 优先级裁决 / CRITICAL    | [`rules-priority.md`](rules-priority.md)             | 一票否决沿用其规则 1 与从属声明            |
| token 溯源判据           | [`token-provenance.md`](token-provenance.md)         | A 组引用其 V1–V3                           |
| 评审 / 证据 / disposition | [`../commands/preview.md`](../commands/preview.md)   | F 组引用其证据四分类与评审隔离             |
