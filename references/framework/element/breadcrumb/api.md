# Breadcrumb API

> `<el-breadcrumb>` 与 `<el-breadcrumb-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-breadcrumb 属性(Props)

| 属性名           | 类型        | 默认值 | 说明                          |
| ---------------- | ----------- | ------ | ----------------------------- |
| `separator`      | `string`    | `'/'`  | 分隔符                        |
| `separator-icon` | `Component` | —      | 图标分隔符(优先于 separator)|

## el-breadcrumb-item 属性(Props)

| 属性名    | 类型      | 默认值 | 说明                          |
| --------- | --------- | ------ | ----------------------------- |
| `to`      | `object`  | —      | 路由跳转对象                  |
| `replace` | `boolean` | `false`| 是否使用 replace 路由         |

## 事件(Events)

无对外事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 组件                  | 插槽名    | 说明               |
| --------------------- | --------- | ------------------ |
| `el-breadcrumb`       | `default` | 面包屑项内容       |
| `el-breadcrumb-item`  | `default` | 单项文字/图标      |
