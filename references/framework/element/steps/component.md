# Steps 步骤条

> Element Plus 步骤条组件 `<el-steps>` `<el-step>`,用于引导用户按步骤完成任务。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-steps> <el-step>
```

`<el-steps>` 为容器,`active` 设置当前步骤(从 0 开始),`direction` 控制方向,`process-status`/`finish-status` 控制状态;`<el-step>` 为单步,`title`/`description`/`icon`。

## 基本用法

```vue
<template>
  <el-steps :active="active" finish-status="success">
    <el-step title="步骤 1" />
    <el-step title="步骤 2" />
    <el-step title="步骤 3" />
  </el-steps>
  <el-button @click="next">下一步</el-button>
</template>

<script setup>
import { ref } from 'vue'
const active = ref(0)
const next = () => { if (active.value < 2) active.value++ }
</script>

<style scoped>
:deep(.el-step__title.is-process) { color: {color-text-primary}; }
:deep(.el-step__title.is-finish) { color: {color-success}; }
</style>
```

## 使用场景

### 场景 1:居中与描述

`align-center` 居中;`description` 设置描述文字。

```vue
<template>
  <el-steps :active="1" align-center>
    <el-step title="填写" description="填写基本信息" />
    <el-step title="确认" description="确认订单信息" />
    <el-step title="完成" description="支付完成" />
  </el-steps>
</template>
```

### 场景 2:竖向与图标

`direction="vertical"` 竖向;`icon` 自定义步骤图标。

```vue
<template>
  <el-steps direction="vertical" :active="1">
    <el-step title="注册" :icon="Edit" />
    <el-step title="审核" :icon="Upload" />
    <el-step title="完成" :icon="Check" />
  </el-steps>
</template>

<script setup>
import { Edit, Upload, Check } from '@element-plus/icons-vue'
</script>
```

### 场景 3:简单模式与状态

`simple` 简单模式;`status` 单独设置某步状态(wait/process/finish/error/success)。

```vue
<template>
  <el-steps :active="2" simple>
    <el-step title="A" />
    <el-step title="B" />
    <el-step title="C" status="error" />
  </el-steps>
</template>
```

## 参考链接

- Element Plus 官方文档 - Steps 步骤条: https://element-plus.org/zh-CN/component/steps
