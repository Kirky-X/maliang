# Spring Reorder —— 拖拽排序弹簧让位骨架

> Framework 模板。长按拖起列表项后,落点索引逐帧重算,其余项各自以弹簧动画错峰让位到新槽位;松手落定。被拖项只跟手(无过渡),其余项才开过渡。MOTION_INTENSITY 3-7 适用(见 [`dials.md`](../meta/dials.md))。

## 视觉效果

```mermaid
flowchart TD
  A["长按 → 项浮起(scale 1.04 + 阴影)"] --> B["拖动跟手,关闭该项目的 transition"]
  B --> C["每帧计算中心点落入的目标索引"]
  C --> D["数据数组重排 → 其余项 translate 到新槽位(各自 spring)"]
  D --> E["松手 → 被拖项弹落到目标槽位,清阴影"]
```

## HTML 结构

```html
<ul class="reorder-list" id="list">
  <li class="row" data-id="a">A</li>
  <li class="row" data-id="b">B</li>
  <li class="row" data-id="c">C</li>
  <li class="row" data-id="d">D</li>
</ul>
```

## CSS

```css
.reorder-list { position: relative; }
.row {
  height: 56px;                /* 固定行高是槽位计算前提,变高行需实测 rect */
  touch-action: none;
  /* 让位过渡只作用于"非被拖项";被拖项由 JS 加 .dragging 关闭过渡 */
  transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1); /* ease-spring,过冲≤1.2 */
}
.row.dragging {
  transition: none;            /* 跟手,零过渡 */
  z-index: 1;
  box-shadow: 0 8px 24px rgba(0,0,0,.18);
  transform: scale(1.04);
}
```

## GSAP JavaScript

```js
import gsap from 'gsap';

const list = document.getElementById('list');
const rows = [...list.children];
const H = rows[0].offsetHeight;
let drag = null;
let order = rows.map((_, i) => i);          // order[槽位] = 元素下标

function slotOf(el) { return order.indexOf(rows.indexOf(el)); }

rows.forEach((row) => {
  row.addEventListener('pointerdown', (e) => {
    drag = { row, sy: e.clientY, oy: gsap.getProperty(row, 'y') };
    row.classList.add('dragging');
    row.setPointerCapture(e.pointerId);
  });
});

list.addEventListener('pointermove', (e) => {
  if (!drag) return;
  const dy = e.clientY - drag.sy;
  gsap.set(drag.row, { y: drag.oy + dy });               // 被拖项:直接跟手
  const center = drag.row.offsetTop + dy + H / 2;
  const target = Math.max(0, Math.min(rows.length - 1, Math.floor(center / H)));
  if (target !== slotOf(drag.row)) {                      // 落点索引变化才重排
    const from = slotOf(drag.row);
    order.splice(from, 1);
    order.splice(target, 0, rows.indexOf(drag.row));
    rows.forEach((r) => {                                 // 其余项:spring 让位
      if (r === drag.row) return;
      gsap.to(r, { y: (slotOf(r) - rows.indexOf(r)) * H,
        duration: 0.3, ease: 'back.out(1.2)', overwrite: 'auto' });
    });
  }
});

list.addEventListener('pointerup', () => {
  if (!drag) return;
  const { row } = drag;
  row.classList.remove('dragging');                       // 恢复过渡后落位
  gsap.to(row, { y: (slotOf(row) - rows.indexOf(row)) * H,
    duration: 0.3, ease: 'back.out(1.2)',
    onComplete: () => commitOrder() });
  drag = null;
});

function commitOrder() { /* 按 order 持久化排序;DOM 归零 translate */ }
```

## 强制规则

- **必须**实现 `prefers-reduced-motion` 降级:让位无动画直接换位(见 [`accessibility.md`](../meta/accessibility.md) 第 2 节)
- 被拖项 `transition: none` 纯跟手;**只改数据槽位**,让位项才开过渡(两端同时过渡是抖动根源)
- 让位统一用 `ease-spring`(过冲 ≤ 1.2,见 [`micro-interactions.md`](../vocabulary/micro-interactions.md) 缓动库),`overwrite: 'auto'` 防止叠加。**近似边界**:`cubic-bezier(0.34, 1.56, 0.64, 1)` 是预烘焙近似弹簧,仅适用于让位项——目标是槽位、一次性过渡、用户不会再抓住它;若列表项可被中途再拖起(可中断场景),CSS 过渡无法抓取反转,该项落定改走 [`interruptible-motion.md`](interruptible-motion.md) 的 JS 弹簧两参数模型(damping + response)
- 行高一致用 `index * H` 计算;变高列表改为逐项实测 rect
- 松手落定后必须 `commitOrder` 归零 translate 并同步 DOM 顺序,二次拖拽前状态必须干净
- 重排/换父的 DOM 搬运用 `parent.moveBefore(node, ref)` 原子移动(Chrome 133+/Edge 133+/Firefox 144+,Safari 不支持):iframe 不重载、CSS 动画不重启、输入焦点不丢——append/insertBefore 实为拆除+插入,三者全丢;Web Components 走 `connectedMoveCallback`;探测 `'moveBefore' in Element.prototype` 回退传统移动并接受状态重置(行为侧「节点复用禁销毁重建」与 [pro-motion.md](../vocabulary/pro-motion.md) `card-layout-morph` / `list-vt-reflow` 同源)
- 触觉反馈:进入新槽位时 vibration ≤ 10ms(见 [`micro-interactions.md`](../vocabulary/micro-interactions.md) `micro-haptic`)
- 邻居让位传播(吸收自交互演示批):被拖项插入点附近的邻居按指数衰减位移依次让位,nudge(n) = 10px x 0.7^n(网格 8px),delay(n) = 24ms x n 错峰;松手弹簧回位与重排一次完成;错峰在单档 80ms 口径内(24ms 起步累加,封顶 5 层)

## 失败模式

| 触发条件 | 处理 |
| --- | --- |
| 列表抖动振荡 | 被拖项也开了过渡;确认 `.dragging { transition: none }` 生效 |
| 让位滞后一拍 | 落点索引只在越界时重算一次的写法漏帧;改为每帧计算+仅变化时重排 |
| 长列表错位 | 行高不一仍用 `index * H`;改用实测 offsetTop |
| 快速甩动丢让位 | 让位 tween 未 `overwrite`,多个 tween 叠加;加 `overwrite: 'auto'` |
| 移动端拖不动页面反而滚了 | 行缺 `touch-action: none` |
| 松手后二次拖拽从旧位置起 | 未归零 translate 就重排 DOM;落定回调里 commit 并清 transform |
