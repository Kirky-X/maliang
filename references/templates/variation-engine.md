# 组合式变化引擎（Variation Engine）

> 目的：防止"同档位跨项目雷同"。dials 解决强度档位，本引擎解决**同档位下的方向差异**——每个项目从 7 根轴各选 1 并整页 commit，不同项目的轴组合必须不同。来源：taste-skill image-to-code §12 + impeccable new-work §3-4 反同质化协议，2026-09 吸收。

## 使用时机

`design-md` Phase 0 的 Design Read 之后、方向确认之前。产出一行"组合声明"（可写进 DESIGN.md frontmatter 或决策记录）：

```
组合 = Pristine Light × technical grid × editorial serif+sans × asymmetric split × bento rhythm × [marquee, layered-crop, product-stack, quote-wall] × [float-up, fade-through]
```

## 七轴选项

### 1. Theme Paradigm（选 1）
1. Pristine Light Mode（纯净浅色）
2. Deep Dark Mode（深邃暗色）
3. Bold Studio Solid（大胆纯色块面）
4. Quiet Premium Neutral（安静高级中性）

### 2. Background Character（选 1）
1. subtle technical grid / dotted field（细微技术网格/点阵）
2. pure solid field with soft ambient gradient depth（纯色 + 柔和环境渐变景深）
3. full-bleed cinematic imagery（全出血影像）
4. tactile textured surface feel（触感材质表面）

### 3. Typography Character（选 1）
1. clean grotesk（干净无衬线）
2. refined grotesk（精致无衬线）
3. expressive display（表现力展示体）
4. compressed statement typography（压缩标语体）
5. editorial serif + sans（编辑衬线 + 无衬线混排）
6. Swiss rational hierarchy（瑞士理性层级）

### 4. Hero Architecture（选 1）
1. cinematic centered minimalist（电影式居中极简）
2. asymmetric split hero（非对称分栏）
3. floating polaroid scatter（悬浮拍立得散布）
4. inline typography behemoth（行内巨字）
5. editorial offset composition（编辑错位构图）
6. massive image-first hero with restrained text（巨图先行 + 克制文字）

### 5. Section System（选 1）
1. modular bento rhythm（模块化 bento 韵律）
2. alternating editorial blocks（交替编辑块）
3. poster-like stacked storytelling（海报式堆叠叙事）
4. gallery-led cadence（画廊主导节奏）
5. Swiss grid discipline（瑞士栅格纪律）
6. asymmetric premium marketing flow（非对称高级营销流）

### 6. Signature Component Set（11 选 4，唯一组合）
diagonal staggered square masonry ／ 3D cascading card deck ／ hover-accordion slice layout ／ pristine gapless bento grid ／ infinite brand marquee strip ／ turning polaroid arc ／ vertical rhythm lines ／ off-grid editorial layout ／ product UI panel stack ／ split testimonial quote wall ／ layered image crop frames

### 7. Motion-Implied Language（6 选 2）
scrubbing text reveal ／ pinned narrative section ／ staggered float-up ／ parallax image drift ／ smooth accordion expansion ／ cinematic fade-through

## 强制规则

1. **整页 commit**：组合选定后全页贯彻，禁止中途换轴、禁止混搭成"四不像"。
2. **组合去重**：与项目**最近 3 次**产出（build-log 头三条，不足 3 条有几条比几条；无日志时按盖章反推最近一条）逐轴对比，与**任一条** ≥5 轴相同即须重选。窗口从「最近一条」扩到「近 3 条」的理由：只比上一条时，A→B→A 的交替轮换永不违规，多个项目会走出同一个循环。来源：hallmark（对比窗口近 3 条），2026-10 吸收。
3. **反品类默认**：列出该品类最惯用的 2-3 个组合并显式拒绝，除非 brief 明确要求；"能从品类猜出你的组合 = 自检失败"。
4. **与模板墙联动**：选定组合后到 [`INDEX.md`](INDEX.md) 找 category/dials 匹配的模板做具象化参照；模板是配方可参考，轴组合是身份须保持。
5. **挑战者捐赠**（可选强化）：让另一方向作为"挑战者"先行构思 5 分钟，verdict 三档（win/competitive/declined）；即使 declined，也必须从挑战者身上指认一项纪律反哺选定方向——"捐赠纪律，绝不搬运外衣"。

## 单次发散会话伪分歧自检

