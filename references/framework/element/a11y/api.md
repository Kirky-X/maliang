# Accessibility API — Element Plus N/A(替代方案)

> 本组件为 N/A,见 [component.md](./component.md) 说明。本文件列出业务层可补充的常用 ARIA 属性,作为 a11y 实现参考。

## 常用 ARIA 属性

| 属性名              | 类型     | 说明                                       |
| ------------------- | -------- | ------------------------------------------ |
| `aria-label`        | `string` | 为无可见文字的元素提供可访问名             |
| `aria-labelledby`   | `string` | 指向提供名称的元素 id                      |
| `aria-describedby`  | `string` | 指向提供描述的元素 id                      |
| `aria-hidden`       | `boolean`| 是否对辅助技术隐藏                         |
| `aria-disabled`     | `boolean`| 是否禁用(语义)                          |
| `aria-expanded`     | `boolean`| 展开/折叠状态                              |
| `aria-checked`      | `boolean`| 选中状态                                   |
| `aria-live`         | `'off' \| 'polite' \| 'assertive'` | 动态内容通知级别   |
| `role`              | `string` | ARIA 角色(如 `dialog`/`tab`/`menu`)     |

## Element Plus 组件已内建的角色(部分)

| 组件          | 内建 role / aria                                         |
| ------------- | -------------------------------------------------------- |
| `el-dialog`   | `role="dialog"`, `aria-modal="true"`                     |
| `el-tabs`     | `role="tablist"` / `role="tab"` / `role="tabpanel"`      |
| `el-menu`     | `role="menubar"` / `role="menu"` / `role="menuitem"`     |
| `el-dropdown` | `role="menu"` / `role="menuitem"`                        |
| `el-alert`    | `role="alert"`                                           |
| `el-switch`   | `role="switch"`, `aria-checked`                          |

## 业务层建议

- 图标按钮(`el-button` 仅含图标)必须补充 `aria-label`。
- 动态通知(成功/失败提示)使用 `role="status" aria-live="polite"`。
- 可关闭的浮层(Dialog/Drawer)关闭后将焦点归还触发元素。
- 表单 `el-form-item` 校验失败时,通过 `aria-invalid` 与 `aria-describedby` 关联错误信息。

## 跨框架对照

| 框架        | 实现方式                              |
| ----------- | ------------------------------------- |
| ArkTS       | `accessibility` 属性组                |
| Flutter     | `Semantics` widget                    |
| Element Plus| 内建 role + 业务层 aria 属性补充      |
