# Dropdown 下拉菜单

> Element Plus 下拉菜单组件 `<el-dropdown>` `<el-dropdown-menu>` `<el-dropdown-item>`,用于触发一组操作。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-dropdown> <el-dropdown-menu> <el-dropdown-item>
```

`<el-dropdown>` 为容器,`trigger` 设置触发方式;`<el-dropdown-menu>` 为菜单容器,`<el-dropdown-item>` 为菜单项,`command` 为命令标识。

## 基本用法

```vue
<template>
  <el-dropdown @command="onCmd">
    <span class="trigger">下拉菜单<el-icon><ArrowDown /></el-icon></span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="a">选项 A</el-dropdown-item>
        <el-dropdown-item command="b">选项 B</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { ArrowDown } from '@element-plus/icons-vue'
const onCmd = (c) => console.log(c)
</script>

<style scoped>
.trigger { color: {color-primary}; cursor: pointer; }
</style>
```

## 使用场景

### 场景 1:触发方式与禁用

`trigger` 取值 `hover`/`click`/`contextmenu`;`disabled` 禁用。

```vue
<template>
  <el-dropdown trigger="click" @command="onCmd">
    <el-button>点击触发</el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="1">启用项</el-dropdown-item>
        <el-dropdown-item command="2" disabled>禁用项</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
const onCmd = (c) => console.log(c)
</script>
```

### 场景 2:带图标与分组分隔

`<el-dropdown-item>` 内放图标;`divided` 显示分隔线。

```vue
<template>
  <el-dropdown>
    <el-button>操作</el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item :icon="Edit">编辑</el-dropdown-item>
        <el-dropdown-item :icon="Share">分享</el-dropdown-item>
        <el-dropdown-item :icon="Delete" divided>删除</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { Edit, Share, Delete } from '@element-plus/icons-vue'
</script>
```

### 场景 3:右键菜单

`trigger="contextmenu"` 实现右键菜单。

```vue
<template>
  <el-dropdown trigger="contextmenu">
    <div class="area">右键点击此处</div>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>复制</el-dropdown-item>
        <el-dropdown-item>粘贴</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped>
.area { padding: {spacing-md}; border: 1px dashed {color-border-default}; border-radius: {radius-md}; color: {color-text-primary}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Dropdown 下拉菜单: https://element-plus.org/zh-CN/component/dropdown
