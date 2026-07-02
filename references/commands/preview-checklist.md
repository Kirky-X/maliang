# Pre-Flight Check 清单 —— preview 子命令机械检查

> 本文件是 [`preview.md`](./preview.md) 第 5 节的**完整检查项清单**,从 preview.md 拆出以控制主文件行数。
> 交付前**机械扫描**(可脚本化,非主观判断)。任一项失败即"硬性失败",不可交付,必须返工。来源:taste-skill + ui-ux-pro-max-skill。

## 5.1 · AI Tells(15 项,见 [`ai-tells.md`](../meta/ai-tells.md))
- [ ] 无 Tailwind 渐变文字 + 中性灰背景组合
- [ ] 非全场 `rounded-2xl`(至少 2 档圆角差异化)
- [ ] 无紫蓝粉渐变大面积背景
- [ ] 非 Inter / Geist 单字族(标题与正文有字体差异)
- [ ] 标题字距非统一 `tracking-tight`
- [ ] 短标题未滥用 `text-balance`
- [ ] 无三列等高卡片网格(feature 区)
- [ ] 容器宽度非全 `max-w-7xl`(差异化)
- [ ] 间距非全 `py-20`(节奏有变化)
- [ ] 无 lorem ipsum 残留
- [ ] 数字非 100/1k/10k 整数凑数
- [ ] 非三档定价 + 中间"Most Popular"(若 Pricing 区存在)
- [ ] 非默认 Lucide `Rocket/Zap/Shield` 三件套
- [ ] 无 `source.unsplash.com/random` 占位
- [ ] 字体非走 Google Fonts CDN 阻塞首屏

## 5.2 · Performance(10 项,见 [`performance.md`](../meta/performance.md))
- [ ] 所有图片含 `width` + `height` 或 `aspect-ratio`
- [ ] 字体含 `font-display: swap`
- [ ] 动画化属性仅限 `transform` / `opacity`
- [ ] grain/noise 用 `::before` 伪元素 + `position: fixed` + `pointer-events: none`
- [ ] `z-index` 全部 token 化(无魔法值)
- [ ] 首屏 JS ≤ 100KB gzip
- [ ] 长列表(> 100 项)用虚拟滚动
- [ ] `box-shadow` 大模糊(≥ 40px)慎用
- [ ] `backdrop-filter` 元素 ≤ 3 个
- [ ] `will-change` 非常驻(动画完成后移除)

## 5.3 · Accessibility · WCAG 对比度(8 项,见 [`accessibility.md`](../meta/accessibility.md))
- [ ] 所有正文文字对比度 ≥ 4.5:1
- [ ] 所有大文本对比度 ≥ 3:1
- [ ] UI 组件(border / 图标)对比度 ≥ 3:1
- [ ] `placeholder` 文字对比度 ≥ 4.5:1
- [ ] 暗色模式下对比度仍达标
- [ ] 非用纯红/纯绿表达信息(色盲友好)
- [ ] `disabled` 文字对比度 ≥ 3:1
- [ ] `focused` focus ring 对比度 ≥ 3:1

## 5.4 · Accessibility · 用户偏好(6 项)
- [ ] 装饰性动画含 `prefers-reduced-motion` 降级
- [ ] 视差 / pin / 横向平移在 reduced-motion 下完全禁用
- [ ] 暗色模式 token 通过 `prefers-color-scheme` 切换
- [ ] `backdrop-filter` 含 `prefers-reduced-transparency` 降级
- [ ] 半透明遮罩含 reduced-transparency 降级
- [ ] 双跑预览:默认 + reduced-motion,无信息丢失

## 5.5 · Accessibility · 交互可达(8 项)
- [ ] 所有交互元素 Tab 可达
- [ ] focus ring 可见(无 `outline: none` 无替代)
- [ ] 触摸目标 ≥ 44pt × 44pt
- [ ] 图片含 `alt`(装饰性 `alt=""`)
- [ ] 按钮无文字时含 `aria-label`
- [ ] 表单含 `<label>` 或 `aria-label`
- [ ] 页首含 "Skip to main content" 跳转链接
- [ ] DOM 顺序 = 视觉顺序(无正整数 `tabindex`)

## 5.6 · Token 完整性(10 项,见 [`token.md`](../meta/token.md))
- [ ] CSS 变量全部从 `:root` 读取,无 `{token-name}` 残留
- [ ] 无硬编码颜色(`#RRGGBB` 字面量在样式内联中)
- [ ] 无硬编码字号(`14px` / `16px` 等具体值,文档说明除外)
- [ ] 无硬编码间距
- [ ] z-index 全 token 化
- [ ] 暗色 token 在 `@media (prefers-color-scheme: dark)` 中覆盖
- [ ] Primitive → Semantic → Component 三层引用单向
- [ ] 组件引用 `{path.to.token}` 而非重复字面值
- [ ] Typography 复合对象字段完整(fontFamily/size/weight/lineHeight)
- [ ] 命名全部 kebab-case,无 camelCase / snake_case 混用

## 5.7 · 完整交互状态(8 项,见 [`principles.md`](../meta/principles.md) 第 14 定律)
- [ ] 所有按钮含 default / hover / pressed / focused / disabled 五态
- [ ] 所有可点击卡片含 hover / pressed 反馈
- [ ] Loading 状态有骨架 / spinner(> 200ms 操作)
- [ ] Empty 状态有插画 + 文案 + CTA
- [ ] Error 状态有错误说明 + 重试 CTA
- [ ] Tactile Feedback(`micro-press-scale` 或 `micro-hover-lift`)
- [ ] 状态过渡 duration ≤ 150ms(状态过渡)
- [ ] 表单提交后有 toast 反馈(成功 / 失败)

