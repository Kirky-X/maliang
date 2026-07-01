# Drawer API

> `<el-drawer>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名                 | 类型                              | 默认值  | 说明                                          |
| ---------------------- | --------------------------------- | ------- | --------------------------------------------- |
| `model-value` / `v-model` | `boolean`                      | —       | 是否显示                                      |
| `title`                | `string`                          | —       | 标题                                          |
| `direction`            | `'rtl' \| 'ltr' \| 'ttb' \| 'btt'` | `'rtl'` | 方向(右/左/上/下)                         |
| `size`                 | `string \| number`                | `'30%'` | 尺寸                                          |
| `modal`                | `boolean`                         | `true`  | 是否显示遮罩                                  |
| `modal-class`          | `string`                          | —       | 遮罩类名                                      |
| `append-to-body`       | `boolean`                         | `false` | 是否追加到 body                               |
| `lock-scroll`          | `boolean`                         | `true`  | 是否锁定 body 滚动                            |
| `open-delay`           | `number`                          | `0`     | 打开延迟(ms)                               |
| `close-delay`          | `number`                          | `0`     | 关闭延迟(ms)                               |
| `close-on-click-modal` | `boolean`                         | `true`  | 点击遮罩是否关闭                              |
| `close-on-press-escape`| `boolean`                         | `true`  | ESC 是否关闭                                  |
| `show-close`           | `boolean`                         | `true`  | 是否显示关闭按钮                              |
| `before-close`         | `(done: () => void) => void`      | —       | 关闭前回调                                    |
| `destroy-on-close`     | `boolean`                         | `false` | 关闭时销毁元素                                |
| `with-header`          | `boolean`                         | `true`  | 是否显示头部                                  |
| `z-index`              | `number`                          | —       | 层级                                          |

## 事件(Events)

| 事件名       | 回调签名         | 说明                  |
| ------------ | ---------------- | --------------------- |
| `open`       | `() => void`     | 打开动画开始          |
| `opened`     | `() => void`     | 打开动画结束          |
| `close`      | `() => void`     | 关闭动画开始          |
| `closed`     | `() => void`     | 关闭动画结束          |
| `open-auto-focus` | `() => void` | 打开后自动聚焦        |
| `close-auto-focus`| `() => void` | 关闭后自动聚焦        |

## 方法(Methods)

无对外暴露专用方法,通过 `v-model` 控制显隐。

## 插槽(Slots)

| 插槽名    | 说明                                            |
| --------- | ----------------------------------------------- |
| `default` | 主体内容                                        |
| `header`  | 标题区,作用域参数 `{ close, titleId, titleClass }` |
| `footer`  | 底部操作区                                      |
