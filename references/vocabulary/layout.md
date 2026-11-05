# 布局模式命名词汇

> 模式词汇库。draw-md 阶段描述页面整体布局时使用的标准化命名。仪表盘与移动端整页布局见文末两节。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `layout-single-column`| 单列居中,最大宽度限制                            | 文章 / 博客 / 长文案                  |
| `layout-two-column`   | 主内容 + 侧边栏(左或右)                         | 文档站、博客详情、Wiki                |
| `layout-three-column` | 三列(导航 + 内容 + 辅助)                       | IDE、邮件客户端、Slack 类             |
| `layout-bento-grid`   | 不对称网格(1 大 + 多中小);深色多彩变体:近黑底+多彩卡片,主网格比 1.42:1、圆角 26、标题字重 800 | SaaS Dashboard、产品功能展示          |
| `layout-masonry`      | 瀑布流(列高不齐)                                | 图片社区、Pinterest 类                |
| `layout-grid-uniform` | 等大网格(N × M)                                 | 商品列表、卡片墙                      |
| `layout-full-bleed`   | 全出血(无外边距)                                | Hero、媒体、视频背景                  |
| `layout-split-screen` | 50/50 左右分屏                                    | 双 CTA、对比展示、登录页              |
| `layout-stacked`      | 全宽纵向堆叠                                      | 营销落地页、品牌叙事                  |
| `layout-canvas`       | 自由画布(拖拽 / 缩放)                           | 设计工具、白板、Figma 类              |

## 页内构图节奏

- **相邻同构图禁令**:同一构图不许相邻两节连用(单构图形页面除外);镜像 split ≤1 次;密节(网格/表)后必接疏节(statement);整页 3-6 种构图
- **节的"质量"定义**:头+一段落只是 head block,不算节;正文最宽行须达 10/12 列;空右半=稀疏签名
- **节首十二式**(章节开头的正向替代库,替代眉标):标题自报 / 段内 lead-in / 首字下沉 / 一符多用的规线 / 图形级数字 / 真 ol 计数 / 图下 caption / 页边注 / 换纸 / 页眉页码 / 持续性符号——合法条件:承载事实、去处或标识,不为装饰而装饰

## 使用规则

- 单页布局模式 ≤ 2 种组合(如 `layout-full-bleed` hero + `layout-single-column` 正文)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节"三列卡片禁令"时,改用 `layout-bento-grid`
- `layout-canvas` 仅用于创意工具,普通 SaaS 禁用
- 移动端默认 `layout-single-column`,跨端时显式标注响应式断点
- 容器宽度差异化:hero `max-w-screen-2xl`、正文 `max-w-3xl`、feature `max-w-5xl`(见 [`ai-tells.md`](../meta/ai-tells.md) 第 3 节)

## 列表密度规则

> 内容密度决定组件选型,长列表的默认排法是 AI 味重灾区。

- **> 5 项的列表禁止默认 `<ul>` + `divide-y`**,必须换组件:双栏分组 / 卡片网格 / tabs / 横向 scroll-snap pills / 轮播 / marquee
- 规格表(spec sheet)四种替代:

| 替代方案      | 形式                                   |
| ------------- | -------------------------------------- |
| 2 列卡阵      | 规格项拆两列紧凑卡阵,替代单列长表     |
| 滚动 pills    | 横向 scroll-snap 药丸,横滑查看全部    |
| 分组块        | 3 簇分组,簇间 1 条软分隔              |
| 精华 + 折叠   | 露出精华 3-4 项,其余折叠进"查看全部" |

## 在 draw-md 中的写法

```markdown
## Layout
- pattern: layout-stacked
- sections:
  - { name: hero, layout: layout-full-bleed }
  - { name: features, layout: layout-bento-grid, columns: 4 }
  - { name: testimonial, layout: layout-single-column, max_width: 3xl }
  - { name: pricing, layout: layout-grid-uniform, columns: 3 }
```

## 生产级硬规则

> 交付前机械检查,任一违反 = 硬性失败。补充 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节"三列卡片禁令"之外的布局专属约束。L3 格子数禁令与 L4 家族多样性增补

### L1 · Zigzag 上限(≤ 3 重复)

