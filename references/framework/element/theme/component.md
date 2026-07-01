# Theme 主题

> Element Plus 主题定制指南。通过 CSS 变量与 SCSS 变量覆盖,实现自定义主题色与暗色模式。本文件为指南类文档,无独立组件标签。

## 定制方式

Element Plus 提供两层定制入口:

1. **CSS 变量覆盖**:运行时覆盖,适合切换主题色 / 暗色模式。
2. **SCSS 变量覆盖**:构建时覆盖,适合深度定制圆角、间距等基础变量。

## 使用场景

### 场景 1:CSS 变量覆盖主题色

通过覆盖 `--el-color-primary` 切换主色。建议映射到 design token。

```vue
<template>
  <div class="custom-theme">
    <el-button type="primary">主色按钮</el-button>
  </div>
</template>

<style scoped>
.custom-theme {
  /* 主色 → {color-primary} */
  --el-color-primary: #409eff;
  /* 主色文字 → {color-text-on-primary} */
  --el-color-primary-light-3: #66b1ff;
  --el-color-primary-light-5: #a0cfff;
  --el-color-primary-light-7: #d9ecff;
  --el-color-primary-light-9: #ecf5ff;
  --el-color-primary-dark-2: #337ecc;
}
</style>
```

### 场景 2:暗色模式

为 `html` 添加 `dark` 类,覆盖背景/文字/边框变量。

```vue
<template>
  <div :class="{ dark: isDark }">
    <el-button @click="isDark = !isDark">切换{{ isDark ? '亮色' : '暗色' }}</el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const isDark = ref(false)
</script>

<style>
.dark {
  --el-bg-color: #141414;           /* 映射 {color-bg-primary} 暗色 */
  --el-bg-color-page: #0a0a0a;
  --el-text-color-primary: #e5eaf3; /* 映射 {color-text-primary} 暗色 */
  --el-text-color-regular: #cfd3dc;
  --el-border-color: #4c4d4f;       /* 映射 {color-border-default} 暗色 */
  --el-fill-color: #303030;
}
</style>
```

### 场景 3:SCSS 变量深度定制

在入口 SCSS 中,于引入 Element Plus 样式前覆盖变量。

```scss
// styles/element-variables.scss
@forward 'element-plus/theme-chalk/src/common/var.scss' with (
  $colors: (
    'primary': ('base': #409eff),
  ),
  $border-radius: (
    'base': 6px,  // 映射 {radius-md}
  )
);

// main.js
// import 'element-plus/theme-chalk/src/index.scss'
```

## 参考链接

- Element Plus 官方文档 - 主题定制: https://element-plus.org/zh-CN/guide/theming
- 暗色模式: https://element-plus.org/zh-CN/guide/dark-mode
