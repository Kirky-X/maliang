# Input 输入框

> Element Plus 输入框组件 `<el-input>`,支持 textarea、前后缀、字数限制与多种类型。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-input>
```

通过 `v-model` 绑定值,`type` 切换 text/textarea/password 等,`maxlength` 限制字数,`show-word-limit` 显示计数,`prefix`/`suffix` 插槽自定义前后缀。

## 基本用法

```vue
<template>
  <el-input v-model="text" placeholder="请输入" />
</template>

<script setup>
import { ref } from 'vue'
const text = ref('')
</script>

<style scoped>
:deep(.el-input__inner) { color: {color-text-primary}; font-size: {font-size-md}; }
</style>
```

## 使用场景

### 场景 1:textarea + 字数限制

`type="textarea"` 切换为多行;`maxlength` + `show-word-limit` 显示计数。

```vue
<template>
  <el-input
    v-model="desc"
    type="textarea"
    :rows="4"
    maxlength="200"
    show-word-limit
    placeholder="请输入描述(最多 200 字)"
  />
</template>

<script setup>
import { ref } from 'vue'
const desc = ref('')
</script>
```

### 场景 2:前后缀图标与插槽

`prefix-icon` / `suffix-icon` 传图标组件,或用 `#prefix` / `#suffix` 插槽。

```vue
<template>
  <el-input v-model="kw" placeholder="搜索" :prefix-icon="Search" clearable />
</template>

<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
const kw = ref('')
</script>

<style scoped>
:deep(.el-input__wrapper) {
  border-radius: {radius-md};
  background-color: {color-bg-primary};
  box-shadow: 0 0 0 1px {color-border-default} inset;
}
</style>
```

### 场景 3:复合输入与禁用

`#prepend` / `#append` 实现复合输入框;`disabled` 禁用。

```vue
<template>
  <el-input v-model="url" placeholder="请输入网址" disabled>
    <template #prepend>https://</template>
    <template #append>.com</template>
  </el-input>
</template>

<script setup>
import { ref } from 'vue'
const url = ref('')
</script>

<style scoped>
:deep(.el-input.is-disabled .el-input__wrapper) {
  background-color: {color-bg-secondary};
  opacity: {opacity-disabled};
}
</style>
```

### 场景 4:密码框与尺寸

`show-password` 切换密码可见;`size` 控制尺寸。

```vue
<template>
  <el-input v-model="pwd" type="password" show-password size="large" placeholder="密码" />
</template>

<script setup>
import { ref } from 'vue'
const pwd = ref('')
</script>
```

## 参考链接

- Element Plus 官方文档 - Input 输入框: https://element-plus.org/zh-CN/component/input