- Zigzag 布局(左右交替的图文 section,如 feature 1 左图右文 → feature 2 右图左文)单页重复 ≤ 3 次
- 超过 3 次 = 节奏疲劳,必须改用 `layout-bento-grid` 或 `layout-stacked` + 视觉变体
- 允许的变体:zigzag × 3 + bento + testimonial(非 zigzag)→ 合规

### L2 · Split-header 禁令

- **禁止** Split-header 布局(顶部导航栏左右分屏 50/50,如左 logo + 右全宽图)
- 理由:与 `hero-split` 视觉冲突,导致首屏双焦点;导航栏应保持单行高度
- 替代:导航栏用 `layout-full-bleed` 单行 + Hero 用 `hero-split`

### L3 · Bento 单元数(≤ 6)

- `layout-bento-grid` 单个 bento 区域内单元数 ≤ 6 个(canonical;数量口径分工:区段原型 5-8 见 [f1-bento-grid](../components/f1-bento-grid.md),整页墙 ≤10 见 [`../templates/bento-grid.md`](../templates/bento-grid.md))
- 超过 6 个 = 视觉拥挤,拆为多个 bento 区域(中间用留白或分隔标题断开)
- 单元大小差异:必须有 1 个"主单元"(≥ 2×2)+ 多个"次单元"(1×1 或 1×2),禁止全等大(否则退化为 `layout-grid-uniform`)
- 格子数 = 内容条数:3 项内容 → 3 格(1+2 或 2+1 非对称),5 项 → 5 格(hero+4 等);网格中部或尾部出现空格子 = 规划错误,**重塑网格形状,禁止贴空白块凑对称**

### L4 · Section 布局重复禁令(≤ 2 个相同布局连续)

- 同一布局模式连续重复 ≤ 2 次(如 `layout-bento-grid` → `layout-bento-grid` → `layout-bento-grid` = 违规)
- 第 3 个 section 必须切换布局(如改为 `layout-single-column` / `layout-split-screen` / `layout-full-bleed`)
- 布局家族多样性下限:8 节及以上的页面,使用的布局家族 ≥ 4 种(家族 = 本文档三张命名表共 31 个模式,各计 1 族;「页内模块展开交互」3 式是页内动效,不计入);`layout-single-column` / `layout-stacked` 基础流式不计入种类统计,防止用正文流凑数
- 同一布局家族整页至多出现 1 次("精选案例"区不得长得像"我们做什么"区);本条**废止**上述"非连续复用合规"口径——bento → single → bento 现在违规,同一家族第 2 次出现必须换家族

### L5 · Marquee 单页 ≤ 1

- Marquee(横向滚动 logo 墙 / 客户 logo 滚动)单页 ≤ 1 个
- 多个 marquee = 动效冗余 + 视觉噪音,触发 [`ai-tells.md`](../meta/ai-tells.md) 装饰性动画
- Marquee 必须 `prefers-reduced-motion: reduce` 时停止滚动,改为静态网格

## 高级布局量化对照

> "普通排法 vs 高级排法"量化对照——高级感不是乱,是量出来的刻意。

| 模式             | 普通排法(AI 默认)                         | 高级排法(量化参数)                                                 | 适用场景            |
| ---------------- | ------------------------------------------- | -------------------------------------------------------------------- | ------------------- |
| 卡片错位 STAGGER | 对齐轴 1 条、错位量 0、等宽卡 3 张          | 对齐轴 3 条、错位量 ≤ 74px、等宽卡 0;标题各自另起一条轴             | 双列瀑布流 / 内容流 |
| 大图主导 SCALE   | 主体占比 16%、最大:最小 1.4×、等大块 3 个  | 主体占比 52%、最大:最小 7.1×、等大块 0;图吃半屏顶到两边,其余退辅助 | 封面型首页 / 旅拍   |
| 非对称 ASYMMETRY | 块宽比 1:1、最大块占比 25%、等大块 4 个     | 块宽比 7:3、最大块占比 62%、等大块 0;右侧收成两块小的               | 图文混排首页        |
| 层叠 OVERLAP     | 层数 1、重叠处 0、明度层次 1                | 层数 3、重叠处 3、明度层次 3;卡片压进图里 42px                       | 播放页 / 主题卡     |
| 留白 WHITESPACE  | 元素数 14、留白占比 18%、最小间距 10px      | 元素数 5、留白占比 68%、最小间距 34px;空出来的地方最大              | 天气 / 单一指标页   |

## 仪表盘页面布局

