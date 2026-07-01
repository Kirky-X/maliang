# Scroll 滚动

> Element Plus 滚动相关组件:`<el-scrollbar>` 滚动条与 `v-infinite-scroll` 无限滚动指令。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-scrollbar>
```

`<el-scrollbar>` 替换原生滚动条,支持自定义样式与高度;`v-infinite-scroll` 指令在滚动到底部时触发加载。

## 基本用法

```vue
<template>
  <el-scrollbar height="200px">
    <div v-for="i in 50" :key="i" class="item">内容 {{ i }}</div>
  </el-scrollbar>
</template>

<style scoped>
.item {
  padding: {spacing-sm} {spacing-md};
  color: {color-text-primary};
}
.item:hover { background-color: {color-bg-secondary}; }
</style>
```

## 使用场景

### 场景 1:横向滚动

`<el-scrollbar>` 默认纵向,内容宽于容器时自动出现横向滚动。

```vue
<template>
  <el-scrollbar>
    <div class="row">
      <div v-for="i in 20" :key="i" class="card">卡片 {{ i }}</div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.row { display: flex; gap: {spacing-sm}; padding: {spacing-sm}; }
.card {
  flex: 0 0 120px; height: 80px;
  background-color: {color-bg-secondary};
  border-radius: {radius-md};
  color: {color-text-primary};
  display: flex; align-items: center; justify-content: center;
}
</style>
```

### 场景 2:无限滚动

`v-infinite-scroll` 指令配合 `infinite-scroll-distance` 设置触发距离。

```vue
<template>
  <div v-infinite-scroll="load" :infinite-scroll-distance="10" class="list">
    <div v-for="item in list" :key="item.id" class="item">{{ item.text }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const list = ref(Array.from({ length: 20 }, (_, i) => ({ id: i, text: `项 ${i}` })))
let count = 20
const load = () => {
  if (count >= 100) return
  list.value.push(...Array.from({ length: 10 }, (_, i) => ({ id: count + i, text: `项 ${count + i}` })))
  count += 10
}
</script>

<style scoped>
.list { height: 300px; overflow: auto; }
.item { padding: {spacing-sm}; color: {color-text-primary}; }
</style>
```

### 场景 3:手动控制滚动位置

通过 ref 调用 `setScrollTop` 控制滚动位置。

```vue
<template>
  <el-scrollbar ref="scrollRef" height="200px">
    <div v-for="i in 50" :key="i" class="item">{{ i }}</div>
  </el-scrollbar>
  <el-button @click="scrollTop">回顶</el-button>
</template>

<script setup>
import { ref } from 'vue'
const scrollRef = ref()
const scrollTop = () => scrollRef.value?.setScrollTop(0)
</script>
```

## 参考链接

- Element Plus 官方文档 - Scrollbar 滚动条: https://element-plus.org/zh-CN/component/scrollbar
- 无限滚动: https://element-plus.org/zh-CN/component/infinite-scroll
