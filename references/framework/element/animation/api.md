# Animation API(过渡动画)

> 本文件列出 Element Plus 内置过渡组件及其属性。无事件/方法/插槽(过渡组件透传到 Vue `<Transition>`)。

## 过渡组件属性

所有过渡组件基于 Vue `<Transition>`,支持透传以下属性:

| 属性名          | 类型                  | 默认值 | 说明                                  |
| --------------- | --------------------- | ------ | ------------------------------------- |
| `name`          | `string`              | —      | 过渡类名前缀(部分组件已固定)        |
| `appear`        | `boolean`             | `false`| 是否在初始渲染时过渡                 |
| `mode`          | `'in-out' \| 'out-in'`| —      | 过渡模式                              |
| `duration`      | `number \| { enter, leave }` | —  | 持续时间(ms)                       |

## 内置过渡组件清单

| 组件                       | name 前缀                | 说明                       |
| -------------------------- | ------------------------ | -------------------------- |
| `el-transition`            | 自定义                   | 通用过渡                   |
| `el-fade-in`               | `el-fade-in`             | 淡入                       |
| `el-fade-in-linear`        | `el-fade-in-linear`      | 线性淡入                   |
| `el-zoom-in`               | `el-zoom-in`             | 缩放进入                   |
| `el-zoom-in-center`        | `el-zoom-in-center`      | 中心缩放进入               |
| `el-collapse-transition`   | `el-zoom-in-left`        | 折叠(高度动画)          |

## 过渡类名约定

| 类名               | 触发时机             |
| ------------------ | -------------------- |
| `.{name}-enter-from` | 进入起始           |
| `.{name}-enter-active`| 进入过程           |
| `.{name}-enter-to` | 进入结束             |
| `.{name}-leave-from` | 离开起始           |
| `.{name}-leave-active`| 离开过程           |
| `.{name}-leave-to` | 离开结束             |

## 自定义示例

```scss
.my-fade-enter-active,
.my-fade-leave-active {
  transition: opacity 0.3s ease;
}
.my-fade-enter-from,
.my-fade-leave-to {
  opacity: 0;
}
```

> 过渡组件不对外暴露事件、方法、专用插槽(默认插槽放置需过渡的元素)。
