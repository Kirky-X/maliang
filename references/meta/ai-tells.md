# AI Tells 黑名单 —— LLM 生成 UI 的常见设计签名

> 规范层。LLM 在生成 UI 时会反复出现一组可识别的"AI 味"签名,这些签名既不专业也易被一眼识破。本文档为硬性禁止清单,生成任何 UI markdown / 框架代码 / 预览 HTML 时,必须自我对照并避开。来源:taste-skill。

每条 Tell 分为「症状」「为什么是 Tell」「替代做法」三段。9 个子分类按出现频率排序。

## 0. 豁免总则(何时不适用)

黑名单治理的是**默认值**:LLM 因为惯性而落进的模式。**有动机的大胆选择不在此列**——"Distinctive is the goal"。命中 Tell 但满足以下任一条件时,不判违规:

1. **DESIGN.md 显式批准**——值已进设计系统并写明理由,是决定不是 slop;清理时不得把系统批准值"修正"回惯例默认。
2. **世界类型自洽**——所选风格(如 neobrutalism / Swiss 极简 / 某品牌既有规范)本身就是该模式的正当来源,且 DESIGN.md 有声明。识别到"反模式 + 正当世界"时,要改写的是理由缺失,不是元素本身。
3. **内容真有动机**——三列布局装的确实是三个并列对等的类目(如"日/周/月"视图切换),而非硬塞三个 feature 凑数。

豁免须**显式记录**(在产物中标注豁免依据,如 `<!-- tell-exempt: 3-col, DESIGN.md 批准 -->`),静默豁免 = 违规。执行侧的误报过滤见 [`../commands/preview.md`](../commands/preview.md) 第 5 节。

## 1. Visual & CSS(视觉与 CSS)

### Tell · Tailwind 渐变文字 + 中性灰背景

- **症状**:`bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent` 配 `bg-slate-900` 底
- **为什么是 Tell**:几乎所有 LLM 生成的 hero 默认套此组合,真实品牌站极少用
- **替代**:用单色高字重 + 一个强调色块/下划线;若必须渐变,限制在品牌色相内 2 阶梯度

### Tell · 全场 `rounded-2xl`

- **症状**:按钮 / 卡片 / 输入框 / 头像全部 `rounded-2xl` 或 `rounded-3xl`
- **为什么是 Tell**:同一圆角无层级关系,失去节奏
- **替代**:按 [`radius.md`](../dimensions/radius.md) 的 sm/md/lg/full 分档,容器 > 控件 > 头像差异化

### Tell · 紫蓝粉渐变背景

- **症状**:`from-purple-600 via-blue-500 to-pink-500` 大面积背景
- **为什么是 Tell**:LLM 默认审美,与具体品牌色无关
- **替代**:背景用中性梯度,品牌色仅做 10% 强调(见 [`color.md`](../dimensions/color.md) 60-30-10)

## 2. Typography(排版)

### Tell · Inter / Geist 单字族全场

- **症状**:全文 `font-sans: 'Inter'` 不混排
- **为什么是 Tell**:专业站点通常标题用 display 字体,正文用 UI 字体
- **替代**:标题用 display(如 Fraunces / Söhne),正文用 Inter / system-ui;或参考 [`design-systems.md`](../dimensions/design-systems.md) 索引中 Vercel/Linear 的字族组合

### Tell · `tracking-tight` 滥用

- **症状**:所有标题统一 `tracking-tight`
- **为什么是 Tell**:display 字体和 UI 字体的字距调整方向相反,统一收紧是惰性
- **替代**:display 加紧(`-0.03em`),UI 字体维持默认或微松

### Tell · `text-balance` / `text-pretty` 装饰性使用

- **症状**:短标题也加 `text-balance`
- **为什么是 Tell**:对短文本无效,显示 LLM 不懂语义
- **替代**:仅长段落(≥ 3 行)用 `text-pretty`,标题不用

## 3. Layout & Spacing(布局与间距)

### Tell · 三列等高卡片网格

- **症状**:feature 区固定 3 列卡片,每张 icon + 标题 + 描述,等高
- **为什么是 Tell**:LLM 默认布局,真实产品极少完全对称(见第 9 节"No 3-Column Card Layouts")
- **替代**:不对称 bento、或纵向叙事 + 一个对比块

