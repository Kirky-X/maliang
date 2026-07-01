# Avatar API

> `<el-avatar>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名    | 类型                                              | 默认值     | 说明                              |
| --------- | ------------------------------------------------- | ---------- | --------------------------------- |
| `icon`    | `string \| Component`                             | —          | 图标(无 src/插槽 时显示)        |
| `size`    | `'large' \| 'default' \| 'small' \| number`       | `'default'`| 尺寸                              |
| `shape`   | `'circle' \| 'square'`                            | `'circle'` | 形状,circle 映射 {radius-full}  |
| `src`     | `string`                                          | —          | 图片地址                          |
| `src-set` | `string`                                          | —          | 原生 srcset                       |
| `alt`     | `string`                                          | —          | 原生 alt                          |
| `fit`     | `'fill' \| 'contain' \| 'cover' \| 'none' \| 'scale-down'` | `'cover'` | 同 object-fit           |

## 事件(Events)

| 事件名  | 回调签名             | 说明                            |
| ------- | -------------------- | ------------------------------- |
| `error` | `(e: Event) => boolean` | 加载失败时触发,返回 false 阻止默认 |

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明                            |
| --------- | ------------------------------- |
| `default` | 自定义内容(图片加载失败时显示) |
