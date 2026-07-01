# Badge 徽章

> Element Plus 徽章组件 `<el-badge>`,用于在元素右上角显示数字或状态点。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-badge>
```

通过 `value` 设置内容(数字或文字),`max` 设置上限(超出显示 `max+`),`is-dot` 显示红点,`hidden` 隐藏,`type` 设置颜色。

## 基本用法

```vue
<template>
  <el-badge :value="12" class="item">
    <el-button>消息</el-button>
  </el-badge>
  <el-badge :value="200" :max="99" class="item">
    <el-button>消息</el-button>
  </el-badge>
</template>

<style scoped>
:deep(.item) { margin-right: {spacing-md}; }
</style>
```

## 使用场景

### 场景 1:红点与文字

`is-dot` 显示红点;`value` 传文字。

```vue
<template>
  <el-badge is-dot class="item">
    <el-icon><Bell /></el-icon>
  </el-badge>
  <el-badge value="new" class="item">
    <el-button>动态</el-button>
  </el-badge>
</template>

<script setup>
import { Bell } from '@element-plus/icons-vue'
</script>
```

### 场景 2:颜色与隐藏

`type` 取值 primary/success/warning/danger/info;`hidden` 隐藏徽章。

```vue
<template>
  <el-badge :value="3" type="danger" :hidden="hidden" class="item">
    <el-button>待办</el-button>
  </el-badge>
  <el-button size="small" @click="hidden = !hidden">切换</el-button>
</template>

<script setup>
import { ref } from 'vue'
const hidden = ref(false)
</script>
```

### 场景 3:自定义内容

`#default` 设置主体,`value` 可为 VNode(通过插槽 `value` 自定义)。

```vue
<template>
  <el-badge value="999+">
    <template #default>
      <div class="box">回复</div>
    </template>
  </el-badge>
</template>

<style scoped>
.box { padding: {spacing-md}; background-color: {color-bg-secondary}; border-radius: {radius-md}; color: {color-text-primary}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Badge 徽章: https://element-plus.org/zh-CN/component/badge
