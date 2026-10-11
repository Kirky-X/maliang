# 专业交互组件模式命名词汇

> 模式词汇库。专业级交互组件三节 39 组:移动动效组件 24 组(倾斜流光、流体形变、磁吸码表、面板分层爆炸、堆叠滑动切换、旋钮转盘、滑动确认、拖放吸入、分段进度、透视轮播等)、桌面 Web 交互组件 10 组(滚动钉住叙事、情境光标、磁吸按钮、悬停跟随预览图、圆形扩散换肤等)与形变组件 5 组(搜索框展开、FAB 展开面板、提交状态反馈、图标变形、标签指示条)。来源:专业交互组件视频截图提取(2026-10,含 AI 描述词原文;同源前篇 2026-09-22 即 number-motion / sheet-drawer)。与 [ROUTING](../motion-skeletons/ROUTING.md)(选型)、[micro-interactions.md](micro-interactions.md)(时长预算)互补——`chart-magnet-cursor` 等 12 组已有实现,本篇做命名收编与挂接,不重复实现。

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
| `panel-explode-layers` | 面板分层爆炸视图 Layered Exploded Panel | 长按面板 3D 侧立(X 52° / Z -28°),四层沿 Z 轴等差推出(0/70/140/210),每层错 6 帧;松手弹簧合拢 | 长按检视堆叠详情(长按判定见 [buttons.md](buttons.md) `press-peek`) |
| `card-swipe-deck` | 堆叠滑动切换 Swipe Card Stack | 顶层跟手,旋转 = 横向位移 × 0.06°/px;超宽 35% 松手沿手势甩出,下层 +12px 上移从 0.94 放大到 1 补位,被甩张回底层排队 | 卡组循环切换(挂 [buttons.md](buttons.md) `card-stack-pull` + `card-fling`) |
| `select-gather-stack` | 多选聚成一叠 Multi Select Stack | 长按进多选;拖动时勾中项从各自位置飞向手指,错 3 帧、缩 0.8 倍带 ±8° 旋转聚成一摞,角标计数弹出;松手整摞落进目标 | 相册多选 / 批量操作(多选态见 [buttons.md](buttons.md) `select-mode-shift`) |
| `btn-split-morph` | 按钮一分为二 Split Button Morph | 点击后按钮从中线裂成左右两个,缝 0→16px、内圆角过渡到满圆,文字换暂停 / 结束;点结束沿原路合拢 | 播放 / 计时控制的主操作钮(位置钉死同 `button-submit-morph`) |
| `scroll-mini-player` | 滚动变小窗 Scroll to Mini Player | 列表滚动距离归一化 0→1 单值驱动:视频宽 470→200、位置顶部→右下角,播放不中断;过阈值吸附角落,点击沿同一路径放大还原 | 列表页视频 / 音频常驻小窗(scrub 挂 [scroll.md](scroll.md) `scroll-scrub-bind`) |
| `nav-scroll-spy` | 分类联动滚动 Scroll Spy Category | 右侧列表滚动,按分组标题进入顶部位置计算当前分类,左侧高亮条弹性平移;点击分类右侧平滑滚到分组标题,滚动期间禁反向触发 | 分组菜单 / 目录联动(左导航右列表) |
| `card-flip-to-detail` | 飞出翻面 Flip to Detail | 点击封面飞到屏幕中心放大,绕 Y 轴翻转到背面带轻微回弹;关闭原路返回 | 封面 → 详情背面(挂 [buttons.md](buttons.md) `card-pop-origin` + `card-flip-3d`) |
| `micro-hold-confirm` | 按住蓄力确认 Hold to Confirm | 危险操作长按确认,进度环沿按钮边缘绘制,未满松手平滑回退 | 删除等不可撤销操作(已有实现:[micro-interactions.md](micro-interactions.md) `micro-hold-confirm`) |
| `picker-rotary-knob` | 旋钮转盘 Rotary Knob | 可拖动旋转旋钮,刻度磁吸,中心数值滚动联动 | 温度 / 音量 / 强度类连续调节(挂 [pickers.md](pickers.md)) |
| `picker-before-after` | 前后对比滑块 Before After Slider | 拖动分割线实时裁切两张图,左右两态同位叠加 | 修图对比、方案对比(已有实现:[pickers.md](pickers.md) `picker-before-after`) |
| `picker-radial-arc` | 弧形快捷菜单 Radial Menu | 悬浮钮长按展开弧形菜单,子项交错弹出,滑过放大并显示标签 | 快捷操作(已有实现:[pickers.md](pickers.md) `picker-radial-arc`) |
| `btn-slide-confirm` | 滑动确认 Slide to Confirm | 滑块滑动确认,文字流光扫过,超 80% 触发,不足弹回 | 危险 / 重要操作的滑动确认 |
| `preview-longpress-peek` | 长按浮起预览 Context Preview | 列表项长按上下文预览,背景模糊压暗,选中项浮起,菜单弹簧展开 | 列表快捷预览(已有实现:[sheet-drawer.md](sheet-drawer.md) `preview-longpress-peek`) |
| `drop-target-attract` | 拖到目标吸入 Drop Target | 拖拽靠近时目标放大张开迎候,松手元素缩小吸入 | 文件归档 / 拖放分拣(拖拽弹簧见 [spring-reorder.md](../motion-skeletons/spring-reorder.md)) |
| `progress-segmented` | 分段进度条 Segmented Story Progress | Stories 式分段自动走,按住暂停,点左右半区切上 / 下一项 | 图集浏览、引导页、快看内容流(已有实现:[progress-confirm.md](progress-confirm.md) `progress-segmented`) |
| `gallery-cover-flow` | 景随图换的轮播 Cover Flow | 横向 3D 透视轮播,当前项居中放大,侧卡 ±46° 侧立;切换时背景取当前图模糊混色与标题同步过渡 | 相册 / 目的地浏览(基础轮播见 [galleries.md](galleries.md) `gallery-carousel`) |

