# Ft8 · 跑马灯滚动页脚（Marquee Scroll）

> 一条无限横滚行：标语与分隔符反复（`工作室 · 2026 · 工作室 · 2026 ·`）。运动系、宣言系品牌的页脚。

## 名称与形状

一条通栏横滚 track（`animation: 32s linear infinite`），内容复制两份实现无缝循环；视觉隐藏的静态文本给辅助技术。动态是它的全部存在理由——静态文本堆一排不是本原型。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 速度 | 24s · 32s · 48s |
| 方向 | 向左 · 向右 · 交替（罕用） |
| 分隔符形 | 中点 · 长破折 · 斜线 |

## 何时用与勿混淆

- **何时用**：品牌声音响亮、运动感强——运动题材、时装 lookbook、品牌向代理。
- **勿混淆**：[Ft4 密集版权页](ft4-dense-typographic.md)（静态文本）；[H1 跑马灯宣言](h1-marquee.md)（hero 静态巨字，不滚动——同页两处「跑马灯」只允许本原型动态滚动）。

## DOM+CSS 骨架

```html
<footer class="foot-marquee" aria-label="页脚">
  <div class="track" aria-hidden="true">
    <span>工作室 · 2026 · 工作室 · 2026 · </span>
    <span>工作室 · 2026 · 工作室 · 2026 · </span>
  </div>
  <p class="visually-hidden">工作室 · 2026 · MIT 许可</p>
</footer>
```

```css
.foot-marquee { overflow: hidden; border-top: 2px solid var(--color-ink); }
.foot-marquee .track { display: flex; gap: var(--space-2xl);
  white-space: nowrap; padding-block: var(--space-md);
  animation: foot-marquee 32s linear infinite; }
@keyframes foot-marquee { to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .foot-marquee .track { animation: none; } }
```

折叠要点：<60rem 已为窄屏设计；速度放慢约 25%；<40rem 速度再放慢、track 高度降一档。

## 反模式

- 编辑/安静语境用跑马灯——运动在安静页面读作吵闹；与 [motion-skeletons](../motion-skeletons/) 的降级纪律一致：`prefers-reduced-motion: reduce` 必须停滚（上述 CSS 已内建）。
- track 内容只复制一份——循环会跳变；必须两份 + `translateX(-50%)`。
- 写页脚标记前未声明轮换：「上一构建页脚：X。本构建：Y，因为 Z」；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id Ft8 · Marquee Scroll）。
