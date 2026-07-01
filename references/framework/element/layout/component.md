# Layout 布局

> Element Plus 24 栅格布局组件 `<el-row>` `<el-col>`,用于快速构建响应式页面骨架。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-row> <el-col>
```

通过 `<el-row>` 定义行容器,`<el-col>` 定义列,基于 24 栅格系统。`gutter` 控制列间距,`span` 控制列宽,`offset`/`push`/`pull` 控制定位。所有间距值引用 design token。

## 基本用法

```vue
<template>
  <el-row>
    <el-col :span="12"><div class="grid-content">span=12</div></el-col>
    <el-col :span="12"><div class="grid-content">span=12</div></el-col>
  </el-row>
</template>

<script setup>
// 24 栅格:span=12 即占一半宽度,列间距由 gutter 控制,映射 {spacing-md}
</script>

<style scoped>
.grid-content {
  border-radius: {radius-md};
  background-color: {color-bg-secondary};
  min-height: 36px;
  padding: {spacing-sm};
  color: {color-text-primary};
}
</style>
```

## 使用场景

### 场景 1:分栏间距(gutter)

`gutter` 单位为 px,建议映射到 spacing token 以保持视觉一致。

```vue
<template>
  <el-row :gutter="20">
    <el-col :span="6"><div class="grid-content">6</div></el-col>
    <el-col :span="6"><div class="grid-content">6</div></el-col>
    <el-col :span="6"><div class="grid-content">6</div></el-col>
    <el-col :span="6"><div class="grid-content">6</div></el-col>
  </el-row>
</template>

<script setup>
// gutter=20 近似 {spacing-lg},建议实际项目中用 token 变量传入
</script>

<style scoped>
.grid-content {
  border-radius: {radius-sm};
  background-color: {color-bg-secondary};
  min-height: 36px;
}
</style>
```

### 场景 2:响应式布局

`xs`/`sm`/`md`/`lg`/`xl` 对应不同断点的列宽,实现响应式。

```vue
<template>
  <el-row :gutter="10">
    <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
      <div class="grid-content">响应式列</div>
    </el-col>
    <el-col :xs="24" :sm="12" :md="16" :lg="18" :xl="20">
      <div class="grid-content">响应式列</div>
    </el-col>
  </el-row>
</template>

<script setup>
// 断点:xs<768, sm≥768, md≥992, lg≥1200, xl≥1920
</script>

<style scoped>
.grid-content {
  border-radius: {radius-md};
  background-color: {color-bg-primary};
  border: 1px solid {color-border-default};
  min-height: 36px;
  padding: {spacing-sm};
}
</style>
```

### 场景 3:对齐与偏移

`justify` 控制水平对齐,`align` 控制垂直对齐,`offset` 控制列偏移。

```vue
<template>
  <el-row justify="center" align="middle">
    <el-col :span="6" :offset="6"><div class="grid-content">offset=6</div></el-col>
    <el-col :span="6"><div class="grid-content">span=6</div></el-col>
  </el-row>
</template>

<style scoped>
.grid-content {
  border-radius: {radius-sm};
  background-color: {color-bg-secondary};
  min-height: 36px;
}
</style>
```

## 参考链接

- Element Plus 官方文档 - Layout 布局: https://element-plus.org/zh-CN/component/layout
