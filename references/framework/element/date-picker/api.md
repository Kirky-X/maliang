# DatePicker API

> `<el-date-picker>` / `<el-time-picker>` / `<el-time-select>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-date-picker 属性(Props,通用)

| 属性名              | 类型                                                       | 默认值     | 说明                                     |
| ------------------- | ---------------------------------------------------------- | ---------- | ---------------------------------------- |
| `model-value` / `v-model` | `Date \| string \| number \| Array`                   | —          | 绑定值(范围型为数组)                  |
| `type`              | `'date' \| 'dates' \| 'datetime' \| 'week' \| 'month' \| 'year' \| 'daterange' \| 'datetimerange' \| 'monthrange'` | `'date'` | 选择器档位 |
| `readonly`          | `boolean`                                                  | `false`    | 只读                                     |
| `disabled`          | `boolean`                                                  | `false`    | 禁用                                     |
| `size`              | `'large' \| 'default' \| 'small'`                          | —          | 尺寸                                     |
| `editable`          | `boolean`                                                  | `true`     | 文本框可输入                             |
| `clearable`         | `boolean`                                                  | `true`     | 可清空                                   |
| `placeholder`       | `string`                                                   | —          | 占位文案(范围型用 start/end-placeholder)|
| `format`            | `string`                                                   | `'YYYY-MM-DD'` | 显示格式(Day.js 格式)             |
| `value-format`      | `string`                                                   | —          | 绑定值格式(如 `'YYYY-MM-DD HH:mm:ss'`) |
| `disabled-date`     | `(date: Date) => boolean`                                  | —          | 禁选日期判定函数                         |
| `shortcuts`         | `Array<{ text, value }>`                                   | —          | 快捷选项                                 |
| `default-time`      | `Date \| Date[]`                                           | —          | 选中日期的默认时刻                       |
| `range-separator`   | `string`                                                   | `'-'`      | 范围分隔符                               |
| `unlink-panels`     | `boolean`                                                  | `false`    | 范围面板不联动                           |
| `teleported`        | `boolean`                                                  | `true`     | 面板是否插入 body                        |

## el-time-picker 属性(Props)

| 属性名           | 类型                             | 默认值    | 说明                       |
| ---------------- | -------------------------------- | --------- | -------------------------- |
| `model-value`    | `Date \| string \| number \| Array` | —      | 绑定值                     |
| `selectable-range` | `string \| string[]`           | —         | 可选时刻范围(如 `'08:00-20:00'`) |
| `format`         | `string`                         | `'HH:mm:ss'` | 显示格式                |
| `arrow-control`  | `boolean`                        | `false`   | 箭头按钮操作               |
| `is-range`       | `boolean`                        | `false`   | 时间范围                   |

## el-time-select 属性(Props)

| 属性名        | 类型     | 默认值  | 说明                              |
| ------------- | -------- | ------- | --------------------------------- |
| `model-value` | `string` | —       | 绑定值(如 `'08:30'`)           |
| `start`       | `string` | `'09:00'` | 起始时间                       |
| `end`         | `string` | `'18:00'` | 结束时间                       |
| `step`        | `string` | `'00:15'` | 间隔档位                       |
| `min-time`    | `string` | —       | 最小可选时间                     |
| `max-time`    | `string` | —       | 最大可选时间                     |

## 事件(Events)

| 事件名          | 回调签名                                | 说明                         |
| --------------- | --------------------------------------- | ---------------------------- |
| `change`        | `(value) => void`                       | 用户确认选择时触发           |
| `blur` / `focus`| `(event) => void`                       | 失焦 / 聚焦                  |
| `calendar-change` | `(dates: [Date, Date]) => void`       | 日历面板选中有变化(范围型)  |
| `panel-change`  | `(value, mode, view) => void`           | 面板年/月视图切换            |
| `visible-change` | `(visible: boolean) => void`           | 面板出现/收起                |

## 方法 / 插槽

- `focus()` / `blur()` / `handleOpen()` / `handleClose()`:实例方法。
- 插槽:`default`(触发输入框内容)、`range-separator`、`header`(面板自定义头部)、`footer`(自定义内容,配 `:clearable`)。

## 关键规格要点

- **录入 vs 浏览**:表单选值用本类;展示型日历用 `el-calendar`(calendar 类),两者交互域不同。
- **禁选策略**:`disabled-date` 范围外置灰(预订场景"今天起可选"),配合 `shortcuts` 快捷档。
- **尺寸**:默认高 32px,`large` 40px,`small` 24px。
- **无障碍**:输入框有 label(表单内配 el-form-item);面板方向键导航 + Enter 确认;`value-format` 建议显式声明避免绑定值类型漂移。
