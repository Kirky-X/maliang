# Tabs 标签页

> Element Plus 标签页组件 `<el-tabs>` `<el-tab-pane>`,用于在同一个面板内切换不同视图。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-tabs> <el-tab-pane>
```

`<el-tabs>` 为容器,`v-model` 绑定当前激活的 `name`;`<el-tab-pane>` 为每个标签页内容,通过 `label` 设置标题、`name` 设置标识。

## 基本用法

```vue
<template>
  <el-tabs v-model="active" class="demo-tabs">
    <el-tab-pane label="用户" name="user">用户管理</el-tab-pane>
    <el-tab-pane label="配置" name="config">配置管理</el-tab-pane>
    <el-tab-pane label="角色" name="role">角色管理</el-tab-pane>
  </el-tabs>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('user')
</script>

<style scoped>
.demo-tabs { color: {color-text-primary}; font-size: {font-size-md}; }
</style>
```

## 使用场景

### 场景 1:卡片式与边框式

`type` 取值 `card` / `border-card`,默认为空(线条式)。

```vue
<template>
  <el-tabs v-model="active" type="card">
    <el-tab-pane label="卡片 A" name="a">A</el-tab-pane>
    <el-tab-pane label="卡片 B" name="b">B</el-tab-pane>
  </el-tabs>
  <el-tabs v-model="active2" type="border-card">
    <el-tab-pane label="边框 A" name="a">A</el-tab-pane>
    <el-tab-pane label="边框 B" name="b">B</el-tab-pane>
  </el-tabs>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('a')
const active2 = ref('a')
</script>

<style scoped>
:deep(.el-tabs__item.is-active) { color: {color-primary}; }
</style>
```

### 场景 2:位置与可关闭

`tab-position` 取值 `top`/`right`/`bottom`/`left`;`closable` 允许关闭标签,`addable` 允许新增。

```vue
<template>
  <el-tabs v-model="active" tab-position="left" closable @tab-remove="onRemove">
    <el-tab-pane v-for="t in tabs" :key="t.name" :label="t.label" :name="t.name">
      {{ t.label }} 内容
    </el-tab-pane>
  </el-tabs>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('1')
const tabs = ref([
  { label: '标签一', name: '1' },
  { label: '标签二', name: '2' },
  { label: '标签三', name: '3' },
])
const onRemove = (name) => {
  tabs.value = tabs.value.filter((t) => t.name !== name)
}
</script>
```

### 场景 3:自定义标签内容

`#label` 插槽可自定义标签(如图标 + 文字)。

```vue
<template>
  <el-tabs v-model="active">
    <el-tab-pane name="user">
      <template #label>
        <span class="label-custom"><el-icon><User /></el-icon> 用户</span>
      </template>
      用户管理
    </el-tab-pane>
  </el-tabs>
</template>

<script setup>
import { ref } from 'vue'
import { User } from '@element-plus/icons-vue'
const active = ref('user')
</script>

<style scoped>
.label-custom { display: inline-flex; align-items: center; gap: {spacing-xs}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Tabs 标签页: https://element-plus.org/zh-CN/component/tabs
