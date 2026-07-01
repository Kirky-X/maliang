# Divider 分割线

> Element Plus 分割线组件 `<el-divider>`,用于分隔内容。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-divider>
```

通过 `direction` 设置方向(horizontal/vertical),`content-position` 设置文字位置,`border-style` 设置样式,`dashed`(2.7+)虚线。

## 基本用法

```vue
<template>
  <div>内容 A</div>
  <el-divider />
  <div>内容 B</div>
</template>

<style scoped>
:deep(.el-divider) { border-color: {color-border-default}; }
</style>
```

## 使用场景

### 场景 1:带文字分割

默认插槽设置文字;`content-position` 取值 left/center/right。

```vue
<template>
  <span>少年</span>
  <el-divider content-position="center">分割</el-divider>
  <span>青年</span>
  <el-divider content-position="right">分割</el-divider>
  <span>中年</span>
</template>
```

### 场景 2:纵向分割

`direction="vertical"` 纵向(需在 flex 容器内)。

```vue
<template>
  <div class="row">
    <span>雨</span>
    <el-divider direction="vertical" />
    <span>雪</span>
    <el-divider direction="vertical" />
    <span>晴</span>
  </div>
</template>

<style scoped>
.row { display: flex; align-items: center; gap: {spacing-sm}; color: {color-text-primary}; }
</style>
```

### 场景 3:虚线与样式

`border-style` 取值 solid/dashed/dotted;`dashed` 是 dashed 的快捷写法(2.7+)。

```vue
<template>
  <div>实线</div>
  <el-divider border-style="dashed" />
  <div>虚线</div>
  <el-divider border-style="dotted" />
  <div>点线</div>
</template>
```

### 场景 4:带图标

`icon` 属性设置分割线图标。

```vue
<template>
  <el-divider :icon="Star">收藏分割</el-divider>
</template>

<script setup>
import { Star } from '@element-plus/icons-vue'
</script>
```

## 参考链接

- Element Plus 官方文档 - Divider 分割线: https://element-plus.org/zh-CN/component/divider
