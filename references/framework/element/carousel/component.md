# Carousel 走马灯

> Element Plus 走马灯组件 `<el-carousel>` `<el-carousel-item>`,用于图片/内容轮播。API 完整定义见 [api.md](./api.md)。

## 组件标签

```
<el-carousel> <el-carousel-item>
```

`<el-carousel>` 为容器,`height` 设置高度,`autoplay` 自动播放,`interval` 切换间隔;`<el-carousel-item>` 为每一页内容。

## 基本用法

```vue
<template>
  <el-carousel height="200px">
    <el-carousel-item v-for="i in 4" :key="i">
      <div class="slide">{{ i }}</div>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.slide {
  height: 100%;
  display: flex; align-items: center; justify-content: center;
  background-color: {color-bg-secondary};
  color: {color-text-primary};
  font-size: {font-size-xl};
  border-radius: {radius-md};
}
</style>
```

## 使用场景

### 场景 1:方向与触发方式

`direction="vertical"` 纵向切换;`trigger="click"` 点击指示器切换。

```vue
<template>
  <el-carousel height="200px" trigger="click" :interval="4000">
    <el-carousel-item v-for="i in 3" :key="i">
      <div class="slide">{{ i }}</div>
    </el-carousel-item>
  </el-carousel>
</template>
```

### 场景 2:卡片化与指示器位置

`type="card"` 卡片模式;`indicator-position` 取值 `outside`/`none`。

```vue
<template>
  <el-carousel height="220px" type="card" indicator-position="outside">
    <el-carousel-item v-for="i in 6" :key="i">
      <div class="slide">{{ i }}</div>
    </el-carousel-item>
  </el-carousel>
</template>
```

### 场景 3:箭头与切换回调

`arrow` 取值 `always`/`hover`/`never`;`@change` 监听切换。

```vue
<template>
  <el-carousel height="200px" arrow="hover" @change="onChange">
    <el-carousel-item v-for="i in 4" :key="i">
      <div class="slide">{{ i }}</div>
    </el-carousel-item>
  </el-carousel>
</template>

<script setup>
const onChange = (cur, prev) => {
  console.log('当前', cur, '上一个', prev)
}
</script>
```

## 参考链接

- Element Plus 官方文档 - Carousel 走马灯: https://element-plus.org/zh-CN/component/carousel
