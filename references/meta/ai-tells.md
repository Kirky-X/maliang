# AI Tells 黑名单 —— LLM 生成 UI 的常见设计签名

> 规范层。LLM 在生成 UI 时会反复出现一组可识别的"AI 味"签名,这些签名既不专业也易被一眼识破。本文档为硬性禁止清单,生成任何 UI markdown / 框架代码 / 预览 HTML 时,必须自我对照并避开。来源:taste-skill。

每条 Tell 分为「症状」「为什么是 Tell」「替代做法」三段。9 个子分类按出现频率排序。

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

## 自检流程

生成任何 UI 产物后,在 preview 阶段(见 [`../commands/preview.md`](../commands/preview.md) 的 Pre-Flight Check)对照本清单逐项检查,触发任一 Tell 即返工。9 子分类无优先级,均为硬性禁止;冲突时按 [`rules-priority.md`](./rules-priority.md) 的 Style(HIGH)档处理。
