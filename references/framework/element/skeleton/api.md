# Skeleton API

> `<el-skeleton>` 与 `<el-skeleton-item>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-skeleton 属性(Props)

| 属性名       | 类型      | 默认值  | 说明                                  |
| ------------ | --------- | ------- | ------------------------------------- |
| `animated`   | `boolean` | `false` | 是否动画                              |
| `count`      | `number`  | `1`     | 渲染次数(重复模板)                |
| `rows`       | `number`  | `0`     | 占位段落行数                          |
| `loading`    | `boolean` | `true`  | 是否显示骨架(true 显示,false 显示插槽内容) |
| `default`    | —         | —       | 真实内容插槽(loading=false 时显示) |

## el-skeleton-item 属性(Props)

| 属性名     | 类型                                                                          | 默认值  | 说明          |
| ---------- | ----------------------------------------------------------------------------- | ------- | ------------- |
| `variant`  | `'text' \| 'caption' \| 'h1' \| 'h3' \| 'text' \| 'rect' \| 'circle' \| 'image'` | `'text'` | 形状变体    |

## 事件(Events)

无对外事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 组件               | 插槽名     | 说明                                  |
| ------------------ | ---------- | ------------------------------------- |
| `el-skeleton`      | `default`  | 真实内容(loading=false 显示)       |
| `el-skeleton`      | `template` | 自定义骨架模板                        |
| `el-skeleton-item` | `default`  | (一般不使用,通过 variant 控制形状) |
