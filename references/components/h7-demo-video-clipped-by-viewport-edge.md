# H7 · 演示视频裁边（Demo Video Clipped-by-viewport-edge）

> 左侧 display 标题，右侧演示视频，最右 10-20% 刻意溢出视口被裁掉。裁切即设计——暗示「产品比屏幕装得下」。

## 名称与形状

两栏 hero：文案左、真机演示视频右，视频容器宽度超出右缘（`width: calc(100% + 12vw)`），被视口裁切而非缩进框里。Linear 首创，Vercel / Resend / Cursor 精化。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 裁切侧 | 右 · 左 · 两侧 |
| 宽高比 | 16/10 · 16/9 · 4/3 |
| 边框 | 发丝线 · 浏览器 chrome · 无框 |

## 何时用与勿混淆

- **何时用**：SaaS / 开发工具 / 仪表盘题材，且手里有产品真实录像（或手建 CSS 模型）。视频属首屏富媒体，落地前过 [performance.md](../meta/performance.md) 视频预算节。
- **勿混淆**：[H4 数字主导](h4-stat-led.md)（数字主导无视频）；[H8 模型分栏](h8-mockup-split-browser-framed.md)（静态截图，不是会动的演示）。

## DOM+CSS 骨架

```html
<section class="hero hero--clipped">
  <div class="hero__copy"><h1>…</h1><p>…</p></div>
  <figure class="hero__media">
    <video autoplay muted loop playsinline preload="metadata"
           poster="/hero-poster.webp">
      <source src="/hero.av1.mp4" type='video/mp4; codecs="av01.0.05M.08"'>
      <source src="/hero.h264.mp4" type="video/mp4">
    </video>
  </figure>
</section>
```

```css
.hero--clipped { display: grid; grid-template-columns: 1fr 1.4fr;
  gap: var(--space-2xl); overflow: visible; }
.hero__media { width: calc(100% + 12vw); aspect-ratio: 16 / 10;
  border-radius: 12px; overflow: hidden; }
@media (max-width: 60rem) { .hero--clipped { grid-template-columns: 1fr; }
  .hero__media { width: 100%; } }
```

折叠要点：<60rem **撤掉裁切**，塌单栏、媒体全宽——375px 上裁切读作坏了而不是设计；<40rem 媒体降为 16/9 并改用 poster 图（蜂窝网络自动播视频是敌意行为，横切规则 9）。

## 反模式

- 编假产品录屏（假数据、假界面）——触发 [ai-tells.md](../meta/ai-tells.md) §10 假产品预览禁令。
- 视频缺 `muted playsinline` 或缺 poster——自动播放策略直接拒播。
- 跨产出照抄同组旋钮值（同裁切侧 + 同边框）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H7 · Demo Video Clipped-Edge）。