> 整页级仪表盘布局:同一句描述词换一种排法的解法库,每条附痛点锚点(什么症状用什么布局)。主表 10 模式作页内区块组合;本节模式作整页主布局,单页选 1 种。

### 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `layout-hero-module` | 主次布局(Hero Module):主模块占 8 列跨两行,次要指标 4 列小模块排右侧与下方,全页唯一视觉重心 | 数据仪表盘首屏,核心指标要统治力 |
| `layout-stacked-bands` | 通栏横带(Stacked Bands):自上而下概览 / 趋势 / 明细三层,每层横贯全宽,层间 48px | 报表型页面;解「模块东一块西一块」 |
| `layout-main-aside` | 主区加右侧窄栏(Main + Aside):主区 8 列,右侧 320px 窄栏 sticky(top 0)放日程与动态,主区单独滚动 | 日程 / 协作页;解「滚下去提醒就没了」 |
| `layout-floating-panels` | 画布铺满加浮动面板(Full-bleed Canvas):全幅画布作底,指标与列表成浮动面板贴四角叠上层,边距 16px | 视觉主导仪表盘;解「图和数字各占一半」 |
| `layout-kanban-columns` | 看板分列(Kanban Columns):按状态等宽列(基准 216px),列头名称 + 计数,列内纵向堆叠,整体横向滚动 | 任务 / 项目追踪;解「不知道进行到哪一步」 |
| `layout-timeline-swimlanes` | 时间轴泳道(Timeline Swimlanes):顶部时间刻度,每行一条泳道,事项按起止时间绘横条,竖向参考线标当前时刻 | 排期 / 资源 / 会程;解「看不出谁和谁撞了」 |
| `layout-goal-anchor` | 目标锚点(Goal Anchor):左侧大标题+进度条突出今日目标,快捷操作紧随其下,右侧助手栏,统计收底部;日/周切换全页同步 | 目标/习惯/打卡型首页 |
| `layout-trend-central` | 趋势居中(Trend Central):趋势图居中主位,关键指标叠印图前,右侧明细稳定;切换指标数字与曲线同步 | 监控/分析页(趋势即主角) |
| `layout-info-three-column` | 信息三列(Info Three-Column):同类信息纵向三列分区,少量强调色只标状态与差值 | 状态总览/环境监测页 |
| `layout-central-axis` | 中央轴观测(Central Axis):中央主视图+双侧信息栏+底部时间轴,衬线大编号配等宽读数 | 观测/监测台 |
| `layout-industrial-fixed-action` | 工业固定操作区(Industrial Fixed Action):右侧固定操作区贯穿到底,左列筛选+玻璃质感表格,选中态联动(数值待核) | 工业操作台/密集操作后台 |
| `layout-glass-dot-matrix` | 毛玻璃点阵(Glass Dot Matrix):浅灰毛玻璃点阵读数,月份带串起整页,月份指标共享状态 | 月报/数据集览页 |
| `layout-console-three-pane` | 三栏控制台(Three-Pane Console):深浅分区三栏;点模式项房名/照片/温度联动一起换 | 智能家居/设备控制台(与 `layout-info-three-column` 互见:彼条静态信息分区,本条模式联动切换) |
| `layout-number-anchor` | 数字锚点(Number Anchor):超大数字作视觉锚点+2×2 紧凑网格+右侧独立纵向面板,层级靠比例/字号/留白 | 单指标强调页 |
| `layout-magazine-editorial` | 杂志编辑式(Magazine Editorial):顶部文字大图分栏+三列图片网格,细线分格克制留白,非卡片化 | 内容/编辑式仪表盘 |

### AI 描述词对照

> 视频提示词原文;落 draw-md 时按模式名与使用规则参数化,不整段照抄。

| # | 布局 | AI 描述词 |
| --- | --- | --- |
| 01 | 主次布局 | 首屏采用主次布局(Hero Module),主模块占 8 列跨两行,次要指标用 4 列小模块排在右侧和下方,全页只有一个视觉重心。 |
| 02 | 通栏横带 | 页面采用通栏横带布局(Stacked Bands),自上而下分为概览、趋势、明细三层,每层横贯全宽,层与层之间留 48 像素间距。 |
| 03 | 主区加右侧窄栏 | 采用主区加侧栏布局(Main + Aside),主区占 8 列,右侧 320 像素窄栏粘性定位(Sticky),放日程与动态,主区单独滚动。 |
| 04 | 画布铺满加浮动面板 | 主区用全幅画布作底(Full-bleed Canvas),指标与列表做成浮动面板(Floating Panels)叠在上层,面板贴四角排布,留 16 像素边距。 |
| 05 | 看板分列 | 采用看板分列布局(Kanban Columns),按状态分为等宽列,列头显示名称与计数,列内纵向堆叠,整体可横向滚动。 |
| 06 | 时间轴泳道 | 采用时间轴泳道布局(Timeline Swimlanes),顶部为时间刻度,每行一条泳道,事项按起止时间绘制为横条,用竖向参考线标记当前时刻。 |

