# Accessibility(a11y)— Element Plus N/A 说明

> **Element Plus 官方文档无独立的 a11y 章节(/guide/accessibility 返回 404)。**

## 缺失原因

Element Plus 没有独立的"无障碍"指南章节。其无障碍能力分散内建在各组件实现中(如 `aria-*` 属性、`role`、键盘聚焦、`focus-trap` 等),由组件各自保证,而非通过统一文档与专用组件暴露。因此不存在独立的 a11y 组件类目。

## 内建的无障碍能力(分散于各组件)

| 能力         | 体现                                                                 |
| ------------ | -------------------------------------------------------------------- |
| 键盘操作     | Button/Menu/Dropdown/Tabs 等支持键盘导航与回车/空格触发             |
| 焦点管理     | Dialog/Drawer/MessageBox 内置 `focus-trap`,关闭后焦点归还           |
| ARIA 角色    | Tabs(`role="tab"`)、Dialog(`role="dialog"`)、Menu(`role="menu"`) 等 |
| 禁用语义     | `disabled` 组件设置 `aria-disabled`                                  |
| 文字提示     | Tooltip/Popover 通过 `aria-describedby` 关联                         |

## 替代方案

- 方案 1:直接使用 Element Plus 组件自带的 a11y 能力,无需额外组件。
- 方案 2:在业务层补充 `aria-label`、`aria-live`(动态通知)、`tabindex` 等属性,提升可访问性。
- 方案 3:配合 Vue 生态的 a11y 校验插件(如 `eslint-plugin-vuejs-accessibility`)。

## 替代实现示例(补充 aria)

```vue
<template>
  <el-button aria-label="保存当前表单" type="primary" @click="save">保存</el-button>
  <el-icon aria-hidden="true"><Star /></el-icon>
  <div role="status" aria-live="polite">{{ message }}</div>
</template>

<script setup>
import { ref } from 'vue'
import { Star } from '@element-plus/icons-vue'
const message = ref('')
const save = () => { message.value = '已保存' }
</script>
```

## 跨框架对照

| 框架        | 实现方式                                          |
| ----------- | ------------------------------------------------- |
| ArkTS       | `accessibility` 属性(text/role/description)     |
| Flutter     | `Semantics` widget                                |
| Element Plus| 无独立章节,能力内建于各组件 + 业务层 aria 补充  |

## 参考链接

- Element Plus 官方文档:无对应章节(/guide/accessibility 404)
- 相关资源:[WAI-ARIA 作者实践](https://www.w3.org/WAI/ARIA/apg/)、[Vue 无障碍](https://vuejs.org/guide/best-practices/accessibility.html)
