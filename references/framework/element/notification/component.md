# Notification 通知

> Element Plus 通知组件 `ElNotification`(函数式),常驻消息中心语义:右上角驻留、可关闭、带操作按钮、支持多行富文本与多条堆叠。与 [`ElMessage`](../message/component.md)(toast,短暂单条)明确区分。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
ElNotification(options) // 函数式调用,无模板标签
```

通过 `type` 表达 info/success/warning/error 四类;`duration: 0` 表示不自动关闭。

## 基本用法

```vue
<template>
  <el-button @click="notify">触发通知</el-button>
</template>

<script setup>
import { ElNotification } from 'element-plus'
const notify = () => {
  ElNotification({
    title: '同步完成',
    message: '3 条变更已同步至云端',
    type: 'success',
    duration: 4500
  })
}
</script>
```

## 使用场景

### 场景 1:带操作按钮的常驻通知

`duration: 0` 不自动关闭;`onClick` + `showClose` 提供操作与关闭。

```vue
<template>
  <el-button @click="notifyFail">触发失败通知</el-button>
</template>

<script setup>
import { h } from 'vue'
import { ElNotification } from 'element-plus'
const notifyFail = () => {
  ElNotification({
    title: '上传失败',
    message: h('p', null, [
      h('span', null, '3 个附件未完成上传,'),
      h('a', { style: 'color: {color-primary}', href: '#/tasks' }, '查看任务')
    ]),
    type: 'error',
    duration: 0,
    showClose: true
  })
}
</script>
```

### 场景 2:多条堆叠与偏移

多条通知自动堆叠;`offset` 控制距顶距离,`position` 控制方位。

```vue
<script setup>
import { ElNotification } from 'element-plus'
const batch = () => {
  ElNotification({ title: '通知一', message: '第一条', offset: 100 })
  ElNotification({ title: '通知二', message: '第二条', offset: 100 })
}
</script>
```

### 场景 3:纯文本与危险色

`plain: true` 去除图标强调,`type: 'warning'` 表达需要用户处理的横幅语义。

```vue
<script setup>
import { ElNotification } from 'element-plus'
ElNotification({
  title: '存储空间不足',
  message: '云盘剩余 200MB,请清理后重试',
  type: 'warning',
  plain: true,
  duration: 0
})
</script>
```

## 参考链接

- Element Plus 官方文档 - Notification 通知: https://element-plus.org/zh-CN/component/notification
