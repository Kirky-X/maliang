# H5 手机专属页容器契约（H5 Frame）

> 目的：**页面只活在手机上**（H5 / 活动页 / 小程序页 / app UI 原型 / 移动端商详 / 报告 H5）时，先立容器再谈设计——视口契约、locked-body 架构、safe-area 数学、拇指区层级、原生家具是约定而非设计机会。与 [`../meta/mobile-floor.md`](../meta/mobile-floor.md) 分工：那个管"桌面页到手机上为什么坏"，本文件管"没有桌面形态的页怎么立起来"。
>
> 来源：Adapted from finesse-ui h5-mobile（github.com/mouse-lin/finesse-skill，MIT License），2026-09 吸收。内容语法（brand/product/commerce）照常从模板墙取，本契约是容器层，包裹它们而非替代。

## 判定

页面**只会**在手机上被打开、且以全屏自包含形式传播（分享卡片 / 扫码 / 内嵌 webview）→ 本契约。普通响应式页面（有桌面形态）→ 不用，走常规响应式 + [`../meta/mobile-floor.md`](../meta/mobile-floor.md)。

## 四层盒子（唯一的骨架）

```html
<body>                    <!-- locked;永不滚动;桌面端是深色包围 -->
  <div class="phone">     <!-- 视口:手机上 100%,桌面上带框 406px -->
    <div class="status">  <!-- 仿 OS 状态栏 flex:none -->
    <div id="app">        <!-- 唯一滚动容器 flex:1; overflow-y:auto -->
    <nav class="tabbar">  <!-- absolute 底部锚定,高于滚动层 -->
    <div class="sheet">   <!-- absolute,translateY(102%) 待命 -->
    <div class="home-ind"><!-- Home 指示条 -->
  </div>
</body>
```

**`body { overflow: hidden }` + `#app { overflow-y: auto }` 就是全部架构**，与其他所有 register 相反。一次买到三件事：状态栏与 TabBar 不靠 `position: fixed` 也钉得稳（iOS Safari 收缩 chrome 里 fixed 不可靠）；橡皮筋回弹被限制在 `#app` 内；bottom sheet 可以相对 `.phone` absolute 而不必和文档流搏斗。

多 tab 变体（app shell 形态）：每个 tab 独立滚动容器 `.view`（同一架构，锁 body 滚子元素）——买到的是**切走再切回滚动位置还在**，原生行为；底部 padding 规则必须应用到每一个 `.view`（漏掉第三个 tab 是经典半吊子修复）。

## 视口契约（原样抄）

```html
<meta name="viewport"
      content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=1, user-scalable=no">
<meta name="theme-color" content="#3f95dd">
```

- `viewport-fit=cover` 让 `env(safe-area-inset-*)` 返回真实数值——没有它 safe-area 全部静默变 `0px`，内容钻进刘海底下。
- `maximum-scale=1, user-scalable=no` 防双击缩放破坏固定框感。**唯一例外**：文字型阅读页（文章/长文官网）删掉这两项——从需要捏合缩放的人手里夺走能力，而纯滚动页没有固定框收益可保护。
- `theme-color` 把浏览器 chrome 染成页面色。

```css
* { box-sizing: border-box; margin: 0; padding: 0;
    -webkit-tap-highlight-color: transparent; }   /* 杀灰闪 */
html, body { height: 100%; overflow-x: clip; }
body { overflow: hidden; background: #08090b;      /* 桌面包围色 */
       display: flex; align-items: center; justify-content: center; }
.phone { position: relative; width: 100%; height: 100%; overflow: hidden;
         display: flex; flex-direction: column; }
#app { flex: 1; overflow-y: auto; overflow-x: clip;
       padding-bottom: calc(env(safe-area-inset-bottom) + 108px); }  /* 让开 TabBar */
#app::-webkit-scrollbar { width: 0; }              /* 手机里的滚动条就是穿帮 */
```

高度用 `100%` 不用 `100dvh`：`.phone` 高度已被 flex 父级约束，`dvh` 在 iOS chrome 收缩时付出 reflow 代价零收益。**dvh 是滚动型移动页的正确答案，固定框内的错误答案。**

## 桌面手机框（H5 页唯一的响应式规则）

