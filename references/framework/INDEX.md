# 框架资源总览

> 本文件是 `references/framework/` 分层框架文档数据库的入口,为 `draw-harmony` / `draw-flutter` / `draw-element` 三个子命令提供组件映射参考;接入契约与实时查询语义见 [adapter-contract.md](./adapter-contract.md)。
> 每个框架下按组件类型组织(共 56 类,3 现有 + 53 新增),每类组件含两份文档(文件名遵循各框架生态术语惯例)。
> **选型判据层**:[`component-routing.md`](./component-routing.md) 按「区块要做什么」给推荐组件组合 + 反模式,draw-md 步骤 2.6 逐区块过表——本文件管「组件类有哪些文档」,选哪个组合先看路由表。
> 部分组件在某框架无原生对应时,以 N/A 占位文件说明缺失原因与替代方案,保持目录结构对称。
> **API 基线**:HarmonyOS NEXT 6.0.0(API 20) / Flutter 3.47.5(stable) / Element Plus 2.14.6;超基线 API 标 `⚠`,分 `safe to plan around` / `unsafe to write today` 两级并附降级写法,详见下文「API 基线」节。
> **事实源与回退(2026-11,取代 2026-10 EP 双源协调注记)**:组件文档以**官网实时抓取**为事实源(按 [adapter-contract.md](./adapter-contract.md) 各组件源 ingest 通道);本仓 `framework/` 快照降级为**回退源**——仅官网程序化抓取失败的框架(当前 ArkUI,见「API 基线」节)以快照为主源,其余框架仅断网兜底,快照缺失则跳过本级并显式报告。element-dev 边界不变:运行时报错与 API 深查询走 element-dev,maliang 只做生成期映射查询。不建持久缓存:查询结果仅会话内按查询键内存去重(契约见 [adapter-contract.md](./adapter-contract.md)「查询契约」)。快照刷新触发条件保持:各框架基线版本变更时同步重建(以本节基线为准)。

---

## API 基线

`framework/` 组件文档与三个 `draw-*` 子命令产出均以本节基线为准,避免 ArkTS/Flutter/EP 快速演进导致生成代码版本错配。

| 框架 | API 基线 | 发布日期 | 来源(查询日期 2026-09-28) |
| ---- | -------- | -------- | ------------------------- |
| HarmonyOS NEXT | 6.0.0 Release(API 20) | 2025-09-25 | API level:OpenHarmony 官方 docs `v6.0-release.md`(新增 API 锚点后缀 20,一手);版本与日期:媒体对「HarmonyOS 6.0.0(20) Release」的一致转述(二手)。华为官方版本说明页(developer.huawei.com/consumer/cn/doc/harmonyos-releases)为 JS 渲染页,程序化抓取失败,未能直接采信 |
| Flutter | 3.47.5(stable 通道) | 2026-09-18 | Flutter 官方 releases JSON(storage.googleapis.com/flutter_infra_release/releases/releases_linux.json)的 `current_release.stable`,hash `6a19cca5`(一手);注意 flutter/flutter 的 GitHub Releases 已停更,勿以其为准 |
| Element Plus | 2.14.6 | 2026-09-18 | `gh api repos/element-plus/element-plus/releases/latest`(一手) |

> **HarmonyOS 待人工复核**:开发套件 26.0.0(API 号自 26.0.0 起改用 SemVer,对应 HarmonyOS 7.0 / OpenHarmony 7.0)已于 2026-08-29 发布——此信息目前仅媒体转述,官方页未能程序化核实。存量设备仍以 6.x 为主,故基线暂取一手可验证的 6.0.0(API 20);人工在官方版本说明页复核后可上调基线并同步本表与三个 `draw-*.md` 头部声明。

### 超基线 API 两级语义

`framework/` 文档与 `draw-*` 产出中,凡依赖高于基线的 API 一律标 `⚠`,按可写性分两级:

| 级别 | 判定 | 处理 |
| ---- | ---- | ---- |
| `⚠ safe to plan around` | 已稳定发布(正式 Release)但超出基线 | 设计与 token 层可正常写入规划;实现时必须附版本/能力检测与降级写法 |
| `⚠ unsafe to write today` | 处于 Beta/预览,或仅来自未核实来源 | 禁止写入产出代码;直接按降级写法用基线内 API 或成熟组合方案实现同等效果 |

### 降级写法

