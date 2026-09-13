# Statistic 统计 / Descriptions 描述列表

> Element Plus 轻量数据展示二件套:`<el-statistic>`(统计数值:大数字 + 标签 + delta)与 `<el-descriptions>`(键值对详情列表)。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-statistic> <el-countdown> <el-descriptions> <el-descriptions-item>
```

`<el-statistic>` 承载数值强调(KPI);`<el-descriptions>` 以 `title` + `<el-descriptions-item label>` 列表承载详情;`<el-countdown>` 为倒计时变体。

## 基本用法

```vue
<template>
  <el-row :gutter="16">
    <el-col :span="8">
      <el-statistic title="今日 GMV" :value="128460" :precision="0" />
    </el-col>
    <el-col :span="8">
      <el-statistic title="订单量" :value="3421" />
    </el-col>
    <el-col :span="8">
      <el-statistic title="退款金额" :value="2180" :precision="2" />
    </el-col>
  </el-row>
</template>
```

## 使用场景

### 场景 1:KPI 卡(统计 + delta)

delta 经插槽拼装,涨跌色按业务语义(而非一刀切红涨):

```vue
<template>
  <el-card shadow="never">
    <el-statistic title="今日 GMV" :value="128460">
      <template #suffix>
        <span class="delta up">↑ 12.4%</span>
      </template>
    </el-statistic>
  </el-card>
</template>

<style scoped>
.delta { font-size: {font-size-sm}; }
.delta.up { color: {color-success}; }
</style>
```

### 场景 2:详情页键值对(descriptions)

`border` 表格式分块;`column` 控制列数;`label-class-name` 定宽键列。

```vue
<template>
  <el-descriptions title="订单信息" :column="2" border>
    <el-descriptions-item label="订单编号">SO-20260908-001</el-descriptions-item>
    <el-descriptions-item label="下单时间">2026-09-08 14:32</el-descriptions-item>
    <el-descriptions-item label="支付方式">微信支付</el-descriptions-item>
    <el-descriptions-item label="配送地址">上海市浦东新区xx路 88 号</el-descriptions-item>
  </el-descriptions>
</template>
```

### 场景 3:数字滚动与倒计时变体

`<el-countdown>` 倒计时;statistic 的 `duration` 驱动数字滚动入场。

```vue
<template>
  <el-countdown title="距秒杀结束" :duration="3600 * 1000" format="HH:mm:ss" />
</template>
```

## 参考链接

- Element Plus 官方文档 - Statistic 统计数值: https://element-plus.org/zh-CN/component/statistic
- Descriptions 描述列表: https://element-plus.org/zh-CN/component/descriptions
