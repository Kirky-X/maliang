# Scroll 组件 API 文档

> **本框架无独立 Scroll 指南页。**

## 缺失原因

ArkTS 官方文档没有独立的 "Scroll 组件" 章节页。滚动能力由 `List` / `Grid` / `Scroll`(容器组件,散落在布局与列表章节) / `WaterFlow` 分散承载。虽然存在 `Scroll` 容器组件,但其用法与 List/Grid 高度重合,官方未单独成页,而是归入"列表与网格"统一介绍。

## 替代方案

- **方案 1:Scroll 容器组件** — `Scroll()` 包裹任意内容,支持纵向/横向滚动,适合内容超出屏幕但非列表结构的场景(如长表单、详情页)。
- **方案 2:List 组件** — 列表场景首选 `List` + `ListItem`,自带性能优化、粘性头部、下拉刷新等能力。
- **方案 3:Grid 组件** — 二维网格滚动用 `Grid`。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无独立指南页(本文件);Scroll 容器组件散在列表章节 |
| Flutter | `SingleChildScrollView` / `ListView` / `CustomScrollView` |
| Element Plus | `<el-scrollbar>` 包裹任意内容 |

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为说明占位)
- 相关组件:[`list`](../list/component.md) / [`grid`](../grid/component.md)
- 列表与网格概述: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-list-grid-development-overview
- 创建列表 (List): https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-layout-development-create-list
