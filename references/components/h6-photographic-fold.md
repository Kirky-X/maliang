# H6 · 摄影满版（Photographic Fold）

> 一张满版真图占满视口，说明文字落在角上。图的分量必须配得上满版。

## 名称与形状

整节就是一张图：`object-fit: cover` 铺满 80dvh，说明文字绝对定位在一角，像照片的图注。无叠加渐变、无卡片区。

## 变体旋钮

| 旋钮 | 可选值（逐旋钮取一值，写入构建盖章） |
| --- | --- |
| 图区 | 满版 · 16/7 · 4/3 · 1/1 方形 |
| 图注位置 | 左下 · 右上 · 边栏 |
| 文字关系 | 图下 · 叠加图上 |

## 何时用与勿混淆

- **何时用**：手里有真摄影素材，画质与构图撑得起满版；空间/实体/旅行/人物题材。
- **勿混淆**：[H2 左右双联](h2-split-diptych.md)（图与文配对成栏）；[H9 手绘插画](h9-custom-illustration-centerpiece.md)（画出来的，不是拍出来的）。

## DOM+CSS 骨架

```html
<section class="hero-photo">
  <img class="bleed" src="" alt="" />
  <p class="caption">2026 年春。</p>
</section>
```

```css
.hero-photo { position: relative; height: 80dvh; }
.hero-photo .bleed { width: 100%; height: 100%; object-fit: cover; }
.hero-photo .caption { position: absolute; bottom: var(--space-md); right: var(--space-md); }
```

折叠要点：<60rem 图保持满版、图注从绝对角落改为图下方行内；<40rem 图注字号降一档，角落图注在任何手机视口都不得压到正文。

## 反模式

- 假图顶替：无真实摄影就用渐变/假 3D 渲染凑满版——违反 [visual-assets.md](../meta/visual-assets.md) 诚实占位口径；给不出真图就换纯文字构图（「或缺席」是合法解）。
- 图上压字不加任何保护、或加深色遮罩压死照片层次——文字可读性按 [color.md](../dimensions/color.md) 对比度门实测。
- 跨产出照抄同组旋钮值（同图区 + 同图注位）= 同款；复用至少换一个旋钮并盖章声明。

## 来源

来源：hallmark components cookbook 改写，2026-10 吸收（原型 id H6 · Photographic Fold）。