### Tell · `max-w-7xl mx-auto px-4` 万能容器

- **症状**:每个 section 都套这层,无差异
- **为什么是 Tell**:失去节奏控制
- **替代**:hero 用 `max-w-screen-2xl`,正文用 `max-w-3xl`,feature 用 `max-w-5xl`,差异化

### Tell · 间距全程 `py-20`

- **症状**:每个 section 上下 `py-20` 完全相同
- **为什么是 Tell**:节奏单调
- **替代**:首屏 `pt-32 pb-20`,中段 `py-16`,尾段 `pt-16 pb-32`,呼吸差异化

## 4. Content & Data(内容与数据)

### Tell · Lorem ipsum 残留

- **症状**:产出含 lorem 字样或无意义占位
- **为什么是 Tell**:LLM 没填充真实意图
- **替代**:用具体场景化文案(产品名、数字、用户角色),哪怕虚构也要具体

### Tell · 假数据全用 100/1k/10k 整数

- **症状**:统计数字清一色 `100+ Users / 1M+ Revenue / 99.9% Uptime`
- **为什么是 Tell**:整数感不可信
- **替代**:用 `2,847` / `127.3K` / `99.97%` 这类带尾数的真实风数据

### Tell · 三档定价 + 中间"Most Popular"

- **症状**:Pricing 区固定 Free / Pro / Enterprise,Pro 高亮
- **为什么是 Tell**:LLM 默认模板
- **替代**:按真实业务设计:单档 + 用量计费、或 4 档 + 自定义高亮、或免定价改 CTA

## 5. External Resources(外部资源)

### Tell · Lucide / Heroicons 图标默认

- **症状**:所有 icon 都用 `lucide-react` 的 `Rocket / Zap / Shield`
- **为什么是 Tell**:Rocket / Zap / Shield 三件套是 LLM 默认,品牌感为零
- **替代**:自定义 SVG,或选用更小众的图标集(Phosphor / Tabler),按 [`icon.md`](../dimensions/icon.md) 选风格

### Tell · Unsplash 占位图带 `?random` 参数

- **症状**:`<img src="https://source.unsplash.com/random/800x600">`
- **为什么是 Tell**:不可复现,且 unsplash random 已停服
- **替代**:用固定 `photos/<id>` URL,或本地图占位 + 注释标注替换位置

### Tell · 默认字体走 Google Fonts CDN

- **症状**:全站 `<link href="fonts.googleapis.com/css2?family=Inter">`
- **为什么是 Tell**:首屏阻塞,违反 [`performance.md`](./performance.md) LCP
- **替代**:`font-display: swap` + 本地 preload 关键字体子集

## 6. Em-dash Ban(英文场景)

### Tell · 滥用 em-dash 连接句子

- **症状**:`The platform — built for speed — ships in days.`
- **为什么是 Tell**:LLM 偏好 em-dash 串句,人类编辑很少这样写
- **替代**:用句号断句、用冒号引出、用括号补充,优先于 em-dash

> **仅英文场景**:中文使用破折号(——)是规范用法,本禁令不适用。

## 7. Lila Rule(柔紫色禁令)

### Tell · 强调色取柔紫 / 莫兰迪紫

- **症状**:primary 取 `#a78bfa` / `#c4b5fd` / `#8b5cf6` 这类柔紫
- **为什么是 Tell**:LLM 默认"高级感"配色,实际让所有产出雷同
- **替代**:选具体品牌色相(参考 [`color-palettes.md`](../dimensions/color-palettes.md) 192 套),避开 indigo-violet-purple 区间;若必须紫,用深紫(`#4c1d95`)或品红紫(`#7c3aed` 偏暖)

## 8. Premium-Consumer Palette Ban(高端消费调色板禁令)

### Tell · 高端品牌默认色 = 黑金 / 米白 / 香槟金

