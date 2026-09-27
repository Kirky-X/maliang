# 微雕手艺集 —— 光学修正与 CSS 打磨配方

> 规范层。专业感不是单点突破，而是大量小而有意的决定叠加——单个不值一提，合起来就是「这东西说不出哪里好但就是 feels right」。本文收录这类微雕配方，宁缺毋滥，逐条可核对。来源：web-design-pascalorg §13/§16 思想吸收（中文自研，非文本翻译），2026-09 吸收。
> **框架边界（先读）**：除光学修正清单为跨端通用的经验数值外，**其余各节均为 Web CSS 专属机制**——ArkTS/Flutter/Element 无对应 CSS 能力，禁止跨框架套用（各端等价能力查 [`../framework/index.md`](../framework/index.md)）。glass/毛玻璃与 squircle 圆角**不在本文**：maliang 已收 [`../templates/glassmorphism.md`](../templates/glassmorphism.md)、[`../dimensions/glass-effect.md`](../dimensions/glass-effect.md)、[`../dimensions/radius.md`](../dimensions/radius.md)。

## 一、六层按钮阴影解剖（仅 Web CSS）

平整色块按钮缺少物理感；专业按钮靠**六层协作**模拟真实光照——渐变给体积、内阴影给环境光与方向光、外阴影给海拔：

```css
.button-polished {
  /* 体积:主色向亮部混白 4% 的纵向微渐变(oklch 混色,色相不偏移) */
  background: linear-gradient(
    to bottom,
    color-mix(in oklch, var(--color-primary), white 4%),
    var(--color-primary)
  );

  box-shadow:
    /* 1. 外切边:0.5px 带色深环,把按钮从同色背景里切出来 */
    0 0 0 0.5px hsl(var(--shadow-hue) / 0.15),
    /* 2. 内环境光:1px 全周白色微透,模拟环境反光(白系高光非阴影,不受禁黑约束) */
    inset 0 0 0 1px rgba(255, 255, 255, 0.08),
    /* 3. 内顶光:顶部 1px 白色略强,统一光源方向(上) */
    inset 0 1px 0 rgba(255, 255, 255, 0.15),
    /* 4-6. 三层海拔投影:带色深色+几何递增(blur=2×offset),近实远虚 */
    0 1px 2px hsl(var(--shadow-hue) / 0.12),
    0 2px 4px hsl(var(--shadow-hue) / 0.08),
    0 4px 8px hsl(var(--shadow-hue) / 0.06);

  text-shadow: 0 1px 1px hsl(var(--shadow-hue) / 0.1);
}
```

- 六层是一个**整体配方**：只抄 4-6 三层外阴影会显脏，缺 1 外切边会在同色背景上融化，缺 2/3 内光会像贴纸
- 4-6 层与 text-shadow 的 `hsl(var(--shadow-hue) / …)` 对齐 [`../dimensions/elevation.md`](../dimensions/elevation.md) §五（`--shadow-hue` 取页面背景色相，禁纯黑；透明度落其 0.06-0.12 区间）
- 阴影**统一光源方向**、亮色界面**弹层 4 层投影**的通用配方见 [`../dimensions/elevation.md`](../dimensions/elevation.md) §五（本文是其上的按钮级微雕）；暗色界面按钮走明度阶梯，不照搬外投影（暗底上阴影不可见）

## 二、噪点纹理配方（仅 Web CSS + SVG）

平整大面积纯色易显「塑料感」；一层极低透明度噪点恢复有机质感。**配方**：`feTurbulence` 生成噪点，内联 data URI 免请求：

```css
.textured::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.03;              /* 允许区间 0.02-0.05:高于 0.05 显脏,低于 0.02 无感 */
  mix-blend-mode: overlay;    /* 叠加混合,明暗两面都起效 */
  pointer-events: none;
}
```

- **性能铁律回链 [`performance.md`](performance.md) grain/noise 节**：全屏纹理必须走 `::before` 伪元素 + `position: fixed` + 尺寸限定 viewport + 平铺，禁止对 `<body>`/大面积容器直接贴图或做动画；本文补的是**配方本身**（feTurbulence 参数与透明度区间），落地时两条合用

## 三、@property 类型化自定义属性（仅 Web CSS）

CSS 自定义属性默认是「不透明字符串」，**无法插值**——直接对 `--angle` 做 transition/animation 只会在首尾值间跳变。`@property` 声明类型后，浏览器才能逐帧插值：

```css
@property --gradient-angle {
  syntax: "<angle>";        /* 声明为角度类型,插值才成立 */
  initial-value: 0deg;
  inherits: false;
}

.rotating-border {
  --gradient-angle: 0deg;
  border-image: conic-gradient(from var(--gradient-angle),
    var(--color-primary), var(--color-accent), var(--color-primary)) 1;
  animation: border-spin 6s linear infinite; /* 装饰循环,时长与启用条件过 dials.md 门槛 */
}

@keyframes border-spin {
  to { --gradient-angle: 360deg; }
}
```

- 适用：旋转渐变边框、角度扫光等「属性本身要动」的场景；装饰性循环动效先过 [`dials.md`](dials.md) 的 MOTION_INTENSITY 门槛，reduced-motion 下停帧
- 兼容：主流现代浏览器均已支持；不支持的环境降级为**静态首帧**（样式不破，动画不跑），无需另写兜底
- 附带收益：`syntax` 声明让非法值在解析期暴露，而不是静默吞掉

## 四、gradient mask 滚动边界淡出（仅 Web CSS）

