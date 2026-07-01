# Typography 文本

> Element Plus 文本组件 `<el-text>`,用于排版与文本语义化。本文件给出组件标签、基本用法与典型使用场景;API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-text>
```

`<el-text>` 通过 `type` 标注语义、`size` 控制字号、`tag` 切换底层标签、`truncated` 截断溢出文字。

> **关于 `<el-heading>` 的说明**:Element Plus **不提供** 独立的 `<el-heading>` 组件。标题语义通过 `<el-text>` 的 `tag` 属性渲染为 `<h1>`~`<h6>` 实现(见场景 3)。这是 Element Plus 的既定设计,本文档不臆造不存在的组件 API。

## 基本用法

```vue
<template>
  <el-text>默认文本</el-text>
  <el-text type="primary">主要文本</el-text>
</template>

<script setup>
// type 映射 {color-primary}/{color-success}/… 功能色 token
</script>
```

## 使用场景

### 场景 1:五种语义类型

`type` 取值 `primary` / `success` / `warning` / `danger` / `info`,映射到功能色 token。

```vue
<template>
  <div class="text-block">
    <el-text type="primary">主要(primary)</el-text>
    <el-text type="success">成功(success)</el-text>
    <el-text type="warning">警告(warning)</el-text>
    <el-text type="danger">危险(danger)</el-text>
    <el-text type="info">信息(info)</el-text>
  </div>
</template>

<script setup>
// type → 文字色 token 映射:
//   primary → {color-primary}
//   success → {color-success}
//   warning → {color-warning}
//   danger  → {color-danger}
//   info    → {color-info}
</script>

<style scoped>
.text-block {
  display: flex;
  flex-direction: column;
  gap: {spacing-xs};
  font-size: {font-size-md};
}
</style>
```

### 场景 2:三种字号

`size` 取值 `large` / `default` / `small`,映射到字号 token(对应 references/dimensions/font.md 的层级)。

```vue
<template>
  <div class="text-block">
    <el-text size="large">大号文本</el-text>
    <el-text size="default">默认文本</el-text>
    <el-text size="small">小号文本</el-text>
  </div>
</template>

<script setup>
// size → 字号 token 映射:
//   large   → {font-size-lg}
//   default → {font-size-md}
//   small   → {font-size-sm}
</script>

<style scoped>
.text-block {
  display: flex;
  flex-direction: column;
  gap: {spacing-xs};
}
</style>
```

### 场景 3:标题(heading)— 通过 `tag` 属性渲染

由于无 `<el-heading>` 组件,标题由 `<el-text>` 配合 `tag="h1"`~`"h6"` 实现,字号/字重由 design token 统一约束。

```vue
<template>
  <h1 class="page-title">
    <el-text tag="span" size="large">页面大标题</el-text>
  </h1>
  <el-text tag="h2">二级标题</el-text>
  <el-text tag="h3">三级标题</el-text>
  <el-text tag="p">正文段落,使用默认字号与字重 {font-weight-regular}。</el-text>
</template>

<script setup>
// 标题层级用 tag 表达语义(h1~h6),视觉字号/字重交给 token:
//   h1 → {font-size-xl} / {font-weight-bold}
//   h2 → {font-size-lg} / {font-weight-semibold}
//   h3 → {font-size-md} / {font-weight-semibold}
//   p  → {font-size-md} / {font-weight-regular}
</script>

<style scoped>
.page-title {
  margin: 0 0 {spacing-sm};
}
:deep(h2) { font-size: {font-size-lg}; font-weight: {font-weight-semibold}; }
:deep(h3) { font-size: {font-size-md}; font-weight: {font-weight-semibold}; }
:deep(p)  { font-size: {font-size-md}; font-weight: {font-weight-regular}; color: {color-text-primary}; }
</style>
```

### 场景 4:文本对齐

`<el-text>` 不提供 `align` 属性。对齐由父容器 `text-align` 或 flex 布局控制(语义透明,不臆造属性)。

```vue
<template>
  <div class="align-left">左对齐:<el-text>Element Plus</el-text></div>
  <div class="align-center">居中对齐:<el-text>Element Plus</el-text></div>
  <div class="align-right">右对齐:<el-text>Element Plus</el-text></div>
</template>

<script setup>
// 对齐不靠组件属性,而是父容器 text-align(对齐无对应 token,属布局范畴)
</script>

<style scoped>
.align-left   { text-align: left;   }
.align-center { text-align: center; }
.align-right  { text-align: right;  }
div { margin-bottom: {spacing-xs}; font-size: {font-size-md}; }
</style>
```

### 场景 5:文本截断

`truncated` 单行省略号;多行截断用 CSS `-webkit-line-clamp`。

```vue
<template>
  <el-text class="single-line" truncated>
    这是一段很长的文本,超出容器宽度后将以省略号截断,适用于列表项标题等场景。
  </el-text>
  <el-text class="multi-line">
    这是一段很长的文本,最多显示两行,超出部分以省略号截断。适用于卡片摘要、
    评论预览等多行文本场景,保证布局高度可控。
  </el-text>
</template>

<script setup>
// truncated=true → overflow:hidden; text-overflow:ellipsis; white-space:nowrap
</script>

<style scoped>
.single-line { display: block; max-width: 320px; font-size: {font-size-md}; }
.multi-line {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  max-width: 320px;
  margin-top: {spacing-sm};
  font-size: {font-size-md};
  color: {color-text-secondary};
}
</style>
```
