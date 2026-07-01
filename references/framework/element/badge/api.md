# Badge API

> `<el-badge>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名        | 类型                                                                | 默认值    | 说明                                  |
| ------------- | ------------------------------------------------------------------- | --------- | ------------------------------------- |
| `value`       | `string \| number`                                                  | —         | 显示值                                |
| `max`         | `number`                                                            | `99`      | 最大值,超出显示 `max+`              |
| `is-dot`      | `boolean`                                                           | `false`   | 是否显示红点                          |
| `hidden`      | `boolean`                                                           | `false`   | 是否隐藏                              |
| `type`        | `'primary' \| 'success' \| 'warning' \| 'danger' \| 'info'`         | `'danger'`| 类型,映射功能色                    |
| `show-zero`   | `boolean`                                                           | `false`   | value 为 0 时是否显示                 |
| `color`       | `string`                                                            | —         | 自定义背景色                          |
| `badge-style` | `object`                                                            | —         | 自定义样式对象                        |
| `offset`      | `[number, number]`                                                  | —         | 偏移 [x, y]                           |

## 事件(Events)

无对外事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明                                  |
| --------- | ------------------------------------- |
| `default` | 主体内容(被徽章标注的元素)         |
| `value`   | 自定义徽章内容(支持 VNode)         |
