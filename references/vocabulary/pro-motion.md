# 专业动效组件模式命名词汇

> 模式词汇库。专业级交互动效组件 8 组:3D 倾斜流光、胶囊流体形变、共享元素展开、磁吸游标码表、速度锚点抽屉、光晕边框、弹簧交错流、按压超调反馈。来源:UI 交互教学视频截图提取(2026-10,8 组组件及 AI 描述词原文,见下文对照;同源前篇 2026-09-22 即 number-motion / sheet-drawer)。与 [ROUTING](../motion-skeletons/ROUTING.md)(选型)、[micro-interactions.md](micro-interactions.md)(时长预算)互补——`chart-magnet-cursor` 等 3 组已有实现,本篇只做命名收编与挂接,不重复实现。

## 命名表

| 模式名 | 视频组件 | 视觉特征 | 适用场景 |
| --- | --- | --- | --- |
| `card-tilt-glare` | 3D倾斜光影面板 Tilt Glare | 卡片随触摸/悬停位置做 3D 透视倾斜,径向反射流光跟随触点,松手 Spring 阻尼回正 | 商品卡、会员卡、封面卡(触摸版;hover 层深版见 [buttons.md](buttons.md) `card-tilt-depth`) |
| `capsule-fluid-morph` | 流体胶囊形变 Fluid Morph | 胶囊按钮长成弹窗面板:位置/尺寸/圆角走高阻尼流体曲线无缝插值,全程同一元素不拆两个 | 筛选胶囊展开、工具胶囊变面板(FLIP 实现见 [shared-element.md](../motion-skeletons/shared-element.md)) |
| `shared-element-expand` | 共享元素无缝展开 Shared Element | 列表小图与详情大图视为同一元素,背景与容器连续平滑缩放 | 卡片→详情页转场(已有实现:FLIP 骨架 [shared-element.md](../motion-skeletons/shared-element.md) + [sheet-drawer.md](sheet-drawer.md) `sheet-grow-into-page`) |
| `chart-magnet-cursor` | 磁吸游标与滚动码表 Snap Odometer | 折线图横滑自动吸附最近数据点,顶部数值滚动计数器实时平滑联动 | 移动端时序图浏览(已有实现:[charts.md](charts.md) `chart-magnet-cursor` + [number-motion.md](number-motion.md) `num-ticker-partial`) |
| `sheet-velocity-anchor` | 阻尼弹性抽屉 Bottom Sheet | 底部抽屉橡皮筋跟手,松手按滑动速度投射目标档位吸附,非只取最近静态档 | 多档位底部抽屉(组合语义:[sheet-drawer.md](sheet-drawer.md) `sheet-velocity-dismiss` + `sheet-notch-snap`,速度投射见 [gesture-arbitration.md](../motion-skeletons/gesture-arbitration.md)) |
| `border-conic-glow` | 动态弥散光晕边框 Conic Glow | conic 渐变描边绕卡片旋转,底部一层呼吸弥散背光同步晕染 | 强调卡、AI 生成内容卡、状态高亮卡 |
| `stagger-spring-cascade` | 物理弹簧交错流 Stagger Cascade | 列表项按固定间隔依次入场,每项带微弱弹性过冲向上滑入 | 列表/图墙首屏入场(spring 变体;ease-out 基准版见 [scroll-reveal-stagger.md](../motion-skeletons/scroll-reveal-stagger.md)) |
| `press-scale-overshoot` | 弹性微缩触觉反馈 Press Scale | 按压弹性压缩 + 深度内阴影,释放轻微超调回弹 | 主操作按钮、卡片按压(增强档;强制基线见 [micro-interactions.md](micro-interactions.md) `micro-press-scale`) |

## AI 描述词对照

> 视频给出的 8 组提示词原文;落成 maliang 产物时按使用规则换算成模式参数,不整段照抄进 draw-md。

