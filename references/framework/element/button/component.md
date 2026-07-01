# Button 按钮

> Element Plus 按钮组件 `<el-button>`,用于触发用户操作。本文件给出组件标签、基本用法与典型使用场景;API 完整定义(属性/事件/方法/插槽)见 [api.md](./api.md)。

## 组件标签

```
<el-button>
```

按钮通过 `type` 区分语义(primary / success / warning / danger / info),通过 `size` 控制尺寸,`plain` / `round` / `circle` 控制外观变体。所有视觉值引用 design token,不在组件内硬编码颜色。

## 基本用法

默认按钮(不设 `type`)为次级按钮;设置 `type` 切换语义色。

```vue
<template>
  <el-button>默认按钮</el-button>
  <el-button type="primary">主要按钮</el-button>
</template>

<script setup>
// 基本按钮:语义色由 type 控制,映射到 {color-primary} 等功能色 token
</script>
```

## 使用场景

### 场景 1:五种语义类型

`type` 取值 `primary` / `success` / `warning` / `danger` / `info`,分别映射到对应功能色 token(功能色语义全局一致,见 references/dimensions/color.md)。

```vue
<template>
  <div class="button-row">
    <el-button type="primary">主要</el-button>
    <el-button type="success">成功</el-button>
    <el-button type="warning">警告</el-button>
    <el-button type="danger">危险</el-button>
    <el-button type="info">信息</el-button>
  </div>
</template>

<script setup>
// type → 功能色 token 映射:
//   primary → {color-primary}
//   success → {color-success}
//   warning → {color-warning}
//   danger  → {color-danger}
//   info    → {color-info}
</script>

<style scoped>
.button-row {
  display: flex;
  gap: {spacing-sm};
}
</style>
```

### 场景 2:三种尺寸

`size` 取值 `large` / `default` / `small`。

```vue
<template>
  <div class="button-row">
    <el-button size="large" type="primary">大型</el-button>
    <el-button size="default" type="primary">默认</el-button>
    <el-button size="small" type="primary">小型</el-button>
  </div>
</template>

<script setup>
// size → 高度/内边距 token 映射:
//   large   → height {component-size-lg}, padding {spacing-md} {spacing-lg}
//   default → height {component-size-md}, padding {spacing-sm} {spacing-md}
//   small   → height {component-size-sm}, padding {spacing-xs} {spacing-sm}
</script>

<style scoped>
.button-row {
  display: flex;
  align-items: center;
  gap: {spacing-sm};
}
</style>
```

### 场景 3:plain / round / circle 外观变体

- `plain` — 朴素按钮:透明背景 + 语义色描边
- `round` — 圆角按钮:圆角半径 {radius-full}
- `circle` — 圆形按钮:正圆,仅放图标,常用于工具栏

```vue
<template>
  <div class="button-row">
    <el-button type="primary" plain>朴素</el-button>
    <el-button type="primary" round>圆角</el-button>
    <el-button type="primary" circle :icon="Search" />
  </div>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
// plain  → 背景透明,边框色 {color-primary},文字色 {color-primary}
// round  → 圆角半径 {radius-full}
// circle → 宽高相等,圆角 {radius-full},仅容纳图标
</script>

<style scoped>
.button-row {
  display: flex;
  align-items: center;
  gap: {spacing-sm};
}
</style>
```

### 场景 4:图标 + 加载态

通过 `icon` 传入图标组件,`loading` 控制加载态(加载时按钮不可重复点击)。

```vue
<template>
  <el-button type="primary" :icon="Search" :loading="loading" @click="onSubmit">
    查询
  </el-button>
</template>

<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const loading = ref(false)
const onSubmit = async () => {
  loading.value = true
  try {
    await fetchData()
  } finally {
    loading.value = false
  }
}
async function fetchData() {
  // 异步请求
}
</script>
```

### 场景 5:禁用 + 按钮组

`disabled` 禁用单个按钮;`<el-button-group>` 把多个按钮编为一组。

```vue
<template>
  <el-button-group>
    <el-button type="primary" :icon="ArrowLeft">上一页</el-button>
    <el-button type="primary" disabled>当前页</el-button>
    <el-button type="primary">
      下一页<el-icon class="el-icon--right"><ArrowRight /></el-icon>
    </el-button>
  </el-button-group>
</template>

<script setup>
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
// disabled → 降透明度 {opacity-disabled},保留语义色可读性(见 references/dimensions/color.md §7)
</script>
```
