# DatePicker 日期时间选择

> Element Plus 日期时间选择组件 `<el-date-picker>`(含 datetime/范围)、`<el-time-picker>` / `<el-time-select>`。用于表单**日期/时间录入**,与展示型 [`<el-calendar>`](../calendar/component.md)(浏览用途)区分。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-date-picker> <el-time-picker> <el-time-select>
```

`<el-date-picker>` 通过 `type` 覆盖 date/dates/datetime/week/month/year/daterange/datetimerange/monthrange 档位;`<el-time-picker>` 任意时间;`<el-time-select>` 档位时间点。

## 基本用法

```vue
<template>
  <div>
    <el-date-picker
      v-model="checkIn"
      type="date"
      placeholder="选择入住日期"
      :disabled-date="disabledDate"
    />
    <el-time-picker v-model="remindAt" placeholder="选择提醒时间" format="HH:mm" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const checkIn = ref('')
const remindAt = ref('')
const disabledDate = (time) => time.getTime() < Date.now() - 86400000
</script>

<style scoped>
.el-input__wrapper { --el-input-border-radius: {radius-md}; }
</style>
```

## 使用场景

### 场景 1:日期范围(预订/筛选)

`type="daterange"` 区间选择,`range-separator` 分隔符。

```vue
<template>
  <el-date-picker
    v-model="range"
    type="daterange"
    range-separator="至"
    start-placeholder="入住日期"
    end-placeholder="离店日期"
    :shortcuts="shortcuts"
  />
</template>

<script setup>
import { ref } from 'vue'
const range = ref([])
const shortcuts = [
  { text: '未来 7 天', value: () => { const e = new Date(); const s = new Date(); return [s, e] } }
]
</script>
```

### 场景 2:日期时间(精确到分秒)

`type="datetime"`;`:time-picker-props` 微调时间面板。

```vue
<template>
  <el-date-picker
    v-model="publishAt"
    type="datetime"
    placeholder="选择发布时间"
    format="YYYY-MM-DD HH:mm"
  />
</template>

<script setup>
import { ref } from 'vue'
const publishAt = ref('')
</script>
```

### 场景 3:档位时间点(time-select)

供选时间离散固定(如配送时段)时用 `<el-time-select>`,禁用已满档。

```vue
<template>
  <el-time-select
    v-model="slot"
    start="08:00"
    step="00:30"
    end="20:00"
    placeholder="选择配送时段"
  />
</template>

<script setup>
import { ref } from 'vue'
const slot = ref('')
</script>
```

## 参考链接

- Element Plus 官方文档 - DatePicker 日期选择器: https://element-plus.org/zh-CN/component/date-picker
- TimePicker 时间选择器: https://element-plus.org/zh-CN/component/time-picker
- TimeSelect 时间选择: https://element-plus.org/zh-CN/component/time-select
