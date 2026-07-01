# Gesture API — Element Plus N/A(替代方案)

> 本组件为 N/A,见 [component.md](./component.md) 替代方案说明。本文件列出原生 DOM 触摸/鼠标事件,作为手势实现的属性/事件参考。

## 原生触摸事件(Touch Events)

| 事件名        | 触发时机               | 关键数据                              |
| ------------- | ---------------------- | ------------------------------------- |
| `touchstart`  | 手指接触屏幕           | `event.touches` 触点列表              |
| `touchmove`   | 手指移动               | `event.touches` / `event.changedTouches` |
| `touchend`    | 手指离开屏幕           | `event.changedTouches`                |
| `touchcancel` | 系统打断(如来电)     | `event.changedTouches`                |

## 原生鼠标事件(Mouse Events)

| 事件名        | 触发时机           |
| ------------- | ------------------ |
| `mousedown`   | 按下鼠标           |
| `mousemove`   | 移动鼠标           |
| `mouseup`     | 释放鼠标           |
| `click`       | 单击               |
| `dblclick`    | 双击               |
| `wheel`       | 滚轮               |

## 指针事件(Pointer Events,推荐统一处理)

| 事件名           | 触发时机           |
| ---------------- | ------------------ |
| `pointerdown`    | 按下(鼠标/触摸/笔)|
| `pointermove`    | 移动               |
| `pointerup`      | 释放               |
| `pointercancel`  | 取消               |

## 手势判定常用阈值(建议)

| 手势   | 判定条件                              | 建议阈值           |
| ------ | ------------------------------------- | ------------------ |
| 单击   | pointerdown→pointerup 位移小、间隔短 | 位移<10px,时长<300ms |
| 长按   | pointerdown 后保持不动                | 时长>500ms         |
| 滑动   | 主轴位移 > 阈值                       | 位移>50px          |
| 双击   | 两次 click 间隔短                     | 间隔<300ms         |

## Vue 绑定方式

```vue
<template>
  <div
    @touchstart="onStart"
    @touchend="onEnd"
    @mousedown="onStart"
    @mouseup="onEnd"
  />
</template>

<script setup>
const onStart = (e) => { /* ... */ }
const onEnd = (e) => { /* ... */ }
</script>
```

> 以上为原生 Web 事件,Element Plus 不额外封装,可在任意 Element Plus 组件上直接绑定。