> **三套用途、禁止混用**：上文七轴管**跨项目防雷同**（选型枚举，项目级、写入 DESIGN.md）；本节**会话内五轴**管**单次发散会话内的运行时自检**（方案级、不落 DESIGN.md）——多方案 prototype、方向探索时启用；本节**跨方向七轴**管**一轮内两方向之间的差异计数**（服务 explore 差异检验，词表与上文七轴相同）。来源：prototype skill 伪分歧判据，2026-09 吸收；并反哺强制规则 5 的挑战者捐赠——挑战者脑内构思同样过本自检，防止挑战者只是选定方向的换色版；跨方向七轴来源：qiaomu-design 仓，2026-10 吸收。

### 会话内五轴（运行时自检）

- **构建前声明分歧轴**：每个变体动手前，一句话说出它在五根轴——layout / density / personality / motion / interaction model——中的哪根上发散；说不出的变体不配进列表。
- **方向词命名**：变体用方向词命名（"安静""编辑感""致密""游戏感"），禁止 Option A/B/C——名字讲不出方向，说明方向不存在。
- **同向即替换**：两个候选若只差强调色或文案，它们是同一个方向；把其中一个换成真正的替代（换布局、换交互模型、换动效叙事）。
- **完成判据**：每个变体有名有轴，且 no two variants share an axis position——任一变体单独拿出来都是可独立发布的答案。
- **收敛则砍并明说**：构建中若两个变体收敛了，砍掉一个并显式告知；"两个真不同的方向"胜过"凑满三个"。
- **发散不降 craft bar**：每个变体单独满足完整 craft 标准（入场 ease-out、UI 动效 ≤400ms、只动 transform/opacity、处理 reduced-motion）；粗糙的变体不会拓宽探索面，只会输在执行并浪费一次方向采样。

### 跨方向七轴（差异计数轴）

> **第三套用途、同一套词表**：本表是**计数口径**——一轮内**方向与方向之间**逐轴计差异，服务 explore 的差异检验与完成判据。它与上文七轴**共用同一份词表**（明度 / 字体家族 / 色彩策略 / 布局结构 / 密度 / 时代气质 / 材质），不是新造一套轴；与本节五轴的分工：**五轴管单方向的运行时自检（声明在哪根轴发散），本表管两方向间的差异计数（数够几条轴）**。来源：qiaomu-design 仓的 divergence-playbook.md，2026-10 吸收。

| 轴 | 两端 | 伪多样的表现 |
| --- | --- | --- |
| 明度轴 | 亮底 ↔ 暗底 | 三个方向全是暗色 |
| 字体家族轴 | 衬线 ↔ 无衬线 ↔ 等宽 ↔ 展示体 / 手写 | 全是几何无衬线换个名字 |
| 色彩策略轴 | 单色克制 ↔ 双色对撞 ↔ 多色系统 | 全是「深底 + 一个荧光色」 |
| 布局结构轴 | 对称网格 ↔ 编辑式不等比 ↔ 自由构成 | 全是居中卡片 |
| 密度轴 | 美术馆留白 ↔ 报纸密排 | 全是中等密度 |
| 时代气质轴 | 复古印刷 ↔ 当代极简 ↔ 未来科幻 | 全是「现代科技感」 |
| 材质轴 | 平面 ↔ 玻璃 ↔ 纸质 ↔ 拟物 | 全是毛玻璃 |

**硬规则**：一轮内**任意两个方向之间至少 4 条轴取值不同**，其中**必须包含明度轴或时代气质轴之一**。两方向只差同轴刻度（都在暗色舒适区里调深浅）= 伪多样，必须换生成引擎重写其中一个。

