# 纹理与印刷质感 —— 有预算的处理,不是氛围

> 维度层。纹理(grain / halftone / 套印 / 扫描线 / 纸边)是**一种带预算的处理**:一页一个纹理族、透明度 token 化、永不动画、永不拦输入。散得到处都是的颗粒是 tic;来自本文件、落在挣得它的主题上的颗粒是手艺。由主题按亲和表挣得,或自定义 lineage 为印刷向时加载;主题未点名纹理时整节不适用。

## 预算(每条都要绑)

- **一页一个纹理族。** 颗粒 / 半调 / 套印错位 / 扫描线 / 纸边,永不两种同页。risograph 印刷算一个族:它的颗粒与套印错位来自同一个滚筒。半调若是照片的处理层,属于图像不算页面。
- **透明度 token 化,写进 token 块**:`--texture-opacity` 全页 ≤ **0.08**,限定在一张卡或一块版 ≤ **0.15**;正文文字下方 ≤ **0.05** 或干脆没有。低频洗色(baseFrequency ≤ 0.02:纤维、纸色)是着色不是斑点,全页可到 0.12,但对比度按合成后的结果实测。
- **永不动画。** 没有飘动的颗粒,没有脉动的网点。
- **每个覆盖层 `pointer-events: none` + `aria-hidden="true"`**——纹理永不拦截输入;复古信号是氛围,不是画一个显示器边框。
- **性能**:纯 CSS 或 data-URI SVG filter;纹理零图片请求。

## 1 · 颗粒(纸)

斑点颗粒,token 化:

```css
:root { --texture-opacity: 0.08; }
.grained { position: relative; isolation: isolate; }
.grained::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 1;
  background-size: 200px 200px; opacity: var(--texture-opacity);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 -4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
}
```

颜色矩阵把噪声变成离散斑点(alpha = 噪声 ×9 −4),颗粒在 1x 下清晰可读;未处理的 `feTurbulence` 在这些透明度下是一层没人看得见的雾。暗底上斑点必须亮:把矩阵前三行改成 `0 0 0 0 1` 让每个斑点变白,透明度不变。一块版、一张强调卡,或挣得颗粒的整页 ≤0.08。

## 2 · 网点(半调)

照片处理用半调:`background-image` 用同一 filter 家族,`baseFrequency` 降到网点可辨(0.15-0.35 按图像尺寸),叠加在图像容器上、算图像的账不算页面的账。正文区永不叠。

## 3 · 套印错位(两版印刷)

文字或色版的"没对准":主层正常渲染,复制层同内容偏移 1-2px、单色(强调色或纸色)、`opacity` 用预算。只用于 display 级标题或版画感图形,正文禁用——套印在小字号上直接伤可读性。

## 4 · 扫描线 / 纸边

扫描线:`repeating-linear-gradient` 1-2px 周期,预算内透明度,只压在图像或版块上。纸边(deckle):容器 mask 或不规则 border-image,属于容器不算纹理族配额之外的账,但同页仍不得出现第二种族。

## 自检(交付前逐项过)

- [ ] 本页纹理族 = 1;risograph 的颗粒+套印算一族
- [ ] `--texture-opacity` 在 token 块声明,数值在预算内(全页 ≤0.08 / 卡 ≤0.15 / 正文下 ≤0.05)
- [ ] 纹理层全部 `pointer-events: none` + `aria-hidden="true"`
- [ ] 零动画、零图片请求(纯 CSS / data-URI SVG)
- [ ] 暗底斑点亮色矩阵已核对;低频洗色的合成对比度已实测
- [ ] `prefers-reduced-motion` 不适用(纹理不动),但若纹理随任何入场动效出现,动效降级后纹理保持静态在场
