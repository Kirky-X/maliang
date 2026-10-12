# Hero 模式命名词汇

> 模式词汇库。为 draw-md 阶段的 Hero 区域提供标准化命名,避免 LLM 用泛化词(如 "顶部大图")描述,产出可直接对应代码的模式名。来源:taste-skill;首屏骨架表来源:oil-ui 仓,2026-10 吸收。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `hero-centered`       | 居中文案 + CTA,无图或背景图淡出                  | 营销首页、SaaS 主页、产品发布         |
| `hero-split`          | 左文案 + 右视觉(图 / 视频 / 产品截图)          | 产品页、功能介绍、电商首页            |
| `hero-fullscreen`     | 全屏图 / 视频 + 浮层文字                          | 品牌站、作品集、影视媒体              |
| `hero-kenburns`       | 全屏图 + Ken Burns 缓慢缩放                       | 品牌、影视、摄影集                    |
| `hero-parallax`       | 多层视差,滚动时背景 / 中景 / 前景速率不同        | 品牌叙事、产品发布                    |
| `hero-canvas`         | WebGL / Canvas 动态背景(粒子 / 流体)            | 科技品牌、3D 交互、创意工具           |
| `hero-illustration`   | 插画为主,文字辅助                                | 健康 / 教育 / 冥想类 App              |
| `hero-card-stack`     | 卡片堆叠 + 滚动揭示(配合 sticky-stack 骨架)     | 产品功能介绍、案例展示                |
| `hero-video-loop`     | 短视频循环 + 文字浮层                             | 消费品、产品演示、IP 落地页           |
| `hero-text-only`      | 纯文字 + 排版,无图                               | 设计师作品集、极简品牌、文档站        |
| `hero-inline-image-type` | 巨型标题词间嵌入小尺寸语境照片(行高对齐、圆角、作视觉标点) | VARIANCE ≥ 7 的品牌 / 作品集站;移动端退化为标题下方堆叠(依赖 [`visual-assets.md`](../meta/visual-assets.md) 图片策略,来源:taste-skill stitch-skill §4) |

## 首屏骨架表(8 种,先于文案)

> **骨架与模式名分工**:本节 8 种管**首屏怎么排**(构图与阅读顺序,说服型 / 营销页用),写文案之前先定;上方命名表 11 种管**这个首屏长成什么**(模式命名与硬约束),draw-md 章节标注用。两者不冲突——先选骨架,再回命名表选承载它的模式。来源:oil-ui 仓,2026-10 吸收。

模型最顽固的习惯是**左右分栏**,它在写文案之前就定下来了:先想好标题、一段说明、一个按钮,摆好就是左右两栏。所以骨架要在写任何文案之前决定;调性决定音量,骨架决定结构——**不要因为调性偏安静就退回左右分栏**。

| 骨架 | 首屏长什么样 |
| --- | --- |
| 满版图像压字 | 一张图占满首屏,标题和动作压在图的安全区里 |
| 居中单一物件 | 一个物件或一句话居中,四周是大面积空白 |
| 画面即界面 | 首屏就是产品界面或一件实物本身,标题、导航和按钮都长在它上面 |
| 满版文字 | 文字本身就是画面,字大到占满首屏、跨过边缘或被裁切 |
| 通栏上下堆叠 | 通栏大标题横跨整个宽度,下面紧接内容 |
| 网格拼贴 | 多块内容同时出现,按网格或拼贴排列,没有单一主角 |
| 纵排或斜向 | 文字竖排、斜切或旋转,打破从左到右的阅读 |
| 左右分栏 | 文字一侧,画面一侧。**这是模型的默认,一轮最多一个方向使用,并写出为什么非它不可**;另一侧必须是跨越结构的图像、色块或图形装置,不能是装在卡片里的产品界面 |

规则:

