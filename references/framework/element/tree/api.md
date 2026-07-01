# Tree API

> `<el-tree>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名                  | 类型                                      | 默认值   | 说明                              |
| ----------------------- | ----------------------------------------- | -------- | --------------------------------- |
| `data`                  | `array`                                   | —        | 树数据                            |
| `props`                 | `object`                                  | —        | 字段映射 {label, children, ...}   |
| `node-key`              | `string`                                  | —        | 节点唯一标识字段(必填,用于记忆)|
| `show-checkbox`         | `boolean`                                 | `false`  | 是否显示复选框                    |
| `default-expand-all`    | `boolean`                                 | `false`  | 默认展开全部                      |
| `default-expanded-keys` | `array`                                   | —        | 默认展开节点                      |
| `default-checked-keys`  | `array`                                   | —        | 默认勾选节点                      |
| `expand-on-click-node`  | `boolean`                                 | `true`   | 点击节点是否展开                  |
| `check-on-click-node`   | `boolean`                                 | `false`  | 点击节点是否勾选                  |
| `lazy`                  | `boolean`                                 | `false`  | 是否懒加载                        |
| `load`                  | `(node, resolve) => void`                 | —        | 懒加载函数                        |
| `filter-node-method`    | `(value, data, node) => boolean`          | —        | 过滤函数                          |
| `accordion`             | `boolean`                                 | `false`  | 是否手风琴模式                    |
| `draggable`             | `boolean`                                 | `false`  | 是否可拖拽                        |
| `highlight-current`     | `boolean`                                 | `false`  | 是否高亮当前节点                  |
| `indent`                | `number`                                  | `16`     | 层级缩进(px)                    |

## 事件(Events,部分)

| 事件名            | 回调签名                                                | 说明                |
| ----------------- | ------------------------------------------------------- | ------------------- |
| `node-click`      | `(data, node, e) => void`                               | 点击节点            |
| `node-contextmenu`| `(e, data, node) => void`                               | 右键节点            |
| `check`           | `(data, { checkedNodes, checkedKeys, ... }) => void`    | 勾选时              |
| `check-change`    | `(data, checked, indeterminate) => void`                | 勾选状态变化        |
| `node-expand`     | `(data, node, e) => void`                               | 展开时              |
| `node-collapse`   | `(data, node, e) => void`                               | 收起时              |
| `node-drop`       | `(draggingNode, dropNode, dropType, e) => void`         | 拖拽完成            |

## 方法(Methods,部分)

| 方法名              | 签名                                              | 说明                |
| ------------------- | ------------------------------------------------- | ------------------- |
| `setCheckedKeys`    | `(keys) => void`                                  | 设置勾选 key        |
| `getCheckedKeys`    | `() => array`                                     | 获取勾选 key        |
| `setCheckedNodes`   | `(nodes) => void`                                 | 设置勾选节点        |
| `getCheckedNodes`   | `(leafOnly?) => array`                            | 获取勾选节点        |
| `setCurrentKey`     | `(key?) => void`                                  | 设置当前节点        |
| `getCurrentKey`     | `() => any`                                       | 获取当前节点 key    |
| `filter`            | `(value) => void`                                 | 过滤                |
| `append`            | `(data, parentNode) => void`                      | 追加节点            |
| `remove`            | `(node) => void`                                  | 移除节点            |
| `updateKeyChildren` | `(key, data) => void`                             | 更新子节点          |

## 插槽(Slots)

| 插槽名    | 作用域参数                          | 说明                |
| --------- | ----------------------------------- | ------------------- |
| `default` | `{ node, data }`                    | 节点内容            |
