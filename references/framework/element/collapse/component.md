# Collapse 折叠面板

> Element Plus 折叠面板组件 `<el-collapse>` `<el-collapse-item>`,用于内容折叠展开。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-collapse> <el-collapse-item>
```

`<el-collapse>` 为容器,`v-model` 绑定展开项数组;`<el-collapse-item>` 为面板项,`name` 为标识,`title` 为标题。

## 基本用法

```vue
<template>
  <el-collapse v-model="active">
    <el-collapse-item title="一致性" name="1">
      <div>与现实生活一致</div>
    </el-collapse-item>
    <el-collapse-item title="反馈" name="2">
      <div>页面反馈</div>
    </el-collapse-item>
  </el-collapse>
</template>

<script setup>
import { ref } from 'vue'
const active = ref(['1'])
</script>

<style scoped>
:deep(.el-collapse-item__header) { color: {color-text-primary}; }
:deep(.el-collapse-item__content) { color: {color-text-primary}; }
</style>
```

## 使用场景

### 场景 1:手风琴模式

`accordion` 只允许展开一项。

```vue
<template>
  <el-collapse v-model="active" accordion>
    <el-collapse-item title="A" name="a"><div>A 内容</div></el-collapse-item>
    <el-collapse-item title="B" name="b"><div>B 内容</div></el-collapse-item>
  </el-collapse>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('a')
</script>
```

### 场景 2:自定义标题与内容

`#title` 插槽自定义标题;内容放默认插槽。

```vue
<template>
  <el-collapse v-model="active">
    <el-collapse-item name="1">
      <template #title>
        <span class="title"><el-icon><User /></el-icon> 自定义标题</span>
      </template>
      <div>自定义内容</div>
    </el-collapse-item>
  </el-collapse>
</template>

<script setup>
import { ref } from 'vue'
import { User } from '@element-plus/icons-vue'
const active = ref(['1'])
</script>

<style scoped>
.title { display: inline-flex; align-items: center; gap: {spacing-xs}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Collapse 折叠面板: https://element-plus.org/zh-CN/component/collapse
