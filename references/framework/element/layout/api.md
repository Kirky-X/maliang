# Layout API

> `<el-row>` 与 `<el-col>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-row 属性(Props)

| 属性名     | 类型                                                              | 默认值    | 说明                                                       |
| ---------- | ----------------------------------------------------------------- | --------- | ---------------------------------------------------------- |
| `gutter`   | `number`                                                          | `0`       | 栅格间隔,单位 px。建议映射 {spacing-sm/md/lg}            |
| `justify`  | `'start' \| 'end' \| 'center' \| 'space-around' \| 'space-between' \| 'space-evenly'` | `'start'` | 水平排列方式(flex 对齐)                                  |
| `align`    | `'top' \| 'middle' \| 'bottom'`                                   | `'top'`   | 垂直排列方式                                               |
| `tag`      | `string`                                                          | `'div'`   | 自定义元素标签                                             |

## el-col 属性(Props)

| 属性名  | 类型             | 默认值 | 说明                                                                |
| ------- | ---------------- | ------ | ------------------------------------------------------------------- |
| `span`  | `number`         | `24`   | 栅格占据的列数(共 24 列)                                          |
| `offset`| `number`         | `0`    | 栅格左侧的间隔格数                                                  |
| `push`  | `number`         | `0`    | 栅格向右移动格数                                                    |
| `pull`  | `number`         | `0`    | 栅格向左移动格数                                                    |
| `xs`    | `number \| object` | —    | `<768px` 响应式栅格数或栅格属性对象                                 |
| `sm`    | `number \| object` | —    | `≥768px` 响应式栅格数或栅格属性对象                                 |
| `md`    | `number \| object` | —    | `≥992px` 响应式栅格数或栅格属性对象                                 |
| `lg`    | `number \| object` | —    | `≥1200px` 响应式栅格数或栅格属性对象                                 |
| `xl`    | `number \| object` | —    | `≥1920px` 响应式栅格数或栅格属性对象                                 |
| `tag`   | `string`         | `'div'`| 自定义元素标签                                                      |

## 事件(Events)

`<el-row>` 与 `<el-col>` 均不对外抛出专用事件。

## 方法(Methods)

无对外暴露方法。

## 插槽(Slots)

| 组件      | 插槽名    | 说明               |
| --------- | --------- | ------------------ |
| `el-row`  | `default` | 行内容,放置 el-col |
| `el-col`  | `default` | 列内容             |