- **症状**:"premium" 触发词立即让 LLM 输出 `bg-black + text-amber-300 + accent-amber-500`
- **为什么是 Tell**:高端 ≠ 黑金;真实高端品牌(Apple / Hermès / Aesop)用克制的中性色 + 一个反预期色
- **替代**:用 [`product-reasoning.md`](./product-reasoning.md) 推理具体品类的高端表达:奢侈品用米白 + 深酒红、科技高端用近黑 + 冷青、家居高端用燕麦 + 苔绿

## 9. No 3-Column Card Layouts(三列卡片布局禁令)

### Tell · Feature 区固定 3 列 icon 卡

- **症状**:经典 "3 个 feature 每个一张卡片 icon+title+desc"
- **为什么是 Tell**:这是 LLM 最强签名,真实产品极少用纯三列对称
- **替代方案**(任选其一):
  1. **Bento Grid**:1 大 + 2 中 + 2 小非对称
  2. **纵向叙事**:每个 feature 一段,左右交替图文
  3. **2x1 + 1**:横排 2 个 + 下方 1 个全宽
  4. **行内嵌**:feature 直接嵌入 hero 文案
  5. **Tab 切换**:多 feature 用 tab 切换,不并列展示

## 10. 生产测试 Tells(真实落地页硬禁模式)

> 来自真实 LLM 落地页测试的硬禁模式——模型"想显得被设计过"时的默认签名。除非 brief 明确要求,否则一律禁止。来源:taste-skill §9.F(em-dash 禁令已并入第 6 节,此处不重复)。

### Hero 与首屏

| 症状                                                       | 为什么是 Tell                                      | 替代                                                         |
| ---------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| Hero 版本标签:`V0.6` / `BETA` / `INVITE-ONLY` / `EARLY ACCESS` | 模型默认的"产品感"装饰,真实产品极少在 hero 标版本 | 删掉;仅当 brief 就是产品发布 / 预览状态时保留                |
| 眉标下微型元句子("以下功能今天全部上线,清单保持很短……")  | 眉标 + 标题 + 正文已足够,元句子是杂讯              | 删掉,信息并入正文                                           |
| Hero 底部装饰文字条(`BRAND. MOTION. SPATIAL.` 式 mono 大写小字条) | 机构作品集陈词滥调                                  | 删掉;仅当条内是真实可点导航或真实状态信息时保留              |
| 节标题右上角悬浮小段落                                     | 与任何元素无对齐关系,是"漂浮的说明"                | 放到标题正下方,或做成对齐的双栏节头                          |
| 垂直旋转文字(90° 竖排的 `INDEX OF WORK`)                  | 作品集网站俗套                                      | 仅当 brief 明确是机构 / 实验向且服务真实构图时使用            |
| 装饰性十字 / 发丝网格线(只为"显得被设计过"画的线)        | 组织不了任何内容                                    | 仅当线在组织真实内容时使用                                    |

### 编号与元标签

| 症状                                                                  | 为什么是 Tell                       | 替代                                                         |
| --------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------ |
| 章节编号眉标:`001 · Capabilities` / `06 · how it works`               | 枚举不是信息,眉标该用平实语言命名主题 | 直接写主题词("能力 / 客户 / 定价")                        |
| `01 / 4` 式图片 / bento 分页标                                        | 数得出来的东西不需要标签             | 删掉                                                          |
| `Index of Work, 2018-2026` 式范围标签眉标                             | 元数据冒充标题                       | 直接说这一节是什么                                            |
| 通用步骤标签:`Stage 1: Install` / `Phase 01` / `Pass One`             | 步骤内容本身才是标签                 | 直接用动宾短语("安装 / 配置 / 上线")                      |
| 中点 `·` 滥用(`foo · bar · baz · qux` 一行连串)                    | 默认分隔符化,读感机械               | 每行元数据 ≤ 1 个 `·`;分隔改用换行 / 发丝线 / 分列          |

### 假产品预览

