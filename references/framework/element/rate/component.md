# Rate 评分

> Element Plus 评分组件 `<el-rate>`,支持半星、只读展示、文案关联与自定义图标。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-rate> <el-rate-text>
```

`v-model` 绑定分数;`allow-half` 半星;`disabled` 只读展示;配合 `show-score` / `show-text` 展示文案。

## 基本用法

```vue
<template>
  <div class="block">
    <el-rate v-model="score" :colors="colors" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const score = ref(0)
const colors = { 2: '{color-error}', 4: '{color-warning}', 5: '{color-success}' }
</script>
```

## 使用场景

### 场景 1:评价表单(半星 + 文案 + 提交)

`allow-half` 半星;`show-text` 关联档位文案;`texts` 按分数档映射。

```vue
<template>
  <el-rate
    v-model="score"
    allow-half
    show-text
    :texts="['很差', '较差', '一般', '满意', '超预期']"
  />
  <el-button type="primary" :disabled="score === 0" @click="submit">提交评价</el-button>
</template>

<script setup>
import { ref } from 'vue'
const score = ref(0)
const submit = () => console.log('提交', score.value)
</script>
```

### 场景 2:商品详情评分展示(只读)

`disabled` 只读 + `show-score` 显示分数,分值保留一位小数。

```vue
<template>
  <el-rate v-model="rate" disabled show-score text-color="{color-warning}" score-template="{value}" />
  <span class="count">(2.3 万条)</span>
</template>

<script setup>
import { ref } from 'vue'
const rate = ref(4.5)
</script>
```

### 场景 3:无分控评(零分兜底)

无评分数据时展示占位文案而非 0 星:

```vue
<template>
  <el-rate v-if="rate > 0" v-model="rate" disabled />
  <span v-else class="empty">暂无评分</span>
</template>

<script setup>
import { ref } from 'vue'
const rate = ref(0)
</script>

<style scoped>
.empty { color: {color-text-secondary}; font-size: {font-size-sm}; }
</style>
```

## 参考链接

- Element Plus 官方文档 - Rate 评分: https://element-plus.org/zh-CN/component/rate
