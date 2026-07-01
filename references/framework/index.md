# 框架资源总览

> 本文件是 `references/framework/` 分层框架文档数据库的入口,为 `draw-harmony` / `draw-flutter` / `draw-element` 三个子命令提供组件映射参考。
> 每个框架下按组件类型组织(共 45 类,3 现有 + 42 新增),每类组件含两份文档(文件名遵循各框架生态术语惯例)。
> 部分组件在某框架无原生对应时,以 N/A 占位文件说明缺失原因与替代方案,保持目录结构对称。

---

## 组件类型索引表

### 现有组件(3 类)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| button | 触发操作的按钮 | [component.md](./harmony/button/component.md) + [usage.md](./harmony/button/usage.md) | [widget.md](./flutter/button/widget.md) + [properties.md](./flutter/button/properties.md) | [component.md](./element/button/component.md) + [api.md](./element/button/api.md) |
| text | 文本展示 | [component.md](./harmony/text/component.md) + [usage.md](./harmony/text/usage.md) | [widget.md](./flutter/text/widget.md) + [properties.md](./flutter/text/properties.md) | [component.md](./element/text/component.md) + [api.md](./element/text/api.md) |
| list | 行列表容器 | [component.md](./harmony/list/component.md) + [usage.md](./harmony/list/usage.md) | [widget.md](./flutter/list/widget.md) + [properties.md](./flutter/list/properties.md) | [component.md](./element/list/component.md) + [api.md](./element/list/api.md) |

### P0 类(4 类,三框架都有原生组件)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| layout | 布局容器(线性/堆叠/网格) | [component.md](./harmony/layout/component.md) + [usage.md](./harmony/layout/usage.md) | [widget.md](./flutter/layout/widget.md) + [properties.md](./flutter/layout/properties.md) | [component.md](./element/layout/component.md) + [api.md](./element/layout/api.md) |
| image | 图片展示 | [component.md](./harmony/image/component.md) + [usage.md](./harmony/image/usage.md) | [widget.md](./flutter/image/widget.md) + [properties.md](./flutter/image/properties.md) | [component.md](./element/image/component.md) + [api.md](./element/image/api.md) |
| tabs | 标签页切换 | [component.md](./harmony/tabs/component.md) + [usage.md](./harmony/tabs/usage.md) | [widget.md](./flutter/tabs/widget.md) + [properties.md](./flutter/tabs/properties.md) | [component.md](./element/tabs/component.md) + [api.md](./element/tabs/api.md) |
| input | 单行文本输入 | [component.md](./harmony/input/component.md) + [usage.md](./harmony/input/usage.md) | [widget.md](./flutter/input/widget.md) + [properties.md](./flutter/input/properties.md) | [component.md](./element/input/component.md) + [api.md](./element/input/api.md) |

### P1 类(21 类,跨框架覆盖,部分 N/A)

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

### P2 类(17 类,通用性中-高,部分单框架)

| 组件类型 | 描述 | HarmonyOS(ArkTS) | Flutter(Dart) | Element Plus(Vue 3) |
| -------- | ---- | ------------------ | ------------- | ------------------- |
| card | 卡片容器 | [component.md](./harmony/card/component.md) + [usage.md](./harmony/card/usage.md)(组合方案) | [widget.md](./flutter/card/widget.md) + [properties.md](./flutter/card/properties.md) | [component.md](./element/card/component.md) + [api.md](./element/card/api.md) |
| table | 数据表格 | [component.md](./harmony/table/component.md) + [usage.md](./harmony/table/usage.md)(组合方案) | [widget.md](./flutter/table/widget.md) + [properties.md](./flutter/table/properties.md) | [component.md](./element/table/component.md) + [api.md](./element/table/api.md) |
| tree | 树形控件 | [component.md](./harmony/tree/component.md) + [usage.md](./harmony/tree/usage.md)(组合方案) | [N/A](./flutter/tree/widget.md)(Flutter 无原生 Tree) | [component.md](./element/tree/component.md) + [api.md](./element/tree/api.md) |
| alert | 警告提示(静态) | [component.md](./harmony/alert/component.md) + [usage.md](./harmony/alert/usage.md) | [widget.md](./flutter/alert/widget.md) + [properties.md](./flutter/alert/properties.md) | [component.md](./element/alert/component.md) + [api.md](./element/alert/api.md) |
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

---

## 框架选型指南

| 场景 | 推荐框架 | 理由 |
| ---- | -------- | ---- |
| HarmonyOS 原生应用 | HarmonyOS(ArkTS) | 华为生态原生支持,ArkTS 声明式 UI 性能最优 |
| 跨平台移动应用(iOS/Android) | Flutter | 单代码库跨平台,Skia 渲染性能接近原生 |
| Web 后台管理系统 | Element Plus | Vue 3 生态成熟,组件丰富,中文文档完善 |
| 需要同时支持移动+Web | Flutter(移动)+ Element Plus(Web) | 分端实现,共享 design token 保证视觉一致 |

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

为跨框架一致性,5 类存在命名冲突的组件统一采用 Element 名作为 slug:

| 概念 | ArkTS 原生名 | Flutter 原生名 | Element 原生名 | 统一 slug |
| ---- | ------------ | -------------- | -------------- | --------- |
| 轮播 | Swiper | CarouselView | Carousel | `carousel` |
| 开关 | Toggle | Switch | Switch | `switch` |
| 气泡/提示 | Popup | (无) | Popover/Tooltip/Popconfirm | `popover` |
| 即时反馈 | Toast | SnackBar | Message | `message` |
| 抽屉/模态 | bindSheet | Drawer | Drawer | `drawer` |

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
4. 在对应框架的 `draw-<framework>.md` 子命令流程文档中补充组件映射条目
5. 在主文档末尾添加 `## 参考链接` 章节,引用官方文档 URL

### 文档内容要求

- **component.md / widget.md**:组件定义、构造函数/标签、核心 API、最小示例代码、`## 参考链接` 章节
- **usage.md / properties.md / api.md**:使用场景、属性列表、事件/方法、完整示例、注意事项
- 所有示例代码 MUST 标注语言标签(```arkts / ```dart / ```vue)
- 属性值如涉及 design token,用 `{token-name}` 引用(与 draw-md 产出一致)
- N/A 占位文件 MUST 包含:缺失原因、替代方案、跨框架对照、参考链接