## AI 描述词对照

> 视频给出的 24 组提示词原文;落成 maliang 产物时按使用规则换算成模式参数,不整段照抄进 draw-md。

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
| 09 | 面板分层爆炸视图 | 面板分层爆炸视图(Layered Exploded Panel):长按时面板用 perspective 1200px 绕 X 轴转 52 度、绕 Z 轴转 -28 度侧立,四层沿 Z 轴分别推到 0、70、140、210,每层错开 6 帧起步;松手用 cubic-bezier(.34,1.36,.5,1) 弹簧合拢。 |
| 10 | 堆叠滑动切换 | 堆叠滑动切换(Swipe Card Stack):顶层跟手位移,旋转角度等于横向位移乘 0.06 度;位移超过宽度的 35% 松手就沿手势方向甩出屏幕,不就弹回原位;下面两层同步上移 12 并从 0.94 放大到 1,被甩走的那张回到最底层继续排队。 |
| 11 | 多选聚成一叠 | 多选聚拢拖动(Multi Select Stack):长按进入多选,勾中项显示选中标记;开始拖动时,选中项从各自位置飞向手指,每项错开 3 帧,缩到 0.8 倍并带 ±8 度旋转叠成一摞,右上角数量角标弹出;松手整摞落进目标。 |
| 12 | 按钮一分为二 | 按钮分裂形变(Split Button Morph):点击后按钮从中线裂成左右两个,中间的缝用 cubic-bezier(.34,1.36,.5,1) 从 0 撑到 16,内侧圆角过渡到满圆,文字换成暂停和结束;点结束两半沿原路合拢。 |
| 13 | 滚动变小窗 | 滚动触发画中画(Scroll to Mini Player):把列表滚动距离归一化成 0 到 1,视频的宽度从 470 缩到 200、位置从顶部移到右下角,全部写成这个值的函数,播放不中断;滚过阈值后吸附到角落,点击小窗沿同一路径放大还原,列表回到顶部。 |
| 14 | 分类联动滚动 | 左右分类联动(Scroll Spy Category):右侧列表滚动时,按每个分组标题进入顶部的位置计算当前分类,左侧高亮条用 cubic-bezier(.2,.9,.22,1) 平移到对应项;点击左侧分类时右侧平滑滚到该分组标题,滚动期间不反向触发高亮跳动。 |
| 15 | 飞出翻面 | 点击封面触发 3D 翻转弹层(Flip to Detail),元素飞到屏幕中心并放大,绕 Y 轴翻转到背面,带轻微回弹,关闭时原路返回。 |
| 16 | 按住蓄力确认 | 危险操作改为长按确认(Hold to Confirm),按住沿按钮边缘绘制进度环,未满松手平滑回退。 |
| 17 | 旋钮转盘 | 可拖动旋转的旋钮控件(Rotary Knob),刻度磁吸,中心数值滚动联动。 |
| 18 | 前后对比滑块 | 图片前后对比滑块(Before After Slider),拖动分割线实时裁切两张图。 |
| 19 | 弧形快捷菜单 | 悬浮按钮长按展开弧形菜单(Radial Menu),子项交错弹出,滑过放大并显示标签。 |
| 20 | 滑动确认 | 滑动确认组件(Slide to Confirm),文字流光扫过,超过 80% 触发,不足弹回。 |
| 21 | 长按浮起预览 | 列表项长按上下文预览(Context Menu Preview),背景模糊压暗,选中项浮起,菜单弹簧展开。 |
| 22 | 拖到目标吸入 | 拖拽放置目标(Drop Target),靠近时目标放大张开,松手元素缩小吸入。 |
| 23 | 分段进度条 | 分段进度条(Segmented Story Progress),按住暂停,点击左右区域切换。 |
| 24 | 景随图换的轮播 | 横向 3D 透视轮播(Cover Flow),当前项居中放大,切换时背景与标题同步过渡。 |

