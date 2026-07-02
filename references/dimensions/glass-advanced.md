# Liquid Glass Advanced —— 真实折射实现(SVG + WebGL 双引擎)

> 维度规范(进阶)。本文件是 [`glass-effect.md`](./glass-effect.md) 基础配方的升级路径:从 `backdrop-filter` 模糊近似 → 物理折射(SDF + 位移图 + IOR + 色差)。
> 技术来源 4 个开源仓库:`shuding/liquid-glass`(SVG SDF)、`archisvaze/liquid-glass`(双引擎 + 物理参数)、`rdev/liquid-glass-react`(Props API)、`@wxperia/liquid-glass-vue`(Vue 适配 + effect 枚举)。来源:taste-skill。

**使用前提**:真实折射性能开销远大于基础配方,必须配 WebGL fallback + `prefers-reduced-motion` 降级。移动端慎用,优先回到 [`glass-effect.md`](./glass-effect.md) 基础配方。

---

## 1. SVG feDisplacementMap + SDF 算法(shuding/liquid-glass)

核心思路:用 Canvas 生成位移图(displacement map),通过 SVG `feDisplacementMap` 滤镜对背景做像素级弯折,模拟玻璃边缘的折射。

### 算法三件套

| 函数                  | 作用                                                   |
| --------------------- | ------------------------------------------------------ |
| `roundedRectSDF`      | 圆角矩形有向距离场,计算像素到玻璃边缘的距离           |
| `smoothStep(a,b,t)`   | 平滑阶梯,把距离场映射为位移强度(边缘高、中心低)     |
| `feDisplacementMap`   | SVG 滤镜,按位移图的 R/G 通道偏移 SourceGraphic 像素   |

### 数据流

```
Canvas 像素 → fragment(uv) 计算 dx,dy → 写入 R/G 通道 → toDataURL
  → feImage 加载 → feDisplacementMap(scale=maxScale) → backdrop-filter: url(#filter)
```

### 最小 fragment(来源:shuding/liquid-glass.js)

```js
fragment: (uv) => {
  const ix = uv.x - 0.5, iy = uv.y - 0.5;
  const d = roundedRectSDF(ix, iy, 0.3, 0.2, 0.6);  // 玻璃形状 SDF
  const displacement = smoothStep(0.8, 0, d - 0.15); // 边缘位移强
  const scaled = smoothStep(0, 1, displacement);
  return { x: ix * scaled + 0.5, y: iy * scaled + 0.5 };  // 中心像素向边缘收缩 = 折射
}
```

**关键参数**:`0.3 / 0.2 / 0.6` = 玻璃半宽 / 半高 / 圆角半径;`0.15` = 边缘折射带宽度;`0.8 → 0` = 位移衰减区间。

### 局限

- `feImage` + `feDisplacementMap` **仅 Chrome / Chromium** 完整支持(见第 7 节矩阵)
- Canvas 每帧重算位移图,CPU 开销大;大尺寸玻璃需节流(raf + dirty flag)
- `backdrop-filter: url(#filter)` 在 Firefox / Safari 失效 → 必须配 WebGL fallback

---

## 2. 物理参数模型 + 双引擎降级(archisvaze/liquid-glass)

archisvaze 提供 **SVG(`index.html`)+ WebGL(`webgl.html`)双引擎**,可按钮切换。

### 引擎对比

| 维度        | SVG 引擎                                      | WebGL 引擎                              |
| ----------- | --------------------------------------------- | --------------------------------------- |
| 实现        | `feDisplacementMap` + `backdrop-filter`       | Three.js 全屏 GLSL shader               |
| 折射        | 位移图 + 可配 IOR                             | 实时 GLSL 光线折射                      |
| 浏览器      | Chrome / Chromium only                        | 所有现代浏览器                          |
| 控件        | 形状 / 折射 / 外观 / 内外阴影 / tint          | 形状 / 折射 / blur / specular / tint / shadow |

### 物理参数(archisvaze 命名)

| 参数             | 语义                                  | 典型范围       |
| ---------------- | ------------------------------------- | -------------- |
| `IOR`            | 折射率(玻璃 ≈ 1.5,水 ≈ 1.33)        | 1.3 - 1.7      |
| `glassThickness` | 玻璃厚度(影响边缘折射带宽度)        | 0.1 - 0.5      |
| `bezelWidth`     | 斜面宽度(边缘高光带)                | 0.05 - 0.2     |
| `specularOpacity`| 高光不透明度                          | 0.3 - 0.8      |
| `saturation`     | 饱和度提升                            | 110% - 180%    |
| `tintColor` + `tintOpacity` | 玻璃着色 RGB + 不透明度    | opacity 0 - 0.3 |

### 双引擎降级策略

```
检测:Chrome/Chromium? 
  → 是:用 SVG 引擎(无需 Three.js,首屏更轻)
  → 否:用 WebGL 引擎(Firefox/Safari 唯一选项)
检测:WebGL 不可用?
  → 是:降级到 glass-effect.md 基础配方(backdrop-filter: blur + saturate)
```

