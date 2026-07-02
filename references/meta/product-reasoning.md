# 产品类型推理 —— 从 Brief 到设计方向

> 规范层。基于产品类型推理出全套设计方向,避免 LLM 默认审美(见 [`ai-tells.md`](./ai-tells.md))。本文列出 10+ 常见产品类型的推理规则,完整 161 类索引见 [`../dimensions/color-palettes.md`](../dimensions/color-palettes.md) 的 192 套调色板(产品类型 × 主题)。来源:ui-ux-pro-max-skill。

## 1. 推理维度

输入一个产品 brief,推理以下 7 个维度,作为 design-md 的输入:

| 维度                | 含义                                   | 输出示例                              |
| ------------------- | -------------------------------------- | ------------------------------------- |
| Recommended_Pattern | 推荐布局模式(见 [`vocabulary/`](../vocabulary/)) | `hero-centered / bento-grid`          |
| Style_Priority      | 设计风格优先级(从高到低)             | `minimal > functional > decorative`   |
| Color_Mood          | 色彩情绪(对应 color-palettes.md 桶)  | `calm-neutral / energetic-warm`       |
| Typography_Mood     | 字体情绪(display + UI)                | `editorial-serif + neutral-sans`      |
| Key_Effects         | 关键视觉效果(限定 ≤ 3 个)            | `subtle-shadow / sticky-stack`        |
| Decision_Rules      | 决策规则(冲突时如何选)               | `若信息密度高 → 优先表格胜过卡片`    |
| Anti_Patterns       | 反模式(禁止出现的模式)               | `禁三列卡片 / 禁渐变文字`             |

## 2. 常见产品类型示例(10+)

### 2.1 SaaS Dashboard(B 端数据后台)

- **Recommended_Pattern**: `sidebar-nav + data-table + filter-bar`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `cool-neutral`(中性灰为主,数据色相区分)
- **Typography_Mood**: `neutral-sans only`(Inter / system-ui,无 display 字体)
- **Key_Effects**: `subtle-shadow / hover-bg-highlight / loading-skeleton`
- **Decision_Rules**: 信息密度 > 美观;表格优先于卡片;过滤项常驻而非模态
- **Anti_Patterns**: 禁视差滚动 / 禁装饰动画 / 禁三列卡片网格
- **Dials**(见 [`dials.md`](./dials.md)): VARIANCE=2 / MOTION=2 / DENSITY=8

### 2.2 Marketing Landing Page(营销落地页)

- **Recommended_Pattern**: `hero-centered + feature-bento + testimonial-strip + pricing-cta`
- **Style_Priority**: `decorative > minimal > functional`
- **Color_Mood**: `energetic-warm` 或 `brand-bold`
- **Typography_Mood**: `display-serif + neutral-sans`
- **Key_Effects**: `scroll-reveal-stagger / sticky-stack / number-counter`
- **Decision_Rules**: 转化率 > 信息完整;首屏 CTA 1 tap 可达;滚动节奏强
- **Anti_Patterns**: 禁纯文字 hero / 禁 3 列等高卡片(见 [`ai-tells.md`](./ai-tells.md) 第 9 节)
- **Dials**: VARIANCE=7 / MOTION=6 / DENSITY=4

### 2.3 E-commerce Product Detail(电商详情页)

- **Recommended_Pattern**: `gallery-left + buy-box-right + review-list + related-grid`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `brand-bold`(品牌色为主,商品图不被压制)
- **Typography_Mood**: `neutral-sans + price-display`(数字特殊字体)
- **Key_Effects**: `image-zoom / sticky-buy-box / review-carousel`
- **Decision_Rules**: 商品图纯背景;价格显眼;加入购物车 1 tap;评价靠前
- **Anti_Patterns**: 禁花哨背景干扰商品 / 禁价格文字过小 / 禁隐藏加购按钮
- **Dials**: VARIANCE=4 / MOTION=4 / DENSITY=6

### 2.4 Content Community(内容社区 / Feed)

