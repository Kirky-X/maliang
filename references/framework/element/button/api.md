# Button API

> `<el-button>` 组件的属性 / 事件 / 方法 / 插槽完整定义。用法与示例见 [component.md](./component.md)。

## 属性(Props)

| 属性名        | 类型                                            | 默认值     | 说明                                                                 |
| ------------- | ----------------------------------------------- | ---------- | -------------------------------------------------------------------- |
| `type`        | `'primary' \| 'success' \| 'warning' \| 'danger' \| 'info' \| 'text'` | `''`(默认) | 按钮语义类型。`text` 为文本按钮(无边框无背景)。映射到 {color-primary}/{color-success}/… |
| `size`        | `'large' \| 'default' \| 'small'`               | `'default'` | 按钮尺寸,影响高度与内边距。映射 {component-size-lg/md/sm}          |
| `plain`       | `boolean`                                       | `false`    | 朴素按钮:透明背景 + 语义色描边,边框色 {color-primary} 等          |
| `round`       | `boolean`                                       | `false`    | 圆角按钮,圆角半径 {radius-full}                                    |
| `circle`      | `boolean`                                       | `false`    | 圆形按钮,正圆,仅容纳图标,圆角 {radius-full}                      |
| `loading`     | `boolean`                                       | `false`    | 加载态,显示加载图标并阻止重复点击                                   |
| `loading-icon`| `string \| Component`                           | `Loading`  | 自定义加载图标                                                       |
| `disabled`    | `boolean`                                       | `false`    | 禁用态,降透明度 {opacity-disabled},保留语义色可读性                |
| `icon`        | `string \| Component`                           | `''`       | 按钮前置图标组件                                                     |
| `autofocus`   | `boolean`                                       | `false`    | 是否自动聚焦                                                         |
| `native-type` | `'button' \| 'submit' \| 'reset'`               | `'button'` | 原生 button 的 type 属性                                             |
| `tag`         | `string \| Component`                           | `'button'` | 按钮根节点渲染的标签/组件                                            |
| `auto-insert-space` | `boolean`                                 | `false`    | 两个中文字符之间是否自动插入空格                                     |

> 说明:`size` 与 `type` 的全局默认值可通过 Element Plus 的 [ConfigProvider](https://element-plus.org/) `size` / `button` 配置覆盖。

## 事件(Events)

| 事件名  | 回调签名                        | 说明                                   |
| ------- | ------------------------------- | -------------------------------------- |
| `click` | `(evt: MouseEvent) => void`     | 点击按钮时触发(disabled / loading 态不触发) |

## 方法(Methods)

`<el-button>` 不对外暴露专用方法。组件 ref 指向底层原生 `<button>` 元素,可通过 ref 调用原生方法:

| 方法    | 签名             | 说明                                   |
| ------- | ---------------- | -------------------------------------- |
| `focus` | `() => void`     | 使按钮获得焦点(通过 `ref.value.focus()`) |
| `blur`  | `() => void`     | 使按钮失去焦点(通过 `ref.value.blur()`)  |

```vue
<template>
  <el-button ref="btnRef" type="primary">自动聚焦按钮</el-button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const btnRef = ref()
onMounted(() => btnRef.value?.focus())
</script>
```

## 插槽(Slots)

| 插槽名    | 说明                                       |
| --------- | ------------------------------------------ |
| `default` | 按钮文本内容                               |
| `icon`    | 自定义前置图标(优先级高于 `icon` 属性)   |
| `loading` | 自定义加载图标(优先级高于 `loading-icon` 属性) |
