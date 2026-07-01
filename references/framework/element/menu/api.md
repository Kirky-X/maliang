# Menu API

> `<el-menu>` / `<el-sub-menu>` / `<el-menu-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-menu 属性(Props)

| 属性名               | 类型                                    | 默认值       | 说明                          |
| -------------------- | --------------------------------------- | ------------ | ----------------------------- |
| `mode`               | `'horizontal' \| 'vertical'`            | `'vertical'` | 模式                          |
| `collapse`           | `boolean`                               | `false`      | 是否折叠(仅 vertical)       |
| `default-active`     | `string`                                | —            | 默认激活项 index              |
| `default-openeds`    | `string[]`                              | —            | 默认展开的 sub-menu index     |
| `unique-opened`      | `boolean`                               | `false`      | 是否只保持一个子菜单展开      |
| `router`             | `boolean`                               | `false`      | 是否使用 vue-router 模式      |
| `ellipsis`           | `boolean`                               | `true`       | horizontal 是否省略溢出       |
| `background-color`   | `string`                                | —            | 菜单背景色                    |
| `text-color`         | `string`                                | —            | 文字色                        |
| `active-text-color`  | `string`                                | —            | 激活项文字色                  |

## el-sub-menu 属性(Props)

| 属性名    | 类型     | 默认值 | 说明                          |
| --------- | -------- | ------ | ----------------------------- |
| `index`   | `string` | —      | 唯一标识(必填)             |
| `popper-class` | `string` | —  | 弹出层自定义类                |
| `show-timeout` | `number` | `300` | 展开延迟(ms)              |
| `hide-timeout` | `number` | `300` | 收起延迟(ms)              |
| `disabled`| `boolean`| `false`| 是否禁用                      |
| `popper-append-to-body` | `boolean` | `true` | 是否追加到 body(已废弃) |

## el-menu-item 属性(Props)

| 属性名     | 类型                  | 默认值 | 说明                          |
| ---------- | --------------------- | ------ | ----------------------------- |
| `index`    | `string`              | —      | 唯一标识(必填)             |
| `route`   | `object`              | —      | router 模式下的路由对象       |
| `disabled` | `boolean`             | `false`| 是否禁用                      |

## el-menu 事件(Events)

| 事件名    | 回调签名                              | 说明                       |
| --------- | ------------------------------------- | -------------------------- |
| `select`  | `(index, indexPath, item, routeResult) => void` | 菜单激活回调 |
| `open`    | `(index, indexPath) => void`          | sub-menu 展开回调          |
| `close`   | `(index, indexPath) => void`          | sub-menu 收起回调          |

## el-menu 方法(Methods)

| 方法名           | 签名                          | 说明                       |
| ---------------- | ----------------------------- | -------------------------- |
| `open`           | `(index: string) => void`     | 展开某 sub-menu            |
| `close`          | `(index: string) => void`     | 收起某 sub-menu            |

## 插槽(Slots)

| 组件            | 插槽名    | 说明                              |
| --------------- | --------- | --------------------------------- |
| `el-menu`       | `default` | 菜单项内容                        |
| `el-sub-menu`   | `title`   | 子菜单标题                        |
| `el-sub-menu`   | `default` | 子菜单内容                        |
| `el-menu-item`  | `default` | 菜单项内容                        |
| `el-menu-item`  | `title`   | (通过 default 设置)             |
