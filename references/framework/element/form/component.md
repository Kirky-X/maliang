# Form 表单

> Element Plus 表单组件 `<el-form>` `<el-form-item>`,支持校验规则、行内表单、标签对齐等。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-form> <el-form-item>
```

`<el-form>` 为容器,`model` 绑定数据对象,`rules` 定义校验规则;`<el-form-item>` 为表单项,`prop` 对应 model 字段以触发校验。

## 基本用法

```vue
<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
    <el-form-item label="用户名" prop="name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">提交</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'
const formRef = ref()
const form = reactive({ name: '' })
const rules = { name: [{ required: true, message: '请输入用户名', trigger: 'blur' }] }
const onSubmit = async () => {
  await formRef.value.validate()
}
</script>
```

## 使用场景

### 场景 1:行内表单与对齐

`inline` 开启行内表单;`label-position` 取值 `left`/`right`/`top`。

```vue
<template>
  <el-form :inline="true" :model="form" label-position="right">
    <el-form-item label="关键词"><el-input v-model="form.kw" /></el-form-item>
    <el-form-item><el-button type="primary">查询</el-button></el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
const form = reactive({ kw: '' })
</script>
```

### 场景 2:自定义校验规则

`validator` 自定义校验函数。

```vue
<template>
  <el-form ref="formRef" :model="form" :rules="rules">
    <el-form-item label="年龄" prop="age">
      <el-input v-model.number="form.age" />
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'
const formRef = ref()
const form = reactive({ age: '' })
const checkAge = (rule, value, callback) => {
  if (!value) return callback(new Error('年龄不能为空'))
  if (!Number.isInteger(value)) return callback(new Error('请输入数字'))
  if (value < 18) return callback(new Error('必须年满 18 岁'))
  callback()
}
const rules = { age: [{ validator: checkAge, trigger: 'blur' }] }
</script>
```

### 场景 3:尺寸与禁用

`size` 设置表单内组件尺寸;`disabled` 禁用所有表单项。

```vue
<template>
  <el-form :model="form" size="small" disabled>
    <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
const form = reactive({ name: '' })
</script>

<style scoped>
:deep(.el-form-item__label) { color: {color-text-primary}; }
:deep(.el-form-item.is-disabled) { opacity: {opacity-disabled}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Form 表单: https://element-plus.org/zh-CN/component/form
