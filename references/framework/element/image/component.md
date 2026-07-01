# Image 图片

> Element Plus 图片组件 `<el-image>`,支持懒加载、占位、预览与加载失败兜底。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-image>
```

通过 `src` 设置图片地址,`lazy` 开启懒加载,`preview-src-list` 开启大图预览,`fit` 控制填充方式。占位与失败态可自定义插槽。

## 基本用法

```vue
<template>
  <el-image :src="url" fit="cover" class="demo-image" />
</template>

<script setup>
const url = 'https://example.com/photo.png'
</script>

<style scoped>
.demo-image {
  width: 200px;
  height: 200px;
  border-radius: {radius-md};
  border: 1px solid {color-border-default};
}
</style>
```

## 使用场景

### 场景 1:懒加载 + 占位

`lazy` 开启懒加载(滚动到视口才加载),`#placeholder` 自定义加载中占位。

```vue
<template>
  <el-image :src="url" lazy fit="cover" class="demo-image">
    <template #placeholder>
      <div class="placeholder">加载中...</div>
    </template>
  </el-image>
</template>

<script setup>
const url = 'https://example.com/photo.png'
</script>

<style scoped>
.demo-image { width: 200px; height: 200px; border-radius: {radius-md}; }
.placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  background-color: {color-bg-secondary};
  color: {color-text-primary};
  font-size: {font-size-sm};
}
</style>
```

### 场景 2:加载失败兜底

`#error` 插槽自定义加载失败显示。

```vue
<template>
  <el-image :src="badUrl" fit="cover" class="demo-image">
    <template #error>
      <div class="error-slot">
        <el-icon><Picture /></el-icon>
        <span>加载失败</span>
      </div>
    </template>
  </el-image>
</template>

<script setup>
import { Picture } from '@element-plus/icons-vue'
const badUrl = 'https://broken.example.com/x.png'
</script>

<style scoped>
.demo-image { width: 200px; height: 200px; border-radius: {radius-md}; }
.error-slot {
  width: 100%; height: 100%;
  display: flex; flex-direction: column; gap: {spacing-xs};
  align-items: center; justify-content: center;
  background-color: {color-bg-secondary};
  color: {color-text-primary};
  font-size: {font-size-sm};
}
</style>
```

### 场景 3:大图预览

`preview-src-list` 传入图片数组开启预览,`initial-index` 设置初始索引,`zoom-rate` 控制缩放比率。

```vue
<template>
  <el-image
    :src="urls[0]"
    :preview-src-list="urls"
    :initial-index="0"
    fit="cover"
    preview-teleported
    class="demo-image"
  />
</template>

<script setup>
const urls = [
  'https://example.com/a.png',
  'https://example.com/b.png',
  'https://example.com/c.png',
]
</script>

<style scoped>
.demo-image { width: 200px; height: 200px; border-radius: {radius-md}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Image 图片: https://element-plus.org/zh-CN/component/image
