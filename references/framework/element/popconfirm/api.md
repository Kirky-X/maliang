# Popconfirm API

> `<el-popconfirm>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-popconfirm 属性(Props)

| 属性名                 | 类型                                         | 默认值     | 说明                                        |
| ---------------------- | -------------------------------------------- | ---------- | ------------------------------------------- |
| `title`                | `string`                                     | —          | 确认问题(必须含明确宾语)                  |
| `confirm-button-text`  | `string`                                     | `'Yes'`    | 确认按钮文案(建议具体动词,如"删除")  |
| `cancel-button-text`   | `string`                                     | `'No'`     | 取消按钮文案                                |
| `confirm-button-type`  | `'primary' \| 'success' \| 'warning' \| 'danger' \| 'info' \| 'text'` | `'primary'` | 确认按钮类型(破坏性用 `danger`) |
| `cancel-button-type`   | 同上                                         | `'text'`   | 取消按钮类型(非危险默认)                |
| `confirm-button-icon`  | `string \| Component`                        | —          | 确认按钮图标                                |
| `cancel-button-icon`   | `string \| Component`                        | —          | 取消按钮图标                                |
| `hide-icon`            | `boolean`                                    | `false`    | 是否隐藏提示图标                            |
| `icon` / `icon-color`  | `string \| Component` / `string`             | `QuestionFilled` / 警示色 | 提示图标与颜色            |
| `width`                | `number \| string`                           | `150`      | 气泡宽度(含宾语/副文案时加宽)           |
| `disabled`             | `boolean`                                    | `false`    | 是否禁用(点击不弹)                       |
| `teleported`           | `boolean`                                    | `true`     | 气泡是否插入 body                           |
| `persistent`           | `boolean`                                    | `true`     | 气泡 DOM 是否常驻                           |

## 事件(Events)

| 事件名    | 回调签名                     | 说明                           |
| --------- | ---------------------------- | ------------------------------ |
| `confirm` | `(e: MouseEvent) => void`    | 点击确认按钮(执行动作点)   |
| `cancel`  | `(e: MouseEvent) => void`    | 点击取消按钮                   |

## 方法 / 插槽

- 无对外方法。
- 插槽:`reference`(触发元素,必须有)、`actions`(`{ confirm, cancel }` 自定义按钮区)、`icon`(自定义图标)。

## popconfirm 与 dialog 的选型分级

| 级别 | 场景 | 组件 |
| ---- | ---- | ---- |
| 轻量 | 列表项删除、移除收藏 | `<el-popconfirm>`(本类) |
| 中等 | 退款、取消订单(含金额宾语) | `<el-popconfirm>` 加宽 + 副文案 |
| 重量 | 注销账户、清空数据(不可逆) | `ElMessageBox.confirm` / `<el-dialog>`(dialog 类) |

## 关键规格要点

- **文案规范**:确认按钮写具体动作("删除""确认注销"),不写"确定";取消为非危险默认样式;问题带宾语(对象名/金额)。
- **危险色纪律**:`confirm-button-type="danger"` 仅用于不可逆/扣款动作。
- **尺寸**:默认宽 150px;含副文案建议 220-260px;气泡高度随内容自适应。
- **无障碍**:气泡内按钮为原生 button 语义;触发元素必须可聚焦(`#reference` 内放 button 而非裸图标);Esc 关闭归取消。
