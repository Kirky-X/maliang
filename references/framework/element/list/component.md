# Table 列表

> Element Plus 表格组件 `<el-table>`,用于结构化列表数据展示。本文件给出组件标签、基本用法与典型使用场景;API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-table>
```

列表由 `<el-table>`(容器,接收 `data`)与若干 `<el-table-column>`(列定义,接收 `prop`/`label`/`width`)组合实现。`border` 加边框、`stripe` 加斑马纹。

## 基本用法

```vue
<template>
  <el-table :data="tableData">
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="age" label="年龄" />
  </el-table>
</template>

<script setup>
// data 为行对象数组,prop 对应行对象字段
const tableData = [
  { name: '张三', age: 28 },
  { name: '李四', age: 34 }
]
</script>
```

## 使用场景

### 场景 1:columns + data 基础列表

`el-table-column` 的 `prop` 绑定数据字段,`label` 为表头文案,`width` 固定列宽。

```vue
<template>
  <el-table :data="users" style="width: 100%">
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="email" label="邮箱" />
    <el-table-column prop="role" label="角色" />
  </el-table>
</template>

<script setup>
const users = [
  { id: 1, name: '张三', email: 'zhangsan@example.com', role: '管理员' },
  { id: 2, name: '李四', email: 'lisi@example.com', role: '编辑' },
  { id: 3, name: '王五', email: 'wangwu@example.com', role: '访客' }
]
</script>

<style scoped>
/* 表头字号 {font-size-sm} / 字重 {font-weight-medium};行高 {font-size-md} */
</style>
```

### 场景 2:border + stripe 样式

`border` 加竖向边框线,`stripe` 开启斑马纹(隔行底色交替)。

```vue
<template>
  <el-table :data="users" border stripe style="width: 100%">
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="role" label="角色" />
  </el-table>
</template>

<script setup>
const users = [
  { id: 1, name: '张三', role: '管理员' },
  { id: 2, name: '李四', role: '编辑' },
  { id: 3, name: '王五', role: '访客' },
  { id: 4, name: '赵六', role: '编辑' }
]
</script>

<style scoped>
/* border  → 单元格边框色 {color-border}
   stripe  → 斑马行底色 {color-bg-secondary} */
</style>
```

### 场景 3:自定义列渲染(作用域插槽)

通过 `#default="{ row }"` 作用域插槽自定义单元格内容(状态标签、操作按钮等)。

```vue
<template>
  <el-table :data="users" border style="width: 100%">
    <el-table-column prop="name" label="姓名" />
    <el-table-column label="状态">
      <template #default="{ row }">
        <el-tag :type="row.active ? 'success' : 'danger'">
          {{ row.active ? '启用' : '停用' }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="160">
      <template #default="{ row }">
        <el-button size="small" type="primary" link @click="onEdit(row)">编辑</el-button>
        <el-button size="small" type="danger" link @click="onDelete(row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
const users = [
  { name: '张三', active: true },
  { name: '李四', active: false }
]
const onEdit = (row) => { /* 编辑 */ }
const onDelete = (row) => { /* 删除 */ }
</script>
```

### 场景 4:选择列 + 索引列

`type="selection"` 多选列,`type="index"` 序号列;配合 `@selection-change` 监听选中项。

```vue
<template>
  <el-table
    ref="tableRef"
    :data="users"
    border
    style="width: 100%"
    @selection-change="onSelectionChange"
  >
    <el-table-column type="selection" width="48" />
    <el-table-column type="index" label="#" width="60" />
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="role" label="角色" />
  </el-table>
  <p class="hint">已选 {{ selected.length }} 项</p>
</template>

<script setup>
import { ref } from 'vue'
const tableRef = ref()
const selected = ref([])
const users = [
  { name: '张三', role: '管理员' },
  { name: '李四', role: '编辑' }
]
const onSelectionChange = (rows) => { selected.value = rows }
</script>

<style scoped>
.hint { margin-top: {spacing-sm}; font-size: {font-size-sm}; color: {color-text-secondary}; }
</style>
```

### 场景 5:排序列

`sortable` 开启列排序(`true` 为前端排序,`'custom'` 为后端排序,配合 `@sort-change`)。

```vue
<template>
  <el-table :data="users" border style="width: 100%" @sort-change="onSortChange">
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="age" label="年龄" sortable width="120" />
    <el-table-column prop="joinDate" label="加入日期" sortable="custom" width="160" />
  </el-table>
</template>

<script setup>
const users = [
  { name: '张三', age: 28, joinDate: '2023-01-15' },
  { name: '李四', age: 34, joinDate: '2022-11-03' },
  { name: '王五', age: 22, joinDate: '2024-06-20' }
]
// sortable='custom' → 后端排序,排序图标点击触发 sort-change
const onSortChange = ({ prop, order }) => {
  // order: 'ascending' | 'descending' | null
  console.log('排序字段:', prop, '方向:', order)
}
</script>
```
