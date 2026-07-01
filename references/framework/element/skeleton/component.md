# Skeleton 骨架屏

> Element Plus 骨架屏组件 `<el-skeleton>` `<el-skeleton-item>`,用于内容加载占位。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-skeleton> <el-skeleton-item>
```

`<el-skeleton>` 为容器,`loading` 控制显隐,`rows` 设置占位行数,`animated` 开启动画;`<el-skeleton-item>` 为单个占位块,`variant` 控制形状。

## 基本用法

```vue
<template>
  <el-skeleton :rows="5" animated />
</template>
```

## 使用场景

### 场景 1:加载态切换

`loading` 为 true 显示骨架,false 显示真实内容;`template` 插槽自定义占位结构。

```vue
<template>
  <el-skeleton :loading="loading" animated>
    <template #default>
      <div class="real">{{ content }}</div>
    </template>
  </el-skeleton>
</template>

<script setup>
import { ref } from 'vue'
const loading = ref(true)
const content = ref('真实内容')
setTimeout(() => (loading.value = false), 2000)
</script>

<style scoped>
.real { color: {color-text-primary}; padding: {spacing-md}; }
</style>
```

### 场景 2:自定义骨架项

`<el-skeleton-item>` 的 `variant` 取值 `text`/`caption`/`h1`/`h3`/`rect`/`circle`/`image`。

```vue
<template>
  <el-skeleton animated>
    <template #template>
      <el-skeleton-item variant="image" style="width: 240px; height: 160px" />
      <div style="padding: 14px">
        <el-skeleton-item variant="h3" style="width: 50%" />
        <el-skeleton-item variant="text" style="margin-top: 12px" />
        <el-skeleton-item variant="text" style="margin-top: 8px" />
      </div>
    </template>
  </el-skeleton>
</template>
```

### 场景 3:卡片骨架

组合多个 skeleton-item 模拟卡片结构。

```vue
<template>
  <el-card>
    <el-skeleton :rows="3" animated />
  </el-card>
</template>
```

## 参考链接

- Element Plus 官方文档 - Skeleton 骨架屏: https://element-plus.org/zh-CN/component/skeleton
