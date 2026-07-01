# Table 表格

> Element Plus 表格组件 `<el-table>` `<el-table-column>`,支持排序、筛选、固定列、多选、自定义渲染。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-table> <el-table-column>
```

`<el-table>` 为容器,`data` 绑定数组;`<el-table-column>` 定义列,`prop` 对应字段,`label` 为表头。

## 基本用法

```vue
<template>
  <el-table :data="tableData" border>
    <el-table-column prop="date" label="日期" width="180" />
    <el-table-column prop="name" label="姓名" width="180" />
    <el-table-column prop="address" label="地址" />
  </el-table>
</template>

<script setup>
const tableData = [
  { date: '2026-07-01', name: '张三', address: '北京' },
  { date: '2026-07-02', name: '李四', address: '上海' },
]
</script>

<style scoped>
:deep(.el-table) {
  border-radius: {radius-md};
  color: {color-text-primary};
}
</style>
```

## 使用场景

### 场景 1:排序与筛选

`sortable` 开启排序(`custom` 由后端排序);列 `filters` + `filter-method` 实现筛选。

```vue
<template>
  <el-table :data="data" @sort-change="onSort">
    <el-table-column prop="name" label="姓名" sortable />
    <el-table-column prop="age" label="年龄" sortable />
    <el-table-column prop="city" label="城市" :filters="filters" :filter-method="filterCity" />
  </el-table>
</template>

<script setup>
const data = [
  { name: '张三', age: 20, city: '北京' },
  { name: '李四', age: 25, city: '上海' },
]
const filters = [{ text: '北京', value: '北京' }, { text: '上海', value: '上海' }]
const filterCity = (value, row) => row.city === value
const onSort = ({ prop, order }) => console.log(prop, order)
</script>
```

### 场景 2:自定义列模板

通过默认插槽自定义单元格内容,作用域参数 `{ row, column, $index }`。

```vue
<template>
  <el-table :data="data">
    <el-table-column label="操作" width="180">
      <template #default="{ row }">
        <el-button size="small" @click="onEdit(row)">编辑</el-button>
        <el-button size="small" type="danger" @click="onDel(row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
const data = [{ id: 1 }]
const onEdit = (row) => console.log('edit', row)
const onDel = (row) => console.log('del', row)
</script>
```

### 场景 3:多选与固定列

`type="selection"` 多选列;`fixed` 固定列(left/right)。

```vue
<template>
  <el-table :data="data" @selection-change="onSel">
    <el-table-column type="selection" width="48" />
    <el-table-column prop="name" label="姓名" fixed="left" />
    <el-table-column prop="addr" label="地址" />
    <el-table-column label="操作" width="100" fixed="right" />
  </el-table>
</template>

<script setup>
const data = [{ name: '张三', addr: '北京' }]
const onSel = (sel) => console.log(sel)
</script>
```

## 参考链接

- Element Plus 官方文档 - Table 表格: https://element-plus.org/zh-CN/component/table
