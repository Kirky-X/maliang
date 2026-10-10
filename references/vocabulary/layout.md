# 布局模式命名词汇

> 模式词汇库。draw-md 阶段描述页面整体布局时使用的标准化命名。来源:taste-skill;仪表盘 6 模式见文末「仪表盘页面布局」节(专业布局术语视频截图提取,2026-10)。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `layout-single-column`| 单列居中,最大宽度限制                            | 文章 / 博客 / 长文案                  |
| `layout-two-column`   | 主内容 + 侧边栏(左或右)                         | 文档站、博客详情、Wiki                |
| `layout-three-column` | 三列(导航 + 内容 + 辅助)                       | IDE、邮件客户端、Slack 类             |
| `layout-bento-grid`   | 不对称网格(1 大 + 多中小)                       | SaaS Dashboard、产品功能展示          |
| `layout-masonry`      | 瀑布流(列高不齐)                                | 图片社区、Pinterest 类                |
| `layout-grid-uniform` | 等大网格(N × M)                                 | 商品列表、卡片墙                      |
| `layout-full-bleed`   | 全出血(无外边距)                                | Hero、媒体、视频背景                  |
| `layout-split-screen` | 50/50 左右分屏                                    | 双 CTA、对比展示、登录页              |
| `layout-stacked`      | 全宽纵向堆叠                                      | 营销落地页、品牌叙事                  |
| `layout-canvas`       | 自由画布(拖拽 / 缩放)                           | 设计工具、白板、Figma 类              |

## 使用规则

- 单页布局模式 ≤ 2 种组合(如 `layout-full-bleed` hero + `layout-single-column` 正文)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节"三列卡片禁令"时,改用 `layout-bento-grid`
- `layout-canvas` 仅用于创意工具,普通 SaaS 禁用
- 移动端默认 `layout-single-column`,跨端时显式标注响应式断点
- 容器宽度差异化:hero `max-w-screen-2xl`、正文 `max-w-3xl`、feature `max-w-5xl`(见 [`ai-tells.md`](../meta/ai-tells.md) 第 3 节)

## 列表密度规则

> 内容密度决定组件选型,长列表的默认排法是 AI 味重灾区。来源:taste-skill §4.9。

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

> 交付前机械检查,任一违反 = 硬性失败。补充 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节"三列卡片禁令"之外的布局专属约束。L3 格子数禁令与 L4 家族多样性增补来源:taste-skill,2026-09 吸收。

### L1 · Zigzag 上限(≤ 3 重复)

- Zigzag 布局(左右交替的图文 section,如 feature 1 左图右文 → feature 2 右图左文)单页重复 ≤ 3 次
- 超过 3 次 = 节奏疲劳,必须改用 `layout-bento-grid` 或 `layout-stacked` + 视觉变体
- 允许的变体:zigzag × 3 + bento + testimonial(非 zigzag)→ 合规

### L2 · Split-header 禁令

- **禁止** Split-header 布局(顶部导航栏左右分屏 50/50,如左 logo + 右全宽图)
- 理由:与 `hero-split` 视觉冲突,导致首屏双焦点;导航栏应保持单行高度
- 替代:导航栏用 `layout-full-bleed` 单行 + Hero 用 `hero-split`

### L3 · Bento 单元数(≤ 6)

- `layout-bento-grid` 单个 bento 区域内单元数 ≤ 6 个
- 超过 6 个 = 视觉拥挤,拆为多个 bento 区域(中间用留白或分隔标题断开)
- 单元大小差异:必须有 1 个"主单元"(≥ 2×2)+ 多个"次单元"(1×1 或 1×2),禁止全等大(否则退化为 `layout-grid-uniform`)
- 格子数 = 内容条数:3 项内容 → 3 格(1+2 或 2+1 非对称),5 项 → 5 格(hero+4 等);网格中部或尾部出现空格子 = 规划错误,**重塑网格形状,禁止贴空白块凑对称**

### L4 · Section 布局重复禁令(≤ 2 个相同布局连续)

- 同一布局模式连续重复 ≤ 2 次(如 `layout-bento-grid` → `layout-bento-grid` → `layout-bento-grid` = 违规)
- 第 3 个 section 必须切换布局(如改为 `layout-single-column` / `layout-split-screen` / `layout-full-bleed`)
- 布局家族多样性下限:8 节及以上的页面,使用的布局家族 ≥ 4 种(家族 = 本文档命名表与仪表盘表共 16 个模式,各计 1 族);`layout-single-column` / `layout-stacked` 基础流式不计入种类统计,防止用正文流凑数
- 同一布局家族整页至多出现 1 次("精选案例"区不得长得像"我们做什么"区);本条**废止**上述"非连续复用合规"口径——bento → single → bento 现在违规,同一家族第 2 次出现必须换家族

### L5 · Marquee 单页 ≤ 1

- Marquee(横向滚动 logo 墙 / 客户 logo 滚动)单页 ≤ 1 个
- 多个 marquee = 动效冗余 + 视觉噪音,触发 [`ai-tells.md`](../meta/ai-tells.md) 装饰性动画
- Marquee 必须 `prefers-reduced-motion: reduce` 时停止滚动,改为静态网格

