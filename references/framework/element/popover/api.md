# Popover API(三件套)

> `<el-popover>` / `<el-tooltip>` / `<el-popconfirm>` 的属性 / 事件 / 方法 / 插槽。用法见 [component.md](./component.md)。

## 共享属性(三者基本一致)

| 属性名               | 类型                                                | 默认值   | 说明                              |
| -------------------- | --------------------------------------------------- | -------- | --------------------------------- |
| `trigger`            | `'hover' \| 'click' \| 'focus' \| 'contextmenu'`    | `'hover'`| 触发方式                          |
| `placement`          | `'top' \| 'top-start' \| 'top-end' \| 'bottom' \| ...` | `'bottom'` | 弹出位置                     |
| `title`              | `string`                                            | —        | 标题                              |
| `effect`             | `'dark' \| 'light'`                                 | `'light'`| 主题                              |
| `width`              | `string \| number`                                  | —        | 宽度(popover)                  |
| `disabled`           | `boolean`                                           | `false`  | 是否禁用                          |
| `visible` / `v-model:visible` | `boolean`                                  | —        | 是否显示(受控)                 |
| `offset`             | `number`                                            | `0`      | 出现位置偏移                      |
| `transition`         | `string`                                            | —        | 过渡动画名                        |
| `show-arrow`         | `boolean`                                           | `true`   | 是否显示箭头                      |
| `popper-class`       | `string`                                            | —        | 自定义弹出层类                    |
| `popper-options`     | `object`                                            | —        | Popper.js 选项                    |
| `virtual-triggering` | `boolean`                                           | `false`  | 是否虚拟触发                      |
| `virtual-ref`        | `HTMLElement`                                       | —        | 虚拟触发引用元素                  |

## el-popover 专属

| 属性名         | 类型     | 说明                 |
| -------------- | -------- | -------------------- |
| `content`      | `string` | 文本内容             |

插槽:`default`(弹出内容)、`reference`(触发元素)。

## el-tooltip 专属

| 属性名        | 类型      | 说明                       |
| ------------- | --------- | -------------------------- |
| `content`     | `string`  | 提示内容                   |
| `raw-content` | `boolean` | 是否按 HTML 渲染           |
| `show-after`  | `number`  | 显示延迟(ms)            |
| `hide-after`  | `number`  | 隐藏延迟(ms)            |
| `auto-close`  | `number`  | 自动关闭延迟(ms)         |
| `tabindex`    | `number`  | 触发元素 tabindex          |

插槽:`content`(提示内容)、`default`(触发元素)。

## el-popconfirm 专属

| 属性名                  | 类型      | 默认值  | 说明                          |
| ----------------------- | --------- | ------- | ----------------------------- |
| `title`                 | `string`  | —       | 确认标题                      |
| `confirm-button-text`   | `string`  | —       | 确认按钮文案                  |
| `cancel-button-text`    | `string`  | —       | 取消按钮文案                  |
| `confirm-button-type`   | `ButtonType` | `'primary'` | 确认按钮类型             |
| `cancel-button-type`    | `ButtonType` | `'text'`    | 取消按钮类型             |
| `icon`                  | `string \| Component` | — | 图标                          |
| `icon-color`            | `string`  | `#f90`  | 图标颜色                      |
| `hide-icon`             | `boolean` | `false` | 是否隐藏图标                  |
| `hide-after`            | `number`  | `200`   | 关闭延迟(ms)               |

## el-popconfirm 事件

| 事件名    | 回调签名     | 说明           |
| --------- | ------------ | -------------- |
| `confirm` | `() => void` | 点击确认时触发 |
| `cancel`  | `() => void` | 点击取消时触发 |

插槽:`reference`(触发元素)。
