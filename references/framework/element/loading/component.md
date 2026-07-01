# Loading 加载

> Element Plus 加载组件,以 `v-loading` 指令为主,辅以 `ElLoadingService` 全屏服务。API 完整定义见 [api.md](./api.md)。

## 组件标签 / API

```
v-loading    ElLoadingService
```

`v-loading="boolean"` 指令在元素上显示遮罩加载;`v-loading.fullscreen` 全屏;`ElLoadingService` 命令式全屏加载并返回可关闭实例。

## 基本用法

```vue
<template>
  <el-table v-loading="loading" :data="data">
    <el-table-column prop="name" label="姓名" />
  </el-table>
  <el-button @click="toggle">切换</el-button>
</template>

<script setup>
import { ref } from 'vue'
const loading = ref(true)
const data = ref([])
const toggle = () => (loading.value = !loading.value)
</script>
```

## 使用场景

### 场景 1:自定义文字与背景

`element-loading-text` 设置文字,`element-loading-background` 设置背景,`element-loading-spinner` 自定义图标。

```vue
<template>
  <div
    v-loading="loading"
    element-loading-text="加载中..."
    element-loading-background="rgba(0, 0, 0, 0.6)"
    class="box"
  >
    内容区
  </div>
</template>

<script setup>
import { ref } from 'vue'
const loading = ref(true)
</script>

<style scoped>
.box {
  height: 200px;
  border-radius: {radius-md};
  background-color: {color-bg-secondary};
  color: {color-text-primary};
  padding: {spacing-md};
}
</style>
```

### 场景 2:全屏加载

`v-loading.fullscreen` 或 `ElLoadingService` 全屏遮罩。

```vue
<template>
  <el-button @click="openFull">全屏加载 3 秒</el-button>
</template>

<script setup>
import { ElLoading } from 'element-plus'
const openFull = () => {
  const inst = ElLoading.service({ fullscreen: true, text: '加载中' })
  setTimeout(() => inst.close(), 3000)
}
</script>
```

### 场景 3:锁定与自定义图标

`v-loading.lock` 全屏时锁定滚动;`element-loading-svg` 传入 SVG 字符串自定义图标。

```vue
<template>
  <div v-loading.fullscreen.lock="loading" class="box">锁定全屏</div>
</template>

<script setup>
import { ref } from 'vue'
const loading = ref(false)
</script>
```

## 参考链接

- Element Plus 官方文档 - Loading 加载: https://element-plus.org/zh-CN/component/loading