---

## 3. React Props API 设计参考(rdev/liquid-glass-react)

React 版提供组件化封装,Props 命名可直接借鉴到 maliang 组件规格。

### 核心 Props

| Prop                  | 类型                                                      | 默认值     | 语义                                 |
| --------------------- | --------------------------------------------------------- | ---------- | ------------------------------------ |
| `displacementScale`   | `number`                                                  | `70`       | 位移强度(折射感)                   |
| `blurAmount`          | `number`                                                  | `0.0625`   | 模糊/磨砂度                          |
| `saturation`          | `number`                                                  | `140`      | 饱和度                               |
| `aberrationIntensity` | `number`                                                  | `2`        | 色差强度(边缘 RGB 分离)            |
| `elasticity`          | `number`                                                  | `0.15`     | 液态弹性(0 = 刚硬,高 = 柔软)       |
| `cornerRadius`        | `number`                                                  | `999`      | 圆角(px)                           |
| `overLight`           | `boolean`                                                 | `false`    | 是否在浅色背景上(切换高光算法)     |
| `mode`                | `"standard" \| "polar" \| "prominent" \| "shader"`        | `"standard"` | 折射模式,`shader` 最精确但最不稳定 |
| `mouseContainer`      | `Ref<HTMLElement>`                                        | `null`     | 鼠标追踪容器(默认自身)             |
| `globalMousePos`      | `{x,y}`                                                   | -          | 全局鼠标坐标(手动控制)             |
| `mouseOffset`         | `{x,y}`                                                   | -          | 鼠标偏移微调                         |

### 用法范式

```tsx
// 卡片(默认 standard 模式)
<LiquidGlass>
  <div className="p-6"><h2>内容</h2></div>
</LiquidGlass>

// 按钮(prominent 模式 + 高弹性 + 色差)
<LiquidGlass
  displacementScale={64} blurAmount={0.1} saturation={130}
  aberrationIntensity={2} elasticity={0.35} cornerRadius={100}
  mode="prominent"
  onClick={...}
>
  <span>Click Me</span>
</LiquidGlass>

// mouseContainer:玻璃响应父容器鼠标,非自身
<LiquidGlass mouseContainer={containerRef} elasticity={0.3}>
  <div className="p-6">...</div>
</LiquidGlass>
```

---

## 4. Vue 适配 + effect 枚举(@wxperia/liquid-glass-vue)

Vue 版基于 React 版改编,额外提供 **effect 枚举**(shader 模式下的视觉变体)与**指令式**用法。

### Vue 特有 Props

| Prop      | 类型                                                                                     | 默认值         | 语义                                            |
| --------- | ---------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------- |
| `effect`  | `"flowingLiquid" \| "liquidGlass" \| "transparentIce" \| "unevenGlass" \| "mosaicGlass"` | `"liquidGlass"` | shader 模式下的视觉变体(仅 `mode="shader"` 生效) |

### effect 枚举语义

| effect            | 视觉特征                              | 适用场景                  |
| ----------------- | ------------------------------------- | ------------------------- |
| `liquidGlass`     | 默认液态玻璃,边缘折射 + 中心透明     | 通用,Apple iOS 26 风      |
| `flowingLiquid`   | 流动感,位移随时间扰动                | 动态背景、品牌叙事        |
| `transparentIce`  | 冰晶感,低饱和 + 高清晰度             | 冷色调产品、科技感        |
| `unevenGlass`     | 不均匀玻璃,表面有凹凸纹理            | 拟物、艺术化场景          |
| `mosaicGlass`     | 马赛克玻璃,像素化折射                 | 创意站、复古数字风        |

### 指令 vs 组件

- **指令(`v-liquid-glass`)**:对已有 DOM 元素施加效果,保留原结构,适合改造第三方组件
- **组件(`<LiquidGlass>`)**:完整玻璃容器方案,适合新建 UI

---

## 5. 组件参数规格表(maliang 推荐命名)

融合 4 个仓库,统一为 maliang 组件 token 命名(kebab-case,对齐 [`token.md`](../meta/token.md)):

| maliang token           | 来源              | 类型    | 默认 | 范围        | 语义                     |
| ----------------------- | ----------------- | ------- | ---- | ----------- | ------------------------ |
| `glass-border-radius`   | React/Vue         | px      | 16   | 4 - 999     | 圆角(999 = 胶囊)        |
| `glass-displacement`    | React/Vue/SVG     | number  | 70   | 0 - 200     | 位移强度(0 = 无折射)    |
| `glass-blur`            | React/Vue         | number  | 0.06 | 0 - 1       | 磨砂度                   |
| `glass-saturation`      | 全部              | %       | 140  | 100 - 200   | 饱和度提升               |
| `glass-aberration`      | React/Vue         | number  | 2    | 0 - 10      | 色差强度                 |
| `glass-elasticity`      | React/Vue         | number  | 0.15 | 0 - 1       | 液态弹性                 |
| `glass-ior`             | archisvaze        | number  | 1.5  | 1.3 - 1.7   | 折射率                   |
| `glass-thickness`       | archisvaze        | number  | 0.25 | 0.1 - 0.5   | 玻璃厚度(折射带宽度)   |
| `glass-bezel`           | archisvaze        | number  | 0.1  | 0.05 - 0.2  | 斜面宽度(边缘高光带)   |
| `glass-specular`        | archisvaze        | number  | 0.5  | 0 - 1       | 高光不透明度             |
| `glass-tint-color`      | archisvaze        | color   | -    | -           | 着色 RGB(可选)          |
| `glass-tint-opacity`    | archisvaze        | number  | 0    | 0 - 0.3     | 着色不透明度             |
| `glass-over-light`      | React/Vue         | boolean | false | true/false | 是否浅色背景(切高光算法)|
| `glass-mode`            | React/Vue         | enum    | standard | standard/polar/prominent/shader | 折射模式 |
| `glass-effect`          | Vue               | enum    | liquidGlass | 见第 4 节 | shader 模式视觉变体      |

