# H2 · 左右双联（Split Diptych）

> 左侧标题 + 导语，右侧图片或产品实证，6/6 或 7/5 分栏。每条主张都配得上一个视觉证据时才用它。

## 名称与形状

两栏 hero：文案栏（标题、导语、一个次级动作）与实证栏（照片 / 证明栏 / 拉引言）并置，栏间以发丝线、负空间或竖线分隔。注意这是 maliang [首屏骨架表](../vocabulary/hero.md) 的「左右分栏」——一轮最多一个方向使用，且方向卡必须写明「为什么非它不可」。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 栏比 | 7/5 · 6/6 · 5/7 |
| 右栏内容 | 照片 · 证明栏 · 拉引言 |
| 分隔 | 发丝线 · 负空间 · 竖线 |

## 何时用与勿混淆

- **何时用**：每条主张都能配一个视觉证明；产品页、案例页。
- **勿混淆**：[H6 摄影满版](h6-photographic-fold.md)（图满版不配对）；[H8 模型分栏](h8-mockup-split-browser-framed.md)（右侧是产品截图模型，不是摄影/证明栏）。

## DOM+CSS 骨架

```html
<section class="hero-split">
  <div><h1>…</h1><p>…</p><a class="cta-outline">…</a></div>
  <figure><img src="" alt="" /></figure>
</section>
```

```css
.hero-split { display: grid; grid-template-columns: 7fr 5fr;
  gap: var(--space-2xl); align-items: center; }
@media (max-width: 60rem) { .hero-split { grid-template-columns: 1fr; } }
```

折叠要点：<60rem 塌单栏（文案在上、实证栏在下），分隔退化为两者之间的一条发丝线；<40rem 实证栏内条目收成两列紧凑网格。

## 反模式

- 右侧放装在卡片里的产品界面截图——[首屏骨架表](../vocabulary/hero.md) 明令：另一侧必须是跨越结构的图像、色块或图形装置。
- 左右等宽 + 居中对齐 + 双按钮的默认组合照抄上一次构建：栏比是旋钮，跨产出照抄同值 = 同款，至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H2 · Split Diptych）。