## 使用规则

- 路线选择:`card-tilt-glare` / `border-conic-glow` / `press-scale-overshoot` 走 R1(CSS transition / 弹簧曲线);`capsule-fluid-morph` / `shared-element-expand` 走 FLIP(见 ROUTING §2 R3);手势驱动的 `card-tilt-glare` / `sheet-velocity-anchor` 必须把 pointer 速度传入弹簧模型(见 [interruptible-motion.md](../motion-skeletons/interruptible-motion.md)),禁止 easing 伪装回弹(见 ROUTING §5)
- `card-tilt-glare`:倾角 ≤ ±9°(与 `card-tilt-depth` 对齐),透视深度 600-1000px;流光是 radial-gradient 叠加层,只动 `transform` 与层内坐标;触屏禁在滚动中触发(手势仲裁,见 [gesture-arbitration.md](../motion-skeletons/gesture-arbitration.md))
- `card-tilt-glare` 与 hover 驱动的 `card-tilt-depth` 按 `(hover: hover) and (pointer: fine)` 探测分派:桌面交付 hover 层深版,触摸交付本篇触摸版,二者不并存
- `capsule-fluid-morph`:只过渡 `transform` 与 `border-radius`,禁改 `width/height/top/left`(见 [performance.md](../meta/performance.md));「高阻尼」= 低过冲弹簧(过冲 ≤ 2%),起止形态差大时保持中途圆角连续
- `sheet-velocity-anchor`:松手用「当前位移 + 速度 × 投射系数」估目标档位再吸附,替代静态最近档;距离/速度双阈值沿用 `sheet-velocity-dismiss`,档位 ≤ 3 沿用 `sheet-notch-snap`
- `border-conic-glow`:旋转用超尺寸伪元素整层 `transform: rotate`(conic-gradient 画在伪元素上),禁动画角度自定义属性(逐帧重绘);背光呼吸只动 `opacity`,blur 半径静态预设;呼吸周期 2-4s,计一拍氛围档(见 ROUTING §3.10 与 [`../meta/dials.md`](../meta/dials.md))
- `stagger-spring-cascade`:间隔 ≤ 120ms、单项 duration ≤ 600ms、过冲 ≤ 1.02(「微弱弹性」上限,超过即卡通感);其余沿用 scroll-reveal-stagger 骨架强制规则
- `press-scale-overshoot`:基线仍为 `micro-press-scale`(scale 0.97,100-160ms 按压档);本篇增强档(scale 0.96)仅限主操作按钮,压缩与内阴影必须同时给——内阴影是深度语义,缺了就只是缩小;释放超调用 cubic-bezier(.34,1.56,.64,1) 近似(见 [buttons.md](buttons.md) `btn-spring`),逐帧跟指针才上真弹簧(ROUTING §3.8)
- 全部 24 组必须给 `prefers-reduced-motion` 静止终态:倾斜/旋转/呼吸停在构图帧,FLIP 直接切换(见 ROUTING §1 GATE 与 [accessibility.md](../meta/accessibility.md))
- `panel-explode-layers`:长按 400ms 判定挂 `press-peek`;层距等差 70px、≤ 4 层;爆炸是瞬时检视态,松手必须合拢回原位(检视不改变布局);合拢曲线与 `press-scale-overshoot` 同源弹簧
- `card-swipe-deck`:甩出判据 = 位移超宽 35% 或速度达标(双判据,见 [gesture-arbitration.md](../motion-skeletons/gesture-arbitration.md));下层补位 +12px / 0.94→1 与顶层甩出同帧;被甩张回队尾循环,页码同步;同屏 ≤ 4 张
- `select-gather-stack`:聚拢每项错 3 帧,缩放 0.8 倍、散转 ±8° 为上限;角标计数随勾选实时增减;松手落进目标后逐项归位回收(从哪里来回哪里去);取消勾选的项不参与聚拢
- `btn-split-morph`:裂缝 0→16px 与文字切换同步;两半钮各自热区 ≥ 44px;全程位置钉死(同 `button-submit-morph` 铁律);结束态两半沿原路合拢,禁淡出重排
- `scroll-mini-player`:全部属性写成归一化进度单值的函数(单驱动,禁多计时器);播放状态跨形变保持(媒体元素不重挂载);两档状态(全宽 / MINI),过阈值吸附;还原走同一路径且列表回顶;reduced-motion 直接跳两态
- `nav-scroll-spy`:当前分类判据 = 分组标题进入顶部;高亮条平移 ≤ 300ms;点击分类平滑滚动到分组标题,滚动期间单向锁(禁 spy 反向触发高亮跳动,滚完再交回);分组 ≤ 9
- `card-flip-to-detail`:飞行放大(位置 / 尺寸)与绕 Y 翻面同一段过渡连续完成,transform-origin 取封面坐标;轻微回弹 = 过冲 ≤ 1.02;关闭沿原路返回(`card-pop-origin` 铁律);背面内容完整可读,禁占位空白
- `micro-hold-confirm`:收编行——判定窗口与进度填充口径全挂 [micro-interactions.md](micro-interactions.md);本行补:进度环沿按钮**边缘**绘制(周描边进度,非中心填充);未满松手进度平滑回退,禁瞬跳清零;必须配不可撤销警示文案
- `picker-rotary-knob`:角度→值线性映射,刻度磁吸整档;中心数值滚动联动(num-ticker);旋转限弧段 ≤ 270°,禁整圈无限旋转(无档位感);松手不停在两档之间
- `picker-before-after`:收编行——分割线跟手实现挂 [pickers.md](pickers.md);本行补:实时裁切用 clip-path inset(只动裁切值,不重绘两张图);分割线热区 ≥ 44px
- `picker-radial-arc`:收编行——按住沿弧弹出 / 滑过放大 / 松手执行挂 [pickers.md](pickers.md);本行补:子项交错弹出错峰 ≤ 40ms/项;弧段 90°·4 项为基准,项数 ≤ 6
- `btn-slide-confirm`:阈值 80%(过了八成才算数),不足弹回且禁停在半途;文字流光 = 背景层位移,只动 transform;确认态锁定后禁再滑;与 `micro-hold-confirm` 分工:hold 适合原地持续按压,slide 适合大按钮 + 明确方向感
- `preview-longpress-peek`:收编行——长按 400ms / 背景压暗虚化 / 三路手势全挂 [sheet-drawer.md](sheet-drawer.md);本行补:菜单弹簧展开过冲 ≤ 1.05,菜单项 ≤ 5
- `drop-target-attract`:靠近判据 = 拖拽元素与目标边缘距离 ≤ 24px;目标张开 ≤ 1.1 倍;松手元素缩小吸入(0.9→0 淡出)目标计数 +1 后回弹落定;目标禁用态不响应张开(误触保护)
- `progress-segmented`:收编行——口径全挂 [progress-confirm.md](progress-confirm.md);本行补:按住暂停即停帧(进度冻结不回退),松手续走;点击左右半区按进度方向就近切换
- `gallery-cover-flow`:侧卡 ±46° 侧立,当前项居中放大 ≤ 1.15 倍;背景从当前图取主色 blur 铺底(混合 37%),切换时背景与标题同帧过渡;同屏卡数 ≤ 7(3D 层数上限)

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

