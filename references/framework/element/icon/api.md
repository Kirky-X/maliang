# Icon API

> `<el-icon>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名   | 类型               | 默认值 | 说明                                       |
| -------- | ------------------ | ------ | ------------------------------------------ |
| `size`   | `number \| string` | —      | 图标尺寸,默认继承父级 font-size           |
| `color`  | `string`           | —      | 图标颜色,默认继承 currentColor            |

> 实际 SVG 由 `@element-plus/icons-vue` 提供的子组件渲染,`<el-icon>` 仅作容器并传递 size/color。

## 事件(Events)

`<el-icon>` 不对外抛出专用事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明                                  |
| --------- | ------------------------------------- |
| `default` | 放置具体图标组件,如 `<Edit />`       |

## 常用图标包(`@element-plus/icons-vue`)

| 图标名      | 用途          | 图标名     | 用途          |
| ----------- | ------------- | ---------- | ------------- |
| `Edit`      | 编辑          | `Delete`   | 删除          |
| `Search`    | 搜索          | `Plus`     | 新增          |
| `Check`     | 确认          | `Close`    | 关闭          |
| `User`      | 用户          | `Setting`  | 设置          |
| `Loading`   | 加载          | `ArrowUp`  | 向上          |
| `ArrowDown` | 向下          | `ArrowLeft`| 向左          |
| `ArrowRight`| 向右          | `Star`     | 收藏          |
| `Picture`   | 图片          | `Upload`   | 上传          |
| `Download`  | 下载          | `Refresh`  | 刷新          |

> 完整图标列表见 https://element-plus.org/zh-CN/component/icon.html
