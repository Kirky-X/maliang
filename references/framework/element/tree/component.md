# Tree 树形

> Element Plus 树形组件 `<el-tree>`,支持懒加载、复选、拖拽、过滤。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-tree>
```

通过 `data` 绑定树数据(含 `label`/`children`),`props` 自定义字段,`lazy` + `load` 懒加载,`show-checkbox` 显示复选框,`node-key` 标识节点。

## 基本用法

```vue
<template>
  <el-tree :data="data" :props="defaultProps" @node-click="onClick" />
</template>

<script setup>
const data = [
  { label: '一级 1', children: [{ label: '二级 1-1' }] },
  { label: '一级 2', children: [{ label: '二级 2-1' }] },
]
const defaultProps = { children: 'children', label: 'label' }
const onClick = (node) => console.log(node)
</script>

<style scoped>
:deep(.el-tree-node__content) { color: {color-text-primary}; }
</style>
```

## 使用场景

### 场景 1:复选与默认展开

`show-checkbox` 显示复选框;`default-expanded-keys` / `default-checked-keys` 设默认值。

```vue
<template>
  <el-tree
    :data="data"
    show-checkbox
    node-key="id"
    :default-expanded-keys="[1]"
    :default-checked-keys="[11]"
  />
</template>

<script setup>
const data = [
  { id: 1, label: '一级 1', children: [{ id: 11, label: '二级 1-1' }] },
  { id: 2, label: '一级 2' },
]
</script>
```

### 场景 2:懒加载

`lazy` + `load(node, resolve)` 按需加载子节点。

```vue
<template>
  <el-tree :props="props" lazy :load="load" node-key="id" />
</template>

<script setup>
const props = { label: 'name', children: 'zones', isLeaf: 'leaf' }
const load = (node, resolve) => {
  if (node.level === 0) return resolve([{ name: '根', id: 1 }])
  setTimeout(() => resolve([{ name: '子 ' + node.label, id: Date.now() }]), 500)
}
</script>
```

### 场景 3:过滤

`filter-node-method` 配合 ref 调用 `filter` 实现搜索。

```vue
<template>
  <el-input v-model="kw" placeholder="过滤" />
  <el-tree ref="treeRef" :data="data" :filter-node-method="filterNode" />
</template>

<script setup>
import { ref, watch } from 'vue'
const treeRef = ref()
const kw = ref('')
const data = [{ label: '苹果' }, { label: '香蕉' }]
const filterNode = (value, data) => !value || data.label.includes(value)
watch(kw, (v) => treeRef.value?.filter(v))
</script>
```

## 参考链接

- Element Plus 官方文档 - Tree 树形控件: https://element-plus.org/zh-CN/component/tree
