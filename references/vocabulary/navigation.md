# 导航模式命名词汇

> 模式词汇库。draw-md 阶段描述导航结构时使用的标准化命名。来源:taste-skill。

## 命名表

| 模式名                | 视觉特征                                          | 适用场景                              |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `nav-top-bar`         | 顶部水平导航栏,logo 左 + 菜单项右                | Web 默认,大多数站点                  |
| `nav-top-transparent` | 透明顶栏:顶栏底色与分隔线全去掉,文字直接落在页面背景上,仅当前项加半透明白色圆角底(**转录补全**,2026-10) | 首屏有大图/渐变背景的后台             |
| `nav-sidebar`         | 左侧垂直导航,常配折叠 / 面包屑                   | SaaS Dashboard、文档站、DevTool       |
| `nav-bottom-tab`      | 底部 tab 栏(移动端),≤ 5 项                     | 移动 App 主导航                       |
| `nav-dock`            | 浮动 dock(类 macOS),底部居中                   | 移动 App 辅助导航、PWA                |
| `nav-hamburger`       | 隐藏在 hamburger 菜单内                          | 移动端、二级导航                      |
| `nav-mega-menu`       | 顶部悬停展开大菜单(多列)                       | 电商、企业站(信息架构深)            |
| `nav-breadcrumb`      | 面包屑路径                                        | 多层级页面(详情 / 设置 / 后台)      |
| `nav-command-palette` | ⌘K 命令面板                                       | DevTool、SaaS、生产力工具             |
| `nav-floating-pill`   | 浮动药丸式导航,滚动时显隐                        | 长滚动页(单页营销 / 品牌站)         |
| `nav-stepper`         | 步进式导航(1/2/3)                                | 流程页(结账、注册、向导)            |
| `nav-floating-island` | 浮岛导航:悬浮胶囊 + 汉堡→X 形变 + 蒙版错峰揭示   | 品牌 / 创意站;移动端降级为全宽 dock(来源:taste-skill soft-skill §5.A) |
| `nav-fab`             | 悬浮操作按钮:右下角单 FAB(一屏仅一个主操作),滚动下滑出现 / 上滑收起联动,避开底部导航安全区 | 移动 App 新建/发布/写等一级操作入口                |
| `nav-tab-spring-underline` | 顶部标签页跟手下划线:下划线随拖动半路跟手,松手落定,选中标签自动滚动居中 | 顶部多 tab(资讯、订单分类)                     |
| `nav-tab-liquid`      | 液态 tab 指示器:选中背景移动中先拉长再收缩最后回弹,像液体流过去 | 分段切换(MOTION ≥ 7)                          |
| `nav-large-title-collapse` | 大标题折叠:缩放/横移/上移/底色全挂同一个滚动进度,大标题随滚动收进导航栏 | iOS 式列表页、个人主页                       |
| `nav-bottom-action-bar` | 吸底操作栏:关键信息+主按钮常驻底部,避开手势安全区(environ safe-area) | 详情页购买栏、多选操作栏                      |
| `nav-tabbar-auto-hide` | 底栏滚动方向感知显隐:下滚收起(内容全宽沉浸),上滚即唤出 | 信息流 / 浏览型页(流程 / 详情页禁用,操作导航须常驻) |
| `nav-predictive-back` | 预测性返回:返回手势中预览目标页,松手确认跳转,中途松开回弹取消 | Android / 鸿蒙系统级返回转场(M3 Expressive) |

## 侧边栏骨架六式(后台/桌面端)

> SaaS/后台侧边栏的组合骨架命名。来源:UI 交互教学视频转录提取(2026-09)。

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `nav-sidebar-float` | 悬浮导视:脱离屏幕边缘浮起,大圆角+低透明度柔和投影 | 品牌化后台、设计工具 |
| `nav-sidebar-dark-heavy` | 深色重底:整页浅色、深色集中给侧栏,当前项才亮 | 传统企业后台 |
| `nav-sidebar-glass` | 磨砂玻璃侧栏:半透明白+背景模糊+1px 亮边(配 [`../dimensions/glass-effect.md`](../dimensions/glass-effect.md)) | 现代 SaaS(与 `nav-sidebar-float` 常组合) |
| `nav-sidebar-rail-double` | 双层图标轨:72px 窄图标轨切模块+240px 二级面板 | IDE、深度后台(模块×页面两维) |
| `nav-sidebar-collapse-hover` | 悬停折叠展开:宽度 72→240 平滑过渡,文字延时 80ms 淡入 | 空间紧张的后台(与 rail 组合) |
| `nav-sidebar-grouped` | 分组留白+底部用户区:分组间距、组名小灰字、底部固定头像与用量,中间列表独立滚动 | 默认推荐,所有多分组后台 |

> 侧边栏通用规则:中间导航列表独立滚动,顶部(产品标识)与底部(用户/用量)固定;当前项用填充底色而非仅变色。

