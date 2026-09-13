# Checkbox API

> `<el-checkbox>` / `<el-checkbox-group>` / `<el-checkbox-button>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-checkbox-group 属性(Props)

| 属性名           | 类型          | 默认值  | 说明                                  |
| ---------------- | ------------- | ------- | ------------------------------------- |
| `model-value` / `v-model` | `Array<string \| number \| boolean>` | — | 绑定值数组 |
| `size`           | `'large' \| 'default' \| 'small'` | — | 尺寸 |
| `disabled`       | `boolean`     | `false` | 是否禁用整组                          |
| `min`            | `number`      | —       | 可被勾选的最少数量                    |
| `max`            | `number`      | —       | 可被勾选的最多数量                    |
| `text-color`     | `string`      | `'#ffffff'` | 按钮激活时文字色                  |
| `fill`           | `string`      | `'#409eff'` | 按钮激活时填充色                  |

## el-checkbox 属性(Props)

| 属性名          | 类型                                   | 默认值  | 说明                                   |
| --------------- | -------------------------------------- | ------- | -------------------------------------- |
| `model-value` / `v-model` | `string \| number \| boolean` | —     | 独立使用时的绑定值                     |
| `value` / `label` | `string \| number \| boolean`        | —      | 选中状态下该选项的值(组内使用)        |
| `indeterminate` | `boolean`                              | `false` | 半选态(仅控制样式,不影响 v-model)    |
| `disabled`      | `boolean`                              | `false` | 是否禁用                               |
| `border`        | `boolean`                              | `false` | 是否显示边框                           |
| `size`          | `'large' \| 'default' \| 'small'`      | —       | 尺寸(边框模式下)                     |
| `name`          | `string`                               | —       | 原生 name 属性                         |
| `checked`       | `boolean`                              | `false` | 当前是否勾选(组内使用)                |

## el-checkbox-button 属性(Props)

| 属性名     | 类型                               | 默认值 | 说明            |
| ---------- | ---------------------------------- | ------ | --------------- |
| `value` / `label` | `string \| number \| boolean` | —     | 选项的值        |
| `disabled` | `boolean`                          | `false`| 是否禁用        |
| `name`     | `string`                           | —      | 原生 name 属性  |

## 事件(Events)

| 事件名   | 回调签名                                        | 说明                       |
| -------- | ----------------------------------------------- | -------------------------- |
| `change` | `(value: string \| number \| boolean \| Array) => void` | 绑定值变化时触发 |

## 方法 / 插槽

- 无对外方法。
- 插槽:`default`(标签文字,可嵌图标与文案)。

## 关键规格要点

- **三态**:checked(`v-model = true`)/ unchecked(`false`)/ indeterminate(`indeterminate` 属性 + Carbon 规范半选视觉);半选只影响样式,勾选状态仍由 v-model 表达。
- **尺寸**:默认高 32px,`large` 40px,`small` 24px;边框模式外框相应变化。
- **无障碍**:原生 `<input type="checkbox">` 承载,键盘空格切换;`aria-checked="mixed"` 由 indeterminate 映射;标签文字必须通过插槽关联(input 不应有空 label)。
