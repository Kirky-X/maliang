# Pre-Flight Check 清单 —— preview 子命令机械检查

> 本文件是 [`preview.md`](./preview.md) 第 5 节的**完整检查项清单**,从 preview.md 拆出以控制主文件行数。
> 交付前**机械扫描**(可脚本化,非主观判断)。任一项失败即"硬性失败",不可交付,必须返工。来源:taste-skill + ui-ux-pro-max-skill。
>
> **Canonical 声明**:本清单是全流水线(design-md / draw-md / preview / redesign)唯一的交付前检查清单;其他文档只引用本文件,不复制条目。
>
> **本清单不豁免编号门禁**:本清单是「全量机械检查」(该项过没过),[`../meta/numbered-gates.md`](../meta/numbered-gates.md) 是「否决门」(这种形态不许交)。两处都过才算过(规则 canonical 见 [`../meta/numbered-gates.md`](../meta/numbered-gates.md) §0)。门禁在本清单全过之后、第 6 节 Pre-Delivery Checklist 之前逐条过,执行纪律见 [`preview.md`](./preview.md) 第 5 节「编号门禁」。
>
> **脚本覆盖**:49/135 项由 [`scripts/preview-check.py`](../../scripts/preview-check.py) 自动执行;
> 其余 86 项为**运行时项**(需浏览器实测/视觉比对/业务交互验证);部分条目标记 **[运行时]**,
> 未标记项按分区语义与 5.13 的 MANUAL/脚本能力归属判断。
> 静态扫描通过是底线而非达标证明 —— 运行时项必须在 preview 第 4 节浏览器验证中逐项确认,
> 且每项结论按 preview.md「证据四分类」标注证据来源,禁止从单一分数声称合规。

## 5.0 · Process 区(动态实测,7 项,先于全部分区执行)

> 来源:ui-ux-pro-max pro-rules canonical 清单。以下是**过程性动作**——必须在真实渲染环境动手实测,静态扫描无法替代;先做本区,再进入 5.1-5.16 静态 / 运行时复选。
> 2026-09 吸收(来源:frontend-design-practicalswan):补入两个压力实测项——设计只对理想数据成立=未完成,压力数据是实测动作,判定细则见 5.16 与 [`../meta/hardening.md`](../meta/hardening.md)。

- [ ] **375px 窄屏实测**:布局在 375px 宽度下无横向溢出、无挤压变形 <sub>[运行时]</sub>
- [ ] **横屏旋转实测**:旋转后布局自适应,无错位 / 内容丢失 <sub>[运行时]</sub>
- [ ] **`prefers-reduced-motion` 下实测**:动画降级生效,信息无丢失 <sub>[运行时]</sub>
- [ ] **最大系统字号(200%)实测**:文字放大后不截断 / 不重叠,布局不破 <sub>[运行时]</sub>
- [ ] **暗色模式独立测对比**:切到暗色后逐区域核对对比度(非简单反色) <sub>[运行时]</sub>
- [ ] **长内容/本地化膨胀实测**:用最长真实内容与译语膨胀文本(德/俄等常见 +30-40%)填充后,布局不破、关键操作不截断 <sub>[运行时]</sub>
- [ ] **慢/失败依赖实测**:接口超时、失败、离线时页面有分状态处置与恢复路径,无无限 spinner <sub>[运行时]</sub>

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

> 脚本化:`preview-check.py` 静态解析 `<style>` 内 color × background 组合(正文/大文本/placeholder/disabled/暗色 media 内规则);渐变、透明、CDN 框架默认色无法静态解析,不猜测。
> 对比度计算规则:正文 ≥ 4.5:1;大文本(≥ 24px,或 ≥ 18.66px 且 weight ≥ 700)≥ 3:1;disabled ≥ 3:1。

- [ ] 所有正文文字对比度 ≥ 4.5:1 <sub>[脚本 contrast.low]</sub>
- [ ] 所有大文本对比度 ≥ 3:1 <sub>[脚本 contrast.low]</sub>
- [ ] UI 组件(border / 图标)对比度 ≥ 3:1 <sub>[运行时:渲染后测量]</sub>
- [ ] `placeholder` 文字对比度 ≥ 4.5:1 <sub>[脚本 contrast.low]</sub>
- [ ] 暗色模式下对比度仍达标 <sub>[脚本:仅覆盖 @media 内重声明规则;继承组合需运行时确认]</sub>
- [ ] 非用纯红/纯绿表达信息(色盲友好) <sub>[脚本 contrast.pure-red-green]</sub>
- [ ] `disabled` 文字对比度 ≥ 3:1 <sub>[脚本 contrast.low]</sub>
- [ ] `focused` focus ring 对比度 ≥ 3:1 <sub>[运行时:渲染后测量]</sub>

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

