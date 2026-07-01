# Pagination 分页

> Element Plus 分页组件 `<el-pagination>`,支持布局自定义、每页条数、跳转。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-pagination>
```

通过 `total` 设置总数,`v-model:current-page` 绑定当前页,`v-model:page-size` 绑定每页条数,`layout` 控制布局,`page-sizes` 设置可选条数。

## 基本用法

```vue
<template>
  <el-pagination
    v-model:current-page="page"
    v-model:page-size="size"
    :total="200"
    layout="prev, pager, next"
    @current-change="onChange"
  />
</template>

<script setup>
import { ref } from 'vue'
const page = ref(1)
const size = ref(10)
const onChange = (p) => console.log(p)
</script>

<style scoped>
:deep(.el-pagination) { color: {color-text-primary}; }
:deep(.el-pager li.is-active) { color: {color-primary}; }
</style>
```

## 使用场景

### 场景 1:完整布局与每页条数

`layout` 用逗号组合 `total`/`sizes`/`prev`/`pager`/`next`/`jumper`。

```vue
<template>
  <el-pagination
    :total="1000"
    :page-sizes="[10, 20, 50, 100]"
    layout="total, sizes, prev, pager, next, jumper"
  />
</template>
```

### 场景 2:小型与背景

`small` 紧凑模式;`background` 显示分页按钮背景。

```vue
<template>
  <el-pagination :total="50" small background layout="prev, pager, next" />
</template>
```

### 场景 3:事件监听

`@size-change` 监听每页条数变化,`@current-change` 监听页码变化。

```vue
<template>
  <el-pagination
    :total="200"
    :page-sizes="[10, 20, 50]"
    layout="sizes, prev, pager, next"
    @size-change="onSize"
    @current-change="onPage"
  />
</template>

<script setup>
const onSize = (s) => console.log('size', s)
const onPage = (p) => console.log('page', p)
</script>
```

## 参考链接

- Element Plus 官方文档 - Pagination 分页: https://element-plus.org/zh-CN/component/pagination
