# Switch API

> `<el-switch>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名                | 类型                                       | 默认值     | 说明                                       |
| --------------------- | ------------------------------------------ | ---------- | ------------------------------------------ |
| `model-value` / `v-model` | `boolean \| string \| number`          | `false`    | 绑定值                                     |
| `disabled`            | `boolean`                                  | `false`    | 是否禁用,降透明度 {opacity-disabled}      |
| `loading`             | `boolean`                                  | `false`    | 是否加载中                                 |
| `size`                | `'large' \| 'default' \| 'small'`          | `'default'`| 尺寸                                       |
| `width`               | `number \| string`                         | —          | 宽度                                       |
| `active-text`         | `string`                                   | —          | 打开时文字                                 |
| `inactive-text`       | `string`                                   | —          | 关闭时文字                                 |
| `active-icon`         | `string \| Component`                      | —          | 打开时图标                                 |
| `inactive-icon`       | `string \| Component`                      | —          | 关闭时图标                                 |
| `active-value`        | `boolean \| string \| number`              | `true`     | 打开对应的值                               |
| `inactive-value`      | `boolean \| string \| number`              | `false`    | 关闭对应的值                               |
| `active-color`        | `string`                                   | `'#409eff'`| 打开背景色,建议映射 {color-primary}      |
| `inactive-color`      | `string`                                   | `'#c0ccda'`| 关闭背景色                                 |
| `border-color`        | `string`                                   | —          | 边框色                                     |
| `inline-prompt`       | `boolean`                                  | `false`    | 文字是否内显                               |
| `inline-prompt-active-class` | `string`                            | —          | 内显激活类                                 |
| `inline-prompt-inactive-class` | `string`                          | —          | 内显非激活类                               |
| `validate-event`      | `boolean`                                  | `true`     | 是否触发表单校验                           |
| `before-change`       | `() => Promise<boolean> \| boolean`        | —          | 切换前钩子,返回 false 取消                |

## 事件(Events)

| 事件名    | 回调签名                                           | 说明                       |
| --------- | -------------------------------------------------- | -------------------------- |
| `change`  | `(val: boolean \| string \| number) => void`       | 状态变化时触发             |
| `input`   | `(val: boolean \| string \| number) => void`       | 输入时触发(已废弃,用 change) |

## 方法(Methods)

无对外暴露方法,通过 `v-model` 控制。

## 插槽(Slots)

| 插槽名            | 说明                          |
| ----------------- | ----------------------------- |
| `active-action`   | 自定义打开时的操作图标        |
| `inactive-action` | 自定义关闭时的操作图标        |
