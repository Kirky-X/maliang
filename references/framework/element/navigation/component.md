# Navigation 导航分组总览

> Element Plus 侧边栏"导航"分组的总览文档,汇总 9 个导航类组件。本文件为分组索引,各组件详细用法见对应单独目录或官方文档。API 速览见 [api.md](./api.md)。

## 分组定位

Element Plus 把 9 个用于"页面/内容定位与流转"的组件归入导航分组:

| 组件        | 标签                              | 用途                       |
| ----------- | --------------------------------- | -------------------------- |
| Affix       | `<el-affix>`                      | 固钉,将元素固定在视口     |
| Anchor      | `<el-anchor>`                     | 锚点跳转                   |
| Backtop     | `<el-backtop>`                    | 回到顶部                   |
| Breadcrumb  | `<el-breadcrumb>`                 | 面包屑,显示当前页面路径   |
| Dropdown    | `<el-dropdown>`                   | 下拉菜单                   |
| Menu        | `<el-menu>`                       | 导航菜单                   |
| PageHeader  | `<el-page-header>`                | 页头                       |
| Steps       | `<el-steps>`                      | 步骤条                     |
| Tabs        | `<el-tabs>`                       | 标签页(见 ../tabs)       |

## 使用场景

### 场景 1:顶部导航 + 面包屑

```vue
<template>
  <el-menu mode="horizontal" :default-active="active">
    <el-menu-item index="1">首页</el-menu-item>
    <el-menu-item index="2">商品</el-menu-item>
  </el-menu>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>商品列表</el-breadcrumb-item>
  </el-breadcrumb>
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

### 场景 2:固钉 + 回到顶部

```vue
<template>
  <el-affix :offset="120">
    <div class="affix-bar">固定栏</div>
  </el-affix>
  <el-backtop :right="100" :bottom="100" />
</template>

<style scoped>
.affix-bar {
  background-color: {color-bg-primary};
  border: 1px solid {color-border-default};
  border-radius: {radius-md};
  padding: {spacing-md};
  color: {color-text-primary};
}
</style>
```

### 场景 3:步骤条引导

```vue
<template>
  <el-steps :active="active" finish-status="success" align-center>
    <el-step title="填写信息" />
    <el-step title="确认订单" />
    <el-step title="支付完成" />
  </el-steps>
</template>

<script setup>
import { ref } from 'vue'
const active = ref(1)
</script>
```

> 详细属性请见各组件单独文档(menu/breadcrumb/dropdown/steps 等目录)或官方文档。

## 参考链接

- Element Plus 官方文档 - 导航分组: https://element-plus.org/zh-CN/component/overview#navigation
- Affix: https://element-plus.org/zh-CN/component/affix
- Backtop: https://element-plus.org/zh-CN/component/backtop
- Breadcrumb: https://element-plus.org/zh-CN/component/breadcrumb
- Dropdown: https://element-plus.org/zh-CN/component/dropdown
- Menu: https://element-plus.org/zh-CN/component/menu
- PageHeader: https://element-plus.org/zh-CN/component/page-header
- Steps: https://element-plus.org/zh-CN/component/steps
- Tabs: https://element-plus.org/zh-CN/component/tabs
