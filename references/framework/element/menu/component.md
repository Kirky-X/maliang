# Menu 菜单

> Element Plus 导航菜单组件 `<el-menu>` `<el-sub-menu>` `<el-menu-item>`,支持水平/垂直、折叠、多级子菜单。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-menu> <el-sub-menu> <el-menu-item>
```

`<el-menu>` 为容器,`default-active` 设置激活项;`<el-sub-menu>` 为可展开子菜单,`<el-menu-item>` 为末级菜单项;`index` 为唯一标识。

## 基本用法

```vue
<template>
  <el-menu :default-active="active">
    <el-menu-item index="1">处理中心</el-menu-item>
    <el-sub-menu index="2">
      <template #title>我的工作台</template>
      <el-menu-item index="2-1">选项 1</el-menu-item>
      <el-menu-item index="2-2">选项 2</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('1')
</script>
```

## 使用场景

### 场景 1:水平菜单

`mode="horizontal"` 切换为顶部水平菜单。

```vue
<template>
  <el-menu mode="horizontal" :default-active="active" :ellipsis="false">
    <el-menu-item index="1">首页</el-menu-item>
    <el-menu-item index="2">商品</el-menu-item>
    <el-menu-item index="3">订单</el-menu-item>
  </el-menu>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('1')
</script>

<style scoped>
:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  color: {color-primary};
  border-bottom-color: {color-primary};
}
</style>
```

### 场景 2:侧边栏折叠菜单

`collapse` 折叠为图标条,常配合 `<el-aside>` 使用。

```vue
<template>
  <el-aside width="200px">
    <el-menu :default-active="active" :collapse="collapsed">
      <el-menu-item index="1" :icon="HomeFilled">首页</el-menu-item>
      <el-sub-menu index="2">
        <template #title><el-icon><Setting /></el-icon>设置</template>
        <el-menu-item index="2-1">账号</el-menu-item>
        <el-menu-item index="2-2">权限</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { ref } from 'vue'
import { HomeFilled, Setting } from '@element-plus/icons-vue'
const active = ref('1')
const collapsed = ref(false)
</script>
```

### 场景 3:自定义主题色

`background-color` / `text-color` / `active-text-color` 自定义配色,建议映射 token。

```vue
<template>
  <el-menu
    :default-active="active"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <el-menu-item index="1">深色菜单</el-menu-item>
  </el-menu>
</template>

<script setup>
import { ref } from 'vue'
const active = ref('1')
</script>
```

## 参考链接

- Element Plus 官方文档 - Menu 菜单: https://element-plus.org/zh-CN/component/menu
