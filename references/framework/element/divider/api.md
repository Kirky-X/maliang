# Divider API

> `<el-divider>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名             | 类型                                              | 默认值        | 说明                              |
| ------------------ | ------------------------------------------------- | ------------- | --------------------------------- |
| `direction`        | `'horizontal' \| 'vertical'`                      | `'horizontal'`| 方向                              |
| `content-position` | `'left' \| 'center' \| 'right'`                   | `'center'`    | 文字位置(horizontal)           |
| `border-style`     | `'none' \| 'solid' \| 'double' \| 'dashed' \| 'dotted'` | `'solid'` | 边框样式                          |
| `icon`             | `string \| Component`                             | —             | 图标                              |
| `dashed`           | `boolean`                                         | `false`       | 是否虚线(2.7+,等同 border-style=dashed) |

## 事件(Events)

无对外事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明                          |
| --------- | ----------------------------- |
| `default` | 分割线文字内容                |
