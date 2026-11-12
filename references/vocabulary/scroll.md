# 滚动模式命名词汇

> 模式词汇库。滚动是页面交互的基础,本表标准化滚动相关动效与行为命名。

## 命名表

| 模式名                  | 视觉特征                                        | 适用场景                              |
| ----------------------- | ----------------------------------------------- | ------------------------------------- |
| `scroll-native`         | 原生滚动,无干预                                | 默认,大多数页面                      |
| `scroll-smooth`         | `scroll-behavior: smooth`                       | 锚点跳转、回到顶部                    |
| `scroll-infinite`       | 滚动到底自动加载(增强:距底约一屏即提前加载,底部 3 圆点依次跳动,新卡逐张错峰接续) | Feed 流、列表、社交社区               |
| `scroll-reveal-stagger-step` | 依次浮现参数档:露出视口约 15% 才触发,自下方约 40px 淡入上浮,同行错峰约 70ms 像发牌,落位轻回弹;卡内图片 1.08→1 缩回 | 卡片列表/网格(挂 [`motion-skeletons/scroll-reveal-stagger.md`](../motion-skeletons/scroll-reveal-stagger.md) 骨架,本行给触发与错峰量化值) |
| `scroll-pull-refresh`   | 下拉刷新                                        | 移动 App、Feed                        |
| `scroll-snap`           | 滚动吸附(横向 / 纵向)                         | 轮播、Tab 切换、全屏叙事              |
| `scroll-parallax`       | 多层视差(背景 / 中景 / 前景速率不同;分层参考 0.2/0.4/0.7/1.2 倍,近景可快于页面;配每帧追剩余距离约 12% 的平滑跟随+停手惯性滑行);R2 原生路线 view-timeline + animation-timeline,`@supports` 必含 `(animation-range: entry)` 过滤部分支持浏览器,禁 scroll-timeline-polyfill(功能不全) | 品牌叙事、产品发布                    |
| `scroll-pinned`         | 元素 pin 在视口(配合 sticky-stack 骨架)        | 章节堆叠、产品功能展示                |
| `scroll-horizontal`     | 垂直滚动驱动横向位移(配合 horizontal-pan 骨架) | 品牌站、作品集、时间线                |
| `scroll-reveal`         | 进入视口揭示(配合 scroll-reveal-stagger 骨架);离场段对称:出视口缩退/淡出用单 view() 时间线 `animation-range: entry, exit` 双区间(fill backwards/forwards),可逆随滚动回放,降级 IO 多档阈值按 intersectionRatio 插值 | 默认推荐,主流消费 App                |
| `scroll-progress`       | 顶部 / 侧边进度条                               | 长文章、教程、流程页                  |
| `scroll-driven-anim`    | 滚动驱动动画(数字 / 图表)                     | 数据展示、产品发布                    |
| `scroll-virtualized`    | 长列表虚拟滚动                                  | 表格 > 100 行、IM 消息列表            |
| `scroll-scrub-bind`     | 动画进度绑定滚动位置(scrub):可逆,停住时动画停在对应进度 | 滚动叙事、大标题折叠(配合 `nav-large-title-collapse`) |
| `scroll-velocity-blur`  | 甩动方向性模糊:滚动越快内容沿运动方向模糊越明显,停止立刻恢复清晰 | 媒体墙、高速 Feed(MOTION ≥ 8)        |
| `scroll-center-focus`   | 中心聚焦放大:靠近屏幕中心的内容放大,离开缩小,建立视觉焦点 | 轮播、卡片流(配合 `scroll-snap`)      |
| `scroll-depth-layers`   | 景深分层滚动:三层内容不同滚动速度/模糊半径/亮度,全由滚动进度驱动 | 品牌叙事首屏(MOTION ≥ 7)             |
| `scroll-overscroll-damp` | 边缘阻尼:列表到顶继续拉越拉越沉拉不穿,松手弹回;顶图随下拉放大 | 移动 App 原生质感(下拉刷新前传)      |
| `scroll-dual-column-parallax` | 双列异速视差:左右两列同向上滚但速度不同成视差,到底两列对齐收尾 | 图文对照、编辑式长文(与 `scroll-parallax` 互见:彼条同区块多层景深,本条双列异速) |
| `scroll-sticky-date-rail` | 日期轨吸附:左窄栏大号日期滚动吸附顶部,被下一天日期从下方推上替换 | 时间线/日志/日程流(与 `scroll-pinned` 互见:彼条静态钉住,本条钉住+推上替换) |
| `scroll-new-content-pill` | 新内容胶囊:新动态从顶部滑下小胶囊提示不打断,点击回顶后新内容逐条插入 | 社交 Feed、协作动态(与 `scroll-infinite` 互见:彼条底部追加,本条顶部插入) |
| `scroll-pan-2d`         | 双向平移面:`scroll-axis-lock: none` 解锁斜向平移(嵌套单轴面板自动保留锁轴),`overscroll-behavior: contain` 防链滚与横滑返回误触;容器 tabindex+键盘可平移;降级 `touch-action: pinch-zoom` + wheel/pointer 直写 scrollLeft/scrollTop(禁 transform) | 地图、缩放图片、无限画布/节点图(配合 [layout.md](layout.md) `layout-canvas`) |
| `scroll-await-settle`   | 滚动完成再触发:await scrollIntoView/scrollTo 的 Promise(Chrome/Edge 150+),完成后再高亮/移焦;被打断 resolve 不 reject,操作 ID 防旧回调;`focus({preventScroll:true})` 防二次滚动;不支持时 await undefined 立即续行(装饰性可接受)或 scrollend+100ms idle 兜底 | 锚点跳转后高亮目标、搜索定位后移焦 |
| `scroll-snap-preview`   | 吸附实时预亮:手势中 `scrollsnapchanging` 预亮 pending 目标(轻 class 切换),`scrollsnapchange` 落定转正 + aria-current;初始加载一次几何对齐(容器须 offsetParent);降级 scroll + rAF 最近距离 + scrollend/100ms 兜底 | 轮播缩略图预亮、全屏叙事指示点(与 `scroll-snap` 磁吸互见) |
| `scroll-snap-sync`      | 吸附落定同步:落定事件 `snapTargetBlock/Inline` 驱动 TOC/侧栏高亮(aria-current="location");mandatory snap 长内容禁用(中段不可达);锚点目标 tabindex="-1" 可接焦;降级 IO threshold 0.9 取顶部可见 | 长文 TOC 高亮、章节-侧栏同步(与 `scroll-snap-preview` 同事件族互见) |
| `scroll-load-anchor`    | 初始滚动锚点:`scroll-initial-target: nearest` 渲染即定位,CSS-only 布局期瞬时无动画;优先级 URL fragment > scroll-start > 本属性;媒体给 aspect-ratio 防定位漂移;不动键盘焦点需手动 focus;降级 DOMContentLoaded + scrollIntoView instant | 日历开场定位今日、Feed 定位精选项 |
| `scroll-aware-float`    | 滚动态感知浮钮:`@container scroll-state(scrollable: top)` 纯 CSS 判滚过首屏才显回顶/FAB(visibility/opacity/translate ≤400ms);不支持时默认常显(勿默认隐藏致永不可见);内容底部预留 padding 防遮末项;降级 IO 顶部 sentinel | 回顶按钮、悬浮 CTA(与 [navigation.md](navigation.md) `nav-floating-pill` 互见) |
| `scroll-edge-hint`      | 边缘可滚暗示:端部渐变阴影(sticky 伪元素 0.75rem 阴影,opacity .2s)或内容渐隐(mask,`@property` 注册 3rem 防跳变),由 scroll-state(scrollable) 显隐、到端自消;横滑用渐隐、竖滚用阴影;RTL 翻转;scroll-padding ≥ fade 宽防吸附落渐隐内 | 横滑 tabs/chips/轮播、弹窗内滚动区、固定头尾表格(与「露下一屏一角」规则互补) |
| `scroll-stuck-style`    | 吸顶变样式:`@container scroll-state(stuck: top)` 纯 CSS 判吸顶瞬间换底色/阴影/压缩(容器必须命名防嵌套碰撞,样式只作用于子代);吸顶改盒模型须 sticky 直接父级 `overflow-anchor: none` 防抖振;scroll-padding-top ≥ header 高;降级 IO rootMargin -1px | 长列表分组标题吸顶、TOC 吸顶、表头吸顶变实底(与 [tables.md](tables.md) `table-sticky-header` 互见) |
| `scroll-pull-reveal`    | 下拉露控件:搜索栏/筛选藏首屏上方,`scroll-initial-target: nearest` 定主内容于首位 + `scroll-snap-type: y mandatory` 保证全显/全隐不悬停半途;必须配 ≥24×24 等效按钮(WCAG 2.5.1 路径手势);降级 scrollIntoView instant block:start | 移动 Feed 顶部藏搜索栏/筛选(与 `scroll-pull-refresh` 分界:彼条触发刷新,本条露出控件) |

