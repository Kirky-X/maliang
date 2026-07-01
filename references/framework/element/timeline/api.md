# Timeline API

> `<el-timeline>` 与 `<el-timeline-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-timeline 属性(Props)

| 属性名        | 类型      | 默认值  | 说明                          |
| ------------- | --------- | ------- | ----------------------------- |
| `reverse`     | `boolean` | `false` | 是否倒序                      |

## el-timeline-item 属性(Props)

| 属性名       | 类型                                                              | 默认值  | 说明                          |
| ------------ | ----------------------------------------------------------------- | ------- | ----------------------------- |
| `timestamp`  | `string`                                                          | —       | 时间戳                        |
| `hide-timestamp` | `boolean`                                                     | `false` | 是否隐藏时间戳                |
| `placement`  | `'top' \| 'bottom'`                                               | `'bottom'` | 时间戳位置                 |
| `type`       | `'primary' \| 'success' \| 'warning' \| 'danger' \| 'info'`       | —       | 节点颜色                      |
| `size`       | `'normal' \| 'large'`                                             | `'normal'` | 节点尺寸                   |
| `hollow`     | `boolean`                                                         | `false` | 是否空心                      |

## 事件(Events)

无对外事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 组件                 | 插槽名    | 说明                          |
| -------------------- | --------- | ----------------------------- |
| `el-timeline`        | `default` | 时间线内容                    |
| `el-timeline-item`   | `default` | 节点内容                      |
| `el-timeline-item`   | `dot`     | 自定义节点图标                |
| `el-timeline-item`   | `timestamp` | 自定义时间戳                |
