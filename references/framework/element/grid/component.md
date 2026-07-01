# Grid 栅格布局(响应式场景)

> Element Plus 响应式栅格场景补充文档。栅格能力由 `<el-row>` `<el-col>` 提供(见 [../layout](../layout/component.md)),本文件聚焦响应式断点与典型响应式页面布局模式。

## 与 Layout 的关系

Element Plus 不存在独立的 `Grid` 组件,栅格系统即 Layout 的 `<el-row>`/`<el-col>`。本文件作为响应式场景的专题说明,完整属性见 [../layout/api.md](../layout/api.md)。

## 响应式断点

| 断点 | 前缀 | 最小宽度   | 典型设备            |
| ---- | ---- | ---------- | ------------------- |
| xs   | `xs` | —(默认)   | 手机(`<768px`)    |
| sm   | `sm` | `768px`    | 平板竖屏            |
| md   | `md` | `992px`    | 平板横屏 / 小笔记本 |
| lg   | `lg` | `1200px`   | 桌面                |
| xl   | `xl` | `1920px`   | 大桌面              |

每个断点可传 `number`(仅 span)或对象 `{ span, offset, pull, push }`。

## 使用场景

### 场景 1:典型后台列表布局

侧栏 + 主区域,小屏堆叠、大屏并排。

```vue
<template>
  <el-row :gutter="20">
    <el-col :xs="24" :md="6"><div class="side">侧边栏</div></el-col>
    <el-col :xs="24" :md="18"><div class="main">主内容</div></el-col>
  </el-row>
</template>

<style scoped>
.side, .main {
  border-radius: {radius-md};
  background-color: {color-bg-secondary};
  min-height: 120px;
  padding: {spacing-md};
  color: {color-text-primary};
}
</style>
```

### 场景 2:卡片栅格(自适应列数)

通过响应式 span 实现 1/2/3/4 列自适应。

```vue
<template>
  <el-row :gutter="16">
    <el-col v-for="i in 8" :key="i" :xs="24" :sm="12" :md="8" :lg="6">
      <div class="card">卡片 {{ i }}</div>
    </el-col>
  </el-row>
</template>

<style scoped>
.card {
  border-radius: {radius-md};
  border: 1px solid {color-border-default};
  background-color: {color-bg-primary};
  padding: {spacing-md};
  margin-bottom: {spacing-md};
  color: {color-text-primary};
}
</style>
```

### 场景 3:对象式响应式属性

断点传入对象可同时设置 span 与 offset。

```vue
<template>
  <el-row :gutter="12">
    <el-col :sm="{ span: 12, offset: 0 }" :lg="{ span: 8, offset: 2 }">
      <div class="block">响应式 + 偏移</div>
    </el-col>
  </el-row>
</template>

<style scoped>
.block {
  border-radius: {radius-sm};
  background-color: {color-bg-secondary};
  min-height: 60px;
}
</style>
```

## 参考链接

- Element Plus 官方文档 - Layout 布局(栅格能力): https://element-plus.org/zh-CN/component/layout
