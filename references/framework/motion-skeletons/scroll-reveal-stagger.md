# Scroll Reveal Stagger —— 滚动揭示交错 GSAP 骨架

> Framework 模板。元素进入视口时按顺序揭示(stagger),最常用的滚动动画。来源:taste-skill。MOTION_INTENSITY 4-10 适用(见 [`dials.md`](../../meta/dials.md))。是 design-md 默认推荐动效。

## 视觉效果

```
元素初始:opacity 0 + translateY(20px)
  ↓
进入视口(80% 可见)
  ↓
依次(每个间隔 80ms)过渡到 opacity 1 + translateY(0)
```

## HTML 结构

```html
<section class="reveal-section">
  <h2 class="reveal">标题</h2>
  <p class="reveal">第一段</p>
  <p class="reveal">第二段</p>
  <ul>
    <li class="reveal">列表项 1</li>
    <li class="reveal">列表项 2</li>
    <li class="reveal">列表项 3</li>
  </ul>
</section>
```

## CSS(初始态)

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  will-change: transform, opacity;
}
/* reduced-motion 下:初始态取消 */
@media (prefers-reduced-motion: reduce) {
  .reveal {
    opacity: 1;
    transform: none;
    will-change: auto;
  }
}
```

## GSAP JavaScript

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const revealElements = document.querySelectorAll('.reveal');

const staggerReveal = gsap.utils.toArray('.reveal-section').forEach(section => {
  const items = section.querySelectorAll('.reveal');
  gsap.to(items, {
    opacity: 1,
    y: 0,
    duration: 0.5,
    stagger: 0.08,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: section,
      start: 'top 80%',
      once: true, // 只触发一次,避免来回滚动反复动画
    },
  });
});

// reduced-motion 降级(强制)
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (prefersReducedMotion.matches) {
  ScrollTrigger.getAll().forEach(trigger => trigger.kill());
  gsap.set('.reveal', { opacity: 1, y: 0, clearProps: 'all' });
}
```

## 进阶:不同方向揭示

```js
// 自定义方向:用 data-reveal-direction
const directions = {
  up: 'translateY(20px)',
  down: 'translateY(-20px)',
  left: 'translateX(-20px)',
  right: 'translateX(20px)',
  scale: 'scale(0.95)',
};

document.querySelectorAll('[data-reveal-direction]').forEach(el => {
  const dir = el.dataset.revealDirection;
  el.style.transform = directions[dir] || directions.up;
});
```

## 进阶:IntersectionObserver 替代方案

不引入 GSAP 时,用原生 IntersectionObserver(更轻量,适合 Level 4-5):

```js
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('revealed');
        }, index * 80); // stagger
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 }
);

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}
.reveal.revealed {
  opacity: 1;
  transform: translateY(0);
}
```

## 强制规则

- **必须**实现 `prefers-reduced-motion` 降级(直接显示)
- **必须**用 `transform` + `opacity`,不用 `top` / `margin`
- **必须**用 `ScrollTrigger.once: true` 或 `observer.unobserve`,避免反复触发
- `translateY` 偏移 ≤ 30px(超过易引起眩晕,违反无障碍)
- `stagger` 间隔 ≤ 120ms(超过显得拖沓)
- `duration` ≤ 600ms
- 同屏揭示元素 ≤ 8 个(超过性能下降)

## 失败模式

| 触发条件                  | 处理                                       |
| ------------------------- | ------------------------------------------ |
| 元素初始态可见(未应用 CSS)| 检查 CSS 加载顺序,JS 在 CSS 之后          |
| reduced-motion 下元素消失 | CSS 用 `@media` 兜底,JS 不依赖动画可用    |
| stagger 看起来跳跃        | 检查 `ease` 是否设置(`power2.out` 推荐) |
| 元素闪烁                  | 检查 `will-change` 是否设置                |
| 长列表性能差              | 改用 IntersectionObserver,移除 GSAP       |
