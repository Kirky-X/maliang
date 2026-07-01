# Animation 过渡动画

> Element Plus 内置过渡组件指南。提供 `<el-fade-in>`、`<el-zoom-in>`、`<el-collapse-transition>` 等过渡,以及全局 transition 类名约定。本文件为指南类文档。

## 内置过渡组件

| 组件                          | 说明                |
| ----------------------------- | ------------------- |
| `<el-transition>`             | 通用过渡(支持 name)|
| `<el-fade-in>`                | 淡入                |
| `<el-fade-in-linear>`         | 线性淡入            |
| `<el-zoom-in>` / `<el-zoom-in-center>` | 缩放进入   |
| `<el-collapse-transition>`    | 折叠展开过渡        |

## 使用场景

### 场景 1:淡入与缩放

```vue
<template>
  <el-button @click="show = !show">切换</el-button>
  <el-fade-in>
    <div v-show="show" class="box">淡入内容</div>
  </el-fade-in>
  <el-zoom-in-center>
    <div v-show="show" class="box">缩放内容</div>
  </el-zoom-in-center>
</template>

<script setup>
import { ref } from 'vue'
const show = ref(true)
</script>

<style scoped>
.box {
  margin-top: {spacing-md};
  padding: {spacing-md};
  border-radius: {radius-md};
  background-color: {color-bg-secondary};
  color: {color-text-primary};
}
</style>
```

### 场景 2:折叠过渡

`<el-collapse-transition>` 用于高度自适应的折叠展开。

```vue
<template>
  <el-button @click="open = !open">展开/收起</el-button>
  <el-collapse-transition>
    <div v-show="open" class="panel">
      <p>折叠内容</p>
      <p>高度自适应</p>
    </div>
  </el-collapse-transition>
</template>

<script setup>
import { ref } from 'vue'
const open = ref(false)
</script>

<style scoped>
.panel {
  padding: {spacing-md};
  border: 1px solid {color-border-default};
  border-radius: {radius-md};
  background-color: {color-bg-primary};
  color: {color-text-primary};
}
</style>
```

### 场景 3:配合 Vue Transition 类名

Element Plus 约定的类名可直接用于原生 `<transition>`/`<transition-group>`。

```vue
<template>
  <transition name="el-fade-in-linear">
    <div v-show="show" class="box">线性淡入</div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
const show = ref(true)
</script>
```

## 参考链接

- Element Plus 官方文档 - 过渡动画: https://element-plus.org/zh-CN/guide/transitions