```css
@media (min-width: 560px) {
  body { background: radial-gradient(120% 90% at 50% 0%, #16181d 0%, #08090b 62%); }
  .phone { width: 406px; height: min(880px, 94vh);
           border-radius: 46px;
           border: 1px solid rgba(255,255,255,.1);
           box-shadow: 0 46px 120px -30px rgba(0,0,0,.9),   /* 落影 */
                       0 0 0 10px #0b0c0e;                  /* 边框环:纯 spread 无模糊,零布局成本 */
  }
}
```

- 边框环（第二个 shadow）按页面色调染色：暗页近黑、奶油页 `#2a2622` 暖炭、粉彩页白。
- 包围 `radial-gradient` 用**页面色板的去饱和近亲**，禁止中性灰——灰读起来像未样式的截图。
- `min(880px, 94vh)`：写死 844px 在 13 寸笔记本上底栏出屏。

## Safe-area 与拇指 —— 两条硬约束

**`env()` 到处用，永远包在 `calc()` 里**：

```css
padding: calc(env(safe-area-inset-top) + 12px) 16px calc(env(safe-area-inset-bottom) + 16px);
height: calc(56px + env(safe-area-inset-bottom));   /* TabBar 总高含 home indicator 区 */
```

**拇指区反转页面**：手机是拇指操作，主操作放**底部**（TabBar / 吸底操作栏 / 底部 sheet / FAB），顶部留给状态与导航——与桌面"右上角是主 CTA"完全相反。破坏性操作放拇指区外侧（顶部），防误触。

**触控规则（桌面没有的）**：点击目标 ≥ 44×44px；`touch-action` 显式声明（横滑页 `pan-y`）；监听 `pointercancel`（来电/手势抢走指针）；滚动容器 `passive: true` 的 scroll 监听；表单 `font-size ≥ 16px` 防 iOS 聚焦自动放大。

## 六种形态（morphology）

| 形态 | 内容 | 骨架 |
| --- | --- | --- |
| **A · App shell** | tabs / 列表 / 详情 / 设置 | 状态栏 + `#app`（多 `.view`） + TabBar；四 tab 上限 |
| **B · Paged deck 活动页** | 一次一屏一信息，上下翻 | `scroll-snap` y 强制 + 全屏 section + 吸底 CTA |
| **C · Snap narrative 数据报告** | 年度总结式，数字大字 + 图表逐屏 | snap 翻页 + 每屏一个数字主角 |
| **D · Commerce stack 移动商详** | 图集 + 价格 + SKU + 吸底购买栏 | 原生商详纵(stack)结构；购买栏常驻拇指区 |
| **E · Longform site 移动官网** | 长滚动 + 章节导航 | 纯滚动（放行捏合缩放）；无 TabBar |
| **F · Ambient screen 氛围屏** | 天气 / 海报 / 单一目的 | 单屏 + 微动效；无滚动 |

选形态 = 选骨架；内容语法（brand/product/commerce）从模板墙取，由形态包裹。

## 原生家具（convention，不是设计机会）

| 家具 | 关键规则 |
| --- | --- |
| Bottom sheet | `translateY(102%)` 待命 → 0 打开；档位/速度判关/背景三件套见 [`../vocabulary/sheet-drawer.md`](../vocabulary/sheet-drawer.md)；相对 `.phone` absolute |
| TabBar | ≤ 5 项；`env(safe-area-inset-bottom)` 垫底；当前项图标+标签同变，不只变色 |
| Home indicator | 独立元素绘制，勿依赖系统；叠在 TabBar padding 区内 |
| Push 转场 | 新页 `translateX(100%)→0`，旧页 `-30%` 视差 + 变暗；返回反向；`prefers-reduced-motion` 降为淡入 |
| FLIP 缩放转场 | 缩略图→详情大图走 [`../motion-skeletons/shared-element.md`](../motion-skeletons/shared-element.md) |
| Toast / 下拉刷新 | toast 顶部安全区下；下拉刷新阻尼见 [`../vocabulary/scroll.md`](../vocabulary/scroll.md) `scroll-overscroll-damp` |

## H5 廉价清单（自检）

- [ ] 桌面打开是带框手机而不是拉伸全屏
- [ ] 刘海/safe-area 真机实测内容不被遮
- [ ] 无 iOS 聚焦自动放大（输入 16px+）
- [ ] 点击无灰色闪块（tap-highlight 已清）
- [ ] TabBar 不随滚动位移；sheet 打开时 body 不滚
- [ ] 转场有 reduced-motion 降级
- [ ] 375px 与 414px 都过 [`../meta/mobile-floor.md`](../meta/mobile-floor.md) 出厂自检
