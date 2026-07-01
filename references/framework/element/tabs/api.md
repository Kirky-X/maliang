# Tabs API

> `<el-tabs>` 与 `<el-tab-pane>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-tabs 属性(Props)

| 属性名           | 类型                                          | 默认值   | 说明                                                |
| ---------------- | --------------------------------------------- | -------- | --------------------------------------------------- |
| `model-value` / `v-model` | `string \| number`                    | —        | 当前激活标签的 name 值                              |
| `type`           | `'card' \| 'border-card' \| ''`               | `''`     | 样式类型                                            |
| `closable`       | `boolean`                                     | `false`  | 标签是否可关闭                                      |
| `addable`        | `boolean`                                     | `false`  | 标签是否可新增                                      |
| `editable`       | `boolean`                                     | `false`  | 标签是否同时可增删(隐含 closable + addable)      |
| `tab-position`   | `'top' \| 'right' \| 'bottom' \| 'left'`      | `'top'`  | 标签位置                                            |
| `stretch`        | `boolean`                                     | `false`  | 标签是否自适应宽度                                  |
| `before-leave`   | `(activeName, oldActiveName) => boolean \| Promise` | — | 切换前的钩子,返回 false 取消                       |

## el-tab-pane 属性(Props)

| 属性名      | 类型               | 默认值 | 说明                          |
| ----------- | ------------------ | ------ | ----------------------------- |
| `label`     | `string`           | `''`   | 标签标题                      |
| `name`      | `string \| number` | —      | 标签标识,对应 v-model        |
| `disabled`  | `boolean`          | `false`| 是否禁用                      |
| `closable`  | `boolean`          | `false`| 该标签是否可关闭              |
| `lazy`      | `boolean`          | `false`| 是否懒渲染                    |

## el-tabs 事件(Events)

| 事件名        | 回调签名                                      | 说明                       |
| ------------- | --------------------------------------------- | -------------------------- |
| `tab-click`   | `(pane: TabsPaneContext, ev: Event) => void`  | 点击标签时触发             |
| `tab-change`  | `(name: TabPaneName) => void`                 | 激活标签改变时触发         |
| `tab-remove`  | `(name: TabPaneName) => void`                 | 移除标签时触发             |
| `tab-add`     | `() => void`                                  | 新增标签时触发             |
| `edit`        | `(name: TabPaneName, action: 'remove' \| 'add') => void` | 增删标签时触发 |

## 方法(Methods)

| 方法名            | 签名             | 说明                       |
| ----------------- | ---------------- | -------------------------- |
| `scrollToActiveTab` | `() => Promise<void>` | 滚动当前激活标签进入视图(动态标签条场景) |

## 插槽(Slots)

| 组件           | 插槽名    | 说明                          |
| -------------- | --------- | ----------------------------- |
| `el-tabs`      | `add-icon`| 自定义新增标签按钮图标        |
| `el-tab-pane`  | `default` | 标签页内容                    |
| `el-tab-pane`  | `label`   | 自定义标签标题(支持图标等) |
