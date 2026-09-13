# Notification API

> `ElNotification` 的配置项 / 事件 / 方法完整定义。用法见 [component.md](./component.md)。

## ElNotification 配置项(Options)

| 属性名         | 类型                                                    | 默认值       | 说明                                       |
| -------------- | ------------------------------------------------------- | ------------ | ------------------------------------------ |
| `title`        | `string`                                                | —            | 标题                                       |
| `message`      | `string \| VNode \| () => VNode`                        | —            | 正文(支持组件/VNode 多行)               |
| `type`         | `'success' \| 'warning' \| 'info' \| 'error'`           | —            | 通知类型(图标 + 强调色)                 |
| `dangerouslyUseHTMLString` | `boolean`                                   | `false`      | 以 HTML 渲染 message(有 XSS 风险,慎用)  |
| `duration`     | `number`                                                | `4500`       | 自动关闭毫秒数;`0` 表示不自动关闭        |
| `position`     | `'top-right' \| 'top-left' \| 'bottom-right' \| 'bottom-left'` | `'top-right'` | 弹出方位                          |
| `show-close`   | `boolean`                                               | `true`       | 是否显示关闭按钮                           |
| `offset`       | `number`                                                | `0`          | 距顶/底偏移(同方位堆叠自动累加)        |
| `plain`        | `boolean`                                               | `false`      | 纯样式(去背景强调)                       |
| `icon`         | `string \| Component`                                   | —            | 自定义图标(覆盖 type 默认图标)          |
| `z-index`      | `number`                                                | —            | 层级(建议由全局 z-index 管理)           |
| `grouping`     | `boolean`                                               | `false`      | 相同内容合并为一条并计数                   |
| `onClick`      | `() => void`                                            | —            | 点击通知回调                               |
| `onClose`      | `() => void`                                            | —            | 关闭回调                                   |

## 方法

| 方法 | 说明 |
| --- | --- |
| `ElNotification(options)` | 打开一条通知,返回 handle |
| `handle.close()` | 关闭该通知 |

## notification 与 message(toast)的分工

| 维度 | `ElNotification`(本类) | `ElMessage`(message 类) |
| ---- | ------------------------ | ------------------------- |
| 驻留 | 常驻(duration 可 0)/多条堆叠 | 短暂,单条,顶部居中 |
| 排版 | 标题 + 多行正文 + 图标 | 单行文本 |
| 操作 | showClose + onClick 可跳转 | 无操作位 |
| 语义 | 消息中心/待处理事件 | 即发即忘轻反馈 |
| 典型 | 同步失败、公告、审批结果 | "已复制""已保存" |

## 关键规格要点

- **驻留语义**:需要用户处理或回看的通知 `duration: 0` + `showClose: true`;即席轻反馈一律走 ElMessage。
- **堆叠**:同 `position` 自动堆叠;首条用 `offset` 避让导航栏。
- **尺寸**:默认宽 330px,多行正文自动增高;移动端窄屏注意裁切。
- **无障碍**:容器 `role="alert"` / `aria-live="polite"`(Element 自动维护);带操作的用 `onClick` 时保证键盘可达(内部用链接/按钮承载)。
