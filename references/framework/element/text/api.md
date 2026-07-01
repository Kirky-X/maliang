# Typography API

> `<el-text>` 组件的属性 / 事件 / 方法 / 插槽定义。用法与示例见 [component.md](./component.md)。

> **`<el-heading>` 不存在**:Element Plus 未提供独立的标题组件。标题通过 `<el-text>` 的 `tag` 属性(渲染为 `<h1>`~`<h6>`)结合 design token 实现视觉层级,详见 component.md 场景 3。下表仅列 `<el-text>` 的真实 API。

## 属性(Props)

| 属性名      | 类型                                                       | 默认值     | 说明                                                           |
| ----------- | ---------------------------------------------------------- | ---------- | -------------------------------------------------------------- |
| `type`      | `'primary' \| 'success' \| 'warning' \| 'danger' \| 'info'` | `''`(默认) | 文本语义类型,设置文字色。映射 {color-primary}/{color-success}/… |
| `size`      | `'large' \| 'default' \| 'small'`                          | `'default'` | 文本字号。映射 {font-size-lg}/{font-size-md}/{font-size-sm}    |
| `tag`       | `string`                                                   | `'span'`   | 渲染的底层标签,可取 `h1`~`h6`、`p`、`div`、`span` 等          |
| `truncated` | `boolean`                                                  | `false`    | 单行截断:超出省略号(`overflow:hidden; text-overflow:ellipsis; white-space:nowrap`) |
| `line-clamp`| `number`                                                   | —          | 多行截断行数(配合 `-webkit-line-clamp`);留空则不截断          |

> 字号层级与字重策略遵循 references/dimensions/font.md;文字色透明度梯度遵循 references/dimensions/font.md §文字透明度梯度(主文 100% / 次文 80% / 辅助 60% …)。

## 事件(Events)

`<el-text>` 为纯展示组件,不抛出自定义事件。

## 方法(Methods)

`<el-text>` 不对外暴露方法。组件 ref 指向 `tag` 渲染出的底层元素,可通过 ref 访问原生 DOM 方法(如 `focus` 仅当 tag 为可聚焦元素时可用)。

## 插槽(Slots)

| 插槽名    | 说明             |
| --------- | ---------------- |
| `default` | 文本内容         |
