# 组件命名词汇索引（30 篇）

> 本目录是 draw-md 组件命名的术语库路由器：**从索引挑名、只加载选中的那几篇**，条目明细在各篇「命名表」。本 INDEX 是 30 篇篇目的唯一清单；SKILL.md 只指向本文件，不逐篇复述。

| 篇目 | 职责 |
| --- | --- |
| [auth](auth.md) | 登录注册模式命名（登录/注册/验证/找回） |
| [buttons](buttons.md) | 按钮与卡片动效反馈命名，[micro-interactions](micro-interactions.md) 的参数级补充 |
| [cards](cards.md) | 卡片容器变体命名 |
| [charts](charts.md) | 图表选型（按数据要回答的问题先选型） |
| [chat](chat.md) | 对话与消息组件命名（气泡生命周期/流式输出/语音输入/滚动锚点/引用角标/消息动作与输入区 14 组） |
| [commerce](commerce.md) | 定价转化模式命名（价格卡/计费切换/对比矩阵/紧迫感/结账信任；文末订单与订阅诚信节） |
| [drag-drop](drag-drop.md) | 拖放模式命名（触发阈值/move-copy 语义/接受性反馈/成败反馈） |
| [forms](forms.md) | 表单模式命名（结构 + 校验时机 + 反馈位置） |
| [galleries](galleries.md) | 图片/媒体集合展示模式 |
| [hero](hero.md) | Hero 区域标准化命名（含首屏骨架表） |
| [layout](layout.md) | 页面整体布局命名（文末含仪表盘/页内模块展开交互/移动端整页布局三节） |
| [media-player](media-player.md) | 媒体播放器模式命名（加载阈值/续播/宽高比适配/浮层暂停） |
| [menus](menus.md) | 菜单形态与条目纪律命名（下拉/右键/编辑菜单/子菜单/开关项） |
| [micro-interactions](micro-interactions.md) | 元素级微交互模式（动效时长预算的 canonical） |
| [navigation](navigation.md) | 导航结构命名 |
| [notifications](notifications.md) | 通知分级与投放纪律命名（四级打断/角标/摘要/偏好管理） |
| [number-motion](number-motion.md) | 数字变化动效命名（数字是最敏感元素） |
| [onboarding](onboarding.md) | 新手引导模式命名（与 states 互补） |
| [pickers](pickers.md) | 选择器交互命名（圆周手势/速度物理/径向菜单） |
| [popups](popups.md) | 弹窗浮层链路命名（进来/停留/退场/成功） |
| [pro-motion](pro-motion.md) | 专业交互组件四节 50 组（移动动效 24 / 桌面 Web 11 / 形变 10 / 质感 5） |
| [progress-confirm](progress-confirm.md) | 进度与确认模式（过程感替代二次确认弹窗） |
| [scroll](scroll.md) | 滚动行为与动效命名 |
| [search](search.md) | 搜索与筛选模式命名（少打字、快收敛、可撤销） |
| [settings](settings.md) | 设置分流与默认值纪律命名（就地/设置页/委托系统层） |
| [sheet-drawer](sheet-drawer.md) | 底部抽屉手势生命周期与浮层链路（文末含专业面板 6 组件） |
| [states](states.md) | 页面级 Loading/Empty/Error 状态命名 |
| [tables](tables.md) | 数据表格模式命名（按量级与操作需求选型） |
| [typography](typography.md) | 高级排版模式（font.md 管「用什么值」，本篇管「怎么排」） |
| [undo-redo](undo-redo.md) | 撤销重做命名（具名撤销/结果可见/批量回退/不限次数） |

---

## 中英术语对照（前端效果词典 80 项）

> 中文说法 → 英文术语 → 库内落点。写提示词时先用对名称（"说不出名称 = 落入默认审美"）；库内已有模式的用模式名，无模式行的词直接作提示词术语使用（标 † 为 CSS/SVG 原语词，不入命名表）。