> 来源注:侧边栏六式与 `nav-tab-spring-underline` 至 `nav-bottom-action-bar` 为**转录补全**(2026-09-22,UI 交互教学视频转录提取);`nav-tabbar-auto-hide` / `nav-predictive-back` 为**外部对标补全**(2026-10,Material 3 / Smashing 底栏金律 / M3 Expressive)。

## 菜单项级交互(侧栏/底栏)

> 菜单是后台里点得最多的地方,它顺了整页就顺;不必全上,挑一两种配着用(如滑动高亮块+命令面板,或菜单内搜索+拖动排序)。来源:UI 交互教学视频转录提取(2026-10)。

| 模式名 | 视觉特征 | 适用场景 |
| --- | --- | --- |
| `nav-menu-sliding-highlight` | 滑动高亮块:圆角高亮底从旧项滑到新项,宽高随目标项伸缩,落位轻回弹 | 后台侧栏当前项指示 |
| `nav-menu-submenu-inline` | 就地展开子菜单:箭头旋转 90°,子项错峰落下,左侧细竖线串住;同时只展开一组 | 树形侧栏 |
| `nav-workspace-switcher` | 工作区切换器:点工作区名原地弹出列表,当前项打勾;切换后名称滚动替换,整条菜单强调色跟随工作区切换 | 多租户/多空间后台 |
| `nav-menu-drag-pin` | 菜单拖动排序+钉住:拖动项轻抬跟手、其余平滑让位,松手吸附(骨架机制见 [`../motion-skeletons/spring-reorder.md`](../motion-skeletons/spring-reorder.md));拖过顶部分隔线固定为常用区,一直排最前 | 长菜单个性化 |
| `nav-menu-filter-search` | 菜单内搜索:输入时非匹配项收拢消失,匹配项上移并拢、命中文字高亮;清空按原序恢复,不弹窗不跳页 | 长菜单快速定位 |
| `nav-menu-flyout` | 悬停滑出二级面板:一级项右侧紧贴滑出,项间移动只换内容不收开,离开自动收起 | 深层级后台(桌面端) |
| `nav-breadcrumb-sibling-peek` | 面包屑同级下拉:点面包屑某段露出同级页面小列,选择后该段文字滚动替换,后续层级同步更新 | 多层级后台(与 `nav-breadcrumb` 组合) |
| `nav-tabbar-expand-label` | 底栏选中展开文字:选中项旁长出文字标签,底色块滑到选中位置,其余项收回只留图标 | 移动底栏(≤ 4 项时收益明显) |
| `nav-rail-right` | 右侧竖轨菜单:主导航收成最右侧通高窄图标轨,整条亮色,当前项深色圆角底,新建按钮固定轨顶(与 `nav-sidebar-rail-double` 互见:彼条左轨+二级面板,本条单右轨) | 内容区需整块展示的看板 |
| `nav-title-as-nav` | 图标菜单配大标题:侧栏收成纯图标轨,当前页面名放大为左上角页面大标题,旁接范围选择器,切图标标题同步更换 | 页面不多的工具类后台 |
| `nav-quick-actions` | 菜单旁快捷操作列:最常用动作做成一列圆形按钮贴菜单旁,最重要的一枚用主色,点击就地执行不跳页 | 新建/导出等高频动作 |
| `nav-dock-disc` | 底栏常驻圆碟:底部导航右端嵌圆形封面/状态碟,进行中轻微浮动、暂停静止,任何页面点击直达当前面板(与 `nav-dock` 互见:彼条入口菜单,本条状态回入口) | 媒体播放/任务进行中的全局回入口 |

> 来源注:本节八式为**转录补全**(2026-10,UI 交互教学视频转录提取);`nav-rail-right` / `nav-title-as-nav` / `nav-quick-actions` / `nav-dock-disc` 4 行为**转录补全**(2026-10 第二批,同源);`nav-top-transparent` 在命名表。

## 使用规则

- 同一站点导航模式 ≤ 2 种组合(如 `nav-top-bar` + `nav-bottom-tab` 跨端)
- 主要功能 1 tap 可达(Navigation HIGH 优先级,见 [`rules-priority.md`](../meta/rules-priority.md))
- 移动端导航项 ≤ 5 个(米勒定律,见 [`principles.md`](../meta/principles.md))
- 触发 hamburger 时,主功能不可埋深处(≤ 2 级)
- 命令面板 ⌘K 与 `nav-top-bar` 共存,不替代主导航

## 在 draw-md 中的写法

```markdown
## Navigation
- primary: nav-top-bar
- items: [Home, Products, Pricing, Docs, Login]
- mobile: nav-bottom-tab
- mobile_items: [Home, Search, Cart, Profile]
- secondary: nav-command-palette (⌘K)
```
