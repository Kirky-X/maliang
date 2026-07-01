# Table API

> `<el-table>` 与 `<el-table-column>` 的属性 / 事件 / 方法 / 插槽定义。用法与示例见 [component.md](./component.md)。

## `<el-table>` 属性(Props)

| 属性名                   | 类型                                   | 默认值     | 说明                                                                 |
| ------------------------ | -------------------------------------- | ---------- | -------------------------------------------------------------------- |
| `data`                   | `any[]`                                | `[]`       | 表格数据(行对象数组),必填                                          |
| `height`                 | `string \| number`                     | —          | 表格固定高度,超出表头固定、表体滚动                                 |
| `max-height`             | `string \| number`                     | —          | 表格最大高度,超出滚动                                               |
| `border`                 | `boolean`                              | `false`    | 是否显示竖向边框,边框色 {color-border}                              |
| `stripe`                 | `boolean`                              | `false`    | 是否斑马纹,斑马行底色 {color-bg-secondary}                          |
| `row-key`                | `string \| ((row) => string)`          | —          | 行唯一标识,用于选择/展开/树形数据保留状态                           |
| `size`                   | `'large' \| 'default' \| 'small'`      | `'default'`| 表格尺寸,影响行高与内边距,映射 {component-size-lg/md/sm}           |
| `fit`                    | `boolean`                              | `true`     | 列宽是否自动撑满父容器                                               |
| `show-header`            | `boolean`                              | `true`     | 是否显示表头                                                         |
| `highlight-current-row`  | `boolean`                              | `false`    | 是否高亮当前行,高亮底色 {color-bg-secondary}                        |
| `current-row-key`        | `string \| number`                     | —          | 当前行 key(受控)                                                   |
| `lazy`                   | `boolean`                              | `false`    | 是否懒加载子节点(树形)                                             |
| `load`                   | `(row, resolve) => void`               | —          | 懒加载子节点回调                                                     |
| `tree-props`             | `{ hasChildren?, children?, checkStrictly? }` | —  | 树形数据结构映射                                                     |
| `default-expand-all`     | `boolean`                              | `false`    | 是否默认展开所有行(树形/展开行)                                    |
| `default-sort`           | `{ prop: string, order: 'ascending' \| 'descending' }` | — | 默认排序列与方向                                                     |
| `span-method`            | `({ row, column, rowIndex, columnIndex }) => [number, number] \| void` | — | 合并行/列方法                        |
| `row-class-name`         | `string \| (({ row, rowIndex }) => string)` | —      | 自定义行 class                                                       |
| `cell-class-name`        | `string \| (({ row, column, rowIndex, columnIndex }) => string)` | — | 自定义单元格 class           |
| `header-row-class-name`  | `string \| (({ rowIndex }) => string)` | —          | 自定义表头行 class                                                   |
| `header-cell-class-name` | `string \| (({ column, columnIndex }) => string)` | —   | 自定义表头单元格 class                                               |
| `empty-text`             | `string`                               | `'暂无数据'`| 空数据时显示文案,色 {color-text-placeholder}                        |
| `show-overflow-tooltip`  | `boolean`                              | `false`    | 内容超出是否以 tooltip 显示(全局,可被列级覆盖)                    |

## `<el-table-column>` 属性(Props)

| 属性名                | 类型                                  | 默认值     | 说明                                                         |
| --------------------- | ------------------------------------- | ---------- | ------------------------------------------------------------ |
| `type`                | `'selection' \| 'index' \| 'expand'`  | —          | 特殊列类型:多选 / 序号 / 展开行                              |
| `prop`                | `string`                              | —          | 对应行对象字段名(普通列必填)                               |
| `label`               | `string`                              | —          | 表头文案                                                     |
| `width`               | `string \| number`                    | —          | 列固定宽度                                                   |
| `min-width`           | `string \| number`                    | —          | 列最小宽度,剩余空间按比例分配                               |
| `fixed`               | `'left' \| 'right' \| boolean`        | `false`    | 固定列到左/右                                                |
| `sortable`            | `boolean \| 'custom'`                 | `false`    | 排序:`true` 前端排序,`'custom'` 后端排序(配合 sort-change) |
| `align`               | `'left' \| 'center' \| 'right'`       | `'left'`   | 单元格内容对齐                                               |
| `header-align`        | `'left' \| 'center' \| 'right'`       | —          | 表头对齐,默认同 `align`                                     |
| `formatter`           | `(row, column, cellValue, index) => any` | —       | 单元格内容格式化函数                                         |
| `show-overflow-tooltip`| `boolean`                            | `false`    | 本列内容超出是否 tooltip 显示                                |
| `resizable`           | `boolean`                             | `true`     | 列宽是否可拖拽调整                                           |
| `selectable`          | `(row, index) => boolean`             | —          | `type='selection'` 时该行是否可选                            |
| `reserve-selection`   | `boolean`                             | `false`    | 翻页/数据变化时是否保留选择(需配合 `row-key`)               |
| `index`               | `number \| ((index) => number)`       | —          | `type='index'` 时序号起始值或计算函数                        |

