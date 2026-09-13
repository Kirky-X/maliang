# Statistic API

> `<el-statistic>` / `<el-descriptions>` / `<el-descriptions-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-statistic 属性(Props)

| 属性名          | 类型                                        | 默认值   | 说明                                        |
| --------------- | ------------------------------------------- | -------- | ------------------------------------------- |
| `value`         | `number`                                    | 必填     | 数值(千分位自动分隔)                     |
| `decimal-separator` | `string`                                | `'.'`    | 小数分隔符                                  |
| `group-separator` | `string`                                  | `','`    | 千分位分隔符(置空关闭)                  |
| `precision`     | `number`                                    | `0`      | 小数位数                                    |
| `formatter`     | `(value: number) => string`                 | —        | 自定义格式化(覆盖 precision/分隔符)     |
| `prefix` / `suffix` | `string \| VNode`                       | —        | 前缀(¥)/ 后缀(单位、delta)             |
| `title`         | `string \| VNode`                           | —        | 标签文字                                    |
| `value-style`   | `CSSProperties`                             | —        | 数值样式(字号/字重/token)               |
| `duration`      | `number`                                    | —        | 数字滚动动画时长(ms)                     |

## el-descriptions 属性(Props)

| 属性名           | 类型                                  | 默认值     | 说明                                       |
| ---------------- | ------------------------------------- | ---------- | ------------------------------------------ |
| `border`         | `boolean`                             | `false`    | 表格式分块(键列底色)                   |
| `column`         | `number`                              | `3`(响应式)| 每行列数(移动端建议 1-2)              |
| `direction`      | `'horizontal' \| 'vertical'`          | `'horizontal'` | 键值排列方向                            |
| `size`           | `'large' \| 'default' \| 'small'`     | —          | 尺寸                                       |
| `title` / `extra`| `string \| VNode`                     | —          | 标题 / 操作区(右上角)                  |
| `label-class-name` / `label-align` | `string` / `'left' \| 'center' \| 'right'` | — | 键列类名 / 对齐                     |

## el-descriptions-item 属性(Props)

| 属性名    | 类型                                        | 默认值 | 说明                       |
| --------- | --------------------------------------------- | ------ | -------------------------- |
| `label`   | `string \| VNode`                             | —      | 键名                       |
| `width` / `min-width` | `number \| string`                | —      | 单元格宽度                 |
| `label-width` | `number \| string`                        | —      | 键列宽(定宽 32%-40%)    |
| `align` / `label-align` | `string`                        | —      | 值/键对齐                  |
| `span`    | `number`                                      | `1`    | 占列数(长值合并)        |
| `rowspan` | `number`                                      | `1`    | 跨行                       |

## 事件 / 方法 / 插槽

- `<el-statistic>` 无事件;`<el-countdown>` 有 `change` / `finish`。
- 插槽:`title` / `prefix` / `suffix`(statistic);`title` / `extra` / `label`(descriptions)。

## 关键规格要点

- **数值排版**:KPI 数值 28-32px + 粗体 + `font-variant-numeric: tabular-nums`(等宽,刷新不跳);标签 small 次要色;delta small,涨跌色按业务语义。
- **键值排版**:键列定宽 32%-40%;`border` 模式键列底色分块;长值 `span` 合并列。
- **列数响应式**:桌面 2-3 列,移动端 1 列(column 属性或栅格控制)。
- **无障碍**:statistic 读屏顺序"标题 → 值 → 后缀";delta 必须带词("涨 12.4%"),箭头仅视觉;descriptions 每项播报"键:值"。