## 高级布局量化对照

> "普通排法 vs 高级排法"量化对照——高级感不是乱,是量出来的刻意。来源:视频研究 v03。

| 模式             | 普通排法(AI 默认)                         | 高级排法(量化参数)                                                 | 适用场景            |
| ---------------- | ------------------------------------------- | -------------------------------------------------------------------- | ------------------- |
| 卡片错位 STAGGER | 对齐轴 1 条、错位量 0、等宽卡 3 张          | 对齐轴 3 条、错位量 ≤ 74px、等宽卡 0;标题各自另起一条轴             | 双列瀑布流 / 内容流 |
| 大图主导 SCALE   | 主体占比 16%、最大:最小 1.4×、等大块 3 个  | 主体占比 52%、最大:最小 7.1×、等大块 0;图吃半屏顶到两边,其余退辅助 | 封面型首页 / 旅拍   |
| 非对称 ASYMMETRY | 块宽比 1:1、最大块占比 25%、等大块 4 个     | 块宽比 7:3、最大块占比 62%、等大块 0;右侧收成两块小的               | 图文混排首页        |
| 层叠 OVERLAP     | 层数 1、重叠处 0、明度层次 1                | 层数 3、重叠处 3、明度层次 3;卡片压进图里 42px                       | 播放页 / 主题卡     |
| 留白 WHITESPACE  | 元素数 14、留白占比 18%、最小间距 10px      | 元素数 5、留白占比 68%、最小间距 34px;空出来的地方最大              | 天气 / 单一指标页   |

## 仪表盘页面布局

> 整页级仪表盘布局:同一句描述词换一种排法的 6 种解法,每条附视频痛点锚点(什么症状用什么布局)。来源:专业布局术语视频截图提取(2026-10,DASHBOARD · WEB PAGE LAYOUT 系列 01-06)。主表 10 模式作页内区块组合;本节 6 模式作整页主布局,单页选 1 种。

### 命名表

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `layout-hero-module` | 主次布局(Hero Module):主模块占 8 列跨两行,次要指标 4 列小模块排右侧与下方,全页唯一视觉重心 | 数据仪表盘首屏,核心指标要统治力 |
| `layout-stacked-bands` | 通栏横带(Stacked Bands):自上而下概览 / 趋势 / 明细三层,每层横贯全宽,层间 48px | 报表型页面;解「模块东一块西一块」 |
| `layout-main-aside` | 主区加右侧窄栏(Main + Aside):主区 8 列,右侧 320px 窄栏 sticky(top 0)放日程与动态,主区单独滚动 | 日程 / 协作页;解「滚下去提醒就没了」 |
| `layout-floating-panels` | 画布铺满加浮动面板(Full-bleed Canvas):全幅画布作底,指标与列表成浮动面板贴四角叠上层,边距 16px | 视觉主导仪表盘;解「图和数字各占一半」 |
| `layout-kanban-columns` | 看板分列(Kanban Columns):按状态等宽列(基准 216px),列头名称 + 计数,列内纵向堆叠,整体横向滚动 | 任务 / 项目追踪;解「不知道进行到哪一步」 |
| `layout-timeline-swimlanes` | 时间轴泳道(Timeline Swimlanes):顶部时间刻度,每行一条泳道,事项按起止时间绘横条,竖向参考线标当前时刻 | 排期 / 资源 / 会程;解「看不出谁和谁撞了」 |

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

- 6 模式为整页级主布局,单页选 1 种;页内区块再用主表 10 模式组合;L4 家族统计两表都计入(各计 1 族)
- `layout-hero-module`:主模块唯一,次模块面积禁超过主模块;8/4 列为桌面基准,窄断点降级单列堆叠
- `layout-stacked-bands`:带数 ≤ 4;层间 48px 写成 spacing token;带与带禁频繁换底色(重色只给一处,见 [`../templates/page/dashboard-styles.md`](../templates/page/dashboard-styles.md) 配色占比公式);带内内容选型:概览 → [number-motion.md](number-motion.md)、趋势 → [charts.md](charts.md)、明细 → [tables.md](tables.md)
- `layout-main-aside`:aside 恒 320px + `top: 0`;主区独立滚动时锁 body 滚动防双滚动条;移动端 aside 降级底部 section 或 sheet(挂 [sheet-drawer.md](sheet-drawer.md))
- `layout-floating-panels`:画布底即 `layout-full-bleed`,本模式在其上加面板层;面板 ≤ 4 贴四角,统一 16px 边距;媒体之上的面板必须实底或加 scrim,保文字对比度(见 [accessibility.md](../meta/accessibility.md));画布素材走 [visual-assets.md](../meta/visual-assets.md)
- `layout-kanban-columns`:列等宽(基准 216px)禁自适应挤压;列头计数与列内卡片数一致;横向滚动配 scroll-snap,禁劫持竖向页面滚动;列内拖拽排序走 [spring-reorder](../motion-skeletons/spring-reorder.md) 骨架
- `layout-timeline-swimlanes`:泳道 ≤ 6;时间刻度行 sticky;NOW 竖线随当前时刻刷新;横条起止吸附刻度(整点 / 半点)
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
