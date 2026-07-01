# Scroll API

> `<el-scrollbar>` 属性 / 事件 / 方法 / 插槽,以及 `v-infinite-scroll` 指令参数。用法见 [component.md](./component.md)。

## el-scrollbar 属性(Props)

| 属性名           | 类型                | 默认值  | 说明                              |
| ---------------- | ------------------- | ------- | --------------------------------- |
| `height`         | `string \| number`  | —       | 高度                              |
| `max-height`     | `string \| number`  | —       | 最大高度                          |
| `native`         | `boolean`           | `false` | 是否使用原生滚动条                |
| `wrap-style`     | `string`            | —       | 内层 wrap 样式                    |
| `wrap-class`     | `string`            | —       | 内层 wrap 类名                    |
| `view-style`     | `string`            | —       | 视图样式                          |
| `view-class`     | `string`            | —       | 视图类名                          |
| `noresize`       | `boolean`           | `false` | 不响应容器尺寸变化                |
| `tag`            | `string`            | `'div'` | 视图标签                          |
| `always`         | `boolean`           | `false` | 滚动条是否常显                    |
| `min-size`       | `number`            | `20`    | 滚动条最小尺寸                    |

## el-scrollbar 事件(Events)

| 事件名   | 回调签名                      | 说明           |
| -------- | ----------------------------- | -------------- |
| `scroll` | `({ scrollTop, scrollLeft }) => void` | 滚动时触发 |

## el-scrollbar 方法(Methods)

| 方法名           | 签名                                  | 说明                       |
| ---------------- | ------------------------------------- | -------------------------- |
| `setScrollTop`   | `(value: number) => void`             | 设置滚动位置               |
| `scrollTo`       | `(options) => void`                   | 平滑滚动                   |
| `wrapRef`        | —                                     | 获取内部 wrap 元素(只读) |

## el-scrollbar 插槽(Slots)

| 插槽名    | 说明       |
| --------- | ---------- |
| `default` | 滚动内容   |

## v-infinite-scroll 指令参数

| 参数名                    | 类型      | 默认值 | 说明                              |
| ------------------------- | --------- | ------ | --------------------------------- |
| `infinite-scroll-disabled`| `boolean` | `false`| 是否禁用                          |
| `infinite-scroll-delay`   | `number`  | `200`  | 节流延迟(ms)                   |
| `infinite-scroll-distance`| `number`  | `0`    | 距底部多少 px 触发                |
| `infinite-scroll-immediate`| `boolean`| `false`| 是否立即执行(适合初始无数据)   |
