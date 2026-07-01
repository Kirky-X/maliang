# Tag API

> `<el-tag>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名     | 类型                                              | 默认值    | 说明                                              |
| ---------- | ------------------------------------------------- | --------- | ------------------------------------------------- |
| `type`     | `'primary' \| 'success' \| 'warning' \| 'danger' \| 'info'` | `''` | 类型,映射功能色 token                          |
| `closable` | `boolean`                                         | `false`   | 是否可关闭                                        |
| `disable-transitions` | `boolean`                              | `false`   | 是否禁用过渡                                      |
| `hit`      | `boolean`                                         | `false`   | 是否描边                                          |
| `color`    | `string`                                          | —         | 背景色                                            |
| `size`     | `'large' \| 'default' \| 'small'`                 | `'default'`| 尺寸                                            |
| `effect`   | `'dark' \| 'light' \| 'plain'`                    | `'light'` | 主题                                              |
| `round`    | `boolean`                                         | `false`   | 是否圆角,映射 {radius-full}                     |
| `bordered` | `boolean`                                         | `true`    | 是否显示边框                                      |

## 事件(Events)

| 事件名   | 回调签名             | 说明                       |
| -------- | -------------------- | -------------------------- |
| `click`  | `(e: MouseEvent) => void` | 点击时触发            |
| `close`  | `(e: MouseEvent) => void` | 关闭按钮点击时触发    |

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明           |
| --------- | -------------- |
| `default` | 标签内容       |
