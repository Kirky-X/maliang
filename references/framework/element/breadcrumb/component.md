# Breadcrumb 面包屑

> Element Plus 面包屑组件 `<el-breadcrumb>` `<el-breadcrumb-item>`,显示当前页面路径。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-breadcrumb> <el-breadcrumb-item>
```

`<el-breadcrumb>` 为容器,`separator` 设置分隔符;`<el-breadcrumb-item>` 为每级,`to` 设置路由跳转。

## 基本用法

```vue
<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>商品</el-breadcrumb-item>
    <el-breadcrumb-item>详情</el-breadcrumb-item>
  </el-breadcrumb>
</template>

<style scoped>
:deep(.el-breadcrumb__item) { color: {color-text-primary}; font-size: {font-size-md}; }
:deep(.el-breadcrumb__inner.is-link):hover { color: {color-primary}; }
</style>
```

## 使用场景

### 场景 1:图标分隔符

`separator-icon` 用图标组件作分隔符。

```vue
<template>
  <el-breadcrumb :separator-icon="ArrowRight">
    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>设置</el-breadcrumb-item>
    <el-breadcrumb-item>账号</el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
</script>
```

### 场景 2:动态生成

结合路由 meta 生成面包屑。

```vue
<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="(item, i) in crumbs" :key="i" :to="item.to">
      {{ item.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const crumbs = computed(() => route.matched.map((r) => ({ to: r.path, title: r.meta?.title || r.name })))
</script>
```

## 参考链接

- Element Plus 官方文档 - Breadcrumb 面包屑: https://element-plus.org/zh-CN/component/breadcrumb
