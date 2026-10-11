# design-md 子命令 —— 创建、应用、验证、导出 DESIGN.md

> 本文件是 `design-md` 子命令的完整流程,由顶层 [`SKILL.md`](../../SKILL.md) 路由进入。
> 产出物 = **DESIGN.md** 设计系统文件(Google Labs agent-first 格式):YAML 前置 token(机器可读)+ Markdown 正文(人类可读设计理由)。
> 想从 DESIGN.md 进一步产出页面级硬token UI markdown,见下游子命令 [`draw-md.md`](./draw-md.md)。

[google/design.md](https://github.com/google-labs-code/design.md) 让 AI 编码代理对设计系统有持久、结构化的理解。一份 DESIGN.md 文件 = **YAML 前置 token**(颜色/字体/间距/组件,机器可读)+ **Markdown 正文**(设计理由与边界用法,人类可读)。

**CLI**: `npx @google/design.md@0.4.0`(Windows 用 `npx designmd`)。全局安装:`npm install -g @google/design.md`

---

## Workflow Overview

| User Intent                           | Phase                                              |
| ------------------------------------- | -------------------------------------------------- |
| 任意 design-md 触发                   | → **Phase 0**: Brief Inference(推理设计方向)     |
| 0c 方向确认后、填模板前                | → **Phase 0d**: 决策表(带 id,供 token 反向引用)  |
| "Create a DESIGN.md for my project"   | → **Phase 1A/1B**: Generate from code or interview |
| "Extract tokens from my CSS/Tailwind" | → **Phase 1A**: Analyze code                       |
| Provides a screenshot/mockup          | → **Phase 1C**: Extract from image                 |
| "Build UI using our design system"    | → **Phase 2**: Apply tokens                        |
| "Lint / validate my DESIGN.md"        | → **Phase 3**: CLI lint(9 项规则)               |
| "Export tokens to Tailwind/CSS"       | → **Phase 3**: CLI export                          |
| "Generate theme variations"           | → **Phase 4**: Variation Engine(见 advanced)     |
| Starting any frontend project         | → Scaffold DESIGN.md **first**                     |

**输入冲突优先级**:若用户同时提供代码和截图,以代码(更精确)为主、截图为辅助校验;若同时表达"新建"和"已有 DESIGN.md",先执行 Edge Cases 中的「合并 vs 覆写」流程(见 advanced)。

**🔴 CHECKPOINT 规则(贯穿全文)**:遇到 🔴 CHECKPOINT 标记时必须真正暂停,等待用户文字回复后才能继续;不能假设默认同意直接往下走。

---

## Phase 0: Brief Inference(推理设计方向)

> 进入 design-md 流程的**第一件事**。Phase 0 分四步:**0a 领域探索**(进入产品的世界,查表前必经)→ **0b 类型查表校准**(类型推档)→ **0c Suggest+Ask 提案块**(方向确认后才动手)→ **0d 决策表**(把方向拆成带 id 的决策,供 Phase 1 的 token 反向引用)。从用户的简短 brief(产品描述 / 截图 / 关键词)推理出设计方向,作为 Phase 1 写 prose 的输入。完整推理规则见 [`meta/product-reasoning.md`](../meta/product-reasoning.md)。

### 0a · 领域探索(四产出)

动手查表之前,先进入"产品的世界",产出四件套:

| 产出              | 要求                                                   | 判定                            |
| ----------------- | ------------------------------------------------------ | ------------------------------- |
| **Domain** 领域词汇 | 该领域的概念 / 隐喻 / 词汇清单                        | ≥ 5 个                          |
| **Color world** 色彩世界 | 该世界物理空间里天然存在的颜色(材质 / 光线 / 环境) | ≥ 5 个                          |
| **Signature** 签名元素 | 只可能属于这个产品的唯一元素                      | 说不出 → 继续探索,禁止进入 0b   |
| **Defaults** 品类默认 | 点名 3 个该品类的惯性默认,并逐条声明拒绝           | 恰好 3 个,逐条拒绝             |

**自检**:把产品名从四产出中删掉,还能认出它是做什么的吗?认不出 = 探索还停留在品类通用层,回 0a 继续。

**锚定三问(与 Signature 互补,折叠在 0a 内回答)**:Signature 说唯一性是什么,三问说它从哪来——

1. **参照物**:品牌锚定哪个**具体场所或物件**?(深夜便利店 / 老式录音棚 / 工业织机——不是"零售行业")色彩 / 字体 / 布局密度 / 动效级别从参照物派生,色板须命名(如"午夜灯箱",禁"蓝橙配色"式命名)
2. **碰撞**:哪两个**不相关影响**碰撞,且肉眼可见?(医疗包装 × 滑板图形 / 表格 × 街头艺术;碰撞看不见 = 还没成立)
3. **反误认清单**:本品牌**永远不要被误认为**什么?列 2-3 条(如"不像加密项目 / 不像银行做的"),供 0b 的 Anti_Patterns 联动

卡壳时从弹药库取词再贴合 brief,不直接照搬:场所(深夜便利店 / 闭馆前的展厅 / 凌晨机场休息室 / 冬日温室 / 废弃厂房)、物件(80 年代合成器 / 手术器械 / 老式打字机 / 工业织机 / 瓷器)、时代运动(构成主义 / 包豪斯 / 孟菲斯 / Swiss 国际主义 / 新陈代谢派)。来源：landing-page-design,2026-09 吸收。

**用户三产出(四产出之后、0b 查表之前的小步)**:回答"谁在用"——

| 产出                 | 要求                                                     | 判定                   |
| -------------------- | -------------------------------------------------------- | ---------------------- |
| **Persona** 用户画像 | 1-3 个核心用户:目标 / 痛点 / 能力边界(各 ≤ 5 行)      | 有真实细节,非品类套话 |
| **Journey** 用户旅程 | 主任务旅程 3-6 步:步骤 / 触点 / 情绪断点               | 至少标出 1 个情绪断点 |
| **JTBD** 核心任务    | 1-2 句"当…时,我要…,以便…"                            | 每句能指导一处设计取舍 |

**降级声明**:没有用户研究输入时,走**证据反推法**(问过去的行为,不问未来的欲望),而非直接跳到模式假设:

1. **开场消息**固定形状:第一句即第一个问题(无铺垫、不诊断、不解释方法优劣)、每条问题**不附理由**、一句话说清答了换到什么(名字 / 每天看到的那句话 / 每天几秒)、「答一条就够」。目标长度 = 两条问题 + 一句换什么,±30%;三倍于此的篇幅是方法叙述,砍它不砍问题。
2. **过去行为六问**(问 2-3 条,原样照抄,不改写——改写就是把解释请回来的地方):
   - 有什么事,你现在拿备忘录、Excel、微信收藏夹或给自己发消息在凑合做?(★★★★★)
   - 有没有你试过、但用了不到两周就删掉的 App 或表格?为什么删?(★★★★★)
   - 哪个 App 你几乎天天开,但每次开都有点烦?(★★★★)
   - 有没有什么事你每隔一阵就要重新搜一遍,永远记不住?(★★★)
   - 翻一下你手机相册,最近最多的是什么照片?(★★★)
   - 上周你为什么事查过资料、算过账,或担心过?(★★★)
3. **解读规则**:凑合工具 = 已验证需求的化石(需求真、会复现、他愿意付每日税,工作从「发明产品」缩窄为「替换一个已知糟糕的工具」);弃用故事直接标定输入预算上界——**新设计的日成本必须低于压垮他的那一次,并把该数写进 DESIGN.md 约束与提案**(没有人知道自己扛得住多少录入,直到他打破过一次);答「没有」到全部六问 = 信息不是死路——降为周级节奏假设;证据指向多个方向时命名 fork 不合并,第二方向记入 deferred。
4. 仍无任何证据输入时,才退到原降级路径:显式写「未做用户研究,按 surface-modes 模式假设」并标低置信;禁止编造用户细节伪装成研究结论。三产出写入 DESIGN.md frontmatter 的 `users:` 块(字段与最小示例见 [`spec-schema.md`](../meta/spec-schema.md))。

> 与 kueiku 的 Mom Test 索引(原则级方法论,存于 kueiku 仓 product-discovery 篇)互补不重复:此处是嵌入设计流程的操作协议——问句原样可复制,解读规则给到结构判定。

**数据型产品前置(必过)**:产品首屏承诺数值 / 进度 / 榜单 / 结论条 / 指标卡(判型见 [`../meta/data-floor.md`](../meta/data-floor.md) §0)时,在 0b 查表之前过数据底座门禁:

1. 首屏 hook 按 `data-floor.md` §1 选合法形态(State / Delta / Imperative)并过密度底线,句子带真实值不写模板;
2. 按 §2 填绑定表:每个数据分句给字段 / 写入方 / 何时写 / 第一天空数据 / 断连日五列,有空格即不批准;
3. 每个 `integration` 字段写明来源系统与 exists_today;今天不存在的,数字离场进 depends_on;
4. day 1/2/7 冷启动台词三行写全,day 1 只索要一件事并说清它换来什么;
5. 绑定表、台词与输入预算上界写入 DESIGN.md `constraints:` 块,交付时按门禁 G29 复核。

**竞品拆解(可选小步)**:手头有竞品截图 / URL 时,选 2-3 个做速记对照表,结论写入 DESIGN.md 附录:

| 维度 | 记什么                           |
| ---- | -------------------------------- |
| 首屏 | 首屏传递什么、主操作是什么       |
| 导航 | 层级深度与结构(顶部 tab / 侧栏) |
| 密度 | 疏密取向与留白策略               |
| 色彩 | 主色相与强调色用法               |

**禁止照抄**:拆解回答"它为什么好、哪些可搬";可搬项仍须过 [`templates/variation-engine.md`](../templates/variation-engine.md) 的反品类默认校验,与 Signature 冲突的舍弃。

### 0b · 类型查表校准

1. **提取 brief 关键词**:从用户输入识别产品类型 / 用户群 / 业务目标 / 平台 / 情绪关键词
2. **匹配产品类型**:对照 [`product-reasoning.md`](../meta/product-reasoning.md) 第 2 节 12 个示例,命中则采用其推理结果;未命中查询 [`color-palettes.md`](../dimensions/color-palettes.md) 192 套桶
3. **推理 7 维输出**:`Recommended_Pattern`(布局,见 [`vocabulary/layout.md`](../vocabulary/layout.md))、`Style_Priority`、`Color_Mood`(→ color-palettes.md)、`Typography_Mood`、`Key_Effects`(≤3)、`Decision_Rules`、`Anti_Patterns`(与 [`ai-tells.md`](../meta/ai-tells.md) 联动)
4. **推断 Dials**:DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY 三档(见 [`dials.md`](../meta/dials.md))
5. **选 1-2 个参考设计系统**:从 [`design-systems.md`](../dimensions/design-systems.md) 11 个系统中选最接近的

**🔴 CHECKPOINT · Brief 推理确认**:展示推理结果让用户确认:

```
📋 设计方向推理:
  产品类型 / 推荐布局 / 风格优先级 / 色彩情绪→palettes
  字体策略 / 关键效果(≤3) / Anti-Patterns
  Dials: VARIANCE=x / MOTION=x / DENSITY=x
  参考系统:[1-2 个]

校准结果确认无误?确认后进入 0c 提案块。
```

### 0c · Suggest+Ask 提案块

将 0a 四产出与 0b 查表结果合并为一个提案块,请用户确认设计方向:

```
🧭 设计方向提案:
  Domain:[领域词汇清单]
  Color world:[该世界的天然色 → 映射到 primary/neutral/tertiary]
  Signature:[唯一签名元素]
  Rejecting:[点名拒绝的 3 个品类惯性默认]
  Direction:[一句话方向 + Dials + 参考系统]
```

**freshness 自检(0c 提案确认前过四查,防跨项目收敛,见 [`ai-tells.md`](../meta/ai-tells.md) 第 13 节)**:

- [ ] 未复用近期项目的 hex(以 decisions 账本方向字段记录为准)
- [ ] 未落"舒适字体"(Inter / Nunito / Space Grotesk 式顺手默认;display 按 [`../dimensions/font.md`](../dimensions/font.md) 候选池气质选)
- [ ] 双影响碰撞在提案里**肉眼可见**
- [ ] 至少含一个意外 wildcard(不"匹配"但让人记住的细节)

任一不过 → 回 0a 锚定三问重推,不进入 CHECKPOINT。

**🔴 CHECKPOINT · 方向提案确认**:提案块必须真正暂停,等待用户文字回复后才进入 Phase 1;用户可只改其中一项(如只换 Signature),其余项视为确认。

### 0d · 决策表(方向定了,值还没定时的中间产物)

> 0c 确认的是**方向**,Phase 1 直接落 token 会跳过"为什么是这个值"。0d 是两者之间的桥:把方向拆成带 id 的决策条目,Phase 1 的 token 逐条回指这些 id。

0c 确认后、Phase 1 之前,把方向声明的立场拆成 **2–3 条原则**(写进 DESIGN.md `## Overview`),每条原则下写决策表:

| 决策类别(全列,逐条落)                                                     |
| ------------------------------------------------------------------------ |
| 圆角档位 · 深度策略(投影 / 描边 / 纯色调) · 强调色预算 · 字号阶梯 · 动效时长与缓动 · 信息密度 · 布局语法 · 文案语气 |

每条决策写一行:`id | 决策内容 | 理由 | 反对的默认`。id 规则为 `D-P<原则序号>-<决策序号>`(`P1`/`P2`/`P3` 对应三条原则),编号与溯源约定见 [`../meta/token-provenance.md`](../meta/token-provenance.md)。

**硬约束**:

- **先有决策,再有 token**。跳过本步直接填模板,得到的 token 值是即兴值——这是 design-md 最常见的产出缺陷,不是效率。
- **原则必须改到值**。一条原则若落不到任何 token 上,它是散文不是立场:让规则落到值上,或从 Overview 删掉(判据见 [`../meta/token-provenance.md`](../meta/token-provenance.md) V3)。
- **理由要写被拒绝的默认**。写不出"我拒绝了什么"的决策是凑数,合并进同条。
- 本步**不必单独请用户确认**(与 0c 的 CHECKPOINT 不同),但决策表要在 Phase 1 交付时随 DESIGN.md 一并展示,用户可推翻单条;被推翻的 id 保留并标取代关系,不静默消失。

### Brief 不充分时 / 与 Phase 1 衔接

若 brief 缺关键词(如只说"做个 App"),不要硬推理:进入 Phase 1B 访谈模式补全,必须人工确认。推理结果写入 DESIGN.md frontmatter 的 `product:` 块(见 [`product-reasoning.md`](../meta/product-reasoning.md) 第 3 节),Phase 1 写 prose 时引用作为"为什么"的依据。

### 信息架构前置(草案)

进入页面设计(`draw-md`)之前,先落一份 IA 草案:**页面清单**(每个主任务各需要哪几页,可对照 [`default-pages/index.md`](../default-pages/index.md) 增删)+ **主跳转图**(哪页 → 哪页、带什么状态分支,一张 mermaid 即可)。标注:**`ui-graph generate` 的关系图以此草案为准**——事后从已产出页面反向派生变事前约定,逐页产出时页面边界与跳转不再靠临场。衔接:`ui-graph` 读该草案作期望基线,`check-nav` 校验实现页是否补齐 flow(见 [`ui-graph.md`](./ui-graph.md))。

---

## Phase 1: Generate a DESIGN.md

**写 prose 前先读 [`philosophy.md`](../meta/philosophy.md)**:设计质量由 prose 意图清晰度决定(三原则:prose 优先 / 具体参考 / 负约束),非值的精度。下面三个子流程产出的 prose 都应遵循它。

### 1A. From Existing Code

1. **Extract token candidates**: scan for color values(所有合法 CSS 颜色格式,见 [`spec-schema.md`](../meta/spec-schema.md) 颜色 token 节)、`font-family`/`font-size`/`font-weight`、spacing values (`px`, `rem`)、border-radius values
2. **Assign semantic roles**: group colors by function (primary action, body text, surface, border, error); name typography levels by usage (headline, body, label, caption)
3. **Infer scale**: 统计所有 spacing 数值,若 ≥70% 是 8 的倍数 → base=8px;否则 base=4px。归一化时四舍五入到最近的 base 倍数
4. **Attach provenance**: 每个提取到的 token 顶层键挂一条 0d 决策 id(`primary: "#212121" # D-P1-1`);**0d 决策表里没有、提取时也判断不出取舍的键,写 `# no-decision: <提取自 file:line>` 显式声明**,不随手编 id。缺这一步的 DESIGN.md 交付在门禁 G02 被拦(见 [`../meta/numbered-gates.md`](../meta/numbered-gates.md))
5. **Write prose rationale**: for each token group, write 2-4 sentences explaining the design intent, not just the values

**🔴 CHECKPOINT · 提取确认**:在填写模板之前,先展示 token 提取结果供用户核对:

```
🎨 提取到的 tokens:
  Colors: primary/secondary/neutral
  Fonts:  [family] [sizes]
  Spacing: base=8px → xs/sm/md/lg/xl
  Radius:  sm=4px, md=8px
  溯源:  M 个 token 键 → 决策 id N 个 / no-decision K 个

归类准确吗?有遗漏或需调整的角色划分?哪个值取错了?
```

用户确认后,填写 DESIGN.md 模板并写完所有 markdown 章节。

### 1B. From Description — Interview Mode

逐一提问(不要一次全抛给用户),每问等待回答后再问下一个:

1. **品牌性格** — 用 3-5 个形容词描述你的产品感觉?(如"专业/极简/温暖/科技感")
2. **色彩方向** — 有现有品牌色吗?偏暖/冷/中性?有禁用色吗?
3. **字体风格** — 衬线体(传统/高端)还是无衬线(现代/简洁)?标题与正文是否用不同字体?
4. **信息密度** — 内容密集的数据 dashboard,还是宽松的消费者应用?
5. **参考品牌** — 有视觉风格接近的产品或网站可以参考吗?

**🔴 CHECKPOINT · 生成前确认**:收集完所有回答后,先汇总设计方向让用户确认,再生成文件:

```
📋 设计方向确认:
  品牌性格 / 色调方向 / 字体策略 / 密度定位 / 参考风格

方向确认无误?确认后生成完整 DESIGN.md。
```

### 1C. From Screenshot or Image

1. Extract dominant colors → assign to `primary`, `secondary`, `tertiary`, `neutral` roles
2. Identify type hierarchy (size ratios, weight contrast between heading and body)
3. Measure spacing patterns (card padding, vertical rhythm, section gaps)
4. Note corner radius character (sharp ≈ 0-2px, subtle ≈ 4-8px, rounded ≈ 12-16px+)
5. Document visible component patterns (button styles, card structure, input fields)

---

## DESIGN.md Template

> 模板中的 `# D-P<n>-<m>` 是 **token 溯源注释**:每个 token 顶层键指回 `decisions` 里产生它的那条决策。无本地依据的键写 `# no-decision: <来源>`,不随手编 id。编号规则、一族同源判据与违规处置见 [`../meta/token-provenance.md`](../meta/token-provenance.md)。

```
---
version: alpha
name: <Product Name>
description: <one-line brand summary>
decisions:                          # 0d 决策表;id 供 token 行尾溯源,字段见 spec-schema.md
  - id: D-P1-1                      # 原则 P1 下的第 1 条决策
    decision: <一句话决策,可被 token 引用>
    rationale: <为什么,含被拒绝的默认>
    date: 2026-01-15
    scope: 全站
  # 原则 P1/P2/P3 对应 ## Overview 里的 2-3 条立场
colors:
  primary: "#..." # D-P1-1
  secondary: "#..." # D-P1-2
  tertiary: "#..." # D-P1-1        # accent / CTA
  neutral: "#..." # D-P1-2         # backgrounds, surfaces
typography:
  headline-lg: # D-P2-1
    fontFamily: ...
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  body-md: # D-P2-1
    fontFamily: ...
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  # 完整阶梯(headline-md/body-lg/label-sm 等)见 spec-schema.md 推荐命名
rounded:
  sm: 4px # D-P3-1
  md: 8px # D-P3-1
  lg: 16px # D-P3-1
  full: 9999px # D-P3-2
spacing:
  xs: 4px # D-P3-1
  sm: 8px # D-P3-1
  md: 16px # D-P3-1
  lg: 32px # no-decision: 继承品牌规范
  xl: 64px # D-P3-1
components:
  button-primary: # D-P1-3
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  # 更多组件模式(hover/active/disabled、chip、input 等)见 examples/design-system/heritage/DESIGN.md
---

## Overview
<Brand personality, target audience, emotional tone. 2-4 sentences.>
<P1/P2/P3 三条原则,每条须落得到下方至少一个 token 值——只写在散文里不改值的原则不算立场,见 token-provenance.md V3。>
## Colors
<Role of each palette. Where it should/shouldn't appear.>
## Typography
<Font strategy. Role of each typeface. Hierarchy.>
## Layout
<Grid model, spacing philosophy, containment. 参考 [`layout.md`](../dimensions/layout.md)>
## Elevation & Depth
<Shadows, tonal layers, borders, or flat contrast.>
## Shapes
<Corner radius philosophy. Sharp = engineered, round = approachable.>
## Components
<Key patterns and interaction states not captured by tokens.>
## Do's and Don'ts
- Do ...
- Don't ...
```

---

## Phase 2: Apply DESIGN.md

### Step 0 — 写入前防覆盖检查

任何会写入 / 覆写 DESIGN.md 的动作(创建、更新、合并)执行前,先检查项目根目录是否已有 DESIGN.md:

- **不存在** → 正常写入;
- **已存在** → 先用 `npx @google/design.md@0.4.0 diff DESIGN.old.md DESIGN.new.md`(或逐节 diff)汇报既有文件与新内容的差异——将新增 / 修改 / 删除哪些 token 与 prose 段落,等待用户显式确认后才写入。**禁止静默覆盖**;既有 decisions 表条目默认原样保留,除非用户逐条同意删除。

### Step 1 — Parse and Internalize

Read the DESIGN.md completely. Extract all token values into a lookup table. Then read the prose — it contains usage guardrails that tokens alone cannot express (e.g., "use tertiary for at most one CTA per screen", "labels are always uppercase").

**🔴 CHECKPOINT · 应用前确认**:如果是首次在项目中应用 DESIGN.md,展示解析结果让用户确认范围:

```
📋 将应用 token 到代码:
  --color-primary/--color-secondary/--font-body-md/--spacing-md
  核心组件约束:[Do's and Don'ts 摘要]

有需排除或额外关注的部分吗?
```

### Step 2 — 选择实现策略

根据项目栈选择 token 注入方式:

| 栈          | 推荐方式                       | 命令                                                                         |
| ----------- | ------------------------------ | ---------------------------------------------------------------------------- |
| Tailwind v4 | CLI 导出 CSS `@theme` 块       | `npx @google/design.md@0.4.0 export --format css-tailwind DESIGN.md > theme.css`   |
| Tailwind v3 | CLI 导出 JSON config           | `npx @google/design.md@0.4.0 export --format json-tailwind DESIGN.md > theme.json` |
| 纯 CSS/SCSS | 手动生成 `:root { --color-* }` | 见下方 CSS 示例                                                              |
| 原生平台    | 手动转换(见 Edge Cases 节)     | —                                                                            |

**CSS custom properties** 手动写法:

```css
:root {
  --color-primary: #1a1c1e;  --color-secondary: #6c7278;
  --spacing-md: 16px;  --radius-md: 8px;
  /* 其余 token 按命名空间 --color-*/--font-*/--spacing-*/--radius-* 同理展开 */
}
```

### Step 3 — Resolve Token References

In the `components` section, `{path.to.token}` references point into the YAML tree. Always resolve these before generating code:

```yaml
button-primary:
  backgroundColor: "{colors.primary}" # → #1A1C1E
  typography: "{typography.label-sm}" # → { fontFamily, fontSize, fontWeight, ... }
  rounded: "{rounded.md}" # → 8px
```

对于嵌套引用(复合 Typography 对象),逐字段展开(`font-family`/`font-size`/`font-weight` 等),完整字段列表见 [`spec-schema.md`](../meta/spec-schema.md) Typography Tokens 节。

### Step 4 — Enforce Prose Guardrails

Actively check generated code against the **Do's and Don'ts** section. Common examples: Single accent color per screen / Consistent corner radius within a view / WCAG AA contrast ratios (4.5:1) / Typography weight limit per screen.

**生成代码时的自查规则**:每写完一个组件,对照 DESIGN.md 的 Do's and Don'ts 列表检查一遍。发现违规时,在代码注释中注明"// ⚠️ 需确认:此处 border-radius 与设计规范 sm=4px 是否一致"。

---

## Phase 3: Validate & Maintain

### Lint a DESIGN.md

```bash
npx @google/design.md@0.4.0 lint DESIGN.md
npx @google/design.md@0.4.0 lint --format json DESIGN.md   # machine-readable output
```

Nine rules, each at a fixed severity (`error` / `warning` / `info`). **完整 9 条规则名、severity、触发场景、JSON output contract 全部见 [`spec-schema.md`](../meta/spec-schema.md) → Linter Rules**(权威镜像,不在此重复)。`contrast-ratio` 自动检查 WCAG AA(4.5:1);exit code 1 当存在 `error` 级 finding;`warning`/`info` 为建议性。Fix all `error` first, then triage `warning` by intent.

### 其他 CLI 命令(Diff / Export / Spec Inject)

```bash
# Diff 两版本(token-level changes, regressions 时 exit 1)
npx @google/design.md@0.4.0 diff DESIGN.old.md DESIGN.new.md
# Export W3C DTCG (.json) for Figma/Style Dictionary(Tailwind v3/v4 见 Phase 2 Step 2)
npx @google/design.md@0.4.0 export --format dtcg DESIGN.md > tokens.json
# Inject spec/rule table into agent prompt(无 prior context 时用)
npx @google/design.md@0.4.0 spec --rules-only --format json
```

`spec` 命令的核心用途:在 agent 无 prior context 时**把 spec/rule table 注入其 prompt**,使其遵循 canonical sections and rules 而非猜测;这不是简单的"打印 spec",是让 agent 拿到与 linter 同一份规则表的桥梁。

### 决策回写(交付末尾固定动作)

每次 design-md 交付的末尾,固定附一格"决策账本",汇总本轮新出现的设计决定(为什么选这个方向 / 为什么拒绝某个默认 / 为什么定这个值):

```
📝 本轮新决策 → 提议写入 DESIGN.md decisions 表:
  | id | 决策 | 理由 | 日期 | 范围 |
  | D-P1-4 | ... | ... | ... | ... |
```

逐条列出后请用户确认:同意的追加进 DESIGN.md 的 decisions 表(五字段 {id, decision, rationale, date, scope},与 [`spec-schema.md`](../meta/spec-schema.md) decisions 一致,scope 省略时默认全站),供后续会话读取("已决定,不是缺陷");拒绝的条目丢弃,不得静默写入。**新决策的 id 接当前最大序号往后排,不复用已被推翻的 id。**

**同格附溯源核对**(缺任一行视为未判定,门禁 G23 阻断交付,格式与判据见 [`../meta/token-provenance.md`](../meta/token-provenance.md) §5):

```
溯源核对(YYYY-MM-DD):
  决策 N 条 / token 顶层键 M 个 / no-decision K 个
  V1 悬空:0 · V2 孤儿:0 · V3 空原则:0
  孤儿清单(应为空,非空则逐条列 key):—
```

**方向字段约定(防跨项目收敛,克制扩展)**:方向类决策按"vibe 名 + 色板(名 + 核心 hex)+ display/body 字体"打包写入 decision 字段(如 `vibe:午夜灯箱;色板:#10233F/#E8452C;字体:Clash Display + Karla`),scope 标全站;**不新增账本列**,五字段结构不变。后续项目的 Phase 0a freshness 自检以此记录作为"近期项目"判定依据。

---

## 约束汇总(硬性)

- [ ] YAML frontmatter MUST 含 name/version/updated/tokens(colors/typography/spacing);token 命名 kebab-case,禁止字面量
- [ ] prose-first 格式:YAML token + Markdown 设计理由(解释"为什么"非"是什么"),禁止纯 JSON/CSS 变量文件
- [ ] 4 个动作(创建/应用/验证/导出)输入输出 MUST 明确,不得跳过验证直接导出
- [ ] 引用 heritage 范例 MUST 用相对路径;导出格式 MUST 支持 Tailwind/CSS/W3C DTCG/lint 至少 3 种
- [ ] **token MUST 溯源**:五个块的顶层键 MUST 带 `# D-P<n>-<m>` 或 `# no-decision: <来源>`;`## Overview` 每条原则 MUST 落到至少一个 token 上(硬门见 [`../meta/token-provenance.md`](../meta/token-provenance.md))

---

## Output Quality Checklist

交付前核对:YAML 无语法错误 · colors 均以 `"#"` 开头加引号(引号是溯源注释生效的前提) · 每个 token 顶层键带溯源 id 或 `no-decision` · 每个 id 在 `decisions` 中查得到 · `## Overview` 的每条原则至少被一个 token 引用 · 溯源核对三行已留痕 · typography 至少含 fontFamily/fontSize/fontWeight/lineHeight · spacing 遵循统一 base scale · components 用 `{path.to.token}` 引用而非重复字面值 · prose 解释"为什么"而非只列数值 · Do's and Don'ts ≥4条且具体可执行 · 章节顺序为 Overview→Colors→Typography→Layout→Elevation→Shapes→Components→Do's and Don'ts · CLI 可用时跑一遍 lint 修完所有 error · 过 [`../meta/numbered-gates.md`](../meta/numbered-gates.md) A 组门禁

---

## 高级特性

**Phase 4 变体引擎(明/暗 / 季节 / A/B / 品牌 / 无障碍)、Edge Cases & Fallbacks(CLI 不可用 / 输入不完整 / 合并覆写 / Lint 错误 / 图片质量不足 / 非 Web 平台等)、Design Read(一行检查点 + Visual Thesis / Content Plan / Interaction Thesis 三件事)、Working Model(最小成本验证设计方向的工作模型)全部见 [`design-md-advanced.md`](./design-md-advanced.md)。**

---

## Reference Files

- [`design-md-advanced.md`](./design-md-advanced.md) — Phase 4 变体引擎 + Edge Cases & Fallbacks
- [`spec-schema.md`](../meta/spec-schema.md) — 完整 token 类型定义 + decisions 五字段 + 溯源注释格式 + 权威 Linter Rules 表(9 条规则名 + severity)
- [`../meta/token-provenance.md`](../meta/token-provenance.md) — 决策 id 编号规则 + token 溯源写法 + 三类违规(悬空/孤儿/空原则)+ 判定留痕,0d 决策表与 Phase 1/3 溯源环节的 canonical
- [`../meta/numbered-gates.md`](../meta/numbered-gates.md) — 交付前编号门禁(design-md 交付过 A 组)
- [`philosophy.md`](../meta/philosophy.md) — DESIGN.md 写作三原则(prose 优先 / 具体参考 / 负约束),Phase 1 写 prose 前必读
- [`../../examples/design-system/heritage/DESIGN.md`](../../examples/design-system/heritage/DESIGN.md) — 生产级 DESIGN.md 范例,含完整 component 变体(hover/active/disabled/chip/input)
