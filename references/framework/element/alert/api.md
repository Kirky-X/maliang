# Alert API

> `<el-alert>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名        | 类型                                              | 默认值    | 说明                                                  |
| ------------- | ------------------------------------------------- | --------- | ----------------------------------------------------- |
| `title`       | `string`                                          | —         | 标题                                                  |
| `type`        | `'success' \| 'warning' \| 'info' \| 'error'`     | `'info'`  | 类型,映射 {color-success}/…                         |
| `description` | `string`                                          | —         | 辅助文字                                              |
| `closable`    | `boolean`                                         | `true`    | 是否可关闭                                            |
| `center`      | `boolean`                                         | `false`   | 文字是否居中                                          |
| `close-text`  | `string`                                          | —         | 关闭按钮文字(closable 为 true 时)                 |
| `show-icon`   | `boolean`                                         | `false`   | 是否显示图标                                          |
| `effect`      | `'light' \| 'dark'`                               | `'light'` | 主题                                                  |

## 事件(Events)

| 事件名   | 回调签名     | 说明           |
| -------- | ------------ | -------------- |
| `close`  | `() => void` | 关闭时触发     |

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名        | 说明                          |
| ------------- | ----------------------------- |
| `default`     | 警告内容(辅助文字)         |
| `title`       | 标题内容                      |
