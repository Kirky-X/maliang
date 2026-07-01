# Form 组件 API 文档

> **本框架无原生 Form 容器组件。**

## 缺失原因

ArkTS 声明式 UI 没有 HTML `<form>` 那样的统一表单容器。表单由 `TextInput` / `TextArea` / `Search` / `Radio` / `Toggle` / `Select` 等独立组件,置于 `Column` 容器内组合而成。表单数据的收集与校验由开发者通过状态管理(`@State`)自行实现。

## 替代方案

- **方案 1:Column 容器 + 多个输入组件** — 用 `Column({ space })` 组织字段,每个字段绑定 `@State`,提交时统一校验。最常用。
- **方案 2:自定义 @Component 封装表单** — 将字段配置数组化,用 `ForEach` 渲染,封装校验逻辑为可复用组件。

## 跨框架对照

| 框架 | 实现方式 |
| --- | --- |
| ArkTS | 无原生 Form 容器(本文件) |
| Flutter | `Form` + `FormField` + `TextFormField`(有 GlobalKey 校验) |
| Element Plus | `<el-form>` + `<el-form-item>`(内置 rules 校验) |

## 参考链接

- ArkTS 官方文档:无独立章节(本组件为 maliang 组合方案)
- 相关组件:[`input`](../input/component.md) / [`radio`](../radio/component.md) / [`switch`](../switch/component.md)
- 文本输入组件: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-common-components-text-input
