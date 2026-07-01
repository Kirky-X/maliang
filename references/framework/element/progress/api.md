# Progress API

> `<el-progress>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名           | 类型                                                                 | 默认值    | 说明                                                       |
| ---------------- | -------------------------------------------------------------------- | --------- | ---------------------------------------------------------- |
| `percentage`     | `number`                                                             | `0`       | 百分比(0-100)                                           |
| `type`           | `'line' \| 'circle' \| 'dashboard'`                                  | `'line'`  | 类型                                                       |
| `stroke-width`   | `number`                                                             | `6`       | 进度条线宽                                                 |
| `width`          | `number`                                                             | `126`     | 环形/仪表盘画布宽度                                        |
| `show-text`      | `boolean`                                                            | `true`    | 是否显示文字                                               |
| `stroke-linecap` | `'butt' \| 'round' \| 'square'`                                      | `'round'` | 线条端点形状                                               |
| `text-inside`    | `boolean`                                                            | `false`   | 文字是否内显(line 类型)                                   |
| `status`         | `'success' \| 'exception' \| 'warning'`                              | —         | 状态,映射 {color-success}/{color-danger}/{color-warning} |
| `indeterminate`  | `boolean`                                                            | `false`   | 是否不确定(动画往返)                                     |
| `duration`       | `number`                                                             | `3`       | 动画周期(s)                                              |
| `color`          | `string \| Array<{ color: string, percentage: number }>`             | —         | 进度条颜色,支持按百分比阶梯                              |
| `striped`        | `boolean`                                                            | `false`   | 是否显示条纹                                               |
| `striped-flow`   | `boolean`                                                            | `false`   | 条纹是否流动                                               |
| `format`         | `(percentage: number) => string`                                     | —         | 自定义文字格式化                                           |

## 事件(Events)

`<el-progress>` 不对外抛出专用事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明                                      |
| --------- | ----------------------------------------- |
| `default` | 自定义显示内容(作用域参数 `{ percentage }`) |
