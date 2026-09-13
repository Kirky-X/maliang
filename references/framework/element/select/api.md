# Select API

> `<el-select>` / `<el-option>` 的属性 / 事件 / 方法 / 插槽完整定义。用法见 [component.md](./component.md)。

## el-select 属性(Props)

| 属性名             | 类型                                    | 默认值    | 说明                                     |
| ------------------ | --------------------------------------- | --------- | ---------------------------------------- |
| `model-value` / `v-model` | `string \| number \| boolean \| object \| Array` | — | 绑定值(多选时为数组) |
| `multiple`         | `boolean`                               | `false`   | 是否多选                                 |
| `disabled`         | `boolean`                               | `false`   | 是否禁用                                 |
| `size`             | `'large' \| 'default' \| 'small'`       | —         | 尺寸(默认高 32px)                     |
| `clearable`        | `boolean`                               | `false`   | 是否可清空                               |
| `collapse-tags`    | `boolean`                               | `false`   | 多选时折叠标签                           |
| `collapse-tags-tooltip` | `boolean`                          | `false`   | 悬停折叠标签展示全部                     |
| `multiple-limit`   | `number`                                | `0`       | 多选最大数量(0 不限制)                 |
| `placeholder`      | `string`                                | `'Select'`| 占位文案                                 |
| `filterable`       | `boolean`                               | `false`   | 是否可搜索                               |
| `allow-create`     | `boolean`                               | `false`   | 允许创建新条目(需 filterable)          |
| `remote`           | `boolean`                               | `false`   | 远程搜索                                 |
| `loading`          | `boolean`                               | `false`   | 远程搜索加载态                           |
| `no-data-text`     | `string`                                | `'无数据'`| 无选项文案                               |
| `popper-class`     | `string`                                | —         | 下拉面板类名                             |
| `teleported`       | `boolean`                               | `true`    | 面板是否插入 body                        |

## el-option 属性(Props)

| 属性名     | 类型                                     | 默认值 | 说明                     |
| ---------- | ---------------------------------------- | ------ | ------------------------ |
| `value`    | `string \| number \| boolean \| object`  | 必填   | 提交值(组内必须唯一)   |
| `label`    | `string \| number`                       | —      | 显示文本(默认取 value) |
| `disabled` | `boolean`                                | `false`| 是否禁用该项             |

## 事件(Events)

| 事件名         | 回调签名                                  | 说明                       |
| -------------- | ----------------------------------------- | -------------------------- |
| `change`       | `(value) => void`                         | 选中值变化时触发           |
| `visible-change` | `(visible: boolean) => void`            | 下拉面板出现/收起          |
| `remove-tag`   | `(tagValue) => void`                      | 多选移除某个标签           |
| `clear`        | `() => void`                              | 点击清空按钮               |
| `blur` / `focus` | `(event) => void`                       | 失焦 / 聚焦                |
| `search`       | `(query: string) => void`                 | filterable 键入时触发      |

## 方法 / 插槽

- `focus()` / `blur()` / `clearSelection()`(多选):实例方法。
- 插槽:`default`(选项)、`empty`(无数据)、`prefix` / `suffix`(前后缀)、`header` / `footer`(面板头尾)、`tag`(多选标签自定义)。

## 与 el-dropdown(动作菜单)的分工

| 维度 | `el-select`(本类) | `el-dropdown`(dropdown 类) |
| ---- | ------------------ | --------------------------- |
| 语义 | 数据录入:提交值到表单/筛选 | 命令触发:点击执行动作 |
| 选中态 | 有(v-model 回显) | 无 |
| 校验 | 可入 el-form rules | 无 |
| 典型 | 城市选择、分类筛选 | "更多操作"、行内命令 |

## 关键规格要点

- **尺寸**:默认高 32px,`large` 40px,`small` 24px;下拉面板项高 34px。
- **选项量级**:3-10 项常规档;>10 项开 `filterable`(对齐 vocabulary `select-searchable`);>100 项换 `el-select-v2`。
- **无障碍**:触发器为 combobox 语义(`aria-expanded` / `aria-activedescendant` 自动维护);面板项方向键导航、Enter 选中、Esc 关闭;placeholder 不能替代 label(表单内必须有 el-form-item label)。
