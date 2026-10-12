# H8 · 模型分栏（Mockup Split, Browser-Framed）

> 左侧标题，右侧装进浏览器框的产品截图，倾斜 1-3° 添生气。卖 Web 应用且有干净截图时的标准解。

## 名称与形状

两栏 hero：文案左、模型右。模型 = 顶栏 chrome（三枚圆点）+ 截图体，整体轻微旋转。框样式可换：浏览器 chrome / macOS 工具栏 / 极简发丝线 / 无框浮起。截图按 [visual-assets.md](../meta/visual-assets.md) 必须是真实产品捕获，禁假 UI 拼贴。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 框样式 | 浏览器 chrome · macOS 工具栏 · 极简发丝线 · 无框浮起 |
| 倾角 | 0° · 1.5° · 3° |
| 截图数 | 单张 · 三张堆叠 · 三张环绕 |

## 何时用与勿混淆

- **何时用**：卖 Web 应用、手里有一张干净明亮的真截图。
- **勿混淆**：[H7 演示视频裁边](h7-demo-video-clipped-by-viewport-edge.md)（会动的视频且溢出视口）；[H2 左右双联](h2-split-diptych.md)（右侧是摄影/证明栏，非产品模型）。

## DOM+CSS 骨架

```html
<section class="hero-mock">
  <div><h1>…</h1><p>按 <kbd>⌘ M</kbd> 随时唤起。</p></div>
  <figure class="mock">
    <header class="mock__chrome"><span></span><span></span><span></span></header>
    <div class="mock__body"><!-- 真截图或 CSS 手建模型 --></div>
  </figure>
</section>
```

```css
.hero-mock { display: grid; grid-template-columns: 1fr 1.2fr;
  gap: var(--space-2xl); align-items: center; }
.mock { transform: rotate(1.5deg); border-radius: 12px; overflow: hidden;
  box-shadow: 0 24px 60px -20px oklch(20% 0.02 60 / 0.18); }
.mock__chrome { display: flex; gap: 6px; padding: 10px 12px;
  background: var(--color-paper-2); border-block-end: 1px solid var(--color-rule); }
```

折叠要点：<60rem **撤倾斜**、塌单栏、模型落到文案下方全宽；<40rem 标注钉合并、编号图例移到模型下方。

## 反模式

- 倾斜 + 裁边 + 浮影三层特效全开——每个原型只做自己的那件事；叠满读作特效合集（见 [polish-craft.md](../meta/polish-craft.md) 克制纪律）。
- 截图是画出来的假界面——禁；真截不了就换 [H9 手绘插画](h9-custom-illustration-centerpiece.md) 并明示插画身份。
- 跨产出照抄同组旋钮值（同框样式 + 同倾角）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H8 · Mockup Split）。