- **布局与页面结构**：网格布局=Grid Layout（[layout](layout.md) 网格系）· 弹性布局=Flexbox † · 便当盒布局=Bento Grid（`layout-bento-grid`）· 瀑布流=Masonry Layout（[cards](cards.md)/[galleries](galleries.md) 瀑布流系）· 分屏布局=Split-screen Layout（[layout](layout.md) 分栏）· 卡片式布局=Card Layout（[cards](cards.md)）· 首屏主视觉=Hero Section（[hero](hero.md)）· 侧边栏=Sidebar（[navigation](navigation.md) nav-rail 系）· 粘性定位=Sticky（[scroll](scroll.md) `scroll-pinned`）· 固定定位=Fixed † · 响应式布局=Responsive Layout（framework 断点系）· 留白=Whitespace（dimensions spacing）
- **组件与信息呈现**：导航栏=Navigation Bar（[navigation](navigation.md)）· 下拉菜单=Dropdown Menu（[menus](menus.md)）· 大型下拉菜单=Mega Menu（[menus](menus.md)）· 标签页=Tabs（[navigation](navigation.md) `nav-tab-liquid`）· 手风琴=Accordion（[layout](layout.md) `accordion-exclusive-expand`）· 模态弹窗=Modal Dialog（[popups](popups.md)）· 抽屉面板=Drawer（[sheet-drawer](sheet-drawer.md)）· 悬浮提示=Tooltip（[micro-interactions](micro-interactions.md) `micro-tooltip`）· 弹出浮层=Popover（[popups](popups.md)）· 轻提示=Toast（[micro-interactions](micro-interactions.md) `micro-toast`）· 轮播=Carousel（[galleries](galleries.md) 轮播族）· 图片灯箱=Lightbox（`gallery-lightbox`）
- **触发与滚动行为**：悬停=Hover（[micro-interactions](micro-interactions.md) hover 族）· 焦点状态=Focus（`micro-focus-ring`）· 按下状态=Active/Pressed（`micro-press-scale`）· 禁用状态=Disabled（[forms](forms.md) 边界停用规则）· 拖放=Drag and Drop（[drag-drop](drag-drop.md)）· 滑动手势=Swipe（[cards](cards.md) swipe 族）· 滚动/平滑滚动/横向滚动=Scroll/Smooth/Horizontal（[scroll](scroll.md)）· 滚动吸附=Scroll Snap（`gallery-carousel-peek-snap` 等）· 无限滚动=Infinite Scroll（`scroll-infinite`）· 回到顶部=Back to Top（[scroll](scroll.md)）
- **基础动效与加载**：过渡=Transition † · 缓动=Easing（[micro-interactions](micro-interactions.md) 缓动口径）· 弹簧动画=Spring Animation（[pro-motion](pro-motion.md) spring 系）· 淡入淡出=Fade In/Out † · 滑入滑出=Slide In/Out † · 缩放=Scale/Zoom † · 旋转=Rotate † · 翻转=Flip（`card-flip-3d`）· 交错入场=Stagger（[pro-motion](pro-motion.md) `stagger-spring-cascade`）· 页面转场=Page Transition（motion-skeletons shared-element 系）· 加载指示=Loading Indicator（[states](states.md) 加载族）· 骨架屏=Skeleton（`state-skeleton`）· 走马灯=Marquee（`type-marquee`）
- **连续展示与跟随**：视差滚动=Parallax（`scroll-dual-column-parallax` 等）· 滚动显现=Scroll Reveal（[scroll](scroll.md) reveal 族）· 滚动进度=Scroll Progress（`scroll-scrub-bind`）· 打字机=Typewriter（`type-typewriter-loop`；AI 流式见 `chat-stream-typewriter`）· 文字揭示=Text Reveal（[typography](typography.md)）· 乱码解码=Text Scramble（`type-text-scramble`）· 数字递增=Count-up（`num-ticker-onview`）· 三维倾斜=3D Tilt（`card-tilt-depth`）· 磁吸效果=Magnetic（`micro-magnet-hover` / `btn-magnetic-follow`）· 光标跟随=Cursor Follow（`micro-cursor-custom` / `cursor-contextual-morph`）· 运动拖尾=Motion Trail（`motion-trail-echo`）
- **视觉效果与材质**：毛玻璃=Glassmorphism（[glass-effect](../dimensions/glass-effect.md)）· 渐变=Gradient † · 颗粒噪点=Grain/Noise（[texture](../dimensions/texture.md)）· 模糊=Blur † · 发光=Glow（[effects-degradation](../dimensions/effects-degradation.md)）· 路径裁切=Clip-path † · 遮罩=Mask † · 扭曲=Distortion † · 黏液融合=Gooey（`micro-gooey-metaball`）· 粒子效果=Particles（[charts](charts.md)/[buttons](buttons.md) 粒子族）· 聚光灯效果=Spotlight（`cursor-spotlight-reveal`；引导遮罩见 `onboard-spotlight-morph`）· 倒影=Reflection（[hero-stage](../dimensions/hero-stage.md) reflection）
- **整体视觉风格**：极简风=Minimalism（[design-systems](../dimensions/design-systems.md)）· 粗野主义=Brutalism / 新粗野主义=Neobrutalism（donors 候选池 neubrutalism-v2）· 新拟态=Neumorphism（[forms](forms.md) `toggle-press-slide-rebound` 等 neu 族）· 拟物风=Skeuomorphism（donors 候选池 skeuomorphism）· 复古风=Retro / 像素风=Pixel Art / 字符画=ASCII Art（donors 候选池,按需晋升）

