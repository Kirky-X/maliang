# 布局模式命名词汇

> 模式词汇库。draw-md 阶段描述页面整体布局时使用的标准化命名。来源:taste-skill。

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

> 交付前机械检查,任一违反 = 硬性失败。补充 [`ai-tells.md`](../meta/ai-tells.md) 第 9 节"三列卡片禁令"之外的布局专属约束。

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

### L4 · Section 布局重复禁令(≤ 2 个相同布局连续)

- 同一布局模式连续重复 ≤ 2 次(如 `layout-bento-grid` → `layout-bento-grid` → `layout-bento-grid` = 违规)
- 第 3 个 section 必须切换布局(如改为 `layout-single-column` / `layout-split-screen` / `layout-full-bleed`)
- 允许:相同布局非连续出现(如 bento → single → bento = 合规)

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
