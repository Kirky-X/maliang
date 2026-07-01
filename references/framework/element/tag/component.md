# Tag 标签

> Element Plus 标签组件 `<el-tag>`,用于标记与分类。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-tag>
```

通过 `type` 区分语义,`effect` 取值 dark/light/plain,`closable` 可关闭,`size` 控制尺寸,`round` 圆角。

## 基本用法

```vue
<template>
  <el-tag>默认</el-tag>
  <el-tag type="success">成功</el-tag>
  <el-tag type="warning">警告</el-tag>
  <el-tag type="danger">危险</el-tag>
  <el-tag type="info">信息</el-tag>
</template>

<style scoped>
:deep(.el-tag) { margin-right: {spacing-sm}; }
</style>
```

## 使用场景

### 场景 1:主题与圆角

`effect` 切换主题;`round` 全圆角;`hit` 描边。

```vue
<template>
  <el-tag effect="dark">深色</el-tag>
  <el-tag effect="plain">朴素</el-tag>
  <el-tag round>圆角</el-tag>
</template>
```

### 场景 2:可关闭与动态

`closable` 显示关闭按钮,`@close` 监听关闭。

```vue
<template>
  <el-tag
    v-for="t in tags"
    :key="t"
    closable
    @close="tags = tags.filter((x) => x !== t)"
  >
    {{ t }}
  </el-tag>
</template>

<script setup>
import { ref } from 'vue'
const tags = ref(['标签一', '标签二', '标签三'])
</script>

<style scoped>
:deep(.el-tag) { margin-right: {spacing-sm}; margin-bottom: {spacing-sm}; }
</style>
```

### 场景 3:带图标与尺寸

`#default` 插槽放图标;`size` 取值 large/default/small。

```vue
<template>
  <el-tag size="large" type="success">
    <el-icon><Check /></el-icon>
    已完成
  </el-tag>
</template>

<script setup>
import { Check } from '@element-plus/icons-vue'
</script>
```

## 参考链接

- Element Plus 官方文档 - Tag 标签: https://element-plus.org/zh-CN/component/tag