## Panel (camp-detail)
- pattern: panel-explode-layers
- tilt: { x: 52deg, z: -28deg }, layers: 4, gap: 70px, stagger: 6f

## Deck (trip-cards)
- pattern: card-swipe-deck
- rotate: 0.06deg/px, fling: { distance: 35%, velocity: true }, underlift: { y: 12, scale: 0.94→1 }

## Confirm (delete-action)
- pattern: btn-slide-confirm
- threshold: 80%, sheen: text-sweep, under: spring-back

## Drop (sort-target)
- pattern: drop-target-attract
- open: within-24px 1.1x, ingest: shrink-in, count: live
```

## 桌面 Web 交互组件

> 10 个桌面 Web 交互组件,统一来自同一套设计系统演示(ROUE / CARVE),两条跨组件统一纪律随行:①全片同一种回弹力度(一条曲线用到底);②主色只给当前交互的一块。均为指针驱动,交付前先过本节门控。来源:专业交互组件视频截图提取(2026-10,同系列)。

### 命名表

| 模式名 | 视频组件 | 视觉特征 | 适用场景 |
| --- | --- | --- | --- |
| `scroll-sticky-story` | 滚动钉住主图 Sticky Scroll Story | 主图 position: sticky 钉在视口,右侧文字分段滚动;主图缩放与位移随段落进度连续过渡,推近对应部位并亮起主色标记圈 | 产品细节叙事页(scroll-pinned + scroll-scrub-bind 的组合) |
| `cursor-contextual-morph` | 情境光标 Contextual Cursor | 隐藏系统光标,小圆点缓动跟随;悬停图片放大到 88px 填充主色,淡入文字标签,离开平滑缩回 | 图墙 / 作品集的「查看」入口(micro-cursor-custom 的语义化变体) |
| `btn-magnetic-follow` | 磁吸按钮 Magnetic Button | 鼠标进入按钮周围 60px 按偏移倍率跟随,内部图标再叠一层倍率(双层层深);离开弹性回原位 | Hero CTA、圆形图标按钮(micro-interactions Magnetic Button 的参数化命名) |
| `btn-icon-expand` | 图标展开标签 Expanding Icon Button | 圆形图标按钮悬停宽度 48px→自适应文字宽,保持全圆角;标签延迟 80ms 淡入,相邻按钮同步让位 | 工具排、标注工具条 |
| `nav-hover-pill` | 导航悬停指示块 Sliding Nav Highlight | 绝对定位圆角底块悬停追随目标项的位置与宽度;移出导航回到当前页项 | 顶部导航(micro-hover 态;选中态见 navigation.md `nav-tab-liquid`) |
| `card-corner-fill` | 角落扩散悬停 Corner Fill Hover | 悬停时主色以角上圆形按钮为圆心 clip-path circle 扩散铺满功能块,文字同步反色,箭头旋转 45° | 功能卡 / 指标卡悬停态 |
| `picker-snap-level` | 分档拖动条 Snapping Level Slider | 圆角轨道 + 圆形拖柄;拖动时数字按离散档位滚动切换,已经过轨道填充主色;松手弹簧吸附最近档位 | 档位 / 力度 / 强度调节(slider-liquid 的离散档变体) |
| `chart-scrub-readout` | 跟手读数柱状图 Scrubbing Bar Chart | 细竖柱密集排列;横向移动时竖向指示线与圆形读数标签跟手,指示线左侧柱体主色、右侧压暗,顶部数值平滑滚动 | 桌面端时序数据扫读(chart-magnet-cursor 的桌面 hover 变体) |
| `list-hover-preview` | 悬停跟随预览图 Hover Image Reveal | 文字列表每行绑定一图;悬停时图片 0.8 缩放淡入并带惯性跟随光标,切换行时新图 0.9 缩放弹入覆盖,移出列表缩小淡出 | 列表行 → 图片的桌面预览(移动端对应 sheet-drawer.md `preview-longpress-peek`) |
| `theme-circular-reveal` | 圆形扩散换肤 Circular Theme Reveal | 以主题按钮为圆心 View Transitions + clip-path circle 扩散换肤,太阳图标同步变月亮,再次点击反向收回 | 主题切换(已有实现:[circular-reveal.md](../motion-skeletons/circular-reveal.md) 骨架;日月 morph 见 [`../dimensions/icon.md`](../dimensions/icon.md)) |

### AI 描述词对照

> 视频提示词原文;落 draw-md 时按模式名与使用规则参数化,不整段照抄。

| # | 组件 | AI 描述词 |
| --- | --- | --- |
| 01 | 滚动钉住主图 | 主图区域使用 position sticky 固定在视口中间,右侧文字分段滚动;根据当前段落计算滚动进度,主图的缩放和位移随进度连续过渡,推近到对应部位并亮起一圈主色标记,段落切换保持平滑。 |
| 02 | 情境光标 | 隐藏系统光标,使用一个带缓动跟随鼠标的小圆点替代;悬停图片时放大到 88px 并填充主色,中间淡入文字标签,离开后平滑缩回原尺寸。 |
| 03 | 磁吸按钮 | 鼠标进入按钮周围 60px 范围时,按钮按照光标偏移量的 0.35 倍跟随位移,内部图标额外跟随 0.15 倍;离开范围后使用 cubic-bezier(.34,1.56,.64,1) 弹性缓动回到原位。(Skill统一:全片同一种回弹力度) |
| 04 | 图标展开标签 | 圆形图标按钮悬停时宽度从 48px 过渡到自适应文字宽度,保持全圆角;标签文字延迟 80ms 淡入,相邻按钮同步平滑让位。 |
| 05 | 导航悬停指示块 | 导航项后放置绝对定位的圆角底块;悬停时读取目标项的位置和宽度,使用弹性缓动移动并同步改变宽度;移出导航后回到当前页面对应的导航项。 |
| 06 | 角落扩散悬停 | 以功能块右上角圆形箭头按钮为扩散中心,悬停时使用 clip-path circle 将主色从按钮位置扩散至整个功能块,文字颜色同步反转,箭头旋转 45 度。(Skill统一:橙色只给当前这一块) |
| 07 | 分档拖动条 | 圆角长条轨道上放置圆形拖柄;拖动时数字按离散档位滚动切换,已经过的轨道填充主色;松手后拖柄使用弹簧缓动吸附到最近档位。 |
| 08 | 跟手读数柱状图 | 细竖柱密集排列;鼠标横向移动时,竖向指示线和圆形读数标签跟随位置移动,指示线左侧柱体使用主色,右侧压暗,顶部数值随位置平滑滚动。 |
| 09 | 悬停跟随预览图 | 文字列表每行绑定一张图片;悬停时图片从 0.8 倍缩放并淡入,同时带惯性跟随光标;切换行时新图从 0.9 倍缩放弹入覆盖旧图,移出列表后缩小淡出。 |
| 10 | 圆形扩散换肤 | 以主题切换按钮中心为圆心,使用 View Transitions 配合 clip-path circle,让新配色从半径 0 逐渐扩散覆盖整个页面;太阳图标同步变成月亮,再次点击时沿相反方向收回。(Skill统一:深浅两套配色现成可用) |

### 使用规则

- **指针门控**:全节均为 hover / 指针驱动,必须 `(hover: hover) and (pointer: fine)` 探针通过才启用,触屏一律不交付(ROUTING §1 探针模式);`prefers-reduced-motion` 全部降级——光标还原系统默认、磁吸回 `micro-hover-lift`、底块与填充直接定位
- **回弹同频(视频 Skill统一①)**:同页所有跟随 / 回弹组件共用同一条曲线与时长(本节基准即 `btn-spring` 曲线 cubic-bezier(.34,1.56,.64,1)),禁各组件各配各的(同频原则见 [buttons.md](buttons.md) 使用规则)
- **主色纪律(视频 Skill统一②)**:hover 主色只给当前交互的一块,其余块保持中性;全页同屏至多一处主色块(dashboard-styles「重色只给一处」的同源纪律)
- `scroll-sticky-story`:钉住挂 [scroll.md](scroll.md) `scroll-pinned`([sticky-stack.md](../motion-skeletons/sticky-stack.md) 骨架),scrub 挂 `scroll-scrub-bind`;进度按段落区间计算,标记圈是「当前段落对应部位」的状态语义,禁做成随机高亮
- `cursor-contextual-morph`:光标必须承载语义(目标名称 / 操作标签),装饰性迟滞圆环是 ROUTING §3.8 slop form,禁用;自定义光标的 a11y 门槛与降级沿用 [micro-interactions.md](micro-interactions.md) `micro-cursor-custom`(慎用档)
- `btn-magnetic-follow`:60px 感应半径、双层跟随(按钮与图标不同倍率,层深语义)保留;位移上限以 micro-interactions.md Magnetic Button **≤ 8px** 为准(视频 0.35 倍在 60px 范围下可达约 21px,超口径弃用,按 8px 上限反算倍率);表单提交按钮禁用(micro-interactions 既有禁令)
- `btn-icon-expand`:48px→auto 动 width(按钮上动 width 合法,`btn-squash` 先例),全程保持全圆角;标签 80ms 延迟淡入防文字溢出裁切;相邻按钮让位与展开同频同缓动;触屏端不展开,点击直接执行
- `nav-hover-pill`:底块 hover 追随读取目标项 rect,与 `nav-tab-liquid`(选中态弹性指示)分工:liquid 管「选了谁」,本模式管「指着谁」;移出导航后底块必须回到当前页项,禁停在最后 hover 处
- `card-corner-fill`:扩散圆心 = 角部按钮圆心坐标(`clip-path: circle()` 起点半径同步扩大);文字反色与箭头 45° 旋转与扩散同频;反色后文字对比度必须达标(见 [accessibility.md](../meta/accessibility.md))
- `picker-snap-level`:档位 ≤ 7;拖动中数字按档滚动切换(num-ticker),已过轨道填充即时更新;松手吸附最近档,一次性过渡用 btn-spring 曲线近似,跟手中途可反向(真弹簧见 [interruptible-motion.md](../motion-skeletons/interruptible-motion.md))
- `chart-scrub-readout`:左侧主色 / 右侧压暗表达「当前 / 非当前」;读数标签跟手,数值滚动属反馈档 ≤ 400ms;数据点 > 500 先降采样(沿用 `chart-magnet-cursor` 口径);移动端换用 `chart-magnet-cursor` 触摸版
- 反馈档时长 ≤ 400ms 硬门同样适用本节(跟随 / 展开 / 填充均为状态反馈,见 [micro-interactions.md](micro-interactions.md) 分层口径)
- `list-hover-preview`:预览图 fixed 容器 rAF lerp 跟随光标(惯性系数 0.1-0.2),只动 transform;切行换图交叉淡入 + 0.9→1 弹入(一次性过渡),列表行本身禁动;预览图预载相邻行,防切换闪空;降级为行内静态缩略图
- `theme-circular-reveal`:实现全挂 [circular-reveal.md](../motion-skeletons/circular-reveal.md)(View Transitions 首选、降级双层 DOM、裁切不缩放、reduced-motion 直接切换);日月图标 morph 与扩散同帧启动;再次点击沿相反方向收回(收场复现入场轨迹,链路铁律);换肤只换 token 值不改 token 结构,深浅两套现成可用

### 在 draw-md 中的写法

```markdown
## Section (product-story)
- pattern: scroll-sticky-story
- sticky: hero-media, segments: 4, zoom: scrub, marker: accent-ring