| 症状                                                                 | 为什么是 Tell            | 替代                                                                  |
| -------------------------------------------------------------------- | ------------------------- | --------------------------------------------------------------------- |
| hero 内 div 假产品 UI(假任务列表 / 假终端 / 假仪表盘)              | 头号 LLM 设计 Tell        | 真实截图 / 生成图 / 真组件预览 / 干脆不放                             |
| 版本脚注(页面 footer 或假截图内 `v1.4.2 · Build 0048` / `last sync 4s ago`) | CLI / devtool 固定件,不是落地页内容 | 营销页删掉;devtool 文档站按真实构建信息呈现                           |
| `Reservation 412 of 800` 式装饰性库存计数                            | 无真实数据的紧迫感表演    | 仅当 brief 是真实限量发售且有真数据时使用                             |

### 文案与署名

| 症状                                                                       | 为什么是 Tell              | 替代                                                                     |
| -------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------ |
| `Quietly in use at` / `Quietly trusted by` 社证标题                        | 假低调是 LLM 签名           | "Trusted by" / "客户包括",或 logo 墙下不放标题                           |
| 诗意栏目标签:`From the field` / `Field notes` / `On our desks`             | 表演式工匠腔                | 平实功能标签("用户评价 / 最新文章"),或不要标签                         |
| 装饰性照片署名:`Field study no. 12 · Ines Caetano` / `Plate 03 · House archive` | 图不见得真是那张,署名是 Pretend | 署名仅用于有授权的真实摄影师;否则删掉,或用一行功能说明("鼠尾草色 6 夸脱款") |
| 假谦虚行业引用("We respect the French ones"式)                           | 俏皮且一眼 AI               | 删掉,写具体事实                                                          |

### 装饰元素与列表

| 症状                                                                       | 为什么是 Tell                     | 替代                                                                       |
| -------------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| 装饰性状态圆点(每个导航项 / 列表行 / badge 前彩点)                      | 无语义的彩色小点是"设计感"补贴    | 仅当圆点传达真实语义状态(服务在线 / 可约名额)且克制使用                   |
| 图上叠 pill 标签(`Brand · 02` / `PLATE · BRAND` 覆盖在照片上)           | 摄影集排版俗套                     | 让图自己说话;需要说明就放图正下方(图外)                                  |
| 长列表 / 规格表每行 `border-t` + `border-b`                                | 每行双线是最懒的排版               | 二选一(行间底线或组顶线)且 sparse;> 5 项换组件(见 taste-skill §4.9) |
| 带底轨的填充进度条当对比图(`bg-zinc-200` 底轨 + 部分填充)               | dashboard 零件搬进落地页           | 数字 + 小图标,或无底轨的细条                                               |
| 天气 / 城市 / 时间条(`LIS 14:23 · 18°C` 放导航或 footer)                | 机构作品集氛围装饰                 | 仅当 brief 明确是分布式工作室 / 旅行品牌 / 实体场所;footer 联系地址不算   |
| 滚动提示:`Scroll to explore` / `↓ scroll` / 动态滚轮图标                 | 用户知道什么是滚动                 | 删掉                                                                        |

## 11. 反射字体清单与饱和外观

> 第 2 节管的是 Inter,这一节管的是训练数据里更广的一层默认:一批"反射字体"与三组高频饱和外观。命中不自动违规(仍走第 0 节豁免总则),但**题材关联永远不构成豁免理由**——书就要衬线、科技就要 mono,正是清单要打破的联想。来源:impeccable(new-work §4 / craft-floor)。

### 反射字体清单(训练数据默认)

Fraunces / Playfair Display / Cormorant / Lora / Crimson / Newsreader / Syne / Space Grotesk / Space Mono / IBM Plex / Inter 当 display 用 / DM Sans / DM Serif / Outfit / Plus Jakarta Sans / Instrument Sans

- **判定**:默认使用其中任一 = 停止寻找的信号。仍要选用时,必须给出"没有其他字体能满足"的理由,题材关联不算理由
- **替代**:按 [`font.md`](../dimensions/font.md) 从受众世界选字;Operate / Read 型页面用系统字体栈 + 工作马 UI 字体即可

### 三大饱和外观(LLM 高频收敛组合)

| 组合     | 构成                                           | 典型误落题材           |
| -------- | ---------------------------------------------- | ----------------------- |
| 奶油纸张 | 奶油底 + 高对比衬线 display + 赤陶 / 信号红强调 | 书卷 / 温暖 / 亲子题材  |
| 近黑霓虹 | 近黑底 + 单一霓虹强调 + 辉光边缘               | 科技 / 潮流题材         |
| 报纸编辑 | 报纸式发丝细线 + 斜体衬线 display + 小号加字距 mono 标签 | 作品集 / 编辑题材       |

