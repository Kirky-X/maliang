# Sticky Stack —— 粘性堆叠 GSAP 骨架

> Framework 模板。滚动时章节依次堆叠(sticky),新章节从下方覆盖旧章节,旧章节按比例缩小 / 变暗。来源:taste-skill。MOTION_INTENSITY ≥ 7 适用(见 [`dials.md`](../../meta/dials.md))。

## 视觉效果

```
滚动开始 → 第一章节 sticky
  ↓
第二章节从下方滑入,覆盖第一章节
  ↓
第一章节同时缩小(scale 0.95)+ 变暗(opacity 0.5)
  ↓
重复,直到最后一章
```

## HTML 结构

```html
<section class="stack-container">
  <div class="stack-card" data-index="0">第一章</div>
  <div class="stack-card" data-index="1">第二章</div>
  <div class="stack-card" data-index="2">第三章</div>
  <div class="stack-card" data-index="3">第四章</div>
</section>
```

## CSS

```css
.stack-container {
  position: relative;
  height: 400vh; /* 4 张卡 → 4 倍视口高度 */
}
.stack-card {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-primary);
  will-change: transform, opacity; /* Hardware Accel,见 performance.md */
}
```

## GSAP JavaScript

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const cards = document.querySelectorAll('.stack-card');
const total = cards.length;

cards.forEach((card, index) => {
  if (index === total - 1) return; // 最后一张不缩小

  gsap.to(card, {
    scale: 0.95,
    opacity: 0.5,
    ease: 'none',
    scrollTrigger: {
      trigger: cards[index + 1],
      start: 'top bottom',
      end: 'top top',
      scrub: 1,
    },
  });
});

// reduced-motion 降级(强制,见 accessibility.md)
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (prefersReducedMotion.matches) {
  ScrollTrigger.getAll().forEach(trigger => trigger.kill());
  gsap.set(cards, { scale: 1, opacity: 1, clearProps: 'all' });
}
```

## 强制规则

- **必须**实现 `prefers-reduced-motion` 降级(见 [`accessibility.md`](../../meta/accessibility.md) 第 2 节)
- **必须**用 `transform` + `opacity`,不用 `top` / `margin`(见 [`performance.md`](../../meta/performance.md) Hardware Accel)
- **必须**用 `ScrollTrigger.scrub` 而非 scroll 事件监听
- 卡片数量 ≤ 5 张(超过性能下降)
- `will-change` 在动画期间设,ScrollTrigger `onLeave` 时清除

## 失败模式

| 触发条件                  | 处理                                       |
| ------------------------- | ------------------------------------------ |
| Safari sticky 兼容性      | 加 `-webkit-sticky`                        |
| 移动端 scroll 不流畅      | 加 `ScrollTrigger.config({ ignoreMobileResize: true })` |
| 卡片闪烁                  | 检查 `will-change` 是否设置                |
| reduced-motion 下仍触发   | 在 ScrollTrigger 注册前判断并 kill         |
