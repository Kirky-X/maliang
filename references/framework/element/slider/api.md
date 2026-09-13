# Slider API

> `<el-slider>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-slider 属性(Props)

| 属性名            | 类型                                          | 默认值    | 说明                                     |
| ----------------- | --------------------------------------------- | --------- | ---------------------------------------- |
| `model-value` / `v-model` | `number \| [number, number]`          | `0`       | 绑定值(range 时为区间数组)            |
| `min` / `max`     | `number`                                      | `0` / `100` | 数值范围                               |
| `step`            | `number`                                      | `1`       | 步长(离散粒度)                        |
| `range`           | `boolean`                                     | `false`   | 双滑块区间模式                           |
| `disabled`        | `boolean`                                     | `false`   | 是否禁用                                 |
| `show-input`      | `boolean`                                     | `false`   | 是否显示数值输入框(单滑块模式)        |
| `show-input-controls` | `boolean`                                 | `true`    | 输入框步进按钮                           |
| `input-size`      | `'large' \| 'default' \| 'small'`             | `'small'` | 输入框尺寸                               |
| `show-steps`      | `boolean`                                     | `false`   | 是否显示刻度点                           |
| `show-tooltip`    | `boolean`                                     | `true`    | 拖动时是否显示值气泡                     |
| `format-tooltip`  | `(val: number) => string \| number`           | —         | 气泡文案格式化(如 `¥${v}`)            |
| `marks`           | `Record<number, string \| MarkOption>`        | —         | 刻度标记                                 |
| `vertical`        | `boolean`                                     | `false`   | 垂直方向(需设 height)                 |
| `height`          | `string`                                      | —         | 垂直模式高度(如 `'200px'`)            |
| `tooltip-class`   | `string`                                      | —         | 气泡自定义类名                           |

## 事件(Events)

| 事件名         | 回调签名                            | 说明                       |
| -------------- | ----------------------------------- | -------------------------- |
| `change`       | `(value: number \| [number, number]) => void` | 拖动/键入**结束**时触发(业务触发点) |
| `input`        | `(value: number \| [number, number]) => void` | 拖动中实时触发(预览用)   |

## 方法 / 插槽

- `focus()`:聚焦滑块。
- 插槽:`mark`(自定义刻度标签内容)。

## 关键规格要点

- **input vs change**:`input` 拖动中高频触发只做轻量预览;业务请求/落库一律挂 `change`(松手触发),与三阶段拖动语义一致。
- **区间钳制**:`range` 模式双滑块自动保证 min ≤ max,最小间隔由 `step` 决定。
- **尺寸**:默认轨道高 6px、滑块 20px;`vertical` 时需显式 `height`。
- **无障碍**:滑块为 `role="slider"` 语义(`aria-valuenow/min/max` 自动维护);方向键按 `step` 调节;气泡文案建议经 `format-tooltip` 本地化(读屏播报同步)。
