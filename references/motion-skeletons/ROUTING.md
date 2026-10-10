# 动效选型路由（Effect × Route）

> 目的：回答"这个动效**值不值得做、用多重的路线做**"——maliang 的 motion-skeletons 回答"怎么实现"，本文件回答"选哪条路线、哪些形态已沦为 AI 味"。同屏动效预算与动机判定见 [`../vocabulary/micro-interactions.md`](../vocabulary/micro-interactions.md)。
>
> 来源：Adapted from finesse-ui（github.com/mouse-lin/finesse-skill，MIT License），2026-09 吸收并本地化（骨架链接替换为 maliang motion-skeletons）。

## 双轴：把"要什么效果"和"怎么实现"分开

| 轴 | 问的问题 | 在哪回答 |
| --- | --- | --- |
| **EFFECT 效果** | 观众看到什么：长廊？粒子？逐字？重排？ | §3 十族目录 |
| **ROUTE 路线** | 怎么实现：CSS？原生滚动？GSAP？WebGL？ | §2 六路线表 |

同一个效果可以走三条路线，成本差 60KB："元素随滚动入场"用 CSS 四行，用 GSAP 60KB——输出一样。**每次都伸手拿重路线的页面不是更强，是更贵更慢，而且看起来和别人一样。**

## §1 GATE —— 写第一个 keyframe 之前过四查

全部强制，后两条是页面真正死掉的地方：

1. **有动机**。每一拍给出一句话理由：层级 / 理解 / 反馈 / 状态 / 身份。「看起来很酷」不是理由；写不出来就砍掉这一拍。
2. **剥掉能活**。去掉所有动画后页面必须可读、完整、可导航。动效是增强，不是结构——内容只在滚动触发后才出现的页面是坏的，不是"有动效"。
3. **有静止终态**。`prefers-reduced-motion: reduce` 不是"关掉动画"，而是**一张构图好的静止帧**——你会选它当截图的那一帧。它与动效同时设计，不是事后补（§2 路线表给出每条路线的静止形态）。
4. **60fps 否则简化**。只动 `transform` 和 `opacity`；其余（`width`/`top`/`filter`/`box-shadow`）都会重合成。中端设备实测 <50fps：砍数量、砍分辨率、或砍这一拍。

```js
// 探针模式——文件顶部读一次,按效果分支
const RM   = matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE = matchMedia('(hover: hover) and (pointer: fine)').matches;
// if (RM) → 直接置终态; else → 动画
// 指针驱动效果必须 && FINE,触屏上永不触发
```

```css
/* CSS 兜底——永远与 JS 分支同时交付,不是替代 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
```

> **兜底是地板，不是降级方案。** 它让动画停止，但不构成静止终态。一个内容 `opacity: 0` 等动画才能出现的 hero，在兜底之下将**永久不可见**。每个动效元素必须以**终态**为默认写法、从别处动画过来，或显式给出 reduced-motion 终态规则。

## §2 六条路线

| 路线 | 重量 | 负责 | reduced-motion 静止形态 | 死法 |
| --- | --- | --- | --- | --- |
| **R1 · CSS transition / keyframes** | 0 | 状态变化、微交互、入场、环境循环 | 已写好的终态 | 试图做时序——无 timeline 无 scrub，`animation-delay` 链不可维护；**手势驱动动效**——过渡无法中途抓取反转、无法继承手指速度，一律改走 JS 弹簧（见 [`interruptible-motion.md`](interruptible-motion.md) 核心原则法则④） |
| **R2 · 原生滚动驱动**（`animation-timeline`） | 0 | 视差、进度、逐项到达、sticky 揭示 | 中段进度帧 | 无 pin、无跨元素编排；需无支持时的优雅退化 |
| **R3 · View Transitions + WAAPI** | 0 | 列表增删、筛选重排、路由切换、展开塌陷 | 即时切换无补间 | 忘写无转换 fallback，旧浏览器硬闪 |
| **R4 · GSAP + ScrollTrigger** | ~60KB | pin 叙事、横向轨、scrub、`containerAnimation` | kill 掉 ScrollTrigger，tween 置终态 | 拿去做 R1/R2 免费能干的活——**最常见的越权** |
| **R5 · Canvas / WebGL / GLSL** | 100-160KB | 粒子、场、流体、材质、后期 | 渲染一帧后停循环 | DOM 没了：文字不可选、图片不可索引、无懒加载 |
| **R6 · 零依赖 CSS 3D 空间** | 0 | 摄像机在 DOM 面板场景中移动 | 摄像机停最佳构图 | 画家算法排序翻转（见深度重叠） |

