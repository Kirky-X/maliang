# Checkbox 多选框

> Element Plus 多选组件 `<el-checkbox>` `<el-checkbox-group>` `<el-checkbox-button>`,支持三态(checked/unchecked/indeterminate)。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-checkbox> <el-checkbox-group> <el-checkbox-button>
```

`<el-checkbox-group>` 为容器,`v-model` 绑定值数组;`<el-checkbox>` 为单选项,`value`/`label` 为值;`indeterminate` 属性控制半选态。

## 基本用法

```vue
<template>
  <div>
    <el-checkbox v-model="checked">是否选中</el-checkbox>
    <el-checkbox-group v-model="picked">
      <el-checkbox value="a">选项 A</el-checkbox>
      <el-checkbox value="b">选项 B</el-checkbox>
      <el-checkbox value="c">选项 C</el-checkbox>
    </el-checkbox-group>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const checked = ref(false)
const picked = ref(['a'])
</script>

<style scoped>
.el-checkbox__label { color: {color-text-primary}; }
.el-checkbox__input.is-checked .el-checkbox__inner {
  background-color: {color-primary};
  border-color: {color-primary};
}
</style>
```

## 使用场景

### 场景 1:三态全选(indeterminate)

父级 `indeterminate` 表达"部分子项选中"(Carbon 三态规范:checked/unchecked/indeterminate)。

```vue
<template>
  <el-checkbox
    v-model="checkAll"
    :indeterminate="isIndeterminate"
    @change="handleCheckAll"
  >全选</el-checkbox>
  <el-checkbox-group v-model="checkedCities" @change="handleChecked">
    <el-checkbox v-for="city in cities" :key="city" :value="city">{{ city }}</el-checkbox>
  </el-checkbox-group>
</template>

<script setup>
import { ref, computed } from 'vue'
const cities = ['上海', '北京', '广州']
const checkedCities = ref(['上海'])
const checkAll = ref(false)
const isIndeterminate = computed(() =>
  checkedCities.value.length > 0 && checkedCities.value.length < cities.length
)
const handleCheckAll = (val) => {
  checkAll.value = val
  checkedCities.value = val ? [...cities] : []
}
const handleChecked = (val) => {
  checkAll.value = val.length === cities.length
}
</script>
```

### 场景 2:按钮样式与数量限制

`<el-checkbox-button>` 提供按钮样式;`max`/`min` 限制可选数量。

```vue
<template>
  <el-checkbox-group v-model="picked" :max="2">
    <el-checkbox-button v-for="c in ['A', 'B', 'C']" :key="c" :value="c">{{ c }}</el-checkbox-button>
  </el-checkbox-group>
</template>
```

### 场景 3:禁用与边框

`disabled` 禁用单项;`border` 显示边框样式。

```vue
<template>
  <el-checkbox v-model="v1" border>选项 A</el-checkbox>
  <el-checkbox v-model="v2" disabled>禁用项</el-checkbox>
</template>
```

## 参考链接

- Element Plus 官方文档 - Checkbox 多选框: https://element-plus.org/zh-CN/component/checkbox