## 5.7 · 完整交互状态(11 项,见 [`principles.md`](../meta/principles.md) 第 14 定律)

> 脚本化:静态代理 — 页面存在交互元素而 `<style>` 缺对应状态选择器时报告;
> 框架 CDN(Element Plus 等)自带状态样式时降级为 warning。`outline: none` 且无
> `:focus` 替代为确定性 error。业务状态需运行时验证。

- [ ] 所有按钮含 default / hover / pressed / focused / disabled 五态 <sub>[脚本 state.no-*(静态代理,warning)]</sub>
- [ ] 所有可点击卡片含 hover / pressed 反馈 <sub>[脚本 state.no-hover/active]</sub>
- [ ] Loading 状态有骨架 / spinner(> 200ms 操作) <sub>[运行时]</sub>
- [ ] Empty 状态有插画 + 文案 + CTA <sub>[运行时]</sub>
- [ ] Error 状态有错误说明 + 重试 CTA <sub>[运行时]</sub>
- [ ] Tactile Feedback(`micro-press-scale` 或 `micro-hover-lift`) <sub>[脚本 state.no-tactile(:active 内 transform)]</sub>
- [ ] 状态过渡 duration ≤ 150ms(状态过渡) <sub>[脚本 anim.duration(400ms 上限,150ms 需运行时确认)]</sub>
- [ ] 表单提交后有 toast 反馈(成功 / 失败) <sub>[运行时]</sub>
- [ ] 同一意图的 CTA 全页只一个标签(如联系意图不得"联系我们 / Get in Touch"混用,意图归类判据见 [`../meta/content-guide.md`](../meta/content-guide.md) §2) <sub>[运行时]</sub>
- [ ] 主 CTA 按钮文案单行显示:移动端实测按钮高度 ≤ 1.5×行高,折行 = 硬失败(先缩短文案或放宽容器 max-width,而非接受两行) <sub>[运行时:机械查按钮高度/行高]</sub>
- [ ] 动作全流程动词一致:按钮、toast、错误提示对同一动作用同一动词词根(如按钮"发布" → toast"已发布" → 错误"发布失败",见 content-guide §2) <sub>[运行时]</sub>

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
- [ ] 入场动画 duration ≤ 400ms(装饰/骨架类长动效按 [`micro-interactions.md`](../vocabulary/micro-interactions.md) 分层第 3 层 ≤ 600ms 且必须可跳过,>400ms 须以 `{duration-*}` token 引用——字面量被脚本按 ≤400ms 硬查)
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

## 5.11 · 视觉一致性锁(8 项)
- [ ] **主题锁**:单页 ≤ 1 个主题色(品牌主色),其余为中性色 + 语义色;多主题色 = 视觉混乱
- [ ] **色彩锁**:palette 不漂移——所有颜色必须可追溯到 DESIGN.md `colors:` 块的 token,无游离色值
- [ ] **形状锁**:圆角风格一致——同类组件圆角档位一致(如所有卡片 `rounded.lg`、所有按钮 `rounded.md`),不混用 sharp/round
- [ ] 阴影档位 ≤ 3 档(sm/md/lg),不出现 5+ 种阴影深度
- [ ] 字号档位 ≤ 7 档(typography scale),不出现 9+ 种字号
- [ ] **原生面锁**:浏览器原生面已主题化——文本选区 `::selection` 与输入光标 `caret-color` 从主题 token 派生,非浏览器默认(Web 项;Harmony/Flutter n/a) <sub>[运行时;可静态抽检样式存在性]</sub>
- [ ] 滚动条与焦点环颜色在暗色 / 品牌界面已主题派生(无默认白滚动条、默认蓝焦点环;Web 项) <sub>[运行时;可静态抽检样式存在性]</sub>
- [ ] 链接下划线偏移 `text-underline-offset` 调至光学正确,数据列/比较数字用 `tabular-nums`(Web 项,判据见 [`../meta/ux-rules.md`](../meta/ux-rules.md) §11;Harmony/Flutter n/a) <sub>[运行时;可静态抽检样式存在性]</sub>

