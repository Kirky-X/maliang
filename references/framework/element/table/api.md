# Table API

> `<el-table>` 与 `<el-table-column>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-table 属性(Props)

| 属性名                 | 类型                              | 默认值   | 说明                              |
| ---------------------- | --------------------------------- | -------- | --------------------------------- |
| `data`                 | `array`                           | —        | 数据数组                          |
| `height`               | `string \| number`                | —        | 高度(固定表头)                 |
| `max-height`           | `string \| number`                | —        | 最大高度                          |
| `border`               | `boolean`                         | `false`  | 是否显示纵向边框                  |
| `stripe`               | `boolean`                         | `false`  | 是否斑马纹                        |
| `row-key`              | `string \| Function`              | —        | 行 key(树/保留选择时需要)      |
| `show-header`          | `boolean`                         | `true`   | 是否显示表头                      |
| `highlight-current-row`| `boolean`                         | `false`  | 是否高亮当前行                    |
| `default-sort`         | `{ prop, order }`                 | —        | 默认排序                          |
| `fit`                  | `boolean`                         | `true`   | 列宽是否自动撑满                  |
| `size`                 | `'large' \| 'default' \| 'small'` | —        | 尺寸                              |
| `lazy`                 | `boolean`                         | `false`  | 是否懒加载(树)                 |

## el-table-column 属性(Props)

| 属性名           | 类型                                                              | 默认值   | 说明                          |
| ---------------- | ----------------------------------------------------------------- | -------- | ----------------------------- |
| `type`           | `'selection' \| 'index' \| 'expand'`                              | —        | 列类型                        |
| `prop`           | `string`                                                          | —        | 字段名                        |
| `label`          | `string`                                                          | —        | 标题                          |
| `width`          | `string \| number`                                                | —        | 列宽                          |
| `min-width`      | `string \| number`                                                | —        | 最小列宽                      |
| `fixed`          | `boolean \| 'left' \| 'right'`                                    | —        | 固定列                        |
| `sortable`       | `boolean \| 'custom'`                                             | `false`  | 排序                          |
| `filters`        | `Array<{ text, value }>`                                          | —        | 筛选项                        |
| `filter-method`  | `(value, row, column) => boolean`                                 | —        | 筛选方法                      |
| `formatter`      | `(row, column, value, $index) => string`                          | —        | 格式化函数                    |
| `align`          | `'left' \| 'center' \| 'right'`                                   | `'left'` | 对齐                          |
| `show-overflow-tooltip` | `boolean`                                                  | `false`  | 溢出省略并 tooltip            |

## el-table 事件(Events,部分)

| 事件名               | 回调签名                                                | 说明                |
| -------------------- | ------------------------------------------------------- | ------------------- |
| `select`             | `(selection, row) => void`                              | 用户勾选时          |
| `select-all`         | `(selection) => void`                                   | 全选时              |
| `selection-change`   | `(selection) => void`                                   | 选择变化            |
| `sort-change`        | `({ column, prop, order }) => void`                     | 排序变化            |
| `row-click`          | `(row, column, event) => void`                          | 点击行              |
| `current-change`     | `(currentRow, oldCurrentRow) => void`                   | 当前行变化          |

## el-table 方法(Methods,部分)

| 方法名               | 签名                                       | 说明                |
| -------------------- | ------------------------------------------ | ------------------- |
| `clearSelection`     | `() => void`                               | 清空选择            |
| `toggleRowSelection` | `(row, selected?) => void`                 | 切换行选中          |
| `toggleAllSelection` | `() => void`                               | 切换全选            |
| `toggleRowExpansion` | `(row, expanded?) => void`                 | 切换展开            |
| `setCurrentRow`      | `(row?) => void`                           | 设置当前行          |
| `clearSort`          | `() => void`                               | 清空排序            |
| `clearFilter`        | `(columnKey?) => void`                     | 清空筛选            |
| `doLayout`           | `() => void`                               | 重新布局            |
| `sort`               | `(prop: string, order: string) => void`    | 手动排序            |

## el-table-column 插槽

| 插槽名     | 作用域参数                              | 说明                |
| ---------- | --------------------------------------- | ------------------- |
| `default`  | `{ row, column, $index, store }`        | 单元格内容          |
| `header`   | `{ column, $index }`                    | 表头内容            |
