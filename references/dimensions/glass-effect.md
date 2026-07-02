# Apple Liquid Glass Web Approximation —— 玻璃质感 Web 实现(基础配方)

> 维度规范(基础配方)。Apple iOS 26 / macOS 26 引入的 Liquid Glass 设计语言,本文件提供基于 `backdrop-filter` 的**基础近似配方**(模糊 + 饱和,无真实折射)。
> 需要真实折射/光线弯折感的进阶实现(SVG feDisplacementMap + WebGL 双引擎)见 [`glass-advanced.md`](./glass-advanced.md)。来源:taste-skill。

**使用前提**:`backdrop-filter` 性能开销大,移动 Safari 表现差。必须遵守 [`performance.md`](../meta/performance.md) 与 [`accessibility.md`](../meta/accessibility.md) 的降级要求。

## 1. 基础配方

四个必备层 + 一个可选层:

| 层          | 实现                                  | 作用                       |
| ----------- | ------------------------------------- | -------------------------- |
| backdrop    | `backdrop-filter: blur(20px) saturate(180%)` | 模糊 + 饱和度提升,模拟折射 |
| 内 border   | `border: 1px solid rgba(255,255,255,0.1)` | 模拟玻璃边缘高光           |
| 内 shadow   | `box-shadow: inset 0 1px 0 rgba(255,255,255,0.15)` | 顶部内高光                 |
| 外 shadow   | `box-shadow: 0 8px 32px rgba(0,0,0,0.1)` | 提升层级感                 |
| (可选)光泽  | `::before` 伪元素 + 渐变 + opacity     | 模拟玻璃顶部反射           |

## 2. 完整 CSS 代码

```css
.glass {
  /* 基础层:半透明背景 + 模糊 */
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%); /* Safari */

  /* 内边框:1px 模拟玻璃边缘 */
  border: 1px solid rgba(255, 255, 255, 0.1);

  /* 内阴影:顶部内高光 */
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.15),  /* 内顶高光 */
    inset 0 -1px 0 rgba(255, 255, 255, 0.05),  /* 内底微光 */
    0 8px 32px rgba(0, 0, 0, 0.1);             /* 外阴影提升层级 */

  /* 圆角:玻璃感需要较大圆角 */
  border-radius: 16px;
}

/* 可选:顶部光泽层 */
.glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0) 50%
  );
  pointer-events: none;
  z-index: 1;
}
```

## 3. 暗色模式适配

暗色模式下,玻璃背景应使用深色半透明 + 边缘高光提升:

```css
@media (prefers-color-scheme: dark) {
  .glass {
    background: rgba(30, 30, 32, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.1),
      inset 0 -1px 0 rgba(255, 255, 255, 0.03),
      0 8px 32px rgba(0, 0, 0, 0.4);
  }

  .glass::before {
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.08) 0%,
      rgba(255, 255, 255, 0) 50%
    );
  }
}
```

## 4. 降级:`prefers-reduced-transparency`

用户开启"减少透明度"时,必须降级为不透明背景(见 [`accessibility.md`](../meta/accessibility.md) 第 4 节):

```css
@media (prefers-reduced-transparency: reduce) {
  .glass {
    background: var(--color-bg-primary);  /* 不透明替代 */
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    border: 1px solid var(--color-border-default);
  }

  .glass::before {
    display: none;
  }
}
```

## 5. 多层叠加

真实 Liquid Glass 由多层玻璃叠加产生深度。Web 近似用 2 层:

```html
<div class="glass-stack">
  <div class="glass glass-back"><!-- 背层玻璃 --></div>
  <div class="glass glass-front"><!-- 前层玻璃,稍小,圆角稍小 --></div>
</div>
```

```css
.glass-stack {
  position: relative;
}
.glass-back {
  position: absolute;
  inset: 0;
  opacity: 0.7;  /* 背层稍透 */
}
.glass-front {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.7);  /* 前层更不透 */
  border-radius: 12px;  /* 前层圆角稍小,露背层边缘 */
}
```

## 6. 使用场景与禁止场景

### 推荐场景

- 顶部 sticky 导航栏(内容滚动时透出背景)
- 浮动 dock / 工具栏
- Modal / Drawer 的遮罩层(替代纯黑 rgba(0,0,0,0.5))
- 卡片悬浮于复杂背景之上(图片 / 视频 / 渐变)

### 禁止场景

- **禁止**:大面积全屏玻璃背景 → paint 开销大,见 [`performance.md`](../meta/performance.md) DOM Cost
- **禁止**:文字直接放玻璃上不测对比度 → 玻璃下的背景不可控,必须用 [`accessibility.md`](../meta/accessibility.md) 的 AA 阈值
- **禁止**:多个玻璃元素深度叠加(> 3 层)→ backdrop-filter 嵌套性能急剧下降
- **禁止**:玻璃作为信息密集表格的背景 → 文字与底层内容混合可读性差

## 7. 性能预算

| 指标                       | 阈值                            |
| -------------------------- | ------------------------------- |
| 单页 `backdrop-filter` 元素 | ≤ 3 个                          |
| blur 半径                  | ≤ 30px(移动端 ≤ 20px)         |
| 玻璃元素面积               | ≤ 50% 视口                      |
| 嵌套层级                   | ≤ 2 层                          |
| 滚动时 backdrop-filter     | 禁用(改为静态背景)           |

超过预算时,改为静态半透明背景 `rgba()` + 阴影,放弃折射感。

## 8. 浏览器兼容

| 浏览器             | 支持情况                                              |
| ------------------ | ----------------------------------------------------- |
| Chrome / Edge 76+  | 完全支持                                               |
| Firefox 103+       | 支持(需 `layout.css.backdrop-filter.enabled`)       |
| Safari 9+          | 需要 `-webkit-` 前缀                                  |
| Samsung Internet   | 支持                                                  |
| 老 IE / 老 Android | 不支持,降级为静态 `rgba()` 背景                      |

降级:`@supports not (backdrop-filter: blur(20px)) { .glass { background: rgba(255,255,255,0.9); } }`。

## 与其他文档的关系

- **真实折射/物理参数模型**见 [`glass-advanced.md`](./glass-advanced.md)(SVG + WebGL 双引擎,本文件为基础配方的进阶升级路径)
- 性能约束见 [`performance.md`](../meta/performance.md) 第 3 节 DOM Cost
- 无障碍降级见 [`accessibility.md`](../meta/accessibility.md) 第 4 节 prefers-reduced-transparency
- 暗色模式规则见 [`color.md`](./color.md) 第 5 节
- z-index 取值见 [`token.md`](../meta/token.md) z-index category
