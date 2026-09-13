# Segmented 分段控制器

> Element Plus 分段控制器 `<el-segmented>`(2.7+),用于 2-5 项互斥的视图切换/筛选,介于 tabs 与 radio 之间。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-segmented>
```

`v-model` 绑定选中值;`options` 支持原始值数组或 `{ label, value, disabled }` 对象数组。

## 基本用法

```vue
<template>
  <el-segmented v-model="range" :options="['日', '周', '月']" />
</template>

<script setup>
import { ref } from 'vue'
const range = ref('周')
</script>

<style scoped>
.el-segmented {
  --el-segmented-item-selected-bg-color: {color-primary};
  --el-segmented-item-selected-color: {color-text-inverse};
}
</style>
```

## 使用场景

### 场景 1:数据视图切换(日/周/月)

```vue
<template>
  <div class="toolbar">
    <span class="title">数据趋势</span>
    <el-segmented v-model="range" :options="opts" @change="reload" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const range = ref('week')
const opts = [
  { label: '日', value: 'day' },
  { label: '周', value: 'week' },
  { label: '月', value: 'month' }
]
const reload = () => console.log('按', range.value, '刷新')
</script>
```

### 场景 2:自定义选项内容(图标 + 文本)

`options` 的对象项可用 `slot` 渲染自定义内容(经默认插槽)。

```vue
<template>
  <el-segmented v-model="mode" :options="modes">
    <template #default="{ item }">
      <span class="mode-item">
        <el-icon><component :is="item.icon" /></el-icon>
        {{ item.label }}
      </span>
    </template>
  </el-segmented>
</template>

<script setup>
import { ref } from 'vue'
import { MapLocation, Sunny, Warning } from '@element-plus/icons-vue'
const mode = ref('standard')
const modes = [
  { label: '标准', value: 'standard', icon: MapLocation },
  { label: '卫星', value: 'satellite', icon: Sunny },
  { label: '路况', value: 'traffic', icon: Warning }
]
</script>
```

### 场景 3:块状大尺寸(block)

`size="large"` + `block` 撑满容器,适合工具栏满宽筛选。

```vue
<template>
  <el-segmented v-model="sort" block size="large" :options="['综合', '销量', '价格', '好评']" />
</template>

<script setup>
import { ref } from 'vue'
const sort = ref('综合')
</script>
```

## 参考链接

- Element Plus 官方文档 - Segmented 分段控制器: https://element-plus.org/zh-CN/component/segmented
