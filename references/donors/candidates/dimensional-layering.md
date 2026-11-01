<!-- 供体候选池快照(中文译本,非蒸馏供体;原文见「原始出处」)。
     站点分组: 通用风格模板(styleGeneral) · 站点摘要: Dimensional Layering 是为通用界面提供的 UI 风格参照,侧重深度、重叠、z-index、层、3D。
     站点色板: #ffffff, #f5f5f5, #e0e0e0
     晋升正式供体须满足 ../README.md §5 三条件;蒸馏稿另立 ../<id>.md,与本快照并存。 -->

# Dimensional Layering

## 1. 视觉主题与氛围

Dimensional Layering 是为通用界面提供的 UI 风格参照,融合深度、重叠、z-index、层、3D、阴影、海拔、浮动、卡片、空间层级。视觉方向由 z-index 堆叠、box-shadow 海拔(4 级)、transform: translateZ()、backdrop-filter、视差塑造。

用于仪表板、卡片布局、模态、导航、产品展示、SaaS 界面。避免用于印刷式布局、简单博客、低端设备、扁平设计要求。

**关键特征:**
- 主色板:中性基底(#FFFFFF、#F5F5F5、#E0E0E0)+ 用于抬升元素的品牌强调色
- 次色板:阴影变化(sm/md/lg/xl)、海拔色、顶层高光色
- 效果:z-index 堆叠、box-shadow 海拔(4 级)、transform: translateZ()、backdrop-filter、视差
- 无障碍:⚠ 中等(屏幕阅读器问题);性能:⚠ 良好;暗色模式:✓ 完整。
- 最适用于:仪表板、卡片布局、模态、导航、产品展示、SaaS 界面
- 避免用于:印刷式布局、简单博客、低端设备、扁平设计要求

## 2. 实现要点

- 框架适配:Tailwind 10/10、MUI 10/10、Chakra 10/10
- 年代参照:2020 年代现代
- 本地预览:[打开 HTML 预览](../../refstyles/46-dimensional-layering.html)
- 库索引:[打开 UI/UX Pro Max 首页](../../index.html)