| 框架 | 降级模式 |
| ---- | -------- |
| HarmonyOS(ArkTS) | 优先基线内等价属性;确需新 API 时用 `canIUse()`(SysCap 能力检测)写降级分支 |
| Flutter(Dart) | 优先基线内 widget;新 API 用主题/平台分支或生态稳定包兜底,禁止 pin 未稳定 channel |
| Element Plus(Vue 3) | 优先基线内组件与 CSS 变量;新 API 做特性检测(typeof/版本判断)后走降级组件或样式 |

> 判据:产出代码必须能在存量主流系统版本上运行;拿不准时一律按 `unsafe to write today` 处理。

---

## 复用阶梯(Use What Exists)


### 控件三级阶梯

| 级别 | 选择               | 说明                                                                                                        |
| ---- | ------------------ | ----------------------------------------------------------------------------------------------------------- |
| 1    | 原生 HTML / 系统组件 | 首选各框架原生控件(`<button>`/`<select>`、ArkTS Toggle、Flutter Switch 等),自带键盘、无障碍与手势行为           |
| 2    | 成熟 headless 原语  | 行为复杂且原生不够用时,选成熟 headless 库(Radix/React Aria 类)或框架生态内验证过的实现,只做视觉定制             |
| 3    | 手搓(最后手段)      | 必须交付完整行为契约:**键盘导航、焦点陷阱、ARIA、click-outside、scroll-lock**——缺任一即 broken 而非"不一致",按不可交付处理 |

### 样式四级阶梯

| 级别 | 选择        | 说明                                                   |
| ---- | ----------- | ------------------------------------------------------ |
| 1    | 设计系统     | 优先用 DESIGN.md 既有 token 与组件规格                   |
| 2    | 提取组件     | 出现**第二次真实复用**时才提取成组件,不过早抽象           |
| 3    | 语义 token   | 无组件可复用时,用语义 token 组合表达                     |
| 4    | 工具类一次性 | 最后才是一次性工具类;同一样式第三次出现即回退到级 2 提取   |

### 结构性 hack 禁令

| 禁止               | 典型形态                          | 正确做法                     |
| ------------------ | --------------------------------- | ----------------------------- |
| 负 margin 抵消父 padding | `margin: -16px` 对冲容器内边距    | 调整容器 padding,或将内容移出容器 |
| 逃生舱 calc()      | `calc(100% - 47px)` 之类魔法数字  | 用 flex/grid 分配空间,让布局系统计算 |
| 绝对定位绕布局流    | `position: absolute` 硬压坐标摆位 | 回到正常布局流重组结构         |

> 判据:**正确答案比 hack 更简单**。写出 hack 前先问"是哪层布局结构错了"。

---

## 组件类型索引表

### 现有组件(3 类)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| button | 触发操作的按钮 | [component.md](./harmony/button/component.md) + [usage.md](./harmony/button/usage.md) | [widget.md](./flutter/button/widget.md) + [properties.md](./flutter/button/properties.md) | [component.md](./element/button/component.md) + [api.md](./element/button/api.md) |
| text | 文本展示 | [component.md](./harmony/text/component.md) + [usage.md](./harmony/text/usage.md) | [widget.md](./flutter/text/widget.md) + [properties.md](./flutter/text/properties.md) | [component.md](./element/text/component.md) + [api.md](./element/text/api.md) |
| list | 行列表容器 | [component.md](./harmony/list/component.md) + [usage.md](./harmony/list/usage.md) | [widget.md](./flutter/list/widget.md) + [properties.md](./flutter/list/properties.md) | [component.md](./element/list/component.md) + [api.md](./element/list/api.md) |