### 使用规则

- 本节模式为整页级主布局,单页选 1 种;页内区块再用主表 10 模式组合;L4 家族统计两表都计入(各计 1 族)
- `layout-hero-module`:主模块唯一,次模块面积禁超过主模块;8/4 列为桌面基准,窄断点降级单列堆叠
- `layout-stacked-bands`:带数 ≤ 4;层间 48px 写成 spacing token;带与带禁频繁换底色(重色只给一处,见 [`../templates/page/dashboard-styles.md`](../templates/page/dashboard-styles.md) 配色占比公式);带内内容选型:概览 → [number-motion.md](number-motion.md)、趋势 → [charts.md](charts.md)、明细 → [tables.md](tables.md)
- `layout-main-aside`:aside 恒 320px + `top: 0`;主区独立滚动时锁 body 滚动防双滚动条;移动端 aside 降级底部 section 或 sheet(挂 [sheet-drawer.md](sheet-drawer.md))
- `layout-floating-panels`:画布底即 `layout-full-bleed`,本模式在其上加面板层;面板 ≤ 4 贴四角,统一 16px 边距;媒体之上的面板必须实底或加 scrim,保文字对比度(见 [accessibility.md](../meta/accessibility.md));画布素材走 [visual-assets.md](../meta/visual-assets.md)
- `layout-kanban-columns`:列等宽(基准 216px)禁自适应挤压;列头计数与列内卡片数一致;横向滚动配 scroll-snap,禁劫持竖向页面滚动;列内拖拽排序走 [spring-reorder](../motion-skeletons/spring-reorder.md) 骨架
- `layout-timeline-swimlanes`:泳道 ≤ 6;时间刻度行 sticky;NOW 竖线随当前时刻刷新;横条起止吸附刻度(整点 / 半点)
- `layout-goal-anchor`:今日目标是全页唯一主视觉,进度条选型走 [charts.md](charts.md);日/周切换数字与列表同步全换
- `layout-trend-central`:叠印指标 ≤ 3,压图须保对比(见 [accessibility.md](../meta/accessibility.md));切指标数字与曲线同帧过渡
- `layout-info-three-column`:强调色只标状态与差值,禁做装饰;三列列宽一致,列内同类信息
- `layout-central-axis`:双侧信息栏对称等宽,底部时间轴 sticky;衬线大编号只做标识不做正文
- `layout-industrial-fixed-action`:右侧操作区固定宽贯穿到底;玻璃表格配方见 [`../dimensions/glass-effect.md`](../dimensions/glass-effect.md)(行内数值待核)
- `layout-glass-dot-matrix`:点阵读数是装饰性呈现,关键数值须有明文备份;月份带共享选中状态,切月全页联动
- `layout-console-three-pane`:点模式项三栏联动同换(房名/照片/温度),禁只换一栏;联动切换选本条,静态分区选 `layout-info-three-column`
- `layout-number-anchor`:层级靠比例/字号/留白表达,禁加框强调;2×2 网格与右侧面板不抢数字焦点
- `layout-magazine-editorial`:细线分格代替卡片阴影,禁卡片化;图片网格 3 列为基准
- `layout-main-aside` 日历联动变体:右栏日历点选日期,下方切当日安排,分栏独立滚动但选择联动
- `layout-floating-panels` 地图变体:画布为地图,指标/筛选/记录面板环绕;空间信息归地图,趋势图表归侧板,分工不重复
- **内容形态决定组件形态**:照片管氛围、封面管内容、图表管数据——不同模块用不同视觉形态,统一间距/圆角/字阶收拢,禁全卡片化
- 移动端 6 模式全部降级纵向单列流;横向滚动只允许出现在 kanban 列区与泳道区内部

### 在 draw-md 中的写法

