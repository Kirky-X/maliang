# Switch 开关

> Element Plus 开关组件 `<el-switch>`,用于二值切换。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-switch>
```

通过 `v-model` 绑定布尔值,`active-text`/`inactive-text` 设置两态文字,`active-color`/`inactive-color` 设置颜色,`loading` 显示加载态。

## 基本用法

```vue
<template>
  <el-switch v-model="value" />
</template>

<script setup>
import { ref } from 'vue'
const value = ref(true)
</script>

<style scoped>
:deep(.el-switch.is-checked .el-switch__core) {
  background-color: {color-primary};
  border-color: {color-primary};
}
</style>
```

## 使用场景

### 场景 1:文字与图标

`active-text` / `inactive-text` 设置文字;`active-icon` / `inactive-icon` 设置图标;`inline-prompt` 文字内显。

```vue
<template>
  <el-switch
    v-model="value"
    active-text="开"
    inactive-text="关"
    inline-prompt
  />
  <el-switch v-model="value2" :active-icon="Check" :inactive-icon="Close" />
</template>

<script setup>
import { ref } from 'vue'
import { Check, Close } from '@element-plus/icons-vue'
const value = ref(true)
const value2 = ref(false)
</script>
```

### 场景 2:自定义值与颜色

`active-value` / `inactive-value` 设置两态实际值(可非布尔);`active-color` / `inactive-color` 自定义颜色,建议映射 token。

```vue
<template>
  <el-switch
    v-model="v"
    active-value="on"
    inactive-value="off"
    active-color="#13ce66"
    inactive-color="#ff4949"
  />
</template>

<script setup>
import { ref } from 'vue'
const v = ref('on')
</script>
```

### 场景 3:加载与禁用

`loading` 显示加载态(异步切换);`disabled` 禁用。

```vue
<template>
  <el-switch v-model="v" :loading="loading" :before-change="beforeChange" />
  <el-switch v-model="v2" disabled />
</template>

<script setup>
import { ref } from 'vue'
const v = ref(false)
const v2 = ref(true)
const loading = ref(false)
const beforeChange = async () => {
  loading.value = true
  await new Promise((r) => setTimeout(r, 800))
  loading.value = false
  return true
}
</script>
```

## 参考链接

- Element Plus 官方文档 - Switch 开关: https://element-plus.org/zh-CN/component/switch
