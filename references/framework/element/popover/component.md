# Popover 弹出框三件套

> Element Plus 弹出类组件汇总:`<el-popover>` 弹出框、`<el-tooltip>` 文字提示、`<el-popconfirm>` 气泡确认框。三者共享触发与定位机制。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-popover> <el-tooltip> <el-popconfirm>
```

- `<el-popover>`:内容更丰富的弹出框,可放任意内容与操作。
- `<el-tooltip>`:轻量文字提示,仅文字/简单 HTML。
- `<el-popconfirm>`:点击触发确认,常用于删除前确认。

## 基本用法

### Popover

```vue
<template>
  <el-popover title="标题" content="这是一段内容" trigger="click" width="200">
    <template #reference>
      <el-button>点击弹出</el-button>
    </template>
  </el-popover>
</template>
```

### Tooltip

```vue
<template>
  <el-tooltip content="提示文字" placement="top">
    <el-button>悬停提示</el-button>
  </el-tooltip>
</template>
```

### Popconfirm

```vue
<template>
  <el-popconfirm title="确认删除?" @confirm="onOk">
    <template #reference>
      <el-button type="danger">删除</el-button>
    </template>
  </el-popconfirm>
</template>

<script setup>
const onOk = () => console.log('已删除')
</script>
```

## 使用场景

### 场景 1:嵌套操作(Popover)

`#default` 自定义弹出内容,`#reference` 设置触发元素。

```vue
<template>
  <el-popover width="240" trigger="click">
    <template #reference>
      <el-button :icon="Setting">设置</el-button>
    </template>
    <div class="pop-body">
      <p>自定义内容</p>
      <el-button type="primary" size="small">保存</el-button>
    </div>
  </el-popover>
</template>

<script setup>
import { Setting } from '@element-plus/icons-vue'
</script>

<style scoped>
.pop-body { color: {color-text-primary}; display: flex; flex-direction: column; gap: {spacing-sm}; }
</style>
```

### 场景 2:虚拟触发与定位

`virtual-triggering` 配合 `virtual-ref` 用外部元素触发;`placement` 控制弹出方向。

```vue
<template>
  <el-tooltip
    :virtual-ref="btnRef"
    virtual-triggering
    content="外部触发"
    placement="right"
  />
  <el-button :ref="(el) => (btnRef = el)">外部元素</el-button>
</template>

<script setup>
import { ref } from 'vue'
const btnRef = ref()
</script>
```

### 场景 3:确认按钮文案(Popconfirm)

`confirm-button-text` / `cancel-button-text` 自定义按钮文案。

```vue
<template>
  <el-popconfirm
    title="此操作不可撤销"
    confirm-button-text="删除"
    cancel-button-text="取消"
    confirm-button-type="danger"
    @confirm="onDelete"
  >
    <template #reference><el-button>删除</el-button></template>
  </el-popconfirm>
</template>

<script setup>
const onDelete = () => console.log('删除')
</script>
```

## 参考链接

- Element Plus 官方文档 - Popover 弹出框: https://element-plus.org/zh-CN/component/popover
- Tooltip 文字提示: https://element-plus.org/zh-CN/component/tooltip
- Popconfirm 气泡确认框: https://element-plus.org/zh-CN/component/popconfirm