### P0 类(6 类,三框架都有原生组件)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| layout | 布局容器(线性/堆叠/网格) | [component.md](./harmony/layout/component.md) + [usage.md](./harmony/layout/usage.md) | [widget.md](./flutter/layout/widget.md) + [properties.md](./flutter/layout/properties.md) | [component.md](./element/layout/component.md) + [api.md](./element/layout/api.md) |
| image | 图片展示 | [component.md](./harmony/image/component.md) + [usage.md](./harmony/image/usage.md) | [widget.md](./flutter/image/widget.md) + [properties.md](./flutter/image/properties.md) | [component.md](./element/image/component.md) + [api.md](./element/image/api.md) |
| tabs | 标签页切换 | [component.md](./harmony/tabs/component.md) + [usage.md](./harmony/tabs/usage.md) | [widget.md](./flutter/tabs/widget.md) + [properties.md](./flutter/tabs/properties.md) | [component.md](./element/tabs/component.md) + [api.md](./element/tabs/api.md) |
| input | 单行文本输入 | [component.md](./harmony/input/component.md) + [usage.md](./harmony/input/usage.md) | [widget.md](./flutter/input/widget.md) + [properties.md](./flutter/input/properties.md) | [component.md](./element/input/component.md) + [api.md](./element/input/api.md) |
| checkbox | 多选框(三态) | [component.md](./harmony/checkbox/component.md) + [usage.md](./harmony/checkbox/usage.md) | [widget.md](./flutter/checkbox/widget.md) + [properties.md](./flutter/checkbox/properties.md) | [component.md](./element/checkbox/component.md) + [api.md](./element/checkbox/api.md) |
| select | 下拉选择器(数据录入) | [component.md](./harmony/select/component.md) + [usage.md](./harmony/select/usage.md) | [widget.md](./flutter/select/widget.md) + [properties.md](./flutter/select/properties.md) | [component.md](./element/select/component.md) + [api.md](./element/select/api.md) |

