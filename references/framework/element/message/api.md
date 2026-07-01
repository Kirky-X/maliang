# Message API

> `<el-message>` 与命令式 `ElMessage` 的属性 / 方法 / 实例方法定义。用法见 [component.md](./component.md)。

## ElMessage Options(属性)

| 属性名                   | 类型                                                                     | 默认值   | 说明                                              |
| ------------------------ | ------------------------------------------------------------------------ | -------- | ------------------------------------------------- |
| `message`                | `string \| VNode`                                                        | —        | 消息内容                                          |
| `type`                   | `'success' \| 'warning' \| 'info' \| 'error'`                            | `'info'` | 类型,映射 {color-success}/…                     |
| `icon`                   | `string \| Component`                                                    | —        | 自定义图标(覆盖默认)                          |
| `dangerouslyUseHTMLString` | `boolean`                                                              | `false`  | 是否将 message 当作 HTML                          |
| `duration`               | `number`                                                                 | `3000`   | 显示时长(ms),0 为不自动关闭                    |
| `show-close`             | `boolean`                                                                | `false`  | 是否显示关闭按钮                                  |
| `center`                 | `boolean`                                                                | `false`  | 是否居中                                          |
| `offset`                 | `number`                                                                 | `20`     | 距顶部偏移(px)                                  |
| `append-to`              | `string \| HTMLElement`                                                  | `document.body` | 挂载节点                                  |
| `grouping`               | `boolean`                                                                | `false`  | 是否合并相同内容                                  |
| `custom-class`           | `string`                                                                 | —        | 自定义类名                                        |
| `z-index`                | `number`                                                                 | —        | 层级                                              |
| `onClose`                | `() => void`                                                             | —        | 关闭回调                                          |

## ElMessage 方法

| 方法名       | 签名                                                                       | 说明                          |
| ------------ | -------------------------------------------------------------------------- | ----------------------------- |
| `ElMessage`  | `(options: string \| Options) => MessageInstance`                          | 创建消息(支持字符串简写)    |
| `success`    | `(message: string \| Options) => MessageInstance`                         | success 类型快捷方法          |
| `warning`    | `(message: string \| Options) => MessageInstance`                         | warning 类型快捷方法          |
| `info`       | `(message: string \| Options) => MessageInstance`                         | info 类型快捷方法             |
| `error`      | `(message: string \| Options) => MessageInstance`                         | error 类型快捷方法            |
| `closeAll`   | `() => void`                                                               | 关闭所有消息                  |

## 实例方法

| 方法名   | 签名         | 说明         |
| -------- | ------------ | ------------ |
| `close`  | `() => void` | 关闭该消息   |

## 插槽(Slots)

`<el-message>` 标签形式下支持 `default` 插槽(message 内容)与 `default`(通过 VNode 传入)。

```js
import { ElMessage, h } from 'element-plus'
ElMessage({ message: h('span', { style: 'color:#f00' }, '红色文字') })
```