滚动容器上下边缘的内容被硬裁切，加一层 mask 渐隐暗示「下面还有」：

```css
.scroll-fade {
  overflow-y: auto;
  max-height: 16rem;
  -webkit-mask-image: linear-gradient(to bottom,
    transparent, black 1rem, black calc(100% - 1rem), transparent);
  mask-image: linear-gradient(to bottom,
    transparent, black 1rem, black calc(100% - 1rem), transparent);
}
```

- 渐隐带 `1rem` 起步，横向轮播同构换 `to right`
- **注意**：mask 是视觉渐隐，不是交互边界——被渐隐的内容仍可点击，勿用 mask 冒充「查看更多」的截断（截断语义按 ux-rules `truncation-strategy` 给展开路径）
- WebKit 前缀历史包袱仍在，`-webkit-mask-image` 与标准属性成对写

## 五、inset ring vs border 判定（仅 Web CSS）

| 场景 | 用什么 | 为什么 |
| --- | --- | --- |
| 图片/头像/媒体容器的描边 | **inset ring**（覆盖层或 `box-shadow` inset） | border 挤压内容盒、改变元素尺寸；ring 不占布局、随圆角弯折、贴在内容上更自然 |
| 结构分隔（面板边界、表单框） | **border** | 分隔是布局语义，本就该占位、参与盒模型 |
| 快速给既有元素加 1px 内描边 | `box-shadow: inset 0 0 0 1px …` 速记 | 不动 DOM、不加覆盖层 |

```css
/* 媒体容器:覆盖层 ring,不占尺寸 */
.media-frame { position: relative; overflow: hidden; border-radius: var(--radius-md); }
.media-frame::after {
  content: ''; position: absolute; inset: 0;
  border-radius: inherit;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
}
```

- 描边颜色的自适应半透明写法（替代明暗两套 hex token）见 [`../dimensions/elevation.md`](../dimensions/elevation.md) rgba 边框阶梯

## 六、光学修正清单（经验数值跨端通用，实现例为 Web CSS）

几何居中不等于视觉居中——字形的光学重心与包围盒天然偏移，人眼期待的是**视觉居中**。数值为经验区间，各端按单位换算（px ↔ vp/dp）：

| 场景 | 修正 | 原因 |
| --- | --- | --- |
| 播放按钮三角 | 在 **SVG viewBox 内**右移 1-2px（而非外层 CSS） | 三角形视觉重心偏左于其包围盒；修在源文件内，所有引用处一次到位 |
| 图标 + 文字的按钮 | 图标一侧 padding **减 2-4px** | 图标自带内留白，与文字侧 padding 相等则图标侧看起来更「空」 |
| 方形容器里的圆形图标 | 图标尺寸 **+5%**，或缩容器 padding | 同尺寸下圆形面积显小，视觉上「缩了一号」 |
| checkbox/radio 与文字同行（小字号） | 控件相对文字基线**负 margin 1-2px** 或下移 | 控件盒基线高于文字视觉中心，原样对齐显得控件「浮起」 |
| pill/全圆角徽章 | 水平 padding **额外 +2-4px** | 全圆角在视觉上「吃掉」两端留白，按半径直觉给 padding 会显挤 |
| 全大写按钮文字 | 底部 padding **+1px**（或 `leading-none` 后手动配平） | 大写字母无降部，文字块视觉重心整体偏上 |

## 七、伪元素与原生伪元素选择器省 DOM（仅 Web CSS）

能用原生伪元素做到的，不造额外节点：

| 选择器 | 替代什么 | 示例 |
| --- | --- | --- |
| `::marker` | 列表符的背景图/伪元素 hack | `li::marker { color: var(--color-text-muted); font-size: 0.8em; }` |
| `::backdrop` | dialog/popover 手搭的遮罩 div | `dialog::backdrop { background: rgba(0,0,0,.5); backdrop-filter: blur(4px); }` |
| `::first-line` | 手动给首行套 span 做排版 | `.article p:first-of-type::first-line { font-weight: 500; }`——随视口重排自动跟随「第一行」，span 做不到 |
| `::selection` | JS 换选区色 | `::selection { background: …; color: …; }`——品牌一致性；对比度仍须过 AA（[`accessibility.md`](accessibility.md)） |
| `::placeholder` | 输入框内叠加层 | 占位符对比度弱于正文即可，但不得低于可读下限（ux-rules `form-labels`：placeholder 不能当唯一标签） |

- 注意 `::first-line` 仅支持有限的字体内属性子集（颜色/字重/字距/变形等），不支持盒模型属性
- `backdrop-filter` 的性能降级方案见 [`../dimensions/glass-effect.md`](../dimensions/glass-effect.md)

## 与其他文档的关系

- [`../dimensions/elevation.md`](../dimensions/elevation.md)：海拔阶梯/表面规则/rgba 边框阶梯/弹层投影通用配方是「体系层」，本文六层按钮阴影是「单件微雕层」，两者叠加使用
- [`performance.md`](performance.md)：噪点/混合模式的性能铁律（伪元素 + fixed + viewport 限尺寸）在 grain/noise 节，本文配方必须在其约束内落地
- [`../dimensions/radius.md`](../dimensions/radius.md)、[`../templates/glassmorphism.md`](../templates/glassmorphism.md)：squircle 与玻璃拟态已收，本文不重复
- 微雕不豁可访问性：焦点环（`focus-states`）、对比度（`color-contrast`）、占位符语义（`form-labels`）在 ux-rules 中均为更高优先级约束
