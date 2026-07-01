# Card API

> `<el-card>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## 属性(Props)

| 属性名        | 类型                                      | 默认值    | 说明                              |
| ------------- | ----------------------------------------- | --------- | --------------------------------- |
| `header`      | `string`                                  | —         | 标题(也可用 #header 插槽)       |
| `body-style`  | `object`                                  | —         | 内容区自定义样式对象              |
| `body-class`  | `string`                                  | —         | 内容区自定义类名                  |
| `shadow`      | `'always' \| 'hover' \| 'never'`          | `'always'`| 阴影显示时机                      |
| `footer`      | `string`                                  | —         | 底部(也可用 #footer 插槽)       |

## 事件(Events)

`<el-card>` 不对外抛出专用事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 插槽名    | 说明           |
| --------- | -------------- |
| `default` | 卡片主体内容   |
| `header`  | 卡片头部       |
| `footer`  | 卡片底部       |