| # | 组件 | AI 描述词 |
| --- | --- | --- |
| 01 | 3D倾斜光影面板 | 为 Card 添加跟随触摸位置的 3D 透视倾斜与径向反射流光,松手带 Spring 阻尼回正。 |
| 02 | 流体胶囊形变 | 实现胶囊按钮向弹窗面板的流体形态变换,尺寸与圆角采用高阻尼流体曲线(Fluid Morph)无缝过渡。 |
| 03 | 共享元素无缝展开 | 实现 Card 到详情页的共享元素转场(Shared Element Transition),背景与 Card 容器做连续平滑缩放。 |
| 04 | 磁吸游标与滚动码表 | 折线图横向滑动带数据点磁吸吸附,顶部数值使用滚动计数器(Odometer / Ticker)实时平滑联动。 |
| 05 | 阻尼弹性抽屉 | 实现支持阻尼橡皮筋回弹的底部抽屉(Bottom Sheet),松手根据手势滑动速度(Velocity)自动计算吸附锚点。 |
| 06 | 动态弥散光晕边框 | 为 Card 添加旋转渐变描边(Conic Gradient Border),底部附带动态模糊的呼吸弥散背光。 |
| 07 | 物理弹簧交错流 | 列表元素入场使用交错动画(Stagger Delay),每个子项带微弱弹性向上滑入(Spring Cascade)。 |
| 08 | 弹性微缩触觉反馈 | 按钮按压添加 scale(0.96) 物理弹性压缩与深度内阴影,释放时触发轻微超调回弹(Spring Overshoot)。 |

## 使用规则

- 路线选择:`card-tilt-glare` / `border-conic-glow` / `press-scale-overshoot` 走 R1(CSS transition / 弹簧曲线);`capsule-fluid-morph` / `shared-element-expand` 走 FLIP(见 ROUTING §2 R3);手势驱动的 `card-tilt-glare` / `sheet-velocity-anchor` 必须把 pointer 速度传入弹簧模型(见 [interruptible-motion.md](../motion-skeletons/interruptible-motion.md)),禁止 easing 伪装回弹(见 ROUTING §5)
- `card-tilt-glare`:倾角 ≤ ±9°(与 `card-tilt-depth` 对齐),透视深度 600-1000px;流光是 radial-gradient 叠加层,只动 `transform` 与层内坐标;触屏禁在滚动中触发(手势仲裁,见 [gesture-arbitration.md](../motion-skeletons/gesture-arbitration.md))
- `card-tilt-glare` 与 hover 驱动的 `card-tilt-depth` 按 `(hover: hover) and (pointer: fine)` 探测分派:桌面交付 hover 层深版,触摸交付本篇触摸版,二者不并存
- `capsule-fluid-morph`:只过渡 `transform` 与 `border-radius`,禁改 `width/height/top/left`(见 [performance.md](../meta/performance.md));「高阻尼」= 低过冲弹簧(过冲 ≤ 2%),起止形态差大时保持中途圆角连续
- `sheet-velocity-anchor`:松手用「当前位移 + 速度 × 投射系数」估目标档位再吸附,替代静态最近档;距离/速度双阈值沿用 `sheet-velocity-dismiss`,档位 ≤ 3 沿用 `sheet-notch-snap`
- `border-conic-glow`:旋转用超尺寸伪元素整层 `transform: rotate`(conic-gradient 画在伪元素上),禁动画角度自定义属性(逐帧重绘);背光呼吸只动 `opacity`,blur 半径静态预设;呼吸周期 2-4s,计一拍氛围档(见 ROUTING §3.10 与 [`../meta/dials.md`](../meta/dials.md))
- `stagger-spring-cascade`:间隔 ≤ 120ms、单项 duration ≤ 600ms、过冲 ≤ 1.02(「微弱弹性」上限,超过即卡通感);其余沿用 scroll-reveal-stagger 骨架强制规则
- `press-scale-overshoot`:基线仍为 `micro-press-scale`(scale 0.97,100-160ms 按压档);本篇增强档(scale 0.96)仅限主操作按钮,压缩与内阴影必须同时给——内阴影是深度语义,缺了就只是缩小;释放超调用 cubic-bezier(.34,1.56,.64,1) 近似(见 [buttons.md](buttons.md) `btn-spring`),逐帧跟指针才上真弹簧(ROUTING §3.8)
- 全部 8 组必须给 `prefers-reduced-motion` 静止终态:倾斜/旋转/呼吸停在构图帧,FLIP 直接切换(见 ROUTING §1 GATE 与 [accessibility.md](../meta/accessibility.md))

## 在 draw-md 中的写法

```markdown
## Card (product-hero)
- pattern: card-tilt-glare
- tilt: ±9deg, perspective: 800px, glare: radial-follow, release: spring-damped
- fine_pointer_fallback: card-tilt-depth

## Sheet (setup-panel)
- pattern: sheet-velocity-anchor
- notches: [50vh, 90vh], project: velocity, rubber_band: true, backdrop: sheet-backdrop-triplet

## Card (ai-highlight)
- pattern: border-conic-glow
- rotate: 4s linear infinite, glow_breathe: 3s, reduced_motion: static-frame

## List (spots-grid)
- pattern: stagger-spring-cascade
- stagger: 100ms, duration: 500ms, overshoot: 1.02, direction: up
```
