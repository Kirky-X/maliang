# Collapse API

> `<el-collapse>` 与 `<el-collapse-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-collapse 属性(Props)

| 属性名           | 类型                  | 默认值  | 说明                              |
| ---------------- | --------------------- | ------- | --------------------------------- |
| `model-value` / `v-model` | `string \| array` | —       | 展开项(name 数组;accordion 时为单个 name) |
| `accordion`      | `boolean`             | `false` | 是否手风琴模式                    |

## el-collapse-item 属性(Props)

| 属性名     | 类型               | 默认值 | 说明                          |
| ---------- | ------------------ | ------ | ----------------------------- |
| `name`     | `string \| number` | —      | 唯一标识                      |
| `title`    | `string`           | —      | 标题(可用 #title 插槽)     |
| `disabled` | `boolean`          | `false`| 是否禁用                      |

## el-collapse 事件(Events)

| 事件名    | 回调签名                                       | 说明                       |
| --------- | ---------------------------------------------- | -------------------------- |
| `change`  | `(activeNames: string \| array) => void`       | 展开项变化时触发           |

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 组件                | 插槽名    | 说明                |
| ------------------- | --------- | ------------------- |
| `el-collapse`       | `default` | 折叠项内容          |
| `el-collapse-item`  | `default` | 面板内容            |
| `el-collapse-item`  | `title`   | 自定义标题          |