### 词典外补充（80 词未覆盖的常用术语）

> 同一对照口径,收录词典 80 项之外的常用说法;锚点均经 grep 核实,真空词标 † 作纯提示词术语。

- **交互与手势**：下拉刷新=Pull to Refresh（`scroll-pull-refresh`）· 边缘阻尼/橡皮筋=Overscroll Rubber-band（`scroll-overscroll-damp`）· 惯性滚动=Momentum Scrolling（`picker-wheel-decay` 速度衰减）· 触觉反馈=Haptics（`micro-haptic`）· 长按=Long-press（`press-peek` / `micro-hold-confirm`）· 双击=Double-tap（`chat-heart-fly-avatar`）· 摇一摇=Shake Gesture † · 拖拽排序=Drag-to-reorder（[drag-drop](drag-drop.md)）· 左滑删除=Swipe-to-delete（`swipe-row-delete`）· 压感=Force Touch † · 手势密码=Pattern Lock † · 生物识别=Biometric（Face ID/指纹）†
- **组件**：涟漪/水波纹=Ripple（`micro-ripple`）· 步进器=Stepper（`picker-stepper-roll`）· 评分=Rating（[forms](forms.md) 评分条）· 面包屑=Breadcrumb（[navigation](navigation.md)）· 树形视图=Tree View（`nav-menu-submenu-inline`）· 虚拟列表=Virtualized List（`scroll-virtualized`）· 时间轴=Timeline（`progress-timeline-card`）· 画中画=Picture-in-Picture（[pro-motion](pro-motion.md) 滚动变小窗）· 扫码=QR Scan（[auth](auth.md)）· 弹幕=Danmaku †
- **图表**：雷达图=Radar / 桑基图=Sankey / K线=Candlestick / 词云=Word Cloud（[charts](charts.md)）· 子弹图=Bullet（charts bullet 网格）· 水球图=Liquid Fill †
- **动效黑话**：容器变换=Container Transform（`shared-element-card-transition`）· 错误抖动=Wobble（`validate-error-shake`）· 呼吸感=Breathing（`player-ambient-sync` 等环境动效）· 扫光=Sheen Sweep（[pro-motion](pro-motion.md)）· 景深=Depth of Field（[pro-motion](pro-motion.md) / [scroll](scroll.md)）· 进度环=Activity Ring（`progress-save-ring` / `habit-week-ring-checkin`）· 转盘=Dial（`picker-knob-dial`）· 老虎机滚轮=Slot Reel（[number-motion](number-motion.md) 翻位族）· 刮刮卡=Scratch Card † · 烟花=Fireworks † · 红包=Red Envelope †
- **风格补充**：液态玻璃=Liquid Glass（`nav-liquid-glass`；配方 [glass-effect](../dimensions/glass-effect.md)/[glass-advanced](../dimensions/glass-advanced.md)）· 黏土风=Claymorphism † · 弥散光/极光渐变=Aurora Gradient † · 等距 2.5D=Isometric † · 手绘风=Hand-drawn † · 瑞士风=Swiss/International † · 包豪斯=Bauhaus † · 孟菲斯=Memphis † · 全息镭射=Holographic † · 蒸汽波=Vaporwave / 赛博朋克=Cyberpunk / 酸性设计=Acid †（风格词提示词直用;禁用形容词表见 [ai-tells](../meta/ai-tells.md)）