- **校准自检**:三种外观本身合法(brief 明确要求时);brief 未锁定审美而产出落在其中之一,即自检失败——"能从品类猜出你的美学,或从品类 + 刻意回避猜出,都算",重做直到两个答案都不明显
- **题材不豁免**:书卷题材不等于奶油纸授权——书布 / 线装 / 护封 / 环衬同样属于那个世界,奶油 + 衬线只是默认穿着题材的外衣

## 自检流程

生成任何 UI 产物后,在 preview 阶段(见 [`../commands/preview.md`](../commands/preview.md) 的 Pre-Flight Check)对照本清单逐项检查,触发任一 Tell 即返工。9 子分类无优先级,均为硬性禁止;冲突时按 [`rules-priority.md`](./rules-priority.md) 的 Style(HIGH) 档处理。

**先过豁免总则再判违规**:命中 Tell 后先查第 0 节三条豁免(DESIGN.md 批准 / 世界类型自洽 / 内容真有动机),豁免成立则显式记录后放行。宁要 3 个高信念发现,不要 40 条 cosmetic 清单——说不出"这条 Tell 让用户付出什么代价/为何读作通用"的,是口味不是缺陷,删除。

## 典型修复对照(Before / After)

同一意图,"默认的写法"与"决定的写法"并置。可对照自检:你的产出更像左列还是右列?

### 对照 1 · 渐变文字 → 单色 + 结构强调

```html
<!-- Before(Tell 1): LLM 默认 hero -->
<h1 class="bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">
  Build faster than ever
</h1>

<!-- After: 字重与字号承担表达,强调色只做下划线 -->
<h1 class="text-6xl font-bold tracking-tight text-neutral-900">
  Build faster than <span class="underline decoration-brand decoration-4">ever</span>
</h1>
```

### 对照 2 · 全场 rounded-2xl → 圆角分档

```css
/* Before(Tell 1): 按钮/卡片/输入框/头像全部 16px */
.btn, .card, .input, .avatar { border-radius: 16px; }

/* After: 容器 > 控件 > 头像 差异化,形成节奏 */
.card   { border-radius: {radius-lg}; }   /* 16px 容器 */
.btn    { border-radius: {radius-md}; }   /* 8px  控件 */
.avatar { border-radius: {radius-full}; } /* 全圆  头像 */
```

### 对照 3 · 三列 feature 卡 → 不对称 bento

```html
<!-- Before(Tell 9): icon + title + desc × 3 等宽等高 -->
<div class="grid grid-cols-3 gap-6"> <FeatureCard/> <FeatureCard/> <FeatureCard/> </div>

<!-- After: 1 大 + 2 小非对称,主角 feature 获得视觉权重 -->
<div class="grid grid-cols-3 gap-6">
  <HeroFeature class="col-span-2 row-span-2"/>  <!-- 主打能力,占 2/3 -->
  <SideFeature/> <SideFeature/>
</div>
```

### 对照 4 · 假数据整数 → 带尾数的真实风

```html
<!-- Before(Tell 4): 整数凑数,不可信 -->
<p>100+ Users · 1M+ Revenue · 99.9% Uptime</p>

<!-- After: 尾数制造"真实存在感",数字参与叙事 -->
<p>2,847 位设计师 · ¥127.3K 月留存流水 · 99.97% 可用性</p>
```

### 对照 5 · 统一 py-20 → 呼吸差异化

```css
/* Before(Tell 3): 每个 section 上下 80px,节奏单调 */
.section { padding: 80px 0; }

/* After: 首屏开阔、中段收紧、尾段留白,呼吸有变化 */
.hero    { padding: 128px 0 80px; }  /* 首屏 pt-32 pb-20 */
.feature { padding: 64px 0; }        /* 中段 py-16 */
.footer  { padding: 64px 0 128px; }  /* 尾段 pt-16 pb-32 */
```
