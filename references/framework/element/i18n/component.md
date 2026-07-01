# i18n 国际化

> Element Plus 国际化指南。通过 `<el-config-provider>` 注入语言包(`locale`),配合 `@element-plus/locale` 提供的多语言。本文件为指南类文档。

## 机制说明

Element Plus 默认使用中文。切换语言有两种方式:

1. **全局**:在 app 入口 `app.use(ElementPlus, { locale })` 传入语言包。
2. **局部**:用 `<el-config-provider :locale="locale">` 包裹子树,实现局部语言切换。

## 使用场景

### 场景 1:全局中文 / 英文切换

```vue
<template>
  <el-config-provider :locale="locale">
    <el-pagination :total="100" />
    <el-date-picker v-model="date" type="date" />
  </el-config-provider>
</template>

<script setup>
import { ref } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
const locale = ref(zhCn)
const date = ref('')
// 切换:locale.value = en
</script>
```

### 场景 2:动态切换语言

```vue
<template>
  <el-radio-group v-model="lang" @change="onChange">
    <el-radio-button label="zh">中文</el-radio-button>
    <el-radio-button label="en">English</el-radio-button>
  </el-radio-group>
  <el-config-provider :locale="locale">
    <el-pagination :total="50" layout="prev, pager, next" />
  </el-config-provider>
</template>

<script setup>
import { ref, shallowRef } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
const lang = ref('zh')
const locale = shallowRef(zhCn)
const onChange = (val) => {
  locale.value = val === 'en' ? en : zhCn
}
</script>
```

### 场景 3:ConfigProvider 配置项

`<el-config-provider>` 还可统一设置 `size`、`zIndex`、`message` 配置等。

```vue
<template>
  <el-config-provider :size="size" :z-index="3000" :locale="locale">
    <app />
  </el-config-provider>
</template>

<script setup>
import { ref } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
const size = ref('default')
const locale = ref(zhCn)
</script>
```

## 参考链接

- Element Plus 官方文档 - 国际化: https://element-plus.org/zh-CN/guide/i18n
- ConfigProvider: https://element-plus.org/zh-CN/component/config-provider