### P1 类(25 类,跨框架覆盖,部分 N/A)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| navigation | 导航容器(栏/抽屉/底部) | [component.md](./harmony/navigation/component.md) + [usage.md](./harmony/navigation/usage.md) | [widget.md](./flutter/navigation/widget.md) + [properties.md](./flutter/navigation/properties.md) | [component.md](./element/navigation/component.md) + [api.md](./element/navigation/api.md) |
| form | 表单容器(多字段提交) | [N/A](./harmony/form/component.md)(ArkTS 无 Form 容器) | [widget.md](./flutter/form/widget.md) + [properties.md](./flutter/form/properties.md) | [component.md](./element/form/component.md) + [api.md](./element/form/api.md) |
| dialog | 模态对话框 | [component.md](./harmony/dialog/component.md) + [usage.md](./harmony/dialog/usage.md) | [widget.md](./flutter/dialog/widget.md) + [properties.md](./flutter/dialog/properties.md) | [component.md](./element/dialog/component.md) + [api.md](./element/dialog/api.md) |
| grid | 网格布局 | [component.md](./harmony/grid/component.md) + [usage.md](./harmony/grid/usage.md) | [widget.md](./flutter/grid/widget.md) + [properties.md](./flutter/grid/properties.md) | [component.md](./element/grid/component.md) + [api.md](./element/grid/api.md) |
| progress | 进度指示器(线性/环形) | [component.md](./harmony/progress/component.md) + [usage.md](./harmony/progress/usage.md) | [widget.md](./flutter/progress/widget.md) + [properties.md](./flutter/progress/properties.md) | [component.md](./element/progress/component.md) + [api.md](./element/progress/api.md) |
| icon | 图标 | [component.md](./harmony/icon/component.md) + [usage.md](./harmony/icon/usage.md) | [widget.md](./flutter/icon/widget.md) + [properties.md](./flutter/icon/properties.md) | [component.md](./element/icon/component.md) + [api.md](./element/icon/api.md) |
| shape | 矢量图形/形状 | [component.md](./harmony/shape/component.md) + [usage.md](./harmony/shape/usage.md) | [widget.md](./flutter/shape/widget.md) + [properties.md](./flutter/shape/properties.md) | [component.md](./element/shape/component.md) + [api.md](./element/shape/api.md) |
| theme | 主题切换(浅/暗) | [component.md](./harmony/theme/component.md) + [usage.md](./harmony/theme/usage.md) | [widget.md](./flutter/theme/widget.md) + [properties.md](./flutter/theme/properties.md) | [component.md](./element/theme/component.md) + [api.md](./element/theme/api.md) |
| animation | 动画/过渡 | [component.md](./harmony/animation/component.md) + [usage.md](./harmony/animation/usage.md) | [widget.md](./flutter/animation/widget.md) + [properties.md](./flutter/animation/properties.md) | [component.md](./element/animation/component.md) + [api.md](./element/animation/api.md) |
| gesture | 手势识别(点击/滑动/长按) | [component.md](./harmony/gesture/component.md) + [usage.md](./harmony/gesture/usage.md) | [widget.md](./flutter/gesture/widget.md) + [properties.md](./flutter/gesture/properties.md) | [N/A](./element/gesture/component.md)(Element 无手势组件) |
| i18n | 国际化/多语言 | [component.md](./harmony/i18n/component.md) + [usage.md](./harmony/i18n/usage.md) | [widget.md](./flutter/i18n/widget.md) + [properties.md](./flutter/i18n/properties.md) | [component.md](./element/i18n/component.md) + [api.md](./element/i18n/api.md) |
| a11y | 无障碍(语义/焦点/对比度) | [component.md](./harmony/a11y/component.md) + [usage.md](./harmony/a11y/usage.md) | [widget.md](./flutter/a11y/widget.md) + [properties.md](./flutter/a11y/properties.md) | [N/A](./element/a11y/component.md)(Element 无 a11y 章节) |
| video | 视频播放 | [component.md](./harmony/video/component.md) + [usage.md](./harmony/video/usage.md) | [widget.md](./flutter/video/widget.md) + [properties.md](./flutter/video/properties.md) | [N/A](./element/video/component.md)(Element 无视频组件) |
| menu | 菜单(下拉/上下文) | [component.md](./harmony/menu/component.md) + [usage.md](./harmony/menu/usage.md) | [widget.md](./flutter/menu/widget.md) + [properties.md](./flutter/menu/properties.md) | [component.md](./element/menu/component.md) + [api.md](./element/menu/api.md) |
| scroll | 滚动容器 | [N/A](./harmony/scroll/component.md)(ArkTS 无独立 Scroll 指南) | [widget.md](./flutter/scroll/widget.md) + [properties.md](./flutter/scroll/properties.md) | [component.md](./element/scroll/component.md) + [api.md](./element/scroll/api.md) |
| carousel | 轮播图 | [component.md](./harmony/carousel/component.md) + [usage.md](./harmony/carousel/usage.md)(ArkTS 原生名 Swiper) | [widget.md](./flutter/carousel/widget.md) + [properties.md](./flutter/carousel/properties.md) | [component.md](./element/carousel/component.md) + [api.md](./element/carousel/api.md) |
| radio | 单选按钮 | [component.md](./harmony/radio/component.md) + [usage.md](./harmony/radio/usage.md) | [widget.md](./flutter/radio/widget.md) + [properties.md](./flutter/radio/properties.md) | [component.md](./element/radio/component.md) + [api.md](./element/radio/api.md) |
| switch | 开关切换 | [component.md](./harmony/switch/component.md) + [usage.md](./harmony/switch/usage.md)(ArkTS 原生名 Toggle) | [widget.md](./flutter/switch/widget.md) + [properties.md](./flutter/switch/properties.md) | [component.md](./element/switch/component.md) + [api.md](./element/switch/api.md) |
| popover | 浮层提示(Popover/Tooltip) | [component.md](./harmony/popover/component.md) + [usage.md](./harmony/popover/usage.md)(ArkTS 原生名 Popup) | [N/A](./flutter/popover/widget.md)(Flutter 无 Popover widget) | [component.md](./element/popover/component.md) + [api.md](./element/popover/api.md)(Popover + Tooltip + Popconfirm) |
| message | 即时反馈消息(Toast/SnackBar) | [component.md](./harmony/message/component.md) + [usage.md](./harmony/message/usage.md)(ArkTS 原生名 Toast) | [widget.md](./flutter/message/widget.md) + [properties.md](./flutter/message/properties.md)(Flutter 原生名 SnackBar) | [component.md](./element/message/component.md) + [api.md](./element/message/api.md) |
| drawer | 抽屉/侧边栏 | [component.md](./harmony/drawer/component.md) + [usage.md](./harmony/drawer/usage.md)(ArkTS 原生名 bindSheet) | [widget.md](./flutter/drawer/widget.md) + [properties.md](./flutter/drawer/properties.md) | [component.md](./element/drawer/component.md) + [api.md](./element/drawer/api.md) |
| upload | 文件/图片上传 | [component.md](./harmony/upload/component.md) + [usage.md](./harmony/upload/usage.md)(组合方案:Picker + List + Progress) | [widget.md](./flutter/upload/widget.md) + [properties.md](./flutter/upload/properties.md)(组合方案:image_picker/file_picker) | [component.md](./element/upload/component.md) + [api.md](./element/upload/api.md) |
| date-picker | 日期时间选择(录入) | [component.md](./harmony/date-picker/component.md) + [usage.md](./harmony/date-picker/usage.md)(DatePickerDialog/TimePickerDialog) | [widget.md](./flutter/date-picker/widget.md) + [properties.md](./flutter/date-picker/properties.md)(showDatePicker/showTimePicker) | [component.md](./element/date-picker/component.md) + [api.md](./element/date-picker/api.md)(el-date-picker/el-time-picker) |
| notification | 常驻通知(消息中心) | [component.md](./harmony/notification/component.md) + [usage.md](./harmony/notification/usage.md)(组合方案:Stack 顶部横幅) | [widget.md](./flutter/notification/widget.md) + [properties.md](./flutter/notification/properties.md)(组合方案:MaterialBanner) | [component.md](./element/notification/component.md) + [api.md](./element/notification/api.md)(ElNotification) |
| slider | 滑块(数值/区间录入) | [component.md](./harmony/slider/component.md) + [usage.md](./harmony/slider/usage.md) | [widget.md](./flutter/slider/widget.md) + [properties.md](./flutter/slider/properties.md)(Slider/RangeSlider) | [component.md](./element/slider/component.md) + [api.md](./element/slider/api.md) |

