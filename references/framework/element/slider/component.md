# Slider 滑块

> Element Plus 滑块组件 `<el-slider>`,支持连续/离散/区间(双滑块)与垂直方向,用于数值/区间录入。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-slider>
```

`v-model` 绑定数值;`range` 属性启用双滑块区间;`show-input` 附加精确数值输入框。

## 基本用法

```vue
<template>
  <div>
    <span class="demonstration">音量 {{ volume }}%</span>
    <el-slider v-model="volume" show-steps :step="5" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const volume = ref(40)
</script>

<style scoped>
.el-slider__bar { background-color: {color-primary}; }
</style>
```

## 使用场景

### 场景 1:区间筛选(双滑块)

`range` 原生双滑块;`format-tooltip` 定制气泡文案。

```vue
<template>
  <el-slider
    v-model="priceRange"
    range
    :min="0"
    :max="1000"
    :step="10"
    :format-tooltip="(v) => `¥${v}`"
  />
</template>

<script setup>
import { ref } from 'vue'
const priceRange = ref([100, 900])
</script>
```

### 场景 2:离散档位(divisions)

`step` + `show-steps` 表达离散档;`marks` 显示刻度标签。

```vue
<template>
  <el-slider
    v-model="level"
    :step="1"
    :min="0"
    :max="3"
    show-steps
    :marks="marks"
  />
</template>

<script setup>
import { ref } from 'vue'
const level = ref(2)
const marks = { 0: '低', 1: '中', 2: '高', 3: '很高' }
</script>
```

### 场景 3:带输入框(精确值)

`show-input` 右侧附数字输入,拖动与键入双向同步。

```vue
<template>
  <el-slider
    v-model="threshold"
    show-input
    :show-input-controls="false"
    input-size="small"
  />
</template>

<script setup>
import { ref } from 'vue'
const threshold = ref(30)
</script>
```

## 参考链接

- Element Plus 官方文档 - Slider 滑块: https://element-plus.org/zh-CN/component/slider