- **同一轮的方向,骨架互不相同**;「大标题九栏、说明三栏」同样算左右分栏(比例版式不改变骨架类别)。
- **左右分栏配额**:一轮(一次 explore 发散)最多一个方向用左右分栏,且该方向必须在方向卡写明「为什么非它不可」——写不出就换骨架。
- **骨架定好之后再写文案**,文案去适应骨架,不让骨架去适应「标题 + 说明 + 按钮」的组合。
- **非说服型页面(画廊 / 商店 / 信息流 / 文档 / 工具 / 后台)不用本表**:首屏就是第一排内容本身或工作区,导航、标题与筛选合计 ≤ 2 行,第一排内容完整出现在首屏(见 [`../commands/explore.md`](../commands/explore.md) 步骤 2.3)。
- **小屏降级**:窄屏 / 移动端收敛为单列,骨架语义保留(如「通栏上下堆叠」保持通栏顺序,不退回左右分栏);方框线框按 3–5 块画,每块写「是什么 / 占多大 / 阅读从哪开始」。

## 使用规则

- draw-md 输出时,Hero 章节必须标注一个模式名,不接受"顶部"等泛化描述
- 模式名与 [`motion-skeletons/`](../motion-skeletons/) 联动:`hero-parallax` 必须配 sticky-stack 或 scroll-reveal-stagger
- 同一站点跨页 Hero 模式 ≤ 2 种(避免混乱)
- 触发 [`ai-tells.md`](../meta/ai-tells.md) 第 1 节"紫蓝粉渐变背景"的,改用 `hero-text-only` 或 `hero-split`
- **内容选择原则**:Hero 打开该主题世界**最具特征之物**,形式任选(headline、图片、动画、live demo、交互时刻皆可)——先定"放什么",再回命名表选承载它的模式;来源:frontend-design-anthropic,2026-09 吸收
- "大数字 + 小标签 + 支撑数据 + 渐变 accent"是默认套路,仅当它确实是该主题的最佳呈现时才用;命中品类惯性默认的,按 [`design-md.md`](../commands/design-md.md) Defaults 品类默认机制逐条声明拒绝
- `hero-canvas` 落地前必须先过 [`performance.md`](../meta/performance.md) Canvas/WebGL 预算节(目的性门槛/降级/资源生命周期);装饰性粒子背景直接拒绝

## 在 draw-md 中的写法

```markdown
## Hero
- pattern: hero-split
- left: { headline, subhead, cta-primary, cta-secondary }
- right: { image: product-screenshot.png, ratio: 4:3 }
- motion: scroll-reveal-stagger (Level 5)
```

## 生产级硬规则

> 交付前机械检查,任一违反 = 硬性失败,不可降级为 warning。补充 [`ai-tells.md`](../meta/ai-tells.md) 与 [`principles.md`](../meta/principles.md) 未覆盖的 Hero 专属约束。

### H1 · Hero 栈 ≤ 4

- Hero 区域纵向元素栈 ≤ 4 层(典型:eyebrow → headline → subhead → CTA)
- 超过 4 层视为信息过载,必须拆分到下方 section
- 允许的 4 层组合:eyebrow + headline + subhead + CTA / headline + subhead + CTA + 次要链接 / logo + headline + CTA + 信任标识

### H2 · Eyebrow 节制(每页 ≤ 1)

- Eyebrow(标题上方的小标签文字,如 "NEW" / "FEATURE")每页 ≤ 1 个
- Hero 内用了 eyebrow,后续 section 标题**禁止**再用 eyebrow(改用纯标题或 section number)
- 违反 = 多 eyebrow 稀释焦点,触发 [`ai-tells.md`](../meta/ai-tells.md) "通用感"

### H3 · Hero CTA ≤ 2

- Hero 内主 CTA + 次 CTA 合计 ≤ 2 个
- 单 CTA:聚焦转化(登录页 / 注册页)
- 双 CTA:主 + 次(如"免费试用" + "查看演示"),次 CTA 必须视觉降级(ghost / text 风)
- **禁止** Hero 内出现 3+ CTA(决策瘫痪,见 [`principles.md`](../meta/principles.md) 希克定律应用)

### H4 · 其他 Hero 硬约束

- Hero 标题字数 ≤ 12 个中文 / ≤ 7 个英文词(超长拆副标题)
- Hero 副标题字数 ≤ 30 个中文 / ≤ 18 个英文词
- Hero 背景图必须含 `aspect-ratio` + `width/height`(见 [`performance.md`](../meta/performance.md) CLS)
- `hero-fullscreen` 必须实现 `min-height: 100svh`(非 `100vh`,移动端地址栏收起抖动)
- Hero 视频必须 `autoplay muted loop playsinline` + `poster` fallback
