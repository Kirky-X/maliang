# Dialog 对话框

> Element Plus 对话框组件 `<el-dialog>`,支持可拖拽、模态遮罩、嵌套等。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-dialog>
```

通过 `v-model` 控制显示,`title` 设置标题,`draggable` 开启拖拽,`modal` 控制遮罩,`before-close` 拦截关闭。

## 基本用法

```vue
<template>
  <el-button type="primary" @click="visible = true">打开</el-button>
  <el-dialog v-model="visible" title="提示" width="30%">
    <span>这是一段内容</span>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="visible = false">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
const visible = ref(false)
</script>
```

## 使用场景

### 场景 1:可拖拽 + 居中

`draggable` 开启拖拽,`align-center` 垂直居中,`overflow` 控制拖出视口行为。

```vue
<template>
  <el-dialog v-model="visible" title="可拖拽" draggable align-center>
    <span>按住标题栏可拖动</span>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
const visible = ref(true)
</script>
```

### 场景 2:关闭前拦截

`before-close` 接收一个 `done` 回调,需手动调用才关闭。

```vue
<template>
  <el-dialog v-model="visible" title="确认关闭" :before-close="handleClose">
    <span>未保存的内容将丢失</span>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'
const visible = ref(true)
const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭?')
    .then(() => done())
    .catch(() => {})
}
</script>
```

### 场景 3:自定义头部与内容

`#header` / `#footer` 插槽自定义;`show-close` 隐藏关闭按钮。

```vue
<template>
  <el-dialog v-model="visible" :show-close="false">
    <template #header="{ close }">
      <div class="custom-header">
        <span class="title">自定义标题</span>
        <el-button text :icon="Close" @click="close" />
      </div>
    </template>
    <div class="body">自定义内容</div>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Close } from '@element-plus/icons-vue'
const visible = ref(true)
</script>

<style scoped>
.custom-header { display: flex; justify-content: space-between; align-items: center; }
.title { color: {color-text-primary}; font-size: {font-size-lg}; }
.body { color: {color-text-primary}; padding: {spacing-md}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Dialog 对话框: https://element-plus.org/zh-CN/component/dialog
