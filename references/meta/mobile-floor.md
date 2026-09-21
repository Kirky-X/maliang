# 移动端机械地板（Mobile Floor）

> 目的：一个在桌面端精致的页面，到手机上坏掉的原因几乎总是这六条**机械原因**，每条可检测、可修复。`preview-checklist.md` 问"手机上坏没坏"，本文件回答"为什么坏、怎么修"。H5 手机专属页（无桌面形态）另见 [`../dimensions/h5-frame.md`](../dimensions/h5-frame.md)，那是容器契约，不是故障修复。
>
> 来源：Adapted from finesse-ui mobile-floor（github.com/mouse-lin/finesse-skill，MIT License），2026-09 吸收。

## M1 · 根级 `overflow-x: clip` —— 用 `clip`，永远不用 `hidden`

横向溢出要在**根/包裹层**裁掉，但 `overflow-x: hidden` 会在元素上创建滚动容器，**杀死 `position: sticky` 导航**（sticky 相对最近的滚动容器定位，容器不滚 = sticky 失效）。

```css
html, body { overflow-x: clip; }   /* clip: 裁剪但不产生滚动容器,sticky 存活 */
```

- `overflow: clip` 浏览器基线已足够（2022+ 全绿）；确需兼容老 WebView 时才降级 `hidden` 并接受 sticky 损失、改用 fixed 导航。

## M2 · 含图网格轨道必须 `minmax(0, 1fr)`

Grid 轨道默认 `minmax(auto, 1fr)`，`auto` 最小值取内容固有宽度——**一张大图会把轨道撑破视口**，两列布局横向爆开。

```css
.grid-2col { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
.grid-2col img { width: 100%; height: auto; display: block; }
```

## M3 · 可点击文字必须能在**任意宽度**下换行

按钮/链接文字是移动端最高频的组件级断裂：容器变窄、文字不下折、撑破或截断。

```css
.btn-label { overflow-wrap: anywhere; }  /* 不够宽时允许在任意字符处折行 */
```

- 同时给按钮 `min-height`（触控 44px 地板）而非固定 height，折两行时不裁切。

## M4 · Display 大标题必须 `overflow-wrap: anywhere; min-width: 0`

超长单词/URL/无空格 CJK 长串在大字号下必然溢出视口；flex/grid 子项还需要 `min-width: 0` 才允许收缩到内容以下。

```css
.display-heading { overflow-wrap: anywhere; min-width: 0; }
```

## M5 · `top: 0` 的 sticky 全页只留一个

两个元素都 `position: sticky; top: 0` 时互相推挤，后者把前者顶出视口——表现为"导航滚着滚着没了"。堆叠 sticky（导航 + 子标题栏）用**递增 top 值**：

```css
.nav { position: sticky; top: 0; z-index: 10; }
.subbar { position: sticky; top: var(--nav-h); z-index: 9; }  /* 接力,不重叠 */
```

## M6 · 全大写 display 标题的 `line-height` 地板是 `1.0`

品牌正文可用 0.86-0.95 的紧行高，但**全大写**的字形更高（无降部留白），`< 1.0` 会裁掉字形或上下行互相咬合。

```css
.caps-display { text-transform: uppercase; line-height: 1.0; }  /* 地板 1.0,推荐 1.05 */
```

## 出厂自检

- [ ] 375px 视口无横向滚动条（`document.documentElement.scrollWidth <= innerWidth`）
- [ ] sticky 导航滚动全程存活（M1 修复后实测）
- [ ] 每个含图网格在 320px 宽度不爆（M2）
- [ ] 最长按钮文案（真实文案，非"按钮"）能折行不裁切（M3）
- [ ] 最长标题（真实数据）不溢出（M4）
- [ ] 页面上所有 sticky 列出 top 值，无重复 0（M5）
- [ ] 全大写标题 line-height ≥ 1.0（M6）