**选型顺序：从 R1 开始，停在第一条能干活的路线。**每往下一步都增加重量，没有观众感谢过页面的 bundle size。唯一正当的越级理由：效果真的需要那条路线独有的能力（`pin` → R4；逐像素材质 → R5）。

**R5 的真实代价不是 KB，是 DOM。**内容一旦变成纹理就不再是内容——不可选中、不可索引、读屏器读不到、没有 `loading="lazy"`。**当"3D 的东西"是照片和文字时，R6 胜 R5**；R5 留给真正的材质（流体、烟雾、虹彩、渲染体），不是画廊。

## §3 十族效果目录

> 从 brief 的**内容**里选族，不从"什么看起来厉害"里选。每族给出：变体池（轮换用）、默认路线、SPECTACLE 区间、**slop form**（已经做滥、读起来就是 AI 味的形态）、死法。与 maliang 骨架的挂接在每族末尾。

### 3.1 Spatial · 摄像机穿行场景
变体：长廊 / 星球内壁 / 圆环 / 隧道 / 螺旋 / 书架墙 / 蜂巢 / 竖井。默认 **R6**，SPECTACLE 7-9，需 ≥12 项真实内容才配做。
**slop form**：WebGL 发光六边形线框无限隧道——墙上没有任何内容。
**死法**：相近深度面板互相翻转遮挡 → 闪烁。
→ 滚动驱动变体见 [`scroll-band-gallery.md`](../templates/page/scroll-band-gallery.md)。

### 3.2 Particle · 粒子场
变体：星云 / 网络图 / DNA 螺旋 / 流场 / 磁力线 / 噪声漂移 / 文字聚散 / 星轨。默认 **R5**（2D 场用 Canvas 2D，深度用 Three.js），SPECTACLE 6-9。
**slop form**：邻居连线的星座图 + 鼠标排斥——**全网出镜率最高的 AI hero**，禁用。
**死法**：DPR 没处理（retina 发糊）；粒子数在开发机上调的（笔记本 20fps）。

### 3.3 Fluid · 流体与材质
变体：Navier-Stokes / 反应扩散 / 虹彩油膜 / 熔融金属 / 墨水扩散 / 波纹 / 光线步进 SDF / 玻璃折射。默认 **R5**（WebGL FBO 多 pass），SPECTACLE 8-10，**必须是页面唯一效果**。
**slop form**：紫到青的动画网格渐变 blob——它只说"AI 创业公司"。
**死法**：手机上全分辨率多 pass；没有设计静止帧（reduced-motion 得到黑矩形）。

### 3.4 Scroll narrative · 滚动叙事
变体：章节 pin 换幕 / 横向轨 / 缩放推进 / 图层剥离 / 序列帧 / 进度轨 / 文字接力。默认 **R2/R4**，SPECTACLE 6-9。
**slop form**：唯一一拍 hero 引擎 + 下方千篇一律的 fade-up。
**死法**：整页只有这一族——四拍节奏（见 §4）要求跨族取材。
→ pin/横向/scrub 骨架：[`sticky-stack.md`](sticky-stack.md) / [`horizontal-pan.md`](horizontal-pan.md) / [`scroll-scrub-bind`](../vocabulary/scroll.md)。

### 3.5 Typographic · 文字即主角
变体：逐字揭开 / 可变字重波 / 大字遮罩 / 字距呼吸 / 跑马灯 / 数字滚动 / 换词 / 描边转填充。默认 **R1**（滚动联动加 R2，错峰 scrub 才用 R4），SPECTACLE 4-7——**清单上最便宜的真爱**。
**slop form**：标题打字机效果 + 光标闪烁。
**死法**：给全页每个 `<h2>` 都拆字——第三处开始就不像刻意了。限 1-3 个标题。**CJK 按字符拆，不按词**（没有空格可拆）。

