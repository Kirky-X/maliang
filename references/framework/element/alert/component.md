# Alert 警告

> Element Plus 警告组件 `<el-alert>`,用于页面非浮层提示。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-alert>
```

通过 `type` 区分 success/warning/info/error,`title` 设置标题,`closable` 控制可关闭,`show-icon` 显示图标,`description` 设置辅助文字。

## 基本用法

```vue
<template>
  <el-alert title="成功提示" type="success" show-icon />
  <el-alert title="警告提示" type="warning" show-icon />
  <el-alert title="错误提示" type="error" show-icon />
  <el-alert title="信息提示" type="info" show-icon />
</template>

<style scoped>
:deep(.el-alert) { margin-bottom: {spacing-md}; border-radius: {radius-md}; }
</style>
```

## 使用场景

### 场景 1:带描述与不可关闭

`description` 设置辅助文字,`closable` 关闭可关闭按钮,`center` 居中。

```vue
<template>
  <el-alert
    title="带辅助文字"
    type="info"
    description="这是一段辅助说明文字"
    :closable="false"
    show-icon
  />
</template>
```

### 场景 2:主题与文字居中

`effect` 取值 `light`/`dark`;`center` 文字居中。

```vue
<template>
  <el-alert title="深色主题" type="warning" effect="dark" center show-icon />
</template>
```

### 场景 3:自定义关闭与插槽

`#default` 自定义内容,`#title` 自定义标题;`@close` 监听关闭。

```vue
<template>
  <el-alert type="success" @close="onClose">
    <template #title>
      <span>自定义标题 <el-tag size="small">新</el-tag></span>
    </template>
    <span>自定义内容</span>
  </el-alert>
</template>

<script setup>
const onClose = () => console.log('closed')
</script>
```

## 参考链接

- Element Plus 官方文档 - Alert 提示: https://element-plus.org/zh-CN/component/alert