### P2 类(22 类,通用性中-高,部分单框架)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| card | 卡片容器 | [component.md](./harmony/card/component.md) + [usage.md](./harmony/card/usage.md)(组合方案) | [widget.md](./flutter/card/widget.md) + [properties.md](./flutter/card/properties.md) | [component.md](./element/card/component.md) + [api.md](./element/card/api.md) |
| table | 数据表格 | [component.md](./harmony/table/component.md) + [usage.md](./harmony/table/usage.md)(组合方案) | [widget.md](./flutter/table/widget.md) + [properties.md](./flutter/table/properties.md) | [component.md](./element/table/component.md) + [api.md](./element/table/api.md) |
| tree | 树形控件 | [component.md](./harmony/tree/component.md) + [usage.md](./harmony/tree/usage.md)(组合方案) | [N/A](./flutter/tree/widget.md)(Flutter 无原生 Tree) | [component.md](./element/tree/component.md) + [api.md](./element/tree/api.md) |
| alert | 警告提示(element=静态横幅;flutter/harmony=模态警示弹窗) | [component.md](./harmony/alert/component.md) + [usage.md](./harmony/alert/usage.md) | [widget.md](./flutter/alert/widget.md) + [properties.md](./flutter/alert/properties.md) | [component.md](./element/alert/component.md) + [api.md](./element/alert/api.md) |
| loading | 加载指示 | [component.md](./harmony/loading/component.md) + [usage.md](./harmony/loading/usage.md) | [widget.md](./flutter/loading/widget.md) + [properties.md](./flutter/loading/properties.md) | [component.md](./element/loading/component.md) + [api.md](./element/loading/api.md) |
| skeleton | 骨架屏 | [component.md](./harmony/skeleton/component.md) + [usage.md](./harmony/skeleton/usage.md)(组合方案) | [N/A](./flutter/skeleton/widget.md)(Flutter 无原生 Skeleton) | [component.md](./element/skeleton/component.md) + [api.md](./element/skeleton/api.md) |
| breadcrumb | 面包屑导航 | [component.md](./harmony/breadcrumb/component.md) + [usage.md](./harmony/breadcrumb/usage.md)(组合方案) | [N/A](./flutter/breadcrumb/widget.md)(Flutter 无原生 Breadcrumb) | [component.md](./element/breadcrumb/component.md) + [api.md](./element/breadcrumb/api.md) |
| dropdown | 下拉选择菜单 | [component.md](./harmony/dropdown/component.md) + [usage.md](./harmony/dropdown/usage.md)(组合方案) | [widget.md](./flutter/dropdown/widget.md) + [properties.md](./flutter/dropdown/properties.md) | [component.md](./element/dropdown/component.md) + [api.md](./element/dropdown/api.md) |
| tag | 标签/Chip | [component.md](./harmony/tag/component.md) + [usage.md](./harmony/tag/usage.md) | [widget.md](./flutter/tag/widget.md) + [properties.md](./flutter/tag/properties.md)(Flutter 用 Chip) | [component.md](./element/tag/component.md) + [api.md](./element/tag/api.md) |
| avatar | 头像 | [component.md](./harmony/avatar/component.md) + [usage.md](./harmony/avatar/usage.md) | [widget.md](./flutter/avatar/widget.md) + [properties.md](./flutter/avatar/properties.md)(Flutter 用 CircleAvatar) | [component.md](./element/avatar/component.md) + [api.md](./element/avatar/api.md) |
| badge | 角标/徽章 | [component.md](./harmony/badge/component.md) + [usage.md](./harmony/badge/usage.md) | [widget.md](./flutter/badge/widget.md) + [properties.md](./flutter/badge/properties.md) | [component.md](./element/badge/component.md) + [api.md](./element/badge/api.md) |
| pagination | 分页 | [component.md](./harmony/pagination/component.md) + [usage.md](./harmony/pagination/usage.md)(组合方案) | [N/A](./flutter/pagination/widget.md)(Flutter 无原生 Pagination) | [component.md](./element/pagination/component.md) + [api.md](./element/pagination/api.md) |
| timeline | 时间线 | [component.md](./harmony/timeline/component.md) + [usage.md](./harmony/timeline/usage.md)(组合方案) | [N/A](./flutter/timeline/widget.md)(Flutter 无原生 Timeline) | [component.md](./element/timeline/component.md) + [api.md](./element/timeline/api.md) |
| calendar | 日历 | [component.md](./harmony/calendar/component.md) + [usage.md](./harmony/calendar/usage.md) | [widget.md](./flutter/calendar/widget.md) + [properties.md](./flutter/calendar/properties.md) | [component.md](./element/calendar/component.md) + [api.md](./element/calendar/api.md) |
| collapse | 折叠面板 | [component.md](./harmony/collapse/component.md) + [usage.md](./harmony/collapse/usage.md)(组合方案) | [widget.md](./flutter/collapse/widget.md) + [properties.md](./flutter/collapse/properties.md)(Flutter 用 ExpansionTile) | [component.md](./element/collapse/component.md) + [api.md](./element/collapse/api.md) |
| steps | 步骤条 | [component.md](./harmony/steps/component.md) + [usage.md](./harmony/steps/usage.md)(组合方案) | [widget.md](./flutter/steps/widget.md) + [properties.md](./flutter/steps/properties.md) | [component.md](./element/steps/component.md) + [api.md](./element/steps/api.md) |
| divider | 分割线 | [component.md](./harmony/divider/component.md) + [usage.md](./harmony/divider/usage.md) | [widget.md](./flutter/divider/widget.md) + [properties.md](./flutter/divider/properties.md) | [component.md](./element/divider/component.md) + [api.md](./element/divider/api.md) |
| segmented | 分段控制器(互斥切换) | [component.md](./harmony/segmented/component.md) + [usage.md](./harmony/segmented/usage.md)(ArkTS 原生名 SegmentButton) | [widget.md](./flutter/segmented/widget.md) + [properties.md](./flutter/segmented/properties.md)(Flutter 原生名 SegmentedButton) | [component.md](./element/segmented/component.md) + [api.md](./element/segmented/api.md)(2.7+) |
| rate | 评分(星级输入/展示) | [component.md](./harmony/rate/component.md) + [usage.md](./harmony/rate/usage.md)(ArkTS 原生名 Rating) | [widget.md](./flutter/rate/widget.md) + [properties.md](./flutter/rate/properties.md)(组合方案:Row + Icon) | [component.md](./element/rate/component.md) + [api.md](./element/rate/api.md) |
| popconfirm | 气泡二次确认(破坏性操作) | [component.md](./harmony/popconfirm/component.md) + [usage.md](./harmony/popconfirm/usage.md)(组合方案:bindPopup 自定义) | [widget.md](./flutter/popconfirm/widget.md) + [properties.md](./flutter/popconfirm/properties.md)(组合方案:showDialog 紧凑弹窗) | [component.md](./element/popconfirm/component.md) + [api.md](./element/popconfirm/api.md) |
| fab | 悬浮操作按钮 | [component.md](./harmony/fab/component.md) + [usage.md](./harmony/fab/usage.md)(组合方案:Stack + 圆形 Button) | [widget.md](./flutter/fab/widget.md) + [properties.md](./flutter/fab/properties.md)(Flutter 原生名 FloatingActionButton) | [component.md](./element/fab/component.md) + [api.md](./element/fab/api.md)(组合方案:fixed 定位 + el-button) |
| statistic | 统计数值/键值对详情 | [component.md](./harmony/statistic/component.md) + [usage.md](./harmony/statistic/usage.md)(组合方案:Text 组合) | [widget.md](./flutter/statistic/widget.md) + [properties.md](./flutter/statistic/properties.md)(组合方案:Text + Row/Table) | [component.md](./element/statistic/component.md) + [api.md](./element/statistic/api.md)(el-statistic/el-descriptions) |

