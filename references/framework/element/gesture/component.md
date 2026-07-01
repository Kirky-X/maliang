# Gesture 手势组件 — Element Plus N/A 说明

> **本框架无原生 Gesture 组件。**

## 缺失原因

Element Plus 是面向 Web 的 Vue 3 组件库,手势交互(长按、拖拽、滑动、双击等)通过原生 DOM 事件(`@click`、`@touchstart`、`@touchmove`、`@touchend`、`@mousedown/mousemove/mouseup`)处理,未抽象为独立手势组件。Web 平台手势模型与原生移动端不同,Element Plus 选择将此类交互交由业务层实现。

## 替代方案

- 方案 1:用原生 Vue 事件 + 指令组合,自行计算 touchstart→touchend 的位移、时长判断手势类型。
- 方案 2:部分手势可由 Element Plus 现有组件模拟——`<el-dialog draggable>` / `<el-drawer>` 支持拖拽;`<el-backtop>` / `<el-scrollbar>` 处理滚动;`<el-carousel>` 支持触摸切换。
- 方案 3:引入第三方手势库(如 `@vueuse/gesture`、`hammerjs`)与 Element Plus 组件协同。

## 替代实现示例(长按 + 滑动)

```vue
<template>
  <div
    class="gesture-area"
    @touchstart="onTouchStart"
    @touchmove="onTouchMove"
    @touchend="onTouchEnd"
  >
    长按 / 滑动区域
  </div>
</template>

<script setup>
import { ref } from 'vue'
const start = ref({ x: 0, y: 0, t: 0 })
const onTouchStart = (e) => {
  const t = e.touches[0]
  start.value = { x: t.clientX, y: t.clientY, t: Date.now() }
}
const onTouchMove = (e) => { /* 计算 swipe */ }
const onTouchEnd = (e) => {
  const dt = Date.now() - start.value.t
  if (dt > 500) console.log('长按')
}
</script>

<style scoped>
.gesture-area {
  padding: {spacing-md};
  border-radius: {radius-md};
  background-color: {color-bg-secondary};
  color: {color-text-primary};
  user-select: none;
}
</style>
```

## 跨框架对照

| 框架        | 实现方式                                        |
| ----------- | ----------------------------------------------- |
| ArkTS       | `gesture`(`TapGesture`/`PanGesture` 等)     |
| Flutter     | `GestureDetector` / `Dismissible` 等 widget    |
| Element Plus| 无原生(本文件),用原生 DOM 事件 + 指令替代    |

## 参考链接

- Element Plus 官方文档:无对应章节
- 相关资源:[Vue 事件处理](https://vuejs.org/guide/essentials/event-handling.html)、[MDN Touch events](https://developer.mozilla.org/zh-CN/docs/Web/API/Touch_events)