## 5.8 · LLM 截断信号(8 项,见 [`llm-behavior.md`](../meta/llm-behavior.md))
- [ ] 最后一个章节字数 ≥ 前面章节均值的 50%
- [ ] 代码块无 `// ...` / `// 其余类似` / `// TODO` 结尾
- [ ] 组件区有 ≥ 1 个组件的完整四态(不只 default)
- [ ] Do's and Don'ts ≥ 6 条(若 DESIGN.md 引用)
- [ ] 章节内容是真正的 X,非"该章节应包含 X"
- [ ] placeholder 占比 < 10%
- [ ] 文案具体(无"现代设计"等空泛词)
- [ ] 数字真实风(有尾数,非整数凑数)

## 5.9 · 第 13 定律 · 动画动机(7 项,见 [`principles.md`](../meta/principles.md))
- [ ] 每段动画可回答"为什么动"(状态变化 / 空间引导 / 反馈)
- [ ] 无装饰性循环动画(MOTION_INTENSITY ≤ 5 时)
- [ ] 入场动画 duration ≤ 600ms
- [ ] stagger 间隔 ≤ 120ms
- [ ] translateY 偏移 ≤ 30px(防眩晕)
- [ ] 缓动函数非默认 `linear`(用 ease-out / cubic-bezier)
- [ ] `ScrollTrigger.once: true` 或等价(避免反复触发)

## 5.10 · 排版细节(6 项,见 [`hero.md`](../vocabulary/hero.md) + [`layout.md`](../vocabulary/layout.md))
- [ ] **em-dash 中文场景放宽**:中文正文用 `——`(全角破折号),英文用 `—`(em-dash);**禁止**中文场景用 `--` 或 `-` 凑数;列表项符号用 `-` 不受此限
- [ ] **eyebrow 计数 ≤ 1**:每页 eyebrow(标题上方小标签)≤ 1 个,Hero 用了则后续 section 禁用(见 [`hero.md`](../vocabulary/hero.md) H2)
- [ ] Hero 标题字数 ≤ 12 中文 / ≤ 7 英文词
- [ ] Hero 副标题字数 ≤ 30 中文 / ≤ 18 英文词
- [ ] 中英文混排含空格(中英之间 1 空格,如"使用 React 框架")
- [ ] 标点符号中英文一致(中文用全角,英文用半角,不混用)

## 5.11 · 视觉一致性锁(5 项)
- [ ] **主题锁**:单页 ≤ 1 个主题色(品牌主色),其余为中性色 + 语义色;多主题色 = 视觉混乱
- [ ] **色彩锁**:palette 不漂移——所有颜色必须可追溯到 DESIGN.md `colors:` 块的 token,无游离色值
- [ ] **形状锁**:圆角风格一致——同类组件圆角档位一致(如所有卡片 `rounded.lg`、所有按钮 `rounded.md`),不混用 sharp/round
- [ ] 阴影档位 ≤ 3 档(sm/md/lg),不出现 5+ 种阴影深度
- [ ] 字号档位 ≤ 7 档(typography scale),不出现 9+ 种字号

## 5.12 · Hero 适配(6 项,见 [`hero.md`](../vocabulary/hero.md))
- [ ] **移动端 Hero**:标题在 393px 宽度下不换行超 3 行;CTA 在移动端单列堆叠(非左右并排)
- [ ] **桌面端 Hero**:标题在 1440px 宽度下不超出容器;CTA 间距 ≥ 16px
- [ ] `hero-fullscreen` 用 `min-height: 100svh`(非 `100vh`,移动端地址栏抖动)
- [ ] Hero 背景图移动端有 `<picture>` + `srcset` 断点(非仅 desktop 图缩放)
- [ ] Hero 视频含 `poster` fallback + `autoplay muted loop playsinline`
- [ ] Hero CTA ≤ 2 个(见 [`hero.md`](../vocabulary/hero.md) H3)

## 5.13 · Core Web Vitals(5 项)
- [ ] **LCP ≤ 2.5s**:最大内容绘制(Hero 图/标题)在 2.5s 内完成;超 4s = 差
- [ ] **CLS ≤ 0.1**:累计布局偏移;所有图片/字体含尺寸预留(`<img width height>` / `aspect-ratio` / `font-display: swap`)
- [ ] **INP ≤ 200ms**:交互到下一帧延迟;长任务(> 50ms)拆分,重计算用 `requestIdleCallback`
- [ ] **FCP ≤ 1.8s**:首次内容绘制;首屏 JS ≤ 100KB gzip,字体不阻塞
- [ ] **TBT ≤ 200ms**:总阻塞时间;主线程长任务(> 50ms)总和 ≤ 200ms

## 统计与执行规则

**统计**:5.1 (15) + 5.2 (10) + 5.3 (8) + 5.4 (6) + 5.5 (8) + 5.6 (10) + 5.7 (8) + 5.8 (8) + 5.9 (7) + 5.10 (6) + 5.11 (5) + 5.12 (6) + 5.13 (5) = **102 项**

### 执行规则
- 全部 102 项均为**机械检查**(可脚本化,非主观判断),任一项失败 = 硬性失败(不可降级为 warning),失败项必须列出具体位置(HTML 行号 / CSS 选择器)
- 修复后重跑全部 102 项(不可只跑失败项),通过后进入 preview.md 第 6 节 Pre-Delivery Checklist(主观维度)
- em-dash / 中英文空格 / 标点一致性为**软警告**(warning,非硬性失败),其余 99 项为硬性失败