---

## 运行时 × 组件源两级选型表

> **选型权在用户**:下表只呈现候选与适用场景,skill 只提醒"哪个更优",不锁定(契约见 [adapter-contract.md](./adapter-contract.md)「用户强制指定门」)。draw-* 遇未指定组件源时:探测项目栈 → 按本表呈现候选(已装排前) → 用户指定 → 回写 DESIGN.md 决策账本。

### 第一级·运行时

| 运行时 | 判据(用户项目信号) |
| ------ | ------------------ |
| react | package.json 含 react(或 Next.js/Remix/Astro/Vite 等框架壳) |
| vue | package.json 含 vue |
| arkts | ArkTS 工程结构(oh-package.json5 / module.json5) |
| flutter | pubspec.yaml 存在 |

### 第二级·组件源

React 生态三源详表:

| | shadcn/ui | Motif | Astryx |
| ---- | --------- | ----- | ------ |
| 形态 | 复制粘贴组件集(源码进项目) | shadcn 第三方 registry,专项部件集 | npm 设计系统(React 19 + StyleX) |
| ingest 通道 | registry-json(官方 registry JSON) | registry-json(llms.txt + 任意 URL 加 .md) | docs-site(astryx.atmeta.com + Storybook) |
| 最适合 | 需要自定义设计的简洁 Web 应用 / 后台管理页;要持有并修改组件源码 | Agent/AI 产品界面:对话流、agent 运行块、生成式媒体控件;给已有 shadcn 项目补件 | 要完整设计系统(foundations + components + patterns + 7 主题包)与 npm 正式依赖的 React 新项目 |
| 慎用 | 密集企业级复杂组件(高级表格/树表需另配 TanStack 等) | 当通用后台全量库用(它是专项集,不是全量库) | Beta 成熟度;StyleX 生态小、第三方插件少 |
| 风险标记 | 源码自持,升级靠手动 diff | 无版本锚点,内容会漂移 | Beta |
| token 契合度 | 高(CSS 变量 + Tailwind) | 高(官方明说沿用 shadcn 主题 token) | 中(StyleX 变量 + 主题包) |

