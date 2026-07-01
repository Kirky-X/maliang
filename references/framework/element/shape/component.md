# Shape 几何图形(汇总)

> Element Plus 无独立"Shape"组件,本文件汇总三个与几何/分隔/水印相关的组件:Border 边框、Divider 分割线、Watermark 水印。各组件详细用法见对应单独目录(Divider 见 ../divider)或官方文档。

## 汇总组件

| 组件      | 标签                  | 用途                          | 官方路径            |
| --------- | --------------------- | ----------------------------- | ------------------- |
| Border    | CSS 工具类            | 边框/圆角/阴影预设样式        | /component/border   |
| Divider   | `<el-divider>`        | 分割线(见 ../divider)       | /component/divider  |
| Watermark | `<el-watermark>`      | 页面/区域水印                 | /component/watermark|

## 使用场景

### 场景 1:Border 边框预设(工具类)

Element Plus 通过 CSS 类提供边框圆角、阴影预设,直接套用类名。

```vue
<template>
  <div class="border-box">圆角 + 阴影 + 边框</div>
  <div class="round-box">圆形容器</div>
</template>

<style scoped>
.border-box {
  border: 1px solid {color-border-default};
  border-radius: {radius-md};
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  padding: {spacing-md};
  background-color: {color-bg-primary};
  color: {color-text-primary};
}
.round-box {
  width: 80px; height: 80px;
  border-radius: {radius-full};
  background-color: {color-primary};
}
</style>
```

### 场景 2:Divider 分割线

```vue
<template>
  <div>内容 A</div>
  <el-divider />
  <div>内容 B</div>
  <el-divider content-position="center">带文字分割</el-divider>
</template>

<style scoped>
:deep(.el-divider) { border-color: {color-border-default}; }
:deep(.el-divider__text) {
  background-color: {color-bg-primary};
  color: {color-text-primary};
}
</style>
```

### 场景 3:Watermark 水印

`content` 设置水印文字,`gap` 控制间距,`rotate` 控制旋转。

```vue
<template>
  <el-watermark :content="['机密', 'maliang']" :gap="[120, 120]" :rotate="-22">
    <div class="watermarked">受水印保护的内容区域</div>
  </el-watermark>
</template>

<style scoped>
.watermarked {
  height: 300px;
  background-color: {color-bg-primary};
  padding: {spacing-md};
  color: {color-text-primary};
}
</style>
```

## 参考链接

- Element Plus 官方文档 - Border 边框: https://element-plus.org/zh-CN/component/border
- Divider 分割线: https://element-plus.org/zh-CN/component/divider
- Watermark 水印: https://element-plus.org/zh-CN/component/watermark