### 3.6 Image transform · 图像变换
变体：位移扭曲 / 遮罩溶解 / 拼贴重排 / 裁切滑移 / 色彩分离 / 双图对比 / 缩略图展开 / 视差裁切。默认 **R1/R2**（`clip-path`、`mask-image` 免费动画）；真逐像素位移才 R5，SPECTACLE 5-8。
**slop form**：所有图片 hover 前灰度、hover 后上色。
**死法**：用在不够好的图上——这一族对素材是双向放大。

### 3.7 Geometric construction · 几何构造
变体：SVG 描边绘制 / 图元拼装 / 网格坍缩 / 等距堆叠 / 分形展开 / 线框成形 / 图表自绘。默认 **R1 + SVG**（`stroke-dashoffset`、`clip-path`），scrub 到滚动加 R2，SPECTACLE 4-7。
**slop form**：无——**这是最被低估的一族**，也是花一拍最安全的地方。`stroke-dashoffset` 画入四行代码，读起来是真功夫。
**死法**：暂时没有。图表自绘配 [`../vocabulary/charts.md`](../vocabulary/charts.md) `chart-ring-draw`。

### 3.8 Physics · 物理与惯性
变体：磁吸 / 弹簧回弹 / 拖拽甩动 / 平滑惯性 / 卡片堆叠 / 摆动 / 橡皮筋。默认 **R1 弹簧曲线**；必须逐帧跟指针才 R4（`quickTo`），SPECTACLE 3-6。
**slop form**：自定义光标——一个点拖着迟滞的圆环。
**死法**：触屏上交付（必须 `&& FINE`）；或用到每个链接上直到读起来像抽搐。
→ 骨架：[`spring-reorder.md`](spring-reorder.md) / [`metaball-tether.md`](metaball-tether.md) / [`interruptible-motion.md`](interruptible-motion.md)。
→ 组件命名：`card-tilt-glare` / `sheet-velocity-anchor` / `press-scale-overshoot` / `stagger-spring-cascade` 见 [`../vocabulary/pro-motion.md`](../vocabulary/pro-motion.md)。

### 3.9 State transition · 状态转场
变体：列表增删 / 筛选重排 / 路由切换 / 展开塌陷 / 排序 / 标签页滑动 / 骨架到内容 / 乐观更新 / **图标级状态切换**（menu↔close、play↔pause、eye 显示↔隐藏、主题日月——morph 变体，设计决策见 [`../dimensions/icon.md`](../dimensions/icon.md) 动效图标节）。默认 **R3**，SPECTACLE 2-5。
**微状态机视角**：把图标当作「一个元素 + 多个命名状态」（空 / 收藏、锁定 / 解锁），morph 表达的是状态迁移本身——收藏、锁定类按钮用同一图标在不同命名状态间形变，比「两个图标瞬换」多传达一层因果。适用约束（仅 stroke 同源图标、两端同网格、统一描边）见 icon.md；库选型与下载一律走 xizhi。
**slop form**：没有——这一族的问题是被**长期缺席**。
**死法**：从来不做。**唯一属于 Operate/产品向页面的动效族**，仪表盘不再像页面刷新靠的就是它。
→ 骨架：[`shared-element.md`](shared-element.md) / [`circular-reveal.md`](circular-reveal.md) / [`../vocabulary/sheet-drawer.md`](../vocabulary/sheet-drawer.md)。
→ 组件命名：`capsule-fluid-morph` / `shared-element-expand` 见 [`../vocabulary/pro-motion.md`](../vocabulary/pro-motion.md)。

### 3.10 Atmosphere · 氛围
变体：颗粒 / 扫描线 / 辉光脉动 / 渐晕呼吸 / 光标光源 / 呼吸背景 / 噪声叠层 / 色温漂移。默认 **R1**（颗粒用一段内联 SVG `feTurbulence`），SPECTACLE 2-5。
**slop form**：全页背后一层全屏动画渐变网格。
**死法**：给颗粒做动画（贵，且是噪声上叠噪声）。**颗粒冻结；此层 opacity > 0.06 的东西一律不动画。**