六源全景速查:

| 组件源 | 运行时 | ingest 通道 | 一句话适用 | 风险标记 |
| ------ | ------ | ----------- | ---------- | -------- |
| ArkUI/ArkTS | arkts | bundled-snapshot(官网 JS 渲染抓取已证失败,见「API 基线」) | 鸿蒙原生应用,唯一源 | 快照滞后需人工复核基线 |
| Flutter(Material/Cupertino) | flutter | docs-site | 跨平台移动,自绘引擎视觉一致性最高 | GitHub Releases 已停更,版本以 releases JSON 为准 |
| Element Plus | vue | docs-site(bundled 快照回退) | Web 后台管理,企业密集组件最全,中文文档完善 | 快照基线滞后时以实时抓取为准 |
| shadcn/ui | react | registry-json | 需要自定义设计的简洁 Web 应用 / 管理页 | 源码自持,升级靠手动 diff |
| Motif | react | registry-json | Agent/AI 产品界面专项部件 | 无版本锚点,内容会漂移 |
| Astryx | react | docs-site | 要完整设计系统 + npm 依赖的 React 新项目 | Beta 成熟度 |

混用规则:

| 组合 | 结论 |
| ---- | ---- |
| shadcn/ui + Motif | 可混(同一 token 体系;registry 依赖自动带入)。主源缺件经用户确认后补齐,产出标注混合来源 |
| Astryx + Tailwind 系(shadcn/Motif) | 不可混(StyleX 与 Tailwind 两套样式引擎,同页冲突) |

## 新增框架接入流程

新运行时或新组件源一律**实时查询、不预写快照**——接入 = 登记一份组件源 profile,禁止为新框架手写全套组件文档。快照仅为官网程序化抓取失败的框架保留(当前 ArkUI)。

1. 按 [adapter-contract.md](./adapter-contract.md) 契约 8 字段新建组件源 profile(在 adapter-contract.md「两层结构」实例表登记,8 字段落全);
2. 更新本文件「运行时 × 组件源两级选型表」(速查表加一行;React 系新源另补详表列);
3. 登记「组件词典」:统一 slug ↔ 框架原生名(原生名不一致类先按「命名 slug 统一约定」登记 slug);
4. 确认 preview 通道:react 系源 → `react` 模板;全新运行时需先扩 `scripts/preview.py` 模板注册表;
5. **不建**组件类型索引表列——组件清单以 profile 组件词典 + 官方组件列表实时抓取为准;
6. 核对对应 draw-* 命令文档失败模式表的三级回退适用性(官网实时抓 → 快照回退 → 组合兜底);
7. 「文档维护规范」的「新增组件流程」仅适用于 bundled-snapshot 型源;实时型源新增组件类 = 更新 profile 组件词典。

