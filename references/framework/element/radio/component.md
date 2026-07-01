# Radio 单选

> Element Plus 单选组件 `<el-radio>` `<el-radio-group>` `<el-radio-button>`,用于在互斥选项中选择。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-radio> <el-radio-group> <el-radio-button>
```

`<el-radio-group>` 为容器,`v-model` 绑定值;`<el-radio>` 为单选项,`label` 为值;`<el-radio-button>` 为按钮样式单选。

## 基本用法

```vue
<template>
  <el-radio-group v-model="picked">
    <el-radio label="1">备选项 A</el-radio>
    <el-radio label="2">备选项 B</el-radio>
  </el-radio-group>
</template>

<script setup>
import { ref } from 'vue'
const picked = ref('1')
</script>

<style scoped>
:deep(.el-radio__label) { color: {color-text-primary}; }
:deep(.el-radio__input.is-checked .el-radio__inner) {
  background-color: {color-primary};
  border-color: {color-primary};
}
</style>
```

## 使用场景

### 场景 1:按钮组单选

`<el-radio-button>` 提供按钮样式,适合少量选项。

```vue
<template>
  <el-radio-group v-model="size">
    <el-radio-button label="large">大</el-radio-button>
    <el-radio-button label="default">默认</el-radio-button>
    <el-radio-button label="small">小</el-radio-button>
  </el-radio-group>
</template>

<script setup>
import { ref } from 'vue'
const size = ref('default')
</script>
```

### 场景 2:禁用与尺寸

`disabled` 禁用整个组或单项;`size` 控制尺寸。

```vue
<template>
  <el-radio-group v-model="v" disabled>
    <el-radio label="1">禁用 A</el-radio>
    <el-radio label="2">禁用 B</el-radio>
  </el-radio-group>
</template>

<script setup>
import { ref } from 'vue'
const v = ref('1')
</script>
```

### 场景 3:带边框

`border` 显示边框样式。

```vue
<template>
  <el-radio-group v-model="v">
    <el-radio label="1" border>选项 A</el-radio>
    <el-radio label="2" border>选项 B</el-radio>
  </el-radio-group>
</template>

<script setup>
import { ref } from 'vue'
const v = ref('1')
</script>
```

## 参考链接

- Element Plus 官方文档 - Radio 单选框: https://element-plus.org/zh-CN/component/radio