```markdown
## Layout (dashboard)
- pattern: layout-hero-module
- hero: { span: 8col, rows: 2 }, secondary: 4col-right-below
- mobile: single-column-stack

## Layout (project-board)
- pattern: layout-kanban-columns
- columns: 5 × 216px, header: name+count, scroll: horizontal-snap
- drag: spring-reorder
```

## 页内模块展开交互

> 页内模块的就地展开与让位(页内动效,不计入 L4 整页家族统计):展开只动受影响的格子/行,其余连续让位,禁整块重绘跳变;`prefers-reduced-motion` 直达终态。

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `grid-cell-expand-fullrow` | 宫格撑行:两列宫格点击一格横向撑成整行、高度增加,其余格子依次重排让位,不跳页 | 功能宫格就地看详情 |
| `schedule-track-expand` | 日程原位展开:点日程项原位展开详情,其余项连续让位,左侧光点同步标记当前项 | 日程/时间轴列表 |
| `accordion-exclusive-expand` | 互斥手风琴:高度逐帧撑开,箭头旋转变身,旧项收起新项展开同步进行,页面不猛跳 | FAQ、设置组、表单分段(与 [cards.md](cards.md) `card-collapsible` 互见:彼条单卡折叠容器,本条多段互斥;长文展开见 [typography.md](typography.md) `type-expand-fulltext`) |

## 移动端页面布局

> 整页级移动 App / 小程序布局公式:标题、搜索、分类、主块、列表的量化排法。与 [`../templates/page/mobile-layouts.md`](../templates/page/mobile-layouts.md)「移动端五式」分工:五式选设计语言气质,本节选整页布局公式,先五式后本节叠加使用。

### 命名表

