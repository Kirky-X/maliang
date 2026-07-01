# Progress 进度条

> Element Plus 进度条组件 `<el-progress>`,支持百分比、状态、条纹动画与环形/仪表盘。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-progress>
```

通过 `percentage` 设置百分比(0-100),`status` 切换 success/exception/warning 状态,`type` 切换 line/circle/dashboard,`stripe` 显示条纹。

## 基本用法

```vue
<template>
  <el-progress :percentage="50" />
  <el-progress :percentage="80" :color="customColor" />
</template>

<script setup>
const customColor = '#409eff'
</script>

<style scoped>
:deep(.el-progress-bar__inner) { background-color: {color-primary}; }
</style>
```

## 使用场景

### 场景 1:状态进度条

`status` 取值 `success` / `exception` / `warning`,自动应用功能色。

```vue
<template>
  <el-progress :percentage="100" status="success" />
  <el-progress :percentage="70" status="warning" />
  <el-progress :percentage="40" status="exception" />
</template>

<script setup>
// status → 功能色映射:
//   success  → {color-success}
//   warning  → {color-warning}
//   exception→ {color-danger}
</script>
```

### 场景 2:条纹动画

`striped` 显示条纹,`striped-flow` 开启动画流动。

```vue
<template>
  <el-progress :percentage="60" striped striped-flow :duration="10" />
</template>
```

### 场景 3:环形与仪表盘

`type="circle"` 环形,`type="dashboard"` 仪表盘;`width` 控制画布尺寸,`stroke-width` 控制线宽。

```vue
<template>
  <el-progress type="circle" :percentage="75" :width="120" />
  <el-progress type="dashboard" :percentage="60" :width="120" />
</template>
```

### 场景 4:自定义颜色阶梯

`color` 传入数组按百分比阶梯着色。

```vue
<template>
  <el-progress :percentage="percentage" :color="colors" />
  <el-button @click="add">+10</el-button>
</template>

<script setup>
import { ref, computed } from 'vue'
const percentage = ref(30)
const colors = [
  { color: '{color-danger}', percentage: 40 },
  { color: '{color-warning}', percentage: 70 },
  { color: '{color-success}', percentage: 100 },
]
const add = () => { percentage.value = Math.min(100, percentage.value + 10) }
</script>
```

## 参考链接

- Element Plus 官方文档 - Progress 进度条: https://element-plus.org/zh-CN/component/progress
