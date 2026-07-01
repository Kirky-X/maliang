# Message 消息提示

> Element Plus 消息提示 `<el-message>` 与命令式 API `ElMessage`,用于轻量全局反馈。API 完整定义见 [api.md](./api.md)。

## 组件标签 / API

```
<el-message>   ElMessage(options) / ElMessage.success(text)
```

通常使用命令式 `ElMessage` 函数调用,而非直接写 `<el-message>` 标签。`type` 区分 success/warning/info/error,`duration` 控制停留时长,`showClose` 显示关闭按钮。

## 基本用法

```vue
<template>
  <el-button @click="open">显示消息</el-button>
</template>

<script setup>
import { ElMessage } from 'element-plus'
const open = () => ElMessage('这是一条消息')
</script>
```

## 使用场景

### 场景 1:四种状态

```vue
<template>
  <el-button type="success" @click="ElMessage.success('成功')">success</el-button>
  <el-button type="warning" @click="ElMessage.warning('警告')">warning</el-button>
  <el-button type="info" @click="ElMessage.info('信息')">info</el-button>
  <el-button type="danger" @click="ElMessage.error('错误')">error</el-button>
</template>

<script setup>
import { ElMessage } from 'element-plus'
</script>

<style scoped>
/* type → 功能色映射:
   success → {color-success}
   warning → {color-warning}
   info    → {color-info}
   error   → {color-danger} */
</style>
```

### 场景 2:可关闭与自定义时长

`showClose` 显示关闭按钮,`duration` 设为 0 则不自动关闭,`center` 居中。

```vue
<template>
  <el-button @click="open">可关闭 + 不自动关闭</el-button>
</template>

<script setup>
import { ElMessage } from 'element-plus'
const open = () =>
  ElMessage({
    message: '需要手动关闭',
    duration: 0,
    showClose: true,
    center: true,
  })
</script>
```

### 场景 3:HTML 内容与图标

`dangerouslyUseHTMLString` 允许 message 含 HTML;`icon` 自定义图标。

```vue
<template>
  <el-button @click="open">HTML 消息</el-button>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { Promotion } from '@element-plus/icons-vue'
const open = () =>
  ElMessage({
    message: '<strong>加粗</strong> 内容',
    dangerouslyUseHTMLString: true,
    icon: Promotion,
  })
</script>
```

### 场景 4:手动关闭实例

`ElMessage` 返回实例,可调用 `close()`。

```vue
<template>
  <el-button @click="open">显示 5 秒后关闭</el-button>
</template>

<script setup>
import { ElMessage } from 'element-plus'
const open = () => {
  const inst = ElMessage({ message: '5 秒后关闭', duration: 0 })
  setTimeout(() => inst.close(), 5000)
}
</script>
```

## 参考链接

- Element Plus 官方文档 - Message 消息提示: https://element-plus.org/zh-CN/component/message