> `scroll-overscroll-damp` 顶图拉伸变体:图片按下拉距离放大(scale ≤ 1.15)+文字淡出+松手阻尼回弹。

## 使用规则

- MOTION_INTENSITY ≥ 7 才能用 `scroll-parallax` / `scroll-pinned` / `scroll-horizontal`(见 [`dials.md`](../meta/dials.md))
- 所有非原生滚动必须实现 `prefers-reduced-motion` 降级到 `scroll-native`(见 [`accessibility.md`](../meta/accessibility.md))
- `scroll-infinite` 必须有 loading skeleton 与"已加载全部"终止态
- `scroll-virtualized` 用于列表 > 100 项,见 [`performance.md`](../meta/performance.md) DOM Cost
- 单页滚动模式 ≤ 2 种组合(如 `scroll-reveal` + `scroll-progress`)
- 内容可滚要可见暗示:视图边缘露出一截下一屏内容,表示"还有更多";截断得刚刚好的视口让人以为已经到底
- 同轴滚动容器禁嵌套(滚动区套滚动区抢滚轮);异轴(纵向页面 × 横向表格)可以

## 在 draw-md 中的写法

```markdown
## Scroll Behavior
- mode: scroll-reveal
- reveal: { pattern: scroll-reveal-stagger, direction: up, stagger: 80ms }
- progress: scroll-progress (top, 4px height, color: color-brand)
- reduced_motion_fallback: scroll-native
```
