# Drawer 抽屉

> Element Plus 抽屉组件 `<el-drawer>`,从屏幕边缘滑出的面板。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-drawer>
```

通过 `v-model` 控制显示,`direction` 设置滑出方向(left/right/top/bottom),`size` 设置尺寸,`before-close` 拦截关闭。

## 基本用法

```vue
<template>
  <el-button @click="visible = true">打开抽屉</el-button>
  <el-drawer v-model="visible" title="我是标题" direction="rtl">
    <span>抽屉内容</span>
  </el-drawer>
</template>

<script setup>
import { ref } from 'vue'
const visible = ref(false)
</script>
```

## 使用场景

### 场景 1:方向与尺寸

`direction` 取值 `rtl`/`ltr`/`ttb`/`bbb`(右/左/上/下);`size` 接受百分比或像素。

```vue
<template>
  <el-drawer v-model="visible" title="底部抽屉" direction="btt" size="40%">
    <span>从底部滑出</span>
  </el-drawer>
</template>

<script setup>
import { ref } from 'vue'
const visible = ref(true)
</script>
```

### 场景 2:无遮罩与多层

`modal` 关闭遮罩,`append-to-body` 嵌套场景追加到 body。

```vue
<template>
  <el-drawer v-model="visible" :modal="false" append-to-body title="无遮罩">
    <span>无遮罩抽屉</span>
  </el-drawer>
</template>

<script setup>
import { ref } from 'vue'
const visible = ref(true)
</script>
```

### 场景 3:自定义头部与底部

`#header` / `#footer` 插槽自定义;`with-header` 关闭默认头部。

```vue
<template>
  <el-drawer v-model="visible">
    <template #header="{ close }">
      <span class="title">自定义标题</span>
      <el-button text :icon="Close" @click="close" />
    </template>
    <div class="body">内容</div>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="visible = false">确定</el-button>
    </template>
  </el-drawer>
</template>

<script setup>
import { ref } from 'vue'
import { Close } from '@element-plus/icons-vue'
const visible = ref(true)
</script>

<style scoped>
.title { color: {color-text-primary}; font-size: {font-size-lg}; }
.body { color: {color-text-primary}; padding: {spacing-md}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Drawer 抽屉: https://element-plus.org/zh-CN/component/drawer
