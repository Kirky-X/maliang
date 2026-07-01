# Input API

> `<el-input>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名            | 类型                                              | 默认值     | 说明                                                       |
| ----------------- | ------------------------------------------------- | ---------- | ---------------------------------------------------------- |
| `model-value` / `v-model` | `string \| number`                        | —          | 绑定值                                                     |
| `type`            | `'text' \| 'textarea' \| 'password' \| ...`       | `'text'`   | 类型,textarea 为多行                                      |
| `size`            | `'large' \| 'default' \| 'small'`                 | `'default'`| 尺寸                                                       |
| `maxlength`       | `number \| string`                                | —          | 最大输入长度                                               |
| `minlength`       | `number \| string`                                | —          | 最小输入长度                                               |
| `show-word-limit` | `boolean`                                         | `false`    | 是否显示字数统计                                           |
| `placeholder`     | `string`                                          | —          | 占位文本                                                   |
| `clearable`       | `boolean`                                         | `false`    | 是否可清空                                                 |
| `show-password`   | `boolean`                                         | `false`    | 是否显示切换密码图标                                       |
| `disabled`        | `boolean`                                         | `false`    | 是否禁用,降透明度 {opacity-disabled}                      |
| `readonly`        | `boolean`                                         | `false`    | 是否只读                                                   |
| `rows`            | `number`                                          | `2`        | textarea 行数                                              |
| `autosize`        | `boolean \| { minRows, maxRows }`                 | `false`    | textarea 自适应高度                                        |
| `prefix-icon`     | `string \| Component`                             | —          | 前置图标                                                   |
| `suffix-icon`     | `string \| Component`                             | —          | 后置图标                                                   |
| `formatter`       | `(value: string) => string`                       | —          | 指定输入值格式化                                           |
| `parser`          | `(value: string) => string`                       | —          | 指定从 formatter 转换回值                                  |
| `validate-event`  | `boolean`                                         | `true`     | 输入时是否触发表单校验                                     |

## 事件(Events)

| 事件名   | 回调签名                          | 说明                              |
| -------- | --------------------------------- | --------------------------------- |
| `input`  | `(value: string \| number) => void` | 输入时触发                        |
| `change` | `(value: string \| number) => void` | 值改变且失焦时触发                |
| `blur`   | `(evt: FocusEvent) => void`       | 失焦时触发                        |
| `focus`  | `(evt: FocusEvent) => void`       | 聚焦时触发                        |
| `clear`  | `() => void`                      | 点击清空按钮时触发                |
| `compositionend` | `(evt: CompositionEvent) => void` | 输入法组合输入结束时触发  |

## 方法(Methods)

| 方法     | 签名             | 说明                       |
| -------- | ---------------- | -------------------------- |
| `focus`  | `() => void`     | 使输入框获得焦点           |
| `blur`   | `() => void`     | 使输入框失去焦点           |
| `select` | `() => void`     | 选中输入框中的文字         |
| `clear`  | `() => void`     | 清空输入框                 |
| `resizeTextarea` | `() => void` | 手动触发 textarea 高度重算 |

## 插槽(Slots)

| 插槽名    | 说明                            |
| --------- | ------------------------------- |
| `prefix`  | 输入框头部内容(优先于 prefix-icon) |
| `suffix`  | 输入框尾部内容(优先于 suffix-icon) |
| `prepend` | 输入框前置内容(复合输入框)     |
| `append`  | 输入框后置内容(复合输入框)     |
