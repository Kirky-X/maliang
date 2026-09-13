# FAB 悬浮操作按钮

> **本组件为 maliang 组合方案,Element Plus 无原生 FAB 悬浮按钮组件。** 通过固定定位(`position: fixed`)+ `<el-button>` 圆形按钮组合实现,移动端"新建/发布/写"一级操作入口(参考 Material FAB 规范)。

## 缺失原因

Element Plus 面向 Web 后台,提供 `el-backtop`(回到顶部)但无通用悬浮操作按钮;FAB 形态需组合实现。

## 替代方案(组合结构)

| 角色 | Element Plus 实现 |
| --- | --- |
| 悬浮定位 | `position: fixed`(right/bottom 定值,配 `{z-index-*}`) |
| 按钮 | `<el-button circle>` 或 `<el-float>` 自定义胶囊 |
| 图标 | `<el-icon>`(`Plus` / `Edit` 等) |
| 滚动联动 | 监听 scroll 事件驱动 `v-show` + CSS 过渡 |

## 组合结构

```css
.fab {
  position: fixed;
  right: 24px;
  bottom: 48px;
  z-index: {z-index-modal};
}
.fab-enter-active, .fab-leave-active { transition: opacity 200ms ease; }
.fab-enter-from, .fab-leave-to { opacity: 0; }
```

## 最小示例

```vue
<template>
  <div class="page">
    <main class="content">列表主体</main>
    <transition name="fab">
      <el-button
        v-show="visible"
        class="fab"
        circle
        size="large"
        aria-label="新建笔记"
        @click="create"
      >
        <el-icon :size="24"><Plus /></el-icon>
      </el-button>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
const visible = ref(true)
let lastY = 0
const onScroll = () => {
  const y = window.scrollY
  visible.value = y < lastY || y < 80 // 上滑收起、下滑显示
  lastY = y
}
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
const create = () => ElMessage.success('新建笔记')
</script>

<style scoped>
.fab {
  position: fixed;
  right: 24px;
  bottom: 48px;
  z-index: {z-index-modal};
}
.fab-enter-active, .fab-leave-active { transition: opacity 200ms ease; }
.fab-enter-from, .fab-leave-to { opacity: 0; }
</style>
```

## 使用场景

### 场景 1:扩展 FAB(带文案胶囊)

```vue
<template>
  <button class="extended-fab" aria-label="写邮件">
    <el-icon><Edit /></el-icon>
    <span>写邮件</span>
  </button>
</template>

<script setup>
import { Edit } from '@element-plus/icons-vue'
</script>

<style scoped>
.extended-fab {
  position: fixed;
  right: 24px;
  bottom: 48px;
  display: inline-flex;
  align-items: center;
  gap: {spacing-sm};
  height: 48px;
  padding: 0 {spacing-md};
  border: none;
  border-radius: {radius-full};
  background: {color-primary};
  color: {color-text-inverse};
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  cursor: pointer;
}
</style>
```

### 场景 2:有 dock/侧栏时的避让

```css
/* 有底部 dock 时上移;有侧栏时留出宽度 */
.fab { bottom: 88px; }
.page.with-sidebar .fab { right: calc(24px + 240px); }
```

## 参考链接

- Element Plus 官方文档 - Button 按钮: https://element-plus.org/zh-CN/component/button
- Element Plus 官方文档 - Backtop 回到顶部(定位参考): https://element-plus.org/zh-CN/component/backtop
- Material 3 - FAB(规范依据): https://m3.material.io/components/floating-action-button
