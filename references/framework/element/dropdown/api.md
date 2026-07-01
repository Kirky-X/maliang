# Dropdown API

> `<el-dropdown>` / `<el-dropdown-menu>` / `<el-dropdown-item>` 的属性 / 事件 / 方法 / 插槽。用法见 [component.md](./component.md)。

## el-dropdown 属性(Props)

| 属性名        | 类型                                            | 默认值    | 说明                              |
| ------------- | ----------------------------------------------- | --------- | --------------------------------- |
| `type`        | `ButtonType`                                    | —         | 触发按钮类型                      |
| `size`        | `'large' \| 'default' \| 'small'`               | `'default'` | 尺寸                            |
| `trigger`     | `'hover' \| 'click' \| 'contextmenu'`           | `'hover'` | 触发方式                          |
| `placement`   | `'top' \| 'bottom' \| 'bottom-start' \| ...`    | `'bottom'`| 弹出位置                          |
| `disabled`    | `boolean`                                       | `false`   | 是否禁用                          |
| `split-button`| `boolean`                                       | `false`   | 是否分裂按钮                      |
| `hide-on-click`| `boolean`                                      | `true`    | 点击菜单项是否关闭                |
| `max-height`  | `string \| number`                              | —         | 菜单最大高度(滚动)            |

## el-dropdown-item 属性(Props)

| 属性名     | 类型                | 默认值 | 说明                          |
| ---------- | ------------------- | ------ | ----------------------------- |
| `command`  | `string \| number \| object` | —  | 命令标识                      |
| `disabled` | `boolean`           | `false`| 是否禁用                      |
| `divided`  | `boolean`           | `false`| 是否显示分隔线                |
| `icon`     | `string \| Component` | —    | 图标                          |

## el-dropdown 事件(Events)

| 事件名    | 回调签名                              | 说明                       |
| --------- | ------------------------------------- | -------------------------- |
| `command` | `(command: any) => void`              | 点击菜单项触发             |
| `click`   | `() => void`                          | 触发元素点击(split-button) |
| `visible-change` | `(visible: boolean) => void`   | 显隐变化                   |

## el-dropdown 方法(Methods)

| 方法名  | 签名         | 说明           |
| ------- | ------------ | -------------- |
| `handleOpen` | `() => void` | 打开菜单 |
| `handleClose`| `() => void` | 关闭菜单 |

## 插槽(Slots)

| 组件                 | 插槽名    | 说明                          |
| -------------------- | --------- | ----------------------------- |
| `el-dropdown`        | `default` | 触发元素                      |
| `el-dropdown`        | `dropdown`| 菜单内容(放 el-dropdown-menu)|
| `el-dropdown-item`   | `default` | 菜单项内容                    |
