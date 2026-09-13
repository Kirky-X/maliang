# Select 下拉选择器

> Element Plus 选择组件 `<el-select>` + `<el-option>` + `<el-select-v2>`(虚拟滚动),用于表单内**数据录入**——从选项集中选定一个或多个值。与动作菜单 [`<el-dropdown>`](../dropdown/component.md) 明确区分。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-select> <el-option> <el-option-group> <el-select-v2>
```

- `<el-select>`:选择器容器,`v-model` 绑定选中值。
- `<el-option>`:单个选项,`value` 为提交值、`label` 为显示文本。
- `<el-select-v2>`:大选项集(>100 项)虚拟滚动版本。

## 基本用法

```vue
<template>
  <el-select v-model="city" placeholder="请选择城市" clearable>
    <el-option
      v-for="c in cities"
      :key="c.value"
      :label="c.label"
      :value="c.value"
    />
  </el-select>
</template>

<script setup>
import { ref } from 'vue'
const city = ref('')
const cities = [
  { value: 'shanghai', label: '上海' },
  { value: 'beijing', label: '北京' },
  { value: 'guangzhou', label: '广州' }
]
</script>

<style scoped>
.el-select { --el-select-border-color-hover: {color-primary}; }
</style>
```

## 使用场景

### 场景 1:表单内常规选择(3-10 项)

配合 `<el-form-item>` 声明式校验;`placeholder` 未选占位,`clearable` 一键清空。

```vue
<template>
  <el-form :model="form" :rules="rules">
    <el-form-item label="商品分类" prop="category">
      <el-select v-model="form.category" placeholder="请选择分类">
        <el-option label="数码" value="digital" />
        <el-option label="家电" value="appliance" />
        <el-option label="服饰" value="clothing" />
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
const form = reactive({ category: '' })
const rules = { category: [{ required: true, message: '请选择分类', trigger: 'change' }] }
</script>
```

### 场景 2:多选与标签折叠

`multiple` 多选;`collapse-tags` 折叠选中项;`collapse-tags-tooltip` 悬停展开全部。

```vue
<template>
  <el-select v-model="tags" multiple collapse-tags collapse-tags-tooltip placeholder="请选择标签">
    <el-option v-for="t in ['新品', '热卖', '限时', '包邮']" :key="t" :label="t" :value="t" />
  </el-select>
</template>

<script setup>
import { ref } from 'vue'
const tags = ref(['新品'])
</script>
```

### 场景 3:可搜索(选项 >10 项)

`filterable` 开启键入搜索,对齐 vocabulary `select-searchable`;超大选项集换 `<el-select-v2>`。

```vue
<template>
  <el-select-v2
    v-model="userId"
    filterable
    :options="options"
    placeholder="搜索并选择成员"
  />
</template>

<script setup>
import { ref } from 'vue'
const userId = ref('')
const options = Array.from({ length: 200 }, (_, i) => ({
  value: `u${i + 1}`,
  label: `成员 ${i + 1}`
}))
</script>
```

## 参考链接

- Element Plus 官方文档 - Select 选择器: https://element-plus.org/zh-CN/component/select
- Select V2 虚拟列表选择器: https://element-plus.org/zh-CN/component/select-v2
