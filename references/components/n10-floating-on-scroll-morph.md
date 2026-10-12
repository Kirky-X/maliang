# N10 · 滚动形变浮窗导航（Floating-on-scroll Morph）

> 顶部粘性栏在滚过阈值后**形变为浮动药丸**。两种视觉模式共用一个 DOM—— cookbook 里最考验功力的导航：四条铁律缺一，形变就读作坏。

## 名称与形状

一个 `<header>` 内外两层：外层 `.nav` 持有「落地栏」视觉，内层 `.nav__inner` 持有「药丸」视觉；滚过阈值切一次 `.is-floating`，所有共享属性交叉淡变。落点配方（四铁律、属性形变表、滚动处理器全文）见 hallmark floating-nav 原文，此处收其骨架。

**四条铁律（简化记）**：①总高恒定（两态 padding 互补，页面不跳）；②位移只用 `transform: translateY()`，禁 margin/padding；③每个共享视觉属性（background / border / backdrop-filter / box-shadow）两态都要显式中性化并进 transition 列表；④全部属性共用一条时长与曲线（~520ms，`cubic-bezier(0.16, 1, 0.3, 1)`）。`backdrop-filter` 两态写 `blur(0)` 不写 `none`（`none` 不参与过渡）。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 触发阈值 | 60px · 80px（≥60 防微滚动抖动） |
| 曲线 | 520ms 单曲线（唯一推荐值——多曲线即八段动画） |
| 目标形态 | 继承 N5 三旋钮（宽/底衬/锚点） |

## 何时用与勿混淆

- **何时用**：氛围/modern-minimal 页面，且这个动态微时刻配得上它的复杂度——一处克制的惊喜。
- **勿混淆**：[N5 浮动药丸](n5-floating-pill.md)（恒为药丸、无滚动行为）；N10 是 N5 加一个会形变过去的落地栏态。

## DOM+CSS 骨架

```html
<header class="nav">
  <div class="nav__inner">
    <a class="wordmark">工作室</a>
    <ul class="nav__links">…</ul>
  </div>
</header>
```

```css
.nav { position: sticky; top: 0; padding-block: 0; background: var(--bar-bg);
  backdrop-filter: saturate(1.4) blur(14px); transition: all 520ms cubic-bezier(0.16,1,0.3,1); }
.nav.is-floating { background: transparent; border-block-end-color: transparent;
  backdrop-filter: blur(0); padding-block: var(--space-2xs); }
.nav.is-floating .nav__inner { max-width: 58rem; border-radius: 999px;
  background: var(--pill-bg); backdrop-filter: blur(18px);
  transform: translateY(12px); box-shadow: 0 8px 24px -12px oklch(0% 0 0 / 0.2); }
```

滚动处理器要点：`{ passive: true }` + rAF 节流 + 布尔翻转守卫（每次状态变化只切一次类，不随每个滚动事件切换）。

折叠要点：<40rem 禁滚动形变（横切规则 7）；窄屏塌缩沿用 N5 降级路径——字标左、汉堡右，两态共用同一套窄屏样式。

## 反模式

- 两个 `<header>` 用 opacity 对切——DOM 翻倍、焦点序错乱、内容失同步；只许单 DOM 交叉淡变。
- 形变中总高变化——内容抖动是本模式最致命的单点错误（铁律 ①）。
- 阈值设 0（一滚就变）——抖动；≥60px。写导航标记前声明：「上一构建导航：X。本构建：Y，因为 Z」（总则 2）；跨产出照抄同组旋钮值 = 同款，复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id N10 · Floating-on-scroll Morph；四铁律出自 hallmark floating-nav 配方）。