---

## N/A 占位说明

部分组件在某框架无原生对应时,仍创建目录与 2 个文件,但内容为 N/A 说明(缺失原因 + 替代方案 + 跨框架对照),保持目录结构对称。

| 框架 | N/A 组件 | 数量 |
| ---- | -------- | ---- |
| HarmonyOS(ArkTS) | form, scroll | 2 类 |
| Flutter(Dart) | popover, tree, skeleton, breadcrumb, pagination, timeline | 6 类 |
| Element Plus(Vue 3) | gesture, a11y, video | 3 类 |
| **合计** | | **11 类**(对应 22 个 N/A 占位文件) |

---

## 命名 slug 统一约定

为跨框架一致性,以下 9 类原生名不一致的组件统一采用固定 slug;其中 8 类 slug 取自 Element 原生名(kebab-case 形式),仅 fab 因 Element 无原生组件(组合方案实现)而沿用 Flutter 原生名 FloatingActionButton 的缩写:

| 概念 | ArkTS 原生名 | Flutter 原生名 | Element 原生名 | 统一 slug |
| ---- | ------------ | -------------- | -------------- | --------- |
| 轮播 | Swiper | CarouselView | Carousel | `carousel` |
| 开关 | Toggle | Switch | Switch | `switch` |
| 气泡/提示 | Popup | (无) | Popover/Tooltip/Popconfirm | `popover` |
| 即时反馈 | Toast | SnackBar | Message | `message` |
| 抽屉/模态 | bindSheet | Drawer | Drawer | `drawer` |
| 分段控制 | SegmentButton | SegmentedButton | Segmented | `segmented` |
| 评分 | Rating | (无,组合方案) | Rate | `rate` |
| 悬浮按钮 | (无,组合方案) | FloatingActionButton | (无,组合方案) | `fab` |
| 日期录入 | DatePickerDialog | showDatePicker | DatePicker | `date-picker` |

各框架文档内部注明原生名,目录名统一用 slug。

---

## 文档维护规范

### 目录约定

每个框架下的组件目录遵循该框架生态的术语惯例:

| 框架 | 文件名惯例 | 含义 |
| ---- | ---------- | ---- |
| HarmonyOS | `component.md` + `usage.md` | 组件 API 定义 + 使用场景示例 |
| Flutter | `widget.md` + `properties.md` | Widget 定义与构造函数 + 属性列表与默认值 |
| Element Plus | `component.md` + `api.md` | 组件用法与示例 + API 属性/事件/方法表 |

### 新增组件流程

1. 在 `references/framework/<framework>/` 下新建组件目录(kebab-case 命名,跨框架统一 slug)
2. 按该框架的文件名惯例创建两份文档
3. 更新本文件的组件类型索引表,新增一行(按 P0/P1/P2 优先级归类),并填写描述列(≤15 字中文短语,格式'是什么 + 用途')
4. 同步 [`component-routing.md`](./component-routing.md) 路由表:新类若命中某个区块功能行,更新该行推荐组合;无命中不改动
5. 在对应框架的 `draw-<framework>.md` 子命令流程文档中补充组件映射条目
6. 在主文档末尾添加 `## 参考链接` 章节,引用官方文档 URL

### 文档内容要求

- **节名跨框架统一**(2026-10 起书面标准):三框架的主文档统一节名——component.md / widget.md 的示例节叫「最小示例」,api.md / properties.md 按各框架既有节名;「注意事项」节**有值得注意的运行时陷阱或平台差异时必写**,确无内容的不设该节(不做空节凑数)。「关联组件」节有真实关联时写,无则不设。示例节改名已落地:element 46 份 component.md「基本用法」→「最小示例」,与 flutter/harmony 对齐。
- **component.md / widget.md**:组件定义、构造函数/标签、核心 API、最小示例代码、`## 参考链接` 章节
- **usage.md / properties.md / api.md**:使用场景、属性列表、事件/方法、完整示例、注意事项
- 所有示例代码 MUST 标注语言标签(```arkts / ```dart / ```vue)
- 属性值如涉及 design token,用 `{token-name}` 引用(与 draw-md 产出一致)
- N/A 占位文件 MUST 包含:缺失原因、替代方案、跨框架对照、参考链接