- **Recommended_Pattern**: `top-tabs + waterfall-feed + floating-compose`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `calm-neutral`(内容多样,UI 退到背景)
- **Typography_Mood**: `neutral-sans only`
- **Key_Effects**: `infinite-scroll / pull-refresh / card-hover-lift`
- **Decision_Rules**: 内容图主导;UI 元素降饱和;头像/作者名前置
- **Anti_Patterns**: 禁 UI 抢内容焦点 / 禁三列卡片网格
- **Dials**: VARIANCE=3 / MOTION=3 / DENSITY=5

### 2.5 Brand Showcase(品牌展示站)

- **Recommended_Pattern**: `hero-fullscreen + scroll-story + gallery-grid`
- **Style_Priority**: `decorative > minimal > functional`
- **Color_Mood**: 自定义品牌色(避开 [`ai-tells.md`](./ai-tells.md) Lila Rule)
- **Typography_Mood**: `display-serif + neutral-sans`(强对比字重)
- **Key_Effects**: `sticky-stack / horizontal-pan / parallax-bg`
- **Decision_Rules**: 品牌识别 > 转化;滚动叙事;每屏单焦点
- **Anti_Patterns**: 禁通用模板感 / 禁三列卡片 / 禁渐变文字
- **Dials**: VARIANCE=9 / MOTION=8 / DENSITY=2

### 2.6 Finance / Banking App(金融 / 银行 App)

- **Recommended_Pattern**: `account-card + transaction-list + chart-summary`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `trust-deep-blue` 或 `trust-deep-green`
- **Typography_Mood**: `neutral-sans + number-display`(tabular-nums)
- **Key_Effects**: `chart-reveal / balance-mask / biometric-prompt`
- **Decision_Rules**: 信任感 > 美观;数字精确(tabular-nums);危险操作二次确认
- **Anti_Patterns**: 禁高饱和强调 / 禁动画过多 / 禁模糊敏感信息
- **Dials**: VARIANCE=2 / MOTION=2 / DENSITY=7

### 2.7 Health / Wellness App(健康 / 冥想)

- **Recommended_Pattern**: `hero-illustration + progress-ring + daily-card`
- **Style_Priority**: `minimal > decorative > functional`
- **Color_Mood**: `calm-pastel`(柔色,避开 [`ai-tells.md`](./ai-tells.md) Lila Rule)
- **Typography_Mood**: `rounded-sans + script-accent`(可选)
- **Key_Effects**: `breathing-animation / progress-ring / streak-counter`
- **Decision_Rules**: 减压 > 信息密度;圆角大;留白多
- **Anti_Patterns**: 禁密集数据 / 禁高对比 / 禁警告色过多
- **Dials**: VARIANCE=4 / MOTION=5 / DENSITY=2

### 2.8 Education / Course Platform(教育 / 课程平台)

- **Recommended_Pattern**: `sidebar-curriculum + video-main + note-panel`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `focus-warm-neutral`
- **Typography_Mood**: `readable-serif(body) + neutral-sans(UI)`
- **Key_Effects**: `progress-bar / confetti-complete / focus-mode-toggle`
- **Decision_Rules**: 阅读舒适 > 花哨;进度可见;笔记可达
- **Anti_Patterns**: 禁视频周围干扰 / 禁弹窗打断学习
- **Dials**: VARIANCE=3 / MOTION=2 / DENSITY=5

### 2.9 Travel / Booking App(旅游 / 预订)

- **Recommended_Pattern**: `search-hero + destination-grid + booking-flow`
- **Style_Priority**: `decorative > functional > minimal`
- **Color_Mood**: `destination-warm`(目的地氛围色)
- **Typography_Mood**: `display-serif(headlines) + neutral-sans(UI)`
- **Key_Effects**: `image-carousel / date-picker-sticky / price-reveal`
- **Decision_Rules**: 目的地图主导;价格透明;预订流程 ≤ 3 步
- **Anti_Patterns**: 禁图片过小 / 禁隐藏费用 / 禁预订步骤过多
- **Dials**: VARIANCE=6 / MOTION=4 / DENSITY=5

