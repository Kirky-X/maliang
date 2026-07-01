# Card 卡片

> Element Plus 卡片组件 `<el-card>`,用于信息容器。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-card>
```

通过 `header` 设置标题,`shadow` 控制阴影(always/hover/never),`body-style` 自定义内容样式。

## 基本用法

```vue
<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>卡片标题</span>
        <el-button text>操作</el-button>
      </div>
    </template>
    <div v-for="i in 4" :key="i" class="item">列表项 {{ i }}</div>
  </el-card>
</template>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.item { padding: {spacing-sm} 0; color: {color-text-primary}; }
:deep(.el-card) {
  border-radius: {radius-md};
  border: 1px solid {color-border-default};
}
</style>
```

## 使用场景

### 场景 1:阴影模式

```vue
<template>
  <el-card shadow="always">始终阴影</el-card>
  <el-card shadow="hover">悬浮阴影</el-card>
  <el-card shadow="never">无阴影</el-card>
</template>

<style scoped>
:deep(.el-card) { margin-bottom: {spacing-md}; }
</style>
```

### 场景 2:无头部简单卡片

不使用 `#header` 即为无头部卡片。

```vue
<template>
  <el-card>
    <div class="content">纯内容卡片</div>
  </el-card>
</template>

<style scoped>
.content { color: {color-text-primary}; padding: {spacing-sm}; }
</style>
```

### 场景 3:自定义 body 样式

`body-style` 传入对象覆盖内容区样式。

```vue
<template>
  <el-card :body-style="{ padding: '0' }">
    <img src="https://example.com/x.png" class="cover" />
    <div class="info">
      <span>带封面的卡片</span>
    </div>
  </el-card>
</template>

<style scoped>
.cover { width: 100%; display: block; }
.info { padding: {spacing-md}; color: {color-text-primary}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Card 卡片: https://element-plus.org/zh-CN/component/card