> 边框光晕类（旋转渐变描边 + 呼吸弥散背光）走组件命名 [`border-conic-glow`](../vocabulary/pro-motion.md)，实现口径见该篇使用规则。

```css
/* Grain——值得背下来唯一的氛围原语。零素材零 JS。 */
body::before {
  content: ''; position: fixed; inset: 0; z-index: 999; pointer-events: none;
  opacity: .04; mix-blend-mode: overlay; background-size: 180px 180px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

## §4 四拍节奏表

> 替代"一个炫技 hero + 满页 fade-up"的默认构图：一页取 **4 拍，来自 4 个不同的族**，强度递减。SPECTACLE 高档位（Experience/Persuade 模式，见 [`../meta/surface-modes.md`](../meta/surface-modes.md)）取"1 个 hero 级 + 3 个次级"；Operate 页只保留 3.9 状态转场族。

| 拍 | 角色 | 取族建议 |
| --- | --- | --- |
| 1 | Hero（首屏一拍） | 3.1-3.3 重族选一（或 3.5 文字族轻量替代） |
| 2 | 滚动叙事拍 | 3.4 |
| 3 | 内容拍 | 3.5-3.7 |
| 4 | 反馈拍 | 3.8-3.9（Operate 页的唯一拍） |

**anti-slop 自检**：把你页面的每一拍对着 §3 对应族的 slop form 读一遍——命中任何一条，重选变体或换族。

## §5 时序模型：spring / easing / linear / 无动画

> 按动效的**驱动源**选时序模型，不按「想要什么感觉」。来源：web-design-pascalorg（Spring Physics vs Easing Decision Framework），2026-09 吸收，中文重写。
>
> **时长从属声明**：本节只取决策框架；一切时长数值以 maliang 强制口径为准（反馈 <300ms、浮层转场 ≤400ms，见 [`../vocabulary/micro-interactions.md`](../vocabulary/micro-interactions.md) 分层口径，从属 [`rules-priority`](../meta/rules-priority.md) 裁决层）。上游 500ms drawer 一类数值与本口径冲突，弃用。

| 驱动源 | 模型 | 理由 | 落点 |
| --- | --- | --- | --- |
| 用户驱动（拖拽、甩动、滑动） | **spring** | 中断后存活、保留速度；必须把 pointer 速度传入（velocity 交接） | [`interruptible-motion.md`](interruptible-motion.md) 两参数模型 + 三公式 |
| 系统驱动（状态变化、反馈、转场） | **easing** | 起止清晰、时序可预测；入场 ease-out、退场 ease-in，可反转过渡镜像缓动 | [`../vocabulary/micro-interactions.md`](../vocabulary/micro-interactions.md) 缓动曲线库 |
| 时间表征（进度、加载、循环） | **linear** | 时间与进度 1:1；仅限 spinner / 进度条类连续动效 | — |
| 高频键盘 / 命令操作 | **无动画** | 每天上百次，延迟即成本（频率法则一票否决） | [`../vocabulary/micro-interactions.md`](../vocabulary/micro-interactions.md) 频率法则 |

**回弹要用真弹簧，不用 easing 伪装**：过冲落定（bounce-and-settle）是弹簧的语义，cubic-bezier 近似只够一次性过渡（近似边界见 [`spring-reorder.md`](spring-reorder.md)）；Web 侧起步参数换算成 damping/response 后按两参数模型声明。**动效嫌慢先砍 duration，不动缓动曲线**——慢几乎总是时长问题。

**exit 原则**：入场 ≠ 退场。退场比入场幅度小、更快——用固定小位移（如 `y: -12px`）表达方向即可，不做全程撤离动画；叠一层轻 `blur(4px)` 软化消失感。退场元素禁交互（指针事件关闭），防止用户点到正在离开的东西。

**View Transitions 注记**：跨页 / 跨容器共享元素转场的**原生方案**是 View Transitions API（本文件 R3 路线），列表增删、路由切换优先走它而非 JS 库；无支持浏览器必须留即时切换 fallback（R3 死法栏）。
