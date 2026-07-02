# 性能强制 —— Core Web Vitals / Hardware Accel / DOM Cost / Z-Index

> 规范层。性能是 HIGH 优先级规则(见 [`rules-priority.md`](./rules-priority.md)),与 Style/Layout/Navigation 同级,高于 Typography/Animation/Forms/Charts。本文列出**强制不可妥协**的性能阈值与实现约束。来源:taste-skill + ui-ux-pro-max-skill。

## 1. Core Web Vitals 硬阈值

| 指标 | 阈值       | 含义                                       | 失败处理                          |
| ---- | ---------- | ------------------------------------------ | --------------------------------- |
| LCP  | < 2.5s     | 最大内容绘制(首屏感知速度)               | preview 阶段 Pre-Flight Check 失败 |
| INP  | < 200ms    | 交互到下一帧(2024 替代 FID)              | 框架代码生成时强制拆分长任务      |
| CLS  | < 0.1      | 累积布局偏移(视觉稳定)                   | 必须为图片/iframe 设 width/height |
| FCP  | < 1.8s     | 首次内容绘制(辅助参考)                   | —                                 |
| TTFB | < 800ms    | 首字节时间(后端/CDN 责任,设计层标注)    | 不在 design 范围,但需提示        |

**移动端乘以 1.5 倍宽松度**:移动网络与中端机型下,LCP < 3.75s 可接受,但 INP 仍 < 200ms 不可放宽。

## 2. Hardware Accel(硬件加速)

只允许动画化以下两个 CSS 属性:

| 属性                | 不会触发布局/绘制 | GPU 合成层 |
| ------------------- | ----------------- | ---------- |
| `transform`         | ✓                 | ✓          |
| `opacity`           | ✓                 | ✓          |
| `filter`(慎用)     | ✓(但开销大)      | ✓          |
| `width/height`      | ✗ 触发 layout     | ✗          |
| `top/left/margin`   | ✗ 触发 layout     | ✗          |
| `box-shadow` 动画   | ✗ 触发 paint      | ✗          |

**强制规则**:

- 入场动画用 `transform: translateY(8px) → 0` + `opacity: 0 → 1`,不用 `top` / `margin-top`
- 滚动揭示用 `transform` + `opacity`,触发器用 `IntersectionObserver` 而非 scroll 事件
- 视差用 `transform: translate3d()`,且仅 MOTION_INTENSITY ≥ 7 时启用
- `will-change` 仅在动画进行中临时设置,完成后移除(常驻 `will-change` 会爆显存)

## 3. DOM Cost(DOM 开销)

### grain/noise 纹理

**禁止**直接对 `<body>` 或大面积容器加 `background-image: url(noise.png)` + 动画——会强制全屏重绘。

**强制方案**:纹理必须用 `::before` 伪元素 + `position: fixed` + `pointer-events: none` + `z-index: 1`(或合适的层叠位置),且尺寸限定为 viewport:

```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background-image: url('noise.svg');
  background-size: 200px 200px;
  opacity: 0.04;
  mix-blend-mode: overlay;
}
```

### 通用 DOM 节流

- 长列表 > 100 项必须虚拟滚动(virtual scroll)
- 图标改 SVG sprite 或 icon font,不内联重复 path
- `box-shadow` 大模糊半径(≥ 40px)慎用,paint 开销大;优先用 `filter: drop-shadow` 或预制 PNG
- `backdrop-filter` 慎用,移动 Safari 性能差,见 [`glass-effect.md`](../dimensions/glass-effect.md) 的降级方案

## 4. Z-Index Restraint(z-index 克制)

**禁止**散落使用 `z-index: 999` / `z-index: 9999` / `z-index: 100000` 等魔法值。

**强制 token 化**(应在 [`token.md`](./token.md) 的 `z-index` category 中定义):

```yaml
z-index:
  base: 0          # 普通文档流
  dropdown: 100    # 下拉菜单
  sticky: 200      # 粘性导航
  drawer: 300      # 抽屉
  modal: 400       # 模态框
  toast: 500       # toast 通知
  tooltip: 600     # tooltip(最高,因需浮于 modal 上)
```

**规则**:

- 每层间隔 100,留扩展空间
- 同层内的子元素用局部 stacking context(`isolation: isolate` 或 `transform: translateZ(0)`),不污染全局
- `z-index` 必须 token 化,代码中禁止字面量(见 [`token.md`](./token.md) 硬性约束)
- tooltip 永远最高(因为可能浮于 modal 之上提示)

## 5. 资源加载策略

| 资源类型 | 策略                                                                |
| -------- | ------------------------------------------------------------------- |
| 字体     | `font-display: swap` + preload 关键字体的子集(woff2)              |
| 图片     | `loading="lazy"`(非首屏)+ `decoding="async"` + 必设 width/height |
| CSS      | 关键 CSS 内联到 `<head>`,非关键 CSS 异步加载                       |
| JS       | `defer` 或 `type="module"`,首屏 JS ≤ 100KB gzip                    |
| 第三方   | 延迟到 `requestIdleCallback` 或用户交互后加载                       |

## 6. Preview 阶段的性能检查

在 [`preview.md`](../commands/preview.md) 的 Pre-Flight Check 中,以下为硬性失败项:

- [ ] 图片无 width/height → CLS 风险
- [ ] 字体无 `font-display: swap` → LCP 风险
- [ ] 动画化非 transform/opacity 属性 → INP 风险
- [ ] grain/noise 用 `body` 背景非伪元素 → paint 风险
- [ ] `z-index` 出现字面量而非 token → 一致性失败
- [ ] 首屏 JS > 100KB gzip → LCP 风险(标注,非硬性失败)

## 与其他文档的关系

- 触发性能与动画冲突时,按 [`rules-priority.md`](./rules-priority.md) Performance(HIGH) > Animation(MEDIUM) 裁决
- 动画档位 MOTION_INTENSITY 由 [`dials.md`](./dials.md) 定义,Level 8-10 必须额外通过性能预算审计
- 框架代码生成时,所有动画实现必须符合第 2 节 Hardware Accel,代码注释标注 `// perf: transform-only`
