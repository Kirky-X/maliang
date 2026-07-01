# Image API

> `<el-image>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名              | 类型                  | 默认值     | 说明                                                        |
| ------------------- | --------------------- | ---------- | ----------------------------------------------------------- |
| `src`               | `string`              | `''`       | 图片地址                                                    |
| `fit`               | `'contain' \| 'cover' \| 'fill' \| 'none' \| 'scale-down'` | `'none'` | 同原生 object-fit                                          |
| `lazy`              | `boolean`             | `false`    | 是否开启懒加载                                              |
| `scroll-container`  | `string \| HTMLElement` | —        | 开启懒加载后的滚动容器选择器或元素                          |
| `alt`               | `string`              | `''`       | 原生 alt                                                    |
| `referrerpolicy`    | `string`              | —          | 原生 referrerpolicy                                         |
| `hide-on-click-modal`| `boolean`            | `false`    | 预览模式下点击遮罩是否关闭                                  |
| `preview-src-list`  | `string[]`            | `[]`       | 开启图片预览的地址列表                                      |
| `preview-teleported`| `boolean`             | `false`    | 预览是否 teleport 到 body                                   |
| `z-index`           | `number`              | `2000`     | 预览层级                                                    |
| `initial-index`     | `number`              | `0`        | 预览初始索引                                                |
| `infinite`          | `boolean`             | `true`     | 预览是否无限循环                                            |
| `zoom-rate`         | `number`              | `1.2`      | 预览缩放比率                                                |
| `min-scale`         | `number`              | `0.2`      | 预览最小缩放                                                |
| `max-scale`         | `number`              | `7`        | 预览最大缩放                                                |
| `crossorigin`       | `string`              | —          | 原生 crossorigin                                            |

## 事件(Events)

| 事件名   | 回调签名                | 说明                 |
| -------- | ----------------------- | -------------------- |
| `load`   | `(e: Event) => void`    | 图片加载成功时触发   |
| `error`  | `(e: Error) => void`    | 图片加载失败时触发   |
| `switch` | `(val: number) => void` | 预览切换图片时触发   |
| `close`  | `() => void`            | 预览关闭时触发       |
| `show`   | `() => void`            | 预览打开时触发       |

## 方法(Methods)

| 方法           | 签名             | 说明                          |
| -------------- | ---------------- | ----------------------------- |
| `setShowItems` | `(urls) => void` | 设置预览图片列表(动态更新) |

## 插槽(Slots)

| 插槽名        | 说明                           |
| ------------- | ------------------------------ |
| `placeholder` | 图片加载中的占位内容           |
| `error`       | 加载失败的内容                 |
| `viewer`      | 自定义预览结构(高级)         |
