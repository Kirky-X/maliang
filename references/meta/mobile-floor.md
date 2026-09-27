# 移动端机械地板（Mobile Floor）

> 目的：一个在桌面端精致的页面，到手机上坏掉的原因几乎总是这六条**机械原因**，每条可检测、可修复。`preview-checklist.md` 问"手机上坏没坏"，本文件回答"为什么坏、怎么修"。H5 手机专属页（无桌面形态）另见 [`../dimensions/h5-frame.md`](../dimensions/h5-frame.md)，那是容器契约，不是故障修复。
> 六条机械原因之外，本文件另覆盖两层桌面测不出的真机议题：浏览器 chrome 取色一致性与真机验证（见文末两节）。
>
> 来源：Adapted from finesse-ui mobile-floor（github.com/mouse-lin/finesse-skill，MIT License），2026-09 吸收；「浏览器 chrome 取色」与「真机验证」两节吸收自 mobile-native（emilkowalski/skills，MIT），2026-09。

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

## M7 · 输入控件字号地板 `16px`

`< 16px` 的输入框在真机聚焦时 iOS Safari 会整页强制放大（桌面复现不了，见真机验证表「聚焦缩放」行）。修因不禁果：**不许**用 viewport `maximum-scale=1 / user-scalable=no` 来「修」（永不禁缩放，2026-09 裁决，见 [`../dimensions/h5-frame.md`](../dimensions/h5-frame.md) 视口契约），把字号提到 16px 即根除。

```css
input, textarea, select { font-size: 16px; }
```

## 浏览器 chrome 取色一致性（theme-color 双 scheme）

> 来源：mobile-native（emilkowalski/skills，MIT），2026-09 吸收。

手机浏览器把页面顶部背景色延伸到地址栏 / 状态栏，取错色会出现"页面与浏览器 chrome 两张皮"。四条决策：

1. **取色对象是页面顶部背景色，不是品牌色**——chrome 与页面无缝衔接，品牌色由页面内容表达；
2. **亮暗双 scheme 各配一色**，用 `media` 拆成两条 meta，跟随系统切换：

```html
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff">
<meta name="theme-color" media="(prefers-color-scheme: dark)"  content="#111318">
```

3. **同时声明 `color-scheme`**，告知浏览器两种形态都被设计过（滚动条、表单控件、`env()` 按当前 scheme 渲染，防暗色下闪白控件）：

```css
:root { color-scheme: light dark; }
```

4. **class 切主题（手动 toggle，非跟随系统）时必须 JS 同步更新 meta**——`media` 拆分只跟随系统，手动切换后地址栏不会自己变：

```js
// 手动切主题:更新受控 meta 的 content;与 media 双 meta 二选一作为真源,防两套真源打架
document.querySelector('meta[name="theme-color"]')
  ?.setAttribute('content', isDark ? '#111318' : '#ffffff');
```

PWA 的 `manifest.theme_color` 与 `<meta name="theme-color">` 是**同一决策**，改一处必须同步另一处。

## 真机验证 —— 模拟环境不可信的八项

> 来源：mobile-native + frontend-design-practicalswan，2026-09 吸收。检查条目归 [`preview-checklist.md`](../commands/preview-checklist.md) §5.15，本节回答"为什么模拟环境测不出"。

| 真机才暴露 | 为什么模拟环境测不出 |
| ---------- | -------------------- |
| 粘滞 hover | 桌面鼠标移开即失 hover；触屏 tap 后 hover 态**粘住**，直到点别处才消失 |
| tap 高亮 | 模拟点击不触发 tap-highlight；真机闪灰色块（未有意设置时） |
| URL 栏吃视口 | 桌面视口固定；真机地址栏收展改变可用高度，`100vh` 元素被截断 |
| 聚焦缩放 | 桌面无缩放；真机聚焦 < 16px 输入框时整页强制放大 |
| overscroll | 桌面无回弹 / 下拉刷新；真机根层被下拉刷新劫持或内层回弹连带整页 |
| safe-area | 模拟外壳是图片；真机刘海 / 手势条真实遮挡导航与按钮 |
| 软键盘 | 模拟环境键盘不真正挤压视口；真机键盘遮挡焦点输入框 |
| PWA standalone | 模拟环境无"添加到主屏"；standalone 形态缺地址栏后导航可能不可用 |

调试路径（USB / `0.0.0.0` 监听 + LAN IP、iOS Safari「开发」菜单、Android `chrome://inspect`、旧手机当测试机）见 preview-checklist §5.15，不在此复制。

## 出厂自检

- [ ] 375px 视口无横向滚动条（`document.documentElement.scrollWidth <= innerWidth`）
- [ ] sticky 导航滚动全程存活（M1 修复后实测）
- [ ] 每个含图网格在 320px 宽度不爆（M2）
- [ ] 最长按钮文案（真实文案，非"按钮"）能折行不裁切（M3）
- [ ] 最长标题（真实数据）不溢出（M4）
- [ ] 页面上所有 sticky 列出 top 值，无重复 0（M5）
- [ ] 全大写标题 line-height ≥ 1.0（M6）
- [ ] 所有 input/textarea/select 字号 ≥ 16px，viewport 无 maximum-scale/user-scalable 禁缩放写法（M7 + 视口契约）
- [ ] 亮暗双 scheme 下地址栏色与页面顶部背景一致，`color-scheme` 已声明（chrome 取色节）
- [ ] 上表八项在至少一台实体设备过一遍（真机验证节）