**与跨项目口径的分工（防口径混淆）**：本节「≥4 轴」管**同一轮内方向之间**；[`### 阈值`](#阈值) 的「差异 ≥3 轴才放行」管**本次组合与历史组合之间**（跨项目 / 跨次构建，词表同为上文七轴）。两处数值不同是因为比较对象不同——同轮要拉开到 4 轴，跨次只要与上次不在同一组合（3 轴）。**两处都不得悄悄降档**。

**三问自检**（出方向后、进比较器前逐问回答）：

1. **遮住颜色还能区分吗？**——布局和字体本身就该不同；遮色后分不出 = 差异只发生在色彩策略轴上。
2. **有一个方向让你不舒服吗？**——三个方向都在自己审美舒适区 = 没有真正发散；不要求选它，但探索面里要有一个逼出取舍的选项。
3. **每个方向能一句话说出「它像什么杂志 / 店铺 / 年代」吗？**——说不出 = 气质模糊，回生成引擎重推。

**确定性种子（掷骰反惰性）**：LLM 天生会选「第一个想到的选项」。选方向、字体与首屏骨架时，用**确定性种子**做一次伪随机——`种子 = 任务描述字符数 mod 候选数量`，按种子从候选清单取一项，并在设计计划 / 决策记录里**写明掷骰结果**。**骰子选中舒适区之外的选项时，禁止悄悄换回**；确实无法落地的，在设计说明显式写「掷骰命中 X，因 <具体约束> 换回 Y」，不静默替换。这条与 [`../meta/ai-tells.md`](../meta/ai-tells.md) §13 跨项目收敛配套：种子是单轮内的反惰性，§13 是跨项目的反收敛。

**风格协议挂载（方向命中时）**：方向若命中已有完整风格协议(模板墙条目 / design-systems 索引里的站点)，实体化时**直接加载对应协议**做深度约束，不凭印象模仿；命中后仍须过本节七轴与三问自检，协议不豁免差异要求。

## 区段原型复用与每构建硬要求(原型词表: [`components/INDEX.md`](../components/INDEX.md),从索引挑名、只加载选中的那几个)

> 两节分工：knob 节管**复用合法性**（同一个原型第二次出现必须不一样），硬要求节管**每页保底变化**（哪怕一个原型都不复用，页面也不许是等宽居中块的堆叠）。来源：hallmark component-cookbook「Within-archetype variation knobs」+ themes/hum「Two requirements every build must meet」，2026-10 吸收。

### knob 声明（复用的唯一合法形态）

- **旋钮是什么**：每个区段原型带 2-3 个变体旋钮——原型内部的二阶变化位（列数与跨度比例 / 密度档 / 描边与容器 / 强调部署 / 编号与连接件样式这类）。旋钮词表随原型定义走（区段原型库每个原型的「变体旋钮」行）；原型未带旋钮定义时，按上述五类结构杠杆自定 2-3 个，声明时写明。
- **同原型复用必换至少一个 knob 并声明**：上一次 Bento 落了 `tiles=6 · spans=regular · border=hairline`，下一次至少一项不同，并把取值写进盖章与 build-log。两个产出落同一原型同一组旋钮值 = 与「项目间都选同一个原型」同级的模板化。
- **盖章扩 knob 值**：复用了区段原型的构建，盖章行在 dial 段后追加两段——`FC=<构图类>` 与 `K=<原型id>:<knob>=<值>,<knob>=<值>`（见下方盖章示例；核验脚本只对账 A-G 与 mode，新增段按信息性读取，供 G41/G43 人工对账）。
- **导航 / 页脚原型连续两次即违规**：导航与页脚是复用率最高、最容易被「顺手」照抄上一次的两个区段，不享受「换一个 knob 即合法」的宽限——系列产出（跨项目 / 跨品牌，与 [`../meta/ai-tells.md`](../meta/ai-tells.md) §13 同域）中相邻两次构建落同一导航或页脚原型即违规，必须换原型。**边界**：同一项目内的页面共享导航 / 页脚是 DESIGN.md 锁定的一致性（「第 7 页必须像第 1 页」），不属本条；本条只管跨项目的系列产出。

### 每构建两个硬要求

1. **一个 off-grid / 非对称时刻**：破栅格的卡、出血的大数字、2/3–1/3 分栏、一处倾斜——页面不得是一列等宽居中块的堆叠。off-grid 的**位置**跨构建轮换（这页在 hero、下页在证明区），不许每页同一位。
2. **一个 designed exception**：一处有意的破例，说明这是人做的——干脆的自嘲旁注、一个可玩的小交互、干净截图上的手写批注、一处全出血色块。**破例类型跨构建轮换**，不每次同款；同款 exception 连续两次 = 新 uniform（处置见 [`../meta/ai-tells.md`](../meta/ai-tells.md) §14 判据）。

两个都缺席 = 构建级不通过，进 design-md 收尾自检。**与 ai-tells 的分工**：§13 管 explore 方向层的意外 wildcard，§14 管单页内逐节重复；本节是两者的**跨构建等价物**——管这一页和上一页之间 off-grid 与 exception 的轮换。

## 跨次构建记忆（Build Log + Stamp）

> 规则 2 的"与最近一次产出对比"以前无可执行的读取路径，只能靠叙述。本节让"Don't Repeat"真正可执行：**PROJECT 内一致性**由 DESIGN.md 锁定（第 7 页必须像第 1 页），**跨次差异**由构建日志驱动（第 7 次构建必须不同于第 6 次）——两个目标相反，禁止共用一份文件。来源：Adapted from finesse-ui divergence §4（MIT），2026-09 吸收，轴替换为本引擎七轴。

### 构建日志 `.maliang/build-log.json`

项目根目录。JSON 数组，**新条目在前**，最多保留 **20** 条：

```json
[
  {
    "date": "2026-09-22",
    "page": "acme-launch",
    "mode": "Experience",
    "axes": {
      "theme": "Deep Dark Mode",
      "background": "tactile textured surface",
      "typography": "editorial serif+sans",
      "hero": "massive image-first",
      "section": "gallery-led cadence",
      "signature": "layered-crop + quote-wall + bento + marquee",
      "motion": "pinned narrative + scrubbing reveal"
    },
    "fold_class": "网格拼贴",
    "knobs": { "bento": "tiles=7 · spans=mosaic · border=accent-corners" },
    "dials": { "variance": 7, "motion": 6, "density": 3 },
    "brief": "工业键盘发布页"
  }
]
```

条目字段在七轴与 dials 之外增两个：`fold_class`（本次首屏构图类，词表见「首屏构图类抽签」节）与 `knobs`（本次复用的区段原型及旋钮取值，未复用原型时省略）。两字段**写后不改**（append-only）：改判、补记都新增条目并注明理由，禁止修改旧值——G43 对账与抽签的 spent 集合都依赖历史为真。「Fold classes used」段即全部条目 `fold_class` 字段按时间序读出的清单，不另立文件。

首次写入时创建 `.maliang/` 目录，并把 `.maliang/` 加入项目 `.gitignore`。

### 盖章 Stamp —— 无日志时的回退

页面 CSS 的第一个非空行（或内联 `<style>` 顶部）写入同一组坐标：

```css
/* maliang · mode=Experience · A=deep-dark · B=tactile-texture · C=editorial-serif
 * D=image-first · E=gallery-led · F=crop+quote+bento+marquee · G=pinned+scrub · V7M6D3
 * FC=grid-collage · K=bento:tiles=7,spans=mosaic,border=accent-corners */
```

`FC=` 段记首屏构图类、`K=` 段记复用原型的旋钮取值（未复用原型时省略 K=）；两段随章走，单独被拷走的 HTML 也能读出「复用换了什么」。核验脚本只机械对账 `mode` 与 A-G，FC/K 段按信息性读取，供 G41 / G43 人工对账。

日志是主记忆（本机连续构建快），盖章是回退（随代码走：新 clone、协作者、被单独拷走的 HTML 都能读）。**两者分工成立的前提是盖章被提交而日志被 ignore**——丢掉任何一个，项目都会静默退回无记忆状态。无 `build-log.json` 时，grep 目标代码里的 `/* maliang ·` 反推一条记录。

### 接线表（两端都是强制的）

| 时机 | 动作 |
| --- | --- |
| design-md Phase 0（Design Read 之前） | 读 `.maliang/build-log.json`；无则 grep `/* maliang ·` 盖章反推；都无 = 首次构建，无约束 |
| 说服型页面发散前（explore §2.3 / draw-md 章节规划） | 跑「首屏构图类抽签」：从 spent 集合之外的类按项目种子取候选；声明本轮构图类 |
| Phase 0 组合声明（旁边） | **把轮换说出来**——用一句话陈述新组合与最近 3 条各在哪几根轴上不同，写进决策记录 |
| design-md 收尾（自检通过后） | 数组头部 prepend 一条（含 `fold_class` 与 `knobs`）、裁到 20 条；把盖章（含 `FC=` / `K=` 段）写进 CSS 首行；随后跑 [`../../scripts/check-structure-history.py`](../../scripts/check-structure-history.py) 做机械核验（立即重复 / 热轴 / 盖章对账，违例即 G41/G42） |

### 阈值

沿用强制规则 2：新组合与 build-log **最近 3 条**逐条对比，与**任一条** ≥5 轴相同即须重选（等价于与该条差异 ≥3 轴才放行）。补全历史页（dials 从未被记录）时只写七轴、省略 dials 数值——**编造的 dial 比缺席更糟**，下一次构建会把它当真值去轮换。

## 首屏构图类抽签（Fold Class）

> 说服型页面（落地页 / 营销首页 / 活动页）的首屏**结构**按本节抽签轮换。为什么是抽不是选：**多样性无法靠文字请求**——十次盲构建产出同一个首屏，无论提示里是要求、允许还是明令禁止那个默认。所以构图类由机制给出，不由手感挑。来源：ui-craft fold/classes.mjs + recipe-landing（「variety cannot be requested in prose」/ FNV-1a 项目播种 / spent 沉底 / 声明类回验），2026-10 吸收；类目不用外部 6 类，词表换用 maliang 8 骨架（见下）。

### 词表与分工

**词表 = [`../vocabulary/hero.md`](../vocabulary/hero.md)「首屏骨架表」8 骨架**：满版图像压字 / 居中单一物件 / 画面即界面 / 满版文字 / 通栏上下堆叠 / 网格拼贴 / 纵排或斜向 / 左右分栏。explore 的首屏骨架与本节构图类是同一份词表，两处不另造名。

与七轴 **Hero Architecture** 的分工：hero 轴管首屏**气质**（电影式居中极简 / 行内巨字……，是跨项目组合身份的一根轴），构图类管首屏**结构**（机械可判、可回验、跨次轮换）。同一次构建两者都落：build-log 条目 `axes.hero` 记气质取值，`fold_class` 记构图类；两套词表不互相替换、不互相推导，也**不互相豁免**——构图类换了不等于 hero 轴可以与上次重复，反之亦然。

### 抽签机制

1. **种子**：项目根目录名（无目录语境时用 DESIGN.md 项目名）。对每个类算 `FNV-1a(种子 + '\0' + 类名)` 得 32 位键，按键升序得该项目的候选序。同一种子次序稳定、可复算（同一项目跨会话抽签结果一致）；不同项目种子不同、起点不同。**必须播种**：外部实现曾以数组序做平局决断，结果所有未花费过任何类的项目都抽出同一前三位——跨项目方差恰好为零，藏在「抽」字后面。引以为鉴。
2. **spent 沉底**：出现在 build-log「Fold classes used」清单里的类（见「跨次构建记忆」节），排名沉到最后——优先从本项目还没用过的类里抽。
3. **左右分栏永远压底**：spent 之外它再垫一层——它是所有模型的默认（外部十次盲建构图十次 split；8 骨架表同样只给它单方向配额）。永远不当第一建议，brief 明确要求时才落。
4. **领取**：从排序取前 3 为本轮候选；explore 一轮的方向按候选序领骨架，方向数超过未花费类数时才允许动用已花费类，并在决策记录写明动用了哪个 spent 类。
5. **相抵顺延**：抽到的类与 brief 硬相抵（如「画面即界面」拿不出可拍的真实产品界面、「满版图像」没有可用图像资产），**写出相抵理由**后取排序下一位——不静默换成心里先想好的那个。构建中途改判换类同样写明理由并入账（改判是决定，静默换类是 G43 违例）。

### 声明类回验

构建完成后，按 8 骨架表「首屏长什么样」一列把成品首屏归类，与声明的 `fold_class` 对照：一致 → 写入 build-log；不一致 → **声明的类没有兑现，比不声明更糟**（它向任何审计读作合规）——按声明类重实现，或改声明并在决策记录注明理由（入账）。回验是目测可判的结构判据，preview 渲染后看三点即够：首屏谁占主导、文字与视觉是什么关系、阅读从哪里开始。判据细节同 [`../meta/numbered-gates.md`](../meta/numbered-gates.md) G43。

### 五套轮换口径，一张表分清

| 口径 | 管什么 | 比较对象 | 通过线 | 门禁 |
| --- | --- | --- | --- | --- |
| 七轴组合 | 项目级视觉身份 | 新组合 vs build-log **最近 3 条** | 与任一条 ≥5 轴相同须重选（= 差异 ≥3 轴放行） | G42（脚本核验） |
| 会话内五轴 | 单方向运行时自检 | 方向 vs 五轴落位 | 任一变体说不出在哪根轴发散即不配进列表 | explore 完成判据 |
| 跨方向七轴 | 一轮内方向间差异计数 | 方向 vs 方向 | ≥4 轴不同，必含明度 / 时代气质之一 | explore 差异检验 |
| 构图类抽签 | 首屏结构的跨次轮换 | 本轮候选 vs 「Fold classes used」 | 未花费集合优先；声明类必须兑现 | G43 |
| knob 声明 | 区段原型复用合法性 | 本次复用 vs 上次同原型 | 至少换一个 knob 并声明；nav/footer 跨项目连续两次即违规 | G42 |

与 [`../meta/ai-tells.md`](../meta/ai-tells.md) 的分工：§13 管 explore 方向层的意外 wildcard（单轮发散），§14 管单页内逐节重复（单页 uniform）；本引擎五套口径全部管**跨构建**——这一页与上一页、这个项目与上个项目之间。
