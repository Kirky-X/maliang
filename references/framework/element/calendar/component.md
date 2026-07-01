# Calendar 日历

> Element Plus 日历组件 `<el-calendar>`,用于显示日期与按月/年浏览。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-calendar>
```

通过 `v-model` 绑定当前日期,`range` 设置日期范围,`#date-cell` 插槽自定义单元格。

## 基本用法

```vue
<template>
  <el-calendar v-model="date" />
</template>

<script setup>
import { ref } from 'vue'
const date = ref(new Date('2026-07-01'))
</script>

<style scoped>
:deep(.el-calendar) { border-radius: {radius-md}; }
:deep(.el-calendar-day):hover { background-color: {color-bg-secondary}; }
</style>
```

## 使用场景

### 场景 1:自定义单元格

`#date-cell` 插槽作用域参数 `{ date, data }`,自定义每日内容。

```vue
<template>
  <el-calendar v-model="date">
    <template #date-cell="{ data }">
      <div class="cell">
        <span>{{ data.day.split('-').slice(2).join() }}</span>
        <el-tag v-if="tasks[data.day]" size="small" type="danger">
          {{ tasks[data.day] }}
        </el-tag>
      </div>
    </template>
  </el-calendar>
</template>

<script setup>
import { ref } from 'vue'
const date = ref(new Date('2026-07-01'))
const tasks = { '2026-07-01': '会议', '2026-07-05': '发布' }
</script>

<style scoped>
.cell { display: flex; flex-direction: column; align-items: center; gap: {spacing-xs}; }
</style>
```

### 场景 2:日期范围

`range` 设置起止日期数组,限制可浏览范围。

```vue
<template>
  <el-calendar :range="range" />
</template>

<script setup>
const range = [new Date('2026-07-01'), new Date('2026-07-31')]
</script>
```

## 参考链接

- Element Plus 官方文档 - Calendar 日历: https://element-plus.org/zh-CN/component/calendar