## 5.12 · Hero 适配(6 项,见 [`hero.md`](../vocabulary/hero.md))
- [ ] **移动端 Hero**:标题在 393px 宽度下不换行超 3 行;CTA 在移动端单列堆叠(非左右并排)
- [ ] **桌面端 Hero**:标题在 1440px 宽度下不超出容器;CTA 间距 ≥ 16px
- [ ] `hero-fullscreen` 用 `min-height: 100svh`(非 `100vh`,移动端地址栏抖动)
- [ ] Hero 背景图移动端有 `<picture>` + `srcset` 断点(非仅 desktop 图缩放)
- [ ] Hero 视频含 `poster` fallback + `autoplay muted loop playsinline`
- [ ] Hero CTA ≤ 2 个(见 [`hero.md`](../vocabulary/hero.md) H3)

## 5.13 · Core Web Vitals(5 项)

> **全部 [运行时]** — LCP/CLS/INP/FCP/TBT 是运行时指标,静态无法测量,需浏览器
> 实测(Chrome DevTools Performance 面板 / Lighthouse / web-vitals 库)。5.2 的
> img 尺寸、font-display 是其静态前置条件。

- [ ] **LCP ≤ 2.5s**:最大内容绘制(Hero 图/标题)在 2.5s 内完成;超 4s = 差 <sub>[运行时]</sub>
- [ ] **CLS ≤ 0.1**:累计布局偏移;所有图片/字体含尺寸预留(`<img width height>` / `aspect-ratio` / `font-display: swap`) <sub>[运行时;前置项已由 5.2 脚本覆盖]</sub>
- [ ] **INP ≤ 200ms**:交互到下一帧延迟;长任务(> 50ms)拆分,重计算用 `requestIdleCallback` <sub>[运行时]</sub>
- [ ] **FCP ≤ 1.8s**:首次内容绘制;首屏 JS ≤ 100KB gzip,字体不阻塞 <sub>[运行时]</sub>
- [ ] **TBT ≤ 200ms**:总阻塞时间;主线程长任务(> 50ms)总和 ≤ 200ms <sub>[运行时]</sub>

## 5.14 · 交付完备性(6 项,见 [`default-pages/index.md`](../default-pages/index.md))

> 来源:taste-skill redesign-skill"AI 通常忘记的东西"清单。多为运行时 / 站点级检查,产物对应 `default-pages` 中的 privacy/terms/not-found 等页面。

- [ ] 法务链接齐备(隐私政策 / 服务条款,页脚可达) <sub>[运行时]</sub>
- [ ] 返回导航:每个非首页有明确"返回上一级 / 首页"路径 <sub>[运行时]</sub>
- [ ] 自定义 404 页存在且有出口(搜索 / 回首页) <sub>[运行时]</sub>
- [ ] 表单有客户端校验(必填 / 格式错误内联提示,非仅提交后报错) <sub>[运行时]</sub>
- [ ] skip-to-content 链接存在且为键盘 Tab 首个可达项 <sub>[脚本:静态可查存在性;位置需运行时]</sub>
- [ ] favicon 存在(含移动端 bookmark 图标) <sub>[运行时;可静态抽检 head 引用]</sub>

## 5.15 · 真机验证(8 项,全部需真机)

> 来源:mobile-native(emilkowalski/skills,MIT)+ frontend-design-practicalswan,2026-09 吸收。
> 以下各项**模拟环境不可信**——桌面 DevTools 设备模拟无法复现真机行为,必须在实体设备实测(模拟器仅用于布局快速校验,见 preview.md 约束汇总)。故障机理与修复见 [`../meta/mobile-floor.md`](../meta/mobile-floor.md)。
>
> **真机调试路径**(本区各项的执行前提):
> - 通用:开发服务监听 `0.0.0.0`,手机与电脑同 LAN,手机浏览器访问 `http://<电脑 LAN IP>:<端口>`,或 USB 连接后端口转发;
> - iOS:Mac Safari「开发」(Develop)菜单选到目标设备页面检查;
> - Android:手机 Chrome 访问 `chrome://inspect` 经 USB 调试连 DevTools;
> - 没有测试机时,淘汰旧手机是最便宜的测试矩阵(低端 Android 尤其暴露性能与键盘问题)。

