# Icon 图标

> Element Plus 图标组件 `<el-icon>` 配合 `@element-plus/icons-vue` 图标包使用。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-icon>
```

`<el-icon>` 是图标容器,内部放置来自 `@element-plus/icons-vue` 的具体图标组件;`size`/`color` 控制大小与颜色。

## 基本用法

```vue
<template>
  <el-icon :size="20" :color="customColor">
    <Edit />
  </el-icon>
</template>

<script setup>
import { Edit } from '@element-plus/icons-vue'
const customColor = '{color-primary}'
</script>
```

## 使用场景

### 场景 1:与按钮/输入框组合

图标可作为 `el-button` 的 `icon`,或放入 `el-input` 前后缀插槽。

```vue
<template>
  <el-button type="primary" :icon="Search">搜索</el-button>
  <el-input placeholder="搜索">
    <template #prefix><el-icon><Search /></el-icon></template>
  </el-input>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>
```

### 场景 2:统一尺寸与颜色

通过 CSS 变量或 `size`/`color` 属性统一控制。

```vue
<template>
  <div class="icon-group">
    <el-icon><Edit /></el-icon>
    <el-icon><Share /></el-icon>
    <el-icon><Delete /></el-icon>
  </div>
</template>

<script setup>
import { Edit, Share, Delete } from '@element-plus/icons-vue'
</script>

<style scoped>
.icon-group .el-icon {
  font-size: {font-size-lg};
  color: {color-text-primary};
}
.icon-group .el-icon:hover { color: {color-primary}; }
</style>
```

### 场景 3:全局注册(可选)

在入口文件全局注册所有图标,即可在模板中直接使用。

```vue
<script setup>
// main.js 中:
// import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// for (const [key, comp] of Object.entries(ElementPlusIconsVue)) {
//   app.component(key, comp)
// }
</script>

<template>
  <el-icon><Edit /></el-icon>
</template>
```

## 参考链接

- Element Plus 官方文档 - Icon 图标: https://element-plus.org/zh-CN/component/icon
- 图标包: https://www.npmjs.com/package/@element-plus/icons-vue
