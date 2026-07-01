# Avatar 头像

> Element Plus 头像组件 `<el-avatar>`,支持图片、图标、文字三种内容。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-avatar>
```

通过 `src` 加载图片,`size` 控制尺寸(number/large/default/small),`shape` 控制形状(circle/square),`icon` 设置图标,加载失败回退到插槽或 icon。

## 基本用法

```vue
<template>
  <el-avatar src="https://example.com/u.png" />
  <el-avatar :size="64" src="https://example.com/u.png" />
</template>

<style scoped>
:deep(.el-avatar) { margin-right: {spacing-sm}; }
</style>
```

## 使用场景

### 场景 1:图标与文字回退

`icon` 设置默认图标;插槽放文字;`@error` 监听加载失败。

```vue
<template>
  <el-avatar :icon="UserFilled" />
  <el-avatar>张</el-avatar>
</template>

<script setup>
import { UserFilled } from '@element-plus/icons-vue'
</script>
```

### 场景 2:形状与尺寸

`shape` 取值 `circle`/`square`;`size` 数字或预设。

```vue
<template>
  <el-avatar shape="square" :size="80" src="https://example.com/u.png" />
  <el-avatar size="large" src="https://example.com/u.png" />
</template>
```

### 场景 3:加载失败回退

`@error` 返回 false 阻止默认行为,自定义回退内容。

```vue
<template>
  <el-avatar :src="src" @error="onError">
    <img v-if="failed" src="https://example.com/fallback.png" />
  </el-avatar>
</template>

<script setup>
import { ref } from 'vue'
const src = 'https://broken.example.com/u.png'
const failed = ref(false)
const onError = () => { failed.value = true; return true }
</script>
```

## 参考链接

- Element Plus 官方文档 - Avatar 头像: https://element-plus.org/zh-CN/component/avatar
