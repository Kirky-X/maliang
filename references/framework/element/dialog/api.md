# Dialog API

> `<el-dialog>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名          | 类型                              | 默认值   | 说明                                              |
| --------------- | --------------------------------- | -------- | ------------------------------------------------- |
| `model-value` / `v-model` | `boolean`                 | —        | 是否显示                                          |
| `title`         | `string`                          | `''`     | 标题                                              |
| `width`         | `string \| number`                | `50%`    | 宽度                                              |
| `top`           | `string`                          | `'15vh'` | 距顶部高度(align-center 时无效)                 |
| `modal`         | `boolean`                         | `true`   | 是否显示遮罩                                      |
| `modal-class`   | `string`                          | —        | 自定义遮罩类名                                    |
| `append-to-body`| `boolean`                         | `false`  | 是否追加到 body(嵌套场景)                       |
| `lock-scroll`   | `boolean`                         | `true`   | 是否锁定 body 滚动                                |
| `open-delay`    | `number`                          | `0`      | 打开延迟(ms)                                    |
| `close-delay`   | `number`                          | `0`      | 关闭延迟(ms)                                    |
| `close-on-click-modal` | `boolean`                  | `true`   | 点击遮罩是否关闭                                  |
| `close-on-press-escape` | `boolean`                 | `true`   | ESC 是否关闭                                      |
| `show-close`    | `boolean`                         | `true`   | 是否显示关闭按钮                                  |
| `before-close`  | `(done: () => void) => void`      | —        | 关闭前回调,需手动调用 done                       |
| `draggable`     | `boolean`                         | `false`  | 是否可拖拽                                        |
| `overflow`      | `boolean`                         | `false`  | draggable 时是否允许拖出视口                      |
| `align-center`  | `boolean`                         | `false`  | 是否垂直水平居中                                  |
| `center`        | `boolean`                         | `false`  | 标题与底部按钮是否居中                            |
| `destroy-on-close` | `boolean`                      | `false`  | 关闭时是否销毁元素                                |
| `fullscreen`    | `boolean`                         | `false`  | 是否全屏                                          |
| `z-index`       | `number`                          | —        | 层级(默认由 z-index 管理)                       |

## 事件(Events)

| 事件名       | 回调签名         | 说明                              |
| ------------ | ---------------- | --------------------------------- |
| `open`       | `() => void`     | 打开动画开始时触发                |
| `opened`     | `() => void`     | 打开动画结束时触发                |
| `close`      | `() => void`     | 关闭动画开始时触发                |
| `closed`     | `() => void`     | 关闭动画结束时触发                |
| `open-auto-focus` | `() => void` | 打开后自动聚焦时触发              |
| `close-auto-focus`| `() => void` | 关闭后自动聚焦时触发              |

## 方法(Methods)

无对外暴露专用方法,通过 `v-model` 控制显隐。

## 插槽(Slots)

| 插槽名    | 说明                                     |
| --------- | ---------------------------------------- |
| `default` | 主体内容                                 |
| `header`  | 标题区,作用域参数 `{ close, titleId, titleClass }` |
| `footer`  | 底部操作区                               |