| 模式名 | 视频组件 | 视觉特征 | 适用场景 |
| --- | --- | --- | --- |
| `layout-wide-caps-list` | 大字标题加整宽大图列表 Wide Caps Image List | 两行宽体大写标题 + 圆角搜索栏(右配黑色圆形筛选钮)+ 分类标签选中黑底;每项整宽圆角大图(16:10),图下一行名称 / 参数 / 圆形箭头钮,逐项进入 | 商品 / 房源目录类列表首屏 |
| `layout-hero-overlay` | 大图头块叠信息 Hero Image Overlay | 头块圆角大图约占屏高 1/3,标题 / 倒计时 / 主按钮(×3)直接压图上,深色渐变保可读;下方等宽日期块当前项近黑(#151213)实心,底部平滑曲线串数值,圆点随当前项移动 | 旅行 / 天气 / 日程类首页 |
| `layout-black-hero` | 黑白两档主次 Black Hero Hierarchy | 浅灰底(#F4F3F4),主信息块近黑(#0B0708)配白字,其余信息块一律白;分类选中项同样变黑;下方黑色横幅(×2)呼应;全页禁第三种强调色 | 阅读 / 工具类首页的两档层级 |
| `layout-bento-grid` | 大色块网格 Bento Grid(移动端规格) | 已有模式,本行补移动端量化:首块整行品牌色填充,超大数字 + 环形进度;标题超粗(900)中英两行;其余四列等宽小格浅色低饱和,圆角统一 24 | 习惯 / 统计 / 仪表类首屏 |
| `layout-poster-dial` | 海报大字加半圆转盘 Poster Dial Layout | 方块粗体巨字标题(52px)叠双色;半圆弧转盘选项沿弧排列(30°/项),选中项转到指针正上方并放大;下方超大等宽数字 + 单一主按钮;底部撞色底栏 | 专注 / 计时类单任务页(转盘交互见 [pickers.md](pickers.md) `picker-radial-arc`) |
| `layout-stacked-deck` | 叠放堆栈 Stacked Deck | 主图居中占屏宽 82%,后面两张依次缩到 0.94 / 0.88 向上错开露边;上拖过阈值最前一张飞出、后卡依次补位,页码同步更新 | 房型 / 内容卡切换(拖拽细节见 [buttons.md](buttons.md) `card-stack-pull` + `card-fling`) |

### AI 描述词对照

> 视频提示词原文;落 draw-md 时按模式名与使用规则参数化,不整段照抄。

| # | 布局 | AI 描述词 |
| --- | --- | --- |
| 01 | 大字标题加整宽大图列表 | 宽体标题大图列表(Wide Caps Image List):顶部两行宽体大写无衬线标题,下面一条圆角搜索栏右侧配黑色圆形筛选按钮,再下一排分类标签,选中项黑底;列表每一项是整宽圆角大图,图下一行放名称、参数和圆形箭头按钮,上下滑动逐项进入。 |
| 02 | 大图头块叠信息 | 大图头块叠信息(Hero Image Overlay):顶部一块圆角大图,高度约占屏幕三分之一,标题、倒计时和主按钮直接压在图上,图上叠深色渐变保证可读;下方白底信息块里一排等宽日期块,当前项用近黑色实心填充,底部一条平滑曲线串起每天的数值,圆点跟着当前项移动。 |
| 03 | 黑白两档主次 | 黑白两档层级(Black Hero Hierarchy):页面用浅灰底,最主要的信息块用近黑色填充配白字,其余信息块一律白色;顶部分类横向滚动,选中项同样变成近黑色;下方再放一条黑色横幅与主块呼应;全页不用第三种强调色。 |
| 04 | 大色块网格 | 便当盒网格(Bento Grid):首块占满整行、用品牌亮黄填充,放一个超大数字,右侧一个环形进度;页面其余部分用浅灰底;标题用超粗黑体中英两行;下面四列等宽小格,每格用浅色低饱和打底,圆角统一 24。 |
| 05 | 海报大字加半圆转盘 | 海报巨字转盘(Poster Dial Layout):顶部用方块粗体英文巨字做标题,黑白两色叠在紫色底上;中间一段半圆弧形转盘,选项沿弧排列,选中项转到指针正上方并放大;下方一个超大等宽数字和一个黑色主按钮;底部一条撞色底栏。 |
| 06 | 叠放堆栈 | 叠放堆栈切换(Stacked Deck):顶部两行细长宽体标题加一排分类;主图居中占屏幕宽度 82%,后面两张依次缩到 0.94 和 0.88 倍、向上错开露出边缘;向上拖过阈值时最前面一张飞出,后面依次补位,底部页码同步更新。 |

### 使用规则

- 6 模式为整页级主布局,单页选 1 种;先用移动端五式定气质,再用本节定布局;L4 家族统计计入(各计 1 族)
- `layout-wide-caps-list`:大图 16:10 统一比例,首屏 3 行为限;逐项进入挂 [pro-motion.md](pro-motion.md) `stagger-spring-cascade`;黑色筛选钮是主色唯一落点,分类标签选中黑底与其同色
- `layout-hero-overlay`:压图文字必须深色渐变托底(对比度达标,见 [accessibility.md](../meta/accessibility.md));日期块当前项实心填充是状态语义;曲线串数值走 [charts.md](charts.md),圆点移动 ≤ 400ms
- `layout-black-hero`:全页两档色(浅灰 / 近黑)禁第三种强调色(与 dashboard-styles「重色只给一处」同源纪律);选中态 = 变黑,禁用描边 / 变色双轨;黑色横幅 ×2 为呼应上限
- `layout-bento-grid`:移动端规格沿用主表 L3(单元 ≤ 6、主单元 ≥ 2×2);全页一个圆角值(24);环形进度走 [charts.md](charts.md) `chart-ring-draw`
- `layout-poster-dial`:转盘档位 ≤ 7,30°/项为基准,选中项放大 ≤ 1.2 倍;中文标题禁照搬英文方块字(换字重不换字体);撞色底栏是全页唯一撞色落点
- `layout-stacked-deck`:堆叠层 ≤ 3(前 + 后两张),缩放 0.94 / 0.88 等差;飞出阈值 + 速度判据见 [gesture-arbitration.md](../motion-skeletons/gesture-arbitration.md),速度翻张参数见 `card-fling`;补位与页码同帧更新
- 移动端全部触控驱动,无 hover;触控目标 ≥ 44px;`prefers-reduced-motion` 降级:逐项进入直接显示、转盘 / 堆栈直接切换

### 在 draw-md 中的写法

```markdown
## Layout (van-list)
- pattern: layout-wide-caps-list
- title: 2-line-caps, image_ratio: 16:10, rows: 3
- entry: stagger-spring-cascade

## Layout (focus-timer)
- pattern: layout-poster-dial
- title: 52px-block, dial: { arc: 180deg, step: 30deg, magnify: 1.2 }
- cta: single-primary, bar: contrast-color
```