## Nav (top-nav)
- pattern: nav-hover-pill
- hover: follow-rect, leave: return-current, fallback: nav-tab-liquid

## Card (metric-tile)
- pattern: card-corner-fill
- origin: corner-button, spread: clip-circle, invert: text-color, icon_rotate: 45deg
```

## 形变组件

> 5 个同容器形变组件(MORPH COMPONENT 系列):同一个容器走一条曲线连续插值到终态,不拆组件、不做透明度交叉,内容等容器落定后再入场,关闭沿同一条曲线反向收回。来源:形变组件视频截图提取(2026-10,MORPH COMPONENT 系列)。与移动节 `capsule-fluid-morph`(通用胶囊→面板)、`press-scale-overshoot`(按压微形变)同族,本节聚焦跨形态大形变。

### 命名表

| 模式名 | 视频组件 | 视觉特征 | 适用场景 |
| --- | --- | --- | --- |
| `search-circle-morph` | 搜索框展开 Circle to Search Bar | 圆形图标按钮形变为搜索输入框:宽 56→470、圆角 999→16 同曲线 360ms 连续插值;图标同步左移到内边距处,占位文字与光标等宽落定后再淡入,全程不切换组件 | 工具栏搜索(行为选型见 [search.md](search.md) `search-on-demand`) |
| `panel-grow-from-plus` | 加号展开面板 FAB to Sheet | 同一容器宽高 64→470×300、圆角 32→28 约 480ms;面板选项等容器落定后按每项 4 帧交错淡入,关闭沿同曲线反向收回 | FAB 新建 / 加购清单(已有实现:[sheet-drawer.md](sheet-drawer.md);通用胶囊形变见 `capsule-fluid-morph`) |
| `btn-commit-morph` | 提交状态反馈 Button to Loader to Success | 点击宽度收到圆形,沿边缘绘制环形进度;走满环合拢,勾形 strokeDasharray 描边画出,再横向展开成结果条;三态共用一个容器位置不变 | 表单提交 / 支付(已有实现:[buttons.md](buttons.md) `btn-commit-morph`) |
| `icon-path-morph` | 图标变形 SVG Path Morph | 中线透明度与横向缩放同时归零,上下两线各旋 45° 合成关闭;播放三角按同一组顶点插值成暂停两竖;全程只改顶点坐标,不切图、不做透明度交叉 | 图标状态切换(汉堡特例见 [buttons.md](buttons.md) `icon-morph-burger`;设计决策见 [`../dimensions/icon.md`](../dimensions/icon.md) 动效图标节) |
| `nav-tab-liquid` | 标签指示条 Elastic Tab Indicator | 切换时前沿先走奔向目标,后沿延后 6 帧追赶,宽度中途拉到 2 倍以上再收回,末端带一次轻微超调 | 分段 / tab 切换(已有实现:[navigation.md](navigation.md) `nav-tab-liquid`) |

### AI 描述词对照

> 视频提示词原文(系列 10 例,本批收录 01-05);落 draw-md 时按模式名与使用规则参数化,不整段照抄。

| # | 组件 | AI 描述词 |
| --- | --- | --- |
| 01 | 搜索框展开 | 圆形图标按钮形变为搜索输入框(Circle to Search Bar):宽度从 56 到 470、圆角从 999 到 16,用同一条 cubic-bezier(.2,.9,.22,1) 在 360ms 内连续插值;图标同步左移到内边距处,占位文字和光标等宽度落定后再淡入,全程不切换组件。 |
| 02 | 加号展开面板 | 悬浮按钮形变为底部面板(FAB to Sheet):同一个容器的宽高从 64 连续过渡到 470 乘 300、圆角从 32 到 28,走 cubic-bezier(.2,.9,.22,1) 约 480ms;面板里的选项等容器落定后按每项 4 帧交错淡入,关闭时沿同一条曲线反向收回原位。 |
| 03 | 提交状态反馈 | 按钮状态形变链(Button to Loader to Success):点击后宽度从 470 收到 76 变成圆形,沿边缘绘制环形进度;走满后环合拢,勾形用 strokeDasharray 描边画出来,再横向展开成结果条。三个状态共用一个容器,位置从头到尾不变。 |
| 04 | 图标变形 | 图标做路径形变(SVG Path Morph):菜单三条横线的中间一条透明度与横向缩放同时归零,上下两条各旋转 45 度合成关闭图标;播放三角按同一组顶点插值成暂停两竖。全程只改顶点坐标,不切图、不做透明度交叉。 |
| 05 | 标签指示条 | 标签指示器液态拉伸(Elastic Tab Indicator):切换时前沿先走 cubic-bezier(.2,.9,.22,1) 奔向目标,后沿延后 6 帧起步追赶,宽度中途被拉到两倍以上再收回,末端带一次轻微超调;用 left 和 width 驱动,别用 scaleX,圆角会被拉扁。 |

### 使用规则

- 形变四铁律:①同一容器从起点连续插值到终态,禁拆成两个组件交叉淡切;②全程一条缓动曲线(本系列基准 cubic-bezier(.2,.9,.22,1));③容器落定后内容才入场(交错淡入),关闭沿同一条曲线反向收回(链路铁律);④形变只动 transform 与几何属性,禁中途改布局语义
- 时长:输入框 / 面板类形变属浮层转场档 ≤ 400ms(视频 480ms 弃用,先例同 ROUTING §5 时长从属声明);tab 指示条属反馈档 ≤ 300ms
- `search-circle-morph`:圆角 999→16 与宽度同帧插值(圆→胶囊→圆角矩形连续过渡);占位文字与光标等容器宽度落定(≥ 90% 进度)后再淡入,禁提前溢出;图标左移距离 = 内边距常量
- `panel-grow-from-plus`:宽高与圆角同步插值;选项每项 4 帧交错;关闭反向收回原位(锚点丢失降级缩放淡出,沿 sheet-drawer 口径);任意胶囊→面板的通用形变走 `capsule-fluid-morph`,本模式限 FAB(+) 起点
- `btn-commit-morph`:三态(提交 / 加载 / 结果)共用容器位置钉死;环形进度沿边缘绘制(周描边);勾用 strokeDasharray 描边画出(画的过程可见);结果条横向展开后禁再变
- `icon-path-morph`:只改 SVG 顶点坐标(path d 插值),禁两张图透明度交叉;两端顶点数必须一致(不足先补齐再插值);stroke 同源图标才可 morph(icon.md 约束);汉堡、播放暂停为最小 Morph 对
- `nav-tab-liquid`:前沿 / 后沿分离驱动(前沿先走、后沿 6 帧追赶),宽度峰值 ≥ 2 倍再收回,末端轻微超调一次;**用 left + width 驱动,禁 scaleX(圆角会被拉扁)**;MOTION ≥ 7 档(navigation.md 既有门槛)

### 在 draw-md 中的写法

```markdown
## Search (toolbar-search)
- pattern: search-circle-morph
- width: 56→470, radius: 999→16, duration: 360ms, curve: cubic-bezier(.2,.9,.22,1)
- placeholder: fade-after-settle, icon: shift-inset

## Tab (view-switch)
- pattern: nav-tab-liquid
- lead_then_tail: 6f, width_peak: 2x, overshoot: once, driver: left+width
```