## `<el-table>` 事件(Events)

| 事件名              | 回调签名                                                              | 说明                         |
| ------------------- | --------------------------------------------------------------------- | ---------------------------- |
| `select`            | `(selection, row) => void`                                            | 用户勾选某行(可查切换状态)   |
| `select-all`        | `(selection) => void`                                                 | 用户勾选全选                 |
| `selection-change`  | `(selection) => void`                                                 | 选择项发生变化               |
| `cell-click`        | `(row, column, cell, event) => void`                                  | 点击单元格                   |
| `cell-dblclick`     | `(row, column, cell, event) => void`                                  | 双击单元格                   |
| `row-click`         | `(row, column, event) => void`                                        | 点击行                       |
| `row-dblclick`      | `(row, column, event) => void`                                        | 双击行                       |
| `row-contextmenu`   | `(row, column, event) => void`                                        | 右键行                       |
| `header-click`      | `(column, event) => void`                                             | 点击表头                     |
| `sort-change`       | `({ column, prop, order }) => void`                                   | 排序变化                     |
| `current-change`    | `(currentRow, oldCurrentRow) => void`                                 | 当前行变化                   |
| `expand-change`     | `(row, expandedRows) => void`                                         | 展开行变化(`type='expand'`) |
| `scroll`            | `({ scrollTop, scrollLeft }) => void`                                 | 表体滚动                     |

## `<el-table>` 方法(Methods)

通过组件 ref 调用。

| 方法名                  | 签名                                                              | 说明                                   |
| ----------------------- | ----------------------------------------------------------------- | -------------------------------------- |
| `clearSelection`        | `() => void`                                                      | 清空选择(仅 `type='selection'`)       |
| `toggleRowSelection`    | `(row, selected?: boolean) => void`                               | 切换某行选中状态                       |
| `toggleAllSelection`    | `() => void`                                                      | 切换全选                               |
| `toggleRowExpansion`    | `(row, expanded?: boolean) => void`                               | 切换展开行(`type='expand'`)           |
| `setCurrentRow`         | `(row) => void`                                                   | 设置当前行                             |
| `clearSort`             | `() => void`                                                      | 清空排序状态                           |
| `clearFilter`           | `(columnKey?) => void`                                            | 清空筛选                               |
| `doLayout`              | `() => void`                                                      | 重新布局(数据/列变化后)              |
| `sort`                  | `(prop: string, order: 'ascending' \| 'descending') => void`     | 手动触发排序                           |
| `scrollTo`              | `(options: ScrollToOptions \| number, y?: number) => void`        | 滚动到指定位置                         |
| `setScrollTop`          | `(top: number) => void`                                           | 设置垂直滚动位置                       |
| `setScrollLeft`         | `(left: number) => void`                                          | 设置水平滚动位置                       |

## 插槽(Slots)

### `<el-table>` 插槽

| 插槽名    | 说明                                              |
| --------- | ------------------------------------------------- |
| `empty`   | 自定义空数据展示                                  |
| `append`  | 表格最后一行之后追加内容(常用于"加载更多"按钮)   |

### `<el-table-column>` 插槽

| 插槽名    | 作用域参数                                      | 说明                                   |
| --------- | ----------------------------------------------- | -------------------------------------- |
| `default` | `{ row, column, $index }`                       | 自定义单元格内容                       |
| `header`  | `{ column, $index }`                            | 自定义表头内容                         |