### 2.10 Developer / DevTool(开发者工具)

- **Recommended_Pattern**: `code-main + sidebar-tree + terminal-bottom`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `dark-first`(默认暗色,见 [`accessibility.md`](./accessibility.md) prefers-color-scheme)
- **Typography_Mood**: `mono(code) + neutral-sans(UI)`
- **Key_Effects**: `syntax-highlight / command-palette / diff-view`
- **Decision_Rules**: 键盘优先;命令面板 ⌘K;代码可读 > 美观
- **Anti_Patterns**: 禁花哨动画 / 禁大圆角 / 禁装饰图标
- **Dials**: VARIANCE=2 / MOTION=1 / DENSITY=8

### 2.11 Media / Streaming(媒体 / 流媒体)

- **Recommended_Pattern**: `hero-carousel + row-scroll + detail-modal`
- **Style_Priority**: `decorative > functional > minimal`
- **Color_Mood**: `dark-cinematic`
- **Typography_Mood**: `display-sans(bold) + neutral-sans(UI)`
- **Key_Effects**: `hero-kenburns / row-hover-scale / autoplay-preview`
- **Decision_Rules**: 海报主导;暗色突出色彩;hover preview 短(2-3s)
- **Anti_Patterns**: 禁 UI 抢海报焦点 / 禁亮色背景
- **Dials**: VARIANCE=6 / MOTION=5 / DENSITY=6

### 2.12 Government / Compliance(政府 / 合规)

- **Recommended_Pattern**: `text-main + sidebar-toc + breadcrumb-top`
- **Style_Priority**: `functional > minimal > decorative`
- **Color_Mood**: `neutral-trust`(蓝/灰,低饱和)
- **Typography_Mood**: `readable-serif(body) + neutral-sans(UI)`
- **Key_Effects**: `focus-highlight / toc-scroll-spy`
- **Decision_Rules**: WCAG AAA(7:1);字号 ≥ 16px;链接明显
- **Anti_Patterns**: 禁动画 / 禁小字 / 禁低对比
- **Dials**: VARIANCE=1 / MOTION=1 / DENSITY=4

## 3. 推理流程(在 design-md Brief Inference 阶段)

```
1. 从 brief 提取关键词(产品类型 / 用户群 / 业务目标)
2. 匹配本文 12 个示例,命中则直接采用其推理结果
3. 未命中:查询 color-palettes.md 的 192 套桶,按业务类型选 3 个候选
4. 让用户在 3 个候选中确认 / 修改
5. 输出 7 维推理结果,写入 DESIGN.md frontmatter 的 `product:` 块
```

DESIGN.md 中的写法:

```yaml
---
product:
  type: saas-dashboard
  recommended_pattern: [sidebar-nav, data-table, filter-bar]
  style_priority: [functional, minimal, decorative]
  color_mood: cool-neutral
  typography_mood: { display: null, ui: neutral-sans }
  key_effects: [subtle-shadow, hover-bg-highlight, loading-skeleton]
  decision_rules: 信息密度 > 美观;表格优先于卡片
  anti_patterns: [no-parallax, no-decorative-motion, no-3-col-cards]
  dials: { variance: 2, motion: 2, density: 8 }
---
```

## 4. 与其他文档的关系

- 推理出的 `color_mood` 在 [`color-palettes.md`](../dimensions/color-palettes.md) 查具体色值
- `recommended_pattern` 命名见 [`vocabulary/`](../vocabulary/)
- `key_effects` 实现见 [`framework/motion-skeletons/`](../framework/motion-skeletons/)
- `dials` 解释见 [`dials.md`](./dials.md)
- `anti_patterns` 与 [`ai-tells.md`](./ai-tells.md) 联动,本文的 anti_patterns 是产品特定,AI Tells 是通用