- [ ] **粘滞 hover 实测**:触屏 tap 后 hover 样式不残留(信息与状态切换不依赖 `:hover` 独占) <sub>[运行时]</sub>
- [ ] **tap 高亮实测**:`-webkit-tap-highlight-color` 有意设置,按压有 `:active` 联动反馈 <sub>[运行时]</sub>
- [ ] **URL 栏对视口单位实测**:地址栏收展时 100vh 元素不截断 / 不抖动(`svh`/`dvh` 实机行为核对) <sub>[运行时]</sub>
- [ ] **聚焦缩放实测**:聚焦任一输入框页面不强制缩放(输入字号 ≥ 16px) <sub>[运行时]</sub>
- [ ] **overscroll 实测**:根层无意外下拉刷新劫持,内层滚动容器回弹不连带整页(双层判据见 [`../meta/web-interface-guidelines.md`](../meta/web-interface-guidelines.md)) <sub>[运行时]</sub>
- [ ] **safe-area 实测**:刘海 / 手势条设备上导航与主要操作不被遮挡 <sub>[运行时]</sub>
- [ ] **软键盘实测**:键盘弹起不遮挡焦点输入框,布局行为符合预期 <sub>[运行时]</sub>
- [ ] **PWA standalone 实测**:添加到主屏后 standalone 模式下布局与导航完整 <sub>[运行时]</sub>

## 5.16 · 生产化加固(6 项,见 [`../meta/hardening.md`](../meta/hardening.md))

> 来源:impeccable harden 思想(pbakaus/impeccable,Apache-2.0),2026-09 吸收,中文自研。
> 核心判据:**设计只对完美数据成立 = 未完成**。5.0 的两项压力实测是本区的执行动作;判定细则、三框架 i18n 判据与 verify 清单见 hardening.md。
> 可脚本化子集(固定宽度文本容器、非逻辑属性)由 validate-draw-md.py 演进承接,本清单不重复其条目。

- [ ] **极端输入谱系**:单字符、超长无空格 token、emoji(含多码位序列)、RTL 文本、千级列表逐类实测,渲染不破不截断 <sub>[运行时]</sub>
- [ ] **错误场景分状态**:4xx / 5xx / 超时 / 离线各有具体文案与恢复动作(非笼统一句"出错了") <sub>[运行时]</sub>
- [ ] **并发双击防重**:提交请求进行中按钮进入 loading / 禁用,双击不产生双提交 <sub>[运行时]</sub>
- [ ] **i18n 三判据**:译语 30-40% 空间余量实测;布局方向用逻辑属性 / start-end 语义(非物理 left-right);日期、货币、复数走格式化接口(三框架判据见 hardening.md §3) <sub>[运行时]</sub>
- [ ] **被中断手势恢复**:`pointercancel`(来电 / 系统手势接管)后无残留状态,下次拖拽无需刷新即可正常工作 <sub>[运行时]</sub>
- [ ] **加固 verify 清单**:交付前逐项过 hardening.md 尾附 verify 清单,结果按证据四分类写入产物报告 <sub>[运行时]</sub>

## 统计与执行规则

**统计**:5.0 (7) + 5.1 (15) + 5.2 (10) + 5.3 (8) + 5.4 (6) + 5.5 (8) + 5.6 (10) + 5.7 (11) + 5.8 (8) + 5.9 (7) + 5.10 (6) + 5.11 (8) + 5.12 (6) + 5.13 (5) + 5.14 (6) + 5.15 (8) + 5.16 (6) = **135 项**

### 执行规则
- 全部 135 项均为**机械检查**(可脚本化或运行时实测,非主观判断),任一项失败 = 硬性失败(不可降级为 warning),失败项必须列出具体位置(HTML 行号 / CSS 选择器)
- 5.0 Process 区先于 5.1-5.16 执行(动态实测是过程性动作,不因静态扫描通过而豁免)
- 5.15 真机验证在浏览器验证之后、交付声明之前执行(模拟环境通过的项不因此豁免真机复测)
- 修复后重跑全部 135 项(不可只跑失败项),通过后先过编号门禁 [`../meta/numbered-gates.md`](../meta/numbered-gates.md) G01–G28,再进入 preview.md 第 6 节 Pre-Delivery Checklist(主观维度)
- em-dash / 中英文空格 / 标点一致性为**软警告**(warning,非硬性失败),其余 132 项为硬性失败