---

## 6. Apple 系统级 effect 枚举(iOS 玻璃材质)

除社区 shader effect 外,Apple iOS 26 系统级玻璃材质有 4 档命名,maliang 在 DESIGN.md `glass:` 块建议沿用:

| effect        | 视觉特征                              | 适用场景                          |
| ------------- | ------------------------------------- | --------------------------------- |
| `clear`       | 几乎透明,极低模糊,高折射             | 浮层、工具栏、导航条              |
| `regular`     | 标准玻璃,中等模糊 + 饱和             | 卡片、Modal、侧边栏               |
| `prominent`   | 厚玻璃,高模糊 + 强饱和 + 边缘高光    | Dock、主控件、Hero 浮层           |
| `dark`        | 深色玻璃,低透 + 暗色 tint            | 暗色模式浮层、视频背景上的控件    |

**映射到 shader effect**:`clear` ≈ `transparentIce`、`regular` ≈ `liquidGlass`、`prominent` ≈ `flowingLiquid`、`dark` = `liquidGlass` + `glass-tint-color: #000` + `glass-tint-opacity: 0.3`。

---

## 7. 浏览器支持矩阵

| 浏览器               | SVG 引擎(`feDisplacementMap`) | WebGL 引擎(Three.js shader) | 基础配方(`backdrop-filter`) |
| -------------------- | ------------------------------ | ---------------------------- | ---------------------------- |
| Chrome / Edge 76+    | ✅ 完全支持                    | ✅ 完全支持                  | ✅ 完全支持                  |
| Firefox 103+         | ❌ `feImage` dataURL 受限      | ✅ 支持                      | ✅ 支持(需 flag 历史)       |
| Safari 9+            | ❌ `feDisplacementMap` 失效    | ✅ 支持                      | ⚠️ 需 `-webkit-` 前缀         |
| Samsung Internet     | ⚠️ 部分支持                    | ✅ 支持                      | ✅ 支持                      |
| 老 IE / 老 Android   | ❌                             | ❌                           | ❌ 降级为静态 `rgba()`        |

**降级链**:SVG 引擎 → WebGL 引擎 → 基础配方(`backdrop-filter: blur + saturate`)→ 静态 `rgba()` 背景。

---

## 8. 与 glass-effect.md 基础配方的关系(升级路径)

### 升级决策

```
是否需要真实折射感(边缘弯折、色差)?
  → 否:用 glass-effect.md 基础配方(性能优、兼容广)
  → 是:进入本文件
    → 目标浏览器仅 Chrome? 用 SVG 引擎(第 1 节,无需 Three.js)
    → 需跨浏览器? 用 WebGL 引擎(第 2 节,Three.js)
    → 框架? React 用第 3 节 Props,Vue 用第 4 节 + effect 枚举
```

### 共享规则(基础与进阶一致)

- **性能预算**:单页玻璃元素 ≤ 3 个(基础配方同),blur ≤ 30px,面积 ≤ 50% 视口
- **无障碍降级**:`prefers-reduced-transparency: reduce` → 退回静态不透明;`prefers-reduced-motion: reduce` → 关闭 shader 动画
- **禁止场景**:大面积全屏玻璃、信息密集表格背景、> 3 层嵌套(均同基础配方)
- **暗色模式**:tint 切深色,specular 降低,见 [`color.md`](./color.md) 第 5 节

### 不可越过基础配方直接用 advanced

advanced 引擎**必须**实现基础配方的降级链终点(`@supports not (backdrop-filter: blur(20px))` → 静态 `rgba()`),否则在不支持 WebGL 的环境会白屏。

---

## 与其他文档的关系

- 基础配方见 [`glass-effect.md`](./glass-effect.md)(本文件的降级终点 + 入口)
- 性能约束见 [`performance.md`](../meta/performance.md) 第 3 节 DOM Cost(advanced 引擎开销远大于基础)
- 无障碍降级见 [`accessibility.md`](../meta/accessibility.md) 第 4 节 prefers-reduced-transparency
- token 命名规范见 [`token.md`](../meta/token.md) 第 `glass-*` 命名空间
