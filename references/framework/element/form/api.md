# Form API

> `<el-form>` 与 `<el-form-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-form 属性(Props)

| 属性名            | 类型                                              | 默认值     | 说明                                                |
| ----------------- | ------------------------------------------------- | ---------- | --------------------------------------------------- |
| `model`           | `object`                                          | —          | 表单数据对象                                        |
| `rules`           | `object`                                          | —          | 表单验证规则                                        |
| `inline`          | `boolean`                                         | `false`    | 行内表单模式                                        |
| `label-position`  | `'left' \| 'right' \| 'top'`                      | `'right'`  | 表单域标签位置                                      |
| `label-width`     | `string \| number`                                | —          | 标签宽度                                            |
| `label-suffix`    | `string`                                          | `''`       | 标签后缀                                            |
| `hide-required-asterisk` | `boolean`                                  | `false`    | 是否隐藏必填字段的红星                              |
| `show-message`    | `boolean`                                         | `true`     | 是否显示校验错误信息                                |
| `inline-message`  | `boolean`                                         | `false`    | 是否以行内形式展示校验信息                          |
| `status-icon`     | `boolean`                                         | `false`    | 是否在输入框中显示校验结果反馈图标                  |
| `validate-on-rule-change` | `boolean`                                 | `true`     | 规则改变时是否立即触发校验                          |
| `size`            | `'large' \| 'default' \| 'small'`                 | —          | 表单内组件尺寸                                      |
| `disabled`        | `boolean`                                         | `false`    | 是否禁用表单内所有组件,降透明度 {opacity-disabled} |
| `scroll-to-error` | `boolean`                                         | `false`    | 校验失败时是否滚动到错误项                          |

## el-form-item 属性(Props)

| 属性名         | 类型                | 默认值  | 说明                          |
| -------------- | ------------------- | ------- | ----------------------------- |
| `prop`         | `string`            | —       | model 字段名,用于校验        |
| `label`        | `string`            | —       | 标签文本                      |
| `label-width`  | `string \| number`  | —       | 标签宽度(覆盖 form)         |
| `required`     | `boolean`           | `false` | 是否必填(覆盖 rules)        |
| `rules`        | `object \| array`   | —       | 该项的校验规则                |
| `error`        | `string`            | —       | 手动设置错误信息              |
| `show-message` | `boolean`           | `true`  | 是否显示错误信息              |
| `inline-message` | `boolean`         | `false` | 行内错误信息                  |
| `size`         | `'large' \| 'default' \| 'small'` | — | 尺寸                          |

## el-form 事件(Events)

| 事件名    | 回调签名                                                 | 说明                 |
| --------- | -------------------------------------------------------- | -------------------- |
| `validate`| `(prop: string, isValid: boolean, message: string) => void` | 任一项校验后触发 |

## el-form 方法(Methods)

| 方法名             | 签名                                                              | 说明                          |
| ------------------ | ----------------------------------------------------------------- | ----------------------------- |
| `validate`         | `(callback?: Function) => Promise<boolean>`                       | 对整个表单校验                |
| `validateField`    | `(props?: string \| string[], callback?: Function) => Promise`    | 对部分字段校验                |
| `resetFields`      | `(props?: string \| string[]) => void`                            | 重置字段并移除校验结果        |
| `scrollToField`    | `(prop: string) => void`                                          | 滚动到某字段                  |
| `clearValidate`    | `(props?: string \| string[]) => void`                           | 移除某项校验结果              |

## 插槽(Slots)

| 组件            | 插槽名    | 说明                          |
| --------------- | --------- | ----------------------------- |
| `el-form`       | `default` | 表单项内容                    |
| `el-form-item`  | `default` | 表单项内容                    |
| `el-form-item`  | `label`   | 自定义标签                    |
| `el-form-item`  | `error`   | 自定义校验信息                |
