# Timeline 时间线

> Element Plus 时间线组件 `<el-timeline>` `<el-timeline-item>`,用于可视化时间流转。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-timeline> <el-timeline-item>
```

`<el-timeline>` 为容器;`<el-timeline-item>` 为节点,`timestamp` 设置时间,`placement` 控制时间位置,`type` 设置节点颜色,`hollow` 空心节点。

## 基本用法

```vue
<template>
  <el-timeline>
    <el-timeline-item v-for="(a, i) in activities" :key="i" :timestamp="a.time">
      {{ a.content }}
    </el-timeline-item>
  </el-timeline>
</template>

<script setup>
const activities = [
  { content: '启动', time: '2026-07-01 09:00' },
  { content: '构建', time: '2026-07-01 10:00' },
  { content: '部署', time: '2026-07-01 11:00' },
]
</script>

<style scoped>
:deep(.el-timeline-item__content) { color: {color-text-primary}; }
</style>
```

## 使用场景

### 场景 1:节点颜色与空心

`type` 取值 primary/success/warning/danger;`hollow` 空心节点;`size` 取值 normal/large。

```vue
<template>
  <el-timeline>
    <el-timeline-item type="primary" timestamp="步骤一">创建</el-timeline-item>
    <el-timeline-item type="success" hollow timestamp="步骤二">审核</el-timeline-item>
    <el-timeline-item type="danger" timestamp="步骤三">驳回</el-timeline-item>
  </el-timeline>
</template>
```

### 场景 2:时间位置与自定义

`placement` 取值 top/bottom;`timestamp` 也可放插槽;`#dot` 自定义节点。

```vue
<template>
  <el-timeline>
    <el-timeline-item placement="top" timestamp="2026-07-01">
      <el-card>
        <h4>自定义卡片</h4>
        <p>详细内容</p>
      </el-card>
    </el-timeline-item>
    <el-timeline-item>
      <template #dot><el-icon style="color: {color-primary}"><Promotion /></el-icon></template>
      自定义节点
    </el-timeline-item>
  </el-timeline>
</template>

<script setup>
import { Promotion } from '@element-plus/icons-vue'
</script>
```

## 参考链接

- Element Plus 官方文档 - Timeline 时间线: https://element-plus.org/zh-CN/component/timeline
