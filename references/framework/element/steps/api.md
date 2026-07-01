# Steps API

> `<el-steps>` 与 `<el-step>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-steps 属性(Props)

| 属性名           | 类型                                                          | 默认值         | 说明                          |
| ---------------- | ------------------------------------------------------------- | -------------- | ----------------------------- |
| `space`          | `number \| string`                                            | —              | 间距                          |
| `direction`      | `'vertical' \| 'horizontal'`                                  | `'horizontal'` | 方向                          |
| `active`         | `number`                                                      | `0`            | 当前步骤                      |
| `process-status` | `'wait' \| 'process' \| 'finish' \| 'error' \| 'success'`     | `'process'`    | 当前步骤状态                  |
| `finish-status`  | `'wait' \| 'process' \| 'finish' \| 'error' \| 'success'`     | `'finish'`     | 完成步骤状态                  |
| `align-center`   | `boolean`                                                     | `false`        | 是否居中(horizontal)        |
| `simple`         | `boolean`                                                     | `false`        | 是否简单模式                  |

## el-step 属性(Props)

| 属性名        | 类型                                                                  | 默认值 | 说明                          |
| ------------- | --------------------------------------------------------------------- | ------ | ----------------------------- |
| `title`       | `string`                                                              | —      | 标题                          |
| `description` | `string`                                                              | —      | 描述                          |
| `icon`        | `string \| Component`                                                 | —      | 图标                          |
| `status`      | `'wait' \| 'process' \| 'finish' \| 'error' \| 'success'`             | —      | 状态(覆盖自动计算)        |

## 事件(Events)

无对外事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 组件        | 插槽名     | 说明                          |
| ----------- | ---------- | ----------------------------- |
| `el-steps`  | `default`  | 步骤内容                      |
| `el-step`   | `default`  | 自定义步骤内容                |
| `el-step`   | `title`    | 自定义标题                    |
| `el-step`   | `description` | 自定义描述                 |
| `el-step`   | `icon`     | 自定义图标                    |
