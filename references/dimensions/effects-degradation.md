# 模拟退化效果配方 —— CRT 扫描线 / Halftone 抖动 / 机械噪点

> 维度规范(效果配方)。给界面叠加「模拟硬件退化」的三条 CSS/SVG 配方:让设计脱离纯数字感,长出物理介质或原始发光体的质感。主要服务 [`../templates/tactical-terminal.md`](../templates/tactical-terminal.md)(CRT 终端)与印刷/工业风模板;来源:taste-skill industrial-brutalist-ui(license 未考——思想内化,配方措辞为本仓库自著),2026-10 吸收。

**使用前提**:全部效果都是纯装饰层,必须满足 [`../meta/accessibility.md`](../meta/accessibility.md) 与 [`../meta/performance.md`](../meta/performance.md) 的降级要求——`prefers-reduced-motion` / `prefers-reduced-transparency` 下整层移除;叠加层一律 `pointer-events: none`;扫描线/噪点用 `position: fixed` 伪元素挂 `body` 而非逐元素添加。**克制原则**:三种效果同时全开 = 廉价滤镜合集;单界面最多一种主导退化 + 一种全局颗粒。

## 1. CRT 扫描线

模拟电子束横向扫描。暗色终端界面的背景层:

```css
body::after {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.1) 2px,
    rgba(0, 0, 0, 0.1) 4px
  );
  z-index: 9999;
}
```

- 行距(`2px/4px`)可按像素密度调整,但条纹不透明度压在 `0.08-0.12`——超过就变成百叶窗。
- 亮色印刷风界面不用本配方(扫描线属于发光体语义)。

## 2. Halftone / 1-bit 抖动

把连续调图像或衬线大字降解为点阵。两层配合:

```html
<div class="dithered">
  <img src="hero.jpg" alt="" />
</div>
```

```css
.dithered { position: relative; display: inline-block; }
.dithered img { display: block; filter: grayscale(1) contrast(1.2); }

/* 网点覆盖层:SVG 径向点阵平铺 + 正片叠底 */
.dithered::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(circle, #000 1px, transparent 1.5px);
  background-size: 4px 4px;
  mix-blend-mode: multiply;
}
```

- 点距(`background-size`)越小越接近印刷铜版纸质感;黑白双色的 1-bit 抖动则再加 `filter: contrast(10)` 极端化。
- 用在图像与衬线字上;正文 mono 数据层**不抖**——信息层必须保持锐利。

## 3. 全局机械噪点

一层低不透明度 SVG 噪声铺满 DOM 根,统一物理颗粒感(亮暗基底通用):

```html
<svg style="display:none">
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" stitchTiles="stitch" />
  </filter>
</svg>
```

```css
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background: #000;
  filter: url(#grain);
  opacity: 0.04;   /* 亮色底可到 0.06,暗色底 0.03-0.04 */
  z-index: 9998;
}
```

- `baseFrequency 0.6-0.9` 之间取细颗粒;opacity 是红线——`> 0.08` 就从「纸感」跌到「信号差」。
- 与扫描线叠加时,噪点放 `::before`、扫描线放 `::after`,互不覆盖。

## 降级与检查

- [ ] 三层都是 `pointer-events: none` 且不参与布局(reflow 零成本)?
- [ ] `prefers-reduced-motion` / `prefers-reduced-transparency` 下整层移除?
- [ ] 单界面 ≤ 一种主导退化 + 一种全局颗粒?
- [ ] 信息层(mono 数据、正文)未被抖动/噪点波及,可读性无损?
